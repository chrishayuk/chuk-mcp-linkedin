# src/chuk_mcp_linkedin/tokens/engagement_tokens.py
"""
Engagement pattern tokens for LinkedIn posts.

Based on 2025 algorithm optimization data.
"""

from typing import Any, Dict, List


class EngagementTokens:
    """Design tokens for engagement optimization"""

    # Hook types with effectiveness power ratings (0-1 scale)
    HOOKS: Dict[str, Dict[str, Any]] = {
        "question": {
            "power": 0.8,
            "examples": ["What if...?", "Why do...?", "How can...?"],
            "best_for": ["polls", "discussion", "community"],
            "templates": [
                "What if {bold_claim}?",
                "Why do {common_problem}?",
                "How can {desired_outcome}?",
            ],
        },
        "stat": {
            "power": 0.9,
            "examples": ["95% of...", "Only 3 out of 10...", "2025 data shows..."],
            "best_for": ["thought_leadership", "credibility", "shock_value"],
            "templates": [
                "{percentage}% of {audience} {surprising_fact}",
                "Only {number} out of {total} {outcome}",
                "{year} data shows {insight}",
            ],
        },
        "story": {
            "power": 0.85,
            "examples": ["Last Tuesday changed everything...", "I'll never forget when..."],
            "best_for": ["personal_brand", "relatability", "emotion"],
            "templates": [
                "{time_reference} changed everything",
                "I'll never forget when {event}",
                "{years_ago}, {pivotal_moment}",
            ],
        },
        "controversy": {
            "power": 0.95,
            "examples": ["Unpopular opinion:", "Everyone's wrong about...", "Stop doing..."],
            "best_for": ["virality", "debate", "attention"],
            "templates": [
                "Unpopular opinion: {contrarian_view}",
                "Everyone's wrong about {topic}",
                "Stop {common_practice}. Here's why:",
                "Hot take: {bold_statement}",
            ],
        },
        "list": {
            "power": 0.7,
            "examples": ["5 ways to...", "The 3 mistakes...", "Here's what works:"],
            "best_for": ["value", "clarity", "scannability"],
            "templates": [
                "{number} ways to {desired_outcome}",
                "The {number} mistakes {audience} make",
                "Here's what works: {promise}",
            ],
        },
        "curiosity": {
            "power": 0.75,
            "examples": ["The secret to...", "What nobody tells you...", "Here's the truth..."],
            "best_for": ["intrigue", "retention", "click_through"],
            "templates": [
                "The secret to {outcome}",
                "What nobody tells you about {topic}",
                "Here's the truth about {controversial_topic}",
                "The {adjective} way to {goal}",
            ],
        },
    }

    # Call-to-action styles with use cases
    CTA_STYLES: Dict[str, Dict[str, Any]] = {
        "direct": {
            "examples": ["Comment below", "Share your thoughts", "Let me know"],
            "best_for": "straightforward_engagement",
            "power": 0.7,
            "templates": [
                "Comment below with {question}",
                "Share your thoughts on {topic}",
                "Let me know {what_to_share}",
            ],
        },
        "curiosity": {
            "examples": ["What do you think?", "Am I missing something?", "Agree or disagree?"],
            "best_for": "opinion_seeking",
            "power": 0.85,
            "templates": [
                "What do you think about {topic}?",
                "Am I missing something here?",
                "Agree or disagree?",
                "Is this {adjective} or am I crazy?",
            ],
        },
        "action": {
            "examples": ["Try this today", "Save this for later", "Tag someone who needs this"],
            "best_for": "utility_posts",
            "power": 0.75,
            "templates": [
                "Try this {timeframe}",
                "Save this for later",
                "Tag someone who {needs_this}",
                "Bookmark this if {condition}",
            ],
        },
        "share": {
            "examples": ["Tag someone who...", "Share if you...", "Send this to..."],
            "best_for": "viral_potential",
            "power": 0.9,
            "templates": [
                "Tag someone who {characteristic}",
                "Share if you {relate}",
                "Send this to {person_type}",
                "Who else needs to see this?",
            ],
        },
        "poll": {
            "examples": ["Vote in the poll", "Which option?", "Pick one"],
            "best_for": "poll_posts",
            "power": 0.95,
            "templates": [
                "Vote in the poll below",
                "Which option resonates with you?",
                "Pick one and tell me why",
            ],
        },
        "soft": {
            "examples": ["Thoughts?", "Your take?", "What's your experience?"],
            "best_for": "natural_conversation",
            "power": 0.8,
            "templates": [
                "Thoughts?",
                "Your take?",
                "What's your experience with {topic}?",
                "How do you handle this?",
            ],
        },
    }

    # First-hour engagement targets (critical for algorithm)
    FIRST_HOUR_TARGETS: Dict[str, int] = {
        "minimum": 10,  # Minimum for algorithm consideration
        "good": 50,  # Good engagement
        "great": 100,  # Great engagement
        "viral": 200,  # Viral potential threshold
    }

    # Comment response strategy
    COMMENT_RESPONSE: Dict[str, Any] = {
        "timing": {
            "critical_window": 60,  # First 60 minutes
            "recommended": 30,  # Respond within 30 min
            "maximum": 120,  # Don't exceed 2 hours
        },
        "depth": {
            "minimal": "Thanks!",
            "standard": "Thanks for sharing! [brief response]",
            "meaningful": "[Thoughtful response with follow-up question]",
            "deep": "[Detailed response, acknowledges specific points, asks question]",
        },
        "best_practices": [
            "Reply within 60 minutes",
            "Make it meaningful, not just 'Thanks!'",
            "Ask follow-up questions",
            "Tag others when relevant",
            "Use their name when possible",
        ],
    }

    # Timing optimization (2025 data)
    TIMING: Dict[str, Any] = {
        "best_days": ["tuesday", "wednesday", "thursday"],
        "worst_days": ["saturday", "sunday"],
        "best_hours": {
            "morning": (7, 9),  # 7-9 AM local time
            "lunch": (12, 14),  # 12-2 PM local time
            "evening": (17, 18),  # 5-6 PM local time
        },
        "posting_frequency": {
            "minimum": 3,  # Posts per week minimum
            "optimal": (4, 5),  # Sweet spot
            "maximum": 7,  # Daily (risk of fatigue)
            "over_limit": 10,  # Definitely too much
        },
    }

    # Formatting for engagement
    FORMATTING: Dict[str, Any] = {
        "bold_usage": {
            "none": 0.0,
            "key_phrases": 0.05,  # 5% of text
            "emphasis": 0.1,  # 10% of text
            "heavy": 0.15,  # Can feel aggressive
        },
        "white_space_ratio": {
            "dense": 0.1,  # 10% white space
            "balanced": 0.3,  # 30% white space (optimal)
            "airy": 0.5,  # 50% white space (very scannable)
        },
    }

    @classmethod
    def get_hook_power(cls, hook_type: str) -> float:
        """Get effectiveness rating for a hook type"""
        result: float = cls.HOOKS.get(hook_type, {}).get("power", 0.5)
        return result

    @classmethod
    def get_cta_power(cls, cta_type: str) -> float:
        """Get effectiveness rating for a CTA type"""
        result: float = cls.CTA_STYLES.get(cta_type, {}).get("power", 0.5)
        return result

    @classmethod
    def get_hook_examples(cls, hook_type: str) -> List[str]:
        """Get example hooks for a type"""
        result: List[str] = cls.HOOKS.get(hook_type, {}).get("examples", [])
        return result

    @classmethod
    def get_cta_examples(cls, cta_type: str) -> List[str]:
        """Get example CTAs for a type"""
        result: List[str] = cls.CTA_STYLES.get(cta_type, {}).get("examples", [])
        return result

    @classmethod
    def is_optimal_posting_time(cls, day: str, hour: int) -> bool:
        """Check if a given time is optimal for posting"""
        day_lower = day.lower()

        # Check if day is valid (in either best_days or worst_days)
        valid_days = cls.TIMING["best_days"] + cls.TIMING["worst_days"]
        if day_lower not in valid_days:
            return False

        # Check if it's a worst day
        if day_lower in cls.TIMING["worst_days"]:
            return False

        # Check if hour is in optimal time slots
        for period, (start, end) in cls.TIMING["best_hours"].items():
            if start <= hour < end:
                return True

        return False
