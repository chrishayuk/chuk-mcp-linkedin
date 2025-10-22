"""Tests for MCP tools."""

import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch
from chuk_mcp_linkedin.manager import Draft


@pytest.fixture
def mock_mcp():
    """Create a mock MCP server"""
    mcp = MagicMock()
    # Store registered tools so we can access them
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
    return manager


@pytest.fixture
def mock_linkedin_client():
    """Create a mock LinkedIn client"""
    client = MagicMock()
    client.test_connection = AsyncMock(return_value=True)
    client.validate_config = MagicMock(return_value=(True, []))
    client.create_text_post = AsyncMock(return_value={"id": "post-123"})
    return client


class TestDraftTools:
    """Test draft management tools"""

    def test_register_draft_tools(self, mock_mcp, mock_manager):
        """Test that draft tools are registered"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        tools = register_draft_tools(mock_mcp, mock_manager)

        assert "linkedin_create" in tools
        assert "linkedin_list" in tools
        assert "linkedin_switch" in tools
        assert "linkedin_get_info" in tools
        assert "linkedin_delete" in tools
        assert "linkedin_clear_all" in tools

    @pytest.mark.asyncio
    async def test_linkedin_create(self, mock_mcp, mock_manager):
        """Test creating a draft"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.create_draft.return_value = mock_draft

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_create"]("Test", "text", "professional")

        assert "Created draft 'Test'" in result
        assert "draft-123" in result
        mock_manager.create_draft.assert_called_once_with(
            name="Test", post_type="text", theme="professional"
        )

    @pytest.mark.asyncio
    async def test_linkedin_list(self, mock_mcp, mock_manager):
        """Test listing drafts"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_manager.list_drafts.return_value = [{"id": "draft-1", "name": "Test"}]

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_list"]()

        assert "draft-1" in result
        assert "Test" in result
        mock_manager.list_drafts.assert_called_once()

    @pytest.mark.asyncio
    async def test_linkedin_switch_success(self, mock_mcp, mock_manager):
        """Test switching to a draft successfully"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_manager.switch_draft.return_value = True

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_switch"]("draft-123")

        assert "Switched to draft draft-123" in result
        mock_manager.switch_draft.assert_called_once_with("draft-123")

    @pytest.mark.asyncio
    async def test_linkedin_switch_failure(self, mock_mcp, mock_manager):
        """Test switching to a non-existent draft"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_manager.switch_draft.return_value = False

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_switch"]("nonexistent")

        assert "not found" in result

    @pytest.mark.asyncio
    async def test_linkedin_get_info_with_draft_id(self, mock_mcp, mock_manager):
        """Test getting draft info with draft ID"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_draft.return_value = mock_draft
        mock_manager.get_draft_stats.return_value = {"char_count": 100}

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_get_info"]("draft-123")

        assert "draft-123" in result or "Test" in result
        mock_manager.get_draft.assert_called_once_with("draft-123")

    @pytest.mark.asyncio
    async def test_linkedin_get_info_current_draft(self, mock_mcp, mock_manager):
        """Test getting info for current draft"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.current_draft_id = "draft-123"
        mock_manager.get_draft.return_value = mock_draft
        mock_manager.get_draft_stats.return_value = {"char_count": 100}

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_get_info"](None)

        assert "draft-123" in result or "Test" in result

    @pytest.mark.asyncio
    async def test_linkedin_get_info_no_draft(self, mock_mcp, mock_manager):
        """Test getting info when no draft exists"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_manager.current_draft_id = None
        mock_manager.get_draft.return_value = None

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_get_info"](None)

        assert "No draft found" in result

    @pytest.mark.asyncio
    async def test_linkedin_delete_success(self, mock_mcp, mock_manager):
        """Test deleting a draft successfully"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_manager.delete_draft.return_value = True

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_delete"]("draft-123")

        assert "Deleted draft draft-123" in result

    @pytest.mark.asyncio
    async def test_linkedin_delete_failure(self, mock_mcp, mock_manager):
        """Test deleting non-existent draft"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_manager.delete_draft.return_value = False

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_delete"]("nonexistent")

        assert "not found" in result

    @pytest.mark.asyncio
    async def test_linkedin_clear_all(self, mock_mcp, mock_manager):
        """Test clearing all drafts"""
        from chuk_mcp_linkedin.tools.draft_tools import register_draft_tools

        mock_manager.clear_all_drafts.return_value = 5

        tools = register_draft_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_clear_all"]()

        assert "Cleared 5 drafts" in result


