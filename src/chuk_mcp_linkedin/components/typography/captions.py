"""
Caption components for LinkedIn documents.

Small descriptive text for images, data sources, and footnotes.
Uses design tokens for consistent typography.
"""

from typing import Dict, Any, Optional
from ...tokens.design_tokens import DesignTokens


class Captions:
    """Caption components for LinkedIn documents"""

    @staticmethod
    def caption(text: str, style: str = "default", color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Standard caption text.

        Args:
            text: Caption text
            style: Caption style (default, muted, highlighted)
            color_scheme: Color scheme to use

        Returns:
            Caption component configuration
        """
        # Style-specific settings
        if style == "muted":
            color = DesignTokens.get_color(color_scheme, "secondary")
            font_weight = DesignTokens.TYPOGRAPHY["weights"]["normal"]
        elif style == "highlighted":
            color = DesignTokens.get_color(color_scheme, "accent")
            font_weight = DesignTokens.TYPOGRAPHY["weights"]["semibold"]
        else:  # default
            color = DesignTokens.get_color(color_scheme, "secondary")
            font_weight = DesignTokens.TYPOGRAPHY["weights"]["medium"]

        return {
            "type": "caption",
            "variant": "caption",
            "text": text,
            "font_size": DesignTokens.get_font_size("small"),  # 18pt (mobile-safe)
            "font_weight": font_weight,
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],  # 1.5
            "color": color,
            "align": "left",
            "style": style,
            "margin_top": DesignTokens.get_spacing("gaps", "tiny"),  # 8px
        }

    @staticmethod
    def image_caption(
        text: str, attribution: Optional[str] = None, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Image caption with optional attribution.

        Args:
            text: Caption text
            attribution: Optional attribution (e.g., "Photo by John Doe")
            color_scheme: Color scheme to use

        Returns:
            Image caption component configuration
        """
        caption_color = DesignTokens.get_color(color_scheme, "secondary")
        attribution_color = DesignTokens.get_color(color_scheme, "secondary")

        config = {
            "type": "caption",
            "variant": "image_caption",
            "text": text,
            "font_size": DesignTokens.get_font_size("small"),  # 18pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": caption_color,
            "align": "left",
            "margin_top": DesignTokens.get_spacing("gaps", "small"),  # 16px
        }

        if attribution:
            config["attribution"] = {
                "text": attribution,
                "font_size": DesignTokens.get_font_size("tiny"),  # 14pt
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
                "font_style": "italic",
                "color": attribution_color,
                "margin_top": DesignTokens.get_spacing("gaps", "tiny"),  # 8px
            }

        return config

    @staticmethod
    def data_source(text: str, color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Data source citation (for charts and tables).

        Args:
            text: Source citation text (e.g., "Source: Internal Analytics 2024")
            color_scheme: Color scheme to use

        Returns:
            Data source component configuration
        """
        color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "caption",
            "variant": "data_source",
            "text": text,
            "font_size": DesignTokens.get_font_size("small"),  # 18pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": color,
            "align": "left",
            "font_style": "italic",
            "margin_top": DesignTokens.get_spacing("gaps", "medium"),  # 24px
            "prefix": "Source: ",  # Optional prefix handling
        }

    @staticmethod
    def footnote(
        text: str, number: Optional[int] = None, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Footnote with optional number.

        Args:
            text: Footnote text
            number: Optional footnote number
            color_scheme: Color scheme to use

        Returns:
            Footnote component configuration
        """
        color = DesignTokens.get_color(color_scheme, "secondary")

        config = {
            "type": "caption",
            "variant": "footnote",
            "text": text,
            "font_size": DesignTokens.get_font_size("small"),  # 18pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": color,
            "align": "left",
            "margin_top": DesignTokens.get_spacing("gaps", "small"),
        }

        if number is not None:
            config["number"] = number
            config["number_style"] = {
                "font_size": DesignTokens.get_font_size("tiny"),  # 14pt
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
                "vertical_align": "super",
            }

        return config

    @staticmethod
    def metadata(
        text: str, icon: Optional[str] = None, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Metadata caption (e.g., date, author, category).

        Args:
            text: Metadata text
            icon: Optional icon/emoji before text
            color_scheme: Color scheme to use

        Returns:
            Metadata component configuration
        """
        color = DesignTokens.get_color(color_scheme, "secondary")

        config = {
            "type": "caption",
            "variant": "metadata",
            "text": text,
            "font_size": DesignTokens.get_font_size("small"),  # 18pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": color,
            "align": "left",
        }

        if icon:
            config["icon"] = {
                "symbol": icon,
                "size": DesignTokens.get_font_size("small"),
                "margin_right": DesignTokens.get_spacing("gaps", "tiny"),  # 8px
            }

        return config

    @staticmethod
    def legal(text: str, color_scheme: str = "minimal") -> Dict[str, Any]:
        """
        Legal/disclaimer text (very small).

        Args:
            text: Legal text
            color_scheme: Color scheme to use

        Returns:
            Legal text component configuration
        """
        color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "caption",
            "variant": "legal",
            "text": text,
            "font_size": DesignTokens.get_font_size("tiny"),  # 14pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["normal"],
            "color": color,
            "align": "left",
            "opacity": 0.7,  # Slightly faded
            "margin_top": DesignTokens.get_spacing("gaps", "large"),
        }
