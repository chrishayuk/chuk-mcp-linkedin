#!/usr/bin/env python3
"""
LinkedIn OAuth Token Helper

This script helps you get a LinkedIn access token through OAuth 2.0.

Usage:
    1. Set your LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in .env
    2. Run: python scripts/get_linkedin_token.py
    3. Follow the browser prompts to authorize
    4. Your access token will be saved to .env
"""

import os
import sys
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import httpx
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import config

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback"""

    auth_code = None

    def do_GET(self):
        """Handle GET request with authorization code"""
        # Parse the callback URL
        query = parse_qs(urlparse(self.path).query)

        if 'code' in query:
            OAuthCallbackHandler.auth_code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body>
                    <h1>Authorization Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            """)
        elif 'error' in query:
            error = query['error'][0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
                <html>
                <body>
                    <h1>Authorization Failed</h1>
                    <p>Error: {error}</p>
                </body>
                </html>
            """.encode())
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


def get_linkedin_token():
    """Get LinkedIn access token through OAuth flow"""

    # Check if credentials are set
    if not config.linkedin_client_id or config.linkedin_client_id == "your_client_id_here":
        print("❌ Error: LINKEDIN_CLIENT_ID not set in .env")
        print("\nPlease set your LinkedIn app credentials in .env:")
        print("  LINKEDIN_CLIENT_ID=your_actual_client_id")
        print("  LINKEDIN_CLIENT_SECRET=your_actual_client_secret")
        return None

    if not config.linkedin_client_secret or config.linkedin_client_secret == "your_client_secret_here":
        print("❌ Error: LINKEDIN_CLIENT_SECRET not set in .env")
        return None

    # OAuth settings
    redirect_uri = "http://localhost:8000/callback"
    authorization_base_url = "https://www.linkedin.com/oauth/v2/authorization"
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    # Request multiple scopes: openid for userinfo, profile for member details, w_member_social for posting
    scope = "openid profile w_member_social"

    print("LinkedIn OAuth Token Helper")
    print("=" * 60)
    print(f"Client ID: {config.linkedin_client_id[:10]}...")
    print(f"Redirect URI: {redirect_uri}")
    print(f"Scope: {scope}")
    print()

    # Step 1: Get authorization URL
    auth_params = {
        "response_type": "code",
        "client_id": config.linkedin_client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": "random_state_string_123"  # Should be random in production
    }

    auth_url = f"{authorization_base_url}?{urlencode(auth_params)}"

    print("Step 1: Opening browser for authorization...")
    print(f"Authorization URL: {auth_url[:80]}...")
    print()

    # Start local server to receive callback
    server = HTTPServer(('localhost', 8000), OAuthCallbackHandler)

    # Open browser
    webbrowser.open(auth_url)

    print("Step 2: Waiting for authorization...")
    print("Please authorize the app in your browser.")
    print()

    # Wait for one request (the callback)
    server.handle_request()

    if not OAuthCallbackHandler.auth_code:
        print("❌ No authorization code received")
        return None

    print(f"✓ Received authorization code: {OAuthCallbackHandler.auth_code[:20]}...")
    print()

    # Step 2: Exchange code for access token
    print("Step 3: Exchanging code for access token...")

    token_data = {
        "grant_type": "authorization_code",
        "code": OAuthCallbackHandler.auth_code,
        "redirect_uri": redirect_uri,
        "client_id": config.linkedin_client_id,
        "client_secret": config.linkedin_client_secret,
    }

    try:
        with httpx.Client() as client:
            response = client.post(
                token_url,
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            if response.status_code == 200:
                token_response = response.json()
                access_token = token_response.get("access_token")
                expires_in = token_response.get("expires_in", "unknown")

                print(f"✓ Access token received!")
                print(f"  Token: {access_token[:20]}...")
                print(f"  Expires in: {expires_in} seconds")
                print()

                # Get person URN
                print("Step 4: Getting your person URN...")
                person_urn = get_person_urn(access_token)

                if person_urn:
                    print(f"✓ Person URN: {person_urn}")
                    print()

                    # Save to .env
                    save_to_env(access_token, person_urn)

                    return access_token
                else:
                    print("⚠️  Could not get person URN automatically")
                    print(f"   Please add manually to .env:")
                    print(f"   LINKEDIN_PERSON_URN=urn:li:person:YOUR_ID")
                    print()
                    save_to_env(access_token, None)
                    return access_token
            else:
                print(f"❌ Token exchange failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None

    except Exception as e:
        print(f"❌ Error getting token: {e}")
        return None


def get_person_urn(access_token):
    """Get the authenticated user's person URN"""
    try:
        with httpx.Client() as client:
            response = client.get(
                "https://api.linkedin.com/v2/userinfo",
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )

            if response.status_code == 200:
                user_info = response.json()
                # The sub field contains the person URN
                sub = user_info.get("sub")
                if sub:
                    return f"urn:li:person:{sub}"

            return None
    except Exception as e:
        print(f"   Error getting person URN: {e}")
        return None


def save_to_env(access_token, person_urn=None):
    """Save credentials to .env file"""
    env_path = Path(__file__).parent.parent / ".env"

    try:
        # Read existing .env
        if env_path.exists():
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []

        # Update lines
        new_lines = []
        token_updated = False
        urn_updated = False

        for line in lines:
            if line.startswith('LINKEDIN_ACCESS_TOKEN='):
                new_lines.append(f'LINKEDIN_ACCESS_TOKEN={access_token}\n')
                token_updated = True
            elif line.startswith('LINKEDIN_PERSON_URN=') and person_urn:
                new_lines.append(f'LINKEDIN_PERSON_URN={person_urn}\n')
                urn_updated = True
            else:
                new_lines.append(line)

        # Add if not found
        if not token_updated:
            new_lines.append(f'LINKEDIN_ACCESS_TOKEN={access_token}\n')
        if person_urn and not urn_updated:
            new_lines.append(f'LINKEDIN_PERSON_URN={person_urn}\n')

        # Write back
        with open(env_path, 'w') as f:
            f.writelines(new_lines)

        print("✓ Credentials saved to .env")
        print()
        print("Next steps:")
        print("  1. Test connection: python scripts/test_connection.py")
        print("  2. Create a draft post: python examples/test_api_publish.py")
        print("  3. Enable publishing: Set ENABLE_PUBLISHING=true in .env")

    except Exception as e:
        print(f"❌ Error saving to .env: {e}")
        print(f"\nPlease manually add to .env:")
        print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
        if person_urn:
            print(f"LINKEDIN_PERSON_URN={person_urn}")


if __name__ == "__main__":
    get_linkedin_token()
