# src/chuk_mcp_linkedin/posts/components/features/tip_box.py
"""
Tip/Note box component for highlighting important information.

Use for pro tips, warnings, important notes, best practices.
"""

from typing import Optional, Any
from ..base import PostComponent


class TipBox(PostComponent):
    """Highlighted tip/note box - for important insights"""

    # Style to emoji mapping
    STYLE_EMOJIS = {"info": "ℹ️", "tip": "💡", "warning": "⚠️", "success": "✅"}

    # Style to default title mapping
    STYLE_TITLES = {"info": "INFO", "tip": "PRO TIP", "warning": "WARNING", "success": "SUCCESS"}

    def __init__(
        self,
        message: str,
        title: Optional[str] = None,
        style: str = "info",
        theme: Optional[Any] = None,
    ):
        self.message = message
        self.title = title
        self.style = style
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Get emoji and title for style
        emoji = self.STYLE_EMOJIS.get(self.style, "💡")
        title = self.title or self.STYLE_TITLES.get(self.style, "TIP")

        # Render tip box
        lines.append("")
        lines.append(f"{emoji} {title.upper()}:")
        lines.append("")
        lines.append(self.message)
        lines.append("")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.message.strip()) > 0 and self.style in self.STYLE_EMOJIS
