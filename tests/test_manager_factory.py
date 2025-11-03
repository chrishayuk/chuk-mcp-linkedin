"""Tests for manager factory module."""

import pytest

from chuk_mcp_linkedin.manager import LinkedInManager
from chuk_mcp_linkedin.manager_factory import (
    ManagerFactory,
    get_current_manager,
    get_factory,
    get_manager_for_user,
    set_factory,
)


class TestManagerFactory:
    """Test ManagerFactory class"""

    def test_factory_initialization_defaults(self):
        """Test factory initializes with defaults"""
        factory = ManagerFactory()
        assert factory.use_artifacts is True
        assert factory.artifact_provider == "memory"
        assert len(factory._managers) == 0

    def test_factory_initialization_custom(self):
        """Test factory initializes with custom settings"""
        factory = ManagerFactory(use_artifacts=False, artifact_provider="filesystem")
        assert factory.use_artifacts is False
        assert factory.artifact_provider == "filesystem"

    def test_get_manager_creates_new(self):
        """Test get_manager creates new manager for user"""
        factory = ManagerFactory()

        # Get manager for user1
        manager1 = factory.get_manager("user1")

        assert manager1 is not None
        assert isinstance(manager1, LinkedInManager)
        assert manager1.user_id == "user1"
        assert "user1" in factory._managers

    def test_get_manager_returns_cached(self):
        """Test get_manager returns cached manager"""
        factory = ManagerFactory()

        # Get manager twice for same user
        manager1 = factory.get_manager("user1")
        manager2 = factory.get_manager("user1")

        # Should be same instance
        assert manager1 is manager2
        assert id(manager1) == id(manager2)

    def test_get_manager_different_users(self):
        """Test get_manager creates separate managers for different users"""
        factory = ManagerFactory()

        # Get managers for different users
        manager1 = factory.get_manager("user1")
        manager2 = factory.get_manager("user2")

        # Should be different instances
        assert manager1 is not manager2
        assert manager1.user_id == "user1"
        assert manager2.user_id == "user2"

    def test_get_manager_uses_artifact_settings(self):
        """Test get_manager uses factory's artifact settings"""
        factory = ManagerFactory(use_artifacts=True, artifact_provider="s3")

        manager = factory.get_manager("test_user")

        assert manager.use_artifacts is True
        assert manager.artifact_provider == "s3"

    def test_clear_manager_success(self):
        """Test clear_manager removes manager from cache"""
        factory = ManagerFactory()

        # Create manager
        factory.get_manager("user1")
        assert "user1" in factory._managers

        # Clear manager
        result = factory.clear_manager("user1")

        assert result is True
        assert "user1" not in factory._managers

    def test_clear_manager_not_found(self):
        """Test clear_manager returns False for non-existent user"""
        factory = ManagerFactory()

        result = factory.clear_manager("nonexistent")

        assert result is False

    def test_clear_manager_doesnt_affect_others(self):
        """Test clearing one manager doesn't affect others"""
        factory = ManagerFactory()

        # Create multiple managers
        factory.get_manager("user1")
        manager2 = factory.get_manager("user2")

        # Clear user1
        factory.clear_manager("user1")

        # user2 should still be there
        assert "user1" not in factory._managers
        assert "user2" in factory._managers
        assert factory.get_manager("user2") is manager2

    def test_get_active_users_empty(self):
        """Test get_active_users returns empty list when no managers"""
        factory = ManagerFactory()

        users = factory.get_active_users()

        assert users == []

    def test_get_active_users_with_managers(self):
        """Test get_active_users returns list of user IDs"""
        factory = ManagerFactory()

        # Create managers for multiple users
        factory.get_manager("user1")
        factory.get_manager("user2")
        factory.get_manager("user3")

        users = factory.get_active_users()

        assert len(users) == 3
        assert "user1" in users
        assert "user2" in users
        assert "user3" in users

    def test_get_active_users_after_clear(self):
        """Test get_active_users updates after clearing manager"""
        factory = ManagerFactory()

        # Create managers
        factory.get_manager("user1")
        factory.get_manager("user2")

        # Clear one
        factory.clear_manager("user1")

        users = factory.get_active_users()

        assert len(users) == 1
        assert "user1" not in users
        assert "user2" in users

    def test_thread_safety(self):
        """Test factory is thread-safe with lock"""
        factory = ManagerFactory()

        # The lock should exist
        assert hasattr(factory, "_lock")
        assert factory._lock is not None

        # Verify lock is a threading lock type
        assert type(factory._lock).__name__ == "lock"

        # Test that we can use the factory (lock is used internally)
        manager = factory.get_manager("test_user")
        assert manager is not None


