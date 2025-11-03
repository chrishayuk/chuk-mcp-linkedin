"""Tests for base PostComponent class."""

import pytest

from chuk_mcp_linkedin.posts.components.base import PostComponent


class ConcreteComponent(PostComponent):
    """Concrete implementation for testing."""

    def __init__(self, content: str):
        self.content = content

    def render(self, theme=None) -> str:
        return f"Rendered: {self.content}"

    def validate(self) -> bool:
        return len(self.content) > 0


class IncompleteComponent(PostComponent):
    """Incomplete implementation that doesn't override methods."""

    def render(self, theme=None) -> str:
        # Explicitly call parent's abstract method to hit the pass statement
        return super().render(theme)

    def validate(self) -> bool:
        # Explicitly call parent's abstract method to hit the pass statement
        return super().validate()


class TestPostComponentAbstractMethods:
    """Test PostComponent abstract methods."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that PostComponent cannot be instantiated directly."""
        with pytest.raises(TypeError):
            PostComponent()

    def test_concrete_implementation_can_be_instantiated(self):
        """Test that concrete implementation can be instantiated."""
        component = ConcreteComponent("test content")
        assert component is not None

    def test_concrete_render_method(self):
        """Test that concrete render method works."""
        component = ConcreteComponent("test")
        result = component.render()
        assert result == "Rendered: test"

    def test_concrete_validate_method(self):
        """Test that concrete validate method works."""
        component = ConcreteComponent("test")
        assert component.validate() is True

    def test_concrete_validate_fails(self):
        """Test that concrete validate method can fail."""
        component = ConcreteComponent("")
        assert component.validate() is False

    def test_render_with_theme_parameter(self):
        """Test that render can be called with theme parameter."""
        component = ConcreteComponent("test")
        result = component.render(theme={"test": "theme"})
        assert result == "Rendered: test"

    def test_abstract_render_returns_none(self):
        """Test calling parent render method returns None."""
        component = IncompleteComponent()
        result = component.render()
        assert result is None

    def test_abstract_validate_returns_none(self):
        """Test calling parent validate method returns None."""
        component = IncompleteComponent()
        result = component.validate()
        assert result is None
