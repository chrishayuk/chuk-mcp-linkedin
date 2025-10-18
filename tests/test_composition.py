"""
Tests for composition system.
"""

import pytest
from chuk_mcp_linkedin.composition import (
    Hook,
    Body,
    CallToAction,
    Hashtags,
    Separator,
    ComposablePost,
    PostBuilder,
)
from chuk_mcp_linkedin import ThemeManager


class TestHook:
    """Test Hook component"""

    def test_hook_creation(self):
        """Test creating a hook"""
        hook = Hook("stat", "95% of marketers use LinkedIn")
        assert hook.hook_type == "stat"
        assert hook.content == "95% of marketers use LinkedIn"

    def test_hook_render(self):
        """Test rendering a hook"""
        hook = Hook("stat", "95% of marketers use LinkedIn")
        rendered = hook.render()
        assert rendered == "95% of marketers use LinkedIn"

    def test_hook_render_with_controversial_theme(self):
        """Test rendering controversial hook with bold theme"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("contrarian_voice")
        hook = Hook("controversy", "Stop doing cold calls", theme)
        rendered = hook.render()
        assert "🚨" in rendered

    def test_hook_validate_success(self):
        """Test hook validation with valid content"""
        hook = Hook("stat", "95% of marketers use LinkedIn")
        assert hook.validate() is True

    def test_hook_validate_empty(self):
        """Test hook validation with empty content"""
        hook = Hook("stat", "")
        assert hook.validate() is False

    def test_hook_validate_too_long(self):
        """Test hook validation with too long content"""
        hook = Hook("stat", "x" * 201)
        assert hook.validate() is False


class TestBody:
    """Test Body component"""

    def test_body_creation(self):
        """Test creating a body"""
        body = Body("Content here", structure="linear")
        assert body.content == "Content here"
        assert body.structure == "linear"

    def test_body_render_linear(self):
        """Test rendering linear body"""
        body = Body("Paragraph 1\n\nParagraph 2", structure="linear")
        rendered = body.render()
        assert "Paragraph 1" in rendered
        assert "Paragraph 2" in rendered

    def test_body_render_listicle(self):
        """Test rendering listicle body"""
        body = Body("Item 1\nItem 2\nItem 3", structure="listicle")
        rendered = body.render()
        assert "→" in rendered or "-" in rendered

    def test_body_render_listicle_with_theme(self):
        """Test rendering listicle with theme"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("technical_expert")
        body = Body("Item 1\nItem 2", structure="listicle", theme=theme)
        rendered = body.render()
        assert "-" in rendered  # Technical theme uses minimal emojis

    def test_body_render_framework(self):
        """Test rendering framework body"""
        body = Body("S - Strategy||H - Hustle||A - Action", structure="framework")
        rendered = body.render()
        assert "S - Strategy" in rendered

    def test_body_render_story_arc(self):
        """Test rendering story arc body"""
        body = Body("Problem\n\nJourney\n\nSolution", structure="story_arc")
        rendered = body.render()
        assert "Problem" in rendered

    def test_body_render_comparison(self):
        """Test rendering comparison body"""
        body = Body("Old way||New way", structure="comparison")
        rendered = body.render()
        assert "❌" in rendered
        assert "✅" in rendered

    def test_body_validate_success(self):
        """Test body validation"""
        body = Body("Content", structure="linear")
        assert body.validate() is True

    def test_body_validate_empty(self):
        """Test body validation with empty content"""
        body = Body("", structure="linear")
        assert body.validate() is False


