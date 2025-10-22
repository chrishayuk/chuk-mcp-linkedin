"""
Complete showcase of ALL LinkedIn post components with HTML preview.

Demonstrates every component type available in the system:
- Post structure components (Hook, Body, CTA, Hashtags, Separator)
- Chart components (Bar, Metrics, Comparison, Progress, Ranking)
- Feature components (Quote, BigStat, Timeline, KeyTakeaway, ProCon)
- Combined examples

Each example generates an interactive HTML preview.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.preview import LinkedInPreview
from chuk_mcp_linkedin.themes import ThemeManager


def save_preview(post: ComposablePost, name: str, description: str) -> str:
    """Generate and save HTML preview for a post"""
    text = post.compose()

    # Create draft data
    draft_data = {"name": name, "post_type": "text", "content": {"composed_text": text}}

    # Create stats
    stats = {
        "char_count": len(text),
        "word_count": len(text.split()),
        "char_remaining": 3000 - len(text),
        "hashtag_count": sum(1 for c in post.components if c.__class__.__name__ == "Hashtags"),
        "has_hook": any(c.__class__.__name__ == "Hook" for c in post.components),
        "has_cta": any(c.__class__.__name__ == "CallToAction" for c in post.components),
    }

    # Generate HTML
    html = LinkedInPreview.generate_html(draft_data, stats)

    # Save to file
    output_dir = Path.home() / ".linkedin_drafts" / "previews" / "showcase"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time())
    filename = f"{name.lower().replace(' ', '_')}_{timestamp}.html"
    filepath = output_dir / filename

    saved_path = LinkedInPreview.save_preview(html, str(filepath))

    print(f"✅ {name}")
    print(f"   {description}")
    print(f"   {len(text)} chars | {len(post.components)} components")
    print()

    return saved_path


# ==============================================================================
# POST STRUCTURE COMPONENTS
# ==============================================================================


def demo_post_structure():
    """Showcase all post structure components"""
    print("\n" + "=" * 70)
    print("POST STRUCTURE COMPONENTS")
    print("=" * 70 + "\n")

    theme_mgr = ThemeManager()
    theme = theme_mgr.get_theme("thought_leader")

    post = ComposablePost("text", theme=theme)

    # Hook types
    post.add_hook("stat", "95% of LinkedIn posts use the wrong structure")

    # Body with different structures
    post.add_body("Here's what actually works in 2025:", structure="linear")

    post.add_body(
        """Strong opening hook
