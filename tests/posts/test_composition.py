"""Tests for posts/composition module."""

import pytest
from chuk_mcp_linkedin.posts.composition import ComposablePost, PostBuilder


class TestComposablePostInit:
    """Test ComposablePost initialization"""

    def test_init_basic(self):
        """Test basic initialization"""
        post = ComposablePost("text")
        assert post.post_type == "text"
        assert post.theme is None
        assert post.variant_config == {}
        assert post.components == []
        assert post.metadata == {}

    def test_init_with_theme(self):
        """Test initialization with theme"""
        theme = type("Theme", (), {"name": "professional"})()
        post = ComposablePost("text", theme=theme)
        assert post.theme == theme

    def test_init_with_variant_config(self):
        """Test initialization with variant config"""
        config = {"structure": "listicle"}
        post = ComposablePost("text", variant_config=config)
        assert post.variant_config == config


class TestComposablePostContentComponents:
    """Test adding content components"""

    def test_add_hook(self):
        """Test adding hook"""
        post = ComposablePost("text")
        result = post.add_hook("question", "Why is this important?")
        assert result is post  # Fluent interface
        assert len(post.components) == 1

    def test_add_body(self):
        """Test adding body"""
        post = ComposablePost("text")
        result = post.add_body("Content here")
        assert result is post
        assert len(post.components) == 1

    def test_add_body_with_structure(self):
        """Test adding body with structure"""
        post = ComposablePost("text")
        post.add_body("Content", structure="listicle")
        assert len(post.components) == 1

    def test_add_body_uses_variant_config(self):
        """Test body uses variant config structure"""
        post = ComposablePost("text", variant_config={"structure": "framework"})
        post.add_body("Content")
        # Structure should come from variant_config
        assert len(post.components) == 1

    def test_add_cta(self):
        """Test adding CTA"""
        post = ComposablePost("text")
        result = post.add_cta("direct", "Click here")
        assert result is post
        assert len(post.components) == 1

    def test_add_hashtags(self):
        """Test adding hashtags"""
        post = ComposablePost("text")
        result = post.add_hashtags(["AI", "Tech"])
        assert result is post
        assert len(post.components) == 1

    def test_add_hashtags_with_placement(self):
        """Test adding hashtags with placement"""
        post = ComposablePost("text")
        post.add_hashtags(["AI", "Tech"], placement="inline")
        assert len(post.components) == 1


class TestComposablePostDataVizComponents:
    """Test adding data visualization components"""

    def test_add_bar_chart(self):
        """Test adding bar chart"""
        post = ComposablePost("text")
        result = post.add_bar_chart({"A": 10, "B": 20})
        assert result is post
        assert len(post.components) == 1

    def test_add_bar_chart_with_title(self):
        """Test adding bar chart with title and unit"""
        post = ComposablePost("text")
        post.add_bar_chart({"A": 10}, title="Chart", unit="hours")
        assert len(post.components) == 1

    def test_add_metrics_chart(self):
        """Test adding metrics chart"""
        post = ComposablePost("text")
        result = post.add_metrics_chart({"Speed": "67%"})
        assert result is post
        assert len(post.components) == 1

    def test_add_comparison_chart(self):
        """Test adding comparison chart"""
        post = ComposablePost("text")
        result = post.add_comparison_chart({"A": "Point", "B": "Point"})
        assert result is post
        assert len(post.components) == 1

    def test_add_progress_chart(self):
        """Test adding progress chart"""
        post = ComposablePost("text")
        result = post.add_progress_chart({"Task": 50})
        assert result is post
        assert len(post.components) == 1

    def test_add_ranking_chart(self):
        """Test adding ranking chart"""
        post = ComposablePost("text")
        result = post.add_ranking_chart({"First": "100"})
        assert result is post
        assert len(post.components) == 1

    def test_add_ranking_chart_without_medals(self):
        """Test adding ranking chart without medals"""
        post = ComposablePost("text")
        post.add_ranking_chart({"First": "100"}, show_medals=False)
        assert len(post.components) == 1


