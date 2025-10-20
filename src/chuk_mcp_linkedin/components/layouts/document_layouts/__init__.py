"""
Document post layouts (PDF slides).

Document posts have 45.85% engagement rate - highest of all formats in 2025.
These layouts are optimized for 1920x1920 square format.

Best practices for 2025:
- Keep to 5-10 slides maximum
- One clear message per slide
- 18pt minimum font size (mobile readability)
- Square format (1920x1920) preferred
- Consistent branding throughout
"""

from typing import Dict, List, Any

from ..base import LayoutConfig

# Import all layout functions
from .title_slide import title_slide
from .content_slide import content_slide
from .split_content import split_content
from .big_number import big_number
from .quote_slide import quote_slide
from .comparison import comparison
from .two_column import two_column
from .checklist import checklist
from .timeline import timeline
from .icon_grid import icon_grid
from .data_visual import data_visual


class DocumentLayouts:
    """
    Pre-built layouts for LinkedIn document posts (PDF slides).

    Best practices for 2025:
    - Keep to 5-10 slides maximum
    - One clear message per slide
    - 18pt minimum font size (mobile readability)
    - Square format (1920x1920) preferred
    - Consistent branding throughout
    """

    # Expose layout functions as static methods
    title_slide = staticmethod(title_slide)
    content_slide = staticmethod(content_slide)
    split_content = staticmethod(split_content)
    big_number = staticmethod(big_number)
    quote_slide = staticmethod(quote_slide)
    comparison = staticmethod(comparison)
    two_column = staticmethod(two_column)
    checklist = staticmethod(checklist)
    timeline = staticmethod(timeline)
    icon_grid = staticmethod(icon_grid)
    data_visual = staticmethod(data_visual)

    @staticmethod
    def get_all() -> Dict[str, LayoutConfig]:
        """Get all document layouts"""
        return {
            "title_slide": title_slide(),
            "content_slide": content_slide(),
            "split_content": split_content(),
            "big_number": big_number(),
            "quote": quote_slide(),
            "comparison": comparison(),
            "two_column": two_column(),
            "checklist": checklist(),
            "timeline": timeline(),
            "icon_grid": icon_grid(),
            "data_visual": data_visual(),
        }

    @staticmethod
    def get_layout(name: str) -> LayoutConfig:
        """Get a specific layout by name"""
        layouts = DocumentLayouts.get_all()
        if name not in layouts:
            raise ValueError(f"Layout '{name}' not found. Available: {list(layouts.keys())}")
        return layouts[name]

    @staticmethod
    def list_layouts() -> List[Dict[str, Any]]:
        """List all layouts with metadata"""
        layouts = DocumentLayouts.get_all()
        return [
            {
                "name": key,
                "type": layout.type.value,
                "description": layout.description,
                "best_for": layout.best_for,
                "use_cases": layout.use_cases,
            }
            for key, layout in layouts.items()
        ]


__all__ = [
    "DocumentLayouts",
    "title_slide",
    "content_slide",
    "split_content",
    "big_number",
    "quote_slide",
    "comparison",
    "two_column",
    "checklist",
    "timeline",
    "icon_grid",
    "data_visual",
]
