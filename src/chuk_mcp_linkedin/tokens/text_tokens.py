# src/chuk_mcp_linkedin/text_tokens.py
"""
Text formatting tokens for LinkedIn posts.

Based on 2025 performance data analysis of 1M+ posts.
"""

from typing import Dict, Tuple, Any


class TextTokens:
    """Design tokens for text formatting on LinkedIn"""

    # LinkedIn character limits
    MAX_LENGTH = 3000
    TRUNCATION_POINT = 210  # "...see more" appears here

    # Ideal length ranges for different post types
    IDEAL_LENGTH: Dict[str, Tuple[int, int]] = {
        "micro": (50, 150),  # Quick update/question
        "short": (150, 300),  # Standard engagement post
        "medium": (300, 800),  # Thought leadership
        "long": (800, 1500),  # Deep dive analysis
        "story": (1000, 3000),  # Long-form narrative
    }

    # Line break styles for scannability
    LINE_BREAKS: Dict[str, int] = {
        "dense": 1,  # Traditional paragraph
        "readable": 2,  # Standard spacing
        "scannable": 3,  # Easy to scan (recommended)
        "dramatic": 5,  # High visual impact
        "extreme": 7,  # Maximum white space
    }

    # Paragraph length guidelines
    PARAGRAPH_LENGTH: Dict[str, Tuple[int, int]] = {
        "tight": (1, 2),  # 1-2 sentences
        "standard": (2, 4),  # 2-4 sentences
        "loose": (4, 6),  # 4-6 sentences
    }

    # Emoji usage formulas (emojis per word ratio)
    EMOJI: Dict[str, float] = {
        "none": 0.0,
        "minimal": 0.01,  # 1 per 100 words (~1-2 per post)
        "moderate": 0.05,  # 1 per 20 words (~3-5 per post)
        "expressive": 0.1,  # 1 per 10 words (~5-10 per post)
        "heavy": 0.15,  # 1 per 7 words (influencer style)
    }

    # Hashtag best practices
    HASHTAGS: Dict[str, Any] = {
        "count": {
            "minimal": (1, 2),
            "optimal": (3, 5),  # Sweet spot based on 2025 data
            "maximum": (5, 7),
            "over_limit": 8,  # Diminishing returns
        },
        "placement": {
            "inline": "Within the text flow",
            "mid": "After main content, before CTA",
            "end": "At the very end (most common)",
            "first_comment": "In first comment (keeps post clean)",
        },
        "strategy": {
            "branded": "Company/personal brand tags",
            "trending": "Current trending topics",
            "niche": "Industry-specific hashtags",
            "mixed": "Blend of all three (recommended)",
        },
    }

    # Visual formatting symbols
    SYMBOLS: Dict[str, str] = {
        "arrow": "→",
        "bullet": "•",
        "checkmark": "✓",
        "cross": "✗",
        "lightning": "⚡",
        "bulb": "💡",
        "target": "🎯",
        "pin": "📌",
    }

    # Separators for visual breaks
    SEPARATORS: Dict[str, str] = {"line": "---", "dots": "• • •", "wave": "~", "heavy": "━━━"}

    @classmethod
    def get_length_range(cls, length_type: str) -> Tuple[int, int]:
        """Get min/max length for a post type"""
        return cls.IDEAL_LENGTH.get(length_type, cls.IDEAL_LENGTH["medium"])

    @classmethod
    def get_line_break_count(cls, style: str) -> int:
        """Get number of line breaks for a style"""
        return cls.LINE_BREAKS.get(style, 2)

    @classmethod
    def calculate_emoji_count(cls, word_count: int, level: str) -> int:
        """Calculate recommended emoji count based on word count"""
        ratio = cls.EMOJI.get(level, 0.05)
        return int(word_count * ratio)

    @classmethod
    def get_hashtag_count(cls, strategy: str) -> Tuple[int, int]:
        """Get recommended hashtag count range"""
        return cls.HASHTAGS["count"].get(strategy, cls.HASHTAGS["count"]["optimal"])
