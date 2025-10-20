"""
Metric components for LinkedIn documents.

KPI cards, metric grids, big stats, and comparison metrics.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any, List as ListType, Optional
from ...tokens.design_tokens import DesignTokens


class Metrics:
    """Metric components for LinkedIn documents"""

    @staticmethod
    def metric_card(
        label: str,
        value: str,
        change: Optional[float] = None,
        icon: Optional[str] = None,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Single metric card with optional change indicator.

        Args:
            label: Metric label (e.g., "Revenue")
            value: Metric value (e.g., "$1.2M")
            change: Optional change percentage
            icon: Optional icon/emoji
            color_scheme: Color scheme to use

        Returns:
            Metric card component configuration
        """
        label_color = DesignTokens.get_color(color_scheme, "secondary")
        value_color = DesignTokens.get_color(color_scheme, "primary")

        config = {
            "type": "metric",
            "variant": "card",
            "label": label,
            "value": value,
            "label_font_size": DesignTokens.get_font_size("body"),
            "label_font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "label_color": label_color,
            "value_font_size": DesignTokens.get_font_size("hero"),  # 120pt
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "value_color": value_color,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "padding": DesignTokens.SPACING["padding"]["normal"],
            "background_color": "#FFFFFF",
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
        }

        if icon:
            config["icon"] = {
                "symbol": icon,
                "size": DesignTokens.VISUAL["icon_sizes"]["large"],
                "margin_bottom": DesignTokens.get_spacing("gaps", "small"),
            }

        if change is not None:
            is_positive = change >= 0
            change_color = (
                DesignTokens.COLORS["semantic"]["success"]
                if is_positive
                else DesignTokens.COLORS["semantic"]["error"]
            )

            config["change"] = {
                "value": change,
                "text": f"{'↑' if is_positive else '↓'} {abs(change):.1f}%",
                "color": change_color,
                "font_size": DesignTokens.get_font_size("large"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
                "margin_top": DesignTokens.get_spacing("gaps", "small"),
            }

        return config

    @staticmethod
    def metric_grid(
        metrics: ListType[Dict[str, Any]], columns: int = 2, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Grid of metric cards.

        Args:
            metrics: List of metric dicts (label, value, change, icon)
            columns: Number of columns (2, 3, or 4)
            color_scheme: Color scheme to use

        Returns:
            Metric grid component configuration
        """
        return {
            "type": "metric",
            "variant": "grid",
            "metrics": metrics,  # [{"label": "Revenue", "value": "$1.2M", "change": 12.5}, ...]
            "columns": columns,
            "column_gap": DesignTokens.get_spacing("gaps", "large"),  # 40px
            "row_gap": DesignTokens.get_spacing("gaps", "large"),
            "color_scheme": color_scheme,
        }

    @staticmethod
    def big_stat(
        value: str,
        label: str,
        context: Optional[str] = None,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Big statistic (hero number).

        Args:
            value: Large stat value (e.g., "45.85%")
            label: Stat label
            context: Optional context text
            color_scheme: Color scheme to use

        Returns:
            Big stat component configuration
        """
        value_color = DesignTokens.get_color(color_scheme, "accent")
        label_color = DesignTokens.get_color(color_scheme, "primary")
        context_color = DesignTokens.get_color(color_scheme, "secondary")

        config = {
            "type": "metric",
            "variant": "big_stat",
            "value": value,
            "label": label,
            "value_font_size": DesignTokens.get_font_size("massive"),  # 200pt
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["black"],
            "value_color": value_color,
            "label_font_size": DesignTokens.get_font_size("xlarge"),  # 42pt
            "label_font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "label_color": label_color,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["display"],
            "text_align": "center",
            "margin_top": DesignTokens.get_spacing("gaps", "xxlarge"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "xxlarge"),
        }

        if context:
            config["context"] = {
                "text": context,
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
                "color": context_color,
                "margin_top": DesignTokens.get_spacing("gaps", "medium"),
            }

        return config

    @staticmethod
    def comparison_metrics(
        metric_a: Dict[str, Any],
        metric_b: Dict[str, Any],
        comparison_label: str = "vs",
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Side-by-side metric comparison.

        Args:
            metric_a: First metric dict (label, value)
            metric_b: Second metric dict (label, value)
            comparison_label: Text between metrics (e.g., "vs", "→")
            color_scheme: Color scheme to use

        Returns:
            Comparison metrics component configuration
        """
        label_color = DesignTokens.get_color(color_scheme, "secondary")
        value_color = DesignTokens.get_color(color_scheme, "primary")
        comparison_color = DesignTokens.get_color(color_scheme, "accent")

        return {
            "type": "metric",
            "variant": "comparison",
            "metric_a": metric_a,
            "metric_b": metric_b,
            "comparison_label": comparison_label,
            "label_font_size": DesignTokens.get_font_size("body"),
            "label_color": label_color,
            "value_font_size": DesignTokens.get_font_size("display"),  # 72pt
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "value_color": value_color,
            "comparison_font_size": DesignTokens.get_font_size("xlarge"),
            "comparison_color": comparison_color,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "gap": DesignTokens.get_spacing("gaps", "xlarge"),  # 60px between metrics
        }

    @staticmethod
    def kpi_row(kpis: ListType[Dict[str, str]], color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Horizontal row of KPIs.

        Args:
            kpis: List of KPI dicts (label, value)
            color_scheme: Color scheme to use

        Returns:
            KPI row component configuration
        """
        label_color = DesignTokens.get_color(color_scheme, "secondary")
        value_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "metric",
            "variant": "kpi_row",
            "kpis": kpis,  # [{"label": "Users", "value": "10K"}, ...]
            "label_font_size": DesignTokens.get_font_size("small"),
            "label_color": label_color,
            "value_font_size": DesignTokens.get_font_size("title"),  # 56pt
            "value_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "value_color": value_color,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "gap": DesignTokens.get_spacing("gaps", "xlarge"),
            "text_align": "center",
        }
