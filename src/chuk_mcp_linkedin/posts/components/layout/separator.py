"""
Visual separator component for LinkedIn posts.

Use for visual breaks between sections.
"""

from typing import Optional, Any
from ..base import PostComponent
from ....tokens.structure_tokens import StructureTokens


class Separator(PostComponent):
    """Visual separator component"""

    def __init__(self, style: str = "line"):
        self.style = style

    def render(self, theme: Optional[Any] = None) -> str:
        return StructureTokens.get_separator(self.style)

    def validate(self) -> bool:
        return True
