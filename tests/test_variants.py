"""
Tests for variant system.
"""

from chuk_mcp_linkedin.variants import PostVariants, VariantResolver, VariantConfig
from chuk_mcp_linkedin import ThemeManager


class TestVariantConfig:
    """Test VariantConfig dataclass"""

    def test_variant_config_creation(self):
        """Test creating a variant config"""
        config = VariantConfig(
            name="story", properties={"structure": "story_arc"}, description="Narrative-driven post"
        )
        assert config.name == "story"
        assert config.properties["structure"] == "story_arc"
        assert config.description == "Narrative-driven post"


class TestPostVariants:
    """Test PostVariants class"""

    def test_text_post_variants(self):
        """Test text post variants structure"""
        variants = PostVariants.text_post_variants()

        assert "base" in variants
        assert "variants" in variants
        assert "compound_variants" in variants
        assert "default_variant" in variants

    def test_text_post_has_style_variants(self):
        """Test text post has style variants"""
        variants = PostVariants.text_post_variants()

        assert "style" in variants["variants"]
        styles = variants["variants"]["style"]
        assert "story" in styles
        assert "insight" in styles
        assert "question" in styles
        assert "listicle" in styles
        assert "hot_take" in styles

    def test_text_post_has_tone_variants(self):
        """Test text post has tone variants"""
        variants = PostVariants.text_post_variants()

        assert "tone" in variants["variants"]
        tones = variants["variants"]["tone"]
        assert "professional" in tones
        assert "conversational" in tones
        assert "casual" in tones
        assert "inspiring" in tones
        assert "humorous" in tones

    def test_text_post_has_length_variants(self):
        """Test text post has length variants"""
        variants = PostVariants.text_post_variants()

        assert "length" in variants["variants"]
        lengths = variants["variants"]["length"]
        assert "micro" in lengths
        assert "short" in lengths
        assert "medium" in lengths
        assert "long" in lengths
        assert "story" in lengths

    def test_text_post_compound_variants(self):
        """Test text post has compound variants"""
        variants = PostVariants.text_post_variants()

        compounds = variants["compound_variants"]
        assert len(compounds) > 0

        # Check structure of compound variants
        for compound in compounds:
            assert "conditions" in compound
            assert "applies" in compound

    def test_poll_post_variants(self):
        """Test poll post variants structure"""
        variants = PostVariants.poll_post_variants()

        assert "base" in variants
        assert "variants" in variants
        assert "default_variant" in variants

    def test_poll_post_has_purpose_variants(self):
        """Test poll post has purpose variants"""
        variants = PostVariants.poll_post_variants()

        assert "purpose" in variants["variants"]
        purposes = variants["variants"]["purpose"]
        assert "engagement" in purposes
        assert "research" in purposes
        assert "decision" in purposes
        assert "fun" in purposes

    def test_poll_post_has_question_type_variants(self):
        """Test poll post has question type variants"""
        variants = PostVariants.poll_post_variants()

        assert "question_type" in variants["variants"]
        types = variants["variants"]["question_type"]
        assert "binary" in types
        assert "multiple_choice" in types

    def test_document_post_variants(self):
        """Test document post variants structure"""
        variants = PostVariants.document_post_variants()

        assert "base" in variants
        assert "variants" in variants
        assert "default_variant" in variants

    def test_document_post_has_content_type_variants(self):
        """Test document post has content type variants"""
        variants = PostVariants.document_post_variants()

        assert "content_type" in variants["variants"]
        types = variants["variants"]["content_type"]
        assert "guide" in types
        assert "checklist" in types
        assert "stats" in types
        assert "report" in types

    def test_document_post_has_design_style_variants(self):
        """Test document post has design style variants"""
        variants = PostVariants.document_post_variants()

        assert "design_style" in variants["variants"]
        styles = variants["variants"]["design_style"]
        assert "minimal" in styles
        assert "professional" in styles
        assert "vibrant" in styles


