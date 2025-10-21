"""
Icon Grid Layout - Visual features/benefits showcase.

Use for:
- Feature showcase
- Benefits list
- Service offerings
- Key points with icons
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, Typography


def icon_grid() -> LayoutConfig:
    """
    Icon grid - visual features/benefits.

    Use for:
    - Feature showcase
    - Benefits list
    - Service offerings
    - Key points with icons
    """
    return LayoutConfig(
        name="Icon Grid",
        type=LayoutType.ICON_GRID,
        description="Grid of icons with labels (2x2 or 3x2)",
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
        content_zone=LayoutZone(
            x=100,
            y=300,
            width=1720,
            height=1450,
            align="center",
            valign="top",
            properties={
                "grid": True,
                "columns": 2,
                "rows": 2,
                "gap": 80,
                "icon_size": 120,
                "title_size": Typography.SIZES["large"],
                "description_size": Typography.SIZES["small"],
            },
        ),
        best_for=["features", "benefits", "services", "key_points"],
        use_cases=["Product features", "Service offerings", "Core values"],
    )
