"""
Component registry for LLM-friendly discovery of available components.

Provides comprehensive information about all post types, variants, themes,
and their properties.
"""

from typing import Dict, List, Any
from .themes.theme_manager import THEMES
from .variants import VariantResolver


class ComponentRegistry:
    """Registry of all available components with schemas"""

    @staticmethod
    def list_post_components() -> Dict[str, Any]:
        """List all post type components with engagement data"""
        return {
            "text_post": {
                "description": "Simple text update",
                "engagement_rank": 6,
                "variants": ["story", "insight", "question", "listicle", "hot_take"],
                "properties": {
                    "commentary": "Main post text (max 3000 chars)",
                    "hooks": "Opening hook lines",
                    "call_to_action": "Engagement driver",
                    "hashtags": "List of hashtags",
                    "emoji_style": "minimal | moderate | expressive",
                },
                "best_for": ["thought leadership", "quick updates", "storytelling"],
                "examples": [
                    "Thought leadership post with framework",
                    "Personal story with lesson",
                    "Industry insight with data",
                ],
            },
            "document_post": {
                "description": "PDF carousel slides (HIGHEST ENGAGEMENT 2025)",
                "engagement_rank": 1,
                "reach_multiplier": 1.8,
                "engagement_rate": 45.85,
                "variants": ["guide", "report", "checklist", "template", "infographic"],
                "properties": {
                    "commentary": "Introduction text",
                    "pdf_path": "Path to PDF file",
                    "slide_count": "5-10 slides recommended",
                    "theme": "Visual theme",
                },
                "best_for": ["education", "lead magnets", "authority building"],
                "best_practices": [
                    "Keep to 5-10 slides",
                    "One message per slide",
                    "18pt minimum font size",
                    "Square or portrait format",
                ],
            },
            "poll_post": {
                "description": "Poll for engagement (HIGHEST REACH 2025)",
                "engagement_rank": 2,
                "reach_multiplier": 3.0,
                "note": "200%+ higher reach than standard posts - most underused format!",
                "variants": ["opinion", "market-research", "decision", "fun"],
                "properties": {
                    "commentary": "Poll introduction",
                    "question": "Poll question",
                    "options": "2-4 answer options",
                    "duration_days": "1-14 days",
                },
                "best_for": ["engagement", "research", "community building"],
            },
            "video_post": {
                "description": "Video content (1.4x engagement)",
                "engagement_rank": 3,
                "reach_multiplier": 1.4,
                "usage_trend": "+69% in 2025",
                "variants": ["short", "tutorial", "interview", "behind_scenes"],
                "properties": {
                    "commentary": "Video description",
                    "video_path": "Path to video file",
                    "duration_seconds": "30-60s optimal",
                    "vertical": "True (recommended)",
                    "captions_enabled": "True (required)",
                },
                "best_practices": [
                    "First 3 seconds are critical",
                    "Always use captions",
                    "Vertical format preferred",
                    "Hook in opening frame",
                ],
            },
            "image_post": {
                "description": "Single image with text (2x comments vs text)",
                "engagement_rank": 4,
                "variants": ["quote", "data-viz", "photo", "announcement", "meme"],
                "properties": {
                    "commentary": "Image description/context",
                    "image_path": "Path to image",
                    "image_format": "square | portrait",
                    "alt_text": "Accessibility text",
                },
                "best_for": ["quick tips", "quotes", "announcements"],
            },
            "carousel_post": {
                "description": "Multi-image storytelling",
                "engagement_rank": 5,
                "trend": "-18% reach, -25% engagement vs 2024",
                "note": "Keep tight - 5-10 slides max",
                "variants": ["tutorial", "stats", "tips", "before-after", "checklist"],
                "properties": {
                    "commentary": "Introduction text",
                    "images": "List of image slides (max 10)",
                    "theme": "Visual theme for carousel",
                },
                "best_for": ["step-by-step", "lists", "comparisons"],
            },
            "article_post": {
                "description": "Link sharing with commentary",
                "engagement_rank": 7,
                "note": "Preview size reduced in 2025 - consider image + link in first comment",
                "variants": ["resource", "commentary", "curated", "news"],
                "properties": {
                    "commentary": "Your take on the article",
                    "article_url": "URL to share",
                    "link_placement": "inline | first-comment (recommended)",
                },
            },
        }

    @staticmethod
    def list_subcomponents() -> Dict[str, Any]:
        """List composition subcomponents"""
        return {
            "hook": {
                "description": "Opening hook to grab attention",
                "types": {
                    "question": {
                        "power": 0.8,
                        "examples": ["What if...?", "Why do...?", "How can...?"],
                    },
                    "stat": {"power": 0.9, "examples": ["95% of...", "2025 data shows..."]},
                    "story": {
                        "power": 0.85,
                        "examples": ["Last Tuesday...", "I'll never forget..."],
                    },
                    "controversy": {
                        "power": 0.95,
                        "examples": ["Unpopular opinion:", "Everyone's wrong about..."],
                    },
                    "list": {"power": 0.7, "examples": ["5 ways to...", "The 3 mistakes..."]},
                    "curiosity": {
                        "power": 0.75,
                        "examples": ["The secret to...", "What nobody tells you..."],
                    },
                },
                "best_practices": [
                    "First 210 chars visible before 'see more'",
                    "Make it count - hook determines read-through",
                ],
            },
            "body": {
                "description": "Main content component",
                "structures": {
                    "linear": "Traditional paragraphs",
                    "listicle": "Numbered/bulleted points",
                    "framework": "Acronym breakdown",
                    "story_arc": "Problem → Journey → Solution",
                    "comparison": "Option A vs Option B",
                },
            },
            "cta": {
                "description": "Call-to-action to drive engagement",
                "types": {
                    "direct": {"power": 0.7, "examples": ["Comment below"]},
                    "curiosity": {"power": 0.85, "examples": ["What do you think?"]},
                    "action": {"power": 0.75, "examples": ["Try this today"]},
                    "share": {"power": 0.9, "examples": ["Tag someone who..."]},
                    "soft": {"power": 0.8, "examples": ["Thoughts?"]},
                },
            },
            "hashtags": {
                "description": "Hashtag strategy",
                "optimal_count": "3-5",
                "max_recommended": 7,
                "strategies": {
                    "minimal": "1-2 targeted hashtags",
                    "optimal": "3-5 balanced mix (recommended)",
                    "branded": "Company/personal tags",
                    "trending": "Current trends",
                    "mixed": "Blend of all (recommended)",
                },
                "placement": ["inline", "mid", "end", "first_comment"],
            },
        }

    @staticmethod
    def list_themes() -> Dict[str, Any]:
        """List available themes"""
        return {
            theme_name: {
                "description": theme.description,
                "tone": theme.tone,
                "goal": theme.primary_goal,
                "post_frequency": f"{theme.post_frequency}x per week",
                "best_formats": theme.preferred_formats,
                "emoji_level": theme.emoji_level,
                "controversy_level": theme.controversy_level,
            }
            for theme_name, theme in THEMES.items()
        }

    @staticmethod
    def get_recommendations(goal: str) -> Dict[str, Any]:
        """Get component recommendations based on goal"""

        recommendations = {
            "engagement": {
                "top_formats": ["poll_post", "video_post", "text_post", "image_post"],
                "theme": "community_builder",
                "post_frequency": "5x per week",
                "best_practices": [
                    "Use polls for maximum reach (200%+ boost)",
                    "Short videos (30-60s) with captions",
                    "Ask questions in every post",
                    "Reply to all comments within 60 min",
                ],
                "hook_types": ["question", "controversy", "curiosity"],
                "cta_types": ["curiosity", "share"],
            },
            "authority": {
                "top_formats": ["document_post", "text_post", "carousel_post"],
                "theme": "thought_leader",
                "post_frequency": "3-4x per week",
                "best_practices": [
                    "Lead with data/stats",
                    "Use frameworks",
                    "Document posts for deep dives",
                    "Minimal hashtags",
                ],
                "hook_types": ["stat", "framework"],
                "cta_types": ["curiosity", "direct"],
            },
            "leads": {
                "top_formats": ["document_post", "video_post", "carousel_post"],
                "theme": "corporate_professional",
                "post_frequency": "3-4x per week",
                "best_practices": [
                    "Valuable downloadables",
                    "Clear CTAs",
                    "Link in first comment",
                    "Professional design",
                ],
                "hook_types": ["stat", "list"],
                "cta_types": ["action", "direct"],
            },
            "community": {
                "top_formats": ["poll_post", "text_post", "video_post"],
                "theme": "community_builder",
                "post_frequency": "5x per week",
                "best_practices": [
                    "Show vulnerability",
                    "Ask for input",
                    "Share team moments",
                    "Respond to everyone",
                ],
                "hook_types": ["question", "story"],
                "cta_types": ["curiosity", "soft"],
            },
            "awareness": {
                "top_formats": ["video_post", "carousel_post", "document_post"],
                "theme": "personal_brand",
                "post_frequency": "4-5x per week",
                "best_practices": [
                    "Mix of formats",
                    "Consistent branding",
                    "Trending hashtags",
                    "Visual content",
                ],
                "hook_types": ["curiosity", "story"],
                "cta_types": ["share", "action"],
            },
        }

        return recommendations.get(goal.lower(), recommendations["engagement"])

    @staticmethod
    def get_complete_system_overview() -> Dict[str, Any]:
        """Get overview of entire system"""
        return {
            "post_types": 7,
            "themes": len(THEMES),
            "subcomponents": 4,
            "variant_systems": 3,
            "engagement_data": "Based on 1M+ posts analyzed in 2025",
            "top_performers": {
                "highest_engagement": "document_post (45.85% engagement rate)",
                "highest_reach": "poll_post (200%+ above average)",
                "fastest_growing": "video_post (+69% usage, 1.4x engagement)",
                "most_underused": "poll_post (biggest opportunity)",
            },
            "system_features": [
                "7 post type components with variants",
                "10 pre-built themes for different personas",
                "CVA-inspired variant system with compounds",
                "Shadcn-style composition patterns",
                "Research-backed design tokens",
                "Algorithm optimization built-in",
            ],
            "key_metrics": {
                "max_post_length": 3000,
                "truncation_point": 210,
                "optimal_hashtags": "3-5",
                "first_hour_target": 50,
                "best_posting_times": ["7-9 AM", "12-2 PM", "5-6 PM"],
            },
        }

    @staticmethod
    def get_component_info(component_type: str) -> Dict[str, Any]:
        """Get detailed information about a specific component"""
        components = ComponentRegistry.list_post_components()
        return components.get(component_type, {})

    @staticmethod
    def get_variant_info(post_type: str) -> Dict[str, Any]:
        """Get variant information for a post type"""
        variants = VariantResolver.get_all_variants(post_type)
        if not variants:
            return {}

        return {
            "post_type": post_type,
            "base": variants.get("base", {}),
            "variants": list(variants.get("variants", {}).keys()),
            "default": variants.get("default_variant", {}),
            "has_compounds": len(variants.get("compound_variants", [])) > 0,
        }

    @staticmethod
    def search_components(query: str) -> List[Dict[str, Any]]:
        """Search for components matching a query"""
        query = query.lower()
        results = []

        # Search post types
        for name, info in ComponentRegistry.list_post_components().items():
            if query in name.lower() or query in info.get("description", "").lower():
                results.append(
                    {
                        "type": "post_component",
                        "name": name,
                        "description": info.get("description", ""),
                        "engagement_rank": info.get("engagement_rank"),
                    }
                )

        # Search themes
        for name, info in ComponentRegistry.list_themes().items():
            if query in name.lower() or query in info.get("description", "").lower():
                results.append(
                    {
                        "type": "theme",
                        "name": name,
                        "description": info.get("description", ""),
                        "goal": info.get("goal"),
                    }
                )

        return results
