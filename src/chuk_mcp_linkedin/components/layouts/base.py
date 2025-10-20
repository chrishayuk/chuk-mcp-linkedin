"""
Base classes for layout system.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, Optional, Any, List


class LayoutType(Enum):
    """Types of layouts available"""

    # Document layouts (for PDF slides)
    TITLE_SLIDE = "title_slide"
    CONTENT_SLIDE = "content_slide"
    SPLIT_CONTENT = "split_content"
    BIG_NUMBER = "big_number"
    QUOTE = "quote"
    COMPARISON = "comparison"
    TWO_COLUMN = "two_column"
    THREE_COLUMN = "three_column"
    CHECKLIST = "checklist"
    TIMELINE = "timeline"
    ICON_GRID = "icon_grid"
    DATA_VISUAL = "data_visual"

    # Carousel layouts (for image posts)
    MINIMAL_TEXT = "minimal_text"
    STANDARD = "standard"
    GRID_4 = "grid_4"
    GRID_6 = "grid_6"
    LIST_STYLE = "list_style"
    NUMBERED = "numbered"
    QUOTE_STYLE = "quote_style"
    BEFORE_AFTER = "before_after"
    STAT_FOCUS = "stat_focus"


@dataclass
class LayoutZone:
    """
    Defines a rectangular zone in a layout.
    All coordinates in pixels.
    """

    x: int
    y: int
    width: int
    height: int
    align: str = "left"  # left, center, right
    valign: str = "top"  # top, middle, bottom

    # Typography
    font_size: Optional[int] = None
    font_weight: Optional[str] = None  # normal, bold, black
    font_family: Optional[str] = None
    line_height: Optional[float] = None
    color: Optional[str] = None

    # Constraints
    max_lines: Optional[int] = None
    truncate: bool = False

    # Special properties
    properties: Dict[str, Any] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


@dataclass
class LayoutConfig:
    """Complete layout configuration"""

    name: str
    type: LayoutType
    description: str

    # Canvas
    canvas_size: Tuple[int, int]  # (width, height) in pixels
    background_color: str = "#FFFFFF"

    # Margins/padding
    safe_area: Dict[str, int] = None  # {top, right, bottom, left}

    # Zones
    title_zone: Optional[LayoutZone] = None
    subtitle_zone: Optional[LayoutZone] = None
    content_zone: Optional[LayoutZone] = None
    content_zone_2: Optional[LayoutZone] = None  # For multi-column
    content_zone_3: Optional[LayoutZone] = None  # For three-column
    image_zone: Optional[LayoutZone] = None
    image_zone_2: Optional[LayoutZone] = None  # For comparisons
    branding_zone: Optional[LayoutZone] = None
    footer_zone: Optional[LayoutZone] = None

    # Additional zones for complex layouts
    custom_zones: Dict[str, LayoutZone] = None

    # Metadata
    best_for: List[str] = None
    use_cases: List[str] = None
    mobile_optimized: bool = True

    def __post_init__(self):
        if self.safe_area is None:
            self.safe_area = {"top": 60, "right": 60, "bottom": 60, "left": 60}
        if self.custom_zones is None:
            self.custom_zones = {}
        if self.best_for is None:
            self.best_for = []
        if self.use_cases is None:
            self.use_cases = []


class CanvasSize:
    """Standard canvas sizes for LinkedIn content"""

    # Carousel/Image posts
    SQUARE = (1080, 1080)  # Most common for carousels
    PORTRAIT = (1080, 1350)  # Instagram-style portrait
    LANDSCAPE = (1200, 628)  # Less common but supported

    # Document posts (PDF slides)
    DOCUMENT_SQUARE = (1920, 1920)  # Recommended for documents
    DOCUMENT_PORTRAIT = (1080, 1920)  # Vertical PDF

    # Safe sizes (within LinkedIn's constraints)
    MIN_SIZE = (400, 400)
    MAX_SIZE = (8192, 8192)


class ColorScheme:
    """Common color schemes for LinkedIn posts"""

    # Professional
    MINIMAL = {
        "background": "#FFFFFF",
        "primary": "#000000",
        "secondary": "#666666",
        "accent": "#0A66C2",  # LinkedIn blue
    }

    # Modern
    MODERN = {
        "background": "#F8F9FA",
        "primary": "#1A1A1A",
        "secondary": "#4A5568",
        "accent": "#3B82F6",
    }

    # Vibrant
    VIBRANT = {
        "background": "#FFFFFF",
        "primary": "#000000",
        "secondary": "#4A5568",
        "accent": "#F59E0B",
        "success": "#10B981",
        "error": "#EF4444",
    }

    # Dark
    DARK = {
        "background": "#1A1A1A",
        "primary": "#FFFFFF",
        "secondary": "#A0AEC0",
        "accent": "#60A5FA",
    }

    # LinkedIn brand
    LINKEDIN = {
        "background": "#FFFFFF",
        "primary": "#000000",
        "secondary": "#666666",
        "accent": "#0A66C2",
        "linkedin_blue": "#0A66C2",
        "linkedin_dark": "#004182",
    }


class Typography:
    """Typography settings for layouts"""

    # Font families (web-safe for maximum compatibility)
    FONTS = {
        "sans": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "serif": "Georgia, 'Times New Roman', serif",
        "mono": "'Courier New', Courier, monospace",
        "display": "'Inter', -apple-system, sans-serif",
    }

    # Font sizes (optimized for mobile readability)
    SIZES = {
        "tiny": 14,
        "small": 18,  # Minimum for mobile
        "body": 24,
        "large": 32,
        "xlarge": 42,
        "title": 56,
        "display": 72,
        "hero": 120,
    }

    # Line heights
    LINE_HEIGHTS = {"tight": 1.2, "normal": 1.5, "relaxed": 1.8, "loose": 2.0}

    # Font weights
    WEIGHTS = {
        "light": "300",
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
        "black": "900",
    }
