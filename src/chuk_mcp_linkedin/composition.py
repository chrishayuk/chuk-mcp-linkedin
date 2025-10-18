"""
Composition system for building LinkedIn posts from subcomponents.

Shadcn-style composition with Hook, Body, CTA, and Hashtags components.
"""

from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from .tokens.text_tokens import TextTokens
from .tokens.engagement_tokens import EngagementTokens
from .tokens.structure_tokens import StructureTokens


class PostComponent(ABC):
    """Base class for all post subcomponents"""

    @abstractmethod
    def render(self, theme: Optional[Any] = None) -> str:
        """Render component to text"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate component configuration"""
        pass


class Hook(PostComponent):
    """Opening hook component"""

    def __init__(
        self,
        hook_type: str,
        content: str,
        theme: Optional[Any] = None
    ):
        self.hook_type = hook_type
        self.content = content
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme

        # Get templates for this hook type
        templates = EngagementTokens.get_hook_examples(self.hook_type)

        # Apply theme-specific emphasis if needed
        rendered = self.content

        if theme and theme.controversy_level in ["bold", "provocative"]:
            if self.hook_type == "controversy":
                rendered = f"🚨 {rendered}"

        return rendered

    def validate(self) -> bool:
        return len(self.content) > 0 and len(self.content) <= 200


class Body(PostComponent):
    """Main content body component"""

    def __init__(
        self,
        content: str,
        structure: str = "linear",
        theme: Optional[Any] = None
    ):
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


class CallToAction(PostComponent):
    """Call-to-action component"""

    def __init__(
        self,
        cta_type: str,
        text: str,
        theme: Optional[Any] = None
    ):
        self.cta_type = cta_type
        self.text = text
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme

        # Add emoji based on theme
        if theme and theme.emoji_level in ["moderate", "expressive", "heavy"]:
            emoji_map = {
                "direct": "👇",
                "curiosity": "🤔",
                "action": "⚡",
                "share": "🔄",
                "soft": "💭"
            }
            emoji = emoji_map.get(self.cta_type, "")
            return f"{emoji} {self.text}" if emoji else self.text

        return self.text

    def validate(self) -> bool:
        return len(self.text) > 0 and len(self.text) <= 200


