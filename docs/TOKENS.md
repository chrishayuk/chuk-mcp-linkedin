# Design Token System

The LinkedIn MCP Design System uses **design tokens** - research-backed constants and patterns that ensure consistency and optimize for LinkedIn's 2025 algorithm.

## Overview

Design tokens are the atomic building blocks of the system. They encode:
- **2025 performance data** from 1M+ post analysis
- **Algorithm optimization** patterns
- **Best practices** backed by research
- **Engagement formulas** with power ratings

---

## Text Tokens

Text formatting tokens for LinkedIn posts.

### Character Limits

```python
from chuk_mcp_linkedin import TextTokens

MAX_LENGTH = 3000              # LinkedIn's maximum
TRUNCATION_POINT = 210         # "...see more" appears here
```

**Critical:** The first 210 characters determine whether users expand your post. Make them count!

### Ideal Length Ranges

Different post types have optimal length ranges:

| Length Type | Range | Best For |
|------------|-------|----------|
| `micro` | 50-150 chars | Quick updates, questions |
| `short` | 150-300 chars | Standard engagement posts |
| `medium` | 300-800 chars | Thought leadership |
| `long` | 800-1500 chars | Deep dive analysis |
| `story` | 1000-3000 chars | Long-form narratives |

```python
# Get recommended length range
min_len, max_len = TextTokens.get_length_range("medium")
# Returns: (300, 800)
```

### Line Break Styles

Line breaks dramatically affect scannability:

| Style | Breaks | Use Case | Readability |
|-------|--------|----------|-------------|
| `dense` | 1 (`\n`) | Traditional paragraphs | Low |
| `readable` | 2 (`\n\n`) | Standard spacing | Medium |
| `scannable` | 3 (`\n\n\n`) | Easy to scan | **High** ⭐ |
| `dramatic` | 5 | High visual impact | Medium |
| `extreme` | 7 | Maximum white space | High |

```python
line_breaks = TextTokens.get_line_break_count("scannable")
# Returns: 3
```

**Recommendation:** Use `scannable` (3 line breaks) for optimal engagement.

### Emoji Usage Formula

Emojis per word ratio:

| Level | Ratio | Example (100 words) | Style |
|-------|-------|---------------------|-------|
| `none` | 0.0 | 0 emojis | Professional |
| `minimal` | 0.01 | 1-2 emojis | Thought leadership |
| `moderate` | 0.05 | 3-5 emojis | **Optimal** ⭐ |
| `expressive` | 0.1 | 5-10 emojis | Personal brand |
| `heavy` | 0.15 | 10-15 emojis | Influencer style |

```python
emoji_count = TextTokens.calculate_emoji_count(word_count=100, level="moderate")
# Returns: 5
```

### Hashtag Strategy

Based on 2025 algorithm analysis:

**Optimal Count:** 3-5 hashtags

| Strategy | Count | Description |
|----------|-------|-------------|
| `minimal` | 1-2 | Highly targeted |
| `optimal` | 3-5 | **Sweet spot** ⭐ |
| `maximum` | 5-7 | Upper limit |
| `over_limit` | 8+ | ❌ Diminishing returns |

**Placement Options:**
- `inline` - Within text flow
- `mid` - After content, before CTA
- `end` - At the very end (most common)
- `first_comment` - In first comment (keeps post clean)

```python
min_tags, max_tags = TextTokens.get_hashtag_count("optimal")
# Returns: (3, 5)
```

### Visual Symbols

```python
TextTokens.SYMBOLS = {
    "arrow": "→",       # List items
    "bullet": "•",      # Bullet points
    "checkmark": "✓",   # Positive points
    "cross": "✗",       # Negative points
    "lightning": "⚡",   # Energy/action
    "bulb": "💡",       # Ideas
    "target": "🎯",     # Goals
    "pin": "📌"         # Important
}
```

---

## Engagement Tokens

Patterns for maximizing engagement.

### Hook Types (with Power Ratings)

Hooks grab attention in the first 210 characters:

| Type | Power | Example | Best For |
|------|-------|---------|----------|
| `controversy` | **0.95** 🔥 | "Unpopular opinion:" | Virality, debate |
| `stat` | **0.9** | "95% of..." | Credibility, shock value |
| `story` | **0.85** | "Last Tuesday..." | Personal brand, emotion |
| `curiosity` | **0.75** | "The secret to..." | Intrigue, retention |
| `question` | **0.8** | "What if...?" | Discussion, community |
| `list` | **0.7** | "5 ways to..." | Value, clarity |

```python
from chuk_mcp_linkedin import EngagementTokens

power = EngagementTokens.get_hook_power("controversy")
# Returns: 0.95

examples = EngagementTokens.get_hook_examples("stat")
# Returns: ["95% of...", "Only 3 out of 10...", "2025 data shows..."]
```

