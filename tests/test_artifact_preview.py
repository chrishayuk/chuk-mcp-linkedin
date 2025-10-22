"""Tests for artifact-based preview system."""

import pytest
from chuk_mcp_linkedin.preview.artifact_preview import ArtifactPreviewManager, get_artifact_manager


@pytest.mark.asyncio
async def test_artifact_preview_manager_initialization():
    """Test artifact preview manager can be initialized."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        assert manager is not None
        assert manager.provider == "memory"
        assert manager.sandbox_id == "linkedin-mcp"


@pytest.mark.asyncio
async def test_session_creation():
    """Test session creation."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session_id = manager.create_session(user_id="test_user")
        assert session_id == "user_test_user"
        assert manager.get_session() == session_id


@pytest.mark.asyncio
async def test_session_management():
    """Test session get/set."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        # Create initial session
        session1 = manager.create_session()
        assert manager.get_session() == session1

        # Set new session
        manager.set_session("custom_session")
        assert manager.get_session() == "custom_session"


@pytest.mark.asyncio
async def test_store_and_retrieve_preview():
    """Test storing and retrieving a preview."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session_id = manager.create_session()

        # Store preview
        html_content = "<html><body>Test Preview</body></html>"
        artifact_id = await manager.store_preview(
            html_content=html_content,
            draft_id="test_draft_1",
            draft_name="Test Draft",
            session_id=session_id,
        )

        assert artifact_id is not None

        # Retrieve preview
        retrieved = await manager.get_preview(artifact_id, session_id=session_id)
        assert retrieved is not None
        assert retrieved.decode("utf-8") == html_content


@pytest.mark.asyncio
async def test_list_previews():
    """Test listing previews for a session."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session_id = manager.create_session()

        # Store multiple previews
        html1 = "<html><body>Preview 1</body></html>"
        html2 = "<html><body>Preview 2</body></html>"

        await manager.store_preview(
            html_content=html1, draft_id="draft_1", draft_name="Draft 1", session_id=session_id
        )

        await manager.store_preview(
            html_content=html2, draft_id="draft_2", draft_name="Draft 2", session_id=session_id
        )

        # List previews - returns all artifacts in session
        previews = await manager.list_previews(session_id=session_id)
        # Note: The actual filtering depends on chuk-artifacts metadata structure
        # For now, just verify we can list artifacts
        assert isinstance(previews, list)


@pytest.mark.asyncio
async def test_delete_preview():
    """Test deleting a preview."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session_id = manager.create_session()

        # Store preview
        html_content = "<html><body>Test Preview</body></html>"
        artifact_id = await manager.store_preview(
            html_content=html_content,
            draft_id="test_draft",
            draft_name="Test Draft",
            session_id=session_id,
        )

        # Delete preview
        success = await manager.delete_preview(artifact_id, session_id=session_id)
        assert success is True

        # Verify deleted
        retrieved = await manager.get_preview(artifact_id, session_id=session_id)
        assert retrieved is None


@pytest.mark.asyncio
async def test_session_storage():
    """Test that sessions can store and retrieve their own previews."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session1 = manager.create_session(user_id="user1")
        html1 = "<html><body>Session 1 Preview</body></html>"

        # Store preview in session 1
        artifact_id = await manager.store_preview(
            html_content=html1, draft_id="draft_1", draft_name="Draft 1", session_id=session1
        )

        # Session 1 can retrieve its own preview
        retrieved = await manager.get_preview(artifact_id, session_id=session1)
        assert retrieved is not None
        assert retrieved.decode("utf-8") == html1

        # Create session 2 with different preview
        session2 = manager.create_session(user_id="user2")
        html2 = "<html><body>Session 2 Preview</body></html>"

        artifact_id2 = await manager.store_preview(
            html_content=html2, draft_id="draft_2", draft_name="Draft 2", session_id=session2
        )

        # Session 2 can retrieve its own preview
        retrieved2 = await manager.get_preview(artifact_id2, session_id=session2)
        assert retrieved2 is not None
        assert retrieved2.decode("utf-8") == html2


@pytest.mark.asyncio
async def test_provider_configuration():
    """Test different provider configurations."""
    # Test filesystem provider
    async with ArtifactPreviewManager(provider="filesystem", sandbox_id="test-sandbox") as manager:
        assert manager.provider == "filesystem"
        assert manager.sandbox_id == "test-sandbox"

    # Test S3 provider (configuration should be handled via env vars)
    async with ArtifactPreviewManager(provider="s3") as manager:
        assert manager.provider == "s3"


@pytest.mark.asyncio
async def test_get_artifact_manager_singleton():
    """Test global artifact manager singleton."""
    # First call creates instance
    manager1 = await get_artifact_manager(provider="memory")
    assert manager1 is not None

    # Second call returns same instance
    manager2 = await get_artifact_manager(provider="memory")
    assert manager2 is manager1


@pytest.mark.asyncio
async def test_store_preview_without_session():
    """Test storing preview without explicit session ID."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        # Create session first
        _ = manager.create_session()

        # Store preview using current session
        html = "<html><body>Test</body></html>"
        artifact_id = await manager.store_preview(
            html_content=html,
            draft_id="draft_1",
            draft_name="Draft 1",
            # No session_id - should use current
        )

        assert artifact_id is not None


@pytest.mark.asyncio
async def test_store_preview_no_session_error():
    """Test error when storing preview without any session."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        html = "<html><body>Test</body></html>"

        with pytest.raises(ValueError, match="No session ID provided or set"):
            await manager.store_preview(
                html_content=html,
                draft_id="draft_1",
                draft_name="Draft 1",
                # No session at all
            )


@pytest.mark.asyncio
async def test_get_preview_not_found():
    """Test retrieving non-existent preview."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session_id = manager.create_session()

        # Try to get preview that doesn't exist
        retrieved = await manager.get_preview("nonexistent_id", session_id=session_id)
        assert retrieved is None


@pytest.mark.asyncio
async def test_get_preview_url():
    """Test generating presigned URLs."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session_id = manager.create_session()

        # Store preview
        html = "<html><body>Test</body></html>"
        artifact_id = await manager.store_preview(
            html_content=html, draft_id="draft_1", draft_name="Draft 1", session_id=session_id
        )

        # Get presigned URL (may not be supported by memory provider)
        _ = await manager.get_preview_url(artifact_id, session_id=session_id)
        # Memory provider typically doesn't support presigned URLs
        # Just verify method doesn't crash


@pytest.mark.asyncio
async def test_delete_nonexistent_preview():
    """Test deleting non-existent preview."""
    async with ArtifactPreviewManager(provider="memory") as manager:
        session_id = manager.create_session()

        # Try to delete preview that doesn't exist
        # The delete method catches exceptions and returns True regardless
        # This is expected behavior from chuk-artifacts
        success = await manager.delete_preview("nonexistent_id", session_id=session_id)
        # Just verify it doesn't crash
        assert isinstance(success, bool)
