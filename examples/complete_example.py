"""
Complete example demonstrating the LinkedIn MCP Design System.

Shows all major features including themes, variants, composition, and patterns.
"""

from chuk_mcp_linkedin import (
    LinkedInManager,
    ThemeManager,
    ComposablePost,
    PostBuilder,
    ComponentRegistry,
    VariantResolver,
    PostVariants,
)


def example_1_simple_text_post():
    """Example 1: Simple text post with theme"""
    print("=" * 60)
    print("Example 1: Simple Text Post with Thought Leader Theme")
    print("=" * 60)

    # Initialize managers
    manager = LinkedInManager()
    theme_mgr = ThemeManager()

    # Get thought leader theme
    theme = theme_mgr.get_theme("thought_leader")

    # Create composable post
    post = ComposablePost("text", theme=theme)

    # Add components using fluent API
    post.add_hook("stat", "80% of B2B decision makers prefer thought leadership content over ads.")
    post.add_body(
        """
Yet most companies just promote.

Here's what actually works:

Lead with insights, not products
Share frameworks, not features
Tell stories, not sales pitches
Build trust, not transactions

The algorithm rewards value.
""",
        structure="listicle",
    )
    post.add_cta("curiosity", "What's your LinkedIn strategy?")
    post.add_hashtags(["B2BMarketing", "LinkedInStrategy", "ContentMarketing"])

    # Compose final text
    final_text = post.compose()

    print(f"\n{final_text}\n")
    print(f"Character count: {len(final_text)}/3000")
    print(f"Preview (first 210 chars): {post.get_preview()}")
    print()


def example_2_story_post():
    """Example 2: Story post using PostBuilder pattern"""
    print("=" * 60)
    print("Example 2: Story Post Using Builder Pattern")
    print("=" * 60)

    theme_mgr = ThemeManager()
    theme = theme_mgr.get_theme("storyteller")

    # Use pre-built story pattern
    story = PostBuilder.story_post(
        hook="I almost quit LinkedIn in 2023.",
        problem="""After 6 months of posting, I had:
- 47 followers
- 3 likes per post
- Zero leads

It was embarrassing.""",
        journey="""Then I changed everything:

✓ Stopped promoting
✓ Started teaching
✓ Engaged authentically
✓ Focused on value""",
        solution="""Within 90 days:
- 5,000 followers
- 50+ leads per week
- Speaking opportunities

The platform rewarded the shift.""",
        lesson="LinkedIn isn't a megaphone. It's a coffee shop. Show up, add value, build relationships.",
        theme=theme,
    )

    final_text = story.compose()
    print(f"\n{final_text}\n")
    print()


def example_3_thought_leadership():
    """Example 3: Thought leadership with framework"""
    print("=" * 60)
    print("Example 3: Thought Leadership with Framework")
    print("=" * 60)

    theme_mgr = ThemeManager()
    theme = theme_mgr.get_theme("thought_leader")

    # Use thought leadership pattern
    post = PostBuilder.thought_leadership_post(
        hook_stat="90% of consultants struggle to explain their value.",
        framework_name="VALUE Framework",
        framework_parts=[
            "Visible - Make results measurable",
            "Actionable - Give clear next steps",
            "Leveraged - Show scalable impact",
            "Unique - Differentiate your approach",
            "Efficient - Prove time/cost savings",
        ],
        conclusion="Master this framework and you'll never struggle to articulate your worth again.",
        theme=theme,
    )

    final_text = post.compose()
    print(f"\n{final_text}\n")
    print()


def example_4_variants_system():
    """Example 4: Using the variant system"""
    print("=" * 60)
    print("Example 4: Variant System with Compounds")
    print("=" * 60)

    # Get text post variants
    variants = PostVariants.text_post_variants()

    # Select variants
    selected = {"style": "hot_take", "tone": "professional", "length": "micro"}

    # Resolve configuration
    config = VariantResolver.resolve(variants, selected)

    print("Selected Variants:")
    for k, v in selected.items():
        print(f"  {k}: {v}")

    print("\nResolved Configuration:")
    for k, v in config.items():
        print(f"  {k}: {v}")

    print("\nSuggested Variants for 'authority' goal:")
    suggestions = VariantResolver.suggest_variants("text", "authority")
    for k, v in suggestions.items():
        print(f"  {k}: {v}")
    print()


