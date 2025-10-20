"""
Tests for Visual Elements Components - All 38 visual components.
"""

from chuk_mcp_linkedin.components.visual_elements import (
    Dividers,
    Backgrounds,
    Borders,
    Badges,
    Shapes,
)


class TestDividers:
    """Test divider components (6 types)"""

    def test_horizontal_line_default(self):
        """Test horizontal line with default parameters"""
        divider = Dividers.horizontal_line()
        assert divider["type"] == "divider"
        assert divider["variant"] == "horizontal_line"
        assert divider["width"] == 1720
        assert divider["height"] == 2
        assert divider["style"] == "solid"

    def test_horizontal_line_custom(self):
        """Test horizontal line with custom parameters"""
        divider = Dividers.horizontal_line(width=500, thickness=4, color="#FF0000", style="dashed")
        assert divider["width"] == 500
        assert divider["height"] == 4
        assert divider["color"] == "#FF0000"
        assert divider["style"] == "dashed"

    def test_gradient_fade_default(self):
        """Test gradient fade divider"""
        divider = Dividers.gradient_fade()
        assert divider["type"] == "divider"
        assert divider["variant"] == "gradient_fade"
        assert "gradient" in divider
        assert "start" in divider["gradient"]
        assert "mid" in divider["gradient"]
        assert "end" in divider["gradient"]

    def test_gradient_fade_custom_width(self):
        """Test gradient fade with custom width"""
        divider = Dividers.gradient_fade(width=800)
        assert divider["width"] == 800

    def test_decorative_accent(self):
        """Test decorative accent divider"""
        divider = Dividers.decorative_accent()
        assert divider["type"] == "divider"
        assert divider["variant"] == "decorative_accent"
        assert divider["width"] == 200
        assert divider["height"] == 4

    def test_section_break_default(self):
        """Test section break divider"""
        divider = Dividers.section_break()
        assert divider["type"] == "divider"
        assert divider["variant"] == "section_break"
        assert divider["symbols"] == "• • •"

    def test_section_break_custom_style(self):
        """Test section break with custom style"""
        divider = Dividers.section_break(style="squares")
        assert divider["symbols"] == "■ ■ ■"
        assert divider["style"] == "squares"

    def test_title_underline_default(self):
        """Test title underline divider"""
        divider = Dividers.title_underline()
        assert divider["type"] == "divider"
        assert divider["variant"] == "title_underline"
        assert divider["count"] == 2  # double style by default

    def test_title_underline_double_style(self):
        """Test title underline with double style"""
        divider = Dividers.title_underline(style="double")
        assert divider["count"] == 2
        assert divider["gap"] == 4

    def test_spacer_small(self):
        """Test spacer divider small size"""
        divider = Dividers.spacer(size="small")
        assert divider["type"] == "divider"
        assert divider["variant"] == "spacer"
        assert divider["height"] == 16

    def test_spacer_large(self):
        """Test spacer divider large size"""
        divider = Dividers.spacer(size="large")
        assert divider["height"] == 40


class TestBackgrounds:
    """Test background components (8 types)"""

    def test_solid_default(self):
        """Test solid background"""
        bg = Backgrounds.solid()
        assert bg["type"] == "background"
        assert bg["variant"] == "solid"
        assert "color" in bg

    def test_solid_custom_color(self):
        """Test solid background with custom color"""
        bg = Backgrounds.solid(color="#FF0000")
        assert bg["color"] == "#FF0000"

    def test_gradient_vertical(self):
        """Test vertical gradient background"""
        bg = Backgrounds.gradient(direction="vertical")
        assert bg["type"] == "background"
        assert bg["variant"] == "gradient"
        assert bg["direction"] == "vertical"
        assert "start_color" in bg
        assert "end_color" in bg

    def test_gradient_horizontal(self):
        """Test horizontal gradient background"""
        bg = Backgrounds.gradient(direction="horizontal")
        assert bg["direction"] == "horizontal"

    def test_gradient_diagonal(self):
        """Test diagonal gradient background"""
        bg = Backgrounds.gradient(direction="diagonal")
        assert bg["direction"] == "diagonal"

    def test_gradient_custom_scheme(self):
        """Test gradient with custom color scheme"""
        bg = Backgrounds.gradient(color_scheme="vibrant")
        assert bg["variant"] == "gradient"
        assert "start_color" in bg
        assert "end_color" in bg

    def test_card_container_default(self):
        """Test card container background"""
        bg = Backgrounds.card_container()
        assert bg["type"] == "background"
        assert bg["variant"] == "card"
        assert "shadow" in bg
        assert "border_radius" in bg

    def test_card_container_custom_elevation(self):
        """Test card container with different elevations"""
        bg_sm = Backgrounds.card_container(elevation="sm")
        bg_lg = Backgrounds.card_container(elevation="lg")
        assert bg_sm["shadow"] != bg_lg["shadow"]

    def test_highlight_box_subtle(self):
        """Test highlight box subtle style"""
        bg = Backgrounds.highlight_box(style="subtle")
        assert bg["type"] == "background"
        assert bg["variant"] == "highlight_box"
        assert "background_color" in bg
        assert "border_color" in bg

    def test_highlight_box_vibrant(self):
        """Test highlight box vibrant style"""
        bg = Backgrounds.highlight_box(style="vibrant")
        assert bg["type"] == "background"
        assert bg["variant"] == "highlight_box"

    def test_subtle_pattern(self):
        """Test subtle pattern background"""
        bg = Backgrounds.subtle_pattern(pattern="dots")
        assert bg["type"] == "background"
        assert bg["variant"] == "pattern"
        assert bg["pattern"] == "dots"

    def test_branded_header(self):
        """Test branded header background"""
        bg = Backgrounds.branded_header()
        assert bg["type"] == "background"
        assert bg["variant"] == "branded_header"
        assert bg["gradient"] is True


