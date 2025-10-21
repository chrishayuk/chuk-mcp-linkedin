"""
Demo script showing MCP tools for all feature components.

Demonstrates the MCP tool workflow for creating posts with:
- Quote components
- BigStat components
- Timeline components
- KeyTakeaway components
- ProCon components
- Separator components
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.manager import LinkedInManager
from chuk_mcp_linkedin.tools.composition_tools import register_composition_tools


class MockMCP:
    """Mock MCP server for testing tools"""

    def __init__(self):
        self.tools = {}

    def tool(self, func):
        """Decorator to register tools"""
        self.tools[func.__name__] = func
        return func


async def demo_quote_tool(manager, tools):
    """Demo quote MCP tool"""
    print("=" * 70)
    print("DEMO: linkedin_add_quote")
    print("=" * 70)

    # Create draft
    draft = manager.create_draft("Quote Demo", "text")

    # Add components via MCP tools
    await tools["linkedin_add_hook"]("story", "Customer Success Story 💡")
    await tools["linkedin_add_body"]("One year ago, this team was struggling with slow deployments...")
    await tools["linkedin_add_quote"](
        text="AI has reduced our deployment time by 80% and improved code quality dramatically.",
        author="Sarah Chen",
        source="CTO at TechCorp"
    )
    await tools["linkedin_add_body"]("Today, they're shipping 10x faster with fewer bugs.")
    await tools["linkedin_add_cta"]("curiosity", "What's your biggest deployment challenge?")
    await tools["linkedin_add_hashtags"](["CustomerSuccess", "DevOps", "AI"])

    # Compose
    result = await tools["linkedin_compose_post"]()
    print(result)
    print()


async def demo_big_stat_tool(manager, tools):
    """Demo big stat MCP tool"""
    print("=" * 70)
    print("DEMO: linkedin_add_big_stat")
    print("=" * 70)

    # Create draft
    draft = manager.create_draft("Big Stat Demo", "text")

    # Add components
    await tools["linkedin_add_hook"]("stat", "The State of AI in Development")
    await tools["linkedin_add_big_stat"](
        number="2.5M",
        label="developers using AI tools daily",
        context="↑ 340% growth year-over-year"
    )
    await tools["linkedin_add_body"]("This explosive growth is transforming how we build software.")
    await tools["linkedin_add_body"]("The question isn't if you should adopt AI tools...")
    await tools["linkedin_add_body"]("It's how quickly you can leverage them to stay competitive.")
    await tools["linkedin_add_cta"]("action", "Join the AI revolution")
    await tools["linkedin_add_hashtags"](["AI", "Development", "FutureTech"])

    # Compose
    result = await tools["linkedin_compose_post"]()
    print(result)
    print()


async def demo_timeline_tool(manager, tools):
    """Demo timeline MCP tool"""
    print("=" * 70)
    print("DEMO: linkedin_add_timeline")
    print("=" * 70)

    # Create draft
    draft = manager.create_draft("Timeline Demo", "text")

    # Add components
    await tools["linkedin_add_hook"]("story", "🚀 How We Built a $10M ARR SaaS in 2 Years")
    await tools["linkedin_add_timeline"](
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
    await tools["linkedin_add_body"]("Key lesson: Focus on solving real problems, not chasing trends.")
    await tools["linkedin_add_cta"]("curiosity", "What milestone are you working toward?")
    await tools["linkedin_add_hashtags"](["Startup", "SaaS", "Entrepreneurship"])

    # Compose
    result = await tools["linkedin_compose_post"]()
    print(result)
    print()


async def demo_key_takeaway_tool(manager, tools):
    """Demo key takeaway MCP tool"""
    print("=" * 70)
    print("DEMO: linkedin_add_key_takeaway")
    print("=" * 70)

    # Create draft
    draft = manager.create_draft("Key Takeaway Demo", "text")

    # Add components
    await tools["linkedin_add_hook"]("question", "Why do 90% of startups fail?")
    await tools["linkedin_add_body"]("I analyzed 500 failed startups over the past 5 years.")
    await tools["linkedin_add_body"]("The pattern was clear:")
    await tools["linkedin_add_body"]("❌ They built solutions looking for problems\n❌ They optimized for vanity metrics\n❌ They ignored customer feedback")
    await tools["linkedin_add_separator"]("line")
    await tools["linkedin_add_key_takeaway"](
        message="Focus on solving real problems, not chasing trends. Listen to your customers, not your ego.",
        title="KEY TAKEAWAY",
        style="box"
    )
    await tools["linkedin_add_cta"]("soft", "What lessons have you learned?")
    await tools["linkedin_add_hashtags"](["Startups", "Entrepreneurship", "Lessons"])

    # Compose
    result = await tools["linkedin_compose_post"]()
    print(result)
    print()


async def demo_pro_con_tool(manager, tools):
    """Demo pro/con MCP tool"""
    print("=" * 70)
    print("DEMO: linkedin_add_pro_con")
    print("=" * 70)

    # Create draft
    draft = manager.create_draft("Pro-Con Demo", "text")

    # Add components
    await tools["linkedin_add_hook"]("question", "Should your team adopt AI coding tools?")
    await tools["linkedin_add_body"]("After 6 months of testing with our 50-person engineering team:")
    await tools["linkedin_add_pro_con"](
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
    await tools["linkedin_add_separator"]("dots")
    await tools["linkedin_add_body"]("Our verdict: The ROI is clear. We're going all-in.")
    await tools["linkedin_add_cta"]("curiosity", "Have you tried AI coding tools?")
    await tools["linkedin_add_hashtags"](["AI", "Development", "TechLeadership"])

    # Compose
    result = await tools["linkedin_compose_post"]()
    print(result)
    print()


async def demo_combined_features(manager, tools):
    """Demo combining multiple feature components"""
    print("=" * 70)
    print("DEMO: COMBINED FEATURES")
    print("=" * 70)

    # Create draft
    draft = manager.create_draft("Combined Features Demo", "text")

    # Add components
    await tools["linkedin_add_hook"]("stat", "📊 The Complete Guide to AI Development Tools")

    # Big stat
    await tools["linkedin_add_big_stat"](
        number="95%",
        label="of Fortune 500 companies using AI tools",
        context="Up from 23% in 2023"
    )

    # Timeline
    await tools["linkedin_add_timeline"](
        steps={
            "2023": "Early adopters experiment",
            "2024": "Mainstream adoption begins",
            "2025": "AI becomes standard practice"
        },
        title="ADOPTION CURVE",
        style="arrow"
    )

    # Quote
    await tools["linkedin_add_quote"](
        text="AI tools have fundamentally changed how we approach software development.",
        author="Emily Rodriguez",
        source="VP Engineering at Scale AI"
    )

    # Separator
    await tools["linkedin_add_separator"]("line")

    # Key takeaway
    await tools["linkedin_add_key_takeaway"](
        message="The question isn't whether to adopt AI tools, but how quickly you can integrate them effectively.",
        style="box"
    )

    await tools["linkedin_add_cta"]("action", "Start your AI journey today")
    await tools["linkedin_add_hashtags"](["AI", "Development", "FutureTech"])

    # Compose
    result = await tools["linkedin_compose_post"]()
    print(result)
    print()


async def demo_validation_errors(manager, tools):
    """Demo validation errors"""
    print("=" * 70)
    print("DEMO: VALIDATION ERRORS")
    print("=" * 70)

    # Create draft
    draft = manager.create_draft("Validation Test", "text")

    # Test 1: Empty quote text
    print("Test 1: Empty quote text")
    result = await tools["linkedin_add_quote"](text="", author="John Doe")
    print(f"Result: {result}")
    print()

    # Test 2: Quote text too long
    print("Test 2: Quote text too long (>500 chars)")
    long_text = "x" * 501
    result = await tools["linkedin_add_quote"](text=long_text, author="John Doe")
    print(f"Result: {result}")
    print()

    # Test 3: Timeline with < 2 steps
    print("Test 3: Timeline with < 2 steps")
    result = await tools["linkedin_add_timeline"](steps={"2023": "Only one step"})
    print(f"Result: {result}")
    print()

    # Test 4: Invalid timeline style
    print("Test 4: Invalid timeline style")
    result = await tools["linkedin_add_timeline"](
        steps={"2023": "Step 1", "2024": "Step 2"},
        style="invalid_style"
    )
    print(f"Result: {result}")
    print()

    # Test 5: Empty pros/cons
    print("Test 5: Empty pros list")
    result = await tools["linkedin_add_pro_con"](pros=[], cons=["Con 1"])
    print(f"Result: {result}")
    print()


async def main():
    """Run all demos"""
    print("\n")
    print("=" * 70)
    print("MCP FEATURE TOOLS DEMONSTRATION")
    print("=" * 70)
    print()

    # Create manager and register tools
    manager = LinkedInManager()
    mcp = MockMCP()
    tools = register_composition_tools(mcp, manager)

    # Run demos
    await demo_quote_tool(manager, tools)
    await demo_big_stat_tool(manager, tools)
    await demo_timeline_tool(manager, tools)
    await demo_key_takeaway_tool(manager, tools)
    await demo_pro_con_tool(manager, tools)
    await demo_combined_features(manager, tools)
    await demo_validation_errors(manager, tools)

    print("=" * 70)
    print("ALL DEMOS COMPLETED")
    print("=" * 70)
    print()
    print(f"✅ Tested 6 new MCP tools:")
    print("   • linkedin_add_quote")
    print("   • linkedin_add_big_stat")
    print("   • linkedin_add_timeline")
    print("   • linkedin_add_key_takeaway")
    print("   • linkedin_add_pro_con")
    print("   • linkedin_add_separator")
    print()


if __name__ == "__main__":
    asyncio.run(main())