class TestGlobalFactory:
    """Test global factory functions"""

    def test_get_factory_creates_default(self):
        """Test get_factory creates default factory if not set"""
        # Reset global factory
        from chuk_mcp_linkedin import manager_factory

        manager_factory._global_factory = None

        # Get factory
        factory = get_factory()

        assert factory is not None
        assert isinstance(factory, ManagerFactory)
        assert factory.use_artifacts is True
        assert factory.artifact_provider == "memory"

    def test_set_and_get_factory(self):
        """Test set_factory and get_factory work together"""
        # Create custom factory
        custom_factory = ManagerFactory(use_artifacts=False, artifact_provider="filesystem")

        # Set it
        set_factory(custom_factory)

        # Get it back
        retrieved_factory = get_factory()

        assert retrieved_factory is custom_factory

    def test_get_factory_returns_same_instance(self):
        """Test get_factory returns same instance on multiple calls"""
        factory1 = get_factory()
        factory2 = get_factory()

        assert factory1 is factory2


class TestGetManagerForUser:
    """Test get_manager_for_user function"""

    def test_get_manager_for_user_with_user_id(self):
        """Test get_manager_for_user with explicit user_id"""
        # Set up factory
        factory = ManagerFactory()
        set_factory(factory)

        # Get manager with explicit user_id
        manager = get_manager_for_user(user_id="explicit_user")

        assert manager is not None
        assert manager.user_id == "explicit_user"

    def test_get_manager_for_user_from_context(self):
        """Test get_manager_for_user gets user_id from context"""
        from chuk_mcp_server import set_user_id
        from chuk_mcp_server.context import clear_all

        # Set up factory
        factory = ManagerFactory()
        set_factory(factory)

        # Set user in context
        set_user_id("context_user")

        try:
            # Get manager without explicit user_id
            manager = get_manager_for_user()

            assert manager is not None
            assert manager.user_id == "context_user"
        finally:
            # Clean up context
            clear_all()

    def test_get_manager_for_user_raises_when_no_user(self):
        """Test get_manager_for_user raises when no user_id"""
        from chuk_mcp_server.context import clear_all

        # Set up factory
        factory = ManagerFactory()
        set_factory(factory)

        # Clear any existing context
        clear_all()

        try:
            # Should raise PermissionError when no user is set
            with pytest.raises(PermissionError):
                get_manager_for_user()
        finally:
            # Clean up context
            clear_all()

    def test_get_manager_for_user_raises_on_permission_error(self):
        """Test get_manager_for_user handles PermissionError from context"""
        from chuk_mcp_server.context import clear_all

        # Set up factory
        factory = ManagerFactory()
        set_factory(factory)

        # Clear context to simulate no authentication
        clear_all()

        try:
            # Should propagate PermissionError
            with pytest.raises(PermissionError, match="User authentication required"):
                get_manager_for_user()
        finally:
            # Clean up context
            clear_all()


class TestGetCurrentManager:
    """Test get_current_manager function"""

    def test_get_current_manager_success(self):
        """Test get_current_manager gets manager from context"""
        from chuk_mcp_server import set_user_id
        from chuk_mcp_server.context import clear_all

        # Set up factory
        factory = ManagerFactory()
        set_factory(factory)

        # Set user in context
        set_user_id("current_user")

        try:
            # Get current manager
            manager = get_current_manager()

            assert manager is not None
            assert manager.user_id == "current_user"
        finally:
            # Clean up context
            clear_all()

    def test_get_current_manager_raises_when_not_authenticated(self):
        """Test get_current_manager raises when not authenticated"""
        from chuk_mcp_server.context import clear_all

        # Set up factory
        factory = ManagerFactory()
        set_factory(factory)

        # Clear context to simulate no authentication
        clear_all()

        try:
            # Should propagate PermissionError
            with pytest.raises(PermissionError, match="User authentication required"):
                get_current_manager()
        finally:
            # Clean up context
            clear_all()


