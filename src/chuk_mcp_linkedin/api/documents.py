"""
LinkedIn Documents API operations.

Handles uploading documents and creating posts with document attachments.
"""

from typing import Dict, Any, Optional
from pathlib import Path
import httpx
from .errors import LinkedInAPIError


class DocumentsAPIMixin:
    """
    Mixin providing LinkedIn Documents API operations.

    Requires the class to have:
    - self.access_token
    - self.person_urn
    - self._get_headers(use_rest_api=True)
    """

    async def upload_document(
        self,
        file_path: str | Path,
        title: Optional[str] = None,
    ) -> str:
        """
        Upload a document to LinkedIn.

        This is a multi-step process:
        1. Initialize upload (get upload URL and document URN)
        2. Upload file to the provided URL
        3. Return document URN for use in posts

        Args:
            file_path: Path to document file (PDF, PPTX, DOC, DOCX)
            title: Optional document title

        Returns:
            Document URN (e.g., urn:li:document:ABC123)

        Raises:
            LinkedInAPIError: If upload fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/documents-api
        """
        if not self.access_token or not self.person_urn:
            raise LinkedInAPIError(
                "LinkedIn API not configured. Set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN"
            )

        file_path = Path(file_path)
        if not file_path.exists():
            raise LinkedInAPIError(f"File not found: {file_path}")

        # Validate file type
        supported_types = {'.pdf', '.ppt', '.pptx', '.doc', '.docx'}
        if file_path.suffix.lower() not in supported_types:
            raise LinkedInAPIError(
                f"Unsupported file type: {file_path.suffix}. "
                f"Supported: {', '.join(supported_types)}"
            )

        # Validate file size (100MB limit)
        file_size = file_path.stat().st_size
        max_size = 100 * 1024 * 1024  # 100MB
        if file_size > max_size:
            raise LinkedInAPIError(
                f"File too large: {file_size / 1024 / 1024:.1f}MB. "
                f"Maximum: 100MB"
            )

        async with httpx.AsyncClient() as client:
            # Step 1: Initialize upload
            init_url = "https://api.linkedin.com/rest/documents?action=initializeUpload"
            init_payload = {
                "initializeUploadRequest": {
                    "owner": self.person_urn
                }
            }

            try:
                response = await client.post(
                    init_url,
                    json=init_payload,
                    headers=self._get_headers(use_rest_api=True),
                    timeout=30.0
                )

                if response.status_code not in (200, 201):
                    raise LinkedInAPIError(
                        f"Failed to initialize document upload: {response.status_code} - {response.text}"
                    )

                init_data = response.json()
                upload_url = init_data["value"]["uploadUrl"]
                document_urn = init_data["value"]["document"]

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error during upload initialization: {str(e)}")

            # Step 2: Upload file
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()

                # Determine MIME type
                import mimetypes
                mime_type, _ = mimetypes.guess_type(str(file_path))
                if not mime_type:
                    # Default MIME types for supported formats
                    mime_types = {
                        '.pdf': 'application/pdf',
                        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                        '.ppt': 'application/vnd.ms-powerpoint',
                        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        '.doc': 'application/msword'
                    }
                    mime_type = mime_types.get(file_path.suffix.lower(), 'application/octet-stream')

                upload_response = await client.put(
                    upload_url,
                    content=file_data,
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": mime_type,
                    },
                    timeout=120.0  # Longer timeout for file upload
                )

                if upload_response.status_code not in (200, 201):
                    raise LinkedInAPIError(
                        f"Failed to upload document: {upload_response.status_code} - {upload_response.text}"
                    )

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error during file upload: {str(e)}")

        return document_urn

    async def create_document_post(
        self,
        text: str,
        document_path: str | Path,
        document_title: Optional[str] = None,
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a post with an attached document on LinkedIn.

        Args:
            text: Post commentary/text
            document_path: Path to document file
            document_title: Optional title for the document
            visibility: Post visibility ("PUBLIC", "CONNECTIONS", "LOGGED_IN")

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api
        """
        # Step 1: Upload document
        document_urn = await self.upload_document(document_path, document_title)

        # Step 2: Create post with document
        file_path = Path(document_path)
        title = document_title or file_path.name

        payload = {
            "author": self.person_urn,
            "commentary": text,
            "visibility": visibility,
            "content": {
                "media": {
                    "id": document_urn,
                    "title": title
                }
            },
            "lifecycleState": "PUBLISHED",
            "distribution": {
                "feedDistribution": "MAIN_FEED"
            }
        }

        url = "https://api.linkedin.com/rest/posts"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(use_rest_api=True),
                    timeout=30.0
                )

                if response.status_code not in (200, 201):
                    error_msg = f"LinkedIn API error: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data}"
                    except Exception:
                        error_msg += f" - {response.text}"
                    raise LinkedInAPIError(error_msg)

                # Handle response - may be JSON or empty
                response_data = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers)
                }

                # Try to parse JSON response if present
                if response.content:
                    try:
                        response_data.update(response.json())
                    except Exception:
                        response_data["text"] = response.text

                # Extract post ID from headers (LinkedIn returns it in x-restli-id)
                if "x-restli-id" in response.headers:
                    response_data["id"] = response.headers["x-restli-id"]

                return response_data

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error while posting to LinkedIn: {str(e)}")
