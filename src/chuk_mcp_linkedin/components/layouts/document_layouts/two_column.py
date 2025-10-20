"""
Two Column Layout - For balanced content presentation.

Use for:
- Pros and cons
- Features and benefits
- Two related topics
"""

from ..base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, Typography


def two_column() -> LayoutConfig:
    """
    Two-column layout - for balanced content.

    Use for:
    - Pros and cons
    - Features and benefits
    - Two related topics
    """
    return LayoutConfig(
        name="Two Column",
        type=LayoutType.TWO_COLUMN,
        description="Two equal columns of content",
        canvas_size=CanvasSize.DOCUMENT_SQUARE,
        safe_area={"top": 100, "right": 100, "bottom": 100, "left": 100},
        title_zone=LayoutZone(
            x=100,
            y=100,
            width=1720,
            height=150,
            align="center",
            valign="top",
            font_size=Typography.SIZES["xlarge"],
            font_weight=Typography.WEIGHTS["bold"],
        ),
        # Left column
        content_zone=LayoutZone(
            x=100,
            y=300,
            width=810,
            height=1450,
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            line_height=Typography.LINE_HEIGHTS["relaxed"],
            properties={"bullet_points": True},
        ),
        # Right column
        content_zone_2=LayoutZone(
            x=1010,
            y=300,
            width=810,
            height=1450,
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            line_height=Typography.LINE_HEIGHTS["relaxed"],
            properties={"bullet_points": True},
        ),
        best_for=["pros_cons", "features_benefits", "parallel_content"],
        use_cases=["Feature list", "Pros and cons", "Dual topics"],
    )
