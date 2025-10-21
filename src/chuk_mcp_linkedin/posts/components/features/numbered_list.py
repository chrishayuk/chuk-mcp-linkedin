"""
Numbered list component for ordered content.

Use for step-by-step guides, rankings, processes, instructions.
"""

from typing import List, Optional, Any
from ..base import PostComponent
from ....tokens.text_tokens import TextTokens


class NumberedList(PostComponent):
    """Enhanced numbered list - for sequential content"""

    # Emoji numbers for emoji_numbers style
    EMOJI_NUMBERS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    def __init__(
        self,
        items: List[str],
        title: Optional[str] = None,
        style: str = "numbers",
        start: int = 1,
        theme: Optional[Any] = None,
    ):
        self.items = items
        self.title = title
        self.style = style
        self.start = start
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.SYMBOLS.get("list", "📝")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Render numbered items based on style
        for i, item in enumerate(self.items):
            number = self.start + i

            if self.style == "emoji_numbers":
                # Use emoji numbers (1️⃣, 2️⃣, etc.)
                if number <= len(self.EMOJI_NUMBERS):
                    prefix = self.EMOJI_NUMBERS[number - 1]
                else:
                    prefix = f"{number}."
            elif self.style == "bold_numbers":
                # Use bold-style numbers (not actual bold, but visual emphasis)
                prefix = f"[{number}]"
            else:
                # Default: regular numbers
                prefix = f"{number}."

            lines.append(f"{prefix} {item}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.items) > 0
            and all(item.strip() for item in self.items)
            and self.style in ["numbers", "emoji_numbers", "bold_numbers"]
            and self.start >= 1
        )
