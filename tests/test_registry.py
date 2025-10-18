"""
Tests for ComponentRegistry.
"""

from chuk_mcp_linkedin.registry import ComponentRegistry


class TestListPostComponents:
    """Test listing post components"""

    def test_list_post_components(self):
        """Test listing all post components"""
        components = ComponentRegistry.list_post_components()

        assert isinstance(components, dict)
        assert len(components) > 0

    def test_has_all_post_types(self):
        """Test has all expected post types"""
        components = ComponentRegistry.list_post_components()

        expected_types = [
            "text_post",
            "document_post",
            "poll_post",
            "video_post",
            "image_post",
            "carousel_post",
            "article_post",
        ]

        for post_type in expected_types:
            assert post_type in components

    def test_components_have_required_fields(self):
        """Test each component has required fields"""
        components = ComponentRegistry.list_post_components()

        for component_name, component_data in components.items():
            assert "description" in component_data, f"{component_name} missing description"
            assert "engagement_rank" in component_data, f"{component_name} missing engagement_rank"
            assert "variants" in component_data, f"{component_name} missing variants"

    def test_document_post_highest_engagement(self):
        """Test document post has highest engagement"""
        components = ComponentRegistry.list_post_components()

        assert components["document_post"]["engagement_rank"] == 1
        assert components["document_post"]["engagement_rate"] == 45.85

    def test_poll_post_highest_reach(self):
        """Test poll post has highest reach"""
        components = ComponentRegistry.list_post_components()

        assert components["poll_post"]["engagement_rank"] == 2
        assert components["poll_post"]["reach_multiplier"] == 3.0


class TestListSubcomponents:
    """Test listing subcomponents"""

    def test_list_subcomponents(self):
        """Test listing all subcomponents"""
        subcomponents = ComponentRegistry.list_subcomponents()

        assert isinstance(subcomponents, dict)
        assert len(subcomponents) > 0

    def test_has_all_subcomponents(self):
        """Test has all expected subcomponents"""
        subcomponents = ComponentRegistry.list_subcomponents()

        expected = ["hook", "body", "cta", "hashtags"]
        for subcomp in expected:
            assert subcomp in subcomponents

    def test_hook_subcomponent_structure(self):
        """Test hook subcomponent structure"""
        subcomponents = ComponentRegistry.list_subcomponents()
        hook = subcomponents["hook"]

        assert "description" in hook
        assert "types" in hook
        assert "best_practices" in hook

    def test_hook_types(self):
        """Test hook types are defined"""
        subcomponents = ComponentRegistry.list_subcomponents()
        hook_types = subcomponents["hook"]["types"]

        expected_types = ["question", "stat", "story", "controversy", "list", "curiosity"]
        for hook_type in expected_types:
            assert hook_type in hook_types
            assert "power" in hook_types[hook_type]
            assert "examples" in hook_types[hook_type]

    def test_cta_subcomponent_structure(self):
        """Test CTA subcomponent structure"""
        subcomponents = ComponentRegistry.list_subcomponents()
        cta = subcomponents["cta"]

        assert "description" in cta
        assert "types" in cta

    def test_hashtags_optimal_count(self):
        """Test hashtags optimal count"""
        subcomponents = ComponentRegistry.list_subcomponents()
        hashtags = subcomponents["hashtags"]

        assert hashtags["optimal_count"] == "3-5"


class TestListThemes:
    """Test listing themes"""

    def test_list_themes(self):
        """Test listing all themes"""
        themes = ComponentRegistry.list_themes()

        assert isinstance(themes, dict)
        assert len(themes) == 10

    def test_themes_have_required_fields(self):
        """Test each theme has required fields"""
        themes = ComponentRegistry.list_themes()

        for theme_name, theme_data in themes.items():
            assert "description" in theme_data, f"{theme_name} missing description"
            assert "tone" in theme_data, f"{theme_name} missing tone"
            assert "goal" in theme_data, f"{theme_name} missing goal"
            assert "post_frequency" in theme_data, f"{theme_name} missing post_frequency"

    def test_thought_leader_theme(self):
        """Test thought leader theme is present"""
        themes = ComponentRegistry.list_themes()

        assert "thought_leader" in themes
        assert themes["thought_leader"]["goal"] == "authority"


