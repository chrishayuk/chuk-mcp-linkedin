"""
Tests for component renderer.

Ensures all component renderers produce valid HTML output.
"""

from chuk_mcp_linkedin.renderer import ComponentRenderer, ShowcaseRenderer
from chuk_mcp_linkedin.components.visual_elements import (
    Dividers,
    Badges,
    Borders,
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


class TestComponentRenderer:
    """Test ComponentRenderer class"""

    def test_safe_text_with_string(self):
        """Test _safe_text with string input"""
        result = ComponentRenderer._safe_text("hello")
        assert result == "hello"

    def test_safe_text_with_dict_text(self):
        """Test _safe_text with dict containing text"""
        result = ComponentRenderer._safe_text({"text": "hello"})
        assert result == "hello"

    def test_safe_text_with_dict_label(self):
        """Test _safe_text with dict containing label"""
        result = ComponentRenderer._safe_text({"label": "hello"})
        assert result == "hello"

    def test_safe_text_with_dict_name(self):
        """Test _safe_text with dict containing name"""
        result = ComponentRenderer._safe_text({"name": "hello"})
        assert result == "hello"

    def test_safe_text_with_none(self):
        """Test _safe_text with None"""
        result = ComponentRenderer._safe_text(None)
        assert result == ""

    def test_render_divider_horizontal_line(self):
        """Test rendering horizontal line divider"""
        component = Dividers.horizontal_line()
        html = ComponentRenderer.render(component)
        assert "<hr" in html
        assert "solid" in html

    def test_render_divider_gradient_fade(self):
        """Test rendering gradient fade divider"""
        component = Dividers.gradient_fade()
        html = ComponentRenderer.render(component)
        assert "linear-gradient" in html

    def test_render_divider_decorative_accent(self):
        """Test rendering decorative accent"""
        component = Dividers.decorative_accent()
        html = ComponentRenderer.render(component)
        assert "height: 8px" in html

    def test_render_divider_section_break(self):
        """Test rendering section break"""
        component = Dividers.section_break()
        html = ComponentRenderer.render(component)
        assert "• • •" in html

    def test_render_divider_title_underline(self):
        """Test rendering title underline"""
        component = Dividers.title_underline()
        html = ComponentRenderer.render(component)
        assert "margin-top: 8px" in html

    def test_render_background(self):
        """Test rendering background component"""
        component = {"type": "background", "variant": "solid", "color": "#FFFFFF"}
        html = ComponentRenderer.render(component)
        assert "background" in html.lower()

    def test_render_border_simple(self):
        """Test rendering simple border"""
        component = Borders.simple_border()
        html = ComponentRenderer.render(component)
        assert "border:" in html

    def test_render_border_accent(self):
        """Test rendering accent border"""
        component = Borders.accent_border(side="left")
        html = ComponentRenderer.render(component)
        assert "border-left:" in html

    def test_render_border_callout_success(self):
        """Test rendering success callout box"""
        component = Borders.callout_box(style="success")
        html = ComponentRenderer.render(component)
        assert "#10B981" in html  # Design token semantic success color

    def test_render_border_callout_warning(self):
        """Test rendering warning callout box"""
        component = Borders.callout_box(style="warning")
        html = ComponentRenderer.render(component)
        assert "#F59E0B" in html  # Design token semantic warning color

    def test_render_badge_pill(self):
        """Test rendering pill badge"""
        component = Badges.pill_badge("NEW")
        html = ComponentRenderer.render(component)
        assert "NEW" in html
        assert "border-radius: 20px" in html

    def test_render_badge_status(self):
        """Test rendering status badge"""
        component = Badges.status_badge("new")
        html = ComponentRenderer.render(component)
        assert "NEW" in html.upper()

    def test_render_badge_percentage_change_positive(self):
        """Test rendering positive percentage change"""
        component = Badges.percentage_change(12.5)
        html = ComponentRenderer.render(component)
        assert "↑" in html
        assert "12.5" in html

    def test_render_badge_percentage_change_negative(self):
        """Test rendering negative percentage change"""
        component = Badges.percentage_change(-8.3)
        html = ComponentRenderer.render(component)
        assert "↓" in html
        assert "8.3" in html

    def test_render_shape_checkmark(self):
        """Test rendering checkmark"""
        component = Shapes.checkmark()
        html = ComponentRenderer.render(component)
        assert "✓" in html

    def test_render_shape_arrow(self):
        """Test rendering arrow"""
        component = Shapes.arrow(direction="right")
        html = ComponentRenderer.render(component)
        assert "→" in html

    def test_render_shape_bullet_point(self):
        """Test rendering bullet point"""
        component = Shapes.bullet_point(style="arrow")
        html = ComponentRenderer.render(component)
        assert "→" in html

    def test_render_shape_icon_container(self):
        """Test rendering icon container"""
        component = Shapes.icon_container("🚀", size=64)
        html = ComponentRenderer.render(component)
        assert "🚀" in html
        assert "64px" in html

    def test_render_header_h1(self):
        """Test rendering H1 header"""
        component = Headers.h1("Test Title")
        html = ComponentRenderer.render(component)
        assert "<h1" in html
        assert "Test Title" in html

    def test_render_header_h2(self):
        """Test rendering H2 header"""
        component = Headers.h2("Section Title")
        html = ComponentRenderer.render(component)
        assert "<h2" in html
        assert "Section Title" in html

    def test_render_header_eyebrow(self):
        """Test rendering eyebrow header"""
        component = Headers.eyebrow("NEW FEATURE")
        html = ComponentRenderer.render(component)
        assert "NEW FEATURE" in html

    def test_render_body_text_paragraph(self):
        """Test rendering paragraph"""
        component = BodyText.paragraph("This is a test paragraph.")
        html = ComponentRenderer.render(component)
        assert "<p" in html
        assert "This is a test paragraph." in html

    def test_render_body_text_highlighted(self):
        """Test rendering highlighted text"""
        component = BodyText.highlighted("Important text")
        html = ComponentRenderer.render(component)
        assert "Important text" in html
        assert "background:" in html

    def test_render_body_text_emphasized(self):
        """Test rendering emphasized text"""
        component = BodyText.emphasized("Emphasized text")
        html = ComponentRenderer.render(component)
        assert "<em" in html
        assert "Emphasized text" in html

    def test_render_body_text_link(self):
        """Test rendering link"""
        component = BodyText.link("Click here", url="https://example.com")
        html = ComponentRenderer.render(component)
        assert "<a href" in html
        assert "https://example.com" in html
        assert "Click here" in html

    def test_render_body_text_code(self):
        """Test rendering code"""
        component = BodyText.code("const x = 1;")
        html = ComponentRenderer.render(component)
        assert "<code" in html
        assert "const x = 1;" in html

    def test_render_caption(self):
        """Test rendering caption"""
        component = Captions.caption("Figure 1: Test")
        html = ComponentRenderer.render(component)
        assert "Figure 1: Test" in html

    def test_render_caption_with_icon(self):
        """Test rendering caption with icon"""
        component = Captions.metadata("Last updated", icon="📅")
        html = ComponentRenderer.render(component)
        assert "Last updated" in html
        assert "📅" in html

    def test_render_quote_pull_quote(self):
        """Test rendering pull quote"""
        component = Quotes.pull_quote("Test quote", author="John Doe")
        html = ComponentRenderer.render(component)
        assert "<blockquote" in html
        assert "Test quote" in html
        assert "John Doe" in html

    def test_render_quote_testimonial(self):
        """Test rendering testimonial"""
        component = Quotes.testimonial(
            text="Great product!",
            author="Jane Smith",
            role="CEO",
            company="Acme Corp",
            rating=5.0,
        )
        html = ComponentRenderer.render(component)
        assert "Great product!" in html
        assert "Jane Smith" in html
        assert "★" in html

    def test_render_quote_blockquote(self):
        """Test rendering blockquote"""
        component = Quotes.blockquote("Test quote", author="Author Name")
        html = ComponentRenderer.render(component)
        assert "Test quote" in html
        assert "Author Name" in html

    def test_render_list_bulleted(self):
        """Test rendering bulleted list"""
        component = Lists.bulleted_list(["Item 1", "Item 2", "Item 3"])
        html = ComponentRenderer.render(component)
        assert "Item 1" in html
        assert "Item 2" in html
        assert "Item 3" in html

    def test_render_list_numbered(self):
        """Test rendering numbered list"""
        component = Lists.numbered_list(["First", "Second", "Third"])
        html = ComponentRenderer.render(component)
        assert "<ol" in html
        assert "First" in html
        assert "Second" in html

    def test_render_list_checklist(self):
        """Test rendering checklist"""
        component = Lists.checklist(
            [
                {"text": "Task 1", "checked": True},
                {"text": "Task 2", "checked": False},
            ]
        )
        html = ComponentRenderer.render(component)
        assert "Task 1" in html
        assert "Task 2" in html
        assert "✓" in html

    def test_render_list_icon_list(self):
        """Test rendering icon list"""
        component = Lists.icon_list(
            [{"icon": "🚀", "text": "Fast"}, {"icon": "⚡", "text": "Powerful"}]
        )
        html = ComponentRenderer.render(component)
        assert "🚀" in html
        assert "Fast" in html
        assert "⚡" in html

    def test_render_chart_bar(self):
        """Test rendering bar chart"""
        component = Charts.bar_chart([{"label": "Q1", "value": 100}, {"label": "Q2", "value": 150}])
        html = ComponentRenderer.render(component)
        assert "Q1" in html
        assert "Q2" in html
        assert "100" in html

    def test_render_chart_bar_empty(self):
        """Test rendering bar chart with no data"""
        component = Charts.bar_chart([])
        html = ComponentRenderer.render(component)
        assert "No data" in html

    def test_render_chart_pie(self):
        """Test rendering pie chart"""
        component = Charts.pie_chart([{"label": "A", "value": 50}, {"label": "B", "value": 50}])
        html = ComponentRenderer.render(component)
        assert "A" in html
        assert "B" in html

    def test_render_metric_card(self):
        """Test rendering metric card"""
        component = Metrics.metric_card(label="Revenue", value="$1.2M", change=12.5)
        html = ComponentRenderer.render(component)
        assert "Revenue" in html
        assert "$1.2M" in html
        assert "↑" in html

    def test_render_metric_big_stat(self):
        """Test rendering big stat"""
        component = Metrics.big_stat(value="45.85%", label="Engagement", context="Highest rate")
        html = ComponentRenderer.render(component)
        assert "45.85%" in html
        assert "Engagement" in html
        assert "Highest rate" in html

    def test_render_metric_big_stat_dict_context(self):
        """Test rendering big stat with dict context"""
        component = Metrics.big_stat(
            value="45.85%",
            label="Engagement",
            context={"text": "Highest rate"},
        )
        html = ComponentRenderer.render(component)
        assert "Highest rate" in html

    def test_render_progress_bar(self):
        """Test rendering progress bar"""
        component = Progress.progress_bar(75, label="Project Completion")
        html = ComponentRenderer.render(component)
        assert "75%" in html
        assert "Project Completion" in html

    def test_render_progress_bar_dict_label(self):
        """Test rendering progress bar with dict label"""
        component = Progress.progress_bar(75, label={"text": "Project"})
        html = ComponentRenderer.render(component)
        assert "Project" in html

    def test_render_progress_step(self):
        """Test rendering step progress"""
        component = Progress.step_progress(["Planning", "Development", "Testing"], current_step=1)
        html = ComponentRenderer.render(component)
        assert "Planning" in html
        assert "Development" in html
        assert "Testing" in html

    def test_render_table_simple(self):
        """Test rendering simple table"""
        component = Tables.simple_table(
            headers=["Name", "Age"],
            rows=[["Alice", "30"], ["Bob", "25"]],
        )
        html = ComponentRenderer.render(component)
        assert "<table" in html
        assert "Name" in html
        assert "Alice" in html

    def test_render_table_pricing(self):
        """Test rendering pricing table"""
        component = Tables.pricing_table(
            [
                {
                    "name": "Basic",
                    "price": "$9",
                    "features": ["Feature 1"],
                    "highlight": False,
                },
                {
                    "name": "Pro",
                    "price": "$29",
                    "features": ["Feature 1", "Feature 2"],
                    "highlight": True,
                },
            ]
        )
        html = ComponentRenderer.render(component)
        assert "Basic" in html
        assert "$9" in html
        assert "Pro" in html

    def test_render_infographic_stat_with_icon(self):
        """Test rendering stat with icon"""
        component = Infographics.stat_with_icon(icon="🚀", value="10K", label="Users")
        html = ComponentRenderer.render(component)
        assert "🚀" in html
        assert "10K" in html
        assert "Users" in html

    def test_render_infographic_funnel(self):
        """Test rendering funnel chart"""
        component = Infographics.funnel_chart(
            [
                {"label": "Visitors", "value": "10K", "percentage": 100},
                {"label": "Signups", "value": "5K", "percentage": 50},
            ]
        )
        html = ComponentRenderer.render(component)
        assert "Visitors" in html
        assert "10K" in html

    def test_render_infographic_process_flow(self):
        """Test rendering process flow"""
        component = Infographics.process_flow(["Step 1", "Step 2", "Step 3"])
        html = ComponentRenderer.render(component)
        assert "Step 1" in html
        assert "Step 2" in html
        assert "→" in html

    def test_render_infographic_timeline(self):
        """Test rendering timeline"""
        component = Infographics.timeline_infographic(
            [
                {
                    "date": "Q1",
                    "title": "Launch",
                    "description": "Product launch",
                    "icon": "🚀",
                }
            ]
        )
        html = ComponentRenderer.render(component)
        assert "Q1" in html
        assert "Launch" in html
        assert "Product launch" in html
        assert "🚀" in html

    def test_render_unknown_component(self):
        """Test rendering unknown component type"""
        component = {"type": "unknown", "variant": "test"}
        html = ComponentRenderer.render(component)
        assert "unknown" in html.lower()


class TestShowcaseRenderer:
    """Test ShowcaseRenderer class"""

    def test_create_showcase_page(self):
        """Test creating complete showcase page"""
        sections = [
            {
                "title": "Test Section",
                "description": "Test description",
                "components": [
                    {
                        "name": "Test Component",
                        "description": "Component description",
                        "component": Headers.h1("Test"),
                    }
                ],
            }
        ]

        html = ShowcaseRenderer.create_showcase_page(title="Test Showcase", sections=sections)

        assert "<!DOCTYPE html>" in html
        assert "Test Showcase" in html
        assert "Test Section" in html
        assert "Test Component" in html
        assert "Component description" in html

    def test_create_showcase_page_no_description(self):
        """Test creating showcase without descriptions"""
        sections = [
            {
                "title": "Test Section",
                "components": [
                    {
                        "name": "Test Component",
                        "component": Headers.h1("Test"),
                    }
                ],
            }
        ]

        html = ShowcaseRenderer.create_showcase_page(title="Test Showcase", sections=sections)

        assert "Test Showcase" in html
        assert "Test Section" in html

    def test_create_showcase_page_with_none_component(self):
        """Test creating showcase with None component"""
        sections = [
            {
                "title": "Test Section",
                "components": [
                    {
                        "name": "Test Component",
                        "component": None,
                    }
                ],
            }
        ]

        html = ShowcaseRenderer.create_showcase_page(title="Test Showcase", sections=sections)

        assert "Test Showcase" in html

    def test_create_showcase_includes_styles(self):
        """Test that showcase includes CSS styles"""
        sections = []
        html = ShowcaseRenderer.create_showcase_page(title="Test", sections=sections)

        assert "<style>" in html
        assert "font-family" in html
        assert "background" in html

    def test_create_showcase_includes_footer(self):
        """Test that showcase includes footer"""
        sections = []
        html = ShowcaseRenderer.create_showcase_page(title="Test", sections=sections)

        assert "chuk-mcp-linkedin" in html
        assert "Design System" in html
