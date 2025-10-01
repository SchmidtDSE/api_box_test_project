#!/usr/bin/env python3
"""

Generate Test Data for API Box SQL Testing

Creates parquet files for testing SQL database functionality.

License: CC-BY-4.0

"""
import sys
from pathlib import Path

# Add toy_api to path
sys.path.insert(0, '/workspace/toy_api')

from toy_api.table_generator import create_table


def main() -> None:
    """Generate test parquet files."""
    output_dir = Path("tables")
    output_dir.mkdir(exist_ok=True)

    print("Generating tables parquet files...")
    create_table(
        table_config="toy_api_config/databases/test_db.yaml",
        dest="tables",
        file_type='parquet'
    )
    print("✓ Generated all tables parquet files")

    print("\n✓ All test data generated successfully!")


if __name__ == "__main__":
    main()
