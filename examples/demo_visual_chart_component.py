#!/usr/bin/env python3
"""
Demo: VisualChart Component

Demonstrates the new VisualChart component in the design system.
Shows all 5 chart types with design token integration.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.composition import ComposablePost


async def demo_visual_charts():
    """Demonstrate all visual chart types"""

    print("=" * 70)
    print("VISUAL CHART COMPONENT DEMO")
    print("=" * 70)
    print()

    # Chart 1: Bar Chart
    print("1️⃣  BAR CHART")
    print("-" * 70)
    post1 = ComposablePost("text")
    post1.add_hook("stat", "📊 Developer Time Allocation")
    post1.add_visual_chart(
        chart_type="bar",
        data={
            "AI-Assisted Coding": 12,
            "Code Review": 6,
            "Documentation": 4,
            "Debugging": 8
        },
        title="Hours Saved Per Week"
    )
    print(post1.compose())
    print()
    print()

    # Chart 2: Metrics
    print("2️⃣  METRICS CHART")
    print("-" * 70)
    post2 = ComposablePost("text")
    post2.add_hook("stat", "📈 AI Impact on Development")
    post2.add_visual_chart(
        chart_type="metrics",
        data={
            "Faster problem-solving": "67%",
            "Fewer bugs": "54%",
            "Better learning": "89%",
            "Using for architecture": "23%"
        },
        title="Key Findings"
    )
    print(post2.compose())
    print()
    print()

    # Chart 3: Comparison
    print("3️⃣  COMPARISON CHART")
    print("-" * 70)
    post3 = ComposablePost("text")
    post3.add_hook("question", "Traditional vs AI-Assisted Development")
    post3.add_visual_chart(
        chart_type="comparison",
        data={
            "Traditional Coding": [
                "Manual boilerplate writing",
                "Stack Overflow searches",
                "Slower iteration cycles"
            ],
            "AI-Assisted Coding": [
                "Auto-generated boilerplate",
                "Instant code suggestions",
                "Rapid prototyping"
            ]
        },
        title="The Shift"
    )
    print(post3.compose())
    print()
    print()

    # Chart 4: Progress
    print("4️⃣  PROGRESS CHART")
    print("-" * 70)
    post4 = ComposablePost("text")
    post4.add_hook("stat", "📊 Project Status Update")
    post4.add_visual_chart(
        chart_type="progress",
        data={
            "Frontend Development": 85,
            "Backend API": 70,
            "Testing Coverage": 60,
            "Documentation": 40
        },
        title="Sprint Progress"
    )
    print(post4.compose())
    print()
    print()

    # Chart 5: Ranking
    print("5️⃣  RANKING CHART")
    print("-" * 70)
    post5 = ComposablePost("text")
    post5.add_hook("stat", "🏆 Most Popular AI Coding Tools 2025")
    post5.add_visual_chart(
        chart_type="ranking",
        data={
            "GitHub Copilot": "10M users",
            "Claude Code": "5M users",
            "Cursor": "3M users",
            "Tabnine": "2M users",
            "Amazon CodeWhisperer": "1.5M users"
        },
        title="Global Rankings"
    )
    post5.add_cta("question", "Which one are you using?")
    post5.add_hashtags(["AI", "CodingTools", "DeveloperProductivity"])
    print(post5.compose())
    print()
    print()

    # Design Tokens Summary
    print("=" * 70)
    print("DESIGN TOKENS USED")
    print("=" * 70)
    print()
    print("✅ TextTokens.CHART_EMOJIS - Chart type indicators")
    print("✅ TextTokens.BAR_COLORS - Colored emoji squares")
    print("✅ TextTokens.INDICATORS - Checkmarks, medals, etc.")
    print("✅ TextTokens.PROGRESS_BARS - Filled/empty characters")
    print("✅ TextTokens.SYMBOLS - Arrows, bullets")
    print()
    print("All components respect the token management system!")
    print()
    print("=" * 70)
    print("MCP TOOL AVAILABLE")
    print("=" * 70)
    print()
    print("Use via MCP:")
    print('  linkedin_add_visual_chart(')
    print('    chart_type="bar",')
    print('    data={"Item A": 10, "Item B": 6},')
    print('    title="My Chart"')
    print('  )')
    print()


if __name__ == "__main__":
    asyncio.run(demo_visual_charts())