def example_5_component_registry():
    """Example 5: Using component registry for discovery"""
    print("=" * 60)
    print("Example 5: Component Registry & Recommendations")
    print("=" * 60)

    registry = ComponentRegistry()

    # Get system overview
    overview = registry.get_complete_system_overview()
    print("System Overview:")
    print(f"  Post Types: {overview['post_types']}")
    print(f"  Themes: {overview['themes']}")
    print(f"  Subcomponents: {overview['subcomponents']}")

    print("\nTop Performers (2025):")
    for key, value in overview["top_performers"].items():
        print(f"  {key}: {value}")

    # Get recommendations for a goal
    print("\nRecommendations for 'engagement' goal:")
    recs = registry.get_recommendations("engagement")
    print(f"  Top formats: {', '.join(recs['top_formats'])}")
    print(f"  Theme: {recs['theme']}")
    print(f"  Frequency: {recs['post_frequency']}")
    print("\n  Best practices:")
    for practice in recs["best_practices"]:
        print(f"    - {practice}")
    print()


def example_6_all_themes():
    """Example 6: Showcase all 10 themes"""
    print("=" * 60)
    print("Example 6: All 10 Pre-Built Themes")
    print("=" * 60)

    theme_mgr = ThemeManager()

    for theme_name in theme_mgr.list_themes():
        summary = theme_mgr.get_theme_summary(theme_name)
        print(f"\n{summary['name']}")
        print(f"  {summary['description']}")
        print(f"  Tone: {summary['tone']} | Goal: {summary['goal']}")
        print(f"  Frequency: {summary['post_frequency']}")
        print(f"  Best formats: {', '.join(summary['best_formats'])}")
    print()


def example_7_draft_management():
    """Example 7: Draft management"""
    print("=" * 60)
    print("Example 7: Draft Management System")
    print("=" * 60)

    manager = LinkedInManager()

    # Create multiple drafts
    draft1 = manager.create_draft("Q4 Results", "text", theme="data_driven")
    print(f"Created: {draft1.name} ({draft1.draft_id})")

    draft2 = manager.create_draft("Team Culture", "text", theme="personal_brand")
    print(f"Created: {draft2.name} ({draft2.draft_id})")

    draft3 = manager.create_draft("Product Launch", "text", theme="corporate_professional")
    print(f"Created: {draft3.name} ({draft3.draft_id})")

    # List all drafts
    print("\nAll Drafts:")
    for draft_info in manager.list_drafts():
        current = " [CURRENT]" if draft_info["is_current"] else ""
        print(f"  {draft_info['name']} ({draft_info['post_type']}){current}")

    # Switch to a draft
    manager.switch_draft(draft1.draft_id)
    print(f"\nSwitched to: {draft1.name}")

    # Get stats
    stats = manager.get_draft_stats(draft1.draft_id)
    print(f"\nDraft Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Clean up
    manager.clear_all_drafts()
    print(f"\nCleared all drafts")
    print()


def example_8_listicle_post():
    """Example 8: Listicle post"""
    print("=" * 60)
    print("Example 8: Listicle Post")
    print("=" * 60)

    theme_mgr = ThemeManager()
    theme = theme_mgr.get_theme("coach_mentor")

    post = PostBuilder.listicle_post(
        hook="5 LinkedIn mistakes I see daily:",
        items=[
            "Treating it like Facebook (it's not)",
            "Posting without a hook (first 210 chars matter)",
            "Using 10+ hashtags (3-5 is optimal)",
            "Never engaging with comments (algorithm killer)",
            "Selling before building trust (relationship first)",
        ],
        conclusion="Master these basics and you'll outperform 90% of LinkedIn users.",
        theme=theme,
    )

    final_text = post.compose()
    print(f"\n{final_text}\n")
    print()


def run_all_examples():
    """Run all examples"""
    example_1_simple_text_post()
    example_2_story_post()
    example_3_thought_leadership()
    example_4_variants_system()
    example_5_component_registry()
    example_6_all_themes()
    example_7_draft_management()
    example_8_listicle_post()


if __name__ == "__main__":
    run_all_examples()
