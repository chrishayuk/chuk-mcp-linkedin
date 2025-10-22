"""Tests for BigStat component."""

from chuk_mcp_linkedin.posts.components.features.big_stat import BigStat


class TestBigStatInitialization:
    def test_init(self):
        component = BigStat("99%", "Success Rate")
        assert component.number == "99%"
        assert component.label == "Success Rate"


class TestBigStatRender:
    def test_render(self):
        component = BigStat("100", "Users")
        result = component.render()
        assert "100" in result
        assert "Users" in result


class TestBigStatValidation:
    def test_validate_valid(self):
        component = BigStat("50", "Metric")
        assert component.validate() is True

    def test_validate_empty_number(self):
        component = BigStat("", "Metric")
        assert component.validate() is False

    def test_validate_empty_label(self):
        component = BigStat("100", "")
        assert component.validate() is False
