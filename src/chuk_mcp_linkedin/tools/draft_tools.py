"""
Draft management tools for LinkedIn posts.

Handles CRUD operations for draft posts.
"""

import json


def register_draft_tools(mcp, manager):
    """Register draft management tools with the MCP server"""

    @mcp.tool
    async def linkedin_create(name: str, post_type: str, theme: str = None) -> str:
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

    @mcp.tool
    async def linkedin_list() -> str:
        """
        List all draft posts.

        Returns:
            JSON list of all drafts with metadata
        """
        drafts = manager.list_drafts()
        return json.dumps(drafts, indent=2)

    @mcp.tool
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

    @mcp.tool
    async def linkedin_get_info(draft_id: str = None) -> str:
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

    @mcp.tool
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

    @mcp.tool
    async def linkedin_clear_all() -> str:
        """
        Clear all drafts.

        Returns:
            Count of drafts cleared
        """
        count = manager.clear_all_drafts()
        return f"Cleared {count} drafts"

    return {
        "linkedin_create": linkedin_create,
        "linkedin_list": linkedin_list,
        "linkedin_switch": linkedin_switch,
        "linkedin_get_info": linkedin_get_info,
        "linkedin_delete": linkedin_delete,
        "linkedin_clear_all": linkedin_clear_all,
    }
