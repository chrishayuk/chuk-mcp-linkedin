"""
Table components for LinkedIn documents.

Data tables, comparison tables, pricing tables, and feature matrices.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any, List as ListType
from ...tokens.design_tokens import DesignTokens


class Tables:
    """Table components for LinkedIn documents"""

    @staticmethod
    def simple_table(
        headers: ListType[str],
        rows: ListType[ListType[str]],
        color_scheme: str = "minimal",
        striped: bool = True,
    ) -> Dict[str, Any]:
        """
        Simple data table.

        Args:
            headers: List of header labels
            rows: List of rows (each row is a list of values)
            color_scheme: Color scheme to use
            striped: Alternating row colors

        Returns:
            Simple table component configuration
        """
        header_bg = DesignTokens.get_color(color_scheme, "secondary")
        text_color = DesignTokens.get_color(color_scheme, "primary")
        border_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "table",
            "variant": "simple",
            "headers": headers,
            "rows": rows,
            "striped": striped,
            "header_color": "#FFFFFF",
            "header_background": header_bg,
            "header_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "text_color": text_color,
            "border_color": f"{border_color}40",  # 25% opacity
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "cell_padding": DesignTokens.SPACING["padding"]["tight"],  # 20px
            "border_width": 1,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
        }

    @staticmethod
    def comparison_table(
        columns: ListType[Dict[str, Any]],
        rows: ListType[Dict[str, Any]],
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Comparison table (e.g., feature comparison).

        Args:
            columns: List of column dicts (label, highlight)
            rows: List of row dicts (feature, values for each column)
            color_scheme: Color scheme to use

        Returns:
            Comparison table component configuration
        """
        header_color = DesignTokens.get_color(color_scheme, "primary")
        highlight_color = DesignTokens.get_color(color_scheme, "accent")
        text_color = DesignTokens.get_color(color_scheme, "primary")
        border_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "table",
            "variant": "comparison",
            "columns": columns,  # [{"label": "Basic", "highlight": False}, {"label": "Pro", "highlight": True}]
            "rows": rows,  # [{"feature": "Users", "values": ["5", "Unlimited"]}, ...]
            "header_color": header_color,
            "highlight_color": highlight_color,
            "highlight_background": f"{highlight_color}10",  # 6% opacity
            "text_color": text_color,
            "border_color": f"{border_color}40",
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "cell_padding": DesignTokens.SPACING["padding"]["tight"],
            "highlight_border_width": 3,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
        }

    @staticmethod
    def pricing_table(
        tiers: ListType[Dict[str, Any]], color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Pricing table with tiers.

        Args:
            tiers: List of tier dicts (name, price, features, highlight)
            color_scheme: Color scheme to use

        Returns:
            Pricing table component configuration
        """
        text_color = DesignTokens.get_color(color_scheme, "primary")
        secondary_color = DesignTokens.get_color(color_scheme, "secondary")
        accent_color = DesignTokens.get_color(color_scheme, "accent")
        success_color = DesignTokens.COLORS["semantic"]["success"]

        return {
            "type": "table",
            "variant": "pricing",
            "tiers": tiers,  # [{"name": "Basic", "price": "$9/mo", "features": [...], "highlight": False}, ...]
            "name_font_size": DesignTokens.get_font_size("large"),
            "name_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "name_color": text_color,
            "price_font_size": DesignTokens.get_font_size("hero"),  # 120pt
            "price_font_weight": DesignTokens.TYPOGRAPHY["weights"]["black"],
            "price_color": accent_color,
            "feature_font_size": DesignTokens.get_font_size("body"),
            "feature_color": secondary_color,
            "checkmark_color": success_color,
            "highlight_border_color": accent_color,
            "highlight_border_width": 3,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "padding": DesignTokens.SPACING["padding"]["loose"],  # 60px
            "border_radius": DesignTokens.LAYOUT["border_radius"]["large"],
            "gap": DesignTokens.get_spacing("gaps", "large"),
        }

    @staticmethod
    def feature_comparison(
        features: ListType[str],
        products: ListType[Dict[str, Any]],
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Feature comparison matrix.

        Args:
            features: List of feature names
            products: List of product dicts (name, feature_values)
            color_scheme: Color scheme to use

        Returns:
            Feature comparison component configuration
        """
        header_color = DesignTokens.get_color(color_scheme, "primary")
        text_color = DesignTokens.get_color(color_scheme, "primary")
        border_color = DesignTokens.get_color(color_scheme, "secondary")
        yes_color = DesignTokens.COLORS["semantic"]["success"]
        no_color = DesignTokens.COLORS["semantic"]["error"]

        return {
            "type": "table",
            "variant": "feature_comparison",
            "features": features,
            "products": products,  # [{"name": "Product A", "values": [True, True, False, ...]}, ...]
            "header_color": header_color,
            "header_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "text_color": text_color,
            "border_color": f"{border_color}40",
            "yes_symbol": "✓",
            "no_symbol": "—",
            "yes_color": yes_color,
            "no_color": no_color,
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "cell_padding": DesignTokens.SPACING["padding"]["tight"],
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
        }

    @staticmethod
    def data_table_with_totals(
        headers: ListType[str],
        rows: ListType[ListType[str]],
        totals: ListType[str],
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Data table with totals row.

        Args:
            headers: List of header labels
            rows: List of data rows
            totals: List of total values (same length as headers)
            color_scheme: Color scheme to use

        Returns:
            Data table with totals configuration
        """
        header_color = DesignTokens.get_color(color_scheme, "primary")
        text_color = DesignTokens.get_color(color_scheme, "primary")
        totals_bg = DesignTokens.get_color(color_scheme, "accent")
        border_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "table",
            "variant": "data_with_totals",
            "headers": headers,
            "rows": rows,
            "totals": totals,
            "header_color": header_color,
            "header_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "text_color": text_color,
            "totals_background": f"{totals_bg}20",  # 12% opacity
            "totals_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "border_color": f"{border_color}40",
            "font_size": DesignTokens.get_font_size("body"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "cell_padding": DesignTokens.SPACING["padding"]["tight"],
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
        }
