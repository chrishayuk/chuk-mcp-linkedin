# Docker Guide

This guide explains how to use Docker with the LinkedIn MCP Server.

## CLI Commands

The LinkedIn MCP Server provides a comprehensive CLI for running in different modes:

```bash
# Run in STDIO mode (for Claude Desktop)
linkedin-mcp stdio

# Run in HTTP mode (API server)
linkedin-mcp http --host 0.0.0.0 --port 8000

# Auto-detect best transport mode
linkedin-mcp auto

# Run with debug logging
linkedin-mcp stdio --debug

# Get help
linkedin-mcp --help
```

### Available Modes

- **stdio**: Standard I/O mode for Claude Desktop integration
- **http**: HTTP API server mode (requires `uvicorn` and `starlette`)
- **auto**: Automatically detect and use the best transport mode

## Quick Start

### Build the Docker Image

```bash
make docker-build
```

or

```bash
docker build -t chuk-mcp-linkedin:latest .
```

### Run the Container

**STDIO Mode (default):**
```bash
make docker-run-stdio
```

**HTTP Mode:**
```bash
make docker-run-http
```

**Development Mode:**
```bash
make docker-run-dev
```

## Docker Compose Profiles

The `docker-compose.yml` file defines three profiles:

### 1. STDIO Profile (Default MCP Mode)
```bash
docker-compose --profile stdio up -d
```

This runs the server in standard I/O mode for integration with Claude Desktop or other MCP clients.

### 2. HTTP Profile (API Mode)
```bash
docker-compose --profile http up -d
```

This runs the server in HTTP mode, exposing an API on port 8000.

Access the server at: http://localhost:8000

### 3. Development Profile
```bash
docker-compose --profile dev up -d
```

This mounts the source code directory for live development.

## Environment Variables

Create a `.env` file in the project root:

```env
# Required - LinkedIn OAuth credentials
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here

# Required for Development - Session storage
SESSION_PROVIDER=memory

# Optional - Server configuration
MCP_SERVER_MODE=stdio
DEBUG=0
```

## Volume Mounts

The Docker containers mount two directories:

1. **`.env` file**: Read-only mount for credentials
2. **`.linkedin_drafts/`**: Persistent storage for drafts

## Docker Commands

### Build Commands
```bash
# Build production image
make docker-build

# Build development image
make docker-build-dev
```

### Run Commands
```bash
# Run in STDIO mode
make docker-run-stdio

# Run in HTTP mode
make docker-run-http

# Run in development mode
make docker-run-dev
```

### Management Commands
```bash
# View logs
make docker-logs

# Stop containers
make docker-stop

# Open shell in container
make docker-shell

# Clean up everything
make docker-clean

# Build and test
make docker-test
```

## Multi-Stage Build

The Dockerfile uses a multi-stage build for optimal image size:

1. **Builder Stage**: Installs all dependencies and builds the package
2. **Runtime Stage**: Contains only what's needed to run the server

This reduces the final image size significantly.

## Security Features

- Runs as non-root user (`mcpuser`)
- Minimal runtime dependencies
- No build tools in final image
- Health check configured

## Health Check

The container includes a health check that verifies the package can be imported:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import chuk_mcp_linkedin; print('OK')" || exit 1
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Or
make docker-logs
```

### Permission issues
Ensure the `.linkedin_drafts/` directory is writable:
```bash
chmod 755 .linkedin_drafts
```

### Port already in use (HTTP mode)
Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

## Advanced Usage

### Custom Dockerfile Build

```bash
docker build \
  --build-arg PYTHON_VERSION=3.12 \
  -t chuk-mcp-linkedin:custom \
  .
```

### Run with Custom Command

```bash
docker run -it --rm \
  -v $(pwd)/.env:/app/.env:ro \
  -v $(pwd)/.linkedin_drafts:/app/.linkedin_drafts \
  chuk-mcp-linkedin:latest \
  python -m chuk_mcp_linkedin.async_server --port 8000
```

### Network Configuration

All containers use the `mcp-network` network for inter-container communication.

```bash
docker network inspect mcp-network
```

## Production Deployment

### Using Docker Compose

```bash
# Production mode with resource limits
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Using Kubernetes

See `k8s/` directory for Kubernetes manifests (coming soon).

### Using Docker Swarm

```bash
docker stack deploy -c docker-compose.yml linkedin-mcp
```

## Maintenance

### Update Image

```bash
# Pull latest changes
git pull

# Rebuild image
make docker-build

# Restart containers
docker-compose down
docker-compose --profile stdio up -d
```

### Backup Drafts

```bash
# The drafts are stored in .linkedin_drafts/
tar -czf linkedin-drafts-backup.tar.gz .linkedin_drafts/
```

## Resources

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
