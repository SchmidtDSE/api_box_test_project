#!/usr/bin/env python3
"""
Comprehensive test script for route restrictions and allowed routes functionality in test_project.

This script tests all the different restriction scenarios configured in the test_project.

License: CC-BY-4.0
"""

#
# IMPORTS
#
import sys
from pathlib import Path

# Add the api_box package to the path for testing
api_box_path = Path(__file__).parent.parent / "api_box"
sys.path.insert(0, str(api_box_path))

from api_box.config import is_route_allowed, load_main_config

#
# CONSTANTS
#
CONFIG_PATH = "config/config.yaml"

#
# PUBLIC
#
def test_global_restrictions():
    """Test global restrictions defined in main config."""
    print("\n" + "="*60)
    print("TESTING GLOBAL RESTRICTIONS")
    print("="*60)
    print("Global restrictions: users/{{}}/delete, admin/{{}}/dangerous")

    config = load_main_config(CONFIG_PATH)

    test_cases = [
        # Global restrictions should apply to all remotes
        ("users/123/delete", "remote_4321", False, "Global restriction on delete"),
        ("users/456/delete", "another_name", False, "Global restriction on delete"),
        ("users/789/delete", "restricted_remote", False, "Global restriction on delete"),

        ("admin/999/dangerous", "remote_4321", False, "Global restriction on dangerous admin"),
        ("admin/888/dangerous", "another_name", False, "Global restriction on dangerous admin"),

        # These should be allowed (not in global restrictions)
        ("users/123/profile", "remote_4321", True, "Not globally restricted"),
        ("users/456/settings", "remote_4321", True, "Not globally restricted"),
        ("admin/safe", "remote_4321", True, "Safe admin route allowed"),
    ]

    return run_test_cases(test_cases, config)


def test_remote_specific_restrictions():
    """Test remote-specific restrictions."""
    print("\n" + "="*60)
    print("TESTING REMOTE-SPECIFIC RESTRICTIONS")
    print("="*60)
    print("restricted_remote: users/{{}}/permissions, admin, admin/{{}}, system/{{}}/config, users/{{}}/private")
    print("another_name: users/{{}}/settings")

    config = load_main_config(CONFIG_PATH)

    test_cases = [
        # restricted_remote has additional restrictions
        ("users/123/permissions", "restricted_remote", False, "Remote-specific restriction"),
        ("admin", "restricted_remote", False, "Remote-specific admin restriction"),
        ("admin/dashboard", "restricted_remote", False, "Remote-specific admin subroute restriction"),
        ("system/prod/config", "restricted_remote", False, "Remote-specific system config restriction"),
        ("users/123/private", "restricted_remote", False, "Remote-specific private data restriction"),

        # Same routes should be allowed on other remotes (if not globally restricted)
        ("users/123/permissions", "remote_4321", True, "Not restricted on this remote"),
        ("admin", "remote_4321", True, "Not restricted on this remote"),
        ("admin/dashboard", "remote_4321", True, "Not restricted on this remote"),
        ("system/prod/config", "remote_4321", True, "Not restricted on this remote"),

        # another_name has users/{{}}/settings restricted
        ("users/123/settings", "another_name", False, "Remote-specific settings restriction"),
        ("users/123/settings", "remote_4321", True, "Settings allowed on other remote"),

        # Routes not restricted should work everywhere
        ("users/123/profile", "restricted_remote", True, "Profile allowed"),
        ("users/123/posts", "restricted_remote", True, "Posts allowed"),
    ]

    return run_test_cases(test_cases, config)


def test_allowed_routes_whitelist():
    """Test explicit allowed routes (whitelist approach)."""
    print("\n" + "="*60)
    print("TESTING ALLOWED ROUTES WHITELIST")
    print("="*60)
    print("allowed_routes_remote allows: users, users/{{}}, users/{{}}/profile, users/{{}}/posts, posts, posts/{{}}, health")

    config = load_main_config(CONFIG_PATH)

    test_cases = [
        # Routes explicitly in the whitelist should be allowed
        ("users", "allowed_routes_remote", True, "Explicitly allowed"),
        ("users/123", "allowed_routes_remote", True, "Explicitly allowed"),
        ("users/123/profile", "allowed_routes_remote", True, "Explicitly allowed"),
        ("users/123/posts", "allowed_routes_remote", True, "Explicitly allowed"),
        ("posts", "allowed_routes_remote", True, "Explicitly allowed"),
        ("posts/456", "allowed_routes_remote", True, "Explicitly allowed"),
        ("health", "allowed_routes_remote", True, "Explicitly allowed"),

        # Routes NOT in the whitelist should be blocked
        ("users/123/settings", "allowed_routes_remote", False, "Not in allowed list"),
        ("users/123/permissions", "allowed_routes_remote", False, "Not in allowed list"),
        ("admin", "allowed_routes_remote", False, "Not in allowed list"),
        ("admin/dashboard", "allowed_routes_remote", False, "Not in allowed list"),
        ("system/config", "allowed_routes_remote", False, "Not in allowed list"),
        ("api/docs", "allowed_routes_remote", False, "Not in allowed list"),

        # Even routes that would normally be allowed elsewhere are blocked
        ("users/123/public", "allowed_routes_remote", False, "Not in whitelist"),
        ("posts/456/comments", "allowed_routes_remote", False, "Not in whitelist"),
    ]

    return run_test_cases(test_cases, config)


