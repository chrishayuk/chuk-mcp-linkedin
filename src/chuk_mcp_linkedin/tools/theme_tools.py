# src/chuk_mcp_linkedin/tools/theme_tools.py
"""
Theme and variant management tools.

Handles theme selection, application, and information retrieval.

All tools require OAuth authorization to prevent server abuse and enable
user-scoped data persistence across sessions.
"""

import json
from typing import Any, Dict, Optional
from chuk_mcp_server.decorators import requires_auth
from ..manager_factory import get_current_manager


def register_theme_tools(mcp: Any) -> Dict[str, Any]:
    """Register theme management tools with the MCP server"""

    from ..themes.theme_manager import ThemeManager
    from ..registry import ComponentRegistry

    theme_manager = ThemeManager()
    registry = ComponentRegistry()

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_list_themes(_external_access_token: Optional[str] = None) -> str:
        """
        List all available themes.

        Returns:
            JSON list of themes with descriptions
        """
        themes = registry.list_themes()
        return json.dumps(themes, indent=2)

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_get_theme(
        theme_name: str, _external_access_token: Optional[str] = None
    ) -> str:
        """
        Get details about a specific theme.

        Args:
            theme_name: Theme name

        Returns:
            JSON with theme details
        """
        theme = theme_manager.get_theme_summary(theme_name)
        return json.dumps(theme, indent=2)

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_apply_theme(
        theme_name: str, _external_access_token: Optional[str] = None
    ) -> str:
        """
        Apply a theme to current draft.

        Args:
            theme_name: Theme to apply

        Returns:
            Success message
        """
        manager = get_current_manager()
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        manager.update_draft(draft.draft_id, theme=theme_name)
        return f"Applied theme '{theme_name}'"

    return {
        "linkedin_list_themes": linkedin_list_themes,
        "linkedin_get_theme": linkedin_get_theme,
        "linkedin_apply_theme": linkedin_apply_theme,
    }
