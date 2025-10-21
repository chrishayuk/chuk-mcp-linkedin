"""
Opening hook component for LinkedIn posts.

Use for question, stat, story, controversy, list, or curiosity hooks.
"""

from typing import Optional, Any
from ..base import PostComponent


class Hook(PostComponent):
    """Opening hook component"""

    def __init__(self, hook_type: str, content: str, theme: Optional[Any] = None):
        self.hook_type = hook_type
        self.content = content
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme

        # Apply theme-specific emphasis if needed
        rendered = self.content

        if theme and theme.controversy_level in ["bold", "provocative"]:
            if self.hook_type == "controversy":
                rendered = f"🚨 {rendered}"

        return rendered

    def validate(self) -> bool:
        return len(self.content) > 0 and len(self.content) <= 200
