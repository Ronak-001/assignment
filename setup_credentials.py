"""
Helper script to set up credentials for local development
This script helps you convert credentials.json to environment variable format
"""

import json
import os

def credentials_to_env_var():
    """Convert credentials.json to environment variable format"""
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please download OAuth 2.0 credentials from Google Cloud Console.")
        return
    
    try:
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
        
        # Convert to JSON string (single line)
        json_string = json.dumps(credentials)
        
        print("=" * 60)
        print("GOOGLE_CREDENTIALS_JSON Environment Variable:")
        print("=" * 60)
        print(json_string)
        print("=" * 60)
        print("\n📋 Copy the above JSON string and use it as:")
        print("   GOOGLE_CREDENTIALS_JSON=<paste-here>")
        print("\n💡 For local testing, add to .env file:")
        print("   GOOGLE_CREDENTIALS_JSON=" + json_string[:50] + "...")
        print("\n💡 For deployment, add to platform environment variables")
        
        # Also save to .env.example for reference
        with open('.env.example', 'a') as f:
            f.write(f"\n# Google OAuth Credentials (JSON as single line)\n")
            f.write(f"# GOOGLE_CREDENTIALS_JSON={json_string}\n")
        
        print("\n✅ Template added to .env.example (for reference)")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def verify_setup():
    """Verify that credentials are set up correctly"""
    print("\n" + "=" * 60)
    print("Verifying Setup...")
    print("=" * 60)
    
    # Check for credentials.json
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found (for local development)")
    else:
        print("❌ credentials.json not found")
    
    # Check for environment variable
    from dotenv import load_dotenv
    load_dotenv()
    
    google_creds = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if google_creds:
        try:
            json.loads(google_creds)
            print("✅ GOOGLE_CREDENTIALS_JSON environment variable set (for deployment)")
        except json.JSONDecodeError:
            print("❌ GOOGLE_CREDENTIALS_JSON is set but invalid JSON")
    else:
        print("⚠️  GOOGLE_CREDENTIALS_JSON not set (needed for cloud deployment)")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("✅ OPENAI_API_KEY environment variable set")
    else:
        print("❌ OPENAI_API_KEY not set")
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_setup()
    else:
        credentials_to_env_var()
        verify_setup()

