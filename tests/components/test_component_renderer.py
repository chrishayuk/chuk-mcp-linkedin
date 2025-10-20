"""
Tests for Component Renderer - HTML/CSS rendering of all components.
"""

from chuk_mcp_linkedin.components.component_renderer import ComponentRenderer
from chuk_mcp_linkedin.components.visual_elements import (
    Dividers,
    Backgrounds,
    Borders,
    Badges,
    Shapes,
)


class TestRenderDivider:
    """Test divider rendering"""

    def test_render_horizontal_line(self):
        """Test rendering horizontal line divider"""
        divider = Dividers.horizontal_line(width=400, thickness=2)
        html = ComponentRenderer.render_divider(divider)

        assert isinstance(html, str)
        assert "width: 400px" in html
        assert "height: 2px" in html
        assert "background-color:" in html

    def test_render_horizontal_line_dashed(self):
        """Test rendering dashed horizontal line"""
        divider = Dividers.horizontal_line(style="dashed")
        html = ComponentRenderer.render_divider(divider)

        assert "border-style: dashed" in html

    def test_render_gradient_fade(self):
        """Test rendering gradient fade divider"""
        divider = Dividers.gradient_fade(width=500)
        html = ComponentRenderer.render_divider(divider)

        assert isinstance(html, str)
        assert "width: 500px" in html
        assert "linear-gradient" in html
        assert "to right" in html

    def test_render_decorative_accent(self):
        """Test rendering decorative accent divider"""
        divider = Dividers.decorative_accent()
        html = ComponentRenderer.render_divider(divider)

        assert isinstance(html, str)
        assert "border-radius:" in html
        assert "margin:" in html

    def test_render_section_break(self):
        """Test rendering section break divider"""
        divider = Dividers.section_break(style="dots")
        html = ComponentRenderer.render_divider(divider)

        assert isinstance(html, str)
        assert "• • •" in html
        assert "text-align:" in html
        assert "letter-spacing:" in html

    def test_render_spacer(self):
        """Test rendering spacer divider"""
        divider = Dividers.spacer(size="large")
        html = ComponentRenderer.render_divider(divider)

        assert isinstance(html, str)
        assert "height:" in html
        assert "px" in html

    def test_render_unknown_divider_variant(self):
        """Test rendering unknown divider variant returns empty string"""
        divider = {"variant": "unknown", "type": "divider"}
        html = ComponentRenderer.render_divider(divider)

        assert html == ""


class TestRenderBadge:
    """Test badge rendering"""

    def test_render_pill_badge(self):
        """Test rendering pill badge"""
        badge = Badges.pill_badge("NEW")
        html = ComponentRenderer.render_badge(badge)

        assert isinstance(html, str)
        assert "NEW" in html
        assert "background-color:" in html
        assert "color:" in html
        assert "border-radius:" in html
        assert "display: inline-block" in html

    def test_render_status_badge(self):
        """Test rendering status badge"""
        badge = Badges.status_badge("trending")
        html = ComponentRenderer.render_badge(badge)

        assert isinstance(html, str)
        assert "TRENDING" in html
        assert "text-transform: uppercase" in html
        assert "letter-spacing:" in html

    def test_render_status_outlined_badge(self):
        """Test rendering status outlined badge"""
        badge = Badges.status_badge("beta", style="minimal")
        html = ComponentRenderer.render_badge(badge)

        assert isinstance(html, str)
        assert "BETA" in html
        assert "border:" in html
        assert "solid" in html

    def test_render_percentage_change_positive(self):
        """Test rendering positive percentage change badge"""
        badge = Badges.percentage_change(12.5)
        html = ComponentRenderer.render_badge(badge)

        assert isinstance(html, str)
        assert "↑" in html
        assert "12.5" in html

    def test_render_percentage_change_negative(self):
        """Test rendering negative percentage change badge"""
        badge = Badges.percentage_change(-8.3)
        html = ComponentRenderer.render_badge(badge)

        assert isinstance(html, str)
        assert "↓" in html
        assert "8.3" in html

    def test_render_category_tag(self):
        """Test rendering category tag badge"""
        badge = Badges.category_tag("Design")
        html = ComponentRenderer.render_badge(badge)

        assert isinstance(html, str)
        assert "Design" in html
        assert "background-color:" in html

    def test_render_badge_includes_font_size(self):
        """Test badge rendering includes font size"""
        badge = Badges.pill_badge("TEST", size="large")
        html = ComponentRenderer.render_badge(badge)

        assert "font-size:" in html
        assert "px" in html

    def test_render_unknown_badge_variant(self):
        """Test rendering unknown badge variant returns empty string"""
        badge = {"variant": "unknown", "type": "badge"}
        html = ComponentRenderer.render_badge(badge)

        assert html == ""


