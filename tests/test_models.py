"""Tests for Pydantic data models."""

import pytest
from pydantic import ValidationError

from chuk_mcp_linkedin.models import (
    # Chart models
    BarChartData,
    MetricsChartData,
    ComparisonChartData,
    ProgressChartData,
    RankingChartData,
    # Content models
    QuoteData,
    BigStatData,
    TimelineData,
    KeyTakeawayData,
    ProConData,
    ChecklistData,
    BeforeAfterData,
    TipBoxData,
    StatsGridData,
    PollPreviewData,
    FeatureListData,
    NumberedListData,
)


class TestBarChartData:
    def test_valid_data(self):
        data = BarChartData(data={"A": 10, "B": 20}, title="Test", unit="units")
        assert data.data == {"A": 10, "B": 20}
        assert data.title == "Test"
        assert data.unit == "units"

    def test_empty_data_fails(self):
        with pytest.raises(ValidationError, match="Chart data cannot be empty"):
            BarChartData(data={})

    def test_non_integer_values_fail(self):
        with pytest.raises(ValidationError):
            BarChartData(data={"A": "not an int"})


class TestMetricsChartData:
    def test_valid_data(self):
        data = MetricsChartData(data={"Speed": "67%", "Quality": "89%"})
        assert data.data == {"Speed": "67%", "Quality": "89%"}

    def test_with_title(self):
        data = MetricsChartData(data={"M1": "V1"}, title="Metrics")
        assert data.title == "Metrics"

    def test_empty_data_fails(self):
        with pytest.raises(ValidationError, match="Metrics data cannot be empty"):
            MetricsChartData(data={})


class TestComparisonChartData:
    def test_valid_data(self):
        data = ComparisonChartData(data={"Option A": ["Point 1"], "Option B": ["Point 2"]})
        assert len(data.data) == 2

    def test_less_than_two_items_fails(self):
        with pytest.raises(ValidationError, match="at least 2 items"):
            ComparisonChartData(data={"Only One": "value"})


class TestProgressChartData:
    def test_valid_data(self):
        data = ProgressChartData(data={"Task": 50})
        assert data.data == {"Task": 50}

    def test_empty_data_fails(self):
        with pytest.raises(ValidationError, match="Progress data cannot be empty"):
            ProgressChartData(data={})

    def test_non_integer_fails(self):
        with pytest.raises(ValidationError):
            ProgressChartData(data={"Task": "not an int"})

    def test_value_below_zero_fails(self):
        with pytest.raises(ValidationError, match="between 0-100"):
            ProgressChartData(data={"Task": -10})

    def test_value_above_hundred_fails(self):
        with pytest.raises(ValidationError, match="between 0-100"):
            ProgressChartData(data={"Task": 150})


class TestRankingChartData:
    def test_valid_data(self):
        data = RankingChartData(data={"First": "1M users", "Second": "500K"})
        assert data.data == {"First": "1M users", "Second": "500K"}
        assert data.show_medals is True

    def test_without_medals(self):
        data = RankingChartData(data={"Item": "Value"}, show_medals=False)
        assert data.show_medals is False

    def test_empty_data_fails(self):
        with pytest.raises(ValidationError, match="Ranking data cannot be empty"):
            RankingChartData(data={})


class TestQuoteData:
    def test_valid_data(self):
        data = QuoteData(text="Great quote", author="John Doe", source="CEO")
        assert data.text == "Great quote"
        assert data.author == "John Doe"
        assert data.source == "CEO"

    def test_without_source(self):
        data = QuoteData(text="Quote", author="Author")
        assert data.source is None

    def test_empty_text_fails(self):
        with pytest.raises(ValidationError):
            QuoteData(text="", author="Author")

    def test_text_too_long_fails(self):
        with pytest.raises(ValidationError):
            QuoteData(text="x" * 501, author="Author")


class TestBigStatData:
    def test_valid_data(self):
        data = BigStatData(number="2.5M", label="users", context="growth")
        assert data.number == "2.5M"
        assert data.label == "users"
        assert data.context == "growth"

    def test_without_context(self):
        data = BigStatData(number="10x", label="faster")
        assert data.context is None


class TestTimelineData:
    def test_valid_data(self):
        data = TimelineData(steps={"2023": "Launch", "2024": "Scale"})
        assert len(data.steps) == 2
        assert data.style == "arrow"

    def test_with_custom_style(self):
        data = TimelineData(steps={"A": "1", "B": "2"}, style="numbered")
        assert data.style == "numbered"

    def test_less_than_two_steps_fails(self):
        with pytest.raises(ValidationError, match="at least 2 steps"):
            TimelineData(steps={"Only": "One"})

    def test_invalid_style_fails(self):
        with pytest.raises(ValidationError):
            TimelineData(steps={"A": "1", "B": "2"}, style="invalid")


class TestKeyTakeawayData:
    def test_valid_data(self):
        data = KeyTakeawayData(message="Important point")
        assert data.message == "Important point"
        assert data.title == "KEY TAKEAWAY"
        assert data.style == "box"

    def test_custom_title_and_style(self):
        data = KeyTakeawayData(message="Point", title="Note", style="highlight")
        assert data.title == "Note"
        assert data.style == "highlight"

    def test_invalid_style_fails(self):
        with pytest.raises(ValidationError):
            KeyTakeawayData(message="Point", style="invalid")


