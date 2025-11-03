"""
Tests for ThemeManager and LinkedInTheme.
"""

import pytest

from chuk_mcp_linkedin.themes.theme_manager import THEMES, LinkedInTheme, ThemeManager


class TestLinkedInTheme:
    """Test LinkedInTheme dataclass"""

    def test_theme_dataclass_creation(self):
        """Test creating a LinkedInTheme"""
        theme = LinkedInTheme(
            name="Test Theme",
            description="Test description",
            tone="professional",
            formality="conversational",
            emotion="analytical",
            primary_goal="authority",
            content_mix={"educational": 0.6, "personal": 0.4},
            emoji_level="minimal",
            line_break_style="scannable",
            paragraph_length="standard",
            preferred_structures=["listicle"],
            hook_style="stat",
            cta_style="curiosity",
            hashtag_strategy="optimal",
            hashtag_placement="end",
            comment_style="thoughtful",
            controversy_level="safe",
            vulnerability_level="selective",
            humor_level="subtle",
            preferred_formats=["text"],
            media_frequency=0.5,
            post_frequency=4,
            best_posting_times=["morning"],
        )
        assert theme.name == "Test Theme"
        assert theme.tone == "professional"
        assert theme.primary_goal == "authority"

    def test_theme_has_all_required_fields(self):
        """Test theme has all required fields"""
        theme = THEMES["thought_leader"]
        required_fields = [
            "name",
            "description",
            "tone",
            "formality",
            "emotion",
            "primary_goal",
            "content_mix",
            "emoji_level",
            "line_break_style",
            "paragraph_length",
            "preferred_structures",
            "hook_style",
            "cta_style",
            "hashtag_strategy",
            "hashtag_placement",
            "comment_style",
            "controversy_level",
            "vulnerability_level",
            "humor_level",
            "preferred_formats",
            "media_frequency",
            "post_frequency",
            "best_posting_times",
        ]
        for field in required_fields:
            assert hasattr(theme, field), f"Theme missing {field}"


class TestPreBuiltThemes:
    """Test pre-built themes"""

    def test_all_themes_exist(self):
        """Test all 10 pre-built themes are defined"""
        expected_themes = [
            "thought_leader",
            "personal_brand",
            "technical_expert",
            "community_builder",
            "corporate_professional",
            "contrarian_voice",
            "storyteller",
            "data_driven",
            "coach_mentor",
            "entertainer",
        ]
        for theme_name in expected_themes:
            assert theme_name in THEMES

    def test_theme_count(self):
        """Test there are exactly 10 pre-built themes"""
        assert len(THEMES) == 10

    def test_all_themes_have_unique_names(self):
        """Test all themes have unique names"""
        names = [theme.name for theme in THEMES.values()]
        assert len(names) == len(set(names))

    def test_all_themes_have_descriptions(self):
        """Test all themes have non-empty descriptions"""
        for theme_name, theme in THEMES.items():
            assert len(theme.description) > 0, f"{theme_name} has no description"

    def test_all_themes_have_valid_content_mix(self):
        """Test all themes have valid content mix"""
        for theme_name, theme in THEMES.items():
            assert isinstance(theme.content_mix, dict)
            assert len(theme.content_mix) > 0
            # Content mix should sum to approximately 1.0
            total = sum(theme.content_mix.values())
            assert 0.9 <= total <= 1.1, f"{theme_name} content_mix sum is {total}"

    def test_all_themes_have_valid_media_frequency(self):
        """Test all themes have valid media frequency"""
        for theme_name, theme in THEMES.items():
            assert 0 <= theme.media_frequency <= 1, f"{theme_name} media_frequency out of range"

    def test_all_themes_have_valid_post_frequency(self):
        """Test all themes have valid post frequency"""
        for theme_name, theme in THEMES.items():
            assert 1 <= theme.post_frequency <= 7, f"{theme_name} post_frequency unrealistic"

    def test_all_themes_have_preferred_structures(self):
        """Test all themes have preferred structures"""
        for theme_name, theme in THEMES.items():
            assert len(theme.preferred_structures) > 0, f"{theme_name} has no preferred structures"

    def test_all_themes_have_preferred_formats(self):
        """Test all themes have preferred formats"""
        for theme_name, theme in THEMES.items():
            assert len(theme.preferred_formats) > 0, f"{theme_name} has no preferred formats"

    def test_all_themes_have_best_posting_times(self):
        """Test all themes have best posting times"""
        for theme_name, theme in THEMES.items():
            assert len(theme.best_posting_times) > 0, f"{theme_name} has no posting times"


