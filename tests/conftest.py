"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return """This is a sample LinkedIn post.

It has multiple paragraphs.

And demonstrates proper formatting."""


@pytest.fixture
def sample_word_count():
    """Sample word count for emoji calculations"""
    return 100


@pytest.fixture
def theme_manager():
    """Theme manager instance"""
    from chuk_mcp_linkedin import ThemeManager

    return ThemeManager()


@pytest.fixture
def all_theme_names():
    """List of all pre-built theme names"""
    return [
        "thought_leader",
        "personal_brand",
        "technical_expert",
        "community_builder",
        "corporate_professional",
        "contrarian_voice",
        "storyteller",
        "data_driven",
        "coach_mentor",
        "entertainer",
    ]
