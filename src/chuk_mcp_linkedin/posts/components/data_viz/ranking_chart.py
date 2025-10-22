"""
Ranked list chart component with medals and numbers.

Use for top lists and leaderboards with 🥇🥈🥉 medals.
"""

from typing import Dict, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class RankingChart(PostComponent):
    """Ranked list with medals and numbers - for top lists and leaderboards"""

    def __init__(
        self,
        data: Dict[str, str],
        title: Optional[str] = None,
        show_medals: bool = True,
        theme: Optional[Any] = None,
    ):
        self.data = data
        self.title = title
        self.show_medals = show_medals
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("ranking", "🏆")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Use design tokens for medals
        medals = [
            TextTokens.INDICATORS.get("gold_medal", "🥇"),
            TextTokens.INDICATORS.get("silver_medal", "🥈"),
            TextTokens.INDICATORS.get("bronze_medal", "🥉"),
        ]

        for idx, (label, value) in enumerate(self.data.items()):
            if self.show_medals and idx < 3:
                prefix = medals[idx]
            else:
                prefix = f"{idx + 1}."

            lines.append(f"{prefix} {label}: {value}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0
