"""
Tests for Design Tokens - Complete coverage of the design token system.
"""

from chuk_mcp_linkedin.tokens.design_tokens import DesignTokens


class TestCanvasTokens:
    """Test canvas size tokens"""

    def test_document_square_dimensions(self):
        """Test document square canvas size"""
        assert DesignTokens.CANVAS["document_square"] == (1920, 1920)

    def test_get_canvas_size_document_square(self):
        """Test get_canvas_size helper for document_square"""
        size = DesignTokens.get_canvas_size("document_square")
        assert size == (1920, 1920)

    def test_get_canvas_size_invalid(self):
        """Test get_canvas_size with invalid key returns square"""
        size = DesignTokens.get_canvas_size("nonexistent")
        assert size == (1080, 1080)  # Returns square as default


class TestTypographyTokens:
    """Test typography tokens"""

    def test_font_sizes_exist(self):
        """Test all font sizes are defined"""
        expected_sizes = [
            "tiny",
            "small",
            "body",
            "large",
            "xlarge",
            "title",
            "display",
            "hero",
            "massive",
        ]
        for size in expected_sizes:
            assert size in DesignTokens.TYPOGRAPHY["sizes"]
            assert isinstance(DesignTokens.TYPOGRAPHY["sizes"][size], int)

    def test_font_weights_exist(self):
        """Test all font weights are defined"""
        expected_weights = ["light", "normal", "medium", "semibold", "bold", "black"]
        for weight in expected_weights:
            assert weight in DesignTokens.TYPOGRAPHY["weights"]

    def test_line_heights_exist(self):
        """Test line heights are defined"""
        assert "tight" in DesignTokens.TYPOGRAPHY["line_heights"]
        assert "normal" in DesignTokens.TYPOGRAPHY["line_heights"]
        assert "relaxed" in DesignTokens.TYPOGRAPHY["line_heights"]

    def test_get_font_size_valid(self):
        """Test get_font_size helper with valid key"""
        assert DesignTokens.get_font_size("title") == 56
        assert DesignTokens.get_font_size("body") == 24
        assert DesignTokens.get_font_size("hero") == 120

    def test_get_font_size_invalid(self):
        """Test get_font_size with invalid key returns body size"""
        assert DesignTokens.get_font_size("nonexistent") == 24

    def test_mobile_minimum_font_size(self):
        """Test that small size meets LinkedIn mobile minimum (18pt)"""
        assert DesignTokens.TYPOGRAPHY["sizes"]["small"] >= 18


class TestColorTokens:
    """Test color tokens"""

    def test_minimal_palette_exists(self):
        """Test minimal color palette"""
        assert "accent" in DesignTokens.COLORS["minimal"]
        assert "primary" in DesignTokens.COLORS["minimal"]
        assert "secondary" in DesignTokens.COLORS["minimal"]
        assert "background" in DesignTokens.COLORS["minimal"]

    def test_semantic_colors_exist(self):
        """Test semantic colors"""
        assert "success" in DesignTokens.COLORS["semantic"]
        assert "warning" in DesignTokens.COLORS["semantic"]
        assert "error" in DesignTokens.COLORS["semantic"]
        assert "info" in DesignTokens.COLORS["semantic"]

    def test_get_color_valid(self):
        """Test get_color helper with valid keys"""
        assert DesignTokens.get_color("minimal", "accent") == "#0A66C2"
        assert DesignTokens.get_color("semantic", "success") == "#10B981"

    def test_get_color_invalid_scheme(self):
        """Test get_color with invalid scheme returns default"""
        assert DesignTokens.get_color("nonexistent", "accent") == "#000000"

    def test_get_color_invalid_key(self):
        """Test get_color with invalid key returns default"""
        assert DesignTokens.get_color("minimal", "nonexistent") == "#000000"

    def test_linkedin_brand_blue(self):
        """Test LinkedIn brand blue color is correct"""
        assert DesignTokens.COLORS["minimal"]["accent"] == "#0A66C2"


class TestSpacingTokens:
    """Test spacing tokens"""

    def test_gaps_exist(self):
        """Test gap spacing tokens"""
        expected_gaps = ["tiny", "small", "medium", "large", "huge"]
        for gap in expected_gaps:
            assert gap in DesignTokens.SPACING["gaps"]
            assert isinstance(DesignTokens.SPACING["gaps"][gap], int)

    def test_padding_exists(self):
        """Test padding tokens"""
        expected_padding = ["tight", "normal", "loose", "spacious"]
        for padding in expected_padding:
            assert padding in DesignTokens.SPACING["padding"]
            assert isinstance(DesignTokens.SPACING["padding"][padding], int)

    def test_safe_area_exists(self):
        """Test safe area tokens"""
        assert "standard" in DesignTokens.SPACING["safe_area"]
        assert isinstance(DesignTokens.SPACING["safe_area"]["standard"], dict)

    def test_get_spacing_gaps(self):
        """Test get_spacing helper for gaps"""
        assert DesignTokens.get_spacing("gaps", "large") == 40
        assert DesignTokens.get_spacing("gaps", "medium") == 24

    def test_get_spacing_padding(self):
        """Test get_spacing helper for padding"""
        assert DesignTokens.get_spacing("padding", "normal") == 40

    def test_get_spacing_safe_area(self):
        """Test get_spacing helper for safe area"""
        result = DesignTokens.get_spacing("safe_area", "standard")
        assert isinstance(result, dict)
        assert "top" in result

    def test_get_spacing_invalid_category(self):
        """Test get_spacing with invalid category returns default"""
        assert DesignTokens.get_spacing("nonexistent", "large") == 40

    def test_get_spacing_invalid_size(self):
        """Test get_spacing with invalid size returns default"""
        assert DesignTokens.get_spacing("gaps", "nonexistent") == 40