class Hashtags(PostComponent):
    """Hashtag component"""

    def __init__(
        self,
        tags: List[str],
        placement: str = "end",
        strategy: str = "mixed",
        theme: Optional[Any] = None
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


class Separator(PostComponent):
    """Visual separator component"""

    def __init__(self, style: str = "line"):
        self.style = style

    def render(self, theme: Optional[Any] = None) -> str:
        return StructureTokens.get_separator(self.style)

    def validate(self) -> bool:
        return True


class ComposablePost:
    """Shadcn-style composition for LinkedIn posts"""

    def __init__(
        self,
        post_type: str,
        theme: Optional[Any] = None,
        variant_config: Optional[Dict] = None
    ):
        self.post_type = post_type
        self.theme = theme
        self.variant_config = variant_config or {}
        self.components: List[PostComponent] = []
        self.metadata: Dict[str, Any] = {}

    def add_hook(self, hook_type: str, content: str) -> 'ComposablePost':
        """Add opening hook"""
        self.components.append(Hook(hook_type, content, self.theme))
        return self

    def add_body(self, content: str, structure: Optional[str] = None) -> 'ComposablePost':
        """Add main content body"""
        structure = structure or self.variant_config.get("structure", "linear")
        self.components.append(Body(content, structure, self.theme))
        return self

    def add_separator(self, style: str = "line") -> 'ComposablePost':
        """Add visual separator"""
        self.components.append(Separator(style))
        return self

    def add_cta(self, cta_type: str, text: str) -> 'ComposablePost':
        """Add call-to-action"""
        self.components.append(CallToAction(cta_type, text, self.theme))
        return self

    def add_hashtags(self, tags: List[str], placement: str = "end") -> 'ComposablePost':
        """Add hashtags"""
        self.components.append(Hashtags(tags, placement, theme=self.theme))
        return self

    def compose(self) -> str:
        """Compose final post text"""
        sections = []

        for component in self.components:
            if component.validate():
                rendered = component.render(self.theme)
                sections.append(rendered)

        final_text = "\n\n".join(sections)

        # Validate total length
        if len(final_text) > TextTokens.MAX_LENGTH:
            raise ValueError(f"Post exceeds {TextTokens.MAX_LENGTH} character limit: {len(final_text)} chars")

        return final_text

    def get_preview(self, chars: int = 210) -> str:
        """Get truncated preview (what users see before 'see more')"""
        full_text = self.compose()
        if len(full_text) <= chars:
            return full_text
        return full_text[:chars] + "..."

    def optimize_for_engagement(self) -> 'ComposablePost':
        """Apply engagement optimizations"""
        # Ensure hook exists
        has_hook = any(isinstance(c, Hook) for c in self.components)
        if not has_hook and self.theme:
            hook_style = getattr(self.theme, "hook_style", "question")
            self.components.insert(0, Hook(hook_style, "", self.theme))

        # Ensure CTA exists
        has_cta = any(isinstance(c, CallToAction) for c in self.components)
        if not has_cta and self.theme:
            cta_style = getattr(self.theme, "cta_style", "curiosity")
            self.components.append(CallToAction(cta_style, "What's your take?", self.theme))

        return self

    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary"""
        return {
            "post_type": self.post_type,
            "theme": self.theme.name if self.theme else None,
            "components": [
                {
                    "type": type(c).__name__,
                    "content": c.render(self.theme)
                }
                for c in self.components
            ],
            "final_text": self.compose(),
            "character_count": len(self.compose()),
            "preview": self.get_preview()
        }


class PostBuilder:
    """Fluent builder for common post patterns"""

    @staticmethod
    def thought_leadership_post(
        hook_stat: str,
        framework_name: str,
        framework_parts: List[str],
        conclusion: str,
        theme: Any
    ) -> ComposablePost:
        """Pre-built thought leadership pattern"""

        post = ComposablePost("text", theme=theme)

        post.add_hook("stat", hook_stat)
        post.add_body(f"Here's the {framework_name}:", structure="linear")

        framework_text = "||".join(framework_parts)
        post.add_body(framework_text, structure="framework")

        post.add_separator("line")
        post.add_body(conclusion, structure="linear")
        post.add_cta("curiosity", "Which resonates most with you?")
        post.add_hashtags([framework_name.replace(" ", ""), "Leadership", "Strategy"])

        return post

    @staticmethod
    def story_post(
        hook: str,
        problem: str,
        journey: str,
        solution: str,
        lesson: str,
        theme: Any
    ) -> ComposablePost:
        """Pre-built story arc pattern"""

        post = ComposablePost("text", theme=theme)

        post.add_hook("story", hook)

        story = f"{problem}\n\n{journey}\n\n{solution}"
        post.add_body(story, structure="story_arc")

        post.add_separator("dots")
        post.add_body(f"The lesson: {lesson}", structure="linear")
        post.add_cta("soft", "Have you experienced something similar?")

        return post

    @staticmethod
    def listicle_post(
        hook: str,
        items: List[str],
        conclusion: str,
        theme: Any
    ) -> ComposablePost:
        """Pre-built listicle pattern"""

        post = ComposablePost("text", theme=theme)

        post.add_hook("list", hook)

        list_content = "\n".join(items)
        post.add_body(list_content, structure="listicle")

        post.add_separator("wave")
        post.add_body(conclusion, structure="linear")
        post.add_cta("action", "Save this for later")

        return post

    @staticmethod
    def comparison_post(
        hook: str,
        option_a: str,
        option_b: str,
        recommendation: str,
        theme: Any
    ) -> ComposablePost:
        """Pre-built comparison pattern"""

        post = ComposablePost("text", theme=theme)

        post.add_hook("question", hook)

        comparison = f"{option_a}||{option_b}"
        post.add_body(comparison, structure="comparison")

        post.add_separator("line")
        post.add_body(f"My take: {recommendation}", structure="linear")
        post.add_cta("curiosity", "Which would you choose?")

        return post
