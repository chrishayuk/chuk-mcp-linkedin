"""
Stats grid component for displaying multiple statistics.

Use for KPI displays, performance metrics, multi-stat comparisons.
"""

from typing import Dict, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class StatsGrid(PostComponent):
    """Multi-stat grid display - for KPI dashboards"""

    def __init__(
        self,
        stats: Dict[str, str],
        title: Optional[str] = None,
        columns: int = 2,
        theme: Optional[Any] = None,
    ):
        self.stats = stats
        self.title = title
        self.columns = columns
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("stats", "📊")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Convert stats to list of tuples
        stat_items = list(self.stats.items())

        # Render in grid format
        # For simplicity in text, we'll just do rows with visual grouping
        for i in range(0, len(stat_items), self.columns):
            row_items = stat_items[i : i + self.columns]
            row_parts = []
            for label, value in row_items:
                row_parts.append(f"{label}: {value}")
            lines.append("  |  ".join(row_parts))

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.stats) >= 2
            and 1 <= self.columns <= 4
            and all(label.strip() and value.strip() for label, value in self.stats.items())
        )
