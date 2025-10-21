"""
Demo script showing HTML previews of all chart and feature components.

Opens each post preview in the browser for visual inspection.
"""

import sys
import time
import webbrowser
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.posts import ComposablePost
from chuk_mcp_linkedin.preview import LinkedInPreview


def generate_preview(post: ComposablePost, name: str, description: str) -> str:
    """Generate and save HTML preview"""
    # Compose the post
    text = post.compose()

    # Count hashtags
    hashtag_count = sum(1 for comp in post.components if comp.__class__.__name__ == "Hashtags")
    has_hook = any(comp.__class__.__name__ == "Hook" for comp in post.components)
    has_cta = any(comp.__class__.__name__ == "CallToAction" for comp in post.components)

    # Create draft data for preview
    draft_data = {
        "name": name,
        "post_type": "text",
        "theme": None,
        "content": {
            "composed_text": text
        }
    }

    # Create stats
    stats = {
        "char_count": len(text),
        "word_count": len(text.split()),
        "char_remaining": 3000 - len(text),
        "hashtag_count": hashtag_count,
        "has_hook": has_hook,
        "has_cta": has_cta,
    }

    # Generate HTML
    html_content = LinkedInPreview.generate_html(draft_data, stats)

    # Save to file
    output_dir = Path(__file__).parent.parent / ".linkedin_drafts" / "previews"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time())
    filename = f"demo_{name.lower().replace(' ', '_')}_{timestamp}.html"
    output_path = output_dir / filename

    saved_path = LinkedInPreview.save_preview(html_content, str(output_path))

    print(f"✅ {name}: {saved_path}")
    print(f"   {description}")
    print(f"   Length: {len(text)} chars, Components: {len(post.components)}")
    print()

    return saved_path


def demo_bar_chart():
    """Demo bar chart component"""
    post = ComposablePost("text")
    post.add_hook("stat", "📊 Developer Productivity in 2025")
    post.add_body("We surveyed 500 developers about AI coding tools.")
    post.add_bar_chart(
        data={"AI-Assisted": 12, "Code Review": 6, "Documentation": 4, "Debugging": 8},
        title="TIME SAVED PER WEEK",
        unit="hours"
    )
    post.add_cta("curiosity", "How much time do you save?")
    post.add_hashtags(["DeveloperProductivity", "AI", "TechTrends"])

    return generate_preview(
        post,
        "Bar Chart Demo",
        "Horizontal bar chart with colored emoji squares"
    )


def demo_metrics_chart():
    """Demo metrics chart component"""
    post = ComposablePost("text")
    post.add_hook("stat", "📈 AI Impact on Development Teams")
    post.add_body("Our latest research reveals significant improvements:")
    post.add_metrics_chart(
        data={
            "Faster problem-solving": "67%",
            "Fewer bugs in production": "54%",
            "Better learning & upskilling": "89%"
        },
        title="KEY FINDINGS"
    )
    post.add_cta("curiosity", "What impact are you seeing?")
    post.add_hashtags(["AI", "Development", "Productivity"])

    return generate_preview(
        post,
        "Metrics Chart Demo",
        "KPI metrics with ✅/❌ indicators"
    )


def demo_progress_chart():
    """Demo progress chart component"""
    post = ComposablePost("text")
    post.add_hook("story", "🚀 Our AI Platform Launch Update")
    post.add_body("Here's where we stand 2 weeks before launch:")
    post.add_progress_chart(
        data={
            "Backend API": 85,
            "Frontend UI": 70,
            "Testing": 45,
            "Documentation": 30
        },
        title="PROJECT STATUS"
    )
    post.add_cta("curiosity", "Which area should we focus on next?")
    post.add_hashtags(["Startup", "ProductDevelopment", "AI"])

    return generate_preview(
        post,
        "Progress Chart Demo",
        "Progress bars showing 0-100% completion"
    )


