"""
Composition system for building LinkedIn posts from subcomponents.

Shadcn-style composition with Hook, Body, CTA, and Hashtags components.
"""

from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from .tokens.text_tokens import TextTokens
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

    def __init__(self, hook_type: str, content: str, theme: Optional[Any] = None):
        self.hook_type = hook_type
        self.content = content
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme

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


class CallToAction(PostComponent):
    """Call-to-action component"""

    def __init__(self, cta_type: str, text: str, theme: Optional[Any] = None):
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
                "soft": "💭",
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


class BarChart(PostComponent):
    """Horizontal bar chart using colored emoji squares - LinkedIn-optimized"""

    def __init__(
        self,
        data: Dict[str, int],
        title: Optional[str] = None,
        unit: str = "",
        theme: Optional[Any] = None,
    ):
        self.data = data
        self.title = title
        self.unit = unit
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("time", "⏱️")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Use design tokens for bar colors
        colors = TextTokens.BAR_COLORS

        for idx, (label, value) in enumerate(self.data.items()):
            color = colors[idx % len(colors)]
            bar = color * int(value)
            value_text = f"{value} {self.unit}".strip() if self.unit else str(value)
            lines.append(f"{bar} {label}: {value_text}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0 and all(isinstance(v, (int, float)) for v in self.data.values())


class MetricsChart(PostComponent):
    """Key metrics with emoji indicators - for KPIs and statistics"""

    def __init__(
        self,
        data: Dict[str, str],
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
            emoji = TextTokens.CHART_EMOJIS.get("metrics", "📈")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        for label, value in self.data.items():
            # Determine emoji based on value or label using design tokens
            if isinstance(value, str):
                if "%" in value or "increase" in label.lower() or "growth" in label.lower():
                    emoji = TextTokens.INDICATORS.get("positive", "✅")
                elif "decrease" in label.lower() or "down" in label.lower():
                    emoji = TextTokens.INDICATORS.get("negative", "❌")
                else:
                    emoji = TextTokens.INDICATORS.get("positive", "✅")
            else:
                emoji = TextTokens.INDICATORS.get("positive", "✅")

            arrow = TextTokens.SYMBOLS.get("arrow", "→")
            lines.append(f"{emoji} {value} {arrow} {label}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0


class ComparisonChart(PostComponent):
    """Side-by-side A vs B comparison - for contrasting options"""

    def __init__(
        self,
        data: Dict[str, Any],
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
            emoji = TextTokens.CHART_EMOJIS.get("comparison", "⚖️")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        items = list(self.data.items())
        bullet = TextTokens.SYMBOLS.get("bullet", "•")

        if len(items) >= 2:
            for idx, (label, points) in enumerate(items):
                emoji = (
                    TextTokens.INDICATORS.get("positive", "✅")
                    if idx == len(items) - 1
                    else TextTokens.INDICATORS.get("negative", "❌")
                )
                lines.append(f"{emoji} {label}:")
                if isinstance(points, list):
                    for point in points:
                        lines.append(f"  {bullet} {point}")
                else:
                    lines.append(f"  {points}")
                if idx < len(items) - 1:
                    lines.append("")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) >= 2


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

        for label, percentage in self.data.items():
            # Convert percentage to progress bar using design tokens
            if isinstance(percentage, (int, float)):
                filled = int(percentage / 10)
                empty = 10 - filled
                bar = filled_char * filled + empty_char * empty
                lines.append(f"{bar} {percentage}% - {label}")
            else:
                lines.append(f"{bullet} {label}: {percentage}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0 and all(
            isinstance(v, (int, float)) and 0 <= v <= 100 for v in self.data.values()
        )


class RankingChart(PostComponent):
    """Ranked list with medals and numbers - for top lists and leaderboards"""

    def __init__(
        self,
        data: Dict[str, str],
        title: Optional[str] = None,
        show_medals: bool = True,
        theme: Optional[Any] = None,
    ):
        self.data = data
        self.title = title
        self.show_medals = show_medals
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("ranking", "🏆")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Use design tokens for medals
        medals = [
            TextTokens.INDICATORS.get("gold_medal", "🥇"),
            TextTokens.INDICATORS.get("silver_medal", "🥈"),
            TextTokens.INDICATORS.get("bronze_medal", "🥉"),
        ]

        for idx, (label, value) in enumerate(self.data.items()):
            if self.show_medals and idx < 3:
                prefix = medals[idx]
            else:
                prefix = f"{idx + 1}."

            lines.append(f"{prefix} {label}: {value}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.data) > 0


class Quote(PostComponent):
    """Quote/testimonial component - for customer quotes, testimonials, inspirational quotes"""

    def __init__(
        self,
        text: str,
        author: str,
        source: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.text = text
        self.author = author
        self.source = source
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Quote emoji
        emoji = TextTokens.SYMBOLS.get("quote", "💬")

        # Format quote with quotation marks
        lines.append(f'{emoji} "{self.text}"')

        # Author line with attribution
        if self.source:
            lines.append(f"   — {self.author}, {self.source}")
        else:
            lines.append(f"   — {self.author}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.text) > 0 and len(self.text) <= 500 and len(self.author) > 0


class BigStat(PostComponent):
    """Big statistic display - for eye-catching numbers and key metrics"""

    def __init__(
        self,
        number: str,
        label: str,
        context: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.number = number
        self.label = label
        self.context = context
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Stats emoji
        emoji = TextTokens.CHART_EMOJIS.get("metrics", "📈")

        # Big number on its own line
        lines.append(f"{emoji} {self.number}")
        lines.append(self.label)

        # Optional context
        if self.context:
            lines.append("")
            lines.append(self.context)

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.number) > 0 and len(self.label) > 0


class Timeline(PostComponent):
    """Timeline/step component - for processes, journeys, historical progression"""

    def __init__(
        self,
        steps: Dict[str, str],
        title: Optional[str] = None,
        style: str = "arrow",
        theme: Optional[Any] = None,
    ):
        self.steps = steps
        self.title = title
        self.style = style
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Title if provided
        if self.title:
            emoji = TextTokens.SYMBOLS.get("calendar", "📅")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Choose separator based on style
        if self.style == "arrow":
            separator = TextTokens.SYMBOLS.get("arrow", "→")
        elif self.style == "numbered":
            separator = None  # Will use numbers
        else:  # dated
            separator = "|"

        # Render steps
        for idx, (key, value) in enumerate(self.steps.items(), 1):
            if self.style == "numbered":
                lines.append(f"{idx}. {key}: {value}")
            else:
                lines.append(f"{key} {separator} {value}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return len(self.steps) >= 2 and self.style in ["arrow", "numbered", "dated"]


class KeyTakeaway(PostComponent):
    """Key takeaway/insight box - for highlighting main points, lessons, TLDR"""

    def __init__(
        self,
        message: str,
        title: str = "KEY TAKEAWAY",
        style: str = "box",
        theme: Optional[Any] = None,
    ):
        self.message = message
        self.title = title
        self.style = style
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Lightbulb emoji for insights
        emoji = TextTokens.SYMBOLS.get("lightbulb", "💡")

        if self.style == "box":
            # Box style with title
            lines.append(f"{emoji} {self.title}:")
            lines.append("")
            lines.append(self.message)
        elif self.style == "highlight":
            # Simple highlight
            lines.append(f"{emoji} {self.message}")
        else:  # simple
            # Just the message
            lines.append(self.message)

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.message) > 0
            and len(self.message) <= 500
            and self.style in ["box", "highlight", "simple"]
        )


class ProCon(PostComponent):
    """Pros & Cons comparison - for decision-making, trade-offs, evaluations"""

    def __init__(
        self,
        pros: List[str],
        cons: List[str],
        title: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        self.pros = pros
        self.cons = cons
        self.title = title
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        theme = theme or self.theme
        lines = []

        # Title if provided
        if self.title:
            emoji = TextTokens.CHART_EMOJIS.get("comparison", "⚖️")
            lines.append(f"{emoji} {self.title.upper()}:")
            lines.append("")

        # Pros section
        positive = TextTokens.INDICATORS.get("positive", "✅")
        lines.append(f"{positive} PROS:")
        for pro in self.pros:
            bullet = TextTokens.SYMBOLS.get("bullet", "•")
            lines.append(f"{bullet} {pro}")

        lines.append("")

        # Cons section
        negative = TextTokens.INDICATORS.get("negative", "❌")
        lines.append(f"{negative} CONS:")
        for con in self.cons:
            bullet = TextTokens.SYMBOLS.get("bullet", "•")
            lines.append(f"{bullet} {con}")

        return "\n".join(lines)

    def validate(self) -> bool:
        return (
            len(self.pros) > 0
            and len(self.cons) > 0
            and all(len(p.strip()) > 0 for p in self.pros)
            and all(len(c.strip()) > 0 for c in self.cons)
        )


class Separator(PostComponent):
    """Visual separator component"""

    def __init__(self, style: str = "line"):
        self.style = style

    def render(self, theme: Optional[Any] = None) -> str:
        return StructureTokens.get_separator(self.style)

    def validate(self) -> bool:
        return True


class DocumentAttachment(PostComponent):
    """Document attachment component - reference to existing PDF/PPTX/DOCX file"""

    def __init__(
        self,
        filepath: str,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        theme: Optional[Any] = None,
    ):
        """
        Attach an existing document file to the post.

        Args:
            filepath: Path to PDF, PPTX, or DOCX file
            title: Document title (defaults to filename)
            caption: Optional caption text
        """
        self.filepath = filepath
        self.title = title
        self.caption = caption
        self.theme = theme

    def render(self, theme: Optional[Any] = None) -> str:
        """Render document reference for text-only view"""
        from pathlib import Path

        path = Path(self.filepath)
        title = self.title or path.stem
        file_ext = path.suffix.upper()

        # For text rendering, show a placeholder
        emoji = TextTokens.SYMBOLS.get("pin", "📌")
        lines = []
        lines.append(f"{emoji} {title}")
        lines.append(f"   (Attached {file_ext} document)")

        if self.caption:
            lines.append("")
            lines.append(self.caption)

        return "\n".join(lines)

    def validate(self) -> bool:
        """Validate document file exists and is supported format"""
        from pathlib import Path

        path = Path(self.filepath)
        if not path.exists():
            return False

        supported_extensions = [".pdf", ".ppt", ".pptx", ".doc", ".docx"]
        return path.suffix.lower() in supported_extensions


class ComposablePost:
    """Shadcn-style composition for LinkedIn posts"""

    def __init__(
        self, post_type: str, theme: Optional[Any] = None, variant_config: Optional[Dict] = None
    ):
        self.post_type = post_type
        self.theme = theme
        self.variant_config = variant_config or {}
        self.components: List[PostComponent] = []
        self.metadata: Dict[str, Any] = {}

    def add_hook(self, hook_type: str, content: str) -> "ComposablePost":
        """Add opening hook"""
        self.components.append(Hook(hook_type, content, self.theme))
        return self

    def add_body(self, content: str, structure: Optional[str] = None) -> "ComposablePost":
        """Add main content body"""
        structure = structure or self.variant_config.get("structure", "linear")
        self.components.append(Body(content, structure, self.theme))
        return self

    def add_separator(self, style: str = "line") -> "ComposablePost":
        """Add visual separator"""
        self.components.append(Separator(style))
        return self

    def add_bar_chart(
        self, data: Dict[str, int], title: Optional[str] = None, unit: str = ""
    ) -> "ComposablePost":
        """Add horizontal bar chart with colored emoji squares

        Args:
            data: Chart data (e.g., {"AI-Assisted": 12, "Code Review": 6})
            title: Optional chart title
            unit: Optional unit label (e.g., "hours", "users")
        """
        self.components.append(BarChart(data, title, unit, self.theme))
        return self

    def add_metrics_chart(
        self, data: Dict[str, str], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add key metrics chart with indicators

        Args:
            data: Metrics data (e.g., {"Faster problem-solving": "67%"})
            title: Optional chart title
        """
        self.components.append(MetricsChart(data, title, self.theme))
        return self

    def add_comparison_chart(
        self, data: Dict[str, Any], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add side-by-side comparison chart

        Args:
            data: Comparison data with 2+ options
            title: Optional chart title
        """
        self.components.append(ComparisonChart(data, title, self.theme))
        return self

    def add_progress_chart(
        self, data: Dict[str, int], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add progress bars chart

        Args:
            data: Progress data as percentages (e.g., {"Completion": 75})
            title: Optional chart title
        """
        self.components.append(ProgressChart(data, title, self.theme))
        return self

    def add_ranking_chart(
        self, data: Dict[str, str], title: Optional[str] = None, show_medals: bool = True
    ) -> "ComposablePost":
        """Add ranking/leaderboard chart with medals

        Args:
            data: Ranking data (e.g., {"Python": "1M users"})
            title: Optional chart title
            show_medals: Show medal emojis for top 3 (default: True)
        """
        self.components.append(RankingChart(data, title, show_medals, self.theme))
        return self

    def add_quote(self, text: str, author: str, source: Optional[str] = None) -> "ComposablePost":
        """Add quote/testimonial

        Args:
            text: Quote text
            author: Author name
            source: Optional source/title (e.g., "CTO at TechCorp")
        """
        self.components.append(Quote(text, author, source, self.theme))
        return self

    def add_big_stat(
        self, number: str, label: str, context: Optional[str] = None
    ) -> "ComposablePost":
        """Add big statistic display

        Args:
            number: The statistic number (e.g., "2.5M", "340%")
            label: Description of the statistic
            context: Optional additional context
        """
        self.components.append(BigStat(number, label, context, self.theme))
        return self

    def add_timeline(
        self, steps: Dict[str, str], title: Optional[str] = None, style: str = "arrow"
    ) -> "ComposablePost":
        """Add timeline/step display

        Args:
            steps: Timeline steps as key-value pairs
            title: Optional timeline title
            style: Timeline style: "arrow", "numbered", or "dated"
        """
        self.components.append(Timeline(steps, title, style, self.theme))
        return self

    def add_key_takeaway(
        self, message: str, title: str = "KEY TAKEAWAY", style: str = "box"
    ) -> "ComposablePost":
        """Add key takeaway/insight box

        Args:
            message: The key takeaway message
            title: Takeaway box title (default: "KEY TAKEAWAY")
            style: Display style: "box", "highlight", or "simple"
        """
        self.components.append(KeyTakeaway(message, title, style, self.theme))
        return self

    def add_pro_con(
        self, pros: List[str], cons: List[str], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add pros & cons comparison

        Args:
            pros: List of pros/advantages
            cons: List of cons/disadvantages
            title: Optional title for the comparison
        """
        self.components.append(ProCon(pros, cons, title, self.theme))
        return self

    def add_cta(self, cta_type: str, text: str) -> "ComposablePost":
        """Add call-to-action"""
        self.components.append(CallToAction(cta_type, text, self.theme))
        return self

    def add_hashtags(self, tags: List[str], placement: str = "end") -> "ComposablePost":
        """Add hashtags"""
        self.components.append(Hashtags(tags, placement, theme=self.theme))
        return self

    def add_document(
        self, filepath: str, title: Optional[str] = None, caption: Optional[str] = None
    ) -> "ComposablePost":
        """Add document attachment (PDF/PPTX/DOCX file)

        Args:
            filepath: Path to existing document file
            title: Document title (defaults to filename)
            caption: Optional caption for the document
        """
        self.components.append(DocumentAttachment(filepath, title, caption, self.theme))
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
            raise ValueError(
                f"Post exceeds {TextTokens.MAX_LENGTH} character limit: {len(final_text)} chars"
            )

        return final_text

    def get_preview(self, chars: int = 210) -> str:
        """Get truncated preview (what users see before 'see more')"""
        full_text = self.compose()
        if len(full_text) <= chars:
            return full_text
        return full_text[:chars] + "..."

    def optimize_for_engagement(self) -> "ComposablePost":
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
                {"type": type(c).__name__, "content": c.render(self.theme)} for c in self.components
            ],
            "final_text": self.compose(),
            "character_count": len(self.compose()),
            "preview": self.get_preview(),
        }


class PostBuilder:
    """Fluent builder for common post patterns"""

    @staticmethod
    def thought_leadership_post(
        hook_stat: str, framework_name: str, framework_parts: List[str], conclusion: str, theme: Any
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
        hook: str, problem: str, journey: str, solution: str, lesson: str, theme: Any
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
    def listicle_post(hook: str, items: List[str], conclusion: str, theme: Any) -> ComposablePost:
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
        hook: str, option_a: str, option_b: str, recommendation: str, theme: Any
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
