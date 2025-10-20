#!/usr/bin/env python3
"""
Quick CLI utility to preview LinkedIn posts.

Usage:
    python preview_post.py                    # Preview current draft
    python preview_post.py draft_id_here      # Preview specific draft
    python preview_post.py --list             # List all drafts
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from chuk_mcp_linkedin.manager import LinkedInManager
import webbrowser
import os


def main():
    manager = LinkedInManager()

    # Handle --list flag
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        drafts = manager.list_drafts()
        if not drafts:
            print("No drafts found. Create one first!")
            return

        print("\n📝 Available Drafts:\n")
        for draft in drafts:
            current_marker = "→" if draft["is_current"] else " "
            print(f"{current_marker} {draft['name']}")
            print(f"  ID: {draft['draft_id']}")
            print(f"  Type: {draft['post_type']}")
            print(f"  Theme: {draft['theme'] or 'None'}")
            print(f"  Updated: {draft['updated_at'][:19]}")
            print()
        return

    # Determine which draft to preview
    if len(sys.argv) > 1:
        draft_id = sys.argv[1]
        draft = manager.get_draft(draft_id)
        if not draft:
            print(f"❌ Draft '{draft_id}' not found")
            print("\nTry: python preview_post.py --list")
            return
    else:
        draft = manager.get_current_draft()
        if not draft:
            print("❌ No current draft found")
            print("\nTry: python preview_post.py --list")
            return
        draft_id = draft.draft_id

    # Generate and open preview
    print(f"🎨 Generating preview for '{draft.name}'...")
    preview_path = manager.generate_html_preview(draft_id)

    if preview_path:
        print(f"✓ Preview saved to: {preview_path}")
        file_url = f"file://{os.path.abspath(preview_path)}"
        webbrowser.open(file_url)
        print("✓ Opened in browser!")
    else:
        print("❌ Failed to generate preview")


if __name__ == "__main__":
    main()
