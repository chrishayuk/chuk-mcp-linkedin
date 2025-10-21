#!/usr/bin/env python3
"""
Test LinkedIn API connection.

Usage:
    python scripts/test_connection.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import LinkedInClient, config


async def test_connection():
    """Test the LinkedIn API connection"""

    print("LinkedIn API Connection Test")
    print("=" * 60)
    print()

    # Check configuration
    print("1. Checking configuration...")
    if config.is_configured():
        print("   ✓ Configuration complete")
        print(f"   Person URN: {config.linkedin_person_urn}")
        print(f"   Access Token: {config.linkedin_access_token[:20]}...")
        print(f"   Publishing enabled: {config.enable_publishing}")
    else:
        missing = config.get_missing_config()
        print(f"   ✗ Missing: {', '.join(missing)}")
        print()
        print("Please run: python scripts/get_linkedin_token.py")
        return

    print()

    # Test connection
    print("2. Testing API connection...")
    client = LinkedInClient()

    is_valid = await client.test_connection()

    if is_valid:
        print("   ✓ Connection successful!")
        print()
        print("Your LinkedIn API is ready to use!")
        print()
        print("Next steps:")
        print("  1. Create a test post: python examples/test_api_publish.py")
        print("  2. Enable publishing: Set ENABLE_PUBLISHING=true in .env")
        print("  3. Publish for real: python examples/test_api_publish.py --publish")
    else:
        print("   ✗ Connection failed")
        print()
        print("Possible issues:")
        print("  - Access token may have expired")
        print("  - Incorrect person URN")
        print("  - App doesn't have w_member_social permission")
        print()
        print("Try running: python scripts/get_linkedin_token.py")


if __name__ == "__main__":
    asyncio.run(test_connection())
