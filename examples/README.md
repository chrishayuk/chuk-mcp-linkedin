# LinkedIn Design System - Examples

Comprehensive examples demonstrating the complete design system with interactive HTML rendering.

## Quick Start

```bash
# Generate interactive HTML showcase of all components
python examples/comprehensive_showcase.py
# Opens: ~/.linkedin_drafts/previews/comprehensive_showcase.html

# Show design tokens with visual examples
python examples/tokens_showcase.py

# Create and preview a LinkedIn post
python examples/preview_example.py

# Complete usage example
python examples/complete_example.py
```

## Examples

### 1. Comprehensive Showcase (`comprehensive_showcase.py`) ⭐

**The main showcase** - Interactive HTML rendering of all 91+ component variants

**Generates:** `~/.linkedin_drafts/previews/comprehensive_showcase.html` (51KB)

**Includes:**
- **Visual Elements (38 variants)**
  - Dividers (6 types)
  - Badges (7 types)
  - Borders (8 types)
  - Shapes (9 types)
  - Backgrounds (8 types)

- **Typography (31 variants)**
  - Headers (7 types)
  - Body Text (7 types)
  - Captions (6 types)
  - Quotes (4 types)
  - Lists (7 types)

- **Data Visualization (22 variants)**
  - Charts (8 types)
  - Metrics (5 types)
  - Progress (5 types)
  - Tables (5 types)
  - Infographics (6 types)

**Features:**
- ✅ Fully rendered HTML components
- ✅ Interactive browser preview
- ✅ Professional showcase styling
- ✅ Grouped by category
- ✅ Descriptive explanations
- ✅ All components use design tokens

**Run:**
```bash
python examples/comprehensive_showcase.py
# Automatically generates HTML and shows path
# Open the file in your browser to view
```

**Preview:**
```html
Component Showcase - Complete Library

TYPOGRAPHY COMPONENTS
└─ Headers
   ├─ H1 - Display Header (72pt, 900 weight)
   ├─ H2 - Large Header (56pt)
   └─ Eyebrow Text (18pt uppercase)

DATA VISUALIZATION COMPONENTS
└─ Charts
   ├─ Bar Chart (with value labels)
   ├─ Pie Chart (proportional segments)
   └─ Line Chart (smooth curves)
```

### 2. Tokens Showcase (`tokens_showcase.py`)

**Shows:** Design token system with visual examples

**Includes:**
- Typography tokens (font sizes, weights, line heights)
- Color schemes (LinkedIn brand, semantic colors)
- Spacing tokens (gaps, padding, safe areas)
- Layout properties (border radius, shadows)
- LinkedIn 2025 optimizations
- All 11 document layout types

**Run:**
```bash
python examples/tokens_showcase.py
```

**Output:**
```
TYPOGRAPHY TOKENS - VISUAL RENDERING
  TINY (14pt)     ← Too small for mobile ✗
  SMALL (18pt)    ← Minimum for mobile ✓
  BODY (24pt)     ← Standard text
  LARGE (32pt)    ← Lead text
  TITLE (56pt)    ← Headers
  HERO (120pt)    ← Big numbers
  MASSIVE (200pt) ← Huge stats
```

### 3. Preview Example (`preview_example.py`)

**Shows:** End-to-end LinkedIn post creation and HTML preview

**Includes:**
- Creating posts with LinkedInManager
- Content composition with themes
- HTML preview generation
- Auto-opening in browser

**Run:**
```bash
python examples/preview_example.py
# Creates a post and opens preview in browser
```

### 4. Complete Example (`complete_example.py`)

**Shows:** Complete usage of all system features

**Run:**
```bash
python examples/complete_example.py
```

## Component System Architecture