class TestThemeCharacteristics:
    """Test specific theme characteristics"""

    def test_thought_leader_theme(self):
        """Test thought leader theme configuration"""
        theme = THEMES["thought_leader"]
        assert theme.tone == "professional"
        assert theme.primary_goal == "authority"
        assert theme.hook_style == "stat"
        assert theme.emoji_level == "minimal"

    def test_personal_brand_theme(self):
        """Test personal brand theme configuration"""
        theme = THEMES["personal_brand"]
        assert theme.tone == "inspirational"
        assert theme.primary_goal == "engagement"
        assert theme.hook_style == "story"
        assert theme.vulnerability_level == "open"

    def test_technical_expert_theme(self):
        """Test technical expert theme configuration"""
        theme = THEMES["technical_expert"]
        assert theme.tone == "technical"
        assert theme.emoji_level == "none"
        assert theme.humor_level == "none"
        assert theme.formality == "formal"

    def test_community_builder_theme(self):
        """Test community builder theme configuration"""
        theme = THEMES["community_builder"]
        assert theme.primary_goal == "community"
        assert theme.hook_style == "question"
        assert theme.emoji_level == "expressive"
        assert "poll" in theme.preferred_formats

    def test_contrarian_voice_theme(self):
        """Test contrarian voice theme configuration"""
        theme = THEMES["contrarian_voice"]
        assert theme.hook_style == "controversy"
        assert theme.controversy_level == "bold"
        assert theme.primary_goal == "engagement"

    def test_storyteller_theme(self):
        """Test storyteller theme configuration"""
        theme = THEMES["storyteller"]
        assert theme.hook_style == "story"
        assert theme.vulnerability_level == "raw"
        assert "story_arc" in theme.preferred_structures

    def test_data_driven_theme(self):
        """Test data-driven theme configuration"""
        theme = THEMES["data_driven"]
        assert theme.hook_style == "stat"
        assert theme.emotion == "analytical"
        assert theme.media_frequency >= 0.7  # High media use for data viz

    def test_entertainer_theme(self):
        """Test entertainer theme configuration"""
        theme = THEMES["entertainer"]
        assert theme.tone == "humorous"
        assert theme.humor_level == "frequent"
        assert theme.emoji_level == "expressive"


