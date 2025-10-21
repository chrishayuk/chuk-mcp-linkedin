#!/usr/bin/env python3
"""
Preview a visual chart post using the post preview functionality.

Creates a draft with visual chart component, then shows:
- Text preview (first 210 chars)
- Full preview
- HTML preview (opens in browser)
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.manager import LinkedInManager
from chuk_mcp_linkedin.composition import ComposablePost


async def preview_chart_post():
    """Create and preview a chart post"""

    print("=" * 70)
    print("VISUAL CHART POST PREVIEW")
    print("=" * 70)
    print()

    # Step 1: Create draft
    print("📝 Creating draft with visual chart component...")
    manager = LinkedInManager()
    draft = manager.create_draft(
        name="Developer Productivity Chart",
        post_type="text"
    )
    print(f"✓ Draft created: {draft.draft_id}")
    print()

    # Step 2: Add components
    print("🔨 Adding components...")

    # Hook
    hook_data = {
        "type": "stat",
        "content": "📊 Developer Productivity in 2025\n\nWe surveyed 500 developers about AI coding tools."
    }
    draft.content.setdefault("components", []).append(
        {"component": "hook", **hook_data}
    )

    # Visual Chart
    chart_data = {
        "type": "bar",
        "data": {
            "AI-Assisted": 12,
            "Code Review": 6,
            "Documentation": 4,
            "Debugging": 8
        },
        "title": "Time Saved Per Week"
    }
    draft.content["components"].append(
        {"component": "visual_chart", **chart_data}
    )

    # Body with insights
    body_data = {
        "content": "📈 KEY FINDINGS:\n\n✅ 67% → Faster problem-solving\n✅ 54% → Fewer bugs in production\n✅ 89% → Better learning & upskilling\n❌ 23% → Using AI for architecture\n\n💡 THE INSIGHT:\n\nMost developers use AI for code generation.\nVery few use it for high-level system design.\n\nThat's the opportunity.",
        "structure": "linear"
    }
    draft.content["components"].append(
        {"component": "body", **body_data}
    )

    # CTA
    cta_data = {
        "type": "question",
        "text": "How are you using AI in your development workflow?"
    }
    draft.content["components"].append(
        {"component": "cta", **cta_data}
    )

    # Hashtags
    hashtag_data = {
        "tags": ["DeveloperProductivity", "AI", "TechTrends", "SoftwareDevelopment"],
        "placement": "end"
    }
    draft.content["components"].append(
        {"component": "hashtags", **hashtag_data}
    )

    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added 5 components (hook, visual_chart, body, cta, hashtags)")
    print()

    # Step 3: Compose the post
    print("🔨 Composing post...")
    post = ComposablePost(draft.post_type)

    for comp in draft.content.get("components", []):
        comp_type = comp.get("component")
        if comp_type == "hook":
            post.add_hook(comp["type"], comp["content"])
        elif comp_type == "visual_chart":
            post.add_visual_chart(comp["type"], comp["data"], comp.get("title"))
        elif comp_type == "body":
            post.add_body(comp["content"], comp.get("structure"))
        elif comp_type == "cta":
            post.add_cta(comp["type"], comp["text"])
        elif comp_type == "hashtags":
            post.add_hashtags(comp["tags"], comp.get("placement", "end"))

    post.optimize_for_engagement()
    final_text = post.compose()

    # Update draft with composed text
    draft.content["composed_text"] = final_text
    manager.update_draft(draft.draft_id, content=draft.content)

    print(f"✓ Post composed ({len(final_text)} characters)")
    print()

    # Step 4: Show hook preview (what appears before "see more")
    print("👁️  HOOK PREVIEW (first 210 chars - before 'see more')")
    print("=" * 70)
    hook_preview = final_text[:210]
    print(hook_preview)
    if len(final_text) > 210:
        print("...")
    print("=" * 70)
    print()
    print(f"Note: LinkedIn truncates at {len(hook_preview)} chars")
    print()

    # Step 5: Show full preview
    print("📄 FULL POST PREVIEW")
    print("=" * 70)
    print(final_text)
    print("=" * 70)
    print()

    # Step 6: Generate HTML preview
    print("🌐 Generating HTML preview...")
    preview_path = manager.generate_html_preview(draft.draft_id)

    if preview_path:
        print(f"✓ HTML preview generated: {preview_path}")
        print()

        # Open in browser
        import webbrowser
        import os
        file_url = f"file://{os.path.abspath(preview_path)}"
        webbrowser.open(file_url)

        print("✓ Opened in browser!")
        print()
        print("The HTML preview shows:")
        print("  • How the visual chart renders")
        print("  • Character count and limits")
        print("  • Component breakdown")
        print("  • LinkedIn-like formatting")
    else:
        print("❌ Could not generate HTML preview")

    print()
    print("=" * 70)
    print("PREVIEW COMPLETE")
    print("=" * 70)
    print()
    print(f"Draft ID: {draft.draft_id}")
    print("Components used:")
    print("  ✓ Hook (stat)")
    print("  ✓ VisualChart (bar) ← NEW!")
    print("  ✓ Body (linear)")
    print("  ✓ CTA (question)")
    print("  ✓ Hashtags (end)")


if __name__ == "__main__":
    asyncio.run(preview_chart_post())
