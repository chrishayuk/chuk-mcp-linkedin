"""
Tests for OAuth modules.

Tests the OAuth context, LinkedIn client, and provider implementation.
"""

from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from chuk_mcp_linkedin.oauth.linkedin_client import LinkedInOAuthClient
from chuk_mcp_linkedin.oauth.provider import LinkedInOAuthProvider
from chuk_mcp_linkedin.oauth_context import (
    clear_linkedin_token,
    get_linkedin_token,
    set_linkedin_token,
)


class TestOAuthContext:
    """Test OAuth context functions"""

    def test_set_and_get_token(self):
        """Test setting and getting token"""
        set_linkedin_token("test_token_123")
        assert get_linkedin_token() == "test_token_123"

    def test_clear_token(self):
        """Test clearing token"""
        set_linkedin_token("test_token")
        clear_linkedin_token()
        assert get_linkedin_token() is None

    def test_get_token_default_none(self):
        """Test getting token returns None by default"""
        clear_linkedin_token()  # Ensure clean state
        assert get_linkedin_token() is None

    def test_token_isolation(self):
        """Test token is isolated per context"""
        set_linkedin_token("token1")
        assert get_linkedin_token() == "token1"

        set_linkedin_token("token2")
        assert get_linkedin_token() == "token2"


class TestLinkedInOAuthClient:
    """Test LinkedIn OAuth client"""

    @pytest.fixture
    def client(self):
        """Create OAuth client instance"""
        return LinkedInOAuthClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:3000/callback",
        )

    def test_initialization(self, client):
        """Test client initializes correctly"""
        assert client.client_id == "test_client_id"
        assert client.client_secret == "test_client_secret"
        assert client.redirect_uri == "http://localhost:3000/callback"

    def test_get_authorization_url_with_defaults(self, client):
        """Test generating authorization URL with default scopes"""
        url = client.get_authorization_url(state="test_state")

        assert "https://www.linkedin.com/oauth/v2/authorization" in url
        assert "client_id=test_client_id" in url
        assert "redirect_uri=http" in url
        assert "state=test_state" in url
        assert "scope=" in url
        assert "response_type=code" in url

    def test_get_authorization_url_with_custom_scopes(self, client):
        """Test authorization URL with custom scopes"""
        url = client.get_authorization_url(
            state="test_state",
            scope=["openid", "profile"],
        )

        assert "scope=openid+profile" in url or "scope=openid%20profile" in url

    @pytest.mark.asyncio
    async def test_exchange_code_for_token_success(self, client):
        """Test successful token exchange"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "linkedin_token_123",
            "expires_in": 5184000,
            "scope": "openid profile",
        }
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.exchange_code_for_token("auth_code_123")

            assert result["access_token"] == "linkedin_token_123"
            assert result["expires_in"] == 5184000

    @pytest.mark.asyncio
    async def test_refresh_access_token_success(self, client):
        """Test successful token refresh"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "new_token_456",
            "expires_in": 5184000,
        }
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.refresh_access_token("refresh_token_123")

            assert result["access_token"] == "new_token_456"

    @pytest.mark.asyncio
    async def test_get_user_info_success(self, client):
        """Test getting user info"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "sub": "linkedin_user_123",
            "name": "Test User",
            "email": "test@example.com",
        }
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.get_user_info("access_token_123")

            assert result["sub"] == "linkedin_user_123"
            assert result["name"] == "Test User"

    @pytest.mark.asyncio
    async def test_validate_token_valid(self, client):
        """Test validating valid token"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"sub": "user_123"}
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.validate_token("valid_token")

            assert result is True

    @pytest.mark.asyncio
    async def test_validate_token_invalid(self, client):
        """Test validating invalid token"""
        import httpx

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=httpx.HTTPError("Invalid token"))
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.validate_token("invalid_token")

            assert result is False


