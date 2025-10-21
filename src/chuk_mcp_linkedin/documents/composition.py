"""
Composition system for building LinkedIn documents from atomic components.

Similar to posts.composition but for visual document formats (PDF/PowerPoint/HTML).
Follows shadcn/ui atomic composition pattern with DesignTokens integration.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from .components.base import DocumentComponent, RenderContext
from .layouts import DocumentLayouts
from ..tokens.design_tokens import DesignTokens
from ..themes.theme_manager import LinkedInTheme


@dataclass
class Slide:
    """Represents a single slide in a document"""

    layout_name: str
    components: List[DocumentComponent] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Content slots (populated from components or direct values)
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    content_2: Optional[str] = None
    image_path: Optional[str] = None

    def add_component(self, component: DocumentComponent) -> "Slide":
        """Add a component to this slide"""
        self.components.append(component)
        return self

    def set_title(self, title: str) -> "Slide":
        """Set slide title"""
        self.title = title
        return self

    def set_subtitle(self, subtitle: str) -> "Slide":
        """Set slide subtitle"""
        self.subtitle = subtitle
        return self

    def set_content(self, content: str) -> "Slide":
        """Set slide content"""
        self.content = content
        return self

    def set_content_2(self, content: str) -> "Slide":
        """Set second content area (for two-column layouts)"""
        self.content_2 = content
        return self

    def set_image(self, image_path: str) -> "Slide":
        """Set image for slide"""
        self.image_path = image_path
        return self


class ComposableDocument:
    """
    Shadcn-style composition for LinkedIn documents.

    Similar to ComposablePost but for visual formats (PDF, PowerPoint, HTML).
    """

    def __init__(
        self,
        format_type: str = "pdf",  # pdf, pptx, html
        canvas_size: str = "document_square",
        color_scheme: str = "minimal",
        theme: Optional[LinkedInTheme] = None,
    ):
        self.format_type = format_type
        self.canvas_size = canvas_size
        self.color_scheme = color_scheme
        self.theme = theme
        self.slides: List[Slide] = []
        self.metadata: Dict[str, Any] = {
            "title": None,
            "author": None,
            "description": None,
        }

    def add_slide(self, layout_name: str) -> Slide:
        """
        Add a new slide with the specified layout.

        Returns the slide for chaining (fluent API).
        """
        slide = Slide(layout_name=layout_name)
        self.slides.append(slide)
        return slide

    def set_metadata(self, title: Optional[str] = None, author: Optional[str] = None,
                     description: Optional[str] = None) -> "ComposableDocument":
        """Set document metadata"""
        if title:
            self.metadata["title"] = title
        if author:
            self.metadata["author"] = author
        if description:
            self.metadata["description"] = description
        return self

    def validate(self) -> bool:
        """Validate document composition"""
        # Check minimum slide count
        min_slides = DesignTokens.LINKEDIN_SPECIFIC["document_slides"]["min"]
        max_slides = DesignTokens.LINKEDIN_SPECIFIC["document_slides"]["max"]

        if len(self.slides) < min_slides:
            raise ValueError(f"Document needs at least {min_slides} slides (has {len(self.slides)})")

        if len(self.slides) > max_slides:
            print(f"Warning: {len(self.slides)} slides exceeds recommended max of {max_slides}")

        # Validate each slide's components
        for i, slide in enumerate(self.slides):
            for component in slide.components:
                if not component.validate():
                    raise ValueError(f"Invalid component in slide {i + 1}: {component.__class__.__name__}")

        return True

    def render(self) -> str:
        """
        Render document to output format.

        Returns HTML by default. PDF/PPTX rendering requires additional libraries.
        """
        self.validate()

        if self.format_type == "html":
            return self._render_html()
        elif self.format_type == "pdf":
            # TODO: Implement PDF rendering with reportlab
            raise NotImplementedError("PDF rendering not yet implemented")
        elif self.format_type == "pptx":
            # TODO: Implement PowerPoint rendering with python-pptx
            raise NotImplementedError("PowerPoint rendering not yet implemented")
        else:
            raise ValueError(f"Unknown format: {self.format_type}")

    def _render_html(self) -> str:
        """Render document as HTML"""
        html_slides = []

        for i, slide in enumerate(self.slides):
            # Get layout configuration
            layout = DocumentLayouts.get_layout(slide.layout_name)

            # Create render context
            context = RenderContext(
                canvas_size=self.canvas_size,
                theme=self.theme,
                color_scheme=self.color_scheme,
                layout=layout,
                slide_index=i,
                format="html",
            )

            # Render slide
            slide_html = self._render_slide(slide, layout, context)
            html_slides.append(slide_html)

        # Wrap in document structure
        return self._wrap_html_document(html_slides)

    def _render_slide(self, slide: Slide, layout: Any, context: RenderContext) -> str:
        """Render a single slide"""
        canvas_width = context.canvas_width
        canvas_height = context.canvas_height
        safe_area = context.get_safe_area()

        # Build slide HTML
        slide_html = f"""
        <div class="slide" style="
            position: relative;
            width: {canvas_width}px;
            height: {canvas_height}px;
            background: {context.background_color};
            page-break-after: always;
        ">
        """

        # Render content zones from layout
        if layout.title_zone and slide.title:
            slide_html += self._render_zone(
                layout.title_zone, slide.title, "title", context
            )

        if layout.subtitle_zone and slide.subtitle:
            slide_html += self._render_zone(
                layout.subtitle_zone, slide.subtitle, "subtitle", context
            )

        if layout.content_zone and slide.content:
            slide_html += self._render_zone(
                layout.content_zone, slide.content, "content", context
            )

        if layout.content_zone_2 and slide.content_2:
            slide_html += self._render_zone(
                layout.content_zone_2, slide.content_2, "content-2", context
            )

        # Render custom components
        for component in slide.components:
            component_html = component.render(context)
            slide_html += component_html

        slide_html += "</div>"
        return slide_html

    def _render_zone(self, zone: Any, content: str, zone_type: str,
                     context: RenderContext) -> str:
        """Render a layout zone"""
        # Use font sizes directly from DesignTokens - they're already in pixels
        font_size = zone.font_size if zone.font_size else 24

        return f"""
        <div class="zone zone-{zone_type}" style="
            position: absolute;
            left: {zone.x}px;
            top: {zone.y}px;
            width: {zone.width}px;
            height: {zone.height}px;
            font-family: {context.font_family};
            font-size: {font_size}px;
            font-weight: {zone.font_weight or 'normal'};
            line-height: {zone.line_height or 1.5};
            text-align: {zone.align};
            color: {zone.color or context.primary_color};
            overflow: hidden;
        ">
            {content}
        </div>
        """

    def _wrap_html_document(self, slides_html: List[str]) -> str:
        """Wrap slides in complete HTML document"""
        slides_combined = "\n".join(slides_html)

        # Get colors and styles from design tokens
        page_bg = DesignTokens.COLORS["modern"]["background"]  # #F8F9FA
        slide_bg = DesignTokens.get_color(self.color_scheme, "background")
        shadow = DesignTokens.VISUAL["shadow"]["lg"]
        padding = DesignTokens.get_spacing("padding", "normal")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.metadata.get('title', 'LinkedIn Document')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: {DesignTokens.TYPOGRAPHY['fonts']['sans']};
            background: {page_bg};
            padding: {padding}px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .slide {{
            margin: 0 0 {padding}px 0;
            box-shadow: {shadow};
            background: {slide_bg};
            /* Scale down for browser display - slides are 1920x1920 */
            transform: scale(0.6);
            transform-origin: top center;
        }}

        .zone {{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            padding: 20px;
        }}

        @media print {{
            body {{
                padding: 0;
                background: white;
            }}

            .slide {{
                margin: 0;
                box-shadow: none;
                transform: none;
                page-break-after: always;
            }}
        }}
    </style>
</head>
<body>
    {slides_combined}
</body>
</html>"""

    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary"""
        return {
            "format_type": self.format_type,
            "canvas_size": self.canvas_size,
            "color_scheme": self.color_scheme,
            "metadata": self.metadata,
            "slide_count": len(self.slides),
            "slides": [
                {
                    "layout": slide.layout_name,
                    "title": slide.title,
                    "component_count": len(slide.components),
                }
                for slide in self.slides
            ],
        }


class DocumentBuilder:
    """Pre-built document patterns for common use cases"""

    @staticmethod
    def pitch_deck(
        title: str,
        problem: str,
        solution: str,
        traction: Dict[str, Any],
        team: List[str],
        ask: str,
        theme: Optional[LinkedInTheme] = None,
    ) -> ComposableDocument:
        """Pre-built pitch deck pattern"""
        doc = ComposableDocument(format_type="html", theme=theme)
        doc.set_metadata(title=title, description="Pitch Deck")

        # Title slide
        doc.add_slide("title_slide")\
           .set_title(title)\
           .set_subtitle("Company Pitch Deck")

        # Problem slide
        doc.add_slide("content_slide")\
           .set_title("The Problem")\
           .set_content(problem)

        # Solution slide
        doc.add_slide("content_slide")\
           .set_title("Our Solution")\
           .set_content(solution)

        # Traction slide
        doc.add_slide("big_number")\
           .set_title(str(traction.get("main_metric", "")))\
           .set_subtitle(traction.get("description", ""))

        # Team slide
        doc.add_slide("content_slide")\
           .set_title("Our Team")\
           .set_content("\n".join(f"• {member}" for member in team))

        # Ask slide
        doc.add_slide("content_slide")\
           .set_title("The Ask")\
           .set_content(ask)

        return doc

    @staticmethod
    def quarterly_report(
        quarter: str,
        highlights: List[str],
        metrics: Dict[str, str],
        goals: List[str],
        theme: Optional[LinkedInTheme] = None,
    ) -> ComposableDocument:
        """Pre-built quarterly report pattern"""
        doc = ComposableDocument(format_type="html", theme=theme)
        doc.set_metadata(title=f"{quarter} Report", description="Quarterly Report")

        # Title
        doc.add_slide("title_slide")\
           .set_title(f"{quarter} Report")\
           .set_subtitle("Performance Highlights")

        # Highlights
        doc.add_slide("content_slide")\
           .set_title("Key Highlights")\
           .set_content("\n".join(f"• {h}" for h in highlights))

        # Metrics (use data visual for charts)
        doc.add_slide("data_visual")\
           .set_title("Performance Metrics")

        # Goals
        doc.add_slide("checklist")\
           .set_title("Next Quarter Goals")\
           .set_content("\n".join(f"☐ {g}" for g in goals))

        return doc

    @staticmethod
    def product_launch(
        product_name: str,
        tagline: str,
        features: List[str],
        benefits: List[str],
        cta: str,
        theme: Optional[LinkedInTheme] = None,
    ) -> ComposableDocument:
        """Pre-built product launch pattern"""
        doc = ComposableDocument(format_type="html", theme=theme)
        doc.set_metadata(title=product_name, description="Product Launch")

        # Title
        doc.add_slide("title_slide")\
           .set_title(product_name)\
           .set_subtitle(tagline)

        # Features
        doc.add_slide("icon_grid")\
           .set_title("Features")\
           .set_content("\n\n".join(features))

        # Benefits
        doc.add_slide("content_slide")\
           .set_title("Benefits")\
           .set_content("\n".join(f"✓ {b}" for b in benefits))

        # CTA
        doc.add_slide("content_slide")\
           .set_title("Get Started")\
           .set_content(cta)

        return doc
