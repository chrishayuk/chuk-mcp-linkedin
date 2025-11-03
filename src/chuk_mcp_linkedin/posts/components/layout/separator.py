# src/chuk_mcp_linkedin/posts/components/layout/seperator.py
"""
Visual separator component for LinkedIn posts.

Use for visual breaks between sections.
"""

from typing import Any, Optional

from ....tokens.structure_tokens import StructureTokens
from ..base import PostComponent


class Separator(PostComponent):
    """Visual separator component"""

    def __init__(self, style: str = "line"):
        self.style = style

    def render(self, theme: Optional[Any] = None) -> str:
        return StructureTokens.get_separator(self.style)

    def validate(self) -> bool:
        return True
