"""
Stat Card component for document slides.

Visual stat display - adapts BigStat from posts to visual format.
"""

from typing import Optional
from ..base import DocumentComponent, RenderContext


class StatCard(DocumentComponent):
    """
    Eye-catching statistic card for document slides.

    Visual version of posts.BigStat component.
    Uses DesignTokens for all styling.
    """

    def __init__(
        self,
        number: str,
        label: str,
        context: Optional[str] = None,
        color: Optional[str] = None,  # Defaults to accent color
        background: Optional[str] = None,  # Optional background color
    ):
        self.number = number
        self.label = label
        self.context_text = context
        self.color = color
        self.background = background

    def render(self, context: RenderContext) -> str:
        """Render stat card to HTML"""
        # Get colors from design tokens
        number_color = self.color or context.accent_color
        bg_color = self.background or "transparent"

        # Get font sizes from design tokens
        number_size = context.get_font_size("massive")
        label_size = context.get_font_size("xlarge")
        context_size = context.get_font_size("body")

        # Build card HTML
        card_html = f"""
        <div class="stat-card" style="
            background: {bg_color};
            padding: {context.get_spacing('padding', 'spacious')}px;
            text-align: center;
            border-radius: 16px;
            margin: {context.get_spacing('gaps', 'large')}px auto;
            max-width: 600px;
        ">
            <div class="stat-number" style="
                font-family: {context.font_family};
                font-size: {number_size}px;
                font-weight: 900;
                color: {number_color};
                line-height: 1;
                margin-bottom: {context.get_spacing('gaps', 'medium')}px;
            ">
                {self.number}
            </div>

            <div class="stat-label" style="
                font-family: {context.font_family};
                font-size: {label_size}px;
                font-weight: 600;
                color: {context.primary_color};
                line-height: 1.3;
                margin-bottom: {context.get_spacing('gaps', 'small')}px;
            ">
                {self.label}
            </div>
        """

        if self.context_text:
            card_html += f"""
            <div class="stat-context" style="
                font-family: {context.font_family};
                font-size: {context_size}px;
                color: {context.secondary_color};
                line-height: 1.5;
            ">
                {self.context_text}
            </div>
            """

        card_html += "</div>"
        return card_html

    def validate(self) -> bool:
        """Validate stat card"""
        return (
            len(self.number) > 0 and
            len(self.label) > 0 and
            len(self.number) <= 20 and
            len(self.label) <= 100
        )

    def get_dimensions(self, context: RenderContext) -> dict:
        """Get stat card dimensions"""
        number_size = context.get_font_size("massive")
        label_size = context.get_font_size("xlarge")
        context_size = context.get_font_size("body")
        padding = context.get_spacing('padding', 'spacious')
        gaps = context.get_spacing('gaps', 'medium')

        # Calculate height
        height = (
            number_size +
            label_size * 1.3 +
            (context_size * 1.5 if self.context_text else 0) +
            padding * 2 +
            gaps * 2
        )

        return {
            "width": 600,
            "height": int(height),
        }
