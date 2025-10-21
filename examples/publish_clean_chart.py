#!/usr/bin/env python3
"""
Publish a clean visual chart using LinkedIn Design System Components

Uses simple formatting that renders well in LinkedIn's proportional font.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.manager import LinkedInManager
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.api import LinkedInClient, config


async def publish_clean_chart():
    """Create and publish a clean chart post using design system"""

    print("=" * 70)
    print("PUBLISHING CLEAN VISUAL CHART - DESIGN SYSTEM")
    print("=" * 70)
    print()

    # Step 1: Create draft
    print("📝 Step 1: Creating draft...")
    manager = LinkedInManager()
    draft = manager.create_draft(
        name="Developer Productivity Visual",
        post_type="text"
    )
    print(f"✓ Created draft: {draft.draft_id}")
    print()

    # Step 2: Add hook component
    print("🎣 Step 2: Adding hook...")
    hook_data = {
        "type": "stat",
        "content": "📊 Developer Productivity in 2025\n\nWe surveyed 500 developers about AI coding tools."
    }
    draft.content.setdefault("components", []).append(
        {"component": "hook", **hook_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added stat hook")
    print()

    # Step 3: Add body with clean visual layout
    print("📄 Step 3: Adding body (clean visual)...")
    # Using simple emojis and text that works in proportional fonts
    chart_body = """⏱️ TIME SAVED PER WEEK:

🟦🟦🟦🟦🟦🟦 AI-Assisted: 12 hours
🟩🟩🟩 Code Review: 6 hours
🟨🟨 Documentation: 4 hours
🟧🟧🟧🟧 Debugging: 8 hours

📈 KEY FINDINGS:

✅ 67% → Faster problem-solving
✅ 54% → Fewer bugs in production
✅ 89% → Better learning & upskilling
❌ 23% → Using AI for architecture

💡 THE INSIGHT:

Most developers use AI for code generation.
Very few use it for high-level system design.

That's the opportunity."""

    body_data = {
        "content": chart_body,
        "structure": "framework"
    }
    draft.content["components"].append(
        {"component": "body", **body_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added clean visual body")
    print()

    # Step 4: Add CTA
    print("📢 Step 4: Adding CTA...")
    cta_data = {
        "type": "question",
        "text": "How are you using AI in your development workflow?"
    }
    draft.content["components"].append(
        {"component": "cta", **cta_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added question CTA")
    print()

    # Step 5: Add hashtags
    print("🏷️  Step 5: Adding hashtags...")
    hashtag_data = {
        "tags": ["DeveloperProductivity", "AI", "TechTrends", "SoftwareDevelopment"],
        "placement": "end"
    }
    draft.content["components"].append(
        {"component": "hashtags", **hashtag_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added 4 hashtags")
    print()

    # Step 6: Compose
    print("🔨 Step 6: Composing post...")
    post = ComposablePost(draft.post_type)

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

    post.optimize_for_engagement()
    final_text = post.compose()

    print(f"✓ Post composed ({len(final_text)} characters)")
    print()

    # Step 7: Preview
    print("👀 Step 7: Preview...")
    print("=" * 70)
    print(final_text)
    print("=" * 70)
    print()

    # Step 8: Publish
    print("📤 Step 8: Publishing to LinkedIn (CONNECTIONS ONLY)...")
    print()

    client = LinkedInClient()

    try:
        result = await client.create_text_post(
            text=final_text,
            visibility="CONNECTIONS"
        )

        post_id = result.get('id', '')

        print("✅ SUCCESS! Clean visual chart published!")
        print()
        print(f"Post ID: {post_id}")
        print(f"Draft ID: {draft.draft_id}")
        print()
        print("View: https://www.linkedin.com/in/chrishayuk")
        print()
        print("This version uses:")
        print("  • Colored square emojis for bars (🟦🟩🟨🟧)")
        print("  • Simple text alignment")
        print("  • Section headers with emojis")
        print("  • Works great in proportional fonts!")
        print()
        print("To delete: Click (...) → Delete")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(publish_clean_chart())