Clear value proposition
Scannable format
Compelling CTA""",
        structure="listicle",
    )

    # Separators
    post.add_separator("line")

    post.add_body("The difference? Engagement rates 3x higher.", structure="linear")

    # Multiple separator styles
    post.add_separator("dots")

    # CTA types
    post.add_cta("curiosity", "What structure do you use for your posts?")

    # Hashtags
    post.add_hashtags(["LinkedIn", "ContentStrategy", "Engagement"])

    return save_preview(
        post,
        "Post Structure Showcase",
        "Hook, Body (listicle), Separators (line/dots), CTA, Hashtags",
    )


# ==============================================================================
# CHART COMPONENTS
# ==============================================================================


def demo_bar_chart():
    """Bar chart with colored emoji squares"""
    post = ComposablePost("text")
    post.add_hook("stat", "📊 Where developers spend their time in 2025")
    post.add_body("We surveyed 500 developers to understand the AI impact:")
    post.add_bar_chart(
        data={
            "AI-Assisted Coding": 12,
            "Code Review": 6,
            "Documentation": 4,
            "Debugging": 8,
            "Meetings": 10,
        },
        title="HOURS SAVED PER WEEK",
        unit="hours",
    )
    post.add_cta("curiosity", "How much time do AI tools save you?")
    post.add_hashtags(["AI", "Productivity", "Development"])

    return save_preview(post, "Bar Chart", "Horizontal bars with colored emoji squares")


def demo_metrics_chart():
    """Metrics with ✅/❌ indicators"""
    post = ComposablePost("text")
    post.add_hook("stat", "📈 AI Impact on Software Development")
    post.add_body("The data is clear - AI tools are transforming how we work:")
    post.add_metrics_chart(
        data={
            "Faster problem-solving": "67%",
            "Fewer bugs in production": "54%",
            "Better code documentation": "89%",
            "Improved team collaboration": "72%",
        },
        title="KEY IMPROVEMENTS",
    )
    post.add_separator("line")
    post.add_body("These aren't marginal gains. They're fundamental shifts.")
    post.add_cta("curiosity", "What impact are you seeing?")
    post.add_hashtags(["AI", "SoftwareEngineering", "Metrics"])

    return save_preview(post, "Metrics Chart", "KPI metrics with ✅/❌ indicators")


def demo_comparison_chart():
    """A vs B comparison"""
    post = ComposablePost("text")
    post.add_hook("question", "Traditional vs AI-Assisted Development: Which wins?")
    post.add_body("After 6 months of testing with our 50-person team:")
    post.add_comparison_chart(
        data={
            "Traditional Approach": [
                "Manual code completion",
                "Slower debugging",
                "Limited context awareness",
                "Manual test writing",
            ],
            "AI-Assisted Approach": [
                "Intelligent completions",
                "Faster bug detection",
                "Context-aware suggestions",
                "Automated test generation",
            ],
        },
        title="DEVELOPMENT APPROACHES",
    )
    post.add_separator("dots")
    post.add_body("The verdict: AI-assisted is 40% faster with better quality.")
    post.add_cta("action", "Time to upgrade your workflow")
    post.add_hashtags(["AI", "Development", "Productivity"])

    return save_preview(post, "Comparison Chart", "Side-by-side A vs B comparison")


def demo_progress_chart():
    """Progress bars (0-100%)"""
    post = ComposablePost("text")
    post.add_hook("story", "🚀 Our AI Platform Launch - 2 Weeks Out")
    post.add_body("Transparency matters. Here's exactly where we stand:")
    post.add_progress_chart(
        data={
            "Backend API": 95,
            "Frontend UI": 85,
            "Testing Suite": 70,
            "Documentation": 60,
            "Marketing Site": 45,
        },
        title="LAUNCH READINESS",
    )
    post.add_separator("line")
    post.add_body("The team is crushing it. Launch day: January 15th.")
    post.add_cta("curiosity", "What should we focus on next?")
    post.add_hashtags(["Startup", "ProductLaunch", "BuildInPublic"])

    return save_preview(post, "Progress Chart", "Progress bars showing 0-100% completion")


def demo_ranking_chart():
    """Ranked list with medals"""
    post = ComposablePost("text")
    post.add_hook("list", "🏆 Most In-Demand Programming Languages (2025)")
    post.add_body("Based on our analysis of 10K job postings:")
    post.add_ranking_chart(
        data={
            "Python": "35% of all postings",
            "JavaScript": "28% of all postings",
            "TypeScript": "22% of all postings",
            "Go": "8% of all postings",
            "Rust": "7% of all postings",
        },
        title="TOP 5 LANGUAGES",
        show_medals=True,
    )
    post.add_separator("line")
    post.add_body("Python dominates, but TypeScript is growing fastest (+40% YoY).")
    post.add_cta("curiosity", "What language are you learning next?")
    post.add_hashtags(["Programming", "CareerDevelopment", "TechTrends"])

    return save_preview(post, "Ranking Chart", "Ranked list with medal emojis for top 3")


# ==============================================================================
# FEATURE COMPONENTS
# ==============================================================================


def demo_quote():
    """Quote/testimonial"""
    post = ComposablePost("text")
    post.add_hook("story", "💡 Customer Success Story: 80% Faster Deployments")
    post.add_body("One year ago, TechCorp was struggling with slow, error-prone deployments.")
    post.add_separator("line")
    post.add_quote(
        text="AI-assisted development has transformed our team. We're shipping 10x faster with 50% fewer bugs. It's not hype - it's measurable impact.",
        author="Sarah Chen",
        source="CTO at TechCorp",
    )
    post.add_separator("line")
    post.add_body("Today, they deploy 20+ times per day with confidence.")
    post.add_cta("soft", "What's your biggest deployment challenge?")
    post.add_hashtags(["CustomerSuccess", "DevOps", "AI"])

    return save_preview(post, "Quote Component", "Quote/testimonial with attribution")


def demo_big_stat():
    """Big eye-catching statistic"""
    post = ComposablePost("text")
    post.add_hook("stat", "The State of AI in Development (2025)")
    post.add_separator("dots")
    post.add_big_stat(
        number="2.5M",
        label="developers using AI coding tools daily",
        context="↑ 340% growth year-over-year (2024 → 2025)",
    )
    post.add_separator("dots")
    post.add_body("This explosive growth is fundamentally changing software development.")
    post.add_body("The question isn't WHETHER to adopt AI tools.")
    post.add_body("It's HOW QUICKLY you can integrate them effectively.")
    post.add_separator("line")
    post.add_cta("action", "Don't get left behind")
    post.add_hashtags(["AI", "Development", "FutureTech"])

    return save_preview(post, "Big Stat", "Eye-catching statistic with context")


def demo_timeline():
    """Timeline/journey"""
    post = ComposablePost("text")
    post.add_hook("story", "🚀 How We Built a $10M ARR SaaS in 24 Months")
    post.add_body("The complete journey from idea to Series A:")
    post.add_timeline(
        steps={
            "Jan 2023": "Launched MVP with 10 beta users",
            "Apr 2023": "First paying customer ($99/mo)",
            "Aug 2023": "Reached 100 customers ($10K MRR)",
            "Dec 2023": "Hit $100K MRR milestone",
            "Apr 2024": "Crossed $500K MRR",
            "Aug 2024": "Raised Series A ($5M)",
            "Dec 2024": "$10M ARR achieved",
        },
        title="OUR GROWTH JOURNEY",
        style="arrow",
    )
    post.add_separator("line")
    post.add_body("Key lesson: Focus on solving real problems, not chasing trends.")
    post.add_cta("curiosity", "What milestone are you working toward?")
    post.add_hashtags(["Startup", "SaaS", "Growth"])

    return save_preview(post, "Timeline", "Timeline/journey with arrow-separated steps")


def demo_key_takeaway():
    """Highlighted key takeaway box"""
    post = ComposablePost("text")
    post.add_hook("question", "Why do 90% of startups fail?")
    post.add_body("I analyzed 500 failed startups over the past 5 years.")
    post.add_separator("line")
    post.add_body("The pattern was crystal clear:")
    post.add_body("❌ Built solutions looking for problems")
    post.add_body("❌ Optimized for vanity metrics")
    post.add_body("❌ Ignored customer feedback")
    post.add_body("❌ Ran out of cash chasing growth")
    post.add_separator("line")
    post.add_key_takeaway(
        message="Focus on solving REAL problems for REAL customers. Revenue beats vanity metrics every time. Listen to your customers, not your ego.",
        title="THE KEY LESSON",
        style="box",
    )
    post.add_separator("line")
    post.add_cta("soft", "What's the hardest lesson you've learned?")
    post.add_hashtags(["Startups", "Entrepreneurship", "Lessons"])

    return save_preview(post, "Key Takeaway", "Highlighted insight/TLDR box")


def demo_pro_con():
    """Pros & cons comparison"""
    post = ComposablePost("text")
    post.add_hook("question", "Should your team adopt AI coding tools?")
    post.add_body("We tested GitHub Copilot for 6 months with our 50-person engineering team.")
    post.add_body("Here's the honest breakdown:")
    post.add_separator("line")
    post.add_pro_con(
        pros=[
            "40% faster development cycle",
            "Fewer production bugs (-30%)",
            "Better code documentation",
            "Improved developer satisfaction",
            "Faster onboarding for new hires",
        ],
        cons=[
            "Initial learning curve (2-3 weeks)",
            "Cost: $20-40 per developer/month",
            "Requires updated code review process",
            "Occasional incorrect suggestions",
        ],
        title="AI CODING TOOLS",
    )
    post.add_separator("line")
    post.add_body("Our verdict: The ROI is undeniable. We're going all-in.")
    post.add_cta("curiosity", "Have you tried AI coding tools? What's your experience?")
    post.add_hashtags(["AI", "Development", "TechLeadership"])

    return save_preview(post, "Pro-Con", "Pros & cons for decision-making")


# ==============================================================================
# COMBINED EXAMPLES
# ==============================================================================


def demo_combined_comprehensive():
    """Comprehensive post using multiple component types"""
    theme_mgr = ThemeManager()
    theme = theme_mgr.get_theme("thought_leader")

    post = ComposablePost("text", theme=theme)

    # Strong hook
    post.add_hook("stat", "📊 The Complete State of AI in Software Development (2025)")

    # Opening context
    post.add_body("We analyzed 1M+ developers across 50K companies.")
    post.add_body("The findings are remarkable:")

    post.add_separator("line")

    # Big stat
    post.add_big_stat(
        number="95%",
        label="of Fortune 500 engineering teams now use AI tools",
        context="Up from 23% in 2023",
    )

    post.add_separator("dots")

    # Timeline of adoption
    post.add_timeline(
        steps={
            "2022": "Early adopters experiment (5%)",
            "2023": "Mainstream awareness (23%)",
            "2024": "Rapid adoption begins (67%)",
            "2025": "AI becomes standard (95%)",
        },
        title="ADOPTION CURVE",
        style="arrow",
    )

    post.add_separator("line")

    # Metrics showing impact
    post.add_body("The impact on productivity:")
    post.add_metrics_chart(
        data={
            "Faster development": "67%",
            "Fewer bugs": "54%",
            "Better documentation": "89%",
            "Higher job satisfaction": "72%",
        },
        title="MEASURED IMPROVEMENTS",
    )

    post.add_separator("line")

    # Customer quote
    post.add_quote(
        text="AI tools have fundamentally changed how we approach software development. It's not about replacing developers - it's about amplifying their capabilities.",
        author="Emily Rodriguez",
        source="VP Engineering at Scale AI",
    )

    post.add_separator("dots")

    # Key takeaway
    post.add_key_takeaway(
        message="The question isn't WHETHER to adopt AI development tools. It's HOW QUICKLY you can integrate them to stay competitive.",
        style="box",
    )

    post.add_separator("line")

    # Strong CTA
    post.add_cta("action", "Start your AI transformation today")

    # Hashtags
    post.add_hashtags(["AI", "SoftwareDevelopment", "FutureTech", "Leadership"])

    return save_preview(
        post,
        "Comprehensive Showcase",
        "Multiple components: BigStat, Timeline, Metrics, Quote, KeyTakeaway",
    )


def demo_data_driven_story():
    """Data-driven narrative with multiple charts"""
    post = ComposablePost("text")

    post.add_hook("stat", "📈 We 10x'd Our Development Velocity in 12 Months")
    post.add_body("Here's exactly how we did it:")

    post.add_separator("line")

    # Show time savings
    post.add_body("1. Time Saved Per Developer:")
    post.add_bar_chart(
        data={"Code Generation": 15, "Bug Detection": 8, "Code Review": 6, "Documentation": 5},
        title="HOURS SAVED PER WEEK",
        unit="hours",
    )

    post.add_separator("dots")

    # Show adoption progress
    post.add_body("2. Tool Adoption Across Team:")
    post.add_progress_chart(
        data={"GitHub Copilot": 100, "ChatGPT": 95, "Cursor": 80, "Claude Code": 60},
        title="TEAM ADOPTION RATES",
    )

    post.add_separator("dots")

    # Show impact ranking
    post.add_body("3. Biggest Impact Areas:")
    post.add_ranking_chart(
        data={
            "Faster prototyping": "10x improvement",
            "Better code quality": "5x improvement",
            "Faster debugging": "4x improvement",
            "Team morale": "3x improvement",
        },
        title="TOP IMPROVEMENTS",
        show_medals=True,
    )

    post.add_separator("line")

    # Conclusion
    post.add_key_takeaway(
        message="The ROI is undeniable: $40/dev/month for 34 hours saved per week. That's a 170:1 return.",
        title="THE BOTTOM LINE",
    )

    post.add_cta("curiosity", "What's your biggest productivity bottleneck?")
    post.add_hashtags(["Productivity", "AI", "Development", "ROI"])

    return save_preview(post, "Data-Driven Story", "Multiple charts telling a complete story")


# ==============================================================================
# MAIN
# ==============================================================================


def main():
    """Generate all component showcases"""
    print("\n" + "=" * 70)
    print("LINKEDIN POST COMPONENTS - COMPLETE SHOWCASE")
    print("=" * 70)
    print("\nGenerating HTML previews for every component type...")
    print()

    previews = []

    # Post Structure
    previews.append(demo_post_structure())

    print("\n📊 CHART COMPONENTS")
    print("-" * 70 + "\n")
    previews.append(demo_bar_chart())
    previews.append(demo_metrics_chart())
    previews.append(demo_comparison_chart())
    previews.append(demo_progress_chart())
    previews.append(demo_ranking_chart())

    print("\n🎨 FEATURE COMPONENTS")
    print("-" * 70 + "\n")
    previews.append(demo_quote())
    previews.append(demo_big_stat())
    previews.append(demo_timeline())
    previews.append(demo_key_takeaway())
    previews.append(demo_pro_con())

    print("\n🔥 COMBINED EXAMPLES")
    print("-" * 70 + "\n")
    previews.append(demo_combined_comprehensive())
    previews.append(demo_data_driven_story())

    print("\n" + "=" * 70)
    print(f"✅ COMPLETE! Generated {len(previews)} HTML previews")
    print("=" * 70)
    print(f"\nSaved to: {Path.home() / '.linkedin_drafts' / 'previews' / 'showcase'}")
    print("\nOpen any preview in your browser to see LinkedIn-style formatting!")
    print("\nComponent types demonstrated:")
    print("  ✓ Post Structure (Hook, Body, CTA, Hashtags, Separator)")
    print("  ✓ Charts (Bar, Metrics, Comparison, Progress, Ranking)")
    print("  ✓ Features (Quote, BigStat, Timeline, KeyTakeaway, ProCon)")
    print("  ✓ Combined examples with multiple components")
    print("\n" + "=" * 70)

    return previews


if __name__ == "__main__":
    previews = main()
