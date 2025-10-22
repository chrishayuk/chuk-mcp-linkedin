"""Tests for KeyTakeaway component."""

from chuk_mcp_linkedin.posts.components.features.key_takeaway import KeyTakeaway


class TestKeyTakeawayInitialization:
    def test_init(self):
        component = KeyTakeaway("Important insight here")
        assert component.message == "Important insight here"


class TestKeyTakeawayRender:
    def test_render(self):
        component = KeyTakeaway("Point 1")
        result = component.render()
        assert "Point 1" in result

    def test_render_highlight_style(self):
        component = KeyTakeaway("Important insight", style="highlight")
        result = component.render()
        assert "Important insight" in result
        assert "💡" in result

    def test_render_simple_style(self):
        component = KeyTakeaway("Simple message", style="simple")
        result = component.render()
        assert "Simple message" in result
        # Simple style should not have emojis in this path
        assert result == "Simple message"


class TestKeyTakeawayValidation:
    def test_validate_valid(self):
        component = KeyTakeaway("Point")
        assert component.validate() is True

    def test_validate_empty(self):
        component = KeyTakeaway("")
        assert component.validate() is False
