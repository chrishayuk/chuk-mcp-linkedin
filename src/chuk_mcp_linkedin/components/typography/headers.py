"""
Header components for LinkedIn documents.

Heading elements with token-based styling for consistent typography hierarchy.
Uses design tokens for font sizes, weights, and colors.
"""

from typing import Dict, Any
from ...tokens.design_tokens import DesignTokens


class Headers:
    """Header components for LinkedIn documents"""

    @staticmethod
    def h1(
        text: str, color_scheme: str = "minimal", align: str = "left", color: str = None
    ) -> Dict[str, Any]:
        """
        Main heading (H1) - Largest heading for titles.

        Args:
            text: Header text
            color_scheme: Color scheme to use (minimal, modern, vibrant, dark)
            align: Text alignment (left, center, right)
            color: Override color (defaults to primary from scheme)

        Returns:
            Header component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "header",
            "variant": "h1",
            "text": text,
            "font_size": DesignTokens.get_font_size("display"),  # 72pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["black"],  # 900
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["display"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["tight"],  # 1.2
            "color": color,
            "align": align,
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),  # 40px
        }

    @staticmethod
    def h2(
        text: str, color_scheme: str = "minimal", align: str = "left", color: str = None
    ) -> Dict[str, Any]:
        """
        Secondary heading (H2) - Section headers.

        Args:
            text: Header text
            color_scheme: Color scheme to use
            align: Text alignment (left, center, right)
            color: Override color (defaults to primary from scheme)

        Returns:
            Header component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "header",
            "variant": "h2",
            "text": text,
            "font_size": DesignTokens.get_font_size("title"),  # 56pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],  # 700
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["display"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["tight"],  # 1.2
            "color": color,
            "align": align,
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),  # 24px
        }

    @staticmethod
    def h3(
        text: str, color_scheme: str = "minimal", align: str = "left", color: str = None
    ) -> Dict[str, Any]:
        """
        Tertiary heading (H3) - Subsection headers.

        Args:
            text: Header text
            color_scheme: Color scheme to use
            align: Text alignment (left, center, right)
            color: Override color (defaults to primary from scheme)

        Returns:
            Header component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "header",
            "variant": "h3",
            "text": text,
            "font_size": DesignTokens.get_font_size("xlarge"),  # 42pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],  # 700
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],  # 1.5
            "color": color,
            "align": align,
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),  # 24px
        }

    @staticmethod
    def h4(
        text: str, color_scheme: str = "minimal", align: str = "left", color: str = None
    ) -> Dict[str, Any]:
        """
        Quaternary heading (H4) - Minor section headers.

        Args:
            text: Header text
            color_scheme: Color scheme to use
            align: Text alignment (left, center, right)
            color: Override color (defaults to primary from scheme)

        Returns:
            Header component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "header",
            "variant": "h4",
            "text": text,
            "font_size": DesignTokens.get_font_size("large"),  # 32pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],  # 600
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],  # 1.5
            "color": color,
            "align": align,
            "margin_bottom": DesignTokens.get_spacing("gaps", "small"),  # 16px
        }

    @staticmethod
    def section_header(
        text: str,
        with_divider: bool = True,
        divider_style: str = "decorative_accent",
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Section header with optional decorative divider.

        Args:
            text: Header text
            with_divider: Include decorative divider below
            divider_style: Type of divider (decorative_accent, title_underline, horizontal_line)
            color_scheme: Color scheme to use

        Returns:
            Section header configuration with optional divider
        """
        color = DesignTokens.get_color(color_scheme, "primary")
        accent_color = DesignTokens.get_color(color_scheme, "accent")

        config = {
            "type": "header",
            "variant": "section_header",
            "text": text,
            "font_size": DesignTokens.get_font_size("xlarge"),  # 42pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["tight"],
            "color": color,
            "align": "left",
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }

        if with_divider:
            config["divider"] = {
                "style": divider_style,
                "color": accent_color,
                "margin_top": DesignTokens.get_spacing("gaps", "tiny"),
            }

        return config

    @staticmethod
    def eyebrow(
        text: str, color_scheme: str = "minimal", transform: str = "uppercase"
    ) -> Dict[str, Any]:
        """
        Eyebrow text (small text above main heading).

        Args:
            text: Eyebrow text
            color_scheme: Color scheme to use
            transform: Text transform (uppercase, lowercase, capitalize, none)

        Returns:
            Eyebrow component configuration
        """
        color = DesignTokens.get_color(color_scheme, "accent")

        return {
            "type": "header",
            "variant": "eyebrow",
            "text": text,
            "font_size": DesignTokens.get_font_size("small"),  # 18pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": color,
            "align": "left",
            "text_transform": transform,
            "letter_spacing": 1.5,  # 1.5px tracking for uppercase
            "margin_bottom": DesignTokens.get_spacing("gaps", "tiny"),  # 8px
        }

    @staticmethod
    def slide_title(
        text: str, subtitle: str = None, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Slide title with optional subtitle (for document layouts).

        Args:
            text: Main title text
            subtitle: Optional subtitle text
            color_scheme: Color scheme to use

        Returns:
            Slide title configuration
        """
        primary_color = DesignTokens.get_color(color_scheme, "primary")
        secondary_color = DesignTokens.get_color(color_scheme, "secondary")

        config = {
            "type": "header",
            "variant": "slide_title",
            "text": text,
            "font_size": DesignTokens.get_font_size("title"),  # 56pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["display"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["tight"],
            "color": primary_color,
            "align": "left",
            "margin_bottom": DesignTokens.get_spacing("gaps", "medium"),
        }

        if subtitle:
            config["subtitle"] = {
                "text": subtitle,
                "font_size": DesignTokens.get_font_size("large"),  # 32pt
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
                "color": secondary_color,
                "margin_top": DesignTokens.get_spacing("gaps", "small"),
            }

        return config
