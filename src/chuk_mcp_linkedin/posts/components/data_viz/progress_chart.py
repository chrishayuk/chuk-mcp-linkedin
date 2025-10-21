"""
Progress bars chart component for tracking completion.

Use for project status with 0-100% values.
"""

from typing import Dict, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class ProgressChart(PostComponent):
    """Progress bars for tracking completion - for project status"""

    def __init__(
        self,
        data: Dict[str, int],
        title: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.data = data
        self.title = title
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("progress", "📊")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        filled_char = TextTokens.PROGRESS_BARS.get("filled", "█")
        empty_char = TextTokens.PROGRESS_BARS.get("empty", "░")
        bullet = TextTokens.SYMBOLS.get("bullet", "•")

        # Find the longest label for alignment
        max_label_len = max(len(label) for label in self.data.keys()) if self.data else 0

        for label, percentage in self.data.items():
            # Convert percentage to progress bar using design tokens
            if isinstance(percentage, (int, float)):
                filled = int(percentage / 10)
                empty = 10 - filled
                bar = filled_char * filled + empty_char * empty
                # Format: Label (padded) bar percentage
                padded_label = label.ljust(max_label_len)
                lines.append(f"{padded_label}  {bar} {percentage}%")
            else:
                lines.append(f"{bullet} {label}: {percentage}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0 and all(
            isinstance(v, (int, float)) and 0 <= v <= 100 for v in self.data.values()
        )
