"""Tests for MetricsChart component."""

from chuk_mcp_linkedin.posts.components.data_viz.metrics_chart import MetricsChart


class TestMetricsChartInitialization:
    """Test MetricsChart component initialization."""

    def test_init_with_minimal_params(self):
        """Test initialization with minimal parameters."""
        data = {"Conversion Rate": "12.5%"}
        chart = MetricsChart(data)
        assert chart.data == data
        assert chart.title is None

    def test_init_with_title(self):
        """Test initialization with title."""
        data = {"Users": "1000"}
        chart = MetricsChart(data, title="KPIs")
        assert chart.title == "KPIs"


class TestMetricsChartRender:
    """Test MetricsChart component rendering."""

    def test_render_without_title(self):
        """Test rendering without title."""
        chart = MetricsChart({"Metric A": "100"})
        result = chart.render()
        assert "Metric A" in result
        assert "100" in result

    def test_render_with_title(self):
        """Test rendering with title."""
        chart = MetricsChart({"Metric": "50"}, title="Stats")
        result = chart.render()
        assert "STATS:" in result

    def test_render_percentage_gets_positive_indicator(self):
        """Test rendering percentage values."""
        chart = MetricsChart({"Growth": "25%"})
        result = chart.render()
        assert "25%" in result
        assert "Growth" in result

    def test_render_increase_gets_positive_indicator(self):
        """Test rendering with 'increase' in label."""
        chart = MetricsChart({"Revenue Increase": "$10K"})
        result = chart.render()
        assert "Revenue Increase" in result

    def test_render_growth_gets_positive_indicator(self):
        """Test rendering with 'growth' in label."""
        chart = MetricsChart({"User Growth": "15%"})
        result = chart.render()
        assert "User Growth" in result

    def test_render_decrease_gets_negative_indicator(self):
        """Test rendering with 'decrease' in label."""
        chart = MetricsChart({"Cost Decrease": "$500"})
        result = chart.render()
        assert "Cost Decrease" in result

    def test_render_down_gets_negative_indicator(self):
        """Test rendering with 'down' in label."""
        chart = MetricsChart({"Sales Down": "5%"})
        result = chart.render()
        assert "Sales Down" in result

    def test_render_neutral_metric(self):
        """Test rendering neutral metric."""
        chart = MetricsChart({"Total Users": "1000"})
        result = chart.render()
        assert "Total Users" in result

    def test_render_non_string_value(self):
        """Test rendering with non-string value."""
        chart = MetricsChart({"Count": 42})
        result = chart.render()
        assert "Count" in result
        assert "42" in result


class TestMetricsChartValidation:
    """Test MetricsChart component validation."""

    def test_validate_valid_data(self):
        """Test validation with valid data."""
        chart = MetricsChart({"A": "100", "B": "200"})
        assert chart.validate() is True

    def test_validate_single_metric(self):
        """Test validation with single metric."""
        chart = MetricsChart({"Metric": "50"})
        assert chart.validate() is True

    def test_validate_empty_data(self):
        """Test validation with empty data."""
        chart = MetricsChart({})
        assert chart.validate() is False
