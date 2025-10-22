# src/chuk_mcp_linkedin/posts/components/features/checklist.py
"""
Checklist component for action items and tasks.

Use for to-do lists, action items, pre-launch checklists, requirements.
"""

from typing import List, Dict, Any, Optional
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class Checklist(PostComponent):
    """Checklist with checkmarks - for actionable tasks"""

    def __init__(
        self,
        items: List[Dict[str, Any]],
        title: Optional[str] = None,
        show_progress: bool = False,
        theme: Optional[Any] = None,
    ):
        self.items = items
        self.title = title
        self.show_progress = show_progress
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.SYMBOLS.get("checklist", "✓")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Show progress if requested
        if self.show_progress:
            completed = sum(1 for item in self.items if item.get("checked", False))
            total = len(self.items)
            lines.append(f"Progress: {completed}/{total} complete")
            lines.append("")

        # Render checklist items
        checked_emoji = TextTokens.SYMBOLS.get("checkmark", "✅")
        unchecked_emoji = TextTokens.SYMBOLS.get("checkbox", "☐")

        for item in self.items:
            text = item.get("text", "")
            checked = item.get("checked", False)
            emoji = checked_emoji if checked else unchecked_emoji
            lines.append(f"{emoji} {text}")

        return "\n".join(lines)

    def validate(self) -> bool:
        if not self.items or len(self.items) == 0:
            return False
        for item in self.items:
            if "text" not in item or not item["text"]:
                return False
        return True
