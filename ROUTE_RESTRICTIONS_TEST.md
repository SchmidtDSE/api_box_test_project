# Route Restrictions Test Documentation

This test_project demonstrates and tests the route restrictions and allowed routes functionality in API Box.

## Test Configuration Overview

### Main Config (`config/config.yaml`)
- **Global Restrictions**:
  - `users/{{}}/delete` - Blocks delete operations on all remotes
  - `admin/{{}}/dangerous` - Blocks dangerous admin operations on all remotes

### Remote Configurations

#### 1. `remote_4321` - Basic Remote (port 4321)
- **Restrictions**: Inherits only global restrictions
- **Description**: Baseline remote for testing global restrictions

#### 2. `another_name` - Custom Route Mapping Remote (port 1234)
- **Custom Route Mappings**:
  - `users/{user_id}/permissions` → `user-permissions/{user_id}`
  - `users/{user_id}` → `users/{user_id}`
  - `users/{user_id}/profile` → `profiles/{user_id}`
- **Additional Restrictions**: `users/{{}}/settings`
- **Description**: Tests custom route mapping with restrictions

#### 3. `restricted_remote` - Heavily Restricted Remote (port 8080)
- **Additional Restrictions**:
  - `users/{{}}/permissions` - No access to user permissions
  - `admin` - No admin access at all
  - `admin/{{}}` - No admin subroutes
  - `system/{{}}/config` - No system configuration access
  - `users/{{}}/private` - No private user data access
- **Description**: Security-focused remote with extensive restrictions

#### 4. `allowed_routes_remote` - Whitelist Remote (port 9090)
- **Allowed Routes Only** (whitelist approach):
  - `users` - List users
  - `users/{{}}` - Get specific user
  - `users/{{}}/profile` - User profiles
  - `users/{{}}/posts` - User posts
  - `posts` - List posts
  - `posts/{{}}` - Get specific post
  - `health` - Health check
- **Description**: Demonstrates explicit allowed routes (everything else is blocked)

## Test Scenarios

### 1. Global Restrictions
- Tests that global restrictions apply to all remotes
- Verifies that `users/{{}}/delete` and `admin/{{}}/dangerous` are blocked everywhere

### 2. Remote-Specific Restrictions
- Tests that remotes can have additional restrictions beyond global ones
- Verifies that `restricted_remote` blocks more routes than others
- Confirms that `another_name` blocks `users/{{}}/settings`

### 3. Allowed Routes Whitelist
- Tests that `allowed_routes_remote` only allows explicitly listed routes
- Verifies that even normally allowed routes are blocked if not in the whitelist

### 4. Custom Route Mapping with Restrictions
- Tests that custom route mappings work with route restrictions
- Verifies that restrictions are checked on the incoming pattern (before mapping)

### 5. Precedence Rules
- Tests that remote-specific settings override global settings
- Verifies that global restrictions still apply even with local overrides

## Running the Tests

```bash
cd test_project
python test_route_restrictions.py
```

## Expected Behavior

The test suite validates that:

1. **Pattern Matching**: Routes are correctly matched using `{{}}` wildcard syntax
2. **Global Enforcement**: Global restrictions apply to all remotes unless overridden
3. **Remote Specificity**: Each remote can have its own additional restrictions or allowed routes
4. **Whitelist Precedence**: When allowed routes are specified, only those routes work
5. **Mapping Compatibility**: Custom route mappings work correctly with restrictions
6. **Security**: Restrictions provide effective access control for API endpoints

## Configuration Syntax

### Restricting Routes (Blacklist)
```yaml
restricted:
  - users/{{}}/delete
  - admin/{{}}
  - specific/exact/path
```

### Specifying Allowed Routes (Whitelist)
```yaml
routes:
  - users
  - users/{{}}
  - users/{{}}/profile
```

### Custom Route Mapping with Restrictions
```yaml
routes:
  - route: "{{route_name}}/users/{user_id}/permissions"
    remote_route: "user-permissions/{{user_id}}"
    method: "GET"
restricted:
  - users/{{}}/settings
```

The `{{}}` syntax acts as a wildcard that matches any path segment.