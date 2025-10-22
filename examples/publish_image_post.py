"""
Publish an image post to LinkedIn

Uploads a single image and creates a post with it.
Set DRY_RUN=1 to preview without actually posting (default).
Set DRY_RUN=0 to publish to LinkedIn.
"""

import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, LinkedInAPIError
from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager


async def main():
    """Upload image and publish post to LinkedIn"""

    dry_run = os.getenv("DRY_RUN", "1") == "1"

    print("\n" + "=" * 60)
    print("LINKEDIN IMAGE POST")
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

    # Get test image
    test_image = Path(__file__).parent.parent / "test_files" / "test_image_1.png"

    if not test_image.exists():
        print(f"\n❌ Test image not found: {test_image}")
        return

    print("\n✓ Test image found")
    print(f"  File: {test_image.name}")
    print(f"  Size: {test_image.stat().st_size / 1024:.1f} KB")

    # Create post using composition
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("image", theme=theme)

    post.add_hook(
        "insight", "A picture is worth a thousand words. But the right caption? Priceless."
    )

    post.add_body(
        """Visual content on LinkedIn performs 2x better than text alone:

→ Higher engagement rates
→ More shares and comments
→ Better storytelling
→ Stronger emotional connection

The key is combining compelling imagery with meaningful context.""",
        structure="linear",
    )

    post.add_cta("curiosity", "How do you use visuals in your LinkedIn content strategy?")

    post.add_hashtags(["VisualContent", "ContentStrategy", "LinkedIn"])

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
        print(f"  1. Upload {test_image.name} to LinkedIn")
        print("  2. Get image URN back")
        print("  3. Create post with image attached")
        print("  4. Post appears in your LinkedIn feed")
        print("\nTo actually post, run:")
        print("  DRY_RUN=0 uv run python examples/publish_image_post.py")
        return

    # Actually post
    try:
        print("\n" + "=" * 60)
        print("UPLOADING TO LINKEDIN")
        print("=" * 60)

        print("\n1️⃣  Uploading image...")
        print("2️⃣  Creating post...")

        result = await client.create_image_post(
            text=post_text,
            image_path=test_image,
            alt_text="Example image for LinkedIn API testing",
            visibility="PUBLIC",
        )

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
        print("   Type: Single image post")
        print(f"   Image: {test_image.name} uploaded")
        print(f"   Text: {len(post_text)} characters")
        print("   Visibility: PUBLIC")

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
        print("  • Image too large - keep under 10MB")

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
