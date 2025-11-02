"""
Google OAuth 2.0 Authentication Manager
Handles user authentication with Google account
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE


class AuthManager:
    """Manages Google OAuth 2.0 authentication"""
    
    def __init__(self):
        self.creds = None
        
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
                    raise FileNotFoundError(
                        f"Credentials file '{CREDENTIALS_FILE}' not found. "
                        "Please download OAuth 2.0 credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
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


