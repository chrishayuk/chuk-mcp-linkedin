# src/chuk_mcp_linkedin/components/visual_elements/badges.py
"""
Badge and label components for LinkedIn documents.

Small visual indicators for status, categories, and highlights.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any
from ...tokens.design_tokens import DesignTokens


class Badges:
    """Badge and label components for LinkedIn documents"""

    @staticmethod
    def pill_badge(text: str, color: str = None, size: str = "medium") -> Dict[str, Any]:
        """
        Pill-shaped badge.

        Args:
            text: Badge text
            color: Badge color (defaults to LinkedIn blue)
            size: "small", "medium", "large"
        """
        if color is None:
            color = DesignTokens.COLORS["linkedin"]["blue"]

        sizes = {
            "small": {
                "font_size": DesignTokens.get_font_size("small"),
                "padding_x": DesignTokens.SPACING["gaps"]["small"],  # 16
                "padding_y": DesignTokens.SPACING["gaps"]["tiny"],  # 8
            },
            "medium": {
                "font_size": DesignTokens.get_font_size("body"),
                "padding_x": DesignTokens.SPACING["gaps"]["small"],  # 16
                "padding_y": DesignTokens.SPACING["gaps"]["tiny"],  # 8
            },
            "large": {
                "font_size": DesignTokens.get_font_size("large"),
                "padding_x": DesignTokens.SPACING["gaps"]["medium"],  # 24
                "padding_y": DesignTokens.SPACING["gaps"]["small"],  # 16
            },
        }

        size_config = sizes.get(size, sizes["medium"])

        return {
            "type": "badge",
            "variant": "pill",
            "text": text,
            "background_color": color,
            "text_color": "#FFFFFF",
            "font_size": size_config["font_size"],
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "padding_x": size_config["padding_x"],
            "padding_y": size_config["padding_y"],
            "border_radius": DesignTokens.LAYOUT["border_radius"]["round"],
        }

    @staticmethod
    def status_badge(status: str, style: str = "semantic") -> Dict[str, Any]:
        """
        Status indicator badge.

        Args:
            status: "new", "trending", "hot", "updated", "beta"
            style: "semantic" (colored) or "minimal" (outlined)
        """
        status_colors = {
            "new": DesignTokens.COLORS["semantic"]["success"],
            "trending": DesignTokens.COLORS["semantic"]["info"],
            "hot": DesignTokens.COLORS["semantic"]["error"],
            "updated": DesignTokens.COLORS["semantic"]["warning"],
            "beta": DesignTokens.COLORS["semantic"]["info"],
        }

        color = status_colors.get(status.lower(), DesignTokens.COLORS["semantic"]["info"])

        if style == "semantic":
            return {
                "type": "badge",
                "variant": "status",
                "text": status.upper(),
                "background_color": color,
                "text_color": "#FFFFFF",
                "font_size": DesignTokens.get_font_size("small"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
                "padding_x": DesignTokens.SPACING["gaps"]["small"],
                "padding_y": DesignTokens.SPACING["gaps"]["tiny"],
                "border_radius": DesignTokens.LAYOUT["border_radius"]["small"],
            }
        else:  # minimal
            return {
                "type": "badge",
                "variant": "status_outlined",
                "text": status.upper(),
                "background_color": "transparent",
                "text_color": color,
                "border_color": color,
                "border_width": 2,
                "font_size": DesignTokens.get_font_size("small"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
                "padding_x": DesignTokens.SPACING["gaps"]["small"],
                "padding_y": DesignTokens.SPACING["gaps"]["tiny"],
                "border_radius": DesignTokens.LAYOUT["border_radius"]["small"],
            }

    @staticmethod
    def number_badge(number: int, color: str = None, shape: str = "circle") -> Dict[str, Any]:
        """
        Number badge (notification style).

        Args:
            number: Number to display
            color: Badge color (defaults to error/red)
            shape: "circle" or "square"
        """
        if color is None:
            color = DesignTokens.COLORS["semantic"]["error"]

        # Use icon sizes from tokens for single/double digits
        size = (
            DesignTokens.VISUAL["icon_sizes"]["small"]
            if number < 10
            else DesignTokens.VISUAL["icon_sizes"]["medium"]
        )

        return {
            "type": "badge",
            "variant": "number",
            "number": number,
            "background_color": color,
            "text_color": "#FFFFFF",
            "font_size": DesignTokens.get_font_size("small"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "size": size,
            "border_radius": (
                DesignTokens.LAYOUT["border_radius"]["round"]
                if shape == "circle"
                else DesignTokens.LAYOUT["border_radius"]["small"]
            ),
        }

    @staticmethod
    def percentage_change(value: float, format_string: str = "{:+.1f}%") -> Dict[str, Any]:
        """
        Percentage change badge (with color based on positive/negative).

        Args:
            value: Percentage value (positive or negative)
            format_string: Format string for display
        """
        is_positive = value >= 0
        color = (
            DesignTokens.COLORS["semantic"]["success"]
            if is_positive
            else DesignTokens.COLORS["semantic"]["error"]
        )
        icon = "↑" if is_positive else "↓"

        formatted_value = format_string.format(value)

        return {
            "type": "badge",
            "variant": "percentage_change",
            "value": value,
            "text": f"{icon} {formatted_value}",
            "background_color": f"{color}20",  # 12% opacity
            "text_color": color,
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "padding_x": DesignTokens.SPACING["gaps"]["small"],
            "padding_y": DesignTokens.SPACING["gaps"]["tiny"],
            "border_radius": DesignTokens.LAYOUT["border_radius"]["small"],
            "is_positive": is_positive,
        }

    @staticmethod
    def category_tag(text: str, color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Category/topic tag.

        Args:
            text: Tag text
            color_scheme: Color scheme to use
        """
        background = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "badge",
            "variant": "category_tag",
            "text": text,
            "background_color": f"{background}20",  # 12% opacity
            "text_color": background,
            "font_size": DesignTokens.get_font_size("small"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "padding_x": DesignTokens.SPACING["gaps"]["small"],
            "padding_y": DesignTokens.SPACING["gaps"]["tiny"],
            "border_radius": DesignTokens.LAYOUT["border_radius"]["small"],
        }

    @staticmethod
    def icon_badge(
        icon: str, text: str = "", color: str = None, style: str = "filled"
    ) -> Dict[str, Any]:
        """
        Badge with icon (emoji or symbol).

        Args:
            icon: Icon/emoji character
            text: Optional text next to icon
            color: Badge color
            style: "filled" or "outlined"
        """
        if color is None:
            color = DesignTokens.COLORS["linkedin"]["blue"]

        if style == "filled":
            return {
                "type": "badge",
                "variant": "icon_filled",
                "icon": icon,
                "text": text,
                "background_color": color,
                "text_color": "#FFFFFF",
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
                "padding_x": DesignTokens.SPACING["gaps"]["small"],
                "padding_y": DesignTokens.SPACING["gaps"]["tiny"],
                "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            }
        else:  # outlined
            return {
                "type": "badge",
                "variant": "icon_outlined",
                "icon": icon,
                "text": text,
                "background_color": "transparent",
                "text_color": color,
                "border_color": color,
                "border_width": 2,
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
                "padding_x": DesignTokens.SPACING["gaps"]["small"],
                "padding_y": DesignTokens.SPACING["gaps"]["tiny"],
                "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            }

    @staticmethod
    def corner_ribbon(text: str, position: str = "top-right", color: str = None) -> Dict[str, Any]:
        """
        Corner ribbon (diagonal badge in corner).

        Args:
            text: Ribbon text
            position: "top-right", "top-left", "bottom-right", "bottom-left"
            color: Ribbon color
        """
        if color is None:
            color = DesignTokens.COLORS["semantic"]["warning"]

        return {
            "type": "badge",
            "variant": "corner_ribbon",
            "text": text,
            "position": position,
            "background_color": color,
            "text_color": "#FFFFFF",
            "font_size": DesignTokens.get_font_size("small"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
        }
