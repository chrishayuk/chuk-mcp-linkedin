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

            with pytest.raises(LinkedInAPIError, match="LinkedIn API error"):
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

            with patch.object(
                configured_client, "upload_image", new_callable=AsyncMock
            ) as mock_upload:
                mock_upload.return_value = "urn:li:image:123"

                result = await configured_client.create_image_post("Test", "test.jpg")

                assert result["id"] == "urn:li:share:123456"
                mock_upload.assert_called_once_with("test.jpg", None)

    @pytest.mark.asyncio
    async def test_create_image_post_with_alt_text(self, configured_client, mock_httpx_success):
        """Test image post creation with alt text"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(
                configured_client, "upload_image", new_callable=AsyncMock
            ) as mock_upload:
                mock_upload.return_value = "urn:li:image:123"

                await configured_client.create_image_post("Test", "test.jpg", alt_text="Test image")

                mock_upload.assert_called_once_with("test.jpg", "Test image")

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

            with patch.object(
                configured_client, "upload_image", new_callable=AsyncMock
            ) as mock_upload:
                mock_upload.side_effect = ["urn:li:image:1", "urn:li:image:2"]

                result = await configured_client.create_multi_image_post(
                    "Test", ["img1.jpg", "img2.jpg"]
                )

                assert result["id"] == "urn:li:share:123456"
                assert mock_upload.call_count == 2

    @pytest.mark.asyncio
    async def test_create_multi_image_post_without_credentials(self):
        """Test multi-image post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_multi_image_post("Test", ["img1.jpg", "img2.jpg"])


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

            with patch.object(
                configured_client, "upload_video", new_callable=AsyncMock
            ) as mock_upload:
                mock_upload.return_value = "urn:li:video:123"

                result = await configured_client.create_video_post("Test", "test.mp4")

                assert result["id"] == "urn:li:share:123456"
                mock_upload.assert_called_once_with("test.mp4", None)

    @pytest.mark.asyncio
    async def test_create_video_post_with_metadata(self, configured_client, mock_httpx_success):
        """Test video post creation with title and description"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(
                configured_client, "upload_video", new_callable=AsyncMock
            ) as mock_upload:
                mock_upload.return_value = "urn:li:video:123"

                await configured_client.create_video_post("Test", "test.mp4", title="Video Title")

                mock_upload.assert_called_once_with("test.mp4", "Video Title")

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
                "Test question", "Which option?", ["Option A", "Option B"]
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
                "Test", "Question?", ["A", "B"], duration="TWO_WEEKS"
            )

            assert result["id"] == "urn:li:share:123456"

    @pytest.mark.asyncio
    async def test_create_poll_post_without_credentials(self):
        """Test poll post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="LinkedIn API error"):
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

            with patch.object(
                configured_client, "upload_document", new_callable=AsyncMock
            ) as mock_upload:
                mock_upload.return_value = "urn:li:document:123"

                result = await configured_client.create_document_post("Test", "test.pdf")

                assert result["id"] == "urn:li:share:123456"
                mock_upload.assert_called_once_with("test.pdf", None)

    @pytest.mark.asyncio
    async def test_create_document_post_with_title(self, configured_client, mock_httpx_success):
        """Test document post creation with title"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_httpx_success)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with patch.object(
                configured_client, "upload_document", new_callable=AsyncMock
            ) as mock_upload:
                mock_upload.return_value = "urn:li:document:123"

                await configured_client.create_document_post(
                    "Test", "test.pdf", document_title="Document Title"
                )

                mock_upload.assert_called_once_with("test.pdf", "Document Title")

    @pytest.mark.asyncio
    async def test_create_document_post_without_credentials(self):
        """Test document post creation fails without credentials"""
        config = LinkedInConfig(linkedin_access_token=None)
        client = LinkedInClient(config=config)

        with pytest.raises(LinkedInAPIError, match="not configured"):
            await client.create_document_post("Test", "test.pdf")


class TestPostResponseHandling:
    """Test post response handling edge cases"""

    @pytest.mark.asyncio
    async def test_create_text_post_response_without_json(self, configured_client):
        """Test text post creation when response has no JSON content"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.content = b""  # Empty content
            mock_response.headers = {"x-restli-id": "urn:li:share:12345"}
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await configured_client.create_text_post("Test")
            assert result["id"] == "urn:li:share:12345"
            assert "status_code" in result

    @pytest.mark.asyncio
    async def test_create_text_post_response_invalid_json(self, configured_client):
        """Test text post creation when response has invalid JSON"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.content = b"invalid json"
            mock_response.text = "invalid json"
            mock_response.headers = {}
            mock_response.json.side_effect = Exception("Invalid JSON")
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await configured_client.create_text_post("Test")
            assert result["text"] == "invalid json"

    @pytest.mark.asyncio
    async def test_create_text_post_error_without_json(self, configured_client):
        """Test text post creation error when response can't be parsed as JSON"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_response.json.side_effect = Exception("Invalid JSON")
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with pytest.raises(LinkedInAPIError, match="LinkedIn API error.*Bad Request"):
                await configured_client.create_text_post("Test")

    @pytest.mark.asyncio
    async def test_create_text_post_http_error(self, configured_client):
        """Test text post creation when HTTPError occurs"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()

            import httpx

            mock_client.post = AsyncMock(side_effect=httpx.HTTPError("Connection failed"))
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            with pytest.raises(LinkedInAPIError, match="HTTP error while posting to LinkedIn"):
                await configured_client.create_text_post("Test")


class TestImagePostEdgeCases:
    """Test image post edge cases"""

    @pytest.mark.asyncio
    async def test_create_image_post_missing_upload_method(self):
        """Test image post creation when upload_image method is missing"""
        # Create a client without MediaAPIMixin (hypothetically)
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )

        # Create a minimal client that doesn't have upload_image
        class MinimalClient:
            def __init__(self, config):
                self.config = config
                self.access_token = config.linkedin_access_token
                self.person_urn = config.linkedin_person_urn

            def _get_headers(self, use_rest_api=False):
                return {}

        from chuk_mcp_linkedin.api.posts import PostsAPIMixin

        # Mix in PostsAPIMixin but not MediaAPIMixin
        class TestClient(PostsAPIMixin, MinimalClient):
            pass

        client = TestClient(config)

        with pytest.raises(LinkedInAPIError, match="upload_image method not available"):
            await client.create_image_post("Test", "test.jpg")


class TestMultiImagePostValidation:
    """Test multi-image post validation"""

    @pytest.mark.asyncio
    async def test_create_multi_image_post_too_few_images(self, configured_client):
        """Test multi-image post with less than 2 images"""
        with pytest.raises(LinkedInAPIError, match="at least 2 images"):
            await configured_client.create_multi_image_post("Test", ["img1.jpg"])

    @pytest.mark.asyncio
    async def test_create_multi_image_post_too_many_images(self, configured_client):
        """Test multi-image post with more than 20 images"""
        images = [f"img{i}.jpg" for i in range(21)]
        with pytest.raises(LinkedInAPIError, match="maximum 20 images"):
            await configured_client.create_multi_image_post("Test", images)

    @pytest.mark.asyncio
    async def test_create_multi_image_post_missing_upload_method(self):
        """Test multi-image post when upload_image method is missing"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )

        class MinimalClient:
            def __init__(self, config):
                self.config = config
                self.access_token = config.linkedin_access_token
                self.person_urn = config.linkedin_person_urn

            def _get_headers(self, use_rest_api=False):
                return {}

        from chuk_mcp_linkedin.api.posts import PostsAPIMixin

        class TestClient(PostsAPIMixin, MinimalClient):
            pass

        client = TestClient(config)

        with pytest.raises(LinkedInAPIError, match="upload_image method not available"):
            await client.create_multi_image_post("Test", ["img1.jpg", "img2.jpg"])

    @pytest.mark.asyncio
    async def test_create_multi_image_post_mismatched_alt_texts(self, configured_client):
        """Test multi-image post with mismatched number of alt texts"""
        with pytest.raises(LinkedInAPIError, match="Number of alt texts must match"):
            await configured_client.create_multi_image_post(
                "Test", ["img1.jpg", "img2.jpg"], alt_texts=["Alt 1"]
            )


