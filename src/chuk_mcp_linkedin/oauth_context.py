# src/chuk_mcp_linkedin/oauth_context.py
"""
OAuth context for passing authentication through MCP request handling.

Uses context variables to make OAuth tokens available to tools during request processing.
"""

from contextvars import ContextVar
from typing import Optional

# Context variable to hold the current LinkedIn access token
linkedin_token_var: ContextVar[Optional[str]] = ContextVar("linkedin_token", default=None)


def set_linkedin_token(token: str) -> None:
    """Set the LinkedIn access token for the current request context."""
    linkedin_token_var.set(token)


def get_linkedin_token() -> Optional[str]:
    """Get the LinkedIn access token from the current request context."""
    return linkedin_token_var.get()


def clear_linkedin_token() -> None:
    """Clear the LinkedIn access token from the current request context."""
    linkedin_token_var.set(None)
