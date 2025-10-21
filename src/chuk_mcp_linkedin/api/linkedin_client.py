"""
LinkedIn API client for posting content.

Handles authentication and posting to LinkedIn via their REST API.
"""

from typing import Dict, Any, Optional
import httpx
from .config import LinkedInConfig


class LinkedInAPIError(Exception):
    """Exception raised for LinkedIn API errors"""
    pass


class LinkedInClient:
    """Client for interacting with LinkedIn API"""

    def __init__(self, config: Optional[LinkedInConfig] = None):
        """
        Initialize LinkedIn API client.

        Args:
            config: LinkedIn configuration (uses default if not provided)
        """
        from .config import config as default_config
        self.config = config or default_config

        self.base_url = self.config.linkedin_api_base_url
        self.access_token = self.config.linkedin_access_token
        self.person_urn = self.config.linkedin_person_urn

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for LinkedIn API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    async def create_text_post(
        self,
        text: str,
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a text post on LinkedIn.

        Args:
            text: Post text/commentary
            visibility: Post visibility ("PUBLIC" or "CONNECTIONS")

        Returns:
            API response with post details

        Raises:
            LinkedInAPIError: If API call fails
        """
        if not self.access_token or not self.person_urn:
            raise LinkedInAPIError(
                "LinkedIn API not configured. Set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN"
            )

        # Build request payload
        payload = {
            "author": self.person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

        # Make API request
        url = f"{self.base_url}/ugcPosts"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=30.0
                )

                # Check for errors
                if response.status_code not in (200, 201):
                    error_msg = f"LinkedIn API error: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('message', '')}"
                    except Exception:
                        error_msg += f" - {response.text}"
                    raise LinkedInAPIError(error_msg)

                return response.json()

            except httpx.HTTPError as e:
                raise LinkedInAPIError(f"HTTP error while posting to LinkedIn: {str(e)}")

    async def create_image_post(
        self,
        text: str,
        image_url: str,
        visibility: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create an image post on LinkedIn.

        Note: This is a simplified version. Full implementation requires
        uploading the image first using the LinkedIn assets API.

        Args:
            text: Post text/commentary
            image_url: URL to the image (must be publicly accessible)
            visibility: Post visibility

        Returns:
            API response
        """
        # TODO: Implement image upload flow
        # 1. Register upload
        # 2. Upload image to LinkedIn
        # 3. Create share with uploaded asset
        raise NotImplementedError(
            "Image posts require multi-step upload process. Coming soon!"
        )

    def validate_config(self) -> tuple[bool, list[str]]:
        """
        Validate LinkedIn API configuration.

        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        missing = []

        if not self.access_token:
            missing.append("LINKEDIN_ACCESS_TOKEN")
        if not self.person_urn:
            missing.append("LINKEDIN_PERSON_URN")

        return (len(missing) == 0, missing)

    async def test_connection(self) -> bool:
        """
        Test the LinkedIn API connection by verifying credentials.

        Returns:
            True if connection is valid, False otherwise
        """
        if not self.access_token:
            return False

        try:
            # Test with userinfo endpoint (requires openid scope)
            url = "https://api.linkedin.com/v2/userinfo"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10.0
                )
                return response.status_code == 200

        except Exception:
            return False
