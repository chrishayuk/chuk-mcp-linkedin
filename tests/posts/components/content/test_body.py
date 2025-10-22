"""Tests for Body component."""

from chuk_mcp_linkedin.posts.components.content.body import Body
from unittest.mock import MagicMock


class TestBodyInitialization:
    """Test Body component initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        body = Body("Test content")
        assert body.content == "Test content"
        assert body.structure == "linear"
        assert body.theme is None

    def test_init_with_structure(self):
        """Test initialization with specific structure."""
        body = Body("Test content", structure="listicle")
        assert body.structure == "listicle"

    def test_init_with_theme(self):
        """Test initialization with theme."""
        theme = MagicMock()
        body = Body("Test content", theme=theme)
        assert body.theme == theme


class TestBodyRenderLinear:
    """Test Body component linear rendering."""

    def test_render_linear_without_theme(self):
        """Test linear rendering without theme."""
        body = Body("Test content", structure="linear")
        result = body.render()
        assert result == "Test content"

    def test_render_linear_with_theme(self):
        """Test linear rendering with theme and paragraphs."""
        theme = MagicMock()
        theme.line_break_style = "relaxed"
        body = Body("Para 1\n\nPara 2", structure="linear", theme=theme)
        result = body.render()
        # Should join paragraphs with line breaks
        assert "Para 1" in result
        assert "Para 2" in result

    def test_render_default_structure(self):
        """Test rendering with default structure calls linear."""
        body = Body("Test content")
        result = body.render()
        assert result == "Test content"


class TestBodyRenderListicle:
    """Test Body component listicle rendering."""

    def test_render_listicle_without_theme(self):
        """Test listicle rendering without theme."""
        body = Body("Item 1\nItem 2\nItem 3", structure="listicle")
        result = body.render()
        assert "→ Item 1" in result
        assert "→ Item 2" in result
        assert "→ Item 3" in result

    def test_render_listicle_with_emoji_none_theme(self):
        """Test listicle rendering with no emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "none"
        body = Body("Item 1\nItem 2", structure="listicle", theme=theme)
        result = body.render()
        assert "- Item 1" in result
        assert "- Item 2" in result

    def test_render_listicle_preserves_existing_symbols(self):
        """Test listicle doesn't double-add symbols."""
        body = Body("→ Item 1\n• Item 2\n✓ Item 3", structure="listicle")
        result = body.render()
        assert result.count("→") == 1  # Doesn't add extra arrow
        assert "• Item 2" in result
        assert "✓ Item 3" in result

    def test_render_listicle_skips_empty_lines(self):
        """Test listicle skips empty lines."""
        body = Body("Item 1\n\n\nItem 2", structure="listicle")
        result = body.render()
        lines = [line for line in result.split("\n") if line.strip()]
        assert len(lines) == 2


class TestBodyRenderFramework:
    """Test Body component framework rendering."""

    def test_render_framework_without_theme(self):
        """Test framework rendering without theme."""
        body = Body("Part 1||Part 2||Part 3", structure="framework")
        result = body.render()
        assert "📌 Part 1" in result
        assert "📌 Part 2" in result
        assert "📌 Part 3" in result

    def test_render_framework_with_minimal_emoji(self):
        """Test framework with minimal emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "minimal"
        body = Body("Part 1||Part 2", structure="framework", theme=theme)
        result = body.render()
        assert "• Part 1" in result
        assert "• Part 2" in result

    def test_render_framework_with_none_emoji(self):
        """Test framework with no emoji theme."""
        theme = MagicMock()
        theme.emoji_level = "none"
        body = Body("Part 1||Part 2", structure="framework", theme=theme)
        result = body.render()
        assert "• Part 1" in result
        assert "• Part 2" in result


class TestBodyRenderStoryArc:
    """Test Body component story arc rendering."""

    def test_render_story_arc_without_theme(self):
        """Test story arc rendering without theme."""
        body = Body("Para 1\n\nPara 2\n\nPara 3", structure="story_arc")
        result = body.render()
        assert "Para 1" in result
        assert "Para 2" in result
        assert "Para 3" in result

    def test_render_story_arc_with_extreme_breaks(self):
        """Test story arc with extreme line breaks."""
        theme = MagicMock()
        theme.line_break_style = "extreme"
        body = Body("Para 1\n\nPara 2", structure="story_arc", theme=theme)
        result = body.render()
        assert "Para 1" in result
        assert "Para 2" in result
        assert "\n\n\n" in result


class TestBodyRenderComparison:
    """Test Body component comparison rendering."""

    def test_render_comparison_with_two_parts(self):
        """Test comparison rendering with two parts."""
        body = Body("Old way||New way", structure="comparison")
        result = body.render()
        assert "❌ Old way" in result
        assert "✅ New way" in result

    def test_render_comparison_with_invalid_parts(self):
        """Test comparison with wrong number of parts."""
        body = Body("Only one part", structure="comparison")
        result = body.render()
        assert result == "Only one part"


class TestBodyValidation:
    """Test Body component validation."""

    def test_validate_valid_content(self):
        """Test validation with valid content."""
        body = Body("Valid content")
        assert body.validate() is True

    def test_validate_empty_content(self):
        """Test validation with empty content."""
        body = Body("")
        assert body.validate() is False

    def test_validate_content_too_long(self):
        """Test validation with content exceeding max length."""
        body = Body("x" * 2801)
        assert body.validate() is False

    def test_validate_content_at_max_length(self):
        """Test validation with content at exactly max length."""
        body = Body("x" * 2800)
        assert body.validate() is True


class TestBodyThemeOverride:
    """Test Body component theme override in render."""

    def test_render_with_theme_override(self):
        """Test render with theme parameter overriding instance theme."""
        instance_theme = MagicMock()
        instance_theme.line_break_style = "standard"

        override_theme = MagicMock()
        override_theme.line_break_style = "relaxed"

        body = Body("Para 1\n\nPara 2", structure="linear", theme=instance_theme)
        result = body.render(theme=override_theme)
        # Should use override theme
        assert "Para 1" in result
