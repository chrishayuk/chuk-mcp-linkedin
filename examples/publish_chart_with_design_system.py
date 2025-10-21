#!/usr/bin/env python3
"""
Publish a visual chart using LinkedIn Design System Components

Creates a post using:
- Hook component
- Body component
- CTA component
- Hashtags component

Then publishes to LinkedIn (CONNECTIONS ONLY)
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.manager import LinkedInManager
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.api import LinkedInClient, config


async def publish_chart_post():
    """Create and publish a visual chart post using design system"""

    print("=" * 70)
    print("PUBLISHING VISUAL CHART - DESIGN SYSTEM WORKFLOW")
    print("=" * 70)
    print()

    # Step 1: Create draft
    print("📝 Step 1: Creating draft...")
    manager = LinkedInManager()
    draft = manager.create_draft(
        name="Developer Productivity Chart",
        post_type="text"
    )
    print(f"✓ Created draft: {draft.draft_id}")
    print()

    # Step 2: Add hook component (stat-based)
    print("🎣 Step 2: Adding hook (stat)...")
    hook_data = {
        "type": "stat",
        "content": "📊 Developer Productivity: AI vs Traditional Coding\n\nHere's what 500 developers told us about their workflow:"
    }
    draft.content.setdefault("components", []).append(
        {"component": "hook", **hook_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added stat hook")
    print()

    # Step 3: Add body with visual chart
    print("📄 Step 3: Adding body (visual chart)...")
    chart_body = """┌─────────────────────────────────────────┐
│ Time Saved Per Week (Hours)            │
├─────────────────────────────────────────┤
│ AI-Assisted:    ████████████ 12h        │
│ Code Review:    ██████ 6h               │
│ Documentation:  ████ 4h                 │
│ Debugging:      ████████ 8h             │
└─────────────────────────────────────────┘

Key Findings:

✓ 67% report faster problem-solving
✓ 54% produce fewer bugs
✓ 89% say AI helps with learning
✗ Only 23% use it for architecture

The biggest gap?
→ Developers underutilize AI for high-level design
→ Most focus on code generation only"""

    body_data = {
        "content": chart_body,
        "structure": "framework"
    }
    draft.content["components"].append(
        {"component": "body", **body_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added visual chart body")
    print()

    # Step 4: Add CTA component
    print("📢 Step 4: Adding CTA (question)...")
    cta_data = {
        "type": "question",
        "text": "What's your experience with AI coding tools?"
    }
    draft.content["components"].append(
        {"component": "cta", **cta_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added question CTA")
    print()

    # Step 5: Add hashtags component
    print("🏷️  Step 5: Adding hashtags...")
    hashtag_data = {
        "tags": ["DeveloperProductivity", "AI", "CodingStats", "TechTrends"],
        "placement": "end"
    }
    draft.content["components"].append(
        {"component": "hashtags", **hashtag_data}
    )
    manager.update_draft(draft.draft_id, content=draft.content)
    print("✓ Added 4 hashtags")
    print()

    # Step 6: Compose using design system
    print("🔨 Step 6: Composing post...")
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

    print(f"✓ Post composed ({len(final_text)} characters)")
    print()

    # Step 7: Show preview
    print("👀 Step 7: Preview...")
    print("=" * 70)
    print(final_text)
    print("=" * 70)
    print()

    # Step 8: Publish to LinkedIn
    print("📤 Step 8: Publishing to LinkedIn (CONNECTIONS ONLY)...")
    print()

    client = LinkedInClient()

    try:
        result = await client.create_text_post(
            text=final_text,
            visibility="CONNECTIONS"
        )

        post_id = result.get('id', '')

        print("✅ SUCCESS! Design system post published to LinkedIn!")
        print()
        print(f"Post ID: {post_id}")
        print(f"Draft ID: {draft.draft_id}")
        print()
        print("View your post:")
        print("→ Go to: https://www.linkedin.com/in/chrishayuk")
        print("→ See how the design system components rendered")
        print()
        print("Components used:")
        print("  ✓ Hook (stat-based)")
        print("  ✓ Body (framework structure with visual chart)")
        print("  ✓ CTA (question)")
        print("  ✓ Hashtags (end placement)")
        print()
        print("To delete: Click (...) on the post → Delete")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(publish_chart_post())
