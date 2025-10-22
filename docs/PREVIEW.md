# LinkedIn Post Preview System

The preview system generates pixel-perfect HTML previews of LinkedIn posts before publishing. See exactly how your content will appear on LinkedIn with real-time analytics and optimization recommendations.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Text Post Previews](#text-post-previews)
- [Document Post Previews](#document-post-previews)
- [Media Post Previews](#media-post-previews)
- [Preview Components](#preview-components)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)

## Features

### Visual Preview
- **Authentic LinkedIn UI**: Accurate post card styling including avatar, header, actions
- **Proper formatting**: Line breaks, hashtag highlighting, emoji rendering
- **"See more" indicator**: Visual marker at 210 characters (LinkedIn's truncation point)
- **Document pages**: Actual PDF/PowerPoint/Word pages rendered as images
- **Interactive carousels**: Navigate through multi-page documents
- **Media attachments**: Images, videos, and document files

### Analytics Dashboard
- **Character analysis**: Total count, optimal length indicators, remaining characters
- **Word count**: Track post length
- **Hashtag optimization**: Count analysis with optimal range (3-5)
- **Component detection**: Identifies hooks, CTAs, and engagement elements
- **Performance indicators**: Warnings for too short/long posts

### Document Preview (with `[preview]` dependencies)
- **PDF rendering**: Converts PDF pages to images using pdf2image + poppler
- **PowerPoint support**: Renders PPTX slides as carousel
- **Word documents**: Displays DOCX pages
- **Smart caching**: Converts once, reuses on subsequent previews
- **LinkedIn-accurate**: Matches LinkedIn's actual document post rendering

## Installation

### Basic Installation

```bash
pip install chuk-mcp-linkedin
```

### With Document Preview Support

For rendering actual document pages (PDF, PowerPoint, Word):

```bash
# Install with preview dependencies
pip install chuk-mcp-linkedin[preview]

# System requirements for PDF support (poppler)
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
```

The `[preview]` dependencies include:
- `pdf2image` - PDF to image conversion (requires poppler)
- `Pillow` - Image processing and manipulation
- `python-pptx` - PowerPoint file support
- `python-docx` - Word document support
- `PyPDF2` - PDF utilities and page counting

## Quick Start

### Preview Your First Post (60 seconds)

```python
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.preview import LinkedInPreview
from chuk_mcp_linkedin.themes import ThemeManager

# Create a post
theme_mgr = ThemeManager()
theme = theme_mgr.get_theme("thought_leader")

post = ComposablePost("text", theme=theme)
post.add_hook("stat", "80% of B2B buyers prefer thought leadership over ads")
post.add_body("Yet most companies just promote. Here's what works instead...")
post.add_cta("curiosity", "What's your take?")
post.add_hashtags(["ThoughtLeadership", "B2B", "ContentStrategy"])

# Generate preview
text = post.compose()
draft_data = {
    "name": "Thought Leadership Post",
    "post_type": "text",
    "content": {"composed_text": text},
    "theme": theme.name
}

stats = {
    "char_count": len(text),
    "word_count": len(text.split()),
    "char_remaining": 3000 - len(text),
    "hashtag_count": 3,
    "has_hook": True,
    "has_cta": True
}

html = LinkedInPreview.generate_html(draft_data, stats=stats, composable_post=post)
preview_path = LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/my_post.html")

print(f"Preview saved: {preview_path}")
# Opens automatically in browser
```

### CLI Preview Tool

The fastest way to preview existing drafts:

```bash
# Preview current draft
python preview_post.py

# Preview specific draft
python preview_post.py draft_id_here

# List all available drafts
python preview_post.py --list
```

## Text Post Previews

Text posts include the post text, hashtags, and engagement analytics.

```python
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.preview import LinkedInPreview

post = ComposablePost("text")
post.add_hook("question", "What's your biggest LinkedIn challenge?")
post.add_body("Most professionals struggle with:\n\n→ Creating consistent content\n→ Growing engagement\n→ Converting leads")
post.add_cta("action", "Comment below!")
post.add_hashtags(["LinkedIn", "ContentMarketing"])

text = post.compose()

draft_data = {
    "name": "Engagement Question",
    "post_type": "text",
    "content": {"composed_text": text}
}

html = LinkedInPreview.generate_html(draft_data)
LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/question_post.html")
```

## Document Post Previews

Document posts render actual PDF, PowerPoint, or Word pages as images in an interactive carousel.

### PDF Document

```python
from pathlib import Path
from chuk_mcp_linkedin.composition import ComposablePost
from chuk_mcp_linkedin.preview import LinkedInPreview
from chuk_mcp_linkedin.utils.document_converter import DocumentConverter

# Create post
post = ComposablePost("document")
post.add_hook("question", "How do you share detailed insights with your network?")
post.add_body("PDFs are perfect for sharing research findings and strategic frameworks.")
post.add_cta("curiosity", "What's your preferred format for long-form content?")
post.add_hashtags(["ContentStrategy", "ThoughtLeadership"])

text = post.compose()

# Set up document
pdf_path = Path("./reports/Q4_strategy.pdf")
page_count = DocumentConverter.get_page_count(str(pdf_path))

draft_data = {
    "name": "Q4 Strategy Report",
    "post_type": "document",
    "content": {
        "composed_text": text,
        "document_file": {
            "filename": pdf_path.name,
            "filepath": str(pdf_path),
            "title": "Q4 Strategy Framework",
            "pages": page_count,
            "file_type": "pdf"
        }
    }
}

# Generate preview with rendered pages
html = LinkedInPreview.generate_html(draft_data, composable_post=post)
preview_path = LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/pdf_post.html")

# Opens browser showing:
# - Post text with commentary
# - Interactive carousel with actual PDF pages as images
# - Navigation controls (prev/next buttons)
# - Page counter (1 / 12)
# - Page indicators
```

### PowerPoint Presentation

```python
pptx_path = Path("./presentations/pitch_deck.pptx")
slide_count = DocumentConverter.get_page_count(str(pptx_path))

draft_data = {
    "name": "Pitch Deck",
    "post_type": "document",
    "content": {
        "composed_text": post.compose(),
        "document_file": {
            "filename": pptx_path.name,
            "filepath": str(pptx_path),
            "title": "Company Pitch Deck 2025",
            "pages": slide_count,
            "file_type": "pptx"
        }
    }
}

html = LinkedInPreview.generate_html(draft_data, composable_post=post)
LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/pptx_post.html")
```

### Word Document

```python
docx_path = Path("./reports/whitepaper.docx")
page_count = DocumentConverter.get_page_count(str(docx_path))

draft_data = {
    "name": "Industry Whitepaper",
    "post_type": "document",
    "content": {
        "composed_text": post.compose(),
        "document_file": {
            "filename": docx_path.name,
            "filepath": str(docx_path),
            "title": "AI in Enterprise: 2025 Trends",
            "pages": page_count,
            "file_type": "docx"
        }
    }
}

html = LinkedInPreview.generate_html(draft_data, composable_post=post)
LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/docx_post.html")
```

## Media Post Previews

### Single Image

```python
draft_data = {
    "name": "Product Launch",
    "post_type": "image",
    "content": {
        "composed_text": "Excited to announce our new product! 🚀",
        "images": [{
            "filepath": "/path/to/product.jpg",
            "alt_text": "Product screenshot"
        }]
    }
}

html = LinkedInPreview.generate_html(draft_data)
LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/image_post.html")
```

### Multiple Images

```python
draft_data = {
    "name": "Event Recap",
    "post_type": "image",
    "content": {
        "composed_text": "Great event yesterday! Here are some highlights 📸",
        "images": [
            {"filepath": "/path/to/photo1.jpg", "alt_text": "Team photo"},
            {"filepath": "/path/to/photo2.jpg", "alt_text": "Keynote"},
            {"filepath": "/path/to/photo3.jpg", "alt_text": "Networking"},
            {"filepath": "/path/to/photo4.jpg", "alt_text": "Panel discussion"}
        ]
    }
}

html = LinkedInPreview.generate_html(draft_data)
LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/multi_image_post.html")
```

### Video Post

```python
draft_data = {
    "name": "Product Demo",
    "post_type": "video",
    "content": {
        "composed_text": "Watch our latest product demo 🎥",
        "video": {
            "title": "Product Demo v2.0",
            "duration": "2:30",
            "thumbnail": "/path/to/thumbnail.jpg"
        }
    }
}

html = LinkedInPreview.generate_html(draft_data)
LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/video_post.html")
```

## Preview Components

### Post Card Elements

The preview includes all LinkedIn post card elements:

**Header**:
- Profile avatar (circular, gradient background)
- Author name ("Your Name" placeholder)
- Author headline ("Your Headline • 1st")
- Post timestamp ("Just now • 🌍")

**Content Area**:
- Post text with proper formatting
- Line breaks preserved
- Hashtags highlighted in LinkedIn blue (#0a66c2)
- "See more" link at 210 characters
- Expandable/collapsible full text

**Media Attachments**:
- Images (single or grid layout)
- Videos (with play button and duration)
- Documents (carousel with page navigation)

**Actions Bar**:
- Like button (👍)
- Comment button (💬)
- Repost button (🔄)
- Send button (📤)

### Analytics Dashboard

**Character Analysis**:
- Total characters with optimal range indicators
- Too short warning (< 150 chars)
- Optimal length badge (300-800 chars)
- Long post warning (> 2000 chars)

**Engagement Metrics**:
- Word count
- Characters remaining (out of 3000)
- Hashtag count with optimization (3-5 optimal)
- Hook detection (✓ Yes / ❌ No)
- CTA detection (✓ Yes / ❌ No)

## Advanced Usage

### Custom Styling

Override default LinkedIn styling:

```python
# Custom preview with your brand colors
custom_css = """
<style>
    .post-card { border: 2px solid #yourcolor; }
    .author-name { color: #yourcolor; }
</style>
"""

html = LinkedInPreview.generate_html(draft_data)
html = html.replace('</head>', f'{custom_css}</head>')
LinkedInPreview.save_preview(html, ".linkedin_drafts/previews/branded.html")
```

### Document Conversion Options

Control document rendering quality and caching:

```python
from chuk_mcp_linkedin.utils.document_converter import DocumentConverter

# High-quality rendering (larger files, better quality)
page_images = DocumentConverter.convert_to_images(
    filepath="report.pdf",
    max_pages=20,  # LinkedIn's limit
    dpi=300  # High quality (default: 150)
)

# Clear cache for a specific document
cache_key = DocumentConverter._get_cache_key("report.pdf")
DocumentConverter.clear_cache(cache_key)

# Clear all cached documents
DocumentConverter.clear_cache()
```

### Batch Preview Generation

Generate previews for multiple posts:

```python
from pathlib import Path

posts = [
    {"name": "Post 1", "content": {...}},
    {"name": "Post 2", "content": {...}},
    {"name": "Post 3", "content": {...}}
]

preview_dir = Path(".linkedin_drafts/previews/batch")
preview_dir.mkdir(parents=True, exist_ok=True)

for i, post_data in enumerate(posts):
    html = LinkedInPreview.generate_html(post_data)
    preview_path = preview_dir / f"post_{i+1}.html"
    LinkedInPreview.save_preview(html, str(preview_path))
    print(f"✓ Generated: {preview_path}")
```

## API Reference

### `LinkedInPreview`

Main class for generating HTML previews.

#### `generate_html(draft_data, stats=None, composable_post=None)`

Generate HTML preview of a LinkedIn post.

**Parameters**:
- `draft_data` (Dict[str, Any]): Draft data containing post content
  - `name` (str): Draft name
  - `post_type` (str): Type of post (text, document, image, video, etc.)
  - `content` (Dict): Post content including text and media
  - `theme` (str, optional): Theme name
- `stats` (Dict[str, Any], optional): Analytics data
  - `char_count` (int): Character count
  - `word_count` (int): Word count
  - `char_remaining` (int): Characters remaining
  - `hashtag_count` (int): Number of hashtags
  - `has_hook` (bool): Whether post has a hook
  - `has_cta` (bool): Whether post has a CTA
- `composable_post` (ComposablePost, optional): ComposablePost instance for document embeds

**Returns**: `str` - HTML content

**Example**:
```python
html = LinkedInPreview.generate_html(
    draft_data={
        "name": "My Post",
        "post_type": "text",
        "content": {"composed_text": "Hello LinkedIn!"}
    },
    stats={
        "char_count": 15,
        "word_count": 2,
        "char_remaining": 2985,
        "hashtag_count": 0,
        "has_hook": False,
        "has_cta": False
    }
)
```

#### `save_preview(html_content, output_path)`

Save HTML preview to file.

**Parameters**:
- `html_content` (str): HTML content to save
- `output_path` (str): Path to save file (relative or absolute)

**Returns**: `str` - Absolute path to saved file

**Example**:
```python
path = LinkedInPreview.save_preview(
    html_content=html,
    output_path=".linkedin_drafts/previews/my_post.html"
)
print(f"Saved to: {path}")
```

### `DocumentConverter`

Utility class for converting documents to images.

#### `convert_to_images(filepath, max_pages=None, dpi=150)`

Convert document to images.

**Parameters**:
- `filepath` (str): Path to document file
- `max_pages` (int, optional): Maximum pages to convert (None for all)
- `dpi` (int): DPI for image conversion (higher = better quality, larger files)

**Returns**: `List[str]` - List of paths to generated images

**Example**:
```python
images = DocumentConverter.convert_to_images(
    filepath="report.pdf",
    max_pages=10,
    dpi=150
)
print(f"Generated {len(images)} page images")
```

#### `get_page_count(filepath)`

Get number of pages in document.

**Parameters**:
- `filepath` (str): Path to document file

**Returns**: `int` - Number of pages

**Example**:
```python
pages = DocumentConverter.get_page_count("presentation.pptx")
print(f"Document has {pages} slides")
```

#### `clear_cache(cache_key=None)`

Clear document conversion cache.

**Parameters**:
- `cache_key` (str, optional): Specific document cache key to clear. If None, clears all cache.

**Example**:
```python
# Clear specific document
DocumentConverter.clear_cache("abc123")

# Clear all cached documents
DocumentConverter.clear_cache()
```

## Best Practices

### Performance

1. **Use caching**: Don't clear cache unless documents change
2. **Reasonable DPI**: Use 150 DPI for previews (default), 300 for final
3. **Limit pages**: Set `max_pages=20` to match LinkedIn's limit
4. **Batch generation**: Generate multiple previews in one session

### Preview Workflow

1. **Draft locally**: Write and edit post text
2. **Generate preview**: Create HTML preview
3. **Review in browser**: Check formatting, length, appearance
4. **Iterate**: Make edits and regenerate preview
5. **Publish**: When satisfied, publish to LinkedIn

### Document Attachments

1. **Optimize PDFs**: Keep under 100MB, under 20 pages
2. **Readable fonts**: Use minimum 18pt font size
3. **Square format**: 1920x1920 for best engagement
4. **Test rendering**: Preview before publishing
5. **Fallback text**: Include meaningful post text, don't rely solely on document

## Troubleshooting

### "pdf2image is required" Error

**Problem**: PDF conversion fails with import error.

**Solution**:
```bash
# Install preview dependencies
pip install chuk-mcp-linkedin[preview]

# Install poppler (system dependency)
# macOS
brew install poppler

# Ubuntu
sudo apt-get install poppler-utils
```

### Document Pages Not Rendering

**Problem**: Document preview shows placeholders instead of actual pages.

**Solutions**:
1. Check file path is correct and file exists
2. Ensure preview dependencies are installed
3. Verify poppler is installed (for PDFs)
4. Check error messages in console output

### "Module 'pdf2image' has no attribute '__version__'" Error

**Problem**: Import error even though pdf2image is installed.

**Solution**: This is normal - pdf2image doesn't have a `__version__` attribute. The module is working correctly.

### Cache Issues

**Problem**: Old document pages showing after updating document.

**Solution**:
```python
from chuk_mcp_linkedin.utils.document_converter import DocumentConverter

# Clear cache for specific document
cache_key = DocumentConverter._get_cache_key("your_document.pdf")
DocumentConverter.clear_cache(cache_key)

# Or clear all cache
DocumentConverter.clear_cache()
```

### Preview Not Opening in Browser

**Problem**: Preview file created but doesn't open automatically.

**Solution**:
```python
import webbrowser
from pathlib import Path

preview_path = Path(".linkedin_drafts/previews/my_post.html")
webbrowser.open(f"file://{preview_path.absolute()}")
```

## Examples

See the `examples/` directory for complete working examples:

- `examples/preview_example.py` - Basic text post preview
- `examples/demo_document_page_preview.py` - Document rendering with PDF and PowerPoint
- `examples/demo_document_attachment.py` - Document attachment workflow
- `examples/showcase_media_types.py` - Image and video post previews

## Related Documentation

- [Design Tokens](./TOKENS.md) - Token system for consistent styling
- [Themes](./THEMES.md) - Theme system for different LinkedIn personas
- [README](../README.md) - Main project documentation