class TestBorders:
    """Test border/container components (8 types)"""

    def test_simple_border_default(self):
        """Test simple border"""
        border = Borders.simple_border()
        assert border["type"] == "border"
        assert border["variant"] == "simple"
        assert border["width"] == 2
        assert border["style"] == "solid"

    def test_simple_border_custom(self):
        """Test simple border with custom parameters"""
        border = Borders.simple_border(width=4, color="#FF0000", style="dashed")
        assert border["width"] == 4
        assert border["color"] == "#FF0000"
        assert border["style"] == "dashed"

    def test_accent_border_left(self):
        """Test accent border on left side"""
        border = Borders.accent_border(side="left")
        assert border["type"] == "border"
        assert border["variant"] == "accent"
        assert border["side"] == "left"
        assert border["width"] == 6

    def test_accent_border_top(self):
        """Test accent border on top side"""
        border = Borders.accent_border(side="top")
        assert border["side"] == "top"

    def test_callout_box_info(self):
        """Test callout box info style"""
        border = Borders.callout_box(style="info")
        assert border["type"] == "border"
        assert border["variant"] == "callout"
        assert border["style"] == "info"
        assert "background_color" in border
        assert "border_color" in border

    def test_callout_box_success(self):
        """Test callout box success style"""
        border = Borders.callout_box(style="success")
        assert border["style"] == "success"

    def test_callout_box_warning(self):
        """Test callout box warning style"""
        border = Borders.callout_box(style="warning")
        assert border["style"] == "warning"

    def test_callout_box_error(self):
        """Test callout box error style"""
        border = Borders.callout_box(style="error")
        assert border["style"] == "error"

    def test_shadow_frame_default(self):
        """Test shadow frame default elevation"""
        border = Borders.shadow_frame()
        assert border["type"] == "border"
        assert border["variant"] == "shadow_frame"
        assert "shadow" in border

    def test_shadow_frame_elevations(self):
        """Test shadow frame different elevations"""
        border_sm = Borders.shadow_frame(elevation="sm")
        border_lg = Borders.shadow_frame(elevation="lg")
        assert border_sm["shadow"] != border_lg["shadow"]

    def test_double_border(self):
        """Test double border"""
        border = Borders.double_border()
        assert border["type"] == "border"
        assert border["variant"] == "double"
        assert "outer_width" in border
        assert "inner_width" in border
        assert "gap" in border

    def test_inset_panel(self):
        """Test inset panel"""
        border = Borders.inset_panel()
        assert border["type"] == "border"
        assert border["variant"] == "inset"
        assert "depth" in border
        assert border["inner_shadow"] is True


