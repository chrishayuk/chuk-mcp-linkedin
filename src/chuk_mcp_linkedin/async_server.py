"""
Async MCP server for LinkedIn post creation with optional OAuth support.

Provides tools for creating, managing, and optimizing LinkedIn posts using
a design system approach with components, themes, and variants.

OAuth Support:
    To enable OAuth, set these environment variables:
    - LINKEDIN_CLIENT_ID: LinkedIn app client ID
    - LINKEDIN_CLIENT_SECRET: LinkedIn app client secret
    - LINKEDIN_REDIRECT_URI: OAuth callback URL (default: http://localhost:8000/oauth/callback)
    - OAUTH_SERVER_URL: OAuth server base URL (default: http://localhost:8000)
    - OAUTH_ENABLED: Enable OAuth (default: true if credentials present)

    Note: Uses generic OAuth implementation from chuk-mcp-server.
"""

from typing import Optional, Any
from chuk_mcp_server import ChukMCPServer
from .manager import LinkedInManager
from .api import LinkedInClient
from .tools.draft_tools import register_draft_tools
from .tools.composition_tools import register_composition_tools
from .tools.theme_tools import register_theme_tools
from .tools.registry_tools import register_registry_tools
from .tools.publishing_tools import register_publishing_tools
import os

# Initialize the MCP server with OAuth provider getter
mcp = ChukMCPServer("chuk-mcp-linkedin")

# Initialize manager and client
manager = LinkedInManager()
linkedin_client = LinkedInClient()

# Set OAuth provider getter in the protocol handler (will be populated after setup_oauth)
mcp.protocol.oauth_provider_getter = lambda: get_oauth_provider()

# Global OAuth provider (will be set if OAuth is enabled)
oauth_provider = None

# Register tools with the server
draft_tools = register_draft_tools(mcp, manager)
composition_tools = register_composition_tools(mcp, manager)
theme_tools = register_theme_tools(mcp, manager)
registry_tools = register_registry_tools(mcp, manager)
publishing_tools = register_publishing_tools(mcp, manager, linkedin_client)

# ============================================================================
# OAuth Integration (Optional)
# ============================================================================


def setup_oauth() -> Optional[Any]:
    """Set up OAuth middleware if credentials are available."""
    global oauth_provider

    OAUTH_ENABLED = os.getenv("OAUTH_ENABLED", "true").lower() == "true"
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

    if OAUTH_ENABLED and LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET:
        # Import generic OAuth middleware from chuk-mcp-server
        from chuk_mcp_server.oauth import OAuthMiddleware

        # Import LinkedIn-specific provider
        from .oauth.provider import LinkedInOAuthProvider

        # Get OAuth configuration from environment
        LINKEDIN_REDIRECT_URI = os.getenv(
            "LINKEDIN_REDIRECT_URI", "http://localhost:8000/oauth/callback"
        )
        OAUTH_SERVER_URL = os.getenv("OAUTH_SERVER_URL", "http://localhost:8000")

        # Create LinkedIn OAuth provider and store globally
        oauth_provider = LinkedInOAuthProvider(
            linkedin_client_id=LINKEDIN_CLIENT_ID,
            linkedin_client_secret=LINKEDIN_CLIENT_SECRET,
            linkedin_redirect_uri=LINKEDIN_REDIRECT_URI,
            oauth_server_url=OAUTH_SERVER_URL,
        )

        # Initialize generic OAuth middleware with LinkedIn provider
        oauth_middleware = OAuthMiddleware(
            mcp_server=mcp,
            provider=oauth_provider,
            oauth_server_url=OAUTH_SERVER_URL,
            callback_path="/oauth/callback",
            scopes_supported=[
                "linkedin.posts",
                "linkedin.profile",
                "linkedin.documents",
            ],
            service_documentation="https://github.com/chrishayuk/chuk-mcp-linkedin",
            provider_name="LinkedIn",
        )

        print("✓ OAuth enabled - MCP clients can authorize with LinkedIn")
        print(f"  OAuth server: {OAUTH_SERVER_URL}")
        print(f"  Discovery: {OAUTH_SERVER_URL}/.well-known/oauth-authorization-server")

        return oauth_middleware
    elif OAUTH_ENABLED:
        print("⚠ OAuth disabled - LinkedIn credentials not configured")
        print("  Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET to enable OAuth")

    return None


def get_oauth_provider() -> Optional[Any]:
    """Get the global OAuth provider instance."""
    return oauth_provider


# Make tools available at module level for easier imports
__all__ = [
    "mcp",
    "manager",
    "linkedin_client",
    "draft_tools",
    "composition_tools",
    "theme_tools",
    "registry_tools",
    "publishing_tools",
]
