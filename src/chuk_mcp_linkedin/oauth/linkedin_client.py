# src/chuk_mcp_linkedin/oauth/linkedin_client.py
"""
LinkedIn OAuth 2.0 client implementation.

Implements LinkedIn's Authorization Code Flow:
https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow

OAuth Flow:
    1. Redirect user to LinkedIn authorization page
    2. User authorizes application
    3. LinkedIn redirects back with authorization code
    4. Exchange code for access token
    5. Use access token for API calls
    6. Refresh token when expired (if refresh token provided)
"""

from typing import Optional, Dict, Any
import httpx
from urllib.parse import urlencode


class LinkedInOAuthClient:
    """
    OAuth 2.0 client for LinkedIn API.

    Manages the OAuth flow to obtain and refresh LinkedIn access tokens.
    """

    # LinkedIn OAuth endpoints
    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    USERINFO_URL = "https://api.linkedin.com/v2/userinfo"

    # Default scopes for LinkedIn posting
    DEFAULT_SCOPES = ["openid", "profile", "w_member_social", "email"]

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ):
        """
        Initialize LinkedIn OAuth client.

        Args:
            client_id: LinkedIn application client ID
            client_secret: LinkedIn application client secret
            redirect_uri: Redirect URI registered with LinkedIn
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(
        self,
        state: str,
        scope: Optional[list[str]] = None,
    ) -> str:
        """
        Generate LinkedIn authorization URL.

        Args:
            state: State parameter for CSRF protection
            scope: List of scopes to request (default: DEFAULT_SCOPES)

        Returns:
            Authorization URL to redirect user to
        """
        scopes = scope or self.DEFAULT_SCOPES

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "scope": " ".join(scopes),
        }

        return f"{self.AUTHORIZATION_URL}?{urlencode(params)}"

    async def exchange_code_for_token(
        self,
        code: str,
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from LinkedIn callback

        Returns:
            Token response dict with:
                - access_token: LinkedIn access token
                - expires_in: Token lifetime in seconds
                - refresh_token: Refresh token (if available)
                - scope: Granted scopes

        Raises:
            httpx.HTTPError: If token exchange fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )

            response.raise_for_status()
            return response.json()

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: LinkedIn refresh token

        Returns:
            Token response dict with new access_token

        Raises:
            httpx.HTTPError: If token refresh fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )

            response.raise_for_status()
            return response.json()

    async def get_user_info(
        self,
        access_token: str,
    ) -> Dict[str, Any]:
        """
        Get user information from LinkedIn.

        Args:
            access_token: LinkedIn access token

        Returns:
            User info dict with:
                - sub: LinkedIn user ID
                - name: User's name
                - email: User's email
                - picture: Profile picture URL

        Raises:
            httpx.HTTPError: If request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.USERINFO_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )

            response.raise_for_status()
            return response.json()

    async def validate_token(
        self,
        access_token: str,
    ) -> bool:
        """
        Validate LinkedIn access token.

        Args:
            access_token: LinkedIn access token

        Returns:
            True if token is valid, False otherwise
        """
        try:
            await self.get_user_info(access_token)
            return True
        except httpx.HTTPError:
            return False
