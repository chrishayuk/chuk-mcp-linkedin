"""
Tests for Document Layouts - All 11 layout types.
"""

from chuk_mcp_linkedin.components.layouts.base import LayoutConfig, LayoutType, LayoutZone
from chuk_mcp_linkedin.documents.layouts import (
    title_slide,
    content_slide,
    split_content,
    big_number,
    quote_slide,
    comparison,
    two_column,
    checklist,
    timeline,
    icon_grid,
    data_visual,
    DocumentLayouts,
)


class TestTitleSlideLayout:
    """Test title slide layout"""

    def test_title_slide_returns_config(self):
        """Test title_slide returns LayoutConfig"""
        layout = title_slide()
        assert isinstance(layout, LayoutConfig)

    def test_title_slide_has_correct_type(self):
        """Test title_slide has correct type"""
        layout = title_slide()
        assert layout.type == LayoutType.TITLE_SLIDE

    def test_title_slide_has_title_zone(self):
        """Test title_slide has title zone"""
        layout = title_slide()
        assert layout.title_zone is not None
        assert isinstance(layout.title_zone, LayoutZone)

    def test_title_slide_has_subtitle_zone(self):
        """Test title_slide has subtitle zone"""
        layout = title_slide()
        assert layout.subtitle_zone is not None
        assert isinstance(layout.subtitle_zone, LayoutZone)

    def test_title_slide_name(self):
        """Test title_slide has correct name"""
        layout = title_slide()
        assert layout.name == "Title Slide"

    def test_title_slide_has_description(self):
        """Test title_slide has description"""
        layout = title_slide()
        assert layout.description
        assert isinstance(layout.description, str)


class TestContentSlideLayout:
    """Test content slide layout"""

    def test_content_slide_returns_config(self):
        """Test content_slide returns LayoutConfig"""
        layout = content_slide()
        assert isinstance(layout, LayoutConfig)

    def test_content_slide_has_correct_type(self):
        """Test content_slide has correct type"""
        layout = content_slide()
        assert layout.type == LayoutType.CONTENT_SLIDE

    def test_content_slide_has_title_zone(self):
        """Test content_slide has title zone"""
        layout = content_slide()
        assert layout.title_zone is not None

    def test_content_slide_has_content_zone(self):
        """Test content_slide has content zone"""
        layout = content_slide()
        assert layout.content_zone is not None

    def test_content_slide_name(self):
        """Test content_slide has correct name"""
        layout = content_slide()
        assert layout.name == "Content Slide"


class TestSplitContentLayout:
    """Test split content layout"""

    def test_split_content_returns_config(self):
        """Test split_content returns LayoutConfig"""
        layout = split_content()
        assert isinstance(layout, LayoutConfig)

    def test_split_content_has_correct_type(self):
        """Test split_content has correct type"""
        layout = split_content()
        assert layout.type == LayoutType.SPLIT_CONTENT

    def test_split_content_has_two_content_zones(self):
        """Test split_content has two content zones"""
        layout = split_content()
        assert layout.content_zone is not None
        assert layout.image_zone is not None

    def test_split_content_name(self):
        """Test split_content has correct name"""
        layout = split_content()
        assert layout.name == "Split Content"


class TestBigNumberLayout:
    """Test big number layout"""

    def test_big_number_returns_config(self):
        """Test big_number returns LayoutConfig"""
        layout = big_number()
        assert isinstance(layout, LayoutConfig)

    def test_big_number_has_correct_type(self):
        """Test big_number has correct type"""
        layout = big_number()
        assert layout.type == LayoutType.BIG_NUMBER

    def test_big_number_has_title_zone(self):
        """Test big_number has title zone for the stat"""
        layout = big_number()
        assert layout.title_zone is not None

    def test_big_number_title_zone_font_size(self):
        """Test big_number title zone has large font"""
        layout = big_number()
        # Should use hero or massive font size
        assert layout.title_zone.font_size >= 120

    def test_big_number_name(self):
        """Test big_number has correct name"""
        layout = big_number()
        assert layout.name == "Big Number"


