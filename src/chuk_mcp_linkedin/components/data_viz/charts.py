"""
Chart components for LinkedIn documents.

Bar charts, line charts, pie charts, and other data visualizations.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any, List as ListType
from ...tokens.design_tokens import DesignTokens


class Charts:
    """Chart components for LinkedIn documents"""

    @staticmethod
    def bar_chart(
        data: ListType[Dict[str, Any]],
        orientation: str = "vertical",
        color_scheme: str = "minimal",
        show_values: bool = True,
        show_labels: bool = True,
    ) -> Dict[str, Any]:
        """
        Bar chart (vertical or horizontal bars).

        Args:
            data: List of dicts with 'label' and 'value' keys
            orientation: Chart orientation (vertical, horizontal)
            color_scheme: Color scheme to use
            show_values: Show values on bars
            show_labels: Show axis labels

        Returns:
            Bar chart component configuration
        """
        bar_color = DesignTokens.get_color(color_scheme, "accent")
        label_color = DesignTokens.get_color(color_scheme, "primary")
        value_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "chart",
            "variant": "bar",
            "data": data,  # [{"label": "Q1", "value": 100}, ...]
            "orientation": orientation,
            "bar_color": bar_color,
            "label_color": label_color,
            "value_color": value_color,
            "show_values": show_values,
            "show_labels": show_labels,
            "bar_spacing": DesignTokens.get_spacing("gaps", "small"),  # 16px
            "bar_radius": DesignTokens.LAYOUT["border_radius"]["small"],  # Rounded ends
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
        }

    @staticmethod
    def line_chart(
        data: ListType[Dict[str, Any]],
        show_points: bool = True,
        smooth: bool = False,
        color_scheme: str = "minimal",
        show_grid: bool = True,
    ) -> Dict[str, Any]:
        """
        Line chart (trend visualization).

        Args:
            data: List of dicts with 'label' and 'value' keys
            show_points: Show data points on line
            smooth: Use smooth curves vs straight lines
            color_scheme: Color scheme to use
            show_grid: Show background grid

        Returns:
            Line chart component configuration
        """
        line_color = DesignTokens.get_color(color_scheme, "accent")
        point_color = DesignTokens.get_color(color_scheme, "accent")
        label_color = DesignTokens.get_color(color_scheme, "primary")
        grid_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "chart",
            "variant": "line",
            "data": data,  # [{"label": "Jan", "value": 100}, ...]
            "line_color": line_color,
            "line_width": 3,  # 3px line
            "point_color": point_color,
            "point_size": 8,  # 8px diameter
            "show_points": show_points,
            "smooth": smooth,
            "show_grid": show_grid,
            "grid_color": f"{grid_color}20",  # 12% opacity
            "label_color": label_color,
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
        }

    @staticmethod
    def pie_chart(
        data: ListType[Dict[str, Any]],
        show_labels: bool = True,
        show_percentages: bool = True,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Pie chart (proportional circle chart).

        Args:
            data: List of dicts with 'label' and 'value' keys
            show_labels: Show segment labels
            show_percentages: Show percentage values
            color_scheme: Color scheme to use

        Returns:
            Pie chart component configuration
        """
        # Use semantic colors for segments
        segment_colors = [
            DesignTokens.get_color(color_scheme, "accent"),
            DesignTokens.COLORS["semantic"]["success"],
            DesignTokens.COLORS["semantic"]["info"],
            DesignTokens.COLORS["semantic"]["warning"],
            DesignTokens.get_color(color_scheme, "secondary"),
        ]

        label_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "chart",
            "variant": "pie",
            "data": data,  # [{"label": "Category A", "value": 30}, ...]
            "segment_colors": segment_colors,
            "show_labels": show_labels,
            "show_percentages": show_percentages,
            "label_color": label_color,
            "label_font_size": DesignTokens.get_font_size("body"),
            "percentage_font_size": DesignTokens.get_font_size("large"),
            "percentage_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
        }

    @staticmethod
    def donut_chart(
        data: ListType[Dict[str, Any]],
        center_text: str = None,
        center_value: str = None,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Donut chart (pie chart with center hole).

        Args:
            data: List of dicts with 'label' and 'value' keys
            center_text: Optional text in center
            center_value: Optional large value in center
            color_scheme: Color scheme to use

        Returns:
            Donut chart component configuration
        """
        segment_colors = [
            DesignTokens.get_color(color_scheme, "accent"),
            DesignTokens.COLORS["semantic"]["success"],
            DesignTokens.COLORS["semantic"]["info"],
            DesignTokens.COLORS["semantic"]["warning"],
            DesignTokens.get_color(color_scheme, "secondary"),
        ]

        center_text_color = DesignTokens.get_color(color_scheme, "primary")

        config = {
            "type": "chart",
            "variant": "donut",
            "data": data,
            "segment_colors": segment_colors,
            "hole_size": 0.6,  # 60% hole (proportion of radius)
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
        }

        if center_value or center_text:
            config["center"] = {}

            if center_value:
                config["center"]["value"] = {
                    "text": center_value,
                    "font_size": DesignTokens.get_font_size("hero"),  # 120pt
                    "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
                    "color": center_text_color,
                }

            if center_text:
                config["center"]["label"] = {
                    "text": center_text,
                    "font_size": DesignTokens.get_font_size("body"),
                    "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
                    "color": DesignTokens.get_color(color_scheme, "secondary"),
                }

        return config

    @staticmethod
    def area_chart(
        data: ListType[Dict[str, Any]],
        fill_opacity: float = 0.3,
        color_scheme: str = "minimal",
        show_line: bool = True,
    ) -> Dict[str, Any]:
        """
        Area chart (filled line chart).

        Args:
            data: List of dicts with 'label' and 'value' keys
            fill_opacity: Area fill opacity (0-1)
            color_scheme: Color scheme to use
            show_line: Show line at top of area

        Returns:
            Area chart component configuration
        """
        area_color = DesignTokens.get_color(color_scheme, "accent")
        line_color = DesignTokens.get_color(color_scheme, "accent")
        label_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "chart",
            "variant": "area",
            "data": data,
            "area_color": f"{area_color}{int(fill_opacity * 255):02x}",  # Color with opacity
            "line_color": line_color if show_line else None,
            "line_width": 3 if show_line else 0,
            "label_color": label_color,
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
        }

    @staticmethod
    def stacked_bar_chart(
        data: ListType[Dict[str, Any]],
        series: ListType[str],
        orientation: str = "vertical",
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Stacked bar chart (multiple series per bar).

        Args:
            data: List of dicts with label and series values
            series: List of series names
            orientation: Chart orientation (vertical, horizontal)
            color_scheme: Color scheme to use

        Returns:
            Stacked bar chart component configuration
        """
        # Use different colors for each series
        series_colors = [
            DesignTokens.get_color(color_scheme, "accent"),
            DesignTokens.COLORS["semantic"]["success"],
            DesignTokens.COLORS["semantic"]["info"],
            DesignTokens.COLORS["semantic"]["warning"],
        ]

        label_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "chart",
            "variant": "stacked_bar",
            "data": data,  # [{"label": "Q1", "series1": 10, "series2": 20}, ...]
            "series": series,  # ["series1", "series2"]
            "series_colors": series_colors,
            "orientation": orientation,
            "label_color": label_color,
            "bar_spacing": DesignTokens.get_spacing("gaps", "small"),
            "bar_radius": DesignTokens.LAYOUT["border_radius"]["small"],
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
        }

    @staticmethod
    def scatter_plot(
        data: ListType[Dict[str, Any]],
        color_scheme: str = "minimal",
        point_size: int = None,
        show_trend_line: bool = False,
    ) -> Dict[str, Any]:
        """
        Scatter plot (x/y coordinate visualization).

        Args:
            data: List of dicts with 'x', 'y', and optional 'label' keys
            color_scheme: Color scheme to use
            point_size: Point size in pixels (defaults to token size)
            show_trend_line: Show trend/regression line

        Returns:
            Scatter plot component configuration
        """
        if point_size is None:
            point_size = 12  # 12px points

        point_color = DesignTokens.get_color(color_scheme, "accent")
        trend_line_color = DesignTokens.COLORS["semantic"]["info"]
        label_color = DesignTokens.get_color(color_scheme, "primary")

        config = {
            "type": "chart",
            "variant": "scatter",
            "data": data,  # [{"x": 10, "y": 20, "label": "Point A"}, ...]
            "point_color": point_color,
            "point_size": point_size,
            "label_color": label_color,
            "font_size": DesignTokens.get_font_size("small"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
        }

        if show_trend_line:
            config["trend_line"] = {
                "color": trend_line_color,
                "width": 2,
                "style": "dashed",
            }

        return config
