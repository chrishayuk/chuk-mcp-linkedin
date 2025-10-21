"""
Comparison Layout - Side-by-side comparison A vs B.

Use for:
- Before/after
- Good vs bad practices
- Option A vs Option B
- Then vs now
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, Typography
from ...tokens.design_tokens import DesignTokens


def comparison() -> LayoutConfig:
    """
    Side-by-side comparison - A vs B.

    Use for:
    - Before/after
    - Good vs bad practices
    - Option A vs Option B
    - Then vs now
    """
    return LayoutConfig(
        name="Comparison",
        type=LayoutType.COMPARISON,
        description="Side-by-side comparison with visual distinction",
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
        # Left side (usually "bad" or "before")
        content_zone=LayoutZone(
            x=100,
            y=300,
            width=760,
            height=1450,
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            line_height=Typography.LINE_HEIGHTS["normal"],
            properties={
                "label": "Option A",
                "background_color": "#FEE2E2",  # Light red
                "icon": "❌",
                "padding": DesignTokens.get_spacing("padding", "normal"),
            },
        ),
        # Right side (usually "good" or "after")
        content_zone_2=LayoutZone(
            x=960,
            y=300,
            width=760,
            height=1450,
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            line_height=Typography.LINE_HEIGHTS["normal"],
            properties={
                "label": "Option B",
                "background_color": "#D1FAE5",  # Light green
                "icon": "✅",
                "padding": DesignTokens.get_spacing("padding", "normal"),
            },
        ),
        branding_zone=LayoutZone(
            x=860, y=1750, width=200, height=70, align="center", valign="bottom"
        ),
        best_for=["comparisons", "before_after", "good_bad"],
        use_cases=["Traditional vs modern", "Wrong vs right way", "Then vs now"],
    )
