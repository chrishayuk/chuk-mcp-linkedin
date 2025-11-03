# src/chuk_mcp_linkedin/posts/components/content/body.py
"""
Main content body component for LinkedIn posts.

Supports multiple structures: linear, listicle, framework, story_arc, comparison.
"""

from typing import Any, Optional

from ....tokens.text_tokens import TextTokens
from ..base import PostComponent


class Body(PostComponent):
    """Main content body component"""

    def __init__(self, content: str, structure: str = "linear", theme: Optional[Any] = None):
        self.content = content
        self.structure = structure
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme

        if self.structure == "listicle":
            return self._render_listicle(theme)
        elif self.structure == "framework":
            return self._render_framework(theme)
        elif self.structure == "story_arc":
            return self._render_story_arc(theme)
        elif self.structure == "comparison":
            return self._render_comparison(theme)
        else:
            return self._render_linear(theme)

    def _render_linear(self, theme: Optional[Any]) -> str:
        """Traditional paragraph flow"""
        if theme:
            line_breaks = "\n" * TextTokens.get_line_break_count(theme.line_break_style)
            paragraphs = self.content.split("\n\n")
            return line_breaks.join(paragraphs)
        return self.content

    def _render_listicle(self, theme: Optional[Any]) -> str:
        """Numbered or bulleted list"""
        lines = self.content.strip().split("\n")
        symbol = TextTokens.SYMBOLS.get("arrow", "→")

        if theme and theme.emoji_level == "none":
            symbol = "-"

        formatted_lines = []
        for line in lines:
            if line.strip():
                # Don't add symbol if line already starts with one
                if not line.strip().startswith(("→", "-", "•", "✓")):
                    formatted_lines.append(f"{symbol} {line.strip()}")
                else:
                    formatted_lines.append(line.strip())

        return "\n".join(formatted_lines)

    def _render_framework(self, theme: Optional[Any]) -> str:
        """Framework with structure"""
        parts = self.content.split("||")
        symbol = TextTokens.SYMBOLS.get("pin", "📌")

        if theme and theme.emoji_level in ["none", "minimal"]:
            symbol = "•"

        return "\n\n".join([f"{symbol} {part.strip()}" for part in parts if part.strip()])

    def _render_story_arc(self, theme: Optional[Any]) -> str:
        """Story with emotional arc"""
        line_breaks = "\n\n\n" if theme and theme.line_break_style == "extreme" else "\n\n"
        paragraphs = self.content.split("\n\n")
        return line_breaks.join([p.strip() for p in paragraphs if p.strip()])

    def _render_comparison(self, theme: Optional[Any]) -> str:
        """A vs B comparison"""
        parts = self.content.split("||")
        if len(parts) == 2:
            return f"❌ {parts[0].strip()}\n\n✅ {parts[1].strip()}"
        return self.content

    def validate(self) -> bool:
        return len(self.content) > 0 and len(self.content) <= 2800
