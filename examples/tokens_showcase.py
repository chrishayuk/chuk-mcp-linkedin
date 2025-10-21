#!/usr/bin/env python3
"""
Layout and Token Management System Showcase

Demonstrates the complete design token system and layout architecture
for LinkedIn document posts and carousels.

This example shows:
1. How design tokens centralize all visual design decisions
2. How layouts reference tokens instead of hardcoded values
3. How to use tokens for consistent, maintainable designs
4. LinkedIn-specific optimizations from 2025 performance data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.tokens import TextTokens, EngagementTokens, StructureTokens, DesignTokens


def showcase_tokens_rendered():
    """Show rendered visual examples of tokens in action"""

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  DESIGN TOKENS - RENDERED VISUAL EXAMPLES".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Typography rendering
    print("=" * 80)
    print("TYPOGRAPHY TOKENS - VISUAL RENDERING")
    print("=" * 80)
    print()

    print("Font Sizes (mobile-optimized, 18pt minimum):")
    print()
    print("  TINY (14pt)     ← Too small for mobile ✗")
    print()
    print("  SMALL (18pt)    ← Minimum for mobile ✓")
    print()
    print("  BODY (24pt)")
    print()
    print("  LARGE (32pt)")
    print()
    print("  XLARGE (42pt)")
    print()
    print("  TITLE (56pt)")
    print()
    print("  DISPLAY (72pt)")
    print()
    print("  HERO (120pt)")
    print()
    print("  MASSIVE (200pt) ← Big stat numbers")
    print()

    # Color scheme rendering
    print("=" * 80)
    print("COLOR SCHEMES - VISUAL RENDERING")
    print("=" * 80)
    print()

    print("LinkedIn Brand Colors:")
    print()
    print("  █████ LinkedIn Blue (#0A66C2)")
    print("  █████ Dark Blue (#004182)")
    print("  █████ Light Blue (#378FE9)")
    print()

    print("Semantic Colors (for status indicators):")
    print()
    print("  ✓ ███ SUCCESS (#10B981) - Positive outcomes")
    print("  ℹ ███ INFO (#3B82F6) - Informational")
    print("  ⚠ ███ WARNING (#F59E0B) - Caution needed")
    print("  ✗ ███ ERROR (#EF4444) - Critical issues")
    print()

    # Spacing rendering
    print("=" * 80)
    print("SPACING TOKENS - VISUAL RENDERING")
    print("=" * 80)
    print()

    print("Gaps (between elements):")
    print()
    print("  tiny (8px):   ║█║  ← Minimal spacing")
    print("  small (16px): ║█    ║")
    print("  medium (24px):║█        ║")
    print("  large (40px): ║█                ║")
    print("  xlarge (60px):║█                            ║")
    print()

    print("Safe Areas (margins around content):")
    print()
    print("  Minimal (40px):     ┌────────────────┐")
    print("                      │    Content     │")
    print("                      └────────────────┘")
    print()
    print("  Comfortable (100px):    ┌──────────┐")
    print("                          │ Content  │")
    print("                          └──────────┘")
    print()

    # Layout properties rendering
    print("=" * 80)
    print("LAYOUT PROPERTIES - VISUAL RENDERING")
    print("=" * 80)
    print()

    print("Border Radius:")
    print()
    print("  none:     ┌────┐")
    print("  small:    ╭────╮")
    print("  medium:   ╭────╮")
    print("  large:    ╭────╮")
    print("  round:    ( ● )")
    print()

    print("Shadow Elevations:")
    print()
    print("  none:  ┌────┐")
    print()
    print("  sm:    ┌────┐")
    print("          ░░░░")
    print()
    print("  md:    ┌────┐")
    print("           ░░░░")
    print()
    print("  lg:    ┌────┐")
    print("            ░░░░░")
    print()

    # LinkedIn-specific optimizations
    print("=" * 80)
    print("LINKEDIN 2025 OPTIMIZATIONS - VISUAL GUIDE")
    print("=" * 80)
    print()

    print("Document Posts (45.85% engagement - HIGHEST):")
    print()
    print("  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐")
    print("  │ Slide 1     │  │ Slide 2     │  │ Slide 3     │")
    print("  │  1920x1920  │  │  1920x1920  │  │  1920x1920  │")
    print("  │  18pt min   │  │  18pt min   │  │  18pt min   │")
    print("  └─────────────┘  └─────────────┘  └─────────────┘")
    print()
    print("  Sweet spot: 5-10 slides")
    print()

    print("'See More' Line (appears at 210 characters):")
    print()
    print("  ┌────────────────────────────────────────────────────┐")
    print("  │ First 210 characters are visible...               │")
    print("  │ This is the hook - make it count!                 │")
    print("  │                                    ... See more ▼ │")
    print("  └────────────────────────────────────────────────────┘")
    print()

    print("=" * 80)
    print()


def showcase_design_tokens():
    """Demonstrate the complete design token system"""

    print("=" * 80)
    print("DESIGN TOKEN SYSTEM - TECHNICAL DETAILS")
    print("=" * 80)
    print()

    # ==========================================
    # 1. CANVAS SIZES
    # ==========================================
    print("1. CANVAS SIZES")
    print("-" * 40)
    print("Document Post (PDF):     ", DesignTokens.CANVAS["document_square"])
    print("Carousel (Square):       ", DesignTokens.CANVAS["square"])
    print("Carousel (Portrait):     ", DesignTokens.CANVAS["portrait"])
    print()
    print("Best Practice: Document posts use 1920x1920 for maximum quality")
    print("              Carousels use 1080x1080 for optimal mobile viewing")
    print()

    # ==========================================
    # 2. TYPOGRAPHY TOKENS
    # ==========================================
    print("2. TYPOGRAPHY TOKENS")
    print("-" * 40)
    print("Font Families:")
    for name, family in DesignTokens.TYPOGRAPHY["fonts"].items():
        print(f"  {name:10} → {family}")
    print()

    print("Font Sizes (optimized for LinkedIn mobile):")
    for name, size in DesignTokens.TYPOGRAPHY["sizes"].items():
        mobile_ok = "✓" if size >= 18 else "✗"
        print(f"  {name:10} → {size:3}pt  {mobile_ok}")
    print()
    print("Note: 18pt minimum for mobile readability (LinkedIn requirement)")
    print()

    print("Font Weights:")
    for name, weight in DesignTokens.TYPOGRAPHY["weights"].items():
        print(f"  {name:10} → {weight}")
    print()

    print("Line Heights:")
    for name, height in DesignTokens.TYPOGRAPHY["line_heights"].items():
        print(f"  {name:10} → {height}")
    print()

    # ==========================================
    # 3. COLOR SCHEMES
    # ==========================================
    print("3. COLOR SCHEMES")
    print("-" * 40)
    schemes = ["minimal", "modern", "vibrant", "dark"]
    for scheme in schemes:
        print(f"{scheme.upper()} Scheme:")
        for color_name, color_value in DesignTokens.COLORS[scheme].items():
            print(f"  {color_name:15} → {color_value}")
        print()

    print("LinkedIn Brand Colors:")
    for name, color in DesignTokens.COLORS["linkedin"].items():
        print(f"  {name:15} → {color}")
    print()

    print("Semantic Colors (for comparisons, alerts, etc.):")
    for name, color in DesignTokens.COLORS["semantic"].items():
        print(f"  {name:15} → {color}")
    print()

    # ==========================================
    # 4. SPACING TOKENS
    # ==========================================
    print("4. SPACING TOKENS")
    print("-" * 40)
    print("Safe Areas (margins):")
    for size, margins in DesignTokens.SPACING["safe_area"].items():
        print(f"  {size:12} → {margins}")
    print()

    print("Gaps (between elements):")
    for size, gap in DesignTokens.SPACING["gaps"].items():
        print(f"  {size:10} → {gap}px")
    print()

    print("Padding (internal spacing):")
    for size, padding in DesignTokens.SPACING["padding"].items():
        print(f"  {size:10} → {padding}px")
    print()

    # ==========================================
    # 5. LAYOUT PROPERTIES
    # ==========================================
    print("5. LAYOUT PROPERTIES")
    print("-" * 40)
    print("Alignment Options:")
    print(f"  Horizontal: {', '.join(DesignTokens.LAYOUT['align']['horizontal'])}")
    print(f"  Vertical:   {', '.join(DesignTokens.LAYOUT['align']['vertical'])}")
    print()

    print("Border Radius:")
    for name, radius in DesignTokens.LAYOUT["border_radius"].items():
        print(f"  {name:10} → {radius}px")
    print()

    print("Grid Configurations:")
    for config_type, config in DesignTokens.LAYOUT["grid"].items():
        print(f"  {config_type}:")
        for name, value in config.items():
            print(f"    {name:10} → {value}")
    print()

    # ==========================================
    # 6. LINKEDIN-SPECIFIC TOKENS
    # ==========================================
    print("6. LINKEDIN-SPECIFIC TOKENS (2025 Best Practices)")
    print("-" * 40)
    print("Document Post Slide Counts:")
    for metric, count in DesignTokens.LINKEDIN_SPECIFIC["document_slides"].items():
        print(f"  {metric:15} → {count} slides")
    print()
    print("🔥 Sweet spot: 5-10 slides for maximum engagement (45.85% rate)")
    print()

    print("Carousel Recommendations:")
    for metric, count in DesignTokens.LINKEDIN_SPECIFIC["carousel_slides"].items():
        print(f"  {metric:15} → {count} slides")
    print()
    print("⚠️  Carousels declining in 2025 (-18% reach, -25% engagement)")
    print("   Keep tight and tactical if using")
    print()

    print("Mobile-First Requirements:")
    for requirement, value in DesignTokens.LINKEDIN_SPECIFIC["mobile"].items():
        print(f"  {requirement:25} → {value}")
    print()

    # ==========================================
    # 7. TEXT CONTENT TOKENS
    # ==========================================
    print("7. TEXT CONTENT TOKENS")
    print("-" * 40)
    print(f"Max post length:        {TextTokens.MAX_LENGTH} characters")
    print(f"'See more' appears at:  {TextTokens.TRUNCATION_POINT} characters")
    print()

    print("Ideal Post Lengths:")
    for length_type, (min_chars, max_chars) in TextTokens.IDEAL_LENGTH.items():
        print(f"  {length_type:10} → {min_chars:4}-{max_chars:4} chars")
    print()

    print("Emoji Levels (% of text that should be emoji):")
    for level, percentage in TextTokens.EMOJI.items():
        emoji_per_100 = int(percentage * 100)
        print(f"  {level:12} → {emoji_per_100:2}%  (~{emoji_per_100//10} per 100 words)")
    print()

    print("Hashtag Strategy:")
    print(f"  Optimal count: {TextTokens.HASHTAGS['count']['optimal']}")
    print(f"  Placement:     {', '.join(TextTokens.HASHTAGS['placement'].keys())}")
    print()

    # ==========================================
    # 8. ENGAGEMENT TOKENS
    # ==========================================
    print("8. ENGAGEMENT TOKENS (Algorithm Optimization)")
    print("-" * 40)
    print("Hook Types (ranked by power):")
    hooks_sorted = sorted(EngagementTokens.HOOKS.items(), key=lambda x: x[1]["power"], reverse=True)
    for hook_type, hook_data in hooks_sorted:
        power_bar = "█" * int(hook_data["power"] * 10)
        print(f"  {hook_type:15} → {hook_data['power']:.2f} {power_bar}")
    print()

    print("🚨 Controversy hooks have highest power (0.95) but use wisely!")
    print("📊 Stats/data hooks are safest high-performers (0.90)")
    print()

    print("Best Posting Times (2025 data):")
    print(f"  Best days:  {', '.join(EngagementTokens.TIMING['best_days'])}")
    print(f"  Best hours: {EngagementTokens.TIMING['best_hours']}")
    print(f"  Frequency:  {EngagementTokens.TIMING['posting_frequency']['optimal']} posts/week")
    print()

    print("First Hour Engagement Targets:")
    for target, count in EngagementTokens.FIRST_HOUR_TARGETS.items():
        print(f"  {target:10} → {count:3} engagements")
    print()
    print("⚡ First hour determines algorithmic reach!")
    print()

    # ==========================================
    # 9. TOKEN HELPER METHODS
    # ==========================================
    print("9. TOKEN HELPER METHODS")
    print("-" * 40)
    print("Design tokens provide helper methods for easy access:")
    print()

    # Demo helper methods
    canvas = DesignTokens.get_canvas_size("document_square")
    print(f"  get_canvas_size('document_square')  → {canvas}")

    font_size = DesignTokens.get_font_size("title")
    print(f"  get_font_size('title')              → {font_size}pt")

    color = DesignTokens.get_color("minimal", "accent")
    print(f"  get_color('minimal', 'accent')      → {color}")

    safe_area = DesignTokens.get_safe_area("comfortable")
    print(f"  get_safe_area('comfortable')        → {safe_area}")
    print()

    # ==========================================
    # SUMMARY
    # ==========================================
    print("=" * 80)
    print("SUMMARY: Why Token-Based Design Matters")
    print("=" * 80)
    print()
    print("✓ CONSISTENCY: All designs use same values → cohesive visual identity")
    print("✓ MAINTAINABILITY: Change once, update everywhere")
    print("✓ PERFORMANCE: Values based on 1M+ posts analyzed in 2025")
    print("✓ MOBILE-FIRST: All tokens optimized for mobile viewing")
    print("✓ ACCESSIBILITY: Minimum font sizes, touch targets, contrast")
    print("✓ PLATFORM-AWARE: LinkedIn-specific optimizations built-in")
    print()
    print("Instead of hardcoding:")
    print("  ❌ font_size = 24")
    print("  ❌ color = '#000000'")
    print("  ❌ margin = 60")
    print()
    print("Use tokens:")
    print("  ✓ font_size = DesignTokens.get_font_size('body')")
    print("  ✓ color = DesignTokens.get_color('minimal', 'primary')")
    print("  ✓ margin = DesignTokens.get_spacing('gaps', 'large')")
    print()


def demo_layout_with_tokens():
    """Demonstrate how layouts use tokens"""

    print("=" * 80)
    print("LAYOUT ARCHITECTURE WITH TOKENS")
    print("=" * 80)
    print()

    print("Layouts reference tokens, not hardcoded values:")
    print()
    print("Example: Content Slide Layout")
    print("-" * 40)
    print()

    # Show how a layout would be structured using tokens
    print("Python Code:")
    print(
        """
