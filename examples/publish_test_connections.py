#!/usr/bin/env python3
"""
Publish test post to LinkedIn (CONNECTIONS ONLY)

This will actually post to LinkedIn, visible only to your connections.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, config


async def publish_test():
    """Publish a test post to LinkedIn"""

    print("=" * 70)
    print("PUBLISHING TO LINKEDIN (CONNECTIONS ONLY)")
    print("=" * 70)
    print()

    # The test post content
    test_post = """🧪 Testing my new LinkedIn MCP server (test post - connections only)

Just successfully integrated the LinkedIn API with my MCP server.

This post was created using:
→ Python + LinkedIn REST API
→ Model Context Protocol (MCP)
→ Custom design system components

Pretty cool to automate LinkedIn posting while maintaining quality! 🚀

#API #Automation #MCP #LinkedIn"""

    print("POST CONTENT:")
    print("-" * 70)
    print(test_post)
    print("-" * 70)
    print()
    print(f"Character count: {len(test_post)}")
    print(f"Visibility: CONNECTIONS ONLY")
    print(f"Publishing enabled: {config.enable_publishing}")
    print()

    # Publish
    print("📤 Publishing to LinkedIn...")
    print()

    client = LinkedInClient()

    try:
        result = await client.create_text_post(
            text=test_post,
            visibility="CONNECTIONS"  # Only visible to connections, not public
        )

        post_id = result.get('id', '')

        print("✅ SUCCESS! Post published to LinkedIn!")
        print()
        print(f"Post ID: {post_id}")
        print()
        print("View your post:")
        print("→ Go to: https://www.linkedin.com/in/chrishayuk")
        print("→ Look for the test post in your feed")
        print()
        print("To delete this test post:")
        print("→ Click the three dots (...) on the post")
        print("→ Select 'Delete'")
        print()
        print("Note: Post is only visible to your connections, not public.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(publish_test())
