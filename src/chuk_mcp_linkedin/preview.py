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
            padding: 16px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        .see-more-line {{
            position: relative;
            margin: 12px 0;
        }}

        .see-more-line::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, #0a66c2, transparent);
            opacity: 0.3;
        }}

        .see-more-text {{
            position: relative;
            text-align: center;
            color: #0a66c2;
            font-size: 12px;
            font-weight: 600;
            background: white;
            display: inline-block;
            padding: 0 12px;
            left: 50%;
            transform: translateX(-50%);
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

        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
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
        hashtag_pattern = r'#(\w+)'
        hashtags = []

        def replace_hashtag(match):
            hashtags.append(match.group(1))
            return f'__HASHTAG_{len(hashtags)-1}__'

        text = re.sub(hashtag_pattern, replace_hashtag, text)

        # Now escape HTML (this won't affect our placeholders)
        text = html.escape(text)

        # Restore hashtags with proper HTML formatting
        for idx, tag in enumerate(hashtags):
            text = text.replace(
                f'__HASHTAG_{idx}__',
                f'<span class="hashtag">#{tag}</span>'
            )

        # Split at 210 characters for "see more" indicator (LinkedIn's truncation point)
        if len(text) > 210:
            # Find a good break point near 210 chars (end of line if possible)
            preview_text = text[:210]
            # Try to break at a newline
            last_newline = preview_text.rfind('\n')
            if last_newline > 150:  # If there's a newline reasonably close
                preview_text = preview_text[:last_newline]

            rest_text = text[len(preview_text):]

            formatted = f"""
                <div class="collapsed-view" id="collapsed" style="display: block;">
                    {preview_text}
                    <div class="see-more-line">
                        <span class="see-more-text" onclick="document.getElementById('collapsed').style.display='none'; document.getElementById('expanded').style.display='block';" style="cursor: pointer;">...see more</span>
                    </div>
                </div>
                <div class="expanded-view" id="expanded" style="display: none;">
                    {text}
                </div>
            """
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
