# LinkedIn MCP Design System - Documentation

Complete documentation for the LinkedIn MCP Design System.

## Overview

The LinkedIn MCP Design System is a comprehensive framework for creating optimized LinkedIn posts using:
- **Design system principles** (shadcn-inspired)
- **2025 performance data** (1M+ posts analyzed)
- **CVA-style variants** (compound variant support)
- **Theme-based composition** (10 pre-built personas)
- **LLM-friendly tools** (24 MCP tools)

---

## Documentation Index

### Core Concepts

1. **[Design Tokens](./TOKENS.md)** ⭐ **Start Here**
   - Text formatting tokens
   - Engagement patterns with power ratings
   - Content structures
   - 2025 algorithm optimization data

2. **[Theme System](./THEMES.md)**
   - 10 pre-built themes for different personas
   - Theme comparison matrix
   - Custom theme creation
   - Multi-theme strategies

3. **[Preview System](./PREVIEW.md)** 🆕
   - HTML preview generation
   - Document page rendering (PDF, PowerPoint, Word)
   - Interactive carousel navigation
   - Analytics dashboard
   - Installation and usage guide

### Quick Links

- **[Main README](../README.md)** - Project overview and quick start
- **[Implementation Status](../IMPLEMENTATION_STATUS.md)** - Complete feature list
- **[Examples](../examples/complete_example.py)** - 8 comprehensive examples

---

## Quick Start Guide

### Installation

```bash
cd chuk-mcp-linkedin
pip install -e .
```

### Basic Usage

```python
from chuk_mcp_linkedin import LinkedInManager, ThemeManager, ComposablePost

# Initialize
manager = LinkedInManager()
theme = ThemeManager().get_theme("thought_leader")

# Create post
post = ComposablePost("text", theme=theme)
post.add_hook("stat", "80% of B2B leads come from LinkedIn")
post.add_body("Here's what works...", structure="listicle")
post.add_cta("curiosity", "What's your strategy?")
post.add_hashtags(["B2BMarketing", "LinkedInTips"])

# Compose final text
final_text = post.compose()
print(final_text)
```

---

## Key Features

### 🎯 2025 Performance Data

All recommendations based on analysis of **1M+ posts**:

| Post Type | Engagement | Trend | Recommendation |
|-----------|-----------|-------|----------------|
| Document (PDF) | **45.85%** | ⬆ Highest | Use for deep content |
| Poll | **200%+ reach** | ⬆ Underused! | Maximum reach opportunity |
| Video | **1.4x engagement** | ⬆ +69% usage | Short, vertical, captions |
| Image | **2x comments** | → Stable | Good for quotes/data |
| Carousel | **-18% reach** | ⬇ Declining | Keep tight (5-10 slides) |
| Text | Variable | → Depends | Needs strong formatting |

### 🎨 Design System Architecture

**Component-Based:**
- 7 post types with variants
- 4 subcomponents (Hook, Body, CTA, Hashtags)
- 10 pre-built themes
- Shadcn-style composition

**CVA-Inspired Variants:**
- Text post variants (style, tone, length)
- Document variants (content_type, design_style)
- Poll variants (purpose, question_type)
- Compound variant support

**Research-Backed Tokens:**
- Hook types with power ratings (0.95 for controversy!)
- CTA effectiveness scores
- Optimal hashtag counts (3-5)
- Best posting times (7-9 AM, 12-2 PM, 5-6 PM)

### 🛠️ MCP Server (24 Tools)

**Draft Management:**
- `linkedin_create` - Create new draft
- `linkedin_list` - List all drafts
- `linkedin_switch` - Switch drafts
- `linkedin_get_info` - Get draft details
- `linkedin_delete` - Delete draft
- `linkedin_clear_all` - Clear all drafts

**Composition:**
- `linkedin_add_hook` - Add opening hook
- `linkedin_add_body` - Add main content
- `linkedin_add_cta` - Add call-to-action
- `linkedin_add_hashtags` - Add hashtags

**Themes:**
- `linkedin_list_themes` - List all themes
- `linkedin_get_theme` - Get theme details
- `linkedin_apply_theme` - Apply theme to draft

**Registry & Discovery:**
- `linkedin_list_components` - List all components
- `linkedin_get_component_info` - Component details
- `linkedin_get_recommendations` - Goal-based recommendations
- `linkedin_get_system_overview` - System overview

**Content Generation:**
- `linkedin_compose_post` - Compose final post
- `linkedin_get_preview` - Get 210-char preview
- `linkedin_export_draft` - Export as JSON

---

## Core Concepts

### Design Tokens

**What are they?**
Research-backed constants that optimize for LinkedIn's 2025 algorithm.