class TestProConData:
    def test_valid_data(self):
        data = ProConData(pros=["Good"], cons=["Bad"])
        assert data.pros == ["Good"]
        assert data.cons == ["Bad"]

    def test_with_title(self):
        data = ProConData(pros=["P"], cons=["C"], title="Analysis")
        assert data.title == "Analysis"

    def test_empty_pros_fails(self):
        with pytest.raises(ValidationError):
            ProConData(pros=[], cons=["Con"])

    def test_empty_item_fails(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            ProConData(pros=[""], cons=["Con"])


class TestChecklistData:
    def test_valid_data(self):
        data = ChecklistData(items=[{"text": "Task 1", "checked": True}])
        assert len(data.items) == 1
        assert data.items[0]["text"] == "Task 1"

    def test_defaults_checked_to_false(self):
        data = ChecklistData(items=[{"text": "Task"}])
        assert data.items[0]["checked"] is False

    def test_with_progress(self):
        data = ChecklistData(items=[{"text": "T"}], show_progress=True)
        assert data.show_progress is True

    def test_empty_items_fails(self):
        with pytest.raises(ValidationError):
            ChecklistData(items=[])

    def test_missing_text_fails(self):
        with pytest.raises(ValidationError, match="must have 'text'"):
            ChecklistData(items=[{"checked": True}])

    def test_empty_text_fails(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            ChecklistData(items=[{"text": ""}])


class TestBeforeAfterData:
    def test_valid_data(self):
        data = BeforeAfterData(before=["Old"], after=["New"])
        assert data.before == ["Old"]
        assert data.after == ["New"]

    def test_with_labels(self):
        data = BeforeAfterData(
            before=["B"], after=["A"], labels={"before": "Old Way", "after": "New Way"}
        )
        assert data.labels == {"before": "Old Way", "after": "New Way"}

    def test_empty_before_fails(self):
        with pytest.raises(ValidationError):
            BeforeAfterData(before=[], after=["New"])

    def test_empty_item_fails(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            BeforeAfterData(before=[""], after=["New"])


class TestTipBoxData:
    def test_valid_data(self):
        data = TipBoxData(message="Helpful tip")
        assert data.message == "Helpful tip"
        assert data.style == "info"

    def test_custom_style(self):
        data = TipBoxData(message="Warning", style="warning", title="Alert")
        assert data.style == "warning"
        assert data.title == "Alert"

    def test_invalid_style_fails(self):
        with pytest.raises(ValidationError):
            TipBoxData(message="Tip", style="invalid")


class TestStatsGridData:
    def test_valid_data(self):
        data = StatsGridData(stats={"A": "1", "B": "2"})
        assert len(data.stats) == 2
        assert data.columns == 2

    def test_custom_columns(self):
        data = StatsGridData(stats={"A": "1", "B": "2"}, columns=3)
        assert data.columns == 3

    def test_less_than_two_stats_fails(self):
        with pytest.raises(ValidationError, match="at least 2"):
            StatsGridData(stats={"Only": "One"})


class TestPollPreviewData:
    def test_valid_data(self):
        data = PollPreviewData(question="Choose?", options=["A", "B"])
        assert data.question == "Choose?"
        assert len(data.options) == 2

    def test_four_options(self):
        data = PollPreviewData(question="Q", options=["A", "B", "C", "D"])
        assert len(data.options) == 4

    def test_less_than_two_options_fails(self):
        with pytest.raises(ValidationError, match="at least 2"):
            PollPreviewData(question="Q", options=["Only one"])

    def test_more_than_four_options_fails(self):
        with pytest.raises(ValidationError):
            PollPreviewData(question="Q", options=["A", "B", "C", "D", "E"])

    def test_empty_option_fails(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            PollPreviewData(question="Q", options=["A", ""])


class TestFeatureListData:
    def test_valid_data(self):
        data = FeatureListData(features=[{"title": "Feature 1", "icon": "⚡"}])
        assert len(data.features) == 1

    def test_defaults_icon(self):
        data = FeatureListData(features=[{"title": "Feature"}])
        assert data.features[0]["icon"] == "•"

    def test_empty_features_fails(self):
        with pytest.raises(ValidationError):
            FeatureListData(features=[])

    def test_missing_title_fails(self):
        with pytest.raises(ValidationError, match="must have a 'title'"):
            FeatureListData(features=[{"icon": "⚡"}])

    def test_empty_title_fails(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            FeatureListData(features=[{"title": ""}])


class TestNumberedListData:
    def test_valid_data(self):
        data = NumberedListData(items=["Item 1", "Item 2"])
        assert len(data.items) == 2
        assert data.style == "numbers"
        assert data.start == 1

    def test_custom_style_and_start(self):
        data = NumberedListData(items=["I"], style="emoji_numbers", start=5)
        assert data.style == "emoji_numbers"
        assert data.start == 5

    def test_invalid_style_fails(self):
        with pytest.raises(ValidationError):
            NumberedListData(items=["I"], style="invalid")

    def test_empty_items_fails(self):
        with pytest.raises(ValidationError):
            NumberedListData(items=[])

    def test_empty_item_fails(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            NumberedListData(items=[""])


class TestModelsInit:
    """Test that models can be imported from __init__"""

    def test_all_models_importable(self):
        # If we get here, all imports succeeded
        assert True