class TestGetRecommendations:
    """Test getting recommendations"""

    def test_get_recommendations_engagement(self):
        """Test recommendations for engagement goal"""
        recs = ComponentRegistry.get_recommendations("engagement")

        assert "top_formats" in recs
        assert "theme" in recs
        assert "best_practices" in recs
        assert "hook_types" in recs
        assert "cta_types" in recs

    def test_get_recommendations_authority(self):
        """Test recommendations for authority goal"""
        recs = ComponentRegistry.get_recommendations("authority")

        assert recs["theme"] == "thought_leader"
        assert "document_post" in recs["top_formats"]

    def test_get_recommendations_leads(self):
        """Test recommendations for leads goal"""
        recs = ComponentRegistry.get_recommendations("leads")

        assert recs["theme"] == "corporate_professional"
        assert "document_post" in recs["top_formats"]

    def test_get_recommendations_community(self):
        """Test recommendations for community goal"""
        recs = ComponentRegistry.get_recommendations("community")

        assert recs["theme"] == "community_builder"
        assert "poll_post" in recs["top_formats"]

    def test_get_recommendations_awareness(self):
        """Test recommendations for awareness goal"""
        recs = ComponentRegistry.get_recommendations("awareness")

        assert recs["theme"] == "personal_brand"
        assert "video_post" in recs["top_formats"]

    def test_get_recommendations_unknown_goal(self):
        """Test recommendations for unknown goal returns default"""
        recs = ComponentRegistry.get_recommendations("unknown_goal")

        # Should return engagement as default
        assert "top_formats" in recs
        assert "theme" in recs

    def test_get_recommendations_case_insensitive(self):
        """Test recommendations are case insensitive"""
        recs1 = ComponentRegistry.get_recommendations("ENGAGEMENT")
        recs2 = ComponentRegistry.get_recommendations("engagement")

        assert recs1 == recs2


class TestGetCompleteSystemOverview:
    """Test getting system overview"""

    def test_get_complete_system_overview(self):
        """Test getting complete system overview"""
        overview = ComponentRegistry.get_complete_system_overview()

        assert isinstance(overview, dict)
        assert "post_types" in overview
        assert "themes" in overview
        assert "subcomponents" in overview

    def test_overview_has_post_types_count(self):
        """Test overview has correct post types count"""
        overview = ComponentRegistry.get_complete_system_overview()

        assert overview["post_types"] == 7

    def test_overview_has_themes_count(self):
        """Test overview has correct themes count"""
        overview = ComponentRegistry.get_complete_system_overview()

        assert overview["themes"] == 10

    def test_overview_has_top_performers(self):
        """Test overview has top performers"""
        overview = ComponentRegistry.get_complete_system_overview()

        assert "top_performers" in overview
        top = overview["top_performers"]
        assert "highest_engagement" in top
        assert "highest_reach" in top
        assert "fastest_growing" in top

    def test_overview_has_key_metrics(self):
        """Test overview has key metrics"""
        overview = ComponentRegistry.get_complete_system_overview()

        assert "key_metrics" in overview
        metrics = overview["key_metrics"]
        assert metrics["max_post_length"] == 3000
        assert metrics["truncation_point"] == 210
        assert metrics["optimal_hashtags"] == "3-5"


class TestGetComponentInfo:
    """Test getting component info"""

    def test_get_component_info_text_post(self):
        """Test getting text post info"""
        info = ComponentRegistry.get_component_info("text_post")

        assert info is not None
        assert "description" in info
        assert "engagement_rank" in info

    def test_get_component_info_document_post(self):
        """Test getting document post info"""
        info = ComponentRegistry.get_component_info("document_post")

        assert info is not None
        assert info["engagement_rank"] == 1

    def test_get_component_info_not_found(self):
        """Test getting info for non-existent component"""
        info = ComponentRegistry.get_component_info("nonexistent")

        assert info == {}