class TestVideoPostEdgeCases:
    """Test video post edge cases"""

    @pytest.mark.asyncio
    async def test_create_video_post_missing_upload_method(self):
        """Test video post when upload_video method is missing"""
        config = LinkedInConfig(
            linkedin_access_token="test_token",
            linkedin_person_urn="urn:li:person:test123",
        )

        class MinimalClient:
            def __init__(self, config):
                self.config = config
                self.access_token = config.linkedin_access_token
                self.person_urn = config.linkedin_person_urn

            def _get_headers(self, use_rest_api=False):
                return {}

        from chuk_mcp_linkedin.api.posts import PostsAPIMixin

        class TestClient(PostsAPIMixin, MinimalClient):
            pass

        client = TestClient(config)

        with pytest.raises(LinkedInAPIError, match="upload_video method not available"):
            await client.create_video_post("Test", "test.mp4")


class TestPollPostValidation:
    """Test poll post validation"""

    @pytest.mark.asyncio
    async def test_create_poll_post_question_too_long(self, configured_client):
        """Test poll post with question exceeding 140 characters"""
        long_question = "x" * 141
        with pytest.raises(LinkedInAPIError, match="Poll question too long"):
            await configured_client.create_poll_post(
                "Test", long_question, ["Option A", "Option B"]
            )

    @pytest.mark.asyncio
    async def test_create_poll_post_too_few_options(self, configured_client):
        """Test poll post with less than 2 options"""
        with pytest.raises(LinkedInAPIError, match="at least 2 options"):
            await configured_client.create_poll_post("Test", "Question?", ["Option A"])

    @pytest.mark.asyncio
    async def test_create_poll_post_too_many_options(self, configured_client):
        """Test poll post with more than 4 options"""
        options = ["A", "B", "C", "D", "E"]
        with pytest.raises(LinkedInAPIError, match="maximum 4 options"):
            await configured_client.create_poll_post("Test", "Question?", options)

    @pytest.mark.asyncio
    async def test_create_poll_post_option_too_long(self, configured_client):
        """Test poll post with option exceeding 30 characters"""
        long_option = "x" * 31
        with pytest.raises(LinkedInAPIError, match="Option.*too long"):
            await configured_client.create_poll_post("Test", "Question?", ["Option A", long_option])

    @pytest.mark.asyncio
    async def test_create_poll_post_invalid_duration(self, configured_client):
        """Test poll post with invalid duration"""
        with pytest.raises(LinkedInAPIError, match="Invalid duration"):
            await configured_client.create_poll_post(
                "Test", "Question?", ["A", "B"], duration="INVALID"
            )


