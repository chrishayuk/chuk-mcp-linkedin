# src/chuk_mcp_linkedin/preview/__init__.py
"""
LinkedIn Post Preview System.

Generate HTML previews of LinkedIn posts with authentic LinkedIn styling.

## Features

- **Authentic LinkedIn UI**: Post card, avatar, header, action buttons
- **Analytics Dashboard**: Character count, hashtags, hooks, CTAs
- **"See More" Line**: Visual indicator at 210 characters
- **Media Support**: Images, videos, document attachments
- **Document Rendering**: Shows actual PDF/PowerPoint/Word pages as images
- **Mobile Responsive**: Preview how posts look on mobile

## Usage

```python
from chuk_mcp_linkedin.preview import LinkedInPreview

# Generate HTML preview
html = LinkedInPreview.generate_html(draft_data, stats=stats)

# Save to file (opens in browser)
preview_path = LinkedInPreview.save_preview(html, "my_post.html")
```

## Document Attachments

When previewing posts with documents attached:
1. PDF/PPTX/DOCX pages are converted to images
2. Displayed in LinkedIn-style carousel
3. Interactive navigation (prev/next, page indicators)
4. Cached for performance

Note: This is for PREVIEW only. To:
- Create actual PDFs/PowerPoint: Use `chuk-mcp-pptx` MCP server
- Upload documents to LinkedIn: Use `chuk_mcp_linkedin.documents` API
"""

from .artifact_preview import ArtifactPreviewManager, get_artifact_manager
from .post_preview import LinkedInPreview

__all__ = ["LinkedInPreview", "ArtifactPreviewManager", "get_artifact_manager"]
