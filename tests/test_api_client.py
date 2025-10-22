"""
Tests for LinkedIn API client.

Tests the API client configuration and structure without making real API calls.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from chuk_mcp_linkedin.api import LinkedInClient, LinkedInConfig, LinkedInAPIError


class TestLinkedInConfig:
    """Test LinkedInConfig class"""

    def test_config_creation(self):
        """Test creating configuration"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        assert config.linkedin_access_token == "test_token"
        assert config.linkedin_person_urn == "urn:li:person:test123"

    def test_config_default_base_url(self):
        """Test default API base URL"""
        config = LinkedInConfig()
        assert config.linkedin_api_base_url == "https://api.linkedin.com/v2"

    def test_config_custom_base_url(self):
        """Test custom API base URL"""
        config = LinkedInConfig(linkedin_api_base_url="https://custom.api.com")
        assert config.linkedin_api_base_url == "https://custom.api.com"


class TestLinkedInClientInit:
    """Test LinkedInClient initialization"""

    def test_client_creation_with_config(self):
        """Test creating client with explicit config"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        client = LinkedInClient(config=config)
        assert client.access_token == "test_token"
        assert client.person_urn == "urn:li:person:test123"

    def test_client_creation_uses_default_config(self):
        """Test creating client without config uses default"""
        client = LinkedInClient()
        # Should not raise an error
        assert client.config is not None

    def test_client_has_base_url(self):
        """Test client has base URL"""
        config = LinkedInConfig(linkedin_api_base_url="https://api.linkedin.com/v2")
        client = LinkedInClient(config=config)
        assert client.base_url == "https://api.linkedin.com/v2"


class TestLinkedInClientHeaders:
    """Test LinkedIn client headers"""

    def test_get_headers_includes_authorization(self):
        """Test headers include authorization"""
        config = LinkedInConfig(linkedin_access_token="test_token")
        client = LinkedInClient(config=config)
        headers = client._get_headers()
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_token"

    def test_get_headers_includes_content_type(self):
        """Test headers include content type"""
        config = LinkedInConfig(linkedin_access_token="test_token")
        client = LinkedInClient(config=config)
        headers = client._get_headers()
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"

    def test_get_headers_includes_protocol_version(self):
        """Test headers include protocol version"""
        config = LinkedInConfig(linkedin_access_token="test_token")
        client = LinkedInClient(config=config)
        headers = client._get_headers()
        assert "X-Restli-Protocol-Version" in headers

    def test_get_headers_with_rest_api_flag(self):
        """Test headers include LinkedIn-Version when use_rest_api=True"""
        config = LinkedInConfig(linkedin_access_token="test_token")
        client = LinkedInClient(config=config)
        headers = client._get_headers(use_rest_api=True)
        assert "Linkedin-Version" in headers
        assert headers["Linkedin-Version"] == "202502"

    def test_get_headers_without_rest_api_flag(self):
        """Test headers don't include LinkedIn-Version when use_rest_api=False"""
        config = LinkedInConfig(linkedin_access_token="test_token")
        client = LinkedInClient(config=config)
        headers = client._get_headers(use_rest_api=False)
        assert "Linkedin-Version" not in headers


class TestLinkedInClientMixins:
    """Test that client has all mixins"""

    def test_client_has_posts_api(self):
        """Test client has posts API methods"""
        client = LinkedInClient()
        assert hasattr(client, "create_text_post")
        assert hasattr(client, "create_image_post")
        assert hasattr(client, "create_video_post")
        assert hasattr(client, "create_multi_image_post")
        assert hasattr(client, "create_poll_post")

    def test_client_has_media_api(self):
        """Test client has media API methods"""
        client = LinkedInClient()
        assert hasattr(client, "upload_image")
        assert hasattr(client, "upload_video")

    def test_client_has_documents_api(self):
        """Test client has documents API methods"""
        client = LinkedInClient()
        assert hasattr(client, "upload_document")
        assert hasattr(client, "create_document_post")


class TestLinkedInAPIError:
    """Test LinkedInAPIError exception"""

    def test_error_creation(self):
        """Test creating API error"""
        error = LinkedInAPIError("Test error message")
        assert str(error) == "Test error message"

    def test_error_is_exception(self):
        """Test error is an Exception"""
        error = LinkedInAPIError("Test")
        assert isinstance(error, Exception)

    def test_error_can_be_raised(self):
        """Test error can be raised"""
        with pytest.raises(LinkedInAPIError):
            raise LinkedInAPIError("Test error")

    def test_error_can_be_caught(self):
        """Test error can be caught"""
        try:
            raise LinkedInAPIError("Test error")
        except LinkedInAPIError as e:
            assert str(e) == "Test error"


