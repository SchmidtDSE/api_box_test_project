#!/usr/bin/env python3
"""
Test curl fixes for API Box

License: CC-BY-4.0
"""
import subprocess
import json
import sys

def run_curl_test(url, expected_status=200, expected_error=None):
    """Run a curl test and check the response."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=10
        )

        # Extract HTTP status code from the end
        output = result.stdout
        if len(output) >= 3:
            status_code = output[-3:]
            response_body = output[:-3]
        else:
            status_code = "000"
            response_body = output

        print(f"URL: {url}")
        print(f"Status: {status_code}")
        print(f"Response: {response_body}")

        try:
            response_json = json.loads(response_body) if response_body else {}
        except json.JSONDecodeError:
            response_json = {"raw": response_body}

        # Check status code
        if int(status_code) != expected_status:
            print(f"❌ Expected status {expected_status}, got {status_code}")
            return False

        # Check for expected error
        if expected_error and "error" in response_json:
            if expected_error in response_json["error"]:
                print(f"✅ Got expected error: {expected_error}")
                return True
            else:
                print(f"❌ Expected error '{expected_error}', got: {response_json['error']}")
                return False
        elif expected_error:
            print(f"❌ Expected error '{expected_error}' but got no error")
            return False
        elif "error" in response_json:
            print(f"❌ Unexpected error: {response_json['error']}")
            return False
        else:
            print("✅ Test passed")
            return True

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout for {url}")
        return False
    except Exception as e:
        print(f"❌ Error testing {url}: {e}")
        return False

def test_curl_fixes():
    """Test various curl scenarios to ensure proper error handling."""
    print("Testing Curl Fixes")
    print("=" * 50)

    base_url = "http://localhost:8000"

    tests = [
        # Test allowed routes
        (f"{base_url}/allowed_routes_remote", 200, None),
        (f"{base_url}/allowed_routes_remote/users", 200, None),
        (f"{base_url}/allowed_routes_remote/health", 200, None),

        # Test blocked routes
        (f"{base_url}/allowed_routes_remote/admin", 403, "not allowed"),
        (f"{base_url}/restricted_remote/users/123/permissions", 403, "not allowed"),

        # Test custom mapping
        (f"{base_url}/custom_mapping_remote/users", 200, None),
        (f"{base_url}/custom_mapping_remote/users/123/permissions", 200, None),

        # Test non-existent routes
        (f"{base_url}/nonexistent_remote", 404, "not found"),
    ]

    passed = 0
    failed = 0

    for url, expected_status, expected_error in tests:
        print(f"\n--- Testing {url} ---")
        if run_curl_test(url, expected_status, expected_error):
            passed += 1
        else:
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All curl tests passed!")
    else:
        print("⚠️  Some curl tests failed")

if __name__ == "__main__":
    test_curl_fixes()