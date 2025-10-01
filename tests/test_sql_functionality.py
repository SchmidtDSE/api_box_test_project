#!/usr/bin/env python3
"""
Test SQL Functionality for API Box

Tests the SQL database wrapper with generated test data.

License: CC-BY-4.0
"""
import sys
from pathlib import Path

# Add api_box to path
sys.path.insert(0, '/workspace/api_box')

from api_box.database_config import load_database_config, find_database_route
from api_box.sql_builder import build_sql_query
import duckdb


def test_load_config():
    """Test loading the database configuration."""
    print("Testing database config loading...")
    config = load_database_config('test_db', config_dir='api_box_config/databases')
    print(f"✓ Loaded database: {config['name']}")
    print(f"  Tables: {list(config['tables'].keys())}")
    print(f"  Queries: {list(config['queries'].keys())}")
    print(f"  Routes: {len(config['routes'])} routes")
    return config


def test_route_matching(config):
    """Test route pattern matching."""
    print("\nTesting route matching...")

    test_paths = [
        'users',
        'users/5',
        'users/5/permissions',
        'users/5/posts',
        'users/active',
        'posts',
        'posts/10',
    ]

    for path in test_paths:
        route = find_database_route(path, config)
        if route:
            print(f"✓ Matched '{path}' -> {route['route']}")
        else:
            print(f"✗ No match for '{path}'")


def test_sql_queries(config):
    """Test SQL query execution."""
    print("\nTesting SQL queries...")

    # Connect to DuckDB
    conn = duckdb.connect(':memory:')

    # Test 1: Get all users
    print("\n1. Get all users:")
    route = find_database_route('users', config)
    sql = build_sql_query(route['sql'], config)
    print(f"   SQL: {sql}")

    try:
        result = conn.execute(sql).fetchdf()
        print(f"   ✓ Returned {len(result)} users")
        if len(result) > 0:
            print(f"   Sample: {result.iloc[0].to_dict()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test 2: Get specific user
    print("\n2. Get user with ID 5:")
    route = find_database_route('users/5', config)
    sql = build_sql_query(route['sql'], config, {'user_id': '5'})
    print(f"   SQL: {sql}")

    try:
        result = conn.execute(sql).fetchdf()
        print(f"   ✓ Returned {len(result)} user(s)")
        if len(result) > 0:
            print(f"   Data: {result.iloc[0].to_dict()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test 3: Get user permissions (uses named query)
    print("\n3. Get permissions for user 5:")
    route = find_database_route('users/5/permissions', config)
    sql = build_sql_query(route['sql'], config, {'user_id': '5'})
    print(f"   SQL: {sql}")

    try:
        result = conn.execute(sql).fetchdf()
        print(f"   ✓ Returned {len(result)} permission(s)")
        if len(result) > 0:
            print(f"   Data: {result.to_dict('records')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test 4: Get user posts (uses named query)
    print("\n4. Get posts for user 5:")
    route = find_database_route('users/5/posts', config)
    sql = build_sql_query(route['sql'], config, {'user_id': '5'})
    print(f"   SQL: {sql}")

    try:
        result = conn.execute(sql).fetchdf()
        print(f"   ✓ Returned {len(result)} post(s)")
        if len(result) > 0:
            print(f"   Sample: {result.iloc[0].to_dict()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test 5: Get active users (uses named query)
    print("\n5. Get active users:")
    route = find_database_route('users/active', config)
    sql = build_sql_query(route['sql'], config)
    print(f"   SQL: {sql}")

    try:
        result = conn.execute(sql).fetchdf()
        print(f"   ✓ Returned {len(result)} active user(s)")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test 6: Get all posts
    print("\n6. Get all posts:")
    route = find_database_route('posts', config)
    sql = build_sql_query(route['sql'], config)
    print(f"   SQL: {sql}")

    try:
        result = conn.execute(sql).fetchdf()
        print(f"   ✓ Returned {len(result)} posts")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test 7: Get specific post
    print("\n7. Get post with ID 10:")
    route = find_database_route('posts/10', config)
    sql = build_sql_query(route['sql'], config, {'post_id': '10'})
    print(f"   SQL: {sql}")

    try:
        result = conn.execute(sql).fetchdf()
        print(f"   ✓ Returned {len(result)} post(s)")
        if len(result) > 0:
            print(f"   Data: {result.iloc[0].to_dict()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    conn.close()


def main():
    """Run all tests."""
    print("=" * 60)
    print("API Box SQL Functionality Tests")
    print("=" * 60)

    config = test_load_config()
    test_route_matching(config)
    test_sql_queries(config)

    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
