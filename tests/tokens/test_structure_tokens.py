"""
Tests for StructureTokens design tokens.
"""

from chuk_mcp_linkedin.tokens.structure_tokens import StructureTokens


class TestFormatTokens:
    """Test content format tokens"""

    def test_all_formats_exist(self):
        """Test all format types are defined"""
        expected_formats = [
            "linear",
            "listicle",
            "framework",
            "story_arc",
            "comparison",
            "question_based",
        ]
        for format_type in expected_formats:
            assert format_type in StructureTokens.FORMATS

    def test_format_has_required_fields(self):
        """Test each format has required fields"""
        required_fields = ["description", "best_for", "readability", "engagement"]
        for format_type, format_data in StructureTokens.FORMATS.items():
            for field in required_fields:
                assert field in format_data, f"{format_type} missing {field}"

    def test_format_engagement_ratings(self):
        """Test format engagement ratings are valid"""
        for format_type, format_data in StructureTokens.FORMATS.items():
            engagement = format_data["engagement"]
            assert 0 <= engagement <= 1, f"{format_type} engagement {engagement} not in 0-1 range"

    def test_format_engagement_order(self):
        """Test format engagement rankings"""
        # Story arc should be highest
        assert StructureTokens.FORMATS["story_arc"]["engagement"] == 0.9
        # Listicle should be high
        assert StructureTokens.FORMATS["listicle"]["engagement"] == 0.85
        # Linear should be lower
        assert StructureTokens.FORMATS["linear"]["engagement"] == 0.6

    def test_format_readability_values(self):
        """Test readability values are valid"""
        valid_readability = ["low", "medium", "high"]
        for format_type, format_data in StructureTokens.FORMATS.items():
            assert format_data["readability"] in valid_readability

    def test_get_format_info(self):
        """Test get_format_info method"""
        info = StructureTokens.get_format_info("listicle")
        assert info["engagement"] == 0.85
        assert info["readability"] == "high"

    def test_get_format_info_invalid(self):
        """Test get_format_info with invalid type returns default"""
        info = StructureTokens.get_format_info("invalid")
        assert info == StructureTokens.FORMATS["linear"]


class TestVisualFormatting:
    """Test visual formatting tokens"""

    def test_all_symbol_types_exist(self):
        """Test all symbol types are defined"""
        expected_types = ["symbols", "checkmarks", "crosses", "arrows", "bullets", "emphasis"]
        for symbol_type in expected_types:
            assert symbol_type in StructureTokens.VISUAL_FORMATTING

    def test_symbols_not_empty(self):
        """Test each symbol type has symbols"""
        for symbol_type, symbols in StructureTokens.VISUAL_FORMATTING.items():
            assert len(symbols) > 0, f"{symbol_type} has no symbols"
            assert isinstance(symbols, list)

    def test_get_symbols(self):
        """Test get_symbols method"""
        arrows = StructureTokens.get_symbols("arrows")
        assert len(arrows) > 0
        assert "→" in arrows

    def test_get_symbols_invalid(self):
        """Test get_symbols with invalid type returns default"""
        symbols = StructureTokens.get_symbols("invalid")
        assert symbols == ["•"]


class TestSeparators:
    """Test separator tokens"""

    def test_all_separators_exist(self):
        """Test all separator styles are defined"""
        expected_separators = ["line", "dots", "wave", "heavy", "double", "minimal"]
        for separator in expected_separators:
            assert separator in StructureTokens.SEPARATORS

    def test_separators_not_empty(self):
        """Test each separator has a value"""
        for separator, value in StructureTokens.SEPARATORS.items():
            assert len(value) > 0, f"{separator} has no value"
            assert isinstance(value, str)

    def test_separators_have_newlines(self):
        """Test separators include proper spacing"""
        for separator, value in StructureTokens.SEPARATORS.items():
            # All separators should have newlines for spacing
            assert "\n" in value

    def test_get_separator(self):
        """Test get_separator method"""
        line_sep = StructureTokens.get_separator("line")
        assert "---" in line_sep

    def test_get_separator_invalid(self):
        """Test get_separator with invalid style returns default"""
        separator = StructureTokens.get_separator("invalid")
        assert separator == StructureTokens.SEPARATORS["minimal"]


class TestHookPatterns:
    """Test hook pattern templates"""

    def test_all_hook_types_exist(self):
        """Test all hook types have patterns"""
        expected_hooks = ["question", "stat", "story", "controversy", "list", "curiosity"]
        for hook_type in expected_hooks:
            assert hook_type in StructureTokens.HOOK_PATTERNS

    def test_hook_patterns_not_empty(self):
        """Test each hook type has templates"""
        for hook_type, patterns in StructureTokens.HOOK_PATTERNS.items():
            assert len(patterns) > 0, f"{hook_type} has no patterns"
            assert isinstance(patterns, list)

    def test_hook_patterns_are_templates(self):
        """Test hook patterns contain placeholders"""
        for hook_type, patterns in StructureTokens.HOOK_PATTERNS.items():
            # At least one pattern should have a placeholder
            has_placeholder = any("{" in pattern for pattern in patterns)
            assert has_placeholder, f"{hook_type} has no template placeholders"

    def test_get_hook_template(self):
        """Test get_hook_template method"""
        stat_templates = StructureTokens.get_hook_template("stat")
        assert len(stat_templates) > 0
        assert isinstance(stat_templates, list)

    def test_get_hook_template_invalid(self):
        """Test get_hook_template with invalid type returns empty"""
        templates = StructureTokens.get_hook_template("invalid")
        assert templates == []


