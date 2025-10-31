# src/chuk_mcp_linkedin/tools/registry_tools.py
"""
Component registry and information tools.

Provides information about available components, recommendations, and system overview.

All tools require OAuth authorization to prevent server abuse and enable
user-scoped data persistence across sessions.
"""

import json
from typing import Any, Dict, Optional
from chuk_mcp_server.decorators import requires_auth


def register_registry_tools(mcp: Any) -> Dict[str, Any]:
    """Register component registry tools with the MCP server"""

    from ..registry import ComponentRegistry

    registry = ComponentRegistry()

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_list_components(_external_access_token: Optional[str] = None) -> str:
        """
        List all available post components.

        Returns:
            JSON list of components with descriptions
        """
        components = registry.list_post_components()
        return json.dumps(components, indent=2)

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_get_component_info(
        component_type: str, _external_access_token: Optional[str] = None
    ) -> str:
        """
        Get detailed information about a component.

        Args:
            component_type: Component type

        Returns:
            JSON with component details
        """
        info = registry.get_component_info(component_type)
        return json.dumps(info, indent=2)

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_get_recommendations(
        goal: str, _external_access_token: Optional[str] = None
    ) -> str:
        """
        Get recommendations based on goal.

        Args:
            goal: Your LinkedIn goal (engagement, authority, leads, community, awareness)

        Returns:
            JSON with recommendations
        """
        recs = registry.get_recommendations(goal)
        return json.dumps(recs, indent=2)

    @mcp.tool  # type: ignore[misc]
    @requires_auth()
    async def linkedin_get_system_overview(_external_access_token: Optional[str] = None) -> str:
        """
        Get complete overview of the design system.

        Returns:
            JSON with system overview
        """
        overview = registry.get_complete_system_overview()
        return json.dumps(overview, indent=2)

    return {
        "linkedin_list_components": linkedin_list_components,
        "linkedin_get_component_info": linkedin_get_component_info,
        "linkedin_get_recommendations": linkedin_get_recommendations,
        "linkedin_get_system_overview": linkedin_get_system_overview,
    }
