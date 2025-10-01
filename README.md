# API Box Test Project

Integration testing environment for [API Box](https://github.com/SchmidtDSE/api_box) route restrictions using configurable [Toy API](https://github.com/brookisme/toy_api) servers.

## Quick Start Commands

Copy and paste these commands to get the full test environment running:

### Terminal 1 - Start Toy APIs
```bash
# Start basic remote (port 4321)
pixi run toy_api basic

# In another terminal:
# Start custom mapping remote (port 1234)
pixi run toy_api custom_mapping

# In another terminal:
# Start restricted remote (port 8080)
pixi run toy_api restricted

# In another terminal:
# Start allowed routes remote (port 9090)
pixi run toy_api allowed_routes
```

### Terminal 2 - Start API Box
```bash
# Run API Box from api_box_test_project root directory
# (Uses api_box_config/ in current directory)
pixi run api-box start
```

### Terminal 3 - Run Integration Tests

```bash
# Run comprehensive route restriction tests
python tests/test_api_box_with_toy_api.py

# Or run specific test suites
python tests/test_route_restrictions.py
python tests/test_sql_functionality.py
```

or run manual tests:

```bash
# Remote API Endpoints - Working
curl http://localhost:8000/basic_remote/latest/users/123/profile
curl http://localhost:8000/allowed_routes_remote/latest/users

# Remote API Endpoints - Blocked
curl http://localhost:8000/basic_remote/latest/users/123/delete
curl http://localhost:8000/restricted_remote/latest/admin/dashboard
curl http://localhost:8000/allowed_routes_remote/latest/users/123/settings

# SQL Database Endpoints
curl http://localhost:8000/test_db/users
curl http://localhost:8000/test_db/users/5
curl http://localhost:8000/test_db/users/5/permissions
curl http://localhost:8000/test_db/users/5/posts
```

## What This Project Tests

This project provides a comprehensive testing environment for **API Box** functionality. It demonstrates:

- **Route restrictions** - Global and remote-specific access control
- **Allowed routes (whitelisting)** - Only specific patterns allowed
- **Custom route mapping** - Mapping between different API endpoint structures
- **SQL database support** - Querying Parquet files via REST endpoints
- **Cloud storage** - Database tables from S3, GCS, HTTPS, and local paths

## Project Components

### API Box Configuration (`api_box_config/`)
- `config.yaml` - Main API Box configuration with global restrictions and databases
- `remotes/` - Individual remote configurations:
  - `basic_remote.yaml` - Basic API (port 4321) with minimal restrictions
  - `custom_mapping_remote.yaml` - Custom route mapping API (port 1234)
  - `restricted_remote.yaml` - Heavily restricted API (port 8080)
  - `allowed_routes_remote.yaml` - Whitelist-only API (port 9090)
- `databases/` - SQL database configurations:
  - `test_db.yaml` - Test database with users, permissions, and posts tables

### Toy API Configuration (`toy_api_config/`)
Matching configurations that define the actual routes for each toy API server:
- `basic.yaml` - Basic routes for testing
- `custom_mapping.yaml` - Custom endpoint structure
- `restricted.yaml` - Routes that will be restricted by API Box
- `allowed_routes.yaml` - Mix of allowed and blocked routes
- `databases/` - Table generation configurations:
  - `test_db.yaml` - Generates test parquet files for SQL testing

### Integration Tests (`tests/`)
- `test_api_box_with_toy_api.py` - Comprehensive test suite with 15+ test cases
- `test_route_restrictions.py` - Direct API Box config testing
- `test_sql_functionality.py` - SQL database functionality tests
- `test_unified_routes.py` - Route testing
- `ROUTE_RESTRICTIONS_TEST.md` - Testing documentation

### Data Generation
- `generate_test_data.py` - Generates parquet files for SQL testing
- `debug_table_gen.py` - Debug utility for table generation
- `tables/` - Generated parquet files (users, permissions, posts)

## Dependencies

- **[API Box](https://github.com/SchmidtDSE/api_box)** - The API gateway being tested
- **[Toy API](https://github.com/brookisme/toy_api)** - Configurable test API servers
- **Python 3.8+** with PyYAML for config parsing

## Project Structure

```
api_box_test_project/
├── api_box_config/                    # API Box configurations
│   ├── config.yaml                    # Main config with restrictions & databases
│   ├── remotes/                       # Remote-specific configurations
│   │   ├── basic_remote.yaml
│   │   ├── custom_mapping_remote.yaml
│   │   ├── restricted_remote.yaml
│   │   └── allowed_routes_remote.yaml
│   └── databases/                     # SQL database configurations
│       └── test_db.yaml               # Test database with parquet tables
├── toy_api_config/                    # Toy API configurations
│   ├── basic.yaml
│   ├── custom_mapping.yaml
│   ├── restricted.yaml
│   ├── allowed_routes.yaml
│   └── databases/                     # Table generation configs
│       └── test_db.yaml               # Generates test parquet data
├── tables/                            # Generated parquet files
│   ├── users.parquet
│   ├── user_permissions.parquet
│   └── posts.parquet
├── tests/                             # Test suite
│   ├── test_api_box_with_toy_api.py  # Integration tests
│   ├── test_route_restrictions.py    # Config tests
│   ├── test_sql_functionality.py     # SQL database tests
│   └── test_unified_routes.py        # Route testing
├── generate_test_data.py              # Data generation script
├── debug_table_gen.py                 # Debug utility
└── README.md                          # This file
```

## Test Scenarios

### Global Restrictions (all remotes)
- `users/{user_id}/delete` - Blocked across all APIs
- `admin/{admin_id}/dangerous` - Blocked dangerous admin routes

### Remote-Specific Restrictions
- `restricted_remote` blocks additional patterns:
  - `users/{user_id}/permissions`
  - `admin/*` (all admin routes)

### Allowed Routes (whitelist)
- `allowed_routes_remote` only allows specific patterns:
  - `users`, `users/{user_id}`, `users/{user_id}/profile`
  - `users/{user_id}/posts`, `posts`, `posts/{post_id}`
  - `health`

### Custom Route Mapping
- `custom_mapping_remote` demonstrates mapping between different API structures
- API Box route `users/{user_id}/permissions` → Toy API `/user-permissions/{user_id}`

## Setup Instructions

1. **Install Toy API**:
   ```bash
   pip install toy_api
   # or clone from: https://github.com/brookisme/toy_api
   ```

2. **Initialize local toy API configs** (optional):
   ```bash
   toy_api --init-config
   # Copies toy_api configs to local toy_api_config/ directory
   ```

3. **Clone API Box**:
   ```bash
   git clone https://github.com/SchmidtDSE/api_box.git
   cd api_box && pixi install
   ```

4. **Run the test environment** using the Quick Start Commands above

## Validation

The integration tests validate that:
- ✅ Global restrictions apply to all remotes
- ✅ Remote-specific restrictions override global settings
- ✅ Whitelist approach works correctly
- ✅ Custom route mapping respects restrictions
- ✅ Port management handles multiple APIs correctly
- ✅ SQL database routes execute queries correctly
- ✅ Table references and parameter substitution work
- ✅ Named queries resolve properly
- ✅ DuckDB integration functions with parquet files

## SQL Database Testing

To test SQL functionality:

```bash
# Generate test data (creates parquet files in tables/)
python generate_test_data.py

# Run SQL functionality tests
python tests/test_sql_functionality.py

# Test via curl
curl http://localhost:8000/test_db/users           # Get all users
curl http://localhost:8000/test_db/users/5         # Get user 5
curl http://localhost:8000/test_db/users/5/posts   # Get posts for user 5
```

The test database demonstrates:
- **Table references**: `[[users]]` → `'tables/users.parquet' AS users`
- **Parameter substitution**: `{{user_id}}` → `'5'` (SQL-escaped)
- **Named queries**: Reusable SQL templates
- **Joins**: Cross-table queries with foreign keys
- **Cloud paths**: Can use s3://, gs://, https:// URIs in table definitions

## License

CC-BY-4.0