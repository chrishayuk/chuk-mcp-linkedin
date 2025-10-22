"""
Showcase different media attachment types in LinkedIn post preview.

Demonstrates:
1. Single image post
2. Multiple images post (2-4 images)
3. Video post
4. Document file post (PDF/PPTX/DOCX)
5. Mixed content post
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager
from chuk_mcp_linkedin.preview import LinkedInPreview
import time


def create_single_image_post():
    """Example 1: Post with single image"""
    print("\n" + "="*60)
    print("CREATING: Single Image Post")
    print("="*60)

    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("text", theme=theme)

    post.add_hook(
        "insight",
        "This is what a LinkedIn post with an image looks like."
    )

    post.add_body("Images make your posts 2.3x more engaging.\n\nUse high-quality visuals that support your message.", structure="linear")

    post.add_hashtags(["ContentStrategy", "VisualContent"])

    # Compose text
    text_content = post.compose()

    # Create draft with image
    draft_data = {
        "name": "Single Image Post",
        "post_type": "image",
        "content": {
            "composed_text": text_content,
            "images": [{
                "filepath": str(Path(__file__).parent.parent / "test_files" / "test_image_1.png"),
                "alt_text": "LinkedIn post image example"
            }]
        },
        "theme": theme.name
    }

    return post, theme, draft_data, "single_image_post"


def create_multiple_images_post():
    """Example 2: Post with multiple images (grid layout)"""
    print("\n" + "="*60)
    print("CREATING: Multiple Images Post (4-image grid)")
    print("="*60)

    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("personal_brand")

    post = ComposablePost("text", theme=theme)

    post.add_hook(
        "story",
        "Behind the scenes of our product launch 🚀"
    )

    post.add_body("""Swipe through to see:

→ The team brainstorming
→ Design iterations
→ Beta testing phase
→ Launch day celebration

It takes a village to ship great products.""", structure="linear")

    post.add_hashtags(["ProductLaunch", "Teamwork", "BehindTheScenes"])

    text_content = post.compose()

    # Create draft with 4 images
    test_files_dir = Path(__file__).parent.parent / "test_files"
    draft_data = {
        "name": "Multiple Images Post",
        "post_type": "image",
        "content": {
            "composed_text": text_content,
            "images": [
                {"filepath": str(test_files_dir / "test_image_1.png"), "alt_text": "Brainstorming session"},
                {"filepath": str(test_files_dir / "test_image_2.png"), "alt_text": "Design iterations"},
                {"filepath": str(test_files_dir / "test_image_3.png"), "alt_text": "Beta testing"},
                {"filepath": str(test_files_dir / "test_image_4.png"), "alt_text": "Launch celebration"},
            ]
        },
        "theme": theme.name
    }

    return post, theme, draft_data, "multiple_images_post"


def create_video_post():
    """Example 3: Post with video"""
    print("\n" + "="*60)
    print("CREATING: Video Post")
    print("="*60)

    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("storyteller")

    post = ComposablePost("text", theme=theme)

    post.add_hook(
        "bold",
        "Watch this 2-minute demo that changed everything."
    )

    post.add_body("""We spent 6 months building this feature.

The result? Our users can now accomplish in 30 seconds what used to take 10 minutes.

Video shows the before vs. after.""", structure="linear")

    post.add_cta("action", "What feature would save you the most time?")

    post.add_hashtags(["ProductDemo", "Innovation", "UX"])

    text_content = post.compose()

    # Create draft with video
    draft_data = {
        "name": "Video Post",
        "post_type": "video",
        "content": {
            "composed_text": text_content,
            "video": {
                "title": "Product Demo",
                "duration": "2:15",
                "thumbnail": str(Path(__file__).parent.parent / "test_files" / "video_thumbnail.png"),
            }
        },
        "theme": theme.name
    }

    return post, theme, draft_data, "video_post"


def create_document_file_post():
    """Example 4: Post with document file attachment"""
    print("\n" + "="*60)
    print("CREATING: Document File Post")
    print("="*60)

    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("data_driven")

    post = ComposablePost("text", theme=theme)

    post.add_hook(
        "value",
        "I'm sharing our complete 2025 content strategy framework."
    )

    post.add_body("""12 months of research distilled into one actionable guide.

Inside you'll find:

→ Content calendar template
→ Topic ideation framework
→ Distribution checklist
→ Performance metrics

