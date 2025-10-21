"""
Demo script showing HTML previews of all 7 new feature components.

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


def demo_checklist():
    """Demo checklist component"""
    post = ComposablePost("text")
    post.add_hook("list", "🚀 Pre-Launch Checklist for SaaS Products")
    post.add_body("Before you launch your product, make sure you've covered these essentials:")
    post.add_checklist(
        items=[
            {"text": "Set up analytics and tracking", "checked": True},
            {"text": "Create onboarding flow", "checked": True},
            {"text": "Write documentation", "checked": True},
            {"text": "Set up customer support", "checked": False},
            {"text": "Prepare marketing materials", "checked": False},
            {"text": "Test payment processing", "checked": False}
        ],
        title="LAUNCH CHECKLIST",
        show_progress=True
    )
    post.add_body("Don't skip the fundamentals. They'll save you time later.")
    post.add_cta("curiosity", "What's on your pre-launch checklist?")
    post.add_hashtags(["SaaS", "ProductLaunch", "Startup"])

    return generate_preview(
        post,
        "Checklist Demo",
        "Action items with progress tracking"
    )


def demo_before_after():
    """Demo before/after component"""
    post = ComposablePost("text")
    post.add_hook("story", "How AI Transformed Our Development Workflow")
    post.add_body("6 months ago, we adopted AI coding tools across our 50-person engineering team.")
    post.add_body("Here's what changed:")
    post.add_before_after(
        before=[
            "Manual code reviews taking 2-3 days",
            "Repetitive boilerplate writing",
            "Documentation always out of date",
            "Junior devs spending weeks on setup"
        ],
        after=[
            "AI-assisted reviews in <1 day",
            "Boilerplate generated instantly",
            "Docs auto-generated from code",
            "Juniors productive from day one"
        ],
        title="THE TRANSFORMATION"
    )
    post.add_separator("line")
    post.add_body("The ROI was clear within the first month. We're never going back.")
    post.add_cta("curiosity", "Have you made a similar transformation?")
    post.add_hashtags(["AI", "Development", "Productivity"])

    return generate_preview(
        post,
        "Before After Demo",
        "Transformation comparison"
    )


def demo_tip_box():
    """Demo tip box component"""
    post = ComposablePost("text")
    post.add_hook("question", "Why do most developers struggle with code reviews?")
    post.add_body("After analyzing 1,000+ code reviews, I found 3 common patterns:")
    post.add_body("1. Reviewing too much code at once\n2. Focusing on style over substance\n3. Not providing actionable feedback")
    post.add_separator("dots")
    post.add_tip_box(
        message="Keep PRs under 400 lines. Smaller changes = better reviews = faster shipping.",
        title="Pro Tip",
        style="tip"
    )
    post.add_body("This one change improved our review quality by 67%.")
    post.add_cta("soft", "What's your code review tip?")
    post.add_hashtags(["CodeReview", "Development", "BestPractices"])

    return generate_preview(
        post,
        "Tip Box Demo",
        "Highlighted pro tip"
    )


def demo_stats_grid():
    """Demo stats grid component"""
    post = ComposablePost("text")
    post.add_hook("stat", "📊 Our Q1 2025 Developer Productivity Report")
    post.add_body("We surveyed 500 development teams about their AI tool adoption.")
    post.add_body("The results are remarkable:")
    post.add_stats_grid(
        stats={
            "Adoption Rate": "89%",
            "Time Saved": "12hrs/week",
            "Bug Reduction": "-34%",
            "Code Quality": "+56%",
            "Team Satisfaction": "9.2/10",
            "ROI": "340%"
        },
        title="KEY METRICS",
        columns=2
    )
    post.add_separator("line")
    post.add_body("The data is clear: AI tools are no longer optional for competitive teams.")
    post.add_cta("action", "Download the full report")
    post.add_hashtags(["AI", "Productivity", "DevTools"])

    return generate_preview(
        post,
        "Stats Grid Demo",
        "Multi-metric grid display"
    )


def demo_poll_preview():
    """Demo poll preview component"""
    post = ComposablePost("text")
    post.add_hook("curiosity", "I'm curious about your testing strategy...")
    post.add_body("We're debating whether to invest more in:")
    post.add_body("• Unit tests (fast, isolated)\n• Integration tests (realistic scenarios)\n• E2E tests (user flows)\n• Manual QA (human judgment)")
    post.add_separator("wave")
    post.add_poll_preview(
        question="Which testing approach gives you the most confidence?",
        options=[
            "Unit tests",
            "Integration tests",
            "E2E tests",
            "Manual QA"
        ]
    )
    post.add_body("Curious to see where the community stands on this!")
    post.add_hashtags(["Testing", "QA", "Development"])

    return generate_preview(
        post,
        "Poll Preview Demo",
        "Interactive poll for engagement"
    )


def demo_feature_list():
    """Demo feature list component"""
    post = ComposablePost("text")
    post.add_hook("story", "We just launched our AI Code Assistant v2.0")
    post.add_body("After 6 months of development and 1,000+ beta testers, here's what's new:")
    post.add_feature_list(
        features=[
            {
                "icon": "⚡",
                "title": "10x Faster Completions",
                "description": "New model architecture reduces latency to <100ms"
            },
            {
                "icon": "🎯",
                "title": "Context-Aware Suggestions",
                "description": "Understands your entire codebase, not just the current file"
            },
            {
                "icon": "🔒",
                "title": "Enterprise Security",
                "description": "SOC 2 compliant with on-premise deployment options"
            },
            {
                "icon": "🌍",
                "title": "50+ Languages",
                "description": "From Python to Rust, we've got you covered"
            }
        ],
        title="NEW FEATURES"
    )
    post.add_separator("line")
    post.add_body("Available now for all Pro and Enterprise users.")
    post.add_cta("action", "Try it free for 14 days")
    post.add_hashtags(["AI", "CodeAssistant", "ProductLaunch"])

    return generate_preview(
        post,
        "Feature List Demo",
        "Product features with icons"
    )


def demo_numbered_list():
    """Demo numbered list component"""
    post = ComposablePost("text")
    post.add_hook("list", "5 Lessons from Scaling to 100 Engineers")
    post.add_body("We grew from 10 to 100 engineers in 18 months.")
    post.add_body("Here's what I learned:")
    post.add_numbered_list(
        items=[
            "Hire for cultural fit first, skills second. Skills can be taught.",
            "Document everything. Your future self will thank you.",
            "Invest in developer experience. Happy devs = better products.",
            "Automate the boring stuff. Let humans do what humans do best.",
            "Create clear career paths. People want growth, not just paychecks."
        ],
        title="KEY LESSONS",
        style="emoji_numbers"
    )
    post.add_separator("dots")
    post.add_body("The hardest lesson? Learning to let go and trust your team.")
    post.add_cta("curiosity", "What lessons have you learned from scaling?")
    post.add_hashtags(["Engineering", "Leadership", "Scaling"])

    return generate_preview(
        post,
        "Numbered List Demo",
        "Sequential lessons with emoji numbers"
    )


def demo_combined_new_features():
    """Demo combining multiple new features"""
    post = ComposablePost("text")
    post.add_hook("stat", "📋 The Ultimate Developer Onboarding Guide")

    # Numbered list of phases
    post.add_numbered_list(
        items=[
            "Week 1: Environment Setup",
            "Week 2: First Code Contribution",
            "Week 3: Code Review Participation",
            "Week 4: Own Your First Feature"
        ],
        title="ONBOARDING PHASES",
        style="bold_numbers"
    )

    # Before/After transformation
    post.add_separator("line")
    post.add_body("We used to struggle with slow onboarding. Then we made changes:")
    post.add_before_after(
        before=["2-3 week ramp-up time", "Overwhelming documentation", "Junior devs felt lost"],
        after=["Productive in 3 days", "Interactive tutorials", "Paired programming from day 1"],
        labels={"before": "OLD APPROACH", "after": "NEW APPROACH"}
    )

    # Feature list
    post.add_feature_list(
        features=[
            {"icon": "🎓", "title": "Interactive Tutorials", "description": "Learn by doing, not reading"},
            {"icon": "👥", "title": "Buddy System", "description": "Every new hire gets a dedicated mentor"},
            {"icon": "📊", "title": "Progress Tracking", "description": "Clear milestones and feedback"}
        ],
        title="KEY COMPONENTS"
    )

    # Tip box
    post.add_tip_box(
        message="The best onboarding investment? Automating your dev environment setup. Save 90% of day-one frustration.",
        style="success"
    )

    # Checklist
    post.add_checklist(
        items=[
            {"text": "Automate environment setup", "checked": True},
            {"text": "Create buddy system", "checked": True},
            {"text": "Build interactive tutorials", "checked": False},
            {"text": "Set up progress tracking", "checked": False}
        ],
        title="YOUR ACTION PLAN"
    )

    post.add_cta("action", "Download our full onboarding playbook")
    post.add_hashtags(["Onboarding", "DevEx", "Engineering"])

    return generate_preview(
        post,
        "Combined New Features",
        "Multiple new components in one post"
    )


def main():
    """Run all demos and open previews"""
    print("=" * 70)
    print("GENERATING NEW FEATURE PREVIEWS")
    print("=" * 70)
    print()

    previews = []

    # Generate all previews
    print("🎨 NEW FEATURE COMPONENTS")
    print("-" * 70)
    previews.append(demo_checklist())
    previews.append(demo_before_after())
    previews.append(demo_tip_box())
    previews.append(demo_stats_grid())
    previews.append(demo_poll_preview())
    previews.append(demo_feature_list())
    previews.append(demo_numbered_list())

    print("\n🔥 COMBINED DEMO")
    print("-" * 70)
    previews.append(demo_combined_new_features())

    print("=" * 70)
    print(f"✅ Generated {len(previews)} preview(s)")
    print("=" * 70)
    print()

    # Ask user which to open
    print("Which preview would you like to open?")
    print("1. Checklist")
    print("2. Before/After")
    print("3. Tip Box")
    print("4. Stats Grid")
    print("5. Poll Preview")
    print("6. Feature List")
    print("7. Numbered List")
    print("8. Combined Features")
    print("A. Open ALL")
    print()

    choice = input("Enter choice (1-8 or A): ").strip().upper()

    if choice == "A":
        print("\nOpening all previews in browser...")
        for i, preview_path in enumerate(previews, 1):
            webbrowser.open(f"file://{preview_path}")
            if i < len(previews):
                time.sleep(0.5)  # Small delay between opens
    elif choice.isdigit() and 1 <= int(choice) <= 8:
        idx = int(choice) - 1
        print(f"\nOpening preview in browser...")
        webbrowser.open(f"file://{previews[idx]}")
    else:
        print("Invalid choice. Opening first preview...")
        webbrowser.open(f"file://{previews[0]}")

    print("\n✅ Done! Check your browser.")


if __name__ == "__main__":
    main()