**Key Tokens:**
- `MAX_LENGTH` = 3000 characters
- `TRUNCATION_POINT` = 210 (critical!)
- Optimal hashtags = 3-5
- Hook power ratings (0-1 scale)
- First hour target = 50+ engagements

**Learn More:** [TOKENS.md](./TOKENS.md)

### Themes

**What are they?**
Complete content strategies for different LinkedIn personas.

**10 Pre-Built Themes:**
1. Thought Leader - Authority & expertise
2. Personal Brand - Authentic connection
3. Technical Expert - Deep knowledge
4. Community Builder - Foster conversation
5. Corporate Professional - Polished communication
6. Contrarian Voice - Challenge status quo
7. Storyteller - Narrative-driven
8. Data-Driven - Numbers-focused
9. Coach/Mentor - Guide & support
10. Entertainer - Fun & memorable

**Learn More:** [THEMES.md](./THEMES.md)

### Variants

**What are they?**
CVA-inspired system for defining post variations with compound support.

**Example:**
```python
# Text post variants
{
  "style": ["story", "insight", "question", "listicle", "hot_take"],
  "tone": ["professional", "conversational", "casual", "inspiring", "humorous"],
  "length": ["micro", "short", "medium", "long", "story"]
}

# Compound: story + inspiring = extreme line breaks + expressive emoji
```

### Composition

**What is it?**
Shadcn-style system for building posts from subcomponents.

**Subcomponents:**
- `Hook` - Opening hook (6 types)
- `Body` - Main content (5 structures)
- `CallToAction` - Engagement driver (6 types)
- `Hashtags` - Hashtag strategy
- `Separator` - Visual breaks

**Example:**
```python
post = (ComposablePost("text", theme=theme)
    .add_hook("stat", "95% of...")
    .add_body("Content...", structure="listicle")
    .add_cta("curiosity", "What do you think?")
    .add_hashtags(["Marketing"])
    .compose())
```

---

## Engagement Optimization

### Critical Metrics (2025 Algorithm)

1. **First Hour Engagement** ⚡
   - Target: 50+ engagements
   - Reply to ALL comments within 60 min
   - Determines total reach

2. **Hook Strength** 🎣
   - First 210 characters visible
   - Use high-power hooks:
     - Controversy (0.95)
     - Stat (0.9)
     - Story (0.85)

3. **Dwell Time** ⏱️
   - How long users stay on post
   - Scannable formatting (3 line breaks)
   - Use listicle structure

4. **Comment Quality** 💬
   - Not just quantity
   - Meaningful replies matter
   - Ask follow-up questions

5. **Share Rate** 🔄
   - Highest algorithm weight
   - Use "share" CTAs (0.9 power)
   - Tag-worthy content

### Best Posting Strategy

**Frequency:** 4-5 posts per week
**Days:** Tuesday, Wednesday, Thursday
**Times:** 7-9 AM, 12-2 PM, 5-6 PM (local)
**Hashtags:** 3-5 (optimal range)
**Emoji:** Moderate (5% ratio)
**Line Breaks:** Scannable (3 breaks)

---

## Use Cases

### 1. Building Authority

**Goal:** Establish expertise
**Theme:** Thought Leader
**Formats:** Document posts, Text with frameworks
**Frequency:** 4x per week
**Hook Style:** Stat (0.9 power)
**CTA Style:** Curiosity

```python
theme = ThemeManager().get_theme("thought_leader")
post = ComposablePost("document", theme=theme)
# Focus on data, frameworks, credibility
```

### 2. Growing Engagement

**Goal:** Maximum reach and interaction
**Theme:** Community Builder
**Formats:** Poll posts, Video, Text
**Frequency:** 5x per week
**Hook Style:** Question (0.8 power)
**CTA Style:** Share (0.9 power)

```python
theme = ThemeManager().get_theme("community_builder")
# Use polls (200%+ reach boost!)
```

### 3. Personal Branding

**Goal:** Build authentic following
**Theme:** Storyteller or Personal Brand
**Formats:** Text (stories), Video, Image
**Frequency:** 4-5x per week
**Hook Style:** Story (0.85 power)
**CTA Style:** Soft

```python
theme = ThemeManager().get_theme("storyteller")
post = PostBuilder.story_post(
    hook="I almost quit...",
    problem="...",
    journey="...",
    solution="...",
    lesson="...",
    theme=theme
)
```

### 4. Lead Generation

**Goal:** Convert connections to leads
**Theme:** Corporate Professional
**Formats:** Document posts, Carousel
**Frequency:** 3-4x per week
**Hook Style:** Stat
**CTA Style:** Action

```python
theme = ThemeManager().get_theme("corporate_professional")
# Focus on value, clear CTAs, professional design
```

---

## Examples

See **[examples/complete_example.py](../examples/complete_example.py)** for:

