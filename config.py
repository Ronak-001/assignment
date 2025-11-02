"""
Configuration file for the RAG chatbot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-3.5-turbo"

# RAG settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3

# Vector store
VECTOR_STORE_PATH = "./chroma_db"

# Google OAuth settings
SCOPES = ['https://www.googleapis.com/auth/documents.readonly', 
          'https://www.googleapis.com/auth/drive.metadata.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'


