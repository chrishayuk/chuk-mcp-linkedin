"""
Title Slide Layout - Hero title slide for first slide impact.

Use for:
- Opening slide
- Section dividers
- Big announcements
"""

from ..base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, ColorScheme, Typography


def title_slide() -> LayoutConfig:
    """
    Hero title slide - first slide impact.

    Use for:
    - Opening slide
    - Section dividers
    - Big announcements
    """
    return LayoutConfig(
        name="Title Slide",
        type=LayoutType.TITLE_SLIDE,
        description="Large centered title for maximum impact",
        canvas_size=CanvasSize.DOCUMENT_SQUARE,
        background_color=ColorScheme.MINIMAL["background"],
        safe_area={"top": 100, "right": 100, "bottom": 100, "left": 100},
        title_zone=LayoutZone(
            x=100,
            y=700,
            width=1720,
            height=500,
            align="center",
            valign="middle",
            font_size=Typography.SIZES["hero"],
            font_weight=Typography.WEIGHTS["black"],
            line_height=Typography.LINE_HEIGHTS["tight"],
            max_lines=3,
            color=ColorScheme.MINIMAL["primary"],
        ),
        subtitle_zone=LayoutZone(
            x=100,
            y=1300,
            width=1720,
            height=150,
            align="center",
            valign="top",
            font_size=Typography.SIZES["large"],
            font_weight=Typography.WEIGHTS["normal"],
            color=ColorScheme.MINIMAL["secondary"],
        ),
        branding_zone=LayoutZone(
            x=100, y=1700, width=200, height=120, align="left", valign="bottom"
        ),
        best_for=["opening", "section_divider", "announcement"],
        use_cases=["Guide intro", "Report title", "Presentation opener"],
    )
