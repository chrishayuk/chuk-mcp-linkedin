"""Tests for PollPreview component."""

from chuk_mcp_linkedin.posts.components.features.poll_preview import PollPreview


class TestPollPreviewInitialization:
    def test_init(self):
        component = PollPreview("Question?", ["Option 1", "Option 2"])
        assert component.question == "Question?"
        assert component.options == ["Option 1", "Option 2"]


class TestPollPreviewRender:
    def test_render(self):
        component = PollPreview("Question?", ["A", "B"])
        result = component.render()
        assert "Question?" in result
        assert "A" in result


class TestPollPreviewValidation:
    def test_validate_valid(self):
        component = PollPreview("Q?", ["A", "B"])
        assert component.validate() is True

    def test_validate_invalid(self):
        component = PollPreview("", ["A"])
        assert component.validate() is False
