# src/chuk_mcp_linkedin/oauth/provider.py
"""
OAuth Authorization Server Provider for MCP clients.

Implements the MCP OAuth specification to authenticate MCP clients
and link them to LinkedIn accounts.

Pure chuk-mcp-server implementation without mcp library dependencies.

Architecture:
    1. MCP client requests authorization
    2. Provider initiates LinkedIn OAuth flow
    3. User authorizes with LinkedIn
    4. Provider links MCP user to LinkedIn account
    5. Provider issues MCP access token
    6. MCP client uses access token for requests
    7. Provider validates token and uses LinkedIn token for API calls
"""

from typing import Optional, Dict, Any
from chuk_mcp_server.oauth import (
    BaseOAuthProvider,
    AuthorizationParams,
    OAuthToken,
    OAuthClientInfo,
    AuthorizeError,
    TokenError,
    RegistrationError,
    TokenStore,
)
from .linkedin_client import LinkedInOAuthClient


class LinkedInOAuthProvider(BaseOAuthProvider):
    """
    OAuth Authorization Server for MCP clients with LinkedIn integration.

    Pure chuk-mcp-server implementation.

    This provider:
    - Authenticates MCP clients
    - Links MCP users to LinkedIn accounts
    - Manages token lifecycle for both layers
    - Auto-refreshes LinkedIn tokens
    """

    def __init__(
        self,
        linkedin_client_id: str,
        linkedin_client_secret: str,
        linkedin_redirect_uri: str,
        oauth_server_url: str = "http://localhost:8000",
        sandbox_id: str = "chuk-mcp-linkedin",
        token_store: Optional[Any] = None,
    ):
        """
        Initialize OAuth provider.

        Args:
            linkedin_client_id: LinkedIn app client ID
            linkedin_client_secret: LinkedIn app client secret
            linkedin_redirect_uri: LinkedIn OAuth callback URL
            oauth_server_url: This OAuth server's base URL
            sandbox_id: Sandbox ID for chuk-sessions isolation
            token_store: Token store instance (if None, creates default TokenStore)
        """
        self.oauth_server_url = oauth_server_url

        # Use provided token store or create default one
        if token_store is not None:
            self.token_store = token_store
        else:
            self.token_store = TokenStore(sandbox_id=sandbox_id)

        self.linkedin_client = LinkedInOAuthClient(
            client_id=linkedin_client_id,
            client_secret=linkedin_client_secret,
            redirect_uri=linkedin_redirect_uri,
        )

        # Track ongoing authorization flows
        self._pending_authorizations: Dict[str, Dict[str, Any]] = {}

    # ============================================================================
    # MCP OAuth Server Implementation
    # ============================================================================

    async def authorize(
        self,
        params: AuthorizationParams,
    ) -> Dict[str, Any]:
        """
        Handle authorization request from MCP client.

        If user doesn't have LinkedIn token, initiates LinkedIn OAuth flow.
        Otherwise, returns authorization code directly.

        Args:
            params: Authorization parameters from MCP client

        Returns:
            Dict with authorization_code or redirect information
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

        # Generate state for this authorization flow
        state = params.state or ""

        # Check if we have a LinkedIn token for this state
        # (State could encode user_id if we already know it)
        user_id = self._pending_authorizations.get(state, {}).get("user_id")

        if user_id:
            # User already linked to LinkedIn
            linkedin_token = await self.token_store.get_linkedin_token(user_id)

            if linkedin_token and not await self.token_store.is_linkedin_token_expired(user_id):
                # Have valid LinkedIn token, create authorization code
                code = await self.token_store.create_authorization_code(
                    user_id=user_id,
                    client_id=params.client_id,
                    redirect_uri=params.redirect_uri,
                    scope=params.scope,
                    code_challenge=params.code_challenge,
                    code_challenge_method=params.code_challenge_method,
                )

                # Clean up pending authorization
                if state in self._pending_authorizations:
                    del self._pending_authorizations[state]

                return {
                    "code": code,
                    "state": state,
                }

        # Need LinkedIn authorization - redirect to LinkedIn
        # Store pending authorization details
        import secrets

        linkedin_state = secrets.token_urlsafe(32)
        self._pending_authorizations[linkedin_state] = {
            "mcp_client_id": params.client_id,
            "mcp_redirect_uri": params.redirect_uri,
            "mcp_state": state,
            "mcp_scope": params.scope,
            "mcp_code_challenge": params.code_challenge,
            "mcp_code_challenge_method": params.code_challenge_method,
        }

        linkedin_auth_url = self.linkedin_client.get_authorization_url(state=linkedin_state)

        # Debug logging
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"🔗 Generated LinkedIn authorization URL: {linkedin_auth_url}")
        logger.info(f"🔗 LinkedIn redirect_uri configured as: {self.linkedin_client.redirect_uri}")

        # Return LinkedIn authorization URL
        # MCP client should redirect user to this URL
        return {
            "authorization_url": linkedin_auth_url,
            "state": linkedin_state,
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

        Args:
            code: Authorization code
            client_id: MCP client ID
            redirect_uri: Redirect URI (must match)
            code_verifier: PKCE code verifier

        Returns:
            OAuth token with access_token and refresh_token
        """
        # Validate authorization code
        code_data = await self.token_store.validate_authorization_code(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        )

        if not code_data:
            raise TokenError(
                error="invalid_grant",
                error_description="Invalid or expired authorization code",
            )

        # Create access token and refresh token
        access_token, refresh_token = await self.token_store.create_access_token(
            user_id=code_data["user_id"],
            client_id=client_id,
            scope=code_data["scope"],
        )

        return OAuthToken(
            access_token=access_token,
            token_type="Bearer",
            expires_in=3600,  # 1 hour
            refresh_token=refresh_token,
            scope=code_data["scope"],
        )

    async def exchange_refresh_token(
        self,
        refresh_token: str,
        client_id: str,
        scope: Optional[str] = None,
    ) -> OAuthToken:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Refresh token
            client_id: MCP client ID
            scope: Optional scope (must be subset of original)

        Returns:
            New OAuth token
        """
        result = await self.token_store.refresh_access_token(refresh_token)

        if not result:
            raise TokenError(
                error="invalid_grant",
                error_description="Invalid refresh token",
            )

        new_access_token, new_refresh_token = result

        return OAuthToken(
            access_token=new_access_token,
            token_type="Bearer",
            expires_in=3600,
            refresh_token=new_refresh_token,
            scope=scope,
        )

    async def validate_access_token(
        self,
        token: str,
    ) -> Dict[str, Any]:
        """
        Validate and load access token.

        Also checks LinkedIn token and refreshes if needed.

        Args:
            token: MCP access token

        Returns:
            Token data with user_id and LinkedIn token
        """
        # Validate MCP token
        token_data = await self.token_store.validate_access_token(token)
        if not token_data:
            raise TokenError(
                error="invalid_token",
                error_description="Invalid or expired access token",
            )

        user_id = token_data["user_id"]

        # Get LinkedIn token
        linkedin_token_data = await self.token_store.get_linkedin_token(user_id)
        if not linkedin_token_data:
            raise TokenError(
                error="insufficient_scope",
                error_description="LinkedIn account not linked",
            )

        # Check if LinkedIn token needs refresh
        if await self.token_store.is_linkedin_token_expired(user_id):
            # Refresh LinkedIn token
            refresh_token = linkedin_token_data.get("refresh_token")
            if refresh_token:
                try:
                    new_token = await self.linkedin_client.refresh_access_token(refresh_token)
                    await self.token_store.update_linkedin_token(
                        user_id=user_id,
                        access_token=new_token["access_token"],
                        refresh_token=new_token.get("refresh_token", refresh_token),
                        expires_in=new_token.get("expires_in", 5184000),
                    )
                    linkedin_token_data = await self.token_store.get_linkedin_token(user_id)
                except Exception as e:
                    raise TokenError(
                        error="invalid_token",
                        error_description=f"Failed to refresh LinkedIn token: {e}",
                    )
            else:
                raise TokenError(
                    error="invalid_token",
                    error_description="LinkedIn token expired and no refresh token available",
                )

        return {
            **token_data,
            "linkedin_access_token": linkedin_token_data["access_token"],
        }

    async def register_client(
        self,
        client_metadata: Dict[str, Any],
    ) -> OAuthClientInfo:
        """
        Register a new MCP client.

        Args:
            client_metadata: Client registration metadata

        Returns:
            Client information with credentials
        """
        client_name = client_metadata.get("client_name", "Unknown Client")
        redirect_uris = client_metadata.get("redirect_uris", [])

        if not redirect_uris:
            raise RegistrationError(
                error="invalid_redirect_uri",
                error_description="At least one redirect URI required",
            )

        credentials = await self.token_store.register_client(
            client_name=client_name,
            redirect_uris=redirect_uris,
        )

        return OAuthClientInfo(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            client_name=client_name,
            redirect_uris=redirect_uris,
        )

    # ============================================================================
    # External OAuth Callback Handler
    # ============================================================================

    async def handle_external_callback(
        self,
        code: str,
        state: str,
    ) -> Dict[str, Any]:
        """
        Handle LinkedIn OAuth callback.

        This completes the LinkedIn OAuth flow and creates MCP authorization code.
        Generic interface method for chuk-mcp-server OAuth middleware.

        Args:
            code: LinkedIn authorization code
            state: State parameter (links to pending authorization)

        Returns:
            Dict with MCP authorization code and redirect info
        """
        # Get pending authorization
        pending = self._pending_authorizations.get(state)
        if not pending:
            raise ValueError("Invalid or expired state parameter")

        # Exchange LinkedIn code for token
        try:
            linkedin_token = await self.linkedin_client.exchange_code_for_token(code)
        except Exception as e:
            raise ValueError(f"LinkedIn token exchange failed: {e}")

        # Get LinkedIn user info to use as user_id
        try:
            user_info = await self.linkedin_client.get_user_info(linkedin_token["access_token"])
            user_id = user_info["sub"]  # LinkedIn user ID
        except Exception as e:
            raise ValueError(f"Failed to get LinkedIn user info: {e}")

        # Store LinkedIn token
        await self.token_store.link_linkedin_token(
            user_id=user_id,
            access_token=linkedin_token["access_token"],
            refresh_token=linkedin_token.get("refresh_token"),
            expires_in=linkedin_token.get("expires_in", 5184000),
        )

        # Create MCP authorization code
        mcp_code = await self.token_store.create_authorization_code(
            user_id=user_id,
            client_id=pending["mcp_client_id"],
            redirect_uri=pending["mcp_redirect_uri"],
            scope=pending["mcp_scope"],
            code_challenge=pending["mcp_code_challenge"],
            code_challenge_method=pending["mcp_code_challenge_method"],
        )

        # Clean up pending authorization
        del self._pending_authorizations[state]

        return {
            "code": mcp_code,
            "state": pending["mcp_state"],
            "redirect_uri": pending["mcp_redirect_uri"],
        }
