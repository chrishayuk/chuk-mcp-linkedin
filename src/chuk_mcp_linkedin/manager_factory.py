"""
Manager factory for creating user-scoped LinkedIn manager instances.

Provides:
- Per-user manager instances with automatic isolation
- Artifact-based storage by default (no local filesystem)
- Automatic cleanup on token expiry
- Thread-safe manager caching

Usage:
    # In tools - context is automatically set by protocol handler
    from chuk_mcp_linkedin.manager_factory import get_current_manager

    @mcp.tool
    @requires_auth()
    async def my_tool():
        manager = get_current_manager()  # Gets manager for authenticated user
        ...
"""

from typing import Dict, Optional
import threading
from .manager import LinkedInManager


class ManagerFactory:
    """
    Factory for creating and caching per-user LinkedInManager instances.

    Each user (identified by user_id from OAuth) gets their own manager instance
    with isolated storage. Managers are cached for performance.

    Security:
    - Each user_id gets a separate manager instance
    - All artifacts are scoped to user_id
    - No cross-user access possible
    - Managers are session-independent (same user, different sessions = same manager)
    """

    def __init__(
        self,
        use_artifacts: bool = True,
        artifact_provider: str = "memory",
    ):
        """
        Initialize the manager factory.

        Args:
            use_artifacts: Whether to use chuk-artifacts for storage (default: True)
            artifact_provider: Storage provider (memory, filesystem, s3, ibm-cos)
        """
        self.use_artifacts = use_artifacts
        self.artifact_provider = artifact_provider

        # Cache of managers keyed by user_id
        self._managers: Dict[str, LinkedInManager] = {}
        self._lock = threading.Lock()

    def get_manager(self, user_id: str) -> LinkedInManager:
        """
        Get or create a manager instance for the given user.

        Args:
            user_id: User identifier from OAuth

        Returns:
            LinkedInManager instance scoped to this user
        """
        with self._lock:
            if user_id not in self._managers:
                # Create new manager for this user
                self._managers[user_id] = LinkedInManager(
                    user_id=user_id,
                    use_artifacts=self.use_artifacts,
                    artifact_provider=self.artifact_provider,
                )

            return self._managers[user_id]

    def clear_manager(self, user_id: str) -> bool:
        """
        Remove a manager from the cache (e.g., on token expiry).

        Args:
            user_id: User identifier

        Returns:
            True if manager was removed, False if not found
        """
        with self._lock:
            if user_id in self._managers:
                del self._managers[user_id]
                return True
            return False

    def get_active_users(self) -> list[str]:
        """
        Get list of active user_ids with cached managers.

        Returns:
            List of user_ids
        """
        with self._lock:
            return list(self._managers.keys())


# Global factory instance (configured in async_server.py)
_global_factory: Optional[ManagerFactory] = None


def get_factory() -> ManagerFactory:
    """Get the global manager factory instance."""
    global _global_factory
    if _global_factory is None:
        # Create default factory if not configured
        _global_factory = ManagerFactory()
    return _global_factory


def set_factory(factory: ManagerFactory) -> None:
    """Set the global manager factory instance."""
    global _global_factory
    _global_factory = factory


def get_manager_for_user(user_id: Optional[str] = None) -> LinkedInManager:
    """
    Convenience function to get a manager for a user.

    Args:
        user_id: User identifier from OAuth. If None, gets from auth context.

    Returns:
        LinkedInManager instance scoped to this user

    Raises:
        ValueError: If user_id is None and not in context
        PermissionError: If not authenticated
    """
    # If user_id not provided, get from context
    if user_id is None:
        from chuk_mcp_server.context import require_user_id

        user_id = require_user_id()

    if not user_id:
        raise ValueError(
            "user_id is required for manager access. "
            "Ensure @requires_auth() decorator is applied to the tool."
        )

    factory = get_factory()
    return factory.get_manager(user_id)


def get_current_manager() -> LinkedInManager:
    """
    Get manager for the current authenticated user.

    Uses auth context to determine the current user.

    Returns:
        LinkedInManager instance scoped to current user

    Raises:
        PermissionError: If no user is authenticated
    """
    return get_manager_for_user()
