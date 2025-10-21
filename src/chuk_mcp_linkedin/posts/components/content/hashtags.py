"""
Hashtag component for LinkedIn posts.

Supports placement: inline, mid, end, first_comment.
"""

from typing import List, Optional, Any
from ..base import PostComponent


class Hashtags(PostComponent):
    """Hashtag component"""

    def __init__(
        self,
        tags: List[str],
        placement: str = "end",
        strategy: str = "mixed",
        theme: Optional[Any] = None,
    ):
        self.tags = tags
        self.placement = placement
        self.strategy = strategy
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme

        # Limit to optimal count
        max_tags = 5
        if theme:
            if theme.hashtag_strategy == "minimal":
                max_tags = 3
            elif theme.hashtag_strategy == "optimal":
                max_tags = 5

        tags_to_use = self.tags[:max_tags]

        # Format
        if self.placement == "inline":
            return " ".join([f"#{tag}" for tag in tags_to_use])
        else:
            return "\n\n" + " ".join([f"#{tag}" for tag in tags_to_use])

    def validate(self) -> bool:
        return len(self.tags) > 0 and all(len(tag) > 0 for tag in self.tags)
