# src/chuk_mcp_linkedin/tools/draft_tools.py
"""
Draft management tools for LinkedIn posts.

Handles CRUD operations for draft posts.
"""

import json
from typing import Any, Dict, Optional


def register_draft_tools(mcp: Any, manager: Any) -> Dict[str, Any]:
    """Register draft management tools with the MCP server"""

    @mcp.tool  # type: ignore[misc]
    async def linkedin_create(name: str, post_type: str, theme: Optional[str] = None) -> str:
        """
        Create a new LinkedIn post draft.

        Args:
            name: Draft name/identifier
            post_type: Type of LinkedIn post (text, document, poll, video, carousel, image)
            theme: Optional theme name

        Returns:
            Success message with draft ID
        """
        draft = manager.create_draft(
            name=name,
            post_type=post_type,
            theme=theme,
        )
        return f"Created draft '{draft.name}' (ID: {draft.draft_id})"

    @mcp.tool  # type: ignore[misc]
    async def linkedin_list() -> str:
        """
        List all draft posts.

        Returns:
            JSON list of all drafts with metadata
        """
        drafts = manager.list_drafts()
        return json.dumps(drafts, indent=2)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_switch(draft_id: str) -> str:
        """
        Switch to a different draft.

        Args:
            draft_id: Draft ID to switch to

        Returns:
            Success or error message
        """
        success = manager.switch_draft(draft_id)
        if success:
            return f"Switched to draft {draft_id}"
        return f"Draft {draft_id} not found"

    @mcp.tool  # type: ignore[misc]
    async def linkedin_get_info(draft_id: Optional[str] = None) -> str:
        """
        Get detailed information about a draft.

        Args:
            draft_id: Draft ID (optional, uses current if not provided)

        Returns:
            JSON with draft details and stats
        """
        draft_id = draft_id or manager.current_draft_id
        draft = manager.get_draft(draft_id) if draft_id else None

        if draft:
            stats = manager.get_draft_stats(draft_id)
            info = {**draft.to_dict(), "stats": stats}
            return json.dumps(info, indent=2)
        return "No draft found"

    @mcp.tool  # type: ignore[misc]
    async def linkedin_delete(draft_id: str) -> str:
        """
        Delete a draft.

        Args:
            draft_id: Draft ID to delete

        Returns:
            Success or error message
        """
        success = manager.delete_draft(draft_id)
        if success:
            return f"Deleted draft {draft_id}"
        return f"Draft {draft_id} not found"

    @mcp.tool  # type: ignore[misc]
    async def linkedin_clear_all() -> str:
        """
        Clear all drafts.

        Returns:
            Count of drafts cleared
        """
        count = manager.clear_all_drafts()
        return f"Cleared {count} drafts"

    @mcp.tool  # type: ignore[misc]
    async def linkedin_preview_url(
        draft_id: Optional[str] = None,
        session_id: Optional[str] = None,
        provider: str = "memory",
        expires_in: int = 3600,
    ) -> str:
        """
        Generate a preview URL for a draft using chuk-artifacts.

        Creates a session-isolated, secure preview URL with automatic cleanup.
        The preview is stored as an artifact with presigned URL access.

        Args:
            draft_id: Draft ID (optional, uses current if not provided)
            session_id: Optional session ID (generates new session if not provided)
            provider: Storage provider (memory, filesystem, s3, ibm-cos)
            expires_in: URL expiration in seconds (default: 1 hour)

        Returns:
            Presigned URL to view the preview, or error message
        """
        from ..preview import LinkedInPreview
        from ..preview.artifact_preview import get_artifact_manager

        # Get draft
        draft_id = draft_id or manager.current_draft_id
        draft = manager.get_draft(draft_id) if draft_id else None

        if not draft:
            return "Error: No draft found"

        # Get stats
        stats = manager.get_draft_stats(draft_id)

        # Generate HTML
        html_content = LinkedInPreview.generate_html(draft.to_dict(), stats)

        # Get or create artifact manager
        artifact_manager = await get_artifact_manager(provider=provider)

        # Create or use session
        if not session_id:
            session_id = artifact_manager.create_session()
        else:
            artifact_manager.set_session(session_id)

        # Store preview as artifact
        artifact_id = await artifact_manager.store_preview(
            html_content=html_content,
            draft_id=draft_id,
            draft_name=draft.name,
            session_id=session_id,
        )

        # Generate presigned URL
        url = await artifact_manager.get_preview_url(
            artifact_id=artifact_id, session_id=session_id, expires_in=expires_in
        )

        if not url:
            return (
                f"Error: Presigned URLs not supported by provider '{provider}'. "
                "Try using a different provider (s3, ibm-cos)."
            )

        return (
            f"Preview URL: {url}\n\n"
            f"Session ID: {session_id}\n"
            f"Artifact ID: {artifact_id}\n"
            f"Expires in: {expires_in} seconds\n\n"
            "This URL is session-isolated and will expire automatically."
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
