"""
LinkedIn Media API operations.

Handles uploading images and videos to LinkedIn.
"""

from typing import Optional
from pathlib import Path
import httpx
from .errors import LinkedInAPIError


class MediaAPIMixin:
    """
    Mixin providing LinkedIn Media API operations (images and videos).

    Requires the class to have:
    - self.access_token
    - self.person_urn
    - self._get_headers(use_rest_api=True)
    """

    async def upload_image(
        self,
        file_path: str | Path,
        alt_text: Optional[str] = None,
    ) -> str:
        """
        Upload an image to LinkedIn.

        This is a multi-step process:
        1. Initialize upload (get upload URL and image URN)
        2. Upload file to the provided URL
        3. Return image URN for use in posts

        Args:
            file_path: Path to image file (JPG, PNG, GIF)
            alt_text: Optional alt text for accessibility

        Returns:
            Image URN (e.g., urn:li:image:ABC123)

        Raises:
            LinkedInAPIError: If upload fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/images-api
        """
        if not self.access_token or not self.person_urn:
            raise LinkedInAPIError(
                "LinkedIn API not configured. Set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN"
            )

        file_path = Path(file_path)
        if not file_path.exists():
            raise LinkedInAPIError(f"File not found: {file_path}")

        # Validate file type
        supported_types = {".jpg", ".jpeg", ".png", ".gif"}
        if file_path.suffix.lower() not in supported_types:
            raise LinkedInAPIError(
                f"Unsupported file type: {file_path.suffix}. "
                f"Supported: {', '.join(supported_types)}"
            )

        # Validate file size (images must have < 36,152,320 pixels)
        # We'll do basic size check, LinkedIn validates pixel count server-side
        file_size = file_path.stat().st_size
        max_size = 10 * 1024 * 1024  # 10MB reasonable limit
        if file_size > max_size:
            raise LinkedInAPIError(
                f"File too large: {file_size / 1024 / 1024:.1f}MB. "
                f"Keep under 10MB for best results"
            )

        async with httpx.AsyncClient() as client:
            # Step 1: Initialize upload
            init_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
            init_payload = {"initializeUploadRequest": {"owner": self.person_urn}}

            try:
                response = await client.post(
                    init_url,
                    json=init_payload,
                    headers=self._get_headers(use_rest_api=True),
                    timeout=30.0,
                )

                if response.status_code not in (200, 201):
                    raise LinkedInAPIError(
                        f"Failed to initialize image upload: {response.status_code} - {response.text}"
                    )

                init_data = response.json()
                upload_url = init_data["value"]["uploadUrl"]
                image_urn = init_data["value"]["image"]

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error during upload initialization: {str(e)}")

            # Step 2: Upload image
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()

                # Determine MIME type
                import mimetypes

                mime_type, _ = mimetypes.guess_type(str(file_path))
                if not mime_type:
                    mime_types = {
                        ".jpg": "image/jpeg",
                        ".jpeg": "image/jpeg",
                        ".png": "image/png",
                        ".gif": "image/gif",
                    }
                    mime_type = mime_types.get(file_path.suffix.lower(), "application/octet-stream")

                upload_response = await client.put(
                    upload_url,
                    content=file_data,
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": mime_type,
                    },
                    timeout=120.0,
                )

                if upload_response.status_code not in (200, 201):
                    raise LinkedInAPIError(
                        f"Failed to upload image: {upload_response.status_code} - {upload_response.text}"
                    )

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error during file upload: {str(e)}")

        return image_urn

    async def upload_video(
        self,
        file_path: str | Path,
        title: Optional[str] = None,
    ) -> str:
        """
        Upload a video to LinkedIn.

        This is a multi-step process:
        1. Initialize upload (get upload URL and video URN)
        2. Upload file to the provided URL
        3. Finalize the upload
        4. Wait for video to be processed by LinkedIn
        5. Return video URN for use in posts

        Args:
            file_path: Path to video file (MP4)
            title: Optional video title

        Returns:
            Video URN (e.g., urn:li:video:ABC123)

        Raises:
            LinkedInAPIError: If upload or processing fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/videos-api

        Notes:
            - Format: MP4 only
            - Length: 3 seconds to 30 minutes
            - Size: 75kb - 500MB
            - Processing time: Usually 5-30 seconds depending on video size
        """
        if not self.access_token or not self.person_urn:
            raise LinkedInAPIError(
                "LinkedIn API not configured. Set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN"
            )

        file_path = Path(file_path)
        if not file_path.exists():
            raise LinkedInAPIError(f"File not found: {file_path}")

        # Validate file type (MP4 only)
        if file_path.suffix.lower() != ".mp4":
            raise LinkedInAPIError(
                f"Unsupported file type: {file_path.suffix}. " f"LinkedIn only supports MP4 videos"
            )

        # Validate file size (75kb - 500MB)
        file_size = file_path.stat().st_size
        min_size = 75 * 1024  # 75kb
        max_size = 500 * 1024 * 1024  # 500MB

        if file_size < min_size:
            raise LinkedInAPIError(f"Video too small: {file_size / 1024:.1f}KB. Minimum: 75KB")
        if file_size > max_size:
            raise LinkedInAPIError(
                f"Video too large: {file_size / 1024 / 1024:.1f}MB. Maximum: 500MB"
            )

        async with httpx.AsyncClient() as client:
            # Step 1: Initialize upload
            init_url = "https://api.linkedin.com/rest/videos?action=initializeUpload"
            init_payload = {
                "initializeUploadRequest": {
                    "owner": self.person_urn,
                    "fileSizeBytes": file_size,
                    "uploadCaptions": False,
                    "uploadThumbnail": False,
                }
            }

            try:
                response = await client.post(
                    init_url,
                    json=init_payload,
                    headers=self._get_headers(use_rest_api=True),
                    timeout=30.0,
                )

                if response.status_code not in (200, 201):
                    raise LinkedInAPIError(
                        f"Failed to initialize video upload: {response.status_code} - {response.text}"
                    )

                init_data = response.json()

                # Video API returns uploadInstructions (array), not direct uploadUrl
                try:
                    video_urn = init_data["value"]["video"]
                    upload_instructions = init_data["value"]["uploadInstructions"]
                    upload_token = init_data["value"].get("uploadToken", "")

                    # For single-part upload, use the first (and only) instruction
                    if not upload_instructions:
                        raise LinkedInAPIError("No upload instructions received from LinkedIn")

                    upload_url = upload_instructions[0]["uploadUrl"]
                except KeyError as e:
                    raise LinkedInAPIError(
                        f"Unexpected response structure from LinkedIn video API. "
                        f"Missing key: {str(e)}. Response: {init_data}"
                    )

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error during upload initialization: {str(e)}")

            # Step 2: Upload video
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()

                upload_response = await client.put(
                    upload_url,
                    content=file_data,
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "video/mp4",
                    },
                    timeout=300.0,  # 5 minutes for video upload
                )

                if upload_response.status_code not in (200, 201):
                    raise LinkedInAPIError(
                        f"Failed to upload video: {upload_response.status_code} - {upload_response.text}"
                    )

                # Get ETag from response headers
                etag = upload_response.headers.get("ETag", "").strip('"')

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error during file upload: {str(e)}")

            # Step 3: Finalize upload
            try:
                finalize_url = "https://api.linkedin.com/rest/videos?action=finalizeUpload"
                finalize_payload = {
                    "finalizeUploadRequest": {
                        "video": video_urn,
                        "uploadToken": upload_token,
                        "uploadedPartIds": [etag] if etag else [],
                    }
                }

                finalize_response = await client.post(
                    finalize_url,
                    json=finalize_payload,
                    headers=self._get_headers(use_rest_api=True),
                    timeout=30.0,
                )

                if finalize_response.status_code not in (200, 201):
                    raise LinkedInAPIError(
                        f"Failed to finalize video upload: {finalize_response.status_code} - {finalize_response.text}"
                    )

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error during video finalization: {str(e)}")

            # Step 4: Wait for video processing
            # LinkedIn processes videos asynchronously after finalization
            # For small videos, this usually takes 5-15 seconds
            # We'll wait a reasonable amount of time before proceeding
            import asyncio

            wait_time = 10  # Wait 10 seconds for processing

            await asyncio.sleep(wait_time)

        return video_urn
