#!/usr/bin/env python3
"""
Example: LinkedIn OAuth Flow with chuk-sessions

This script demonstrates the complete OAuth flow:
1. Start OAuth server with chuk-sessions token storage
2. Register an MCP client
3. Initiate LinkedIn OAuth flow
4. Handle LinkedIn callback
5. Exchange authorization code for access token
6. Use access token to make LinkedIn API calls

Prerequisites:
- LinkedIn Developer App created at https://www.linkedin.com/developers/
- LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET set as environment variables
- Redis running (optional, uses memory backend by default)

Usage:
    # Development (memory backend)
    export LINKEDIN_CLIENT_ID=your_client_id
    export LINKEDIN_CLIENT_SECRET=your_client_secret
    python examples/oauth_linkedin_example.py

    # Production (Redis backend)
    export SESSION_PROVIDER=redis
    export SESSION_REDIS_URL=redis://localhost:6379/0
    python examples/oauth_linkedin_example.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path so we can import chuk_mcp_linkedin
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.oauth import TokenStore, LinkedInOAuthProvider


class OAuthExample:
    """Example OAuth flow with LinkedIn"""

    def __init__(self):
        # Get LinkedIn credentials from environment
        self.linkedin_client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.linkedin_client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")

        if not self.linkedin_client_id or not self.linkedin_client_secret:
            raise ValueError(
                "Please set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET environment variables.\n"
                "Get these from: https://www.linkedin.com/developers/apps"
            )

        # OAuth server configuration
        self.oauth_server_url = "http://localhost:8000"
        self.linkedin_redirect_uri = f"{self.oauth_server_url}/oauth/linkedin/callback"

        # Initialize token store (uses memory by default, Redis if configured)
        self.token_store = TokenStore(sandbox_id="oauth-example")

        # Initialize OAuth provider
        self.provider = LinkedInOAuthProvider(
            linkedin_client_id=self.linkedin_client_id,
            linkedin_client_secret=self.linkedin_client_secret,
            linkedin_redirect_uri=self.linkedin_redirect_uri,
            oauth_server_url=self.oauth_server_url,
            token_store=self.token_store,
        )

    async def run_example(self):
        """Run the complete OAuth flow example"""

        print("=" * 80)
        print("LinkedIn OAuth Flow Example with chuk-sessions")
        print("=" * 80)
        print()

        # Check backend
        backend = os.getenv("SESSION_PROVIDER", "memory")
        redis_url = os.getenv("SESSION_REDIS_URL", "N/A")
        print(f"📦 Token Storage Backend: {backend.upper()}")
        if backend == "redis":
            print(f"🔗 Redis URL: {redis_url}")
        print()

        # Step 1: Register MCP Client
        print("Step 1: Registering MCP Client")
        print("-" * 80)

        client_info = await self.provider.register_client(
            {
                "client_name": "OAuth Example Client",
                "redirect_uris": ["http://localhost:3000/callback"],
            }
        )

        print("✅ Client registered successfully!")
        print(f"   Client ID: {client_info.client_id}")
        print(f"   Client Secret: {client_info.client_secret[:10]}...")
        print()

        # Step 2: Initiate Authorization Flow
        print("Step 2: Initiating LinkedIn Authorization")
        print("-" * 80)

        from chuk_mcp_linkedin.oauth.models import AuthorizationParams

        auth_params = AuthorizationParams(
            response_type="code",
            client_id=client_info.client_id,
            redirect_uri="http://localhost:3000/callback",
            scope="linkedin.posts",
            state="example-state-123",
        )

        auth_result = await self.provider.authorize(auth_params)

        if auth_result.get("requires_external_authorization"):
            linkedin_url = auth_result["authorization_url"]
            print("🔗 LinkedIn authorization required")
            print(f"   Authorization URL: {linkedin_url[:80]}...")
            print()
            print("📋 Manual Steps Required:")
            print("   1. Open the LinkedIn authorization URL in your browser")
            print("   2. Log in to LinkedIn and authorize the app")
            print(
                "   3. LinkedIn will redirect to: {}/oauth/linkedin/callback?code=...".format(
                    self.oauth_server_url
                )
            )
            print("   4. Copy the 'code' parameter from the redirect URL")
            print()
            print("⚠️  For this example to work automatically, you would need to:")
            print("   - Run the OAuth server (linkedin-mcp http --port 8000)")
            print("   - Set up proper redirect handling")
            print("   - Handle the callback in a web server")
            print()
            print("💡 TIP: This example demonstrates the OAuth flow structure.")
            print("   In production, the MCP server handles this automatically.")
            print()

            # Show what the flow looks like
            print("📊 Complete OAuth Flow:")
            print("   " + "─" * 76)
            print("   1. MCP Client → OAuth Server: Request authorization")
            print("   2. OAuth Server → LinkedIn: Redirect user for login")
            print("   3. User authorizes on LinkedIn")
            print("   4. LinkedIn → OAuth Server: Callback with code")
            print("   5. OAuth Server → LinkedIn: Exchange code for token")
            print("   6. OAuth Server: Store LinkedIn token in chuk-sessions")
            print("   7. OAuth Server → MCP Client: Return authorization code")
            print("   8. MCP Client → OAuth Server: Exchange code for MCP token")
            print("   9. MCP Client uses MCP token for API calls")
            print("   10. OAuth Server validates MCP token & uses LinkedIn token")
            print("   " + "─" * 76)
            print()

            # Simulate the callback (in real scenario this would come from LinkedIn)
            print("🔧 Simulating OAuth Callback (for demonstration)")
            print("-" * 80)

            # In a real scenario, you would:
            # 1. Open browser: webbrowser.open(linkedin_url)
            # 2. Wait for callback
            # 3. Extract code from callback URL

            print("⚠️  Cannot complete without actual LinkedIn authorization")
            print("   To test the full flow:")
            print()
            print("   # Terminal 1: Start OAuth server")
            print("   $ export LINKEDIN_CLIENT_ID=your_id")
            print("   $ export LINKEDIN_CLIENT_SECRET=your_secret")
            print("   $ uv run linkedin-mcp http --port 8000")
            print()
            print("   # Terminal 2: Use MCP client (e.g., Claude Desktop)")
            print("   # Configure Claude Desktop to use OAuth with this server")
            print()

            return

        # If we got here, authorization completed (mock scenario)
        print(f"✅ Authorization code received: {auth_result['code'][:20]}...")
        print()

        # Step 3: Exchange Authorization Code for Access Token
        print("Step 3: Exchanging Authorization Code for Access Token")
        print("-" * 80)

        token = await self.provider.exchange_authorization_code(
            code=auth_result["code"],
            client_id=client_info.client_id,
            redirect_uri="http://localhost:3000/callback",
        )

        print("✅ Access token received!")
        print(f"   Token Type: {token.token_type}")
        print(f"   Expires In: {token.expires_in} seconds")
        print(f"   Access Token: {token.access_token[:20]}...")
        if token.refresh_token:
            print(f"   Refresh Token: {token.refresh_token[:20]}...")
        print()

        # Step 4: Validate Access Token
        print("Step 4: Validating Access Token")
        print("-" * 80)

        token_data = await self.provider.validate_access_token(token.access_token)

        print("✅ Token validated successfully!")
        print(f"   User ID: {token_data['user_id']}")
        print(f"   Client ID: {token_data['client_id']}")
        print(f"   LinkedIn Token: {token_data.get('linkedin_access_token', 'N/A')[:20]}...")
        print()

        # Step 5: Show Token Storage
        print("Step 5: Inspecting Token Storage (chuk-sessions)")
        print("-" * 80)

        backend = os.getenv("SESSION_PROVIDER", "memory")
        print(f"📦 Backend: {backend}")
        print(f"🔑 Tokens stored with prefix: {self.token_store.sandbox_id}")
        print()
        print("Stored keys:")
        print(f"   • {self.token_store.sandbox_id}:access_token:{token.access_token[:20]}...")
        print(f"   • {self.token_store.sandbox_id}:refresh_token:{token.refresh_token[:20]}...")
        print(f"   • {self.token_store.sandbox_id}:linkedin_token:{token_data['user_id']}")
        print(f"   • {self.token_store.sandbox_id}:client:{client_info.client_id}")
        print()

        if backend == "redis":
            print("💡 You can inspect Redis directly:")
            print("   $ redis-cli")
            print(f"   > KEYS {self.token_store.sandbox_id}:*")
            print(
                f"   > GET {self.token_store.sandbox_id}:access_token:{token.access_token[:20]}..."
            )
            print()

        # Step 6: Refresh Token
        print("Step 6: Refreshing Access Token")
        print("-" * 80)

        new_token = await self.provider.exchange_refresh_token(
            refresh_token=token.refresh_token,
            client_id=client_info.client_id,
        )

        print("✅ Token refreshed successfully!")
        print(f"   New Access Token: {new_token.access_token[:20]}...")
        print(f"   New Refresh Token: {new_token.refresh_token[:20]}...")
        print("   Old tokens have been rotated (invalidated)")
        print()

        # Summary
        print("=" * 80)
        print("✅ OAuth Flow Complete!")
        print("=" * 80)
        print()
        print("Summary:")
        print(f"   • Token storage backend: {backend}")
        print(f"   • MCP client registered: {client_info.client_id}")
        print("   • Access token issued and validated")
        print("   • Token refresh successful")
        print("   • All tokens stored in chuk-sessions")
        print()
        print("Next Steps:")
        print("   1. Run the full OAuth server: uv run linkedin-mcp http --port 8000")
        print("   2. Configure MCP client (e.g., Claude Desktop) to use OAuth")
        print("   3. Test with real LinkedIn authorization")
        print("   4. For production: Switch to Redis backend (SESSION_PROVIDER=redis)")
        print()


async def main():
    """Main entry point"""
    try:
        example = OAuthExample()
        await example.run_example()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print()
        print("Setup Instructions:")
        print("1. Create LinkedIn Developer App: https://www.linkedin.com/developers/apps")
        print("2. Set environment variables:")
        print("   export LINKEDIN_CLIENT_ID=your_client_id")
        print("   export LINKEDIN_CLIENT_SECRET=your_client_secret")
        print()
        print("3. Optional - Use Redis backend:")
        print("   export SESSION_PROVIDER=redis")
        print("   export SESSION_REDIS_URL=redis://localhost:6379/0")
        print()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
