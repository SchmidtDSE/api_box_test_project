#!/usr/bin/env python3
"""
Debug table generation

License: CC-BY-4.0
"""
import sys
sys.path.insert(0, '/workspace/toy_api')

from toy_api.table_generator import create_table

# Test with a simple config
config = {
    "config": {
        "NB_USERS": 5
    },
    "shared": {
        "user_id[[NB_USERS]]": "UNIQUE[int]"
    },
    "tables": {
        "users[[NB_USERS]]": {
            "user_id": "[[user_id]]",
            "name": "NAME"
        }
    }
}

result = create_table(config, to_dataframe=False)
print("Result keys:", result.keys() if isinstance(result, dict) else "single table")
print("\nFirst few rows:")
if isinstance(result, dict):
    for table_name, data in result.items():
        print(f"\n{table_name}:")
        for row in data[:3]:
            print(f"  {row}")
else:
    for row in result[:3]:
        print(f"  {row}")
