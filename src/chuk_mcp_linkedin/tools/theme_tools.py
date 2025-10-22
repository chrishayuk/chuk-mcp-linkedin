# src/chuk_mcp_linkedin/tools/theme_tools.py
"""
Theme and variant management tools.

Handles theme selection, application, and information retrieval.
"""

import json


def register_theme_tools(mcp, manager):
    """Register theme management tools with the MCP server"""

    from ..themes.theme_manager import ThemeManager
    from ..registry import ComponentRegistry

    theme_manager = ThemeManager()
    registry = ComponentRegistry()

    @mcp.tool
    async def linkedin_list_themes() -> str:
        """
        List all available themes.

        Returns:
            JSON list of themes with descriptions
        """
        themes = registry.list_themes()
        return json.dumps(themes, indent=2)

    @mcp.tool
    async def linkedin_get_theme(theme_name: str) -> str:
        """
        Get details about a specific theme.

        Args:
            theme_name: Theme name

        Returns:
            JSON with theme details
        """
        theme = theme_manager.get_theme_summary(theme_name)
        return json.dumps(theme, indent=2)

    @mcp.tool
    async def linkedin_apply_theme(theme_name: str) -> str:
        """
        Apply a theme to current draft.

        Args:
            theme_name: Theme to apply

        Returns:
            Success message
        """
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
