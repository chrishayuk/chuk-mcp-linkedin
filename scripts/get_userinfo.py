#!/usr/bin/env python3
"""
Try to get user info from LinkedIn's userinfo endpoint.
This requires openid scope.
"""

import asyncio
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import config
import httpx


async def get_userinfo():
    """Try to get userinfo"""

    print("Getting LinkedIn User Info (OpenID)")
    print("=" * 60)
    print()

    token = config.linkedin_access_token
    print(f"Using token: {token[:20]}...")
    print()

    url = "https://api.linkedin.com/v2/userinfo"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
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

                if 'sub' in data:
                    member_id = data['sub']
                    member_urn = f"urn:li:member:{member_id}"
                    print(f"Member ID: {member_id}")
                    print(f"Member URN: {member_urn}")
                    print()
                    print("Add this to your .env:")
                    print(f"LINKEDIN_PERSON_URN={member_urn}")
                else:
                    print("⚠️  No 'sub' field in response")
            else:
                print(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(json.dumps(error_data, indent=2))
                except:
                    print(response.text)
                print()
                print("This error means your access token doesn't have the 'openid' scope.")
                print("You need to run the OAuth flow again with these scopes:")
                print("  - openid")
                print("  - profile")
                print("  - w_member_social")
                print()
                print("Run: python scripts/get_linkedin_token.py")

        except Exception as e:
            print(f"❌ Exception: {e}")


if __name__ == "__main__":
    asyncio.run(get_userinfo())
