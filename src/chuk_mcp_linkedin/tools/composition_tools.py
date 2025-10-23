# src/chuk_mcp_linkedin/tools/composition_tools.py
"""
Composition tools for building LinkedIn posts.

Thin wrapper around ComposablePost for MCP tool integration.
"""

from typing import Any, Dict, Optional, List

from ..posts.composition import ComposablePost
from ..themes.theme_manager import ThemeManager


def _get_or_create_post(manager: Any) -> ComposablePost:
    """Get or create ComposablePost instance for current draft."""
    draft = manager.get_current_draft()
    if not draft:
        raise ValueError("No active draft")

    # Get or create ComposablePost instance
    if not hasattr(draft.content, "get") or "_composable_post" not in draft.content:
        # Create new ComposablePost
        theme = None
        if draft.theme:
            theme_mgr = ThemeManager()
            theme = theme_mgr.get_theme(draft.theme)

        post = ComposablePost(draft.post_type, theme=theme, variant_config=draft.variant_config)
        draft.content["_composable_post"] = post

    result: ComposablePost = draft.content["_composable_post"]
    return result


def register_composition_tools(mcp: Any, manager: Any) -> Dict[str, Any]:
    """Register composition tools with the MCP server"""

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_hook(hook_type: str, content: str) -> str:
        """
        Add opening hook to current draft.

        Args:
            hook_type: Type of hook (question, stat, story, controversy, list, curiosity)
            content: Hook text

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_hook(hook_type, content)
            return f"Added {hook_type} hook to draft"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_body(content: str, structure: str = "linear") -> str:
        """
        Add main content body to current draft.

        Args:
            content: Body text
            structure: Content structure (linear, listicle, framework, story_arc, comparison)

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_body(content, structure=structure)
            return f"Added body with {structure} structure"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_cta(cta_type: str, text: str) -> str:
        """
        Add call-to-action to current draft.

        Args:
            cta_type: Type of CTA (direct, curiosity, action, share, soft)
            text: CTA text

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_cta(cta_type, text)
            return f"Added {cta_type} CTA"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_bar_chart(
        data: Dict[str, int], title: Optional[str] = None, unit: str = ""
    ) -> str:
        """
        Add horizontal bar chart using colored emoji squares.

        Args:
            data: Chart data with labels and integer values (e.g., {"AI-Assisted": 12, "Code Review": 6})
            title: Optional chart title
            unit: Optional unit label (e.g., "hours", "users", "tasks")

        Returns:
            Success message

        Example:
            data={"AI-Assisted": 12, "Code Review": 6, "Documentation": 4}, unit="hours"
        """
        try:
            post = _get_or_create_post(manager)
            post.add_bar_chart(data, title=title, unit=unit)
            return f"Added bar chart with {len(data)} bars"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_metrics_chart(data: Dict[str, str], title: Optional[str] = None) -> str:
        """
        Add key metrics chart with emoji indicators (✅/❌).

        Args:
            data: Metrics data with labels and string values (e.g., {"Faster problem-solving": "67%"})
            title: Optional chart title

        Returns:
            Success message

        Example:
            data={"Faster problem-solving": "67%", "Better learning": "89%"}
        """
        try:
            post = _get_or_create_post(manager)
            post.add_metrics_chart(data, title=title)
            return f"Added metrics chart with {len(data)} metrics"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_comparison_chart(
        data: Dict[str, Any], title: Optional[str] = None
    ) -> str:
        """
        Add side-by-side A vs B comparison chart.

        Args:
            data: Comparison data with 2+ options (values can be strings or lists)
            title: Optional chart title

        Returns:
            Success message

        Example:
            data={
                "Traditional Dev": ["Slower iterations", "Manual testing"],
                "AI-Assisted Dev": ["Faster prototyping", "Automated tests"]
            }
        """
        try:
            post = _get_or_create_post(manager)
            post.add_comparison_chart(data, title=title)
            return f"Added comparison chart with {len(data)} options"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_progress_chart(data: Dict[str, int], title: Optional[str] = None) -> str:
        """
        Add progress bars chart for tracking completion (0-100%).

        Args:
            data: Progress data with labels and percentage values (e.g., {"Completion": 75})
            title: Optional chart title

        Returns:
            Success message

        Example:
            data={"Completion": 75, "Testing": 50, "Documentation": 30}
        """
        try:
            post = _get_or_create_post(manager)
            post.add_progress_chart(data, title=title)
            return f"Added progress chart with {len(data)} items"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_ranking_chart(
        data: Dict[str, str], title: Optional[str] = None, show_medals: bool = True
    ) -> str:
        """
        Add ranking/leaderboard chart with medals (🥇🥈🥉) for top 3.

        Args:
            data: Ranking data with labels and descriptions (e.g., {"Python": "1M users"})
            title: Optional chart title
            show_medals: Show medal emojis for top 3 positions (default: true)

        Returns:
            Success message

        Example:
            data={"Python": "1M users", "JavaScript": "900K users", "Rust": "500K users"}
        """
        try:
            post = _get_or_create_post(manager)
            post.add_ranking_chart(data, title=title, show_medals=show_medals)
            return f"Added ranking chart with {len(data)} items"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_quote(text: str, author: str, source: Optional[str] = None) -> str:
        """
        Add a quote or testimonial to current draft.

        Args:
            text: Quote text (max 500 chars)
            author: Quote author name
            source: Optional source/attribution (e.g., "CTO at TechCorp")

        Returns:
            Success message

        Example:
            text="AI has transformed our development process",
            author="Sarah Chen",
            source="CTO at TechCorp"
        """
        try:
            post = _get_or_create_post(manager)
            post.add_quote(text, author, source=source)
            return f"Added quote from {author}"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_big_stat(number: str, label: str, context: Optional[str] = None) -> str:
        """
        Add a big eye-catching statistic to current draft.

        Args:
            number: Statistic number (e.g., "2.5M", "340%", "10x")
            label: Description of what the number represents
            context: Optional additional context (e.g., "↑ 340% YoY growth")

        Returns:
            Success message

        Example:
            number="2.5M",
            label="developers using AI tools daily",
            context="↑ 340% growth year-over-year"
        """
        try:
            post = _get_or_create_post(manager)
            post.add_big_stat(number, label, context=context)
            return f"Added big stat: {number}"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_timeline(
        steps: Dict[str, str], title: Optional[str] = None, style: str = "arrow"
    ) -> str:
        """
        Add a timeline or step-by-step process to current draft.

        Args:
            steps: Timeline steps with dates/labels and descriptions
            title: Optional timeline title
            style: Timeline style (arrow, numbered, dated) - default: arrow

        Returns:
            Success message

        Example:
            steps={"Jan 2023": "Launched MVP", "Jun 2023": "Reached 1K users"},
            title="OUR JOURNEY",
            style="arrow"
        """
        try:
            post = _get_or_create_post(manager)
            post.add_timeline(steps, title=title, style=style)
            return f"Added timeline with {len(steps)} steps"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_key_takeaway(
        message: str, title: str = "KEY TAKEAWAY", style: str = "box"
    ) -> str:
        """
        Add a highlighted key insight or TLDR to current draft.

        Args:
            message: The key takeaway message (max 500 chars)
            title: Box title (default: "KEY TAKEAWAY")
            style: Display style (box, highlight, simple) - default: box

        Returns:
            Success message

        Example:
            message="Focus on solving real problems, not chasing trends",
            title="KEY TAKEAWAY",
            style="box"
        """
        try:
            post = _get_or_create_post(manager)
            post.add_key_takeaway(message, title=title, style=style)
            return "Added key takeaway"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_pro_con(
        pros: List[str], cons: List[str], title: Optional[str] = None
    ) -> str:
        """
        Add a pros & cons comparison to current draft.

        Args:
            pros: List of pros/advantages
            cons: List of cons/disadvantages
            title: Optional comparison title

        Returns:
            Success message

        Example:
            pros=["40% faster development", "Better code quality"],
            cons=["Initial learning curve", "$20-40 per developer/month"],
            title="AI CODING TOOLS"
        """
        try:
            post = _get_or_create_post(manager)
            post.add_pro_con(pros, cons, title=title)
            return f"Added pro/con comparison ({len(pros)} pros, {len(cons)} cons)"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_separator(style: str = "line") -> str:
        """
        Add a visual separator to current draft.

        Args:
            style: Separator style (line, dots, wave) - default: line

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_separator(style=style)
            return f"Added {style} separator"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_checklist(
        items: List[Dict[str, Any]], title: Optional[str] = None, show_progress: bool = False
    ) -> str:
        """
        Add checklist with checkmarks to current draft.

        Args:
            items: Checklist items (each with 'text' and optional 'checked')
            title: Optional checklist title
            show_progress: Show completion progress

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_checklist(items, title=title, show_progress=show_progress)
            return f"Added checklist with {len(items)} items"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_before_after(
        before: List[str],
        after: List[str],
        title: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Add before/after transformation comparison.

        Args:
            before: List of 'before' items
            after: List of 'after' items
            title: Optional comparison title
            labels: Custom labels (e.g., {"before": "Old Way", "after": "New Way"})

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_before_after(before, after, title=title, labels=labels)
            return "Added before/after comparison"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_tip_box(
        message: str, title: Optional[str] = None, style: str = "info"
    ) -> str:
        """
        Add highlighted tip/note box.

        Args:
            message: Tip or note message
            title: Optional tip box title
            style: Box style (info, tip, warning, success)

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_tip_box(message, title=title, style=style)
            return f"Added {style} tip box"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_stats_grid(
        stats: Dict[str, str], title: Optional[str] = None, columns: int = 2
    ) -> str:
        """
        Add multi-stat grid display.

        Args:
            stats: Statistics as key-value pairs
            title: Optional grid title
            columns: Number of columns (1-4)

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_stats_grid(stats, title=title, columns=columns)
            return f"Added stats grid with {len(stats)} stats"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_poll_preview(question: str, options: List[str]) -> str:
        """
        Add poll preview for engagement.

        Args:
            question: Poll question
            options: Poll options (2-4)

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_poll_preview(question, options)
            return f"Added poll with {len(options)} options"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_feature_list(
        features: List[Dict[str, str]], title: Optional[str] = None
    ) -> str:
        """
        Add feature list with icons and descriptions.

        Args:
            features: Features (each with 'title', optional 'icon' and 'description')
            title: Optional feature list title

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_feature_list(features, title=title)
            return f"Added feature list with {len(features)} features"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_numbered_list(
        items: List[str], title: Optional[str] = None, style: str = "numbers", start: int = 1
    ) -> str:
        """
        Add enhanced numbered list.

        Args:
            items: List items
            title: Optional list title
            style: Numbering style (numbers, emoji_numbers, bold_numbers)
            start: Starting number

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_numbered_list(items, title=title, style=style, start=start)
            return f"Added numbered list with {len(items)} items"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_add_hashtags(tags: List[str], placement: str = "end") -> str:
        """
        Add hashtags to current draft.

        Args:
            tags: List of hashtags (without #)
            placement: Where to place hashtags (inline, mid, end, first_comment)

        Returns:
            Success message
        """
        try:
            post = _get_or_create_post(manager)
            post.add_hashtags(tags, placement=placement)
            return f"Added {len(tags)} hashtags"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_compose_post(optimize: bool = True) -> str:
        """
        Compose post from components in current draft.

        Args:
            optimize: Optimize for engagement (default: true)

        Returns:
            Composed post text
        """
        try:
            post = _get_or_create_post(manager)

            # Optimize if requested
            if optimize:
                post.optimize_for_engagement()

            # Compose final text
            final_text = post.compose()

            # Update draft with composed text
            draft = manager.get_current_draft()
            draft.content["composed_text"] = final_text
            manager.update_draft(draft.draft_id, content=draft.content)

            return f"Composed post ({len(final_text)} chars):\n\n{final_text}"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_get_preview() -> str:
        """
        Get preview of current draft (first 210 chars).

        Returns:
            Preview text showing what appears before "see more"
        """
        try:
            post = _get_or_create_post(manager)
            preview = post.get_preview(210)
            return f"Preview (first 210 chars):\n\n{preview}"
        except ValueError as e:
            return str(e)

    @mcp.tool  # type: ignore[misc]
    async def linkedin_preview_html(
        output_path: Optional[str] = None, open_browser: bool = True
    ) -> str:
        """
        Generate HTML preview of current draft and open in browser.

        Args:
            output_path: Optional custom output path for HTML file
            open_browser: Auto-open preview in browser (default: true)

        Returns:
            Path to generated preview file
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Generate preview
        saved_path = manager.generate_html_preview(draft.draft_id, output_path)

        if not saved_path:
            return "Failed to generate preview"

        # Open in browser if requested
        if open_browser:
            import webbrowser
            import os

            # Convert to file:// URL
            file_url = f"file://{os.path.abspath(saved_path)}"
            webbrowser.open(file_url)

            return f"Preview generated and opened in browser:\n{saved_path}"
        else:
            return f"Preview generated:\n{saved_path}\n\nOpen in browser to view."

    @mcp.tool  # type: ignore[misc]
    async def linkedin_export_draft() -> str:
        """
        Export current draft as JSON.

        Returns:
            JSON string of draft
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        export_json = manager.export_draft(draft.draft_id)
        return export_json or "Export failed"

    return {
        # Content components
        "linkedin_add_hook": linkedin_add_hook,
        "linkedin_add_body": linkedin_add_body,
        "linkedin_add_cta": linkedin_add_cta,
        "linkedin_add_hashtags": linkedin_add_hashtags,
        # Data visualization components
        "linkedin_add_bar_chart": linkedin_add_bar_chart,
        "linkedin_add_metrics_chart": linkedin_add_metrics_chart,
        "linkedin_add_comparison_chart": linkedin_add_comparison_chart,
        "linkedin_add_progress_chart": linkedin_add_progress_chart,
        "linkedin_add_ranking_chart": linkedin_add_ranking_chart,
        # Feature components
        "linkedin_add_quote": linkedin_add_quote,
        "linkedin_add_big_stat": linkedin_add_big_stat,
        "linkedin_add_timeline": linkedin_add_timeline,
        "linkedin_add_key_takeaway": linkedin_add_key_takeaway,
        "linkedin_add_pro_con": linkedin_add_pro_con,
        "linkedin_add_checklist": linkedin_add_checklist,
        "linkedin_add_before_after": linkedin_add_before_after,
        "linkedin_add_tip_box": linkedin_add_tip_box,
        "linkedin_add_stats_grid": linkedin_add_stats_grid,
        "linkedin_add_poll_preview": linkedin_add_poll_preview,
        "linkedin_add_feature_list": linkedin_add_feature_list,
        "linkedin_add_numbered_list": linkedin_add_numbered_list,
        # Layout components
        "linkedin_add_separator": linkedin_add_separator,
        # Composition & preview
        "linkedin_compose_post": linkedin_compose_post,
        "linkedin_get_preview": linkedin_get_preview,
        "linkedin_preview_html": linkedin_preview_html,
        "linkedin_export_draft": linkedin_export_draft,
    }
