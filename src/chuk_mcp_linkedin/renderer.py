"""
Component renderer for LinkedIn design system.

Converts component configuration dictionaries to HTML for preview.
"""

from typing import Dict, Any, List
import html as html_module


class ComponentRenderer:
    """Renders component configurations to HTML"""

    @staticmethod
    def _safe_text(value: Any) -> str:
        """
        Safely extract text from a value that might be a dict or string.

        Args:
            value: Value to extract text from (dict, str, or other)

        Returns:
            Text string
        """
        if value is None:
            return ""
        if isinstance(value, dict):
            # Try common text keys
            return value.get("text", value.get("label", value.get("name", str(value))))
        return str(value)

    @staticmethod
    def render(component: Dict[str, Any]) -> str:
        """
        Render a component configuration to HTML.

        Args:
            component: Component configuration dictionary

        Returns:
            HTML string
        """
        comp_type = component.get("type")

        # Route to appropriate renderer
        if comp_type == "divider":
            return ComponentRenderer._render_divider(component)
        elif comp_type == "background":
            return ComponentRenderer._render_background(component)
        elif comp_type == "border":
            return ComponentRenderer._render_border(component)
        elif comp_type == "badge":
            return ComponentRenderer._render_badge(component)
        elif comp_type == "shape":
            return ComponentRenderer._render_shape(component)
        elif comp_type == "header":
            return ComponentRenderer._render_header(component)
        elif comp_type == "body_text":
            return ComponentRenderer._render_body_text(component)
        elif comp_type == "caption":
            return ComponentRenderer._render_caption(component)
        elif comp_type == "quote":
            return ComponentRenderer._render_quote(component)
        elif comp_type == "list":
            return ComponentRenderer._render_list(component)
        elif comp_type == "chart":
            return ComponentRenderer._render_chart(component)
        elif comp_type == "metric":
            return ComponentRenderer._render_metric(component)
        elif comp_type == "progress":
            return ComponentRenderer._render_progress(component)
        elif comp_type == "table":
            return ComponentRenderer._render_table(component)
        elif comp_type == "infographic":
            return ComponentRenderer._render_infographic(component)
        else:
            return f'<div class="unknown-component">Unknown component type: {comp_type}</div>'

    # Visual Elements Renderers

    @staticmethod
    def _render_divider(comp: Dict[str, Any]) -> str:
        """Render divider component"""
        variant = comp.get("variant")
        color = comp.get("color", "#000000")
        width = comp.get("width", "100%")
        height = comp.get("height", 2)
        style = comp.get("style", "solid")

        if variant == "gradient_fade":
            return f"""
            <div style="height: {height}px; width: {width};
                 background: linear-gradient(to right, transparent, {color}, transparent);
                 margin: 20px 0;"></div>
            """
        elif variant == "decorative_accent":
            return f"""
            <div style="height: 8px; width: 120px; background: {color}; margin: 20px auto;"></div>
            """
        elif variant == "section_break":
            return f"""
            <div style="text-align: center; margin: 40px 0; color: {color}; font-size: 24px;">• • •</div>
            """
        elif variant == "title_underline":
            return f"""
            <div style="height: {height}px; width: {width}; background: {color}; margin-top: 8px;"></div>
            """
        else:  # horizontal_line
            return f"""
            <hr style="border: none; border-top: {height}px {style} {color}; margin: 20px 0;" />
            """

    @staticmethod
    def _render_background(comp: Dict[str, Any]) -> str:
        """Render background component (returns CSS style)"""
        variant = comp.get("variant")
        color = comp.get("color", "#FFFFFF")

        # Backgrounds are typically applied to containers, not standalone
        return f'<div class="background-preview" style="background: {color}; padding: 40px; min-height: 100px; border-radius: 8px;">(Background: {variant})</div>'

    @staticmethod
    def _render_border(comp: Dict[str, Any]) -> str:
        """Render border component"""
        variant = comp.get("variant")
        color = comp.get("border_color", "#000000")
        width = comp.get("border_width", 2)
        content = comp.get("content", "Content with border")

        if variant == "accent":
            side = comp.get("side", "left")
            border_style = f"border-{side}: {width}px solid {color};"
            return f"""
            <div style="{border_style} padding: 20px; margin: 10px 0;">
                {html_module.escape(content)}
            </div>
            """
        elif variant == "callout":
            # Use border_color from component (already set to correct semantic color)
            bg = comp.get("background_color", color)
            return f"""
            <div style="border: 3px solid {color}; padding: 20px; margin: 10px 0; border-radius: 8px; background: {bg};">
                {html_module.escape(content)}
            </div>
            """
        else:  # simple_border
            return f"""
            <div style="border: {width}px solid {color}; padding: 20px; margin: 10px 0; border-radius: 8px;">
                {html_module.escape(content)}
            </div>
            """

    @staticmethod
    def _render_badge(comp: Dict[str, Any]) -> str:
        """Render badge component"""
        variant = comp.get("variant")
        text = comp.get("text", "")
        bg_color = comp.get("background_color", "#0a66c2")
        text_color = comp.get("text_color", "#FFFFFF")

        if variant == "pill":
            return f"""
            <span style="display: inline-block; background: {bg_color}; color: {text_color};
                  padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;
                  text-transform: uppercase; margin: 4px;">{html_module.escape(text)}</span>
            """
        elif variant == "status":
            icon_map = {"success": "✓", "warning": "⚠", "error": "✗", "info": "ℹ"}
            status = comp.get("status", "info")
            icon = icon_map.get(status, "ℹ")
            return f"""
            <span style="display: inline-block; background: {bg_color}; color: {text_color};
                  padding: 8px 12px; border-radius: 4px; font-size: 14px; font-weight: 600;
                  margin: 4px;">{icon} {html_module.escape(text)}</span>
            """
        elif variant == "percentage_change":
            value = comp.get("value", 0)
            direction = "↑" if value >= 0 else "↓"
            color = "#057642" if value >= 0 else "#cc1016"
            return f"""
            <span style="color: {color}; font-weight: 600; font-size: 16px;">
                {direction} {abs(value)}%
            </span>
            """
        else:
            return f"""<span class="badge" style="background: {bg_color}; color: {text_color}; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{html_module.escape(text)}</span>"""

    @staticmethod
    def _render_shape(comp: Dict[str, Any]) -> str:
        """Render shape component"""
        variant = comp.get("variant")

        if variant == "checkmark":
            color = comp.get("color", "#057642")
            size = comp.get("size", 24)
            return f'<span style="color: {color}; font-size: {size}px;">✓</span>'
        elif variant == "arrow":
            direction = comp.get("direction", "right")
            arrows = {"up": "↑", "down": "↓", "left": "←", "right": "→"}
            return f'<span style="font-size: 20px;">{arrows.get(direction, "→")}</span>'
        elif variant == "bullet_point":
            symbol = comp.get("symbol", "•")
            return f'<span style="margin-right: 8px;">{symbol}</span>'
        elif variant == "icon_container":
            icon = comp.get("icon", "🚀")
            size = comp.get("size", 48)
            bg_color = comp.get("background_color", "#0a66c215")
            return f"""
            <div style="display: inline-flex; align-items: center; justify-content: center;
                  width: {size}px; height: {size}px; background: {bg_color};
                  border-radius: 8px; font-size: {size * 0.6}px;">{icon}</div>
            """
        else:
            return f'<div class="shape {variant}"></div>'

    # Typography Renderers

    @staticmethod
    def _render_header(comp: Dict[str, Any]) -> str:
        """Render header component"""
        variant = comp.get("variant")
        text = comp.get("text", "")
        font_size = comp.get("font_size", 24)
        font_weight = comp.get("font_weight", 700)
        color = comp.get("color", "#000000")
        align = comp.get("text_align", "left")
        transform = comp.get("text_transform", "none")

        tag_map = {
            "h1": "h1",
            "h2": "h2",
            "h3": "h3",
            "h4": "h4",
            "section_header": "h3",
            "eyebrow": "div",
            "slide_title": "h2",
        }
        tag = tag_map.get(variant, "h2")

        return f"""
        <{tag} style="font-size: {font_size}pt; font-weight: {font_weight}; color: {color};
              text-align: {align}; text-transform: {transform}; margin: 20px 0 10px 0;">
            {html_module.escape(text)}
        </{tag}>
        """

    @staticmethod
    def _render_body_text(comp: Dict[str, Any]) -> str:
        """Render body text component"""
        variant = comp.get("variant")
        text = comp.get("text", "")
        font_size = comp.get("font_size", 16)
        line_height = comp.get("line_height", 1.6)
        color = comp.get("color", "#000000")

        if variant == "highlighted":
            bg_color = comp.get("background_color", "#fff3cd")
            return f"""
            <span style="background: {bg_color}; padding: 4px 8px; border-radius: 4px;
                  font-size: {font_size}pt; line-height: {line_height}; color: {color};">
                {html_module.escape(text)}
            </span>
            """
        elif variant == "emphasized":
            return f"""
            <em style="font-size: {font_size}pt; line-height: {line_height}; color: {color}; font-style: italic;">
                {html_module.escape(text)}
            </em>
            """
        elif variant == "link":
            href = comp.get("url", "#")
            return f"""
            <a href="{href}" style="color: #0a66c2; font-size: {font_size}pt; text-decoration: underline;">
                {html_module.escape(text)}
            </a>
            """
        elif variant == "code":
            return f"""
            <code style="background: #f5f5f5; padding: 2px 6px; border-radius: 3px;
                  font-family: 'Courier New', monospace; font-size: {font_size}pt; color: #d63384;">
                {html_module.escape(text)}
            </code>
            """
        else:  # paragraph, lead_text, small_text
            return f"""
            <p style="font-size: {font_size}pt; line-height: {line_height}; color: {color}; margin: 12px 0;">
                {html_module.escape(text)}
            </p>
            """

    @staticmethod
    def _render_caption(comp: Dict[str, Any]) -> str:
        """Render caption component"""
        text = comp.get("text", "")
        font_size = comp.get("font_size", 14)
        color = comp.get("color", "#666666")
        font_style = comp.get("font_style", "normal")
        icon = comp.get("icon", "")

        icon_html = f'<span style="margin-right: 6px;">{icon}</span>' if icon else ""

        return f"""
        <div style="font-size: {font_size}pt; color: {color}; font-style: {font_style};
              margin: 8px 0; opacity: 0.85;">
            {icon_html}{html_module.escape(text)}
        </div>
        """

    @staticmethod
    def _render_quote(comp: Dict[str, Any]) -> str:
        """Render quote component"""
        variant = comp.get("variant")
        text = comp.get("text", "")
        author_data = comp.get("author", "")
        font_size = comp.get("font_size", 20)
        color = comp.get("color", "#000000")

        if variant == "testimonial":
            # Author is a dict for testimonials
            if isinstance(author_data, dict):
                name = author_data.get("name", "")
                role_data = author_data.get("role", {})

                # Rating is also a dict
                rating_data = comp.get("rating", {})
                if isinstance(rating_data, dict):
                    rating_value = rating_data.get("value", 0)
                    stars = (
                        "★" * int(rating_value) + "☆" * (5 - int(rating_value))
                        if rating_value
                        else ""
                    )
                else:
                    stars = ""

                attribution = f"{name}"
                if isinstance(role_data, dict):
                    role_text = role_data.get("text", "")
                    if role_text:
                        attribution += f", {role_text}"
            else:
                # Fallback if author is string
                attribution = str(author_data)
                stars = ""

            return f"""
            <blockquote style="border-left: 4px solid #0a66c2; padding-left: 20px; margin: 20px 0;
                  font-size: {font_size}pt; color: {color}; font-style: italic;">
                "{html_module.escape(text)}"
                <footer style="margin-top: 12px; font-size: 14pt; font-style: normal; color: #666;">
                    {stars}<br>
                    — {html_module.escape(attribution)}
                </footer>
            </blockquote>
            """
        else:  # pull_quote, blockquote
            # Author is a string for other quote types
            author = str(author_data) if author_data else ""
            author_html = (
                f'<footer style="margin-top: 12px; font-size: 14pt; font-style: normal; color: #666;">— {html_module.escape(author)}</footer>'
                if author
                else ""
            )
            return f"""
            <blockquote style="border-left: 4px solid #0a66c2; padding-left: 20px; margin: 20px 0;
                  font-size: {font_size}pt; color: {color}; font-style: italic;">
                "{html_module.escape(text)}"
                {author_html}
            </blockquote>
            """

    @staticmethod
    def _render_list(comp: Dict[str, Any]) -> str:
        """Render list component"""
        variant = comp.get("variant")
        items = comp.get("items", [])

        if variant == "numbered":
            list_items = "".join(
                [f'<li style="margin: 8px 0;">{html_module.escape(item)}</li>' for item in items]
            )
            return f'<ol style="margin: 16px 0; padding-left: 24px;">{list_items}</ol>'
        elif variant == "checklist":
            checked_symbol = comp.get("checked_symbol", "✓")
            unchecked_symbol = comp.get("unchecked_symbol", "☐")
            list_items = ""
            for item in items:
                if isinstance(item, dict):
                    symbol = checked_symbol if item.get("checked") else unchecked_symbol
                    text = item.get("text", "")
                    color = "#057642" if item.get("checked") else "#666666"
                else:
                    symbol = unchecked_symbol
                    text = item
                    color = "#666666"
                list_items += f'<div style="margin: 8px 0;"><span style="color: {color}; margin-right: 8px;">{symbol}</span>{html_module.escape(str(text))}</div>'
            return f'<div style="margin: 16px 0;">{list_items}</div>'
        elif variant == "icon_list":
            list_items = ""
            for item in items:
                if isinstance(item, dict):
                    icon = item.get("icon", "•")
                    text = item.get("text", "")
                else:
                    icon = "•"
                    text = item
                list_items += f'<div style="margin: 8px 0;"><span style="margin-right: 8px;">{icon}</span>{html_module.escape(str(text))}</div>'
            return f'<div style="margin: 16px 0;">{list_items}</div>'
        else:  # bulleted_list
            bullet = comp.get("bullet", "→")
            list_items = "".join(
                [
                    f'<li style="margin: 8px 0; list-style: none;"><span style="margin-right: 8px;">{bullet}</span>{html_module.escape(str(item))}</li>'
                    for item in items
                ]
            )
            return f'<ul style="margin: 16px 0; padding-left: 0;">{list_items}</ul>'

    # Data Viz Renderers

    @staticmethod
    def _render_chart(comp: Dict[str, Any]) -> str:
        """Render chart component"""
        variant = comp.get("variant")
        data = comp.get("data", [])
        bar_color = comp.get("bar_color", "#0a66c2")

        if variant == "bar":
            if not data:
                return "<div>No data</div>"

            max_value = max(item["value"] for item in data)
            bars_html = ""
            for item in data:
                label = item.get("label", "")
                value = item.get("value", 0)
                percentage = (value / max_value * 100) if max_value > 0 else 0
                bars_html += f"""
                <div style="margin: 12px 0;">
                    <div style="font-size: 14px; margin-bottom: 4px;">{html_module.escape(label)}</div>
                    <div style="background: #f0f0f0; height: 30px; border-radius: 4px; overflow: hidden;">
                        <div style="background: {bar_color}; height: 100%; width: {percentage}%;
                              display: flex; align-items: center; justify-content: flex-end;
                              padding-right: 8px; color: white; font-weight: 600; font-size: 12px;">
                            {value}
                        </div>
                    </div>
                </div>
                """
            return f'<div style="margin: 20px 0;">{bars_html}</div>'
        elif variant == "pie":
            # Simple pie representation
            total = sum(item["value"] for item in data)
            items_html = ""
            for item in data:
                label = item.get("label", "")
                value = item.get("value", 0)
                percentage = (value / total * 100) if total > 0 else 0
                items_html += f"""
                <div style="margin: 8px 0; display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; background: {bar_color};
                          border-radius: 3px; margin-right: 8px;"></div>
                    <span>{html_module.escape(label)}: {percentage:.1f}%</span>
                </div>
                """
            return f'<div style="margin: 20px 0;">{items_html}</div>'
        else:
            return '<div class="chart">Chart visualization</div>'

    @staticmethod
    def _render_metric(comp: Dict[str, Any]) -> str:
        """Render metric component"""
        variant = comp.get("variant")

        if variant == "card":
            label = comp.get("label", "")
            value = comp.get("value", "")
            change = comp.get("change")
            icon = comp.get("icon", "")

            change_html = ""
            if change:
                direction = "↑" if change.get("value", 0) >= 0 else "↓"
                color = "#057642" if change.get("value", 0) >= 0 else "#cc1016"
                change_html = f'<div style="color: {color}; font-size: 16px; margin-top: 8px;">{direction} {change.get("text", "")}</div>'

            icon_html = (
                f'<div style="font-size: 32px; margin-bottom: 12px;">{icon}</div>' if icon else ""
            )

            return f"""
            <div style="border: 2px solid #e0e0e0; border-radius: 12px; padding: 24px; margin: 12px; display: inline-block; min-width: 200px;">
                {icon_html}
                <div style="font-size: 14px; color: #666; margin-bottom: 8px;">{html_module.escape(label)}</div>
                <div style="font-size: 36px; font-weight: 700; color: #000;">{html_module.escape(value)}</div>
                {change_html}
            </div>
            """
        elif variant == "big_stat":
            value = comp.get("value", "")
            label = comp.get("label", "")
            context_data = comp.get("context", "")

            context_html = ""
            if context_data:
                if isinstance(context_data, dict):
                    # Handle nested dict structure from component
                    context_text = ComponentRenderer._safe_text(context_data.get("text", ""))
                    context_html = f'<div style="font-size: 14px; color: #666; margin-top: 12px;">{html_module.escape(context_text)}</div>'
                else:
                    context_html = f'<div style="font-size: 14px; color: #666; margin-top: 12px;">{html_module.escape(str(context_data))}</div>'

            return f"""
            <div style="text-align: center; padding: 40px; margin: 20px 0;">
                <div style="font-size: 72px; font-weight: 800; color: #0a66c2; margin-bottom: 16px;">{html_module.escape(value)}</div>
                <div style="font-size: 24px; color: #000; font-weight: 600;">{html_module.escape(label)}</div>
                {context_html}
            </div>
            """
        else:
            return '<div class="metric">Metric visualization</div>'

    @staticmethod
    def _render_progress(comp: Dict[str, Any]) -> str:
        """Render progress component"""
        variant = comp.get("variant")

        if variant == "bar":
            percentage = comp.get("percentage", 0)
            label_data = comp.get("label", "")
            # Handle nested dict structure from component
            if isinstance(label_data, dict):
                label = ComponentRenderer._safe_text(label_data.get("text", ""))
            else:
                label = str(label_data) if label_data else ""
            color = comp.get("fill_color", "#0a66c2")

            label_html = (
                f'<div style="font-size: 14px; margin-bottom: 8px;">{html_module.escape(label)}</div>'
                if label
                else ""
            )

            return f"""
            <div style="margin: 20px 0;">
                {label_html}
                <div style="background: #e0e0e0; height: 24px; border-radius: 12px; overflow: hidden;">
                    <div style="background: {color}; height: 100%; width: {percentage}%;
                          display: flex; align-items: center; justify-content: center;
                          color: white; font-weight: 600; font-size: 12px;">
                        {percentage}%
                    </div>
                </div>
            </div>
            """
        elif variant == "steps":
            steps = comp.get("steps", [])
            current_step = comp.get("current_step", 0)

            steps_html = ""
            for i, step in enumerate(steps):
                is_complete = i < current_step
                is_current = i == current_step
                color = "#057642" if is_complete else ("#0a66c2" if is_current else "#e0e0e0")

                steps_html += f"""
                <div style="display: flex; align-items: center;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: {color};
                          color: white; display: flex; align-items: center; justify-content: center;
                          font-weight: 600;">{i + 1}</div>
                    <div style="margin-left: 12px; font-size: 14px;">{html_module.escape(step)}</div>
                </div>
                """
                if i < len(steps) - 1:
                    line_color = "#057642" if is_complete else "#e0e0e0"
                    steps_html += f'<div style="width: 2px; height: 20px; background: {line_color}; margin-left: 15px;"></div>'

            return f'<div style="margin: 20px 0;">{steps_html}</div>'
        else:
            return '<div class="progress">Progress visualization</div>'

    @staticmethod
    def _render_table(comp: Dict[str, Any]) -> str:
        """Render table component"""
        variant = comp.get("variant")

        if variant == "simple":
            headers = comp.get("headers", [])
            rows = comp.get("rows", [])

            header_html = "".join(
                [
                    f'<th style="padding: 12px; text-align: left; background: #0a66c2; color: white; font-weight: 600;">{html_module.escape(h)}</th>'
                    for h in headers
                ]
            )

            rows_html = ""
            for i, row in enumerate(rows):
                bg = "#f9f9f9" if i % 2 == 0 else "white"
                cells = "".join(
                    [
                        f'<td style="padding: 12px; border-bottom: 1px solid #e0e0e0; background: {bg};">{html_module.escape(str(cell))}</td>'
                        for cell in row
                    ]
                )
                rows_html += f"<tr>{cells}</tr>"

            return f"""
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0;">
                <thead><tr>{header_html}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
            """
        elif variant == "pricing":
            tiers = comp.get("tiers", [])

            tiers_html = ""
            for tier in tiers:
                name = tier.get("name", "")
                price = tier.get("price", "")
                features = tier.get("features", [])
                highlight = tier.get("highlight", False)

                border = "3px solid #0a66c2" if highlight else "1px solid #e0e0e0"
                features_html = "".join(
                    [
                        f'<div style="margin: 8px 0;">✓ {html_module.escape(f)}</div>'
                        for f in features
                    ]
                )

                tiers_html += f"""
                <div style="border: {border}; border-radius: 12px; padding: 24px; margin: 12px;
                      display: inline-block; vertical-align: top; min-width: 250px;">
                    <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px;">{html_module.escape(name)}</div>
                    <div style="font-size: 36px; font-weight: 800; color: #0a66c2; margin-bottom: 20px;">{html_module.escape(price)}</div>
                    <div style="font-size: 14px; color: #666;">{features_html}</div>
                </div>
                """

            return f'<div style="margin: 20px 0; text-align: center;">{tiers_html}</div>'
        else:
            return '<div class="table">Table visualization</div>'

    @staticmethod
    def _render_infographic(comp: Dict[str, Any]) -> str:
        """Render infographic component"""
        variant = comp.get("variant")

        if variant == "stat_with_icon":
            icon = comp.get("icon", "🚀")
            value = comp.get("value", "")
            label = comp.get("label", "")

            return f"""
            <div style="text-align: center; padding: 40px; margin: 20px 0;">
                <div style="font-size: 80px; margin-bottom: 20px;">{icon}</div>
                <div style="font-size: 60px; font-weight: 800; color: #0a66c2; margin-bottom: 12px;">{html_module.escape(value)}</div>
                <div style="font-size: 20px; color: #666;">{html_module.escape(label)}</div>
            </div>
            """
        elif variant == "funnel":
            stages = comp.get("stages", [])

            stages_html = ""
            for i, stage in enumerate(stages):
                label = stage.get("label", "")
                value = stage.get("value", "")
                percentage = stage.get("percentage", 100)
                width = percentage

                stages_html += f"""
                <div style="margin: 16px auto; text-align: center;">
                    <div style="background: linear-gradient(to right, #0a66c2, #0073b1);
                          width: {width}%; height: 60px; margin: 0 auto;
                          display: flex; align-items: center; justify-content: center;
                          color: white; font-weight: 600; clip-path: polygon(5% 0%, 95% 0%, 100% 100%, 0% 100%);">
                        {html_module.escape(label)}: {html_module.escape(value)}
                    </div>
                </div>
                """

            return f'<div style="margin: 40px 0;">{stages_html}</div>'
        elif variant == "process_flow":
            steps = comp.get("steps", [])

            steps_html = ""
            for i, step in enumerate(steps):
                steps_html += f"""
                <div style="display: inline-block; background: #0a66c2; color: white;
                      padding: 16px 24px; border-radius: 8px; margin: 8px; font-weight: 600;">
                    {html_module.escape(step)}
                </div>
                """
                if i < len(steps) - 1:
                    steps_html += '<span style="font-size: 24px; margin: 0 8px;">→</span>'

            return f'<div style="text-align: center; margin: 40px 0;">{steps_html}</div>'
        elif variant == "timeline":
            events = comp.get("events", [])

            events_html = ""
            for event in events:
                date = event.get("date", "")
                title = event.get("title", "")
                description = event.get("description", "")
                icon = event.get("icon", "")

                icon_html = (
                    f'<div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>'
                    if icon
                    else ""
                )

                events_html += f"""
                <div style="margin: 20px 0; padding-left: 40px; border-left: 4px solid #0a66c2; position: relative;">
                    <div style="position: absolute; left: -14px; top: 0; width: 24px; height: 24px;
                          background: #0a66c2; border-radius: 50%; border: 4px solid white;"></div>
                    {icon_html}
                    <div style="font-size: 14px; color: #666; font-weight: 600; margin-bottom: 4px;">{html_module.escape(date)}</div>
                    <div style="font-size: 18px; font-weight: 700; margin-bottom: 8px;">{html_module.escape(title)}</div>
                    <div style="font-size: 14px; color: #666;">{html_module.escape(description)}</div>
                </div>
                """

            return f'<div style="margin: 40px 0;">{events_html}</div>'
        else:
            return '<div class="infographic">Infographic visualization</div>'


