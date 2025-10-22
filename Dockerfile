# LinkedIn MCP Server Dockerfile
# ================================
# Multi-stage build for optimal image size
# Based on chuk-mcp-server patterns

# Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy project configuration
COPY pyproject.toml README.md ./
COPY src ./src

# Install the package with all dependencies
# Use --no-cache to reduce layer size
RUN uv pip install --system --no-cache -e ".[http]"

# Runtime stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app/src ./src
COPY --from=builder /app/README.md ./
COPY --from=builder /app/pyproject.toml ./

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    mkdir -p /app/.linkedin_drafts && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    MCP_SERVER_MODE=stdio

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '/app/src'); import chuk_mcp_linkedin; print('OK')" || exit 1

# Default command - run MCP server in stdio mode via CLI
CMD ["linkedin-mcp", "stdio"]

# Alternative commands:
# CMD ["linkedin-mcp", "http", "--host", "0.0.0.0", "--port", "8000"]  # HTTP mode
# CMD ["linkedin-mcp", "auto"]                                          # Auto-detect mode

# Expose port for HTTP mode (optional)
EXPOSE 8000

# Labels for metadata
LABEL maintainer="chris@chuk.ai" \
      description="LinkedIn MCP Server - Model Context Protocol server for LinkedIn content creation" \
      version="1.0.0" \
      org.opencontainers.image.source="https://github.com/chrishayuk/chuk-mcp-linkedin" \
      org.opencontainers.image.title="LinkedIn MCP Server" \
      org.opencontainers.image.description="Design system MCP server for creating LinkedIn posts" \
      org.opencontainers.image.authors="Christopher Hay <chris@chuk.ai>"
