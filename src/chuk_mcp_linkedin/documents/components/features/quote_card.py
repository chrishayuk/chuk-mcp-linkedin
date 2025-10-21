"""
Quote Card component for document slides.

Visual quote display - adapts Quote from posts to visual format.
"""

from typing import Optional
from ..base import DocumentComponent, RenderContext


class QuoteCard(DocumentComponent):
    """
    Visual quote/testimonial card for document slides.

    Visual version of posts.Quote component.
    Uses DesignTokens for all styling.
    """

    def __init__(
        self,
        text: str,
        author: str,
        source: Optional[str] = None,
        style: str = "default",  # default, centered, bordered
    ):
        self.text = text
        self.author = author
        self.source = source
        self.style = style

    def render(self, context: RenderContext) -> str:
        """Render quote card to HTML"""
        # Get styling from design tokens
        quote_size = context.get_font_size("large")
        author_size = context.get_font_size("body")
        padding = context.get_spacing('padding', 'spacious')

        # Get background color with opacity from tokens
        from ....tokens.design_tokens import DesignTokens
        bg_opacity = DesignTokens.VISUAL["opacity"]["faint"]  # 0.1
        # Create subtle background using accent color with low opacity
        bg_style = f"background: {context.accent_color}1a;"  # Hex with alpha

        # Style variations
        border_style = ""
        if self.style == "bordered":
            border_style = f"border-left: 6px solid {context.accent_color}; padding-left: {padding}px;"
        elif self.style == "centered":
            border_style = "text-align: center;"

        # Build quote mark emoji
        quote_emoji = "💬"

        # Build attribution
        attribution = f"— {self.author}"
        if self.source:
            attribution += f", {self.source}"

        # Get icon size from tokens
        icon_size = DesignTokens.VISUAL["icon_sizes"]["medium"]

        return f"""
        <div class="quote-card" style="
            {bg_style}
            padding: {padding}px;
            border-radius: {DesignTokens.LAYOUT['border_radius']['medium']}px;
            margin: {context.get_spacing('gaps', 'large')}px auto;
            max-width: 800px;
            {border_style}
        ">
            <div class="quote-icon" style="
                font-size: {icon_size}px;
                margin-bottom: {context.get_spacing('gaps', 'small')}px;
            ">
                {quote_emoji}
            </div>

            <div class="quote-text" style="
                font-family: {context.font_family};
                font-size: {quote_size}px;
                font-weight: 500;
                color: {context.primary_color};
                line-height: 1.6;
                margin-bottom: {context.get_spacing('gaps', 'medium')}px;
                font-style: italic;
            ">
                "{self.text}"
            </div>

            <div class="quote-attribution" style="
                font-family: {context.font_family};
                font-size: {author_size}px;
                font-weight: 600;
                color: {context.secondary_color};
            ">
                {attribution}
            </div>
        </div>
        """

    def validate(self) -> bool:
        """Validate quote card"""
        return (
            len(self.text) > 0 and
            len(self.text) <= 500 and
            len(self.author) > 0
        )

    def get_dimensions(self, context: RenderContext) -> dict:
        """Get quote card dimensions"""
        quote_size = context.get_font_size("large")
        author_size = context.get_font_size("body")
        padding = context.get_spacing('padding', 'spacious')
        gaps = context.get_spacing('gaps', 'medium')

        # Estimate height based on text length
        lines = len(self.text) // 60 + 1  # Rough estimate
        height = (
            48 +  # Icon
            (quote_size * 1.6 * lines) +  # Quote text
            author_size +  # Attribution
            padding * 2 +
            gaps * 2
        )

        return {
            "width": 800,
            "height": int(height),
        }
