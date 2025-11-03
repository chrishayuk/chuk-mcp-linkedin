# src/chuk_mcp_linkedin/posts/components/__init__.py
"""
LinkedIn post components.

All atomic components for building LinkedIn posts following shadcn/ui design philosophy.
One component per file, organized by function.
"""

# Base class
from .base import PostComponent

# Content components
from .content import (
    Body,
    CallToAction,
    Hashtags,
    Hook,
)

# Data visualization components
from .data_viz import (
    BarChart,
    ComparisonChart,
    MetricsChart,
    ProgressChart,
    RankingChart,
)

# Feature components
from .features import (
    BeforeAfter,
    BigStat,
    Checklist,
    FeatureList,
    KeyTakeaway,
    NumberedList,
    PollPreview,
    ProCon,
    Quote,
    StatsGrid,
    Timeline,
    TipBox,
)

# Layout components
from .layout import (
    Separator,
)

__all__ = [
    # Base
    "PostComponent",
    # Content
    "Hook",
    "Body",
    "CallToAction",
    "Hashtags",
    # Data viz
    "BarChart",
    "MetricsChart",
    "ComparisonChart",
    "ProgressChart",
    "RankingChart",
    # Features
    "Quote",
    "BigStat",
    "Timeline",
    "KeyTakeaway",
    "ProCon",
    "Checklist",
    "BeforeAfter",
    "TipBox",
    "StatsGrid",
    "PollPreview",
    "FeatureList",
    "NumberedList",
    # Layout
    "Separator",
]
