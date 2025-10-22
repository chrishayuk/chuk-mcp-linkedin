"""Tests for ComparisonChart component."""

from chuk_mcp_linkedin.posts.components.data_viz.comparison_chart import ComparisonChart


class TestComparisonChartInitialization:
    """Test ComparisonChart component initialization."""

    def test_init_with_minimal_params(self):
        """Test initialization with minimal parameters."""
        data = {"Before": ["Old feature"], "After": ["New feature"]}
        chart = ComparisonChart(data)
        assert chart.data == data
        assert chart.title is None

    def test_init_with_title(self):
        """Test initialization with title."""
        data = {"Option A": ["Point 1"], "Option B": ["Point 2"]}
        chart = ComparisonChart(data, title="Comparison")
        assert chart.title == "Comparison"


class TestComparisonChartRender:
    """Test ComparisonChart component rendering."""

    def test_render_without_title(self):
        """Test rendering without title."""
        data = {"Bad": ["Point 1"], "Good": ["Point 2"]}
        chart = ComparisonChart(data)
        result = chart.render()
        assert "Bad:" in result
        assert "Good:" in result

    def test_render_with_title(self):
        """Test rendering with title."""
        data = {"A": ["X"], "B": ["Y"]}
        chart = ComparisonChart(data, title="Test")
        result = chart.render()
        assert "TEST:" in result

    def test_render_with_list_points(self):
        """Test rendering with list of points."""
        data = {"Old": ["Point 1", "Point 2"], "New": ["Point 3", "Point 4"]}
        chart = ComparisonChart(data)
        result = chart.render()
        assert "Point 1" in result
        assert "Point 2" in result
        assert "Point 3" in result
        assert "Point 4" in result

    def test_render_with_string_points(self):
        """Test rendering with string instead of list."""
        data = {"Option A": "Description A", "Option B": "Description B"}
        chart = ComparisonChart(data)
        result = chart.render()
        assert "Description A" in result
        assert "Description B" in result

    def test_render_adds_negative_positive_indicators(self):
        """Test rendering adds negative/positive indicators."""
        data = {"Bad": ["X"], "Good": ["Y"]}
        chart = ComparisonChart(data)
        result = chart.render()
        # Should have indicators for first (negative) and last (positive)
        assert "❌" in result or "✅" in result


class TestComparisonChartValidation:
    """Test ComparisonChart component validation."""

    def test_validate_valid_data(self):
        """Test validation with valid data (2+ items)."""
        chart = ComparisonChart({"A": ["X"], "B": ["Y"]})
        assert chart.validate() is True

    def test_validate_three_items(self):
        """Test validation with three items."""
        chart = ComparisonChart({"A": ["X"], "B": ["Y"], "C": ["Z"]})
        assert chart.validate() is True

    def test_validate_one_item(self):
        """Test validation with only one item."""
        chart = ComparisonChart({"A": ["X"]})
        assert chart.validate() is False

    def test_validate_empty_data(self):
        """Test validation with empty data."""
        chart = ComparisonChart({})
        assert chart.validate() is False
