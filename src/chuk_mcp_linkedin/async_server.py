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

import os
from typing import Any, Optional

from chuk_mcp_server import ChukMCPServer

from .api import LinkedInClient
from .manager import LinkedInManager
from .manager_factory import ManagerFactory, set_factory
from .tools.composition_tools import register_composition_tools
from .tools.draft_tools import register_draft_tools
from .tools.publishing_tools import register_publishing_tools
from .tools.registry_tools import register_registry_tools
from .tools.theme_tools import register_theme_tools

# Initialize the MCP server with OAuth provider getter
mcp = ChukMCPServer("chuk-mcp-linkedin")

# Initialize manager factory (creates per-user managers)
# Use artifacts by default, configure storage backend via env vars
manager_factory = ManagerFactory(
    use_artifacts=True,
    artifact_provider=os.getenv("ARTIFACT_PROVIDER", "memory"),
)
set_factory(manager_factory)

# Legacy: Keep a single manager for backward compatibility (will be deprecated)
manager = LinkedInManager()
linkedin_client = LinkedInClient()

# Set OAuth provider getter in the protocol handler (will be populated after setup_oauth)
mcp.protocol.oauth_provider_getter = lambda: get_oauth_provider()

# Global OAuth provider (will be set if OAuth is enabled)
oauth_provider = None

# Global token store - shared across all OAuth operations
# This ensures tokens stored in one context are visible in another
# TODO: Remove when chuk-sessions ships shared_memory provider
_global_token_store = None

# Register tools with the server (tools will use factory internally)
draft_tools = register_draft_tools(mcp)
composition_tools = register_composition_tools(mcp)
theme_tools = register_theme_tools(mcp)
registry_tools = register_registry_tools(mcp)
publishing_tools = register_publishing_tools(mcp, linkedin_client)

# ============================================================================
# OAuth Integration (Optional)
# ============================================================================


def setup_preview_routes() -> None:
    """Set up preview routes for serving HTML previews."""
    from chuk_mcp_server.endpoint_registry import http_endpoint_registry
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, JSONResponse

    async def serve_preview(request: Request) -> HTMLResponse | JSONResponse:
        """Serve HTML preview for a draft using shareable preview token."""
        preview_token = request.path_params.get("preview_token")

        if not preview_token:
            return JSONResponse({"error": "preview_token required"}, status_code=400)

        # Search across all active user managers for the draft with this token
        try:
            from .manager_factory import get_factory

            factory = get_factory()
            active_users = factory.get_active_users()

            # Search through all users' managers
            for user_id in active_users:
                user_manager = factory.get_manager(user_id)
                draft = user_manager.get_draft_by_preview_token(preview_token)

                if draft:
                    # Found the draft, generate/retrieve preview
                    html_content = await user_manager.read_preview_html_async(draft.draft_id)

                    if not html_content:
                        return JSONResponse(
                            {"error": "Failed to generate preview"}, status_code=500
                        )

                    return HTMLResponse(content=html_content)

            # Token not found in any user's drafts
            return JSONResponse(
                {"error": "Preview not found. The draft may have been deleted."}, status_code=404
            )

        except Exception as e:
            return JSONResponse({"error": f"Failed to serve preview: {str(e)}"}, status_code=500)

    # Register route using the endpoint registry (called before app is created)
    http_endpoint_registry.register_endpoint(
        path="/preview/{preview_token}",
        handler=serve_preview,
        methods=["GET"],
        name="preview_draft",
        description="Preview a draft post in HTML format using shareable token",
    )


# ============================================================================
# HTTP Server Setup (Preview Routes + OAuth)
# ============================================================================


def setup_http_server() -> Optional[Any]:
    """Set up HTTP server features: preview routes and optional OAuth."""
    # Always setup preview routes for HTTP mode
    setup_preview_routes()

    # Setup OAuth if credentials are available
    return setup_oauth()


def setup_oauth() -> Optional[Any]:
    """Set up OAuth middleware if credentials are available."""
    global oauth_provider, _global_token_store

    OAUTH_ENABLED = os.getenv("OAUTH_ENABLED", "true").lower() == "true"
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

    if OAUTH_ENABLED and LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET:
        # Import generic OAuth middleware from chuk-mcp-server
        from chuk_mcp_server.oauth import OAuthMiddleware, TokenStore

        # Import LinkedIn-specific provider
        from .oauth.provider import LinkedInOAuthProvider

        # Get OAuth configuration from environment
        LINKEDIN_REDIRECT_URI = os.getenv(
            "LINKEDIN_REDIRECT_URI", "http://localhost:8000/oauth/callback"
        )
        OAUTH_SERVER_URL = os.getenv("OAUTH_SERVER_URL", "http://localhost:8000")

        # Validate credentials aren't test values
        if LINKEDIN_CLIENT_ID.startswith("test_") or LINKEDIN_CLIENT_SECRET.startswith("test_"):
            print("⚠️  WARNING: Using test LinkedIn credentials!")
            print("   OAuth flow will not work with test credentials.")
            print("   To use OAuth, obtain real credentials from:")
            print("   https://www.linkedin.com/developers/apps")

        # Create a SINGLE global token store that will be shared across all OAuth operations
        # This is a workaround for chuk-sessions memory provider creating isolated contexts
        # TODO: Remove when chuk-sessions ships shared_memory provider
        if _global_token_store is None:
            _global_token_store = TokenStore(sandbox_id="chuk-mcp-linkedin")
            print("✓ Created shared token store for OAuth")

        # Create LinkedIn OAuth provider with SHARED token store
        oauth_provider = LinkedInOAuthProvider(
            linkedin_client_id=LINKEDIN_CLIENT_ID,
            linkedin_client_secret=LINKEDIN_CLIENT_SECRET,
            linkedin_redirect_uri=LINKEDIN_REDIRECT_URI,
            oauth_server_url=OAUTH_SERVER_URL,
            token_store=_global_token_store,  # Share the instance!
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
        print(f"  Protected Resource: {OAUTH_SERVER_URL}/.well-known/oauth-protected-resource")

        return oauth_middleware
    elif OAUTH_ENABLED:
        print("⚠ OAuth disabled - LinkedIn credentials not configured")
        print("  Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET to enable OAuth")

    return None


def get_oauth_provider() -> Optional[Any]:
    """Get the global OAuth provider instance."""
    return oauth_provider


def get_token_store() -> Optional[Any]:
    """Get the global token store instance."""
    return _global_token_store


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
