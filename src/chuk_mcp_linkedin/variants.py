"""
CVA-inspired variant system for LinkedIn posts.

Provides variant definitions and resolution with compound variant support.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class VariantConfig:
    """Configuration for a single variant option"""
    name: str
    properties: Dict[str, Any]
    description: Optional[str] = None


class PostVariants:
    """CVA-style variants for LinkedIn posts with compound support"""

    @staticmethod
    def text_post_variants() -> Dict[str, Any]:
        """Variants for text-only posts"""
        return {
            "base": {
                "type": "text",
                "max_length": 3000,
                "has_media": False
            },
            "variants": {
                "style": {
                    "story": {
                        "structure": "story_arc",
                        "emoji_level": "moderate",
                        "line_break_style": "dramatic",
                        "paragraph_length": "tight",
                        "ideal_length": (1000, 2000),
                        "hook_style": "story",
                        "vulnerability_required": True
                    },
                    "insight": {
                        "structure": "framework",
                        "emoji_level": "minimal",
                        "line_break_style": "scannable",
                        "paragraph_length": "standard",
                        "ideal_length": (300, 800),
                        "hook_style": "stat",
                        "credibility_markers": True
                    },
                    "question": {
                        "structure": "question_based",
                        "emoji_level": "moderate",
                        "line_break_style": "scannable",
                        "paragraph_length": "tight",
                        "ideal_length": (50, 200),
                        "hook_style": "question",
                        "requires_cta": True
                    },
                    "listicle": {
                        "structure": "listicle",
                        "emoji_level": "minimal",
                        "line_break_style": "scannable",
                        "paragraph_length": "tight",
                        "ideal_length": (200, 600),
                        "hook_style": "list",
                        "numbered": True
                    },
                    "hot_take": {
                        "structure": "linear",
                        "emoji_level": "minimal",
                        "line_break_style": "dramatic",
                        "paragraph_length": "tight",
                        "ideal_length": (100, 400),
                        "hook_style": "controversy",
                        "controversy_level": "bold"
                    }
                },
                "tone": {
                    "professional": {
                        "formality": "formal",
                        "emoji_level": "none",
                        "humor_level": "none",
                        "vulnerability_level": "guarded"
                    },
                    "conversational": {
                        "formality": "conversational",
                        "emoji_level": "moderate",
                        "humor_level": "subtle",
                        "vulnerability_level": "selective"
                    },
                    "casual": {
                        "formality": "friendly",
                        "emoji_level": "moderate",
                        "humor_level": "moderate",
                        "vulnerability_level": "open"
                    },
                    "inspiring": {
                        "formality": "friendly",
                        "emoji_level": "expressive",
                        "humor_level": "subtle",
                        "vulnerability_level": "open",
                        "emotion": "warm"
                    },
                    "humorous": {
                        "formality": "casual",
                        "emoji_level": "expressive",
                        "humor_level": "frequent",
                        "vulnerability_level": "open"
                    }
                },
                "length": {
                    "micro": {
                        "ideal_length": (50, 150),
                        "line_break_style": "readable",
                        "paragraph_length": "tight",
                        "hook_required": True
                    },
                    "short": {
                        "ideal_length": (150, 300),
                        "line_break_style": "scannable",
                        "paragraph_length": "tight"
                    },
                    "medium": {
                        "ideal_length": (300, 800),
                        "line_break_style": "scannable",
                        "paragraph_length": "standard"
                    },
                    "long": {
                        "ideal_length": (800, 1500),
                        "line_break_style": "dramatic",
                        "paragraph_length": "standard",
                        "structure_required": True
                    },
                    "story": {
                        "ideal_length": (1000, 3000),
                        "line_break_style": "extreme",
                        "paragraph_length": "loose",
                        "structure": "story_arc"
                    }
                }
            },
            "compound_variants": [
                {
                    "conditions": {"style": "story", "tone": "inspiring"},
                    "applies": {
                        "emoji_level": "expressive",
                        "line_break_style": "extreme",
                        "vulnerability_level": "raw",
                        "cta_style": "soft"
                    }
                },
                {
                    "conditions": {"style": "hot_take", "tone": "professional"},
                    "applies": {
                        "emoji_level": "none",
                        "line_break_style": "dramatic",
                        "controversy_level": "moderate",
                        "cta_style": "curiosity"
                    }
                },
                {
                    "conditions": {"style": "listicle", "length": "long"},
                    "applies": {
                        "numbered": True,
                        "visual_symbols": True,
                        "line_break_style": "scannable",
                        "paragraph_length": "tight"
                    }
                },
                {
                    "conditions": {"tone": "humorous", "length": "micro"},
                    "applies": {
                        "structure": "linear",
                        "hook_style": "curiosity",
                        "cta_style": "share"
                    }
                }
            ],
            "default_variant": {
                "style": "insight",
                "tone": "conversational",
                "length": "medium"
            }
        }

    @staticmethod
    def poll_post_variants() -> Dict[str, Any]:
        """Variants for poll posts (highest reach format)"""
        return {
            "base": {
                "type": "poll",
                "options_range": (2, 4),
                "duration_days": (1, 14)
            },
            "variants": {
                "purpose": {
                    "engagement": {
                        "question_style": "provocative",
                        "duration_days": 3,
                        "commentary_length": "short",
                        "follow_up_required": True
                    },
                    "research": {
                        "question_style": "neutral",
                        "duration_days": 7,
                        "commentary_length": "medium",
                        "results_post_required": True
                    },
                    "decision": {
                        "question_style": "help_seeking",
                        "duration_days": 3,
                        "commentary_length": "medium",
                        "vulnerability_level": "open"
                    },
                    "fun": {
                        "question_style": "playful",
                        "duration_days": 1,
                        "commentary_length": "micro",
                        "emoji_level": "expressive"
                    }
                },
                "question_type": {
                    "binary": {
                        "options_count": 2,
                        "controversy_potential": "high"
                    },
                    "multiple_choice": {
                        "options_count": (3, 4),
                        "include_other": True
                    }
                }
            },
            "default_variant": {
                "purpose": "engagement",
                "question_type": "binary"
            }
        }

    @staticmethod
    def document_post_variants() -> Dict[str, Any]:
        """Variants for document/PDF posts (highest engagement format)"""
        return {
            "base": {
                "type": "document",
                "format": "pdf",
                "slide_limit": (5, 10)
            },
            "variants": {
                "content_type": {
                    "guide": {
                        "slide_count": (7, 10),
                        "layout": "educational",
                        "text_density": "medium",
                        "visual_ratio": 0.4
                    },
                    "checklist": {
                        "slide_count": (5, 8),
                        "layout": "list_based",
                        "text_density": "low",
                        "visual_ratio": 0.3,
                        "checkboxes": True
                    },
                    "stats": {
                        "slide_count": (5, 7),
                        "layout": "data_focused",
                        "text_density": "low",
                        "visual_ratio": 0.7,
                        "charts_required": True
                    },
                    "report": {
                        "slide_count": (8, 10),
                        "layout": "professional",
                        "text_density": "high",
                        "visual_ratio": 0.5,
                        "credibility_markers": True
                    }
                },
                "design_style": {
                    "minimal": {
                        "color_count": 2,
                        "font_count": 1,
                        "decoration": "none",
                        "white_space": "high"
                    },
                    "professional": {
                        "color_count": 3,
                        "font_count": 2,
                        "decoration": "subtle",
                        "white_space": "medium",
                        "branding": True
                    },
                    "vibrant": {
                        "color_count": 5,
                        "font_count": 2,
                        "decoration": "bold",
                        "white_space": "low",
                        "gradients": True
                    }
                }
            },
            "default_variant": {
                "content_type": "guide",
                "design_style": "professional"
            }
        }


class VariantResolver:
    """Resolve variants and apply them to posts"""

    @staticmethod
    def resolve(
        base_variants: Dict[str, Any],
        selected: Dict[str, str],
        theme: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Resolve variant selections into final configuration.
        Applies base → variants → compounds → theme overrides.
        """
        config = base_variants["base"].copy()

        # Apply selected variants
        for variant_type, variant_name in selected.items():
            if variant_type in base_variants["variants"]:
                variant_config = base_variants["variants"][variant_type].get(variant_name, {})
                config.update(variant_config)

        # Apply compound variants
        for compound in base_variants.get("compound_variants", []):
            if all(
                selected.get(k) == v
                for k, v in compound["conditions"].items()
            ):
                config.update(compound["applies"])

        # Apply theme overrides if provided
        if theme:
            theme_overrides = {
                "emoji_level": getattr(theme, "emoji_level", None),
                "line_break_style": getattr(theme, "line_break_style", None),
                "formality": getattr(theme, "formality", None),
                "hook_style": getattr(theme, "hook_style", None),
                "cta_style": getattr(theme, "cta_style", None),
            }
            # Only apply non-None theme values that aren't already explicitly set
            for key, value in theme_overrides.items():
                if value is not None and key not in selected:
                    config[key] = value

        return config

    @staticmethod
    def suggest_variants(
        post_type: str,
        goal: str,
        theme: Optional[Any] = None
    ) -> Dict[str, str]:
        """Suggest optimal variant combinations based on goal"""

        suggestions = {
            "text": {
                "authority": {"style": "insight", "tone": "professional", "length": "medium"},
                "engagement": {"style": "question", "tone": "conversational", "length": "short"},
                "virality": {"style": "hot_take", "tone": "conversational", "length": "micro"},
                "community": {"style": "story", "tone": "inspiring", "length": "long"},
            },
            "document": {
                "authority": {"content_type": "report", "design_style": "professional"},
                "engagement": {"content_type": "checklist", "design_style": "vibrant"},
                "education": {"content_type": "guide", "design_style": "professional"},
            },
            "poll": {
                "engagement": {"purpose": "engagement", "question_type": "binary"},
                "research": {"purpose": "research", "question_type": "multiple_choice"},
                "community": {"purpose": "decision", "question_type": "multiple_choice"},
            }
        }

        return suggestions.get(post_type, {}).get(goal, {})

    @staticmethod
    def get_all_variants(post_type: str) -> Dict[str, Any]:
        """Get all available variants for a post type"""
        variant_methods = {
            "text": PostVariants.text_post_variants,
            "poll": PostVariants.poll_post_variants,
            "document": PostVariants.document_post_variants,
        }

        method = variant_methods.get(post_type)
        if method:
            return method()

        return {}
