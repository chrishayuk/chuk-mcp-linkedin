"""
Content Slide Layout - Standard content slide, most versatile.

Use for:
- Main content pages
- Lists and bullet points
- General information
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, ColorScheme, Typography


def content_slide() -> LayoutConfig:
    """
    Standard content slide - most versatile.

    Use for:
    - Main content pages
    - Lists and bullet points
    - General information
    """
    return LayoutConfig(
        name="Content Slide",
        type=LayoutType.CONTENT_SLIDE,
        description="Title + content area with bullets/lists",
        canvas_size=CanvasSize.DOCUMENT_SQUARE,
        safe_area={"top": 100, "right": 100, "bottom": 100, "left": 100},
        title_zone=LayoutZone(
            x=100,
            y=100,
            width=1720,
            height=200,
            align="left",
            valign="top",
            font_size=Typography.SIZES["title"],
            font_weight=Typography.WEIGHTS["bold"],
            line_height=Typography.LINE_HEIGHTS["tight"],
            max_lines=2,
            color=ColorScheme.MINIMAL["primary"],
        ),
        content_zone=LayoutZone(
            x=100,
            y=350,
            width=1720,
            height=1350,
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            font_weight=Typography.WEIGHTS["normal"],
            line_height=Typography.LINE_HEIGHTS["relaxed"],
            color=ColorScheme.MINIMAL["primary"],
            properties={"bullet_points": True, "max_bullets": 5},
        ),
        branding_zone=LayoutZone(
            x=1720, y=1750, width=100, height=70, align="right", valign="bottom"
        ),
        best_for=["content", "lists", "steps", "tips"],
        use_cases=["How-to steps", "Key points", "Bullet lists", "Takeaways"],
    )
