"""
Tests for LinkedIn Posts API.

Tests post creation methods with mocked HTTP requests.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from chuk_mcp_linkedin.api import LinkedInClient, LinkedInConfig, LinkedInAPIError


@pytest.fixture
def configured_client():
    """Create a configured LinkedIn client for testing"""
    config = LinkedInConfig(
        linkedin_access_token="test_token",
        linkedin_person_urn="urn:li:person:test123",
    )
    return LinkedInClient(config=config)


@pytest.fixture
def mock_httpx_success():
    """Mock successful HTTP response"""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "urn:li:share:123456",
        "created": {"time": 1234567890},
    }
    mock_response.raise_for_status = MagicMock()
    return mock_response


@pytest.fixture
def mock_httpx_error():
    """Mock error HTTP response"""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "status": 400,
        "message": "Invalid request",
    }

    def raise_for_status():
        from httpx import HTTPStatusError
        raise HTTPStatusError("400 Bad Request", request=MagicMock(), response=mock_response)

    mock_response.raise_for_status = raise_for_status
    return mock_response


class TestCreateTextPost:
    """Test create_text_post method"""

    @pytest.mark.asyncio
    async def test_create_text_post_success(self, configured_client, mock_httpx_success):
        """Test successful text post creation"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await configured_client.create_text_post("Test post")

            assert result["id"] == "urn:li:share:123456"
            mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_text_post_with_visibility(self, configured_client, mock_httpx_success):
        """Test text post creation with custom visibility"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await configured_client.create_text_post("Test", visibility="CONNECTIONS")

            assert result["id"] == "urn:li:share:123456"

    @pytest.mark.asyncio
    async def test_create_text_post_without_credentials(self):
        """Test text post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None, linkedin_person_urn=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_text_post("Test")

    @pytest.mark.asyncio
    async def test_create_text_post_api_error(self, configured_client, mock_httpx_error):
        """Test text post creation with API error"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_error)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with pytest.raises(LinkedInAPIError, match="Failed to create"):
                await configured_client.create_text_post("Test")


class TestCreateImagePost:
    """Test create_image_post method"""

    @pytest.mark.asyncio
    async def test_create_image_post_success(self, configured_client, mock_httpx_success):
        """Test successful image post creation"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_image", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:image:123"

                result = await configured_client.create_image_post("Test", "test.jpg")

                assert result["id"] == "urn:li:share:123456"
                mock_upload.assert_called_once_with("test.jpg", alt_text=None)

    @pytest.mark.asyncio
    async def test_create_image_post_with_alt_text(self, configured_client, mock_httpx_success):
        """Test image post creation with alt text"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_image", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:image:123"

                result = await configured_client.create_image_post("Test", "test.jpg", alt_text="Test image")

                mock_upload.assert_called_once_with("test.jpg", alt_text="Test image")

    @pytest.mark.asyncio
    async def test_create_image_post_without_credentials(self):
        """Test image post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_image_post("Test", "test.jpg")


class TestCreateMultiImagePost:
    """Test create_multi_image_post method"""

    @pytest.mark.asyncio
    async def test_create_multi_image_post_success(self, configured_client, mock_httpx_success):
        """Test successful multi-image post creation"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_image", new_callable=AsyncMock) as mock_upload:
                mock_upload.side_effect = ["urn:li:image:1", "urn:li:image:2"]

                result = await configured_client.create_multi_image_post("Test", ["img1.jpg", "img2.jpg"])

                assert result["id"] == "urn:li:share:123456"
                assert mock_upload.call_count == 2

    @pytest.mark.asyncio
    async def test_create_multi_image_post_without_credentials(self):
        """Test multi-image post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_multi_image_post("Test", ["img1.jpg"])


class TestCreateVideoPost:
    """Test create_video_post method"""

    @pytest.mark.asyncio
    async def test_create_video_post_success(self, configured_client, mock_httpx_success):
        """Test successful video post creation"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_video", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:video:123"

                result = await configured_client.create_video_post("Test", "test.mp4")

                assert result["id"] == "urn:li:share:123456"
                mock_upload.assert_called_once_with("test.mp4", title=None, description=None)

    @pytest.mark.asyncio
    async def test_create_video_post_with_metadata(self, configured_client, mock_httpx_success):
        """Test video post creation with title and description"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_video", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:video:123"

                result = await configured_client.create_video_post(
                    "Test", "test.mp4",
                    title="Video Title",
                    description="Video Description"
                )

                mock_upload.assert_called_once_with("test.mp4", title="Video Title", description="Video Description")

    @pytest.mark.asyncio
    async def test_create_video_post_without_credentials(self):
        """Test video post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_video_post("Test", "test.mp4")


class TestCreatePollPost:
    """Test create_poll_post method"""

    @pytest.mark.asyncio
    async def test_create_poll_post_success(self, configured_client, mock_httpx_success):
        """Test successful poll post creation"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await configured_client.create_poll_post(
                "Test question",
                "Which option?",
                ["Option A", "Option B"]
            )

            assert result["id"] == "urn:li:share:123456"

    @pytest.mark.asyncio
    async def test_create_poll_post_with_duration(self, configured_client, mock_httpx_success):
        """Test poll post creation with custom duration"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await configured_client.create_poll_post(
                "Test",
                "Question?",
                ["A", "B"],
                duration_days=14
            )

            assert result["id"] == "urn:li:share:123456"

    @pytest.mark.asyncio
    async def test_create_poll_post_without_credentials(self):
        """Test poll post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_poll_post("Test", "Question?", ["A", "B"])


class TestCreateDocumentPost:
    """Test create_document_post method"""

    @pytest.mark.asyncio
    async def test_create_document_post_success(self, configured_client, mock_httpx_success):
        """Test successful document post creation"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_document", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:document:123"

                result = await configured_client.create_document_post("Test", "test.pdf")

                assert result["id"] == "urn:li:share:123456"
                mock_upload.assert_called_once_with("test.pdf", title=None)

    @pytest.mark.asyncio
    async def test_create_document_post_with_title(self, configured_client, mock_httpx_success):
        """Test document post creation with title"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_document", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:document:123"

                result = await configured_client.create_document_post(
                    "Test",
                    "test.pdf",
                    document_title="Document Title"
                )

                mock_upload.assert_called_once_with("test.pdf", title="Document Title")

    @pytest.mark.asyncio
    async def test_create_document_post_without_credentials(self):
        """Test document post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_document_post("Test", "test.pdf")
