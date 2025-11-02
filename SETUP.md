# Setup Guide

## Quick Start

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get Google OAuth Credentials

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable APIs:
   - Navigate to "APIs & Services" → "Library"
   - Search and enable "Google Docs API"
   - Search and enable "Google Drive API"
4. Create OAuth 2.0 Credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     - User Type: External
     - Add your email as test user
   - Application type: **Desktop app**
   - Name: "RAG Chatbot" (or any name)
   - Click "Create"
   - Download the JSON file
   - Rename it to `credentials.json` and place in project root

### Step 3: Set Up OpenAI API Key

1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create `.env` file in project root:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

### Step 4: Run the Application

```bash
streamlit run app.py
```

A browser window will open automatically. If not, navigate to `http://localhost:8501`

### Step 5: First Time Authentication

1. Click "Sign in with Google"
2. A browser window will open for Google authentication
3. Select your Google account
4. Grant permissions (read access to Google Docs)
5. You'll be redirected back to the app

## Troubleshooting

### "Credentials file not found" error
- Ensure `credentials.json` is in the project root directory
- Check filename is exactly `credentials.json` (not `credentials.json.json`)

### "OPENAI_API_KEY not found" error
- Create `.env` file in project root
- Add: `OPENAI_API_KEY=your-key-here`
- Restart the application

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Google API errors
- Verify APIs are enabled in Google Cloud Console
- Check OAuth consent screen is configured
- Ensure test user email is added (if in testing mode)

### Port already in use
- Streamlit defaults to port 8501
- Change port: `streamlit run app.py --server.port 8502`

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── auth_manager.py             # Google OAuth authentication
├── google_docs_manager.py      # Google Docs API operations
├── rag_system.py               # RAG pipeline implementation
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── credentials.json            # Google OAuth (you need to add this)
├── .env                        # Environment variables (you need to add this)
└── README.md                   # Documentation
```

## Testing

1. After authentication, click "Refresh Documents List"
2. Select one or more documents
3. Click "Create Knowledge Base"
4. Wait for processing to complete
5. Start asking questions in the chat interface

## Notes

- The first authentication creates `token.json` for future sessions
- Vector store is saved in `chroma_db/` directory
- Selected documents persist in session state
- Chat history is maintained during the session

