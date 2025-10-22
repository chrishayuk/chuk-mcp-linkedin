"""Tests for RankingChart component."""

from chuk_mcp_linkedin.posts.components.data_viz.ranking_chart import RankingChart


class TestRankingChartInitialization:
    """Test RankingChart component initialization."""

    def test_init_with_minimal_params(self):
        """Test initialization with minimal parameters."""
        data = {"First": "100 pts", "Second": "90 pts"}
        chart = RankingChart(data)
        assert chart.data == data
        assert chart.title is None
        assert chart.show_medals is True

    def test_init_with_all_params(self):
        """Test initialization with all parameters."""
        data = {"Top": "100"}
        chart = RankingChart(data, title="Leaderboard", show_medals=False)
        assert chart.title == "Leaderboard"
        assert chart.show_medals is False


class TestRankingChartRender:
    """Test RankingChart component rendering."""

    def test_render_without_title(self):
        """Test rendering without title."""
        chart = RankingChart({"Player 1": "100", "Player 2": "90"})
        result = chart.render()
        assert "Player 1" in result
        assert "Player 2" in result

    def test_render_with_title(self):
        """Test rendering with title."""
        chart = RankingChart({"Item": "Score"}, title="Top 5")
        result = chart.render()
        assert "TOP 5:" in result

    def test_render_with_medals_first_place(self):
        """Test rendering first place gets gold medal."""
        chart = RankingChart({"First": "100"})
        result = chart.render()
        assert "🥇" in result

    def test_render_with_medals_second_place(self):
        """Test rendering second place gets silver medal."""
        chart = RankingChart({"First": "100", "Second": "90"})
        result = chart.render()
        assert "🥈" in result

    def test_render_with_medals_third_place(self):
        """Test rendering third place gets bronze medal."""
        chart = RankingChart({"First": "100", "Second": "90", "Third": "80"})
        result = chart.render()
        assert "🥉" in result

    def test_render_with_medals_fourth_place(self):
        """Test rendering fourth place gets number."""
        data = {"1st": "100", "2nd": "90", "3rd": "80", "4th": "70"}
        chart = RankingChart(data)
        result = chart.render()
        assert "4." in result

    def test_render_without_medals(self):
        """Test rendering without medals."""
        chart = RankingChart({"First": "100", "Second": "90"}, show_medals=False)
        result = chart.render()
        assert "1." in result
        assert "2." in result
        assert "🥇" not in result
        assert "🥈" not in result


class TestRankingChartValidation:
    """Test RankingChart component validation."""

    def test_validate_valid_data(self):
        """Test validation with valid data."""
        chart = RankingChart({"A": "100", "B": "90"})
        assert chart.validate() is True

    def test_validate_single_item(self):
        """Test validation with single item."""
        chart = RankingChart({"Winner": "100"})
        assert chart.validate() is True

    def test_validate_empty_data(self):
        """Test validation with empty data."""
        chart = RankingChart({})
        assert chart.validate() is False
