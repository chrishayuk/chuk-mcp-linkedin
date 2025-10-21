"""
Text Block component for document slides.

Rich text content with automatic formatting and design token integration.
"""

from typing import Optional
from ..base import DocumentComponent, RenderContext


class TextBlock(DocumentComponent):
    """
    Rich text block for document slides.

    Uses DesignTokens for all styling - NO hardcoded values.
    """

    def __init__(
        self,
        content: str,
        font_size: str = "body",  # Key from DesignTokens.TYPOGRAPHY['sizes']
        font_weight: str = "normal",  # Key from DesignTokens.TYPOGRAPHY['weights']
        alignment: str = "left",  # left, center, right
        color: Optional[str] = None,  # Defaults to primary color from theme
        max_width: Optional[str] = None,  # Key from DesignTokens.LAYOUT['max_width']
    ):
        self.content = content
        self.font_size = font_size
        self.font_weight = font_weight
        self.alignment = alignment
        self.color = color
        self.max_width = max_width

    def render(self, context: RenderContext) -> str:
        """Render text block to HTML"""
        # Get styling from design tokens
        font_size_px = context.get_font_size(self.font_size)
        color = self.color or context.primary_color

        # Get max width if specified
        max_width_px = None
        if self.max_width:
            from ....tokens.design_tokens import DesignTokens
            max_width_px = DesignTokens.LAYOUT["max_width"].get(self.max_width, None)

        # Build style
        style = f"""
            font-family: {context.font_family};
            font-size: {font_size_px}px;
            font-weight: {self.font_weight};
            text-align: {self.alignment};
            color: {color};
            line-height: 1.6;
            margin: {context.get_spacing('padding', 'normal')}px 0;
        """

        if max_width_px:
            style += f"max-width: {max_width_px}px; margin-left: auto; margin-right: auto;"

        return f"""
        <div class="text-block" style="{style}">
            {self._format_content(self.content)}
        </div>
        """

    def _format_content(self, content: str) -> str:
        """Format content with automatic line breaks"""
        # Convert newlines to <br> tags
        return content.replace('\n', '<br>')

    def validate(self) -> bool:
        """Validate text block"""
        return len(self.content) > 0 and len(self.content) <= 5000

    def get_dimensions(self, context: RenderContext) -> dict:
        """Get text block dimensions"""
        # Estimate height based on content length and font size
        font_size = context.get_font_size(self.font_size)
        lines = len(self.content.split('\n'))
        height = lines * font_size * 1.6 + context.get_spacing('padding', 'normal') * 2

        return {
            "width": context.available_width,
            "height": int(height),
        }
