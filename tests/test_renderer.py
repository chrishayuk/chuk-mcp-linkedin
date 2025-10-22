"""
Tests for component renderer.

Tests the ComponentRenderer and ShowcaseRenderer classes.
"""

import pytest
from chuk_mcp_linkedin.renderer import ComponentRenderer, ShowcaseRenderer


class TestComponentRendererHelpers:
    """Test ComponentRenderer helper methods"""

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


class TestDividerRendering:
    """Test divider component rendering"""

    def test_render_horizontal_line(self):
        """Test rendering horizontal line divider"""
        component = {
            "type": "divider",
            "variant": "horizontal_line",
            "width": 400,
            "height": 2,
            "color": "#000000",
            "style": "solid",
        }
        html = ComponentRenderer.render(component)
        assert "<hr" in html
        assert "solid" in html
        assert "#000000" in html

    def test_render_gradient_fade(self):
        """Test rendering gradient fade divider"""
        component = {
            "type": "divider",
            "variant": "gradient_fade",
            "width": 500,
            "height": 3,
            "color": "#0a66c2",
        }
        html = ComponentRenderer.render(component)
        assert "linear-gradient" in html
        assert "to right" in html

    def test_render_decorative_accent(self):
        """Test rendering decorative accent divider"""
        component = {"type": "divider", "variant": "decorative_accent"}
        html = ComponentRenderer.render(component)
        assert "height: 8px" in html

    def test_render_section_break(self):
        """Test rendering section break divider"""
        component = {"type": "divider", "variant": "section_break"}
        html = ComponentRenderer.render(component)
        assert "• • •" in html


class TestBadgeRendering:
    """Test badge component rendering"""

    def test_render_pill_badge(self):
        """Test rendering pill badge"""
        component = {
            "type": "badge",
            "variant": "pill",
            "text": "NEW",
            "background_color": "#0a66c2",
            "text_color": "#FFFFFF",
        }
        html = ComponentRenderer.render(component)
        assert "NEW" in html
        assert "border-radius: 20px" in html
        assert "#0a66c2" in html

    def test_render_status_badge(self):
        """Test rendering status badge"""
        component = {
            "type": "badge",
            "variant": "status",
            "text": "TRENDING",
            "background_color": "#10B981",
            "text_color": "#FFFFFF",
            "status": "success",
        }
        html = ComponentRenderer.render(component)
        assert "TRENDING" in html

    def test_render_percentage_change_positive(self):
        """Test rendering positive percentage change badge"""
        component = {"type": "badge", "variant": "percentage_change", "value": 12.5}
        html = ComponentRenderer.render(component)
        assert "↑" in html
        assert "12.5" in html
        assert "#057642" in html

    def test_render_percentage_change_negative(self):
        """Test rendering negative percentage change badge"""
        component = {"type": "badge", "variant": "percentage_change", "value": -8.3}
        html = ComponentRenderer.render(component)
        assert "↓" in html
        assert "8.3" in html
        assert "#cc1016" in html


class TestShapeRendering:
    """Test shape component rendering"""

    def test_render_checkmark(self):
        """Test rendering checkmark"""
        component = {"type": "shape", "variant": "checkmark", "color": "#057642", "size": 24}
        html = ComponentRenderer.render(component)
        assert "✓" in html

    def test_render_arrow(self):
        """Test rendering arrow"""
        component = {"type": "shape", "variant": "arrow", "direction": "right"}
        html = ComponentRenderer.render(component)
        assert "→" in html

    def test_render_bullet_point(self):
        """Test rendering bullet point"""
        component = {"type": "shape", "variant": "bullet_point", "symbol": "→"}
        html = ComponentRenderer.render(component)
        assert "→" in html

    def test_render_icon_container(self):
        """Test rendering icon container"""
        component = {"type": "shape", "variant": "icon_container", "icon": "🚀", "size": 64}
        html = ComponentRenderer.render(component)
        assert "🚀" in html
        assert "64px" in html


class TestBorderRendering:
    """Test border component rendering"""

    def test_render_simple_border(self):
        """Test rendering simple border"""
        component = {
            "type": "border",
            "variant": "simple",
            "border_width": 2,
            "border_color": "#000000",
        }
        html = ComponentRenderer.render(component)
        assert "border:" in html

    def test_render_accent_border_left(self):
        """Test rendering accent border on left"""
        component = {
            "type": "border",
            "variant": "accent",
            "side": "left",
            "border_width": 4,
            "border_color": "#0a66c2",
        }
        html = ComponentRenderer.render(component)
        assert "border-left:" in html

    def test_render_callout_success(self):
        """Test rendering success callout box"""
        component = {
            "type": "border",
            "variant": "callout",
            "border_color": "#10B981",
            "background_color": "#D1FAE5",
        }
        html = ComponentRenderer.render(component)
        assert "#10B981" in html