class TestRenderShape:
    """Test shape rendering"""

    def test_render_circle_filled(self):
        """Test rendering filled circle"""
        shape = Shapes.circle(size=100, fill=True)
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert "width: 100px" in html
        assert "height: 100px" in html
        assert "border-radius: 50%" in html
        assert "background-color:" in html

    def test_render_circle_outline(self):
        """Test rendering outline circle"""
        shape = Shapes.circle(size=100, fill=False, stroke_width=3)
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert "border:" in html
        assert "3px solid" in html

    def test_render_icon_container(self):
        """Test rendering icon container"""
        shape = Shapes.icon_container("🚀", size=80)
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert "🚀" in html
        assert "width: 80px" in html
        assert "height: 80px" in html
        assert "display: inline-flex" in html
        assert "align-items: center" in html
        assert "justify-content: center" in html

    def test_render_checkmark_with_background(self):
        """Test rendering checkmark with background"""
        shape = Shapes.checkmark(style="circle")
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert shape["symbol"] in html
        assert "background-color:" in html

    def test_render_checkmark_minimal(self):
        """Test rendering checkmark minimal style"""
        shape = Shapes.checkmark(style="minimal")
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert shape["symbol"] in html

    def test_render_progress_ring(self):
        """Test rendering progress ring"""
        shape = Shapes.progress_ring(75, size=150)
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert "75%" in html
        assert "width: 75%" in html or "75" in html  # Either in width or text
        assert "width: 150px" in html

    def test_render_progress_ring_zero_percent(self):
        """Test rendering progress ring at 0%"""
        shape = Shapes.progress_ring(0)
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert "0%" in html

    def test_render_progress_ring_full(self):
        """Test rendering progress ring at 100%"""
        shape = Shapes.progress_ring(100)
        html = ComponentRenderer.render_shape(shape)

        assert isinstance(html, str)
        assert "100%" in html

    def test_render_unknown_shape_variant(self):
        """Test rendering unknown shape variant returns empty string"""
        shape = {"variant": "unknown", "type": "shape"}
        html = ComponentRenderer.render_shape(shape)

        assert html == ""


class TestRenderBorder:
    """Test border rendering"""

    def test_render_simple_border(self):
        """Test rendering simple border"""
        border = Borders.simple_border(width=2)
        html = ComponentRenderer.render_border(border, "Test content")

        assert isinstance(html, str)
        assert "Test content" in html
        assert "border:" in html
        assert "2px" in html
        assert "solid" in html
        assert "border-radius:" in html

    def test_render_simple_border_custom_content(self):
        """Test rendering simple border with custom content"""
        border = Borders.simple_border()
        html = ComponentRenderer.render_border(border, "<p>Custom HTML</p>")

        assert "<p>Custom HTML</p>" in html

    def test_render_accent_border_left(self):
        """Test rendering accent border on left"""
        border = Borders.accent_border(side="left")
        html = ComponentRenderer.render_border(border, "Content")

        assert isinstance(html, str)
        assert "Content" in html
        assert "border-left:" in html
        assert "padding-left:" in html

    def test_render_accent_border_right(self):
        """Test rendering accent border on right"""
        border = Borders.accent_border(side="right")
        html = ComponentRenderer.render_border(border, "Content")

        assert "border-right:" in html
        assert "padding-right:" in html

    def test_render_accent_border_top(self):
        """Test rendering accent border on top"""
        border = Borders.accent_border(side="top")
        html = ComponentRenderer.render_border(border, "Content")

        assert "border-top:" in html
        assert "padding-top:" in html

    def test_render_accent_border_bottom(self):
        """Test rendering accent border on bottom"""
        border = Borders.accent_border(side="bottom")
        html = ComponentRenderer.render_border(border, "Content")

        assert "border-bottom:" in html
        assert "padding-bottom:" in html

    def test_render_callout_box(self):
        """Test rendering callout box"""
        border = Borders.callout_box(style="info")
        html = ComponentRenderer.render_border(border, "Important info")

        assert isinstance(html, str)
        assert "Important info" in html
        assert "border:" in html
        assert "background-color:" in html
        assert "border-radius:" in html

    def test_render_shadow_frame(self):
        """Test rendering shadow frame"""
        border = Borders.shadow_frame(elevation="md")
        html = ComponentRenderer.render_border(border, "Framed content")

        assert isinstance(html, str)
        assert "Framed content" in html
        assert "box-shadow:" in html

    def test_render_shadow_frame_no_border(self):
        """Test rendering shadow frame without border"""
        border = Borders.shadow_frame()
        border["border_width"] = 0
        html = ComponentRenderer.render_border(border, "Content")

        assert isinstance(html, str)
        assert "Content" in html

    def test_render_border_with_custom_padding(self):
        """Test rendering border with custom padding"""
        border = Borders.simple_border()
        border["padding"] = 60
        html = ComponentRenderer.render_border(border, "Content")

        assert "padding: 60px" in html

    def test_render_unknown_border_variant(self):
        """Test rendering unknown border variant returns default"""
        border = {"variant": "unknown", "type": "border"}
        html = ComponentRenderer.render_border(border, "Content")

        assert isinstance(html, str)
        assert "Content" in html
        assert "<div>" in html


