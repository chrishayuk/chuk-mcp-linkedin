"""
Body text components for LinkedIn documents.

Paragraph text with proper line height and spacing for readability.
Uses design tokens for consistent typography.
"""

from typing import Dict, Any
from ...tokens.design_tokens import DesignTokens


class BodyText:
    """Body text components for LinkedIn documents"""

    @staticmethod
    def paragraph(
        text: str,
        size: str = "body",
        line_height: str = "relaxed",
        color_scheme: str = "minimal",
        color: str = None,
        align: str = "left",
    ) -> Dict[str, Any]:
        """
        Standard paragraph text.

        Args:
            text: Paragraph text
            size: Font size (small, body, large)
            line_height: Line height (tight, normal, relaxed, loose)
            color_scheme: Color scheme to use
            color: Override color (defaults to primary)
            align: Text alignment (left, center, right, justify)

        Returns:
            Paragraph component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "body_text",
            "variant": "paragraph",
            "text": text,
            "font_size": DesignTokens.get_font_size(size),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"][line_height],
            "color": color,
            "align": align,
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),  # 24px
        }

    @staticmethod
    def lead_text(text: str, color_scheme: str = "minimal", color: str = None) -> Dict[str, Any]:
        """
        Lead paragraph text (larger intro paragraph).

        Args:
            text: Lead text
            color_scheme: Color scheme to use
            color: Override color (defaults to primary)

        Returns:
            Lead text component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "body_text",
            "variant": "lead",
            "text": text,
            "font_size": DesignTokens.get_font_size("large"),  # 32pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],  # 1.8
            "color": color,
            "align": "left",
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),  # 40px
        }

    @staticmethod
    def small_text(text: str, color_scheme: str = "minimal", color: str = None) -> Dict[str, Any]:
        """
        Small descriptive text.

        Args:
            text: Small text
            color_scheme: Color scheme to use
            color: Override color (defaults to secondary)

        Returns:
            Small text component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "body_text",
            "variant": "small",
            "text": text,
            "font_size": DesignTokens.get_font_size("small"),  # 18pt (mobile-safe)
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],  # 1.5
            "color": color,
            "align": "left",
            "margin_bottom": DesignTokens.get_spacing("gaps", "small"),  # 16px
        }

    @staticmethod
    def emphasized(
        text: str,
        style: str = "bold",
        color_scheme: str = "minimal",
        color: str = None,
    ) -> Dict[str, Any]:
        """
        Emphasized text (bold, italic, or both).

        Args:
            text: Text to emphasize
            style: Emphasis style (bold, italic, both)
            color_scheme: Color scheme to use
            color: Override color (defaults to primary)

        Returns:
            Emphasized text component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "primary")

        font_weight = DesignTokens.TYPOGRAPHY["weights"]["normal"]
        font_style = "normal"

        if style == "bold":
            font_weight = DesignTokens.TYPOGRAPHY["weights"]["bold"]
        elif style == "italic":
            font_style = "italic"
        elif style == "both":
            font_weight = DesignTokens.TYPOGRAPHY["weights"]["bold"]
            font_style = "italic"

        return {
            "type": "body_text",
            "variant": "emphasized",
            "text": text,
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": font_weight,
            "font_style": font_style,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": color,
            "display": "inline",  # Inline element
        }

    @staticmethod
    def highlighted(
        text: str, background_color: str = None, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Highlighted text with background color.

        Args:
            text: Text to highlight
            background_color: Background color (defaults to accent with opacity)
            color_scheme: Color scheme to use

        Returns:
            Highlighted text component configuration
        """
        if background_color is None:
            accent = DesignTokens.get_color(color_scheme, "accent")
            background_color = f"{accent}20"  # 12% opacity

        text_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "body_text",
            "variant": "highlighted",
            "text": text,
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": text_color,
            "background_color": background_color,
            "padding_x": DesignTokens.SPACING["gaps"]["tiny"],  # 8px
            "padding_y": 4,  # 4px
            "border_radius": DesignTokens.LAYOUT["border_radius"]["small"],
            "display": "inline",
        }

    @staticmethod
    def link(text: str, url: str = None, color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Link text with underline.

        Args:
            text: Link text
            url: URL (optional, for reference)
            color_scheme: Color scheme to use

        Returns:
            Link component configuration
        """
        link_color = DesignTokens.get_color(color_scheme, "accent")

        config = {
            "type": "body_text",
            "variant": "link",
            "text": text,
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": link_color,
            "text_decoration": "underline",
            "display": "inline",
        }

        if url:
            config["url"] = url

        return config

    @staticmethod
    def code(text: str, inline: bool = True) -> Dict[str, Any]:
        """
        Code text with monospace font.

        Args:
            text: Code text
            inline: If True, inline code; if False, code block

        Returns:
            Code component configuration
        """
        background_color = "#F3F4F6"  # Light gray background
        text_color = "#1F2937"  # Dark gray text

        config = {
            "type": "body_text",
            "variant": "code",
            "text": text,
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["mono"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": text_color,
            "background_color": background_color,
        }

        if inline:
            config["display"] = "inline"
            config["padding_x"] = 6
            config["padding_y"] = 3
            config["border_radius"] = DesignTokens.LAYOUT["border_radius"]["small"]
        else:
            config["display"] = "block"
            config["padding"] = DesignTokens.SPACING["padding"]["normal"]  # 40px
            config["border_radius"] = DesignTokens.LAYOUT["border_radius"]["medium"]
            config["margin_bottom"] = DesignTokens.get_spacing("gaps", "medium")

        return config
