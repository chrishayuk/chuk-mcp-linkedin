# src/chuk_mcp_linkedin/posts/components/features/timeline.py
"""
Timeline/step component for LinkedIn posts.

Use for processes, journeys, and historical progression.
"""

from typing import Any, Dict, Optional

from ....tokens.text_tokens import TextTokens
from ..base import PostComponent


class Timeline(PostComponent):
    """Timeline/step component - for processes, journeys, historical progression"""

    def __init__(
        self,
        steps: Dict[str, str],
        title: Optional[str] = None,
        style: str = "arrow",
        theme: Optional[Any] = None,
    ):
        self.steps = steps
        self.title = title
        self.style = style
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Title if provided
        if self.title:
            emoji = TextTokens.SYMBOLS.get("calendar", "📅")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Choose separator based on style
        if self.style == "arrow":
            separator = TextTokens.SYMBOLS.get("arrow", "→")
        elif self.style == "numbered":
            separator = None  # Will use numbers
        else:  # dated
            separator = "|"

        # Render steps
        for idx, (key, value) in enumerate(self.steps.items(), 1):
            if self.style == "numbered":
                lines.append(f"{idx}. {key}: {value}")
            else:
                lines.append(f"{key} {separator} {value}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.steps) >= 2 and self.style in ["arrow", "numbered", "dated"]
