# Architecture Overview

Clean, focused architecture for the LinkedIn MCP Server.

## Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **No Duplication**: Document creation belongs in `chuk-mcp-pptx`, not here
3. **Clear Boundaries**: Preview vs Creation vs API Integration

## Module Structure

```
chuk-mcp-linkedin/
├── /preview/                    # HTML preview generation
│   ├── __init__.py             # Exports: LinkedInPreview
│   ├── post_preview.py         # Generate HTML previews of posts
│   └── component_renderer.py  # Simple HTML rendering
│
├── /api/                        # LinkedIn API integration
│   ├── __init__.py             # Exports: All API classes
│   ├── linkedin_client.py      # Main LinkedIn API client
│   ├── documents_api.py        # Upload documents to LinkedIn
│   ├── document_attachment.py  # Attach documents to posts
│   └── config.py               # API configuration
│
├── /posts/                      # Post text composition
│   ├── __init__.py
│   ├── composition.py          # ComposablePost
│   └── /components/            # Hook, Body, CTA, Hashtags
│
├── /themes/                     # Post themes and tone
└── /utils/                      # Shared utilities
    └── document_converter.py  # Convert docs to images for preview
```

## What Each Module Does

### `/preview/` - Post Preview Generation

**Purpose**: Generate HTML previews of LinkedIn posts for local viewing

**Key Features**:
- Authentic LinkedIn UI (post card, avatar, action buttons)
- Media rendering (images, videos, document files)
- Document-to-image conversion for preview
- Analytics dashboard (character count, hashtags, etc.)

