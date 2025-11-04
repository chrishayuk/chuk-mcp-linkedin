"""
Artifact-based preview system using chuk-artifacts.

Provides session-isolated, secure preview URLs with automatic cleanup.
"""

import os
import uuid
from typing import Any, List, Optional

from chuk_artifacts import ArtifactStore
from chuk_artifacts.config import configure_filesystem, configure_memory, configure_s3


class ArtifactPreviewManager:
    """
    Manages draft previews using chuk-artifacts for session-based storage.

    Features:
    - Session-isolated previews (each session only sees their own drafts)
    - Automatic cleanup of expired artifacts
    - Presigned URLs for secure access
    - Grid architecture: grid/{sandbox_id}/{session_id}/{artifact_id}
    """

    def __init__(self, provider: str = "memory", sandbox_id: str = "linkedin-mcp"):
        """
        Initialize artifact preview manager.

        Args:
            provider: Storage provider (memory, filesystem, s3, ibm-cos)
            sandbox_id: Sandbox identifier for grid isolation
        """
        self.provider = provider
        self.sandbox_id = sandbox_id
        self._store: Optional[ArtifactStore] = None
        self._current_session: Optional[str] = None

    async def __aenter__(self) -> "ArtifactPreviewManager":
        """Async context manager entry."""
        # Configure provider
        if self.provider == "memory":
            configure_memory()
        elif self.provider == "filesystem":
            configure_filesystem(root=f".artifacts/{self.sandbox_id}")
        elif self.provider in ("s3", "ibm-cos"):
            # Map Fly.io environment variables to chuk-artifacts expected names
            # Fly sets AWS_ENDPOINT_URL_S3, but chuk-artifacts expects S3_ENDPOINT_URL
            if "AWS_ENDPOINT_URL_S3" in os.environ and "S3_ENDPOINT_URL" not in os.environ:
                os.environ["S3_ENDPOINT_URL"] = os.environ["AWS_ENDPOINT_URL_S3"]

            # Configure S3 using environment variables
            configure_s3(
                access_key=os.environ.get("AWS_ACCESS_KEY_ID", ""),
                secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
                bucket=os.environ.get("ARTIFACT_BUCKET", ""),
                endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
                region=os.environ.get("AWS_REGION", "auto"),
            )

        self._store = ArtifactStore()
        await self._store.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self._store:
            await self._store.__aexit__(exc_type, exc_val, exc_tb)

    def create_session(self, user_id: Optional[str] = None) -> str:
        """
        Create a new session for a user.

        Args:
            user_id: Optional user identifier (generates UUID if not provided)

        Returns:
            Session ID
        """
        if not user_id:
            user_id = str(uuid.uuid4())

        session_id = f"user_{user_id}"
        self._current_session = session_id
        return session_id

    def set_session(self, session_id: str) -> None:
        """
        Set the current session.

        Args:
            session_id: Session ID to use
        """
        self._current_session = session_id

    def get_session(self) -> Optional[str]:
        """
        Get the current session ID.

        Returns:
            Current session ID or None
        """
        return self._current_session

    async def store_preview(
        self, html_content: str, draft_id: str, draft_name: str, session_id: Optional[str] = None
    ) -> str:
        """
        Store a draft preview as an artifact.

        Args:
            html_content: HTML preview content
            draft_id: Draft ID
            draft_name: Draft name for metadata
            session_id: Optional session ID (uses current if not provided)

        Returns:
            Artifact ID
        """
        if not self._store:
            raise RuntimeError("ArtifactStore not initialized. Use 'async with' context.")

        # Use provided session or current session
        session = session_id or self._current_session
        if not session:
            raise ValueError("No session ID provided or set")

        # Store HTML as artifact
        artifact_id_result: str = await self._store.store(
            data=html_content.encode("utf-8"),
            mime="text/html",
            summary=f"LinkedIn Post Preview: {draft_name}",
            filename=f"{draft_id}_preview.html",
            user_id=session,
            meta={
                "draft_id": draft_id,
                "draft_name": draft_name,
                "type": "preview",
                "sandbox_id": self.sandbox_id,
            },
        )

        return artifact_id_result

    async def get_preview(
        self, artifact_id: str, session_id: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Retrieve a preview artifact.

        Args:
            artifact_id: Artifact ID to retrieve
            session_id: Optional session ID (uses current if not provided)

        Returns:
            HTML content as bytes, or None if not found or access denied
        """
        if not self._store:
            raise RuntimeError("ArtifactStore not initialized. Use 'async with' context.")

        try:
            # Retrieve enforces session isolation automatically
            content_result: bytes | None = await self._store.retrieve(artifact_id)
            return content_result
        except Exception:
            # Access denied or not found
            return None

    async def get_preview_url(
        self, artifact_id: str, session_id: Optional[str] = None, expires_in: int = 3600
    ) -> Optional[str]:
        """
        Get a presigned URL for a preview.

        Args:
            artifact_id: Artifact ID
            session_id: Optional session ID (uses current if not provided)
            expires_in: URL expiration in seconds (default: 1 hour)

        Returns:
            Presigned URL or None if not available
        """
        if not self._store:
            raise RuntimeError("ArtifactStore not initialized. Use 'async with' context.")

        try:
            # Generate presigned URL (duration-based)
            url_result: str | None = await self._store.presign_short(
                artifact_id, expires_in=expires_in
            )
            return url_result
        except Exception:
            # Not supported by provider or access denied
            return None

    async def list_previews(self, session_id: Optional[str] = None) -> List[Any]:
        """
        List all previews for a session.

        Args:
            session_id: Optional session ID (uses current if not provided)

        Returns:
            List of artifact metadata dictionaries
        """
        if not self._store:
            raise RuntimeError("ArtifactStore not initialized. Use 'async with' context.")

        session = session_id or self._current_session
        if not session:
            raise ValueError("No session ID provided or set")

        # List artifacts for session
        artifacts = await self._store.list_by_session(session)

        # Filter for preview artifacts (if metadata is available)
        previews = [
            artifact for artifact in artifacts if artifact.get("meta", {}).get("type") == "preview"
        ]

        return previews

    async def delete_preview(self, artifact_id: str, session_id: Optional[str] = None) -> bool:
        """
        Delete a preview artifact.

        Args:
            artifact_id: Artifact ID to delete
            session_id: Optional session ID (uses current if not provided)

        Returns:
            True if deleted, False if not found or access denied
        """
        if not self._store:
            raise RuntimeError("ArtifactStore not initialized. Use 'async with' context.")

        try:
            await self._store.delete(artifact_id)
            return True
        except Exception:
            return False


# Global artifact preview manager instance
_artifact_manager: Optional[ArtifactPreviewManager] = None


async def get_artifact_manager(
    provider: str = "memory", sandbox_id: str = "linkedin-mcp"
) -> ArtifactPreviewManager:
    """
    Get or create the global artifact preview manager.

    Args:
        provider: Storage provider (memory, filesystem, s3, ibm-cos)
        sandbox_id: Sandbox identifier

    Returns:
        ArtifactPreviewManager instance
    """
    global _artifact_manager

    if _artifact_manager is None:
        _artifact_manager = ArtifactPreviewManager(provider=provider, sandbox_id=sandbox_id)
        # Initialize the store
        await _artifact_manager.__aenter__()

    return _artifact_manager
