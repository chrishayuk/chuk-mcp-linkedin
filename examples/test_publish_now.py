#!/usr/bin/env python3
"""
Test: Actually Publish to LinkedIn

⚠️  WARNING: This script will ACTUALLY POST to LinkedIn!
This is a real test - the post will appear on your profile.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, config


async def test_publish():
    """Publish a test post to LinkedIn"""

    print("=" * 70)
    print("⚠️  LINKEDIN PUBLISHING TEST")
    print("=" * 70)
    print()
    print("This will post to your LinkedIn profile:")
    print("https://www.linkedin.com/in/chrishayuk")
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
    print(f"Visibility: CONNECTIONS ONLY (not public)")
    print(f"Publishing enabled: {config.enable_publishing}")
    print(f"Person URN: {config.linkedin_person_urn}")
    print()

    # Confirm before posting
    print("⚠️  This will be posted to LinkedIn (visible to your connections only)")
    response = input("Type 'yes' to publish, anything else to cancel: ")
    print()

    if response.lower() != 'yes':
        print("❌ Cancelled - nothing posted")
        return

    # Actually publish
    print("📤 Publishing to LinkedIn (connections only)...")
    print()

    client = LinkedInClient()

    try:
        result = await client.create_text_post(
            text=test_post,
            visibility="CONNECTIONS"  # Only visible to connections, not public
        )

        print("✅ SUCCESS! Post published to LinkedIn!")
        print()
        print(f"Post ID: {result.get('id')}")
        print()
        print("Check your LinkedIn profile:")
        print("https://www.linkedin.com/in/chrishayuk")
        print()
        print("You can delete this test post from LinkedIn if you want.")

    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Publishing failed. Check your credentials and try again.")


if __name__ == "__main__":
    asyncio.run(test_publish())
