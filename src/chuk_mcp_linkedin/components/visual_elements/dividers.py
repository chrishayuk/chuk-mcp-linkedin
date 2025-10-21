# src/chuk_mcp_linkedin/components/visual_elements/dividers.py
"""
Divider components for LinkedIn documents.

Visual separators to create sections and improve scannability.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any
from ...tokens.design_tokens import DesignTokens


class Dividers:
    """Section dividers and separators for LinkedIn documents"""

    @staticmethod
    def horizontal_line(
        width: int = 1720, thickness: int = 2, color: str = None, style: str = "solid"
    ) -> Dict[str, Any]:
        """
        Simple horizontal line divider.

        Args:
            width: Line width in pixels
            thickness: Line thickness (1-10px)
            color: Line color (defaults to secondary)
            style: "solid", "dashed", "dotted"
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "secondary")

        return {
            "type": "divider",
            "variant": "horizontal_line",
            "width": width,
            "height": thickness,
            "color": color,
            "style": style,
            "margin_top": DesignTokens.get_spacing("gaps", "large"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),
        }

    @staticmethod
    def gradient_fade(
        width: int = 1720, height: int = 40, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Gradient fade divider (subtle).

        Args:
            width: Divider width
            height: Fade height
            color_scheme: Color scheme to use
        """
        primary = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "divider",
            "variant": "gradient_fade",
            "width": width,
            "height": height,
            "gradient": {
                "start": f"{primary}00",  # Transparent
                "mid": f"{primary}20",  # 12% opacity
                "end": f"{primary}00",  # Transparent
            },
            "margin_top": DesignTokens.get_spacing("gaps", "medium"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def decorative_accent(
        accent_color: str = None, width: int = 200, thickness: int = 4
    ) -> Dict[str, Any]:
        """
        Short decorative accent line (like LinkedIn brand style).

        Args:
            accent_color: Accent color (defaults to LinkedIn blue)
            width: Accent width (typically 100-300px)
            thickness: Accent thickness (3-8px)
        """
        if accent_color is None:
            accent_color = DesignTokens.COLORS["linkedin"]["blue"]

        return {
            "type": "divider",
            "variant": "decorative_accent",
            "width": width,
            "height": thickness,
            "color": accent_color,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["small"],
            "margin_top": DesignTokens.get_spacing("gaps", "small"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }

    @staticmethod
    def section_break(style: str = "dots", color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Section break with visual elements.

        Args:
            style: "dots", "squares", "diamond"
            color_scheme: Color scheme to use
        """
        secondary = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "divider",
            "variant": "section_break",
            "style": style,
            "color": secondary,
            "symbols": {"dots": "• • •", "squares": "■ ■ ■", "diamond": "◆"}.get(style, "• • •"),
            "font_size": DesignTokens.get_font_size("large"),
            "margin_top": DesignTokens.get_spacing("gaps", "xlarge"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "xlarge"),
            "align": "center",
        }

    @staticmethod
    def spacer(size: str = "medium") -> Dict[str, Any]:
        """
        Invisible spacer (no visual, just spacing).

        Args:
            size: "small", "medium", "large", "xlarge", "huge"
        """
        gap = DesignTokens.get_spacing("gaps", size)

        return {"type": "divider", "variant": "spacer", "height": gap, "visible": False}

    @staticmethod
    def title_underline(width: int = 1720, style: str = "double") -> Dict[str, Any]:
        """
        Underline for titles and headers.

        Args:
            width: Underline width
            style: "single", "double", "thick"
        """
        color = DesignTokens.get_color("minimal", "primary")

        styles = {
            "single": {"thickness": 1, "count": 1, "gap": 0},
            "double": {"thickness": 1, "count": 2, "gap": 4},
            "thick": {"thickness": 4, "count": 1, "gap": 0},
        }

        style_config = styles.get(style, styles["single"])

        return {
            "type": "divider",
            "variant": "title_underline",
            "width": width,
            "thickness": style_config["thickness"],
            "count": style_config["count"],
            "gap": style_config["gap"],
            "color": color,
            "margin_top": DesignTokens.get_spacing("gaps", "tiny"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }
