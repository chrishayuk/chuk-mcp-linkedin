"""
Timeline Layout - Chronological events display.

Use for:
- Company history
- Project milestones
- Roadmap
- Journey/process
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, Typography


def timeline() -> LayoutConfig:
    """
    Timeline layout - chronological events.

    Use for:
    - Company history
    - Project milestones
    - Roadmap
    - Journey/process
    """
    return LayoutConfig(
        name="Timeline",
        type=LayoutType.TIMELINE,
        description="Vertical timeline with dates and events",
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
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            line_height=Typography.LINE_HEIGHTS["normal"],
            properties={
                "timeline": True,
                "dot_position": 300,  # X position of timeline dots
                "date_width": 250,
                "event_indent": 380,
                "spacing_between": 120,
            },
        ),
        best_for=["chronology", "milestones", "history", "roadmap"],
        use_cases=["Company timeline", "Project phases", "2024 highlights"],
    )