1. Simple text post with theme
2. Story post using builder pattern
3. Thought leadership with framework
4. Variant system usage
5. Component registry discovery
6. All 10 themes showcase
7. Draft management
8. Listicle posts

Run examples:
```bash
python examples/complete_example.py
```

---

## API Reference

### Core Classes

```python
# Manager
from chuk_mcp_linkedin import LinkedInManager
manager = LinkedInManager()
draft = manager.create_draft("name", "text", theme="thought_leader")

# Theme Manager
from chuk_mcp_linkedin import ThemeManager
theme_mgr = ThemeManager()
theme = theme_mgr.get_theme("personal_brand")

# Composition
from chuk_mcp_linkedin import ComposablePost
post = ComposablePost("text", theme=theme)

# Post Builder
from chuk_mcp_linkedin import PostBuilder
post = PostBuilder.story_post(...)

# Component Registry
from chuk_mcp_linkedin import ComponentRegistry
registry = ComponentRegistry()
recs = registry.get_recommendations("engagement")

# Tokens
from chuk_mcp_linkedin import TextTokens, EngagementTokens, StructureTokens
```

---

## Running the MCP Server

### Start Server

```bash
python -m chuk_mcp_linkedin.server
```

### Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "python",
      "args": ["-m", "chuk_mcp_linkedin.server"],
      "cwd": "/path/to/chuk-mcp-linkedin"
    }
  }
}
```

### Available Tools

Use these tools in Claude conversations:

```
linkedin_create - Create new draft
linkedin_add_hook - Add opening hook
linkedin_add_body - Add main content
linkedin_add_cta - Add call-to-action
linkedin_add_hashtags - Add hashtags
linkedin_compose_post - Generate final post
linkedin_list_themes - See all themes
linkedin_get_recommendations - Get suggestions for your goal
... and 16 more tools!
```

---

## Performance Tips

### 🔥 Hot Tips for Maximum Engagement

1. **Use Polls!** - 200%+ reach boost (most underused format)
2. **Document Posts** - 45.85% engagement (highest performer)
3. **First 210 Characters** - Make them irresistible
4. **Reply Within 60 Minutes** - Critical for algorithm
5. **3-5 Hashtags** - Sweet spot (more doesn't help)
6. **Scannable Formatting** - 3 line breaks between sections
7. **High-Power Hooks** - Controversy (0.95) or Stat (0.9)
8. **Post 4-5x Per Week** - Consistency wins

### ❌ Common Mistakes

1. Using 8+ hashtags (diminishing returns)
2. Not replying to comments quickly (algorithm penalty)
3. Weak hooks (first 210 chars matter!)
4. Posting on weekends (lower reach)
5. Dense paragraphs (low scannability)
6. No CTA (missed engagement)
7. Too infrequent (< 3x per week)
8. Ignoring video/polls (missing opportunities)

---

## Troubleshooting

### Low Engagement?

**Check:**
- [ ] Hook strength in first 210 characters
- [ ] Posting time (7-9 AM, 12-2 PM, 5-6 PM optimal)
- [ ] Reply speed (within 60 minutes?)
- [ ] Hashtag count (3-5 is sweet spot)
- [ ] Line break formatting (scannable = 3 breaks)
- [ ] CTA presence (every post needs one)

**Try:**
- Switch to poll post (200%+ reach boost)
- Use controversy hook (0.95 power rating)
- Post on Tuesday/Wednesday/Thursday
- Add more line breaks (scannable formatting)
- Reply to every comment within 1 hour

### Post Too Long?

```python
# Check character count
text = post.compose()
print(f"Length: {len(text)}/3000")

# Optimize length
from chuk_mcp_linkedin import TextTokens
ideal_min, ideal_max = TextTokens.get_length_range("medium")
# Aim for 300-800 chars for thought leadership
```

### Want More Authority?

```python
# Use data-driven theme
theme = ThemeManager().get_theme("data_driven")

# Use stat hooks
post.add_hook("stat", "95% of executives...")

# Create document posts (45.85% engagement!)
post = ComposablePost("document", theme=theme)
```

---

## Contributing

This is a comprehensive, production-ready system. Future enhancements could include:

- LinkedIn API integration for publishing
- Analytics and A/B testing
- Image/PDF generation
- Video creation tools
- Automated content calendar

---

## License

MIT License - See [LICENSE](../LICENSE)

---

## Resources

- **Main README:** [../README.md](../README.md)
- **Design Tokens:** [TOKENS.md](./TOKENS.md)
- **Theme System:** [THEMES.md](./THEMES.md)
- **Preview System:** [PREVIEW.md](./PREVIEW.md)
- **Examples:** [../examples/complete_example.py](../examples/complete_example.py)
- **Implementation Status:** [../IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md)

---

**Built with ❤️ by [Christopher Hay](https://github.com/chrishayuk)**

Based on 2025 LinkedIn performance data and design system principles.
