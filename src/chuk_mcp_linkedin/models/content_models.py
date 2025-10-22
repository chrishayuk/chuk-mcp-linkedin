"""
Pydantic models for content component data structures.

Provides type-safe validation for Quote, BigStat, Timeline, KeyTakeaway, and ProCon components.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any


class QuoteData(BaseModel):
    """Data model for quote/testimonial components"""

    text: str = Field(..., description="Quote text", min_length=1, max_length=500)
    author: str = Field(..., description="Quote author name", min_length=1)
    source: str | None = Field(None, description="Optional source/title (e.g., 'CTO at TechCorp')")


class BigStatData(BaseModel):
    """Data model for big statistic display"""

    number: str = Field(
        ...,
        description="The statistic number (e.g., '2.5M', '340%', '10x')",
        examples=["2.5M", "340%", "10x", "99.9%"],
    )
    label: str = Field(
        ..., description="Description of the statistic", min_length=1, max_length=200
    )
    context: str | None = Field(
        None, description="Optional additional context (e.g., '↑ 340% growth YoY')", max_length=200
    )


class TimelineData(BaseModel):
    """Data model for timeline/step components"""

    steps: Dict[str, str] = Field(
        ...,
        description="Timeline steps as key-value pairs (year/step: description)",
        examples=[{"2023": "Launched MVP", "2024": "Reached 10K users"}],
    )
    title: str | None = Field(None, description="Optional timeline title")
    style: str = Field(
        "arrow",
        description="Timeline style: 'arrow', 'numbered', 'dated'",
        pattern="^(arrow|numbered|dated)$",
    )

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, v):
        if not v or len(v) < 2:
            raise ValueError("Timeline requires at least 2 steps")
        return v


class KeyTakeawayData(BaseModel):
    """Data model for key takeaway/insight box"""

    message: str = Field(..., description="The key takeaway message", min_length=1, max_length=500)
    title: str = Field("KEY TAKEAWAY", description="Takeaway box title", max_length=50)
    style: str = Field(
        "box",
        description="Display style: 'box', 'highlight', 'simple'",
        pattern="^(box|highlight|simple)$",
    )


class ProConData(BaseModel):
    """Data model for pros & cons comparison"""

    pros: List[str] = Field(..., description="List of pros/advantages", min_length=1)
    cons: List[str] = Field(..., description="List of cons/disadvantages", min_length=1)
    title: str | None = Field(None, description="Optional title for the comparison")

    @field_validator("pros", "cons")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Must have at least one item")
        for item in v:
            if not item or len(item.strip()) == 0:
                raise ValueError("Items cannot be empty")
        return v


class ChecklistData(BaseModel):
    """Data model for checklist component"""

    items: List[Dict[str, Any]] = Field(
        ...,
        description="Checklist items with text and checked status",
        min_length=1,
        examples=[[{"text": "Deploy to production", "checked": True}]],
    )
    title: str | None = Field(None, description="Optional checklist title")
    show_progress: bool = Field(
        False, description="Show completion progress (e.g., '3/5 complete')"
    )

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Checklist must have at least one item")
        for item in v:
            if "text" not in item:
                raise ValueError("Each checklist item must have 'text' field")
            if not item["text"] or len(item["text"].strip()) == 0:
                raise ValueError("Checklist item text cannot be empty")
            # checked defaults to False if not provided
            if "checked" not in item:
                item["checked"] = False
        return v


class BeforeAfterData(BaseModel):
    """Data model for before/after comparison"""

    before: List[str] = Field(..., description="List of 'before' items", min_length=1)
    after: List[str] = Field(..., description="List of 'after' items", min_length=1)
    title: str | None = Field(None, description="Optional comparison title")
    labels: Dict[str, str] | None = Field(
        None,
        description="Custom labels for before/after (e.g., {'before': 'Old Way', 'after': 'New Way'})",
    )

    @field_validator("before", "after")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Must have at least one item")
        for item in v:
            if not item or len(item.strip()) == 0:
                raise ValueError("Items cannot be empty")
        return v


class TipBoxData(BaseModel):
    """Data model for tip/note box"""

    message: str = Field(..., description="Tip or note message", min_length=1, max_length=500)
    title: str | None = Field(
        None, description="Optional tip box title (e.g., 'Pro Tip', 'Warning')", max_length=50
    )
    style: str = Field(
        "info",
        description="Box style: 'info', 'tip', 'warning', 'success'",
        pattern="^(info|tip|warning|success)$",
    )


class StatsGridData(BaseModel):
    """Data model for stats grid display"""

    stats: Dict[str, str] = Field(
        ...,
        description="Statistics as key-value pairs (label: value)",
        min_length=2,
        examples=[{"Speed": "+67%", "Quality": "+54%"}],
    )
    title: str | None = Field(None, description="Optional grid title")
    columns: int = Field(2, description="Number of columns in the grid", ge=1, le=4)

    @field_validator("stats")
    @classmethod
    def validate_stats(cls, v):
        if len(v) < 2:
            raise ValueError("Stats grid requires at least 2 statistics")
        return v


class PollPreviewData(BaseModel):
    """Data model for poll preview"""

    question: str = Field(..., description="Poll question", min_length=1, max_length=300)
    options: List[str] = Field(..., description="Poll options", min_length=2, max_length=4)

    @field_validator("options")
    @classmethod
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError("Poll must have at least 2 options")
        if len(v) > 4:
            raise ValueError("Poll cannot have more than 4 options")
        for option in v:
            if not option or len(option.strip()) == 0:
                raise ValueError("Poll options cannot be empty")
        return v


class FeatureListData(BaseModel):
    """Data model for feature list with icons"""

    features: List[Dict[str, str]] = Field(
        ...,
        description="Features with icon, title, and optional description",
        min_length=1,
        examples=[[{"icon": "⚡", "title": "Fast", "description": "Lightning fast performance"}]],
    )
    title: str | None = Field(None, description="Optional feature list title")

    @field_validator("features")
    @classmethod
    def validate_features(cls, v):
        if not v:
            raise ValueError("Feature list must have at least one feature")
        for feature in v:
            if "title" not in feature:
                raise ValueError("Each feature must have a 'title' field")
            if not feature["title"] or len(feature["title"].strip()) == 0:
                raise ValueError("Feature title cannot be empty")
            # icon is optional but should have default
            if "icon" not in feature:
                feature["icon"] = "•"
        return v


class NumberedListData(BaseModel):
    """Data model for numbered list"""

    items: List[str] = Field(..., description="List items", min_length=1)
    title: str | None = Field(None, description="Optional list title")
    style: str = Field(
        "numbers",
        description="Numbering style: 'numbers', 'emoji_numbers', 'bold_numbers'",
        pattern="^(numbers|emoji_numbers|bold_numbers)$",
    )
    start: int = Field(1, description="Starting number", ge=1)

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Numbered list must have at least one item")
        for item in v:
            if not item or len(item.strip()) == 0:
                raise ValueError("List items cannot be empty")
        return v