def test_custom_route_mapping_with_restrictions():
    """Test that custom route mappings work with restrictions."""
    print("\n" + "="*60)
    print("TESTING CUSTOM ROUTE MAPPING WITH RESTRICTIONS")
    print("="*60)
    print("another_name has custom route mappings and additional restrictions")

    config = load_main_config(CONFIG_PATH)

    test_cases = [
        # Routes with custom mappings should be checked against the original pattern
        ("users/123/permissions", "another_name", True, "Custom mapped route allowed"),
        ("users/123", "another_name", True, "Custom mapped route allowed"),
        ("users/123/profile", "another_name", True, "Custom mapped route allowed"),

        # Remote-specific restrictions should still apply
        ("users/123/settings", "another_name", False, "Remote-specific restriction"),

        # Global restrictions should still apply
        ("users/123/delete", "another_name", False, "Global restriction"),

        # Routes not in custom mapping should follow normal rules
        ("users/123/other", "another_name", True, "Not restricted, not custom mapped"),
    ]

    return run_test_cases(test_cases, config)


def test_precedence_rules():
    """Test that restriction precedence rules work correctly."""
    print("\n" + "="*60)
    print("TESTING PRECEDENCE RULES")
    print("="*60)
    print("Remote-specific settings should override global settings")

    config = load_main_config(CONFIG_PATH)

    test_cases = [
        # allowed_routes_remote has whitelist, so even normally allowed routes are blocked
        ("users/123/anything", "allowed_routes_remote", False, "Whitelist overrides global permissions"),
        ("admin/safe", "allowed_routes_remote", False, "Whitelist overrides global permissions"),

        # restricted_remote has additional restrictions beyond global
        ("users/123/permissions", "restricted_remote", False, "Additional remote restriction"),
        ("users/123/permissions", "remote_4321", True, "Not restricted on other remote"),

        # Global restrictions still apply even with remote-specific rules
        ("users/123/delete", "restricted_remote", False, "Global restriction applies"),
        ("users/123/delete", "allowed_routes_remote", False, "Global restriction applies even with whitelist"),
    ]

    return run_test_cases(test_cases, config)


def run_test_cases(test_cases, config):
    """Run a list of test cases and return success status."""
    passed = 0
    failed = 0

    for route, remote, expected, description in test_cases:
        result = is_route_allowed(route, config, remote)
        status = "✓" if result == expected else "✗"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {route} on {remote}: {result} ({description})")

    print(f"\nSection Results: {passed} passed, {failed} failed")
    return failed == 0


def main():
    """Run all restriction tests."""
    print("API Box Route Restrictions Test Suite - test_project")
    print("Testing comprehensive route restriction and allowed routes functionality")

    try:
        config = load_main_config(CONFIG_PATH)
        print(f"✓ Loaded config: {config['name']}")
        print(f"  Description: {config['description']}")
        print(f"  Remotes: {', '.join(config['remotes'])}")
    except Exception as e:
        print(f"✗ Failed to load config: {e}")
        return 1

    # Run all test suites
    all_passed = True
    all_passed &= test_global_restrictions()
    all_passed &= test_remote_specific_restrictions()
    all_passed &= test_allowed_routes_whitelist()
    all_passed &= test_custom_route_mapping_with_restrictions()
    all_passed &= test_precedence_rules()

    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)

    if all_passed:
        print("✓ All route restriction tests passed!")
        print("\nThe route restriction and allowed routes functionality is working correctly:")
        print("  • Global restrictions are enforced across all remotes")
        print("  • Remote-specific restrictions override global settings")
        print("  • Allowed routes whitelist approach works")
        print("  • Custom route mapping is compatible with restrictions")
        print("  • Precedence rules are working as expected")
        return 0
    else:
        print("✗ Some route restriction tests failed!")
        print("\nPlease check the implementation of:")
        print("  • Route pattern matching with {{}} syntax")
        print("  • Remote-specific config loading")
        print("  • Precedence between global and remote restrictions")
        return 1


if __name__ == "__main__":
    sys.exit(main())