"""
Bullet List component for document slides.

Formatted bullet lists with design token integration.
"""

from typing import List, Optional
from ..base import DocumentComponent, RenderContext
from ....tokens.text_tokens import TextTokens


class BulletList(DocumentComponent):
    """
    Formatted bullet list for document slides.

    Uses DesignTokens for styling, TextTokens for bullet symbols.
    """

    def __init__(
        self,
        items: List[str],
        bullet_style: str = "bullet",  # bullet, checkmark, arrow, numbered
        font_size: str = "body",
        spacing: str = "medium",  # Key from DesignTokens.SPACING['gaps']
        max_items: int = 8,  # LinkedIn best practice: don't overcrowd slides
    ):
        self.items = items[:max_items]  # Limit items for readability
        self.bullet_style = bullet_style
        self.font_size = font_size
        self.spacing = spacing
        self.max_items = max_items

    def render(self, context: RenderContext) -> str:
        """Render bullet list to HTML"""
        # Get styling from design tokens
        font_size_px = context.get_font_size(self.font_size)
        gap_px = context.get_spacing('gaps', self.spacing)

        # Get bullet symbol from text tokens
        bullet_symbols = {
            "bullet": TextTokens.SYMBOLS["bullet"],
            "checkmark": TextTokens.SYMBOLS["checkmark"],
            "arrow": TextTokens.SYMBOLS["arrow"],
            "numbered": None,  # Use numbers
        }
        bullet = bullet_symbols.get(self.bullet_style, "•")

        # Build list items
        list_items = []
        for i, item in enumerate(self.items, 1):
            prefix = f"{i}." if self.bullet_style == "numbered" else bullet
            list_items.append(f"""
            <div style="
                display: flex;
                align-items: flex-start;
                margin-bottom: {gap_px}px;
            ">
                <span style="
                    min-width: 30px;
                    font-weight: 600;
                    color: {context.accent_color};
                ">{prefix}</span>
                <span style="flex: 1;">{item}</span>
            </div>
            """)

        return f"""
        <div class="bullet-list" style="
            font-family: {context.font_family};
            font-size: {font_size_px}px;
            color: {context.primary_color};
            line-height: 1.6;
            padding: {context.get_spacing('padding', 'normal')}px;
        ">
            {''.join(list_items)}
        </div>
        """

    def validate(self) -> bool:
        """Validate bullet list"""
        return (
            len(self.items) > 0 and
            len(self.items) <= self.max_items and
            all(len(item) > 0 for item in self.items)
        )

    def get_dimensions(self, context: RenderContext) -> dict:
        """Get bullet list dimensions"""
        font_size = context.get_font_size(self.font_size)
        gap = context.get_spacing('gaps', self.spacing)
        padding = context.get_spacing('padding', 'normal')

        # Estimate height
        item_height = font_size * 1.6
        total_gaps = gap * (len(self.items) - 1)
        height = (item_height * len(self.items)) + total_gaps + (padding * 2)

        return {
            "width": context.available_width,
            "height": int(height),
        }
