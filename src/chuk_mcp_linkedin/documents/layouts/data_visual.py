"""
Data Visual Layout - For charts and graphs.

Use for:
- Chart display
- Graph visualization
- Data presentation
- Metrics dashboard
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, ColorScheme, Typography
from ...tokens.design_tokens import DesignTokens


def data_visual() -> LayoutConfig:
    """
    Data visualization layout - for charts/graphs.

    Use for:
    - Chart display
    - Graph visualization
    - Data presentation
    - Metrics dashboard
    """
    return LayoutConfig(
        name="Data Visual",
        type=LayoutType.DATA_VISUAL,
        description="Large area for charts/graphs with title and caption",
        canvas_size=CanvasSize.DOCUMENT_SQUARE,
        safe_area={"top": 100, "right": 100, "bottom": 100, "left": 100},
        title_zone=LayoutZone(
            x=100,
            y=100,
            width=1720,
            height=150,
            align="left",
            valign="top",
            font_size=Typography.SIZES["xlarge"],
            font_weight=Typography.WEIGHTS["bold"],
        ),
        image_zone=LayoutZone(
            x=100,
            y=300,
            width=1720,
            height=1250,
            align="center",
            valign="middle",
            properties={
                "chart_area": True,
                "padding": DesignTokens.get_spacing("padding", "normal"),
            },
        ),
        subtitle_zone=LayoutZone(
            x=100,
            y=1600,
            width=1720,
            height=150,
            align="left",
            valign="top",
            font_size=Typography.SIZES["small"],
            color=ColorScheme.MINIMAL["secondary"],
            properties={"caption": True},
        ),
        best_for=["charts", "graphs", "data", "metrics"],
        use_cases=["Sales charts", "Growth graphs", "Performance metrics"],
    )
