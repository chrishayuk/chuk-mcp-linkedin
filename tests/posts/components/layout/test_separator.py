"""Tests for Separator component."""

from chuk_mcp_linkedin.posts.components.layout.separator import Separator


class TestSeparatorInitialization:
    def test_init_with_defaults(self):
        sep = Separator()
        assert sep.style == "line"

    def test_init_with_custom_style(self):
        sep = Separator(style="dots")
        assert sep.style == "dots"


class TestSeparatorRender:
    def test_render_line_style(self):
        sep = Separator(style="line")
        result = sep.render()
        assert "---" in result

    def test_render_dots_style(self):
        sep = Separator(style="dots")
        result = sep.render()
        assert "• • •" in result

    def test_render_minimal_style(self):
        sep = Separator(style="minimal")
        result = sep.render()
        assert result == "\n\n"

    def test_render_unknown_style(self):
        sep = Separator(style="unknown")
        result = sep.render()
        # Unknown style returns minimal
        assert result == "\n\n"


class TestSeparatorValidation:
    def test_validate_always_true(self):
        sep = Separator()
        assert sep.validate() is True
