#!/usr/bin/env python3
"""
Example: Generate HTML preview of LinkedIn posts

This example demonstrates how to:
1. Create a LinkedIn post draft
2. Add content using composition
3. Generate an HTML preview
4. View it in your browser
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.manager import LinkedInManager
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager


def main():
    """Run the preview example"""

    # Initialize manager and theme manager
    manager = LinkedInManager()
    theme_mgr = ThemeManager()

    print("🎨 LinkedIn Post Preview Example\n")

    # Create a new draft
    print("Creating new post draft...")
    draft = manager.create_draft(
        name="Thought Leadership Example",
        post_type="text",
        theme="thought_leader",
    )

    # Add content using composition
    print("Adding content components...")

    # Add hook
    draft.content.setdefault("components", []).append(
        {
            "component": "hook",
            "type": "stat",
            "content": "80% of B2B decision makers prefer thought leadership content over ads.",
        }
    )

    # Add body
    draft.content.setdefault("components", []).append(
        {
            "component": "body",
            "content": """Yet most companies just promote.

Here's what actually works:

→ Lead with insights, not products
→ Share frameworks, not features
→ Tell stories, not sales pitches
→ Build trust, not transactions

The algorithm rewards value.""",
            "structure": "listicle",
        }
    )

    # Add CTA
    draft.content.setdefault("components", []).append(
        {"component": "cta", "type": "curiosity", "text": "What's your content strategy?"}
    )

    # Add hashtags
    draft.content.setdefault("components", []).append(
        {
            "component": "hashtags",
            "tags": ["LinkedInTips", "ThoughtLeadership", "ContentStrategy"],
            "placement": "end",
        }
    )

    # Compose the final text
    from chuk_mcp_linkedin.composition import ComposablePost

    theme = theme_mgr.get_theme("thought_leader")
    post = ComposablePost("text", theme=theme)

    for comp in draft.content.get("components", []):
        comp_type = comp.get("component")
        if comp_type == "hook":
            post.add_hook(comp["type"], comp["content"])
        elif comp_type == "body":
            post.add_body(comp["content"], comp.get("structure"))
        elif comp_type == "cta":
            post.add_cta(comp["type"], comp["text"])
        elif comp_type == "hashtags":
            post.add_hashtags(comp["tags"], comp.get("placement", "end"))

    post.optimize_for_engagement()
    final_text = post.compose()

    # Update draft with composed text
    draft.content["composed_text"] = final_text
    manager.update_draft(draft.draft_id, content=draft.content)

    print(f"✓ Draft created: {draft.name}\n")

    # Generate HTML preview
    print("Generating HTML preview...")
    preview_path = manager.generate_html_preview(draft.draft_id)

    if preview_path:
        print(f"✓ Preview saved to: {preview_path}\n")

        # Open in browser
        print("Opening preview in browser...")
        import webbrowser
        import os

        file_url = f"file://{os.path.abspath(preview_path)}"
        webbrowser.open(file_url)

        print("✓ Preview opened in browser!\n")
        print("📊 Preview includes:")
        print("  • LinkedIn-style post card")
        print("  • Character count and stats")
        print("  • Engagement indicators")
        print("  • Full post content with formatting")
        print("\n💡 Tip: Keep the preview open and regenerate to see changes in real-time!")

    else:
        print("❌ Failed to generate preview")


if __name__ == "__main__":
    main()