class TestQuoteSlideLayout:
    """Test quote slide layout"""

    def test_quote_slide_returns_config(self):
        """Test quote_slide returns LayoutConfig"""
        layout = quote_slide()
        assert isinstance(layout, LayoutConfig)

    def test_quote_slide_has_correct_type(self):
        """Test quote_slide has correct type"""
        layout = quote_slide()
        assert layout.type == LayoutType.QUOTE

    def test_quote_slide_has_content_zone(self):
        """Test quote_slide has content zone for quote"""
        layout = quote_slide()
        assert layout.content_zone is not None

    def test_quote_slide_has_subtitle_zone(self):
        """Test quote_slide has subtitle zone for attribution"""
        layout = quote_slide()
        assert layout.subtitle_zone is not None

    def test_quote_slide_name(self):
        """Test quote_slide has correct name"""
        layout = quote_slide()
        assert layout.name == "Quote Slide"


class TestComparisonLayout:
    """Test comparison layout"""

    def test_comparison_returns_config(self):
        """Test comparison returns LayoutConfig"""
        layout = comparison()
        assert isinstance(layout, LayoutConfig)

    def test_comparison_has_correct_type(self):
        """Test comparison has correct type"""
        layout = comparison()
        assert layout.type == LayoutType.COMPARISON

    def test_comparison_has_title_zone(self):
        """Test comparison has title zone"""
        layout = comparison()
        assert layout.title_zone is not None

    def test_comparison_has_two_content_zones(self):
        """Test comparison has content_zone and content_zone_2"""
        layout = comparison()
        assert layout.content_zone is not None
        assert layout.content_zone_2 is not None

    def test_comparison_name(self):
        """Test comparison has correct name"""
        layout = comparison()
        assert layout.name == "Comparison"


class TestTwoColumnLayout:
    """Test two column layout"""

    def test_two_column_returns_config(self):
        """Test two_column returns LayoutConfig"""
        layout = two_column()
        assert isinstance(layout, LayoutConfig)

    def test_two_column_has_correct_type(self):
        """Test two_column has correct type"""
        layout = two_column()
        assert layout.type == LayoutType.TWO_COLUMN

    def test_two_column_has_content_zone(self):
        """Test two_column has content_zone"""
        layout = two_column()
        assert layout.content_zone is not None

    def test_two_column_has_content_zone_2(self):
        """Test two_column has content_zone_2"""
        layout = two_column()
        assert layout.content_zone_2 is not None

    def test_two_column_name(self):
        """Test two_column has correct name"""
        layout = two_column()
        assert layout.name == "Two Column"


class TestChecklistLayout:
    """Test checklist layout"""

    def test_checklist_returns_config(self):
        """Test checklist returns LayoutConfig"""
        layout = checklist()
        assert isinstance(layout, LayoutConfig)

    def test_checklist_has_correct_type(self):
        """Test checklist has correct type"""
        layout = checklist()
        assert layout.type == LayoutType.CHECKLIST

    def test_checklist_has_title_zone(self):
        """Test checklist has title zone"""
        layout = checklist()
        assert layout.title_zone is not None

    def test_checklist_has_content_zone(self):
        """Test checklist has content zone"""
        layout = checklist()
        assert layout.content_zone is not None

    def test_checklist_name(self):
        """Test checklist has correct name"""
        layout = checklist()
        assert layout.name == "Checklist"


class TestTimelineLayout:
    """Test timeline layout"""

    def test_timeline_returns_config(self):
        """Test timeline returns LayoutConfig"""
        layout = timeline()
        assert isinstance(layout, LayoutConfig)

    def test_timeline_has_correct_type(self):
        """Test timeline has correct type"""
        layout = timeline()
        assert layout.type == LayoutType.TIMELINE

    def test_timeline_has_title_zone(self):
        """Test timeline has title zone"""
        layout = timeline()
        assert layout.title_zone is not None

    def test_timeline_has_content_zone(self):
        """Test timeline has content zone"""
        layout = timeline()
        assert layout.content_zone is not None

    def test_timeline_name(self):
        """Test timeline has correct name"""
        layout = timeline()
        assert layout.name == "Timeline"


