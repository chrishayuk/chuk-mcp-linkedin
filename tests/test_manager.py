"""
Tests for LinkedInManager and Draft.
"""

import pytest
import json
import tempfile
from pathlib import Path
from chuk_mcp_linkedin.manager import Draft, LinkedInManager


class TestDraft:
    """Test Draft class"""

    def test_draft_creation(self):
        """Test creating a draft"""
        draft = Draft(
            draft_id="draft_1",
            name="My Post",
            post_type="text",
            content={"text": "Hello world"},
            theme="thought_leader",
        )
        assert draft.draft_id == "draft_1"
        assert draft.name == "My Post"
        assert draft.post_type == "text"
        assert draft.theme == "thought_leader"

    def test_draft_update_content(self):
        """Test updating draft content"""
        draft = Draft(
            draft_id="draft_1", name="My Post", post_type="text", content={"text": "Hello"}
        )
        original_updated = draft.updated_at

        draft.update_content({"text": "Hello world"})
        assert draft.content["text"] == "Hello world"
        assert draft.updated_at != original_updated

    def test_draft_to_dict(self):
        """Test converting draft to dictionary"""
        draft = Draft(
            draft_id="draft_1",
            name="My Post",
            post_type="text",
            content={"text": "Hello"},
            theme="thought_leader",
        )
        draft_dict = draft.to_dict()

        assert draft_dict["draft_id"] == "draft_1"
        assert draft_dict["name"] == "My Post"
        assert draft_dict["theme"] == "thought_leader"
        assert "created_at" in draft_dict
        assert "updated_at" in draft_dict

    def test_draft_from_dict(self):
        """Test creating draft from dictionary"""
        data = {
            "draft_id": "draft_1",
            "name": "My Post",
            "post_type": "text",
            "content": {"text": "Hello"},
            "theme": "thought_leader",
        }
        draft = Draft.from_dict(data)

        assert draft.draft_id == "draft_1"
        assert draft.name == "My Post"
        assert draft.theme == "thought_leader"


