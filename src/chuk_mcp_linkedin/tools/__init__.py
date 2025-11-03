# src/chuk_mcp_linkedin/tools/__init__.py
"""
MCP tools for LinkedIn post management.

Organized into modules by functionality:
- draft_tools: Draft CRUD operations
- composition_tools: Post composition and content building
- theme_tools: Theme and variant management
- publishing_tools: LinkedIn API publishing
- registry_tools: Component registry and information

Each module provides a register_*_tools function that registers
tools with the MCP server using decorators.
"""

from .composition_tools import register_composition_tools
from .draft_tools import register_draft_tools
from .publishing_tools import register_publishing_tools
from .registry_tools import register_registry_tools
from .theme_tools import register_theme_tools

__all__ = [
    "register_draft_tools",
    "register_composition_tools",
    "register_theme_tools",
    "register_publishing_tools",
    "register_registry_tools",
]
