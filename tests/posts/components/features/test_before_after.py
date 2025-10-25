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

    def test_render_with_title(self):
        component = BeforeAfter(["Old way"], ["New way"], title="Transformation")
        result = component.render()
        assert "TRANSFORMATION" in result
        assert "Old way" in result
        assert "New way" in result

    def test_render_with_custom_labels(self):
        component = BeforeAfter(
            ["Before item"], ["After item"], labels={"before": "OLD", "after": "NEW"}
        )
        result = component.render()
        assert "OLD" in result
        assert "NEW" in result
        assert "Before item" in result
        assert "After item" in result


class TestBeforeAfterValidation:
    def test_validate_valid(self):
        component = BeforeAfter(["A"], ["B"])
        assert component.validate() is True

    def test_validate_empty(self):
        component = BeforeAfter([], [])
        assert component.validate() is False
