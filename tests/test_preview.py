"""Tests for preview module."""

import tempfile
from pathlib import Path

from chuk_mcp_linkedin.preview.component_renderer import ComponentRenderer
from chuk_mcp_linkedin.preview.post_preview import LinkedInPreview


class TestComponentRenderer:
    """Test ComponentRenderer class"""

    def test_render_divider_horizontal_line(self):
        """Test rendering horizontal line divider"""
        divider = {
            "variant": "horizontal_line",
            "width": 400,
            "height": 2,
            "color": "#000",
            "margin_top": 10,
            "margin_bottom": 10,
            "style": "solid",
        }
        result = ComponentRenderer.render_divider(divider)
        assert "width: 400px" in result
        assert "height: 2px" in result
        assert "background-color: #000" in result

    def test_render_divider_horizontal_line_dashed(self):
        """Test rendering dashed horizontal line divider"""
        divider = {
            "variant": "horizontal_line",
            "width": 400,
            "height": 2,
            "color": "#000",
            "margin_top": 10,
            "margin_bottom": 10,
            "style": "dashed",
        }
        result = ComponentRenderer.render_divider(divider)
        assert "border-style: dashed" in result

    def test_render_divider_gradient_fade(self):
        """Test rendering gradient fade divider"""
        divider = {
            "variant": "gradient_fade",
            "width": 400,
            "height": 4,
            "margin_top": 10,
            "margin_bottom": 10,
            "gradient": {"start": "#000", "mid": "#666", "end": "#fff"},
        }
        result = ComponentRenderer.render_divider(divider)
        assert "linear-gradient" in result
        assert "#000" in result
        assert "#666" in result
        assert "#fff" in result

    def test_render_divider_decorative_accent(self):
        """Test rendering decorative accent divider"""
        divider = {
            "variant": "decorative_accent",
            "width": 100,
            "height": 4,
            "color": "#0a66c2",
            "border_radius": 2,
            "margin_top": 10,
            "margin_bottom": 10,
        }
        result = ComponentRenderer.render_divider(divider)
        assert "border-radius: 2px" in result
        assert "#0a66c2" in result

    def test_render_divider_section_break(self):
        """Test rendering section break divider"""
        divider = {
            "variant": "section_break",
            "align": "center",
            "color": "#666",
            "font_size": 16,
            "margin_top": 20,
            "margin_bottom": 20,
            "symbols": "• • •",
        }
        result = ComponentRenderer.render_divider(divider)
        assert "text-align: center" in result
        assert "• • •" in result

    def test_render_divider_spacer(self):
        """Test rendering spacer divider"""
        divider = {"variant": "spacer", "height": 30}
        result = ComponentRenderer.render_divider(divider)
        assert "height: 30px" in result

    def test_render_divider_unknown_variant(self):
        """Test rendering unknown divider variant returns empty string"""
        divider = {"variant": "unknown"}
        result = ComponentRenderer.render_divider(divider)
        assert result == ""

    def test_render_badge_pill(self):
        """Test rendering pill badge"""
        badge = {
            "variant": "pill",
            "text": "New",
            "background_color": "#0a66c2",
            "text_color": "#fff",
            "padding_y": 6,
            "padding_x": 12,
            "font_size": 18,
            "font_weight": "600",
            "border_radius": 999,
        }
        result = ComponentRenderer.render_badge(badge)
        assert "New" in result
        assert "#0a66c2" in result
        assert "#fff" in result

    def test_render_badge_status(self):
        """Test rendering status badge"""
        badge = {
            "variant": "status",
            "text": "Active",
            "background_color": "#057642",
            "text_color": "#fff",
        }
        result = ComponentRenderer.render_badge(badge)
        assert "Active" in result
        assert "text-transform: uppercase" in result

    def test_render_badge_status_outlined(self):
        """Test rendering outlined status badge"""
        badge = {
            "variant": "status_outlined",
            "text": "Pending",
            "background_color": "#fff",
            "text_color": "#f5b800",
            "border_width": 2,
            "border_color": "#f5b800",
        }
        result = ComponentRenderer.render_badge(badge)
        assert "Pending" in result
        assert "border: 2px solid #f5b800" in result

    def test_render_badge_percentage_change(self):
        """Test rendering percentage change badge"""
        badge = {
            "variant": "percentage_change",
            "text": "+12%",
            "background_color": "#e6f4ea",
            "text_color": "#057642",
        }
        result = ComponentRenderer.render_badge(badge)
        assert "+12%" in result

    def test_render_badge_category_tag(self):
        """Test rendering category tag badge"""
        badge = {
            "variant": "category_tag",
            "text": "Technology",
            "background_color": "#e8f0fe",
            "text_color": "#0a66c2",
        }
        result = ComponentRenderer.render_badge(badge)
        assert "Technology" in result

    def test_render_badge_unknown_variant(self):
        """Test rendering unknown badge variant returns empty string"""
        badge = {"variant": "unknown", "text": "Test"}
        result = ComponentRenderer.render_badge(badge)
        assert result == ""

    def test_render_shape_circle_filled(self):
        """Test rendering filled circle shape"""
        shape = {"variant": "circle", "size": 50, "color": "#0a66c2", "fill": True}
        result = ComponentRenderer.render_shape(shape)
        assert "width: 50px" in result
        assert "height: 50px" in result
        assert "border-radius: 50%" in result
        assert "background-color: #0a66c2" in result

    def test_render_shape_circle_outline(self):
        """Test rendering outline circle shape"""
        shape = {
            "variant": "circle",
            "size": 50,
            "color": "#0a66c2",
            "fill": False,
            "stroke_width": 2,
        }
        result = ComponentRenderer.render_shape(shape)
        assert "border: 2px solid #0a66c2" in result

    def test_render_shape_icon_container(self):
        """Test rendering icon container shape"""
        shape = {
            "variant": "icon_container",
            "size": 60,
            "border_radius": 8,
            "background_color": "#e8f0fe",
            "icon_color": "#0a66c2",
            "icon_size": 30,
            "icon": "⚡",
        }
        result = ComponentRenderer.render_shape(shape)
        assert "⚡" in result
        assert "#e8f0fe" in result

    def test_render_shape_checkmark_without_background(self):
        """Test rendering checkmark without background"""
        shape = {
            "variant": "checkmark",
            "size": 30,
            "color": "#057642",
            "symbol": "✓",
            "background": False,
        }
        result = ComponentRenderer.render_shape(shape)
        assert "✓" in result
        assert "color: #057642" in result

    def test_render_shape_checkmark_with_background(self):
        """Test rendering checkmark with background"""
        shape = {
            "variant": "checkmark",
            "size": 30,
            "color": "#057642",
            "symbol": "✓",
            "background": True,
            "border_radius": 4,
        }
        result = ComponentRenderer.render_shape(shape)
        assert "✓" in result
        assert "background-color: #057642" in result

    def test_render_shape_progress_ring(self):
        """Test rendering progress ring shape"""
        shape = {
            "variant": "progress_ring",
            "size": 100,
            "percentage": 75,
            "background_color": "#e0dfdc",
            "progress_color": "#0a66c2",
        }
        result = ComponentRenderer.render_shape(shape)
        assert "75%" in result
        assert "#0a66c2" in result

    def test_render_shape_unknown_variant(self):
        """Test rendering unknown shape variant returns empty string"""
        shape = {"variant": "unknown"}
        result = ComponentRenderer.render_shape(shape)
        assert result == ""

    def test_render_border_simple(self):
        """Test rendering simple border"""
        border = {
            "variant": "simple",
            "width": 2,
            "style": "solid",
            "color": "#e0dfdc",
            "radius": 8,
            "padding": 20,
        }
        result = ComponentRenderer.render_border(border, "Test content")
        assert "Test content" in result
        assert "border: 2px solid #e0dfdc" in result
        assert "border-radius: 8px" in result

    def test_render_border_accent_left(self):
        """Test rendering accent border on left"""
        border = {"variant": "accent", "width": 4, "color": "#0a66c2", "side": "left"}
        result = ComponentRenderer.render_border(border, "Content")
        assert "border-left: 4px solid #0a66c2" in result

    def test_render_border_accent_right(self):
        """Test rendering accent border on right"""
        border = {"variant": "accent", "width": 4, "color": "#0a66c2", "side": "right"}
        result = ComponentRenderer.render_border(border, "Content")
        assert "border-right: 4px solid #0a66c2" in result

    def test_render_border_accent_top(self):
        """Test rendering accent border on top"""
        border = {"variant": "accent", "width": 4, "color": "#0a66c2", "side": "top"}
        result = ComponentRenderer.render_border(border, "Content")
        assert "border-top: 4px solid #0a66c2" in result

    def test_render_border_accent_bottom(self):
        """Test rendering accent border on bottom"""
        border = {
            "variant": "accent",
            "width": 4,
            "color": "#0a66c2",
            "side": "bottom",
        }
        result = ComponentRenderer.render_border(border, "Content")
        assert "border-bottom: 4px solid #0a66c2" in result

    def test_render_border_callout(self):
        """Test rendering callout border"""
        border = {
            "variant": "callout",
            "border_width": 2,
            "border_color": "#0a66c2",
            "background_color": "#e8f0fe",
            "border_radius": 8,
        }
        result = ComponentRenderer.render_border(border, "Content")
        assert "#e8f0fe" in result

    def test_render_border_shadow_frame(self):
        """Test rendering shadow frame border"""
        border = {
            "variant": "shadow_frame",
            "border_width": 1,
            "border_color": "#e0dfdc",
            "border_radius": 8,
            "shadow": "0 2px 8px rgba(0,0,0,0.1)",
        }
        result = ComponentRenderer.render_border(border, "Content")
        assert "box-shadow:" in result

    def test_render_border_shadow_frame_no_border(self):
        """Test rendering shadow frame without border"""
        border = {
            "variant": "shadow_frame",
            "border_width": 0,
            "border_color": "#e0dfdc",
            "border_radius": 8,
            "shadow": "0 2px 8px rgba(0,0,0,0.1)",
        }
        result = ComponentRenderer.render_border(border, "Content")
        assert "box-shadow:" in result

    def test_render_border_unknown_variant(self):
        """Test rendering unknown border variant returns wrapped content"""
        border = {"variant": "unknown"}
        result = ComponentRenderer.render_border(border, "Content")
        assert "Content" in result

    def test_render_background_solid(self):
        """Test rendering solid background"""
        background = {"variant": "solid", "color": "#f3f2ef"}
        result = ComponentRenderer.render_background(background, "Content", 400, 200)
        assert "background-color: #f3f2ef" in result
        assert "width: 400px" in result
        assert "height: 200px" in result

    def test_render_background_gradient_vertical(self):
        """Test rendering vertical gradient background"""
        background = {
            "variant": "gradient",
            "direction": "vertical",
            "start_color": "#fff",
            "end_color": "#f3f2ef",
        }
        result = ComponentRenderer.render_background(background)
        assert "linear-gradient(to bottom" in result

    def test_render_background_gradient_horizontal(self):
        """Test rendering horizontal gradient background"""
        background = {
            "variant": "gradient",
            "direction": "horizontal",
            "start_color": "#fff",
            "end_color": "#f3f2ef",
        }
        result = ComponentRenderer.render_background(background)
        assert "linear-gradient(to right" in result

    def test_render_background_gradient_diagonal(self):
        """Test rendering diagonal gradient background"""
        background = {
            "variant": "gradient",
            "direction": "diagonal",
            "start_color": "#fff",
            "end_color": "#f3f2ef",
        }
        result = ComponentRenderer.render_background(background)
        assert "linear-gradient(to bottom right" in result

    def test_render_background_card(self):
        """Test rendering card background"""
        background = {
            "variant": "card",
            "color": "#fff",
            "shadow": "0 2px 8px rgba(0,0,0,0.1)",
            "border_radius": 8,
            "padding": 20,
        }
        result = ComponentRenderer.render_background(background)
        assert "box-shadow:" in result

    def test_render_background_highlight_box(self):
        """Test rendering highlight box background"""
        background = {
            "variant": "highlight_box",
            "background_color": "#e8f0fe",
            "border_width": 2,
            "border_color": "#0a66c2",
            "border_radius": 8,
            "padding": 20,
        }
        result = ComponentRenderer.render_background(background)
        assert "#e8f0fe" in result

    def test_render_background_unknown_variant(self):
        """Test rendering unknown background variant returns wrapped content"""
        background = {"variant": "unknown"}
        result = ComponentRenderer.render_background(background, "Content")
        assert "Content" in result

    def test_render_components_grid_with_title(self):
        """Test rendering components grid with title"""
        components = [
            {"type": "divider", "variant": "spacer", "height": 20},
            {
                "type": "badge",
                "variant": "pill",
                "text": "New",
                "background_color": "#0a66c2",
                "text_color": "#fff",
            },
        ]
        result = ComponentRenderer.render_components_grid(components, "Test Components")
        assert "Test Components" in result
        assert "New" in result

    def test_render_components_grid_without_title(self):
        """Test rendering components grid without title"""
        components = [{"type": "divider", "variant": "spacer", "height": 20}]
        result = ComponentRenderer.render_components_grid(components)
        assert "<div style='display: grid" in result

    def test_render_components_grid_all_types(self):
        """Test rendering all component types in grid"""
        components = [
            {"type": "divider", "variant": "spacer", "height": 20},
            {
                "type": "badge",
                "variant": "pill",
                "text": "Badge",
                "background_color": "#0a66c2",
                "text_color": "#fff",
            },
            {"type": "shape", "variant": "circle", "size": 30, "color": "#000", "fill": True},
            {
                "type": "border",
                "variant": "simple",
                "width": 2,
                "style": "solid",
                "color": "#000",
                "radius": 4,
            },
            {"type": "background", "variant": "solid", "color": "#f3f2ef"},
        ]
        result = ComponentRenderer.render_components_grid(components)
        assert "Badge" in result


