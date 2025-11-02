"""
Google OAuth 2.0 Authentication Manager
Handles user authentication with Google account
"""

import os
import json
import pickle
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE, GOOGLE_CREDENTIALS_JSON


class AuthManager:
    """Manages Google OAuth 2.0 authentication"""
    
    def __init__(self):
        self.creds = None
        self._ensure_credentials_file()
    
    def _ensure_credentials_file(self):
        """
        Create credentials.json from environment variable if it doesn't exist.
        This allows the same code to work both locally (with file) and in cloud (with env var).
        """
        # If file already exists, use it (local development)
        if os.path.exists(CREDENTIALS_FILE):
            return
        
        # If file doesn't exist but env var is set, create file from env var (cloud deployment)
        if GOOGLE_CREDENTIALS_JSON:
            try:
                # Parse the JSON string from environment variable
                credentials_data = json.loads(GOOGLE_CREDENTIALS_JSON)
                # Write to file (will be created at runtime)
                with open(CREDENTIALS_FILE, 'w') as f:
                    json.dump(credentials_data, f, indent=2)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid GOOGLE_CREDENTIALS_JSON format. "
                    f"Please ensure it's valid JSON: {str(e)}"
                )
        
    def authenticate(self):
        """
        Authenticate user with Google account
        Returns credentials object
        """
        # Check if token exists (user previously authenticated)
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired credentials
                self.creds.refresh(Request())
            else:
                # Get new credentials
                if not os.path.exists(CREDENTIALS_FILE):
                    if not GOOGLE_CREDENTIALS_JSON:
                        raise FileNotFoundError(
                            f"Credentials file '{CREDENTIALS_FILE}' not found and "
                            "GOOGLE_CREDENTIALS_JSON environment variable not set. "
                            "Please either:\n"
                            "1. Download OAuth 2.0 credentials from Google Cloud Console and save as credentials.json, OR\n"
                            "2. Set GOOGLE_CREDENTIALS_JSON environment variable with the JSON content."
                        )
                    # Try to create from env var (already done in __init__, but ensure it exists)
                    self._ensure_credentials_file()
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                
                # Detect cloud environment - no browser available
                # Check for common cloud environment indicators
                is_cloud = (
                    os.getenv('STREAMLIT_SERVER_PORT') is not None or
                    os.getenv('STREAMLIT_SHARING_MODE') is not None or
                    'streamlit.app' in os.getenv('SERVER_NAME', '') or
                    not os.getenv('DISPLAY')  # No display available
                )
                
                if is_cloud:
                    # Cloud environment - return flow for manual authorization
                    raise RuntimeError("CLOUD_ENV_DETECTED")
                else:
                    # Local environment - try browser
                    try:
                        self.creds = flow.run_local_server(port=0, open_browser=True)
                    except Exception as e:
                        # Browser failed - fall back to manual flow
                        if "browser" in str(e).lower() or "runnable" in str(e).lower():
                            raise RuntimeError("CLOUD_ENV_DETECTED")
                        else:
                            raise
            
            # Save credentials for future use
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)
        
        return self.creds
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)
                return self.creds and self.creds.valid
        return False


