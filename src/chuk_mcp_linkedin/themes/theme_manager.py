"""
Theme management system for LinkedIn posts.

Provides 10 pre-built themes for different LinkedIn personas and strategies.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any


@dataclass
class LinkedInTheme:
    """Complete theme definition for LinkedIn voice and strategy"""

    # Identity
    name: str
    description: str

    # Voice & Tone
    tone: str  # professional, casual, inspirational, technical, humorous
    formality: str  # formal, conversational, friendly, casual
    emotion: str  # neutral, warm, passionate, analytical, playful

    # Content Strategy
    primary_goal: str  # authority, engagement, community, leads, awareness
    content_mix: Dict[str, float]  # {"educational": 0.4, "personal": 0.3, "promotional": 0.3}

    # Formatting Style
    emoji_level: str  # none, minimal, moderate, expressive, heavy
    line_break_style: str  # dense, readable, scannable, dramatic, extreme
    paragraph_length: str  # tight, standard, loose

    # Structure Preferences
    preferred_structures: List[str]  # ["listicle", "framework", "story_arc"]
    hook_style: str  # question, stat, story, controversy, list, curiosity
    cta_style: str  # direct, curiosity, action, share, soft

    # Engagement Style
    hashtag_strategy: str  # minimal, optimal, branded, trending, mixed
    hashtag_placement: str  # inline, mid, end, first_comment
    comment_style: str  # brief, thoughtful, conversational, deep

    # Content Characteristics
    controversy_level: str  # safe, moderate, bold, provocative
    vulnerability_level: str  # guarded, selective, open, raw
    humor_level: str  # none, subtle, moderate, frequent

    # Visual Preferences
    preferred_formats: List[str]  # ["text", "carousel", "video", "document"]
    media_frequency: float  # 0.0 to 1.0 (how often to include media)

    # Scheduling
    post_frequency: int  # Posts per week
    best_posting_times: List[str]  # ["morning", "lunch"]


# Pre-built themes for common LinkedIn personas
THEMES: Dict[str, LinkedInTheme] = {
    "thought_leader": LinkedInTheme(
        name="Thought Leader",
        description="Establish expertise and industry authority",
        tone="professional",
        formality="conversational",
        emotion="analytical",
        primary_goal="authority",
        content_mix={"educational": 0.6, "personal": 0.2, "promotional": 0.2},
        emoji_level="minimal",
        line_break_style="scannable",
        paragraph_length="standard",
        preferred_structures=["framework", "listicle", "comparison"],
        hook_style="stat",
        cta_style="curiosity",
        hashtag_strategy="minimal",
        hashtag_placement="end",
        comment_style="thoughtful",
        controversy_level="moderate",
        vulnerability_level="selective",
        humor_level="subtle",
        preferred_formats=["text", "document", "carousel"],
        media_frequency=0.4,
        post_frequency=4,
        best_posting_times=["morning", "lunch"],
    ),
    "personal_brand": LinkedInTheme(
        name="Personal Brand Builder",
        description="Build authentic personal connection and following",
        tone="inspirational",
        formality="friendly",
        emotion="warm",
        primary_goal="engagement",
        content_mix={"personal": 0.5, "educational": 0.3, "promotional": 0.2},
        emoji_level="moderate",
        line_break_style="dramatic",
        paragraph_length="tight",
        preferred_structures=["story_arc", "linear", "question_based"],
        hook_style="story",
        cta_style="share",
        hashtag_strategy="mixed",
        hashtag_placement="end",
        comment_style="conversational",
        controversy_level="safe",
        vulnerability_level="open",
        humor_level="moderate",
        preferred_formats=["text", "image", "video"],
        media_frequency=0.6,
        post_frequency=5,
        best_posting_times=["morning", "evening"],
    ),
    "technical_expert": LinkedInTheme(
        name="Technical Expert",
        description="Deep technical knowledge and precision",
        tone="technical",
        formality="formal",
        emotion="analytical",
        primary_goal="authority",
        content_mix={"educational": 0.7, "personal": 0.1, "promotional": 0.2},
        emoji_level="none",
        line_break_style="readable",
        paragraph_length="standard",
        preferred_structures=["listicle", "framework", "linear"],
        hook_style="question",
        cta_style="direct",
        hashtag_strategy="niche",
        hashtag_placement="end",
        comment_style="deep",
        controversy_level="safe",
        vulnerability_level="guarded",
        humor_level="none",
        preferred_formats=["text", "document", "carousel"],
        media_frequency=0.3,
        post_frequency=3,
        best_posting_times=["morning"],
    ),
    "community_builder": LinkedInTheme(
        name="Community Builder",
        description="Foster connection and conversation",
        tone="casual",
        formality="friendly",
        emotion="playful",
        primary_goal="community",
        content_mix={"personal": 0.4, "educational": 0.4, "promotional": 0.2},
        emoji_level="expressive",
        line_break_style="scannable",
        paragraph_length="tight",
        preferred_structures=["question_based", "story_arc", "listicle"],
        hook_style="question",
        cta_style="curiosity",
        hashtag_strategy="trending",
        hashtag_placement="first_comment",
        comment_style="conversational",
        controversy_level="safe",
        vulnerability_level="open",
        humor_level="frequent",
        preferred_formats=["poll", "text", "video"],
        media_frequency=0.5,
        post_frequency=5,
        best_posting_times=["morning", "lunch", "evening"],
    ),
    "corporate_professional": LinkedInTheme(
        name="Corporate Professional",
        description="Polished corporate communication",
        tone="professional",
        formality="formal",
        emotion="neutral",
        primary_goal="awareness",
        content_mix={"educational": 0.5, "promotional": 0.3, "personal": 0.2},
        emoji_level="minimal",
        line_break_style="readable",
        paragraph_length="standard",
        preferred_structures=["linear", "listicle", "comparison"],
        hook_style="stat",
        cta_style="direct",
        hashtag_strategy="branded",
        hashtag_placement="end",
        comment_style="brief",
        controversy_level="safe",
        vulnerability_level="guarded",
        humor_level="none",
        preferred_formats=["document", "image", "article"],
        media_frequency=0.7,
        post_frequency=3,
        best_posting_times=["morning", "lunch"],
    ),
    "contrarian_voice": LinkedInTheme(
        name="Contrarian Voice",
        description="Challenge status quo, spark debate",
        tone="professional",
        formality="conversational",
        emotion="passionate",
        primary_goal="engagement",
        content_mix={"educational": 0.5, "personal": 0.3, "promotional": 0.2},
        emoji_level="minimal",
        line_break_style="dramatic",
        paragraph_length="tight",
        preferred_structures=["linear", "comparison", "question_based"],
        hook_style="controversy",
        cta_style="curiosity",
        hashtag_strategy="minimal",
        hashtag_placement="mid",
        comment_style="thoughtful",
        controversy_level="bold",
        vulnerability_level="selective",
        humor_level="subtle",
        preferred_formats=["text", "carousel", "video"],
        media_frequency=0.3,
        post_frequency=4,
        best_posting_times=["morning", "lunch"],
    ),
    "storyteller": LinkedInTheme(
        name="Storyteller",
        description="Narrative-driven, emotional connection",
        tone="inspirational",
        formality="conversational",
        emotion="warm",
        primary_goal="engagement",
        content_mix={"personal": 0.6, "educational": 0.3, "promotional": 0.1},
        emoji_level="moderate",
        line_break_style="dramatic",
        paragraph_length="loose",
        preferred_structures=["story_arc", "linear"],
        hook_style="story",
        cta_style="soft",
        hashtag_strategy="minimal",
        hashtag_placement="end",
        comment_style="conversational",
        controversy_level="safe",
        vulnerability_level="raw",
        humor_level="moderate",
        preferred_formats=["text", "video", "image"],
        media_frequency=0.5,
        post_frequency=4,
        best_posting_times=["morning", "evening"],
    ),
    "data_driven": LinkedInTheme(
        name="Data-Driven Analyst",
        description="Let the numbers tell the story",
        tone="professional",
        formality="conversational",
        emotion="analytical",
        primary_goal="authority",
        content_mix={"educational": 0.7, "personal": 0.1, "promotional": 0.2},
        emoji_level="minimal",
        line_break_style="scannable",
        paragraph_length="tight",
        preferred_structures=["listicle", "comparison", "framework"],
        hook_style="stat",
        cta_style="direct",
        hashtag_strategy="niche",
        hashtag_placement="end",
        comment_style="thoughtful",
        controversy_level="moderate",
        vulnerability_level="guarded",
        humor_level="subtle",
        preferred_formats=["document", "carousel", "image"],
        media_frequency=0.8,
        post_frequency=3,
        best_posting_times=["morning", "lunch"],
    ),
    "coach_mentor": LinkedInTheme(
        name="Coach/Mentor",
        description="Guide and support your audience",
        tone="inspirational",
        formality="friendly",
        emotion="warm",
        primary_goal="community",
        content_mix={"educational": 0.5, "personal": 0.4, "promotional": 0.1},
        emoji_level="moderate",
        line_break_style="scannable",
        paragraph_length="tight",
        preferred_structures=["framework", "question_based", "listicle"],
        hook_style="question",
        cta_style="action",
        hashtag_strategy="optimal",
        hashtag_placement="end",
        comment_style="deep",
        controversy_level="safe",
        vulnerability_level="open",
        humor_level="moderate",
        preferred_formats=["text", "carousel", "video"],
        media_frequency=0.5,
        post_frequency=5,
        best_posting_times=["morning", "evening"],
    ),
    "entertainer": LinkedInTheme(
        name="The Entertainer",
        description="Make LinkedIn fun and memorable",
        tone="humorous",
        formality="casual",
        emotion="playful",
        primary_goal="engagement",
        content_mix={"personal": 0.5, "educational": 0.3, "promotional": 0.2},
        emoji_level="expressive",
        line_break_style="dramatic",
        paragraph_length="tight",
        preferred_structures=["story_arc", "linear", "question_based"],
        hook_style="curiosity",
        cta_style="share",
        hashtag_strategy="trending",
        hashtag_placement="first_comment",
        comment_style="conversational",
        controversy_level="moderate",
        vulnerability_level="open",
        humor_level="frequent",
        preferred_formats=["text", "video", "image"],
        media_frequency=0.6,
        post_frequency=5,
        best_posting_times=["lunch", "evening"],
    ),
}


class ThemeManager:
    """Manage and apply themes to posts"""

    def __init__(self):
        self.themes = THEMES.copy()
        self.custom_themes: Dict[str, LinkedInTheme] = {}

    def get_theme(self, name: str) -> LinkedInTheme:
        """Get theme by name"""
        if name in self.themes:
            return self.themes[name]
        elif name in self.custom_themes:
            return self.custom_themes[name]
        else:
            raise ValueError(f"Theme '{name}' not found")

    def list_themes(self) -> List[str]:
        """List all available themes"""
        return list(self.themes.keys()) + list(self.custom_themes.keys())

    def get_all_themes(self) -> Dict[str, LinkedInTheme]:
        """Get all themes"""
        return {**self.themes, **self.custom_themes}

    def create_custom_theme(self, **kwargs) -> LinkedInTheme:
        """Create a custom theme"""
        theme = LinkedInTheme(**kwargs)
        self.custom_themes[theme.name.lower().replace(" ", "_")] = theme
        return theme

    def export_theme(self, theme_name: str) -> Dict[str, Any]:
        """Export theme as dictionary"""
        theme = self.get_theme(theme_name)
        return asdict(theme)

    def import_theme(self, theme_dict: Dict[str, Any]) -> LinkedInTheme:
        """Import theme from dictionary"""
        theme = LinkedInTheme(**theme_dict)
        theme_key = theme.name.lower().replace(" ", "_")
        self.custom_themes[theme_key] = theme
        return theme

    def get_theme_summary(self, theme_name: str) -> Dict[str, Any]:
        """Get summary of theme characteristics"""
        theme = self.get_theme(theme_name)
        return {
            "name": theme.name,
            "description": theme.description,
            "tone": theme.tone,
            "goal": theme.primary_goal,
            "post_frequency": f"{theme.post_frequency}x per week",
            "best_formats": theme.preferred_formats,
            "emoji_level": theme.emoji_level,
            "controversy_level": theme.controversy_level,
        }

    def recommend_theme(self, goal: str) -> List[str]:
        """Recommend themes based on goal"""
        recommendations = []

        for theme_name, theme in self.get_all_themes().items():
            if theme.primary_goal == goal.lower():
                recommendations.append(theme_name)

        return recommendations if recommendations else ["thought_leader"]