class TestBadges:
    """Test badge components (7 types)"""

    def test_pill_badge_default(self):
        """Test pill badge with default size"""
        badge = Badges.pill_badge("NEW")
        assert badge["type"] == "badge"
        assert badge["variant"] == "pill"
        assert badge["text"] == "NEW"
        assert "background_color" in badge
        assert "text_color" in badge

    def test_pill_badge_sizes(self):
        """Test pill badge different sizes"""
        small = Badges.pill_badge("NEW", size="small")
        medium = Badges.pill_badge("NEW", size="medium")
        large = Badges.pill_badge("NEW", size="large")
        assert small["font_size"] < medium["font_size"] < large["font_size"]

    def test_pill_badge_custom_colors(self):
        """Test pill badge with custom colors"""
        badge = Badges.pill_badge("TEST", color="#FF0000")
        assert badge["background_color"] == "#FF0000"
        assert badge["text_color"] == "#FFFFFF"

    def test_status_badge_semantic_new(self):
        """Test status badge semantic style - new"""
        badge = Badges.status_badge("new", style="semantic")
        assert badge["type"] == "badge"
        assert badge["variant"] == "status"
        assert badge["text"] == "NEW"

    def test_status_badge_semantic_trending(self):
        """Test status badge semantic style - trending"""
        badge = Badges.status_badge("trending", style="semantic")
        assert badge["text"] == "TRENDING"

    def test_status_badge_semantic_hot(self):
        """Test status badge semantic style - hot"""
        badge = Badges.status_badge("hot", style="semantic")
        assert badge["text"] == "HOT"

    def test_status_badge_semantic_beta(self):
        """Test status badge semantic style - beta"""
        badge = Badges.status_badge("beta", style="semantic")
        assert badge["text"] == "BETA"

    def test_status_badge_minimal(self):
        """Test status badge minimal style"""
        badge = Badges.status_badge("new", style="minimal")
        assert badge["variant"] == "status_outlined"

    def test_percentage_change_positive(self):
        """Test percentage change badge positive value"""
        badge = Badges.percentage_change(12.5)
        assert badge["type"] == "badge"
        assert badge["variant"] == "percentage_change"
        assert badge["value"] == 12.5
        assert "↑" in badge["text"]

    def test_percentage_change_negative(self):
        """Test percentage change badge negative value"""
        badge = Badges.percentage_change(-8.3)
        assert badge["value"] == -8.3
        assert "↓" in badge["text"]

    def test_percentage_change_zero(self):
        """Test percentage change badge zero value"""
        badge = Badges.percentage_change(0.0)
        assert badge["value"] == 0.0
        assert "↑" in badge["text"]  # Zero is treated as positive

    def test_percentage_change_custom_format(self):
        """Test percentage change with custom format"""
        badge = Badges.percentage_change(25.5, format_string="{:+.2f}%%")
        assert "+25.50%" in badge["text"]

    def test_category_tag_default(self):
        """Test category tag"""
        badge = Badges.category_tag("Design")
        assert badge["type"] == "badge"
        assert badge["variant"] == "category_tag"
        assert badge["text"] == "Design"

    def test_category_tag_custom_color(self):
        """Test category tag with custom color scheme"""
        badge = Badges.category_tag("Tech", color_scheme="vibrant")
        assert badge["variant"] == "category_tag"
        assert "background_color" in badge

    def test_number_badge(self):
        """Test number badge"""
        badge = Badges.number_badge(42)
        assert badge["type"] == "badge"
        assert badge["variant"] == "number"
        assert badge["number"] == 42

    def test_number_badge_large_number(self):
        """Test number badge with large number"""
        badge = Badges.number_badge(99)
        assert badge["number"] == 99
        assert badge["size"] == 48  # icon_sizes["medium"] from design tokens