class TestCallToAction:
    """Test CallToAction component"""

    def test_cta_creation(self):
        """Test creating a CTA"""
        cta = CallToAction("curiosity", "What do you think?")
        assert cta.cta_type == "curiosity"
        assert cta.text == "What do you think?"

    def test_cta_render_plain(self):
        """Test rendering CTA without theme"""
        cta = CallToAction("curiosity", "What do you think?")
        rendered = cta.render()
        assert rendered == "What do you think?"

    def test_cta_render_with_emoji_theme(self):
        """Test rendering CTA with emoji theme"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("personal_brand")
        cta = CallToAction("curiosity", "What do you think?", theme)
        rendered = cta.render()
        assert "🤔" in rendered

    def test_cta_validate_success(self):
        """Test CTA validation"""
        cta = CallToAction("curiosity", "What do you think?")
        assert cta.validate() is True

    def test_cta_validate_empty(self):
        """Test CTA validation with empty text"""
        cta = CallToAction("curiosity", "")
        assert cta.validate() is False


class TestHashtags:
    """Test Hashtags component"""

    def test_hashtags_creation(self):
        """Test creating hashtags"""
        hashtags = Hashtags(["Marketing", "LinkedIn", "Tips"])
        assert len(hashtags.tags) == 3

    def test_hashtags_render(self):
        """Test rendering hashtags"""
        hashtags = Hashtags(["Marketing", "LinkedIn"])
        rendered = hashtags.render()
        assert "#Marketing" in rendered
        assert "#LinkedIn" in rendered

    def test_hashtags_limit_to_optimal(self):
        """Test hashtags limited to optimal count"""
        hashtags = Hashtags(["Tag1", "Tag2", "Tag3", "Tag4", "Tag5", "Tag6", "Tag7"])
        rendered = hashtags.render()
        # Should limit to 5 tags
        assert rendered.count("#") == 5

    def test_hashtags_with_minimal_theme(self):
        """Test hashtags with minimal theme"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")
        hashtags = Hashtags(["Tag1", "Tag2", "Tag3", "Tag4"], theme=theme)
        rendered = hashtags.render()
        # Minimal theme limits to 3
        assert rendered.count("#") == 3

    def test_hashtags_inline_placement(self):
        """Test inline hashtag placement"""
        hashtags = Hashtags(["Marketing"], placement="inline")
        rendered = hashtags.render()
        assert not rendered.startswith("\n\n")

    def test_hashtags_validate_success(self):
        """Test hashtags validation"""
        hashtags = Hashtags(["Marketing", "LinkedIn"])
        assert hashtags.validate() is True

    def test_hashtags_validate_empty(self):
        """Test hashtags validation with empty list"""
        hashtags = Hashtags([])
        assert hashtags.validate() is False


class TestSeparator:
    """Test Separator component"""

    def test_separator_creation(self):
        """Test creating a separator"""
        separator = Separator("line")
        assert separator.style == "line"

    def test_separator_render(self):
        """Test rendering separator"""
        separator = Separator("line")
        rendered = separator.render()
        assert "---" in rendered

    def test_separator_validate(self):
        """Test separator validation"""
        separator = Separator("line")
        assert separator.validate() is True


class TestComposablePost:
    """Test ComposablePost"""

    def test_composable_post_creation(self):
        """Test creating a composable post"""
        post = ComposablePost("text")
        assert post.post_type == "text"
        assert len(post.components) == 0

    def test_composable_post_add_hook(self):
        """Test adding hook to post"""
        post = ComposablePost("text")
        post.add_hook("stat", "95% of marketers...")
        assert len(post.components) == 1
        assert isinstance(post.components[0], Hook)

    def test_composable_post_add_body(self):
        """Test adding body to post"""
        post = ComposablePost("text")
        post.add_body("Content here")
        assert len(post.components) == 1
        assert isinstance(post.components[0], Body)

    def test_composable_post_add_cta(self):
        """Test adding CTA to post"""
        post = ComposablePost("text")
        post.add_cta("curiosity", "What do you think?")
        assert len(post.components) == 1
        assert isinstance(post.components[0], CallToAction)

    def test_composable_post_add_hashtags(self):
        """Test adding hashtags to post"""
        post = ComposablePost("text")
        post.add_hashtags(["Marketing", "LinkedIn"])
        assert len(post.components) == 1
        assert isinstance(post.components[0], Hashtags)

    def test_composable_post_add_separator(self):
        """Test adding separator to post"""
        post = ComposablePost("text")
        post.add_separator("line")
        assert len(post.components) == 1
        assert isinstance(post.components[0], Separator)

    def test_composable_post_fluent_api(self):
        """Test fluent API chaining"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")

        post = (
            ComposablePost("text", theme=theme)
            .add_hook("stat", "95% of marketers...")
            .add_body("Content here")
            .add_cta("curiosity", "Thoughts?")
            .add_hashtags(["Marketing"])
        )

        assert len(post.components) == 4

    def test_composable_post_compose(self):
        """Test composing final post"""
        post = ComposablePost("text")
        post.add_hook("stat", "95% of marketers use LinkedIn")
        post.add_body("Here's why that matters")
        post.add_cta("curiosity", "What do you think?")

        final_text = post.compose()
        assert "95% of marketers" in final_text
        assert "why that matters" in final_text
        assert "What do you think?" in final_text

    def test_composable_post_get_preview(self):
        """Test getting preview"""
        post = ComposablePost("text")
        post.add_hook("stat", "x" * 300)

        preview = post.get_preview(210)
        assert len(preview) <= 213  # 210 + "..."

    def test_composable_post_optimize_for_engagement(self):
        """Test optimizing post for engagement"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")

        post = ComposablePost("text", theme=theme)
        post.add_body("Content")
        post.optimize_for_engagement()

        # Should have added hook and CTA
        has_hook = any(isinstance(c, Hook) for c in post.components)
        has_cta = any(isinstance(c, CallToAction) for c in post.components)
        assert has_hook
        assert has_cta

    def test_composable_post_to_dict(self):
        """Test converting post to dictionary"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")

        post = ComposablePost("text", theme=theme)
        post.add_hook("stat", "95% of marketers...")
        post.add_body("Content")

        post_dict = post.to_dict()
        assert post_dict["post_type"] == "text"
        assert post_dict["theme"] == "Thought Leader"
        assert len(post_dict["components"]) == 2

    def test_composable_post_too_long_raises_error(self):
        """Test composing post that's too long raises error"""
        post = ComposablePost("text")
        # Add multiple components that together exceed limit
        # Hook allows 200 chars, Body allows 2800 chars
        post.add_hook("stat", "x" * 200)
        post.add_body("y" * 1500)
        post.add_body("z" * 1500)  # Total > 3000 with newlines

        with pytest.raises(ValueError, match="exceeds.*character limit"):
            post.compose()


