# src/chuk_mcp_linkedin/tools/publishing_tools.py
"""
Publishing tools for LinkedIn API integration.

Handles actual posting to LinkedIn via the API.
"""

import json
from typing import Any, Dict


def register_publishing_tools(mcp: Any, manager: Any, linkedin_client: Any) -> Dict[str, Any]:
    """Register publishing tools with the MCP server"""

    from ..api import LinkedInAPIError, config as linkedin_config

    @mcp.tool  # type: ignore[misc]
    async def linkedin_publish(visibility: str = "PUBLIC", dry_run: bool = False) -> str:
        """
        Publish current draft to LinkedIn.

        Args:
            visibility: Post visibility (PUBLIC or CONNECTIONS)
            dry_run: Preview what would be published without actually posting

        Returns:
            Success message or error
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Check if configured
        if not linkedin_config.is_configured():
            missing = linkedin_config.get_missing_config()
            return (
                f"LinkedIn API not configured. Missing: {', '.join(missing)}\n\n"
                "Please set these environment variables in .env file.\n"
                "See .env.example for details."
            )

        # Get post text
        post_text = draft.content.get("composed_text") or draft.content.get("commentary", "")
        if not post_text:
            return "No post content to publish. Add content first or compose the post."

        # Dry run - show what would be published
        if dry_run:
            return (
                f"DRY RUN - Would publish to LinkedIn:\n\n"
                f"Visibility: {visibility}\n"
                f"Length: {len(post_text)} characters\n\n"
                f"Content:\n{post_text[:500]}{'...' if len(post_text) > 500 else ''}"
            )

        # Safety check
        if not linkedin_config.enable_publishing:
            return (
                "Publishing is disabled. Set ENABLE_PUBLISHING=true in .env to enable.\n"
                "This is a safety switch to prevent accidental posts during testing."
            )

        # Publish!
        try:
            result = await linkedin_client.create_text_post(text=post_text, visibility=visibility)

            # Extract post ID from response
            post_id = result.get("id", "unknown")

            return (
                f"Successfully published to LinkedIn!\n\n"
                f"Post ID: {post_id}\n"
                f"Visibility: {visibility}\n"
                f"Characters: {len(post_text)}"
            )

        except LinkedInAPIError as e:
            return f"Failed to publish: {str(e)}"

    @mcp.tool  # type: ignore[misc]
    async def linkedin_test_connection() -> str:
        """
        Test LinkedIn API connection and configuration.

        Returns:
            Connection status
        """
        is_valid = await linkedin_client.test_connection()

        if is_valid:
            return (
                "LinkedIn API connection successful!\n\n"
                f"Access token: configured\n"
                f"Person URN: {linkedin_config.linkedin_person_urn}\n"
                f"Publishing enabled: {linkedin_config.enable_publishing}"
            )
        else:
            is_configured, missing = linkedin_client.validate_config()
            if not is_configured:
                return (
                    f"LinkedIn API not configured. Missing: {', '.join(missing)}\n\n"
                    "Please set these environment variables in .env file."
                )
            else:
                return "LinkedIn API connection failed. Check your access token and person URN."

    @mcp.tool  # type: ignore[misc]
    async def linkedin_get_config_status() -> str:
        """
        Get LinkedIn API configuration status.

        Returns:
            JSON with configuration details
        """
        is_configured = linkedin_config.is_configured()
        missing = linkedin_config.get_missing_config()

        status = {
            "configured": is_configured,
            "access_token": ("✓ set" if linkedin_config.linkedin_access_token else "✗ missing"),
            "person_urn": linkedin_config.linkedin_person_urn or "✗ missing",
            "publishing_enabled": linkedin_config.enable_publishing,
            "missing_fields": missing,
        }

        return json.dumps(status, indent=2)

    return {
        "linkedin_publish": linkedin_publish,
        "linkedin_test_connection": linkedin_test_connection,
        "linkedin_get_config_status": linkedin_get_config_status,
    }
