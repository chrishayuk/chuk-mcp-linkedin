"""
LinkedIn API integration module.

Handles authentication, configuration, and API communication with LinkedIn.
"""

from .config import LinkedInConfig, config
from .linkedin_client import LinkedInClient, LinkedInAPIError

__all__ = [
    "LinkedInConfig",
    "config",
    "LinkedInClient",
    "LinkedInAPIError",
]
