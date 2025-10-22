# src/chuk_mcp_linkedin/preview/post_preview.py
"""
LinkedIn post preview generator.

Creates HTML previews of LinkedIn posts for local viewing.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import html


class LinkedInPreview:
    """Generate HTML previews of LinkedIn posts"""

    @staticmethod
    def generate_html(
        draft_data: Dict[str, Any],
        stats: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate HTML preview of a LinkedIn post.

        Args:
            draft_data: Draft data dictionary
            stats: Optional stats dictionary

        Returns:
            HTML string
        """
        post_type = draft_data.get("post_type", "text")
        content = draft_data.get("content", {})
        theme = draft_data.get("theme", "No theme")

        # Extract text content
        text_content = LinkedInPreview._extract_text_content(content)

        # Check for media attachments (images, videos, document files)
        media_html = LinkedInPreview._render_media_attachments(content)

        # Generate stats section
        stats_html = LinkedInPreview._generate_stats(stats) if stats else ""

        # Generate preview
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Post Preview - {html.escape(draft_data.get('name', 'Draft'))}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background: #f3f2ef;
            padding: 20px;
            color: rgba(0, 0, 0, 0.9);
        }}

        .container {{
            max-width: 680px;
            margin: 0 auto;
        }}

        .preview-header {{
            background: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            border: 1px solid #e0dfdc;
            border-bottom: none;
        }}

        .preview-header h1 {{
            font-size: 20px;
            color: #0a66c2;
            margin-bottom: 8px;
        }}

        .preview-meta {{
            display: flex;
            gap: 20px;
            font-size: 13px;
            color: rgba(0, 0, 0, 0.6);
            flex-wrap: wrap;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .meta-label {{
            font-weight: 600;
        }}

        .post-card {{
            background: white;
            border: 1px solid #e0dfdc;
            border-radius: 0 0 8px 8px;
            overflow: hidden;
        }}

        .post-header {{
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid #e0dfdc;
        }}

        .avatar {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0a66c2, #0073b1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
            font-weight: 600;
        }}

        .post-author {{
            flex: 1;
        }}

        .author-name {{
            font-size: 14px;
            font-weight: 600;
            color: rgba(0, 0, 0, 0.9);
        }}

        .author-headline {{
            font-size: 12px;
            color: rgba(0, 0, 0, 0.6);
            margin-top: 2px;
        }}

        .post-timestamp {{
            font-size: 12px;
            color: rgba(0, 0, 0, 0.6);
            margin-top: 4px;
        }}

        .post-type-badge {{
            display: inline-block;
            background: #0a66c2;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}

        .post-content {{
            padding: 16px 16px 0 16px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        .see-more-link {{
            color: #0a66c2;
            font-weight: 600;
            cursor: pointer;
        }}

        .see-more-link:hover {{
            text-decoration: underline;
        }}

        .hashtag {{
            color: #0a66c2;
            font-weight: 500;
        }}

        .post-actions {{
            padding: 8px 16px;
            border-top: 1px solid #e0dfdc;
            display: flex;
            justify-content: space-around;
        }}

        .action-btn {{
            flex: 1;
            padding: 12px;
            background: none;
            border: none;
            color: rgba(0, 0, 0, 0.6);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: background 0.2s;
        }}

        .action-btn:hover {{
            background: rgba(0, 0, 0, 0.05);
        }}

        .stats-section {{
            background: white;
            border: 1px solid #e0dfdc;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }}

        .stats-section h2 {{
            font-size: 16px;
            margin-bottom: 16px;
            color: rgba(0, 0, 0, 0.9);
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
        }}

        .stat-item {{
            padding: 12px;
            background: #f3f2ef;
            border-radius: 4px;
        }}

        .stat-label {{
            font-size: 12px;
            color: rgba(0, 0, 0, 0.6);
            margin-bottom: 4px;
        }}

        .stat-value {{
            font-size: 20px;
            font-weight: 600;
            color: #0a66c2;
        }}

        .stat-indicator {{
            font-size: 12px;
            margin-top: 4px;
        }}

        .stat-good {{
            color: #057642;
        }}

        .stat-warning {{
            color: #f5b800;
        }}

        .stat-bad {{
            color: #cc1016;
        }}

        .footer {{
            text-align: center;
            margin-top: 20px;
            padding: 20px;
            color: rgba(0, 0, 0, 0.6);
            font-size: 12px;
        }}

        /* Media attachment styles */
        .media-attachment {{
            margin-top: -12px;
            border-top: none;
        }}

        .media-image {{
            width: 100%;
            display: block;
            background: #000;
        }}

        .media-video {{
            width: 100%;
            background: #000;
            position: relative;
            margin-top: -12px;
            border-top: none;
        }}

        .video-placeholder {{
            width: 100%;
            aspect-ratio: 16 / 9;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}

        .video-play-button {{
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .video-play-button:hover {{
            transform: scale(1.1);
        }}

        .video-play-button::after {{
            content: '';
            width: 0;
            height: 0;
            border-left: 25px solid #0a66c2;
            border-top: 15px solid transparent;
            border-bottom: 15px solid transparent;
            margin-left: 8px;
        }}

        .video-duration {{
            position: absolute;
            bottom: 12px;
            right: 12px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}

        .document-file-card {{
            border-top: none;
            margin-top: -12px;
            padding: 16px;
            background: #f3f2ef;
            display: flex;
            align-items: center;
            gap: 16px;
            cursor: pointer;
            transition: background 0.2s;
        }}

        .document-file-card:hover {{
            background: #e8e6e3;
        }}

        .document-icon {{
            width: 48px;
            height: 48px;
            background: #fff;
            border: 1px solid #e0dfdc;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            flex-shrink: 0;
        }}

        .document-info {{
            flex: 1;
            min-width: 0;
        }}

        .document-title {{
            font-size: 14px;
            font-weight: 600;
            color: rgba(0, 0, 0, 0.9);
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .document-meta {{
            font-size: 12px;
            color: rgba(0, 0, 0, 0.6);
        }}

        .multi-image-grid {{
            display: grid;
            gap: 1px;
            background: #000;
            border-top: none;
            margin-top: -12px;
        }}

        .multi-image-grid.grid-1 {{
            grid-template-columns: 1fr;
        }}

        .multi-image-grid.grid-2 {{
            grid-template-columns: 1fr 1fr;
        }}

        .multi-image-grid.grid-3 {{
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 200px 200px;
        }}

        .multi-image-grid.grid-3 img:first-child {{
            grid-column: span 2;
            height: 200px;
        }}

        .multi-image-grid.grid-4 {{
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 200px 200px;
        }}

        .multi-image-grid img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
        }}

        .multi-image-grid.grid-1 img {{
            height: auto;
            max-height: 500px;
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .multi-image-grid img {{
                height: 200px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="preview-header">
            <h1>LinkedIn Post Preview</h1>
            <div class="preview-meta">
                <div class="meta-item">
                    <span class="meta-label">Draft:</span>
                    <span>{html.escape(draft_data.get('name', 'Untitled'))}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Type:</span>
                    <span>{html.escape(post_type.title())}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Theme:</span>
                    <span>{html.escape(str(theme).replace('_', ' ').title())}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Generated:</span>
                    <span>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
                </div>
            </div>
        </div>

        <div class="post-card">
            <div class="post-header">
                <div class="avatar">Y</div>
                <div class="post-author">
                    <div class="author-name">Your Name</div>
                    <div class="author-headline">Your Headline • 1st</div>
                    <div class="post-timestamp">Just now • 🌍</div>
                </div>
            </div>

            <div class="post-content">
                {LinkedInPreview._format_content(text_content)}
            </div>

            {media_html}

            <div class="post-actions">
                <button class="action-btn">👍 Like</button>
                <button class="action-btn">💬 Comment</button>
                <button class="action-btn">🔄 Repost</button>
                <button class="action-btn">📤 Send</button>
            </div>
        </div>

        {stats_html}

        <div class="footer">
            Generated by chuk-mcp-linkedin | This is a preview only
        </div>
    </div>
</body>
</html>"""

        return html_template

    @staticmethod
    def _render_media_attachments(content: Dict[str, Any]) -> str:
        """Render media attachments (images, videos, document files)"""
        media_html_parts = []

        # Check for images
        if "images" in content:
            images = content["images"]
            if images:
                media_html_parts.append(LinkedInPreview._render_images(images))

        # Check for video
        if "video" in content:
            video = content["video"]
            if video:
                media_html_parts.append(LinkedInPreview._render_video(video))

        # Check for document file
        if "document_file" in content:
            doc_file = content["document_file"]
            if doc_file:
                media_html_parts.append(LinkedInPreview._render_document_file(doc_file))

        return "\n".join(media_html_parts)

    @staticmethod
    def _render_images(images: list) -> str:
        """Render image attachments (single or multiple images)"""
        if not images:
            return ""

        image_count = len(images)
        grid_class = f"grid-{min(image_count, 4)}"

        # For single image
        if image_count == 1:
            img = images[0]
            img_path = img.get("filepath", img.get("url", ""))
            alt_text = img.get("alt_text", "Image")

            return f"""
            <div class="media-attachment">
                <img src="file://{img_path}" alt="{html.escape(alt_text)}" class="media-image">
            </div>
            """

        # For multiple images
        images_html = []
        for img in images[:4]:  # LinkedIn max is 20, but we'll show 4 for preview
            img_path = img.get("filepath", img.get("url", ""))
            alt_text = img.get("alt_text", "Image")
            images_html.append(f'<img src="file://{img_path}" alt="{html.escape(alt_text)}">')

        return f"""
        <div class="multi-image-grid {grid_class}">
            {''.join(images_html)}
        </div>
        """

    @staticmethod
    def _render_video(video: Dict[str, Any]) -> str:
        """Render video attachment with placeholder"""
        duration = video.get("duration", "0:00")
        thumbnail = video.get("thumbnail", "")

        if thumbnail:
            return f"""
            <div class="media-attachment media-video">
                <div class="video-placeholder" style="background-image: url('file://{thumbnail}'); background-size: cover;">
                    <div class="video-play-button"></div>
                    <div class="video-duration">{duration}</div>
                </div>
            </div>
            """
        else:
            return f"""
            <div class="media-attachment media-video">
                <div class="video-placeholder">
                    <div class="video-play-button"></div>
                    <div class="video-duration">{duration}</div>
                </div>
            </div>
            """

    @staticmethod
    def _render_document_file(doc_file: Dict[str, Any]) -> str:
        """Render document file as carousel (like LinkedIn converts PDFs/PPTX to images)"""
        filename = doc_file.get("filename", "Document")
        file_type = doc_file.get("file_type", "pdf").upper()
        filepath = doc_file.get("filepath", "")
        pages = doc_file.get("pages", 1)

        carousel_id = f"doc_carousel_{abs(hash(filename))}"

        # Try to convert document to images
        page_images = []
        try:
            from ..utils.document_converter import DocumentConverter

            # Convert document to images (with caching)
            page_images = DocumentConverter.convert_to_images(
                filepath,
                max_pages=20,  # LinkedIn limit
                dpi=150,  # Good balance of quality and performance
            )

            # Update page count based on actual conversion
            if page_images:
                pages = len(page_images)
        except Exception as e:
            # Fall back to placeholder if conversion fails
            print(f"Warning: Could not convert document to images: {e}")
            page_images = []

        # Generate slides (either with images or placeholders)
        slides_html = []
        for i in range(pages):
            if i < len(page_images):
                # Render with actual page image
                page_img_path = page_images[i]
                slides_html.append(
                    f"""
            <div class="carousel-item" data-slide="{i}">
                <div class="document-page-preview">
                    <div class="page-number">Page {i + 1} of {pages}</div>
                    <img src="file://{page_img_path}" alt="Page {i + 1}" class="document-page-image">
                </div>
            </div>
                """
                )
            else:
                # Render placeholder if image not available
                slides_html.append(
                    f"""
            <div class="carousel-item" data-slide="{i}">
                <div class="document-page-preview">
                    <div class="page-number">Page {i + 1} of {pages}</div>
                    <div class="page-placeholder">
                        <div class="document-icon-large">📄</div>
                        <div class="document-filename">{html.escape(filename)}</div>
                        <div class="page-info">{file_type} • Page {i + 1}/{pages}</div>
                    </div>
                </div>
            </div>
                """
                )

        slides_html_str = "\n".join(slides_html)

        return f"""
        <style>
            .document-carousel {{
                margin-top: -12px;
                background: #f3f2ef;
                border-top: none;
                padding: 20px;
                position: relative;
            }}

            .document-carousel .carousel-viewport {{
                position: relative;
                width: 100%;
                overflow: hidden;
                border-radius: 8px;
                background: white;
            }}

            .document-carousel .carousel-track {{
                display: flex;
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}

            .document-carousel .carousel-item {{
                flex: 0 0 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .document-page-preview {{
                width: 100%;
                aspect-ratio: 8.5 / 11;
                background: white;
                position: relative;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                border: 1px solid #e0dfdc;
            }}

            .document-page-image {{
                width: 100%;
                height: 100%;
                object-fit: contain;
                display: block;
            }}

            .page-number {{
                position: absolute;
                top: 12px;
                right: 12px;
                background: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
            }}

            .page-placeholder {{
                text-align: center;
                padding: 40px;
            }}

            .document-icon-large {{
                font-size: 64px;
                margin-bottom: 16px;
            }}

            .document-filename {{
                font-size: 14px;
                font-weight: 600;
                color: rgba(0, 0, 0, 0.9);
                margin-bottom: 8px;
            }}

            .page-info {{
                font-size: 12px;
                color: rgba(0, 0, 0, 0.6);
            }}

            .document-carousel .carousel-nav {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                z-index: 10;
            }}

            .document-carousel .carousel-nav.prev {{
                left: 10px;
            }}

            .document-carousel .carousel-nav.next {{
                right: 10px;
            }}

            .document-carousel .carousel-nav button {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                border: none;
                background: rgba(0, 0, 0, 0.6);
                color: white;
                font-size: 24px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
            }}

            .document-carousel .carousel-nav button:hover {{
                background: rgba(0, 0, 0, 0.8);
                transform: scale(1.1);
            }}

            .document-carousel .carousel-nav button:disabled {{
                opacity: 0.3;
                cursor: not-allowed;
            }}

            .document-carousel .carousel-indicators {{
                display: flex;
                gap: 6px;
                margin-top: 16px;
                justify-content: center;
            }}

            .document-carousel .indicator-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: rgba(0, 0, 0, 0.3);
                cursor: pointer;
                transition: all 0.2s;
            }}

            .document-carousel .indicator-dot.active {{
                background: #0A66C2;
                width: 24px;
                border-radius: 4px;
            }}

            .document-carousel .slide-counter {{
                text-align: center;
                margin-top: 12px;
                font-size: 13px;
                color: #666;
                font-weight: 500;
            }}
        </style>

        <div class="document-carousel" id="{carousel_id}">
            <div class="carousel-viewport">
                <div class="carousel-track">
                    {slides_html_str}
                </div>

                <div class="carousel-nav prev">
                    <button class="prev-btn" aria-label="Previous page">‹</button>
                </div>

                <div class="carousel-nav next">
                    <button class="next-btn" aria-label="Next page">›</button>
                </div>
            </div>

            <div class="carousel-indicators">
                {''.join(f'<div class="indicator-dot{"active" if i == 0 else ""}" data-slide="{i}"></div>' for i in range(pages))}
            </div>

            <div class="slide-counter">
                <span class="current-slide">1</span> / <span class="total-slides">{pages}</span>
            </div>
        </div>

        <script>
        (function() {{
            const carousel = document.getElementById('{carousel_id}');
            let currentSlide = 0;
            const totalSlides = {pages};
            const track = carousel.querySelector('.carousel-track');
            const prevBtn = carousel.querySelector('.prev-btn');
            const nextBtn = carousel.querySelector('.next-btn');
            const indicators = carousel.querySelectorAll('.indicator-dot');
            const currentSlideSpan = carousel.querySelector('.current-slide');

            function updateCarousel() {{
                const offset = -currentSlide * 100;
                track.style.transform = `translateX(${{offset}}%)`;

                indicators.forEach((dot, i) => {{
                    dot.classList.toggle('active', i === currentSlide);
                }});

                currentSlideSpan.textContent = currentSlide + 1;

                prevBtn.disabled = currentSlide === 0;
                nextBtn.disabled = currentSlide === totalSlides - 1;
            }}

            function nextSlide() {{
                if (currentSlide < totalSlides - 1) {{
                    currentSlide++;
                    updateCarousel();
                }}
            }}

            function prevSlide() {{
                if (currentSlide > 0) {{
                    currentSlide--;
                    updateCarousel();
                }}
            }}

            function goToSlide(index) {{
                currentSlide = index;
                updateCarousel();
            }}

            prevBtn.addEventListener('click', prevSlide);
            nextBtn.addEventListener('click', nextSlide);

            indicators.forEach((dot, index) => {{
                dot.addEventListener('click', () => goToSlide(index));
            }});

            // Keyboard navigation
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowLeft') prevSlide();
                if (e.key === 'ArrowRight') nextSlide();
            }});

            updateCarousel();
        }})();
        </script>
        """

    @staticmethod
    def _extract_text_content(content: Dict[str, Any]) -> str:
        """Extract text content from draft content"""
        # Check for composed text first
        if "composed_text" in content:
            return content["composed_text"]

        # Try commentary
        if "commentary" in content:
            return content["commentary"]

        # Try to build from components
        components = content.get("components", [])
        parts = []

        for comp in components:
            comp_type = comp.get("component")
            if comp_type == "hook":
                parts.append(comp.get("content", ""))
            elif comp_type == "body":
                parts.append(comp.get("content", ""))
            elif comp_type == "cta":
                parts.append(comp.get("text", ""))
            elif comp_type == "hashtags":
                tags = comp.get("tags", [])
                parts.append(" ".join(f"#{tag}" for tag in tags))

        return "\n\n".join(parts) if parts else "No content yet"

    @staticmethod
    def _format_content(text: str) -> str:
        """Format content with proper HTML escaping and highlighting"""
        import re

        # First, find and mark hashtags BEFORE escaping
        # Replace hashtags with a placeholder
        hashtag_pattern = r"#(\w+)"
        hashtags = []

        def replace_hashtag(match):
            hashtags.append(match.group(1))
            return f"__HASHTAG_{len(hashtags)-1}__"

        text = re.sub(hashtag_pattern, replace_hashtag, text)

        # Now escape HTML (this won't affect our placeholders)
        text = html.escape(text)

        # Restore hashtags with proper HTML formatting
        for idx, tag in enumerate(hashtags):
            text = text.replace(f"__HASHTAG_{idx}__", f'<span class="hashtag">#{tag}</span>')

        # Split at 210 characters for "see more" indicator (LinkedIn's truncation point)
        if len(text) > 210:
            # Find a good break point near 210 chars (end of line if possible)
            preview_text = text[:210]
            # Try to break at a newline
            last_newline = preview_text.rfind("\n")
            if last_newline > 150:  # If there's a newline reasonably close
                preview_text = preview_text[:last_newline]

            # Trim trailing whitespace/newlines from preview_text to reduce gap before "see more"
            preview_text = preview_text.rstrip()

            formatted = f"""<div class="collapsed-view" id="collapsed" style="display: block;">{preview_text} <span class="see-more-link" onclick="document.getElementById('collapsed').style.display='none'; document.getElementById('expanded').style.display='block';">...more</span></div>
<div class="expanded-view" id="expanded" style="display: none;">
{text}
</div>"""
        else:
            formatted = text

        return formatted

    @staticmethod
    def _generate_stats(stats: Dict[str, Any]) -> str:
        """Generate stats section HTML"""
        char_count = stats.get("char_count", 0)
        word_count = stats.get("word_count", 0)
        char_remaining = stats.get("char_remaining", 3000)
        hashtag_count = stats.get("hashtag_count", 0)

        # Determine indicators
        char_indicator = ""
        if char_count < 150:
            char_indicator = '<span class="stat-warning">⚠️ Too short</span>'
        elif char_count > 2000:
            char_indicator = '<span class="stat-warning">⚠️ Long post</span>'
        elif char_count >= 300 and char_count <= 800:
            char_indicator = '<span class="stat-good">✓ Optimal length</span>'
        else:
            char_indicator = '<span class="stat-indicator">📝 Good</span>'

        hashtag_indicator = ""
        if hashtag_count == 0:
            hashtag_indicator = '<span class="stat-warning">⚠️ No hashtags</span>'
        elif hashtag_count >= 3 and hashtag_count <= 5:
            hashtag_indicator = '<span class="stat-good">✓ Optimal</span>'
        elif hashtag_count > 10:
            hashtag_indicator = '<span class="stat-bad">⚠️ Too many</span>'

        hook_status = "✓ Yes" if stats.get("has_hook") else "❌ No"
        cta_status = "✓ Yes" if stats.get("has_cta") else "❌ No"

        return f"""
        <div class="stats-section">
            <h2>Post Analytics</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-label">Character Count</div>
                    <div class="stat-value">{char_count}</div>
                    <div class="stat-indicator">{char_indicator}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Word Count</div>
                    <div class="stat-value">{word_count}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Characters Remaining</div>
                    <div class="stat-value">{char_remaining}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Hashtags</div>
                    <div class="stat-value">{hashtag_count}</div>
                    <div class="stat-indicator">{hashtag_indicator}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Has Hook</div>
                    <div class="stat-value" style="font-size: 16px;">{hook_status}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Has CTA</div>
                    <div class="stat-value" style="font-size: 16px;">{cta_status}</div>
                </div>
            </div>
        </div>
        """

    @staticmethod
    def save_preview(html_content: str, output_path: str) -> str:
        """
        Save HTML preview to file.

        Args:
            html_content: HTML content to save
            output_path: Path to save the file

        Returns:
            Absolute path to saved file
        """
        from pathlib import Path

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(path.absolute())
