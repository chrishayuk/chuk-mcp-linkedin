"""
LinkedIn API base client.

Handles authentication, configuration, and common functionality.
"""

from typing import Dict, Optional
import httpx
from .config import LinkedInConfig


class LinkedInClient:
    """
    Base client for interacting with LinkedIn API.

    Provides authentication, headers, and configuration management.
    Specific operations (posts, documents) are added via composition.
    """

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

    def _get_headers(self, use_rest_api: bool = False) -> Dict[str, str]:
        """
        Get headers for LinkedIn API requests.

        Args:
            use_rest_api: Whether to include Linkedin-Version header for new REST API

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

        # Newer REST API endpoints require Linkedin-Version header
        if use_rest_api:
            headers["Linkedin-Version"] = "202502"

        return headers

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
                    url, headers={"Authorization": f"Bearer {self.access_token}"}, timeout=10.0
                )
                return response.status_code == 200

        except Exception:
            return False