100% free. No email required.""", structure="linear")

    post.add_cta("value", "Download it and let me know what you think!")

    post.add_hashtags(["ContentStrategy", "Marketing", "FreeResource"])

    text_content = post.compose()

    # Create draft with document file
    draft_data = {
        "name": "Document File Post",
        "post_type": "document",
        "content": {
            "composed_text": text_content,
            "document_file": {
                "filename": "2025_Content_Strategy_Framework.pdf",
                "file_type": "PDF",
                "pages": 24,
                "size": "2.4 MB",
                "filepath": str(Path(__file__).parent.parent / "test_files" / "test_document.pdf"),
            }
        },
        "theme": theme.name
    }

    return post, theme, draft_data, "document_file_post"


def create_presentation_file_post():
    """Example 5: Post with PowerPoint presentation"""
    print("\n" + "="*60)
    print("CREATING: Presentation File Post")
    print("="*60)

    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("coach_mentor")

    post = ComposablePost("text", theme=theme)

    post.add_hook(
        "how_to",
        "My exact pitch deck template that raised $2M."
    )

    post.add_body("""After 50+ investor meetings, here's what works:

✓ Problem slide (1 slide)
✓ Solution slide (1 slide)
✓ Traction slide (1 slide with BIG numbers)
✓ Team slide (1 slide)
✓ Ask slide (1 slide)

That's it. 5 slides.

Download the template below.""", structure="linear")

    post.add_hashtags(["Startups", "Fundraising", "PitchDeck"])

    text_content = post.compose()

    # Create draft with PPTX file
    draft_data = {
        "name": "Presentation File Post",
        "post_type": "document",
        "content": {
            "composed_text": text_content,
            "document_file": {
                "filename": "Pitch_Deck_Template.pptx",
                "file_type": "PPTX",
                "pages": 5,
                "size": "892 KB",
                "filepath": str(Path(__file__).parent.parent / "test_files" / "test_presentation.pptx"),
            }
        },
        "theme": theme.name
    }

    return post, theme, draft_data, "presentation_file_post"


def generate_preview(post, theme, draft_data, name):
    """Generate and save preview for a media post"""
    text_content = draft_data["content"]["composed_text"]

    print(f"\n--- PREVIEW ({name}) ---")
    print(f"Type: {draft_data['post_type']}")
    print(f"Text: {text_content[:100]}...")

    # Check what media is included
    content = draft_data["content"]
    if "images" in content:
        print(f"Images: {len(content['images'])} image(s)")
    if "video" in content:
        print("Video: Yes")
    if "document_file" in content:
        print(f"Document: {content['document_file']['filename']}")

    stats = {
        "char_count": len(text_content),
        "word_count": len(text_content.split()),
        "char_remaining": 3000 - len(text_content),
        "hashtag_count": len([line for line in text_content.split('\n') if '#' in line]),
        "has_hook": True,
        "has_cta": True,
    }

    html_preview = LinkedInPreview.generate_html(
        draft_data,
        stats=stats
    )

    preview_path = f".linkedin_drafts/previews/media/{name}_{int(time.time())}.html"
    saved_path = LinkedInPreview.save_preview(html_preview, preview_path)

    print(f"✓ Preview saved: {saved_path}")
    return saved_path


def main():
    """Generate all media type examples"""
    print("="*60)
    print("LINKEDIN MEDIA TYPES SHOWCASE")
    print("="*60)
    print("Generating previews for different media types...")

    # Create media directory
    Path(".linkedin_drafts/previews/media").mkdir(parents=True, exist_ok=True)

    examples = [
        create_single_image_post,
        create_multiple_images_post,
        create_video_post,
        create_document_file_post,
        create_presentation_file_post,
    ]

    preview_paths = []

    for example_func in examples:
        post, theme, draft_data, name = example_func()
        preview_path = generate_preview(post, theme, draft_data, name)
        preview_paths.append(preview_path)

    print("\n" + "="*60)
    print("ALL MEDIA PREVIEWS GENERATED")
    print("="*60)
    print(f"\nGenerated {len(preview_paths)} preview files:\n")

    for i, path in enumerate(preview_paths, 1):
        filename = Path(path).name
        print(f"{i}. {filename}")

    print(f"\nOpen them in your browser:")
    print(f"  cd .linkedin_drafts/previews/media")
    print(f"  open *.html")

    return preview_paths


if __name__ == "__main__":
    previews = main()
