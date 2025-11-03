# src/chuk_mcp_linkedin/posts/components/features/quote.py
"""
Quote/testimonial component for LinkedIn posts.

Use for customer quotes, testimonials, and inspirational quotes.
"""

from typing import Any, Optional

from ....tokens.text_tokens import TextTokens
from ..base import PostComponent


class Quote(PostComponent):
    """Quote/testimonial component - for customer quotes, testimonials, inspirational quotes"""

    def __init__(
        self,
        text: str,
        author: str,
        source: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.text = text
        self.author = author
        self.source = source
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Quote emoji
        emoji = TextTokens.SYMBOLS.get("quote", "💬")

        # Format quote with quotation marks
        lines.append(f'{emoji} "{self.text}"')

        # Author line with attribution
        if self.source:
            lines.append(f"   — {self.author}, {self.source}")
        else:
            lines.append(f"   — {self.author}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.text) > 0 and len(self.text) <= 500 and len(self.author) > 0