class TestComposablePostFeatureComponents:
    """Test adding feature components"""

    def test_add_quote(self):
        """Test adding quote"""
        post = ComposablePost("text")
        result = post.add_quote("Quote text", "Author")
        assert result is post
        assert len(post.components) == 1

    def test_add_quote_with_source(self):
        """Test adding quote with source"""
        post = ComposablePost("text")
        post.add_quote("Quote", "Author", source="CEO")
        assert len(post.components) == 1

    def test_add_big_stat(self):
        """Test adding big stat"""
        post = ComposablePost("text")
        result = post.add_big_stat("2.5M", "users")
        assert result is post
        assert len(post.components) == 1

    def test_add_big_stat_with_context(self):
        """Test adding big stat with context"""
        post = ComposablePost("text")
        post.add_big_stat("10x", "faster", context="growth")
        assert len(post.components) == 1

    def test_add_timeline(self):
        """Test adding timeline"""
        post = ComposablePost("text")
        result = post.add_timeline({"2024": "Launch", "2025": "Scale"})
        assert result is post
        assert len(post.components) == 1

    def test_add_timeline_with_style(self):
        """Test adding timeline with style"""
        post = ComposablePost("text")
        post.add_timeline({"2024": "Launch"}, style="numbered")
        assert len(post.components) == 1

    def test_add_key_takeaway(self):
        """Test adding key takeaway"""
        post = ComposablePost("text")
        result = post.add_key_takeaway("Important message")
        assert result is post
        assert len(post.components) == 1

    def test_add_key_takeaway_custom(self):
        """Test adding key takeaway with custom title and style"""
        post = ComposablePost("text")
        post.add_key_takeaway("Message", title="Note", style="highlight")
        assert len(post.components) == 1

    def test_add_pro_con(self):
        """Test adding pro/con"""
        post = ComposablePost("text")
        result = post.add_pro_con(["Pro1"], ["Con1"])
        assert result is post
        assert len(post.components) == 1

    def test_add_pro_con_with_title(self):
        """Test adding pro/con with title"""
        post = ComposablePost("text")
        post.add_pro_con(["Pro"], ["Con"], title="Analysis")
        assert len(post.components) == 1

    def test_add_checklist(self):
        """Test adding checklist"""
        post = ComposablePost("text")
        result = post.add_checklist([{"text": "Task 1"}])
        assert result is post
        assert len(post.components) == 1

    def test_add_checklist_with_progress(self):
        """Test adding checklist with progress"""
        post = ComposablePost("text")
        post.add_checklist([{"text": "Task"}], show_progress=True)
        assert len(post.components) == 1

    def test_add_before_after(self):
        """Test adding before/after"""
        post = ComposablePost("text")
        result = post.add_before_after(["Old"], ["New"])
        assert result is post
        assert len(post.components) == 1

    def test_add_before_after_with_labels(self):
        """Test adding before/after with labels"""
        post = ComposablePost("text")
        post.add_before_after(["Old"], ["New"], labels={"before": "Before", "after": "After"})
        assert len(post.components) == 1

    def test_add_tip_box(self):
        """Test adding tip box"""
        post = ComposablePost("text")
        result = post.add_tip_box("Helpful tip")
        assert result is post
        assert len(post.components) == 1

    def test_add_tip_box_custom(self):
        """Test adding tip box with custom style"""
        post = ComposablePost("text")
        post.add_tip_box("Tip", title="Note", style="warning")
        assert len(post.components) == 1

    def test_add_stats_grid(self):
        """Test adding stats grid"""
        post = ComposablePost("text")
        result = post.add_stats_grid({"A": "1", "B": "2"})
        assert result is post
        assert len(post.components) == 1

    def test_add_stats_grid_custom(self):
        """Test adding stats grid with custom columns"""
        post = ComposablePost("text")
        post.add_stats_grid({"A": "1", "B": "2"}, columns=3)
        assert len(post.components) == 1

    def test_add_poll_preview(self):
        """Test adding poll preview"""
        post = ComposablePost("text")
        result = post.add_poll_preview("Question?", ["A", "B"])
        assert result is post
        assert len(post.components) == 1

    def test_add_feature_list(self):
        """Test adding feature list"""
        post = ComposablePost("text")
        result = post.add_feature_list([{"title": "Feature 1"}])
        assert result is post
        assert len(post.components) == 1

    def test_add_numbered_list(self):
        """Test adding numbered list"""
        post = ComposablePost("text")
        result = post.add_numbered_list(["Item 1", "Item 2"])
        assert result is post
        assert len(post.components) == 1

    def test_add_numbered_list_custom(self):
        """Test adding numbered list with custom style"""
        post = ComposablePost("text")
        post.add_numbered_list(["Item"], style="emoji_numbers", start=5)
        assert len(post.components) == 1


