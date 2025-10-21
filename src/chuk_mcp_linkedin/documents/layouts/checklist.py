"""
Checklist Layout - For actionable items and step-by-step guides.

Use for:
- Step-by-step guides
- Checklists
- Action items
- Requirements
"""

from ...components.layouts.base import LayoutConfig, LayoutType, LayoutZone, CanvasSize, Typography


def checklist() -> LayoutConfig:
    """
    Checklist layout - actionable items.

    Use for:
    - Step-by-step guides
    - Checklists
    - Action items
    - Requirements
    """
    return LayoutConfig(
        name="Checklist",
        type=LayoutType.CHECKLIST,
        description="Checklist with checkbox icons",
        canvas_size=CanvasSize.DOCUMENT_SQUARE,
        safe_area={"top": 100, "right": 100, "bottom": 150, "left": 100},
        title_zone=LayoutZone(
            x=100,
            y=100,
            width=1720,
            height=180,
            align="left",
            valign="top",
            font_size=Typography.SIZES["title"],
            font_weight=Typography.WEIGHTS["bold"],
        ),
        content_zone=LayoutZone(
            x=100,
            y=330,
            width=1720,
            height=1370,
            align="left",
            valign="top",
            font_size=Typography.SIZES["body"],
            line_height=Typography.LINE_HEIGHTS["loose"],
            properties={
                "checkbox": True,
                "checkbox_style": "☐",  # Empty checkbox
                "spacing_between": 60,
                "max_items": 7,
            },
        ),
        branding_zone=LayoutZone(
            x=100, y=1750, width=1720, height=70, align="center", valign="bottom"
        ),
        best_for=["checklists", "action_items", "steps"],
        use_cases=["Pre-launch checklist", "Setup steps", "Requirements"],
    )
