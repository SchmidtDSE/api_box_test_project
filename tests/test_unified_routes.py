#!/usr/bin/env python3
"""
Test the unified routes structure

License: CC-BY-4.0
"""
import sys
sys.path.insert(0, '/workspace/api_box')

from api_box.config import _route_matches_patterns

def test_unified_routes():
    """Test the unified routes structure with mixed string/dict patterns."""
    print("Testing Unified Routes Structure")
    print("=" * 50)

    # Mock routes config like custom_mapping_remote
    routes = [
        "users",                                        # String route
        "users/{{user_id}}",                           # String route with variable
        "users/{{user_id}}/profile",                  # String route
        {                                              # Dict route with custom mapping
            "route": "users/{{user_id}}/permissions",
            "remote_route": "user-permissions/{{user_id}}",
            "method": "get"
        }
    ]

    # Test cases
    tests = [
        ("users", True),                     # Should match string route
        ("users/123", True),                 # Should match string route with variable
        ("users/123/profile", True),         # Should match string route
        ("users/123/permissions", True),     # Should match dict route
        ("users/123/settings", False),      # Should not match any route
        ("posts", False),                    # Should not match any route
    ]

    passed = 0
    failed = 0

    for route, expected in tests:
        result = _route_matches_patterns(route, routes)
        status = "✅" if result == expected else "❌"
        print(f"{status} Route '{route}': {result} (expected {expected})")

        if result == expected:
            passed += 1
        else:
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All unified route tests passed!")
        print("\nNow routes can contain:")
        print("- Strings: 'users' (simple GET routes)")
        print("- Dicts: {'route': 'users/{{id}}', 'method': 'post'} (different method)")
        print("- Dicts: {'route': 'users/{{id}}/perms', 'remote_route': 'user-perms/{{id}}'} (custom mapping)")
    else:
        print("⚠️  Some tests failed - check unified route logic")

if __name__ == "__main__":
    test_unified_routes()