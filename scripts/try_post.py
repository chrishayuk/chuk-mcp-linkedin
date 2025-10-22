#!/usr/bin/env python3
"""
Try to make a test post to LinkedIn to reveal URN info from error.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_linkedin.api import config
import httpx


async def try_post():
    """Try different person URN formats"""

    print("Testing LinkedIn Person URN formats")
    print("=" * 60)
    print()

    # Different URN formats to try
    urns_to_try = [
        config.linkedin_person_urn,  # Try the URN from .env first
        "urn:li:person:me",
        "me",
    ]

    test_text = "Test post - please ignore"

    for urn in urns_to_try:
        print(f"Trying with URN: {urn}")

        payload = {
            "author": urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": test_text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        url = "https://api.linkedin.com/v2/ugcPosts"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {config.linkedin_access_token}",
                        "Content-Type": "application/json",
                        "X-Restli-Protocol-Version": "2.0.0",
                    },
                    timeout=30.0,
                )

                print(f"  Status: {response.status_code}")

                if response.status_code in (200, 201):
                    print(f"  ✓ SUCCESS! This URN works: {urn}")
                    result = response.json()
                    print(f"  Response: {result}")
                    print()
                    print("Add this to .env:")
                    print(f"LINKEDIN_PERSON_URN={urn}")
                    return
                else:
                    print(f"  Error: {response.text}")
                    print()

            except Exception as e:
                print(f"  Exception: {e}")
                print()

    print("None of the URN formats worked.")
    print()
    print("The error messages above might contain clues about the correct format.")
    print("Look for any mention of 'person' or 'urn' in the error messages.")


if __name__ == "__main__":
    asyncio.run(try_post())
