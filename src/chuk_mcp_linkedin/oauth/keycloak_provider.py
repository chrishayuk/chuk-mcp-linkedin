"""
Keycloak OAuth Provider for MCP LinkedIn Server.

This provider delegates OAuth to Keycloak, which manages LinkedIn as an Identity Provider.
The MCP server validates Keycloak tokens and exchanges them for LinkedIn tokens.

Architecture:
    1. MCP client requests authorization
    2. Provider returns Keycloak authorization URL
    3. User authenticates with Keycloak (which may redirect to LinkedIn)
    4. Keycloak issues token to user
    5. MCP client sends Keycloak token to MCP server
    6. MCP server validates token with Keycloak
    7. MCP server exchanges Keycloak token for LinkedIn token via broker endpoint
    8. MCP server uses LinkedIn token for API calls

OAuth Protected Resource Pattern:
    - MCP server serves /.well-known/oauth-protected-resource
    - Points to Keycloak as the authorization server
    - MCP server does NOT proxy OAuth calls - all handled by Keycloak
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


class KeycloakOAuthProvider(BaseOAuthProvider):
    """
    OAuth provider that uses Keycloak for authentication and token brokering.

    Keycloak manages LinkedIn as an Identity Provider and stores LinkedIn tokens.
    This provider validates Keycloak tokens and retrieves LinkedIn tokens via
    Keycloak's token broker endpoint.
    """

    def __init__(
        self,
        keycloak_base_url: str,
        realm_name: str,
        provider_alias: str = "linkedin",
        oauth_server_url: str = "http://localhost:8000",
        sandbox_id: str = "chuk-mcp-linkedin",
        token_store: Optional[Any] = None,
    ):
        """
        Initialize Keycloak OAuth provider.

        Args:
            keycloak_base_url: Keycloak server URL (e.g., http://localhost:8080)
            realm_name: Keycloak realm name
            provider_alias: Identity provider alias in Keycloak (default: linkedin)
            oauth_server_url: This MCP server's base URL
            sandbox_id: Sandbox ID for token isolation
            token_store: Token store instance (if None, creates default TokenStore)
        """
        self.keycloak_base_url = keycloak_base_url.rstrip("/")
        self.realm_name = realm_name
        self.provider_alias = provider_alias
        self.oauth_server_url = oauth_server_url.rstrip("/")

        # Keycloak endpoints
        self.realm_url = f"{self.keycloak_base_url}/realms/{self.realm_name}"
        self.token_broker_url = f"{self.realm_url}/broker/{self.provider_alias}/token"
        self.userinfo_url = f"{self.realm_url}/protocol/openid-connect/userinfo"
        self.auth_server_metadata_url = f"{self.realm_url}/.well-known/openid-configuration"

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

        This tells MCP clients that this resource is protected and points them
        to Keycloak as the authorization server.

        Returns:
            Dict with resource metadata per RFC 8414
        """
        return {
            "resource": self.oauth_server_url,
            "authorization_servers": [self.realm_url],
            "scopes_supported": [
                "linkedin.posts",
                "linkedin.profile",
                "linkedin.documents",
            ],
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

        Returns Keycloak authorization URL - MCP client should redirect user there.
        Keycloak handles the entire OAuth flow including LinkedIn authentication.

        Args:
            params: Authorization parameters from MCP client

        Returns:
            Dict with Keycloak authorization URL
        """
        # Validate client
        if not await self.token_store.validate_client(
            params.client_id,
            redirect_uri=params.redirect_uri,
        ):
            raise AuthorizeError(
                error="invalid_client",
                error_description="Invalid client_id or redirect_uri",
            )

        # Build Keycloak authorization URL
        # Keycloak will handle LinkedIn authentication if needed
        keycloak_auth_url = (
            f"{self.realm_url}/protocol/openid-connect/auth"
            f"?client_id={params.client_id}"
            f"&redirect_uri={params.redirect_uri}"
            f"&response_type=code"
            f"&scope=openid profile email"
        )

        if params.state:
            keycloak_auth_url += f"&state={params.state}"

        if params.code_challenge:
            keycloak_auth_url += f"&code_challenge={params.code_challenge}"
            keycloak_auth_url += f"&code_challenge_method={params.code_challenge_method or 'S256'}"

        return {
            "authorization_url": keycloak_auth_url,
            "state": params.state or "",
            "requires_external_authorization": True,
        }

    async def exchange_authorization_code(
        self,
        code: str,
        client_id: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> OAuthToken:
        """
        Exchange authorization code for access token.

        Note: In Keycloak mode, the MCP client exchanges the code directly with
        Keycloak. This method is here for compatibility but may not be used.

        Args:
            code: Authorization code from Keycloak
            client_id: MCP client ID
            redirect_uri: Redirect URI (must match)
            code_verifier: PKCE code verifier

        Returns:
            OAuth token with access_token
        """
        # In Keycloak mode, the client gets the token directly from Keycloak
        # This method validates that token and stores it
        raise NotImplementedError(
            "In Keycloak mode, clients exchange codes directly with Keycloak. "
            "Use validate_access_token with the Keycloak token."
        )

    async def exchange_refresh_token(
        self,
        refresh_token: str,
        client_id: str,
        scope: Optional[str] = None,
    ) -> OAuthToken:
        """
        Refresh access token using refresh token.

        In Keycloak mode, clients refresh tokens directly with Keycloak.

        Args:
            refresh_token: Refresh token
            client_id: MCP client ID
            scope: Optional scope

        Returns:
            New OAuth token
        """
        raise NotImplementedError(
            "In Keycloak mode, clients refresh tokens directly with Keycloak."
        )

    async def validate_access_token(
        self,
        token: str,
    ) -> Dict[str, Any]:
        """
        Validate Keycloak access token and retrieve LinkedIn token.

        This is the core method for Keycloak integration:
        1. Validates the Keycloak token by calling userinfo endpoint
        2. Exchanges Keycloak token for LinkedIn token via broker endpoint
        3. Returns token data with LinkedIn access token

        Args:
            token: Keycloak access token from MCP client

        Returns:
            Token data with user_id and LinkedIn access token
        """
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🔍 Validating Keycloak access token")

        # Step 1: Validate Keycloak token and get user info
        try:
            user_info = await self._get_keycloak_userinfo(token)
            user_id = user_info.get("sub")  # Keycloak user ID

            if not user_id:
                raise TokenError(
                    error="invalid_token",
                    error_description="Token validation failed: no user ID",
                )

            logger.info(f"✓ Keycloak token validated for user: {user_id}")

        except httpx.HTTPError as e:
            logger.error(f"❌ Keycloak token validation failed: {e}")
            raise TokenError(
                error="invalid_token",
                error_description=f"Keycloak token validation failed: {e}",
            )

        # Step 2: Exchange Keycloak token for LinkedIn token
        try:
            linkedin_token = await self._get_linkedin_token(token)
            logger.info("✓ Retrieved LinkedIn token from Keycloak broker")

        except Exception as e:
            logger.error(f"❌ Failed to get LinkedIn token: {e}")
            raise TokenError(
                error="insufficient_scope",
                error_description=f"Failed to retrieve LinkedIn token: {e}",
            )

        return {
            "user_id": user_id,
            "client_id": "keycloak",  # Keycloak manages clients
            "scope": "linkedin.posts linkedin.profile",
            "external_access_token": linkedin_token,
        }

    async def register_client(
        self,
        client_metadata: Dict[str, Any],
    ) -> OAuthClientInfo:
        """
        Register a new MCP client.

        In Keycloak mode, clients are registered in Keycloak, not here.

        Args:
            client_metadata: Client registration metadata

        Returns:
            Client information
        """
        raise RegistrationError(
            error="unsupported_operation",
            error_description="Client registration is managed by Keycloak. "
            "Register clients in Keycloak admin console.",
        )

    # ============================================================================
    # Keycloak Integration Methods
    # ============================================================================

    async def _get_keycloak_userinfo(self, access_token: str) -> Dict[str, Any]:
        """
        Get user info from Keycloak to validate token.

        Args:
            access_token: Keycloak access token

        Returns:
            User info dict with sub (user ID)

        Raises:
            httpx.HTTPError: If request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.userinfo_url,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            result: Dict[str, Any] = response.json()
            return result

    async def _get_linkedin_token(self, keycloak_token: str) -> str:
        """
        Exchange Keycloak user token for stored LinkedIn token.

        Uses Keycloak's token broker endpoint to retrieve the LinkedIn token
        that Keycloak stored when the user authenticated via LinkedIn IdP.

        Args:
            keycloak_token: User's Keycloak access token

        Returns:
            LinkedIn access token

        Raises:
            Exception: If token retrieval fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.token_broker_url,
                headers={"Authorization": f"Bearer {keycloak_token}"},
            )

            if response.status_code == 200:
                data = response.json()
                linkedin_token = data.get("access_token")
                if not linkedin_token or not isinstance(linkedin_token, str):
                    raise Exception("No access_token in Keycloak broker response")
                result_token: str = linkedin_token
                return result_token

            elif response.status_code == 400:
                raise Exception(
                    "Token not found. Ensure 'Store Tokens' is enabled in "
                    "Keycloak Identity Provider settings."
                )

            elif response.status_code in (401, 403):
                raise Exception(
                    "Permission denied. Check 'broker -> read-token' role mapping "
                    "for the user in Keycloak."
                )

            else:
                raise Exception(f"Keycloak broker error: {response.text}")

    # ============================================================================
    # External OAuth Callback Handler (Not Used in Keycloak Mode)
    # ============================================================================

    async def handle_external_callback(
        self,
        code: str,
        state: str,
    ) -> Dict[str, Any]:
        """
        Handle external OAuth callback.

        Not used in Keycloak mode - Keycloak handles all callbacks.

        Args:
            code: Authorization code
            state: State parameter

        Returns:
            Callback result
        """
        raise NotImplementedError(
            "Keycloak mode does not use external callbacks. Keycloak handles all OAuth flows."
        )


# Made with Bob
