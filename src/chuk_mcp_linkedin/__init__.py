"""
chuk-mcp-linkedin - Design system MCP server for LinkedIn posts.

A comprehensive design system for creating LinkedIn posts with shadcn-inspired
component architecture, CVA-style variants, and powerful theming.

## Quick Start

```python
from chuk_mcp_linkedin import LinkedInManager, ThemeManager, ComposablePost

# Initialize
manager = LinkedInManager()
theme_mgr = ThemeManager()

# Create a post with theme
theme = theme_mgr.get_theme("thought_leader")
post = ComposablePost("text", theme=theme)

# Compose using fluent API
post.add_hook("stat", "95% of B2B leads come from LinkedIn")
post.add_body("Here's what works...", structure="listicle")
post.add_cta("curiosity", "What's your strategy?")
post.add_hashtags(["B2BMarketing", "LinkedInTips"])

# Generate final text
final_text = post.compose()
```

## Features

- **7 Post Types**: Text, Document, Poll, Video, Carousel, Image, Article
- **10 Themes**: Thought Leader, Personal Brand, Technical Expert, etc.
- **CVA Variants**: Flexible variant system with compound support
- **Design Tokens**: Research-backed optimization (2025 data)
- **LLM-Friendly**: Complete component registry for discovery

## 2025 Performance Insights

- Document Posts: 45.85% engagement (HIGHEST)
- Poll Posts: 200%+ reach (MOST UNDERUSED)
- Video Posts: 1.4x engagement (+69% usage)

"""

from .manager import LinkedInManager, Draft
from .composition import ComposablePost, PostBuilder, Hook, Body, CallToAction, Hashtags
from .themes.theme_manager import ThemeManager, LinkedInTheme, THEMES
from .registry import ComponentRegistry
from .variants import PostVariants, VariantResolver
from .tokens import TextTokens, EngagementTokens, StructureTokens
from .preview import LinkedInPreview

__version__ = "0.1.0"

__all__ = [
    # Core Management
    "LinkedInManager",
    "Draft",
    # Composition
    "ComposablePost",
    "PostBuilder",
    "Hook",
    "Body",
    "CallToAction",
    "Hashtags",
    # Themes
    "ThemeManager",
    "LinkedInTheme",
    "THEMES",
    # Registry & Variants
    "ComponentRegistry",
    "PostVariants",
    "VariantResolver",
    # Design Tokens
    "TextTokens",
    "EngagementTokens",
    "StructureTokens",
    # Preview
    "LinkedInPreview",
]
