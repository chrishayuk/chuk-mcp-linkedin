#!/usr/bin/env python3
"""
Publish a visual chart/infographic to LinkedIn (CONNECTIONS ONLY)

Creates a text-based visual chart using Unicode box drawing characters.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, config


async def publish_chart():
    """Publish a visual chart post to LinkedIn"""

    print("=" * 70)
    print("PUBLISHING VISUAL CHART TO LINKEDIN (CONNECTIONS ONLY)")
    print("=" * 70)
    print()

    # Visual chart post with Unicode box drawing characters
    chart_post = """📊 Developer Productivity: AI vs Traditional Coding

Here's what 500 developers told us about their workflow:

┌─────────────────────────────────────────┐
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
→ Most focus on code generation only

What's your experience with AI coding tools?

#DeveloperProductivity #AI #CodingStats #TechTrends"""

    print("POST CONTENT (VISUAL CHART):")
    print("-" * 70)
    print(chart_post)
    print("-" * 70)
    print()
    print(f"Character count: {len(chart_post)}")
    print(f"Visibility: CONNECTIONS ONLY")
    print()

    # Publish
    print("📤 Publishing visual chart to LinkedIn...")
    print()

    client = LinkedInClient()

    try:
        result = await client.create_text_post(
            text=chart_post,
            visibility="CONNECTIONS"
        )

        post_id = result.get('id', '')

        print("✅ SUCCESS! Visual chart published to LinkedIn!")
        print()
        print(f"Post ID: {post_id}")
        print()
        print("View your post:")
        print("→ Go to: https://www.linkedin.com/in/chrishayuk")
        print("→ Check how the visual chart renders")
        print()
        print("To delete this test post:")
        print("→ Click the three dots (...) on the post")
        print("→ Select 'Delete'")
        print()
        print("Note: The box drawing characters should render nicely on LinkedIn!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(publish_chart())