class TestLinkedInPreview:
    """Test LinkedInPreview class"""

    def test_generate_html_basic(self):
        """Test basic HTML generation"""
        draft_data = {
            "name": "Test Draft",
            "post_type": "text",
            "content": {"commentary": "This is a test post"},
            "theme": "professional",
        }
        html = LinkedInPreview.generate_html(draft_data)
        assert "<!DOCTYPE html>" in html
        assert "Test Draft" in html
        assert "This is a test post" in html

    def test_generate_html_with_stats(self):
        """Test HTML generation with stats"""
        draft_data = {
            "name": "Test",
            "post_type": "text",
            "content": {"commentary": "Post"},
        }
        stats = {
            "char_count": 500,
            "word_count": 100,
            "char_remaining": 2500,
            "hashtag_count": 3,
            "has_hook": True,
            "has_cta": True,
        }
        html = LinkedInPreview.generate_html(draft_data, stats)
        assert "Post Analytics" in html
        assert "500" in html
        assert "100" in html

    def test_extract_text_content_composed_text(self):
        """Test extracting composed text"""
        content = {"composed_text": "Composed content"}
        result = LinkedInPreview._extract_text_content(content)
        assert result == "Composed content"

    def test_extract_text_content_commentary(self):
        """Test extracting commentary"""
        content = {"commentary": "Commentary content"}
        result = LinkedInPreview._extract_text_content(content)
        assert result == "Commentary content"

    def test_extract_text_content_components(self):
        """Test extracting text from components"""
        content = {
            "components": [
                {"component": "hook", "content": "Hook text"},
                {"component": "body", "content": "Body text"},
                {"component": "cta", "text": "CTA text"},
                {"component": "hashtags", "tags": ["ai", "tech"]},
            ]
        }
        result = LinkedInPreview._extract_text_content(content)
        assert "Hook text" in result
        assert "Body text" in result
        assert "CTA text" in result
        assert "#ai" in result
        assert "#tech" in result

    def test_extract_text_content_empty(self):
        """Test extracting text from empty content"""
        content = {}
        result = LinkedInPreview._extract_text_content(content)
        assert result == "No content yet"

    def test_format_content_short(self):
        """Test formatting short content"""
        text = "Short post"
        result = LinkedInPreview._format_content(text)
        assert "Short post" in result
        assert "...more" not in result

    def test_format_content_long_with_see_more(self):
        """Test formatting long content with see more"""
        text = "A" * 250
        result = LinkedInPreview._format_content(text)
        assert "...more" in result
        assert "collapsed-view" in result
        assert "expanded-view" in result

    def test_format_content_with_hashtags(self):
        """Test formatting content with hashtags"""
        text = "Check out #AI and #MachineLearning"
        result = LinkedInPreview._format_content(text)
        assert '<span class="hashtag">#AI</span>' in result
        assert '<span class="hashtag">#MachineLearning</span>' in result

    def test_format_content_html_escape(self):
        """Test HTML escaping in content"""
        text = "<script>alert('xss')</script>"
        result = LinkedInPreview._format_content(text)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_render_media_attachments_images(self):
        """Test rendering image attachments"""
        content = {"images": [{"filepath": "/path/to/image.jpg", "alt_text": "Test image"}]}
        result = LinkedInPreview._render_media_attachments(content)
        assert "media-image" in result
        assert "/path/to/image.jpg" in result

    def test_render_media_attachments_video(self):
        """Test rendering video attachments"""
        content = {"video": {"duration": "1:30", "thumbnail": "/path/to/thumb.jpg"}}
        result = LinkedInPreview._render_media_attachments(content)
        assert "video-play-button" in result
        assert "1:30" in result

    def test_render_media_attachments_document(self):
        """Test rendering document attachments"""
        content = {
            "document_file": {
                "filename": "presentation.pdf",
                "file_type": "pdf",
                "filepath": "/nonexistent/file.pdf",
                "pages": 5,
            }
        }
        result = LinkedInPreview._render_media_attachments(content)
        assert "document-carousel" in result
        assert "presentation.pdf" in result

    def test_render_images_single(self):
        """Test rendering single image"""
        images = [{"filepath": "/path/to/image.jpg", "alt_text": "Test"}]
        result = LinkedInPreview._render_images(images)
        assert "media-image" in result
        assert "/path/to/image.jpg" in result

    def test_render_images_multiple(self):
        """Test rendering multiple images"""
        images = [
            {"filepath": "/path/1.jpg", "alt_text": "Image 1"},
            {"filepath": "/path/2.jpg", "alt_text": "Image 2"},
            {"filepath": "/path/3.jpg", "alt_text": "Image 3"},
        ]
        result = LinkedInPreview._render_images(images)
        assert "multi-image-grid" in result
        assert "grid-3" in result
        assert "/path/1.jpg" in result

    def test_render_images_empty(self):
        """Test rendering empty image list"""
        result = LinkedInPreview._render_images([])
        assert result == ""

    def test_render_video_with_thumbnail(self):
        """Test rendering video with thumbnail"""
        video = {"duration": "2:30", "thumbnail": "/path/to/thumb.jpg"}
        result = LinkedInPreview._render_video(video)
        assert "video-placeholder" in result
        assert "/path/to/thumb.jpg" in result
        assert "2:30" in result

    def test_render_video_without_thumbnail(self):
        """Test rendering video without thumbnail"""
        video = {"duration": "1:00"}
        result = LinkedInPreview._render_video(video)
        assert "video-placeholder" in result
        assert "1:00" in result

    def test_generate_stats_optimal_char_count(self):
        """Test generating stats with optimal character count"""
        stats = {
            "char_count": 500,
            "word_count": 100,
            "char_remaining": 2500,
            "hashtag_count": 4,
            "has_hook": True,
            "has_cta": True,
        }
        result = LinkedInPreview._generate_stats(stats)
        assert "500" in result
        assert "Optimal length" in result

    def test_generate_stats_too_short(self):
        """Test generating stats with too short content"""
        stats = {
            "char_count": 100,
            "word_count": 20,
            "char_remaining": 2900,
            "hashtag_count": 0,
        }
        result = LinkedInPreview._generate_stats(stats)
        assert "Too short" in result
        assert "No hashtags" in result

    def test_generate_stats_too_long(self):
        """Test generating stats with too long content"""
        stats = {
            "char_count": 2500,
            "word_count": 500,
            "char_remaining": 500,
            "hashtag_count": 15,
        }
        result = LinkedInPreview._generate_stats(stats)
        assert "Long post" in result
        assert "Too many" in result

    def test_generate_stats_good_length(self):
        """Test generating stats with good length"""
        stats = {
            "char_count": 1000,
            "word_count": 200,
            "char_remaining": 2000,
            "hashtag_count": 2,
        }
        result = LinkedInPreview._generate_stats(stats)
        assert "1000" in result
        assert "Good" in result

    def test_generate_stats_no_hook_or_cta(self):
        """Test generating stats without hook or CTA"""
        stats = {
            "char_count": 500,
            "word_count": 100,
            "char_remaining": 2500,
            "hashtag_count": 3,
            "has_hook": False,
            "has_cta": False,
        }
        result = LinkedInPreview._generate_stats(stats)
        assert "❌ No" in result

    def test_save_preview(self):
        """Test saving preview to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "preview.html"
            html_content = "<html><body>Test</body></html>"

            result = LinkedInPreview.save_preview(html_content, str(output_path))

            assert Path(result).exists()
            assert Path(result).read_text(encoding="utf-8") == html_content

    def test_save_preview_creates_parent_dirs(self):
        """Test that save_preview creates parent directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "dir" / "preview.html"
            html_content = "<html><body>Test</body></html>"

            result = LinkedInPreview.save_preview(html_content, str(output_path))

            assert Path(result).exists()
            assert Path(result).parent.exists()


class TestPreviewInit:
    """Test preview package initialization"""

    def test_component_renderer_importable(self):
        """Test that ComponentRenderer can be imported from preview"""
        from chuk_mcp_linkedin.preview.component_renderer import ComponentRenderer

        assert ComponentRenderer is not None

    def test_linkedin_preview_importable(self):
        """Test that LinkedInPreview can be imported from preview"""
        from chuk_mcp_linkedin.preview.post_preview import LinkedInPreview

        assert LinkedInPreview is not None
