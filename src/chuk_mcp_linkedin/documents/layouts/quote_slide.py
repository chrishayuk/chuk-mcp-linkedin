"""
Quote Slide Layout - For testimonials and pull quotes.

Use for:
- Customer testimonials
- Expert quotes
- Key takeaways
- Memorable statements
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, ColorScheme, Typography


def quote_slide() -> LayoutConfig:
    """
    Quote slide - for testimonials or pull quotes.

    Use for:
    - Customer testimonials
    - Expert quotes
    - Key takeaways
    - Memorable statements
    """
    return LayoutConfig(
        name="Quote Slide",
        type=LayoutType.QUOTE,
        description="Large centered quote with attribution",
        canvas_size=CanvasSize.DOCUMENT_SQUARE,
        safe_area={"top": 200, "right": 200, "bottom": 200, "left": 200},
        content_zone=LayoutZone(
            x=200,
            y=500,
            width=1520,
            height=800,
            align="center",
            valign="middle",
            font_size=Typography.SIZES["xlarge"],
            font_weight=Typography.WEIGHTS["medium"],
            line_height=Typography.LINE_HEIGHTS["relaxed"],
            max_lines=5,
            color=ColorScheme.MINIMAL["primary"],
            properties={"quote_marks": True, "italic": True},
        ),
        subtitle_zone=LayoutZone(
            x=200,
            y=1400,
            width=1520,
            height=150,
            align="center",
            valign="top",
            font_size=Typography.SIZES["body"],
            font_weight=Typography.WEIGHTS["semibold"],
            color=ColorScheme.MINIMAL["secondary"],
            properties={"attribution": True},
        ),
        branding_zone=LayoutZone(
            x=860, y=1700, width=200, height=100, align="center", valign="bottom"
        ),
        best_for=["testimonials", "quotes", "key_messages"],
        use_cases=["Customer quotes", "Expert opinions", "Key takeaways"],
    )
