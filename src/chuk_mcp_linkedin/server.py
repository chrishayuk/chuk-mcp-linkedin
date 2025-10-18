"""
MCP server for LinkedIn post creation.

Provides tools for creating, managing, and optimizing LinkedIn posts.
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
from typing import Any, Optional, List
import json

from .manager import LinkedInManager
from .composition import ComposablePost, PostBuilder
from .themes.theme_manager import ThemeManager, THEMES
from .registry import ComponentRegistry
from .variants import VariantResolver, PostVariants


class LinkedInServer:
    """MCP Server for LinkedIn posts"""

    def __init__(self):
        self.server = Server("linkedin-design-system")
        self.manager = LinkedInManager()
        self.theme_manager = ThemeManager()
        self.registry = ComponentRegistry()

        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools"""

        # Draft Management Tools
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                # === DRAFT MANAGEMENT ===
                Tool(
                    name="linkedin_create",
                    description="Create a new LinkedIn post draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Draft name/identifier"},
                            "post_type": {
                                "type": "string",
                                "enum": ["text", "document", "poll", "video", "carousel", "image"],
                                "description": "Type of LinkedIn post"
                            },
                            "theme": {"type": "string", "description": "Theme name (optional)"}
                        },
                        "required": ["name", "post_type"]
                    }
                ),
                Tool(
                    name="linkedin_list",
                    description="List all draft posts",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="linkedin_switch",
                    description="Switch to a different draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "draft_id": {"type": "string", "description": "Draft ID to switch to"}
                        },
                        "required": ["draft_id"]
                    }
                ),
                Tool(
                    name="linkedin_get_info",
                    description="Get detailed information about a draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "draft_id": {"type": "string", "description": "Draft ID (optional, uses current if not provided)"}
                        }
                    }
                ),
                Tool(
                    name="linkedin_delete",
                    description="Delete a draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "draft_id": {"type": "string", "description": "Draft ID to delete"}
                        },
                        "required": ["draft_id"]
                    }
                ),
                Tool(
                    name="linkedin_clear_all",
                    description="Clear all drafts",
                    inputSchema={"type": "object", "properties": {}}
                ),

                # === COMPOSITION ===
                Tool(
                    name="linkedin_add_hook",
                    description="Add opening hook to current draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "hook_type": {
                                "type": "string",
                                "enum": ["question", "stat", "story", "controversy", "list", "curiosity"],
                                "description": "Type of hook"
                            },
                            "content": {"type": "string", "description": "Hook text"}
                        },
                        "required": ["hook_type", "content"]
                    }
                ),
                Tool(
                    name="linkedin_add_body",
                    description="Add main content body to current draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "description": "Body text"},
                            "structure": {
                                "type": "string",
                                "enum": ["linear", "listicle", "framework", "story_arc", "comparison"],
                                "description": "Content structure"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                Tool(
                    name="linkedin_add_cta",
                    description="Add call-to-action to current draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "cta_type": {
                                "type": "string",
                                "enum": ["direct", "curiosity", "action", "share", "soft"],
                                "description": "Type of CTA"
                            },
                            "text": {"type": "string", "description": "CTA text"}
                        },
                        "required": ["cta_type", "text"]
                    }
                ),
                Tool(
                    name="linkedin_add_hashtags",
                    description="Add hashtags to current draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of hashtags (without #)"
                            },
                            "placement": {
                                "type": "string",
                                "enum": ["inline", "mid", "end", "first_comment"],
                                "description": "Where to place hashtags"
                            }
                        },
                        "required": ["tags"]
                    }
                ),

                # === THEME & VARIANT MANAGEMENT ===
                Tool(
                    name="linkedin_list_themes",
                    description="List all available themes",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="linkedin_get_theme",
                    description="Get details about a specific theme",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "theme_name": {"type": "string", "description": "Theme name"}
                        },
                        "required": ["theme_name"]
                    }
                ),
                Tool(
                    name="linkedin_apply_theme",
                    description="Apply a theme to current draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "theme_name": {"type": "string", "description": "Theme to apply"}
                        },
                        "required": ["theme_name"]
                    }
                ),

                # === COMPONENT REGISTRY ===
                Tool(
                    name="linkedin_list_components",
                    description="List all available post components",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="linkedin_get_component_info",
                    description="Get detailed information about a component",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_type": {"type": "string", "description": "Component type"}
                        },
                        "required": ["component_type"]
                    }
                ),
                Tool(
                    name="linkedin_get_recommendations",
                    description="Get recommendations based on goal",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "goal": {
                                "type": "string",
                                "enum": ["engagement", "authority", "leads", "community", "awareness"],
                                "description": "Your LinkedIn goal"
                            }
                        },
                        "required": ["goal"]
                    }
                ),
                Tool(
                    name="linkedin_get_system_overview",
                    description="Get complete overview of the design system",
                    inputSchema={"type": "object", "properties": {}}
                ),

                # === CONTENT GENERATION ===
                Tool(
                    name="linkedin_compose_post",
                    description="Compose post from components in current draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "optimize": {
                                "type": "boolean",
                                "description": "Optimize for engagement (default: true)"
                            }
                        }
                    }
                ),
                Tool(
                    name="linkedin_get_preview",
                    description="Get preview of current draft (first 210 chars)",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="linkedin_export_draft",
                    description="Export current draft as JSON",
                    inputSchema={"type": "object", "properties": {}}
                ),
            ]

        # Tool handlers
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls"""

            # === DRAFT MANAGEMENT ===
            if name == "linkedin_create":
                draft = self.manager.create_draft(
                    name=arguments["name"],
                    post_type=arguments["post_type"],
                    theme=arguments.get("theme")
                )
                return [TextContent(
                    type="text",
                    text=f"Created draft '{draft.name}' (ID: {draft.draft_id})"
                )]

            elif name == "linkedin_list":
                drafts = self.manager.list_drafts()
                return [TextContent(
                    type="text",
                    text=json.dumps(drafts, indent=2)
                )]

            elif name == "linkedin_switch":
                success = self.manager.switch_draft(arguments["draft_id"])
                if success:
                    return [TextContent(type="text", text=f"Switched to draft {arguments['draft_id']}")]
                return [TextContent(type="text", text=f"Draft {arguments['draft_id']} not found")]

            elif name == "linkedin_get_info":
                draft_id = arguments.get("draft_id") or self.manager.current_draft_id
                draft = self.manager.get_draft(draft_id) if draft_id else None

                if draft:
                    stats = self.manager.get_draft_stats(draft_id)
                    info = {
                        **draft.to_dict(),
                        "stats": stats
                    }
                    return [TextContent(type="text", text=json.dumps(info, indent=2))]
                return [TextContent(type="text", text="No draft found")]

            elif name == "linkedin_delete":
                success = self.manager.delete_draft(arguments["draft_id"])
                if success:
                    return [TextContent(type="text", text=f"Deleted draft {arguments['draft_id']}")]
                return [TextContent(type="text", text=f"Draft {arguments['draft_id']} not found")]

            elif name == "linkedin_clear_all":
                count = self.manager.clear_all_drafts()
                return [TextContent(type="text", text=f"Cleared {count} drafts")]

            # === COMPOSITION ===
            elif name == "linkedin_add_hook":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft. Create one first with linkedin_create.")]

                hook_data = {
                    "type": arguments["hook_type"],
                    "content": arguments["content"]
                }
                draft.content.setdefault("components", []).append({"component": "hook", **hook_data})
                self.manager.update_draft(draft.draft_id, content=draft.content)

                return [TextContent(type="text", text=f"Added {arguments['hook_type']} hook to draft")]

            elif name == "linkedin_add_body":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft")]

                body_data = {
                    "content": arguments["content"],
                    "structure": arguments.get("structure", "linear")
                }
                draft.content.setdefault("components", []).append({"component": "body", **body_data})
                self.manager.update_draft(draft.draft_id, content=draft.content)

                return [TextContent(type="text", text=f"Added body with {body_data['structure']} structure")]

            elif name == "linkedin_add_cta":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft")]

                cta_data = {
                    "type": arguments["cta_type"],
                    "text": arguments["text"]
                }
                draft.content.setdefault("components", []).append({"component": "cta", **cta_data})
                self.manager.update_draft(draft.draft_id, content=draft.content)

                return [TextContent(type="text", text=f"Added {arguments['cta_type']} CTA")]

            elif name == "linkedin_add_hashtags":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft")]

                hashtag_data = {
                    "tags": arguments["tags"],
                    "placement": arguments.get("placement", "end")
                }
                draft.content.setdefault("components", []).append({"component": "hashtags", **hashtag_data})
                self.manager.update_draft(draft.draft_id, content=draft.content)

                return [TextContent(type="text", text=f"Added {len(arguments['tags'])} hashtags")]

            # === THEME MANAGEMENT ===
            elif name == "linkedin_list_themes":
                themes = self.registry.list_themes()
                return [TextContent(type="text", text=json.dumps(themes, indent=2))]

            elif name == "linkedin_get_theme":
                theme = self.theme_manager.get_theme_summary(arguments["theme_name"])
                return [TextContent(type="text", text=json.dumps(theme, indent=2))]

            elif name == "linkedin_apply_theme":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft")]

                self.manager.update_draft(draft.draft_id, theme=arguments["theme_name"])
                return [TextContent(type="text", text=f"Applied theme '{arguments['theme_name']}'")]

            # === REGISTRY ===
            elif name == "linkedin_list_components":
                components = self.registry.list_post_components()
                return [TextContent(type="text", text=json.dumps(components, indent=2))]

            elif name == "linkedin_get_component_info":
                info = self.registry.get_component_info(arguments["component_type"])
                return [TextContent(type="text", text=json.dumps(info, indent=2))]

            elif name == "linkedin_get_recommendations":
                recs = self.registry.get_recommendations(arguments["goal"])
                return [TextContent(type="text", text=json.dumps(recs, indent=2))]

            elif name == "linkedin_get_system_overview":
                overview = self.registry.get_complete_system_overview()
                return [TextContent(type="text", text=json.dumps(overview, indent=2))]

            # === COMPOSITION ===
            elif name == "linkedin_compose_post":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft")]

                # Get theme if specified
                theme = None
                if draft.theme:
                    theme = self.theme_manager.get_theme(draft.theme)

                # Create composable post
                post = ComposablePost(draft.post_type, theme=theme)

                # Add components from draft
                for comp in draft.content.get("components", []):
                    comp_type = comp.get("component")
                    if comp_type == "hook":
                        post.add_hook(comp["type"], comp["content"])
                    elif comp_type == "body":
                        post.add_body(comp["content"], comp.get("structure"))
                    elif comp_type == "cta":
                        post.add_cta(comp["type"], comp["text"])
                    elif comp_type == "hashtags":
                        post.add_hashtags(comp["tags"], comp.get("placement", "end"))

                # Optimize if requested
                if arguments.get("optimize", True):
                    post.optimize_for_engagement()

                # Compose final text
                final_text = post.compose()

                # Update draft with composed text
                draft.content["composed_text"] = final_text
                self.manager.update_draft(draft.draft_id, content=draft.content)

                return [TextContent(type="text", text=f"Composed post ({len(final_text)} chars):\n\n{final_text}")]

            elif name == "linkedin_get_preview":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft")]

                preview = self.manager.get_draft_preview(draft.draft_id)
                return [TextContent(type="text", text=f"Preview (first 210 chars):\n\n{preview}")]

            elif name == "linkedin_export_draft":
                draft = self.manager.get_current_draft()
                if not draft:
                    return [TextContent(type="text", text="No active draft")]

                export_json = self.manager.export_draft(draft.draft_id)
                return [TextContent(type="text", text=export_json or "Export failed")]

            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    async def run(self):
        """Run the server"""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point"""
    import asyncio

    server = LinkedInServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
