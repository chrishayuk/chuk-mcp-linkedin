"""
Demo script showing HTML previews of all 11 document layouts.

Creates visual representations of each layout type with sample content.
Opens each layout preview in the browser for inspection.
"""

import sys
import time
import webbrowser
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.documents import DocumentLayouts


def generate_layout_preview_html(layout_name: str, layout, sample_content: dict) -> str:
    """Generate HTML preview of a document layout"""

    # Get layout details
    canvas_width, canvas_height = layout.canvas_size

    # Build zones HTML
    zones_html = []

    if layout.title_zone:
        zone = layout.title_zone
        font_size = (zone.font_size * 0.15) if zone.font_size else 24
        zones_html.append(f"""
        <div class="zone title-zone" style="
            left: {zone.x}px;
            top: {zone.y}px;
            width: {zone.width}px;
            height: {zone.height}px;
            font-size: {font_size}px;
            text-align: {zone.align};
            vertical-align: {zone.valign};
        ">
            <div class="zone-label">TITLE ZONE</div>
            <div class="zone-content">{sample_content.get('title', 'Title Here')}</div>
        </div>
        """)

    if layout.subtitle_zone:
        zone = layout.subtitle_zone
        font_size = (zone.font_size * 0.15) if zone.font_size else 16
        zones_html.append(f"""
        <div class="zone subtitle-zone" style="
            left: {zone.x}px;
            top: {zone.y}px;
            width: {zone.width}px;
            height: {zone.height}px;
            font-size: {font_size}px;
            text-align: {zone.align};
        ">
            <div class="zone-label">SUBTITLE ZONE</div>
            <div class="zone-content">{sample_content.get('subtitle', 'Subtitle text')}</div>
        </div>
        """)

    if layout.content_zone:
        zone = layout.content_zone
        label = zone.properties.get('label', 'CONTENT') if zone.properties else 'CONTENT'
        font_size = (zone.font_size * 0.15) if zone.font_size else 14
        zones_html.append(f"""
        <div class="zone content-zone" style="
            left: {zone.x}px;
            top: {zone.y}px;
            width: {zone.width}px;
            height: {zone.height}px;
            font-size: {font_size}px;
            text-align: {zone.align};
        ">
            <div class="zone-label">{label} ZONE</div>
            <div class="zone-content">{sample_content.get('content', 'Content goes here...')}</div>
        </div>
        """)

    if layout.content_zone_2:
        zone = layout.content_zone_2
        label = zone.properties.get('label', 'CONTENT 2') if zone.properties else 'CONTENT 2'
        font_size = (zone.font_size * 0.15) if zone.font_size else 14
        zones_html.append(f"""
        <div class="zone content-zone-2" style="
            left: {zone.x}px;
            top: {zone.y}px;
            width: {zone.width}px;
            height: {zone.height}px;
            font-size: {font_size}px;
            text-align: {zone.align};
        ">
            <div class="zone-label">{label} ZONE</div>
            <div class="zone-content">{sample_content.get('content_2', 'Second content area...')}</div>
        </div>
        """)

    if layout.image_zone:
        zone = layout.image_zone
        zones_html.append(f"""
        <div class="zone image-zone" style="
            left: {zone.x}px;
            top: {zone.y}px;
            width: {zone.width}px;
            height: {zone.height}px;
        ">
            <div class="zone-label">IMAGE ZONE</div>
            <div class="zone-content image-placeholder">🖼️<br>Image/Chart Area</div>
        </div>
        """)

    if layout.branding_zone:
        zone = layout.branding_zone
        zones_html.append(f"""
        <div class="zone branding-zone" style="
            left: {zone.x}px;
            top: {zone.y}px;
            width: {zone.width}px;
            height: {zone.height}px;
        ">
            <div class="zone-content">🏢 Logo</div>
        </div>
        """)

    zones_combined = "\n".join(zones_html)

    # Build metadata
    best_for = ", ".join(layout.best_for) if layout.best_for else "General use"
    use_cases = layout.use_cases[:3] if layout.use_cases else []
    use_cases_html = "<br>".join(f"• {uc}" for uc in use_cases)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{layout.name} - Document Layout Preview</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}

        .header h1 {{
            color: #0a66c2;
            font-size: 32px;
            margin-bottom: 10px;
        }}

        .header .type {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 15px;
        }}

        .header .description {{
            color: #333;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
        }}

        .metadata {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }}

        .metadata-item {{
            background: #f8f9fa;
            padding: 12px 15px;
            border-radius: 6px;
        }}

        .metadata-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}

        .metadata-value {{
            font-size: 14px;
            color: #333;
            line-height: 1.5;
        }}

        .layout-preview {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}

        .canvas {{
            position: relative;
            width: 100%;
            max-width: 600px;
            aspect-ratio: 1;
            margin: 0 auto;
            background: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .zone {{
            position: absolute;
            border: 2px dashed #0a66c2;
            background: rgba(10, 102, 194, 0.05);
            padding: 10px;
            transition: all 0.3s ease;
        }}

        .zone:hover {{
            background: rgba(10, 102, 194, 0.15);
            border-style: solid;
            z-index: 10;
            box-shadow: 0 2px 10px rgba(10, 102, 194, 0.3);
        }}

        .zone-label {{
            font-size: 9px;
            color: #0a66c2;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
            opacity: 0.8;
        }}

        .zone-content {{
            font-size: 12px;
            color: #333;
            line-height: 1.4;
            overflow: hidden;
        }}

        .title-zone {{
            border-color: #9333ea;
            background: rgba(147, 51, 234, 0.08);
        }}

        .title-zone:hover {{
            background: rgba(147, 51, 234, 0.15);
        }}

        .title-zone .zone-label {{
            color: #9333ea;
        }}

        .title-zone .zone-content {{
            font-weight: 700;
        }}

        .subtitle-zone {{
            border-color: #06b6d4;
            background: rgba(6, 182, 212, 0.08);
        }}

        .subtitle-zone:hover {{
            background: rgba(6, 182, 212, 0.15);
        }}

        .subtitle-zone .zone-label {{
            color: #06b6d4;
        }}

        .content-zone {{
            border-color: #10b981;
            background: rgba(16, 185, 129, 0.08);
        }}

        .content-zone:hover {{
            background: rgba(16, 185, 129, 0.15);
        }}

        .content-zone .zone-label {{
            color: #10b981;
        }}

        .content-zone-2 {{
            border-color: #f59e0b;
            background: rgba(245, 158, 11, 0.08);
        }}

        .content-zone-2:hover {{
            background: rgba(245, 158, 11, 0.15);
        }}

        .content-zone-2 .zone-label {{
            color: #f59e0b;
        }}

        .image-zone {{
            border-color: #ec4899;
            background: rgba(236, 72, 153, 0.08);
        }}

        .image-zone:hover {{
            background: rgba(236, 72, 153, 0.15);
        }}

        .image-zone .zone-label {{
            color: #ec4899;
        }}

        .image-placeholder {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            font-size: 24px;
            color: #ec4899;
        }}

        .branding-zone {{
            border-color: #64748b;
            background: rgba(100, 116, 139, 0.08);
        }}

        .branding-zone:hover {{
            background: rgba(100, 116, 139, 0.15);
        }}

        .branding-zone .zone-label {{
            color: #64748b;
        }}

        .legend {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}

        .legend h3 {{
            font-size: 14px;
            color: #333;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .legend-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
        }}

        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
            border: 2px solid;
        }}

        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            font-size: 13px;
            opacity: 0.9;
        }}

        @media (max-width: 768px) {{
            .canvas {{
                max-width: 100%;
            }}

            .zone-label {{
                font-size: 7px;
            }}

            .zone-content {{
                font-size: 9px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{layout.name}</h1>
            <div class="type">{layout.type.value.replace('_', ' ')}</div>
            <div class="description">{layout.description}</div>

            <div class="metadata">
                <div class="metadata-item">
                    <div class="metadata-label">Canvas Size</div>
                    <div class="metadata-value">{canvas_width} × {canvas_height}px</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Best For</div>
                    <div class="metadata-value">{best_for}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Use Cases</div>
                    <div class="metadata-value">{use_cases_html}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Generated</div>
                    <div class="metadata-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                </div>
            </div>
        </div>

        <div class="layout-preview">
            <div class="canvas">
                {zones_combined}
            </div>

            <div class="legend">
                <h3>Zone Legend</h3>
                <div class="legend-grid">
                    <div class="legend-item">
                        <div class="legend-color" style="border-color: #9333ea; background: rgba(147, 51, 234, 0.1);"></div>
                        <span>Title Zone</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="border-color: #06b6d4; background: rgba(6, 182, 212, 0.1);"></div>
                        <span>Subtitle Zone</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="border-color: #10b981; background: rgba(16, 185, 129, 0.1);"></div>
                        <span>Content Zone</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="border-color: #f59e0b; background: rgba(245, 158, 11, 0.1);"></div>
                        <span>Content Zone 2</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="border-color: #ec4899; background: rgba(236, 72, 153, 0.1);"></div>
                        <span>Image Zone</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="border-color: #64748b; background: rgba(100, 116, 139, 0.1);"></div>
                        <span>Branding Zone</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            Generated by chuk-mcp-linkedin | Document Layout Preview
        </div>
    </div>
</body>
</html>"""

    return html


def demo_title_slide():
    """Demo title slide layout"""
    layout = DocumentLayouts.title_slide()
    content = {
        "title": "Q1 2025 Results",
        "subtitle": "Growth & Performance Highlights",
    }
    return ("title_slide", layout, content, "Hero opening slide")


def demo_content_slide():
    """Demo content slide layout"""
    layout = DocumentLayouts.content_slide()
    content = {
        "title": "What Actually Works in 2025",
        "content": "• Lead with insights, not products\n• Share frameworks, not features\n• Tell stories, not sales pitches\n• Build trust, not transactions\n• Focus on value delivery",
    }
    return ("content_slide", layout, content, "Standard content with bullets")


def demo_split_content():
    """Demo split content layout"""
    layout = DocumentLayouts.split_content()
    content = {
        "title": "Before vs After",
        "content": "We transformed our workflow by implementing AI tools across the entire team. Results were immediate and measurable.",
    }
    return ("split_content", layout, content, "Text + image split")


def demo_big_number():
    """Demo big number layout"""
    layout = DocumentLayouts.big_number()
    content = {
        "title": "45.85%",
        "subtitle": "Engagement rate for document posts\n(highest of all formats in 2025)",
    }
    return ("big_number", layout, content, "Eye-catching stat display")


def demo_quote_slide():
    """Demo quote slide layout"""
    layout = DocumentLayouts.quote_slide()
    content = {
        "content": '"This completely changed how we think about LinkedIn content"',
        "subtitle": "— Sarah Johnson, Marketing Director\nFortune 500 Company",
    }
    return ("quote_slide", layout, content, "Testimonial showcase")


def demo_comparison():
    """Demo comparison layout"""
    layout = DocumentLayouts.comparison()
    content = {
        "title": "Traditional vs Modern Approach",
        "content": "❌ Post and ghost\n❌ Self-promotion\n❌ Sales pitches\n❌ Irregular posting",
        "content_2": "✅ Consistent engagement\n✅ Value-first content\n✅ Authentic conversations\n✅ Strategic scheduling",
    }
    return ("comparison", layout, content, "Side-by-side A vs B")


def demo_two_column():
    """Demo two column layout"""
    layout = DocumentLayouts.two_column()
    content = {
        "title": "Pros and Cons",
        "content": "ADVANTAGES:\n• Fast implementation\n• Low initial cost\n• Easy to learn\n• Quick results",
        "content_2": "CONSIDERATIONS:\n• Limited customization\n• Scalability concerns\n• Ongoing maintenance\n• Feature limitations",
    }
    return ("two_column", layout, content, "Balanced comparison")


def demo_checklist():
    """Demo checklist layout"""
    layout = DocumentLayouts.checklist()
    content = {
        "title": "Pre-Launch Checklist",
        "content": "☐ Test all functionality\n☐ Prepare marketing materials\n☐ Set up analytics tracking\n☐ Schedule announcement posts\n☐ Brief support team\n☐ Monitor first 24 hours",
    }
    return ("checklist", layout, content, "Action items list")


def demo_timeline():
    """Demo timeline layout"""
    layout = DocumentLayouts.timeline()
    content = {
        "title": "2024 Milestones",
        "content": "JAN → Product Launch\n\nMAR → Hit 1K Users\n\nJUN → Series A $5M\n\nSEP → Team of 25\n\nDEC → 10K Customers",
    }
    return ("timeline", layout, content, "Chronological progress")


def demo_icon_grid():
    """Demo icon grid layout"""
    layout = DocumentLayouts.icon_grid()
    content = {
        "title": "Core Features",
        "content": "🚀 FAST\nLightning quick performance\n\n⚡ POWERFUL\nFull-featured platform\n\n💡 SMART\nAI-powered insights\n\n🎯 PRECISE\nData-driven decisions",
    }
    return ("icon_grid", layout, content, "Feature highlights grid")


def demo_data_visual():
    """Demo data visual layout"""
    layout = DocumentLayouts.data_visual()
    content = {
        "title": "2024 Performance Metrics",
        "content": "Source: Internal analytics dashboard | Data as of Q4 2024",
    }
    return ("data_visual", layout, content, "Chart/graph slide")


def main():
    """Run all layout demos and open previews"""
    print("=" * 70)
    print("GENERATING DOCUMENT LAYOUT PREVIEWS")
    print("=" * 70)
    print()
    print("📄 Document posts have 45.85% engagement (HIGHEST format in 2025)")
    print("📐 All layouts optimized for 1920x1920 square format")
    print()

    # Generate all layout demos
    demos = [
        demo_title_slide(),
        demo_content_slide(),
        demo_split_content(),
        demo_big_number(),
        demo_quote_slide(),
        demo_comparison(),
        demo_two_column(),
        demo_checklist(),
        demo_timeline(),
        demo_icon_grid(),
        demo_data_visual(),
    ]

    previews = []
    output_dir = Path(__file__).parent.parent / ".linkedin_drafts" / "previews" / "layouts"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🎨 GENERATING LAYOUT PREVIEWS")
    print("-" * 70)

    for i, (name, layout, content, description) in enumerate(demos, 1):
        # Generate HTML
        html_content = generate_layout_preview_html(name, layout, content)

        # Save to file
        timestamp = int(time.time())
        filename = f"layout_{name}_{timestamp}.html"
        output_path = output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        previews.append(str(output_path.absolute()))

        print(f"✅ {i:2d}. {layout.name:20s} - {description}")
        print(f"     {output_path}")
        print()

    print("=" * 70)
    print(f"✅ Generated {len(previews)} layout preview(s)")
    print("=" * 70)
    print()

    # Ask user which to open
    print("Which preview would you like to open?")
    for i, (name, layout, _, description) in enumerate(demos, 1):
        print(f"{i:2d}. {layout.name} - {description}")
    print(" A. Open ALL")
    print()

    choice = input("Enter choice (1-11 or A): ").strip().upper()

    if choice == "A":
        print("\nOpening all previews in browser...")
        for i, preview_path in enumerate(previews, 1):
            webbrowser.open(f"file://{preview_path}")
            if i < len(previews):
                time.sleep(0.3)  # Small delay between opens
    elif choice.isdigit() and 1 <= int(choice) <= 11:
        idx = int(choice) - 1
        print(f"\nOpening {demos[idx][1].name} preview in browser...")
        webbrowser.open(f"file://{previews[idx]}")
    else:
        print("Invalid choice. Opening first preview...")
        webbrowser.open(f"file://{previews[0]}")

    print("\n✅ Done! Check your browser.")


if __name__ == "__main__":
    main()
