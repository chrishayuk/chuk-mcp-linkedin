#!/usr/bin/env python3
"""
Hello World: Compose → Draft → Preview URL

Demonstrates the complete workflow from post composition to shareable preview URL.
No OAuth required - runs locally with memory provider.

Usage:
    uv run python examples/hello_preview.py
    # or
    python examples/hello_preview.py
"""

import asyncio
from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.themes import ThemeManager
from chuk_mcp_linkedin.manager_factory import ManagerFactory, set_factory


async def main():
    print("🚀 LinkedIn MCP Server - Hello Preview Demo\n")

    # Initialize factory with memory-based artifacts
    factory = ManagerFactory(use_artifacts=True, artifact_provider="memory")
    set_factory(factory)

    # Get manager for demo user
    mgr = factory.get_manager("demo_user")

    # Step 1: Compose a post using the thought leader theme
    print("📝 Step 1: Composing post...")
    theme = ThemeManager().get_theme("thought_leader")
    post = ComposablePost("text", theme=theme)

    post.add_hook("question", "What's the most underrated growth lever on LinkedIn in 2025?")
    post.add_body(
        "Hint: documents. Short, skimmable, 5–10 pages. " "Try it this week.", structure="linear"
    )
    post.add_cta("curiosity", "Tried docs vs text lately?")
    post.add_hashtags(["LinkedInTips", "B2B", "ContentStrategy"])

    text = post.compose()
    print(f"✓ Post composed ({len(text)} chars)\n")

    # Step 2: Create a draft with the composed content
    print("📋 Step 2: Creating draft...")
    draft = mgr.create_draft("Hello Preview Demo", "text")
    # Update draft with our composed text
    mgr.update_draft(draft.draft_id, content={"text": text})
    print(f"✓ Draft created (ID: {draft.draft_id})\n")

    # Step 3: Generate preview URL
    print("🔗 Step 3: Generating preview URL...")
    preview_url = await mgr.generate_preview_url(
        draft_id=draft.draft_id, base_url="http://localhost:8000", expires_in=3600
    )

    print("✓ Preview URL generated\n")
    print("=" * 60)
    print(f"Preview URL: {preview_url}")
    print("=" * 60)
    print("\n📌 Note: Start the HTTP server to view the preview:")
    print("   OAUTH_ENABLED=false uv run linkedin-mcp http --port 8000")
    print("\n💡 Tip: The URL expires in 1 hour (3600 seconds)")
    print("🔗 Open the preview URL in your browser to see the formatted post")


if __name__ == "__main__":
    asyncio.run(main())
