"""
LinkedIn posts module.

Complete system for composing LinkedIn posts with atomic components.
"""

from .composition import ComposablePost, PostBuilder
from .components import (
    PostComponent,
    # Content
    Hook, Body, CallToAction, Hashtags,
    # Data viz
    BarChart, MetricsChart, ComparisonChart, ProgressChart, RankingChart,
    # Features
    Quote, BigStat, Timeline, KeyTakeaway, ProCon,
    Checklist, BeforeAfter, TipBox, StatsGrid, PollPreview, FeatureList, NumberedList,
    # Layout
    Separator,
)

__all__ = [
    # Composition
    "ComposablePost",
    "PostBuilder",
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
