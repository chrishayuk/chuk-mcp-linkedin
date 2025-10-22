"""Tests for BarChart component."""

from chuk_mcp_linkedin.posts.components.data_viz.bar_chart import BarChart


class TestBarChartInitialization:
    """Test BarChart component initialization."""

    def test_init_with_minimal_params(self):
        """Test initialization with minimal parameters."""
        data = {"Q1": 10, "Q2": 20}
        chart = BarChart(data)
        assert chart.data == data
        assert chart.title is None
        assert chart.unit == ""

    def test_init_with_all_params(self):
        """Test initialization with all parameters."""
        data = {"Q1": 100, "Q2": 150}
        chart = BarChart(data, title="Revenue", unit="K")
        assert chart.title == "Revenue"
        assert chart.unit == "K"


class TestBarChartRender:
    """Test BarChart component rendering."""

    def test_render_without_title(self):
        """Test rendering without title."""
        chart = BarChart({"A": 5, "B": 3})
        result = chart.render()
        assert "A: 5" in result
        assert "B: 3" in result

    def test_render_with_title(self):
        """Test rendering with title."""
        chart = BarChart({"A": 5}, title="Test Chart")
        result = chart.render()
        assert "TEST CHART:" in result

    def test_render_with_unit(self):
        """Test rendering with unit."""
        chart = BarChart({"Sales": 100}, unit="USD")
        result = chart.render()
        assert "100 USD" in result

    def test_render_creates_bars(self):
        """Test rendering creates bar visualization."""
        chart = BarChart({"Item": 3})
        result = chart.render()
        # Should have colored squares representing the bar
        assert len(result) > 0


class TestBarChartValidation:
    """Test BarChart component validation."""

    def test_validate_valid_data(self):
        """Test validation with valid data."""
        chart = BarChart({"A": 10, "B": 20})
        assert chart.validate() is True

    def test_validate_empty_data(self):
        """Test validation with empty data."""
        chart = BarChart({})
        assert chart.validate() is False

    def test_validate_float_values(self):
        """Test validation with float values."""
        chart = BarChart({"A": 10.5, "B": 20.7})
        assert chart.validate() is True

    def test_validate_non_numeric_values(self):
        """Test validation with non-numeric values."""
        chart = BarChart({"A": "not a number"})
        assert chart.validate() is False
