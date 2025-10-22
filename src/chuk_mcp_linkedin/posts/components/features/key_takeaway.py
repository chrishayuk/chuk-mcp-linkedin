"""
Key takeaway/insight box component for LinkedIn posts.

Use for highlighting main points, lessons, and TLDR sections.
"""

from typing import Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class KeyTakeaway(PostComponent):
    """Key takeaway/insight box - for highlighting main points, lessons, TLDR"""

    def __init__(
        self,
        message: str,
        title: str = "KEY TAKEAWAY",
        style: str = "box",
        theme: Optional[Any] = None,
    ):
        self.message = message
        self.title = title
        self.style = style
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Lightbulb emoji for insights
        emoji = TextTokens.SYMBOLS.get("lightbulb", "💡")

        if self.style == "box":
            # Box style with title
            lines.append(f"{emoji} {self.title}:")
            lines.append("")
            lines.append(self.message)
        elif self.style == "highlight":
            # Simple highlight
            lines.append(f"{emoji} {self.message}")
        else:  # simple
            # Just the message
            lines.append(self.message)

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.message) > 0
            and len(self.message) <= 500
            and self.style in ["box", "highlight", "simple"]
        )
