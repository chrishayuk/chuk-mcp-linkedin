"""
List components for LinkedIn documents.

Bulleted lists, numbered lists, checklists, and icon lists.
Uses design tokens and structure tokens for consistent styling.
"""

from typing import Dict, Any, List as ListType
from ...tokens.design_tokens import DesignTokens


class Lists:
    """List components for LinkedIn documents"""

    @staticmethod
    def bulleted_list(
        items: ListType[str],
        bullet_style: str = "arrow",
        color_scheme: str = "minimal",
        size: str = "body",
    ) -> Dict[str, Any]:
        """
        Bulleted list with custom bullet styles.

        Args:
            items: List of text items
            bullet_style: Bullet type (arrow, disc, checkmark, star, custom symbols from tokens)
            color_scheme: Color scheme to use
            size: Font size (small, body, large)

        Returns:
            Bulleted list component configuration
        """
        text_color = DesignTokens.get_color(color_scheme, "primary")
        bullet_color = DesignTokens.get_color(color_scheme, "accent")

        # Get bullet symbol from structure tokens
        bullet_symbols = {
            "arrow": "→",
            "disc": "•",
            "checkmark": "✓",
            "star": "★",
            "pin": "📌",
            "lightning": "⚡",
            "target": "🎯",
        }

        bullet = bullet_symbols.get(bullet_style, bullet_symbols["arrow"])

        return {
            "type": "list",
            "variant": "bulleted",
            "items": items,
            "bullet": bullet,
            "bullet_color": bullet_color,
            "font_size": DesignTokens.get_font_size(size),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],  # 1.8
            "color": text_color,
            "item_spacing": DesignTokens.get_spacing("gaps", "small"),  # 16px between items
            "bullet_spacing": DesignTokens.get_spacing("gaps", "small"),  # 16px bullet-to-text
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def numbered_list(
        items: ListType[str],
        start_number: int = 1,
        number_style: str = "decimal",
        color_scheme: str = "minimal",
        size: str = "body",
    ) -> Dict[str, Any]:
        """
        Numbered list with different numbering styles.

        Args:
            items: List of text items
            start_number: Starting number
            number_style: Number format (decimal, roman, alpha)
            color_scheme: Color scheme to use
            size: Font size (small, body, large)

        Returns:
            Numbered list component configuration
        """
        text_color = DesignTokens.get_color(color_scheme, "primary")
        number_color = DesignTokens.get_color(color_scheme, "accent")

        return {
            "type": "list",
            "variant": "numbered",
            "items": items,
            "start_number": start_number,
            "number_style": number_style,  # decimal (1,2,3), roman (I,II,III), alpha (A,B,C)
            "number_color": number_color,
            "font_size": DesignTokens.get_font_size(size),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
            "color": text_color,
            "item_spacing": DesignTokens.get_spacing("gaps", "small"),
            "number_spacing": DesignTokens.get_spacing("gaps", "small"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def checklist(
        items: ListType[Dict[str, Any]],
        show_checkmarks: bool = True,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Checklist with completed/incomplete states.

        Args:
            items: List of dicts with 'text' and optional 'checked' (bool)
            show_checkmarks: Show checkmarks for completed items
            color_scheme: Color scheme to use

        Returns:
            Checklist component configuration
        """
        text_color = DesignTokens.get_color(color_scheme, "primary")
        checked_color = DesignTokens.COLORS["semantic"]["success"]
        unchecked_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "list",
            "variant": "checklist",
            "items": items,
            "show_checkmarks": show_checkmarks,
            "checked_symbol": "✓",
            "unchecked_symbol": "☐",
            "checked_color": checked_color,
            "unchecked_color": unchecked_color,
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
            "color": text_color,
            "item_spacing": DesignTokens.get_spacing(
                "gaps", "medium"
            ),  # 24px (larger for checklists)
            "symbol_spacing": DesignTokens.get_spacing("gaps", "small"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),
        }

    @staticmethod
    def icon_list(items: ListType[Dict[str, Any]], color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        List where each item has its own icon.

        Args:
            items: List of dicts with 'text' and 'icon' (emoji/symbol)
            color_scheme: Color scheme to use

        Returns:
            Icon list component configuration
        """
        text_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "list",
            "variant": "icon_list",
            "items": items,  # Each item: {"icon": "🚀", "text": "..."}
            "icon_size": DesignTokens.get_font_size("large"),  # 32pt
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
            "color": text_color,
            "item_spacing": DesignTokens.get_spacing("gaps", "medium"),  # 24px
            "icon_spacing": DesignTokens.get_spacing("gaps", "small"),  # 16px
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),
        }

    @staticmethod
    def two_column_list(
        items: ListType[str],
        bullet_style: str = "arrow",
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Two-column bulleted list (for compact layouts).

        Args:
            items: List of text items
            bullet_style: Bullet type
            color_scheme: Color scheme to use

        Returns:
            Two-column list component configuration
        """
        text_color = DesignTokens.get_color(color_scheme, "primary")
        bullet_color = DesignTokens.get_color(color_scheme, "accent")

        bullet_symbols = {
            "arrow": "→",
            "disc": "•",
            "checkmark": "✓",
        }

        bullet = bullet_symbols.get(bullet_style, bullet_symbols["arrow"])

        return {
            "type": "list",
            "variant": "two_column",
            "items": items,
            "bullet": bullet,
            "bullet_color": bullet_color,
            "columns": 2,
            "column_gap": DesignTokens.get_spacing("gaps", "xlarge"),  # 60px
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
            "color": text_color,
            "item_spacing": DesignTokens.get_spacing("gaps", "small"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def definition_list(
        items: ListType[Dict[str, str]], color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Definition list (term: description pairs).

        Args:
            items: List of dicts with 'term' and 'description'
            color_scheme: Color scheme to use

        Returns:
            Definition list component configuration
        """
        term_color = DesignTokens.get_color(color_scheme, "primary")
        description_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "list",
            "variant": "definition",
            "items": items,  # Each item: {"term": "...", "description": "..."}
            "term_font_size": DesignTokens.get_font_size("body"),
            "term_font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "term_color": term_color,
            "description_font_size": DesignTokens.get_font_size("body"),
            "description_font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "description_color": description_color,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
            "item_spacing": DesignTokens.get_spacing("gaps", "medium"),  # 24px
            "term_description_gap": DesignTokens.get_spacing("gaps", "tiny"),  # 8px
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),
        }
