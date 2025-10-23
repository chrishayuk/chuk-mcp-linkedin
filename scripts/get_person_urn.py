#!/usr/bin/env python3
"""
Get LinkedIn Person URN from access token.

Usage:
    python scripts/get_person_urn.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import config
import httpx


async def get_person_urn():
    """Get the authenticated user's person URN"""

    print("Getting LinkedIn Person URN")
    print("=" * 60)
    print()

    if not config.linkedin_access_token or config.linkedin_access_token == "your_access_token_here":
        print("❌ Error: LINKEDIN_ACCESS_TOKEN not set in .env")
        return

    print(f"Access Token: {config.linkedin_access_token[:20]}...")
    print()

    # Try multiple endpoints to get the person URN
    endpoints_to_try = [
        ("https://api.linkedin.com/v2/userinfo", "OpenID Connect userinfo"),
        ("https://api.linkedin.com/v2/me", "LinkedIn v2 me endpoint"),
    ]

    for url, name in endpoints_to_try:
        print(f"Trying {name}...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={"Authorization": f"Bearer {config.linkedin_access_token}"},
                    timeout=10.0,
                )

                print(f"  Status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    print(f"  Response: {data}")
                    print()

                    # Try to extract person URN
                    person_urn = None

                    # OpenID Connect format
                    if "sub" in data:
                        person_urn = f"urn:li:person:{data['sub']}"
                    # Direct ID format
                    elif "id" in data:
                        # Remove urn prefix if present
                        person_id = data["id"]
                        if person_id.startswith("urn:li:person:"):
                            person_urn = person_id
                        else:
                            person_urn = f"urn:li:person:{person_id}"

                    if person_urn:
                        print("✓ Found Person URN!")
                        print(f"  {person_urn}")
                        print()

                        # Update .env
                        update_env(person_urn)
                        return person_urn
                else:
                    print(f"  Error: {response.text}")
                    print()

        except Exception as e:
            print(f"  Error: {e}")
            print()

    print("❌ Could not automatically get Person URN")
    print()
    print("Alternative methods:")
    print("1. Use LinkedIn API Explorer: https://www.linkedin.com/developers/")
    print("2. Check the response from: GET https://api.linkedin.com/v2/me")
    print("3. Look for 'id' or 'sub' field in the response")
    print()
    print("Once you have it, add to .env:")
    print("LINKEDIN_PERSON_URN=urn:li:person:YOUR_NUMERIC_ID")


def update_env(person_urn):
    """Update .env file with person URN"""
    env_path = Path(__file__).parent.parent / ".env"

    try:
        # Read existing .env
        with open(env_path, "r") as f:
            lines = f.readlines()

        # Update person URN line
        new_lines = []
        updated = False

        for line in lines:
            if line.startswith("LINKEDIN_PERSON_URN="):
                new_lines.append(f"LINKEDIN_PERSON_URN={person_urn}\n")
                updated = True
            else:
                new_lines.append(line)

        # Add if not found
        if not updated:
            new_lines.append(f"LINKEDIN_PERSON_URN={person_urn}\n")

        # Write back
        with open(env_path, "w") as f:
            f.writelines(new_lines)

        print("✓ Updated .env with Person URN")
        print()
        print("Next steps:")
        print("  1. Test connection: python scripts/test_connection.py")
        print("  2. Create draft post: python examples/test_api_publish.py")

    except Exception as e:
        print(f"Error updating .env: {e}")


if __name__ == "__main__":
    asyncio.run(get_person_urn())