def demo_ranking_chart():
    """Demo ranking chart component"""
    post = ComposablePost("text")
    post.add_hook("list", "🏆 Most Popular Programming Languages in 2025")
    post.add_body("Based on our annual developer survey:")
    post.add_ranking_chart(
        data={
            "Python": "1.2M developers",
            "JavaScript": "1.1M developers",
            "TypeScript": "850K developers",
            "Go": "420K developers",
            "Rust": "380K developers"
        },
        title="TOP 5 LANGUAGES",
        show_medals=True
    )
    post.add_cta("curiosity", "What language are you focusing on?")
    post.add_hashtags(["Programming", "TechTrends", "Developers"])

    return generate_preview(
        post,
        "Ranking Chart Demo",
        "Ranked list with medals for top 3"
    )


def demo_quote():
    """Demo quote component"""
    post = ComposablePost("text")
    post.add_hook("story", "Customer Success Story 💡")
    post.add_body("One year ago, this team was struggling with slow deployments...")
    post.add_quote(
        text="AI has reduced our deployment time by 80% and improved code quality dramatically.",
        author="Sarah Chen",
        source="CTO at TechCorp"
    )
    post.add_body("Today, they're shipping 10x faster with fewer bugs.")
    post.add_cta("curiosity", "What's your biggest deployment challenge?")
    post.add_hashtags(["CustomerSuccess", "DevOps", "AI"])

    return generate_preview(
        post,
        "Quote Demo",
        "Quote/testimonial with attribution"
    )


def demo_big_stat():
    """Demo big stat component"""
    post = ComposablePost("text")
    post.add_hook("stat", "The State of AI in Development")
    post.add_big_stat(
        number="2.5M",
        label="developers using AI tools daily",
        context="↑ 340% growth year-over-year"
    )
    post.add_body("This explosive growth is transforming how we build software.")
    post.add_body("The question isn't if you should adopt AI tools...")
    post.add_body("It's how quickly you can leverage them to stay competitive.")
    post.add_cta("action", "Join the AI revolution")
    post.add_hashtags(["AI", "Development", "FutureTech"])

    return generate_preview(
        post,
        "Big Stat Demo",
        "Eye-catching statistic display"
    )


def demo_timeline():
    """Demo timeline component"""
    post = ComposablePost("text")
    post.add_hook("story", "🚀 How We Built a $10M ARR SaaS in 2 Years")
    post.add_timeline(
        steps={
            "Jan 2023": "Launched MVP with 10 beta users",
            "Jun 2023": "Reached 1,000 paying customers",
            "Dec 2023": "Hit $1M ARR milestone",
            "Jun 2024": "Raised Series A ($5M)",
            "Dec 2024": "Crossed $10M ARR"
        },
        title="OUR JOURNEY",
        style="arrow"
    )
    post.add_body("Key lesson: Focus on solving real problems, not chasing trends.")
    post.add_cta("curiosity", "What milestone are you working toward?")
    post.add_hashtags(["Startup", "SaaS", "Entrepreneurship"])

    return generate_preview(
        post,
        "Timeline Demo",
        "Timeline with arrow-separated steps"
    )


def demo_key_takeaway():
    """Demo key takeaway component"""
    post = ComposablePost("text")
    post.add_hook("question", "Why do 90% of startups fail?")
    post.add_body("I analyzed 500 failed startups over the past 5 years.")
    post.add_body("The pattern was clear:")
    post.add_body("❌ They built solutions looking for problems\n❌ They optimized for vanity metrics\n❌ They ignored customer feedback")
    post.add_separator("line")
    post.add_key_takeaway(
        message="Focus on solving real problems, not chasing trends. Listen to your customers, not your ego.",
        title="KEY TAKEAWAY",
        style="box"
    )
    post.add_cta("soft", "What lessons have you learned?")
    post.add_hashtags(["Startups", "Entrepreneurship", "Lessons"])

    return generate_preview(
        post,
        "Key Takeaway Demo",
        "Highlighted insight/TLDR box"
    )