class TestGetVariantInfo:
    """Test getting variant info"""

    def test_get_variant_info_text(self):
        """Test getting variant info for text post"""
        info = ComponentRegistry.get_variant_info("text")

        assert info is not None
        assert "post_type" in info
        assert "base" in info
        assert "variants" in info
        assert "has_compounds" in info

    def test_get_variant_info_poll(self):
        """Test getting variant info for poll post"""
        info = ComponentRegistry.get_variant_info("poll")

        assert info is not None
        assert info["post_type"] == "poll"

    def test_get_variant_info_document(self):
        """Test getting variant info for document post"""
        info = ComponentRegistry.get_variant_info("document")

        assert info is not None
        assert info["post_type"] == "document"

    def test_get_variant_info_unknown(self):
        """Test getting variant info for unknown post type"""
        info = ComponentRegistry.get_variant_info("unknown")

        assert info == {}


class TestSearchComponents:
    """Test searching components"""

    def test_search_components_poll(self):
        """Test searching for poll"""
        results = ComponentRegistry.search_components("poll")

        assert len(results) > 0
        # Should find poll_post
        poll_results = [r for r in results if "poll" in r["name"].lower()]
        assert len(poll_results) > 0

    def test_search_components_engagement(self):
        """Test searching for engagement"""
        results = ComponentRegistry.search_components("engagement")

        assert len(results) > 0

    def test_search_components_theme(self):
        """Test searching finds themes"""
        results = ComponentRegistry.search_components("thought")

        assert len(results) > 0
        # Should find thought_leader theme
        theme_results = [r for r in results if r["type"] == "theme"]
        assert len(theme_results) > 0

    def test_search_components_case_insensitive(self):
        """Test search is case insensitive"""
        results1 = ComponentRegistry.search_components("POLL")
        results2 = ComponentRegistry.search_components("poll")

        assert len(results1) == len(results2)

    def test_search_components_no_results(self):
        """Test search with no matching results"""
        results = ComponentRegistry.search_components("xyz123nonexistent")

        assert len(results) == 0

    def test_search_results_have_required_fields(self):
        """Test search results have required fields"""
        results = ComponentRegistry.search_components("post")

        for result in results:
            assert "type" in result
            assert "name" in result
            assert "description" in result


class TestIntegration:
    """Integration tests for registry"""

    def test_all_post_components_have_variants(self):
        """Test all post components have variants"""
        components = ComponentRegistry.list_post_components()

        for component_name, component_data in components.items():
            assert "variants" in component_data
            assert len(component_data["variants"]) > 0

    def test_all_engagement_ranks_unique(self):
        """Test all post types have unique engagement ranks"""
        components = ComponentRegistry.list_post_components()

        ranks = [c["engagement_rank"] for c in components.values()]
        assert len(ranks) == len(set(ranks))

    def test_recommendations_match_existing_themes(self):
        """Test recommendations reference existing themes"""
        themes = ComponentRegistry.list_themes()
        goals = ["engagement", "authority", "leads", "community", "awareness"]

        for goal in goals:
            recs = ComponentRegistry.get_recommendations(goal)
            assert recs["theme"] in themes

    def test_recommendations_match_existing_components(self):
        """Test recommendations reference existing components"""
        components = ComponentRegistry.list_post_components()
        goals = ["engagement", "authority", "leads", "community", "awareness"]

        for goal in goals:
            recs = ComponentRegistry.get_recommendations(goal)
            for format in recs["top_formats"]:
                assert format in components

    def test_subcomponent_power_ratings_valid(self):
        """Test all subcomponent power ratings are valid"""
        subcomponents = ComponentRegistry.list_subcomponents()

        # Check hooks
        for hook_type, hook_data in subcomponents["hook"]["types"].items():
            power = hook_data["power"]
            assert 0 <= power <= 1, f"{hook_type} power {power} not in 0-1 range"

        # Check CTAs
        for cta_type, cta_data in subcomponents["cta"]["types"].items():
            power = cta_data["power"]
            assert 0 <= power <= 1, f"{cta_type} power {power} not in 0-1 range"
