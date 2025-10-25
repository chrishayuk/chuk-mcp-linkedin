# src/chuk_mcp_linkedin/tools/publishing_tools.py
"""
Publishing tools for LinkedIn API integration.

Handles actual posting to LinkedIn via the API with OAuth authentication.
"""

from typing import Any, Dict, Optional


def register_publishing_tools(mcp: Any, manager: Any, linkedin_client: Any) -> Dict[str, Any]:
    """Register publishing tools with the MCP server"""

    from ..api import LinkedInAPIError, config as linkedin_config

    @mcp.tool  # type: ignore[misc]
    async def linkedin_publish(
        visibility: str = "PUBLIC",
        dry_run: bool = False,
        _linkedin_access_token: Optional[str] = None,
    ) -> str:
        """
        Publish current draft to LinkedIn.

        Args:
            visibility: Post visibility (PUBLIC or CONNECTIONS)
            dry_run: Preview what would be published without actually posting
            _linkedin_access_token: LinkedIn access token (injected by OAuth middleware)

        Returns:
            Success message or error
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Check if OAuth token is provided
        if not _linkedin_access_token:
            return (
                "Authentication required. Please authorize with LinkedIn using OAuth.\n\n"
                "The MCP client must provide a valid access token via the Authorization header."
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

        # Create a LinkedIn client with the OAuth access token
        from ..api import LinkedInClient

        oauth_client = LinkedInClient()
        oauth_client.access_token = _linkedin_access_token
        oauth_client.person_urn = linkedin_config.linkedin_person_urn

        # Publish!
        try:
            result = await oauth_client.create_text_post(text=post_text, visibility=visibility)

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
    async def linkedin_test_connection(_linkedin_access_token: Optional[str] = None) -> str:
        """
        Test LinkedIn API connection and configuration.

        Args:
            _linkedin_access_token: LinkedIn access token (injected by OAuth middleware)

        Returns:
            Connection status
        """
        # Check if OAuth token is provided
        if not _linkedin_access_token:
            return (
                "Authentication required. Please authorize with LinkedIn using OAuth.\n\n"
                "The MCP client must provide a valid access token via the Authorization header."
            )

        # Create a LinkedIn client with the OAuth access token
        from ..api import LinkedInClient

        oauth_client = LinkedInClient()
        oauth_client.access_token = _linkedin_access_token

        is_valid = await oauth_client.test_connection()

        if is_valid:
            return (
                "LinkedIn API connection successful!\n\n"
                f"Access token: validated via OAuth\n"
                f"Token length: {len(_linkedin_access_token)} characters"
            )
        else:
            return "LinkedIn API connection failed. Please re-authorize with LinkedIn."

    return {
        "linkedin_publish": linkedin_publish,
        "linkedin_test_connection": linkedin_test_connection,
    }
