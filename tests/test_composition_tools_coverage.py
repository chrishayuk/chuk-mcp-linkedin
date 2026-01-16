"""Comprehensive tests for composition_tools.py coverage.

Tests all error handling paths and edge cases.
"""

from unittest.mock import MagicMock, patch

import pytest

from chuk_mcp_linkedin.manager import Draft
from chuk_mcp_linkedin.tools import composition_tools


@pytest.fixture
def mock_mcp():
    """Create a mock MCP server"""
    mcp = MagicMock()
    mcp.registered_tools = {}

    def tool_decorator(func):
        mcp.registered_tools[func.__name__] = func
        return func

    mcp.tool = tool_decorator
    return mcp


@pytest.fixture
def mock_manager():
    """Create a mock manager"""
    manager = MagicMock()
    manager.current_draft_id = "draft-123"
    manager.user_id = "test-user"
    return manager


def _cache_key(user_id: str, draft_id: str) -> str:
    """Generate user-scoped cache key (must match composition_tools._get_cache_key)"""
    return f"{user_id}:{draft_id}"


class TestCompositionToolsErrorPaths:
    """Test error handling paths in composition tools"""

    @pytest.fixture(autouse=True)
    def patch_manager(self, mock_manager):
        """Automatically patch get_current_manager for all tests in this class"""
        with patch(
            "chuk_mcp_linkedin.tools.composition_tools.get_current_manager",
            return_value=mock_manager,
        ):
            yield

    @pytest.mark.asyncio
    async def test_add_hook_exception_handling(self, mock_mcp, mock_manager):
        """Test hook with exception from ComposablePost"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        # Trigger validation error by using invalid hook type with ComposablePost
        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_hook.side_effect = ValueError("Invalid hook type")
            # Add mock to cache
            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_hook"]("invalid_type", "content")
            assert "Invalid hook type" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_body_exception_handling(self, mock_mcp, mock_manager):
        """Test body with exception from ComposablePost"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_body.side_effect = ValueError("Content too long")
            # Add mock to cache
            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_body"]("x" * 10000, "linear")
            assert "Content too long" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_cta_exception_handling(self, mock_mcp, mock_manager):
        """Test CTA with exception from ComposablePost"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_cta.side_effect = ValueError("Invalid CTA type")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_cta"]("invalid", "text")
            assert "Invalid CTA type" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_bar_chart_exception(self, mock_mcp, mock_manager):
        """Test bar chart with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_bar_chart.side_effect = ValueError("Invalid data")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_bar_chart"]({"A": "invalid"}, "Title")
            assert "Invalid data" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_metrics_chart_exception(self, mock_mcp, mock_manager):
        """Test metrics chart with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_metrics_chart.side_effect = ValueError("Invalid metrics")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_metrics_chart"]({"A": 123}, "Title")
            assert "Invalid metrics" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_comparison_chart_exception(self, mock_mcp, mock_manager):
        """Test comparison chart with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_comparison_chart.side_effect = ValueError("Need 2 options")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_comparison_chart"]({"A": "only one"}, "Title")
            assert "Need 2 options" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_progress_chart_exception(self, mock_mcp, mock_manager):
        """Test progress chart with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_progress_chart.side_effect = ValueError("Invalid percentage")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_progress_chart"]({"A": 150}, "Title")
            assert "Invalid percentage" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_ranking_chart_exception(self, mock_mcp, mock_manager):
        """Test ranking chart with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_ranking_chart.side_effect = ValueError("Invalid ranking data")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_ranking_chart"]({}, "Title")
            assert "Invalid ranking data" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_quote_exception(self, mock_mcp, mock_manager):
        """Test quote with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_quote.side_effect = ValueError("Quote too long")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_quote"]("x" * 1000, "Author")
            assert "Quote too long" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_big_stat_exception(self, mock_mcp, mock_manager):
        """Test big stat with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_big_stat.side_effect = ValueError("Invalid stat")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_big_stat"]("", "label")
            assert "Invalid stat" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_timeline_exception(self, mock_mcp, mock_manager):
        """Test timeline with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_timeline.side_effect = ValueError("Empty timeline")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_timeline"]({}, "Title")
            assert "Empty timeline" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_key_takeaway_exception(self, mock_mcp, mock_manager):
        """Test key takeaway with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_key_takeaway.side_effect = ValueError("Message too long")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_key_takeaway"]("x" * 1000)
            assert "Message too long" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_pro_con_exception(self, mock_mcp, mock_manager):
        """Test pro/con with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_pro_con.side_effect = ValueError("Empty lists")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_pro_con"]([], [])
            assert "Empty lists" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_separator_exception(self, mock_mcp, mock_manager):
        """Test separator with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_separator.side_effect = ValueError("Invalid style")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_separator"]("invalid")
            assert "Invalid style" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_checklist_exception(self, mock_mcp, mock_manager):
        """Test checklist with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_checklist.side_effect = ValueError("Invalid checklist items")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_checklist"]([])
            assert "Invalid checklist items" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_before_after_exception(self, mock_mcp, mock_manager):
        """Test before/after with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_before_after.side_effect = ValueError("Mismatched lists")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_before_after"]([], [])
            assert "Mismatched lists" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_tip_box_exception(self, mock_mcp, mock_manager):
        """Test tip box with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_tip_box.side_effect = ValueError("Message empty")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_tip_box"]("")
            assert "Message empty" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_stats_grid_exception(self, mock_mcp, mock_manager):
        """Test stats grid with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_stats_grid.side_effect = ValueError("Invalid columns")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_stats_grid"]({"A": "1"}, columns=10)
            assert "Invalid columns" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_poll_preview_exception(self, mock_mcp, mock_manager):
        """Test poll preview with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_poll_preview.side_effect = ValueError("Not enough options")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_poll_preview"]("Question?", ["A"])
            assert "Not enough options" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_feature_list_exception(self, mock_mcp, mock_manager):
        """Test feature list with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_feature_list.side_effect = ValueError("Missing title")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_feature_list"]([{"no_title": "oops"}])
            assert "Missing title" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_numbered_list_exception(self, mock_mcp, mock_manager):
        """Test numbered list with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_numbered_list.side_effect = ValueError("Empty list")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_numbered_list"]([])
            assert "Empty list" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_add_hashtags_exception(self, mock_mcp, mock_manager):
        """Test hashtags with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.add_hashtags.side_effect = ValueError("No tags")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_add_hashtags"]([])
            assert "No tags" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_compose_post_exception(self, mock_mcp, mock_manager):
        """Test compose post with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.compose.side_effect = ValueError("Content exceeds limit")
            mock_post.optimize_for_engagement.return_value = None
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_compose_post"](optimize=True)
            assert "Content exceeds limit" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_get_preview_exception(self, mock_mcp, mock_manager):
        """Test get preview with exception"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        with patch("chuk_mcp_linkedin.tools.composition_tools.ComposablePost") as _:
            mock_post = MagicMock()
            mock_post.get_preview.side_effect = ValueError("No content")
            # Add mock to cache

            composition_tools._post_cache[_cache_key("test-user", "draft-123")] = mock_post

            result = await tools["linkedin_get_preview"]()
            assert "No content" in result

            # Cleanup cache
            composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_get_or_create_post_with_theme(self, mock_mcp, mock_manager):
        """Test _get_or_create_post creates post with theme"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme="thought_leader"
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp)

        # Call any tool to trigger _get_or_create_post with theme
        result = await tools["linkedin_add_body"]("Test content")

        assert "Added body" in result
        # Verify ComposablePost was created in cache with theme
        assert _cache_key("test-user", "draft-123") in composition_tools._post_cache

        # Cleanup cache
        composition_tools._post_cache.clear()

    @pytest.mark.asyncio
    async def test_preview_html_failed_generation(self, mock_mcp, mock_manager):
        """Test HTML preview when generation fails"""
        from unittest.mock import AsyncMock

        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft
        mock_manager.generate_preview_url = AsyncMock(return_value=None)  # Failure

        tools = register_composition_tools(mock_mcp)
        result = await tools["linkedin_preview_html"](open_browser=False)

        assert "Failed to generate preview" in result