class ShowcaseRenderer:
    """Renders component showcases to HTML"""

    @staticmethod
    def create_showcase_page(title: str, sections: List[Dict[str, Any]]) -> str:
        """
        Create a complete HTML showcase page.

        Args:
            title: Page title
            sections: List of section dicts with 'title', 'description', 'components'

        Returns:
            HTML string
        """
        sections_html = ""
        for section in sections:
            section_title = section.get("title", "")
            section_desc = section.get("description", "")
            components = section.get("components", [])

            components_html = ""
            for comp_info in components:
                comp_name = comp_info.get("name", "")
                comp_desc = comp_info.get("description", "")
                component = comp_info.get("component")

                rendered = ComponentRenderer.render(component) if component else ""

                components_html += f"""
                <div class="component-example">
                    <div class="component-header">
                        <h4>{html_module.escape(comp_name)}</h4>
                        {f'<p class="component-description">{html_module.escape(comp_desc)}</p>' if comp_desc else ''}
                    </div>
                    <div class="component-preview">
                        {rendered}
                    </div>
                </div>
                """

            sections_html += f"""
            <section class="showcase-section">
                <h2>{html_module.escape(section_title)}</h2>
                {f'<p class="section-description">{html_module.escape(section_desc)}</p>' if section_desc else ''}
                <div class="components-grid">
                    {components_html}
                </div>
            </section>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_module.escape(title)}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background: #f5f5f5;
            color: #000;
            line-height: 1.6;
        }}

        .header {{
            background: linear-gradient(135deg, #0a66c2, #0073b1);
            color: white;
            padding: 60px 20px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 12px;
        }}

        .header p {{
            font-size: 20px;
            opacity: 0.95;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .showcase-section {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 40px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        .showcase-section h2 {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #0a66c2;
        }}

        .section-description {{
            font-size: 16px;
            color: #666;
            margin-bottom: 32px;
        }}

        .components-grid {{
            display: grid;
            gap: 32px;
        }}

        .component-example {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}

        .component-header {{
            background: #f9f9f9;
            padding: 16px 20px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .component-header h4 {{
            font-size: 18px;
            font-weight: 600;
            color: #000;
            margin-bottom: 4px;
        }}

        .component-description {{
            font-size: 14px;
            color: #666;
        }}

        .component-preview {{
            padding: 24px;
            background: white;
        }}

        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 14px;
        }}

        .footer a {{
            color: #0a66c2;
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{html_module.escape(title)}</h1>
        <p>LinkedIn Design System Component Library</p>
    </div>

    <div class="container">
        {sections_html}
    </div>

    <div class="footer">
        <p>Generated by <strong>chuk-mcp-linkedin</strong> Design System</p>
        <p>All components use token-based design for consistency and LinkedIn 2025 best practices</p>
    </div>
</body>
</html>"""
