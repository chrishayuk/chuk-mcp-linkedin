#!/usr/bin/env python3
"""
Test making an actual LinkedIn post with current credentials.
This is in DRY RUN mode by default - won't actually post.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, config


async def test_post():
    """Test posting"""

    print("LinkedIn Post Test")
    print("=" * 60)
    print()
    print(f"Person URN: {config.linkedin_person_urn}")
    print(f"Token: {config.linkedin_access_token[:20]}...")
    print(f"Publishing enabled: {config.enable_publishing}")
    print()

    client = LinkedInClient()

    test_text = "🧪 Test post from MCP LinkedIn Server - please ignore"

    print(f"Attempting to post: {test_text}")
    print()

    # Test the API call to see what error we get
    print("🔍 Testing API call...")
    print("⚠️  Note: ENABLE_PUBLISHING=false, so this should not actually post")
    print()

    try:
        result = await client.create_text_post(
            text=test_text,
            visibility="PUBLIC"
        )

        print()
        print("✓ SUCCESS!")
        print("Result:")
        print(result)

    except Exception as e:
        print()
        print(f"❌ Error: {e}")
        print()
        print("This tells us if the URN format is correct.")


if __name__ == "__main__":
    asyncio.run(test_post())
