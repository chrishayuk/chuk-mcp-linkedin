# LinkedIn MCP Server Examples

Clean, focused examples demonstrating core functionality of the LinkedIn MCP Server.

## Available Examples

### 1. **Complete Component Showcase** ⭐

#### `showcase_all_components.py`
**THE MAIN SHOWCASE** - Interactive HTML previews of EVERY post component.

**Features:**
- **Post Structure:** Hook, Body, CTA, Hashtags, Separator
- **Charts:** Bar, Metrics, Comparison, Progress, Ranking (5 types)
- **Features:** Quote, BigStat, Timeline, KeyTakeaway, ProCon (5 types)
- **Combined Examples:** Multiple components in real-world posts
- Generates 13 HTML previews
- LinkedIn-style formatting
- Opens in browser

**Run:**
```bash
python examples/showcase_all_components.py
```

**Output:** Saves 13 HTML files to `~/.linkedin_drafts/previews/showcase/`

This is the best place to start to see everything the system can do!

---

### 2. **Charts & Data Visualization**

#### `demo_atomic_charts.py`
Terminal output demonstration of all chart components with Pydantic validation.

**Features:**
- Bar charts with colored emoji squares
- Metrics charts with ✅/❌ indicators
- Comparison charts (A vs B)
- Progress bars (0-100%)
- Ranking charts with medals
- Combined charts in one post
- Pydantic data validation examples

**Run:**
```bash
python examples/demo_atomic_charts.py
```

#### `demo_charts_preview.py`
Interactive HTML previews of all chart and feature components.

**Features:**
- All chart types with LinkedIn-style previews
- Feature components (Quote, BigStat, Timeline, KeyTakeaway, ProCon)
- Combined components example
- Opens previews in browser
- Interactive preview selection

**Run:**
```bash
python examples/demo_charts_preview.py
```

### 3. **Media Attachments**

#### `showcase_media_types.py`
Demonstrates different media types in LinkedIn posts.

**Features:**
- Single image posts
- Multiple images (2-4 grid layout)
- Video posts with thumbnails
- PDF document attachments
- PowerPoint presentations
- Interactive HTML previews

**Run:**
```bash
python examples/showcase_media_types.py
```

### 4. **Documents**

#### `demo_document_page_preview.py`
Shows document-to-image conversion for preview (like LinkedIn does).

**Features:**
- PDF pages rendered as images
- PowerPoint slides rendered as images
- Interactive carousel navigation
- Cached conversions for performance
- Requires: `pip install chuk-mcp-linkedin[preview]`

**Run:**
```bash
python examples/demo_document_page_preview.py
```

**Requirements:**
- Install preview dependencies: `pip install chuk-mcp-linkedin[preview]`
- Install poppler: `brew install poppler` (macOS) or `sudo apt-get install poppler-utils` (Ubuntu)

#### `demo_document_upload_and_attach.py`
Complete workflow for LinkedIn's Documents API.

**Features:**
- Document validation (size, format, pages)
- Upload documents to LinkedIn API
- Get document URNs
- Create posts with document attachments
- Integration with ComposablePost

**Run:**
```bash
python examples/demo_document_upload_and_attach.py
```

**Note:** Requires LinkedIn API credentials to actually upload. Example shows the structure.

## Quick Start

### Install Dependencies

**Core functionality:**
```bash
pip install chuk-mcp-linkedin
```

**With preview support:**
```bash
pip install "chuk-mcp-linkedin[preview]"
brew install poppler  # macOS only, for PDF support
```

### Run Any Example

```bash
# From the project root
python examples/demo_charts_preview.py

# Or from examples directory
cd examples
python demo_charts_preview.py
```

## Example Categories

### Complete Showcase ⭐
- `showcase_all_components.py` - **START HERE** - Every component with HTML preview

### Charts & Visualization
- `demo_atomic_charts.py` - Terminal output with validation
- `demo_charts_preview.py` - HTML previews in browser

### Media Types
- `showcase_media_types.py` - Images, videos, documents

### Documents
- `demo_document_page_preview.py` - Document rendering
- `demo_document_upload_and_attach.py` - LinkedIn API workflow

## Output Locations

Examples save previews to:
- **HTML previews:** `~/.linkedin_drafts/previews/`
- **Document cache:** `~/.linkedin_drafts/document_cache/`

## Common Patterns

### Create a Post with Charts

```python
from chuk_mcp_linkedin.posts import ComposablePost

post = ComposablePost("text")
post.add_hook("stat", "📊 Data-Driven Insights")
post.add_bar_chart(
    data={"Q1": 100, "Q2": 150, "Q3": 200},
    title="QUARTERLY GROWTH",
    unit="customers"
)
post.add_cta("curiosity", "What's your growth rate?")
post.add_hashtags(["Data", "Growth"])

text = post.compose()
```

### Generate HTML Preview

```python
from chuk_mcp_linkedin.preview import LinkedInPreview

draft_data = {
    "name": "My Post",
    "post_type": "text",
    "content": {"composed_text": text}
}

html = LinkedInPreview.generate_html(draft_data)
preview_path = LinkedInPreview.save_preview(html, "my_post.html")
```

### Upload Document to LinkedIn

```python
from chuk_mcp_linkedin.api import LinkedInDocumentsAPI, DocumentPostBuilder

# Upload document
api = LinkedInDocumentsAPI(access_token)
doc = api.upload_document(
    "report.pdf",
    owner_urn="urn:li:person:abc123",
    title="Q4 Report"
)

# Create post with document
post = DocumentPostBuilder.create_document_post(
    commentary="Check out our Q4 results!",
    document_urn=doc.urn,
    document_title="Q4 Performance Report"
)
```

## Testing Examples

All examples are self-contained and can be run independently. They use test files from:
```
/test_files/
  ├── test_image_1.png
  ├── test_document.pdf
  └── test_presentation.pptx
```

## Need Help?

- **Documentation:** `/docs/ARCHITECTURE.md`
- **API Reference:** `/docs/README.md`
- **Issues:** https://github.com/chrishayuk/chuk-mcp-linkedin/issues

## Example Output

All examples provide clear terminal output and/or open HTML previews in your browser:

- ✅ Chart examples show formatted text output
- 🌐 Preview examples open HTML in browser
- 📊 Document examples show conversion progress
- 🔗 API examples show workflow structure

Happy posting! 🚀
