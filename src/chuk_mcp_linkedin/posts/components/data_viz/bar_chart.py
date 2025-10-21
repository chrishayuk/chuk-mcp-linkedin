"""
Horizontal bar chart component using colored emoji squares.

LinkedIn-optimized for proportional fonts.
"""

from typing import Dict, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class BarChart(PostComponent):
    """Horizontal bar chart using colored emoji squares - LinkedIn-optimized"""

    def __init__(
        self,
        data: Dict[str, int],
        title: Optional[str] = None,
        unit: str = "",
        theme: Optional[Any] = None,
    ):
        self.data = data
        self.title = title
        self.unit = unit
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("time", "⏱️")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Use design tokens for bar colors
        colors = TextTokens.BAR_COLORS

        for idx, (label, value) in enumerate(self.data.items()):
            color = colors[idx % len(colors)]
            bar = color * int(value)
            value_text = f"{value} {self.unit}".strip() if self.unit else str(value)
            lines.append(f"{bar} {label}: {value_text}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0 and all(isinstance(v, (int, float)) for v in self.data.values())
