"""
Tests for LinkedIn Documents API.

Tests document upload and post creation methods with mocked HTTP requests.
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
def mock_document_init_response():
    """Mock document upload initialization response"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "value": {
            "uploadUrl": "https://upload.example.com/document",
            "document": "urn:li:document:123456",
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
def mock_post_success_response():
    """Mock successful post creation response"""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "urn:li:share:123456",
        "created": {"time": 1234567890},
    }
    mock_response.raise_for_status = MagicMock()
    return mock_response


@pytest.fixture
def mock_file_stat():
    """Mock file stat for file size"""
    mock_stat = MagicMock()
    mock_stat.st_size = 1024 * 1024  # 1MB
    return mock_stat


class TestUploadDocument:
    """Test upload_document method"""

    @pytest.mark.asyncio
    async def test_upload_document_success(
        self,
        configured_client,
        mock_document_init_response,
        mock_upload_success_response,
        mock_file_stat
    ):
        """Test successful document upload"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.side_effect = [mock_document_init_response, mock_upload_success_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("pathlib.Path.suffix", new_callable=lambda: ".pdf"):
                    with patch("builtins.open", mock_open(read_data=b"fake pdf data")):
                        result = await configured_client.upload_document("test.pdf")

                        assert result == "urn:li:document:123456"
                        assert mock_client.post.call_count == 2

    @pytest.mark.asyncio
    async def test_upload_document_with_title(
        self,
        configured_client,
        mock_document_init_response,
        mock_upload_success_response,
        mock_file_stat
    ):
        """Test document upload with title"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.side_effect = [mock_document_init_response, mock_upload_success_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("pathlib.Path.suffix", new_callable=lambda: ".pdf"):
                    with patch("builtins.open", mock_open(read_data=b"fake pdf data")):
                        result = await configured_client.upload_document("test.pdf", title="Document Title")

                        assert result == "urn:li:document:123456"

    @pytest.mark.asyncio
    async def test_upload_document_without_credentials(self):
        """Test document upload fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None, linkedin_person_urn=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.upload_document("test.pdf")

    @pytest.mark.asyncio
    async def test_upload_document_init_fails(self, configured_client):
        """Test document upload when initialization fails"""
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

            with pytest.raises(LinkedInAPIError, match="Failed to upload document"):
                await configured_client.upload_document("test.pdf")

    @pytest.mark.asyncio
    async def test_upload_document_upload_fails(
        self,
        configured_client,
        mock_document_init_response,
        mock_file_stat
    ):
        """Test document upload when file upload fails"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_error_response = MagicMock()
            mock_error_response.status_code = 500

            def raise_for_status():
                from httpx import HTTPStatusError
                raise HTTPStatusError("500 Server Error", request=MagicMock(), response=mock_error_response)

            mock_error_response.raise_for_status = raise_for_status
            mock_client.post.side_effect = [mock_document_init_response, mock_error_response]
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch("pathlib.Path.stat", return_value=mock_file_stat):
                with patch("pathlib.Path.suffix", new_callable=lambda: ".pdf"):
                    with patch("builtins.open", mock_open(read_data=b"fake pdf data")):
                        with pytest.raises(LinkedInAPIError, match="Failed to upload document"):
                            await configured_client.upload_document("test.pdf")


class TestCreateDocumentPost:
    """Test create_document_post method"""

    @pytest.mark.asyncio
    async def test_create_document_post_success(
        self,
        configured_client,
        mock_post_success_response
    ):
        """Test successful document post creation"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_post_success_response
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(configured_client, "upload_document", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:document:123"

                result = await configured_client.create_document_post("Test", "test.pdf")

                assert result["id"] == "urn:li:share:123456"
                mock_upload.assert_called_once_with("test.pdf", title=None)

    @pytest.mark.asyncio
    async def test_create_document_post_with_title(
        self,
        configured_client,
        mock_post_success_response
    ):
        """Test document post creation with title"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_post_success_response
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

    @pytest.mark.asyncio
    async def test_create_document_post_api_error(self, configured_client):
        """Test document post creation with API error"""
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

            with patch.object(configured_client, "upload_document", new_callable=AsyncMock) as mock_upload:
                mock_upload.return_value = "urn:li:document:123"

                with pytest.raises(LinkedInAPIError, match="Failed to create document post"):
                    await configured_client.create_document_post("Test", "test.pdf")
