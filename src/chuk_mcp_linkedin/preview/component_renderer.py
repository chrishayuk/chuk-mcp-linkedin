# src/chuk_mcp_linkedin/preview/component_renderer.py
"""
Component Renderer - Converts components to HTML/CSS.

Renders visual elements, layouts, and other components as HTML for browser preview.
"""

from typing import Dict, Any, List


class ComponentRenderer:
    """Renders components as HTML/CSS"""

    @staticmethod
    def render_divider(divider: Dict[str, Any]) -> str:
        """Render divider component to HTML"""
        variant = divider.get("variant", "horizontal_line")

        if variant == "horizontal_line":
            return f"""
<div style="
    width: {divider['width']}px;
    height: {divider['height']}px;
    background-color: {divider['color']};
    margin-top: {divider['margin_top']}px;
    margin-bottom: {divider['margin_bottom']}px;
    {'border-style: dashed;' if divider['style'] == 'dashed' else ''}
"></div>
"""

        elif variant == "gradient_fade":
            gradient = divider.get("gradient", {})
            return f"""
<div style="
    width: {divider['width']}px;
    height: {divider['height']}px;
    background: linear-gradient(to right, {gradient['start']}, {gradient['mid']}, {gradient['end']});
    margin-top: {divider['margin_top']}px;
    margin-bottom: {divider['margin_bottom']}px;
"></div>
"""

        elif variant == "decorative_accent":
            return f"""
<div style="
    width: {divider['width']}px;
    height: {divider['height']}px;
    background-color: {divider['color']};
    border-radius: {divider['border_radius']}px;
    margin: {divider['margin_top']}px auto {divider['margin_bottom']}px auto;
"></div>
"""

        elif variant == "section_break":
            return f"""
<div style="
    text-align: {divider['align']};
    color: {divider['color']};
    font-size: {divider['font_size']}px;
    margin-top: {divider['margin_top']}px;
    margin-bottom: {divider['margin_bottom']}px;
    letter-spacing: 8px;
">{divider['symbols']}</div>
"""

        elif variant == "spacer":
            return f"""<div style="height: {divider['height']}px;"></div>"""

        return ""

    @staticmethod
    def render_badge(badge: Dict[str, Any]) -> str:
        """Render badge component to HTML"""
        variant = badge.get("variant", "pill")

        common_style = f"""
display: inline-block;
padding: {badge.get('padding_y', 6)}px {badge.get('padding_x', 12)}px;
font-size: {badge.get('font_size', 18)}px;
font-weight: {badge.get('font_weight', '600')};
border-radius: {badge.get('border_radius', 999)}px;
"""

        if variant == "pill":
            return f"""
<span style="{common_style}
    background-color: {badge['background_color']};
    color: {badge['text_color']};
">{badge['text']}</span>
"""

        elif variant == "status":
            return f"""
<span style="{common_style}
    background-color: {badge['background_color']};
    color: {badge['text_color']};
    text-transform: uppercase;
    letter-spacing: 0.5px;
">{badge['text']}</span>
"""

        elif variant == "status_outlined":
            return f"""
<span style="{common_style}
    background-color: {badge['background_color']};
    color: {badge['text_color']};
    border: {badge['border_width']}px solid {badge['border_color']};
    text-transform: uppercase;
    letter-spacing: 0.5px;
">{badge['text']}</span>
"""

        elif variant == "percentage_change":
            return f"""
<span style="{common_style}
    background-color: {badge['background_color']};
    color: {badge['text_color']};
">{badge['text']}</span>
"""

        elif variant == "category_tag":
            return f"""
<span style="{common_style}
    background-color: {badge['background_color']};
    color: {badge['text_color']};
">{badge['text']}</span>
"""

        return ""

    @staticmethod
    def render_shape(shape: Dict[str, Any]) -> str:
        """Render shape component to HTML"""
        variant = shape.get("variant", "circle")

        if variant == "circle":
            return f"""
<div style="
    width: {shape['size']}px;
    height: {shape['size']}px;
    border-radius: 50%;
    {'background-color: ' + shape['color'] + ';' if shape['fill'] else 'border: ' + str(shape.get('stroke_width', 2)) + 'px solid ' + shape['color'] + ';'}
    display: inline-block;
"></div>
"""

        elif variant == "icon_container":
            return f"""
<div style="
    width: {shape['size']}px;
    height: {shape['size']}px;
    border-radius: {shape['border_radius']}px;
    background-color: {shape['background_color']};
    color: {shape['icon_color']};
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: {shape['icon_size']}px;
">{shape['icon']}</div>
"""

        elif variant == "checkmark":
            bg_style = ""
            if shape.get("background"):
                bg_style = f"background-color: {shape['color']}; color: white; border-radius: {shape['border_radius']}px; padding: 8px;"

            return f"""
<div style="
    width: {shape['size']}px;
    height: {shape['size']}px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: {shape['size'] - 10}px;
    font-weight: bold;
    {bg_style}
    {'color: ' + shape['color'] + ';' if not shape.get('background') else ''}
">{shape['symbol']}</div>
"""

        elif variant == "progress_ring":
            # Simple progress bar instead of ring for now
            percentage = shape["percentage"]
            return f"""
<div style="
    width: {shape['size']}px;
    height: 20px;
    background-color: {shape['background_color']};
    border-radius: 10px;
    overflow: hidden;
    position: relative;
">
    <div style="
        width: {percentage}%;
        height: 100%;
        background-color: {shape['progress_color']};
        transition: width 0.3s ease;
    "></div>
    <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        text-align: center;
        line-height: 20px;
        font-size: 12px;
        font-weight: bold;
        color: #333;
    ">{percentage}%</div>
</div>
"""

        return ""

    @staticmethod
    def render_border(border: Dict[str, Any], content: str = "Content") -> str:
        """Render border/container component to HTML"""
        variant = border.get("variant", "simple")

        padding = border.get("padding", 40)

        if variant == "simple":
            return f"""
<div style="
    border: {border['width']}px {border['style']} {border['color']};
    border-radius: {border['radius']}px;
    padding: {padding}px;
">{content}</div>
"""

        elif variant == "accent":
            side = border.get("side", "left")
            border_prop = {
                "left": "border-left",
                "right": "border-right",
                "top": "border-top",
                "bottom": "border-bottom",
            }.get(side, "border-left")

            return f"""
<div style="
    {border_prop}: {border['width']}px solid {border['color']};
    padding: {padding}px;
    padding-{side}: {padding + border['width']}px;
">{content}</div>
"""

        elif variant == "callout":
            return f"""
<div style="
    border: {border['border_width']}px solid {border['border_color']};
    background-color: {border['background_color']};
    border-radius: {border['border_radius']}px;
    padding: {padding}px;
">{content}</div>
"""

        elif variant == "shadow_frame":
            return f"""
<div style="
    {'border: ' + str(border['border_width']) + 'px solid ' + border['border_color'] + ';' if border['border_width'] > 0 else ''}
    border-radius: {border['border_radius']}px;
    padding: {padding}px;
    box-shadow: {border['shadow']};
">{content}</div>
"""

        return f"<div>{content}</div>"

    @staticmethod
    def render_background(
        background: Dict[str, Any], content: str = "Content", width: int = 400, height: int = 200
    ) -> str:
        """Render background component to HTML"""
        variant = background.get("variant", "solid")

        if variant == "solid":
            return f"""
<div style="
    background-color: {background['color']};
    width: {width}px;
    height: {height}px;
    padding: 20px;
">{content}</div>
"""

        elif variant == "gradient":
            direction_map = {
                "vertical": "to bottom",
                "horizontal": "to right",
                "diagonal": "to bottom right",
            }
            direction = direction_map.get(background.get("direction", "vertical"), "to bottom")

            return f"""
<div style="
    background: linear-gradient({direction}, {background['start_color']}, {background['end_color']});
    width: {width}px;
    height: {height}px;
    padding: 20px;
">{content}</div>
"""

        elif variant == "card":
            return f"""
<div style="
    background-color: {background['color']};
    box-shadow: {background['shadow']};
    border-radius: {background['border_radius']}px;
    padding: {background['padding']}px;
    width: {width}px;
">{content}</div>
"""

        elif variant == "highlight_box":
            return f"""
<div style="
    background-color: {background['background_color']};
    border: {background['border_width']}px solid {background['border_color']};
    border-radius: {background['border_radius']}px;
    padding: {background['padding']}px;
    width: {width}px;
">{content}</div>
"""

        return f"<div>{content}</div>"

    @staticmethod
    def render_components_grid(components: List[Dict[str, Any]], title: str = "") -> str:
        """Render multiple components in a grid"""
        html = ""

        if title:
            html += (
                f"<h2 style='margin-top: 40px; margin-bottom: 20px; color: #1a1a1a;'>{title}</h2>"
            )

        html += "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px;'>"

        for component in components:
            comp_type = component.get("type", "unknown")

            if comp_type == "divider":
                html += f"<div>{ComponentRenderer.render_divider(component)}</div>"
            elif comp_type == "badge":
                html += f"<div>{ComponentRenderer.render_badge(component)}</div>"
            elif comp_type == "shape":
                html += f"<div>{ComponentRenderer.render_shape(component)}</div>"
            elif comp_type == "border":
                html += f"<div>{ComponentRenderer.render_border(component, 'Sample Content')}</div>"
            elif comp_type == "background":
                html += f"<div>{ComponentRenderer.render_background(component, 'Sample Content', 250, 150)}</div>"

        html += "</div>"

        return html