class TestLinkedInManager:
    """Test LinkedInManager class"""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage for tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def manager(self, temp_storage):
        """Create manager with temporary storage"""
        return LinkedInManager(storage_path=temp_storage)

    def test_manager_initialization(self, temp_storage):
        """Test manager initializes correctly"""
        manager = LinkedInManager(storage_path=temp_storage)
        assert manager.storage_path == Path(temp_storage)
        assert len(manager.drafts) == 0
        assert manager.current_draft_id is None

    def test_create_draft(self, manager):
        """Test creating a draft"""
        draft = manager.create_draft(
            name="My Post",
            post_type="text",
            content={"text": "Hello world"},
            theme="thought_leader",
        )

        assert draft.name == "My Post"
        assert draft.post_type == "text"
        assert draft.theme == "thought_leader"
        assert draft.draft_id in manager.drafts
        assert manager.current_draft_id == draft.draft_id

    def test_create_multiple_drafts(self, manager):
        """Test creating multiple drafts"""
        manager.create_draft("Post 1", "text")
        draft2 = manager.create_draft("Post 2", "poll")

        assert len(manager.drafts) == 2
        assert manager.current_draft_id == draft2.draft_id

    def test_get_draft(self, manager):
        """Test getting a draft by ID"""
        draft = manager.create_draft("My Post", "text")
        retrieved = manager.get_draft(draft.draft_id)

        assert retrieved is not None
        assert retrieved.draft_id == draft.draft_id

    def test_get_draft_not_found(self, manager):
        """Test getting non-existent draft"""
        draft = manager.get_draft("nonexistent")
        assert draft is None

    def test_get_current_draft(self, manager):
        """Test getting current draft"""
        draft = manager.create_draft("My Post", "text")
        current = manager.get_current_draft()

        assert current is not None
        assert current.draft_id == draft.draft_id

    def test_get_current_draft_none(self, manager):
        """Test getting current draft when none exists"""
        current = manager.get_current_draft()
        assert current is None

    def test_list_drafts(self, manager):
        """Test listing all drafts"""
        manager.create_draft("Post 1", "text")
        manager.create_draft("Post 2", "poll")

        drafts = manager.list_drafts()
        assert len(drafts) == 2
        assert drafts[0]["name"] == "Post 1"
        assert drafts[1]["name"] == "Post 2"
        assert drafts[1]["is_current"] is True

    def test_switch_draft(self, manager):
        """Test switching to a different draft"""
        draft1 = manager.create_draft("Post 1", "text")
        manager.create_draft("Post 2", "poll")

        # Switch back to draft1
        success = manager.switch_draft(draft1.draft_id)
        assert success is True
        assert manager.current_draft_id == draft1.draft_id

    def test_switch_draft_invalid(self, manager):
        """Test switching to invalid draft"""
        success = manager.switch_draft("nonexistent")
        assert success is False

    def test_update_draft(self, manager):
        """Test updating a draft"""
        draft = manager.create_draft("My Post", "text", content={"text": "Hello"})

        success = manager.update_draft(
            draft.draft_id, content={"text": "Hello world"}, theme="personal_brand"
        )

        assert success is True
        updated_draft = manager.get_draft(draft.draft_id)
        assert updated_draft.content["text"] == "Hello world"
        assert updated_draft.theme == "personal_brand"

    def test_update_draft_not_found(self, manager):
        """Test updating non-existent draft"""
        success = manager.update_draft("nonexistent", content={"text": "Hello"})
        assert success is False

    def test_delete_draft(self, manager):
        """Test deleting a draft"""
        draft = manager.create_draft("My Post", "text")

        success = manager.delete_draft(draft.draft_id)
        assert success is True
        assert draft.draft_id not in manager.drafts

    def test_delete_draft_updates_current(self, manager):
        """Test deleting current draft updates current_draft_id"""
        draft1 = manager.create_draft("Post 1", "text")
        draft2 = manager.create_draft("Post 2", "poll")

        # Delete current draft
        manager.delete_draft(draft2.draft_id)
        assert manager.current_draft_id == draft1.draft_id

    def test_delete_draft_not_found(self, manager):
        """Test deleting non-existent draft"""
        success = manager.delete_draft("nonexistent")
        assert success is False

    def test_clear_all_drafts(self, manager):
        """Test clearing all drafts"""
        manager.create_draft("Post 1", "text")
        manager.create_draft("Post 2", "poll")
        manager.create_draft("Post 3", "document")

        count = manager.clear_all_drafts()
        assert count == 3
        assert len(manager.drafts) == 0
        assert manager.current_draft_id is None

    def test_export_draft(self, manager):
        """Test exporting draft as JSON"""
        draft = manager.create_draft(
            "My Post", "text", content={"text": "Hello"}, theme="thought_leader"
        )

        json_str = manager.export_draft(draft.draft_id)
        assert json_str is not None

        # Parse and verify
        data = json.loads(json_str)
        assert data["name"] == "My Post"
        assert data["theme"] == "thought_leader"

    def test_export_draft_not_found(self, manager):
        """Test exporting non-existent draft"""
        json_str = manager.export_draft("nonexistent")
        assert json_str is None

    def test_import_draft(self, manager):
        """Test importing draft from JSON"""
        draft_json = json.dumps(
            {
                "draft_id": "imported_1",
                "name": "Imported Post",
                "post_type": "text",
                "content": {"text": "Imported content"},
                "theme": "storyteller",
            }
        )

        draft = manager.import_draft(draft_json)
        assert draft is not None
        assert draft.name == "Imported Post"
        assert draft.theme == "storyteller"
        assert draft.draft_id in manager.drafts

    def test_import_draft_duplicate_id(self, manager):
        """Test importing draft with duplicate ID gets new ID"""
        draft1 = manager.create_draft("Post 1", "text")

        draft_json = json.dumps(
            {
                "draft_id": draft1.draft_id,  # Same ID
                "name": "Duplicate",
                "post_type": "text",
                "content": {"text": "Content"},
            }
        )

        draft2 = manager.import_draft(draft_json)
        assert draft2.draft_id != draft1.draft_id

    def test_import_draft_invalid_json(self, manager):
        """Test importing invalid JSON"""
        draft = manager.import_draft("invalid json{")
        assert draft is None

    def test_get_draft_preview(self, manager):
        """Test getting draft preview"""
        draft = manager.create_draft("My Post", "text", content={"commentary": "x" * 300})

        preview = manager.get_draft_preview(draft.draft_id, chars=210)
        assert len(preview) <= 213  # 210 + "..."

    def test_get_draft_preview_not_found(self, manager):
        """Test getting preview of non-existent draft"""
        preview = manager.get_draft_preview("nonexistent")
        assert preview is None

    def test_get_draft_stats(self, manager):
        """Test getting draft statistics"""
        draft = manager.create_draft(
            "My Post",
            "text",
            content={
                "commentary": "Hello world this is my post",
                "hook": "Attention grabber",
                "cta": "What do you think?",
                "hashtags": ["Marketing", "LinkedIn"],
            },
        )

        stats = manager.get_draft_stats(draft.draft_id)
        assert stats is not None
        assert stats["word_count"] > 0
        assert stats["char_count"] > 0
        assert stats["has_hook"] is True
        assert stats["has_cta"] is True
        assert stats["hashtag_count"] == 2

    def test_get_draft_stats_not_found(self, manager):
        """Test getting stats of non-existent draft"""
        stats = manager.get_draft_stats("nonexistent")
        assert stats is None

    def test_get_info(self, manager):
        """Test getting manager info"""
        manager.create_draft("Post 1", "text")
        manager.create_draft("Post 2", "poll")

        info = manager.get_info()
        assert info["total_drafts"] == 2
        assert info["current_draft_id"] is not None
        assert "text" in info["draft_types"]
        assert "poll" in info["draft_types"]

    def test_persistence(self, temp_storage):
        """Test drafts persist across manager instances"""
        # Create drafts with first manager
        manager1 = LinkedInManager(storage_path=temp_storage)
        draft1 = manager1.create_draft("Post 1", "text")
        draft2 = manager1.create_draft("Post 2", "poll")

        # Create new manager instance with same storage
        manager2 = LinkedInManager(storage_path=temp_storage)

        # Drafts should be loaded
        assert len(manager2.drafts) == 2
        assert draft1.draft_id in manager2.drafts
        assert draft2.draft_id in manager2.drafts

    def test_save_and_load_preserves_data(self, temp_storage):
        """Test save and load preserves all draft data"""
        manager1 = LinkedInManager(storage_path=temp_storage)
        draft = manager1.create_draft(
            "My Post",
            "text",
            content={"text": "Hello", "hook": "Stat"},
            theme="thought_leader",
            variant_config={"style": "insight"},
        )

        # Load in new manager
        manager2 = LinkedInManager(storage_path=temp_storage)
        loaded_draft = manager2.get_draft(draft.draft_id)

        assert loaded_draft.name == "My Post"
        assert loaded_draft.post_type == "text"
        assert loaded_draft.theme == "thought_leader"
        assert loaded_draft.content["text"] == "Hello"
        assert loaded_draft.variant_config["style"] == "insight"

    def test_update_draft_with_variant_config(self, manager):
        """Test updating draft with variant config"""
        draft = manager.create_draft("My Post", "text", variant_config={"style": "insight"})

        # Update variant config
        manager.update_draft(draft.draft_id, variant_config={"tone": "professional"})

        updated_draft = manager.get_draft(draft.draft_id)
        assert updated_draft.variant_config["style"] == "insight"
        assert updated_draft.variant_config["tone"] == "professional"

    def test_get_draft_preview_with_text_fallback(self, manager):
        """Test getting draft preview falls back to text field"""
        draft = manager.create_draft("My Post", "text", content={"text": "x" * 300})

        preview = manager.get_draft_preview(draft.draft_id, chars=210)
        assert len(preview) <= 213  # 210 + "..."

    def test_get_draft_preview_short_content(self, manager):
        """Test getting draft preview with short content"""
        draft = manager.create_draft("My Post", "text", content={"commentary": "Short"})

        preview = manager.get_draft_preview(draft.draft_id, chars=210)
        assert preview == "Short"

    def test_load_drafts_with_corrupted_file(self, temp_storage):
        """Test loading drafts skips corrupted files"""
        manager1 = LinkedInManager(storage_path=temp_storage)
        manager1.create_draft("Valid Post", "text")

        # Create a corrupted JSON file
        corrupted_file = Path(temp_storage) / "corrupted.json"
        with open(corrupted_file, "w") as f:
            f.write("invalid json{")

        # Load in new manager - should skip corrupted file
        manager2 = LinkedInManager(storage_path=temp_storage)
        assert len(manager2.drafts) == 1  # Only the valid draft loaded

    def test_generate_html_preview(self, manager):
        """Test generating HTML preview for a draft"""
        draft = manager.create_draft(
            "My Post",
            "text",
            content={"commentary": "Hello world", "hook": "Test", "cta": "Engage!"},
        )

        html_path = manager.generate_html_preview(draft.draft_id)
        assert html_path is not None
        assert Path(html_path).exists()
        assert Path(html_path).suffix == ".html"

    def test_generate_html_preview_custom_path(self, manager, temp_storage):
        """Test generating HTML preview with custom output path"""
        draft = manager.create_draft("My Post", "text", content={"commentary": "Test"})

        custom_path = str(Path(temp_storage) / "custom_preview.html")
        html_path = manager.generate_html_preview(draft.draft_id, output_path=custom_path)

        assert html_path == custom_path
        assert Path(html_path).exists()

    def test_generate_html_preview_not_found(self, manager):
        """Test generating HTML preview for non-existent draft"""
        html_path = manager.generate_html_preview("nonexistent")
        assert html_path is None

    def test_session_id_generation(self, temp_storage):
        """Test that manager generates a session ID"""
        manager = LinkedInManager(storage_path=temp_storage)
        assert manager.session_id is not None
        assert isinstance(manager.session_id, str)

    def test_custom_session_id(self, temp_storage):
        """Test manager with custom session ID"""
        manager = LinkedInManager(storage_path=temp_storage, session_id="custom_session")
        assert manager.session_id == "custom_session"

    def test_session_management(self, manager):
        """Test session get/set"""
        original_session = manager.get_session()
        assert original_session is not None

        # Set new session
        manager.set_session("new_session")
        assert manager.get_session() == "new_session"

    def test_lock_draft_to_session(self, manager):
        """Test locking draft to session"""
        draft = manager.create_draft("Test", "text")

        # Draft should be auto-locked to current session on creation
        assert manager.is_draft_accessible(draft.draft_id)

        # Lock to different session
        success = manager.lock_draft_to_session(draft.draft_id, "other_session")
        assert success is True

        # Should not be accessible from current session
        assert manager.is_draft_accessible(draft.draft_id) is False

        # But accessible from other session
        assert manager.is_draft_accessible(draft.draft_id, "other_session") is True

    def test_lock_nonexistent_draft(self, manager):
        """Test locking non-existent draft"""
        success = manager.lock_draft_to_session("nonexistent", "session")
        assert success is False

    def test_is_draft_accessible_unlocked(self, manager):
        """Test checking accessibility of unlocked draft"""
        draft = manager.create_draft("Test", "text")

        # Remove from session lock
        if draft.draft_id in manager.draft_sessions:
            del manager.draft_sessions[draft.draft_id]

        # Should be accessible to any session
        assert manager.is_draft_accessible(draft.draft_id) is True
        assert manager.is_draft_accessible(draft.draft_id, "any_session") is True

    def test_is_draft_accessible_nonexistent(self, manager):
        """Test checking accessibility of non-existent draft"""
        assert manager.is_draft_accessible("nonexistent") is False

    def test_list_drafts_session_filtering(self, temp_storage):
        """Test listing drafts with session filtering"""
        manager = LinkedInManager(storage_path=temp_storage, session_id="session1")

        # Create drafts in session 1
        _ = manager.create_draft("Draft 1", "text")
        _ = manager.create_draft("Draft 2", "text")

        # List drafts for session 1
        drafts = manager.list_drafts()
        assert len(drafts) == 2

        # List drafts for different session (should be empty)
        drafts_other = manager.list_drafts(session_id="session2")
        assert len(drafts_other) == 0

        # List all drafts
        all_drafts = manager.list_drafts(include_all=True)
        assert len(all_drafts) == 2

    def test_list_drafts_includes_session_metadata(self, manager):
        """Test draft list includes session metadata"""
        _ = manager.create_draft("Test", "text")

        drafts = manager.list_drafts()
        assert len(drafts) == 1

        draft_info = drafts[0]
        assert "session_id" in draft_info
        assert "is_locked" in draft_info
        assert draft_info["is_locked"] is True


