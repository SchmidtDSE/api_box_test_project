# API Box Test Project

Integration testing environment for [API Box](https://github.com/SchmidtDSE/api_box) route restrictions using configurable [Toy API](https://github.com/brookisme/toy_api) servers.

## Quick Start Commands

Copy and paste these commands to get the full test environment running:

```bash
# generate databases (see: toy_api_config/[config.py, databases/*.yaml])
# - creates/outputs-files-to: CWD/tables/ folder
pixi run toy_api database/versioned_db
pixi run toy_api database/test_db

# start up remote-apis (see: toy_api_config/[config.py, remotes/*.yaml])
pixi run toy_api start --all

# start up api-box (see: api_box_config/)
pixi run api-box start
```

### ENDPOINT TESTS

```bash
# ========================================
# Basic Remote API - Working
# ========================================
# Basic user routes (inherits global restrictions only)
curl http://localhost:8000/basic_remote/users
curl http://localhost:8000/basic_remote/users/1005
curl http://localhost:8000/basic_remote/users/1005/profile
curl http://localhost:8000/basic_remote/users/1005/permissions
curl http://localhost:8000/basic_remote/health

# ========================================
# Versioned Remote API - Working
# ========================================
# Specific version (1.2)
curl http://localhost:8000/versioned_remote/1.2/users
curl http://localhost:8000/versioned_remote/1.2/users/1005
curl http://localhost:8000/versioned_remote/1.2/users/1005/profile
curl http://localhost:8000/versioned_remote/1.2/users/1005/posts
curl http://localhost:8000/versioned_remote/1.2/health

# Latest version (resolves to 1.2)
curl http://localhost:8000/versioned_remote/latest/users
curl http://localhost:8000/versioned_remote/latest/users/1005
curl http://localhost:8000/versioned_remote/latest/health

# ========================================
# Allowed Routes Remote API - Working (Whitelist)
# ========================================
# Only explicitly allowed routes work
curl http://localhost:8000/allowed_routes_remote/users
curl http://localhost:8000/allowed_routes_remote/users/1005
curl http://localhost:8000/allowed_routes_remote/users/1005/profile
curl http://localhost:8000/allowed_routes_remote/users/1005/posts
curl http://localhost:8000/allowed_routes_remote/posts
curl http://localhost:8000/allowed_routes_remote/health

# ========================================
# Remote API Endpoints - Blocked
# ========================================
# Basic remote - globally restricted
curl http://localhost:8000/basic_remote/users/1005/delete
curl http://localhost:8000/basic_remote/admin/5/dangerous

# Restricted remote - remote-specific restrictions
curl http://localhost:8000/restricted_remote/users/1005/permissions
curl http://localhost:8000/restricted_remote/admin/dashboard
curl http://localhost:8000/restricted_remote/system/123/config
curl http://localhost:8000/restricted_remote/users/1005/private

# Allowed routes remote - not in whitelist
curl http://localhost:8000/allowed_routes_remote/users/1005/settings
curl http://localhost:8000/allowed_routes_remote/admin

# ========================================
# SQL Database Endpoints - test_db
# ========================================
# User queries
curl http://localhost:8000/test_db/users
curl http://localhost:8000/test_db/users/1005
curl http://localhost:8000/test_db/users/1005/permissions
curl http://localhost:8000/test_db/users/1005/posts
curl http://localhost:8000/test_db/users/active

# Post queries
curl http://localhost:8000/test_db/posts
curl http://localhost:8000/test_db/posts/10

# ========================================
# SQL Database Endpoints - versioned_db
# ========================================
# Specific version (1.2)
curl http://localhost:8000/versioned_db/1.2/users
curl http://localhost:8000/versioned_db/1.2/users/1005
curl http://localhost:8000/versioned_db/1.2/users/1005/permissions
curl http://localhost:8000/versioned_db/1.2/users/1005/posts
curl http://localhost:8000/versioned_db/1.2/posts

# Latest version (resolves to 1.2)
curl http://localhost:8000/versioned_db/latest/users
curl http://localhost:8000/versioned_db/latest/users/1005
curl http://localhost:8000/versioned_db/latest/users/1005/permissions
```

## License

CC-BY-4.0