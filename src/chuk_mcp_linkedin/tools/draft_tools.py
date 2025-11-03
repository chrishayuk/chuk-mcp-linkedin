# src/chuk_mcp_linkedin/tools/draft_tools.py
"""
Draft management tools for LinkedIn posts.

Handles CRUD operations for draft posts.

All tools require OAuth authorization to prevent server abuse and enable
user-scoped data persistence across sessions.

User Isolation:
    - Protocol handler sets user_id in context from OAuth token
    - get_current_manager() retrieves user-specific manager from context
    - No cross-user access possible - all operations are scoped to user_id
    - No need to pass _user_id parameter - it's automatic!
"""

import json
from typing import Any, Dict, Optional
from chuk_mcp_server.decorators import requires_auth
from ..manager_factory import get_current_manager


def register_draft_tools(mcp: Any) -> Dict[str, Any]:
    """Register draft management tools with the MCP server"""

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_create(
        name: str,
        post_type: str,
        theme: Optional[str] = None,
        _external_access_token: Optional[str] = None,
    ) -> str:
        """
        Create a new LinkedIn post draft.

        Args:
            name: Draft name/identifier
            post_type: Type of LinkedIn post (text, document, poll, video, carousel, image)
            theme: Optional theme name

        Returns:
            Success message with draft ID
        """
        manager = get_current_manager()
        draft = manager.create_draft(
            name=name,
            post_type=post_type,
            theme=theme,
        )
        return f"Created draft '{draft.name}' (ID: {draft.draft_id})"

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_list(_external_access_token: Optional[str] = None) -> str:
        """
        List all draft posts for the authenticated LinkedIn user.

        Returns:
            JSON list of all drafts with metadata
        """
        manager = get_current_manager()
        drafts = manager.list_drafts()
        return json.dumps(drafts, indent=2)

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_switch(
        draft_id: str,
        _external_access_token: Optional[str] = None,
    ) -> str:
        """
        Switch to a different draft.

        Args:
            draft_id: Draft ID to switch to

        Returns:
            Success or error message
        """
        manager = get_current_manager()
        success = manager.switch_draft(draft_id)
        if success:
            return f"Switched to draft {draft_id}"
        return f"Draft {draft_id} not found"

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_get_info(
        draft_id: Optional[str] = None,
        _external_access_token: Optional[str] = None,
    ) -> str:
        """
        Get detailed information about a draft.

        Args:
            draft_id: Draft ID (optional, uses current if not provided)

        Returns:
            JSON with draft details and stats
        """
        manager = get_current_manager()
        draft_id = draft_id or manager.current_draft_id
        draft = manager.get_draft(draft_id) if draft_id else None

        if draft and draft_id:
            stats = manager.get_draft_stats(draft_id)
            info = {**draft.to_dict(), "stats": stats}
            return json.dumps(info, indent=2)
        return "No draft found"

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_delete(
        draft_id: str,
        _external_access_token: Optional[str] = None,
    ) -> str:
        """
        Delete a draft.

        Args:
            draft_id: Draft ID to delete

        Returns:
            Success or error message
        """
        manager = get_current_manager()
        success = manager.delete_draft(draft_id)
        if success:
            return f"Deleted draft {draft_id}"
        return f"Draft {draft_id} not found"

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_clear_all(_external_access_token: Optional[str] = None) -> str:
        """
        Clear all drafts for the authenticated LinkedIn user.

        Returns:
            Count of drafts cleared
        """
        manager = get_current_manager()
        count = manager.clear_all_drafts()
        return f"Cleared {count} drafts"

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_preview_url(
        draft_id: Optional[str] = None,
        base_url: Optional[str] = None,
        expires_in: int = 3600,
        _external_access_token: Optional[str] = None,
    ) -> str:
        """
        Generate a shareable preview URL for a draft.

        Returns a URL that can be shared with anyone:
        - For S3/cloud storage: Returns a signed URL that expires after the specified time
        - For memory/filesystem: Returns a token-based URL (no expiration)

        No authentication required to view the preview.

        NOTE: For token-based URLs (memory/filesystem), the server must be running in HTTP mode.
        If using STDIO mode (e.g., MCP CLI), start a separate HTTP server with:
            linkedin-mcp http --port 8000

        Args:
            draft_id: Draft ID (optional, uses current if not provided)
            base_url: Base URL of the server (optional, auto-detected from OAUTH_SERVER_URL or defaults to http://localhost:8000)
            expires_in: Expiration time in seconds for signed URLs (default: 3600 = 1 hour)

        Returns:
            Shareable preview URL or error message
        """
        import os

        manager = get_current_manager()
        draft_id = draft_id or manager.current_draft_id

        if not draft_id:
            return "Error: No draft selected"

        # Auto-detect base_url from OAUTH_SERVER_URL environment variable if not provided
        if base_url is None:
            base_url = os.getenv("OAUTH_SERVER_URL", "http://localhost:8000")

        # Generate preview URL using manager's method
        preview_url = await manager.generate_preview_url(
            draft_id=draft_id, base_url=base_url, expires_in=expires_in
        )

        if not preview_url:
            return "Error: Failed to generate preview URL"

        draft = manager.get_draft(draft_id)
        storage_type = (
            "signed URL (S3)"
            if manager.artifact_provider in ("s3", "ibm-cos")
            else "token-based URL"
        )

        return (
            f"Preview URL: {preview_url}\n\n"
            f"Draft: {draft.name if draft else 'Unknown'}\n"
            f"Draft ID: {draft_id}\n"
            f"URL Type: {storage_type}\n\n"
            "This URL is shareable and does not require authentication.\n"
            "Open this URL in your browser to view the formatted preview.\n\n"
            f"{'NOTE: Signed URL expires in ' + str(expires_in) + ' seconds' if manager.artifact_provider in ('s3', 'ibm-cos') else 'NOTE: If the URL returns Not Found, run the server in HTTP mode: linkedin-mcp http --port 8000'}"
        )

    return {
        "linkedin_create": linkedin_create,
        "linkedin_list": linkedin_list,
        "linkedin_switch": linkedin_switch,
        "linkedin_get_info": linkedin_get_info,
        "linkedin_delete": linkedin_delete,
        "linkedin_clear_all": linkedin_clear_all,
        "linkedin_preview_url": linkedin_preview_url,
    }