class TestHeaderRendering:
    """Test header component rendering"""

    def test_render_h1(self):
        """Test rendering H1 header"""
        component = {
            "type": "header",
            "variant": "h1",
            "text": "Test Title",
            "font_size": 36,
            "font_weight": 700,
            "color": "#000000",
        }
        html = ComponentRenderer.render(component)
        assert "<h1" in html
        assert "Test Title" in html

    def test_render_h2(self):
        """Test rendering H2 header"""
        component = {
            "type": "header",
            "variant": "h2",
            "text": "Section Title",
            "font_size": 28,
            "font_weight": 700,
        }
        html = ComponentRenderer.render(component)
        assert "<h2" in html
        assert "Section Title" in html

    def test_render_eyebrow(self):
        """Test rendering eyebrow header"""
        component = {
            "type": "header",
            "variant": "eyebrow",
            "text": "NEW FEATURE",
            "text_transform": "uppercase",
        }
        html = ComponentRenderer.render(component)
        assert "NEW FEATURE" in html


class TestBodyTextRendering:
    """Test body text component rendering"""

    def test_render_paragraph(self):
        """Test rendering paragraph"""
        component = {
            "type": "body_text",
            "variant": "paragraph",
            "text": "This is a test paragraph.",
            "font_size": 16,
        }
        html = ComponentRenderer.render(component)
        assert "<p" in html
        assert "This is a test paragraph." in html

    def test_render_highlighted_text(self):
        """Test rendering highlighted text"""
        component = {
            "type": "body_text",
            "variant": "highlighted",
            "text": "Important text",
            "background_color": "#fff3cd",
        }
        html = ComponentRenderer.render(component)
        assert "Important text" in html
        assert "background:" in html

    def test_render_link(self):
        """Test rendering link"""
        component = {
            "type": "body_text",
            "variant": "link",
            "text": "Click here",
            "url": "https://example.com",
        }
        html = ComponentRenderer.render(component)
        assert "<a href" in html
        assert "https://example.com" in html
        assert "Click here" in html

    def test_render_code(self):
        """Test rendering code"""
        component = {"type": "body_text", "variant": "code", "text": "const x = 1;"}
        html = ComponentRenderer.render(component)
        assert "<code" in html
        assert "const x = 1;" in html


class TestListRendering:
    """Test list component rendering"""

    def test_render_bulleted_list(self):
        """Test rendering bulleted list"""
        component = {
            "type": "list",
            "variant": "bulleted",
            "items": ["Item 1", "Item 2", "Item 3"],
            "bullet": "→",
        }
        html = ComponentRenderer.render(component)
        assert "Item 1" in html
        assert "Item 2" in html
        assert "→" in html

    def test_render_numbered_list(self):
        """Test rendering numbered list"""
        component = {"type": "list", "variant": "numbered", "items": ["First", "Second", "Third"]}
        html = ComponentRenderer.render(component)
        assert "<ol" in html
        assert "First" in html
        assert "Second" in html

    def test_render_checklist(self):
        """Test rendering checklist"""
        component = {
            "type": "list",
            "variant": "checklist",
            "items": [{"text": "Task 1", "checked": True}, {"text": "Task 2", "checked": False}],
            "checked_symbol": "✓",
            "unchecked_symbol": "☐",
        }
        html = ComponentRenderer.render(component)
        assert "Task 1" in html
        assert "Task 2" in html
        assert "✓" in html

    def test_render_icon_list(self):
        """Test rendering icon list"""
        component = {
            "type": "list",
            "variant": "icon_list",
            "items": [{"icon": "🚀", "text": "Fast"}, {"icon": "⚡", "text": "Powerful"}],
        }
        html = ComponentRenderer.render(component)
        assert "🚀" in html
        assert "Fast" in html


class TestChartRendering:
    """Test chart component rendering"""

    def test_render_bar_chart(self):
        """Test rendering bar chart"""
        component = {
            "type": "chart",
            "variant": "bar",
            "data": [{"label": "Q1", "value": 100}, {"label": "Q2", "value": 150}],
            "bar_color": "#0a66c2",
        }
        html = ComponentRenderer.render(component)
        assert "Q1" in html
        assert "Q2" in html
        assert "100" in html

    def test_render_bar_chart_empty(self):
        """Test rendering bar chart with no data"""
        component = {"type": "chart", "variant": "bar", "data": []}
        html = ComponentRenderer.render(component)
        assert "No data" in html

    def test_render_pie_chart(self):
        """Test rendering pie chart"""
        component = {
            "type": "chart",
            "variant": "pie",
            "data": [{"label": "A", "value": 50}, {"label": "B", "value": 50}],
        }
        html = ComponentRenderer.render(component)
        assert "A" in html
        assert "B" in html


