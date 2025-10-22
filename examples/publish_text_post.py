"""
Publish a simple text post to LinkedIn

Uses the new Posts API to create a text-only post.
Set DRY_RUN=1 to preview without actually posting (default).
Set DRY_RUN=0 to publish to LinkedIn.
"""

import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, LinkedInAPIError
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager


async def main():
    """Create and publish a text post to LinkedIn"""

    dry_run = os.getenv("DRY_RUN", "1") == "1"

    print("\n" + "=" * 60)
    print("LINKEDIN TEXT POST")
    print("=" * 60)
    print(f"Mode: {'DRY RUN (no actual post)' if dry_run else 'LIVE (will post!)'}")
    print()

    # Initialize client
    try:
        client = LinkedInClient()

        # Validate configuration
        is_valid, missing = client.validate_config()
        if not is_valid:
            print("❌ LinkedIn API not configured!")
            print(f"Missing: {', '.join(missing)}")
            print("\nPlease set:")
            print("  export LINKEDIN_ACCESS_TOKEN='your_token'")
            print("  export LINKEDIN_PERSON_URN='urn:li:person:YOUR_ID'")
            return

        print("✓ Client initialized")
        print(f"  Person URN: {client.person_urn[:30]}...")

    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return

    # Create post using composition
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("text", theme=theme)

    post.add_hook("insight", "The best API documentation tells you not just HOW, but WHY.")

    post.add_body(
        """After migrating from LinkedIn's UGC API to the new Posts API:

→ Simpler payload structure
→ Cleaner response handling
→ Better header management
→ More consistent behavior

Sometimes upgrading is worth the effort.""",
        structure="linear",
    )

    post.add_cta("curiosity", "What API migrations have you tackled recently?")

    post.add_hashtags(["APIDesign", "DeveloperExperience", "LinkedIn"])

    post_text = post.compose()

    print("\n" + "=" * 60)
    print("POST CONTENT")
    print("=" * 60)
    print(post_text)
    print()
    print(f"Character count: {len(post_text)}")

    if dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN - NO ACTUAL POST")
        print("=" * 60)
        print("\nWhat would happen:")
        print("  1. Create text post using new Posts API")
        print("  2. Post appears in your LinkedIn feed")
        print("\nTo actually post, run:")
        print("  DRY_RUN=0 uv run python examples/publish_text_post.py")
        return

    # Actually post
    try:
        print("\n" + "=" * 60)
        print("POSTING TO LINKEDIN")
        print("=" * 60)

        print("\n📤 Creating post...")

        result = await client.create_text_post(text=post_text, visibility="PUBLIC")

        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)

        post_urn = result.get("id", "")
        post_status = result.get("status_code", "N/A")

        print(f"\nPost URN: {post_urn}")
        print(f"HTTP Status: {post_status}")

        # Format post URL for easy access
        if post_urn and ("ugcPost" in post_urn or "share" in post_urn):
            post_url = f"https://www.linkedin.com/feed/update/{post_urn}"
            print("\n🔗 View your post:")
            print(f"   {post_url}")
            print("\nOr check your LinkedIn feed:")
            print("   https://www.linkedin.com/feed/")

        print("\n📊 Details:")
        print("   Type: Text post")
        print(f"   Text: {len(post_text)} characters")
        print("   Visibility: PUBLIC")
        print("   API: Posts API (new)")

    except LinkedInAPIError as e:
        print("\n" + "=" * 60)
        print("❌ LINKEDIN API ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\nCommon issues:")
        print("  • Access token expired - get a new one")
        print("  • Missing scopes - token needs w_member_social")
        print("  • Rate limit - wait a few minutes")
        print("  • Invalid person URN - verify it's correct")

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
