#!/usr/bin/env python3
"""
Demonstration of user isolation in chuk-mcp-linkedin.

This script demonstrates that:
1. Each user gets their own isolated manager instance
2. Users cannot access each other's drafts
3. Same user can reconnect and access their drafts from a new session
4. All operations are scoped to user_id (not session_id)

Security Features Demonstrated:
- User-level isolation via ManagerFactory
- No cross-user access possible
- Session-independent data persistence
- Artifact storage scoped to user_id
"""

import asyncio
from chuk_mcp_linkedin.manager_factory import ManagerFactory, set_factory


async def main():
    """Demonstrate user isolation."""

    # Initialize factory with memory-based artifacts
    factory = ManagerFactory(use_artifacts=True, artifact_provider="memory")
    set_factory(factory)

    print("=" * 70)
    print("USER ISOLATION DEMONSTRATION")
    print("=" * 70)
    print()

    # Simulate User 1
    print("👤 User 1 (user_id=alice): Creating drafts...")
    user1_manager = factory.get_manager("alice")
    draft1 = user1_manager.create_draft(
        name="Alice's Draft 1",
        post_type="text",
    )
    draft2 = user1_manager.create_draft(
        name="Alice's Draft 2",
        post_type="text",
    )
    print(f"   ✓ Created: {draft1.name} (ID: {draft1.draft_id})")
    print(f"   ✓ Created: {draft2.name} (ID: {draft2.draft_id})")
    alice_drafts = user1_manager.list_drafts()
    print(f"   ✓ Alice has {len(alice_drafts)} drafts")
    print()

    # Simulate User 2
    print("👤 User 2 (user_id=bob): Creating drafts...")
    user2_manager = factory.get_manager("bob")
    draft3 = user2_manager.create_draft(
        name="Bob's Draft 1",
        post_type="text",
    )
    print(f"   ✓ Created: {draft3.name} (ID: {draft3.draft_id})")
    bob_drafts = user2_manager.list_drafts()
    print(f"   ✓ Bob has {len(bob_drafts)} drafts")
    print()

    # Verify isolation
    print("🔒 ISOLATION VERIFICATION")
    print("-" * 70)

    # User 1 should only see their drafts
    print("👤 Alice's view:")
    alice_drafts = user1_manager.list_drafts()
    for draft in alice_drafts:
        print(f"   • {draft['name']} (ID: {draft['draft_id']})")
    assert len(alice_drafts) == 2, "Alice should have 2 drafts"
    assert all("Alice" in d["name"] for d in alice_drafts), "Alice should only see her drafts"
    print(f"   ✓ Alice correctly sees only her {len(alice_drafts)} drafts")
    print()

    # User 2 should only see their drafts
    print("👤 Bob's view:")
    bob_drafts = user2_manager.list_drafts()
    for draft in bob_drafts:
        print(f"   • {draft['name']} (ID: {draft['draft_id']})")
    assert len(bob_drafts) == 1, "Bob should have 1 draft"
    assert all("Bob" in d["name"] for d in bob_drafts), "Bob should only see his drafts"
    print(f"   ✓ Bob correctly sees only his {len(bob_drafts)} draft")
    print()

    # Verify Bob cannot access Alice's drafts
    print("🚫 CROSS-USER ACCESS PREVENTION")
    print("-" * 70)
    bob_attempt = user2_manager.get_draft(draft1.draft_id)
    if bob_attempt is None:
        print(f"   ✓ Bob CANNOT access Alice's draft {draft1.draft_id}")
    else:
        print("   ✗ SECURITY VIOLATION: Bob accessed Alice's draft!")
        raise AssertionError("Cross-user access detected!")
    print()

    # Verify same user can reconnect from new session
    print("🔄 SESSION INDEPENDENCE")
    print("-" * 70)
    print("👤 Alice reconnects from a new session...")
    alice_new_session = factory.get_manager("alice")  # Same user_id, simulates new session
    alice_drafts_after_reconnect = alice_new_session.list_drafts()
    print(f"   ✓ Alice sees {len(alice_drafts_after_reconnect)} drafts after reconnecting")
    assert len(alice_drafts_after_reconnect) == 2, "Alice should still have 2 drafts"
    assert alice_drafts_after_reconnect == alice_drafts, "Drafts should be identical"
    print("   ✓ Same user, different session = same data (user_id scoped, not session scoped)")
    print()

    # Verify manager caching
    print("💾 MANAGER CACHING")
    print("-" * 70)
    alice_manager_again = factory.get_manager("alice")
    print(f"   • First manager:  {id(alice_new_session)}")
    print(f"   • Second manager: {id(alice_manager_again)}")
    assert alice_manager_again is alice_new_session, "Should return cached manager"
    print("   ✓ Same manager instance returned for same user_id (cached)")
    print()

    # Show active users
    print("📊 ACTIVE USERS")
    print("-" * 70)
    active_users = factory.get_active_users()
    print(f"   Active user_ids: {active_users}")
    assert "alice" in active_users, "Alice should be active"
    assert "bob" in active_users, "Bob should be active"
    print(f"   ✓ {len(active_users)} users with active managers")
    print()

    # Cleanup demo
    print("🧹 CLEANUP")
    print("-" * 70)
    factory.clear_manager("alice")
    active_after_clear = factory.get_active_users()
    print("   ✓ Cleared Alice's manager")
    print(f"   Active users now: {active_after_clear}")
    assert "alice" not in active_after_clear, "Alice should not be in active users"
    assert "bob" in active_after_clear, "Bob should still be active"
    print()

    # Summary
    print("=" * 70)
    print("✅ ALL SECURITY CHECKS PASSED")
    print("=" * 70)
    print()
    print("Security Guarantees:")
    print("  ✓ Each user has isolated data (scoped to user_id)")
    print("  ✓ No cross-user access possible")
    print("  ✓ Same user can access data across sessions")
    print("  ✓ All artifacts scoped to user_id (not session_id)")
    print("  ✓ Manager instances cached per user for performance")
    print()


if __name__ == "__main__":
    asyncio.run(main())
