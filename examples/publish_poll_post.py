"""
Publish a poll post to LinkedIn

Creates a poll with 2-4 options and custom duration.
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
    """Create and publish a poll post to LinkedIn"""

    dry_run = os.getenv("DRY_RUN", "1") == "1"

    print("\n" + "=" * 60)
    print("LINKEDIN POLL POST")
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

    post = ComposablePost("poll", theme=theme)

    post.add_hook("question", "Quick poll for my developer network:")

    post.add_body(
        """I'm curious about the state of API development in 2025.

Whether you're building microservices, integrations, or full platforms - your experience matters.

Vote below and drop a comment with your reasoning!""",
        structure="linear",
    )

    post.add_cta("curiosity", "What makes your choice the best for modern development?")

    post.add_hashtags(["APIs", "DeveloperTools", "SoftwareEngineering"])

    post_text = post.compose()

    # Poll configuration
    poll_question = "What's your primary API development approach in 2025?"
    poll_options = ["REST APIs", "GraphQL", "gRPC", "WebSockets"]
    poll_duration = "ONE_WEEK"

    print("\n" + "=" * 60)
    print("POST CONTENT")
    print("=" * 60)
    print(post_text)
    print()
    print(f"Character count: {len(post_text)}")

    print("\n" + "=" * 60)
    print("POLL CONFIGURATION")
    print("=" * 60)
    print(f"Question: {poll_question}")
    print("Options:")
    for i, option in enumerate(poll_options, 1):
        print(f"  {i}. {option}")
    print(f"Duration: {poll_duration}")

    if dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN - NO ACTUAL POST")
        print("=" * 60)
        print("\nWhat would happen:")
        print("  1. Create poll post with 4 options")
        print("  2. Poll runs for one week")
        print("  3. Post appears in your LinkedIn feed")
        print("  4. Connections can vote and see results")
        print("\nTo actually post, run:")
        print("  DRY_RUN=0 uv run python examples/publish_poll_post.py")
        return

    # Actually post
    try:
        print("\n" + "=" * 60)
        print("POSTING TO LINKEDIN")
        print("=" * 60)

        print("\n📊 Creating poll...")

        result = await client.create_poll_post(
            text=post_text,
            question=poll_question,
            options=poll_options,
            duration=poll_duration,
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
        print("   Type: Poll post")
        print(f"   Question: {len(poll_question)} characters")
        print(f"   Options: {len(poll_options)}")
        print(f"   Duration: {poll_duration}")
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
        print("  • Question too long - max 140 characters")
        print("  • Option text too long - max 30 characters each")
        print("  • Wrong number of options - need 2-4 options")

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
