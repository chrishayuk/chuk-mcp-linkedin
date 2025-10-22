"""Tests for NumberedList component."""

from chuk_mcp_linkedin.posts.components.features.numbered_list import NumberedList


class TestNumberedListInitialization:
    def test_init(self):
        component = NumberedList(["Item 1", "Item 2"])
        assert component.items == ["Item 1", "Item 2"]


class TestNumberedListRender:
    def test_render(self):
        component = NumberedList(["Item 1", "Item 2"])
        result = component.render()
        assert "Item 1" in result
        assert "Item 2" in result

    def test_render_with_title(self):
        component = NumberedList(["Item 1"], title="Steps")
        result = component.render()
        assert "STEPS" in result
        assert "Item 1" in result

    def test_render_emoji_numbers_style(self):
        component = NumberedList(["First", "Second"], style="emoji_numbers")
        result = component.render()
        assert "1️⃣" in result
        assert "2️⃣" in result

    def test_render_emoji_numbers_beyond_ten(self):
        # Create 11 items to test fallback when emoji numbers run out
        items = [f"Item {i}" for i in range(1, 12)]
        component = NumberedList(items, style="emoji_numbers")
        result = component.render()
        assert "11." in result  # Should fall back to regular numbers

    def test_render_bold_numbers_style(self):
        component = NumberedList(["First"], style="bold_numbers")
        result = component.render()
        assert "[1]" in result


class TestNumberedListValidation:
    def test_validate_valid(self):
        component = NumberedList(["Item"])
        assert component.validate() is True

    def test_validate_empty(self):
        component = NumberedList([])
        assert component.validate() is False
