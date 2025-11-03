"""Tests for Hook component."""

from unittest.mock import MagicMock

from chuk_mcp_linkedin.posts.components.content.hook import Hook


class TestHookInitialization:
    """Test Hook component initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        hook = Hook("question", "What if we could change everything?")
        assert hook.hook_type == "question"
        assert hook.content == "What if we could change everything?"
        assert hook.theme is None

    def test_init_with_theme(self):
        """Test initialization with theme."""
        theme = MagicMock()
        hook = Hook("stat", "99% of people don't know this", theme=theme)
        assert hook.theme == theme


class TestHookRender:
    """Test Hook component rendering."""

    def test_render_without_theme(self):
        """Test rendering without theme."""
        hook = Hook("question", "What's your biggest challenge?")
        result = hook.render()
        assert result == "What's your biggest challenge?"

    def test_render_controversy_with_bold_theme(self):
        """Test controversy hook with bold theme."""
        theme = MagicMock()
        theme.controversy_level = "bold"
        hook = Hook("controversy", "This is controversial", theme=theme)
        result = hook.render()
        assert result == "🚨 This is controversial"

    def test_render_controversy_with_provocative_theme(self):
        """Test controversy hook with provocative theme."""
        theme = MagicMock()
        theme.controversy_level = "provocative"
        hook = Hook("controversy", "This is controversial", theme=theme)
        result = hook.render()
        assert result == "🚨 This is controversial"

    def test_render_controversy_without_bold_theme(self):
        """Test controversy hook without bold/provocative theme."""
        theme = MagicMock()
        theme.controversy_level = "mild"
        hook = Hook("controversy", "This is controversial", theme=theme)
        result = hook.render()
        assert result == "This is controversial"

    def test_render_non_controversy_with_bold_theme(self):
        """Test non-controversy hook with bold theme."""
        theme = MagicMock()
        theme.controversy_level = "bold"
        hook = Hook("question", "What do you think?", theme=theme)
        result = hook.render()
        assert result == "What do you think?"

    def test_render_with_theme_override(self):
        """Test render with theme parameter overriding instance theme."""
        instance_theme = MagicMock()
        instance_theme.controversy_level = "mild"

        override_theme = MagicMock()
        override_theme.controversy_level = "bold"

        hook = Hook("controversy", "Bold statement", theme=instance_theme)
        result = hook.render(theme=override_theme)
        assert result == "🚨 Bold statement"


class TestHookValidation:
    """Test Hook component validation."""

    def test_validate_valid_content(self):
        """Test validation with valid content."""
        hook = Hook("question", "Valid hook")
        assert hook.validate() is True

    def test_validate_empty_content(self):
        """Test validation with empty content."""
        hook = Hook("question", "")
        assert hook.validate() is False

    def test_validate_content_too_long(self):
        """Test validation with content exceeding max length."""
        hook = Hook("question", "x" * 201)
        assert hook.validate() is False

    def test_validate_content_at_max_length(self):
        """Test validation with content at exactly max length."""
        hook = Hook("question", "x" * 200)
        assert hook.validate() is True

    def test_validate_minimal_content(self):
        """Test validation with minimal content."""
        hook = Hook("question", "x")
        assert hook.validate() is True


class TestHookTypes:
    """Test different hook types."""

    def test_question_hook_type(self):
        """Test question hook type."""
        hook = Hook("question", "Why does this matter?")
        assert hook.hook_type == "question"

    def test_stat_hook_type(self):
        """Test stat hook type."""
        hook = Hook("stat", "90% of startups fail")
        assert hook.hook_type == "stat"

    def test_story_hook_type(self):
        """Test story hook type."""
        hook = Hook("story", "I remember the day everything changed")
        assert hook.hook_type == "story"

    def test_list_hook_type(self):
        """Test list hook type."""
        hook = Hook("list", "3 things I learned")
        assert hook.hook_type == "list"

    def test_curiosity_hook_type(self):
        """Test curiosity hook type."""
        hook = Hook("curiosity", "You won't believe what happened next")
        assert hook.hook_type == "curiosity"
