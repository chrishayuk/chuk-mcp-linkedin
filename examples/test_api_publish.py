"""
Test script for LinkedIn API publishing.

Demonstrates the complete workflow:
1. Create a draft using design system components
2. Compose the post with theme and optimization
3. Preview the post
4. Publish to LinkedIn (with dry-run option)

Usage:
    # Dry run (no actual posting)
    python examples/test_api_publish.py

    # Actually publish (requires .env configuration)
    python examples/test_api_publish.py --publish
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin import LinkedInManager
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.api import LinkedInClient, config


async def main():
    """Run the test workflow"""

    print("=" * 60)
    print("LinkedIn API Publishing Test")
    print("=" * 60)
    print()

    # Check if --publish flag is set
    should_publish = "--publish" in sys.argv

    # Initialize manager and theme
    manager = LinkedInManager()
    theme_mgr = ThemeManager()
    client = LinkedInClient()

    # Check API configuration
    print("1. Checking LinkedIn API configuration...")
    is_configured = config.is_configured()

    if is_configured:
        print("   ✓ LinkedIn API is configured")
        print(f"   Person URN: {config.linkedin_person_urn}")
        print(f"   Publishing enabled: {config.enable_publishing}")
    else:
        missing = config.get_missing_config()
        print(f"   ✗ Missing configuration: {', '.join(missing)}")
        print("   See .env.example for setup instructions")

        if should_publish:
            print("\n   Cannot publish without configuration. Exiting.")
            return

    print()

    # Test connection if configured
    if is_configured:
        print("2. Testing LinkedIn API connection...")
        is_valid = await client.test_connection()
        if is_valid:
            print("   ✓ Connection successful!")
        else:
            print("   ✗ Connection failed - check your access token")
            if should_publish:
                return
        print()

    # Create a draft
    print("3. Creating draft post...")
    draft = manager.create_draft(
        name="Test API Post",
        post_type="text",
        theme="thought_leader"
    )
    print(f"   ✓ Created draft: {draft.draft_id}")
    print()

    # Get theme
    theme = theme_mgr.get_theme("thought_leader")

    # Build post using composition
    print("4. Composing post with components...")
    post = ComposablePost("text", theme=theme)

    # Add hook
    post.add_hook(
        "stat",
        "80% of LinkedIn posts get zero engagement."
    )

    # Add body
    post.add_body(
        """Here's why most posts fail (and how to fix it):

→ Weak hook - People scroll past in 2 seconds
→ No value - Just promoting, not helping
→ Poor formatting - Walls of text nobody reads
→ Missing CTA - No invitation to engage

The algorithm rewards posts that start conversations, not broadcasts.

Start treating LinkedIn like a conversation platform, not a megaphone.""",
        structure="listicle"
    )

    # Add CTA
    post.add_cta(
        "curiosity",
        "What's the biggest mistake you see on LinkedIn?"
    )

    # Add hashtags
    post.add_hashtags(
        ["LinkedInTips", "ContentStrategy", "ThoughtLeadership"],
        placement="end"
    )

    # Optimize
    post.optimize_for_engagement()

    # Compose
    final_text = post.compose()

    print(f"   ✓ Post composed ({len(final_text)} characters)")
    print()

    # Save composed text to draft
    draft.content["composed_text"] = final_text
    manager.update_draft(draft.draft_id, content=draft.content)

    # Show preview
    print("5. Post preview:")
    print("-" * 60)
    print(final_text)
    print("-" * 60)
    print()

    # Show first 210 chars (visible before "see more")
    preview = final_text[:210]
    print("6. Hook preview (first 210 chars - visible before 'see more'):")
    print("-" * 60)
    print(preview + "..." if len(final_text) > 210 else preview)
    print("-" * 60)
    print()

    # Publish logic
    if should_publish:
        if not is_configured:
            print("7. Cannot publish - LinkedIn API not configured")
            return

        if not config.enable_publishing:
            print("7. Publishing disabled in config (ENABLE_PUBLISHING=false)")
            print("   Set ENABLE_PUBLISHING=true in .env to enable actual publishing")
            print()
            print("   Running DRY RUN instead...")
            print("-" * 60)
            print(f"Would publish to LinkedIn:")
            print(f"  Visibility: PUBLIC")
            print(f"  Length: {len(final_text)} characters")
            print("-" * 60)
        else:
            print("7. Publishing to LinkedIn...")
            try:
                result = await client.create_text_post(
                    text=final_text,
                    visibility="PUBLIC"
                )

                post_id = result.get("id", "unknown")
                print(f"   ✓ Successfully published!")
                print(f"   Post ID: {post_id}")
                print()
                print("   View your post on LinkedIn!")

            except Exception as e:
                print(f"   ✗ Failed to publish: {e}")
    else:
        print("7. DRY RUN (use --publish flag to actually post)")
        print("-" * 60)
        print(f"Would publish to LinkedIn:")
        print(f"  Visibility: PUBLIC")
        print(f"  Length: {len(final_text)} characters")
        print(f"  Publishing enabled: {config.enable_publishing}")
        print("-" * 60)
        print()
        print("To publish for real:")
        print("  1. Configure .env with your LinkedIn credentials")
        print("  2. Set ENABLE_PUBLISHING=true")
        print("  3. Run: python examples/test_api_publish.py --publish")

    print()
    print("=" * 60)
    print("Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
