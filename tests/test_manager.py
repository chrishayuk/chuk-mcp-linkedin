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
