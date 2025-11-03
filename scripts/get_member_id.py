#!/usr/bin/env python3
"""
Try to get LinkedIn member ID using various methods.
"""

import asyncio
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import httpx

from chuk_mcp_linkedin.api import config


async def get_member_id():
    """Try to get member ID"""

    print("Getting LinkedIn Member ID")
    print("=" * 60)
    print()

    token = config.linkedin_access_token

    # Try to decode the token (it might contain the member ID)
    print("1. Checking if token contains member ID...")
    try:
        # Tokens are sometimes JWTs which can be decoded
        parts = token.split(".")
        if len(parts) == 3:
            # Might be a JWT
            payload = parts[1]
            # Add padding if needed
            payload += "=" * (4 - len(payload) % 4)
            decoded = base64.urlsafe_b64decode(payload)
            data = json.loads(decoded)
            print(f"   Token payload: {data}")
            if "sub" in data:
                member_id = data["sub"]
                print(f"   ✓ Found member ID in token: {member_id}")
                urn = f"urn:li:member:{member_id}"
                update_env(urn)
                return
    except Exception as e:
        print(f"   Not a decodable JWT: {e}")

    print()

    # Try LinkedIn's profile endpoint with different versions
    endpoints = [
        "https://api.linkedin.com/v2/me",
        "https://api.linkedin.com/v2/people/~",
        "https://api.linkedin.com/v1/people/~",
    ]

    for url in endpoints:
        print(f"2. Trying: {url}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "X-Restli-Protocol-Version": "2.0.0",
                    },
                    timeout=10.0,
                )

                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")

                    # Try to extract ID
                    if "id" in data:
                        member_id = data["id"]
                        if member_id.startswith("urn:li:member:"):
                            urn = member_id
                        else:
                            urn = f"urn:li:member:{member_id}"
                        print(f"   ✓ Found member URN: {urn}")
                        update_env(urn)
                        return
                else:
                    print(f"   Error: {response.text}")
            except Exception as e:
                print(f"   Error: {e}")
        print()

    print("❌ Could not get member ID automatically")
    print()
    print("Manual option:")
    print("You may need to manually inspect your LinkedIn app settings or use")
    print("the LinkedIn API test console to get your member ID.")


def update_env(urn):
    """Update .env with member URN"""
    env_path = Path(__file__).parent.parent / ".env"

    try:
        with open(env_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        updated = False

        for line in lines:
            if line.startswith("LINKEDIN_PERSON_URN="):
                new_lines.append(f"LINKEDIN_PERSON_URN={urn}\n")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_lines.append(f"LINKEDIN_PERSON_URN={urn}\n")

        with open(env_path, "w") as f:
            f.writelines(new_lines)

        print()
        print(f"✓ Updated .env with: {urn}")
        print()
        print("Next steps:")
        print("  1. Test: python scripts/test_connection.py")
        print("  2. Draft post: python examples/test_api_publish.py")

    except Exception as e:
        print(f"Error updating .env: {e}")


if __name__ == "__main__":
    asyncio.run(get_member_id())