class TestThemeManager:
    """Test ThemeManager class"""

    def test_theme_manager_initialization(self):
        """Test ThemeManager initializes correctly"""
        manager = ThemeManager()
        assert len(manager.themes) == 10
        assert len(manager.custom_themes) == 0

    def test_get_theme_valid(self):
        """Test getting a valid theme"""
        manager = ThemeManager()
        theme = manager.get_theme("thought_leader")
        assert theme.name == "Thought Leader"
        assert isinstance(theme, LinkedInTheme)

    def test_get_theme_invalid(self):
        """Test getting an invalid theme raises error"""
        manager = ThemeManager()
        with pytest.raises(ValueError, match="Theme 'nonexistent' not found"):
            manager.get_theme("nonexistent")

    def test_list_themes(self):
        """Test listing all themes"""
        manager = ThemeManager()
        themes = manager.list_themes()
        assert len(themes) == 10
        assert "thought_leader" in themes
        assert "entertainer" in themes

    def test_get_all_themes(self):
        """Test getting all themes"""
        manager = ThemeManager()
        all_themes = manager.get_all_themes()
        assert len(all_themes) == 10
        assert isinstance(all_themes["thought_leader"], LinkedInTheme)

    def test_create_custom_theme(self):
        """Test creating a custom theme"""
        manager = ThemeManager()
        custom_theme = manager.create_custom_theme(
            name="Custom Theme",
            description="Custom description",
            tone="professional",
            formality="conversational",
            emotion="analytical",
            primary_goal="authority",
            content_mix={"educational": 1.0},
            emoji_level="minimal",
            line_break_style="scannable",
            paragraph_length="standard",
            preferred_structures=["listicle"],
            hook_style="stat",
            cta_style="curiosity",
            hashtag_strategy="optimal",
            hashtag_placement="end",
            comment_style="thoughtful",
            controversy_level="safe",
            vulnerability_level="selective",
            humor_level="subtle",
            preferred_formats=["text"],
            media_frequency=0.5,
            post_frequency=4,
            best_posting_times=["morning"],
        )
        assert custom_theme.name == "Custom Theme"
        assert "custom_theme" in manager.custom_themes

    def test_custom_theme_appears_in_list(self):
        """Test custom theme appears in theme list"""
        manager = ThemeManager()
        manager.create_custom_theme(
            name="New Theme",
            description="Test",
            tone="professional",
            formality="conversational",
            emotion="analytical",
            primary_goal="authority",
            content_mix={"educational": 1.0},
            emoji_level="minimal",
            line_break_style="scannable",
            paragraph_length="standard",
            preferred_structures=["listicle"],
            hook_style="stat",
            cta_style="curiosity",
            hashtag_strategy="optimal",
            hashtag_placement="end",
            comment_style="thoughtful",
            controversy_level="safe",
            vulnerability_level="selective",
            humor_level="subtle",
            preferred_formats=["text"],
            media_frequency=0.5,
            post_frequency=4,
            best_posting_times=["morning"],
        )
        themes = manager.list_themes()
        assert "new_theme" in themes

    def test_get_custom_theme(self):
        """Test getting a custom theme"""
        manager = ThemeManager()
        manager.create_custom_theme(
            name="Test Theme",
            description="Test",
            tone="professional",
            formality="conversational",
            emotion="analytical",
            primary_goal="authority",
            content_mix={"educational": 1.0},
            emoji_level="minimal",
            line_break_style="scannable",
            paragraph_length="standard",
            preferred_structures=["listicle"],
            hook_style="stat",
            cta_style="curiosity",
            hashtag_strategy="optimal",
            hashtag_placement="end",
            comment_style="thoughtful",
            controversy_level="safe",
            vulnerability_level="selective",
            humor_level="subtle",
            preferred_formats=["text"],
            media_frequency=0.5,
            post_frequency=4,
            best_posting_times=["morning"],
        )
        theme = manager.get_theme("test_theme")
        assert theme.name == "Test Theme"

    def test_export_theme(self):
        """Test exporting a theme"""
        manager = ThemeManager()
        theme_dict = manager.export_theme("thought_leader")
        assert isinstance(theme_dict, dict)
        assert theme_dict["name"] == "Thought Leader"
        assert "tone" in theme_dict
        assert "primary_goal" in theme_dict

    def test_import_theme(self):
        """Test importing a theme"""
        manager = ThemeManager()
        # First export a theme
        theme_dict = manager.export_theme("thought_leader")
        # Modify it
        theme_dict["name"] = "Imported Theme"
        # Import it back
        imported = manager.import_theme(theme_dict)
        assert imported.name == "Imported Theme"
        assert "imported_theme" in manager.custom_themes

    def test_get_theme_summary(self):
        """Test getting theme summary"""
        manager = ThemeManager()
        summary = manager.get_theme_summary("thought_leader")
        assert summary["name"] == "Thought Leader"
        assert "description" in summary
        assert "tone" in summary
        assert "goal" in summary
        assert "post_frequency" in summary

    def test_recommend_theme_by_goal(self):
        """Test recommending themes by goal"""
        manager = ThemeManager()

        # Test authority goal
        authority_themes = manager.recommend_theme("authority")
        assert len(authority_themes) > 0
        assert "thought_leader" in authority_themes

        # Test engagement goal
        engagement_themes = manager.recommend_theme("engagement")
        assert len(engagement_themes) > 0

        # Test community goal
        community_themes = manager.recommend_theme("community")
        assert len(community_themes) > 0

    def test_recommend_theme_invalid_goal(self):
        """Test recommending themes with invalid goal returns default"""
        manager = ThemeManager()
        recommendations = manager.recommend_theme("invalid_goal")
        assert recommendations == ["thought_leader"]


