"""
Key metrics chart component with emoji indicators.

Use for KPIs and statistics with ✅/❌ indicators.
"""

from typing import Dict, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class MetricsChart(PostComponent):
    """Key metrics with emoji indicators - for KPIs and statistics"""

    def __init__(
        self,
        data: Dict[str, str],
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
            emoji = TextTokens.CHART_EMOJIS.get("metrics", "📈")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        for label, value in self.data.items():
            # Determine emoji based on value or label using design tokens
            if isinstance(value, str):
                if "%" in value or "increase" in label.lower() or "growth" in label.lower():
                    emoji = TextTokens.INDICATORS.get("positive", "✅")
                elif "decrease" in label.lower() or "down" in label.lower():
                    emoji = TextTokens.INDICATORS.get("negative", "❌")
                else:
                    emoji = TextTokens.INDICATORS.get("positive", "✅")
            else:
                emoji = TextTokens.INDICATORS.get("positive", "✅")

            arrow = TextTokens.SYMBOLS.get("arrow", "→")
            lines.append(f"{emoji} {value} {arrow} {label}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0
