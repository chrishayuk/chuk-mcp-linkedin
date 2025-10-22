"""
Publish a multi-image carousel post to LinkedIn

Uploads multiple images (2-20) and creates a carousel post.
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
    """Upload multiple images and publish carousel post to LinkedIn"""

    dry_run = os.getenv("DRY_RUN", "1") == "1"

    print("\n" + "=" * 60)
    print("LINKEDIN MULTI-IMAGE CAROUSEL POST")
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

    # Get test images
    test_files_dir = Path(__file__).parent.parent / "test_files"
    test_images = [
        test_files_dir / "test_image_1.png",
        test_files_dir / "test_image_2.png",
        test_files_dir / "test_image_3.png",
        test_files_dir / "test_image_4.png",
    ]

    # Check which images exist
    existing_images = [img for img in test_images if img.exists()]

    if len(existing_images) < 2:
        print(f"\n❌ Need at least 2 images for carousel, found {len(existing_images)}")
        return

    print(f"\n✓ Test images found: {len(existing_images)}")
    for img in existing_images:
        print(f"  • {img.name} ({img.stat().st_size / 1024:.1f} KB)")

    # Alt texts for each image
    alt_texts = [
        "Step 1: Planning and research",
        "Step 2: Implementation",
        "Step 3: Testing and validation",
        "Step 4: Launch and iterate",
    ][: len(existing_images)]

    # Create post using composition
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("carousel", theme=theme)

    post.add_hook("insight", "The best stories unfold one frame at a time. Swipe to see how →")

    post.add_body(
        """Carousel posts on LinkedIn are powerful for:

→ Step-by-step guides
→ Before/after transformations
→ Portfolio showcases
→ Multi-part narratives

Each slide keeps your audience engaged, building toward your key message.""",
        structure="linear",
    )

    post.add_cta("curiosity", "What's your favorite type of visual content to create?")

    post.add_hashtags(["CarouselPosts", "VisualStorytelling", "ContentMarketing"])

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
        print(f"  1. Upload {len(existing_images)} images to LinkedIn")
        print("  2. Get image URNs back")
        print("  3. Create carousel post with all images")
        print("  4. Post appears in your LinkedIn feed")
        print("\nTo actually post, run:")
        print("  DRY_RUN=0 uv run python examples/publish_multi_image_post.py")
        return

    # Actually post
    try:
        print("\n" + "=" * 60)
        print("UPLOADING TO LINKEDIN")
        print("=" * 60)

        print(f"\n1️⃣  Uploading {len(existing_images)} images...")
        print("2️⃣  Creating carousel post...")

        result = await client.create_multi_image_post(
            text=post_text, image_paths=existing_images, alt_texts=alt_texts, visibility="PUBLIC"
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
        print("   Type: Multi-image carousel")
        print(f"   Images: {len(existing_images)} uploaded")
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
        print("  • Too many images - maximum 20 allowed")
        print("  • Images too large - keep under 10MB each")

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
