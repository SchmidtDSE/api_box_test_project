# Test Project

Configuration project for testing API Box functionality with multiple remote API configurations.

## Description

This project contains configuration files for testing API Box's ability to proxy requests to multiple remote APIs. It includes a main configuration file and several remote API configuration files to demonstrate different routing and access control scenarios.

## Project Structure

```
test_project/
├── config/
│   ├── config.yaml          # Main API Box configuration
│   └── remotes/
│       ├── remote_1234.yaml # Remote API configuration example 1
│       └── remote_4321.yaml # Remote API configuration example 2
├── pixi.lock                # Pixi dependency lockfile
└── pyproject.toml          # Project configuration and dependencies
```

## Configuration Files

### Main Config (`config/config.yaml`)
Contains the primary API Box configuration including:
- Project metadata (name, description, authors)
- List of remote APIs to proxy
- Global routing and access control rules

### Remote Configs (`config/remotes/*.yaml`)
Individual configuration files for each remote API, containing:
- Remote API connection details (URL, authentication)
- API-specific routing rules
- Access control restrictions

## Quick Start

### Prerequisites

Requirements are managed through a [Pixi](https://pixi.sh/latest) project environment:

```bash
# Install dependencies
pixi install
```

### Usage with API Box

This configuration project is designed to be used with API Box:

1. **Start the remote APIs** (if using Toy API):
   ```bash
   cd ../toy_api
   pixi run toy-api --port 1234
   pixi run toy-api --port 4321
   ```

2. **Start API Box with this configuration**:
   ```bash
   cd ../api_box
   pixi run api-box --config ../test_project/config/config.yaml
   ```

3. **Test the proxy functionality**:
   ```bash
   # Access remote APIs through API Box
   curl http://localhost:8000/remote_1234/latest/users/
   curl http://localhost:8000/remote_4321/latest/users/
   ```

## Configuration Examples

### Main Configuration Structure
```yaml
name: "Test Project"
description: "Configuration for testing API Box"
authors: ["Developer"]
remotes:
  - "remote_1234"
  - "remote_4321"
```

### Remote Configuration Structure
```yaml
name: "remote_1234"
url: "http://localhost:1234"
description: "Test remote API on port 1234"
```

## Development

This configuration project demonstrates:
- Multi-remote API setup
- Configuration file organization
- API Box routing capabilities
- Access control testing scenarios

Use this project as a reference for setting up your own API Box configurations.

## License

CC-BY-4.0