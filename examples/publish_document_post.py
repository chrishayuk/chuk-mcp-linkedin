"""
Publish a document post to LinkedIn

Uploads a document and creates a post with it attached.
Runs automatically without prompts - use with caution!

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
    """Upload document and publish post to LinkedIn"""

    dry_run = os.getenv("DRY_RUN", "1") == "1"

    print("\n" + "=" * 60)
    print("LINKEDIN DOCUMENT UPLOAD TEST")
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
            print("\nTo get these values, run:")
            print("  open scripts/get_member_id.html")
            return

        print(f"✓ Client initialized")
        print(f"  Person URN: {client.person_urn[:30]}...")

    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return

    # Get test document
    test_doc = Path(__file__).parent.parent / "test_files" / "test_document.pdf"

    if not test_doc.exists():
        print(f"\n❌ Test document not found: {test_doc}")
        return

    print(f"\n✓ Test document found")
    print(f"  File: {test_doc.name}")
    print(f"  Size: {test_doc.stat().st_size / 1024:.1f} KB")

    # Create post text
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("document", theme=theme)
    post.add_hook(
        "question",
        "Ever wonder how to share detailed insights on LinkedIn?"
    )
    post.add_body("""Documents are perfect for:

→ Research findings
→ Case studies
→ Strategic frameworks
→ Technical reports

LinkedIn converts each page to an interactive carousel.""", structure="linear")

    post.add_cta(
        "curiosity",
        "What's your preferred format for sharing long-form content?"
    )
    post.add_hashtags(["ContentStrategy", "ThoughtLeadership", "Documents"])

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
        print("  1. Upload test_document.pdf to LinkedIn")
        print("  2. Get document URN back")
        print("  3. Create post with document attached")
        print("  4. Post appears in your LinkedIn feed")
        print("\nTo actually post, run:")
        print("  DRY_RUN=0 uv run python examples/publish_document_post.py")
        return

    # Actually post
    try:
        print("\n" + "=" * 60)
        print("UPLOADING TO LINKEDIN")
        print("=" * 60)

        print("\n1️⃣  Initializing document upload...")
        print("2️⃣  Uploading file...")
        print("3️⃣  Creating post...")

        result = await client.create_document_post(
            text=post_text,
            document_path=test_doc,
            document_title="LinkedIn API Test Document",
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
        print(f"   Document: {test_doc.name} uploaded")
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

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
