"""
Tests for typography components.

Ensures all typography components create valid configurations.
"""

from chuk_mcp_linkedin.components.typography import (
    Headers,
    BodyText,
    Captions,
    Quotes,
    Lists,
)


class TestHeaders:
    """Test Headers class"""

    def test_h1_default(self):
        """Test H1 with defaults"""
        component = Headers.h1("Main Title")
        assert component["type"] == "header"
        assert component["variant"] == "h1"
        assert component["text"] == "Main Title"
        assert component["align"] == "left"
        assert "font_size" in component
        assert "color" in component

    def test_h1_with_custom_color(self):
        """Test H1 with custom color"""
        component = Headers.h1("Title", color="#FF0000")
        assert component["color"] == "#FF0000"

    def test_h1_with_alignment(self):
        """Test H1 with center alignment"""
        component = Headers.h1("Title", align="center")
        assert component["align"] == "center"

    def test_h2_default(self):
        """Test H2 with defaults"""
        component = Headers.h2("Section Title")
        assert component["type"] == "header"
        assert component["variant"] == "h2"
        assert component["text"] == "Section Title"

    def test_h2_with_color_scheme(self):
        """Test H2 with different color scheme"""
        component = Headers.h2("Title", color_scheme="modern")
        assert "color" in component

    def test_h3_default(self):
        """Test H3 with defaults"""
        component = Headers.h3("Subsection Title")
        assert component["type"] == "header"
        assert component["variant"] == "h3"
        assert component["text"] == "Subsection Title"

    def test_h3_with_custom_color(self):
        """Test H3 with custom color"""
        component = Headers.h3("Title", color="#00FF00")
        assert component["color"] == "#00FF00"

    def test_h4_default(self):
        """Test H4 with defaults"""
        component = Headers.h4("Minor Section")
        assert component["type"] == "header"
        assert component["variant"] == "h4"
        assert component["text"] == "Minor Section"

    def test_h4_with_custom_color(self):
        """Test H4 with custom color"""
        component = Headers.h4("Title", color="#0000FF")
        assert component["color"] == "#0000FF"

    def test_section_header_without_divider(self):
        """Test section header without divider"""
        component = Headers.section_header("Section", with_divider=False)
        assert component["type"] == "header"
        assert component["variant"] == "section_header"
        assert "divider" not in component

    def test_section_header_with_divider(self):
        """Test section header with divider"""
        component = Headers.section_header("Section", with_divider=True)
        assert "divider" in component
        assert component["divider"]["style"] == "decorative_accent"

    def test_section_header_custom_divider_style(self):
        """Test section header with custom divider style"""
        component = Headers.section_header(
            "Section", with_divider=True, divider_style="horizontal_line"
        )
        assert component["divider"]["style"] == "horizontal_line"

    def test_eyebrow_default(self):
        """Test eyebrow with defaults"""
        component = Headers.eyebrow("NEW FEATURE")
        assert component["type"] == "header"
        assert component["variant"] == "eyebrow"
        assert component["text_transform"] == "uppercase"

    def test_eyebrow_custom_transform(self):
        """Test eyebrow with custom transform"""
        component = Headers.eyebrow("feature", transform="lowercase")
        assert component["text_transform"] == "lowercase"

    def test_slide_title_without_subtitle(self):
        """Test slide title without subtitle"""
        component = Headers.slide_title("Presentation Title")
        assert component["type"] == "header"
        assert component["variant"] == "slide_title"
        assert "subtitle" not in component

    def test_slide_title_with_subtitle(self):
        """Test slide title with subtitle"""
        component = Headers.slide_title("Main Title", subtitle="Secondary Text")
        assert "subtitle" in component
        assert component["subtitle"]["text"] == "Secondary Text"