**What it does NOT do**:
- Does NOT create documents (that's `chuk-mcp-pptx`)
- Does NOT compose post text (that's `/posts`)
- Does NOT upload to LinkedIn (that's `/documents` and `/api`)

**Example**:
```python
from chuk_mcp_linkedin.preview import LinkedInPreview

# Generate HTML preview
html = LinkedInPreview.generate_html(draft_data, stats=stats)

# Save and open in browser
preview_path = LinkedInPreview.save_preview(html, "my_post.html")
```

### `/api/` - LinkedIn API Integration

**Purpose**: All LinkedIn API communication (posts, documents, configuration)

**Key Features**:
- Main LinkedIn API client for posting
- Upload PDF/PPTX/DOCX to LinkedIn
- Get document URNs from LinkedIn API
- Attach documents to posts using URNs
- Validate documents (size, format, page count)
- API configuration and authentication

**What it does NOT do**:
- Does NOT create documents (use `chuk-mcp-pptx` MCP server)
- Does NOT preview posts (use `/preview`)

**Example**:
```python
from chuk_mcp_linkedin.api import (
    LinkedInClient,
    LinkedInDocumentsAPI,
    DocumentPostBuilder
)

# Upload document to LinkedIn
api = LinkedInDocumentsAPI(access_token)
doc = api.upload_document(
    "Q4_Report.pdf",
    owner_urn="urn:li:person:abc123",
    title="Q4 2024 Strategy Report"
)

# Create post with document attached
post = DocumentPostBuilder.create_document_post(
    commentary="Check out our Q4 results! 📊",
    document_urn=doc.urn,
    document_title="Q4 Performance Report"
)

# Post to LinkedIn
client = LinkedInClient(access_token)
response = client.create_post(post)
```

### `/posts/` - Post Text Composition

**Purpose**: Compose LinkedIn post text with themes and components

**Key Features**:
- Theme-based composition (thought leader, storyteller, educator)
- Components: Hook, Body, CTA, Hashtags
- Automatic formatting and structure

**Example**:
```python
from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.themes import ThemeManager

theme = ThemeManager().get_theme("thought_leader")
post = ComposablePost("text", theme=theme)

post.add_hook("stat", "95% of LinkedIn posts fail to engage")
post.add_body("Here's why...")
post.add_cta("curiosity", "What's your biggest content challenge?")
post.add_hashtags(["ContentStrategy", "LinkedIn"])

text = post.compose()
```

### `/components/` - HTML Rendering Helpers

**Purpose**: Simple HTML rendering for visual elements

**Key Features**:
- Badges, callouts, progress bars
- Charts and data visualizations
- Reusable across preview and composition

**Not for**: Complex document layouts (removed - use `chuk-mcp-pptx`)

## Workflow Examples

### 1. Create Post with Document Attachment

```python
# Step 1: Create post text (using /posts)
from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.themes import ThemeManager

theme = ThemeManager().get_theme("educator")
post = ComposablePost("document", theme=theme)
post.add_hook("stat", "Document posts get 45.85% engagement")
post.add_body("Here's our Q4 strategy...")
post.add_cta("curiosity", "What resonates with your strategy?")
text = post.compose()

# Step 2: Upload document to LinkedIn (using /documents)
from chuk_mcp_linkedin.documents import LinkedInDocumentsAPI

api = LinkedInDocumentsAPI(access_token)
doc = api.upload_document(
    "Q4_Strategy.pdf",
    owner_urn="urn:li:person:abc123",
    title="Q4 2024 Strategy"
)

# Step 3: Create post data
from chuk_mcp_linkedin.documents import attach_document_to_post

post_dict = {
    "content": {"commentary": text},
    "visibility": "PUBLIC"
}
post_dict = attach_document_to_post(
    post_dict,
    document_urn=doc.urn,
    title="Q4 2024 Strategy"
)

# Step 4: Preview locally (using /preview)
from chuk_mcp_linkedin.preview import LinkedInPreview

draft_data = {
    "name": "Q4 Strategy Post",
    "post_type": "document",
    "content": {
        "composed_text": text,
        "document_file": {
            "filename": "Q4_Strategy.pdf",
            "filepath": "/path/to/Q4_Strategy.pdf",
            "file_type": "pdf",
            "pages": 10
        }
    }
}

html = LinkedInPreview.generate_html(draft_data)
preview_path = LinkedInPreview.save_preview(html, "preview.html")

# Step 5: Post to LinkedIn (using /api)
from chuk_mcp_linkedin.api import LinkedInClient

client = LinkedInClient(access_token)
response = client.create_post(post_dict)
```

### 2. Preview Post with Images

```python
# Create post
from chuk_mcp_linkedin.posts import ComposablePost

post = ComposablePost("image")
post.add_hook("story", "This changed everything...")
post.add_body("When we implemented this strategy...")
text = post.compose()

# Generate preview
from chuk_mcp_linkedin.preview import LinkedInPreview

draft_data = {
    "name": "Image Post",
    "post_type": "image",
    "content": {
        "composed_text": text,
        "images": [
            {
                "filepath": "/path/to/image1.jpg",
                "alt_text": "Before and after"
            },
            {
                "filepath": "/path/to/image2.jpg",
                "alt_text": "Results"
            }
        ]
    }
}

html = LinkedInPreview.generate_html(draft_data)
LinkedInPreview.save_preview(html, "image_preview.html")
```

## What Was Removed & Reorganized

### Document Creation System (Deleted)

The following were removed because **document creation belongs in `chuk-mcp-pptx`**:

- `/preview/document_preview.py` - ComposableDocument class (787 lines)
- `/preview/components/` - Document creation components
- `/preview/layouts/` - Document layout system
- Document creation methods in `post_preview.py`

**Why**: This MCP server is for LinkedIn posting, not document creation. Use the dedicated `chuk-mcp-pptx` MCP server to create PowerPoint/PDF files.

### API Consolidation (Reorganized)

All LinkedIn API functionality consolidated into `/api/`:

- Documents API: `/api/documents_api.py` - Upload documents to LinkedIn
- Document Attachment: `/api/document_attachment.py` - Attach documents to posts
- LinkedIn Client: `/api/linkedin_client.py` - Main API client
- Configuration: `/api/config.py` - API configuration

**Why**: All LinkedIn API integration should be in one place (`/api/`) for better organization and discoverability.

**Import from api module**:
```python
from chuk_mcp_linkedin.api import (
    LinkedInClient,
    LinkedInDocumentsAPI,
    DocumentPostBuilder
)
```

### Decision Rationale

**Before**: Mixed responsibilities
```
documents/
  ├── composition.py      # CREATE documents (slides, layouts)
  ├── api.py              # UPLOAD documents to LinkedIn
  └── attachment.py       # ATTACH documents to posts
```

**After**: Clear separation
```
documents/
  ├── api.py              # UPLOAD existing documents
  └── attachment.py       # ATTACH uploaded documents

# Document CREATION moved to:
chuk-mcp-pptx/           # Separate MCP server
```

**Benefits**:
1. Single Responsibility: Each server does one thing well
2. No Duplication: One PowerPoint/PDF creation system
3. Clearer API: Upload vs Create are separate operations
4. Better Testing: Focused test coverage

## Integration Points

### With `chuk-mcp-pptx` MCP Server

```python
# 1. Create PowerPoint using chuk-mcp-pptx
from chuk_mcp_pptx import create_presentation

pptx_path = create_presentation({
    "title": "Q4 Strategy",
    "slides": [
        {"layout": "title", "content": {"title": "Q4 2024"}},
        {"layout": "content", "content": {"title": "Goals", "body": "..."}}
    ]
})

# 2. Upload to LinkedIn using chuk-mcp-linkedin
from chuk_mcp_linkedin.api import LinkedInDocumentsAPI

api = LinkedInDocumentsAPI(access_token)
doc = api.upload_document(pptx_path, owner_urn, "Q4 Strategy")

# 3. Attach to post
from chuk_mcp_linkedin.api import DocumentPostBuilder

post = DocumentPostBuilder.create_document_post(
    commentary="Our Q4 strategy is here!",
    document_urn=doc.urn,
    document_title="Q4 2024 Strategy"
)

# 4. Preview locally
from chuk_mcp_linkedin.preview import LinkedInPreview

draft_data = {
    "content": {
        "composed_text": post["content"]["commentary"],
        "document_file": {
            "filename": "Q4_Strategy.pptx",
            "filepath": pptx_path,
            "pages": 10
        }
    }
}
html = LinkedInPreview.generate_html(draft_data)
```

### With LinkedIn API

```python
# Full workflow: Compose → Upload → Preview → Post
from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.api import (
    LinkedInClient,
    LinkedInDocumentsAPI,
    attach_document_to_post
)
from chuk_mcp_linkedin.preview import LinkedInPreview

# 1. Compose text
post = ComposablePost("document")
# ... add components ...
text = post.compose()

# 2. Upload document
api = LinkedInDocumentsAPI(access_token)
doc = api.upload_document(filepath, owner_urn, title)

# 3. Create post data
post_dict = {"content": {"commentary": text}}
post_dict = attach_document_to_post(post_dict, doc.urn, title)

# 4. Preview
html = LinkedInPreview.generate_html({"content": {"composed_text": text}})

# 5. Post to LinkedIn
client = LinkedInClient(access_token)
response = client.create_post(post_dict)
```

## Dependencies

### Preview Dependencies (Optional)

Install with: `pip install "chuk-mcp-linkedin[preview]"`

Required for document-to-image conversion in previews:
- `pdf2image` - Convert PDF pages to images
- `Pillow` - Image manipulation
- `python-pptx` - Read PowerPoint files
- `python-docx` - Read Word documents
- `PyPDF2` - PDF page counting

**Note**: Also requires `poppler` system library (`brew install poppler`)

### Core Dependencies

- `httpx` - HTTP client for LinkedIn API
- `pydantic` - Data validation
- Standard library only for other features

## Testing Strategy

### Unit Tests

Each module has focused unit tests:
- `/preview/`: Test HTML generation, document conversion
- `/documents/`: Test API integration, validation
- `/posts/`: Test composition, themes

### Integration Tests

Test workflows across modules:
- Upload document → Attach to post → Preview
- Compose post → Generate preview → Post to LinkedIn

### Example Test Structure

```python
# tests/test_preview.py
def test_preview_with_document_images():
    """Test preview converts document pages to images"""
    draft_data = {
        "content": {
            "document_file": {
                "filepath": "test.pdf",
                "pages": 3
            }
        }
    }
    html = LinkedInPreview.generate_html(draft_data)
    assert "document-page-image" in html

# tests/test_documents.py
def test_upload_and_attach():
    """Test document upload and attachment"""
    api = LinkedInDocumentsAPI(token)
    doc = api.upload_document("test.pdf", owner_urn, "Test")

    post_dict = {"content": {"commentary": "Test"}}
    post_dict = attach_document_to_post(post_dict, doc.urn, "Test")

    assert post_dict["content"]["document"]["id"] == doc.urn
```

## Migration Guide

If you were using the old document creation system:

### Before (Old Way)
```python
from chuk_mcp_linkedin.documents import ComposableDocument

# This no longer exists!
doc = ComposableDocument()
doc.add_slide("title", {"title": "Q4"})
doc.render_to_file("output.html")
```

### After (New Way)
```python
# Use chuk-mcp-pptx to CREATE documents
from chuk_mcp_pptx import create_presentation

pptx_path = create_presentation({
    "slides": [{"layout": "title", "content": {"title": "Q4"}}]
})

# Use chuk-mcp-linkedin to UPLOAD to LinkedIn
from chuk_mcp_linkedin.documents import LinkedInDocumentsAPI

api = LinkedInDocumentsAPI(token)
doc = api.upload_document(pptx_path, owner_urn, "Q4")

# Use chuk-mcp-linkedin to PREVIEW locally
from chuk_mcp_linkedin.preview import LinkedInPreview

draft_data = {
    "content": {
        "document_file": {
            "filepath": pptx_path,
            "filename": "Q4.pptx",
            "pages": 5
        }
    }
}
html = LinkedInPreview.generate_html(draft_data)
```

## Summary

**chuk-mcp-linkedin** is now focused on:
1. **Composing** LinkedIn post text
2. **Uploading** existing documents to LinkedIn
3. **Attaching** documents to posts
4. **Previewing** posts locally as HTML
5. **Posting** to LinkedIn API

**It does NOT**:
- Create PowerPoint/PDF files (use `chuk-mcp-pptx`)
- Provide complex document layouts (use `chuk-mcp-pptx`)
- Handle document rendering beyond preview images

This clean separation makes each MCP server better at its core responsibility.