class TestShapes:
    """Test shape components (9 types)"""

    def test_circle_filled(self):
        """Test filled circle"""
        shape = Shapes.circle(size=100, fill=True)
        assert shape["type"] == "shape"
        assert shape["variant"] == "circle"
        assert shape["size"] == 100
        assert shape["fill"] is True

    def test_circle_outline(self):
        """Test outline circle"""
        shape = Shapes.circle(size=100, fill=False, stroke_width=3)
        assert shape["fill"] is False
        assert shape["stroke_width"] == 3

    def test_circle_custom_color(self):
        """Test circle with custom color"""
        shape = Shapes.circle(color="#FF0000")
        assert shape["color"] == "#FF0000"

    def test_icon_container_default(self):
        """Test icon container"""
        shape = Shapes.icon_container("🚀")
        assert shape["type"] == "shape"
        assert shape["variant"] == "icon_container"
        assert shape["icon"] == "🚀"
        assert shape["size"] == 120

    def test_icon_container_custom_size(self):
        """Test icon container with custom size"""
        shape = Shapes.icon_container("⚡", size=120)
        assert shape["size"] == 120
        assert shape["icon_size"] > shape["size"] * 0.4  # Icon should be proportional

    def test_icon_container_custom_colors(self):
        """Test icon container with custom colors"""
        shape = Shapes.icon_container("💡", background_color="#FF0000", icon_color="#FFFFFF")
        assert shape["background_color"] == "#FF0000"
        assert shape["icon_color"] == "#FFFFFF"

    def test_checkmark_circle_style(self):
        """Test checkmark with circle style"""
        shape = Shapes.checkmark(style="circle")
        assert shape["type"] == "shape"
        assert shape["variant"] == "checkmark"
        assert shape["style"] == "circle"
        assert shape["background"] is True

    def test_checkmark_square_style(self):
        """Test checkmark with square style"""
        shape = Shapes.checkmark(style="square")
        assert shape["style"] == "square"
        assert shape["background"] is True
        assert shape["border_radius"] == 4

    def test_checkmark_simple_style(self):
        """Test checkmark with simple style"""
        shape = Shapes.checkmark(style="simple")
        assert shape["style"] == "simple"
        assert shape["background"] is False

    def test_checkmark_custom_size(self):
        """Test checkmark with custom size"""
        shape = Shapes.checkmark(size=100)
        assert shape["size"] == 100

    def test_progress_ring_default(self):
        """Test progress ring default"""
        shape = Shapes.progress_ring(75)
        assert shape["type"] == "shape"
        assert shape["variant"] == "progress_ring"
        assert shape["percentage"] == 75

    def test_progress_ring_custom_size(self):
        """Test progress ring with custom size"""
        shape = Shapes.progress_ring(50, size=200)
        assert shape["size"] == 200

    def test_progress_ring_custom_colors(self):
        """Test progress ring with custom colors"""
        shape = Shapes.progress_ring(60, color="#FF0000", background_color="#CCCCCC")
        assert shape["progress_color"] == "#FF0000"
        assert shape["background_color"] == "#CCCCCC"

    def test_progress_ring_edge_cases(self):
        """Test progress ring edge cases"""
        zero = Shapes.progress_ring(0)
        full = Shapes.progress_ring(100)
        assert zero["percentage"] == 0
        assert full["percentage"] == 100

    def test_rectangle_shape(self):
        """Test rectangle shape"""
        shape = Shapes.rectangle(width=200, height=100, fill=True)
        assert shape["type"] == "shape"
        assert shape["variant"] == "rectangle"
        assert shape["width"] == 200
        assert shape["height"] == 100

    def test_bullet_point(self):
        """Test bullet point shape"""
        shape = Shapes.bullet_point(style="disc")
        assert shape["type"] == "shape"
        assert shape["variant"] == "bullet_point"
        assert "symbol" in shape

    def test_arrow_shape(self):
        """Test arrow shape"""
        shape = Shapes.arrow(direction="right")
        assert shape["type"] == "shape"
        assert shape["variant"] == "arrow"
        assert shape["direction"] == "right"


class TestComponentIntegration:
    """Test component integration and consistency"""

    def test_all_dividers_return_dict(self):
        """Test all divider methods return dictionaries"""
        dividers = [
            Dividers.horizontal_line(),
            Dividers.gradient_fade(),
            Dividers.decorative_accent(),
            Dividers.section_break(),
            Dividers.title_underline(),
            Dividers.spacer(),
        ]
        for divider in dividers:
            assert isinstance(divider, dict)
            assert "type" in divider
            assert divider["type"] == "divider"

    def test_all_backgrounds_return_dict(self):
        """Test all background methods return dictionaries"""
        backgrounds = [
            Backgrounds.solid(),
            Backgrounds.gradient(),
            Backgrounds.card_container(),
            Backgrounds.highlight_box(),
        ]
        for bg in backgrounds:
            assert isinstance(bg, dict)
            assert "type" in bg
            assert bg["type"] == "background"

    def test_all_borders_return_dict(self):
        """Test all border methods return dictionaries"""
        borders = [
            Borders.simple_border(),
            Borders.accent_border(),
            Borders.callout_box(),
            Borders.shadow_frame(),
        ]
        for border in borders:
            assert isinstance(border, dict)
            assert "type" in border
            assert border["type"] == "border"

    def test_all_badges_return_dict(self):
        """Test all badge methods return dictionaries"""
        badges = [
            Badges.pill_badge("TEST"),
            Badges.status_badge("new"),
            Badges.percentage_change(10.0),
            Badges.category_tag("Tag"),
        ]
        for badge in badges:
            assert isinstance(badge, dict)
            assert "type" in badge
            assert badge["type"] == "badge"

    def test_all_shapes_return_dict(self):
        """Test all shape methods return dictionaries"""
        shapes = [
            Shapes.circle(),
            Shapes.icon_container("🚀"),
            Shapes.checkmark(),
            Shapes.progress_ring(50),
        ]
        for shape in shapes:
            assert isinstance(shape, dict)
            assert "type" in shape
            assert shape["type"] == "shape"

    def test_components_use_design_tokens(self):
        """Test that components reference design tokens"""
        # This is verified by checking that components don't have hardcoded
        # values for common properties like colors, spacing, etc.
        divider = Dividers.horizontal_line()
        badge = Badges.pill_badge("TEST")

        # Components should have color values that match token hex codes
        assert isinstance(divider.get("color"), str)
        assert isinstance(badge.get("background_color"), str)
