"""
Draft management system for LinkedIn posts.

Handles CRUD operations for draft posts with session-based locking.
Integrates with chuk-artifacts for session-isolated storage.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uuid
from pathlib import Path

from chuk_artifacts import ArtifactStore
from chuk_artifacts.config import configure_memory, configure_filesystem


class Draft:
    """Represents a LinkedIn post draft"""

    def __init__(
        self,
        draft_id: str,
        name: str,
        post_type: str,
        content: Dict[str, Any],
        theme: Optional[str] = None,
        variant_config: Optional[Dict[str, Any]] = None,
    ):
        self.draft_id = draft_id
        self.name = name
        self.post_type = post_type
        self.content = content
        self.theme = theme
        self.variant_config = variant_config or {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.metadata: Dict[str, Any] = {}

    def update_content(self, content: Dict[str, Any]):
        """Update draft content"""
        self.content.update(content)
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert draft to dictionary"""
        return {
            "draft_id": self.draft_id,
            "name": self.name,
            "post_type": self.post_type,
            "content": self.content,
            "theme": self.theme,
            "variant_config": self.variant_config,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Draft":
        """Create draft from dictionary"""
        draft = cls(
            draft_id=data["draft_id"],
            name=data["name"],
            post_type=data["post_type"],
            content=data["content"],
            theme=data.get("theme"),
            variant_config=data.get("variant_config", {}),
        )
        draft.created_at = data.get("created_at", draft.created_at)
        draft.updated_at = data.get("updated_at", draft.updated_at)
        draft.metadata = data.get("metadata", {})
        return draft


class LinkedInManager:
    """Manager for LinkedIn post drafts with session-based locking"""

    def __init__(
        self,
        storage_path: Optional[str] = None,
        session_id: Optional[str] = None,
        use_artifacts: bool = False,
        artifact_provider: str = "memory",
    ):
        """
        Initialize manager with optional storage path and session ID.

        Args:
            storage_path: Path to store drafts (defaults to .linkedin_drafts)
            session_id: Optional session ID for session-based locking
            use_artifacts: Whether to use chuk-artifacts for storage (default: False)
            artifact_provider: Storage provider if using artifacts (memory, filesystem, s3, ibm-cos)
        """
        self.storage_path = Path(storage_path or ".linkedin_drafts")
        self.storage_path.mkdir(exist_ok=True)

        self.drafts: Dict[str, Draft] = {}
        self.current_draft_id: Optional[str] = None

        # Session management
        self.session_id = session_id or str(uuid.uuid4())
        self.draft_sessions: Dict[str, str] = {}  # draft_id -> session_id mapping

        # Artifact storage
        self.use_artifacts = use_artifacts
        self.artifact_provider = artifact_provider
        self._artifact_store: Optional[ArtifactStore] = None
        self._artifact_initialized = False

        # Load existing drafts
        self._load_drafts()

    async def __aenter__(self):
        """Async context manager entry."""
        if self.use_artifacts and not self._artifact_initialized:
            # Configure provider
            if self.artifact_provider == "memory":
                configure_memory()
            elif self.artifact_provider == "filesystem":
                configure_filesystem(root=".artifacts/linkedin-drafts")
            elif self.artifact_provider in ("s3", "ibm-cos"):
                # S3 configuration should be done via environment variables
                pass

            self._artifact_store = ArtifactStore()
            await self._artifact_store.__aenter__()
            self._artifact_initialized = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._artifact_store:
            await self._artifact_store.__aexit__(exc_type, exc_val, exc_tb)
            self._artifact_initialized = False

    async def _ensure_artifact_store(self):
        """Ensure artifact store is initialized."""
        if self.use_artifacts and not self._artifact_initialized:
            # Configure provider
            if self.artifact_provider == "memory":
                configure_memory()
            elif self.artifact_provider == "filesystem":
                configure_filesystem(root=".artifacts/linkedin-drafts")
            elif self.artifact_provider in ("s3", "ibm-cos"):
                # S3 configuration should be done via environment variables
                pass

            self._artifact_store = ArtifactStore()
            await self._artifact_store.__aenter__()
            self._artifact_initialized = True

    async def store_draft_as_artifact(self, draft_id: str) -> Optional[str]:
        """
        Store a draft as an artifact.

        Args:
            draft_id: Draft ID to store

        Returns:
            Artifact ID or None if not using artifacts or draft not found
        """
        if not self.use_artifacts:
            return None

        draft = self.get_draft(draft_id)
        if not draft:
            return None

        await self._ensure_artifact_store()

        # Serialize draft to JSON
        draft_json = json.dumps(draft.to_dict(), indent=2)

        # Store as artifact
        artifact_id = await self._artifact_store.store(
            data=draft_json.encode("utf-8"),
            mime="application/json",
            summary=f"LinkedIn Draft: {draft.name}",
            filename=f"{draft_id}.json",
            user_id=self.session_id,
            meta={
                "draft_id": draft_id,
                "draft_name": draft.name,
                "post_type": draft.post_type,
                "type": "draft",
            },
        )

        return artifact_id

    async def retrieve_draft_from_artifact(self, artifact_id: str) -> Optional[Draft]:
        """
        Retrieve a draft from an artifact.

        Args:
            artifact_id: Artifact ID to retrieve

        Returns:
            Draft object or None if not found
        """
        if not self.use_artifacts:
            return None

        await self._ensure_artifact_store()

        try:
            # Retrieve artifact
            data = await self._artifact_store.retrieve(artifact_id)
            if not data:
                return None

            # Deserialize draft
            draft_data = json.loads(data.decode("utf-8"))
            draft = Draft.from_dict(draft_data)

            return draft
        except Exception:
            return None

    def set_session(self, session_id: str):
        """
        Set the current session ID.

        Args:
            session_id: Session ID to use
        """
        self.session_id = session_id

    def get_session(self) -> str:
        """
        Get the current session ID.

        Returns:
            Current session ID
        """
        return self.session_id

    def lock_draft_to_session(self, draft_id: str, session_id: Optional[str] = None) -> bool:
        """
        Lock a draft to a specific session.

        Args:
            draft_id: Draft ID to lock
            session_id: Session ID to lock to (uses current if not provided)

        Returns:
            True if locked, False if draft not found
        """
        if draft_id not in self.drafts:
            return False

        session = session_id or self.session_id
        self.draft_sessions[draft_id] = session
        return True

    def is_draft_accessible(self, draft_id: str, session_id: Optional[str] = None) -> bool:
        """
        Check if a draft is accessible by the current session.

        Args:
            draft_id: Draft ID to check
            session_id: Session ID to check (uses current if not provided)

        Returns:
            True if accessible, False otherwise
        """
        if draft_id not in self.drafts:
            return False

        # If draft not locked to any session, it's accessible
        if draft_id not in self.draft_sessions:
            return True

        # Check if session matches
        session = session_id or self.session_id
        return self.draft_sessions[draft_id] == session

    def create_draft(
        self,
        name: str,
        post_type: str,
        content: Optional[Dict[str, Any]] = None,
        theme: Optional[str] = None,
        variant_config: Optional[Dict[str, Any]] = None,
    ) -> Draft:
        """Create a new draft and lock it to the current session"""
        draft_id = f"draft_{len(self.drafts) + 1}_{datetime.now().timestamp()}"

        draft = Draft(
            draft_id=draft_id,
            name=name,
            post_type=post_type,
            content=content or {},
            theme=theme,
            variant_config=variant_config,
        )

        self.drafts[draft_id] = draft
        self.current_draft_id = draft_id

        # Lock draft to current session
        self.lock_draft_to_session(draft_id)

        self._save_draft(draft)

        return draft

    def get_draft(self, draft_id: str) -> Optional[Draft]:
        """Get a draft by ID"""
        return self.drafts.get(draft_id)

    def get_current_draft(self) -> Optional[Draft]:
        """Get the currently active draft"""
        if self.current_draft_id:
            return self.drafts.get(self.current_draft_id)
        return None

    def list_drafts(
        self, session_id: Optional[str] = None, include_all: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List drafts accessible by the current session.

        Args:
            session_id: Optional session ID (uses current if not provided)
            include_all: If True, include all drafts regardless of session (default: False)

        Returns:
            List of draft metadata dictionaries
        """
        session = session_id or self.session_id

        drafts_list = []
        for draft in self.drafts.values():
            # Skip if not accessible and not including all
            if not include_all and not self.is_draft_accessible(draft.draft_id, session):
                continue

            drafts_list.append(
                {
                    "draft_id": draft.draft_id,
                    "name": draft.name,
                    "post_type": draft.post_type,
                    "theme": draft.theme,
                    "created_at": draft.created_at,
                    "updated_at": draft.updated_at,
                    "is_current": draft.draft_id == self.current_draft_id,
                    "session_id": self.draft_sessions.get(draft.draft_id),
                    "is_locked": draft.draft_id in self.draft_sessions,
                }
            )

        return drafts_list

    def switch_draft(self, draft_id: str) -> bool:
        """Switch to a different draft"""
        if draft_id in self.drafts:
            self.current_draft_id = draft_id
            return True
        return False

    def update_draft(
        self,
        draft_id: str,
        content: Optional[Dict[str, Any]] = None,
        theme: Optional[str] = None,
        variant_config: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update a draft"""
        draft = self.get_draft(draft_id)
        if not draft:
            return False

        if content:
            draft.update_content(content)
        if theme:
            draft.theme = theme
        if variant_config:
            draft.variant_config.update(variant_config)

        draft.updated_at = datetime.now().isoformat()

        self._save_draft(draft)

        return True

    def delete_draft(self, draft_id: str) -> bool:
        """Delete a draft"""
        if draft_id in self.drafts:
            self.drafts.pop(draft_id)

            # Delete from storage
            draft_file = self.storage_path / f"{draft_id}.json"
            if draft_file.exists():
                draft_file.unlink()

            # Update current draft if needed
            if self.current_draft_id == draft_id:
                self.current_draft_id = next(iter(self.drafts.keys()), None)

            return True
        return False

    def clear_all_drafts(self) -> int:
        """Clear all drafts"""
        count = len(self.drafts)

        # Delete all files
        for draft_file in self.storage_path.glob("*.json"):
            draft_file.unlink()

        self.drafts.clear()
        self.current_draft_id = None

        return count

    def export_draft(self, draft_id: str) -> Optional[str]:
        """Export draft as JSON string"""
        draft = self.get_draft(draft_id)
        if draft:
            return json.dumps(draft.to_dict(), indent=2)
        return None

    def import_draft(self, draft_json: str) -> Optional[Draft]:
        """Import draft from JSON string"""
        try:
            data = json.loads(draft_json)
            draft = Draft.from_dict(data)

            # Ensure unique ID
            if draft.draft_id in self.drafts:
                draft.draft_id = f"{draft.draft_id}_{datetime.now().timestamp()}"

            self.drafts[draft.draft_id] = draft
            self._save_draft(draft)

            return draft
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error importing draft: {e}")
            return None

    def get_draft_preview(self, draft_id: str, chars: int = 210) -> Optional[str]:
        """Get preview of a draft (first N characters)"""
        draft = self.get_draft(draft_id)
        if not draft:
            return None

        # Try to get commentary from content
        commentary = draft.content.get("commentary", "")
        if not commentary:
            commentary = draft.content.get("text", "")

        if len(commentary) <= chars:
            return commentary

        return commentary[:chars] + "..."

    def get_draft_stats(self, draft_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics about a draft"""
        draft = self.get_draft(draft_id)
        if not draft:
            return None

        commentary = draft.content.get("commentary", "")
        word_count = len(commentary.split())
        char_count = len(commentary)

        return {
            "draft_id": draft.draft_id,
            "word_count": word_count,
            "char_count": char_count,
            "char_remaining": 3000 - char_count,
            "preview_visible": min(210, char_count),
            "has_hook": draft.content.get("hook") is not None,
            "has_cta": draft.content.get("cta") is not None,
            "hashtag_count": len(draft.content.get("hashtags", [])),
        }

    def _save_draft(self, draft: Draft):
        """Save draft to storage"""
        draft_file = self.storage_path / f"{draft.draft_id}.json"
        with open(draft_file, "w") as f:
            json.dump(draft.to_dict(), f, indent=2)

    def _load_drafts(self):
        """Load drafts from storage"""
        for draft_file in self.storage_path.glob("*.json"):
            try:
                with open(draft_file, "r") as f:
                    data = json.load(f)
                    draft = Draft.from_dict(data)
                    self.drafts[draft.draft_id] = draft
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading draft {draft_file}: {e}")

        # Set first draft as current if none set
        if self.drafts and not self.current_draft_id:
            self.current_draft_id = next(iter(self.drafts.keys()))

    def get_info(self) -> Dict[str, Any]:
        """Get manager information"""
        return {
            "total_drafts": len(self.drafts),
            "current_draft_id": self.current_draft_id,
            "storage_path": str(self.storage_path),
            "draft_types": list(set(d.post_type for d in self.drafts.values())),
        }

    def generate_html_preview(
        self, draft_id: str, output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate HTML preview for a draft.

        Args:
            draft_id: Draft ID to preview
            output_path: Optional path to save the preview (defaults to previews/{draft_id}.html)

        Returns:
            Path to the saved HTML file, or None if draft not found
        """
        from .preview import LinkedInPreview

        draft = self.get_draft(draft_id)
        if not draft:
            return None

        # Get stats
        stats = self.get_draft_stats(draft_id)

        # Generate HTML
        html_content = LinkedInPreview.generate_html(draft.to_dict(), stats)

        # Determine output path
        if not output_path:
            preview_dir = self.storage_path / "previews"
            preview_dir.mkdir(exist_ok=True)
            output_path = str(preview_dir / f"{draft_id}.html")

        # Save preview
        saved_path = LinkedInPreview.save_preview(html_content, output_path)

        return saved_path