class TestPostBuilder:
    """Test PostBuilder patterns"""

    def test_thought_leadership_post(self):
        """Test thought leadership builder"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")

        post = PostBuilder.thought_leadership_post(
            hook_stat="95% of leaders fail at this",
            framework_name="SMART Goals",
            framework_parts=[
                "S - Specific",
                "M - Measurable",
                "A - Achievable",
                "R - Relevant",
                "T - Time-bound",
            ],
            conclusion="Use this framework to succeed",
            theme=theme,
        )

        final_text = post.compose()
        assert "95% of leaders" in final_text
        assert "S - Specific" in final_text

    def test_story_post(self):
        """Test story builder"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("storyteller")

        post = PostBuilder.story_post(
            hook="Last year changed everything",
            problem="I was struggling with burnout",
            journey="I tried many solutions",
            solution="Finally found balance",
            lesson="Prioritize your health",
            theme=theme,
        )

        final_text = post.compose()
        assert "Last year" in final_text
        assert "burnout" in final_text

    def test_listicle_post(self):
        """Test listicle builder"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")

        post = PostBuilder.listicle_post(
            hook="5 ways to improve your LinkedIn",
            items=[
                "Optimize your profile",
                "Post consistently",
                "Engage with others",
                "Use hashtags wisely",
                "Track your metrics",
            ],
            conclusion="Start with just one",
            theme=theme,
        )

        final_text = post.compose()
        assert "5 ways" in final_text
        assert "Optimize your profile" in final_text

    def test_comparison_post(self):
        """Test comparison builder"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("thought_leader")

        post = PostBuilder.comparison_post(
            hook="Which is better?",
            option_a="Traditional marketing",
            option_b="LinkedIn marketing",
            recommendation="LinkedIn wins for B2B",
            theme=theme,
        )

        final_text = post.compose()
        assert "Which is better?" in final_text
        assert "❌" in final_text
        assert "✅" in final_text


class TestIntegration:
    """Integration tests for composition"""

    def test_full_post_with_all_components(self):
        """Test creating a full post with all components"""
        theme_manager = ThemeManager()
        theme = theme_manager.get_theme("personal_brand")

        # Create a longer post to ensure preview is shorter
        long_body = "Here's what happened " * 20  # Make it longer

        post = (
            ComposablePost("text", theme=theme)
            .add_hook("story", "Last year I made a mistake")
            .add_body(long_body, structure="linear")
            .add_separator("line")
            .add_body("Item 1\nItem 2\nItem 3", structure="listicle")
            .add_separator("dots")
            .add_cta("soft", "What's your experience?")
            .add_hashtags(["PersonalBrand", "Learning"])
        )

        final_text = post.compose()
        preview = post.get_preview()

        assert len(final_text) > len(preview)
        assert "Last year" in final_text
        assert "#PersonalBrand" in final_text

    def test_theme_influences_rendering(self):
        """Test that theme influences component rendering"""
        theme_manager = ThemeManager()

        # Technical expert: no emojis
        tech_theme = theme_manager.get_theme("technical_expert")
        tech_post = ComposablePost("text", theme=tech_theme)
        tech_post.add_cta("curiosity", "Thoughts?")
        tech_text = tech_post.compose()

        # Entertainer: lots of emojis
        fun_theme = theme_manager.get_theme("entertainer")
        fun_post = ComposablePost("text", theme=fun_theme)
        fun_post.add_cta("curiosity", "Thoughts?")
        fun_text = fun_post.compose()

        # Fun post should have more emojis
        assert fun_text.count("🤔") >= tech_text.count("🤔")