class TestBodyStructures:
    """Test body structure tokens"""

    def test_all_body_structures_exist(self):
        """Test all body structures are defined"""
        expected_structures = ["problem_solution", "before_after", "three_act", "pyramid"]
        for structure in expected_structures:
            assert structure in StructureTokens.BODY_STRUCTURES

    def test_body_structure_has_required_fields(self):
        """Test each body structure has required fields"""
        required_fields = ["sections", "flow", "best_for"]
        for structure, data in StructureTokens.BODY_STRUCTURES.items():
            for field in required_fields:
                assert field in data, f"{structure} missing {field}"

    def test_body_structure_sections_not_empty(self):
        """Test each structure has sections"""
        for structure, data in StructureTokens.BODY_STRUCTURES.items():
            assert len(data["sections"]) > 0, f"{structure} has no sections"
            assert isinstance(data["sections"], list)


class TestCTAPatterns:
    """Test CTA pattern templates"""

    def test_all_cta_types_exist(self):
        """Test all CTA types have patterns"""
        expected_ctas = ["direct", "curiosity", "action", "share", "soft"]
        for cta_type in expected_ctas:
            assert cta_type in StructureTokens.CTA_PATTERNS

    def test_cta_patterns_not_empty(self):
        """Test each CTA type has templates"""
        for cta_type, patterns in StructureTokens.CTA_PATTERNS.items():
            assert len(patterns) > 0, f"{cta_type} has no patterns"
            assert isinstance(patterns, list)

    def test_get_cta_template(self):
        """Test get_cta_template method"""
        curiosity_templates = StructureTokens.get_cta_template("curiosity")
        assert len(curiosity_templates) > 0
        assert isinstance(curiosity_templates, list)

    def test_get_cta_template_invalid(self):
        """Test get_cta_template with invalid type returns empty"""
        templates = StructureTokens.get_cta_template("invalid")
        assert templates == []


class TestLengthByStructure:
    """Test length guidelines by structure"""

    def test_length_structures_exist(self):
        """Test length ranges for structures are defined"""
        expected_structures = ["linear", "listicle", "framework", "story_arc"]
        for structure in expected_structures:
            assert structure in StructureTokens.LENGTH_BY_STRUCTURE

    def test_length_ranges_valid(self):
        """Test all length ranges are valid"""
        for structure, lengths in StructureTokens.LENGTH_BY_STRUCTURE.items():
            for length_type, (min_len, max_len) in lengths.items():
                assert min_len < max_len, f"{structure}.{length_type} min >= max"
                assert min_len > 0, f"{structure}.{length_type} min <= 0"
                assert max_len <= 3000, f"{structure}.{length_type} exceeds max"

    def test_listicle_lengths_reasonable(self):
        """Test listicle lengths are appropriate for item counts"""
        listicle = StructureTokens.LENGTH_BY_STRUCTURE["listicle"]
        # Micro should be shorter
        assert listicle["micro"] == (100, 200)
        # Long should be longer
        assert listicle["long"] == (800, 1500)

    def test_get_recommended_length(self):
        """Test get_recommended_length method"""
        min_len, max_len = StructureTokens.get_recommended_length("listicle", "medium")
        assert min_len == 400
        assert max_len == 800

    def test_get_recommended_length_invalid_structure(self):
        """Test get_recommended_length with invalid structure uses default"""
        min_len, max_len = StructureTokens.get_recommended_length("invalid", "short")
        # Should use linear defaults
        assert min_len == 150
        assert max_len == 400

    def test_get_recommended_length_invalid_type(self):
        """Test get_recommended_length with invalid length type uses default"""
        min_len, max_len = StructureTokens.get_recommended_length("linear", "invalid")
        # Should return default
        assert isinstance(min_len, int)
        assert isinstance(max_len, int)
        assert min_len < max_len


class TestIntegration:
    """Integration tests for structure tokens"""

    def test_all_formats_have_examples_or_structure(self):
        """Test each format has either example or structure"""
        for format_type, data in StructureTokens.FORMATS.items():
            has_example = "example" in data
            has_structure = "structure" in data
            assert has_example or has_structure, f"{format_type} has neither example nor structure"

    def test_engagement_ratings_reasonable(self):
        """Test all engagement ratings are reasonable"""
        engagements = [f["engagement"] for f in StructureTokens.FORMATS.values()]

        # All should be between 0 and 1
        for engagement in engagements:
            assert 0 <= engagement <= 1

        # Should have variation
        assert len(set(engagements)) > 1

    def test_story_arc_is_highest_engagement(self):
        """Test story_arc has highest engagement"""
        max_engagement = max(f["engagement"] for f in StructureTokens.FORMATS.values())
        assert StructureTokens.FORMATS["story_arc"]["engagement"] == max_engagement


class TestEdgeCases:
    """Test edge cases and validation"""

    def test_invalid_format_type_graceful(self):
        """Test invalid format type returns default"""
        info = StructureTokens.get_format_info("nonexistent")
        assert info == StructureTokens.FORMATS["linear"]

    def test_invalid_symbol_type_graceful(self):
        """Test invalid symbol type returns default"""
        symbols = StructureTokens.get_symbols("nonexistent")
        assert symbols == ["•"]

    def test_invalid_separator_graceful(self):
        """Test invalid separator returns default"""
        separator = StructureTokens.get_separator("nonexistent")
        assert separator == StructureTokens.SEPARATORS["minimal"]

    def test_empty_hook_type_graceful(self):
        """Test empty hook type returns empty list"""
        templates = StructureTokens.get_hook_template("")
        assert templates == []

    def test_empty_cta_type_graceful(self):
        """Test empty CTA type returns empty list"""
        templates = StructureTokens.get_cta_template("")
        assert templates == []