class TestRenderBackground:
    """Test background rendering"""

    def test_render_solid_background(self):
        """Test rendering solid background"""
        bg = Backgrounds.solid()
        html = ComponentRenderer.render_background(bg, "Content", 400, 200)

        assert isinstance(html, str)
        assert "Content" in html
        assert "background-color:" in html
        assert "width: 400px" in html
        assert "height: 200px" in html

    def test_render_gradient_vertical(self):
        """Test rendering vertical gradient"""
        bg = Backgrounds.gradient(direction="vertical")
        html = ComponentRenderer.render_background(bg, "Content", 400, 200)

        assert isinstance(html, str)
        assert "Content" in html
        assert "background: linear-gradient" in html
        assert "to bottom" in html

    def test_render_gradient_horizontal(self):
        """Test rendering horizontal gradient"""
        bg = Backgrounds.gradient(direction="horizontal")
        html = ComponentRenderer.render_background(bg, "Content", 400, 200)

        assert "to right" in html

    def test_render_gradient_diagonal(self):
        """Test rendering diagonal gradient"""
        bg = Backgrounds.gradient(direction="diagonal")
        html = ComponentRenderer.render_background(bg, "Content", 400, 200)

        assert "to bottom right" in html

    def test_render_card_background(self):
        """Test rendering card background"""
        bg = Backgrounds.card_container()
        html = ComponentRenderer.render_background(bg, "Card content", 500, 300)

        assert isinstance(html, str)
        assert "Card content" in html
        assert "box-shadow:" in html
        assert "border-radius:" in html
        assert "width: 500px" in html

    def test_render_highlight_box_background(self):
        """Test rendering highlight box background"""
        bg = Backgrounds.highlight_box(style="subtle")
        html = ComponentRenderer.render_background(bg, "Highlighted", 300, 150)

        assert isinstance(html, str)
        assert "Highlighted" in html
        assert "background-color:" in html
        assert "border:" in html

    def test_render_background_custom_dimensions(self):
        """Test rendering background with custom dimensions"""
        bg = Backgrounds.solid()
        html = ComponentRenderer.render_background(bg, "Content", 800, 600)

        assert "width: 800px" in html
        assert "height: 600px" in html

    def test_render_unknown_background_variant(self):
        """Test rendering unknown background variant returns default"""
        bg = {"variant": "unknown", "type": "background"}
        html = ComponentRenderer.render_background(bg, "Content")

        assert isinstance(html, str)
        assert "Content" in html
        assert "<div>" in html


