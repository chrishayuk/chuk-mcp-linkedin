# src/chuk_mcp_linkedin/tools/publishing_tools.py
"""
Publishing tools for LinkedIn API integration.

Handles actual posting to LinkedIn via the API with OAuth authentication.
"""

from typing import Any, Dict, Optional

from chuk_mcp_server.decorators import requires_auth

from ..manager_factory import get_current_manager


def register_publishing_tools(mcp: Any, linkedin_client: Any) -> Dict[str, Any]:
    """Register publishing tools with the MCP server"""

    from ..api import LinkedInAPIError

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_publish(
        visibility: str = "PUBLIC",
        dry_run: bool = False,
        _external_access_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Publish current draft to LinkedIn.

        Args:
            visibility: Post visibility (PUBLIC or CONNECTIONS)
            dry_run: Preview what would be published without actually posting
            _external_access_token: External OAuth access token (injected by OAuth middleware)

        Returns:
            Dictionary with status, post_id, post_url, visibility, character_count, and author_urn on success,
            or status and error details on failure
        """
        import logging

        logger = logging.getLogger(__name__)
        logger.info(
            f"linkedin_publish called with token: {'present' if _external_access_token else 'MISSING'}"
        )

        manager = get_current_manager()
        draft = manager.get_current_draft()
        if not draft:
            return {
                "status": "error",
                "error": "No active draft",
                "error_type": "no_draft",
            }

        # Protocol handler should have already validated OAuth - this is a safety check
        if not _external_access_token:
            logger.error("linkedin_publish: OAuth token not injected despite @requires_auth!")
            return {
                "status": "error",
                "error": "Authentication required. Please authorize with LinkedIn using OAuth.",
                "error_type": "missing_oauth_token",
            }

        # Get post text
        post_text = draft.content.get("composed_text") or draft.content.get("commentary", "")
        if not post_text:
            return {
                "status": "error",
                "error": "No post content to publish. Add content first or compose the post.",
                "error_type": "missing_content",
            }

        # Dry run - show what would be published
        if dry_run:
            return {
                "status": "dry_run",
                "visibility": visibility,
                "character_count": len(post_text),
                "content_preview": post_text[:500] + ("..." if len(post_text) > 500 else ""),
                "full_content": post_text,
            }

        # Create a LinkedIn client with the OAuth access token
        import httpx

        from ..api import LinkedInClient

        oauth_client = LinkedInClient()
        oauth_client.access_token = _external_access_token

        # Get person URN from LinkedIn API using the OAuth token
        try:
            async with httpx.AsyncClient() as client:
                userinfo_response = await client.get(
                    "https://api.linkedin.com/v2/userinfo",
                    headers={"Authorization": f"Bearer {_external_access_token}"},
                    timeout=10.0,
                )
                userinfo_response.raise_for_status()
                userinfo = userinfo_response.json()
                person_id = userinfo.get("sub")

                if not person_id:
                    return {
                        "status": "error",
                        "error": "Failed to get LinkedIn user profile. The 'sub' field is missing from userinfo.",
                        "error_type": "missing_person_id",
                    }

                # Convert person ID to URN format if needed
                if person_id.startswith("urn:"):
                    person_urn = person_id
                else:
                    person_urn = f"urn:li:person:{person_id}"

                oauth_client.person_urn = person_urn
                logger.info(f"Retrieved person URN from LinkedIn: {person_urn}")

        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to get LinkedIn user profile: {str(e)}",
                "error_type": "userinfo_fetch_failed",
            }

        # Publish!
        try:
            result = await oauth_client.create_text_post(text=post_text, visibility=visibility)

            # Extract post ID from response
            post_id = result.get("id", "unknown")

            # Convert post ID to LinkedIn URL
            # Post ID format: urn:li:share:7390188640271798272
            # URL format: https://www.linkedin.com/feed/update/urn:li:share:7390188640271798272/
            post_url = f"https://www.linkedin.com/feed/update/{post_id}/"

            return {
                "status": "published",
                "post_id": post_id,
                "post_url": post_url,
                "visibility": visibility,
                "character_count": len(post_text),
                "author_urn": person_urn,
            }

        except LinkedInAPIError as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": "linkedin_api_error",
            }

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_test_connection(
        _external_access_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Test LinkedIn API connection and configuration.

        Args:
            _external_access_token: External OAuth access token (injected by OAuth middleware)

        Returns:
            Dictionary with connection status and user profile information (name, email, person_id, person_urn)
            on success, or status and error details on failure
        """
        # Check if OAuth token is provided
        if not _external_access_token:
            return {
                "status": "error",
                "error": "Authentication required. Please authorize with LinkedIn using OAuth.",
                "error_type": "missing_oauth_token",
            }

        # Create a LinkedIn client with the OAuth access token
        import httpx

        from ..api import LinkedInClient

        oauth_client = LinkedInClient()
        oauth_client.access_token = _external_access_token

        # Test connection and get user info
        try:
            async with httpx.AsyncClient() as client:
                userinfo_response = await client.get(
                    "https://api.linkedin.com/v2/userinfo",
                    headers={"Authorization": f"Bearer {_external_access_token}"},
                    timeout=10.0,
                )
                userinfo_response.raise_for_status()
                userinfo = userinfo_response.json()

                person_id = userinfo.get("sub")
                # Format as URN if needed
                if person_id and not person_id.startswith("urn:"):
                    person_urn = f"urn:li:person:{person_id}"
                else:
                    person_urn = person_id

                return {
                    "status": "connected",
                    "name": userinfo.get("name"),
                    "email": userinfo.get("email"),
                    "person_id": person_id,
                    "person_urn": person_urn,
                    "oauth_validated": True,
                    "token_length": len(_external_access_token),
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": "connection_failed",
            }

    return {
        "linkedin_publish": linkedin_publish,
        "linkedin_test_connection": linkedin_test_connection,
    }
