"""
Infographic components for LinkedIn documents.

Visual data representations: stat with icon, funnel charts, process flows, and comparison bars.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any, List as ListType
from ...tokens.design_tokens import DesignTokens


class Infographics:
    """Infographic components for LinkedIn documents"""

    @staticmethod
    def stat_with_icon(
        icon: str,
        value: str,
        label: str,
        color: str = None,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Statistic with large icon.

        Args:
            icon: Icon/emoji
            value: Stat value
            label: Stat label
            color: Icon/accent color (defaults to accent from scheme)
            color_scheme: Color scheme to use

        Returns:
            Stat with icon component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "accent")

        value_color = DesignTokens.get_color(color_scheme, "primary")
        label_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "infographic",
            "variant": "stat_with_icon",
            "icon": icon,
            "value": value,
            "label": label,
            "icon_size": DesignTokens.VISUAL["icon_sizes"]["huge"],  # 120px
            "icon_color": color,
            "value_font_size": DesignTokens.get_font_size("hero"),  # 120pt
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "value_color": value_color,
            "label_font_size": DesignTokens.get_font_size("large"),
            "label_font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "label_color": label_color,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "text_align": "center",
            "gap": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def funnel_chart(
        stages: ListType[Dict[str, Any]], color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Funnel chart (conversion funnel).

        Args:
            stages: List of stage dicts (label, value, percentage)
            color_scheme: Color scheme to use

        Returns:
            Funnel chart component configuration
        """
        funnel_color = DesignTokens.get_color(color_scheme, "accent")
        text_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "infographic",
            "variant": "funnel",
            "stages": stages,  # [{"label": "Visitors", "value": "10K", "percentage": 100}, ...]
            "funnel_color": funnel_color,
            "text_color": text_color,
            "label_font_size": DesignTokens.get_font_size("large"),
            "label_font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "value_font_size": DesignTokens.get_font_size("title"),  # 56pt
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "stage_gap": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def process_flow(
        steps: ListType[str],
        orientation: str = "horizontal",
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Process flow diagram.

        Args:
            steps: List of step labels
            orientation: Flow direction (horizontal, vertical)
            color_scheme: Color scheme to use

        Returns:
            Process flow component configuration
        """
        step_bg_color = DesignTokens.get_color(color_scheme, "accent")
        arrow_color = DesignTokens.get_color(color_scheme, "secondary")
        text_color = "#FFFFFF"

        return {
            "type": "infographic",
            "variant": "process_flow",
            "steps": steps,
            "orientation": orientation,
            "step_background": step_bg_color,
            "arrow_color": arrow_color,
            "text_color": text_color,
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "step_padding": DesignTokens.SPACING["padding"]["normal"],  # 40px
            "step_border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            "arrow_size": DesignTokens.VISUAL["icon_sizes"]["small"],  # 32px
            "gap": DesignTokens.get_spacing("gaps", "large"),
        }

    @staticmethod
    def comparison_bars(
        items: ListType[Dict[str, Any]],
        max_value: float,
        color_scheme: str = "minimal",
        show_values: bool = True,
    ) -> Dict[str, Any]:
        """
        Horizontal comparison bars.

        Args:
            items: List of item dicts (label, value)
            max_value: Maximum value for scaling
            color_scheme: Color scheme to use
            show_values: Show value numbers

        Returns:
            Comparison bars component configuration
        """
        bar_color = DesignTokens.get_color(color_scheme, "accent")
        label_color = DesignTokens.get_color(color_scheme, "primary")
        value_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "infographic",
            "variant": "comparison_bars",
            "items": items,  # [{"label": "Product A", "value": 85}, ...]
            "max_value": max_value,
            "bar_color": bar_color,
            "bar_background": f"{bar_color}20",  # 12% opacity
            "label_color": label_color,
            "value_color": value_color,
            "show_values": show_values,
            "bar_height": 40,  # 40px bars
            "bar_border_radius": DesignTokens.LAYOUT["border_radius"]["small"],
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "item_gap": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def icon_grid_stat(
        items: ListType[Dict[str, Any]], columns: int = 2, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Grid of icon+stat combinations.

        Args:
            items: List of item dicts (icon, value, label)
            columns: Number of columns
            color_scheme: Color scheme to use

        Returns:
            Icon grid stat component configuration
        """
        icon_color = DesignTokens.get_color(color_scheme, "accent")
        value_color = DesignTokens.get_color(color_scheme, "primary")
        label_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "infographic",
            "variant": "icon_grid_stat",
            "items": items,  # [{"icon": "🚀", "value": "10K", "label": "Users"}, ...]
            "columns": columns,
            "icon_size": DesignTokens.VISUAL["icon_sizes"]["xlarge"],  # 96px
            "icon_color": icon_color,
            "value_font_size": DesignTokens.get_font_size("display"),  # 72pt
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "value_color": value_color,
            "label_font_size": DesignTokens.get_font_size("body"),
            "label_color": label_color,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "column_gap": DesignTokens.get_spacing("gaps", "xlarge"),
            "row_gap": DesignTokens.get_spacing("gaps", "xlarge"),
            "text_align": "center",
        }

    @staticmethod
    def timeline_infographic(
        events: ListType[Dict[str, Any]],
        orientation: str = "horizontal",
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Timeline infographic.

        Args:
            events: List of event dicts (date, title, description, icon)
            orientation: Timeline direction (horizontal, vertical)
            color_scheme: Color scheme to use

        Returns:
            Timeline infographic component configuration
        """
        line_color = DesignTokens.get_color(color_scheme, "accent")
        marker_color = DesignTokens.get_color(color_scheme, "accent")
        text_color = DesignTokens.get_color(color_scheme, "primary")
        date_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "infographic",
            "variant": "timeline",
            "events": events,  # [{"date": "Q1 2024", "title": "Launch", "description": "...", "icon": "🚀"}, ...]
            "orientation": orientation,
            "line_color": line_color,
            "line_width": 4,
            "marker_color": marker_color,
            "marker_size": DesignTokens.VISUAL["icon_sizes"]["small"],  # 32px
            "text_color": text_color,
            "date_color": date_color,
            "title_font_size": DesignTokens.get_font_size("large"),
            "title_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "description_font_size": DesignTokens.get_font_size("body"),
            "date_font_size": DesignTokens.get_font_size("body"),
            "date_font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "event_gap": DesignTokens.get_spacing("gaps", "xlarge"),
        }
