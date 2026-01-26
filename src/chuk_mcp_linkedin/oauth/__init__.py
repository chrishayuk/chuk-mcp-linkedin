# src/chuk_mcp_linkedin/oauth/__init__.py
"""
LinkedIn OAuth integration.

Uses the generic OAuth implementation from chuk-mcp-server
with LinkedIn-specific provider.
"""

from .linkedin_client import LinkedInOAuthClient
from .provider import LinkedInOAuthProvider
from .keycloak_provider import KeycloakOAuthProvider
from .passthrough_provider import PassthroughOAuthProvider

__all__ = [
    "LinkedInOAuthProvider",
    "LinkedInOAuthClient",
    "KeycloakOAuthProvider",
    "PassthroughOAuthProvider",
]
