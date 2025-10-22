# src/chuk_mcp_linkedin/posts/components/features/pro_con.py
"""
Pros & Cons comparison component for LinkedIn posts.

Use for decision-making, trade-offs, and evaluations.
"""

from typing import List, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class ProCon(PostComponent):
    """Pros & Cons comparison - for decision-making, trade-offs, evaluations"""

    def __init__(
        self,
        pros: List[str],
        cons: List[str],
        title: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.pros = pros
        self.cons = cons
        self.title = title
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Title if provided
        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("comparison", "⚖️")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Pros section
        positive = TextTokens.INDICATORS.get("positive", "✅")
        lines.append(f"{positive} PROS:")
        for pro in self.pros:
            bullet = TextTokens.SYMBOLS.get("bullet", "•")
            lines.append(f"{bullet} {pro}")

        lines.append("")

        # Cons section
        negative = TextTokens.INDICATORS.get("negative", "❌")
        lines.append(f"{negative} CONS:")
        for con in self.cons:
            bullet = TextTokens.SYMBOLS.get("bullet", "•")
            lines.append(f"{bullet} {con}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.pros) > 0
            and len(self.cons) > 0
            and all(len(p.strip()) > 0 for p in self.pros)
            and all(len(c.strip()) > 0 for c in self.cons)
        )
