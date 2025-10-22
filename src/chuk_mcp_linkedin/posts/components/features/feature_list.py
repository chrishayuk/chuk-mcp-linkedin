# src/chuk_mcp_linkedin/posts/components/features/feature_list.py
"""
Feature list component with icons and descriptions.

Use for product features, benefits, capabilities, service offerings.
"""

from typing import List, Dict, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class FeatureList(PostComponent):
    """Feature list with icons - for product/service highlights"""

    def __init__(
        self,
        features: List[Dict[str, str]],
        title: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.features = features
        self.title = title
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.SYMBOLS.get("features", "✨")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Render features
        for feature in self.features:
            icon = feature.get("icon", "•")
            title = feature.get("title", "")
            description = feature.get("description", "")

            if description:
                lines.append(f"{icon} {title}")
                lines.append(f"   {description}")
            else:
                lines.append(f"{icon} {title}")

        return "\n".join(lines)

    def validate(self) -> bool:
        if not self.features or len(self.features) == 0:
            return False
        for feature in self.features:
            if "title" not in feature or not feature["title"].strip():
                return False
        return True
