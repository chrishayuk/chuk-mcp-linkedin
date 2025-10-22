"""
Configuration management for LinkedIn MCP server.

Handles environment variables and settings for LinkedIn API integration.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LinkedInConfig(BaseSettings):
    """LinkedIn API configuration from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LinkedIn OAuth credentials
    linkedin_client_id: Optional[str] = Field(
        default=None,
        description="LinkedIn OAuth Client ID",
    )

    linkedin_client_secret: Optional[str] = Field(
        default=None,
        description="LinkedIn OAuth Client Secret",
    )

    # Access token (obtained through OAuth flow)
    linkedin_access_token: Optional[str] = Field(
        default=None,
        description="LinkedIn OAuth Access Token",
    )

    # Person URN (user's LinkedIn URN)
    linkedin_person_urn: Optional[str] = Field(
        default=None,
        description="LinkedIn Person URN (e.g., urn:li:person:ABC123)",
    )

    # API settings
    linkedin_api_base_url: str = Field(
        default="https://api.linkedin.com/v2",
        description="LinkedIn API base URL",
    )

    # Feature flags
    enable_publishing: bool = Field(
        default=False,
        description="Enable actual publishing to LinkedIn (safety switch)",
    )

    def is_configured(self) -> bool:
        """Check if LinkedIn API is properly configured"""
        return bool(self.linkedin_access_token and self.linkedin_person_urn)

    def get_missing_config(self) -> list[str]:
        """Get list of missing required configuration"""
        missing = []
        if not self.linkedin_access_token:
            missing.append("LINKEDIN_ACCESS_TOKEN")
        if not self.linkedin_person_urn:
            missing.append("LINKEDIN_PERSON_URN")
        return missing


# Global config instance
config = LinkedInConfig()
