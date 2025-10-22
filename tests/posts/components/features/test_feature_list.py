"""Tests for FeatureList component."""

from chuk_mcp_linkedin.posts.components.features.feature_list import FeatureList


class TestFeatureListInitialization:
    def test_init(self):
        features = [{"title": "Feature 1"}, {"title": "Feature 2"}]
        component = FeatureList(features)
        assert component.features == features


class TestFeatureListRender:
    def test_render(self):
        component = FeatureList([{"title": "Feature 1"}])
        result = component.render()
        assert "Feature 1" in result

    def test_render_with_title(self):
        component = FeatureList([{"title": "F1"}], title="Features")
        result = component.render()
        assert "FEATURES" in result
        assert "F1" in result

    def test_render_with_description(self):
        features = [{"title": "Feature", "description": "This is a description"}]
        component = FeatureList(features)
        result = component.render()
        assert "Feature" in result
        assert "This is a description" in result


class TestFeatureListValidation:
    def test_validate_valid(self):
        component = FeatureList([{"title": "Feature"}])
        assert component.validate() is True

    def test_validate_empty(self):
        component = FeatureList([])
        assert component.validate() is False

    def test_validate_missing_title(self):
        component = FeatureList([{"description": "No title"}])
        assert component.validate() is False

    def test_validate_empty_title(self):
        component = FeatureList([{"title": ""}])
        assert component.validate() is False
