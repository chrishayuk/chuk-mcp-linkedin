"""
Draft management system for LinkedIn posts.

Handles CRUD operations for draft posts with session-based locking.

Storage Architecture:
- Drafts (JSON): Stored via local filesystem (legacy) or chuk-artifacts
- Previews (HTML): Always stored via chuk-artifacts for VFS abstraction

Preview HTML is always managed through chuk-artifacts, enabling seamless
deployment across multiple storage backends (memory, filesystem, S3, IBM COS)
without code changes.

For production deployments requiring S3/cloud storage:
- Set artifact_provider="s3" or "ibm-cos" in manager initialization
- Configure S3/COS credentials via environment variables
- Previews automatically use the configured artifact storage backend

Preview Methods:
- read_preview_html_async(): Read preview HTML from artifacts
- generate_html_preview_async(): Generate and store preview HTML in artifacts
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from chuk_artifacts import ArtifactStore
from chuk_artifacts.config import configure_filesystem, configure_memory
from pydantic import BaseModel, ConfigDict, Field


class DraftModel(BaseModel):
    """Pydantic model for LinkedIn post draft"""

    draft_id: str = Field(..., description="Unique draft identifier")
    name: str = Field(..., description="Draft name", min_length=1)
    post_type: str = Field(..., description="Type of post (text, image, carousel, etc.)")
    content: Dict[str, Any] = Field(default_factory=dict, description="Draft content")
    theme: Optional[str] = Field(None, description="Optional theme identifier")
    variant_config: Dict[str, Any] = Field(
        default_factory=dict, description="Variant configuration"
    )
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    preview_token: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        description="Unique token for shareable preview URLs",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "draft_id": "draft_1_1234567890",
                "name": "My LinkedIn Post",
                "post_type": "text",
                "content": {"composed_text": "Example post content..."},
                "theme": "thought_leader",
                "variant_config": {},
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00",
                "metadata": {},
            }
        }
    )


class Draft:
    """Represents a LinkedIn post draft with Pydantic validation"""

    def __init__(
        self,
        draft_id: str,
        name: str,
        post_type: str,
        content: Optional[Dict[str, Any]] = None,
        theme: Optional[str] = None,
        variant_config: Optional[Dict[str, Any]] = None,
    ):
        self._model = DraftModel(
            draft_id=draft_id,
            name=name,
            post_type=post_type,
            content=content or {},
            theme=theme,
            variant_config=variant_config or {},
        )

    @property
    def draft_id(self) -> str:
        """Get draft ID"""
        return self._model.draft_id

    @draft_id.setter
    def draft_id(self, value: str) -> None:
        """Set draft ID"""
        self._model.draft_id = value

    @property
    def name(self) -> str:
        """Get draft name"""
        return self._model.name

    @name.setter
    def name(self, value: str) -> None:
        """Set draft name"""
        self._model.name = value
        self._model.updated_at = datetime.now().isoformat()

    @property
    def post_type(self) -> str:
        """Get post type"""
        return self._model.post_type

    @property
    def content(self) -> Dict[str, Any]:
        """Get draft content"""
        return self._model.content

    @property
    def theme(self) -> Optional[str]:
        """Get theme"""
        return self._model.theme

    @theme.setter
    def theme(self, value: Optional[str]) -> None:
        """Set theme"""
        self._model.theme = value
        self._model.updated_at = datetime.now().isoformat()

    @property
    def variant_config(self) -> Dict[str, Any]:
        """Get variant config"""
        return self._model.variant_config

    @property
    def created_at(self) -> str:
        """Get created timestamp"""
        return self._model.created_at

    @created_at.setter
    def created_at(self, value: str) -> None:
        """Set created timestamp"""
        self._model.created_at = value

    @property
    def updated_at(self) -> str:
        """Get updated timestamp"""
        return self._model.updated_at

    @updated_at.setter
    def updated_at(self, value: str) -> None:
        """Set updated timestamp"""
        self._model.updated_at = value

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get metadata"""
        return self._model.metadata

    @property
    def preview_token(self) -> str:
        """Get shareable preview token"""
        return self._model.preview_token

    def update_content(self, content: Dict[str, Any]) -> None:
        """Update draft content"""
        self._model.content.update(content)
        self._model.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert draft to dictionary"""
        return self._model.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Draft":
        """Create draft from dictionary"""
        model = DraftModel(**data)
        draft = cls.__new__(cls)
        draft._model = model
        return draft


class LinkedInManager:
    """Manager for LinkedIn post drafts with user-level isolation"""

    def __init__(
        self,
        storage_path: Optional[str] = None,
        user_id: Optional[str] = None,
        use_artifacts: bool = False,
        artifact_provider: str = "memory",
    ):
        """
        Initialize manager with optional storage path and user ID.

        Args:
            storage_path: Path to store drafts (defaults to .linkedin_drafts)
            user_id: OAuth user ID for user-level isolation (required for multi-user deployments)
            use_artifacts: Whether to use chuk-artifacts for storage (default: False)
            artifact_provider: Storage provider if using artifacts (memory, filesystem, s3, ibm-cos)
        """
        # User identity (from OAuth) - used for isolation
        self.user_id = user_id or "anonymous"

        # Legacy filesystem storage (will be deprecated)
        self.storage_path = Path(storage_path or f".linkedin_drafts/{self.user_id}")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.drafts: Dict[str, Draft] = {}
        self.current_draft_id: Optional[str] = None

        # Artifact storage
        self.use_artifacts = use_artifacts
        self.artifact_provider = artifact_provider
        self._artifact_store: Optional[ArtifactStore] = None
        self._artifact_initialized = False

        # Load existing drafts
        self._load_drafts()

    async def __aenter__(self) -> "LinkedInManager":
        """Async context manager entry - initializes artifact store for previews."""
        await self._ensure_artifact_store()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self._artifact_store:
            await self._artifact_store.__aexit__(exc_type, exc_val, exc_tb)
            self._artifact_initialized = False

    async def _ensure_artifact_store(self) -> None:
        """Ensure artifact store is initialized (always required for preview HTML)."""
        if not self._artifact_initialized:
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
        if self._artifact_store is None:
            return None

        artifact_id = await self._artifact_store.store(
            data=draft_json.encode("utf-8"),
            mime="application/json",
            summary=f"LinkedIn Draft: {draft.name}",
            filename=f"{draft_id}.json",
            user_id=self.user_id,
            meta={
                "draft_id": draft_id,
                "draft_name": draft.name,
                "post_type": draft.post_type,
                "type": "draft",
            },
        )

        return str(artifact_id)

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

        if self._artifact_store is None:
            return None

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

    def create_draft(
        self,
        name: str,
        post_type: str,
        content: Optional[Dict[str, Any]] = None,
        theme: Optional[str] = None,
        variant_config: Optional[Dict[str, Any]] = None,
    ) -> Draft:
        """Create a new draft for the authenticated user"""
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

        self._save_draft(draft)

        return draft

    def get_draft(self, draft_id: str) -> Optional[Draft]:
        """Get a draft by ID"""
        return self.drafts.get(draft_id)

    def get_draft_by_preview_token(self, preview_token: str) -> Optional[Draft]:
        """Get a draft by its preview token"""
        for draft in self.drafts.values():
            if draft.preview_token == preview_token:
                return draft
        return None

    def get_current_draft(self) -> Optional[Draft]:
        """Get the currently active draft"""
        if self.current_draft_id:
            return self.drafts.get(self.current_draft_id)
        return None

    def list_drafts(self) -> List[Dict[str, Any]]:
        """
        List all drafts for the authenticated user.

        Returns:
            List of draft metadata dictionaries
        """
        drafts_list = []
        for draft in self.drafts.values():
            drafts_list.append(
                {
                    "draft_id": draft.draft_id,
                    "name": draft.name,
                    "post_type": draft.post_type,
                    "theme": draft.theme,
                    "created_at": draft.created_at,
                    "updated_at": draft.updated_at,
                    "is_current": draft.draft_id == self.current_draft_id,
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
            return str(commentary)

        return str(commentary[:chars]) + "..."

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

    def _save_draft(self, draft: Draft) -> None:
        """Save draft to storage"""
        draft_file = self.storage_path / f"{draft.draft_id}.json"
        with open(draft_file, "w") as f:
            json.dump(draft.to_dict(), f, indent=2)

    def _load_drafts(self) -> None:
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

    async def generate_html_preview_async(self, draft_id: str) -> Optional[str]:
        """
        Generate HTML preview for a draft and store in artifacts.

        Args:
            draft_id: Draft ID to preview

        Returns:
            Artifact ID of the saved HTML file, or None if draft not found

        Note:
            User isolation is enforced automatically - each user's manager instance
            only has access to their own drafts and artifacts.
        """
        from .preview import LinkedInPreview

        draft = self.get_draft(draft_id)
        if not draft:
            return None

        # Get stats
        stats = self.get_draft_stats(draft_id)

        # Generate HTML
        html_content = LinkedInPreview.generate_html(draft.to_dict(), stats)

        # Always store as artifact
        await self._ensure_artifact_store()

        if self._artifact_store is None:
            return None

        artifact_id = await self._artifact_store.store(
            data=html_content.encode("utf-8"),
            mime="text/html",
            summary=f"Preview: {draft.name}",
            filename=f"previews/{draft_id}.html",
            user_id=self.user_id,
            meta={
                "draft_id": draft_id,
                "draft_name": draft.name,
                "type": "preview",
            },
        )
        return str(artifact_id)

    async def read_preview_html_async(self, draft_id: str) -> Optional[str]:
        """
        Read HTML preview content for a draft from artifact storage.

        Args:
            draft_id: Draft ID to read preview for

        Returns:
            HTML content as string, or None if not found

        Note:
            User isolation is enforced automatically - each user's manager instance
            only has access to their own drafts and artifacts.
        """
        # Check if draft exists
        draft = self.get_draft(draft_id)
        if not draft:
            return None

        # Always use artifacts
        await self._ensure_artifact_store()

        if self._artifact_store is None:
            return None

        try:
            # List all artifacts for this user
            artifacts = await self._artifact_store.list_by_session(session_id=self.user_id)

            # Filter for preview artifacts matching this draft_id
            for artifact_id in artifacts:
                # Get metadata for this artifact
                meta = await self._artifact_store.metadata(artifact_id)
                if meta and meta.get("type") == "preview" and meta.get("draft_id") == draft_id:
                    # Found matching preview
                    data = await self._artifact_store.retrieve(artifact_id)
                    if data:
                        return str(data.decode("utf-8"))

            # Preview not found in artifacts, generate it
            artifact_id = await self.generate_html_preview_async(draft_id)
            if not artifact_id:
                return None

            # Retrieve the newly generated preview
            data = await self._artifact_store.retrieve(artifact_id)
            if data:
                return str(data.decode("utf-8"))

        except Exception:
            return None

        return None

    async def generate_preview_url(
        self, draft_id: str, base_url: str = "http://localhost:8000", expires_in: int = 3600
    ) -> Optional[str]:
        """
        Generate a preview URL for a draft.

        For S3/cloud storage: Uses signed URLs from chuk-artifacts
        For memory/filesystem: Uses shareable token-based URLs

        Args:
            draft_id: Draft ID to preview
            base_url: Base URL of the server (for token-based URLs)
            expires_in: Expiration time in seconds (for signed URLs)

        Returns:
            Preview URL or None if draft not found
        """
        draft = self.get_draft(draft_id)
        if not draft:
            return None

        # For S3/cloud storage, use signed URLs
        if self.artifact_provider in ("s3", "ibm-cos"):
            # Ensure preview exists in artifacts
            artifact_id = await self.generate_html_preview_async(draft_id)
            if not artifact_id:
                return None

            await self._ensure_artifact_store()
            if self._artifact_store is None:
                return None

            # Generate signed URL
            signed_url = await self._artifact_store.get_shareable_url(
                artifact_id=artifact_id, expires_in=expires_in
            )
            return str(signed_url) if signed_url else None

        # For memory/filesystem, use token-based URL
        return f"{base_url}/preview/{draft.preview_token}"
