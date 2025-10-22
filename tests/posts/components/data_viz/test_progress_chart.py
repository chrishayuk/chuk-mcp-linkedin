"""Tests for ProgressChart component."""

from chuk_mcp_linkedin.posts.components.data_viz.progress_chart import ProgressChart


class TestProgressChartInitialization:
    """Test ProgressChart component initialization."""

    def test_init_with_minimal_params(self):
        """Test initialization with minimal parameters."""
        data = {"Task A": 50, "Task B": 75}
        chart = ProgressChart(data)
        assert chart.data == data
        assert chart.title is None

    def test_init_with_title(self):
        """Test initialization with title."""
        data = {"Project": 80}
        chart = ProgressChart(data, title="Progress")
        assert chart.title == "Progress"


class TestProgressChartRender:
    """Test ProgressChart component rendering."""

    def test_render_without_title(self):
        """Test rendering without title."""
        chart = ProgressChart({"Task": 50})
        result = chart.render()
        assert "Task" in result
        assert "50%" in result

    def test_render_with_title(self):
        """Test rendering with title."""
        chart = ProgressChart({"Task": 60}, title="Status")
        result = chart.render()
        assert "STATUS:" in result

    def test_render_creates_progress_bars(self):
        """Test rendering creates progress bars."""
        chart = ProgressChart({"Task": 70})
        result = chart.render()
        # Should have filled and empty characters
        assert "█" in result or "░" in result

    def test_render_zero_percent(self):
        """Test rendering 0% progress."""
        chart = ProgressChart({"Task": 0})
        result = chart.render()
        assert "0%" in result

    def test_render_hundred_percent(self):
        """Test rendering 100% progress."""
        chart = ProgressChart({"Task": 100})
        result = chart.render()
        assert "100%" in result

    def test_render_multiple_tasks_aligned(self):
        """Test rendering multiple tasks with alignment."""
        chart = ProgressChart({"Short": 50, "Longer Task": 75})
        result = chart.render()
        assert "Short" in result
        assert "Longer Task" in result

    def test_render_non_numeric_value(self):
        """Test rendering with non-numeric value (edge case)."""
        chart = ProgressChart({"Task": "invalid"})
        result = chart.render()
        assert "Task" in result
        assert "invalid" in result


class TestProgressChartValidation:
    """Test ProgressChart component validation."""

    def test_validate_valid_data(self):
        """Test validation with valid percentages."""
        chart = ProgressChart({"A": 50, "B": 75})
        assert chart.validate() is True

    def test_validate_zero_percent(self):
        """Test validation with 0%."""
        chart = ProgressChart({"Task": 0})
        assert chart.validate() is True

    def test_validate_hundred_percent(self):
        """Test validation with 100%."""
        chart = ProgressChart({"Task": 100})
        assert chart.validate() is True

    def test_validate_float_values(self):
        """Test validation with float values."""
        chart = ProgressChart({"Task": 50.5})
        assert chart.validate() is True

    def test_validate_negative_percentage(self):
        """Test validation with negative percentage."""
        chart = ProgressChart({"Task": -10})
        assert chart.validate() is False

    def test_validate_over_hundred_percent(self):
        """Test validation with percentage over 100."""
        chart = ProgressChart({"Task": 150})
        assert chart.validate() is False

    def test_validate_empty_data(self):
        """Test validation with empty data."""
        chart = ProgressChart({})
        assert chart.validate() is False
