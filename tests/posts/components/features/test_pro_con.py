"""Tests for ProCon component."""

from chuk_mcp_linkedin.posts.components.features.pro_con import ProCon


class TestProConInitialization:
    def test_init(self):
        component = ProCon(["Pro 1"], ["Con 1"])
        assert component.pros == ["Pro 1"]
        assert component.cons == ["Con 1"]


class TestProConRender:
    def test_render(self):
        component = ProCon(["Pro 1"], ["Con 1"])
        result = component.render()
        assert "Pro 1" in result
        assert "Con 1" in result

    def test_render_with_title(self):
        component = ProCon(["Pro 1"], ["Con 1"], title="Decision Analysis")
        result = component.render()
        assert "DECISION ANALYSIS" in result
        assert "Pro 1" in result
        assert "Con 1" in result


class TestProConValidation:
    def test_validate_valid(self):
        component = ProCon(["Pro"], ["Con"])
        assert component.validate() is True

    def test_validate_empty(self):
        component = ProCon([], [])
        assert component.validate() is False
