"""
Tests for LinkedIn Media API.

Tests image and video upload methods with mocked HTTP requests.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from pathlib import Path
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
def mock_image_init_response():
    """Mock image upload initialization response"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "value": {
            "uploadUrl": "https://upload.example.com/image",
            "image": "urn:li:image:123456",
        }
    }
    mock_response.raise_for_status = MagicMock()
    return mock_response


@pytest.fixture
def mock_video_init_response():
    """Mock video upload initialization response"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "value": {
            "uploadUrl": "https://upload.example.com/video",
            "video": "urn:li:video:123456",
        }
    }
    mock_response.raise_for_status = MagicMock()
    return mock_response


@pytest.fixture
def mock_upload_success_response():
    """Mock successful upload response"""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.raise_for_status = MagicMock()
    return mock_response


@pytest.fixture
def mock_file_stat():
    """Mock file stat for file size"""
    mock_stat = MagicMock()
    mock_stat.st_size = 1024 * 1024  # 1MB
    return mock_stat


class TestUploadImage:
    """Test upload_image method"""

    @pytest.mark.asyncio
    async def test_upload_image_success(
        self,
        configured_client,
        mock_image_init_response,
        mock_upload_success_response,
        mock_file_stat
    ):
        """Test successful image upload"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.side_effect = [mock_image_init_response, mock_upload_success_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("builtins.open", mock_open(read_data=b"fake image data")):
                    result = await configured_client.upload_image("test.jpg")

                    assert result == "urn:li:image:123456"
                    assert mock_client.post.call_count == 2

    @pytest.mark.asyncio
    async def test_upload_image_with_alt_text(
        self,
        configured_client,
        mock_image_init_response,
        mock_upload_success_response,
        mock_file_stat
    ):
        """Test image upload with alt text"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.side_effect = [mock_image_init_response, mock_upload_success_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("builtins.open", mock_open(read_data=b"fake image data")):
                    result = await configured_client.upload_image("test.jpg", alt_text="Test image")

                    assert result == "urn:li:image:123456"

    @pytest.mark.asyncio
    async def test_upload_image_without_credentials(self):
        """Test image upload fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None, linkedin_person_urn=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.upload_image("test.jpg")

    @pytest.mark.asyncio
    async def test_upload_image_init_fails(self, configured_client):
        """Test image upload when initialization fails"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_error_response = MagicMock()
            mock_error_response.status_code = 400
            mock_error_response.json.return_value = {"message": "Invalid request"}

            def raise_for_status():
                from httpx import HTTPStatusError
                raise HTTPStatusError("400 Bad Request", request=MagicMock(), response=mock_error_response)

            mock_error_response.raise_for_status = raise_for_status
            mock_client.post.return_value = mock_error_response
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with pytest.raises(LinkedInAPIError, match="Failed to upload image"):
                await configured_client.upload_image("test.jpg")

    @pytest.mark.asyncio
    async def test_upload_image_upload_fails(
        self,
        configured_client,
        mock_image_init_response,
        mock_file_stat
    ):
        """Test image upload when file upload fails"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_error_response = MagicMock()
            mock_error_response.status_code = 500

            def raise_for_status():
                from httpx import HTTPStatusError
                raise HTTPStatusError("500 Server Error", request=MagicMock(), response=mock_error_response)

            mock_error_response.raise_for_status = raise_for_status
            mock_client.post.side_effect = [mock_image_init_response, mock_error_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("builtins.open", mock_open(read_data=b"fake image data")):
                    with pytest.raises(LinkedInAPIError, match="Failed to upload image"):
                        await configured_client.upload_image("test.jpg")


class TestUploadVideo:
    """Test upload_video method"""

    @pytest.mark.asyncio
    async def test_upload_video_success(
        self,
        configured_client,
        mock_video_init_response,
        mock_upload_success_response,
        mock_file_stat
    ):
        """Test successful video upload"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.side_effect = [mock_video_init_response, mock_upload_success_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("builtins.open", mock_open(read_data=b"fake video data")):
                    result = await configured_client.upload_video("test.mp4")

                    assert result == "urn:li:video:123456"
                    assert mock_client.post.call_count == 2

    @pytest.mark.asyncio
    async def test_upload_video_with_metadata(
        self,
        configured_client,
        mock_video_init_response,
        mock_upload_success_response,
        mock_file_stat
    ):
        """Test video upload with title and description"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.side_effect = [mock_video_init_response, mock_upload_success_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("builtins.open", mock_open(read_data=b"fake video data")):
                    result = await configured_client.upload_video(
                        "test.mp4",
                        title="Video Title",
                        description="Video Description"
                    )

                    assert result == "urn:li:video:123456"

    @pytest.mark.asyncio
    async def test_upload_video_without_credentials(self):
        """Test video upload fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None, linkedin_person_urn=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.upload_video("test.mp4")

    @pytest.mark.asyncio
    async def test_upload_video_init_fails(self, configured_client):
        """Test video upload when initialization fails"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_error_response = MagicMock()
            mock_error_response.status_code = 400
            mock_error_response.json.return_value = {"message": "Invalid request"}

            def raise_for_status():
                from httpx import HTTPStatusError
                raise HTTPStatusError("400 Bad Request", request=MagicMock(), response=mock_error_response)

            mock_error_response.raise_for_status = raise_for_status
            mock_client.post.return_value = mock_error_response
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with pytest.raises(LinkedInAPIError, match="Failed to upload video"):
                await configured_client.upload_video("test.mp4")

    @pytest.mark.asyncio
    async def test_upload_video_upload_fails(
        self,
        configured_client,
        mock_video_init_response,
        mock_file_stat
    ):
        """Test video upload when file upload fails"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_error_response = MagicMock()
            mock_error_response.status_code = 500

            def raise_for_status():
                from httpx import HTTPStatusError
                raise HTTPStatusError("500 Server Error", request=MagicMock(), response=mock_error_response)

            mock_error_response.raise_for_status = raise_for_status
            mock_client.post.side_effect = [mock_video_init_response, mock_error_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("builtins.open", mock_open(read_data=b"fake video data")):
                    with pytest.raises(LinkedInAPIError, match="Failed to upload video"):
                        await configured_client.upload_video("test.mp4")