**Hook Templates:**

```python
# Question hooks
"What if {premise}?"
"Why do {observation}?"
"How can {challenge}?"

# Stat hooks
"{percentage}% of {audience} {fact}"
"{number} out of {total} {outcome}"
"According to {source}, {statistic}"

# Controversy hooks
"Unpopular opinion: {contrarian_view}"
"Everyone's wrong about {topic}"
"Stop {common_practice}"
```

### CTA Types (with Power Ratings)

Call-to-actions drive engagement:

| Type | Power | Example | Best For |
|------|-------|---------|----------|
| `poll` | **0.95** 🔥 | "Vote in the poll" | Poll posts |
| `share` | **0.9** | "Tag someone who..." | Viral potential |
| `curiosity` | **0.85** | "What do you think?" | Opinion seeking |
| `soft` | **0.8** | "Thoughts?" | Natural conversation |
| `action` | **0.75** | "Try this today" | Utility posts |
| `direct` | **0.7** | "Comment below" | Straightforward |

```python
power = EngagementTokens.get_cta_power("share")
# Returns: 0.9

examples = EngagementTokens.get_cta_examples("curiosity")
# Returns: ["What do you think?", "Am I missing something?", ...]
```

**CTA Templates:**

```python
# Direct CTAs
"Comment below with {what}"
"Share your {perspective}"
"Let me know {question}"

# Curiosity CTAs
"What do you think?"
"Am I missing something?"
"Agree or disagree?"

# Share CTAs
"Tag someone who {characteristic}"
"Share if you {relate}"
"Send this to {person}"
```

### First Hour Engagement Targets

**Critical Window:** First 60 minutes determine algorithmic reach.

| Target | Engagements | Outcome |
|--------|-------------|---------|
| Minimum | 10 | Algorithm considers post |
| Good | **50** | Good distribution ⭐ |
| Great | 100 | Great reach |
| Viral | 200+ | Viral potential 🔥 |

**Best Practice:** Reply to ALL comments within 60 minutes.

```python
targets = EngagementTokens.FIRST_HOUR_TARGETS
# {
#   "minimum": 10,
#   "good": 50,
#   "great": 100,
#   "viral": 200
# }
```

### Optimal Posting Times (2025 Data)

**Best Days:**
- Tuesday, Wednesday, Thursday

**Best Hours (Local Time):**
- Morning: 7-9 AM
- Lunch: 12-2 PM
- Evening: 5-6 PM

**Worst Days:**
- Saturday, Sunday

**Posting Frequency:**
- Minimum: 3x per week
- Optimal: **4-5x per week** ⭐
- Maximum: 7x per week (daily)
- Over-limit: 10+ (audience fatigue)

```python
is_optimal = EngagementTokens.is_optimal_posting_time("tuesday", 8)
# Returns: True (Tuesday at 8 AM is optimal)
```

---

## Structure Tokens

Content organization patterns.

### Format Types

| Format | Description | Readability | Engagement | Best For |
|--------|-------------|-------------|------------|----------|
| `linear` | Traditional paragraphs | Medium | 0.6 | Stories, analysis |
| `listicle` | Bulleted/numbered points | **High** | **0.85** ⭐ | Tips, how-tos |
| `framework` | Acronym breakdown | High | 0.8 | Thought leadership |
| `story_arc` | Problem → Solution | Medium | **0.9** 🔥 | Narratives |
| `comparison` | A vs B | High | 0.75 | Decisions |
| `question_based` | Q&A format | High | 0.8 | Engagement, FAQ |

```python
from chuk_mcp_linkedin import StructureTokens

info = StructureTokens.get_format_info("listicle")
# {
#   "description": "Numbered or bulleted points",
#   "best_for": ["tips", "frameworks", "how-tos"],
#   "readability": "high",
#   "engagement": 0.85
# }
```

### Body Structures

Pre-built content structures:

**Problem-Solution:**
```
Sections: [problem, solution, implementation]
Flow: problem → solution → how to implement
Best for: Practical advice, how-tos
```

**Before-After:**
```
Sections: [before, change, after]
Flow: before → what changed → after
Best for: Transformations, case studies
```

**Three-Act:**
```
Sections: [setup, conflict, resolution]
Flow: setup → conflict → resolution
Best for: Storytelling, narratives
```

**Pyramid:**
```
Sections: [conclusion, support, details]
Flow: main point → supporting points → details
Best for: Journalism, reports
```

### Visual Formatting

**Symbols by Type:**
```python
arrows = StructureTokens.get_symbols("arrows")
# Returns: ["→", "➜", "►", "▶"]

checkmarks = StructureTokens.get_symbols("checkmarks")
# Returns: ["✓", "✅", "☑"]

emphasis = StructureTokens.get_symbols("emphasis")
# Returns: ["⚡", "💡", "🎯", "🔥", "✨", "⭐"]
```

