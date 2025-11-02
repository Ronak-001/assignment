"""
RAG System
Implements Retrieval-Augmented Generation pipeline
"""

import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import (
    OPENAI_API_KEY, 
    EMBEDDING_MODEL, 
    LLM_MODEL, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP,
    TOP_K_RESULTS,
    VECTOR_STORE_PATH
)


class RAGSystem:
    """RAG system for document retrieval and answer generation"""
    
    def __init__(self):
        """Initialize RAG system with vector store and LLM"""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        try:
            self.embeddings = OpenAIEmbeddings(
                model=EMBEDDING_MODEL,
                openai_api_key=OPENAI_API_KEY
            )
            
            self.llm = ChatOpenAI(
                model=LLM_MODEL,
                temperature=0.7,
                openai_api_key=OPENAI_API_KEY
            )
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg or "insufficient_quota" in error_msg.lower():
                raise ValueError(
                    "OpenAI API quota exceeded. Please check your billing and quota at "
                    "https://platform.openai.com/account/billing"
                ) from e
            raise
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
        
        self.vector_store = None
        self.retriever = None
        self.qa_chain = None
    
    def create_knowledge_base(self, documents_data):
        """
        Create vector store from selected documents
        
        Args:
            documents_data: List of dicts with 'id', 'name', and 'content' keys
        """
        # Combine all document texts
        all_texts = []
        metadatas = []
        
        for doc in documents_data:
            doc_id = doc['id']
            doc_name = doc['name']
            content = doc['content']
            
            if not content.strip():
                continue
            
            # Split document into chunks using create_documents
            chunks = self.text_splitter.create_documents([content])
            
            for i, chunk in enumerate(chunks):
                all_texts.append(chunk.page_content)
                metadatas.append({
                    'document_id': doc_id,
                    'document_name': doc_name,
                    'chunk_index': i
                })
        
        if not all_texts:
            raise ValueError("No text content found in selected documents")
        
        # Create or get vector store
        if os.path.exists(VECTOR_STORE_PATH):
            # Clear existing store
            import shutil
            shutil.rmtree(VECTOR_STORE_PATH)
        
        # Create new vector store
        self.vector_store = Chroma.from_texts(
            texts=all_texts,
            metadatas=metadatas,
            embedding=self.embeddings,
            persist_directory=VECTOR_STORE_PATH
        )
        
        # Create retriever
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": TOP_K_RESULTS}
        )
        
        # Create QA chain with LangChain 1.0+ API
        prompt_template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know from the provided context.
        Use only the information from the context provided.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create the chain using the new LangChain 1.0+ pattern
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        # Store formatted docs function for later use
        self.format_docs = format_docs
        
        self.qa_chain = (
            {
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def query(self, question):
        """
        Query the RAG system
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (answer, source_documents, found_in_docs)
        """
        if not self.qa_chain:
            raise ValueError("Knowledge base not initialized. Please add documents first.")
        
        # Get relevant documents - use vector store directly for compatibility
        # In LangChain 1.0+, retrievers use invoke(), but we'll query vector store directly
        try:
            # Try to get documents from retriever using invoke (LangChain 1.0+)
            source_docs = self.retriever.invoke(question)
        except (AttributeError, TypeError, Exception):
            # Fallback: query vector store directly (most reliable)
            try:
                source_docs = self.vector_store.similarity_search(question, k=TOP_K_RESULTS)
            except Exception:
                # Last resort: try old API
                source_docs = getattr(self.retriever, 'get_relevant_documents', lambda x: [])(question)
        
        # Query the chain
        answer = self.qa_chain.invoke(question)
        
        # Check if answer was found in documents
        # If no source documents or answer indicates uncertainty, mark as not found
        found_in_docs = len(source_docs) > 0 and not any(
            phrase in answer.lower() for phrase in [
                "i don't know",
                "i do not know",
                "not provided",
                "cannot determine",
                "not found"
            ]
        )
        
        return answer, source_docs, found_in_docs
    
    def generate_fallback_answer(self, question):
        """
        Generate answer using general knowledge when not found in documents
        
        Args:
            question: User's question
            
        Returns:
            Answer string
        """
        # Use LLM directly without retrieval
        from langchain_core.messages import HumanMessage
        
        messages = [HumanMessage(content=question)]
        response = self.llm.invoke(messages)
        
        return response.content
