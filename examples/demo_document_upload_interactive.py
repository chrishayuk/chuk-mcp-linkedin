"""
Test: Upload a document to LinkedIn and create a post

This example demonstrates the complete flow:
1. Upload a document (PDF, PPTX, etc.) to LinkedIn
2. Create a post with the uploaded document attached
3. Verify the post was created successfully

Requirements:
- LINKEDIN_ACCESS_TOKEN environment variable
- LINKEDIN_PERSON_URN environment variable
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, LinkedInAPIError
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager


async def test_document_upload():
    """Test uploading a document and creating a post"""

    print("\n" + "=" * 60)
    print("LINKEDIN DOCUMENT UPLOAD TEST")
    print("=" * 60)

    # Initialize client
    try:
        client = LinkedInClient()

        # Validate configuration
        is_valid, missing = client.validate_config()
        if not is_valid:
            print("\n❌ LinkedIn API not configured!")
            print(f"Missing: {', '.join(missing)}")
            print("\nPlease set:")
            print("  export LINKEDIN_ACCESS_TOKEN='your_token'")
            print("  export LINKEDIN_PERSON_URN='urn:li:person:YOUR_ID'")
            return

        print("\n✓ Client initialized")
        print(f"  Person URN: {client.person_urn}")

    except Exception as e:
        print(f"\n❌ Error initializing client: {e}")
        return

    # Get test document
    test_doc = Path(__file__).parent.parent / "test_files" / "test_document.pdf"

    if not test_doc.exists():
        print(f"\n❌ Test document not found: {test_doc}")
        return

    print(f"\n✓ Test document found: {test_doc.name}")
    print(f"  Size: {test_doc.stat().st_size / 1024:.1f} KB")

    # Create post text using composition
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("document", theme=theme)
    post.add_hook("question", "Ever wonder how to share detailed insights on LinkedIn?")
    post.add_body(
        """Documents are perfect for:

→ Research findings
→ Case studies
→ Strategic frameworks
→ Technical reports

LinkedIn converts each page to an interactive carousel.""",
        structure="linear",
    )

    post.add_cta("curiosity", "What's your preferred format for sharing long-form content?")
    post.add_hashtags(["ContentStrategy", "ThoughtLeadership", "Documents"])

    post_text = post.compose()

    print("\n" + "=" * 60)
    print("POST TEXT")
    print("=" * 60)
    print(post_text)
    print()

    # Confirm before posting
    print("\n" + "=" * 60)
    print("READY TO POST")
    print("=" * 60)
    print(f"Document: {test_doc.name}")
    print("Title: API Testing Document")
    print(f"Characters: {len(post_text)}")
    print()

    response = input("Post to LinkedIn? (yes/no): ").strip().lower()

    if response != "yes":
        print("\n❌ Cancelled by user")
        return

    # Upload and post
    try:
        print("\n" + "=" * 60)
        print("UPLOADING TO LINKEDIN")
        print("=" * 60)

        print("\nStep 1: Uploading document...")
        result = await client.create_document_post(
            text=post_text,
            document_path=test_doc,
            document_title="API Testing Document",
            visibility="PUBLIC",
        )

        print("\n✓ SUCCESS!")
        print("\nResponse:")
        print(f"  Post ID: {result.get('id', 'N/A')}")
        print(f"  Status: {result.get('lifecycleState', 'N/A')}")

        # Try to extract post URL
        post_id = result.get("id", "")
        if post_id:
            # Format: urn:li:share:123456 or activity:123456
            if ":" in post_id:
                activity_id = post_id.split(":")[-1]
                post_url = f"https://www.linkedin.com/feed/update/{post_id}"
                print(f"  URL: {post_url}")

        print("\n" + "=" * 60)
        print("POST CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("\nCheck your LinkedIn feed to see the post with document.")

    except LinkedInAPIError as e:
        print(f"\n❌ LinkedIn API Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify your access token has the correct scopes:")
        print("     - w_member_social (post content)")
        print("     - Documents permissions")
        print("  2. Check token hasn't expired")
        print("  3. Verify person URN is correct")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()


async def test_upload_only():
    """Test just uploading a document without posting"""

    print("\n" + "=" * 60)
    print("LINKEDIN DOCUMENT UPLOAD ONLY TEST")
    print("=" * 60)

    # Initialize client
    try:
        client = LinkedInClient()

        # Validate configuration
        is_valid, missing = client.validate_config()
        if not is_valid:
            print("\n❌ LinkedIn API not configured!")
            print(f"Missing: {', '.join(missing)}")
            return

        print("\n✓ Client initialized")

    except Exception as e:
        print(f"\n❌ Error initializing client: {e}")
        return

    # Get test document
    test_doc = Path(__file__).parent.parent / "test_files" / "test_document.pdf"

    if not test_doc.exists():
        print(f"\n❌ Test document not found: {test_doc}")
        return

    print(f"\n✓ Test document: {test_doc.name}")

    response = input("\nUpload document to LinkedIn? (yes/no): ").strip().lower()

    if response != "yes":
        print("\n❌ Cancelled")
        return

    try:
        print("\n📤 Uploading...")
        document_urn = await client.upload_document(test_doc, title="Test Upload")

        print("\n✓ Upload successful!")
        print(f"  Document URN: {document_urn}")
        print("\nYou can now use this URN to attach the document to a post.")

    except LinkedInAPIError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Main entry point"""

    print("\nLinkedIn Document Upload Test")
    print("\nOptions:")
    print("  1. Upload document and create post")
    print("  2. Upload document only (no post)")
    print("  3. Cancel")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        asyncio.run(test_document_upload())
    elif choice == "2":
        asyncio.run(test_upload_only())
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()
