"""
Demo script showing the new document composition system.

Demonstrates atomic component composition for LinkedIn documents,
similar to the posts composition system but for visual formats.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.documents import (
    ComposableDocument,
    DocumentBuilder,
    TextBlock,
    BulletList,
    Heading,
    StatCard,
    QuoteCard,
)
from chuk_mcp_linkedin.themes import ThemeManager


def demo_basic_composition():
    """Demo basic document composition"""
    print("=" * 70)
    print("DEMO 1: Basic Document Composition")
    print("=" * 70)
    print()

    # Get a theme
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("thought_leader")

    # Create document
    doc = ComposableDocument(format_type="html", theme=theme, color_scheme="minimal")
    doc.set_metadata(
        title="Q1 2025 Results",
        author="Chris Hay",
        description="Quarterly performance report"
    )

    # Title slide
    doc.add_slide("title_slide")\
       .set_title("Q1 2025 Results")\
       .set_subtitle("Growth & Performance Highlights")

    # Content slide with components
    slide = doc.add_slide("content_slide")\
        .set_title("Key Highlights")

    slide.add_component(BulletList([
        "Revenue up 45% year-over-year",
        "10,000 new customers acquired",
        "Product launched in 5 new markets",
        "Team grew to 50 people",
    ], bullet_style="checkmark"))

    # Big stat slide with stat card
    slide = doc.add_slide("big_number")\
        .set_title("Engagement")

    slide.add_component(StatCard(
        number="45.85%",
        label="Engagement Rate",
        context="Highest of all LinkedIn formats in 2025"
    ))

    # Quote slide (layout name is "quote" not "quote_slide")
    slide = doc.add_slide("quote")
    slide.add_component(QuoteCard(
        text="This completely changed how we think about LinkedIn content",
        author="Sarah Johnson",
        source="Marketing Director, Fortune 500",
        style="centered"
    ))

    # Validate and render
    print(f"✅ Document created: {len(doc.slides)} slides")
    print(f"📊 Metadata: {doc.metadata}")
    print()

    # Render to HTML
    html = doc.render()
    print(f"✅ Rendered {len(html)} characters of HTML")
    print()

    # Save to file
    output_dir = Path(__file__).parent.parent / ".linkedin_drafts" / "previews" / "composition"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "demo_basic_composition.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"💾 Saved to: {output_path}")
    print(f"🌐 Open in browser: file://{output_path.absolute()}")
    print()

    return doc


def demo_document_builder():
    """Demo DocumentBuilder pre-built patterns"""
    print("=" * 70)
    print("DEMO 2: DocumentBuilder Pre-built Patterns")
    print("=" * 70)
    print()

    # Get theme
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("data_driven")

    # Pitch Deck Builder
    print("📊 Creating pitch deck...")
    pitch_deck = DocumentBuilder.pitch_deck(
        title="AI-Powered Analytics Platform",
        problem="Companies struggle to make sense of their data. 80% of data goes unused.",
        solution="Our AI platform turns raw data into actionable insights in real-time.",
        traction={
            "main_metric": "2.5M",
            "description": "Data points analyzed daily\n↑ 340% growth YoY"
        },
        team=[
            "Jane Doe - CEO (ex-Google)",
            "John Smith - CTO (ex-Meta)",
            "Alice Johnson - Head of AI (PhD Stanford)"
        ],
        ask="Seeking $5M Series A to scale to 100K customers",
        theme=theme,
    )

    print(f"✅ Pitch deck: {len(pitch_deck.slides)} slides")
    print()

    # Quarterly Report Builder
    print("📈 Creating quarterly report...")
    quarterly_report = DocumentBuilder.quarterly_report(
        quarter="Q1 2025",
        highlights=[
            "Revenue: $2.5M (+45% YoY)",
            "Customers: 10,000 (+120% YoY)",
            "Team: 50 people (+25 new hires)",
            "Product: 5 new markets launched"
        ],
        metrics={
            "Revenue": "$2.5M",
            "Customers": "10,000",
            "Growth": "45%",
            "Retention": "92%"
        },
        goals=[
            "Hit $5M ARR",
            "Expand to 10 new markets",
            "Launch mobile app",
            "Grow team to 75"
        ],
        theme=theme,
    )

    print(f"✅ Quarterly report: {len(quarterly_report.slides)} slides")
    print()

    # Product Launch Builder
    print("🚀 Creating product launch...")
    product_launch = DocumentBuilder.product_launch(
        product_name="LinkedIn Analytics Pro",
        tagline="Turn your LinkedIn data into growth",
        features=[
            "🎯 AI-Powered Insights",
            "📊 Real-time Analytics",
            "📈 Growth Tracking",
            "🔍 Competitor Analysis"
        ],
        benefits=[
            "Save 10 hours per week on content planning",
            "Increase engagement by 45%",
            "Identify trending topics before they peak",
            "Optimize posting times for maximum reach"
        ],
        cta="Start your free 14-day trial today\nNo credit card required",
        theme=theme,
    )

    print(f"✅ Product launch: {len(product_launch.slides)} slides")
    print()

    # Render and save all
    output_dir = Path(__file__).parent.parent / ".linkedin_drafts" / "previews" / "composition"
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, doc in [
        ("pitch_deck", pitch_deck),
        ("quarterly_report", quarterly_report),
        ("product_launch", product_launch)
    ]:
        html = doc.render()
        output_path = output_dir / f"demo_{name}.html"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"💾 {name}: {output_path}")

    print()
    print(f"🌐 All files saved to: {output_dir}")
    print()

    return pitch_deck, quarterly_report, product_launch


def demo_mixed_components():
    """Demo mixing layouts with atomic components"""
    print("=" * 70)
    print("DEMO 3: Mixing Layouts with Atomic Components")
    print("=" * 70)
    print()

    # Create document with multiple color schemes
    doc = ComposableDocument(format_type="html", color_scheme="modern")
    doc.set_metadata(title="Component Showcase")

    # Slide 1: Heading + Text
    slide = doc.add_slide("content_slide")\
        .set_title("Typography Components")

    slide.add_component(Heading("Level 1 Heading", level=1))
    slide.add_component(Heading("Level 2 Heading", level=2))
    slide.add_component(Heading("Level 3 Heading", level=3))
    slide.add_component(TextBlock(
        "This is a text block using DesignTokens. All font sizes, colors, and spacing come from the token system.",
        font_size="body",
        alignment="left"
    ))

    # Slide 2: Lists
    slide = doc.add_slide("content_slide")\
        .set_title("List Components")

    slide.add_component(BulletList(
        ["Bullet point one", "Bullet point two", "Bullet point three"],
        bullet_style="bullet"
    ))

    slide.add_component(BulletList(
        ["Completed task", "Another done", "All finished"],
        bullet_style="checkmark"
    ))

    slide.add_component(BulletList(
        ["First step", "Second step", "Third step"],
        bullet_style="numbered"
    ))

    # Slide 3: Stats
    slide = doc.add_slide("content_slide")\
        .set_title("Stat Components")

    slide.add_component(StatCard(
        "100%",
        "Design Tokens Used",
        "No hardcoded values in any component"
    ))

    # Slide 4: Quote (layout name is "quote" not "quote_slide")
    slide = doc.add_slide("quote")

    slide.add_component(QuoteCard(
        "The atomic composition pattern makes building documents as easy as building posts",
        "Document Component System",
        "chuk-mcp-linkedin",
        style="centered"
    ))

    print(f"✅ Showcase created: {len(doc.slides)} slides")
    print(f"📦 Using DesignTokens for all styling")
    print()

    # Render and save
    html = doc.render()
    output_dir = Path(__file__).parent.parent / ".linkedin_drafts" / "previews" / "composition"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "demo_mixed_components.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"💾 Saved to: {output_path}")
    print(f"🌐 Open in browser: file://{output_path.absolute()}")
    print()

    return doc


def main():
    """Run all demos"""
    print("\n")
    print("█" * 70)
    print("█  DOCUMENT COMPOSITION SYSTEM DEMO")
    print("█  Atomic Components + DesignTokens + Themes")
    print("█" * 70)
    print("\n")

    # Run demos
    demo_basic_composition()
    demo_document_builder()
    demo_mixed_components()

    print("=" * 70)
    print("✅ ALL DEMOS COMPLETE")
    print("=" * 70)
    print()
    print("Key Features Demonstrated:")
    print("  ✓ Atomic component composition (like posts)")
    print("  ✓ DesignTokens integration (no hardcoded values)")
    print("  ✓ Theme support (LinkedInTheme)")
    print("  ✓ Fluent API (method chaining)")
    print("  ✓ DocumentBuilder patterns (pitch_deck, quarterly_report, etc.)")
    print("  ✓ Component reusability (StatCard, QuoteCard)")
    print()


if __name__ == "__main__":
    main()
