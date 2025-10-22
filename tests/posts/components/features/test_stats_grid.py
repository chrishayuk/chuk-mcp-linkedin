"""Tests for StatsGrid component."""

from chuk_mcp_linkedin.posts.components.features.stats_grid import StatsGrid


class TestStatsGridInitialization:
    def test_init(self):
        component = StatsGrid({"Metric": "100"})
        assert component.stats == {"Metric": "100"}


class TestStatsGridRender:
    def test_render(self):
        component = StatsGrid({"Metric": "100"})
        result = component.render()
        assert "Metric" in result
        assert "100" in result

    def test_render_with_title(self):
        component = StatsGrid({"M1": "V1", "M2": "V2"}, title="Performance Metrics")
        result = component.render()
        assert "PERFORMANCE METRICS" in result
        assert "📊" in result
        assert "M1" in result
        assert "V1" in result


class TestStatsGridValidation:
    def test_validate_valid(self):
        component = StatsGrid({"M1": "V1", "M2": "V2"})
        assert component.validate() is True

    def test_validate_empty(self):
        component = StatsGrid({})
        assert component.validate() is False
