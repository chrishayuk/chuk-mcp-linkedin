# src/chuk_mcp_linkedin/tokens/structure_tokens.py
"""
Content structure tokens for LinkedIn posts.

Patterns for organizing and formatting post content.
"""

from typing import Dict, List, Any


class StructureTokens:
    """Design tokens for content structure and formatting"""

    # Content structure formats
    FORMATS: Dict[str, Dict[str, Any]] = {
        "linear": {
            "description": "Traditional paragraph flow",
            "best_for": ["stories", "analysis", "long_form"],
            "readability": "medium",
            "engagement": 0.6,
            "example": "Paragraph 1\n\nParagraph 2\n\nParagraph 3",
        },
        "listicle": {
            "description": "Numbered or bulleted points",
            "best_for": ["tips", "frameworks", "how_tos"],
            "readability": "high",
            "engagement": 0.85,
            "example": "→ Point 1\n→ Point 2\n→ Point 3",
        },
        "framework": {
            "description": "Acronym or structured framework",
            "best_for": ["thought_leadership", "teaching", "credibility"],
            "readability": "high",
            "engagement": 0.8,
            "example": "S - Strategy\nH - Hustle\nA - Action\nR - Results\nE - Execution",
        },
        "story_arc": {
            "description": "Problem → Journey → Solution → Lesson",
            "best_for": ["personal_brand", "inspiration", "relatability"],
            "readability": "medium",
            "engagement": 0.9,
            "structure": ["problem", "journey", "solution", "lesson"],
        },
        "comparison": {
            "description": "Option A vs Option B",
            "best_for": ["decision_making", "education", "clarity"],
            "readability": "high",
            "engagement": 0.75,
            "example": "❌ Old way\n✅ New way",
        },
        "question_based": {
            "description": "Series of questions with answers",
            "best_for": ["engagement", "teaching", "FAQ"],
            "readability": "high",
            "engagement": 0.8,
            "example": "Q: [Question]\nA: [Answer]",
        },
    }

    # Visual formatting patterns
    VISUAL_FORMATTING: Dict[str, List[str]] = {
        "symbols": ["→", "•", "✓", "✗", "⚡", "💡", "🎯", "📌"],
        "checkmarks": ["✓", "✅", "☑"],
        "crosses": ["✗", "❌", "✘"],
        "arrows": ["→", "➜", "►", "▶"],
        "bullets": ["•", "◦", "▪", "▸"],
        "emphasis": ["⚡", "💡", "🎯", "🔥", "✨", "⭐"],
    }

    # Separator styles
    SEPARATORS: Dict[str, str] = {
        "line": "\n\n---\n\n",
        "dots": "\n\n• • •\n\n",
        "wave": "\n\n~\n\n",
        "heavy": "\n\n━━━\n\n",
        "double": "\n\n===\n\n",
        "minimal": "\n\n",
    }

    # Opening hook patterns
    HOOK_PATTERNS: Dict[str, List[str]] = {
        "question": [
            "What if {premise}?",
            "Why do {observation}?",
            "How can {challenge}?",
            "When will {prediction}?",
            "Where does {inquiry}?",
        ],
        "stat": [
            "{percentage}% of {audience} {fact}",
            "{number} out of {total} {outcome}",
            "According to {source}, {statistic}",
            "New data shows {insight}",
        ],
        "story": [
            "{time_ago} changed everything for me",
            "I'll never forget {event}",
            "Here's what happened when {situation}",
            "Last {time_period}, {pivotal_moment}",
        ],
        "controversy": [
            "Unpopular opinion: {contrarian_view}",
            "Everyone's wrong about {topic}",
            "Stop {common_practice}",
            "Hot take: {bold_claim}",
        ],
        "list": [
            "{number} ways to {outcome}",
            "The {number} mistakes {audience} make",
            "Here's what actually works:",
            "{number} things I learned about {topic}",
        ],
        "curiosity": [
            "The secret to {goal}",
            "What nobody tells you about {topic}",
            "Here's the truth: {revelation}",
            "The {adjective} way to {result}",
        ],
    }

    # Content body structures
    BODY_STRUCTURES: Dict[str, Dict[str, Any]] = {
        "problem_solution": {
            "sections": ["problem", "solution", "implementation"],
            "flow": "problem → solution → how to implement",
            "best_for": ["practical advice", "how-tos"],
        },
        "before_after": {
            "sections": ["before", "change", "after"],
            "flow": "before → what changed → after",
            "best_for": ["transformations", "case studies"],
        },
        "three_act": {
            "sections": ["setup", "conflict", "resolution"],
            "flow": "setup → conflict → resolution",
            "best_for": ["storytelling", "narratives"],
        },
        "pyramid": {
            "sections": ["conclusion", "support", "details"],
            "flow": "main point → supporting points → details",
            "best_for": ["journalism", "reports"],
        },
    }

    # CTA patterns
    CTA_PATTERNS: Dict[str, List[str]] = {
        "direct": [
            "Comment below with {what}",
            "Share your {perspective}",
            "Let me know {question}",
        ],
        "curiosity": [
            "What do you think?",
            "Am I missing something?",
            "Agree or disagree?",
            "How would you handle this?",
        ],
        "action": [
            "Try this {timeframe}",
            "Save this for later",
            "Bookmark if {condition}",
            "Use this {how}",
        ],
        "share": [
            "Tag someone who {characteristic}",
            "Share if you {relate}",
            "Send this to {person}",
            "Who else needs this?",
        ],
        "soft": ["Thoughts?", "Your take?", "Experiences?", "What's worked for you?"],
    }

    # Post length guidelines by structure
    LENGTH_BY_STRUCTURE: Dict[str, Dict[str, Any]] = {
        "linear": {
            "micro": (50, 150),
            "short": (150, 400),
            "medium": (400, 1000),
            "long": (1000, 2500),
        },
        "listicle": {
            "micro": (100, 200),  # 3-5 items
            "short": (200, 400),  # 5-7 items
            "medium": (400, 800),  # 7-10 items
            "long": (800, 1500),  # 10-15 items
        },
        "framework": {"short": (200, 400), "medium": (400, 800), "long": (800, 1200)},
        "story_arc": {"short": (400, 800), "medium": (800, 1500), "long": (1500, 3000)},
    }

    @classmethod
    def get_format_info(cls, format_type: str) -> Dict[str, Any]:
        """Get information about a structure format"""
        return cls.FORMATS.get(format_type, cls.FORMATS["linear"])

    @classmethod
    def get_symbols(cls, symbol_type: str) -> List[str]:
        """Get symbols for a specific type"""
        return cls.VISUAL_FORMATTING.get(symbol_type, ["•"])

    @classmethod
    def get_separator(cls, style: str) -> str:
        """Get separator string for a style"""
        return cls.SEPARATORS.get(style, cls.SEPARATORS["minimal"])

    @classmethod
    def get_hook_template(cls, hook_type: str) -> List[str]:
        """Get hook templates for a type"""
        return cls.HOOK_PATTERNS.get(hook_type, [])

    @classmethod
    def get_cta_template(cls, cta_type: str) -> List[str]:
        """Get CTA templates for a type"""
        return cls.CTA_PATTERNS.get(cta_type, [])

    @classmethod
    def get_recommended_length(cls, structure: str, length_type: str) -> tuple:
        """Get recommended character length for structure and length type"""
        structure_lengths = cls.LENGTH_BY_STRUCTURE.get(
            structure, cls.LENGTH_BY_STRUCTURE["linear"]
        )
        return structure_lengths.get(length_type, (150, 400))