```
src/chuk_mcp_linkedin/
├── tokens/                      # Design tokens
│   ├── design_tokens.py         # Visual design (typography, colors, spacing)
│   ├── text_tokens.py           # Content formatting rules
│   ├── engagement_tokens.py     # Algorithm optimization
│   └── structure_tokens.py      # Content structure patterns
│
├── components/                  # Component library
│   ├── layouts/                 # 11 document layouts
│   │   └── document_layouts.py
│   ├── visual_elements/         # 38 visual components
│   │   ├── dividers.py
│   │   ├── badges.py
│   │   ├── borders.py
│   │   ├── shapes.py
│   │   └── backgrounds.py
│   ├── typography/              # 31 typography components
│   │   ├── headers.py
│   │   ├── body_text.py
│   │   ├── captions.py
│   │   ├── quotes.py
│   │   └── lists.py
│   └── data_viz/                # 22 data viz components
│       ├── charts.py
│       ├── metrics.py
│       ├── progress.py
│       ├── tables.py
│       └── infographics.py
│
├── renderer.py                  # HTML component renderer
└── preview.py                   # LinkedIn post previewer
```

## System Completion Status

| Category | Components | Status |
|----------|------------|--------|
| **Layouts** | 11 layouts | ✅ 100% |
| **Visual Elements** | 38 variants | ✅ 100% |
| **Typography** | 31 variants | ✅ 100% |
| **Data Visualization** | 22 variants | ✅ 100% |
| **Content Blocks** | 10 planned | ⏳ Phase 2 |
| **Media** | 4 planned | ⏳ Phase 2 |
| **Interactive** | 3 planned | ⏳ Phase 3 |

**Current:** 68/85 components (80% complete)

## Token-Based Design

All components reference design tokens for consistency:

```python
# Typography
from chuk_mcp_linkedin.tokens.design_tokens import DesignTokens

font_size = DesignTokens.get_font_size('title')      # 56pt
font_weight = DesignTokens.TYPOGRAPHY['weights']['bold']  # 700

# Colors
color = DesignTokens.get_color('minimal', 'accent')  # #0A66C2
success = DesignTokens.COLORS['semantic']['success'] # #057642

# Spacing
gap = DesignTokens.get_spacing('gaps', 'large')      # 40px
padding = DesignTokens.SPACING['padding']['normal']  # 40px
```

## Usage Example

```python
from chuk_mcp_linkedin.components.typography import Headers, Lists
from chuk_mcp_linkedin.components.data_viz import Charts, Metrics
from chuk_mcp_linkedin.renderer import ShowcaseRenderer

# Create components
title = Headers.h2("Q4 2024 Results")
chart = Charts.bar_chart([
    {"label": "Q1", "value": 100},
    {"label": "Q2", "value": 150},
])
metric = Metrics.metric_card(
    label="Revenue",
    value="$1.2M",
    change=12.5
)

# Render to HTML
sections = [{
    "title": "Performance Dashboard",
    "components": [
        {"name": "Title", "component": title},
        {"name": "Growth Chart", "component": chart},
        {"name": "Revenue Metric", "component": metric},
    ]
}]

html = ShowcaseRenderer.create_showcase_page(
    title="My Dashboard",
    sections=sections
)
```

## LinkedIn 2025 Optimizations

All components follow LinkedIn's 2025 best practices:

✅ **Mobile-First:** 18pt minimum font size
✅ **Document Posts:** 45.85% engagement (highest format)
✅ **Character Limits:** 3000 max, 300-800 optimal
✅ **Hashtags:** 3-5 optimal
✅ **Visual Hierarchy:** Token-based typography scale
✅ **Accessibility:** WCAG compliant contrast ratios
✅ **Responsive:** Works on all LinkedIn platforms

## Next Steps

1. **Explore:** Run `comprehensive_showcase.py` to see all components
2. **Build:** Use components in your LinkedIn content
3. **Extend:** Add Phase 2 components (Content Blocks, Media)
4. **Share:** Export designs as HTML previews

---

**Total System:** 11 layouts + 91 component variants + complete token system = Production-ready LinkedIn design system
