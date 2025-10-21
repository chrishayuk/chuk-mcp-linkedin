"""
Async MCP server for LinkedIn post creation.

Provides tools for creating, managing, and optimizing LinkedIn posts using
a design system approach with components, themes, and variants.
"""

from chuk_mcp_server import ChukMCPServer
from .manager import LinkedInManager
from .api import LinkedInClient

# Initialize the MCP server
mcp = ChukMCPServer("chuk-mcp-linkedin")

# Initialize manager and client
manager = LinkedInManager()
linkedin_client = LinkedInClient()

# Register all tool modules
from .tools.draft_tools import register_draft_tools
from .tools.composition_tools import register_composition_tools
from .tools.theme_tools import register_theme_tools
from .tools.registry_tools import register_registry_tools
from .tools.publishing_tools import register_publishing_tools

# Register tools with the server
draft_tools = register_draft_tools(mcp, manager)
composition_tools = register_composition_tools(mcp, manager)
theme_tools = register_theme_tools(mcp, manager)
registry_tools = register_registry_tools(mcp, manager)
publishing_tools = register_publishing_tools(mcp, manager, linkedin_client)

# Make tools available at module level for easier imports
__all__ = [
    "mcp",
    "manager",
    "linkedin_client",
    "draft_tools",
    "composition_tools",
    "theme_tools",
    "registry_tools",
    "publishing_tools",
]
