# src/chuk_mcp_linkedin/posts/components/base.py
"""
Base component class for all LinkedIn post components.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class PostComponent(ABC):
    """Base class for all post subcomponents"""

    @abstractmethod
    def render(self, theme: Optional[Any] = None) -> str:
        """Render component to text"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate component configuration"""
        pass