def demo_pro_con():
    """Demo pro/con component"""
    post = ComposablePost("text")
    post.add_hook("question", "Should your team adopt AI coding tools?")
    post.add_body("After 6 months of testing with our 50-person engineering team:")
    post.add_pro_con(
        pros=[
            "40% faster development cycle",
            "Fewer production bugs",
            "Better code documentation",
            "Improved developer satisfaction"
        ],
        cons=[
            "Initial learning curve (2-3 weeks)",
            "Cost: $20-40 per developer/month",
            "Requires code review process updates"
        ],
        title="AI CODING TOOLS"
    )
    post.add_separator("dots")
    post.add_body("Our verdict: The ROI is clear. We're going all-in.")
    post.add_cta("curiosity", "Have you tried AI coding tools?")
    post.add_hashtags(["AI", "Development", "TechLeadership"])

    return generate_preview(
        post,
        "Pro-Con Demo",
        "Pros & cons comparison for decisions"
    )


def demo_combined_features():
    """Demo combining multiple feature components"""
    post = ComposablePost("text")
    post.add_hook("stat", "📊 The Complete Guide to AI Development Tools")

    # Big stat
    post.add_big_stat(
        number="95%",
        label="of Fortune 500 companies using AI tools",
        context="Up from 23% in 2023"
    )

    # Timeline
    post.add_timeline(
        steps={
            "2023": "Early adopters experiment",
            "2024": "Mainstream adoption begins",
            "2025": "AI becomes standard practice"
        },
        title="ADOPTION CURVE",
        style="arrow"
    )

    # Quote
    post.add_quote(
        text="AI tools have fundamentally changed how we approach software development.",
        author="Emily Rodriguez",
        source="VP Engineering at Scale AI"
    )

    # Key takeaway
    post.add_key_takeaway(
        message="The question isn't whether to adopt AI tools, but how quickly you can integrate them effectively.",
        style="box"
    )

    post.add_cta("action", "Start your AI journey today")
    post.add_hashtags(["AI", "Development", "FutureTech"])

    return generate_preview(
        post,
        "Combined Features Demo",
        "Multiple feature components in one post"
    )


def main():
    """Run all demos and open previews"""
    print("=" * 70)
    print("GENERATING LINKEDIN POST PREVIEWS")
    print("=" * 70)
    print()

    previews = []

    # Generate all previews
    print("📊 DATA VISUALIZATION COMPONENTS")
    print("-" * 70)
    previews.append(demo_bar_chart())
    previews.append(demo_metrics_chart())
    previews.append(demo_progress_chart())
    previews.append(demo_ranking_chart())

    print("\n🎨 FEATURE COMPONENTS")
    print("-" * 70)
    previews.append(demo_quote())
    previews.append(demo_big_stat())
    previews.append(demo_timeline())
    previews.append(demo_key_takeaway())
    previews.append(demo_pro_con())

    print("\n🔥 COMBINED DEMO")
    print("-" * 70)
    previews.append(demo_combined_features())

    print("=" * 70)
    print(f"✅ Generated {len(previews)} preview(s)")
    print("=" * 70)
    print()

    # Ask user which to open
    print("Which preview would you like to open?")
    print("1. Bar Chart")
    print("2. Metrics Chart")
    print("3. Progress Chart")
    print("4. Ranking Chart")
    print("5. Quote")
    print("6. Big Stat")
    print("7. Timeline")
    print("8. Key Takeaway")
    print("9. Pro/Con")
    print("10. Combined Features")
    print("A. Open ALL")
    print()

    choice = input("Enter choice (1-10 or A): ").strip().upper()

    if choice == "A":
        print("\nOpening all previews in browser...")
        for i, preview_path in enumerate(previews, 1):
            webbrowser.open(f"file://{preview_path}")
            if i < len(previews):
                time.sleep(0.5)  # Small delay between opens
    elif choice.isdigit() and 1 <= int(choice) <= 10:
        idx = int(choice) - 1
        print(f"\nOpening preview in browser...")
        webbrowser.open(f"file://{previews[idx]}")
    else:
        print("Invalid choice. Opening first preview...")
        webbrowser.open(f"file://{previews[0]}")

    print("\n✅ Done! Check your browser.")


if __name__ == "__main__":
    main()