class TestIconGridLayout:
    """Test icon grid layout"""

    def test_icon_grid_returns_config(self):
        """Test icon_grid returns LayoutConfig"""
        layout = icon_grid()
        assert isinstance(layout, LayoutConfig)

    def test_icon_grid_has_correct_type(self):
        """Test icon_grid has correct type"""
        layout = icon_grid()
        assert layout.type == LayoutType.ICON_GRID

    def test_icon_grid_has_title_zone(self):
        """Test icon_grid has title zone"""
        layout = icon_grid()
        assert layout.title_zone is not None

    def test_icon_grid_has_grid_zones(self):
        """Test icon_grid has grid zones"""
        layout = icon_grid()
        # Should have multiple grid zones
        assert hasattr(layout, "grid_zones") or layout.content_zone is not None

    def test_icon_grid_name(self):
        """Test icon_grid has correct name"""
        layout = icon_grid()
        assert layout.name == "Icon Grid"


class TestDataVisualLayout:
    """Test data visual layout"""

    def test_data_visual_returns_config(self):
        """Test data_visual returns LayoutConfig"""
        layout = data_visual()
        assert isinstance(layout, LayoutConfig)

    def test_data_visual_has_correct_type(self):
        """Test data_visual has correct type"""
        layout = data_visual()
        assert layout.type == LayoutType.DATA_VISUAL

    def test_data_visual_has_title_zone(self):
        """Test data_visual has title zone"""
        layout = data_visual()
        assert layout.title_zone is not None

    def test_data_visual_has_image_zone(self):
        """Test data_visual has image zone"""
        layout = data_visual()
        assert layout.image_zone is not None

    def test_data_visual_name(self):
        """Test data_visual has correct name"""
        layout = data_visual()
        assert layout.name == "Data Visual"


class TestDocumentLayoutsClass:
    """Test DocumentLayouts aggregator class"""

    def test_document_layouts_has_all_layouts(self):
        """Test DocumentLayouts has all 11 layout functions"""
        assert hasattr(DocumentLayouts, "title_slide")
        assert hasattr(DocumentLayouts, "content_slide")
        assert hasattr(DocumentLayouts, "split_content")
        assert hasattr(DocumentLayouts, "big_number")
        assert hasattr(DocumentLayouts, "quote_slide")
        assert hasattr(DocumentLayouts, "comparison")
        assert hasattr(DocumentLayouts, "two_column")
        assert hasattr(DocumentLayouts, "checklist")
        assert hasattr(DocumentLayouts, "timeline")
        assert hasattr(DocumentLayouts, "icon_grid")
        assert hasattr(DocumentLayouts, "data_visual")

    def test_document_layouts_functions_are_callable(self):
        """Test all DocumentLayouts functions are callable"""
        assert callable(DocumentLayouts.title_slide)
        assert callable(DocumentLayouts.content_slide)
        assert callable(DocumentLayouts.split_content)
        assert callable(DocumentLayouts.big_number)
        assert callable(DocumentLayouts.quote_slide)
        assert callable(DocumentLayouts.comparison)
        assert callable(DocumentLayouts.two_column)
        assert callable(DocumentLayouts.checklist)
        assert callable(DocumentLayouts.timeline)
        assert callable(DocumentLayouts.icon_grid)
        assert callable(DocumentLayouts.data_visual)

    def test_get_all_returns_dict(self):
        """Test get_all returns a dictionary"""
        all_layouts = DocumentLayouts.get_all()
        assert isinstance(all_layouts, dict)

    def test_get_all_returns_11_layouts(self):
        """Test get_all returns all 11 layouts"""
        all_layouts = DocumentLayouts.get_all()
        assert len(all_layouts) == 11

    def test_get_all_layout_keys(self):
        """Test get_all returns correct layout keys"""
        all_layouts = DocumentLayouts.get_all()
        expected_keys = [
            "title_slide",
            "content_slide",
            "split_content",
            "big_number",
            "quote",
            "comparison",
            "two_column",
            "checklist",
            "timeline",
            "icon_grid",
            "data_visual",
        ]
        assert set(all_layouts.keys()) == set(expected_keys)

    def test_get_all_values_are_layout_configs(self):
        """Test get_all returns LayoutConfig instances"""
        all_layouts = DocumentLayouts.get_all()
        for layout in all_layouts.values():
            assert isinstance(layout, LayoutConfig)

    def test_get_layout_valid_name(self):
        """Test get_layout returns correct layout by name"""
        layout = DocumentLayouts.get_layout("title_slide")
        assert isinstance(layout, LayoutConfig)
        assert layout.name == "Title Slide"

    def test_get_layout_invalid_name(self):
        """Test get_layout with invalid name raises ValueError"""
        try:
            DocumentLayouts.get_layout("nonexistent_layout")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected

    def test_get_layout_all_names_work(self):
        """Test get_layout works for all layout names"""
        layout_names = [
            "title_slide",
            "content_slide",
            "split_content",
            "big_number",
            "quote",
            "comparison",
            "two_column",
            "checklist",
            "timeline",
            "icon_grid",
            "data_visual",
        ]
        for name in layout_names:
            layout = DocumentLayouts.get_layout(name)
            assert layout is not None
            assert isinstance(layout, LayoutConfig)


