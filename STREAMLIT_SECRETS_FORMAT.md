# Streamlit Cloud Secrets Format (TOML)

When deploying to Streamlit Cloud, you need to add secrets in TOML format.

## How to Add Secrets

1. Go to your app in Streamlit Cloud
2. Click **"⋮" (three dots)** → **"Settings"**
3. Click **"Secrets"** tab
4. Paste the TOML content below
5. Replace placeholder values with your actual credentials
6. Click **"Save"**

## TOML Format Template

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"

GOOGLE_CREDENTIALS_JSON = '''
{
  "installed": {
    "client_id": "xxx.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost"]
  }
}
'''
```

## Important Notes

### 1. String Format
- Use double quotes `"` for simple strings (like OPENAI_API_KEY)
- Use triple quotes `'''` for multi-line strings (like JSON)

### 2. JSON Format Options

**Option A: Multi-line with triple quotes (Recommended - Easier to read)**
```toml
GOOGLE_CREDENTIALS_JSON = '''
{
  "installed": {
    "client_id": "xxx",
    "project_id": "xxx",
    ...
  }
}
'''
```

**Option B: Single-line (Also works)**
```toml
GOOGLE_CREDENTIALS_JSON = '{"installed":{"client_id":"xxx","project_id":"xxx","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"xxx","redirect_uris":["http://localhost"]}}'
```

### 3. Getting Your Values

**OPENAI_API_KEY:**
- Get from: https://platform.openai.com/api-keys
- Format: `sk-...`

**GOOGLE_CREDENTIALS_JSON:**
- Open your local `credentials.json` file
- Copy the entire content
- Paste it between the triple quotes `'''`

## Complete Example (Ready to Use)

Replace the values below with your actual credentials:

```toml
OPENAI_API_KEY = "sk-proj-abc123def456ghi789..."

GOOGLE_CREDENTIALS_JSON = '''
{
  "installed": {
    "client_id": "131789153362-glq2mtck208t6lqk4i7lnoh7lmrkl2i5.apps.googleusercontent.com",
    "project_id": "assi-477005",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-xxxxxxxxxxxxx",
    "redirect_uris": ["http://localhost"]
  }
}
'''
```

## Quick Copy-Paste Template

1. Copy your OpenAI API key
2. Open your local `credentials.json`
3. Copy its entire content
4. Paste into this template:

```toml
OPENAI_API_KEY = "PASTE_YOUR_OPENAI_KEY_HERE"

GOOGLE_CREDENTIALS_JSON = '''
PASTE_YOUR_CREDENTIALS_JSON_HERE
'''
```

## Verification

After saving secrets:
1. Wait a few seconds for the app to restart
2. Check if the app loads without credential errors
3. Test the authentication flow

## Troubleshooting

### ❌ "Invalid TOML format"
- Check that quotes match (use `"` not `'` for strings, or `'''` for multi-line)
- Ensure no trailing commas in JSON
- Verify JSON is valid

### ❌ "Credentials not found"
- Check that GOOGLE_CREDENTIALS_JSON is correctly formatted
- Ensure the JSON structure matches exactly
- Try single-line format if multi-line doesn't work

### ❌ "OpenAI API error"
- Verify OPENAI_API_KEY starts with `sk-`
- Check the key is valid and has credits
- Ensure no extra spaces or quotes around the key

## Security Reminder

✅ **Do:**
- Use Streamlit Cloud Secrets (secure, encrypted)
- Rotate keys regularly
- Keep secrets private

❌ **Don't:**
- Commit secrets to GitHub
- Share secrets publicly
- Use production keys in development

---

**See also:** `STREAMLIT_CLOUD_DEPLOY.md` for complete deployment guide.

