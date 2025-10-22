"""Tests for Checklist component."""

from chuk_mcp_linkedin.posts.components.features.checklist import Checklist


class TestChecklistInitialization:
    def test_init(self):
        items = [{"text": "Task 1"}, {"text": "Task 2"}]
        component = Checklist(items)
        assert component.items == items


class TestChecklistRender:
    def test_render(self):
        component = Checklist([{"text": "Task 1"}])
        result = component.render()
        assert "Task 1" in result

    def test_render_with_title(self):
        component = Checklist([{"text": "Task"}], title="My Checklist")
        result = component.render()
        assert "MY CHECKLIST" in result
        assert "Task" in result

    def test_render_with_progress(self):
        items = [
            {"text": "Task 1", "checked": True},
            {"text": "Task 2", "checked": False},
            {"text": "Task 3", "checked": True},
        ]
        component = Checklist(items, show_progress=True)
        result = component.render()
        assert "Progress:" in result
        assert "2/3" in result


class TestChecklistValidation:
    def test_validate_valid(self):
        component = Checklist([{"text": "Task"}])
        assert component.validate() is True

    def test_validate_empty(self):
        component = Checklist([])
        assert component.validate() is False

    def test_validate_missing_text_key(self):
        component = Checklist([{"checked": True}])
        assert component.validate() is False

    def test_validate_empty_text(self):
        component = Checklist([{"text": ""}])
        assert component.validate() is False
