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
pixi run api-box
```

### Terminal 3 - Run Integration Tests

```bash
# Run comprehensive route restriction tests
python test_api_box_with_toy_api.py
```

or run manual tests:

```bash
# Working Endpoints
curl http://localhost:8000/basic_remote/latest/users/123/profile  
curl http://localhost:8000/allowed_routes_remote/latest/users

# Blocked Endpoints
curl http://localhost:8000/basic_remote/latest/users/123/delete
curl http://localhost:8000/restricted_remote/latest/admin/dashboard
curl http://localhost:8000/allowed_routes_remote/latest/users/123/settings  
```

## What This Project Tests

This project provides a comprehensive testing environment for **API Box route restrictions** functionality. It demonstrates:

- **Global route restrictions** - patterns blocked across all remotes
- **Remote-specific restrictions** - additional restrictions for specific APIs
- **Allowed routes (whitelisting)** - only specific patterns allowed
- **Custom route mapping** - mapping between different API endpoint structures

## Project Components

### API Box Configuration (`api_box_config/`)
- `config.yaml` - Main API Box configuration with global restrictions
- `remotes/` - Individual remote configurations:
  - `basic_remote.yaml` - Basic API (port 4321) with minimal restrictions
  - `custom_mapping_remote.yaml` - Custom route mapping API (port 1234)
  - `restricted_remote.yaml` - Heavily restricted API (port 8080)
  - `allowed_routes_remote.yaml` - Whitelist-only API (port 9090)

### Toy API Configuration (`toy_api_config/`)
Matching configurations that define the actual routes for each toy API server:
- `basic.yaml` - Basic routes for testing
- `custom_mapping.yaml` - Custom endpoint structure
- `restricted.yaml` - Routes that will be restricted by API Box
- `allowed_routes.yaml` - Mix of allowed and blocked routes

### Integration Tests
- `test_api_box_with_toy_api.py` - Comprehensive test suite with 15+ test cases
- `test_route_restrictions.py` - Direct API Box config testing
- `ROUTE_RESTRICTIONS_TEST.md` - Testing documentation

## Dependencies

- **[API Box](https://github.com/SchmidtDSE/api_box)** - The API gateway being tested
- **[Toy API](https://github.com/brookisme/toy_api)** - Configurable test API servers
- **Python 3.8+** with PyYAML for config parsing

## Project Structure

```
api_box_test_project/
├── api_box_config/              # API Box configurations
│   ├── config.yaml              # Main config with global restrictions
│   └── remotes/                 # Remote-specific configurations
│       ├── basic_remote.yaml
│       ├── custom_mapping_remote.yaml
│       ├── restricted_remote.yaml
│       └── allowed_routes_remote.yaml
├── toy_api_config/              # Toy API configurations
│   ├── basic.yaml
│   ├── custom_mapping.yaml
│   ├── restricted.yaml
│   └── allowed_routes.yaml
├── test_api_box_with_toy_api.py # Integration test suite
├── test_route_restrictions.py   # Config-only tests
└── README.md                    # This file
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

## License

CC-BY-4.0