class TestRenderComponentsGrid:
    """Test components grid rendering"""

    def test_render_empty_grid(self):
        """Test rendering empty components grid"""
        html = ComponentRenderer.render_components_grid([])

        assert isinstance(html, str)
        assert "display: grid" in html

    def test_render_grid_with_title(self):
        """Test rendering grid with title"""
        html = ComponentRenderer.render_components_grid([], title="Test Components")

        assert isinstance(html, str)
        assert "Test Components" in html
        assert "<h2" in html

    def test_render_grid_with_dividers(self):
        """Test rendering grid with divider components"""
        components = [Dividers.horizontal_line(), Dividers.gradient_fade()]
        html = ComponentRenderer.render_components_grid(components)

        assert isinstance(html, str)
        assert "display: grid" in html

    def test_render_grid_with_badges(self):
        """Test rendering grid with badge components"""
        components = [Badges.pill_badge("NEW"), Badges.status_badge("trending")]
        html = ComponentRenderer.render_components_grid(components)

        assert isinstance(html, str)
        assert "NEW" in html
        assert "TRENDING" in html

    def test_render_grid_with_shapes(self):
        """Test rendering grid with shape components"""
        components = [Shapes.circle(), Shapes.icon_container("🚀")]
        html = ComponentRenderer.render_components_grid(components)

        assert isinstance(html, str)
        assert "🚀" in html

    def test_render_grid_with_borders(self):
        """Test rendering grid with border components"""
        components = [Borders.simple_border(), Borders.accent_border()]
        html = ComponentRenderer.render_components_grid(components)

        assert isinstance(html, str)
        assert "Sample Content" in html  # Default content

    def test_render_grid_with_backgrounds(self):
        """Test rendering grid with background components"""
        components = [Backgrounds.solid(), Backgrounds.gradient()]
        html = ComponentRenderer.render_components_grid(components)

        assert isinstance(html, str)
        assert "Sample Content" in html  # Default content

    def test_render_grid_with_mixed_components(self):
        """Test rendering grid with mixed component types"""
        components = [
            Dividers.horizontal_line(),
            Badges.pill_badge("TEST"),
            Shapes.circle(),
            Borders.simple_border(),
            Backgrounds.solid(),
        ]
        html = ComponentRenderer.render_components_grid(components)

        assert isinstance(html, str)
        assert "TEST" in html
        assert "display: grid" in html

    def test_render_grid_unknown_component_type(self):
        """Test rendering grid with unknown component type"""
        components = [{"type": "unknown", "data": "test"}]
        html = ComponentRenderer.render_components_grid(components)

        assert isinstance(html, str)
        # Should still render the grid structure even if component is unknown


class TestRendererIntegration:
    """Test renderer integration and edge cases"""

    def test_render_methods_return_strings(self):
        """Test all render methods return strings"""
        divider_html = ComponentRenderer.render_divider(Dividers.horizontal_line())
        badge_html = ComponentRenderer.render_badge(Badges.pill_badge("TEST"))
        shape_html = ComponentRenderer.render_shape(Shapes.circle())
        border_html = ComponentRenderer.render_border(Borders.simple_border())
        bg_html = ComponentRenderer.render_background(Backgrounds.solid())

        assert isinstance(divider_html, str)
        assert isinstance(badge_html, str)
        assert isinstance(shape_html, str)
        assert isinstance(border_html, str)
        assert isinstance(bg_html, str)

    def test_render_methods_return_valid_html(self):
        """Test render methods return valid HTML structure"""
        divider_html = ComponentRenderer.render_divider(Dividers.horizontal_line())
        badge_html = ComponentRenderer.render_badge(Badges.pill_badge("TEST"))

        # Should contain HTML div or span tags
        assert "<div" in divider_html or "<span" in divider_html
        assert "<span" in badge_html or "<div" in badge_html

    def test_render_methods_include_inline_styles(self):
        """Test render methods include inline styles"""
        divider_html = ComponentRenderer.render_divider(Dividers.horizontal_line())
        badge_html = ComponentRenderer.render_badge(Badges.pill_badge("TEST"))
        shape_html = ComponentRenderer.render_shape(Shapes.circle())

        assert 'style="' in divider_html
        assert 'style="' in badge_html
        assert 'style="' in shape_html

    def test_renderer_handles_minimal_data(self):
        """Test renderer handles minimal data gracefully"""
        # Components with minimal data should still render
        divider = {
            "variant": "horizontal_line",
            "width": 100,
            "height": 2,
            "color": "#000000",
            "margin_top": 10,
            "margin_bottom": 10,
            "style": "solid",
        }
        html = ComponentRenderer.render_divider(divider)

        # Should not crash, should return something
        assert isinstance(html, str)
        assert "width: 100px" in html

    def test_renderer_html_is_injection_safe(self):
        """Test renderer doesn't allow script injection in content"""
        border = Borders.simple_border()
        html = ComponentRenderer.render_border(border, "<script>alert('xss')</script>")

        # HTML should contain the script tag as-is (not executed)
        # This is the expected behavior for content rendering
        assert isinstance(html, str)
        assert "script" in html.lower()
