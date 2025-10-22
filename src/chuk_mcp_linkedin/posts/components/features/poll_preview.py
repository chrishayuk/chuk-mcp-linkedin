# src/chuk_mcp_linkedin/posts/components/features/poll_preview.py
"""
Poll preview component for engagement.

Use for poll visualization, survey questions, audience engagement.
"""

from typing import List, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class PollPreview(PostComponent):
    """Poll preview - for engagement and feedback"""

    def __init__(
        self,
        question: str,
        options: List[str],
        theme: Optional[Any] = None,
    ):
        self.question = question
        self.options = options
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Poll emoji
        emoji = TextTokens.SYMBOLS.get("poll", "📊")
        lines.append(f"{emoji} POLL:")
        lines.append("")
        lines.append(self.question)
        lines.append("")

        # Render options with radio button emoji
        radio_emoji = "◯"
        for i, option in enumerate(self.options, 1):
            lines.append(f"{radio_emoji} {option}")

        lines.append("")
        lines.append("💬 Vote in the poll below!")

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.question.strip()) > 0
            and 2 <= len(self.options) <= 4
            and all(option.strip() for option in self.options)
        )
