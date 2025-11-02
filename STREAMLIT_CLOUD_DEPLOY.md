# Streamlit Cloud Deployment (Recommended)

Since Vercel has limited support for Streamlit apps, **Streamlit Cloud** is the recommended option for deploying this application.

## Why Streamlit Cloud?

- ✅ Native Streamlit support
- ✅ Free tier available
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS
- ✅ Environment variable management
- ✅ Zero configuration needed

## Step-by-Step Deployment

### Step 1: Push Code to GitHub

1. Create a GitHub repository (if not already created)
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

### Step 2: Sign Up for Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign up with your GitHub account
3. Authorize Streamlit Cloud to access your repositories

### Step 3: Deploy Your App

1. Click **"New app"** in Streamlit Cloud dashboard
2. Select your repository
3. Select branch (usually `main` or `master`)
4. Set main file path: `app.py`
5. Click **"Deploy"**

### Step 4: Configure Environment Variables

1. In Streamlit Cloud, go to your app's **Settings**
2. Click **"Secrets"**
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

**Important**: 
- Use triple quotes `'''` for multi-line JSON in Streamlit secrets
- Or keep it as a single line (removing line breaks)

### Step 5: Update Google OAuth Redirect URIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services → Credentials**
3. Click on your OAuth 2.0 Client ID
4. Under **Authorized redirect URIs**, add:
   - `https://your-app-name.streamlit.app`
   - Keep `http://localhost:8501` for local testing

### Step 6: Access Your App

Your app will be available at:
```
https://your-app-name.streamlit.app
```

## Troubleshooting

### App won't deploy
- Check that `app.py` is in the root directory
- Verify all dependencies are in `requirements.txt`
- Check deployment logs for errors

### Authentication not working
- Verify `GOOGLE_CREDENTIALS_JSON` is set correctly in secrets
- Check that redirect URI matches your Streamlit Cloud URL
- Ensure OAuth consent screen is configured

### Import errors
- Make sure all packages are in `requirements.txt`
- Check Python version compatibility (Streamlit Cloud uses Python 3.8+)

## Alternative: Railway Deployment

If you prefer Railway:

1. Sign up at https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. Add environment variables:
   - `OPENAI_API_KEY`
   - `GOOGLE_CREDENTIALS_JSON`
5. Set start command: `streamlit run app.py --server.port $PORT`
6. Deploy!

## Alternative: Render Deployment

1. Sign up at https://render.com
2. New Web Service → Connect GitHub
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Add environment variables
5. Deploy!

