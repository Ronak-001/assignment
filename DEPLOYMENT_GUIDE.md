# Deployment Guide - Local & Cloud

This guide explains how to set up the application for both **local development** and **cloud deployment** using the same codebase.

## 🏠 Local Development Setup

### Option 1: Using credentials.json file (Recommended for Local)

1. **Download Google OAuth Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 credentials
   - Download as JSON file
   - Save as `credentials.json` in project root

2. **Set up OpenAI API Key:**
   - Create `.env` file:
     ```env
     OPENAI_API_KEY=sk-your-openai-api-key-here
     ```

3. **Run locally:**
   ```bash
   streamlit run app.py
   ```

### Option 2: Using Environment Variables (Same as Cloud)

1. **Convert credentials.json to environment variable:**
   ```bash
   python setup_credentials.py
   ```
   This will show you the JSON string to use.

2. **Create `.env` file:**
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key-here
   GOOGLE_CREDENTIALS_JSON={"installed":{"client_id":"...","project_id":"..."}}
   ```

3. **Run locally:**
   ```bash
   streamlit run app.py
   ```

### Verify Local Setup

```bash
python setup_credentials.py verify
```

This will check:
- ✅ credentials.json exists (or GOOGLE_CREDENTIALS_JSON is set)
- ✅ OPENAI_API_KEY is set
- ✅ All configurations are valid

## ☁️ Cloud Deployment Setup

### Platform: Streamlit Cloud (Recommended)

1. **Push code to GitHub**

2. **Deploy on Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Connect your GitHub repo
   - Deploy the app

3. **Add Environment Variables (Secrets):**
   - In Streamlit Cloud → Settings → Secrets
   - Add:

   ```toml
   OPENAI_API_KEY = "sk-your-openai-api-key-here"
   GOOGLE_CREDENTIALS_JSON = '''
   {
     "installed": {
       "client_id": "xxx.apps.googleusercontent.com",
       "project_id": "xxx",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
       "client_secret": "xxx",
       "redirect_uris": ["http://localhost"]
     }
   }
   '''
   ```

4. **Update Google OAuth Redirect URIs:**
   - Add your Streamlit Cloud URL: `https://your-app.streamlit.app`

### Platform: Streamlit Cloud (Recommended)

See **`STREAMLIT_CLOUD_DEPLOY.md`** for complete step-by-step guide.

### Platform: Railway

1. **Add Environment Variables:**
   - Railway Dashboard → Variables
   - Add both `OPENAI_API_KEY` and `GOOGLE_CREDENTIALS_JSON`

2. **Set Start Command:**
   ```
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

### Platform: Render

1. **Add Environment Variables:**
   - Render Dashboard → Environment
   - Add both variables

2. **Set Build & Start Commands:**
   ```
   Build: pip install -r requirements.txt
   Start: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

## 🔄 How It Works

The application automatically detects which method you're using:

1. **Priority Order:**
   - First: Checks for `credentials.json` file (local development)
   - Second: Falls back to `GOOGLE_CREDENTIALS_JSON` env var (cloud deployment)
   - Creates `credentials.json` from env var if needed

2. **Same Code Everywhere:**
   - ✅ Works locally with `credentials.json`
   - ✅ Works in cloud with `GOOGLE_CREDENTIALS_JSON` env var
   - ✅ No code changes needed between local and cloud

## 📋 Quick Reference

### Local Development
```bash
# Method 1: Use credentials.json file
# Just place credentials.json in project root

# Method 2: Use .env file
OPENAI_API_KEY=sk-...
GOOGLE_CREDENTIALS_JSON={"installed":{...}}
```

### Cloud Deployment
```bash
# Set these environment variables:
OPENAI_API_KEY=sk-...
GOOGLE_CREDENTIALS_JSON={"installed":{...}}
```

### Get GOOGLE_CREDENTIALS_JSON Value

**Option 1: Use helper script**
```bash
python setup_credentials.py
```

**Option 2: Manual**
1. Open `credentials.json`
2. Copy entire content
3. Paste as environment variable value
4. Can be single line or formatted JSON

## 🔒 Security Best Practices

1. **Never commit secrets:**
   - ✅ `credentials.json` is in `.gitignore`
   - ✅ `.env` is in `.gitignore`
   - ✅ Use environment variables in cloud

2. **Local development:**
   - Use `credentials.json` file (excluded from Git)
   - Or use `.env` file (excluded from Git)

3. **Cloud deployment:**
   - Always use platform's environment variable/secrets system
   - Never hardcode credentials in code

## 🧪 Testing Before Deployment

1. **Test locally with env vars:**
   ```bash
   # Remove credentials.json temporarily
   mv credentials.json credentials.json.backup
   
   # Set environment variable
   export GOOGLE_CREDENTIALS_JSON='{"installed":{...}}'
   
   # Run app
   streamlit run app.py
   
   # If it works, deployment should work too!
   ```

2. **Verify setup:**
   ```bash
   python setup_credentials.py verify
   ```

## ❓ Troubleshooting

### "Credentials file not found" Error
- **Local:** Make sure `credentials.json` exists OR `GOOGLE_CREDENTIALS_JSON` is in `.env`
- **Cloud:** Ensure `GOOGLE_CREDENTIALS_JSON` environment variable is set

### "Invalid JSON format" Error
- Verify JSON is valid at https://jsonlint.com
- Check for extra quotes or escape characters
- Try single-line format

### OAuth Redirect URI Mismatch
- Update Google Cloud Console OAuth settings
- Add your deployment URL to authorized redirect URIs

## 📝 Summary

- ✅ **Same code works locally and in cloud**
- ✅ **Local:** Use `credentials.json` file OR `.env` with `GOOGLE_CREDENTIALS_JSON`
- ✅ **Cloud:** Set `GOOGLE_CREDENTIALS_JSON` environment variable
- ✅ **Automatic detection:** Code chooses the right method automatically
- ✅ **Helper script:** Use `python setup_credentials.py` to convert credentials

