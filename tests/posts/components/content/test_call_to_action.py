"""Tests for CallToAction component."""

from unittest.mock import MagicMock

from chuk_mcp_linkedin.posts.components.content.call_to_action import CallToAction


class TestCallToActionInitialization:
    """Test CallToAction component initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        cta = CallToAction("direct", "Comment your thoughts below")
        assert cta.cta_type == "direct"
        assert cta.text == "Comment your thoughts below"
        assert cta.theme is None

    def test_init_with_theme(self):
        """Test initialization with theme."""
        theme = MagicMock()
        cta = CallToAction("action", "Click the link", theme=theme)
        assert cta.theme == theme


class TestCallToActionRender:
    """Test CallToAction component rendering."""

    def test_render_without_theme(self):
        """Test rendering without theme."""
        cta = CallToAction("direct", "Share your thoughts")
        result = cta.render()
        assert result == "Share your thoughts"

    def test_render_direct_with_moderate_emoji(self):
        """Test direct CTA with moderate emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "moderate"
        cta = CallToAction("direct", "Comment below", theme=theme)
        result = cta.render()
        assert result == "👇 Comment below"

    def test_render_curiosity_with_expressive_emoji(self):
        """Test curiosity CTA with expressive emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "expressive"
        cta = CallToAction("curiosity", "What do you think?", theme=theme)
        result = cta.render()
        assert result == "🤔 What do you think?"

    def test_render_action_with_heavy_emoji(self):
        """Test action CTA with heavy emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "heavy"
        cta = CallToAction("action", "Take action now", theme=theme)
        result = cta.render()
        assert result == "⚡ Take action now"

    def test_render_share_with_moderate_emoji(self):
        """Test share CTA with moderate emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "moderate"
        cta = CallToAction("share", "Share this post", theme=theme)
        result = cta.render()
        assert result == "🔄 Share this post"

    def test_render_soft_with_moderate_emoji(self):
        """Test soft CTA with moderate emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "moderate"
        cta = CallToAction("soft", "Let me know", theme=theme)
        result = cta.render()
        assert result == "💭 Let me know"

    def test_render_with_minimal_emoji(self):
        """Test rendering with minimal emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "minimal"
        cta = CallToAction("direct", "Comment below", theme=theme)
        result = cta.render()
        assert result == "Comment below"

    def test_render_with_none_emoji(self):
        """Test rendering with no emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "none"
        cta = CallToAction("direct", "Comment below", theme=theme)
        result = cta.render()
        assert result == "Comment below"

    def test_render_unknown_type_with_emoji(self):
        """Test rendering unknown CTA type with emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "moderate"
        cta = CallToAction("unknown_type", "Do something", theme=theme)
        result = cta.render()
        assert result == "Do something"

    def test_render_with_theme_override(self):
        """Test render with theme parameter overriding instance theme."""
        instance_theme = MagicMock()
        instance_theme.emoji_level = "none"

        override_theme = MagicMock()
        override_theme.emoji_level = "moderate"

        cta = CallToAction("direct", "Comment below", theme=instance_theme)
        result = cta.render(theme=override_theme)
        assert result == "👇 Comment below"


class TestCallToActionValidation:
    """Test CallToAction component validation."""

    def test_validate_valid_text(self):
        """Test validation with valid text."""
        cta = CallToAction("direct", "Valid CTA")
        assert cta.validate() is True

    def test_validate_empty_text(self):
        """Test validation with empty text."""
        cta = CallToAction("direct", "")
        assert cta.validate() is False

    def test_validate_text_too_long(self):
        """Test validation with text exceeding max length."""
        cta = CallToAction("direct", "x" * 201)
        assert cta.validate() is False

    def test_validate_text_at_max_length(self):
        """Test validation with text at exactly max length."""
        cta = CallToAction("direct", "x" * 200)
        assert cta.validate() is True

    def test_validate_minimal_text(self):
        """Test validation with minimal text."""
        cta = CallToAction("direct", "x")
        assert cta.validate() is True


class TestCallToActionTypes:
    """Test different CTA types."""

    def test_direct_cta_type(self):
        """Test direct CTA type."""
        cta = CallToAction("direct", "Comment below")
        assert cta.cta_type == "direct"

    def test_curiosity_cta_type(self):
        """Test curiosity CTA type."""
        cta = CallToAction("curiosity", "Want to learn more?")
        assert cta.cta_type == "curiosity"

    def test_action_cta_type(self):
        """Test action CTA type."""
        cta = CallToAction("action", "Sign up now")
        assert cta.cta_type == "action"

    def test_share_cta_type(self):
        """Test share CTA type."""
        cta = CallToAction("share", "Share with your network")
        assert cta.cta_type == "share"

    def test_soft_cta_type(self):
        """Test soft CTA type."""
        cta = CallToAction("soft", "Thoughts?")
        assert cta.cta_type == "soft"