class TestManagerIsolation:
    """Test that managers are properly isolated per user"""

    def test_managers_have_separate_state(self):
        """Test that different user managers have separate state"""
        factory = ManagerFactory()

        # Use unique user IDs to avoid test interference
        # Get managers for different users and clear any existing drafts
        manager1 = factory.get_manager("isolation_user1")
        manager1.clear_all_drafts()  # Clean up any previous test artifacts

        manager2 = factory.get_manager("isolation_user2")
        manager2.clear_all_drafts()  # Clean up any previous test artifacts

        # Create draft in manager1
        draft1 = manager1.create_draft("User 1 Draft", "text")

        # manager2 should not see manager1's drafts
        assert len(manager1.drafts) == 1
        assert len(manager2.drafts) == 0

        # Create draft in manager2
        draft2 = manager2.create_draft("User 2 Draft", "text")

        # Each should only see their own
        assert len(manager1.drafts) == 1
        assert len(manager2.drafts) == 1
        assert draft1.draft_id in manager1.drafts
        assert draft2.draft_id in manager2.drafts
        assert draft1.draft_id not in manager2.drafts
        assert draft2.draft_id not in manager1.drafts

    def test_same_user_gets_same_manager(self):
        """Test that same user always gets same manager instance"""
        factory = ManagerFactory()

        # Use unique user ID to avoid test interference
        # Get manager and clear any existing drafts
        manager1 = factory.get_manager("user_same_test")
        manager1.clear_all_drafts()  # Clean up any previous test artifacts

        # Create a draft
        draft = manager1.create_draft("Test Draft", "text")

        # Get manager again for same user
        manager2 = factory.get_manager("user_same_test")

        # Should be same instance with same state
        assert manager1 is manager2
        assert len(manager2.drafts) == 1
        assert draft.draft_id in manager2.drafts


class TestFactoryConfiguration:
    """Test factory configuration options"""

    def test_memory_provider(self):
        """Test factory with memory artifact provider"""
        factory = ManagerFactory(use_artifacts=True, artifact_provider="memory")

        manager = factory.get_manager("test_user")

        assert manager.use_artifacts is True
        assert manager.artifact_provider == "memory"

    def test_filesystem_provider(self):
        """Test factory with filesystem artifact provider"""
        factory = ManagerFactory(use_artifacts=True, artifact_provider="filesystem")

        manager = factory.get_manager("test_user")

        assert manager.use_artifacts is True
        assert manager.artifact_provider == "filesystem"

    def test_s3_provider(self):
        """Test factory with S3 artifact provider"""
        factory = ManagerFactory(use_artifacts=True, artifact_provider="s3")

        manager = factory.get_manager("test_user")

        assert manager.use_artifacts is True
        assert manager.artifact_provider == "s3"

    def test_artifacts_disabled(self):
        """Test factory with artifacts disabled"""
        factory = ManagerFactory(use_artifacts=False)

        manager = factory.get_manager("test_user")

        assert manager.use_artifacts is False


class TestErrorHandling:
    """Test error handling"""

    def test_get_manager_with_empty_user_id(self):
        """Test get_manager with empty string user_id"""
        factory = ManagerFactory()

        # Empty string becomes "anonymous" in LinkedInManager
        manager = factory.get_manager("")

        assert manager is not None
        assert manager.user_id == "anonymous"

    def test_get_manager_with_special_characters(self):
        """Test get_manager with special characters in user_id"""
        factory = ManagerFactory()

        # Special characters should work
        manager = factory.get_manager("user@example.com")

        assert manager is not None
        assert manager.user_id == "user@example.com"

    def test_clear_manager_multiple_times(self):
        """Test clearing same manager multiple times"""
        factory = ManagerFactory()

        # Create manager
        factory.get_manager("user1")

        # Clear first time
        result1 = factory.clear_manager("user1")
        assert result1 is True

        # Clear second time
        result2 = factory.clear_manager("user1")
        assert result2 is False  # Already cleared
