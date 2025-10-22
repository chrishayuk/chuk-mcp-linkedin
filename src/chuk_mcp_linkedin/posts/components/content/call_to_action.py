# src/chuk_mcp_linkedin/posts/components/content/call_to_action.py
"""
Call-to-action component for LinkedIn posts.

Supports types: direct, curiosity, action, share, soft.
"""

from typing import Optional, Any
from ..base import PostComponent


class CallToAction(PostComponent):
    """Call-to-action component"""

    def __init__(self, cta_type: str, text: str, theme: Optional[Any] = None):
        self.cta_type = cta_type
        self.text = text
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme

        # Add emoji based on theme
        if theme and theme.emoji_level in ["moderate", "expressive", "heavy"]:
            emoji_map = {
                "direct": "👇",
                "curiosity": "🤔",
                "action": "⚡",
                "share": "🔄",
                "soft": "💭",
            }
            emoji = emoji_map.get(self.cta_type, "")
            return f"{emoji} {self.text}" if emoji else self.text

        return self.text

    def validate(self) -> bool:
        return len(self.text) > 0 and len(self.text) <= 200