class TestLinkedInClientValidation:
    """Test LinkedIn client configuration validation"""

    def test_validate_config_with_all_credentials(self):
        """Test validation succeeds with all credentials"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        client = LinkedInClient(config=config)
        is_valid, missing = client.validate_config()
        assert is_valid is True
        assert len(missing) == 0

    def test_validate_config_missing_token(self):
        """Test validation fails with missing token"""
        config = LinkedInConfig(
            linkedin_access_token=None,
            linkedin_person_urn="urn:li:person:test123",
        )
        client = LinkedInClient(config=config)
        is_valid, missing = client.validate_config()
        assert is_valid is False
        assert "LINKEDIN_ACCESS_TOKEN" in missing

    def test_validate_config_missing_person_urn(self):
        """Test validation fails with missing person URN"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn=None,
        )
        client = LinkedInClient(config=config)
        is_valid, missing = client.validate_config()
        assert is_valid is False
        assert "LINKEDIN_PERSON_URN" in missing

    def test_validate_config_missing_both(self):
        """Test validation fails with both missing"""
        config = LinkedInConfig(
            linkedin_access_token=None,
            linkedin_person_urn=None,
        )
        client = LinkedInClient(config=config)
        is_valid, missing = client.validate_config()
        assert is_valid is False
        assert "LINKEDIN_ACCESS_TOKEN" in missing
        assert "LINKEDIN_PERSON_URN" in missing
        assert len(missing) == 2


class TestLinkedInConfigMethods:
    """Test LinkedInConfig helper methods"""

    def test_is_configured_with_credentials(self):
        """Test is_configured returns True with credentials"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        assert config.is_configured() is True

    def test_is_configured_without_token(self):
        """Test is_configured returns False without token"""
        config = LinkedInConfig(
            linkedin_access_token=None,
            linkedin_person_urn="urn:li:person:test123",
        )
        assert config.is_configured() is False

    def test_is_configured_without_urn(self):
        """Test is_configured returns False without URN"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn=None,
        )
        assert config.is_configured() is False

    def test_is_configured_without_both(self):
        """Test is_configured returns False without either"""
        config = LinkedInConfig(
            linkedin_access_token=None,
            linkedin_person_urn=None,
        )
        assert config.is_configured() is False

    def test_get_missing_config_all_present(self):
        """Test get_missing_config returns empty list when all present"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        missing = config.get_missing_config()
        assert len(missing) == 0

    def test_get_missing_config_token_missing(self):
        """Test get_missing_config identifies missing token"""
        config = LinkedInConfig(
            linkedin_access_token=None,
            linkedin_person_urn="urn:li:person:test123",
        )
        missing = config.get_missing_config()
        assert "LINKEDIN_ACCESS_TOKEN" in missing

    def test_get_missing_config_urn_missing(self):
        """Test get_missing_config identifies missing URN"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn=None,
        )
        missing = config.get_missing_config()
        assert "LINKEDIN_PERSON_URN" in missing

    def test_get_missing_config_both_missing(self):
        """Test get_missing_config identifies both missing"""
        config = LinkedInConfig(
            linkedin_access_token=None,
            linkedin_person_urn=None,
        )
        missing = config.get_missing_config()
        assert "LINKEDIN_ACCESS_TOKEN" in missing
        assert "LINKEDIN_PERSON_URN" in missing


class TestLinkedInClientConnection:
    """Test LinkedIn client connection testing"""

    @pytest.mark.asyncio
    async def test_connection_success(self):
        """Test successful connection"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        client = LinkedInClient(config=config)

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.test_connection()
            assert result is True

    @pytest.mark.asyncio
    async def test_connection_no_token(self):
        """Test connection fails without token"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        result = await client.test_connection()
        assert result is False

    @pytest.mark.asyncio
    async def test_connection_http_error(self):
        """Test connection fails on HTTP error"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        client = LinkedInClient(config=config)

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.test_connection()
            assert result is False

    @pytest.mark.asyncio
    async def test_connection_exception(self):
        """Test connection fails on exception"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )
        client = LinkedInClient(config=config)

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=Exception("Connection error"))
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await client.test_connection()
            assert result is False