class TestThemeIntegration:
    """Integration tests for themes"""

    def test_all_themes_are_valid(self):
        """Test all pre-built themes are valid"""
        manager = ThemeManager()
        for theme_name in THEMES.keys():
            theme = manager.get_theme(theme_name)
            assert isinstance(theme, LinkedInTheme)
            assert len(theme.name) > 0
            assert len(theme.description) > 0

    def test_themes_have_diverse_goals(self):
        """Test themes cover different primary goals"""
        goals = set(theme.primary_goal for theme in THEMES.values())
        assert len(goals) > 1  # Should have variety

    def test_themes_have_diverse_tones(self):
        """Test themes cover different tones"""
        tones = set(theme.tone for theme in THEMES.values())
        assert len(tones) > 1  # Should have variety

    def test_themes_have_diverse_formality(self):
        """Test themes cover different formality levels"""
        formalities = set(theme.formality for theme in THEMES.values())
        assert len(formalities) > 1  # Should have variety

    def test_emoji_levels_range(self):
        """Test themes use different emoji levels"""
        emoji_levels = set(theme.emoji_level for theme in THEMES.values())
        assert "none" in emoji_levels  # Technical expert
        assert "expressive" in emoji_levels  # Community builder/Entertainer

    def test_controversy_levels_range(self):
        """Test themes have different controversy levels"""
        controversy_levels = set(theme.controversy_level for theme in THEMES.values())
        assert "safe" in controversy_levels
        assert "bold" in controversy_levels  # Contrarian

    def test_humor_levels_range(self):
        """Test themes have different humor levels"""
        humor_levels = set(theme.humor_level for theme in THEMES.values())
        assert "none" in humor_levels  # Technical/Corporate
        assert "frequent" in humor_levels  # Entertainer


class TestEdgeCases:
    """Test edge cases and validation"""

    def test_theme_manager_isolation(self):
        """Test theme managers are isolated"""
        manager1 = ThemeManager()
        manager2 = ThemeManager()

        manager1.create_custom_theme(
            name="Manager 1 Theme",
            description="Test",
            tone="professional",
            formality="conversational",
            emotion="analytical",
            primary_goal="authority",
            content_mix={"educational": 1.0},
            emoji_level="minimal",
            line_break_style="scannable",
            paragraph_length="standard",
            preferred_structures=["listicle"],
            hook_style="stat",
            cta_style="curiosity",
            hashtag_strategy="optimal",
            hashtag_placement="end",
            comment_style="thoughtful",
            controversy_level="safe",
            vulnerability_level="selective",
            humor_level="subtle",
            preferred_formats=["text"],
            media_frequency=0.5,
            post_frequency=4,
            best_posting_times=["morning"],
        )

        # Manager2 should not have Manager1's custom theme
        assert "manager_1_theme" not in manager2.custom_themes

    def test_export_import_round_trip(self):
        """Test exporting and importing preserves theme"""
        manager = ThemeManager()
        original = manager.get_theme("thought_leader")

        # Export and import
        exported = manager.export_theme("thought_leader")
        exported["name"] = "Round Trip Theme"
        imported = manager.import_theme(exported)

        # Check key fields preserved
        assert imported.tone == original.tone
        assert imported.primary_goal == original.primary_goal
        assert imported.emoji_level == original.emoji_level

    def test_custom_theme_name_normalization(self):
        """Test custom theme names are normalized"""
        manager = ThemeManager()
        manager.create_custom_theme(
            name="My Custom Theme",
            description="Test",
            tone="professional",
            formality="conversational",
            emotion="analytical",
            primary_goal="authority",
            content_mix={"educational": 1.0},
            emoji_level="minimal",
            line_break_style="scannable",
            paragraph_length="standard",
            preferred_structures=["listicle"],
            hook_style="stat",
            cta_style="curiosity",
            hashtag_strategy="optimal",
            hashtag_placement="end",
            comment_style="thoughtful",
            controversy_level="safe",
            vulnerability_level="selective",
            humor_level="subtle",
            preferred_formats=["text"],
            media_frequency=0.5,
            post_frequency=4,
            best_posting_times=["morning"],
        )

        # Should be accessible with normalized name
        assert "my_custom_theme" in manager.custom_themes
        theme = manager.get_theme("my_custom_theme")
        assert theme.name == "My Custom Theme"
