# chuk-mcp-linkedin

A comprehensive design system MCP server for creating LinkedIn posts with shadcn-inspired component architecture, CVA-style variants, and powerful theming.

## Overview

`chuk-mcp-linkedin` brings design system principles to LinkedIn content creation. Create posts using composable components, variants, and themes - similar to modern frontend design systems like shadcn/ui but for social media content.

## Features

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

```bash
pip install chuk-mcp-linkedin
```

## Quick Start

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

```python
from chuk_mcp_linkedin import DocumentPost, ChartComponents

# Create document post
doc = DocumentPost(
    commentary="Our Q4 results are in. Here's what we learned 📊",
    variant="report",
    theme=theme_mgr.get_theme("data_driven")
)

# Add slides
doc.add_slide(
    layout="title_slide",
    content={"title": "Q4 2024 Results", "subtitle": "Growth & Insights"}
)

# Add metrics with chart
metrics_chart = ChartComponents.metric_grid(
    title="Key Metrics",
    metrics=[
        {"label": "Revenue", "value": "$1.2M", "trend": "+12%"},
        {"label": "Customers", "value": "450", "trend": "+25%"},
    ]
)

doc.add_slide(
    layout="content_slide",
    content={"title": "Q4 Performance", "chart": metrics_chart}
)

doc.publish()
```

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
- `linkedin_preview` - Get preview
- `linkedin_export_draft` - Export as JSON

### Analytics
- `linkedin_get_post_stats` - Get post analytics
- `linkedin_get_suggestions` - Get content suggestions
- `linkedin_analyze_draft` - Analyze draft performance potential

## Design Tokens

Research-backed design tokens for optimal engagement:

### Text Formatting
- Character limits (3000 max, 210 before "see more")
- Ideal lengths (micro: 50-150, short: 150-300, medium: 300-800, long: 800-1500, story: 1000-3000)
- Line break styles (dense, readable, scannable, dramatic, extreme)

### Emoji Usage
- None, minimal (1%), moderate (5%), expressive (10%), heavy (15%)

### Hashtags
- Optimal count: 3-5 hashtags
- Placement strategies: inline, mid, end, first_comment

### Engagement Patterns
- Hook types with power ratings (controversy: 0.95, stat: 0.9, story: 0.85)
- CTA styles (direct, curiosity, action, share, soft)
- First hour targets (minimum: 10, good: 50, viral: 100 engagements)

### Timing
- Best days: Tuesday, Wednesday, Thursday
- Best hours: 7-9 AM, 12-2 PM, 5-6 PM
- Optimal frequency: 4-5 posts per week

## Architecture

```
src/chuk_mcp_linkedin/
├── components/        # Post type components
├── subcomponents/     # Composition subcomponents
├── tokens/           # Design tokens
├── themes/           # Theme system
├── layouts/          # Visual layouts
├── charts/           # Chart components
├── variants.py       # Variant system
├── composition.py    # Composition patterns
├── registry.py       # Component registry
├── manager.py        # Draft management
└── server.py         # MCP server
```

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
```

## License

MIT

## Credits

Built by [Christopher Hay](https://github.com/chrishayuk)

Based on 2025 LinkedIn performance data from analysis of 1M+ posts across 9K company pages.

Design system principles inspired by [shadcn/ui](https://ui.shadcn.com/) and [CVA](https://cva.style/).
