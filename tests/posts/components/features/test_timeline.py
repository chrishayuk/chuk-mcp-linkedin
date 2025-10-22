"""Tests for Timeline component."""

from chuk_mcp_linkedin.posts.components.features.timeline import Timeline


class TestTimelineInitialization:
    def test_init(self):
        steps = {"2024": "Launch", "2025": "Scale"}
        component = Timeline(steps)
        assert component.steps == steps


class TestTimelineRender:
    def test_render(self):
        steps = {"2024": "Launch", "2025": "Scale"}
        component = Timeline(steps)
        result = component.render()
        assert "2024" in result
        assert "Launch" in result

    def test_render_with_title(self):
        steps = {"2024": "Launch"}
        component = Timeline(steps, title="Journey")
        result = component.render()
        assert "JOURNEY" in result
        assert "2024" in result

    def test_render_numbered_style(self):
        steps = {"Jan": "Start", "Feb": "Continue"}
        component = Timeline(steps, style="numbered")
        result = component.render()
        assert "1. Jan: Start" in result
        assert "2. Feb: Continue" in result

    def test_render_dated_style(self):
        steps = {"Q1": "Launch", "Q2": "Grow"}
        component = Timeline(steps, style="dated")
        result = component.render()
        assert "Q1 | Launch" in result


class TestTimelineValidation:
    def test_validate_valid(self):
        steps = {"2024": "E1", "2025": "E2"}
        component = Timeline(steps)
        assert component.validate() is True

    def test_validate_empty(self):
        component = Timeline({})
        assert component.validate() is False
