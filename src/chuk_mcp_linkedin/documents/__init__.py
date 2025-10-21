"""
Document generation module for LinkedIn content.

Complete system for creating LinkedIn document posts (PDF slides).
Atomic composition similar to posts module, using DesignTokens and themes.

Document posts have the highest engagement rate (45.85%) in 2025.
Best practices:
- Keep to 5-10 slides maximum
- One clear message per slide
- 18pt minimum font size (mobile readability)
- Square format (1920x1920) preferred
- Consistent branding throughout

Example usage:
    from chuk_mcp_linkedin.documents import ComposableDocument, TextBlock, StatCard
    from chuk_mcp_linkedin.themes import ThemeManager

    theme = ThemeManager().get_theme('thought_leader')
    doc = ComposableDocument(format_type='html', theme=theme)

    # Add slides with layouts and components
    doc.add_slide('title_slide')\\
       .set_title('Q1 2025 Results')\\
       .set_subtitle('Growth & Performance')

    doc.add_slide('content_slide')\\
       .set_title('Key Highlights')\\
       .add_component(StatCard('45.85%', 'Engagement Rate'))

    html = doc.render()
"""

# Composition system
from .composition import ComposableDocument, DocumentBuilder, Slide

# Layout system
from .layouts import DocumentLayouts

# Base classes
from .components.base import DocumentComponent, RenderContext

# Content components
from .components.content import TextBlock, BulletList, Heading

# Feature components
from .components.features import StatCard, QuoteCard

__all__ = [
    # Composition
    "ComposableDocument",
    "DocumentBuilder",
    "Slide",
    # Layouts
    "DocumentLayouts",
    # Base
    "DocumentComponent",
    "RenderContext",
    # Content
    "TextBlock",
    "BulletList",
    "Heading",
    # Features
    "StatCard",
    "QuoteCard",
]