class TestCreatePostHelper:
    """Test _create_post helper method"""

    @pytest.mark.asyncio
    async def test_create_post_response_without_json(self, configured_client):
        """Test _create_post when response has no JSON content"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.content = b""
            mock_response.headers = {"x-restli-id": "urn:li:share:12345"}
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            payload = {
                "author": "urn:li:person:test123",
                "commentary": "Test",
                "visibility": "PUBLIC",
            }
            result = await configured_client._create_post(payload)
            assert result["id"] == "urn:li:share:12345"

    @pytest.mark.asyncio
    async def test_create_post_response_invalid_json(self, configured_client):
        """Test _create_post when response has invalid JSON"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.content = b"invalid json"
            mock_response.text = "invalid json"
            mock_response.headers = {}
            mock_response.json.side_effect = Exception("Invalid JSON")
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            payload = {
                "author": "urn:li:person:test123",
                "commentary": "Test",
            }
            result = await configured_client._create_post(payload)
            assert result["text"] == "invalid json"

    @pytest.mark.asyncio
    async def test_create_post_error_without_json(self, configured_client):
        """Test _create_post error when response can't be parsed as JSON"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_response.json.side_effect = Exception("Invalid JSON")
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            payload = {"author": "urn:li:person:test123"}
            with pytest.raises(LinkedInAPIError, match="LinkedIn API error.*Bad Request"):
                await configured_client._create_post(payload)

    @pytest.mark.asyncio
    async def test_create_post_http_error(self, configured_client):
        """Test _create_post when HTTPError occurs"""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()

            import httpx

            mock_client.post = AsyncMock(side_effect=httpx.HTTPError("Connection failed"))
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            payload = {"author": "urn:li:person:test123"}
            with pytest.raises(LinkedInAPIError, match="HTTP error while posting to LinkedIn"):
                await configured_client._create_post(payload)
