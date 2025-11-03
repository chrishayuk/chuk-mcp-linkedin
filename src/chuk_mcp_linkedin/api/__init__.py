# src/chuk_mcp_linkedin/api/__init__.py
"""
LinkedIn API integration module.

Clean, modular API for interacting with LinkedIn.
"""

from .client import LinkedInClient as BaseLinkedInClient
from .config import LinkedInConfig, config
from .documents import DocumentsAPIMixin
from .errors import LinkedInAPIError
from .media import MediaAPIMixin
from .posts import PostsAPIMixin


class LinkedInClient(PostsAPIMixin, MediaAPIMixin, DocumentsAPIMixin, BaseLinkedInClient):
    """
    LinkedIn API client with all capabilities.

    Combines:
    - Base client (authentication, headers, config validation)
    - Posts API (text, image, video, multi-image, poll posts)
    - Media API (image and video uploads)
    - Documents API (document upload and posts)

    Example:
        >>> client = LinkedInClient()
        >>> # Text post
        >>> await client.create_text_post("Hello LinkedIn!")
        >>>
        >>> # Image post
        >>> await client.create_image_post("Check this out", "image.jpg")
        >>>
        >>> # Multi-image carousel
        >>> await client.create_multi_image_post("Swipe through", ["img1.jpg", "img2.jpg"])
        >>>
        >>> # Video post
        >>> await client.create_video_post("Watch this", "video.mp4")
        >>>
        >>> # Poll post
        >>> await client.create_poll_post("Quick poll:", "Favorite language?", ["Python", "Go"])
        >>>
        >>> # Document post
        >>> await client.create_document_post("Read this", "report.pdf")
    """

    pass


__all__ = [
    "LinkedInConfig",
    "config",
    "LinkedInClient",
    "LinkedInAPIError",
]