class TestComposablePostLayoutComponents:
    """Test adding layout components"""

    def test_add_separator(self):
        """Test adding separator"""
        post = ComposablePost("text")
        result = post.add_separator()
        assert result is post
        assert len(post.components) == 1

    def test_add_separator_custom(self):
        """Test adding separator with custom style"""
        post = ComposablePost("text")
        post.add_separator(style="dots")
        assert len(post.components) == 1


class TestComposablePostComposition:
    """Test post composition methods"""

    def test_compose_empty(self):
        """Test composing empty post"""
        post = ComposablePost("text")
        result = post.compose()
        assert result == ""

    def test_compose_single_component(self):
        """Test composing with single component"""
        post = ComposablePost("text")
        post.add_hook("question", "Why?")
        result = post.compose()
        assert "Why?" in result

    def test_compose_multiple_components(self):
        """Test composing with multiple components"""
        post = ComposablePost("text")
        post.add_hook("question", "Why?")
        post.add_body("Because.")
        post.add_cta("direct", "Click here")
        result = post.compose()
        assert "Why?" in result
        assert "Because." in result
        assert "Click here" in result

    def test_compose_with_separator(self):
        """Test composing with separator"""
        post = ComposablePost("text")
        post.add_body("Part 1")
        post.add_separator()
        post.add_body("Part 2")
        result = post.compose()
        assert "Part 1" in result
        assert "Part 2" in result

    def test_compose_too_long_raises_error(self):
        """Test compose raises error if too long"""
        post = ComposablePost("text")
        # Add content that exceeds max length (LinkedIn limit is 3000)
        # Need to add multiple components to exceed limit since Body has its own validation
        for i in range(6):
            post.add_body("x" * 500)  # 6 * 500 = 3000 chars + separators
        with pytest.raises(ValueError, match="exceeds.*character limit"):
            post.compose()

    def test_get_preview_short(self):
        """Test get_preview with short content"""
        post = ComposablePost("text")
        post.add_body("Short content")
        preview = post.get_preview(210)
        assert preview == "Short content"

    def test_get_preview_long(self):
        """Test get_preview with long content"""
        post = ComposablePost("text")
        post.add_body("A" * 300)
        preview = post.get_preview(210)
        assert len(preview) == 213  # 210 + "..."
        assert preview.endswith("...")


class TestComposablePostOptimization:
    """Test engagement optimization"""

    def test_optimize_adds_hook_if_missing(self):
        """Test optimize adds hook if missing"""
        theme = type("Theme", (), {"name": "professional", "hook_style": "question"})()
        post = ComposablePost("text", theme=theme)
        post.add_body("Content")
        post.optimize_for_engagement()
        # Should have hook + body + cta (optimize adds both)
        assert len(post.components) == 3

    def test_optimize_adds_cta_if_missing(self):
        """Test optimize adds CTA if missing"""
        theme = type("Theme", (), {"name": "professional", "cta_style": "curiosity"})()
        post = ComposablePost("text", theme=theme)
        post.add_body("Content")
        post.optimize_for_engagement()
        # Should have hook + body + cta
        assert len(post.components) == 3

    def test_optimize_does_not_add_if_present(self):
        """Test optimize does not add if hook/cta already present"""
        theme = type("Theme", (), {"name": "professional"})()
        post = ComposablePost("text", theme=theme)
        post.add_hook("question", "Why?")
        post.add_body("Content")
        post.add_cta("direct", "Act")
        post.optimize_for_engagement()
        # Should still have just 3 components
        assert len(post.components) == 3

    def test_optimize_without_theme(self):
        """Test optimize without theme does nothing"""
        post = ComposablePost("text")
        post.add_body("Content")
        post.optimize_for_engagement()
        # Should still have just 1 component
        assert len(post.components) == 1


