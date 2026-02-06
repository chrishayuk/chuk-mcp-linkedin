"""
Passthrough OAuth Provider for MCP LinkedIn Server.

This provider accepts a bearer token from the MCP client and passes it directly
to the external_token without any token exchange. Always validates the token
with LinkedIn's userinfo endpoint to extract the user_id.

Architecture:
    1. MCP client sends bearer token in Authorization header
    2. Provider validates token with LinkedIn userinfo endpoint
    3. Provider extracts user_id from LinkedIn response (stable across token refreshes)
    4. Provider passes token directly as external_access_token
    5. MCP server uses token for LinkedIn API calls

Use Cases:
    - Testing and development
    - When you already have LinkedIn tokens
    - Simple authentication without OAuth complexity
    - Single-user or multi-user scenarios with proper user isolation

"""

from typing import Any, Dict, Optional

import httpx
from chuk_mcp_server.oauth import (
    AuthorizationParams,
    AuthorizeError,
    BaseOAuthProvider,
    OAuthClientInfo,
    OAuthToken,
    RegistrationError,
    TokenError,
    TokenStore,
)


class PassthroughOAuthProvider(BaseOAuthProvider):
    """
    OAuth provider that passes bearer tokens directly to external services.

    This provider accepts a bearer token and passes it through without exchange.
    Optionally validates the token with LinkedIn's userinfo endpoint to extract
    user information using the LinkedInOAuthClient.
    """

    def __init__(
        self,
        oauth_server_url: str = "http://localhost:8000",
        sandbox_id: str = "chuk-mcp-linkedin",
        token_store: Optional[Any] = None,
        linkedin_userinfo_url: str = "https://api.linkedin.com/v2/userinfo",
    ):
        """
        Initialize Passthrough OAuth provider.

        Args:
            oauth_server_url: This MCP server's base URL
            sandbox_id: Sandbox ID for token isolation
            token_store: Token store instance (if None, creates default TokenStore)
            linkedin_userinfo_url: LinkedIn userinfo endpoint URL
        """
        self.oauth_server_url = oauth_server_url.rstrip("/")
        self.linkedin_userinfo_url = linkedin_userinfo_url

        # Use provided token store or create default one
        if token_store is not None:
            self.token_store = token_store
        else:
            self.token_store = TokenStore(sandbox_id=sandbox_id)

    # ============================================================================
    # OAuth Protected Resource Metadata
    # ============================================================================

    def get_protected_resource_metadata(self) -> Dict[str, Any]:
        """
        Return OAuth Protected Resource metadata.

        This tells MCP clients that this resource is protected but uses
        passthrough authentication.

        Returns:
            Dict with resource metadata per RFC 8414
        """
        return {
            "resource": self.oauth_server_url,
            "authorization_servers": [self.oauth_server_url],
            "scopes_supported": [
                "linkedin.posts",
                "linkedin.profile",
                "linkedin.documents",
            ],
            "passthrough_mode": True,
        }

    # ============================================================================
    # MCP OAuth Server Implementation
    # ============================================================================

    async def authorize(
        self,
        params: AuthorizationParams,
    ) -> Dict[str, Any]:
        """
        Handle authorization request from MCP client.

        In passthrough mode, this is not typically used as clients send tokens directly.
        Returns an error indicating passthrough mode usage.

        Args:
            params: Authorization parameters from MCP client

        Returns:
            Dict with error message
        """
        raise AuthorizeError(
            error="unsupported_operation",
            error_description="Passthrough mode does not use authorization flow. "
            "Send bearer token directly in Authorization header.",
        )

    async def exchange_authorization_code(
        self,
        code: str,
        client_id: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> OAuthToken:
        """
        Exchange authorization code for access token.

        Not used in passthrough mode - clients send tokens directly.

        Args:
            code: Authorization code
            client_id: MCP client ID
            redirect_uri: Redirect URI (must match)
            code_verifier: PKCE code verifier

        Returns:
            OAuth token with access_token
        """
        raise NotImplementedError(
            "Passthrough mode does not use authorization codes. "
            "Send bearer token directly in Authorization header."
        )

    async def exchange_refresh_token(
        self,
        refresh_token: str,
        client_id: str,
        scope: Optional[str] = None,
    ) -> OAuthToken:
        """
        Refresh access token using refresh token.

        Not used in passthrough mode - clients manage token refresh.

        Args:
            refresh_token: Refresh token
            client_id: MCP client ID
            scope: Optional scope

        Returns:
            New OAuth token
        """
        raise NotImplementedError(
            "Passthrough mode does not support token refresh. "
            "Obtain a new token and send it in Authorization header."
        )

    async def validate_access_token(
        self,
        token: str,
    ) -> Dict[str, Any]:
        """
        Validate bearer token and pass it through as external_access_token.

        This is the core method for passthrough integration:
        1. Validates the token with LinkedIn userinfo endpoint
        2. Extracts user_id from LinkedIn response (stable across token refreshes)
        3. Returns token data with the same token as external_access_token

        Args:
            token: Bearer token from MCP client

        Returns:
            Token data with user_id and external_access_token

        Raises:
            TokenError: If token validation fails or user_id cannot be extracted
        """
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🔍 Validating bearer token with LinkedIn in passthrough mode")

        # Get user info from LinkedIn to extract user_id
        try:
            # Call LinkedIn userinfo endpoint directly
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.linkedin_userinfo_url,
                    headers={"Authorization": f"Bearer {token}"},
                )
                response.raise_for_status()
                user_info = response.json()

            user_id = user_info.get("sub")  # LinkedIn user ID
            user_name = user_info.get("name", "Unknown")  # User's display name

            if not user_id:
                raise TokenError(
                    error="invalid_token",
                    error_description="No user ID in LinkedIn response",
                )

            logger.info(f"✓ Authenticated LinkedIn user: {user_name} (ID: {user_id})")

        except TokenError:
            # Re-raise TokenError as-is
            raise
        except httpx.HTTPError as e:
            logger.error(f"❌ Failed to get user info from LinkedIn: {e}")
            raise TokenError(
                error="invalid_token",
                error_description=f"Failed to get user info: {e}",
            )
        except Exception as e:
            logger.error(f"❌ Unexpected error getting user info: {e}")
            raise TokenError(
                error="invalid_token",
                error_description=f"Unexpected error: {e}",
            )

        # Return token data with the same token as external_access_token
        return {
            "user_id": user_id,
            "client_id": "passthrough",
            "scope": "linkedin.posts linkedin.profile",
            "external_access_token": token,  # Pass through the same token
        }

    async def register_client(
        self,
        client_metadata: Dict[str, Any],
    ) -> OAuthClientInfo:
        """
        Register a new MCP client.

        Not used in passthrough mode - no client registration needed.

        Args:
            client_metadata: Client registration metadata

        Returns:
            Client information
        """
        raise RegistrationError(
            error="unsupported_operation",
            error_description="Passthrough mode does not require client registration. "
            "Send bearer token directly in Authorization header.",
        )

    # ============================================================================
    # External OAuth Callback Handler (Not Used in Passthrough Mode)
    # ============================================================================

    async def handle_external_callback(
        self,
        code: str,
        state: str,
    ) -> Dict[str, Any]:
        """
        Handle external OAuth callback.

        Not used in passthrough mode - no OAuth flow.

        Args:
            code: Authorization code
            state: State parameter

        Returns:
            Callback result
        """
        raise NotImplementedError(
            "Passthrough mode does not use OAuth callbacks. "
            "Send bearer token directly in Authorization header."
        )


# Made with Bob