layout = LayoutConfig(
    name="Content Slide",
    canvas_size=DesignTokens.get_canvas_size("document_square"),
    safe_area=DesignTokens.get_safe_area("comfortable"),

    title_zone=LayoutZone(
        x=100, y=100, width=1720, height=200,
        font_size=DesignTokens.get_font_size("title"),
        font_weight=DesignTokens.TYPOGRAPHY["weights"]["bold"],
        color=DesignTokens.get_color("minimal", "primary"),
    ),

    content_zone=LayoutZone(
        x=100, y=350, width=1720, height=1350,
        font_size=DesignTokens.get_font_size("body"),
        line_height=DesignTokens.TYPOGRAPHY["line_heights"]["relaxed"],
    ),
)
"""
    )
    print()

    print("Benefits:")
    print("  • Change DesignTokens.TYPOGRAPHY['sizes']['title'] = 72")
    print("  • All layouts using 'title' size update automatically")
    print("  • No need to search/replace hardcoded values")
    print()


def showcase_all_layouts():
    """Showcase all 11 document layouts with visual representations"""

    from chuk_mcp_linkedin.documents.layouts import DocumentLayouts

    print("=" * 80)
    print("ALL DOCUMENT LAYOUTS (11 TYPES)")
    print("=" * 80)
    print()
    print("Document posts have 45.85% engagement rate - HIGHEST of all formats!")
    print("Optimal: 5-10 slides per document | Format: 1920x1920 square")
    print()

    layouts = DocumentLayouts.get_all()

    for i, (layout_name, layout) in enumerate(layouts.items(), 1):
        print(f"\n{i}. {layout.name.upper()}")
        print("=" * 80)
        print(f"Type:        {layout.type.value}")
        print(f"Description: {layout.description}")
        print(f"Canvas:      {layout.canvas_size[0]}x{layout.canvas_size[1]}px")
        print()

        # Best for section
        if layout.best_for:
            print(f"Best For:    {', '.join(layout.best_for)}")
        if layout.use_cases:
            print(f"Use Cases:   {', '.join(layout.use_cases)}")
        print()

        # Visual representation
        print("Layout Structure:")
        print("-" * 40)
        _print_layout_visual(layout)
        print()

        # Zone details
        print("Zones:")
        if layout.title_zone:
            print(
                f"  Title:     {layout.title_zone.width}x{layout.title_zone.height}px at ({layout.title_zone.x}, {layout.title_zone.y})"
            )
            print(
                f"             Font: {layout.title_zone.font_size}pt {layout.title_zone.font_weight}"
            )

        if layout.subtitle_zone:
            print(
                f"  Subtitle:  {layout.subtitle_zone.width}x{layout.subtitle_zone.height}px at ({layout.subtitle_zone.x}, {layout.subtitle_zone.y})"
            )
            print(f"             Font: {layout.subtitle_zone.font_size}pt")

        if layout.content_zone:
            print(
                f"  Content:   {layout.content_zone.width}x{layout.content_zone.height}px at ({layout.content_zone.x}, {layout.content_zone.y})"
            )
            print(
                f"             Font: {layout.content_zone.font_size}pt, line-height: {layout.content_zone.line_height}"
            )
            if layout.content_zone.properties:
                for key, value in layout.content_zone.properties.items():
                    print(f"             {key}: {value}")

        if layout.content_zone_2:
            print(
                f"  Content 2: {layout.content_zone_2.width}x{layout.content_zone_2.height}px at ({layout.content_zone_2.x}, {layout.content_zone_2.y})"
            )
            if layout.content_zone_2.properties:
                for key, value in layout.content_zone_2.properties.items():
                    print(f"             {key}: {value}")

        if layout.image_zone:
            print(
                f"  Image:     {layout.image_zone.width}x{layout.image_zone.height}px at ({layout.image_zone.x}, {layout.image_zone.y})"
            )

        if layout.branding_zone:
            print(
                f"  Branding:  {layout.branding_zone.width}x{layout.branding_zone.height}px at ({layout.branding_zone.x}, {layout.branding_zone.y})"
            )
        print()

        # Usage example
        print("Usage Example:")
        print("-" * 40)
        _print_usage_example(layout_name, layout)
        print()


def _print_layout_visual(layout):
    """Print ASCII visual representation of layout"""

    # Simple ASCII art representation based on layout type
    visuals = {
        "title_slide": """
        ┌────────────────────────────────────────┐
        │                                        │
        │                                        │
        │          LARGE CENTERED TITLE          │
        │              Subtitle                  │
        │                                        │
        │                                        │
        │                                        │
        │                                        │
        │  [Logo]                                │
        └────────────────────────────────────────┘
        """,
        "content_slide": """
        ┌────────────────────────────────────────┐
        │  Slide Title                           │
        │  ────────────────────────────────────  │
        │                                        │
        │  • Bullet point one                    │
        │  • Bullet point two                    │
        │  • Bullet point three                  │
        │  • Bullet point four                   │
        │  • Bullet point five                   │
        │                                        │
        │                            [Logo]      │
        └────────────────────────────────────────┘
        """,
        "split_content": """
        ┌────────────────────────────────────────┐
        │           Section Title                │
        │  ────────────────────────────────────  │
        │                        │               │
        │  Text content goes     │               │
        │  here on the left      │    Image or   │
        │  side with bullets     │    Visual     │
        │  or paragraphs         │    Content    │
        │                        │               │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "big_number": """
        ┌────────────────────────────────────────┐
        │                                        │
        │                                        │
        │                                        │
        │              45.85%                    │
        │                                        │
        │        Engagement Rate Increase        │
        │                                        │
        │                                        │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "quote": """
        ┌────────────────────────────────────────┐
        │                                        │
        │                                        │
        │    "This is a powerful quote that      │
        │     captures attention and makes       │
        │     your point memorable"              │
        │                                        │
        │              - Attribution             │
        │                                        │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "comparison": """
        ┌────────────────────────────────────────┐
        │              A vs B                    │
        │  ────────────────────────────────────  │
        │   ❌ Option A      │  ✅ Option B      │
        │                    │                   │
        │  • Wrong way       │  • Right way      │
        │  • Old method      │  • New method     │
        │  • Bad practice    │  • Best practice  │
        │                    │                   │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "two_column": """
        ┌────────────────────────────────────────┐
        │           Two Columns                  │
        │  ────────────────────────────────────  │
        │                    │                   │
        │  Left Column       │  Right Column     │
        │  • Point 1         │  • Point 1        │
        │  • Point 2         │  • Point 2        │
        │  • Point 3         │  • Point 3        │
        │                    │                   │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "checklist": """
        ┌────────────────────────────────────────┐
        │  Action Items Checklist                │
        │  ────────────────────────────────────  │
        │                                        │
        │  ☐ First action item to complete       │
        │                                        │
        │  ☐ Second action item                  │
        │                                        │
        │  ☐ Third action item                   │
        │                                        │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "timeline": """
        ┌────────────────────────────────────────┐
        │           Timeline Title               │
        │  ────────────────────────────────────  │
        │                                        │
        │  Jan ──●── Product Launch              │
        │        │                               │
        │  Mar ──●── Hit 1K Users                │
        │        │                               │
        │  Jun ──●── Series A Funding            │
        │                                        │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "icon_grid": """
        ┌────────────────────────────────────────┐
        │         Features Overview              │
        │  ────────────────────────────────────  │
        │                                        │
        │   🚀 Feature 1    │   ⚡ Feature 2    │
        │   Description     │   Description     │
        │                   │                   │
        │   💡 Feature 3    │   🎯 Feature 4    │
        │   Description     │   Description     │
        │                                        │
        │            [Logo]                      │
        └────────────────────────────────────────┘
        """,
        "data_visual": """
        ┌────────────────────────────────────────┐
        │  Chart Title                           │
        │  ────────────────────────────────────  │
        │                                        │
        │     ┌────────────────────────┐         │
        │     │                        │         │
        │     │    Chart/Graph Area    │         │
        │     │                        │         │
        │     └────────────────────────┘         │
        │                                        │
        │  Source: Data caption here             │
        └────────────────────────────────────────┘
        """,
    }

    visual = visuals.get(layout.type.value.replace("_", "_"), "        [Layout visualization]")
    print(visual)