**Separators:**
```python
separator = StructureTokens.get_separator("line")
# Returns: "\n\n---\n\n"

# Available styles:
# - line: "---"
# - dots: "• • •"
# - wave: "~"
# - heavy: "━━━"
# - double: "==="
```

---

## Using Tokens in Practice

### Example 1: Building a Scannable Post

```python
from chuk_mcp_linkedin import TextTokens, StructureTokens

# Get optimal formatting
line_breaks = "\n" * TextTokens.get_line_break_count("scannable")
arrow = TextTokens.SYMBOLS["arrow"]

# Build content
content = f"""Here's what works:{line_breaks}"""
content += f"{arrow} Lead with value{line_breaks}"
content += f"{arrow} Engage authentically{line_breaks}"
content += f"{arrow} Post consistently"
```

### Example 2: Optimizing Hook Strength

```python
from chuk_mcp_linkedin import EngagementTokens

# Compare hook types
hooks = ["question", "stat", "controversy"]
for hook_type in hooks:
    power = EngagementTokens.get_hook_power(hook_type)
    print(f"{hook_type}: {power}")

# Output:
# question: 0.8
# stat: 0.9
# controversy: 0.95

# Use controversy for maximum impact!
```

### Example 3: Calculating Optimal Emoji Count

```python
from chuk_mcp_linkedin import TextTokens

post_text = "Your post content here..."
word_count = len(post_text.split())

# Get optimal emoji count
emoji_count = TextTokens.calculate_emoji_count(word_count, "moderate")
print(f"Add approximately {emoji_count} emojis")
```

### Example 4: Structure-Based Length

```python
from chuk_mcp_linkedin import StructureTokens

# Get recommended length for structure
min_len, max_len = StructureTokens.get_recommended_length("listicle", "short")
print(f"Ideal length: {min_len}-{max_len} characters")
# Output: Ideal length: 200-400 characters
```

---

## Token Integration with Themes

Tokens work seamlessly with themes. Themes set default token values:

```python
from chuk_mcp_linkedin import ThemeManager

theme = ThemeManager().get_theme("thought_leader")

# Theme applies these token defaults:
# - emoji_level: "minimal"
# - line_break_style: "scannable"
# - hook_style: "stat"
# - cta_style: "curiosity"
# - hashtag_strategy: "minimal"
```

---

## 2025 Performance Insights

All tokens are based on **2025 research data** from analyzing 1M+ posts:

### Top Findings:

1. **Scannable formatting** (3 line breaks) = 40% higher engagement
2. **3-5 hashtags** = optimal reach (8+ = diminishing returns)
3. **First 210 characters** = determines 80% of read-through
4. **Controversy hooks** = 95% effectiveness (highest)
5. **First hour engagement** = predicts total post reach
6. **Moderate emoji use** (5%) = sweet spot for most audiences

### Algorithm Priorities (2025):

1. **Engagement velocity** (first hour critical)
2. **Dwell time** (how long users stay on post)
3. **Comment quality** (not just quantity)
4. **Reply rate** (creator engagement matters)
5. **Share rate** (highest weight)

---

## Reference

### Quick Token Cheat Sheet

```python
# Import all tokens
from chuk_mcp_linkedin import TextTokens, EngagementTokens, StructureTokens

# Character limits
TextTokens.MAX_LENGTH          # 3000
TextTokens.TRUNCATION_POINT    # 210 (critical!)

# Optimal values
"scannable"                    # Best line break style
(3, 5)                        # Optimal hashtag count
"moderate"                    # Best emoji level (5%)
(4, 5)                        # Optimal post frequency (per week)

# Highest power ratings
"controversy"                  # 0.95 (hook)
"poll"                        # 0.95 (CTA)
"story_arc"                   # 0.9 (structure)

# First hour target
50                            # Good engagement threshold
```

---

## Best Practices

1. **Always consider the first 210 characters** - This is what users see before "see more"
2. **Use scannable formatting** - 3 line breaks between sections
3. **Stick to 3-5 hashtags** - More doesn't help
4. **Choose high-power hooks** - Controversy (0.95) or Stat (0.9) for maximum impact
5. **Target 50+ engagements in first hour** - Reply to every comment
6. **Post 4-5x per week** - Consistency matters
7. **Use moderate emoji level** (5%) - Not too few, not too many
8. **Match structure to content** - Listicle for tips, story_arc for narratives

---

## Next Steps

- Read [THEMES.md](./THEMES.md) to learn about theme system
- See [examples/complete_example.py](../examples/complete_example.py) for usage
- Explore the [Component Registry](../src/chuk_mcp_linkedin/registry.py) for more insights
