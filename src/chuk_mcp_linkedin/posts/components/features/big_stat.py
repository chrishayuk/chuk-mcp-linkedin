# src/chuk_mcp_linkedin/posts/components/features/big_stat.py
"""
Big statistic display component for LinkedIn posts.

Use for eye-catching numbers and key metrics.
"""

from typing import Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class BigStat(PostComponent):
    """Big statistic display - for eye-catching numbers and key metrics"""

    def __init__(
        self,
        number: str,
        label: str,
        context: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.number = number
        self.label = label
        self.context = context
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Stats emoji
        emoji = TextTokens.CHART_EMOJIS.get("metrics", "📈")

        # Big number on its own line
        lines.append(f"{emoji} {self.number}")
        lines.append(self.label)

        # Optional context
        if self.context:
            lines.append("")
            lines.append(self.context)

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.number) > 0 and len(self.label) > 0