def _print_usage_example(layout_name, layout):
    """Print usage example for each layout"""

    examples = {
        "title_slide": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.title_slide()
content = {
    "title": "Q4 2024 Results",
    "subtitle": "Growth & Performance Highlights"
}
""",
        "content_slide": '''
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.content_slide()
content = {
    "title": "What Actually Works",
    "body": """
• Lead with insights, not products
• Share frameworks, not features
• Tell stories, not sales pitches
• Build trust, not transactions
• Focus on value delivery
"""
}
''',
        "split_content": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.split_content()
content = {
    "title": "Before vs After",
    "body": "Text explanation of the transformation",
    "image": "path/to/visual.png"
}
""",
        "big_number": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.big_number()
content = {
    "title": "45.85%",
    "subtitle": "Engagement rate for document posts\\n(highest of all formats in 2025)"
}
""",
        "quote": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.quote_slide()
content = {
    "body": "This completely changed how we think about LinkedIn content",
    "subtitle": "- Marketing Director, Fortune 500 Company"
}
""",
        "comparison": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.comparison()
content = {
    "title": "Traditional vs Modern Approach",
    "option_a": "• Post and ghost\\n• Self-promotion\\n• Sales pitches",
    "option_b": "• Consistent engagement\\n• Value-first content\\n• Authentic conversations"
}
""",
        "two_column": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.two_column()
content = {
    "title": "Pros and Cons",
    "left": "• Advantage 1\\n• Advantage 2\\n• Advantage 3",
    "right": "• Limitation 1\\n• Limitation 2\\n• Limitation 3"
}
""",
        "checklist": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.checklist()
content = {
    "title": "Pre-Launch Checklist",
    "items": [
        "Test all functionality",
        "Prepare marketing materials",
        "Set up analytics tracking",
        "Schedule announcement posts",
        "Brief support team"
    ]
}
""",
        "timeline": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.timeline()
content = {
    "title": "2024 Milestones",
    "events": [
        {"date": "Jan", "event": "Product Launch"},
        {"date": "Mar", "event": "Hit 1K Users"},
        {"date": "Jun", "event": "Series A $5M"},
        {"date": "Sep", "event": "Team of 25"}
    ]
}
""",
        "icon_grid": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts

layout = DocumentLayouts.icon_grid()
content = {
    "title": "Core Features",
    "items": [
        {"icon": "🚀", "title": "Fast", "desc": "Lightning quick"},
        {"icon": "⚡", "title": "Powerful", "desc": "Full featured"},
        {"icon": "💡", "title": "Smart", "desc": "AI-powered"},
        {"icon": "🎯", "title": "Precise", "desc": "Data-driven"}
    ]
}
""",
        "data_visual": """
from chuk_mcp_linkedin.components.layouts import DocumentLayouts
from chuk_mcp_linkedin.charts import ChartComponents

layout = DocumentLayouts.data_visual()
chart = ChartComponents.bar_chart(
    title="Quarterly Revenue",
    labels=["Q1", "Q2", "Q3", "Q4"],
    values=[120, 150, 90, 180]
)
content = {
    "title": "2024 Performance",
    "chart": chart,
    "caption": "Source: Internal analytics"
}
""",
    }

    example = examples.get(layout_name, f"# Use DocumentLayouts.{layout_name}()")
    print(example.strip())


def show_2025_optimizations():
    """Show LinkedIn 2025-specific optimizations in tokens"""

    print("=" * 80)
    print("2025 LINKEDIN OPTIMIZATIONS")
    print("=" * 80)
    print()

    print("Based on analysis of 1M+ posts across 9K company pages:")
    print()

    # Document posts
    print("📄 DOCUMENT POSTS (PDF Carousels)")
    print("-" * 40)
    print("Engagement Rate:  45.85% (HIGHEST OF ALL FORMATS)")
    print("Optimal Slides:   5-10 slides")
    print("Font Size Min:    18pt (mobile requirement)")
    print("Format:           1920x1920 square")
    print()
    print("Token Support:")
    print(
        f"  • DesignTokens.CANVAS['document_square']           → {DesignTokens.CANVAS['document_square']}"
    )
    print(
        f"  • DesignTokens.LINKEDIN_SPECIFIC['document_slides'] → {DesignTokens.LINKEDIN_SPECIFIC['document_slides']}"
    )
    print(
        f"  • DesignTokens.LINKEDIN_SPECIFIC['mobile']          → min font {DesignTokens.LINKEDIN_SPECIFIC['mobile']['min_font_size']}pt"
    )
    print()

    # Polls
    print("📊 POLL POSTS")
    print("-" * 40)
    print("Reach Multiplier: 3.0x (200%+ higher reach!)")
    print("Status:           Most underused format (opportunity!)")
    print()
    print("Token Support:")
    print(
        f"  • EngagementTokens.HOOKS['question']['power']       → {EngagementTokens.HOOKS['question']['power']}"
    )
    print()

    # Carousels
    print("🎠 CAROUSEL POSTS")
    print("-" * 40)
    print("Reach Change:     -18% (declining)")
    print("Engagement:       -25% (vs 2024)")
    print("Recommendation:   Keep to 5-10 slides if using")
    print()
    print("Token Support:")
    print(
        f"  • DesignTokens.LINKEDIN_SPECIFIC['carousel_slides'] → max {DesignTokens.LINKEDIN_SPECIFIC['carousel_slides']['optimal_max']}"
    )
    print()

    # Timing
    print("⏰ TIMING OPTIMIZATION")
    print("-" * 40)
    print(f"Best Days:        {', '.join(EngagementTokens.TIMING['best_days']).title()}")
    print(f"Best Times:       {EngagementTokens.TIMING['best_hours']}")
    print(
        f"First Hour:       Critical for algorithm (target: {EngagementTokens.FIRST_HOUR_TARGETS['good']}+ engagements)"
    )
    print()


if __name__ == "__main__":
    # Show rendered visual examples first
    showcase_tokens_rendered()
    print("\n\n")

    # Then technical details
    showcase_design_tokens()
    print("\n\n")

    demo_layout_with_tokens()
    print("\n\n")

    showcase_all_layouts()
    print("\n\n")

    show_2025_optimizations()

    print("\n" + "=" * 80)
    print("SHOWCASE COMPLETE")
    print("=" * 80)
    print()
    print("You've seen:")
    print("  ✓ Rendered visual examples of tokens in action")
    print("  ✓ Complete design token system (typography, colors, spacing)")
    print("  ✓ How layouts reference tokens")
    print("  ✓ All 11 document layout types with visuals")
    print("  ✓ 2025 LinkedIn performance optimizations")
    print()
    print("For more examples, see:")
    print("  • components_showcase.py - Visual components rendering")
    print("  • preview_example.py     - HTML preview generation")
    print("  • complete_example.py    - Comprehensive usage")
    print("=" * 80)
