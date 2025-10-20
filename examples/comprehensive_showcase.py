#!/usr/bin/env python3
"""
Comprehensive Component Showcase

Demonstrates ALL implemented components with rendered HTML output:
- Visual Elements (38 variants)
- Typography (31 variants)
- Data Visualization (22 variants)

Generates interactive HTML preview files.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.components.visual_elements import (
    Dividers,
    Backgrounds,
    Borders,
    Badges,
    Shapes,
)
from chuk_mcp_linkedin.components.typography import (
    Headers,
    BodyText,
    Captions,
    Quotes,
    Lists,
)
from chuk_mcp_linkedin.components.data_viz import (
    Charts,
    Metrics,
    Progress,
    Tables,
    Infographics,
)
from chuk_mcp_linkedin.renderer import ShowcaseRenderer


def create_visual_elements_showcase():
    """Create visual elements showcase section"""
    return [
        {
            "title": "Dividers",
            "description": "Line separators, gradients, and section breaks",
            "components": [
                {
                    "name": "Horizontal Line",
                    "description": "Simple line separator with customizable style",
                    "component": Dividers.horizontal_line(thickness=2, style="solid"),
                },
                {
                    "name": "Gradient Fade",
                    "description": "Subtle gradient divider for elegant transitions",
                    "component": Dividers.gradient_fade(),
                },
                {
                    "name": "Decorative Accent",
                    "description": "Short accent line for visual interest",
                    "component": Dividers.decorative_accent(),
                },
                {
                    "name": "Section Break",
                    "description": "Dots separator for content sections",
                    "component": Dividers.section_break(),
                },
                {
                    "name": "Title Underline",
                    "description": "Underline for headers and titles",
                    "component": Dividers.title_underline(width="40%"),
                },
            ],
        },
        {
            "title": "Badges",
            "description": "Pills, status indicators, and tags",
            "components": [
                {
                    "name": "Pill Badge",
                    "description": "Rounded badge for labels and tags",
                    "component": Badges.pill_badge("NEW"),
                },
                {
                    "name": "Status Badge",
                    "description": "Semantic status indicator",
                    "component": Badges.status_badge("new"),
                },
                {
                    "name": "Percentage Change",
                    "description": "Shows increase/decrease with color coding",
                    "component": Badges.percentage_change(12.5),
                },
                {
                    "name": "Category Tag",
                    "description": "Tag for categorization",
                    "component": Badges.category_tag("#DesignSystem"),
                },
            ],
        },
        {
            "title": "Borders",
            "description": "Borders, frames, and containers",
            "components": [
                {
                    "name": "Simple Border",
                    "description": "Basic border around content",
                    "component": Borders.simple_border(),
                },
                {
                    "name": "Accent Border (Left)",
                    "description": "Bold left border for callouts",
                    "component": Borders.accent_border(side="left"),
                },
                {
                    "name": "Callout Box (Success)",
                    "description": "Success message container",
                    "component": Borders.callout_box(style="success"),
                },
                {
                    "name": "Callout Box (Warning)",
                    "description": "Warning message container",
                    "component": Borders.callout_box(style="warning"),
                },
            ],
        },
        {
            "title": "Shapes",
            "description": "Icons, bullets, and decorative elements",
            "components": [
                {
                    "name": "Checkmark",
                    "description": "Success indicator",
                    "component": Shapes.checkmark(size=32),
                },
                {
                    "name": "Arrows",
                    "description": "Directional indicators",
                    "component": Shapes.arrow(direction="right", size=24),
                },
                {
                    "name": "Icon Container",
                    "description": "Rounded container for icons",
                    "component": Shapes.icon_container("🚀", size=64),
                },
                {
                    "name": "Bullet Points",
                    "description": "Custom list bullets",
                    "component": Shapes.bullet_point(style="arrow"),
                },
            ],
        },
    ]


def create_typography_showcase():
    """Create typography showcase section"""
    return [
        {
            "title": "Headers",
            "description": "7 header variants for titles and headings",
            "components": [
                {
                    "name": "H1 - Display Header",
                    "description": "72pt, 900 weight - Main slide titles",
                    "component": Headers.h1("Q4 2024 Results"),
                },
                {
                    "name": "H2 - Large Header",
                    "description": "56pt - Section headers",
                    "component": Headers.h2("Performance Overview"),
                },
                {
                    "name": "H3 - Medium Header",
                    "description": "42pt - Subsection headers",
                    "component": Headers.h3("Key Metrics"),
                },
                {
                    "name": "Eyebrow Text",
                    "description": "18pt uppercase - Labels above headers",
                    "component": Headers.eyebrow("NEW FEATURE", transform="uppercase"),
                },
            ],
        },
        {
            "title": "Body Text",
            "description": "7 body text variants for content",
            "components": [
                {
                    "name": "Paragraph",
                    "description": "24pt, 1.8 line height - Standard body text",
                    "component": BodyText.paragraph(
                        "This is standard paragraph text optimized for LinkedIn mobile viewing with relaxed line height."
                    ),
                },
                {
                    "name": "Lead Text",
                    "description": "32pt - Introductory text",
                    "component": BodyText.lead_text(
                        "This is lead text used for important introductions."
                    ),
                },
                {
                    "name": "Highlighted Text",
                    "description": "Background highlight for emphasis",
                    "component": BodyText.highlighted(
                        "Important information highlighted for attention"
                    ),
                },
                {
                    "name": "Emphasized Text",
                    "description": "Italic emphasis",
                    "component": BodyText.emphasized("Emphasized italic text"),
                },
                {
                    "name": "Link",
                    "description": "Clickable link",
                    "component": BodyText.link("Learn more", url="https://example.com"),
                },
                {
                    "name": "Code",
                    "description": "Inline code formatting",
                    "component": BodyText.code("const result = true;"),
                },
            ],
        },
        {
            "title": "Captions",
            "description": "6 caption variants for metadata and sources",
            "components": [
                {
                    "name": "Caption",
                    "description": "18pt - Image and chart captions",
                    "component": Captions.caption("Figure 1: Engagement metrics over time"),
                },
                {
                    "name": "Data Source",
                    "description": "Italic source attribution",
                    "component": Captions.data_source("Source: Internal Analytics, Q4 2024"),
                },
                {
                    "name": "Metadata",
                    "description": "With icon support",
                    "component": Captions.metadata("Last updated: January 2025", icon="📅"),
                },
            ],
        },
        {
            "title": "Quotes",
            "description": "4 quote variants for testimonials and pull quotes",
            "components": [
                {
                    "name": "Pull Quote",
                    "description": "42pt serif italic - Standout quotes",
                    "component": Quotes.pull_quote(
                        "This product completely transformed how we work",
                        author="Sarah Johnson, CEO",
                    ),
                },
                {
                    "name": "Testimonial",
                    "description": "With author, role, company, and rating",
                    "component": Quotes.testimonial(
                        text="Amazing results in just 30 days! Our team productivity increased by 40%.",
                        author="John Smith",
                        role="Marketing Director",
                        company="Acme Corporation",
                        rating=5.0,
                    ),
                },
                {
                    "name": "Blockquote",
                    "description": "Standard quote format",
                    "component": Quotes.blockquote(
                        "The best investment we made this year", author="Jane Doe"
                    ),
                },
            ],
        },
        {
            "title": "Lists",
            "description": "7 list variants for organized content",
            "components": [
                {
                    "name": "Bulleted List (Arrow)",
                    "description": "Arrow-style bullets",
                    "component": Lists.bulleted_list(
                        [
                            "Document posts: 45.85% engagement",
                            "Poll posts: 200%+ higher reach",
                            "Video posts: 1.4x engagement",
                        ],
                        bullet_style="arrow",
                    ),
                },
                {
                    "name": "Numbered List",
                    "description": "Sequential numbered items",
                    "component": Lists.numbered_list(
                        ["First step: Research", "Second step: Plan", "Third step: Execute"]
                    ),
                },
                {
                    "name": "Checklist",
                    "description": "Checkable task list",
                    "component": Lists.checklist(
                        [
                            {"text": "Complete Phase 1", "checked": True},
                            {"text": "Complete Phase 2", "checked": True},
                            {"text": "Complete Phase 3", "checked": False},
                        ]
                    ),
                },
                {
                    "name": "Icon List",
                    "description": "Custom icon per item",
                    "component": Lists.icon_list(
                        [
                            {"icon": "🚀", "text": "Fast performance"},
                            {"icon": "⚡", "text": "Powerful features"},
                            {"icon": "💡", "text": "Smart automation"},
                        ]
                    ),
                },
            ],
        },
    ]


def create_data_viz_showcase():
    """Create data visualization showcase section"""
    return [
        {
            "title": "Charts",
            "description": "8 chart variants for data visualization",
            "components": [
                {
                    "name": "Bar Chart",
                    "description": "Vertical bars for comparisons",
                    "component": Charts.bar_chart(
                        [
                            {"label": "Q1 2024", "value": 100},
                            {"label": "Q2 2024", "value": 150},
                            {"label": "Q3 2024", "value": 120},
                            {"label": "Q4 2024", "value": 180},
                        ],
                        show_values=True,
                    ),
                },
                {
                    "name": "Pie Chart",
                    "description": "Proportional segments",
                    "component": Charts.pie_chart(
                        [
                            {"label": "Product A", "value": 45},
                            {"label": "Product B", "value": 30},
                            {"label": "Product C", "value": 25},
                        ]
                    ),
                },
            ],
        },
        {
            "title": "Metrics",
            "description": "5 metric variants for KPIs",
            "components": [
                {
                    "name": "Metric Card",
                    "description": "Card with value, label, and change indicator",
                    "component": Metrics.metric_card(
                        label="Monthly Revenue",
                        value="$1.2M",
                        change=12.5,
                        icon="💰",
                    ),
                },
                {
                    "name": "Big Stat",
                    "description": "200pt massive number for impact",
                    "component": Metrics.big_stat(
                        value="45.85%",
                        label="Engagement Rate",
                        context="Highest of all formats in 2025",
                    ),
                },
            ],
        },
        {
            "title": "Progress",
            "description": "5 progress variants for tracking",
            "components": [
                {
                    "name": "Progress Bar",
                    "description": "Horizontal progress indicator",
                    "component": Progress.progress_bar(75, label="Project Completion"),
                },
                {
                    "name": "Step Progress",
                    "description": "Multi-step tracker",
                    "component": Progress.step_progress(
                        ["Planning", "Development", "Testing", "Launch"], current_step=2
                    ),
                },
                {
                    "name": "Milestone Tracker",
                    "description": "Timeline of milestones",
                    "component": Progress.milestone_tracker(
                        [
                            {
                                "title": "Product Launch",
                                "date": "Q1 2024",
                                "status": "completed",
                            },
                            {"title": "1K Users", "date": "Q2 2024", "status": "completed"},
                            {
                                "title": "Series A",
                                "date": "Q3 2024",
                                "status": "in_progress",
                            },
                            {"title": "10K Users", "date": "Q4 2024", "status": "pending"},
                        ]
                    ),
                },
            ],
        },
        {
            "title": "Tables",
            "description": "5 table variants for structured data",
            "components": [
                {
                    "name": "Simple Table",
                    "description": "Basic data table with headers",
                    "component": Tables.simple_table(
                        headers=["Product", "Price", "Sales"],
                        rows=[
                            ["Product A", "$99", "1,234"],
                            ["Product B", "$149", "2,345"],
                            ["Product C", "$199", "3,456"],
                        ],
                        striped=True,
                    ),
                },
                {
                    "name": "Pricing Table",
                    "description": "Feature tiers with pricing",
                    "component": Tables.pricing_table(
                        [
                            {
                                "name": "Basic",
                                "price": "$9/mo",
                                "features": [
                                    "5 team members",
                                    "10GB storage",
                                    "Basic support",
                                ],
                                "highlight": False,
                            },
                            {
                                "name": "Pro",
                                "price": "$29/mo",
                                "features": [
                                    "Unlimited team members",
                                    "1TB storage",
                                    "Priority support",
                                    "Advanced analytics",
                                ],
                                "highlight": True,
                            },
                            {
                                "name": "Enterprise",
                                "price": "Custom",
                                "features": [
                                    "Everything in Pro",
                                    "Dedicated support",
                                    "Custom integrations",
                                ],
                                "highlight": False,
                            },
                        ]
                    ),
                },
            ],
        },
        {
            "title": "Infographics",
            "description": "6 infographic variants for visual data stories",
            "components": [
                {
                    "name": "Stat with Icon",
                    "description": "120px icon with huge stat",
                    "component": Infographics.stat_with_icon(
                        icon="🚀", value="10K", label="Active Users"
                    ),
                },
                {
                    "name": "Funnel Chart",
                    "description": "Conversion funnel visualization",
                    "component": Infographics.funnel_chart(
                        [
                            {"label": "Website Visitors", "value": "10,000", "percentage": 100},
                            {"label": "Signups", "value": "5,000", "percentage": 50},
                            {"label": "Active Users", "value": "2,500", "percentage": 25},
                            {"label": "Paying Customers", "value": "1,000", "percentage": 10},
                        ]
                    ),
                },
                {
                    "name": "Process Flow",
                    "description": "Step-by-step process diagram",
                    "component": Infographics.process_flow(
                        ["Research", "Design", "Build", "Test", "Launch"],
                        orientation="horizontal",
                    ),
                },
                {
                    "name": "Timeline Infographic",
                    "description": "Visual timeline with events",
                    "component": Infographics.timeline_infographic(
                        [
                            {
                                "date": "Q1 2024",
                                "title": "Product Launch",
                                "description": "Released v1.0 to public",
                                "icon": "🚀",
                            },
                            {
                                "date": "Q2 2024",
                                "title": "Hit 1K Users",
                                "description": "Reached first growth milestone",
                                "icon": "📈",
                            },
                            {
                                "date": "Q3 2024",
                                "title": "Series A Funding",
                                "description": "Raised $5M to scale",
                                "icon": "💰",
                            },
                            {
                                "date": "Q4 2024",
                                "title": "Team Expansion",
                                "description": "Grew to 25 team members",
                                "icon": "👥",
                            },
                        ]
                    ),
                },
            ],
        },
    ]


def main():
    """Generate comprehensive showcase HTML"""
    print("Generating comprehensive component showcase...")
    print()

    # Collect all sections
    all_sections = []

    print("✓ Building Visual Elements showcase...")
    all_sections.extend(create_visual_elements_showcase())

    print("✓ Building Typography showcase...")
    all_sections.extend(create_typography_showcase())

    print("✓ Building Data Visualization showcase...")
    all_sections.extend(create_data_viz_showcase())

    print()
    print(f"Total sections: {len(all_sections)}")

    # Count components
    total_components = sum(len(section.get("components", [])) for section in all_sections)
    print(f"Total component examples: {total_components}")
    print()

    # Generate HTML
    print("Generating HTML...")
    html_content = ShowcaseRenderer.create_showcase_page(
        title="Component Showcase - Complete Library",
        sections=all_sections,
    )

    # Save to both user's .linkedin_drafts and local outputs folder
    output_dirs = [
        Path.home() / ".linkedin_drafts" / "previews",
        Path(__file__).parent.parent / "outputs",
    ]

    saved_paths = []
    for output_dir in output_dirs:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "comprehensive_showcase.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        saved_paths.append(output_file)
        print(f"✓ HTML saved to: {output_file}")
    print()
    print("=" * 80)
    print("COMPREHENSIVE SHOWCASE COMPLETE!")
    print("=" * 80)
    print()
    print("Summary:")
    print("  ✓ Visual Elements: 4 categories showcased")
    print("  ✓ Typography: 5 component types showcased")
    print("  ✓ Data Visualization: 5 component types showcased")
    print()
    print(f"  📊 Total: {total_components} component examples rendered")
    print()
    print("Open the HTML file in your browser to view the interactive showcase:")
    for path in saved_paths:
        print(f"  file://{path}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