class TestLinkedInOAuthProvider:
    """Test LinkedIn OAuth provider"""

    @pytest.fixture
    def mock_token_store(self):
        """Create mock token store"""
        store = AsyncMock()
        store.validate_client = AsyncMock(return_value=True)
        store.create_authorization_code = AsyncMock(return_value="auth_code_123")
        store.validate_authorization_code = AsyncMock(
            return_value={
                "user_id": "user_123",
                "client_id": "client_456",
                "scope": "linkedin.posts",
            }
        )
        store.create_access_token = AsyncMock(return_value=("access_token", "refresh_token"))
        store.validate_access_token = AsyncMock(
            return_value={
                "user_id": "user_123",
                "client_id": "client_456",
            }
        )
        store.get_external_token = AsyncMock(
            return_value={
                "access_token": "linkedin_token",
                "refresh_token": "linkedin_refresh",
            }
        )
        store.is_external_token_expired = AsyncMock(return_value=False)
        store.register_client = AsyncMock(
            return_value={
                "client_id": "new_client_id",
                "client_secret": "new_client_secret",
            }
        )
        store.refresh_access_token = AsyncMock(return_value=("new_access", "new_refresh"))
        store.link_external_token = AsyncMock()
        store.update_external_token = AsyncMock()
        return store

    @pytest.fixture
    def provider(self, mock_token_store):
        """Create provider instance"""
        return LinkedInOAuthProvider(
            linkedin_client_id="linkedin_client_id",
            linkedin_client_secret="linkedin_client_secret",
            linkedin_redirect_uri="http://localhost:8000/oauth/linkedin/callback",
            oauth_server_url="http://localhost:8000",
            token_store=mock_token_store,
        )

    def test_initialization(self, provider):
        """Test provider initializes correctly"""
        assert provider.oauth_server_url == "http://localhost:8000"
        assert provider.linkedin_client is not None
        assert provider.token_store is not None

    @pytest.mark.asyncio
    async def test_register_client_success(self, provider):
        """Test registering a new client"""
        client_metadata = {
            "client_name": "Test Client",
            "redirect_uris": ["http://localhost:3000/callback"],
        }

        result = await provider.register_client(client_metadata)

        assert result.client_id == "new_client_id"
        assert result.client_secret == "new_client_secret"
        assert result.client_name == "Test Client"

    @pytest.mark.asyncio
    async def test_register_client_no_redirect_uris(self, provider):
        """Test registering client without redirect URIs fails"""
        from chuk_mcp_server.oauth import RegistrationError

        client_metadata = {
            "client_name": "Test Client",
            "redirect_uris": [],
        }

        with pytest.raises(RegistrationError):
            await provider.register_client(client_metadata)

    @pytest.mark.asyncio
    async def test_exchange_authorization_code_success(self, provider):
        """Test exchanging authorization code for token"""
        token = await provider.exchange_authorization_code(
            code="auth_code",
            client_id="client_id",
            redirect_uri="http://localhost:3000/callback",
        )

        assert token.access_token == "access_token"
        assert token.refresh_token == "refresh_token"
        assert token.token_type == "Bearer"

    @pytest.mark.asyncio
    async def test_exchange_authorization_code_invalid(self, provider, mock_token_store):
        """Test exchanging invalid authorization code"""
        from chuk_mcp_server.oauth import TokenError

        mock_token_store.validate_authorization_code = AsyncMock(return_value=None)

        with pytest.raises(TokenError):
            await provider.exchange_authorization_code(
                code="invalid_code",
                client_id="client_id",
                redirect_uri="http://localhost:3000/callback",
            )

    @pytest.mark.asyncio
    async def test_exchange_refresh_token_success(self, provider):
        """Test refreshing access token"""
        token = await provider.exchange_refresh_token(
            refresh_token="refresh_token",
            client_id="client_id",
        )

        assert token.access_token == "new_access"
        assert token.refresh_token == "new_refresh"

    @pytest.mark.asyncio
    async def test_validate_access_token_success(self, provider):
        """Test validating access token"""
        result = await provider.validate_access_token("access_token")

        assert result["user_id"] == "user_123"
        assert result["external_access_token"] == "linkedin_token"

    @pytest.mark.asyncio
    async def test_validate_access_token_invalid(self, provider, mock_token_store):
        """Test validating invalid access token"""
        from chuk_mcp_server.oauth import TokenError

        mock_token_store.validate_access_token = AsyncMock(return_value=None)

        with pytest.raises(TokenError):
            await provider.validate_access_token("invalid_token")

    @pytest.mark.asyncio
    async def test_validate_access_token_no_linkedin_token(self, provider, mock_token_store):
        """Test validating token without LinkedIn token"""
        from chuk_mcp_server.oauth import TokenError

        mock_token_store.get_external_token = AsyncMock(return_value=None)

        with pytest.raises(TokenError):
            await provider.validate_access_token("access_token")

    @pytest.mark.asyncio
    async def test_authorize_with_invalid_client(self, provider, mock_token_store):
        """Test authorization with invalid client"""
        from chuk_mcp_server.oauth import AuthorizationParams, AuthorizeError

        mock_token_store.validate_client = AsyncMock(return_value=False)

        params = AuthorizationParams(
            client_id="invalid_client",
            redirect_uri="http://localhost:3000/callback",
            response_type="code",
        )

        with pytest.raises(AuthorizeError, match="Invalid client_id"):
            await provider.authorize(params)

    @pytest.mark.asyncio
    async def test_authorize_requires_linkedin_auth(self, provider, mock_token_store):
        """Test authorization that requires LinkedIn authentication"""
        from chuk_mcp_server.oauth import AuthorizationParams

        mock_token_store.validate_client = AsyncMock(return_value=True)

        params = AuthorizationParams(
            client_id="client_id",
            redirect_uri="http://localhost:3000/callback",
            response_type="code",
            state="test_state",
        )

        result = await provider.authorize(params)

        assert "authorization_url" in result
        assert "linkedin.com" in result["authorization_url"]
        assert result["requires_external_authorization"] is True

    @pytest.mark.asyncio
    async def test_authorize_with_existing_linkedin_token(self, provider, mock_token_store):
        """Test authorization when LinkedIn token already exists"""
        from chuk_mcp_server.oauth import AuthorizationParams

        mock_token_store.validate_client = AsyncMock(return_value=True)
        mock_token_store.get_external_token = AsyncMock(
            return_value={"access_token": "linkedin_token", "refresh_token": "refresh"}
        )
        mock_token_store.is_external_token_expired = AsyncMock(return_value=False)

        # Set up pending authorization with user_id
        state = "test_state"
        provider._pending_authorizations[state] = {"user_id": "user_123"}

        params = AuthorizationParams(
            client_id="client_id",
            redirect_uri="http://localhost:3000/callback",
            response_type="code",
            state=state,
        )

        result = await provider.authorize(params)

        assert "code" in result
        assert result["state"] == state
        assert state not in provider._pending_authorizations

    @pytest.mark.asyncio
    async def test_exchange_refresh_token_invalid(self, provider, mock_token_store):
        """Test refreshing with invalid refresh token"""
        from chuk_mcp_server.oauth import TokenError

        mock_token_store.refresh_access_token = AsyncMock(return_value=None)

        with pytest.raises(TokenError, match="Invalid refresh token"):
            await provider.exchange_refresh_token(
                refresh_token="invalid_refresh",
                client_id="client_id",
            )

    @pytest.mark.asyncio
    async def test_validate_access_token_refresh_linkedin_token(self, provider, mock_token_store):
        """Test validating token triggers LinkedIn token refresh"""
        mock_token_store.is_external_token_expired = AsyncMock(return_value=True)

        with patch.object(provider.linkedin_client, "refresh_access_token") as mock_refresh:
            mock_refresh.return_value = {
                "access_token": "new_linkedin_token",
                "refresh_token": "new_refresh",
                "expires_in": 5184000,
            }

            await provider.validate_access_token("access_token")

            mock_refresh.assert_called_once_with("linkedin_refresh")
            mock_token_store.update_external_token.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_access_token_refresh_fails(self, provider, mock_token_store):
        """Test validation fails when LinkedIn token refresh fails"""
        from chuk_mcp_server.oauth import TokenError

        mock_token_store.is_external_token_expired = AsyncMock(return_value=True)

        with patch.object(provider.linkedin_client, "refresh_access_token") as mock_refresh:
            mock_refresh.side_effect = Exception("Refresh failed")

            with pytest.raises(TokenError, match="Failed to refresh LinkedIn token"):
                await provider.validate_access_token("access_token")

    @pytest.mark.asyncio
    async def test_validate_access_token_no_refresh_token(self, provider, mock_token_store):
        """Test validation fails when LinkedIn token expired and no refresh token"""
        from chuk_mcp_server.oauth import TokenError

        mock_token_store.is_external_token_expired = AsyncMock(return_value=True)
        mock_token_store.get_external_token = AsyncMock(
            return_value={"access_token": "expired_token"}  # No refresh_token
        )

        with pytest.raises(TokenError, match="no refresh token available"):
            await provider.validate_access_token("access_token")

    @pytest.mark.asyncio
    async def test_handle_external_callback_success(self, provider, mock_token_store):
        """Test handling LinkedIn OAuth callback"""
        # Set up pending authorization data
        state = "linkedin_state_123"
        pending_data = {
            "mcp_client_id": "client_id",
            "mcp_redirect_uri": "http://localhost:3000/callback",
            "mcp_state": "mcp_state",
            "mcp_scope": "linkedin.posts",
            "mcp_code_challenge": None,
            "mcp_code_challenge_method": None,
        }

        # Mock the persistent storage methods
        mock_token_store.get_pending_authorization = AsyncMock(return_value=pending_data)
        mock_token_store.delete_pending_authorization = AsyncMock(return_value=True)

        # Also set in memory for backwards compatibility check
        provider._pending_authorizations[state] = pending_data

        with patch.object(provider.linkedin_client, "exchange_code_for_token") as mock_exchange:
            with patch.object(provider.linkedin_client, "get_user_info") as mock_user_info:
                mock_exchange.return_value = {
                    "access_token": "linkedin_token",
                    "refresh_token": "linkedin_refresh",
                    "expires_in": 5184000,
                }
                mock_user_info.return_value = {"sub": "linkedin_user_123"}

                result = await provider.handle_external_callback(
                    code="linkedin_code",
                    state=state,
                )

                assert result["code"] == "auth_code_123"
                assert result["state"] == "mcp_state"
                assert state not in provider._pending_authorizations
                mock_token_store.link_external_token.assert_called_once()
                mock_token_store.delete_pending_authorization.assert_called_once_with(state)

    @pytest.mark.asyncio
    async def test_handle_external_callback_invalid_state(self, provider, mock_token_store):
        """Test callback with invalid state"""
        # Mock persistent storage to return None (state not found)
        mock_token_store.get_pending_authorization = AsyncMock(return_value=None)

        with pytest.raises(ValueError, match="Invalid or expired state"):
            await provider.handle_external_callback(
                code="linkedin_code",
                state="invalid_state",
            )

    @pytest.mark.asyncio
    async def test_handle_external_callback_token_exchange_fails(self, provider, mock_token_store):
        """Test callback when LinkedIn token exchange fails"""
        state = "linkedin_state_123"
        pending_data = {
            "mcp_client_id": "client_id",
            "mcp_redirect_uri": "http://localhost:3000/callback",
            "mcp_state": "mcp_state",
            "mcp_scope": "linkedin.posts",
            "mcp_code_challenge": None,
            "mcp_code_challenge_method": None,
        }

        # Mock persistent storage
        mock_token_store.get_pending_authorization = AsyncMock(return_value=pending_data)
        provider._pending_authorizations[state] = pending_data

        with patch.object(provider.linkedin_client, "exchange_code_for_token") as mock_exchange:
            mock_exchange.side_effect = Exception("Exchange failed")

            with pytest.raises(ValueError, match="LinkedIn token exchange failed"):
                await provider.handle_external_callback(
                    code="linkedin_code",
                    state=state,
                )

    @pytest.mark.asyncio
    async def test_handle_external_callback_user_info_fails(self, provider, mock_token_store):
        """Test callback when getting user info fails"""
        state = "linkedin_state_123"
        pending_data = {
            "mcp_client_id": "client_id",
            "mcp_redirect_uri": "http://localhost:3000/callback",
            "mcp_state": "mcp_state",
            "mcp_scope": "linkedin.posts",
            "mcp_code_challenge": None,
            "mcp_code_challenge_method": None,
        }

        # Mock persistent storage
        mock_token_store.get_pending_authorization = AsyncMock(return_value=pending_data)
        provider._pending_authorizations[state] = pending_data

        with patch.object(provider.linkedin_client, "exchange_code_for_token") as mock_exchange:
            with patch.object(provider.linkedin_client, "get_user_info") as mock_user_info:
                mock_exchange.return_value = {"access_token": "linkedin_token"}
                mock_user_info.side_effect = Exception("User info failed")

                with pytest.raises(ValueError, match="Failed to get LinkedIn user info"):
                    await provider.handle_external_callback(
                        code="linkedin_code",
                        state=state,
                    )

    def test_initialization_without_token_store(self):
        """Test provider initialization without explicit token store"""
        provider = LinkedInOAuthProvider(
            linkedin_client_id="client_id",
            linkedin_client_secret="client_secret",
            linkedin_redirect_uri="http://localhost:8000/callback",
        )

        assert provider.token_store is not None
        assert provider.oauth_server_url == "http://localhost:8000"


class TestOAuthImports:
    """Test OAuth module imports"""

    def test_import_provider(self):
        """Test importing provider"""
        from chuk_mcp_linkedin.oauth import LinkedInOAuthProvider

        assert LinkedInOAuthProvider is not None

    def test_import_client(self):
        """Test importing client"""
        from chuk_mcp_linkedin.oauth import LinkedInOAuthClient

        assert LinkedInOAuthClient is not None

    def test_all_exports(self):
        """Test __all__ exports"""
        import chuk_mcp_linkedin.oauth as oauth_module

        assert "LinkedInOAuthProvider" in oauth_module.__all__
        assert "LinkedInOAuthClient" in oauth_module.__all__
