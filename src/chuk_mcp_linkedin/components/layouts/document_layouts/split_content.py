"""
Split Content Layout - 50/50 split layout with text + visual.

Use for:
- Text with supporting image
- Before/after comparisons
- Concept + visualization
"""

from ..base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, Typography


def split_content() -> LayoutConfig:
    """
    50/50 split layout - text + visual.

    Use for:
    - Text with supporting image
    - Before/after comparisons
    - Concept + visualization
    """
    return LayoutConfig(
        name="Split Content",
        type=LayoutType.SPLIT_CONTENT,
        description="50/50 split - text on left, visual on right",
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
            max_lines=1,
        ),
        content_zone=LayoutZone(
            x=100,
            y=300,
            width=810,
            height=1450,
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            line_height=Typography.LINE_HEIGHTS["relaxed"],
        ),
        image_zone=LayoutZone(
            x=1010,
            y=300,
            width=810,
            height=1450,
            align="center",
            valign="middle",
            properties={"fit": "cover", "border_radius": 8},
        ),
        branding_zone=LayoutZone(
            x=860, y=1750, width=200, height=70, align="center", valign="bottom"
        ),
        best_for=["text_visual", "before_after", "comparison"],
        use_cases=["Product + description", "Problem + solution", "Concept + diagram"],
    )