class TestComposablePostToDict:
    """Test to_dict export"""

    def test_to_dict_basic(self):
        """Test basic to_dict"""
        post = ComposablePost("text")
        post.add_hook("question", "Why?")
        result = post.to_dict()
        assert result["post_type"] == "text"
        assert result["theme"] is None
        assert len(result["components"]) == 1
        assert "final_text" in result
        assert "character_count" in result
        assert "preview" in result

    def test_to_dict_with_theme(self):
        """Test to_dict with theme"""
        theme = type(
            "Theme",
            (),
            {
                "name": "professional",
                "line_break_style": "moderate",
                "emoji_level": "minimal",
                "controversy_level": "safe",
            },
        )()
        post = ComposablePost("text", theme=theme)
        post.add_hook("question", "Test")
        result = post.to_dict()
        assert result["theme"] == "professional"


class TestPostBuilder:
    """Test PostBuilder helper patterns"""

    def test_thought_leadership_post(self):
        """Test thought leadership pattern"""
        theme = type(
            "Theme",
            (),
            {
                "name": "professional",
                "controversy_level": "safe",
                "emoji_level": "minimal",
                "line_break_style": "moderate",
                "hashtag_strategy": "minimal",
            },
        )()
        post = PostBuilder.thought_leadership_post(
            hook_stat="95% agree",
            framework_name="3-Part Framework",
            framework_parts=["Part 1", "Part 2", "Part 3"],
            conclusion="Apply this today",
            theme=theme,
        )
        assert len(post.components) > 0
        result = post.compose()
        assert "95% agree" in result
        assert "3-Part Framework" in result

    def test_story_post(self):
        """Test story pattern"""
        theme = type(
            "Theme",
            (),
            {
                "name": "storyteller",
                "controversy_level": "safe",
                "emoji_level": "moderate",
                "line_break_style": "generous",
            },
        )()
        post = PostBuilder.story_post(
            hook="Let me tell you",
            problem="The problem was",
            journey="The journey",
            solution="The solution",
            lesson="The lesson learned",
            theme=theme,
        )
        assert len(post.components) > 0
        result = post.compose()
        assert "Let me tell you" in result
        assert "lesson learned" in result

    def test_listicle_post(self):
        """Test listicle pattern"""
        theme = type(
            "Theme",
            (),
            {
                "name": "personal_brand",
                "controversy_level": "safe",
                "emoji_level": "moderate",
                "line_break_style": "moderate",
            },
        )()
        post = PostBuilder.listicle_post(
            hook="5 key points",
            items=["Point 1", "Point 2", "Point 3"],
            conclusion="That's it",
            theme=theme,
        )
        assert len(post.components) > 0
        result = post.compose()
        assert "5 key points" in result
        assert "Point 1" in result

    def test_comparison_post(self):
        """Test comparison pattern"""
        theme = type(
            "Theme",
            (),
            {
                "name": "technical_expert",
                "controversy_level": "safe",
                "emoji_level": "none",
                "line_break_style": "tight",
            },
        )()
        post = PostBuilder.comparison_post(
            hook="Which is better?",
            option_a="Option A features",
            option_b="Option B features",
            recommendation="I recommend A",
            theme=theme,
        )
        assert len(post.components) > 0
        result = post.compose()
        assert "Which is better?" in result
        assert "recommend" in result


class TestComposablePostFluent:
    """Test fluent interface chaining"""

    def test_fluent_chaining(self):
        """Test method chaining"""
        post = (
            ComposablePost("text")
            .add_hook("question", "Why?")
            .add_body("Content")
            .add_separator()
            .add_cta("direct", "Act")
            .add_hashtags(["Test"])
        )
        assert len(post.components) == 5
        result = post.compose()
        assert "Why?" in result
        assert "Content" in result
        assert "Act" in result
