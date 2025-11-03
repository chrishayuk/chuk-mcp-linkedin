"""
Test script for atomic chart components.

Demonstrates all 5 chart types with type-safe Pydantic models.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.models import (
    BarChartData,
    ComparisonChartData,
    MetricsChartData,
    ProgressChartData,
    RankingChartData,
)
from chuk_mcp_linkedin.posts import ComposablePost


def test_bar_chart():
    """Test bar chart component"""
    print("=" * 60)
    print("BAR CHART TEST")
    print("=" * 60)

    # Validate with Pydantic
    chart_data = BarChartData(
        data={"AI-Assisted": 12, "Code Review": 6, "Documentation": 4, "Debugging": 8},
        title="TIME SAVED PER WEEK",
        unit="hours",
    )

    post = ComposablePost("text")
    post.add_hook("stat", "📊 Developer Productivity in 2025")
    post.add_body("We surveyed 500 developers about AI coding tools.")
    post.add_bar_chart(chart_data.data, chart_data.title, chart_data.unit)

    result = post.compose()
    print(result)
    print(f"\nCharacter count: {len(result)}")
    print()


def test_metrics_chart():
    """Test metrics chart component"""
    print("=" * 60)
    print("METRICS CHART TEST")
    print("=" * 60)

    # Validate with Pydantic
    chart_data = MetricsChartData(
        data={
            "Faster problem-solving": "67%",
            "Fewer bugs in production": "54%",
            "Better learning & upskilling": "89%",
        },
        title="KEY FINDINGS",
    )

    post = ComposablePost("text")
    post.add_hook("stat", "📈 AI Impact on Development Teams")
    post.add_metrics_chart(chart_data.data, chart_data.title)

    result = post.compose()
    print(result)
    print(f"\nCharacter count: {len(result)}")
    print()


def test_comparison_chart():
    """Test comparison chart component"""
    print("=" * 60)
    print("COMPARISON CHART TEST")
    print("=" * 60)

    # Validate with Pydantic
    chart_data = ComparisonChartData(
        data={
            "Traditional Development": [
                "Slower iterations",
                "Manual testing",
                "Limited code suggestions",
            ],
            "AI-Assisted Development": [
                "Faster prototyping",
                "Automated tests",
                "Intelligent completions",
            ],
        },
        title="DEVELOPMENT APPROACHES",
    )

    post = ComposablePost("text")
    post.add_hook("question", "Which development approach works better in 2025?")
    post.add_comparison_chart(chart_data.data, chart_data.title)

    result = post.compose()
    print(result)
    print(f"\nCharacter count: {len(result)}")
    print()


def test_progress_chart():
    """Test progress chart component"""
    print("=" * 60)
    print("PROGRESS CHART TEST")
    print("=" * 60)

    # Validate with Pydantic
    chart_data = ProgressChartData(
        data={"Backend API": 85, "Frontend UI": 70, "Testing": 45, "Documentation": 30},
        title="PROJECT STATUS",
    )

    post = ComposablePost("text")
    post.add_hook("story", "🚀 Our AI Platform Launch Update")
    post.add_body("Here's where we stand 2 weeks before launch:")
    post.add_progress_chart(chart_data.data, chart_data.title)
    post.add_cta("curiosity", "Which area should we focus on next?")

    result = post.compose()
    print(result)
    print(f"\nCharacter count: {len(result)}")
    print()


def test_ranking_chart():
    """Test ranking chart component"""
    print("=" * 60)
    print("RANKING CHART TEST")
    print("=" * 60)

    # Validate with Pydantic
    chart_data = RankingChartData(
        data={
            "Python": "1.2M developers",
            "JavaScript": "1.1M developers",
            "TypeScript": "850K developers",
            "Go": "420K developers",
            "Rust": "380K developers",
        },
        title="TOP 5 LANGUAGES IN 2025",
        show_medals=True,
    )

    post = ComposablePost("text")
    post.add_hook("list", "🏆 Most Popular Programming Languages")
    post.add_body("Based on our 2025 developer survey:")
    post.add_ranking_chart(chart_data.data, chart_data.title, chart_data.show_medals)
    post.add_cta("curiosity", "What language are you focusing on?")
    post.add_hashtags(["Programming", "TechTrends", "Developers"])

    result = post.compose()
    print(result)
    print(f"\nCharacter count: {len(result)}")
    print()


def test_combined_charts():
    """Test multiple charts in one post"""
    print("=" * 60)
    print("COMBINED CHARTS TEST")
    print("=" * 60)

    post = ComposablePost("text")

    # Hook
    post.add_hook("stat", "📊 The State of AI in Software Development")

    # Introduction
    post.add_body("Our 2025 survey of 500 developers reveals interesting patterns:")

    # Bar chart - time saved
    post.add_bar_chart(
        data={"AI Coding": 12, "Code Review": 6, "Debugging": 8},
        title="HOURS SAVED PER WEEK",
        unit="hours",
    )

    # Metrics - impact
    post.add_body("But the real impact goes beyond time:")
    post.add_metrics_chart(
        data={
            "Faster problem-solving": "67%",
            "Better code quality": "54%",
            "Improved learning": "89%",
        },
        title="DEVELOPER IMPACT",
    )

    # Progress - adoption
    post.add_body("Current adoption across different use cases:")
    post.add_progress_chart(
        data={
            "Code completion": 95,
            "Bug detection": 78,
            "Test generation": 62,
            "Architecture design": 23,
        },
        title="ADOPTION RATES",
    )

    # CTA
    post.add_cta("curiosity", "How is AI changing your development workflow?")

    # Hashtags
    post.add_hashtags(["AI", "SoftwareDevelopment", "TechTrends"])

    result = post.compose()
    print(result)
    print(f"\nCharacter count: {len(result)}")
    print()


def test_validation_errors():
    """Test Pydantic validation"""
    print("=" * 60)
    print("VALIDATION ERROR TESTS")
    print("=" * 60)

    # Test 1: Empty data
    try:
        BarChartData(data={}, title="Test")
        print("❌ Should have failed: empty data")
    except Exception as e:
        print(f"✅ Caught empty data: {e}")

    # Test 2: Invalid progress percentage
    try:
        ProgressChartData(data={"Test": 150})  # > 100
        print("❌ Should have failed: invalid percentage")
    except Exception as e:
        print(f"✅ Caught invalid percentage: {e}")

    # Test 3: Comparison with < 2 items
    try:
        ComparisonChartData(data={"Only One": "item"})
        print("❌ Should have failed: < 2 comparison items")
    except Exception as e:
        print(f"✅ Caught insufficient items: {e}")

    # Test 4: Bar chart with non-integer values
    try:
        BarChartData(data={"Test": "not a number"})
        print("❌ Should have failed: non-integer value")
    except Exception as e:
        print(f"✅ Caught non-integer value: {e}")

    print()


if __name__ == "__main__":
    test_bar_chart()
    test_metrics_chart()
    test_comparison_chart()
    test_progress_chart()
    test_ranking_chart()
    test_combined_charts()
    test_validation_errors()

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
