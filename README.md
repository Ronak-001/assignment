# RAG-Powered Chatbot with Google Docs Integration

A Retrieval-Augmented Generation (RAG) chatbot that integrates with Google Docs to answer questions based on your documents.

## Features

- 🔐 **Google OAuth 2.0 Authentication**: Secure sign-in with Google account
- 📚 **Google Docs Integration**: List and select documents from your Google Drive
- 🤖 **RAG Architecture**: Advanced retrieval-augmented generation for context-aware responses
- 🔄 **Explicit Fallback**: Transparently indicates when answers aren't found in documents, then uses general knowledge
- 💬 **Interactive Chat Interface**: Clean, user-friendly Streamlit-based UI
- 📊 **Document Source Tracking**: Shows which documents were used for answers

## Mandatory Requirements

✅ Google Account Authentication (OAuth 2.0)  
✅ Python Backend  
✅ Google Docs Listing  
✅ Document Selection  
✅ RAG Pipeline  
✅ Explicit Fallback Mechanism  
✅ Chatbot Interface  

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── auth_manager.py             # Google OAuth 2.0 authentication
├── google_docs_manager.py      # Google Docs API integration
├── rag_system.py               # RAG pipeline implementation
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── credentials.json            # Google OAuth credentials (user-provided)
├── token.json                  # Saved authentication token (auto-generated)
├── chroma_db/                  # Vector store database (auto-generated)
└── README.md                   # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Google Cloud account
- OpenAI API key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Google Docs API**
   - **Google Drive API**
4. Create OAuth 2.0 Credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Application type: **Desktop app**
   - Download the JSON file
   - Save it as `credentials.json` in the project root

### 4. OpenAI API Key

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## Usage

1. **Sign In**: Click "Sign in with Google" and complete the OAuth flow
2. **Load Documents**: Click "Refresh Documents List" to see all your Google Docs
3. **Select Documents**: Check the boxes next to documents you want to include in the knowledge base
4. **Create Knowledge Base**: Click "Create Knowledge Base" to process and index selected documents
5. **Start Chatting**: Ask questions about your documents in natural language

## How It Works

### RAG Pipeline

1. **Document Loading**: Fetches content from selected Google Docs
2. **Text Chunking**: Splits documents into manageable chunks
3. **Embedding**: Converts chunks into vector embeddings using OpenAI
4. **Vector Store**: Stores embeddings in ChromaDB for efficient retrieval
5. **Retrieval**: Finds most relevant chunks based on query similarity
6. **Generation**: Uses GPT to generate answers from retrieved context

### Fallback Mechanism

If the answer cannot be found in your documents:
1. Explicitly states: "I couldn't find an answer in your selected documents"
2. Provides a response using general knowledge

## Configuration

Edit `config.py` to customize:
- Embedding model
- LLM model
- Chunk size and overlap
- Number of retrieval results

## Code Architecture

The project follows a modular structure:

- **`auth_manager.py`**: Handles OAuth 2.0 authentication flow
- **`google_docs_manager.py`**: Manages Google Docs API operations
- **`rag_system.py`**: Implements the complete RAG pipeline
- **`app.py`**: Streamlit UI and application orchestration
- **`config.py`**: Centralized configuration management

## Dependencies

- `openai`: OpenAI API for embeddings and LLM
- `langchain`: RAG framework and utilities
- `chromadb`: Vector database for embeddings
- `google-api-python-client`: Google Docs/Drive API
- `streamlit`: Web interface framework

## Important Notes

- The backend is implemented in **Python** (mandatory requirement)
- Code follows clean, modular architecture
- Proper error handling and user feedback
- Vector store persists between sessions
- OAuth token is saved for future use

## Troubleshooting

**Authentication Issues:**
- Ensure `credentials.json` is in the project root
- Check that OAuth consent screen is configured in Google Cloud Console

**API Errors:**
- Verify OpenAI API key is set in `.env`
- Check Google APIs are enabled in Cloud Console

**Import Errors:**
- Run `pip install -r requirements.txt` again
- Ensure Python version is 3.8+

## License

This project is created for educational purposes.


