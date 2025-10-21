"""
Big Number Layout - Massive stat display for impact.

Use for:
- Key metrics
- Big statistics
- Growth numbers
- ROI/results
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, ColorScheme, Typography


def big_number() -> LayoutConfig:
    """
    Massive stat display - for impact.

    Use for:
    - Key metrics
    - Big statistics
    - Growth numbers
    - ROI/results
    """
    return LayoutConfig(
        name="Big Number",
        type=LayoutType.BIG_NUMBER,
        description="Huge number/stat with description",
        canvas_size=CanvasSize.DOCUMENT_SQUARE,
        safe_area={"top": 100, "right": 100, "bottom": 100, "left": 100},
        title_zone=LayoutZone(
            x=100,
            y=450,
            width=1720,
            height=700,
            align="center",
            valign="middle",
            font_size=200,  # HUGE
            font_weight=Typography.WEIGHTS["black"],
            line_height=1.0,
            max_lines=1,
            color=ColorScheme.LINKEDIN["accent"],
            properties={"number": True},
        ),
        subtitle_zone=LayoutZone(
            x=100,
            y=1200,
            width=1720,
            height=400,
            align="center",
            valign="top",
            font_size=Typography.SIZES["large"],
            font_weight=Typography.WEIGHTS["medium"],
            line_height=Typography.LINE_HEIGHTS["normal"],
            max_lines=3,
            color=ColorScheme.MINIMAL["secondary"],
        ),
        branding_zone=LayoutZone(
            x=860, y=1750, width=200, height=70, align="center", valign="bottom"
        ),
        best_for=["statistics", "metrics", "results", "growth"],
        use_cases=["Revenue numbers", "User growth", "% increases", "ROI stats"],
    )
