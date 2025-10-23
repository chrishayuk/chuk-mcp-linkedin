# src/chuk_mcp_linkedin/models/chart_models.py
"""
Pydantic models for chart component data structures.

Provides type-safe validation for chart inputs.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any


class BarChartData(BaseModel):
    """Data model for bar charts"""

    data: Dict[str, int] = Field(
        ...,
        description="Chart data with labels as keys and integer values",
        examples=[{"AI-Assisted": 12, "Code Review": 6, "Documentation": 4}],
    )
    title: str | None = Field(None, description="Optional chart title")
    unit: str = Field("", description="Optional unit label (e.g., 'hours', 'users', 'tasks')")

    @field_validator("data")
    @classmethod
    def validate_data(cls, v: Dict[str, int]) -> Dict[str, int]:
        if not v:
            raise ValueError("Chart data cannot be empty")
        if not all(isinstance(val, int) for val in v.values()):
            raise ValueError("All values must be integers")
        return v


class MetricsChartData(BaseModel):
    """Data model for metrics charts with indicators"""

    data: Dict[str, str] = Field(
        ...,
        description="Metrics data with labels and string values (e.g., percentages)",
        examples=[{"Faster problem-solving": "67%", "Better learning": "89%"}],
    )
    title: str | None = Field(None, description="Optional chart title")

    @field_validator("data")
    @classmethod
    def validate_data(cls, v: Dict[str, str]) -> Dict[str, str]:
        if not v:
            raise ValueError("Metrics data cannot be empty")
        return v


class ComparisonChartData(BaseModel):
    """Data model for comparison charts"""

    data: Dict[str, Any] = Field(
        ...,
        description="Comparison data with 2+ options. Values can be strings or lists of points.",
        examples=[
            {
                "Traditional Dev": ["Slower iterations", "Manual testing"],
                "AI-Assisted Dev": ["Faster prototyping", "Automated tests"],
            }
        ],
    )
    title: str | None = Field(None, description="Optional chart title")

    @field_validator("data")
    @classmethod
    def validate_data(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if len(v) < 2:
            raise ValueError("Comparison chart requires at least 2 items")
        return v


class ProgressChartData(BaseModel):
    """Data model for progress bar charts"""

    data: Dict[str, int] = Field(
        ...,
        description="Progress data with labels and percentage values (0-100)",
        examples=[{"Completion": 75, "Testing": 50, "Documentation": 30}],
    )
    title: str | None = Field(None, description="Optional chart title")

    @field_validator("data")
    @classmethod
    def validate_data(cls, v: Dict[str, int]) -> Dict[str, int]:
        if not v:
            raise ValueError("Progress data cannot be empty")
        for label, value in v.items():
            if not isinstance(value, int):
                raise ValueError(f"Value for '{label}' must be an integer")
            if not 0 <= value <= 100:
                raise ValueError(f"Progress value for '{label}' must be between 0-100, got {value}")
        return v


class RankingChartData(BaseModel):
    """Data model for ranking/leaderboard charts"""

    data: Dict[str, str] = Field(
        ...,
        description="Ranking data with labels and description values",
        examples=[{"Python": "1M users", "JavaScript": "900K users", "Rust": "500K users"}],
    )
    title: str | None = Field(None, description="Optional chart title")
    show_medals: bool = Field(True, description="Show medal emojis for top 3 positions")

    @field_validator("data")
    @classmethod
    def validate_data(cls, v: Dict[str, str]) -> Dict[str, str]:
        if not v:
            raise ValueError("Ranking data cannot be empty")
        return v
