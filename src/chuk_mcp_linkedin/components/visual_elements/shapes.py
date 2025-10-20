"""
Shape and icon components for LinkedIn documents.

Geometric shapes and visual elements for decoration and emphasis.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any
from ...tokens.design_tokens import DesignTokens


class Shapes:
    """Geometric shapes and visual elements"""

    @staticmethod
    def circle(
        size: int = 100, color: str = None, fill: bool = True, stroke_width: int = 0
    ) -> Dict[str, Any]:
        """
        Circle shape.

        Args:
            size: Circle diameter
            color: Fill or stroke color
            fill: True for filled, False for outline
            stroke_width: Stroke width if not filled
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "accent")

        return {
            "type": "shape",
            "variant": "circle",
            "size": size,
            "color": color,
            "fill": fill,
            "stroke_width": stroke_width if not fill else 0,
        }

    @staticmethod
    def rectangle(
        width: int = 200,
        height: int = 100,
        color: str = None,
        fill: bool = True,
        radius: str = "none",
    ) -> Dict[str, Any]:
        """
        Rectangle shape.

        Args:
            width: Rectangle width
            height: Rectangle height
            color: Fill color
            fill: True for filled, False for outline
            radius: Border radius size name
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "primary")

        border_radius = DesignTokens.LAYOUT["border_radius"].get(radius, 0)

        return {
            "type": "shape",
            "variant": "rectangle",
            "width": width,
            "height": height,
            "color": color,
            "fill": fill,
            "border_radius": border_radius,
        }

    @staticmethod
    def icon_container(
        icon: str,
        size: int = 120,
        background_color: str = None,
        icon_color: str = "#FFFFFF",
        shape: str = "circle",
    ) -> Dict[str, Any]:
        """
        Icon with background container.

        Args:
            icon: Icon character (emoji or symbol)
            size: Container size
            background_color: Background color
            icon_color: Icon color
            shape: "circle", "square", "rounded"
        """
        if background_color is None:
            background_color = DesignTokens.COLORS["linkedin"]["blue"]

        radius_map = {
            "circle": DesignTokens.LAYOUT["border_radius"]["round"],
            "square": 0,
            "rounded": DesignTokens.LAYOUT["border_radius"]["large"],
        }

        return {
            "type": "shape",
            "variant": "icon_container",
            "icon": icon,
            "size": size,
            "background_color": background_color,
            "icon_color": icon_color,
            "icon_size": int(size * 0.5),  # Icon is 50% of container
            "border_radius": radius_map.get(shape, 0),
        }

    @staticmethod
    def arrow(
        direction: str = "right", size: int = 60, color: str = None, style: str = "solid"
    ) -> Dict[str, Any]:
        """
        Arrow shape.

        Args:
            direction: "up", "down", "left", "right"
            size: Arrow size
            color: Arrow color
            style: "solid", "outline", "simple"
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "accent")

        # Arrow symbols by direction
        symbols = {"up": "↑", "down": "↓", "left": "←", "right": "→"}

        return {
            "type": "shape",
            "variant": "arrow",
            "direction": direction,
            "symbol": symbols.get(direction, "→"),
            "size": size,
            "color": color,
            "style": style,
        }

    @staticmethod
    def checkmark(size: int = 40, color: str = None, style: str = "circle") -> Dict[str, Any]:
        """
        Checkmark icon.

        Args:
            size: Checkmark size
            color: Checkmark color (defaults to success green)
            style: "circle", "square", "simple"
        """
        if color is None:
            color = DesignTokens.COLORS["semantic"]["success"]

        return {
            "type": "shape",
            "variant": "checkmark",
            "symbol": "✓",
            "size": size,
            "color": color,
            "style": style,
            "background": style in ["circle", "square"],
            "border_radius": (
                DesignTokens.LAYOUT["border_radius"]["round"]
                if style == "circle"
                else DesignTokens.LAYOUT["border_radius"]["small"]
            ),
        }

    @staticmethod
    def bullet_point(style: str = "disc", size: int = 12, color: str = None) -> Dict[str, Any]:
        """
        Bullet point marker.

        Args:
            style: "disc", "circle", "square", "arrow", "checkmark", "star"
            size: Bullet size
            color: Bullet color
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "primary")

        symbols = {
            "disc": "•",
            "circle": "○",
            "square": "■",
            "arrow": "→",
            "checkmark": "✓",
            "star": "★",
        }

        return {
            "type": "shape",
            "variant": "bullet_point",
            "style": style,
            "symbol": symbols.get(style, "•"),
            "size": size,
            "color": color,
        }

    @staticmethod
    def decorative_element(
        element: str = "dots", color: str = None, opacity: float = 0.3
    ) -> Dict[str, Any]:
        """
        Decorative shape element.

        Args:
            element: "dots", "circles", "squares", "lines", "abstract"
            color: Element color
            opacity: Element opacity
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "accent")

        return {
            "type": "shape",
            "variant": "decorative",
            "element": element,
            "color": color,
            "opacity": opacity,
        }

    @staticmethod
    def progress_ring(
        percentage: float,
        size: int = 120,
        stroke_width: int = 12,
        color: str = None,
        background_color: str = None,
    ) -> Dict[str, Any]:
        """
        Circular progress ring.

        Args:
            percentage: Progress percentage (0-100)
            size: Ring diameter
            stroke_width: Ring thickness
            color: Progress color
            background_color: Background ring color
        """
        if color is None:
            color = DesignTokens.COLORS["linkedin"]["blue"]
        if background_color is None:
            background_color = DesignTokens.get_color("minimal", "secondary")

        return {
            "type": "shape",
            "variant": "progress_ring",
            "percentage": min(100, max(0, percentage)),
            "size": size,
            "stroke_width": stroke_width,
            "progress_color": color,
            "background_color": background_color,
        }

    @staticmethod
    def divider_ornament(
        ornament: str = "diamond", size: int = 24, color: str = None
    ) -> Dict[str, Any]:
        """
        Ornamental shape for dividers.

        Args:
            ornament: "diamond", "star", "dot", "square"
            size: Ornament size
            color: Ornament color
        """
        if color is None:
            color = DesignTokens.get_color("minimal", "accent")

        symbols = {"diamond": "◆", "star": "★", "dot": "●", "square": "■"}

        return {
            "type": "shape",
            "variant": "divider_ornament",
            "ornament": ornament,
            "symbol": symbols.get(ornament, "◆"),
            "size": size,
            "color": color,
        }
