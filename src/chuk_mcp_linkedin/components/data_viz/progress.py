"""
Progress indicator components for LinkedIn documents.

Progress bars, rings, step progress, and milestone trackers.
Uses design tokens for consistent styling.
"""

from typing import Dict, Any, List as ListType
from ...tokens.design_tokens import DesignTokens


class Progress:
    """Progress indicator components for LinkedIn documents"""

    @staticmethod
    def progress_bar(
        percentage: float,
        label: str = None,
        color: str = None,
        color_scheme: str = "minimal",
        height: int = None,
    ) -> Dict[str, Any]:
        """
        Horizontal progress bar.

        Args:
            percentage: Progress percentage (0-100)
            label: Optional label text
            color: Progress bar color (defaults to accent)
            color_scheme: Color scheme to use
            height: Bar height in pixels (defaults to token size)

        Returns:
            Progress bar component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "accent")

        if height is None:
            height = 20  # 20px default height

        background_color = f"{color}20"  # 12% opacity
        label_color = DesignTokens.get_color(color_scheme, "primary")

        config = {
            "type": "progress",
            "variant": "bar",
            "percentage": percentage,
            "bar_color": color,
            "background_color": background_color,
            "height": height,
            "border_radius": DesignTokens.LAYOUT["border_radius"]["medium"],
        }

        if label:
            config["label"] = {
                "text": label,
                "font_size": DesignTokens.get_font_size("body"),
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
                "color": label_color,
                "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
                "margin_bottom": DesignTokens.get_spacing("gaps", "tiny"),
            }

        return config

    @staticmethod
    def progress_ring(
        percentage: float,
        size: int = None,
        color: str = None,
        color_scheme: str = "minimal",
        show_percentage: bool = True,
    ) -> Dict[str, Any]:
        """
        Circular progress ring.

        Args:
            percentage: Progress percentage (0-100)
            size: Ring diameter in pixels (defaults to token size)
            color: Ring color (defaults to accent)
            color_scheme: Color scheme to use
            show_percentage: Show percentage text in center

        Returns:
            Progress ring component configuration
        """
        if color is None:
            color = DesignTokens.get_color(color_scheme, "accent")

        if size is None:
            size = DesignTokens.VISUAL["icon_sizes"]["huge"]  # 120px

        background_color = f"{color}20"  # 12% opacity
        percentage_color = DesignTokens.get_color(color_scheme, "primary")

        config = {
            "type": "progress",
            "variant": "ring",
            "percentage": percentage,
            "size": size,
            "ring_color": color,
            "background_color": background_color,
            "stroke_width": 12,  # 12px stroke
        }

        if show_percentage:
            config["center_text"] = {
                "text": f"{percentage:.0f}%",
                "font_size": DesignTokens.get_font_size("title"),  # 56pt
                "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
                "color": percentage_color,
                "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            }

        return config

    @staticmethod
    def step_progress(
        steps: ListType[str], current_step: int, color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Step-by-step progress indicator.

        Args:
            steps: List of step labels
            current_step: Current step index (0-based)
            color_scheme: Color scheme to use

        Returns:
            Step progress component configuration
        """
        completed_color = DesignTokens.COLORS["semantic"]["success"]
        current_color = DesignTokens.get_color(color_scheme, "accent")
        pending_color = DesignTokens.get_color(color_scheme, "secondary")
        label_color = DesignTokens.get_color(color_scheme, "primary")

        return {
            "type": "progress",
            "variant": "steps",
            "steps": steps,
            "current_step": current_step,
            "completed_color": completed_color,
            "current_color": current_color,
            "pending_color": pending_color,
            "label_color": label_color,
            "step_size": DesignTokens.VISUAL["icon_sizes"]["medium"],  # 48px circles
            "connector_height": 4,  # 4px line between steps
            "font_size": DesignTokens.get_font_size("body"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["medium"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "gap": DesignTokens.get_spacing("gaps", "large"),  # 40px between steps
        }

    @staticmethod
    def milestone_tracker(
        milestones: ListType[Dict[str, Any]], color_scheme: str = "minimal"
    ) -> Dict[str, Any]:
        """
        Milestone progress tracker.

        Args:
            milestones: List of milestone dicts (title, date, status)
            color_scheme: Color scheme to use

        Returns:
            Milestone tracker component configuration
        """
        completed_color = DesignTokens.COLORS["semantic"]["success"]
        in_progress_color = DesignTokens.get_color(color_scheme, "accent")
        pending_color = DesignTokens.get_color(color_scheme, "secondary")
        text_color = DesignTokens.get_color(color_scheme, "primary")
        date_color = DesignTokens.get_color(color_scheme, "secondary")

        return {
            "type": "progress",
            "variant": "milestones",
            "milestones": milestones,  # [{"title": "Launch", "date": "Q1", "status": "completed"}, ...]
            "completed_color": completed_color,
            "in_progress_color": in_progress_color,
            "pending_color": pending_color,
            "text_color": text_color,
            "date_color": date_color,
            "marker_size": DesignTokens.VISUAL["icon_sizes"]["small"],  # 32px
            "title_font_size": DesignTokens.get_font_size("body"),
            "title_font_weight": DesignTokens.TYPOGRAPHY["weights"]["semibold"],
            "date_font_size": DesignTokens.get_font_size("small"),
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
            "milestone_spacing": DesignTokens.get_spacing("gaps", "large"),
        }

    @staticmethod
    def gauge(
        value: float,
        min_value: float = 0,
        max_value: float = 100,
        label: str = None,
        color_scheme: str = "minimal",
    ) -> Dict[str, Any]:
        """
        Gauge/speedometer-style indicator.

        Args:
            value: Current value
            min_value: Minimum value
            max_value: Maximum value
            label: Optional label
            color_scheme: Color scheme to use

        Returns:
            Gauge component configuration
        """
        gauge_color = DesignTokens.get_color(color_scheme, "accent")
        value_color = DesignTokens.get_color(color_scheme, "primary")
        label_color = DesignTokens.get_color(color_scheme, "secondary")

        percentage = ((value - min_value) / (max_value - min_value)) * 100

        config = {
            "type": "progress",
            "variant": "gauge",
            "value": value,
            "min_value": min_value,
            "max_value": max_value,
            "percentage": percentage,
            "gauge_color": gauge_color,
            "value_color": value_color,
            "size": DesignTokens.VISUAL["icon_sizes"]["huge"],  # 120px
            "stroke_width": 12,
            "font_size": DesignTokens.get_font_size("title"),
            "font_weight": DesignTokens.TYPOGRAPHY["weights"]["bold"],
            "font_family": DesignTokens.TYPOGRAPHY["fonts"]["sans"],
        }

        if label:
            config["label"] = {
                "text": label,
                "font_size": DesignTokens.get_font_size("body"),
                "color": label_color,
            }

        return config
