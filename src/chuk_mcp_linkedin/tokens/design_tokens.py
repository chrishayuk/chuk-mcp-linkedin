# src/chuk_mcp_linkedin/tokens/design_tokens.py
"""
Design tokens for visual layouts (documents, carousels, images).

Centralized design system tokens for typography, colors, spacing,
and canvas sizes - similar to the PPTX design token system.
"""

from typing import Any, Dict, Tuple


class DesignTokens:
    """Design tokens for LinkedIn visual content"""

    # ==========================================
    # CANVAS SIZES
    # ==========================================
    CANVAS = {
        # Carousel/Image posts
        "square": (1080, 1080),  # Most common for carousels
        "portrait": (1080, 1350),  # Instagram-style portrait
        "landscape": (1200, 628),  # Less common but supported
        # Document posts (PDF slides)
        "document_square": (1920, 1920),  # Recommended for documents
        "document_portrait": (1080, 1920),  # Vertical PDF
        # Constraints
        "min_size": (400, 400),
        "max_size": (8192, 8192),
    }

    # ==========================================
    # TYPOGRAPHY
    # ==========================================
    TYPOGRAPHY = {
        # Font families (web-safe)
        "fonts": {
            "sans": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "serif": "Georgia, 'Times New Roman', serif",
            "mono": "'Courier New', Courier, monospace",
            "display": "'Inter', -apple-system, sans-serif",
        },
        # Font sizes (optimized for mobile readability)
        # Minimum 18pt for LinkedIn mobile viewing
        "sizes": {
            "tiny": 14,  # Use sparingly
            "small": 18,  # Minimum for mobile
            "body": 24,  # Standard content
            "large": 32,  # Subheadings
            "xlarge": 42,  # Section headers
            "title": 56,  # Slide titles
            "display": 72,  # Big headlines
            "hero": 120,  # Hero numbers/text
            "massive": 200,  # Big stat numbers
        },
        # Line heights
        "line_heights": {
            "tight": 1.2,
            "normal": 1.5,
            "relaxed": 1.8,
            "loose": 2.0,
        },
        # Font weights
        "weights": {
            "light": "300",
            "normal": "400",
            "medium": "500",
            "semibold": "600",
            "bold": "700",
            "black": "900",
        },
    }

    # ==========================================
    # COLORS
    # ==========================================
    COLORS = {
        # Color schemes
        "minimal": {
            "background": "#FFFFFF",
            "primary": "#000000",
            "secondary": "#666666",
            "accent": "#0A66C2",  # LinkedIn blue
        },
        "modern": {
            "background": "#F8F9FA",
            "primary": "#1A1A1A",
            "secondary": "#4A5568",
            "accent": "#3B82F6",
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444",
        },
        "vibrant": {
            "background": "#FFFFFF",
            "primary": "#000000",
            "secondary": "#4A5568",
            "accent": "#F59E0B",
            "success": "#10B981",
            "error": "#EF4444",
            "info": "#3B82F6",
        },
        "dark": {
            "background": "#1A1A1A",
            "primary": "#FFFFFF",
            "secondary": "#A0AEC0",
            "accent": "#60A5FA",
        },
        # LinkedIn brand colors
        "linkedin": {
            "blue": "#0A66C2",
            "dark_blue": "#004182",
            "light_blue": "#378FE9",
        },
        # Semantic colors
        "semantic": {
            "success": "#10B981",
            "error": "#EF4444",
            "warning": "#F59E0B",
            "info": "#3B82F6",
            "success_light": "#D1FAE5",
            "error_light": "#FEE2E2",
            "warning_light": "#FEF3C7",
            "info_light": "#DBEAFE",
        },
    }

    # ==========================================
    # SPACING
    # ==========================================
    SPACING = {
        # Safe areas / margins (in pixels)
        "safe_area": {
            "minimal": {"top": 40, "right": 40, "bottom": 40, "left": 40},
            "standard": {"top": 60, "right": 60, "bottom": 60, "left": 60},
            "comfortable": {"top": 100, "right": 100, "bottom": 100, "left": 100},
            "spacious": {"top": 150, "right": 150, "bottom": 150, "left": 150},
        },
        # Internal spacing
        "gaps": {
            "tiny": 8,
            "small": 16,
            "medium": 24,
            "large": 40,
            "xlarge": 60,
            "xxlarge": 80,
            "huge": 120,
        },
        # Padding
        "padding": {
            "tight": 20,
            "normal": 40,
            "loose": 60,
            "spacious": 80,
        },
    }

    # ==========================================
    # LAYOUT PROPERTIES
    # ==========================================
    LAYOUT = {
        # Alignment
        "align": {
            "horizontal": ["left", "center", "right"],
            "vertical": ["top", "middle", "bottom"],
        },
        # Border radius
        "border_radius": {
            "none": 0,
            "small": 4,
            "medium": 8,
            "large": 16,
            "xlarge": 24,
            "round": 9999,
        },
        # Grid configurations
        "grid": {
            "columns": {
                "single": 1,
                "two": 2,
                "three": 3,
                "four": 4,
            },
            "gaps": {
                "tight": 20,
                "normal": 40,
                "loose": 60,
                "spacious": 80,
            },
        },
        # Max content widths for readability
        "max_width": {
            "narrow": 600,
            "normal": 800,
            "wide": 1000,
            "full": 1720,  # For 1920px canvas with 100px margins
        },
    }

    # ==========================================
    # VISUAL ELEMENTS
    # ==========================================
    VISUAL = {
        # Icon sizes
        "icon_sizes": {
            "tiny": 24,
            "small": 32,
            "medium": 48,
            "large": 64,
            "xlarge": 96,
            "huge": 120,
        },
        # Image fit modes
        "image_fit": ["cover", "contain", "fill", "none"],
        # Opacity levels
        "opacity": {
            "transparent": 0,
            "faint": 0.1,
            "light": 0.3,
            "medium": 0.5,
            "heavy": 0.7,
            "strong": 0.9,
            "opaque": 1.0,
        },
        # Shadows
        "shadow": {
            "none": "none",
            "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
            "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
            "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
            "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
        },
    }

    # ==========================================
    # LINKEDIN-SPECIFIC
    # ==========================================
    LINKEDIN_SPECIFIC = {
        # Recommended slide counts for document posts
        "document_slides": {
            "min": 3,
            "optimal_min": 5,
            "optimal_max": 10,
            "max": 15,  # Beyond this, engagement drops
        },
        # Carousel recommendations
        "carousel_slides": {
            "min": 2,
            "optimal_max": 10,
            "max": 20,  # LinkedIn's technical limit
        },
        # Mobile-first design requirements
        "mobile": {
            "min_font_size": 18,  # Absolute minimum for readability
            "recommended_font_size": 24,  # Better for mobile
            "touch_target_min": 44,  # Minimum tap target size
        },
        # Performance optimizations
        "performance": {
            "max_file_size_mb": 10,  # LinkedIn's limit for documents
            "recommended_file_size_mb": 5,  # For faster loading
            "image_quality": 90,  # JPEG quality (0-100)
        },
    }

    # ==========================================
    # HELPER METHODS
    # ==========================================

    @staticmethod
    def get_canvas_size(format_type: str) -> Tuple[int, int]:
        """Get canvas size for a given format"""
        return DesignTokens.CANVAS.get(format_type, DesignTokens.CANVAS["square"])

    @staticmethod
    def get_font_size(size_name: str) -> int:
        """Get font size by name"""
        sizes: Dict[str, int] = DesignTokens.TYPOGRAPHY["sizes"]  # type: ignore[assignment]
        result: int = sizes.get(size_name, 24)
        return result

    @staticmethod
    def get_color(scheme: str, color_name: str) -> str:
        """Get color from a scheme"""
        result: str = DesignTokens.COLORS.get(scheme, {}).get(color_name, "#000000")
        return result

    @staticmethod
    def get_spacing(spacing_type: str, size_name: str) -> Any:
        """Get spacing value"""
        spacing_dict: Dict[str, Any] = DesignTokens.SPACING.get(spacing_type, {})  # type: ignore[assignment]
        result: Any = spacing_dict.get(size_name, 40)
        return result

    @staticmethod
    def get_safe_area(size: str = "standard") -> Dict[str, int]:
        """Get safe area margins"""
        safe_area_dict: Dict[str, Dict[str, int]] = DesignTokens.SPACING["safe_area"]  # type: ignore[assignment]
        result: Dict[str, int] = safe_area_dict.get(size, safe_area_dict["standard"])
        return result
