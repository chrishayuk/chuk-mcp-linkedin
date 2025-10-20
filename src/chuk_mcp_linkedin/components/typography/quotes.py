"""
Quote components for LinkedIn documents.

Pull quotes, blockquotes, and testimonials with proper formatting.
Uses design tokens for consistent typography.
"""

from typing import Dict, Any, Optional
from ...tokens.design_tokens import DesignTokens


class Quotes:
    """Quote components for LinkedIn documents"""

    @staticmethod
    def pull_quote(
        text: str,
        author: Optional[str] = None,
        style: str = "minimal",
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Pull quote (large emphasized quote).

        Args:
            text: Quote text
            author: Optional author attribution
            style: Quote style (minimal, accent, boxed)
            color_scheme: Color scheme to use

        Returns:
            Pull quote component configuration
        """
        quote_color = DesignTokens.get_color(color_scheme, "primary")
        accent_color = DesignTokens.get_color(color_scheme, "accent")
        author_color = DesignTokens.get_color(color_scheme, "secondary")

        config = {
            "type": "quote",
            "variant": "pull_quote",
            "text": text,
            "font_size": DesignTokens.get_font_size("xlarge"),  # 42pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["serif"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],  # 1.8
            "color": quote_color,
            "font_style": "italic",
            "align": "center",
            "margin_top": DesignTokens.get_spacing("gaps", "xlarge"),  # 60px
            "margin_bottom": DesignTokens.get_spacing("gaps", "xlarge"),
            "style": style,
        }

        # Style-specific decorations
        if style == "accent":
            config["border_left"] = {
                "width": 4,
                "color": accent_color,
                "padding_left": DesignTokens.get_spacing("gaps", "medium"),
            }
            config["align"] = "left"
        elif style == "boxed":
            config["background_color"] = f"{accent_color}10"  # 6% opacity
            config["padding"] = DesignTokens.SPACING["padding"]["loose"]  # 60px
            config["border_radius"] = DesignTokens.LAYOUT["border_radius"]["medium"]

        # Add author attribution if provided
        if author:
            config["author"] = {
                "text": author,
                "font_size": DesignTokens.get_font_size("body"),  # 24pt
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
                "font_style": "normal",
                "color": author_color,
                "margin_top": DesignTokens.get_spacing("gaps", "medium"),
                "prefix": "— ",  # Em dash before author
            }

        return config

    @staticmethod
    def blockquote(
        text: str,
        author: Optional[str] = None,
        with_border: bool = True,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Blockquote (standard indented quote).

        Args:
            text: Quote text
            author: Optional author attribution
            with_border: Include left border accent
            color_scheme: Color scheme to use

        Returns:
            Blockquote component configuration
        """
        quote_color = DesignTokens.get_color(color_scheme, "primary")
        border_color = DesignTokens.get_color(color_scheme, "accent")
        author_color = DesignTokens.get_color(color_scheme, "secondary")

        config = {
            "type": "quote",
            "variant": "blockquote",
            "text": text,
            "font_size": DesignTokens.get_font_size("large"),  # 32pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["serif"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],  # 1.8
            "color": quote_color,
            "font_style": "italic",
            "align": "left",
            "margin_top": DesignTokens.get_spacing("gaps", "large"),  # 40px
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),
            "margin_left": DesignTokens.get_spacing("gaps", "xlarge"),  # 60px (indent)
        }

        if with_border:
            config["border_left"] = {
                "width": 4,
                "color": border_color,
                "padding_left": DesignTokens.get_spacing("gaps", "medium"),  # 24px
            }

        if author:
            config["author"] = {
                "text": author,
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
                "font_style": "normal",
                "color": author_color,
                "margin_top": DesignTokens.get_spacing("gaps", "small"),
                "prefix": "— ",
            }

        return config

    @staticmethod
    def testimonial(
        text: str,
        author: str,
        role: Optional[str] = None,
        company: Optional[str] = None,
        avatar: Optional[str] = None,
        rating: Optional[float] = None,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Testimonial quote with author details.

        Args:
            text: Testimonial text
            author: Author name
            role: Author role/title
            company: Author company
            avatar: Optional avatar image URL
            rating: Optional rating (0-5)
            color_scheme: Color scheme to use

        Returns:
            Testimonial component configuration
        """
        quote_color = DesignTokens.get_color(color_scheme, "primary")
        author_color = DesignTokens.get_color(color_scheme, "primary")
        role_color = DesignTokens.get_color(color_scheme, "secondary")
        accent_color = DesignTokens.get_color(color_scheme, "accent")

        config = {
            "type": "quote",
            "variant": "testimonial",
            "text": text,
            "font_size": DesignTokens.get_font_size("large"),  # 32pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
            "color": quote_color,
            "align": "left",
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),
            "author": {
                "name": author,
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
                "color": author_color,
            },
        }

        # Add role and company if provided
        if role or company:
            role_parts = []
            if role:
                role_parts.append(role)
            if company:
                role_parts.append(company)

            config["author"]["role"] = {
                "text": ", ".join(role_parts),
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
                "color": role_color,
            }

        # Add avatar if provided
        if avatar:
            config["author"]["avatar"] = {
                "src": avatar,
                "size": DesignTokens.VISUAL["icon_sizes"]["medium"],  # 48px
                "border_radius": DesignTokens.LAYOUT["border_radius"]["round"],
            }

        # Add rating if provided
        if rating is not None:
            config["rating"] = {
                "value": rating,
                "max": 5.0,
                "color": accent_color,
                "symbol": "★",
                "size": DesignTokens.get_font_size("body"),
                "margin_bottom": DesignTokens.get_spacing("gaps", "small"),
            }

        return config

    @staticmethod
    def quote_with_marks(
        text: str,
        author: Optional[str] = None,
        color_scheme: str = "minimal",
        marks_style: str = "modern",
    ) -> Dict[str, Any]:
        """
        Quote with decorative quotation marks.

        Args:
            text: Quote text
            author: Optional author attribution
            color_scheme: Color scheme to use
            marks_style: Quotation mark style (modern, traditional, minimal)

        Returns:
            Quote with marks component configuration
        """
        quote_color = DesignTokens.get_color(color_scheme, "primary")
        marks_color = DesignTokens.get_color(color_scheme, "accent")
        author_color = DesignTokens.get_color(color_scheme, "secondary")

        # Different quotation mark styles
        marks = {
            "modern": {"open": """, "close": """},
            "traditional": {"open": '"', "close": '"'},
            "minimal": {"open": "'", "close": "'"},
        }

        selected_marks = marks.get(marks_style, marks["modern"])

        config = {
            "type": "quote",
            "variant": "quote_with_marks",
            "text": text,
            "font_size": DesignTokens.get_font_size("large"),  # 32pt
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["normal"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "line_height": DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
            "color": quote_color,
            "align": "center",
            "margin_top": DesignTokens.get_spacing("gaps", "large"),
            "margin_bottom": DesignTokens.get_spacing("gaps", "large"),
            "quotation_marks": {
                "open": selected_marks["open"],
                "close": selected_marks["close"],
                "font_size": DesignTokens.get_font_size("hero"),  # 120pt
                "color": marks_color,
                "opacity": 0.2,
            },
        }

        if author:
            config["author"] = {
                "text": author,
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
                "color": author_color,
                "margin_top": DesignTokens.get_spacing("gaps", "medium"),
                "prefix": "— ",
            }

        return config