class TestMetricRendering:
    """Test metric component rendering"""

    def test_render_metric_card(self):
        """Test rendering metric card"""
        component = {
            "type": "metric",
            "variant": "card",
            "label": "Revenue",
            "value": "$1.2M",
            "change": {"value": 12.5, "text": "12.5%"},
        }
        html = ComponentRenderer.render(component)
        assert "Revenue" in html
        assert "$1.2M" in html
        assert "↑" in html

    def test_render_big_stat(self):
        """Test rendering big stat"""
        component = {
            "type": "metric",
            "variant": "big_stat",
            "value": "45.85%",
            "label": "Engagement",
            "context": {"text": "Highest rate"},
        }
        html = ComponentRenderer.render(component)
        assert "45.85%" in html
        assert "Engagement" in html
        assert "Highest rate" in html


class TestProgressRendering:
    """Test progress component rendering"""

    def test_render_progress_bar(self):
        """Test rendering progress bar"""
        component = {
            "type": "progress",
            "variant": "bar",
            "percentage": 75,
            "label": {"text": "Project Completion"},
            "fill_color": "#0a66c2",
        }
        html = ComponentRenderer.render(component)
        assert "75%" in html
        assert "Project Completion" in html

    def test_render_step_progress(self):
        """Test rendering step progress"""
        component = {
            "type": "progress",
            "variant": "steps",
            "steps": ["Planning", "Development", "Testing"],
            "current_step": 1,
        }
        html = ComponentRenderer.render(component)
        assert "Planning" in html
        assert "Development" in html
        assert "Testing" in html


class TestTableRendering:
    """Test table component rendering"""

    def test_render_simple_table(self):
        """Test rendering simple table"""
        component = {
            "type": "table",
            "variant": "simple",
            "headers": ["Name", "Age"],
            "rows": [["Alice", "30"], ["Bob", "25"]],
        }
        html = ComponentRenderer.render(component)
        assert "<table" in html
        assert "Name" in html
        assert "Alice" in html

    def test_render_pricing_table(self):
        """Test rendering pricing table"""
        component = {
            "type": "table",
            "variant": "pricing",
            "tiers": [
                {"name": "Basic", "price": "$9", "features": ["Feature 1"], "highlight": False},
                {
                    "name": "Pro",
                    "price": "$29",
                    "features": ["Feature 1", "Feature 2"],
                    "highlight": True,
                },
            ],
        }
        html = ComponentRenderer.render(component)
        assert "Basic" in html
        assert "$9" in html
        assert "Pro" in html


class TestInfographicRendering:
    """Test infographic component rendering"""

    def test_render_stat_with_icon(self):
        """Test rendering stat with icon"""
        component = {
            "type": "infographic",
            "variant": "stat_with_icon",
            "icon": "🚀",
            "value": "10K",
            "label": "Users",
        }
        html = ComponentRenderer.render(component)
        assert "🚀" in html
        assert "10K" in html
        assert "Users" in html

    def test_render_funnel_chart(self):
        """Test rendering funnel chart"""
        component = {
            "type": "infographic",
            "variant": "funnel",
            "stages": [
                {"label": "Visitors", "value": "10K", "percentage": 100},
                {"label": "Signups", "value": "5K", "percentage": 50},
            ],
        }
        html = ComponentRenderer.render(component)
        assert "Visitors" in html
        assert "10K" in html

    def test_render_process_flow(self):
        """Test rendering process flow"""
        component = {
            "type": "infographic",
            "variant": "process_flow",
            "steps": ["Step 1", "Step 2", "Step 3"],
        }
        html = ComponentRenderer.render(component)
        assert "Step 1" in html
        assert "Step 2" in html
        assert "→" in html

    def test_render_timeline(self):
        """Test rendering timeline"""
        component = {
            "type": "infographic",
            "variant": "timeline",
            "events": [
                {
                    "date": "Q1",
                    "title": "Launch",
                    "description": "Product launch",
                    "icon": "🚀",
                }
            ],
        }
        html = ComponentRenderer.render(component)
        assert "Q1" in html
        assert "Launch" in html
        assert "Product launch" in html
        assert "🚀" in html


class TestUnknownComponent:
    """Test unknown component handling"""

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
                        "component": {
                            "type": "header",
                            "variant": "h1",
                            "text": "Test",
                            "font_size": 36,
                        },
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
                        "component": {"type": "header", "variant": "h1", "text": "Test"},
                    }
                ],
            }
        ]

        html = ShowcaseRenderer.create_showcase_page(title="Test Showcase", sections=sections)

        assert "Test Showcase" in html
        assert "Test Section" in html

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
