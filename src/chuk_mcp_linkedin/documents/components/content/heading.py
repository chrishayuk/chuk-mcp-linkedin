"""
Heading component for document slides.

Section headings with design token integration.
"""

from typing import Optional
from ..base import DocumentComponent, RenderContext


class Heading(DocumentComponent):
    """
    Section heading for document slides.

    Uses DesignTokens for typography - NO hardcoded values.
    """

    def __init__(
        self,
        text: str,
        level: int = 1,  # 1-6, affects font size
        alignment: str = "left",  # left, center, right
        color: Optional[str] = None,  # Defaults to primary color
        underline: bool = False,
    ):
        self.text = text
        self.level = max(1, min(6, level))  # Clamp to 1-6
        self.alignment = alignment
        self.color = color
        self.underline = underline

    def render(self, context: RenderContext) -> str:
        """Render heading to HTML"""
        # Map levels to design token font sizes
        size_map = {
            1: "hero",      # Biggest
            2: "display",
            3: "title",
            4: "xlarge",
            5: "large",
            6: "body",      # Smallest
        }
        size_key = size_map[self.level]
        font_size_px = context.get_font_size(size_key)

        # Map levels to font weights
        weight_map = {
            1: "900",  # black
            2: "700",  # bold
            3: "700",  # bold
            4: "600",  # semibold
            5: "600",  # semibold
            6: "500",  # medium
        }
        font_weight = weight_map[self.level]

        color = self.color or context.primary_color

        # Build style
        style = f"""
            font-family: {context.font_family};
            font-size: {font_size_px}px;
            font-weight: {font_weight};
            text-align: {self.alignment};
            color: {color};
            line-height: 1.2;
            margin: {context.get_spacing('gaps', 'large')}px 0 {context.get_spacing('gaps', 'medium')}px 0;
        """

        if self.underline:
            style += f"""
            border-bottom: 4px solid {context.accent_color};
            padding-bottom: {context.get_spacing('gaps', 'small')}px;
            """

        return f"""
        <h{self.level} class="heading" style="{style}">
            {self.text}
        </h{self.level}>
        """

    def validate(self) -> bool:
        """Validate heading"""
        return len(self.text) > 0 and len(self.text) <= 200

    def get_dimensions(self, context: RenderContext) -> dict:
        """Get heading dimensions"""
        size_map = {
            1: "hero",
            2: "display",
            3: "title",
            4: "xlarge",
            5: "large",
            6: "body",
        }
        size_key = size_map[self.level]
        font_size = context.get_font_size(size_key)

        # Estimate height
        height = font_size * 1.2 + context.get_spacing('gaps', 'large') + context.get_spacing('gaps', 'medium')

        return {
            "width": context.available_width,
            "height": int(height),
        }