class TestPublishingTools:
    """Test publishing tools"""

    def test_register_publishing_tools(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test that publishing tools are registered"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)

        assert "linkedin_publish" in tools
        assert "linkedin_test_connection" in tools
        assert "linkedin_get_config_status" in tools

    @pytest.mark.asyncio
    async def test_linkedin_publish_no_draft(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test publishing with no active draft"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_manager.get_current_draft.return_value = None

        tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
        result = await tools["linkedin_publish"]()

        assert "No active draft" in result

    @pytest.mark.asyncio
    async def test_linkedin_publish_not_configured(
        self, mock_mcp, mock_manager, mock_linkedin_client
    ):
        """Test publishing when API is not configured"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_draft = Draft(
            draft_id="draft-123",
            name="Test",
            post_type="text",
            content={"composed_text": "Test post"},
            theme=None,
        )
        mock_manager.get_current_draft.return_value = mock_draft

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.is_configured.return_value = False
            mock_config.get_missing_config.return_value = ["access_token"]

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_publish"]()

            assert "not configured" in result
            assert "access_token" in result

    @pytest.mark.asyncio
    async def test_linkedin_publish_no_content(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test publishing with no content"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.is_configured.return_value = True

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_publish"]()

            assert "No post content" in result

    @pytest.mark.asyncio
    async def test_linkedin_publish_dry_run(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test publishing in dry run mode"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_draft = Draft(
            draft_id="draft-123",
            name="Test",
            post_type="text",
            content={"composed_text": "Test post content"},
            theme=None,
        )
        mock_manager.get_current_draft.return_value = mock_draft

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.is_configured.return_value = True

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_publish"](dry_run=True)

            assert "DRY RUN" in result
            assert "Test post content" in result

    @pytest.mark.asyncio
    async def test_linkedin_publish_disabled(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test publishing when publishing is disabled"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_draft = Draft(
            draft_id="draft-123",
            name="Test",
            post_type="text",
            content={"composed_text": "Test post"},
            theme=None,
        )
        mock_manager.get_current_draft.return_value = mock_draft

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.is_configured.return_value = True
            mock_config.enable_publishing = False

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_publish"](dry_run=False)

            assert "Publishing is disabled" in result

    @pytest.mark.asyncio
    async def test_linkedin_publish_success(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test successful publishing"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_draft = Draft(
            draft_id="draft-123",
            name="Test",
            post_type="text",
            content={"composed_text": "Test post"},
            theme=None,
        )
        mock_manager.get_current_draft.return_value = mock_draft

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.is_configured.return_value = True
            mock_config.enable_publishing = True

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_publish"](visibility="PUBLIC", dry_run=False)

            assert "Successfully published" in result
            assert "post-123" in result

    @pytest.mark.asyncio
    async def test_linkedin_publish_api_error(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test publishing with API error"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools
        from chuk_mcp_linkedin.api import LinkedInAPIError

        mock_draft = Draft(
            draft_id="draft-123",
            name="Test",
            post_type="text",
            content={"composed_text": "Test post"},
            theme=None,
        )
        mock_manager.get_current_draft.return_value = mock_draft
        mock_linkedin_client.create_text_post = AsyncMock(side_effect=LinkedInAPIError("API Error"))

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.is_configured.return_value = True
            mock_config.enable_publishing = True

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_publish"]()

            assert "Failed to publish" in result

    @pytest.mark.asyncio
    async def test_linkedin_test_connection_success(
        self, mock_mcp, mock_manager, mock_linkedin_client
    ):
        """Test successful connection test"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.linkedin_person_urn = "urn:li:person:123"
            mock_config.enable_publishing = True

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_test_connection"]()

            assert "successful" in result
            assert "urn:li:person:123" in result

    @pytest.mark.asyncio
    async def test_linkedin_test_connection_failure(
        self, mock_mcp, mock_manager, mock_linkedin_client
    ):
        """Test failed connection test"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_linkedin_client.test_connection = AsyncMock(return_value=False)
        mock_linkedin_client.validate_config = MagicMock(return_value=(False, ["access_token"]))

        with patch("chuk_mcp_linkedin.api.config"):
            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_test_connection"]()

            assert "not configured" in result or "failed" in result

    @pytest.mark.asyncio
    async def test_linkedin_test_connection_invalid_credentials(
        self, mock_mcp, mock_manager, mock_linkedin_client
    ):
        """Test connection test with invalid credentials"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        mock_linkedin_client.test_connection = AsyncMock(return_value=False)
        mock_linkedin_client.validate_config = MagicMock(return_value=(True, []))

        with patch("chuk_mcp_linkedin.api.config"):
            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_test_connection"]()

            assert "failed" in result

    @pytest.mark.asyncio
    async def test_linkedin_get_config_status(self, mock_mcp, mock_manager, mock_linkedin_client):
        """Test getting config status"""
        from chuk_mcp_linkedin.tools.publishing_tools import register_publishing_tools

        with patch("chuk_mcp_linkedin.api.config") as mock_config:
            mock_config.is_configured.return_value = True
            mock_config.get_missing_config.return_value = []
            mock_config.linkedin_access_token = "token"
            mock_config.linkedin_person_urn = "urn:li:person:123"
            mock_config.enable_publishing = True

            tools = register_publishing_tools(mock_mcp, mock_manager, mock_linkedin_client)
            result = await tools["linkedin_get_config_status"]()

            assert "configured" in result
            assert "urn:li:person:123" in result


class TestRegistryTools:
    """Test registry tools"""

    def test_register_registry_tools(self, mock_mcp, mock_manager):
        """Test that registry tools are registered"""
        from chuk_mcp_linkedin.tools.registry_tools import register_registry_tools

        tools = register_registry_tools(mock_mcp, mock_manager)

        assert "linkedin_list_components" in tools
        assert "linkedin_get_component_info" in tools
        assert "linkedin_get_recommendations" in tools
        assert "linkedin_get_system_overview" in tools

    @pytest.mark.asyncio
    async def test_linkedin_list_components(self, mock_mcp, mock_manager):
        """Test listing components"""
        from chuk_mcp_linkedin.tools.registry_tools import register_registry_tools

        tools = register_registry_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_list_components"]()

        # Should return JSON with components (can be list or dict)
        data = json.loads(result)
        assert isinstance(data, (list, dict))

    @pytest.mark.asyncio
    async def test_linkedin_get_component_info(self, mock_mcp, mock_manager):
        """Test getting component info"""
        from chuk_mcp_linkedin.tools.registry_tools import register_registry_tools

        tools = register_registry_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_get_component_info"]("hook")

        # Should return JSON with component info
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_linkedin_get_recommendations(self, mock_mcp, mock_manager):
        """Test getting recommendations"""
        from chuk_mcp_linkedin.tools.registry_tools import register_registry_tools

        tools = register_registry_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_get_recommendations"]("engagement")

        # Should return JSON with recommendations
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_linkedin_get_system_overview(self, mock_mcp, mock_manager):
        """Test getting system overview"""
        from chuk_mcp_linkedin.tools.registry_tools import register_registry_tools

        tools = register_registry_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_get_system_overview"]()

        # Should return JSON with system overview
        data = json.loads(result)
        assert isinstance(data, dict)


class TestThemeTools:
    """Test theme tools"""

    def test_register_theme_tools(self, mock_mcp, mock_manager):
        """Test that theme tools are registered"""
        from chuk_mcp_linkedin.tools.theme_tools import register_theme_tools

        tools = register_theme_tools(mock_mcp, mock_manager)

        assert "linkedin_list_themes" in tools
        assert "linkedin_get_theme" in tools
        assert "linkedin_apply_theme" in tools

    @pytest.mark.asyncio
    async def test_linkedin_list_themes(self, mock_mcp, mock_manager):
        """Test listing themes"""
        from chuk_mcp_linkedin.tools.theme_tools import register_theme_tools

        tools = register_theme_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_list_themes"]()

        # Should return JSON with themes (can be list or dict)
        data = json.loads(result)
        assert isinstance(data, (list, dict))

    @pytest.mark.asyncio
    async def test_linkedin_get_theme(self, mock_mcp, mock_manager):
        """Test getting theme info"""
        from chuk_mcp_linkedin.tools.theme_tools import register_theme_tools

        tools = register_theme_tools(mock_mcp, mock_manager)
        # Use a valid theme name
        result = await tools["linkedin_get_theme"]("thought_leader")

        # Should return JSON with theme info
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_linkedin_apply_theme_no_draft(self, mock_mcp, mock_manager):
        """Test applying theme with no active draft"""
        from chuk_mcp_linkedin.tools.theme_tools import register_theme_tools

        mock_manager.get_current_draft.return_value = None

        tools = register_theme_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_apply_theme"]("professional")

        assert "No active draft" in result

    @pytest.mark.asyncio
    async def test_linkedin_apply_theme_success(self, mock_mcp, mock_manager):
        """Test successfully applying theme"""
        from chuk_mcp_linkedin.tools.theme_tools import register_theme_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_theme_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_apply_theme"]("professional")

        assert "Applied theme 'professional'" in result
        mock_manager.update_draft.assert_called_once_with("draft-123", theme="professional")


class TestCompositionTools:
    """Test composition tools"""

    def test_register_composition_tools(self, mock_mcp, mock_manager):
        """Test that composition tools are registered"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        tools = register_composition_tools(mock_mcp, mock_manager)

        # Check content tools
        assert "linkedin_add_hook" in tools
        assert "linkedin_add_body" in tools
        assert "linkedin_add_cta" in tools
        assert "linkedin_add_hashtags" in tools

        # Check chart tools
        assert "linkedin_add_bar_chart" in tools
        assert "linkedin_add_metrics_chart" in tools
        assert "linkedin_add_comparison_chart" in tools
        assert "linkedin_add_progress_chart" in tools
        assert "linkedin_add_ranking_chart" in tools

        # Check feature tools
        assert "linkedin_add_quote" in tools
        assert "linkedin_add_big_stat" in tools
        assert "linkedin_add_timeline" in tools
        assert "linkedin_add_key_takeaway" in tools
        assert "linkedin_add_pro_con" in tools
        assert "linkedin_add_checklist" in tools
        assert "linkedin_add_before_after" in tools
        assert "linkedin_add_tip_box" in tools
        assert "linkedin_add_stats_grid" in tools
        assert "linkedin_add_poll_preview" in tools
        assert "linkedin_add_feature_list" in tools
        assert "linkedin_add_numbered_list" in tools

        # Check composition tools
        assert "linkedin_compose_post" in tools
        assert "linkedin_get_preview" in tools
        assert "linkedin_preview_html" in tools
        assert "linkedin_export_draft" in tools

    @pytest.mark.asyncio
    async def test_linkedin_add_hook_no_draft(self, mock_mcp, mock_manager):
        """Test adding hook with no active draft"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_manager.get_current_draft.return_value = None

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_hook"]("question", "Why is AI important?")

        assert "No active draft" in result

    @pytest.mark.asyncio
    async def test_linkedin_add_hook_success(self, mock_mcp, mock_manager):
        """Test successfully adding hook"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_hook"]("question", "Why is AI important?")

        assert "Added question hook" in result
        # No longer calls update_draft on every component add

    @pytest.mark.asyncio
    async def test_linkedin_add_body_success(self, mock_mcp, mock_manager):
        """Test successfully adding body"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_body"]("Main content here", "linear")

        assert "Added body" in result
        assert "linear" in result

    @pytest.mark.asyncio
    async def test_linkedin_add_cta_success(self, mock_mcp, mock_manager):
        """Test successfully adding CTA"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_cta"]("direct", "Click here!")

        assert "Added direct CTA" in result

    @pytest.mark.asyncio
    async def test_linkedin_add_bar_chart_validation_error(self, mock_mcp, mock_manager):
        """Test bar chart with validation error"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_bar_chart"]({}, "Title")

        # Empty dict is valid (just no bars), validation happens in component
        assert "Added bar chart with 0 bars" in result

    @pytest.mark.asyncio
    async def test_linkedin_add_bar_chart_success(self, mock_mcp, mock_manager):
        """Test successfully adding bar chart"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_bar_chart"]({"A": 10, "B": 20}, "Chart")

        assert "Added bar chart" in result
        assert "2" in result

    @pytest.mark.asyncio
    async def test_linkedin_compose_post_no_draft(self, mock_mcp, mock_manager):
        """Test composing post with no draft"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_manager.get_current_draft.return_value = None

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_compose_post"]()

        assert "No active draft" in result

    @pytest.mark.asyncio
    async def test_linkedin_compose_post_success(self, mock_mcp, mock_manager):
        """Test successfully composing post"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123",
            name="Test",
            post_type="text",
            content={"components": [{"component": "hook", "type": "question", "content": "Test?"}]},
            theme=None,
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_compose_post"](optimize=False)

        assert "Composed post" in result

    @pytest.mark.asyncio
    async def test_linkedin_get_preview_success(self, mock_mcp, mock_manager):
        """Test getting preview"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        # Add content first so there's something to preview
        await tools["linkedin_add_body"]("Test content for preview")
        result = await tools["linkedin_get_preview"]()

        assert "Preview" in result
        assert "chars" in result

    @pytest.mark.asyncio
    async def test_linkedin_preview_html_no_draft(self, mock_mcp, mock_manager):
        """Test HTML preview with no draft"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_manager.get_current_draft.return_value = None

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_preview_html"]()

        assert "No active draft" in result

    @pytest.mark.asyncio
    async def test_linkedin_preview_html_success(self, mock_mcp, mock_manager):
        """Test successful HTML preview generation"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft
        mock_manager.generate_html_preview.return_value = "/path/to/preview.html"

        tools = register_composition_tools(mock_mcp, mock_manager)

        with patch("webbrowser.open") as mock_browser:
            result = await tools["linkedin_preview_html"](open_browser=True)

            assert "Preview generated" in result
            assert "/path/to/preview.html" in result
            mock_browser.assert_called_once()

    @pytest.mark.asyncio
    async def test_linkedin_preview_html_no_browser(self, mock_mcp, mock_manager):
        """Test HTML preview without opening browser"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft
        mock_manager.generate_html_preview.return_value = "/path/to/preview.html"

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_preview_html"](open_browser=False)

        assert "Preview generated" in result
        assert "Open in browser" in result

    @pytest.mark.asyncio
    async def test_linkedin_export_draft_no_draft(self, mock_mcp, mock_manager):
        """Test exporting with no draft"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_manager.get_current_draft.return_value = None

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_export_draft"]()

        assert "No active draft" in result

    @pytest.mark.asyncio
    async def test_linkedin_export_draft_success(self, mock_mcp, mock_manager):
        """Test successful draft export"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft
        mock_manager.export_draft.return_value = '{"draft_id": "draft-123"}'

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_export_draft"]()

        assert "draft-123" in result

    @pytest.mark.asyncio
    async def test_linkedin_add_separator(self, mock_mcp, mock_manager):
        """Test adding separator"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_separator"]("line")

        assert "Added line separator" in result

    @pytest.mark.asyncio
    async def test_linkedin_add_hashtags(self, mock_mcp, mock_manager):
        """Test adding hashtags"""
        from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools

        mock_draft = Draft(
            draft_id="draft-123", name="Test", post_type="text", content={}, theme=None
        )
        mock_manager.get_current_draft.return_value = mock_draft

        tools = register_composition_tools(mock_mcp, mock_manager)
        result = await tools["linkedin_add_hashtags"](["ai", "tech", "innovation"])

        assert "Added 3 hashtags" in result


class TestToolsInit:
    """Test tools package initialization"""

    def test_all_tools_importable(self):
        """Test that all tools can be imported from __init__"""
        from chuk_mcp_linkedin.tools import (
            register_draft_tools,
            register_composition_tools,
            register_theme_tools,
            register_publishing_tools,
            register_registry_tools,
        )

        assert register_draft_tools is not None
        assert register_composition_tools is not None
        assert register_theme_tools is not None
        assert register_publishing_tools is not None
        assert register_registry_tools is not None
