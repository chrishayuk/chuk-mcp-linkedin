# src/chuk_mcp_linkedin/tools/registry_tools.py
"""
Component registry and information tools.

Provides information about available components, recommendations, and system overview.
"""

import json


def register_registry_tools(mcp, manager):
    """Register component registry tools with the MCP server"""

    from ..registry import ComponentRegistry

    registry = ComponentRegistry()

    @mcp.tool
    async def linkedin_list_components() -> str:
        """
        List all available post components.

        Returns:
            JSON list of components with descriptions
        """
        components = registry.list_post_components()
        return json.dumps(components, indent=2)

    @mcp.tool
    async def linkedin_get_component_info(component_type: str) -> str:
        """
        Get detailed information about a component.

        Args:
            component_type: Component type

        Returns:
            JSON with component details
        """
        info = registry.get_component_info(component_type)
        return json.dumps(info, indent=2)

    @mcp.tool
    async def linkedin_get_recommendations(goal: str) -> str:
        """
        Get recommendations based on goal.

        Args:
            goal: Your LinkedIn goal (engagement, authority, leads, community, awareness)

        Returns:
            JSON with recommendations
        """
        recs = registry.get_recommendations(goal)
        return json.dumps(recs, indent=2)

    @mcp.tool
    async def linkedin_get_system_overview() -> str:
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
