#!/usr/bin/env python3
"""
Setup script for YouTube Tech Video Agent
Handles initial configuration and YouTube API authentication
"""

import os
import json
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config import Config
from logger import get_logger

logger = get_logger(__name__)

class YouTubeSetup:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self):
        self.credentials_file = "youtube_credentials.json"
        
    def authenticate_youtube(self) -> dict:
        """Authenticate with YouTube API and return credentials"""
        logger.info("Starting YouTube API authentication...")
        
        flow = InstalledAppFlow.from_client_config(
            {
                "web": {
                    "client_id": Config.YOUTUBE_CLIENT_ID,
                    "client_secret": Config.YOUTUBE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost:8080"]
                }
            },
            self.SCOPES
        )
        
        logger.info("Opening browser for authentication...")
        credentials = flow.run_local_server(port=8080)
        
        # Convert credentials to dict for storage
        creds_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        logger.info("Authentication successful!")
        return creds_dict
    
    def save_credentials(self, credentials: dict):
        """Save credentials to file"""
        with open(self.credentials_file, 'w') as f:
            json.dump(credentials, f, indent=2)
        logger.info(f"Credentials saved to {self.credentials_file}")
    
    def load_credentials(self) -> Optional[dict]:
        """Load credentials from file"""
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                return json.load(f)
        return None
    
    def test_authentication(self, credentials: dict) -> bool:
        """Test if credentials work"""
        try:
            # Create credentials object
            creds = Credentials(
                credentials['token'],
                refresh_token=credentials['refresh_token'],
                token_uri=credentials['token_uri'],
                client_id=credentials['client_id'],
                client_secret=credentials['client_secret'],
                scopes=credentials['scopes']
            )
            
            # Test by refreshing token
            if creds.expired:
                creds.refresh(Request())
            
            logger.info("Authentication test successful!")
            return True
            
        except Exception as e:
            logger.error(f"Authentication test failed: {e}")
            return False
    
    def setup_environment_file(self):
        """Create .env file from .env.example"""
        env_example = ".env.example"
        env_file = ".env"
        
        if os.path.exists(env_file):
            logger.info(f"{env_file} already exists")
            return
        
        if not os.path.exists(env_example):
            logger.error(f"{env_example} not found")
            return
        
        # Read example file
        with open(env_example, 'r') as f:
            content = f.read()
        
        # Write to .env file
        with open(env_file, 'w') as f:
            f.write(content)
        
        logger.info(f"Created {env_file} from {env_example}")
        logger.info("Please edit .env file with your API keys and configuration")

def main():
    """Main setup process"""
    setup = YouTubeSetup()
    
    print("=== YouTube Tech Video Agent Setup ===\n")
    
    # Step 1: Create .env file
    print("Step 1: Creating environment configuration file...")
    setup.setup_environment_file()
    
    print("\nStep 2: YouTube API Authentication")
    print("Please make sure you have:")
    print("1. Google Cloud Console project with YouTube Data API v3 enabled")
    print("2. OAuth 2.0 credentials (Client ID and Client Secret)")
    print("3. Added these to your .env file")
    
    input("\nPress Enter when ready to authenticate...")
    
    try:
        # Authenticate with YouTube
        credentials = setup.authenticate_youtube()
        
        # Test authentication
        print("\nTesting authentication...")
        if setup.test_authentication(credentials):
            print("✅ Authentication successful!")
            
            # Save credentials
            setup.save_credentials(credentials)
            
            print("\n=== Setup Complete! ===")
            print("You can now run the agent with:")
            print("  python main.py --mode once      # Run once")
            print("  python main.py --mode automated # Run with scheduling")
            print("  python main.py --status         # Check status")
            
        else:
            print("❌ Authentication test failed")
            
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print(f"❌ Setup failed: {e}")

if __name__ == "__main__":
    main()