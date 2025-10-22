# chuk-mcp-linkedin

MCP server for LinkedIn content creation and posting with theme-based composition, document API integration, and local HTML previews.

## Overview

`chuk-mcp-linkedin` streamlines LinkedIn posting workflows: compose posts with themes and components, upload existing documents via LinkedIn's API, preview posts locally in authentic LinkedIn UI, and publish to LinkedIn.

**What it does:**
- ✅ Compose post text with themes and components
- ✅ Upload existing PDF/PPTX/DOCX to LinkedIn via Documents API
- ✅ Preview posts locally with authentic LinkedIn UI
- ✅ Post to LinkedIn API

**What it doesn't do:**
- ❌ Create PowerPoint/PDF files (use [`chuk-mcp-pptx`](https://github.com/chrishayuk/chuk-mcp-pptx) for that)

## Features

- **Local Preview System**: Generate pixel-perfect HTML previews of posts before publishing
  - LinkedIn-style UI rendering
  - Real-time analytics and optimization tips
  - "See more" line visualization at 210 characters
  - Browser-based preview with CLI utility
- **Component-Based Architecture**: 13+ specialized post types (text, document, poll, video, carousel, etc.)
- **Variant System**: CVA-inspired variants with compound variant support
- **Theme System**: 10 pre-built themes (thought leader, storyteller, community builder, etc.)
- **Composition Patterns**: Build complex posts from subcomponents (hooks, body, CTA, hashtags)
- **Design Tokens**: Research-backed tokens for engagement, formatting, and timing
- **2025 Performance Data**: Built-in optimization based on 1M+ post analysis
- **MCP Integration**: Full Model Context Protocol support for LLM workflows

## 2025 LinkedIn Performance Insights

Based on analysis of 1M+ posts across 9K company pages:

### Top Performing Formats
1. **Document Posts (PDF)** - 45.85% engagement rate (HIGHEST)
2. **Poll Posts** - 200%+ higher reach (MOST UNDERUSED)
3. **Video Posts** - 1.4x engagement (rising fast)
4. **Image Posts** - 2x more comments than text
5. **Carousel Posts** - Declining (keep to 5-10 slides)

### Key Insights
- Polls achieve highest reach but are least used (opportunity!)
- Document posts dominate engagement (carousel's successor)
- Video usage up 69%, vertical format preferred
- First 210 characters critical (before "see more")
- First hour engagement determines algorithmic reach

## Installation

### Basic Installation

```bash
pip install chuk-mcp-linkedin
```

### With Document Preview Support

For rendering actual document pages (PDF, PowerPoint, Word) in previews:

```bash
# Install with preview dependencies
pip install chuk-mcp-linkedin[preview]

# System requirements for PDF support (poppler)
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Windows
# Download poppler from: https://github.com/oschwartz10612/poppler-windows/releases
```

The preview dependencies include:
- `pdf2image` - PDF to image conversion
- `Pillow` - Image processing
- `python-pptx` - PowerPoint support
- `python-docx` - Word document support
- `PyPDF2` - PDF utilities

## Quick Start

### Preview Your First Post (60 seconds)

```bash
# 1. Try the preview example
python examples/preview_example.py

# 2. Browser opens automatically showing your LinkedIn post preview
#    with analytics and optimization tips

# 3. Edit and preview your own drafts
python preview_post.py --list    # See all drafts
python preview_post.py           # Preview current draft
```

### Simple Text Post

```python
from chuk_mcp_linkedin import LinkedInManager, ThemeManager

# Initialize
manager = LinkedInManager()
theme_mgr = ThemeManager()

# Create thought leadership post
theme = theme_mgr.get_theme("thought_leader")

post = manager.create_text_post(
    commentary="""80% of B2B decision makers prefer thought leadership content over ads.

Yet most companies just promote.

Here's what actually works:

→ Lead with insights, not products
→ Share frameworks, not features
→ Tell stories, not sales pitches
→ Build trust, not transactions

The algorithm rewards value.""",
    variant="insight",
    tone="professional",
    theme=theme
)

post.publish(visibility="PUBLIC")
```

### Document Post (Highest Engagement)

Document posts have the highest engagement rate (45.85%)! Upload an existing PDF/PPTX/DOCX:

```python
from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.documents import LinkedInDocumentsAPI, DocumentPostBuilder
from chuk_mcp_linkedin.themes import ThemeManager

# 1. Compose post text
theme = theme_mgr.get_theme("data_driven")
post = ComposablePost("document", theme=theme)
post.add_hook("stat", "Document posts get 45.85% engagement")
post.add_body("Our Q4 results are in. Here's what we learned 📊")
post.add_cta("curiosity", "What's your biggest takeaway?")
text = post.compose()

# 2. Upload existing document to LinkedIn
# Note: Create the PDF/PPTX using chuk-mcp-pptx first
api = LinkedInDocumentsAPI(access_token)
doc = api.upload_document(
    "Q4_Report.pdf",  # Your existing PDF
    owner_urn="urn:li:person:abc123",
    title="Q4 2024 Results"
)

# 3. Create post with document attached
post_data = DocumentPostBuilder.create_document_post(
    commentary=text,
    document_urn=doc.urn,
    document_title="Q4 2024 Results"
)

# 4. Publish
from chuk_mcp_linkedin.api import LinkedInClient
client = LinkedInClient(access_token)
client.create_post(post_data)
```

**Creating PDF/PowerPoint**: Use [`chuk-mcp-pptx`](https://github.com/chrishayuk/chuk-mcp-pptx) to create the actual PDF/PowerPoint files first, then upload them with this MCP.

### Poll Post (Highest Reach)

```python
# Create poll (200%+ higher reach!)
poll = manager.create_poll_post(
    commentary="Quick question for my network:\n\nWhat's your biggest LinkedIn challenge in 2025?",
    question="Pick your top challenge:",
    options=[
        "Creating consistent content",
        "Growing engagement",
        "Converting leads",
        "Building community"
    ],
    duration_days=3,
    purpose="research",
    theme=theme_mgr.get_theme("community_builder")
)

poll.publish()
```

### Composition Pattern (Advanced)

```python
from chuk_mcp_linkedin import ComposablePost

# Build post using composition
post = (ComposablePost("text", theme=theme)
    .add_hook("stat", "95% of LinkedIn posts get zero comments")
    .add_body("""
Here's why (and how to fix it):

Most posts lack these 3 elements:

→ Strong hook (first 210 characters)
→ Clear value (what's in it for them)
→ Conversation starter (invite engagement)

Start treating posts like conversations, not broadcasts.
""", structure="listicle")
    .add_cta("curiosity", "What's your biggest LinkedIn frustration?")
    .add_hashtags(["LinkedInTips", "ContentStrategy"])
    .optimize_for_engagement()
    .compose())

manager.publish_text(post)
```

## Local Preview System

Preview your LinkedIn posts locally in a pixel-perfect browser preview before publishing. See exactly how your post will appear on LinkedIn with real-time analytics and optimization recommendations.

### Features

**Visual Preview**:
- Authentic LinkedIn post card styling (avatar, header, actions)
- Proper text formatting and line breaks
- Hashtag highlighting
- "See more" line indicator at 210 characters
- **Document page rendering** - Actual PDF/PowerPoint/Word pages as images
- Interactive carousel navigation for multi-page documents

**Analytics Dashboard**:
- Character and word counts
- Characters remaining (3000 max)
- Optimal length indicators (warnings for too short/long)
- Hashtag count analysis (optimal: 3-5)
- Hook and CTA status indicators
- Engagement optimization tips

**Document Preview** (with `[preview]` dependencies):
- Converts PDF pages to images (exactly like LinkedIn does)
- Renders PowerPoint slides as carousel
- Displays Word document pages
- Smart caching - converts once, reuses on subsequent previews
- LinkedIn-style carousel with navigation controls
- Page counter and indicators

### Python API

```python
from chuk_mcp_linkedin import LinkedInManager

manager = LinkedInManager()

# Create and compose your post
draft = manager.create_draft("My Post", "text")
# ... add content ...

# Generate HTML preview - opens automatically in browser
preview_path = manager.generate_html_preview(draft.draft_id)
```

#### Preview with Document Attachments

```python
from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.preview import LinkedInPreview
from chuk_mcp_linkedin.themes import ThemeManager

# Create post with document
theme_mgr = ThemeManager()
theme = theme_mgr.get_theme("thought_leader")

post = ComposablePost("document", theme=theme)
post.add_hook("question", "How do you share detailed insights?")
post.add_body("PDFs are perfect for sharing research and frameworks.")
post.add_cta("curiosity", "What's your preferred format?")
post.add_hashtags(["ContentStrategy", "ThoughtLeadership"])

# Compose text
text = post.compose()

# Create draft with document attachment
draft_data = {
    "name": "Q4 Strategy Report",
    "post_type": "document",
    "content": {
        "composed_text": text,
        "document_file": {
            "filename": "strategy.pdf",
            "filepath": "/path/to/strategy.pdf",
            "title": "Q4 Strategy Framework",
            "pages": 12,
            "file_type": "pdf"
        }
    },
    "theme": theme.name
}

# Generate preview with actual rendered pages
html_preview = LinkedInPreview.generate_html(draft_data)
preview_path = LinkedInPreview.save_preview(html_preview, ".linkedin_drafts/previews/my_post.html")

# Preview opens with:
# - Your post text
# - Interactive carousel showing each PDF page as an image
# - Navigation controls (prev/next, page indicators)
# - Just like LinkedIn's actual document post preview!
```

**Note**: The preview system converts PDF/PPTX/DOCX pages to images (just like LinkedIn does). Create the actual documents using [`chuk-mcp-pptx`](https://github.com/chrishayuk/chuk-mcp-pptx), then preview them here.

### Quick Preview CLI

The fastest way to preview posts:

```bash
# Preview current draft (auto-opens in browser)
python preview_post.py

# Preview specific draft
python preview_post.py draft_id_here

# List all available drafts
python preview_post.py --list
```

### MCP Tool

```python
# Via MCP server
linkedin_preview_html(open_browser=True)
```

**Preview Output**: All previews are saved to `.linkedin_drafts/previews/` as standalone HTML files you can share or archive.

**Live Editing Workflow**: Keep the preview open in your browser and run the preview command again after edits to see changes instantly.

## Component System

### Post Types

- `TextPost` - Simple text updates with variants (story, insight, question, listicle, hot_take)
- `DocumentPost` - PDF carousels (highest engagement format in 2025)
- `PollPost` - Polls for engagement (highest reach - 200%+ above average)
- `VideoPost` - Video content (1.4x engagement)
- `CarouselPost` - Multi-image storytelling (keep under 10 slides)
- `ImagePost` - Single image posts
- `StoryPost` - Personal narratives with emotional arc
- `ArticlePost` - Link sharing with commentary
- Plus: `BehindTheScenesPost`, `HumorPost`, `AnnouncementPost`, `EventPost`, `ThoughtLeadershipPost`

### Subcomponents

- `Hook` - Opening hooks (question, stat, story, controversy, list, curiosity)
- `Body` - Main content with structures (linear, listicle, framework, story_arc, comparison)
- `CallToAction` - Engagement drivers (direct, curiosity, action, share, soft)
- `Hashtags` - Hashtag strategies (minimal, optimal, branded, trending)

### Themes

10 pre-built themes for different LinkedIn personas:

- `thought_leader` - Establish expertise and authority
- `personal_brand` - Build authentic personal connection
- `technical_expert` - Deep technical knowledge
- `community_builder` - Foster conversation and connection
- `corporate_professional` - Polished corporate communication
- `contrarian_voice` - Challenge status quo, spark debate
- `storyteller` - Narrative-driven emotional connection
- `data_driven` - Let numbers tell the story
- `coach_mentor` - Guide and support your audience
- `entertainer` - Make LinkedIn fun and memorable

## MCP Server Tools

### Draft Management
- `linkedin_create` - Create new draft
- `linkedin_list` - List all drafts
- `linkedin_switch` - Switch between drafts
- `linkedin_delete` - Delete draft
- `linkedin_get_info` - Get draft details

### Content Creation
- `linkedin_text_post` - Create text post
- `linkedin_document_post` - Create document post
- `linkedin_poll_post` - Create poll post
- `linkedin_video_post` - Create video post
- `linkedin_carousel_post` - Create carousel post

### Composition
- `linkedin_add_hook` - Add opening hook
- `linkedin_add_body` - Add main content
- `linkedin_add_cta` - Add call-to-action
- `linkedin_add_hashtags` - Add hashtags

### Enhancement
- `linkedin_optimize_length` - Optimize text length
- `linkedin_suggest_emojis` - Suggest emoji placement
- `linkedin_format_for_scannability` - Add formatting for readability
- `linkedin_apply_theme` - Apply theme to draft

### Publishing
- `linkedin_publish` - Publish to LinkedIn
- `linkedin_schedule` - Schedule for later
- `linkedin_preview` - Get text preview (first 210 chars)
- `linkedin_preview_html` - Generate HTML preview and open in browser
- `linkedin_export_draft` - Export as JSON

### Analytics
- `linkedin_get_post_stats` - Get post analytics
- `linkedin_get_suggestions` - Get content suggestions
- `linkedin_analyze_draft` - Analyze draft performance potential

## Design Token System

A centralized design system that manages all visual and content decisions, similar to the PPTX MCP approach.

### Why Token-Based Design?

Instead of hardcoding values:
```python
❌ font_size = 24
❌ color = '#000000'
❌ margin = 60
```

Use design tokens:
```python
✓ font_size = DesignTokens.get_font_size('body')
✓ color = DesignTokens.get_color('minimal', 'primary')
✓ margin = DesignTokens.get_spacing('gaps', 'large')
```

**Benefits:**
- **Consistency**: All designs use same values
- **Maintainability**: Change once, update everywhere
- **Performance**: Values based on 1M+ posts analyzed
- **Mobile-First**: All tokens optimized for mobile
- **Platform-Aware**: LinkedIn-specific optimizations built-in

### Token Categories

#### 1. **Design Tokens** (`DesignTokens`)
Visual design system for layouts, documents, and carousels:

**Canvas Sizes:**
- Document posts: 1920x1920 (square, highest engagement format)
- Carousels: 1080x1080 (square) or 1080x1350 (portrait)

**Typography:**
- Font sizes: tiny (14pt) → massive (200pt)
- Font weights: light → black
- Line heights: tight (1.2) → loose (2.0)
- Minimum 18pt for LinkedIn mobile readability

**Colors:**
- 5 color schemes: minimal, modern, vibrant, dark, linkedin
- Semantic colors: success, error, warning, info
- LinkedIn brand blue: #0A66C2

**Spacing:**
- Safe areas: minimal → spacious
- Gaps: tiny (8px) → huge (120px)
- Padding: tight (20px) → spacious (80px)

#### 2. **Text Tokens** (`TextTokens`)
Content formatting and structure:
- Character limits (3000 max, 210 before "see more")
- Ideal lengths (micro: 50-150, short: 150-300, medium: 300-800, long: 800-1500, story: 1000-3000)
- Line break styles (dense, readable, scannable, dramatic, extreme)
- Emoji levels: none → heavy (0-15% of text)
- Hashtag strategy: optimal count 3-5

#### 3. **Engagement Tokens** (`EngagementTokens`)
Algorithm optimization patterns:
- Hook types with power ratings (controversy: 0.95, stat: 0.9, story: 0.85)
- CTA styles (direct, curiosity, action, share, soft)
- First hour targets (minimum: 10, good: 50, viral: 100 engagements)
- Timing optimization (Tuesday-Thursday, 7-9 AM / 12-2 PM / 5-6 PM)

#### 4. **Structure Tokens** (`StructureTokens`)
Content structure patterns:
- Formats: linear, listicle, framework, story_arc, comparison
- Visual formatting: symbols (→, •, ✓), separators
- Hook patterns and templates

### LinkedIn-Specific Optimizations (2025 Data)

Based on 1M+ posts analyzed:

**Document Posts (PDF):**
- Engagement rate: 45.85% (HIGHEST)
- Optimal slides: 5-10
- Format: 1920x1920 square
- Font min: 18pt

**Poll Posts:**
- Reach multiplier: 3.0x (200%+ higher!)
- Most underused format (opportunity!)

**Carousels:**
- Declining (-18% reach, -25% engagement vs 2024)
- Keep to 5-10 slides maximum

### Example: Token Usage

```python
from chuk_mcp_linkedin.tokens import DesignTokens, TextTokens, EngagementTokens

# Get canvas size for document
canvas = DesignTokens.get_canvas_size("document_square")  # (1920, 1920)

# Get optimal font size
title_size = DesignTokens.get_font_size("title")  # 56pt

# Check if mobile-friendly
min_font = DesignTokens.LINKEDIN_SPECIFIC["mobile"]["min_font_size"]  # 18pt

# Get optimal post length
ideal_length = TextTokens.IDEAL_LENGTH["medium"]  # (300, 800)

# Get hook power rating
stat_power = EngagementTokens.HOOKS["stat"]["power"]  # 0.9

# Get best posting time
best_days = EngagementTokens.TIMING["best_days"]  # ['tuesday', 'wednesday', 'thursday']
```

### Try the Showcase

Run the complete token and layout showcase:
```bash
python examples/layout_token_showcase.py
```

This demonstrates:
- All token categories with examples
- How layouts reference tokens
- 2025 LinkedIn-specific optimizations
- Mobile-first design principles

## Component Architecture

### Visual Component Library

The design system includes a comprehensive library of reusable visual components for creating LinkedIn documents and carousels.

#### ✅ **Fully Implemented Components**

**Visual Elements** (38 total variants across 5 categories):

1. **Dividers** (6 variants)
   - `horizontal_line()` - Simple line separators
   - `gradient_fade()` - Subtle gradient dividers
   - `decorative_accent()` - LinkedIn-style accent lines
   - `section_break()` - Visual section separators (•••)
   - `spacer()` - Invisible spacing elements
   - `title_underline()` - Title underlines (single/double/thick)

2. **Badges** (7 variants)
   - `pill_badge()` - Rounded pill-shaped badges
   - `status_badge()` - Semantic status indicators (NEW, TRENDING, etc.)
   - `number_badge()` - Notification-style number badges
   - `percentage_change()` - Change indicators with ↑↓ arrows
   - `category_tag()` - Topic/category tags
   - `icon_badge()` - Icon+text badges
   - `corner_ribbon()` - Diagonal corner ribbons

3. **Backgrounds** (8 variants)
   - `solid()` - Solid color backgrounds
   - `gradient()` - Linear gradients (vertical/horizontal/diagonal)
   - `subtle_pattern()` - Subtle texture patterns
   - `card()` - Card containers with shadows
   - `highlight_box()` - Highlighted content boxes
   - `branded_header()` - Branded header sections
   - `split_background()` - Split backgrounds for comparisons
   - `image_overlay()` - Semi-transparent overlays for images

4. **Borders** (8 variants)
   - `simple()` - Basic borders
   - `accent()` - Accent borders (left/right/top/bottom)
   - `double()` - Double-line borders
   - `gradient()` - Gradient borders
   - `corner_brackets()` - Corner bracket decoration
   - `callout()` - Callout boxes (success/warning/error/info)
   - `shadow_frame()` - Elevated frames with shadows
   - `inset_panel()` - Inset panels

5. **Shapes** (9 variants)
   - `circle()` - Circles (filled/outline)
   - `rectangle()` - Rectangles and squares
   - `icon_container()` - Icon container boxes
   - `arrow()` - Directional arrows
   - `checkmark()` - Checkmarks and crosses
   - `bullet_point()` - Custom bullet points
   - `decorative_element()` - Decorative shapes
   - `progress_ring()` - Progress indicators
   - `divider_ornament()` - Decorative divider elements

**Document Layouts** (11 types):
- Title Slide, Content Slide, Split Content, Big Number
- Quote Slide, Comparison, Two Column, Checklist
- Timeline, Icon Grid, Data Visual

All components use the design token system for consistent styling and are mobile-optimized.

#### Usage Example

```python
from chuk_mcp_linkedin.components import Dividers, Badges, Backgrounds, Borders, Shapes

# Create visual elements
accent = Dividers.decorative_accent()
new_badge = Badges.pill_badge("NEW", size="medium")
card_bg = Backgrounds.card()
highlight = Borders.callout(type="success")
icon = Shapes.icon_container("🚀", size="large")

# Use in document layouts
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.content_slide()
# Add components to layout zones
```

#### ⚠️ **Placeholder Components** (Not Yet Implemented)

The following component categories are defined in `__init__.py` files but implementation files don't exist yet:

**Typography Components** (5 needed):
- `Headers` - H1, H2, H3 with token-based sizing
- `BodyText` - Paragraph text with line height/spacing
- `Captions` - Small descriptive text
- `Quotes` - Pull quotes and blockquotes
- `Lists` - Bulleted and numbered lists

**Data Visualization** (5 needed):
- `Charts` - Bar, line, pie, donut charts
- `Metrics` - KPI metric cards with icons
- `Progress` - Progress bars and rings
- `Tables` - Data tables with styling
- `Infographics` - Visual data representations

**Content Blocks** (6 needed):
- `CTA` - Call-to-action blocks
- `Testimonials` - Customer testimonial cards
- `FeatureCards` - Product/service feature cards
- `TimelineItems` - Timeline event blocks
- `ChecklistItems` - Checklist/task items
- `StatCards` - Statistic display cards

**Media Components** (4 needed):
- `Images` - Image handling with crops/filters
- `Avatars` - Profile avatars and logos
- `VideoFrames` - Video thumbnails and frames
- `IconSets` - Icon libraries and sets

**Interactive Components** (3 needed):
- `Buttons` - CTA buttons with hover states
- `PollOptions` - Poll option styling
- `FormElements` - Input elements for forms

**Additional Needed**:
- `CarouselLayouts` - Layouts for carousel posts (mentioned but not implemented)
- `LayoutRenderer` - Render layouts to actual visual output (mentioned but not implemented)

### Component Development Status

| Category | Status | Count | Progress |
|----------|--------|-------|----------|
| Tokens | ✅ Complete | 4 | 100% |
| Document Layouts | ✅ Complete | 11 | 100% |
| Visual Elements | ✅ Complete | 38 variants | 100% |
| Preview System | ✅ Complete | 1 | 100% |
| Typography | ⚠️ Placeholder | 0/5 | 0% |
| Data Viz | ⚠️ Placeholder | 0/5 | 0% |
| Content Blocks | ⚠️ Placeholder | 0/6 | 0% |
| Media | ⚠️ Placeholder | 0/4 | 0% |
| Interactive | ⚠️ Placeholder | 0/3 | 0% |
| Carousel Layouts | ⚠️ Placeholder | 0 | 0% |
| Layout Renderer | ⚠️ Placeholder | 0 | 0% |

**Overall Progress**: 58 implemented / 85 total components (68% complete)

## Architecture

Clean, focused architecture with clear separation of concerns:

```
src/chuk_mcp_linkedin/
├── /preview/                      # Post preview generation
│   ├── __init__.py               # Exports: LinkedInPreview
│   ├── post_preview.py           # Generate HTML previews of posts
│   └── /utils/
│       └── document_converter.py # Convert docs to images for preview
│
├── /documents/                    # LinkedIn Documents API
│   ├── __init__.py               # Exports: API classes, attachment helpers
│   ├── api.py                    # Upload documents to LinkedIn
│   └── attachment.py             # Attach documents to posts
│
├── /posts/                        # Post text composition
│   ├── __init__.py
│   ├── composition.py            # ComposablePost
│   └── /components/              # Hook, Body, CTA, Hashtags
│
├── /components/                   # HTML rendering helpers (shared)
│   ├── component_renderer.py    # Simple HTML rendering
│   ├── /visual_elements/         # Badges, callouts, etc.
│   └── /data_viz/                # Charts, metrics
│
├── /themes/                       # Post themes and tone
├── /api/                          # LinkedIn API client
├── /utils/                        # Shared utilities
└── server.py                      # MCP server

preview_post.py                    # Quick CLI preview utility
```

**See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.**

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests

# Type checking
mypy src

# Try the preview example
python examples/preview_example.py
```

## Examples

Check out the `examples/` directory:

**`layout_token_showcase.py`** - Complete design token and layout system demonstration
```bash
python examples/layout_token_showcase.py
```
Comprehensive showcase of the entire token system:
- All design tokens (typography, colors, spacing, layouts)
- Text and engagement tokens
- LinkedIn-specific 2025 optimizations
- How layouts reference tokens
- Mobile-first design principles

**`preview_example.py`** - Complete preview workflow demonstration
```bash
python examples/preview_example.py
```
Creates a sample thought leadership post and generates a browser preview with analytics.

**`complete_example.py`** - Comprehensive usage examples covering all post types and features.

**Quick Start**:
```bash
# See the token system in action
python examples/layout_token_showcase.py

# Try the preview system
python examples/preview_example.py

# Or use the CLI utility for your drafts
python preview_post.py --list
```

## License

MIT

## Credits

Built by [Christopher Hay](https://github.com/chrishayuk)

Based on 2025 LinkedIn performance data from analysis of 1M+ posts across 9K company pages.

Design system principles inspired by [shadcn/ui](https://ui.shadcn.com/) and [CVA](https://cva.style/).
