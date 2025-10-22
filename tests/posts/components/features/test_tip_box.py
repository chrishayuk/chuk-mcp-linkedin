"""Tests for TipBox component."""

from chuk_mcp_linkedin.posts.components.features.tip_box import TipBox


class TestTipBoxInitialization:
    def test_init(self):
        component = TipBox("This is a tip")
        assert component.message == "This is a tip"


class TestTipBoxRender:
    def test_render(self):
        component = TipBox("Helpful tip")
        result = component.render()
        assert "Helpful tip" in result


class TestTipBoxValidation:
    def test_validate_valid(self):
        component = TipBox("Valid tip")
        assert component.validate() is True

    def test_validate_empty(self):
        component = TipBox("")
        assert component.validate() is False

    def test_validate_invalid_style(self):
        component = TipBox("Tip", style="invalid")
        assert component.validate() is False
