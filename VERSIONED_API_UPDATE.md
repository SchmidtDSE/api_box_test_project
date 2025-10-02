# Versioned API Update - Object-Based Responses

## Changes Made

Updated versioned_remote API configs to use object-based responses as the primary pattern, while keeping explicit responses as examples.

### Custom Objects Added

Added to `/workspace/api_box_test_project/toy_api_config/objects/test.yaml`:

```yaml
# Test user list (paginated)
test_user_list:
  users: [[object.test.test_user]][3]
  total: 3
  page: 1
  version: str

# Test post list
test_post_list:
  posts: [[object.test.test_post]][5]
  total: 5
  page: 1

# User with posts (composite)
test_user_posts:
  user_id: UNIQUE[int]
  posts: [[object.test.test_post]][2]
  total: 2
```

### Version 1.2 (Latest) - Mix of Core and Custom Objects

**Object-based routes:**
- `/users` → `test.test_user_list` (custom)
- `/users/{{user_id}}` → `core.user` (built-in)
- `/users/{{user_id}}/profile` → `core.user_profile` (built-in)
- `/users/{{user_id}}/posts` → `test.test_user_posts` (custom composite)
- `/posts` → `test.test_post_list` (custom)
- `/posts/{{post_id}}` → `core.post` (built-in)

**Explicit responses (kept as examples):**
- `/health` - Simple status object
- `/api/info` - API metadata

### Version 0.2 (Mid-Version) - Core Objects Only

**Object-based routes:**
- `/users` → `core.user_list`
- `/users/{{user_id}}` → `core.user`
- `/users/{{user_id}}/profile` → `core.user_profile`
- `/posts` → `core.post_list`

**Explicit response:**
- `/health` - Version-specific status

### Version 0.1 (Earliest) - Minimal Feature Set

**Object-based routes:**
- `/users` → `core.user_list`
- `/users/{{user_id}}` → `core.user`

**Explicit response:**
- `/health` - Version indicator

## Code Updates

### response_generator.py

Added support for **both** response types:

1. **Object-based** (string): `"core.user"`, `"test.test_user_list"`
2. **Explicit** (dict/list): Raw YAML data with `{{param}}` substitution

```python
def generate_response(response_type: Union[str, Dict, list], params: Dict[str, str], path: str):
    # Handle explicit response (dict or list)
    if isinstance(response_type, (dict, list)):
        return _substitute_params(response_type, params)

    # Handle object-based response (string reference)
    if isinstance(response_type, str):
        return dummy_data_generator.generate_object(...)
```

### _substitute_params()

New function to handle `{{param}}` substitution in explicit responses:

```python
def _substitute_params(response_data: Union[Dict, list], params: Dict[str, str]):
    """Replace {{param}} placeholders with actual URL parameter values."""
    json_str = json.dumps(response_data)
    for key, value in params.items():
        json_str = re.sub(r'\{\{' + key + r'\}\}', str(value), json_str)
    return json.loads(json_str)
```

## Benefits

### Object-Based (Recommended)
- ✅ Reusable across APIs and databases
- ✅ Consistent data structure
- ✅ Easy to maintain and update
- ✅ Supports complex types (lists, composites)
- ✅ Can reference other objects

### Explicit (Use Sparingly)
- ✅ Simple, direct responses
- ✅ Good for version-specific data
- ✅ Useful for minimal endpoints
- ✅ No object definition needed

## Example Usage

### Object-Based Response
```yaml
- route: "/users"
  methods: ["GET"]
  response: "test.test_user_list"  # References object definition
```

### Explicit Response
```yaml
- route: "/health"
  methods: ["GET"]
  response:              # Inline data
    status: ok
    version: "1.2"
```

### Mixed (Best Practice)
```yaml
routes:
  # Object-based for data endpoints
  - route: "/users"
    response: "core.user_list"

  - route: "/users/{{user_id}}"
    response: "core.user"

  # Explicit for simple status/metadata
  - route: "/health"
    response:
      status: ok
      version: "1.0"
```

## Testing

To test the versioned APIs:

```bash
# Start the versioned remote APIs
cd /workspace/api_box_test_project
pixi run toy_api start --all versioned_remote

# Test different versions
curl http://localhost:5200/health    # v0.1
curl http://localhost:5200/users

curl http://localhost:5250/health    # v0.2
curl http://localhost:5250/users
curl http://localhost:5250/posts

curl http://localhost:5300/health    # v1.2 (latest)
curl http://localhost:5300/users
curl http://localhost:5300/posts
curl http://localhost:5300/api/info
```