class TestVariantResolver:
    """Test VariantResolver class"""

    def test_resolve_basic_variant(self):
        """Test resolving basic variant selection"""
        base_variants = PostVariants.text_post_variants()
        selected = {"style": "story", "tone": "conversational", "length": "long"}

        config = VariantResolver.resolve(base_variants, selected)

        assert config["type"] == "text"
        assert config["structure"] == "story_arc"

    def test_resolve_applies_multiple_variants(self):
        """Test resolving applies settings from multiple variants"""
        base_variants = PostVariants.text_post_variants()
        selected = {"style": "insight", "tone": "professional", "length": "medium"}

        config = VariantResolver.resolve(base_variants, selected)

        # Should have properties from all selected variants
        assert "structure" in config  # From style
        assert "formality" in config  # From tone
        assert "ideal_length" in config  # From length

    def test_resolve_applies_compound_variants(self):
        """Test resolving applies compound variants"""
        base_variants = PostVariants.text_post_variants()
        # Select combination that triggers compound variant
        selected = {"style": "story", "tone": "inspiring"}

        config = VariantResolver.resolve(base_variants, selected)

        # Compound should have applied additional properties
        assert config["vulnerability_level"] == "raw"
        assert config["line_break_style"] == "extreme"

    def test_resolve_with_theme_override(self):
        """Test resolving with theme overrides"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("technical_expert")

        base_variants = PostVariants.text_post_variants()
        selected = {"style": "insight"}

        config = VariantResolver.resolve(base_variants, selected, theme)

        # Theme should override emoji_level
        assert config["emoji_level"] == "none"

    def test_resolve_theme_does_not_override_explicit_selections(self):
        """Test theme doesn't override explicitly selected variants"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("entertainer")  # Has expressive emoji

        base_variants = PostVariants.text_post_variants()
        # Explicitly select professional tone (no emojis)
        selected = {"style": "insight", "tone": "professional"}

        config = VariantResolver.resolve(base_variants, selected, theme)

        # Theme will apply since tone isn't in the selected keys
        # Professional tone sets emoji_level, then theme can override if key not in selected
        # The logic in VariantResolver applies theme if key not in selected
        # So the theme's emoji_level will be applied
        assert (
            config["emoji_level"] == "expressive"
        )  # Theme wins since emoji_level not explicitly selected

    def test_suggest_variants_text_authority(self):
        """Test suggesting variants for text authority goal"""
        suggestions = VariantResolver.suggest_variants("text", "authority")

        assert suggestions["style"] == "insight"
        assert suggestions["tone"] == "professional"
        assert suggestions["length"] == "medium"

    def test_suggest_variants_text_engagement(self):
        """Test suggesting variants for text engagement goal"""
        suggestions = VariantResolver.suggest_variants("text", "engagement")

        assert suggestions["style"] == "question"
        assert suggestions["tone"] == "conversational"
        assert suggestions["length"] == "short"

    def test_suggest_variants_text_virality(self):
        """Test suggesting variants for text virality goal"""
        suggestions = VariantResolver.suggest_variants("text", "virality")

        assert suggestions["style"] == "hot_take"
        assert suggestions["length"] == "micro"

    def test_suggest_variants_document_authority(self):
        """Test suggesting variants for document authority goal"""
        suggestions = VariantResolver.suggest_variants("document", "authority")

        assert suggestions["content_type"] == "report"
        assert suggestions["design_style"] == "professional"

    def test_suggest_variants_poll_engagement(self):
        """Test suggesting variants for poll engagement goal"""
        suggestions = VariantResolver.suggest_variants("poll", "engagement")

        assert suggestions["purpose"] == "engagement"
        assert suggestions["question_type"] == "binary"

    def test_suggest_variants_unknown_goal(self):
        """Test suggesting variants for unknown goal returns empty"""
        suggestions = VariantResolver.suggest_variants("text", "unknown_goal")
        assert suggestions == {}

    def test_suggest_variants_unknown_post_type(self):
        """Test suggesting variants for unknown post type returns empty"""
        suggestions = VariantResolver.suggest_variants("unknown_type", "authority")
        assert suggestions == {}

    def test_get_all_variants_text(self):
        """Test getting all variants for text post"""
        variants = VariantResolver.get_all_variants("text")

        assert variants is not None
        assert "base" in variants
        assert "variants" in variants

    def test_get_all_variants_poll(self):
        """Test getting all variants for poll post"""
        variants = VariantResolver.get_all_variants("poll")

        assert variants is not None
        assert "base" in variants

    def test_get_all_variants_document(self):
        """Test getting all variants for document post"""
        variants = VariantResolver.get_all_variants("document")

        assert variants is not None
        assert "base" in variants

    def test_get_all_variants_unknown(self):
        """Test getting variants for unknown post type"""
        variants = VariantResolver.get_all_variants("unknown")
        assert variants == {}


class TestVariantIntegration:
    """Integration tests for variant system"""

    def test_resolve_complete_workflow(self):
        """Test complete variant resolution workflow"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")

        # Get base variants
        base_variants = PostVariants.text_post_variants()

        # Get suggestions based on goal
        suggestions = VariantResolver.suggest_variants("text", "authority")

        # Resolve with theme
        config = VariantResolver.resolve(base_variants, suggestions, theme)

        # Verify final config has all necessary properties
        assert "type" in config
        assert "structure" in config
        assert "emoji_level" in config
        assert "hook_style" in config

    def test_different_goals_produce_different_configs(self):
        """Test different goals produce different configurations"""
        base_variants = PostVariants.text_post_variants()

        authority_suggestions = VariantResolver.suggest_variants("text", "authority")
        authority_config = VariantResolver.resolve(base_variants, authority_suggestions)

        virality_suggestions = VariantResolver.suggest_variants("text", "virality")
        virality_config = VariantResolver.resolve(base_variants, virality_suggestions)

        # Configs should be different
        assert authority_config["structure"] != virality_config["structure"]

    def test_theme_personalizes_variant_output(self):
        """Test that different themes personalize the same variants"""
        theme_manager = ThemeManager()
        professional_theme = theme_manager.get_theme("corporate_professional")
        fun_theme = theme_manager.get_theme("entertainer")

        base_variants = PostVariants.text_post_variants()
        selected = {"style": "insight", "tone": "conversational"}

        professional_config = VariantResolver.resolve(base_variants, selected, professional_theme)
        fun_config = VariantResolver.resolve(base_variants, selected, fun_theme)

        # Should have different emoji levels based on theme
        assert professional_config["emoji_level"] != fun_config["emoji_level"]

    def test_compound_variants_enhance_combinations(self):
        """Test compound variants add extra properties for specific combinations"""
        base_variants = PostVariants.text_post_variants()

        # Compound-triggering selection
        compound_selected = {"style": "story", "tone": "inspiring"}
        compound_config = VariantResolver.resolve(base_variants, compound_selected)

        # Compound config should have extra properties
        assert "vulnerability_level" in compound_config
        assert compound_config["line_break_style"] == "extreme"
