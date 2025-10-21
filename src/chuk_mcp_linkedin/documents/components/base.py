"""
Base component class for all LinkedIn document components.

Document components render to visual formats (HTML, PDF, PowerPoint).
Uses DesignTokens and LinkedInTheme for consistent styling.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from dataclasses import dataclass, field

from ...tokens.design_tokens import DesignTokens
from ...themes.theme_manager import LinkedInTheme


@dataclass
class RenderContext:
    """
    Context for rendering document components.

    Uses DesignTokens for all visual properties - NO hardcoded values.
    """

    # Canvas configuration
    canvas_size: str = "document_square"  # Key from DesignTokens.CANVAS
    theme: Optional[LinkedInTheme] = None
    color_scheme: str = "minimal"  # Key from DesignTokens.COLORS

    # Layout context
    layout: Optional[Any] = None
    slide_index: int = 0
    format: str = "html"  # html, pdf, pptx

    # Positioning context (set dynamically)
    current_x: int = 0
    current_y: int = 0
    available_width: int = field(default=0)
    available_height: int = field(default=0)

    def __post_init__(self):
        """Initialize computed properties from design tokens"""
        # Get canvas dimensions from tokens
        width, height = DesignTokens.get_canvas_size(self.canvas_size)

        # Set available dimensions if not already set
        if self.available_width == 0:
            self.available_width = width
        if self.available_height == 0:
            self.available_height = height

    @property
    def canvas_width(self) -> int:
        """Get canvas width from design tokens"""
        return DesignTokens.get_canvas_size(self.canvas_size)[0]

    @property
    def canvas_height(self) -> int:
        """Get canvas height from design tokens"""
        return DesignTokens.get_canvas_size(self.canvas_size)[1]

    @property
    def font_family(self) -> str:
        """Get font family from design tokens"""
        return DesignTokens.TYPOGRAPHY["fonts"]["sans"]

    @property
    def primary_color(self) -> str:
        """Get primary color from design tokens"""
        return DesignTokens.get_color(self.color_scheme, "primary")

    @property
    def secondary_color(self) -> str:
        """Get secondary color from design tokens"""
        return DesignTokens.get_color(self.color_scheme, "secondary")

    @property
    def accent_color(self) -> str:
        """Get accent color from design tokens"""
        return DesignTokens.get_color(self.color_scheme, "accent")

    @property
    def background_color(self) -> str:
        """Get background color from design tokens"""
        return DesignTokens.get_color(self.color_scheme, "background")

    def get_font_size(self, size_name: str) -> int:
        """Get font size from design tokens"""
        return DesignTokens.get_font_size(size_name)

    def get_spacing(self, spacing_type: str, size_name: str) -> Any:
        """Get spacing from design tokens"""
        return DesignTokens.get_spacing(spacing_type, size_name)

    def get_safe_area(self, size: str = "comfortable") -> Dict[str, int]:
        """Get safe area margins from design tokens"""
        return DesignTokens.get_safe_area(size)


class DocumentComponent(ABC):
    """
    Base class for all document components.

    Similar to PostComponent but renders to visual formats.
    """

    @abstractmethod
    def render(self, context: RenderContext) -> str:
        """
        Render component to output format.

        Returns HTML by default, can be adapted for PDF/PPTX.

        Args:
            context: RenderContext with design tokens and theme

        Returns:
            HTML string for the component
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate component configuration"""
        pass

    def get_dimensions(self, context: RenderContext) -> Dict[str, int]:
        """
        Get required dimensions for this component.

        Returns dict with width, height keys.
        """
        return {
            "width": context.available_width,
            "height": 100,  # Default height
        }

    def to_dict(self) -> Dict[str, Any]:
        """Export component as dictionary"""
        return {
            "type": self.__class__.__name__,
            "valid": self.validate(),
        }
