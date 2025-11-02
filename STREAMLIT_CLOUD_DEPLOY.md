# Streamlit Cloud Deployment Guide

Complete guide for deploying the RAG Chatbot on Streamlit Cloud.

## Why Streamlit Cloud?

- ✅ **Native Streamlit Support** - Built specifically for Streamlit apps
- ✅ **Free Tier** - Deploy unlimited apps for free
- ✅ **Easy Deployment** - Push to GitHub, deploy in minutes
- ✅ **Automatic HTTPS** - Secure by default
- ✅ **Environment Variables** - Easy secrets management
- ✅ **Zero Configuration** - No config files needed
- ✅ **Auto-Updates** - Automatically redeploys on git push

## Prerequisites

1. **GitHub Account** - Code must be in a GitHub repository
2. **Google OAuth Credentials** - Ready from Google Cloud Console
3. **OpenAI API Key** - Have your API key ready

## Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Ensure your code is ready:**
   - All files are in the repository
   - `requirements.txt` contains all dependencies
   - `app.py` is in the root directory

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

### Step 2: Sign Up for Streamlit Cloud

1. Go to **https://streamlit.io/cloud**
2. Click **"Sign up"** or **"Get started"**
3. Sign in with your **GitHub account**
4. Authorize Streamlit Cloud to access your repositories

### Step 3: Deploy Your App

1. In Streamlit Cloud dashboard, click **"New app"**
2. **Select Repository:**
   - Choose your repository from the dropdown
   - Or click "Browse repos" if not listed
3. **Configure App:**
   - **Branch:** Select branch (usually `main` or `master`)
   - **Main file path:** `app.py`
   - **App URL:** Choose a unique subdomain (e.g., `rag-chatbot-docs`)
4. Click **"Deploy"**

### Step 4: Configure Environment Variables (Secrets)

1. In your app's page, click **"⋮" (three dots)** → **"Settings"**
2. Click **"Secrets"** tab
3. Add your secrets in this format:

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

**Important Notes:**
- Use triple quotes `'''` for multi-line JSON
- Or use single-line JSON (remove line breaks)
- Both formats work

**How to get GOOGLE_CREDENTIALS_JSON:**
1. Open your local `credentials.json` file
2. Copy the entire content
3. Paste it in the secrets (keep the `'''` quotes around it)

### Step 5: Update Google OAuth Redirect URIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services → Credentials**
3. Click on your **OAuth 2.0 Client ID**
4. Under **Authorized redirect URIs**, click **"Add URI"**
5. Add your Streamlit Cloud URL:
   ```
   https://your-app-name.streamlit.app
   ```
   (Replace `your-app-name` with your actual app name)
6. Also keep `http://localhost:8501` for local testing
7. Click **"Save"**

### Step 6: Verify Deployment

1. Wait for deployment to complete (2-5 minutes)
2. Click **"View app"** or visit your app URL
3. Test the authentication flow
4. Test document selection and chat functionality

## App URL Format

Your deployed app will be available at:
```
https://your-app-name.streamlit.app
```

## Managing Your Deployment

### Update Your App

Simply push to GitHub:
```bash
git add .
git commit -m "Update app"
git push origin main
```

Streamlit Cloud will automatically redeploy!

### View Logs

1. Go to your app in Streamlit Cloud dashboard
2. Click **"Manage app"** → **"Logs"**
3. View real-time logs and errors

### Update Secrets

1. Go to **Settings** → **Secrets**
2. Edit the secret values
3. Click **"Save"**
4. App will automatically restart

### Delete App

1. Go to **Settings**
2. Scroll to bottom
3. Click **"Delete app"**
4. Confirm deletion

## Troubleshooting

### ❌ "App failed to deploy"

**Check:**
- `app.py` is in root directory
- All dependencies in `requirements.txt`
- Check logs for specific errors

**Solution:**
- Verify `requirements.txt` has all packages
- Check Python version compatibility
- Review deployment logs

### ❌ "Module not found" error

**Solution:**
- Ensure all imports are in `requirements.txt`
- Check deployment logs for missing packages
- Add missing packages to `requirements.txt`

### ❌ "Credentials file not found"

**Solution:**
- Verify `GOOGLE_CREDENTIALS_JSON` is set in Secrets
- Check JSON format is correct
- Use triple quotes for multi-line JSON

### ❌ "Authentication failed"

**Solution:**
- Verify redirect URI is added in Google Cloud Console
- Check that redirect URI matches your Streamlit Cloud URL exactly
- Ensure OAuth consent screen is configured
- Verify credentials JSON is correct

### ❌ "OpenAI API error"

**Solution:**
- Check `OPENAI_API_KEY` is set correctly
- Verify API key is valid and has credits
- Check quota limits

## Quick Reference

### Required Files

- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ All source files (auth_manager.py, rag_system.py, etc.)

### Environment Variables (Secrets)

```toml
OPENAI_API_KEY = "sk-..."
GOOGLE_CREDENTIALS_JSON = '''{...}'''
```

### Google Cloud Console Setup

1. Enable Google Docs API
2. Enable Google Drive API
3. Create OAuth 2.0 credentials
4. Add redirect URI: `https://your-app.streamlit.app`

## Cost

- **Streamlit Cloud Free Tier:**
  - Unlimited public apps
  - Private apps available (paid)
  - No credit card required for free tier

## Security Best Practices

- ✅ Never commit credentials.json to Git
- ✅ Use Streamlit Secrets for all sensitive data
- ✅ Regularly rotate API keys
- ✅ Monitor usage and costs
- ✅ Keep dependencies updated

## Support

- **Streamlit Cloud Docs:** https://docs.streamlit.io/streamlit-cloud
- **Streamlit Community:** https://discuss.streamlit.io
- **Check Logs:** Settings → Logs in your app dashboard

---

## Summary

Deploying to Streamlit Cloud is simple:

1. ✅ Push code to GitHub
2. ✅ Connect to Streamlit Cloud
3. ✅ Set environment variables (Secrets)
4. ✅ Update Google OAuth redirect URI
5. ✅ Deploy and enjoy!

Your app will be live in minutes! 🚀
