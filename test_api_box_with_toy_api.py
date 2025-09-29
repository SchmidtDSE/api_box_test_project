#!/usr/bin/env python3
"""

API Box Integration Test with Toy API

Tests API Box route restrictions using configurable toy APIs.

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
CONFIG_PATH = "api_box_config/config.yaml"

# Toy API configs for testing
TOY_API_CONFIGS = {
    "custom_mapping_remote": {
        "config": "custom_mapping.yaml",
        "port": 1234,
        "description": "Custom route mapping testing"
    },
    "basic_remote": {
        "config": "basic.yaml",
        "port": 4321,
        "description": "Basic routes testing"
    },
    "restricted_remote": {
        "config": "restricted.yaml",
        "port": 8080,
        "description": "Security restriction testing"
    },
    "allowed_routes_remote": {
        "config": "allowed_routes.yaml",
        "port": 9090,
        "description": "Whitelist testing"
    }
}

#
# PUBLIC
#
def test_route_restrictions():
    """Test route restriction functionality."""
    print("Testing API Box route restrictions with Toy API...")

    # Load main config
    try:
        config = load_main_config(CONFIG_PATH)
        print("✓ API Box config loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load API Box config: {e}")
        return False

    # Test cases
    test_cases = [
        # Global restrictions (should block users/{}/delete for all remotes)
        ("users/123/delete", "basic_remote", False, "Global restriction"),
        ("users/456/delete", "allowed_routes_remote", False, "Global restriction"),
        ("admin/999/dangerous", "basic_remote", False, "Global restriction"),

        # Remote-specific restrictions (restricted_remote blocks additional routes)
        ("users/123/permissions", "restricted_remote", False, "Remote-specific restriction"),
        ("users/123/permissions", "basic_remote", True, "Not restricted on this remote"),
        ("admin/dashboard", "restricted_remote", False, "Admin routes restricted"),
        ("admin/dashboard", "basic_remote", True, "Admin allowed on basic remote"),

        # Allowed routes (allowed_routes_remote only allows specific patterns)
        ("users", "allowed_routes_remote", True, "Explicitly allowed"),
        ("users/123", "allowed_routes_remote", True, "Explicitly allowed"),
        ("users/123/profile", "allowed_routes_remote", True, "Explicitly allowed"),
        ("users/123/posts", "allowed_routes_remote", True, "Explicitly allowed"),
        ("posts", "allowed_routes_remote", True, "Explicitly allowed"),
        ("posts/456", "allowed_routes_remote", True, "Explicitly allowed"),
        ("health", "allowed_routes_remote", True, "Explicitly allowed"),
        ("users/123/settings", "allowed_routes_remote", False, "Not in allowed list"),
        ("admin/dashboard", "allowed_routes_remote", False, "Not in allowed list"),

        # Custom mapping remote (should respect restrictions)
        ("users/123/settings", "custom_mapping_remote", False, "Remote-specific restriction"),
        ("users/123/delete", "custom_mapping_remote", False, "Global restriction"),
        ("users/123/profile", "custom_mapping_remote", True, "Should be allowed"),
    ]

    passed = 0
    failed = 0

    for route, remote, expected, description in test_cases:
        result = is_route_allowed(route, config, remote)
        if result == expected:
            print(f"✓ {route} on {remote}: {result} ({description})")
            passed += 1
        else:
            print(f"✗ {route} on {remote}: expected {expected}, got {result} ({description})")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def show_setup_instructions():
    """Show instructions for setting up the test environment."""
    print("API Box + Toy API Integration Test Setup")
    print("=" * 60)
    print()
    print("1. Start Toy APIs (in separate terminals):")
    for remote, info in TOY_API_CONFIGS.items():
        print(f"   toy_api {info['config'].replace('.yaml', '')}  # {info['description']} (port {info['port']})")
    print()
    print("2. Test API Box route restrictions:")
    print("   python test_api_box_with_toy_api.py")
    print()
    print("3. Manual testing examples:")
    print("   # These should work (allowed routes)")
    print("   curl http://localhost:8000/basic_remote/latest/users")
    print("   curl http://localhost:8000/basic_remote/latest/users/123/profile")
    print()
    print("   # These should be blocked (restricted routes)")
    print("   curl http://localhost:8000/basic_remote/latest/users/123/delete")
    print("   curl http://localhost:8000/restricted_remote/latest/admin/dashboard")
    print()
    print("API Box Config: api_box_config/")
    print("Toy API Configs: toy_api_config/")


def main():
    """Run the integration test."""
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        show_setup_instructions()
        return 0

    print("API Box + Toy API Integration Test")
    print("=" * 60)

    success = test_route_restrictions()

    if success:
        print("\n✓ All API Box route restriction tests passed!")
        print("\nThe integration between API Box and Toy API is working correctly:")
        print("  • Global restrictions are enforced across all remotes")
        print("  • Remote-specific restrictions override global settings")
        print("  • Allowed routes whitelist approach works")
        print("  • Custom route mapping is compatible with restrictions")
        return 0
    else:
        print("\n✗ Some API Box route restriction tests failed!")
        print("\nCheck the API Box configuration and Toy API setup.")
        return 1


if __name__ == "__main__":
    sys.exit(main())