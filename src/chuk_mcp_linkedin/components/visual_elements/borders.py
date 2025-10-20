"""
Border and frame components for LinkedIn documents.

Visual containers to emphasize and organize content.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any
from ...tokens.design_tokens import DesignTokens


class Borders:
    """Border and frame components for LinkedIn documents"""

    @staticmethod
    def simple_border(
        width: int = 2, color: str = None, style: str = "solid", radius: str = "medium"
    ) -> Dict[str, Any]:
        """
        Simple border around content.

        Args:
            width: Border width in pixels
            color: Border color (defaults to secondary)
            style: "solid", "dashed", "dotted"
            radius: Border radius size name
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "secondary")

        border_radius = DesignTokens.LAYOUT["border_radius"].get(radius, 8)

        return {
            "type": "border",
            "variant": "simple",
            "width": width,
            "color": color,
            "style": style,
            "radius": border_radius,
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def accent_border(side: str = "left", width: int = 6, color: str = None) -> Dict[str, Any]:
        """
        Accent border on one side (LinkedIn style).

        Args:
            side: "left", "right", "top", "bottom"
            width: Border width
            color: Border color (defaults to LinkedIn blue)
        """
        if color is None:
            color = DesignTokens.COLORS["linkedin"]["blue"]

        return {
            "type": "border",
            "variant": "accent",
            "side": side,
            "width": width,
            "color": color,
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def double_border(
        outer_width: int = 2, inner_width: int = 1, gap: int = 4, color: str = None
    ) -> Dict[str, Any]:
        """
        Double border (elegant).

        Args:
            outer_width: Outer border width
            inner_width: Inner border width
            gap: Space between borders
            color: Border color
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "primary")

        return {
            "type": "border",
            "variant": "double",
            "outer_width": outer_width,
            "inner_width": inner_width,
            "gap": gap,
            "color": color,
            "radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def gradient_border(
        width: int = 3, colors: list = None, direction: str = "diagonal"
    ) -> Dict[str, Any]:
        """
        Gradient border (modern).

        Args:
            width: Border width
            colors: List of gradient colors
            direction: "horizontal", "vertical", "diagonal"
        """
        if colors is None:
            colors = [
                DesignTokens.COLORS["linkedin"]["blue"],
                DesignTokens.COLORS["linkedin"]["light_blue"],
            ]

        return {
            "type": "border",
            "variant": "gradient",
            "width": width,
            "colors": colors,
            "direction": direction,
            "radius": DesignTokens.LAYOUT["border_radius"]["large"],
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def corner_brackets(size: int = 40, width: int = 3, color: str = None) -> Dict[str, Any]:
        """
        Corner brackets (frame corners only).

        Args:
            size: Bracket size (length)
            width: Bracket thickness
            color: Bracket color
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "accent")

        return {
            "type": "border",
            "variant": "corner_brackets",
            "size": size,
            "width": width,
            "color": color,
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def callout_box(
        border_color: str = None, background_color: str = None, style: str = "info"
    ) -> Dict[str, Any]:
        """
        Callout box with semantic styling.

        Args:
            border_color: Border color (overrides style)
            background_color: Background color (overrides style)
            style: "info", "success", "warning", "error"
        """
        # Semantic color mapping
        semantic_colors = {
            "info": {
                "border": DesignTokens.COLORS["semantic"]["info"],
                "background": DesignTokens.COLORS["semantic"]["info_light"],
            },
            "success": {
                "border": DesignTokens.COLORS["semantic"]["success"],
                "background": DesignTokens.COLORS["semantic"]["success_light"],
            },
            "warning": {
                "border": DesignTokens.COLORS["semantic"]["warning"],
                "background": DesignTokens.COLORS["semantic"]["warning_light"],
            },
            "error": {
                "border": DesignTokens.COLORS["semantic"]["error"],
                "background": DesignTokens.COLORS["semantic"]["error_light"],
            },
        }

        colors = semantic_colors.get(style, semantic_colors["info"])

        if border_color is None:
            border_color = colors["border"]
        if background_color is None:
            background_color = colors["background"]

        return {
            "type": "border",
            "variant": "callout",
            "border_width": 2,
            "border_color": border_color,
            "background_color": background_color,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            "padding": DesignTokens.get_spacing("padding", "normal"),
            "style": style,
        }

    @staticmethod
    def shadow_frame(elevation: str = "md", border_width: int = 0) -> Dict[str, Any]:
        """
        Frame with drop shadow (no/minimal border).

        Args:
            elevation: Shadow elevation ("sm", "md", "lg", "xl")
            border_width: Optional border width
        """
        shadow = DesignTokens.VISUAL["shadow"].get(elevation, "md")

        return {
            "type": "border",
            "variant": "shadow_frame",
            "shadow": shadow,
            "border_width": border_width,
            "border_color": (
                DesignTokens.get_color("minimal", "secondary") if border_width > 0 else None
            ),
            "border_radius": DesignTokens.LAYOUT["border_radius"]["large"],
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def inset_panel(depth: int = 2, color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Inset panel (appears sunken).

        Args:
            depth: Inset depth effect (1-5)
            color_scheme: Color scheme to use
        """
        background = DesignTokens.get_color(color_scheme, "background")

        return {
            "type": "border",
            "variant": "inset",
            "depth": depth,
            "background_color": background,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            "padding": DesignTokens.get_spacing("padding", "normal"),
            "inner_shadow": True,
        }
