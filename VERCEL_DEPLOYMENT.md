# Vercel Deployment Guide

## ⚠️ IMPORTANT: Vercel is NOT Recommended for Streamlit Apps

**Vercel is designed for serverless functions and static sites, not for Streamlit applications.**

Streamlit requires a long-running process with WebSocket support, which doesn't work well with Vercel's serverless architecture.

### ✅ Recommended Alternatives:

1. **Streamlit Cloud** (BEST for Streamlit apps)
   - Free tier
   - Native Streamlit support
   - Zero configuration
   - See: `STREAMLIT_CLOUD_DEPLOY.md`

2. **Railway** - Good Python support, easy setup
3. **Render** - Free tier, good for Streamlit
4. **Heroku** - Established platform for Python apps

---

## If You Must Use Vercel

**Note:** This requires significant modifications and may not work reliably. Consider Streamlit Cloud instead.

## Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com
2. **GitHub Repository**: Push your code to GitHub
3. **Google Cloud Console**: OAuth credentials ready
4. **OpenAI API Key**: Have your API key ready

## Step 1: Prepare Your Code

Ensure your code is pushed to a GitHub repository.

## Step 2: Set Up Vercel Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure the project settings (see below)

## Step 3: Configure Environment Variables

In your Vercel project settings, go to **Settings → Environment Variables** and add:

### Required Environment Variables:

#### 1. OPENAI_API_KEY
```
Name: OPENAI_API_KEY
Value: sk-your-openai-api-key-here
```

#### 2. GOOGLE_CREDENTIALS_JSON
```
Name: GOOGLE_CREDENTIALS_JSON
Value: (paste entire JSON content from credentials.json)
```

**How to get GOOGLE_CREDENTIALS_JSON value:**

1. Open your `credentials.json` file
2. Copy the **entire content** (including all braces and quotes)
3. Paste it as the value for `GOOGLE_CREDENTIALS_JSON`

**Example format:**
```json
{"installed":{"client_id":"xxx.apps.googleusercontent.com","project_id":"xxx","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"xxx","redirect_uris":["http://localhost"]}}
```

**Important:** 
- Remove all line breaks and format as a single line
- OR keep it as formatted JSON (both work)
- Make sure all quotes are properly escaped

## Step 4: Vercel Configuration Files

Create `vercel.json` in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**Note:** Vercel has limited support for Streamlit apps. Consider these alternatives:

### Alternative Deployment Options:

1. **Streamlit Cloud** (Recommended for Streamlit apps)
   - Free hosting
   - Native Streamlit support
   - Easy deployment
   - Visit: https://streamlit.io/cloud

2. **Railway**
   - Good for Python apps
   - Easy environment variable setup
   - Visit: https://railway.app

3. **Render**
   - Free tier available
   - Good for Streamlit apps
   - Visit: https://render.com

## Step 5: Deploy

1. Push your code to GitHub
2. Vercel will automatically detect changes and redeploy
3. Check the deployment logs for any errors

## Environment Variables Setup Summary

### For Vercel:

1. **Go to**: Project Settings → Environment Variables
2. **Add**:

| Variable Name | Value | Description |
|--------------|-------|-------------|
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key |
| `GOOGLE_CREDENTIALS_JSON` | `{"installed":{...}}` | Complete JSON from credentials.json |

### Getting GOOGLE_CREDENTIALS_JSON:

**Method 1: Copy from file**
1. Open `credentials.json`
2. Select all (Ctrl+A / Cmd+A)
3. Copy (Ctrl+C / Cmd+C)
4. Paste into Vercel environment variable

**Method 2: Using command line**
```bash
# On Mac/Linux
cat credentials.json | tr -d '\n' | pbcopy

# On Windows (PowerShell)
Get-Content credentials.json -Raw | Set-Clipboard

# Or use Python
python -c "import json; print(json.dumps(json.load(open('credentials.json'))))"
```

## Troubleshooting

### Issue: "Credentials file not found"
- **Solution**: Ensure `GOOGLE_CREDENTIALS_JSON` environment variable is set correctly
- Check that the JSON is valid (use a JSON validator)

### Issue: "Invalid JSON format"
- **Solution**: Make sure the entire JSON object is copied, including outer braces
- Verify quotes are properly escaped
- Test JSON validity at https://jsonlint.com

### Issue: Streamlit not working on Vercel
- **Solution**: Vercel has limited Python support
- Consider using Streamlit Cloud, Railway, or Render instead

### Issue: OAuth redirect URI mismatch
- **Solution**: Update Google Cloud Console OAuth credentials:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. APIs & Services → Credentials
  3. Edit your OAuth 2.0 Client ID
  4. Add authorized redirect URIs:
     - For local: `http://localhost:8501`
     - For Vercel: `https://your-app.vercel.app`
     - For Streamlit Cloud: `https://your-app.streamlit.app`

## Testing Locally with Environment Variables

Before deploying, test locally:

1. Create `.env` file:
```env
OPENAI_API_KEY=sk-your-key-here
GOOGLE_CREDENTIALS_JSON={"installed":{"client_id":"...","project_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"...","redirect_uris":["http://localhost"]}}
```

2. Run the app:
```bash
streamlit run app.py
```

## Security Notes

- ✅ Never commit `credentials.json` to Git (it's in `.gitignore`)
- ✅ Use environment variables for production
- ✅ Keep API keys secure
- ✅ Regularly rotate credentials

## Next Steps After Deployment

1. Update Google OAuth redirect URIs to include your deployment URL
2. Test authentication flow
3. Monitor usage and costs
4. Set up proper error logging

