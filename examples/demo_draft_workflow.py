#!/usr/bin/env python3
"""
Demo: LinkedIn Draft Post Workflow

This script demonstrates creating a LinkedIn post using the design system
components without actually publishing.

Shows:
- Creating a draft
- Adding hook
- Adding body paragraphs
- Adding CTA
- Adding hashtags
- Composing with optimization
- Previewing the result
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.manager import LinkedInManager
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager


async def demo_workflow():
    """Demonstrate the draft post workflow"""

    print("=" * 70)
    print("LinkedIn Draft Post Workflow Demo")
    print("=" * 70)
    print()

    # Initialize manager
    manager = LinkedInManager()

    # Step 1: Create a new draft
    print("📝 Step 1: Creating a new draft...")
    print("-" * 70)
    draft = manager.create_draft(
        name="AI in Software Development",
        post_type="text"
    )
    print(f"✓ Created draft: {draft.draft_id}")
    print(f"  Name: {draft.name}")
    print(f"  Type: {draft.post_type}")
    print()

    # Step 2: Add a compelling hook
    print("🎣 Step 2: Adding a hook...")
    print("-" * 70)
    hook_data = {
        "type": "contrarian",
        "content": "The future of coding isn't about writing more code.\n\nIt's about writing better prompts."
    }
    draft.content.setdefault("components", []).append(
        {"component": "hook", **hook_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print(f"✓ Added {hook_data['type']} hook")
    print()

    # Step 3: Add body content with insights
    print("📄 Step 3: Adding body paragraphs...")
    print("-" * 70)

    body_lines = [
        "→ Junior developers spend 80% of their time debugging",
        "→ Senior developers spend 80% of their time preventing bugs",
        "→ AI-assisted developers spend 80% of their time asking the right questions",
        "",
        "The skill isn't syntax anymore.",
        "It's problem decomposition.",
        "",
        "You need to:",
        "• Break down complex problems into clear steps",
        "• Communicate context effectively to AI tools",
        "• Validate and iterate on AI-generated solutions",
        "• Understand when to use AI vs. when to code from scratch",
        "",
        "The developers who master this will 10x their output.",
        "The ones who don't will be left behind.",
    ]

    body_content = "\n".join(body_lines)
    body_data = {
        "content": body_content,
        "structure": "listicle"
    }
    draft.content["components"].append(
        {"component": "body", **body_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print(f"✓ Added body with {body_data['structure']} structure")
    print()

    # Step 4: Add a call-to-action
    print("📢 Step 4: Adding a call-to-action...")
    print("-" * 70)
    cta_data = {
        "type": "question",
        "text": "What AI tools are you using in your development workflow?"
    }
    draft.content["components"].append(
        {"component": "cta", **cta_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print(f"✓ Added {cta_data['type']} CTA")
    print()

    # Step 5: Add hashtags
    print("🏷️  Step 5: Adding hashtags...")
    print("-" * 70)
    hashtag_data = {
        "tags": ["AI", "SoftwareDevelopment", "DeveloperTools", "FutureOfWork"],
        "placement": "end"
    }
    draft.content["components"].append(
        {"component": "hashtags", **hashtag_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print(f"✓ Added {len(hashtag_data['tags'])} hashtags")
    print()

    # Step 6: Compose the post
    print("🔨 Step 6: Composing the post...")
    print("-" * 70)

    # Create composable post
    post = ComposablePost(draft.post_type)

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

    # Optimize for engagement
    post.optimize_for_engagement()

    # Compose final text
    final_text = post.compose()

    # Update draft with composed text
    draft.content["composed_text"] = final_text
    manager.update_draft(draft.draft_id, content=draft.content)

    print(f"✓ Post composed ({len(final_text)} characters)")
    print()

    # Step 7: Full preview
    print("👀 Step 7: Full post preview...")
    print("=" * 70)
    print(final_text)
    print("=" * 70)
    print()

    # Step 8: Hook preview (what users see before "see more")
    print("🔍 Step 8: Hook preview (first 210 chars - visible before 'see more')...")
    print("-" * 70)
    hook_preview = final_text[:210]
    print(hook_preview)
    if len(final_text) > 210:
        print("...")
    print("-" * 70)
    print()

    # Step 9: Show metadata
    print("📊 Step 9: Post metadata...")
    print("-" * 70)
    char_count = len(final_text)
    component_count = len(draft.content.get("components", []))
    has_hook = any(c.get("component") == "hook" for c in draft.content.get("components", []))
    has_cta = any(c.get("component") == "cta" for c in draft.content.get("components", []))
    hashtag_comp = next((c for c in draft.content.get("components", []) if c.get("component") == "hashtags"), None)
    hashtag_count = len(hashtag_comp.get("tags", [])) if hashtag_comp else 0

    print(f"Draft ID: {draft.draft_id}")
    print(f"Name: {draft.name}")
    print(f"Created: {draft.created_at}")
    print(f"Last modified: {draft.updated_at}")
    print(f"Character count: {char_count} / 3000")
    print(f"Remaining: {3000 - char_count} characters")
    print(f"Components: {component_count}")
    print(f"Has hook: {has_hook}")
    print(f"Has CTA: {has_cta}")
    print(f"Hashtags: {hashtag_count}")
    print()

    # Step 10: What's next
    print("🚀 Step 10: What's next?")
    print("-" * 70)
    print("This draft is ready! Via MCP tools you can:")
    print()
    print("  • linkedin_get_preview() - Preview before 'see more'")
    print("  • linkedin_preview_html() - Generate HTML preview in browser")
    print("  • linkedin_export_draft() - Export as JSON")
    print("  • linkedin_list() - See all your drafts")
    print("  • linkedin_publish(dry_run=true) - Test publish flow")
    print()
    print("To publish for real:")
    print("  1. Set ENABLE_PUBLISHING=true in .env")
    print("  2. Use linkedin_publish(visibility='PUBLIC')")
    print()

    print("=" * 70)
    print("✓ Demo Complete!")
    print("=" * 70)
    print()
    print(f"Draft ID: {draft.draft_id}")
    print("Access via MCP tools or check ~/.linkedin_drafts/")


if __name__ == "__main__":
    asyncio.run(demo_workflow())