class TestBodyText:
    """Test BodyText class"""

    def test_paragraph_default(self):
        """Test paragraph with defaults"""
        component = BodyText.paragraph("This is a paragraph.")
        assert component["type"] == "body_text"
        assert component["variant"] == "paragraph"
        assert component["text"] == "This is a paragraph."

    def test_paragraph_with_custom_color(self):
        """Test paragraph with custom color"""
        component = BodyText.paragraph("Text", color="#FF0000")
        assert component["color"] == "#FF0000"

    def test_lead_text(self):
        """Test lead text"""
        component = BodyText.lead_text("Lead paragraph text.")
        assert component["variant"] == "lead"
        assert "font_size" in component

    def test_lead_text_with_custom_color(self):
        """Test lead text with custom color"""
        component = BodyText.lead_text("Text", color="#00FF00")
        assert component["color"] == "#00FF00"

    def test_small_text(self):
        """Test small text"""
        component = BodyText.small_text("Fine print.")
        assert component["variant"] == "small"

    def test_small_text_with_custom_color(self):
        """Test small text with custom color"""
        component = BodyText.small_text("Text", color="#0000FF")
        assert component["color"] == "#0000FF"

    def test_highlighted_text(self):
        """Test highlighted text"""
        component = BodyText.highlighted("Important text")
        assert component["variant"] == "highlighted"
        assert "background_color" in component

    def test_highlighted_text_custom_background(self):
        """Test highlighted text with custom background"""
        component = BodyText.highlighted("Text", background_color="#FFFF00")
        assert component["background_color"] == "#FFFF00"

    def test_emphasized_text(self):
        """Test emphasized text"""
        component = BodyText.emphasized("Emphasized text")
        assert component["variant"] == "emphasized"

    def test_emphasized_text_styles(self):
        """Test emphasized text with different styles"""
        bold = BodyText.emphasized("Bold", style="bold")
        italic = BodyText.emphasized("Italic", style="italic")
        both = BodyText.emphasized("Both", style="both")
        assert bold["font_weight"] != italic["font_weight"]
        assert italic["font_style"] == "italic"
        assert both["font_style"] == "italic"

    def test_link(self):
        """Test link"""
        component = BodyText.link("Click here", url="https://example.com")
        assert component["variant"] == "link"
        assert component["url"] == "https://example.com"

    def test_link_without_url(self):
        """Test link without URL"""
        component = BodyText.link("Link")
        assert "url" not in component

    def test_code_inline(self):
        """Test inline code"""
        component = BodyText.code("const x = 1;", inline=True)
        assert component["variant"] == "code"
        assert component["display"] == "inline"

    def test_code_block(self):
        """Test code block"""
        code = "def hello():\n    print('world')"
        component = BodyText.code(code, inline=False)
        assert component["display"] == "block"


class TestCaptions:
    """Test Captions class"""

    def test_caption_default(self):
        """Test caption with defaults"""
        component = Captions.caption("Figure 1: Example")
        assert component["type"] == "caption"
        assert component["variant"] == "caption"
        assert component["text"] == "Figure 1: Example"

    def test_caption_styles(self):
        """Test caption with different styles"""
        default = Captions.caption("Text", style="default")
        muted = Captions.caption("Text", style="muted")
        highlighted = Captions.caption("Text", style="highlighted")
        assert default["style"] == "default"
        assert muted["style"] == "muted"
        assert highlighted["style"] == "highlighted"

    def test_metadata(self):
        """Test metadata caption"""
        component = Captions.metadata("Last updated: Today")
        assert component["variant"] == "metadata"

    def test_metadata_with_icon(self):
        """Test metadata with icon"""
        component = Captions.metadata("Date", icon="📅")
        assert "icon" in component
        assert component["icon"]["symbol"] == "📅"

    def test_image_caption(self):
        """Test image caption"""
        component = Captions.image_caption("Photo by John Doe")
        assert component["variant"] == "image_caption"

    def test_image_caption_with_attribution(self):
        """Test image caption with attribution"""
        component = Captions.image_caption("Caption", attribution="Getty Images")
        assert "attribution" in component
        assert component["attribution"]["text"] == "Getty Images"

    def test_data_source(self):
        """Test data source caption"""
        component = Captions.data_source("Internal Analytics 2024")
        assert component["variant"] == "data_source"
        assert component["font_style"] == "italic"

    def test_footnote_without_number(self):
        """Test footnote without number"""
        component = Captions.footnote("This is a footnote.")
        assert component["variant"] == "footnote"
        assert "number" not in component

    def test_footnote_with_number(self):
        """Test footnote with number"""
        component = Captions.footnote("Footnote text", number=1)
        assert component["number"] == 1
        assert "number_style" in component

    def test_legal(self):
        """Test legal text"""
        component = Captions.legal("Terms and conditions apply.")
        assert component["variant"] == "legal"
        assert component["opacity"] == 0.7


