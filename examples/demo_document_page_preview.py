"""
Demo: Document page preview with actual page rendering

Shows how to preview a post with a document attachment where
the actual pages/slides are rendered as images (like LinkedIn does).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import time

from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.preview import LinkedInPreview
from chuk_mcp_linkedin.themes.theme_manager import ThemeManager
from chuk_mcp_linkedin.utils.document_converter import DocumentConverter


def create_pdf_preview():
    """Create a post with PDF attachment showing actual pages"""

    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("document", theme=theme)

    post.add_hook("question", "How do you share detailed insights with your network?")

    post.add_body(
        """PDFs are perfect for sharing:

→ Research findings
→ Case studies
→ Technical reports
→ Strategic frameworks

LinkedIn converts each page to an image carousel.""",
        structure="linear",
    )

    post.add_cta("curiosity", "What's your preferred format for long-form content?")

    post.add_hashtags(["ContentStrategy", "ThoughtLeadership", "PDFs"])

    # Get text content
    text_content = post.compose()

    # Get test PDF file
    pdf_path = Path(__file__).parent.parent / "test_files" / "test_document.pdf"

    # Get page count
    page_count = DocumentConverter.get_page_count(str(pdf_path))

    print("\n" + "=" * 60)
    print("DOCUMENT PREVIEW WITH PAGE RENDERING")
    print("=" * 60)
    print(f"Document: {pdf_path.name}")
    print(f"Pages: {page_count}")
    print("Type: PDF")
    print()

    # Create preview with document metadata
    draft_data = {
        "name": "Post with PDF Pages",
        "post_type": "document",
        "content": {
            "composed_text": text_content,
            "document_file": {
                "filename": pdf_path.name,
                "filepath": str(pdf_path),
                "title": "Strategy Framework",
                "pages": page_count,
                "file_type": "pdf",
            },
        },
        "theme": theme.name,
    }

    stats = {
        "char_count": len(text_content),
        "word_count": len(text_content.split()),
        "char_remaining": 3000 - len(text_content),
        "hashtag_count": 3,
        "has_hook": True,
        "has_cta": True,
    }

    # Generate preview (this will convert PDF to images automatically)
    print("Converting PDF pages to images...")
    html_preview = LinkedInPreview.generate_html(draft_data, stats=stats)

    # Save preview
    preview_dir = Path.home() / ".linkedin_drafts" / "previews" / "documents"
    preview_dir.mkdir(parents=True, exist_ok=True)
    preview_path = preview_dir / f"pdf_page_preview_{int(time.time())}.html"
    saved_path = LinkedInPreview.save_preview(html_preview, str(preview_path))

    print("\n✓ PDF converted to images")
    print(f"✓ Preview saved: {saved_path}")
    print("\nThe preview shows:")
    print("  • Post text with hook and CTA")
    print("  • Interactive carousel with ACTUAL PDF pages as images")
    print("  • Page navigation (prev/next buttons)")
    print("  • Page indicators and counter")
    print("  • LinkedIn-style formatting")

    return saved_path


def create_pptx_preview():
    """Create a post with PowerPoint attachment"""

    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    post = ComposablePost("document", theme=theme)

    post.add_hook("stat", "70% of B2B buyers prefer visual content")

    post.add_body(
        """That's why I use slide decks to share:

📊 Data insights
📈 Performance metrics
🎯 Strategic roadmaps
💡 Framework breakdowns

Each slide becomes part of an interactive carousel.""",
        structure="linear",
    )

    post.add_cta("action", "Save this for your next presentation")

    post.add_hashtags(["Presentations", "DataViz", "B2B"])

    # Get text content
    text_content = post.compose()

    # Get test PPTX file
    pptx_path = Path(__file__).parent.parent / "test_files" / "test_presentation.pptx"

    # Get slide count
    slide_count = DocumentConverter.get_page_count(str(pptx_path))

    print("\n" + "=" * 60)
    print("POWERPOINT PREVIEW WITH SLIDE RENDERING")
    print("=" * 60)
    print(f"Document: {pptx_path.name}")
    print(f"Slides: {slide_count}")
    print("Type: PPTX")
    print()

    # Create preview with document metadata
    draft_data = {
        "name": "Post with PowerPoint Slides",
        "post_type": "document",
        "content": {
            "composed_text": text_content,
            "document_file": {
                "filename": pptx_path.name,
                "filepath": str(pptx_path),
                "title": "Q4 Performance Review",
                "pages": slide_count,
                "file_type": "pptx",
            },
        },
        "theme": theme.name,
    }

    stats = {
        "char_count": len(text_content),
        "word_count": len(text_content.split()),
        "char_remaining": 3000 - len(text_content),
        "hashtag_count": 3,
        "has_hook": True,
        "has_cta": True,
    }

    # Generate preview
    print("Converting PowerPoint slides to images...")
    html_preview = LinkedInPreview.generate_html(draft_data, stats=stats)

    # Save preview
    preview_dir = Path.home() / ".linkedin_drafts" / "previews" / "documents"
    preview_dir.mkdir(parents=True, exist_ok=True)
    preview_path = preview_dir / f"pptx_page_preview_{int(time.time())}.html"
    saved_path = LinkedInPreview.save_preview(html_preview, str(preview_path))

    print("\n✓ PowerPoint converted to images")
    print(f"✓ Preview saved: {saved_path}")

    return saved_path


def main():
    """Run all document preview demos"""

    print("\n" + "=" * 60)
    print("LINKEDIN DOCUMENT PAGE PREVIEW DEMO")
    print("=" * 60)
    print("\nThis demo shows how documents are converted to images")
    print("for preview, just like LinkedIn does with PDF/PPTX uploads.")
    print("\nNote: Requires preview dependencies:")
    print("  pip install chuk-mcp-linkedin[preview]")
    print()

    try:
        # Test PDF preview
        pdf_preview = create_pdf_preview()

        # Test PPTX preview
        pptx_preview = create_pptx_preview()

        print("\n" + "=" * 60)
        print("PREVIEW COMPLETE")
        print("=" * 60)
        print("\nGenerated previews:")
        print(f"  • PDF:  file://{pdf_preview}")
        print(f"  • PPTX: file://{pptx_preview}")
        print("\nOpen these files in your browser to see the rendered pages!")
        print("\nFeatures:")
        print("  ✓ Actual document pages rendered as images")
        print("  ✓ Interactive carousel navigation")
        print("  ✓ Page counter and indicators")
        print("  ✓ Cached for performance (won't re-convert)")
        print("  ✓ LinkedIn-style preview formatting")

    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease install preview dependencies:")
        print("  pip install chuk-mcp-linkedin[preview]")
        print("\nFor PDF support, you also need poppler:")
        print("  macOS:   brew install poppler")
        print("  Ubuntu:  sudo apt-get install poppler-utils")
        print("  Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
