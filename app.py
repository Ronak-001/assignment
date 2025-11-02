"""
Streamlit Web Application
Main entry point for the RAG-powered chatbot
"""

import streamlit as st
import os
from auth_manager import AuthManager
from google_docs_manager import GoogleDocsManager
from rag_system import RAGSystem
from config import CREDENTIALS_FILE


def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'credentials' not in st.session_state:
        st.session_state.credentials = None
    if 'docs_manager' not in st.session_state:
        st.session_state.docs_manager = None
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    if 'selected_docs' not in st.session_state:
        st.session_state.selected_docs = []
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'knowledge_base_created' not in st.session_state:
        st.session_state.knowledge_base_created = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def main():
    """Main application function"""
    st.set_page_config(
        page_title="RAG Chatbot with Google Docs",
        page_icon="🤖",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("🤖 RAG-Powered Chatbot with Google Docs Integration")
    st.markdown("---")
    
    # Check for credentials file
    if not os.path.exists(CREDENTIALS_FILE):
        st.error(
            f"⚠️ **Credentials file not found!**\n\n"
            f"Please download OAuth 2.0 credentials from Google Cloud Console and save as '{CREDENTIALS_FILE}'.\n\n"
            "**Steps:**\n"
            "1. Go to https://console.cloud.google.com/\n"
            "2. Create/select a project\n"
            "3. Enable Google Docs API and Google Drive API\n"
            "4. Create OAuth 2.0 credentials (Desktop app)\n"
            "5. Download and save as 'credentials.json'"
        )
        return
    
    # Authentication Section
    if not st.session_state.authenticated:
        st.header("🔐 Authentication")
        st.write("Sign in with your Google account to access your documents.")
        
        if st.button("Sign in with Google", type="primary"):
            with st.spinner("Authenticating with Google..."):
                try:
                    auth_manager = AuthManager()
                    credentials = auth_manager.authenticate()
                    st.session_state.credentials = credentials
                    st.session_state.authenticated = True
                    st.session_state.docs_manager = GoogleDocsManager(credentials)
                    st.success("✅ Successfully authenticated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Authentication failed: {str(e)}")
    else:
        # Main Application
        st.success("✅ Authenticated with Google")
        
        # Sidebar for document management
        with st.sidebar:
            st.header("📚 Document Management")
            
            # Load documents button
            if st.button("🔄 Refresh Documents List", type="primary"):
                with st.spinner("Loading your Google Docs..."):
                    try:
                        docs = st.session_state.docs_manager.list_documents()
                        st.session_state.documents = docs
                        st.success(f"Found {len(docs)} documents!")
                    except Exception as e:
                        st.error(f"Error loading documents: {str(e)}")
            
            # Display documents
            if st.session_state.documents:
                st.subheader("Your Documents")
                selected_doc_ids = []
                
                for doc in st.session_state.documents:
                    doc_id = doc['id']
                    doc_name = doc['name']
                    is_selected = st.checkbox(
                        doc_name,
                        key=f"doc_{doc_id}",
                        value=doc_id in st.session_state.selected_docs
                    )
                    if is_selected:
                        selected_doc_ids.append(doc_id)
                
                st.session_state.selected_docs = selected_doc_ids
                
                # Create knowledge base button
                if st.button("📖 Create Knowledge Base", type="primary"):
                    if not selected_doc_ids:
                        st.warning("Please select at least one document!")
                    else:
                        with st.spinner("Creating knowledge base..."):
                            try:
                                # Fetch content for selected documents
                                documents_data = []
                                for doc in st.session_state.documents:
                                    if doc['id'] in selected_doc_ids:
                                        content = st.session_state.docs_manager.get_document_content(doc['id'])
                                        documents_data.append({
                                            'id': doc['id'],
                                            'name': doc['name'],
                                            'content': content
                                        })
                                
                                # Initialize RAG system
                                rag_system = RAGSystem()
                                rag_system.create_knowledge_base(documents_data)
                                st.session_state.rag_system = rag_system
                                st.session_state.knowledge_base_created = True
                                st.success(f"✅ Knowledge base created with {len(selected_doc_ids)} document(s)!")
                                st.rerun()
                            except Exception as e:
                                error_msg = str(e)
                                if "quota" in error_msg.lower() or "429" in error_msg or "insufficient_quota" in error_msg.lower():
                                    st.error(
                                        "⚠️ **OpenAI API Quota Exceeded**\n\n"
                                        "You have exceeded your OpenAI API quota or billing is not set up.\n\n"
                                        "**Solutions:**\n"
                                        "1. Check your OpenAI account billing: https://platform.openai.com/account/billing\n"
                                        "2. Add payment method if not already added\n"
                                        "3. Verify your API usage and limits: https://platform.openai.com/usage\n"
                                        "4. Wait for quota to reset or upgrade your plan\n\n"
                                        f"**Technical Details:** {error_msg}"
                                    )
                                elif "OPENAI_API_KEY" in error_msg or "api key" in error_msg.lower():
                                    st.error(
                                        "⚠️ **OpenAI API Key Error**\n\n"
                                        "Please check your `.env` file and ensure `OPENAI_API_KEY` is set correctly."
                                    )
                                else:
                                    st.error(f"❌ **Error creating knowledge base:**\n\n{error_msg}")
                
                if st.session_state.knowledge_base_created:
                    st.info(f"📚 Knowledge base ready with {len(st.session_state.selected_docs)} document(s)")
            else:
                st.info("Click 'Refresh Documents List' to load your Google Docs")
            
            # Logout button
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.credentials = None
                st.session_state.docs_manager = None
                st.session_state.documents = []
                st.session_state.selected_docs = []
                st.session_state.rag_system = None
                st.session_state.knowledge_base_created = False
                st.session_state.chat_history = []
                st.rerun()
        
        # Main chat interface
        st.header("💬 Chat with your Documents")
        
        if not st.session_state.knowledge_base_created:
            st.info("👈 Please select documents from the sidebar and create a knowledge base to start chatting.")
        else:
            # Display chat history
            for i, (role, message) in enumerate(st.session_state.chat_history):
                with st.chat_message(role):
                    st.write(message)
                    if role == "assistant" and i < len(st.session_state.chat_history) - 1:
                        # Show if answer was from documents (will be handled in the query)
                        pass
            
            # Chat input
            user_question = st.chat_input("Ask a question about your documents...")
            
            if user_question:
                # Add user message to chat
                st.session_state.chat_history.append(("user", user_question))
                st.chat_message("user").write(user_question)
                
                # Get answer from RAG system
                with st.spinner("Thinking..."):
                    try:
                        answer, source_docs, found_in_docs = st.session_state.rag_system.query(user_question)
                        
                        # Format response with fallback handling
                        if found_in_docs:
                            response = answer
                            if source_docs:
                                response += "\n\n📄 **Sources:**\n"
                                unique_docs = {}
                                for doc in source_docs:
                                    doc_name = doc.metadata.get('document_name', 'Unknown')
                                    if doc_name not in unique_docs:
                                        unique_docs[doc_name] = True
                                for doc_name in unique_docs.keys():
                                    response += f"- {doc_name}\n"
                        else:
                            # Explicit fallback
                            response = (
                                "⚠️ **I couldn't find an answer to your question in your selected documents.**\n\n"
                                "Here's what I know from my general knowledge:\n\n"
                            )
                            fallback_answer = st.session_state.rag_system.generate_fallback_answer(user_question)
                            response += fallback_answer
                        
                        # Add assistant response to chat
                        st.session_state.chat_history.append(("assistant", response))
                        st.chat_message("assistant").write(response)
                        
                    except Exception as e:
                        error_msg = str(e)
                        if "quota" in error_msg.lower() or "429" in error_msg or "insufficient_quota" in error_msg.lower():
                            error_display = (
                                "⚠️ **OpenAI API Quota Exceeded**\n\n"
                                "Unable to process your query due to OpenAI API quota limits.\n\n"
                                "**Please:**\n"
                                "1. Check billing: https://platform.openai.com/account/billing\n"
                                "2. Add payment method if needed\n"
                                "3. Check usage limits: https://platform.openai.com/usage"
                            )
                        else:
                            error_display = f"❌ **Error:** {error_msg}"
                        
                        st.session_state.chat_history.append(("assistant", error_display))
                        st.chat_message("assistant").write(error_display)
            
            # Clear chat button
            if st.session_state.chat_history:
                if st.button("🗑️ Clear Chat History"):
                    st.session_state.chat_history = []
                    st.rerun()


if __name__ == "__main__":
    main()