class TestLayoutTokens:
    """Test layout tokens"""

    def test_border_radius_exists(self):
        """Test border radius tokens"""
        expected_radii = ["none", "small", "medium", "large", "xlarge", "round"]
        for radius in expected_radii:
            assert radius in DesignTokens.LAYOUT["border_radius"]
            assert isinstance(DesignTokens.LAYOUT["border_radius"][radius], int)

    def test_shadows_exist(self):
        """Test shadow tokens"""
        expected_shadows = ["none", "sm", "md", "lg", "xl"]
        for shadow in expected_shadows:
            assert shadow in DesignTokens.VISUAL["shadow"]
            assert isinstance(DesignTokens.VISUAL["shadow"][shadow], str)

    def test_get_safe_area_helper(self):
        """Test get_safe_area convenience helper"""
        result = DesignTokens.get_safe_area("standard")
        assert isinstance(result, dict)
        assert result["top"] == 60
        assert result["bottom"] == 60

    def test_get_safe_area_invalid(self):
        """Test get_safe_area with invalid key returns standard"""
        result = DesignTokens.get_safe_area("nonexistent")
        assert isinstance(result, dict)
        assert result["top"] == 60  # standard values


class TestVisualTokens:
    """Test visual tokens"""

    def test_opacity_levels_exist(self):
        """Test opacity tokens"""
        expected_opacities = [
            "transparent",
            "faint",
            "light",
            "medium",
            "heavy",
            "strong",
            "opaque",
        ]
        for opacity in expected_opacities:
            assert opacity in DesignTokens.VISUAL["opacity"]
            assert isinstance(DesignTokens.VISUAL["opacity"][opacity], (int, float))

    def test_opacity_ranges(self):
        """Test opacity values are in valid range (0.0 to 1.0)"""
        for opacity in DesignTokens.VISUAL["opacity"].values():
            assert 0.0 <= opacity <= 1.0


class TestLinkedInSpecificTokens:
    """Test LinkedIn-specific optimization tokens"""

    def test_document_slides_recommendations(self):
        """Test document slides recommendations"""
        assert "document_slides" in DesignTokens.LINKEDIN_SPECIFIC
        doc_slides = DesignTokens.LINKEDIN_SPECIFIC["document_slides"]
        assert "min" in doc_slides
        assert "optimal_min" in doc_slides
        assert "optimal_max" in doc_slides
        assert "max" in doc_slides

    def test_carousel_slides_recommendations(self):
        """Test carousel slides recommendations"""
        assert "carousel_slides" in DesignTokens.LINKEDIN_SPECIFIC
        carousel = DesignTokens.LINKEDIN_SPECIFIC["carousel_slides"]
        assert "min" in carousel
        assert "optimal_max" in carousel
        assert "max" in carousel

    def test_mobile_requirements(self):
        """Test mobile-first design requirements"""
        assert "mobile" in DesignTokens.LINKEDIN_SPECIFIC
        mobile = DesignTokens.LINKEDIN_SPECIFIC["mobile"]
        assert mobile["min_font_size"] == 18
        assert mobile["touch_target_min"] == 44
        assert mobile["recommended_font_size"] == 24

    def test_performance_optimizations(self):
        """Test performance optimization guidelines"""
        assert "performance" in DesignTokens.LINKEDIN_SPECIFIC
        perf = DesignTokens.LINKEDIN_SPECIFIC["performance"]
        assert "max_file_size_mb" in perf
        assert "recommended_file_size_mb" in perf
        assert "image_quality" in perf


class TestTokenIntegration:
    """Test token system integration"""

    def test_all_token_categories_present(self):
        """Test all major token categories exist"""
        assert hasattr(DesignTokens, "CANVAS")
        assert hasattr(DesignTokens, "TYPOGRAPHY")
        assert hasattr(DesignTokens, "COLORS")
        assert hasattr(DesignTokens, "SPACING")
        assert hasattr(DesignTokens, "LAYOUT")
        assert hasattr(DesignTokens, "VISUAL")
        assert hasattr(DesignTokens, "LINKEDIN_SPECIFIC")

    def test_all_helpers_exist(self):
        """Test all helper methods exist"""
        assert callable(DesignTokens.get_canvas_size)
        assert callable(DesignTokens.get_font_size)
        assert callable(DesignTokens.get_color)
        assert callable(DesignTokens.get_spacing)
        assert callable(DesignTokens.get_safe_area)

    def test_token_consistency(self):
        """Test that safe area tokens are consistent across different access methods"""
        direct = DesignTokens.SPACING["safe_area"]["standard"]
        via_get_spacing = DesignTokens.get_spacing("safe_area", "standard")
        via_get_safe_area = DesignTokens.get_safe_area("standard")
        assert direct == via_get_spacing == via_get_safe_area
