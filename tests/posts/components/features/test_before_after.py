"""Tests for BeforeAfter component."""

from chuk_mcp_linkedin.posts.components.features.before_after import BeforeAfter


class TestBeforeAfterInitialization:
    def test_init(self):
        component = BeforeAfter(["Old way"], ["New way"])
        assert component.before == ["Old way"]
        assert component.after == ["New way"]


class TestBeforeAfterRender:
    def test_render(self):
        component = BeforeAfter(["Point 1"], ["Point 2"])
        result = component.render()
        assert "Point 1" in result
        assert "Point 2" in result


class TestBeforeAfterValidation:
    def test_validate_valid(self):
        component = BeforeAfter(["A"], ["B"])
        assert component.validate() is True

    def test_validate_empty(self):
        component = BeforeAfter([], [])
        assert component.validate() is False
