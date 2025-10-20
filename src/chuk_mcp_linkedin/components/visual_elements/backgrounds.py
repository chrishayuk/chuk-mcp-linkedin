"""
Background components for LinkedIn documents.

Subtle patterns, gradients, and containers to enhance visual hierarchy.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any
from ...tokens.design_tokens import DesignTokens


class Backgrounds:
    """Background patterns and containers for LinkedIn documents"""

    @staticmethod
    def solid(color: str = None, color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Solid color background.

        Args:
            color: Background color (overrides color_scheme)
            color_scheme: Color scheme to use
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "background")

        return {
            "type": "background",
            "variant": "solid",
            "color": color,
        }

    @staticmethod
    def gradient(
        direction: str = "vertical", color_scheme: str = "minimal", opacity: float = 0.05
    ) -> Dict[str, Any]:
        """
        Subtle gradient background.

        Args:
            direction: "vertical", "horizontal", "diagonal"
            color_scheme: Color scheme to use
            opacity: Gradient opacity (0.0-1.0)
        """
        primary = DesignTokens.get_color(color_scheme, "primary")
        background = DesignTokens.get_color(color_scheme, "background")

        # Convert hex to rgba with opacity
        gradient_color = f"{primary}{int(opacity * 255):02x}"

        return {
            "type": "background",
            "variant": "gradient",
            "direction": direction,
            "start_color": background,
            "end_color": gradient_color,
        }

    @staticmethod
    def subtle_pattern(
        pattern: str = "dots", color_scheme: str = "minimal", opacity: float = 0.03
    ) -> Dict[str, Any]:
        """
        Subtle background pattern.

        Args:
            pattern: "dots", "grid", "diagonal_lines", "circles"
            color_scheme: Color scheme to use
            opacity: Pattern opacity (very subtle)
        """
        secondary = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "background",
            "variant": "pattern",
            "pattern": pattern,
            "color": secondary,
            "opacity": opacity,
            "size": "medium",  # Pattern size
        }

    @staticmethod
    def card_container(color_scheme: str = "minimal", elevation: str = "medium") -> Dict[str, Any]:
        """
        Card-style container background.

        Args:
            color_scheme: Color scheme to use
            elevation: "none", "sm", "md", "lg", "xl"
        """
        background = DesignTokens.get_color(color_scheme, "background")
        shadow = DesignTokens.VISUAL["shadow"].get(elevation, "md")

        return {
            "type": "background",
            "variant": "card",
            "color": background,
            "shadow": shadow,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def highlight_box(color: str = None, style: str = "subtle") -> Dict[str, Any]:
        """
        Highlighted content box.

        Args:
            color: Highlight color (defaults to LinkedIn blue)
            style: "subtle", "vibrant", "pastel"
        """
        if color is None:
            color = DesignTokens.COLORS["linkedin"]["blue"]

        # Opacity based on style
        opacity_map = {"subtle": 0.05, "vibrant": 0.15, "pastel": 0.10}
        opacity = opacity_map.get(style, 0.05)

        # Convert to rgba
        bg_color = f"{color}{int(opacity * 255):02x}"

        return {
            "type": "background",
            "variant": "highlight_box",
            "background_color": bg_color,
            "border_color": color,
            "border_width": 2,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
            "padding": DesignTokens.get_spacing("padding", "normal"),
        }

    @staticmethod
    def branded_header(color_scheme: str = "linkedin", height: int = 200) -> Dict[str, Any]:
        """
        Branded header background (top of slide).

        Args:
            color_scheme: "linkedin", "minimal", "vibrant"
            height: Header height
        """
        if color_scheme == "linkedin":
            color = DesignTokens.COLORS["linkedin"]["blue"]
        else:
            color = DesignTokens.get_color(color_scheme, "accent")

        return {
            "type": "background",
            "variant": "branded_header",
            "color": color,
            "height": height,
            "gradient": True,
            "gradient_direction": "vertical",
            "gradient_opacity": 0.8,
        }

    @staticmethod
    def split_background(
        left_color: str = None, right_color: str = None, split_position: float = 0.5
    ) -> Dict[str, Any]:
        """
        Two-tone split background (for comparison layouts).

        Args:
            left_color: Left side color (defaults to error_light)
            right_color: Right side color (defaults to success_light)
            split_position: Split position (0.0-1.0, default 0.5 = middle)
        """
        if left_color is None:
            left_color = DesignTokens.COLORS["semantic"]["error_light"]
        if right_color is None:
            right_color = DesignTokens.COLORS["semantic"]["success_light"]

        return {
            "type": "background",
            "variant": "split",
            "left_color": left_color,
            "right_color": right_color,
            "split_position": split_position,
        }

    @staticmethod
    def image_overlay(
        image_path: str, overlay_color: str = "#000000", overlay_opacity: float = 0.5
    ) -> Dict[str, Any]:
        """
        Image background with color overlay.

        Args:
            image_path: Path to background image
            overlay_color: Overlay color
            overlay_opacity: Overlay opacity (0.0-1.0)
        """
        return {
            "type": "background",
            "variant": "image_overlay",
            "image_path": image_path,
            "overlay_color": overlay_color,
            "overlay_opacity": overlay_opacity,
            "fit": "cover",
        }
