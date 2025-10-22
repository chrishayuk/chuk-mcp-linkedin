# src/chuk_mcp_linkedin/posts/composition.py
"""
Composition system for building LinkedIn posts from components.

Shadcn-style atomic composition with type-safe components.
"""

from typing import List, Optional, Dict, Any
from .components import (
    PostComponent,
    Hook,
    Body,
    CallToAction,
    Hashtags,
    BarChart,
    MetricsChart,
    ComparisonChart,
    ProgressChart,
    RankingChart,
    Quote,
    BigStat,
    Timeline,
    KeyTakeaway,
    ProCon,
    Checklist,
    BeforeAfter,
    TipBox,
    StatsGrid,
    PollPreview,
    FeatureList,
    NumberedList,
    Separator,
)
from ..tokens.text_tokens import TextTokens


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

    # Content components
    def add_hook(self, hook_type: str, content: str) -> "ComposablePost":
        """Add opening hook"""
        self.components.append(Hook(hook_type, content, self.theme))
        return self

    def add_body(self, content: str, structure: Optional[str] = None) -> "ComposablePost":
        """Add main content body"""
        structure = structure or self.variant_config.get("structure", "linear")
        self.components.append(Body(content, structure, self.theme))
        return self

    def add_cta(self, cta_type: str, text: str) -> "ComposablePost":
        """Add call-to-action"""
        self.components.append(CallToAction(cta_type, text, self.theme))
        return self

    def add_hashtags(self, tags: List[str], placement: str = "end") -> "ComposablePost":
        """Add hashtags"""
        self.components.append(Hashtags(tags, placement, theme=self.theme))
        return self

    # Data viz components
    def add_bar_chart(
        self, data: Dict[str, int], title: Optional[str] = None, unit: str = ""
    ) -> "ComposablePost":
        """Add horizontal bar chart with colored emoji squares"""
        self.components.append(BarChart(data, title, unit, self.theme))
        return self

    def add_metrics_chart(
        self, data: Dict[str, str], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add key metrics chart with indicators"""
        self.components.append(MetricsChart(data, title, self.theme))
        return self

    def add_comparison_chart(
        self, data: Dict[str, Any], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add side-by-side comparison chart"""
        self.components.append(ComparisonChart(data, title, self.theme))
        return self

    def add_progress_chart(
        self, data: Dict[str, int], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add progress bars chart"""
        self.components.append(ProgressChart(data, title, self.theme))
        return self

    def add_ranking_chart(
        self, data: Dict[str, str], title: Optional[str] = None, show_medals: bool = True
    ) -> "ComposablePost":
        """Add ranking/leaderboard chart with medals"""
        self.components.append(RankingChart(data, title, show_medals, self.theme))
        return self

    # Feature components
    def add_quote(self, text: str, author: str, source: Optional[str] = None) -> "ComposablePost":
        """Add quote/testimonial"""
        self.components.append(Quote(text, author, source, self.theme))
        return self

    def add_big_stat(
        self, number: str, label: str, context: Optional[str] = None
    ) -> "ComposablePost":
        """Add big statistic display"""
        self.components.append(BigStat(number, label, context, self.theme))
        return self

    def add_timeline(
        self, steps: Dict[str, str], title: Optional[str] = None, style: str = "arrow"
    ) -> "ComposablePost":
        """Add timeline/step display"""
        self.components.append(Timeline(steps, title, style, self.theme))
        return self

    def add_key_takeaway(
        self, message: str, title: str = "KEY TAKEAWAY", style: str = "box"
    ) -> "ComposablePost":
        """Add key takeaway/insight box"""
        self.components.append(KeyTakeaway(message, title, style, self.theme))
        return self

    def add_pro_con(
        self, pros: List[str], cons: List[str], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add pros & cons comparison"""
        self.components.append(ProCon(pros, cons, title, self.theme))
        return self

    def add_checklist(
        self, items: List[Dict[str, Any]], title: Optional[str] = None, show_progress: bool = False
    ) -> "ComposablePost":
        """Add checklist with checkmarks"""
        self.components.append(Checklist(items, title, show_progress, self.theme))
        return self

    def add_before_after(
        self,
        before: List[str],
        after: List[str],
        title: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> "ComposablePost":
        """Add before/after transformation comparison"""
        self.components.append(BeforeAfter(before, after, title, labels, self.theme))
        return self

    def add_tip_box(
        self, message: str, title: Optional[str] = None, style: str = "info"
    ) -> "ComposablePost":
        """Add highlighted tip/note box"""
        self.components.append(TipBox(message, title, style, self.theme))
        return self

    def add_stats_grid(
        self, stats: Dict[str, str], title: Optional[str] = None, columns: int = 2
    ) -> "ComposablePost":
        """Add multi-stat grid display"""
        self.components.append(StatsGrid(stats, title, columns, self.theme))
        return self

    def add_poll_preview(self, question: str, options: List[str]) -> "ComposablePost":
        """Add poll preview for engagement"""
        self.components.append(PollPreview(question, options, self.theme))
        return self

    def add_feature_list(
        self, features: List[Dict[str, str]], title: Optional[str] = None
    ) -> "ComposablePost":
        """Add feature list with icons and descriptions"""
        self.components.append(FeatureList(features, title, self.theme))
        return self

    def add_numbered_list(
        self, items: List[str], title: Optional[str] = None, style: str = "numbers", start: int = 1
    ) -> "ComposablePost":
        """Add enhanced numbered list"""
        self.components.append(NumberedList(items, title, style, start, self.theme))
        return self

    # Layout components
    def add_separator(self, style: str = "line") -> "ComposablePost":
        """Add visual separator"""
        self.components.append(Separator(style))
        return self

    # Composition methods
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
