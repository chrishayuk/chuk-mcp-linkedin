# src/chuk_mcp_linkedin/api/posts.py
"""
LinkedIn Posts API operations.

Handles creating text posts, image posts, video posts, and other post types.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import httpx
from .errors import LinkedInAPIError


class PostsAPIMixin:
    """
    Mixin providing LinkedIn Posts API operations.

    Requires the class to have:
    - self.access_token
    - self.person_urn
    - self._get_headers(use_rest_api=True)
    """

    async def create_text_post(
        self,
        text: str,
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a text post on LinkedIn using the Posts API.

        Args:
            text: Post text/commentary
            visibility: Post visibility ("PUBLIC", "CONNECTIONS", or "LOGGED_IN")

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api
        """
        if not self.access_token or not self.person_urn:  # type: ignore[attr-defined]
            raise LinkedInAPIError(
                "LinkedIn API not configured. Access token and Person URN required (obtained via OAuth)"
            )

        # Build request payload using new Posts API format
        payload = {
            "author": self.person_urn,  # type: ignore[attr-defined]
            "commentary": text,
            "visibility": visibility,
            "lifecycleState": "PUBLISHED",
            "distribution": {"feedDistribution": "MAIN_FEED"},
        }

        # Use new Posts API endpoint
        url = "https://api.linkedin.com/rest/posts"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(use_rest_api=True),  # type: ignore[attr-defined]
                    timeout=30.0,
                )

                # Check for errors
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
                    "headers": dict(response.headers),
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

    async def create_image_post(
        self,
        text: str,
        image_path: str | Path,
        alt_text: Optional[str] = None,
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a post with a single image on LinkedIn.

        Args:
            text: Post text/commentary
            image_path: Path to image file (JPG, PNG, GIF)
            alt_text: Optional alt text for accessibility
            visibility: Post visibility ("PUBLIC", "CONNECTIONS", or "LOGGED_IN")

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/images-api
        """
        # Step 1: Upload image (requires MediaAPIMixin)
        if not hasattr(self, "upload_image"):
            raise LinkedInAPIError(
                "upload_image method not available. Ensure MediaAPIMixin is included."
            )

        image_urn = await self.upload_image(image_path, alt_text)

        # Step 2: Create post with image
        payload = {
            "author": self.person_urn,  # type: ignore[attr-defined]
            "commentary": text,
            "visibility": visibility,
            "content": {"media": {"id": image_urn, "altText": alt_text or ""}},
            "lifecycleState": "PUBLISHED",
            "distribution": {"feedDistribution": "MAIN_FEED"},
        }

        return await self._create_post(payload)

    async def create_multi_image_post(
        self,
        text: str,
        image_paths: List[str | Path],
        alt_texts: Optional[List[str]] = None,
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a carousel post with multiple images on LinkedIn.

        Args:
            text: Post text/commentary
            image_paths: List of paths to image files (2-20 images)
            alt_texts: Optional list of alt texts for each image
            visibility: Post visibility ("PUBLIC", "CONNECTIONS", or "LOGGED_IN")

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/multiimage-post-api

        Notes:
            - Minimum 2 images, maximum 20 images
            - Only for non-sponsored posts
        """
        # Validate image count
        if len(image_paths) < 2:
            raise LinkedInAPIError("Multi-image posts require at least 2 images")
        if len(image_paths) > 20:
            raise LinkedInAPIError("Multi-image posts support maximum 20 images")

        # Upload all images
        if not hasattr(self, "upload_image"):
            raise LinkedInAPIError(
                "upload_image method not available. Ensure MediaAPIMixin is included."
            )

        # Prepare alt texts
        if alt_texts is None:
            alt_texts = ["" for _ in image_paths]
        elif len(alt_texts) != len(image_paths):
            raise LinkedInAPIError("Number of alt texts must match number of images")

        # Upload images and build image array
        images = []
        for image_path, alt_text in zip(image_paths, alt_texts):
            image_urn = await self.upload_image(image_path, alt_text)
            images.append({"id": image_urn, "altText": alt_text})

        # Create post with multiple images
        payload = {
            "author": self.person_urn,  # type: ignore[attr-defined]
            "commentary": text,
            "visibility": visibility,
            "content": {"multiImage": {"images": images}},
            "lifecycleState": "PUBLISHED",
            "distribution": {"feedDistribution": "MAIN_FEED"},
        }

        return await self._create_post(payload)

    async def create_video_post(
        self,
        text: str,
        video_path: str | Path,
        title: Optional[str] = None,
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a post with a video on LinkedIn.

        Args:
            text: Post text/commentary
            video_path: Path to video file (MP4 only)
            title: Optional video title
            visibility: Post visibility ("PUBLIC", "CONNECTIONS", or "LOGGED_IN")

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/videos-api

        Notes:
            - Format: MP4 only
            - Length: 3 seconds to 30 minutes
            - Size: 75kb - 500MB
        """
        # Step 1: Upload video (requires MediaAPIMixin)
        if not hasattr(self, "upload_video"):
            raise LinkedInAPIError(
                "upload_video method not available. Ensure MediaAPIMixin is included."
            )

        video_urn = await self.upload_video(video_path, title)

        # Step 2: Create post with video
        file_path = Path(video_path)
        video_title = title or file_path.stem

        payload = {
            "author": self.person_urn,  # type: ignore[attr-defined]
            "commentary": text,
            "visibility": visibility,
            "content": {"media": {"id": video_urn, "title": video_title}},
            "lifecycleState": "PUBLISHED",
            "distribution": {"feedDistribution": "MAIN_FEED"},
        }

        return await self._create_post(payload)

    async def create_poll_post(
        self,
        text: str,
        question: str,
        options: List[str],
        duration: str = "THREE_DAYS",
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a poll post on LinkedIn.

        Args:
            text: Post text/commentary
            question: Poll question (max 140 characters)
            options: List of poll options (2-4 options, max 30 chars each)
            duration: Poll duration - "ONE_DAY", "THREE_DAYS", "ONE_WEEK", or "TWO_WEEKS"
            visibility: Post visibility ("PUBLIC", "CONNECTIONS", or "LOGGED_IN")

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails

        Reference:
            https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/poll-post-api

        Example:
            >>> await client.create_poll_post(
            ...     "Quick question for my network:",
            ...     "What's your favorite programming language?",
            ...     ["Python", "JavaScript", "Go", "Rust"],
            ...     duration="ONE_WEEK"
            ... )

        Notes:
            - Minimum 2 options, maximum 4 options
            - Question max length: 140 characters
            - Option text max length: 30 characters
            - Only non-sponsored posts allowed
        """
        # Validate poll parameters
        if len(question) > 140:
            raise LinkedInAPIError(
                f"Poll question too long: {len(question)} chars. Maximum: 140 characters"
            )

        if len(options) < 2:
            raise LinkedInAPIError("Poll must have at least 2 options")
        if len(options) > 4:
            raise LinkedInAPIError("Poll can have maximum 4 options")

        for i, option in enumerate(options):
            if len(option) > 30:
                raise LinkedInAPIError(
                    f"Option {i + 1} too long: {len(option)} chars. Maximum: 30 characters"
                )

        # Validate duration
        valid_durations = ["ONE_DAY", "THREE_DAYS", "ONE_WEEK", "TWO_WEEKS"]
        if duration not in valid_durations:
            raise LinkedInAPIError(
                f"Invalid duration: {duration}. Valid: {', '.join(valid_durations)}"
            )

        # Build poll options
        poll_options = [{"text": option} for option in options]

        # Create poll post payload
        payload = {
            "author": self.person_urn,  # type: ignore[attr-defined]
            "commentary": text,
            "visibility": visibility,
            "content": {
                "poll": {
                    "question": question,
                    "options": poll_options,
                    "settings": {"duration": duration},
                }
            },
            "lifecycleState": "PUBLISHED",
            "distribution": {"feedDistribution": "MAIN_FEED"},
        }

        return await self._create_post(payload)

    async def _create_post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper to create a post with given payload.

        Args:
            payload: Post payload dict

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails
        """
        url = "https://api.linkedin.com/rest/posts"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(use_rest_api=True),  # type: ignore[attr-defined]
                    timeout=30.0,
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
                    "headers": dict(response.headers),
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
