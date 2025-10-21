"""
Composition tools for building LinkedIn posts.

Handles post composition, component assembly, and preview generation.
"""

import json
from ..models import (
    BarChartData,
    MetricsChartData,
    ComparisonChartData,
    ProgressChartData,
    RankingChartData,
    QuoteData,
    BigStatData,
    TimelineData,
    KeyTakeawayData,
    ProConData,
    ChecklistData,
    BeforeAfterData,
    TipBoxData,
    StatsGridData,
    PollPreviewData,
    FeatureListData,
    NumberedListData,
)


def register_composition_tools(mcp, manager):
    """Register composition tools with the MCP server"""

    @mcp.tool
    async def linkedin_add_hook(hook_type: str, content: str) -> str:
        """
        Add opening hook to current draft.

        Args:
            hook_type: Type of hook (question, stat, story, controversy, list, curiosity)
            content: Hook text

        Returns:
            Success message
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft. Create one first with linkedin_create."

        hook_data = {"type": hook_type, "content": content}
        draft.content.setdefault("components", []).append(
            {"component": "hook", **hook_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added {hook_type} hook to draft"

    @mcp.tool
    async def linkedin_add_body(content: str, structure: str = "linear") -> str:
        """
        Add main content body to current draft.

        Args:
            content: Body text
            structure: Content structure (linear, listicle, framework, story_arc, comparison)

        Returns:
            Success message
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        body_data = {"content": content, "structure": structure}
        draft.content.setdefault("components", []).append(
            {"component": "body", **body_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added body with {structure} structure"

    @mcp.tool
    async def linkedin_add_cta(cta_type: str, text: str) -> str:
        """
        Add call-to-action to current draft.

        Args:
            cta_type: Type of CTA (direct, curiosity, action, share, soft)
            text: CTA text

        Returns:
            Success message
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        cta_data = {"type": cta_type, "text": text}
        draft.content.setdefault("components", []).append({"component": "cta", **cta_data})
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added {cta_type} CTA"

    @mcp.tool
    async def linkedin_add_bar_chart(
        data: dict, title: str = None, unit: str = ""
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            chart_model = BarChartData(data=data, title=title, unit=unit)
        except Exception as e:
            return f"Validation error: {str(e)}"

        chart_data = {
            "data": chart_model.data,
            "title": chart_model.title,
            "unit": chart_model.unit
        }
        draft.content.setdefault("components", []).append(
            {"component": "bar_chart", **chart_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added bar chart with {len(data)} bars"

    @mcp.tool
    async def linkedin_add_metrics_chart(
        data: dict, title: str = None
    ) -> str:
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            chart_model = MetricsChartData(data=data, title=title)
        except Exception as e:
            return f"Validation error: {str(e)}"

        chart_data = {
            "data": chart_model.data,
            "title": chart_model.title
        }
        draft.content.setdefault("components", []).append(
            {"component": "metrics_chart", **chart_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added metrics chart with {len(data)} metrics"

    @mcp.tool
    async def linkedin_add_comparison_chart(
        data: dict, title: str = None
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            chart_model = ComparisonChartData(data=data, title=title)
        except Exception as e:
            return f"Validation error: {str(e)}"

        chart_data = {
            "data": chart_model.data,
            "title": chart_model.title
        }
        draft.content.setdefault("components", []).append(
            {"component": "comparison_chart", **chart_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added comparison chart with {len(data)} options"

    @mcp.tool
    async def linkedin_add_progress_chart(
        data: dict, title: str = None
    ) -> str:
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            chart_model = ProgressChartData(data=data, title=title)
        except Exception as e:
            return f"Validation error: {str(e)}"

        chart_data = {
            "data": chart_model.data,
            "title": chart_model.title
        }
        draft.content.setdefault("components", []).append(
            {"component": "progress_chart", **chart_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added progress chart with {len(data)} items"

    @mcp.tool
    async def linkedin_add_ranking_chart(
        data: dict, title: str = None, show_medals: bool = True
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            chart_model = RankingChartData(data=data, title=title, show_medals=show_medals)
        except Exception as e:
            return f"Validation error: {str(e)}"

        chart_data = {
            "data": chart_model.data,
            "title": chart_model.title,
            "show_medals": chart_model.show_medals
        }
        draft.content.setdefault("components", []).append(
            {"component": "ranking_chart", **chart_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added ranking chart with {len(data)} items"

    @mcp.tool
    async def linkedin_add_quote(
        text: str, author: str, source: str = None
    ) -> str:
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            quote_model = QuoteData(text=text, author=author, source=source)
        except Exception as e:
            return f"Validation error: {str(e)}"

        quote_data = {
            "text": quote_model.text,
            "author": quote_model.author,
            "source": quote_model.source
        }
        draft.content.setdefault("components", []).append(
            {"component": "quote", **quote_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added quote from {author}"

    @mcp.tool
    async def linkedin_add_big_stat(
        number: str, label: str, context: str = None
    ) -> str:
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            stat_model = BigStatData(number=number, label=label, context=context)
        except Exception as e:
            return f"Validation error: {str(e)}"

        stat_data = {
            "number": stat_model.number,
            "label": stat_model.label,
            "context": stat_model.context
        }
        draft.content.setdefault("components", []).append(
            {"component": "big_stat", **stat_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added big stat: {number}"

    @mcp.tool
    async def linkedin_add_timeline(
        steps: dict, title: str = None, style: str = "arrow"
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            timeline_model = TimelineData(steps=steps, title=title, style=style)
        except Exception as e:
            return f"Validation error: {str(e)}"

        timeline_data = {
            "steps": timeline_model.steps,
            "title": timeline_model.title,
            "style": timeline_model.style
        }
        draft.content.setdefault("components", []).append(
            {"component": "timeline", **timeline_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added timeline with {len(steps)} steps"

    @mcp.tool
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            takeaway_model = KeyTakeawayData(message=message, title=title, style=style)
        except Exception as e:
            return f"Validation error: {str(e)}"

        takeaway_data = {
            "message": takeaway_model.message,
            "title": takeaway_model.title,
            "style": takeaway_model.style
        }
        draft.content.setdefault("components", []).append(
            {"component": "key_takeaway", **takeaway_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added key takeaway"

    @mcp.tool
    async def linkedin_add_pro_con(
        pros: list[str], cons: list[str], title: str = None
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Validate with Pydantic
        try:
            procon_model = ProConData(pros=pros, cons=cons, title=title)
        except Exception as e:
            return f"Validation error: {str(e)}"

        procon_data = {
            "pros": procon_model.pros,
            "cons": procon_model.cons,
            "title": procon_model.title
        }
        draft.content.setdefault("components", []).append(
            {"component": "pro_con", **procon_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added pro/con comparison ({len(pros)} pros, {len(cons)} cons)"

    @mcp.tool
    async def linkedin_add_separator(style: str = "line") -> str:
        """
        Add a visual separator to current draft.

        Args:
            style: Separator style (line, dots, wave) - default: line

        Returns:
            Success message
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        separator_data = {"style": style}
        draft.content.setdefault("components", []).append(
            {"component": "separator", **separator_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added {style} separator"

    @mcp.tool
    async def linkedin_add_checklist(
        items: list[dict], title: str = None, show_progress: bool = False
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        try:
            checklist_model = ChecklistData(items=items, title=title, show_progress=show_progress)
        except Exception as e:
            return f"Validation error: {str(e)}"

        checklist_data = {
            "items": checklist_model.items,
            "title": checklist_model.title,
            "show_progress": checklist_model.show_progress
        }
        draft.content.setdefault("components", []).append(
            {"component": "checklist", **checklist_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added checklist with {len(items)} items"

    @mcp.tool
    async def linkedin_add_before_after(
        before: list[str], after: list[str], title: str = None, labels: dict = None
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        try:
            before_after_model = BeforeAfterData(before=before, after=after, title=title, labels=labels)
        except Exception as e:
            return f"Validation error: {str(e)}"

        before_after_data = {
            "before": before_after_model.before,
            "after": before_after_model.after,
            "title": before_after_model.title,
            "labels": before_after_model.labels
        }
        draft.content.setdefault("components", []).append(
            {"component": "before_after", **before_after_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added before/after comparison"

    @mcp.tool
    async def linkedin_add_tip_box(
        message: str, title: str = None, style: str = "info"
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        try:
            tip_model = TipBoxData(message=message, title=title, style=style)
        except Exception as e:
            return f"Validation error: {str(e)}"

        tip_data = {
            "message": tip_model.message,
            "title": tip_model.title,
            "style": tip_model.style
        }
        draft.content.setdefault("components", []).append(
            {"component": "tip_box", **tip_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added {style} tip box"

    @mcp.tool
    async def linkedin_add_stats_grid(
        stats: dict, title: str = None, columns: int = 2
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        try:
            stats_model = StatsGridData(stats=stats, title=title, columns=columns)
        except Exception as e:
            return f"Validation error: {str(e)}"

        stats_data = {
            "stats": stats_model.stats,
            "title": stats_model.title,
            "columns": stats_model.columns
        }
        draft.content.setdefault("components", []).append(
            {"component": "stats_grid", **stats_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added stats grid with {len(stats)} stats"

    @mcp.tool
    async def linkedin_add_poll_preview(
        question: str, options: list[str]
    ) -> str:
        """
        Add poll preview for engagement.

        Args:
            question: Poll question
            options: Poll options (2-4)

        Returns:
            Success message
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        try:
            poll_model = PollPreviewData(question=question, options=options)
        except Exception as e:
            return f"Validation error: {str(e)}"

        poll_data = {
            "question": poll_model.question,
            "options": poll_model.options
        }
        draft.content.setdefault("components", []).append(
            {"component": "poll_preview", **poll_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added poll with {len(options)} options"

    @mcp.tool
    async def linkedin_add_feature_list(
        features: list[dict], title: str = None
    ) -> str:
        """
        Add feature list with icons and descriptions.

        Args:
            features: Features (each with 'title', optional 'icon' and 'description')
            title: Optional feature list title

        Returns:
            Success message
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        try:
            feature_model = FeatureListData(features=features, title=title)
        except Exception as e:
            return f"Validation error: {str(e)}"

        feature_data = {
            "features": feature_model.features,
            "title": feature_model.title
        }
        draft.content.setdefault("components", []).append(
            {"component": "feature_list", **feature_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added feature list with {len(features)} features"

    @mcp.tool
    async def linkedin_add_numbered_list(
        items: list[str], title: str = None, style: str = "numbers", start: int = 1
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
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        try:
            list_model = NumberedListData(items=items, title=title, style=style, start=start)
        except Exception as e:
            return f"Validation error: {str(e)}"

        list_data = {
            "items": list_model.items,
            "title": list_model.title,
            "style": list_model.style,
            "start": list_model.start
        }
        draft.content.setdefault("components", []).append(
            {"component": "numbered_list", **list_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added numbered list with {len(items)} items"

    @mcp.tool
    async def linkedin_add_hashtags(tags: list[str], placement: str = "end") -> str:
        """
        Add hashtags to current draft.

        Args:
            tags: List of hashtags (without #)
            placement: Where to place hashtags (inline, mid, end, first_comment)

        Returns:
            Success message
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        hashtag_data = {"tags": tags, "placement": placement}
        draft.content.setdefault("components", []).append(
            {"component": "hashtags", **hashtag_data}
        )
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Added {len(tags)} hashtags"

    @mcp.tool
    async def linkedin_compose_post(optimize: bool = True) -> str:
        """
        Compose post from components in current draft.

        Args:
            optimize: Optimize for engagement (default: true)

        Returns:
            Composed post text
        """
        from ..posts import ComposablePost
        from ..themes.theme_manager import ThemeManager

        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        # Get theme if specified
        theme = None
        if draft.theme:
            theme_mgr = ThemeManager()
            theme = theme_mgr.get_theme(draft.theme)

        # Create composable post
        post = ComposablePost(draft.post_type, theme=theme)

        # Add components from draft
        for comp in draft.content.get("components", []):
            comp_type = comp.get("component")
            if comp_type == "hook":
                post.add_hook(comp["type"], comp["content"])
            elif comp_type == "body":
                post.add_body(comp["content"], comp.get("structure"))
            elif comp_type == "bar_chart":
                post.add_bar_chart(comp["data"], comp.get("title"), comp.get("unit", ""))
            elif comp_type == "metrics_chart":
                post.add_metrics_chart(comp["data"], comp.get("title"))
            elif comp_type == "comparison_chart":
                post.add_comparison_chart(comp["data"], comp.get("title"))
            elif comp_type == "progress_chart":
                post.add_progress_chart(comp["data"], comp.get("title"))
            elif comp_type == "ranking_chart":
                post.add_ranking_chart(comp["data"], comp.get("title"), comp.get("show_medals", True))
            elif comp_type == "quote":
                post.add_quote(comp["text"], comp["author"], comp.get("source"))
            elif comp_type == "big_stat":
                post.add_big_stat(comp["number"], comp["label"], comp.get("context"))
            elif comp_type == "timeline":
                post.add_timeline(comp["steps"], comp.get("title"), comp.get("style", "arrow"))
            elif comp_type == "key_takeaway":
                post.add_key_takeaway(comp["message"], comp.get("title", "KEY TAKEAWAY"), comp.get("style", "box"))
            elif comp_type == "pro_con":
                post.add_pro_con(comp["pros"], comp["cons"], comp.get("title"))
            elif comp_type == "checklist":
                post.add_checklist(comp["items"], comp.get("title"), comp.get("show_progress", False))
            elif comp_type == "before_after":
                post.add_before_after(comp["before"], comp["after"], comp.get("title"), comp.get("labels"))
            elif comp_type == "tip_box":
                post.add_tip_box(comp["message"], comp.get("title"), comp.get("style", "info"))
            elif comp_type == "stats_grid":
                post.add_stats_grid(comp["stats"], comp.get("title"), comp.get("columns", 2))
            elif comp_type == "poll_preview":
                post.add_poll_preview(comp["question"], comp["options"])
            elif comp_type == "feature_list":
                post.add_feature_list(comp["features"], comp.get("title"))
            elif comp_type == "numbered_list":
                post.add_numbered_list(comp["items"], comp.get("title"), comp.get("style", "numbers"), comp.get("start", 1))
            elif comp_type == "separator":
                post.add_separator(comp.get("style", "line"))
            elif comp_type == "cta":
                post.add_cta(comp["type"], comp["text"])
            elif comp_type == "hashtags":
                post.add_hashtags(comp["tags"], comp.get("placement", "end"))

        # Optimize if requested
        if optimize:
            post.optimize_for_engagement()

        # Compose final text
        final_text = post.compose()

        # Update draft with composed text
        draft.content["composed_text"] = final_text
        manager.update_draft(draft.draft_id, content=draft.content)

        return f"Composed post ({len(final_text)} chars):\n\n{final_text}"

    @mcp.tool
    async def linkedin_get_preview() -> str:
        """
        Get preview of current draft (first 210 chars).

        Returns:
            Preview text showing what appears before "see more"
        """
        draft = manager.get_current_draft()
        if not draft:
            return "No active draft"

        preview = manager.get_draft_preview(draft.draft_id)
        return f"Preview (first 210 chars):\n\n{preview}"

    @mcp.tool
    async def linkedin_preview_html(output_path: str = None, open_browser: bool = True) -> str:
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

    @mcp.tool
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