class TestQuotes:
    """Test Quotes class"""

    def test_blockquote_default(self):
        """Test blockquote with defaults"""
        component = Quotes.blockquote("Quote text")
        assert component["type"] == "quote"
        assert component["variant"] == "blockquote"
        assert component["text"] == "Quote text"

    def test_blockquote_with_author(self):
        """Test blockquote with author"""
        component = Quotes.blockquote("Quote", author="John Doe")
        assert "author" in component
        assert isinstance(component["author"], dict)

    def test_blockquote_with_border(self):
        """Test blockquote border options"""
        with_border = Quotes.blockquote("Quote", with_border=True)
        assert "border_left" in with_border or "border" in str(with_border)

    def test_pull_quote(self):
        """Test pull quote"""
        component = Quotes.pull_quote("Pull quote text")
        assert component["variant"] == "pull_quote"

    def test_pull_quote_with_author(self):
        """Test pull quote with author"""
        component = Quotes.pull_quote("Quote", author="Jane Smith")
        assert "author" in component
        assert isinstance(component["author"], dict)

    def test_pull_quote_styles(self):
        """Test pull quote with different styles"""
        minimal = Quotes.pull_quote("Quote", style="minimal")
        accent = Quotes.pull_quote("Quote", style="accent")
        boxed = Quotes.pull_quote("Quote", style="boxed")
        assert minimal["style"] == "minimal"
        assert accent["style"] == "accent"
        assert "border_left" in accent
        assert boxed["style"] == "boxed"
        assert "background_color" in boxed

    def test_testimonial_minimal(self):
        """Test testimonial with minimal data"""
        component = Quotes.testimonial("Great product!", author="User")
        assert component["variant"] == "testimonial"
        assert component["text"] == "Great product!"

    def test_testimonial_with_role_and_company(self):
        """Test testimonial with role and company"""
        component = Quotes.testimonial(
            text="Excellent!",
            author="John Doe",
            role="CEO",
            company="Acme Corp",
        )
        assert component["author"]["name"] == "John Doe"
        assert "role" in component["author"]
        # Company is concatenated with role
        role_text = component["author"]["role"]["text"]
        assert "CEO" in role_text

    def test_testimonial_with_rating(self):
        """Test testimonial with rating"""
        component = Quotes.testimonial("Great!", author="User", rating=5.0)
        assert "rating" in component
        assert component["rating"]["value"] == 5.0

    def test_testimonial_with_avatar(self):
        """Test testimonial with avatar"""
        component = Quotes.testimonial(
            "Great!", author="User", avatar="https://example.com/avatar.jpg"
        )
        # Avatar URL is stored in the author dict
        assert component["author"]


class TestLists:
    """Test Lists class"""

    def test_bulleted_list_default(self):
        """Test bulleted list with defaults"""
        component = Lists.bulleted_list(["Item 1", "Item 2", "Item 3"])
        assert component["type"] == "list"
        assert component["variant"] == "bulleted"
        assert len(component["items"]) == 3
        assert component["bullet"] == "→"

    def test_bulleted_list_custom_bullet(self):
        """Test bulleted list with custom bullet"""
        component = Lists.bulleted_list(["Item"], bullet_style="checkmark")
        assert component["bullet"] == "✓"

    def test_numbered_list_default(self):
        """Test numbered list with defaults"""
        component = Lists.numbered_list(["First", "Second", "Third"])
        assert component["variant"] == "numbered"
        assert component["start_number"] == 1

    def test_numbered_list_custom_start(self):
        """Test numbered list with custom start number"""
        component = Lists.numbered_list(["Item"], start_number=5)
        assert component["start_number"] == 5

    def test_checklist(self):
        """Test checklist"""
        items = [
            {"text": "Task 1", "checked": True},
            {"text": "Task 2", "checked": False},
        ]
        component = Lists.checklist(items)
        assert component["variant"] == "checklist"
        assert component["checked_symbol"] == "✓"

    def test_icon_list(self):
        """Test icon list"""
        items = [
            {"icon": "🚀", "text": "Fast"},
            {"icon": "⚡", "text": "Powerful"},
        ]
        component = Lists.icon_list(items)
        assert component["variant"] == "icon_list"
        assert len(component["items"]) == 2

    def test_two_column_list(self):
        """Test two-column list"""
        component = Lists.two_column_list(["A", "B", "C", "D"])
        assert component["variant"] == "two_column"
        assert component["columns"] == 2

    def test_two_column_list_custom_bullet(self):
        """Test two-column list with custom bullet"""
        component = Lists.two_column_list(["A"], bullet_style="disc")
        assert component["bullet"] == "•"

    def test_definition_list(self):
        """Test definition list"""
        items = [
            {"term": "HTML", "description": "HyperText Markup Language"},
            {"term": "CSS", "description": "Cascading Style Sheets"},
        ]
        component = Lists.definition_list(items)
        assert component["variant"] == "definition"
        assert len(component["items"]) == 2
