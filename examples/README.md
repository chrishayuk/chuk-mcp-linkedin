# LinkedIn MCP Server Examples

Clean, focused examples demonstrating core functionality of the LinkedIn MCP Server.

## Important Note

**All examples use OAuth 2.1 for authentication.** The legacy examples that used `LINKEDIN_ACCESS_TOKEN` have been removed.

For OAuth setup, see:
- **[oauth_linkedin_example.py](#5-oauth--authentication)** - Complete OAuth flow demonstration
- **[docs/OAUTH.md](../docs/OAUTH.md)** - OAuth setup guide

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

### Publishing to LinkedIn

Publishing requires OAuth authentication. See the OAuth example:

```python
# See examples/oauth_linkedin_example.py for complete OAuth flow
# The MCP server handles OAuth automatically when configured properly
```

For production use, configure the MCP server with OAuth:
```bash
export LINKEDIN_CLIENT_ID=your_client_id
export LINKEDIN_CLIENT_SECRET=your_client_secret
export SESSION_PROVIDER=memory
uv run linkedin-mcp http --port 8000
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

---

## 5. **OAuth & Authentication**

### `oauth_linkedin_example.py`
Complete LinkedIn OAuth flow demonstration with chuk-sessions token storage.

**Features:**
- MCP client registration
- LinkedIn OAuth authorization flow
- Token exchange and validation
- Token refresh with rotation
- chuk-sessions storage (memory or Redis)
- Step-by-step flow visualization

**Run:**
```bash
# Set LinkedIn credentials
export LINKEDIN_CLIENT_ID=your_client_id
export LINKEDIN_CLIENT_SECRET=your_client_secret

# Run with memory backend (default)
python examples/oauth_linkedin_example.py

# Or with Redis backend
export SESSION_PROVIDER=redis
export SESSION_REDIS_URL=redis://localhost:6379/0
python examples/oauth_linkedin_example.py
```

**Output:**
```
================================================================================
LinkedIn OAuth Flow Example with chuk-sessions
================================================================================

📦 Token Storage Backend: MEMORY

Step 1: Registering MCP Client
--------------------------------------------------------------------------------
✅ Client registered successfully!
   Client ID: xoUmSxhdFGnoRVQ-mz4i8g
   Client Secret: 5c7UhwF0KG...

Step 2: Initiating LinkedIn Authorization
--------------------------------------------------------------------------------
🔗 LinkedIn authorization required
...

📊 Complete OAuth Flow:
   ────────────────────────────────────────────────────────────────────────────
   1. MCP Client → OAuth Server: Request authorization
   2. OAuth Server → LinkedIn: Redirect user for login
   3. User authorizes on LinkedIn
   4. LinkedIn → OAuth Server: Callback with code
   5. OAuth Server → LinkedIn: Exchange code for token
   6. OAuth Server: Store LinkedIn token in chuk-sessions
   7. OAuth Server → MCP Client: Return authorization code
   8. MCP Client → OAuth Server: Exchange code for MCP token
   9. MCP Client uses MCP token for API calls
   10. OAuth Server validates MCP token & uses LinkedIn token
   ────────────────────────────────────────────────────────────────────────────
```

**Prerequisites:**
1. Create LinkedIn app at https://www.linkedin.com/developers/apps
2. Add redirect URI: `http://localhost:8000/oauth/linkedin/callback`
3. Copy Client ID and Client Secret

**Token Storage:**

Tokens are automatically stored in chuk-sessions with TTL:
- Authorization codes: 10 minutes
- MCP access tokens: 1 hour
- MCP refresh tokens: 30 days
- LinkedIn tokens: 60 days

**Backend Options:**

| Backend | Use Case | Configuration |
|---------|----------|---------------|
| Memory (default) | Development, testing | No config needed |
| Redis | Production, multi-user | `SESSION_PROVIDER=redis` |

**Inspect Tokens (Redis):**
```bash
# Connect to Redis
redis-cli

# List all tokens
KEYS chuk-mcp-linkedin:*

# Get specific token
GET chuk-mcp-linkedin:access_token:abc123...

# Check time remaining
TTL chuk-mcp-linkedin:access_token:abc123...
```

**Full Production Setup:**

```bash
# Terminal 1: Start OAuth server
export LINKEDIN_CLIENT_ID=your_client_id
export LINKEDIN_CLIENT_SECRET=your_client_secret
export SESSION_PROVIDER=redis
export SESSION_REDIS_URL=redis://localhost:6379/0

uv run linkedin-mcp http --port 8000

# Terminal 2: Configure MCP client (Claude Desktop)
# Edit ~/Library/Application Support/Claude/claude_desktop_config.json:
{
  "mcpServers": {
    "linkedin": {
      "command": "linkedin-mcp",
      "args": ["http", "--port", "8000"],
      "authorization": {
        "type": "oauth2",
        "authorization_url": "http://localhost:8000/oauth/authorize",
        "token_url": "http://localhost:8000/oauth/token"
      }
    }
  }
}
```

**See Also:**
- `OAUTH_WITH_CHUK_SESSIONS.md` - Complete OAuth + chuk-sessions guide
- `OAUTH_IMPLEMENTATION_SUMMARY.md` - OAuth architecture details
