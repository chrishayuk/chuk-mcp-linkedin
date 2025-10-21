#!/usr/bin/env python3
"""
Try to get member info from LinkedIn's /v2/me endpoint.
"""

import asyncio
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import config
import httpx


async def get_me():
    """Try to get /v2/me"""

    print("Getting LinkedIn Member Info (/v2/me)")
    print("=" * 60)
    print()

    token = config.linkedin_access_token
    print(f"Using token: {token[:20]}...")
    print()

    url = "https://api.linkedin.com/v2/me"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "X-Restli-Protocol-Version": "2.0.0",
                },
                timeout=10.0
            )

            print(f"Status: {response.status_code}")
            print()

            if response.status_code == 200:
                data = response.json()
                print("✓ Success!")
                print()
                print(json.dumps(data, indent=2))
                print()

                # Try to extract member ID
                if 'id' in data:
                    raw_id = data['id']
                    print(f"Raw ID field: {raw_id}")

                    # Check if it's already a URN
                    if raw_id.startswith('urn:li:'):
                        member_urn = raw_id
                        print(f"Member URN: {member_urn}")
                    else:
                        member_urn = f"urn:li:member:{raw_id}"
                        print(f"Member URN: {member_urn}")

                    print()
                    print("Add this to your .env:")
                    print(f"LINKEDIN_PERSON_URN={member_urn}")
                else:
                    print("⚠️  No 'id' field in response")
            else:
                print(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(json.dumps(error_data, indent=2))
                except:
                    print(response.text)

        except Exception as e:
            print(f"❌ Exception: {e}")


if __name__ == "__main__":
    asyncio.run(get_me())