class TestLayoutConfiguration:
    """Test layout configuration and zones"""

    def test_all_layouts_have_canvas_size(self):
        """Test all layouts have canvas size defined"""
        all_layouts = DocumentLayouts.get_all()
        for layout in all_layouts.values():
            assert layout.canvas_size is not None
            assert isinstance(layout.canvas_size, tuple)
            assert len(layout.canvas_size) == 2

    def test_all_layouts_have_names(self):
        """Test all layouts have names"""
        all_layouts = DocumentLayouts.get_all()
        for layout in all_layouts.values():
            assert layout.name
            assert isinstance(layout.name, str)
            assert len(layout.name) > 0

    def test_all_layouts_have_descriptions(self):
        """Test all layouts have descriptions"""
        all_layouts = DocumentLayouts.get_all()
        for layout in all_layouts.values():
            assert layout.description
            assert isinstance(layout.description, str)

    def test_all_layouts_have_types(self):
        """Test all layouts have LayoutType"""
        all_layouts = DocumentLayouts.get_all()
        for layout in all_layouts.values():
            assert isinstance(layout.type, LayoutType)

    def test_layout_zones_have_coordinates(self):
        """Test layout zones have x, y, width, height"""
        layout = content_slide()
        if layout.title_zone:
            assert hasattr(layout.title_zone, "x")
            assert hasattr(layout.title_zone, "y")
            assert hasattr(layout.title_zone, "width")
            assert hasattr(layout.title_zone, "height")

    def test_layout_zones_coordinates_are_positive(self):
        """Test layout zone coordinates are non-negative"""
        all_layouts = DocumentLayouts.get_all()
        for layout in all_layouts.values():
            zones = []
            if hasattr(layout, "title_zone") and layout.title_zone:
                zones.append(layout.title_zone)
            if hasattr(layout, "content_zone") and layout.content_zone:
                zones.append(layout.content_zone)

            for zone in zones:
                assert zone.x >= 0
                assert zone.y >= 0
                assert zone.width > 0
                assert zone.height > 0

    def test_layout_zones_fit_within_canvas(self):
        """Test layout zones fit within canvas bounds"""
        all_layouts = DocumentLayouts.get_all()
        for layout in all_layouts.values():
            canvas_width, canvas_height = layout.canvas_size

            zones = []
            if hasattr(layout, "title_zone") and layout.title_zone:
                zones.append(layout.title_zone)
            if hasattr(layout, "content_zone") and layout.content_zone:
                zones.append(layout.content_zone)

            for zone in zones:
                assert zone.x + zone.width <= canvas_width
                assert zone.y + zone.height <= canvas_height


class TestLayoutTokenIntegration:
    """Test that layouts use design tokens"""

    def test_layouts_use_token_font_sizes(self):
        """Test layouts reference design token font sizes"""
        layout = big_number()
        # Big number should use massive or hero font size from tokens
        # which are 200 or 120, not random hardcoded values
        assert layout.title_zone.font_size in [120, 200]

    def test_layouts_use_token_spacing(self):
        """Test layouts use token-based spacing"""
        layout = content_slide()
        # Font sizes should come from token system, not hardcoded
        valid_token_sizes = [14, 18, 24, 32, 42, 56, 72, 120, 200]
        assert layout.title_zone.font_size in valid_token_sizes

    def test_layouts_use_consistent_canvas(self):
        """Test all layouts use consistent canvas from tokens"""
        all_layouts = DocumentLayouts.get_all()
        # All should use same canvas (document_square: 1920x1920)
        for layout in all_layouts.values():
            assert layout.canvas_size == (1920, 1920)
