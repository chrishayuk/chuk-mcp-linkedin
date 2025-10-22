"""
Side-by-side A vs B comparison chart component.

Use for contrasting options with bullet points.
"""

from typing import Dict, Any, Optional
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class ComparisonChart(PostComponent):
    """Side-by-side A vs B comparison - for contrasting options"""

    def __init__(
        self,
        data: Dict[str, Any],
        title: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.data = data
        self.title = title
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("comparison", "⚖️")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        items = list(self.data.items())
        bullet = TextTokens.SYMBOLS.get("bullet", "•")

        if len(items) >= 2:
            for idx, (label, points) in enumerate(items):
                emoji = (
                    TextTokens.INDICATORS.get("positive", "✅")
                    if idx == len(items) - 1
                    else TextTokens.INDICATORS.get("negative", "❌")
                )
                lines.append(f"{emoji} {label}:")
                if isinstance(points, list):
                    for point in points:
                        lines.append(f"  {bullet} {point}")
                else:
                    lines.append(f"  {points}")
                if idx < len(items) - 1:
                    lines.append("")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) >= 2
