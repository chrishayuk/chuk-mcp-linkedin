# src/chuk_mcp_linkedin/posts/components/features/before_after.py
"""
Before/After comparison component for transformations.

Use for showing improvements, transformations, comparisons, results.
"""

from typing import List, Dict, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class BeforeAfter(PostComponent):
    """Before/After comparison - for transformation stories"""

    def __init__(
        self,
        before: List[str],
        after: List[str],
        title: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        theme: Optional[Any] = None,
    ):
        self.before = before
        self.after = after
        self.title = title
        self.labels = labels or {"before": "BEFORE", "after": "AFTER"}
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.SYMBOLS.get("transformation", "🔄")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Before section
        before_label = self.labels.get("before", "BEFORE")
        before_emoji = "❌"
        lines.append(f"{before_emoji} {before_label}:")
        for item in self.before:
            lines.append(f"• {item}")

        lines.append("")

        # After section
        after_label = self.labels.get("after", "AFTER")
        after_emoji = "✅"
        lines.append(f"{after_emoji} {after_label}:")
        for item in self.after:
            lines.append(f"• {item}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.before) > 0
            and len(self.after) > 0
            and all(item.strip() for item in self.before)
            and all(item.strip() for item in self.after)
        )
