"""Tests for Quote component."""

from chuk_mcp_linkedin.posts.components.features.quote import Quote


class TestQuoteInitialization:
    def test_init(self):
        component = Quote("Great quote", "Author Name")
        assert component.text == "Great quote"
        assert component.author == "Author Name"


class TestQuoteRender:
    def test_render(self):
        component = Quote("Test quote", "Author")
        result = component.render()
        assert "Test quote" in result
        assert "Author" in result


class TestQuoteValidation:
    def test_validate_valid(self):
        component = Quote("Valid quote", "Author")
        assert component.validate() is True

    def test_validate_empty_text(self):
        component = Quote("", "Author")
        assert component.validate() is False

    def test_validate_empty_author(self):
        component = Quote("Text", "")
        assert component.validate() is False
