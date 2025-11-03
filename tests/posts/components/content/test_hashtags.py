"""Tests for Hashtags component."""

from unittest.mock import MagicMock

from chuk_mcp_linkedin.posts.components.content.hashtags import Hashtags


class TestHashtagsInitialization:
    """Test Hashtags component initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        hashtags = Hashtags(["AI", "Tech", "Innovation"])
        assert hashtags.tags == ["AI", "Tech", "Innovation"]
        assert hashtags.placement == "end"
        assert hashtags.strategy == "mixed"
        assert hashtags.theme is None

    def test_init_with_custom_placement(self):
        """Test initialization with custom placement."""
        hashtags = Hashtags(["AI", "Tech"], placement="inline")
        assert hashtags.placement == "inline"

    def test_init_with_custom_strategy(self):
        """Test initialization with custom strategy."""
        hashtags = Hashtags(["AI", "Tech"], strategy="niche")
        assert hashtags.strategy == "niche"

    def test_init_with_theme(self):
        """Test initialization with theme."""
        theme = MagicMock()
        hashtags = Hashtags(["AI"], theme=theme)
        assert hashtags.theme == theme


class TestHashtagsRender:
    """Test Hashtags component rendering."""

    def test_render_inline_placement(self):
        """Test rendering with inline placement."""
        hashtags = Hashtags(["AI", "Tech", "Innovation"], placement="inline")
        result = hashtags.render()
        assert result == "#AI #Tech #Innovation"
        assert not result.startswith("\n")

    def test_render_end_placement(self):
        """Test rendering with end placement."""
        hashtags = Hashtags(["AI", "Tech", "Innovation"], placement="end")
        result = hashtags.render()
        assert result == "\n\n#AI #Tech #Innovation"

    def test_render_mid_placement(self):
        """Test rendering with mid placement."""
        hashtags = Hashtags(["AI", "Tech"], placement="mid")
        result = hashtags.render()
        assert result == "\n\n#AI #Tech"

    def test_render_first_comment_placement(self):
        """Test rendering with first_comment placement."""
        hashtags = Hashtags(["AI", "Tech"], placement="first_comment")
        result = hashtags.render()
        assert result == "\n\n#AI #Tech"

    def test_render_limits_to_5_tags_default(self):
        """Test rendering limits to 5 tags by default."""
        hashtags = Hashtags(["Tag1", "Tag2", "Tag3", "Tag4", "Tag5", "Tag6", "Tag7"])
        result = hashtags.render()
        assert result == "\n\n#Tag1 #Tag2 #Tag3 #Tag4 #Tag5"

    def test_render_with_minimal_theme(self):
        """Test rendering with minimal theme limits to 3 tags."""
        theme = MagicMock()
        theme.hashtag_strategy = "minimal"
        hashtags = Hashtags(["Tag1", "Tag2", "Tag3", "Tag4", "Tag5"], theme=theme)
        result = hashtags.render()
        assert result == "\n\n#Tag1 #Tag2 #Tag3"

    def test_render_with_optimal_theme(self):
        """Test rendering with optimal theme limits to 5 tags."""
        theme = MagicMock()
        theme.hashtag_strategy = "optimal"
        hashtags = Hashtags(["Tag1", "Tag2", "Tag3", "Tag4", "Tag5", "Tag6"], theme=theme)
        result = hashtags.render()
        assert result == "\n\n#Tag1 #Tag2 #Tag3 #Tag4 #Tag5"

    def test_render_with_fewer_tags_than_limit(self):
        """Test rendering with fewer tags than limit."""
        hashtags = Hashtags(["Tag1", "Tag2"])
        result = hashtags.render()
        assert result == "\n\n#Tag1 #Tag2"

    def test_render_with_theme_override(self):
        """Test render with theme parameter overriding instance theme."""
        instance_theme = MagicMock()
        instance_theme.hashtag_strategy = "optimal"

        override_theme = MagicMock()
        override_theme.hashtag_strategy = "minimal"

        hashtags = Hashtags(["Tag1", "Tag2", "Tag3", "Tag4"], theme=instance_theme)
        result = hashtags.render(theme=override_theme)
        assert result == "\n\n#Tag1 #Tag2 #Tag3"


class TestHashtagsValidation:
    """Test Hashtags component validation."""

    def test_validate_valid_tags(self):
        """Test validation with valid tags."""
        hashtags = Hashtags(["AI", "Tech"])
        assert hashtags.validate() is True

    def test_validate_empty_tags_list(self):
        """Test validation with empty tags list."""
        hashtags = Hashtags([])
        assert hashtags.validate() is False

    def test_validate_tags_with_empty_string(self):
        """Test validation with tags containing empty string."""
        hashtags = Hashtags(["AI", "", "Tech"])
        assert hashtags.validate() is False

    def test_validate_single_tag(self):
        """Test validation with single tag."""
        hashtags = Hashtags(["AI"])
        assert hashtags.validate() is True

    def test_validate_many_tags(self):
        """Test validation with many tags."""
        hashtags = Hashtags(["Tag" + str(i) for i in range(20)])
        assert hashtags.validate() is True


class TestHashtagsEdgeCases:
    """Test Hashtags component edge cases."""

    def test_single_tag_inline(self):
        """Test rendering single tag inline."""
        hashtags = Hashtags(["AI"], placement="inline")
        result = hashtags.render()
        assert result == "#AI"

    def test_tags_with_spaces_in_names(self):
        """Test tags preserve spaces in names."""
        hashtags = Hashtags(["Artificial Intelligence", "Machine Learning"])
        result = hashtags.render()
        assert "#Artificial Intelligence" in result
        assert "#Machine Learning" in result

    def test_theme_without_hashtag_strategy(self):
        """Test theme without hashtag_strategy attribute."""
        theme = MagicMock()
        theme.hashtag_strategy = None
        hashtags = Hashtags(["Tag1", "Tag2", "Tag3", "Tag4", "Tag5", "Tag6"], theme=theme)
        result = hashtags.render()
        # Should default to 5 tags
        assert result == "\n\n#Tag1 #Tag2 #Tag3 #Tag4 #Tag5"
