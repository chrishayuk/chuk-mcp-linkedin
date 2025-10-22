"""
Publish a video post to LinkedIn

Uploads a video and creates a post with it.
Set DRY_RUN=1 to preview without actually posting (default).
Set DRY_RUN=0 to publish to LinkedIn.

Note: Requires a test video file (MP4 format, 75KB-500MB, 3sec-30min)
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
    """Upload video and publish post to LinkedIn"""

    dry_run = os.getenv("DRY_RUN", "1") == "1"

    print("\n" + "=" * 60)
    print("LINKEDIN VIDEO POST")
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

        print(f"✓ Client initialized")
        print(f"  Person URN: {client.person_urn[:30]}...")

    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return

    # Get test video
    test_video = Path(__file__).parent.parent / "test_files" / "test_video.mp4"

    if not test_video.exists():
        print(f"\n❌ Test video not found: {test_video}")
        print("\nTo use this example, add a test video:")
        print(f"  1. Create or find an MP4 video (75KB-500MB, 3sec-30min)")
        print(f"  2. Save it as: {test_video}")
        print("\nVideo requirements:")
        print("  • Format: MP4 only")
        print("  • Size: 75KB minimum, 500MB maximum")
        print("  • Duration: 3 seconds minimum, 30 minutes maximum")
        print("  • Aspect ratio: 16:9 recommended")
        return

    print(f"\n✓ Test video found")
    print(f"  File: {test_video.name}")
    print(f"  Size: {test_video.stat().st_size / 1024 / 1024:.1f} MB")

    # Create post using composition
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("video", theme=theme)

    post.add_hook(
        "insight",
        "Video content gets 5x more engagement than static posts."
    )

    post.add_body("""Here's what makes video powerful on LinkedIn:

→ Captures attention in the feed
→ Explains complex ideas simply
→ Builds personal connection
→ Algorithm favors native video

Whether it's a demo, tutorial, or thought piece - video lets you connect with your audience in ways text can't match.""", structure="linear")

    post.add_cta(
        "curiosity",
        "What type of video content resonates most with your audience?"
    )

    post.add_hashtags(["VideoContent", "LinkedInVideo", "ContentCreation"])

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
        print(f"  1. Upload {test_video.name} to LinkedIn")
        print("  2. Get video URN back")
        print("  3. Create post with video attached")
        print("  4. Post appears in your LinkedIn feed")
        print("\nTo actually post, run:")
        print("  DRY_RUN=0 uv run python examples/publish_video_post.py")
        return

    # Actually post
    try:
        print("\n" + "=" * 60)
        print("UPLOADING TO LINKEDIN")
        print("=" * 60)

        print("\n1️⃣  Uploading video...")
        print("2️⃣  Finalizing upload...")
        print("3️⃣  Waiting for LinkedIn to process video...")
        print("4️⃣  Creating post...")

        result = await client.create_video_post(
            text=post_text,
            video_path=test_video,
            title="LinkedIn API Test Video",
            visibility="PUBLIC"
        )

        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)

        post_urn = result.get('id', '')
        post_status = result.get('status_code', 'N/A')

        print(f"\nPost URN: {post_urn}")
        print(f"HTTP Status: {post_status}")

        # Format post URL for easy access
        if post_urn and ('ugcPost' in post_urn or 'share' in post_urn):
            post_url = f"https://www.linkedin.com/feed/update/{post_urn}"
            print(f"\n🔗 View your post:")
            print(f"   {post_url}")
            print(f"\nOr check your LinkedIn feed:")
            print(f"   https://www.linkedin.com/feed/")

        print("\n📊 Details:")
        print(f"   Type: Video post")
        print(f"   Video: {test_video.name} uploaded")
        print(f"   Size: {test_video.stat().st_size / 1024 / 1024:.1f} MB")
        print(f"   Text: {len(post_text)} characters")
        print(f"   Visibility: PUBLIC")

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
        print("  • Video too large - maximum 500MB")
        print("  • Video too small - minimum 75KB")
        print("  • Wrong format - must be MP4")
        print("  • Duration invalid - 3 seconds to 30 minutes")

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