class TestLinkedInManagerWithArtifacts:
    """Test LinkedInManager with artifact storage"""

    @pytest.mark.asyncio
    async def test_artifact_storage_initialization(self):
        """Test artifact storage initialization"""
        async with LinkedInManager(use_artifacts=True, artifact_provider="memory") as manager:
            assert manager.use_artifacts is True
            assert manager.artifact_provider == "memory"

    @pytest.mark.asyncio
    async def test_store_draft_as_artifact(self):
        """Test storing draft as artifact"""
        async with LinkedInManager(use_artifacts=True, artifact_provider="memory") as manager:
            draft = manager.create_draft(
                name="Test Draft", post_type="text", content={"commentary": "Test"}
            )

            artifact_id = await manager.store_draft_as_artifact(draft.draft_id)
            assert artifact_id is not None

    @pytest.mark.asyncio
    async def test_store_nonexistent_draft_as_artifact(self):
        """Test storing non-existent draft as artifact"""
        async with LinkedInManager(use_artifacts=True, artifact_provider="memory") as manager:
            artifact_id = await manager.store_draft_as_artifact("nonexistent")
            assert artifact_id is None

    @pytest.mark.asyncio
    async def test_retrieve_draft_from_artifact(self):
        """Test retrieving draft from artifact"""
        async with LinkedInManager(use_artifacts=True, artifact_provider="memory") as manager:
            # Create and store draft
            original = manager.create_draft(
                name="Test Draft", post_type="text", content={"commentary": "Test content"}
            )

            artifact_id = await manager.store_draft_as_artifact(original.draft_id)

            # Retrieve from artifact
            retrieved = await manager.retrieve_draft_from_artifact(artifact_id)
            assert retrieved is not None
            assert retrieved.name == "Test Draft"
            assert retrieved.content["commentary"] == "Test content"

    @pytest.mark.asyncio
    async def test_retrieve_nonexistent_artifact(self):
        """Test retrieving non-existent artifact"""
        async with LinkedInManager(use_artifacts=True, artifact_provider="memory") as manager:
            retrieved = await manager.retrieve_draft_from_artifact("nonexistent")
            assert retrieved is None

    @pytest.mark.asyncio
    async def test_artifact_storage_disabled(self):
        """Test that artifact storage is disabled by default"""
        manager = LinkedInManager(use_artifacts=False)
        assert manager.use_artifacts is False

        # Store should return None when artifacts disabled
        draft = manager.create_draft("Test", "text")
        artifact_id = await manager.store_draft_as_artifact(draft.draft_id)
        assert artifact_id is None
