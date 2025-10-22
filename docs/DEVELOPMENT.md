# Development Guide

Complete guide for developing the LinkedIn MCP Server.

## Quick Start

```bash
# Install dependencies
make install
make dev

# Install pre-commit hooks
make hooks-install

# Run tests
make test

# Run all checks
make check
```

## Project Structure

```
chuk-mcp-linkedin/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── docs/                       # Documentation
│   ├── CI_CD.md               # CI/CD guide
│   ├── DOCKER.md              # Docker guide
│   └── DEVELOPMENT.md         # This file
├── src/chuk_mcp_linkedin/     # Source code
│   ├── api/                   # LinkedIn API client
│   ├── models/                # Data models
│   ├── posts/                 # Post composition
│   ├── preview/               # Preview generation
│   ├── themes/                # Theme system
│   ├── tokens/                # Design tokens
│   ├── tools/                 # MCP tools
│   └── utils/                 # Utilities
├── tests/                     # Test suite
├── .pre-commit-config.yaml    # Pre-commit hooks
├── docker-compose.yml         # Docker Compose
├── Dockerfile                 # Docker image
├── Makefile                   # Development automation
└── pyproject.toml            # Project configuration
```

## Development Workflow

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/your-org/chuk-mcp-linkedin.git
cd chuk-mcp-linkedin

# Install dependencies
make install
make dev

# Install pre-commit hooks
make hooks-install
```

### 2. Make Changes

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make your changes
# ...

# Run quality checks
make quality

# Run tests
make test
```

### 3. Commit Changes

Pre-commit hooks run automatically:

```bash
git add .
git commit -m "Add my feature"
```

If hooks fail:
```bash
# Fix issues
make format
make lint

# Commit again
git commit -m "Add my feature"
```

### 4. Push and Create PR

```bash
git push origin feature/my-feature
```

Then create a pull request on GitHub.

## Development Commands

### Installation

```bash
make install      # Install dependencies
make dev          # Install dev dependencies
```

### Testing

```bash
make test         # Run all tests
make test-fast    # Run tests in parallel
make coverage     # Generate coverage report
make coverage-html # Open HTML coverage report
```

### Code Quality

```bash
make lint         # Run linter
make format       # Format code
make typecheck    # Run type checker
make security     # Security checks
make quality      # All quality checks
```

### Pre-commit Hooks

```bash
make hooks-install    # Install hooks
make hooks-run        # Run hooks manually
make hooks-update     # Update hook versions
make hooks-uninstall  # Uninstall hooks
```

### CI/CD

```bash
make ci           # Full CI pipeline
make ci-quick     # Quick CI check
make check        # All checks (quality + tests + coverage)
```

### Docker

```bash
make docker-build      # Build Docker image
make docker-test       # Build and test image
make docker-run-stdio  # Run in STDIO mode
make docker-run-http   # Run in HTTP mode
make docker-stop       # Stop containers
make docker-clean      # Clean up Docker resources
```

### Shortcuts

```bash
make t            # test
make c            # coverage
make f            # format
make l            # lint
make q            # quality
make ch           # check
```

## Code Style

### Python Version

- Python 3.11+ required
- Target: Python 3.11 and 3.12

### Formatting

- **Black** with 100-character line length
- **Ruff** for import sorting and linting

```bash
# Format code
make format
```

### Linting

- **Ruff** for comprehensive linting
- Configuration in `pyproject.toml`

```bash
# Run linter
make lint
```

### Type Checking

- **MyPy** with relaxed settings
- Ignore missing imports for third-party packages

```bash
# Run type checker
make typecheck
```

### Security

- **Bandit** for security vulnerability scanning
- Skips assert checks for test files

```bash
# Run security check
make security
```

## Testing

### Running Tests

```bash
# All tests
make test

# Fast (parallel)
make test-fast

# Specific test file
uv run pytest tests/test_composition.py

# With verbose output
uv run pytest tests/ -v

# With coverage
make coverage
```

### Writing Tests

Tests use `pytest` and follow this structure:

```python
"""Tests for my module."""

import pytest
from chuk_mcp_linkedin.my_module import MyClass


class TestMyClass:
    """Test MyClass functionality"""

    def test_basic_functionality(self):
        """Test basic use case"""
        obj = MyClass()
        assert obj.method() == expected_result

    @pytest.mark.asyncio
    async def test_async_method(self):
        """Test async method"""
        obj = MyClass()
        result = await obj.async_method()
        assert result is not None
```

### Coverage Requirements

- Minimum: 90%
- Target: 95%+
- Current: 98%

## Architecture

### Component System

The project uses a component-based architecture inspired by shadcn/ui:

```python
from chuk_mcp_linkedin.posts import ComposablePost

# Create post
post = ComposablePost("text", theme="thought_leader")

# Add components
post.add_hook("question", "What drives innovation?")
post.add_body("Innovation comes from...", structure="linear")
post.add_cta("direct", "Share your thoughts!")

# Compose final post
final_text = post.compose()
```

### Design Tokens

Three token systems provide consistent styling:

1. **Text Tokens** - Typography, formatting
2. **Engagement Tokens** - Emojis, symbols
3. **Structure Tokens** - Layout, spacing

### Theme System

10 pre-built themes for different content styles:

- Thought Leader
- Data Driven
- Storyteller
- Educator
- Provocateur
- Professional
- Casual
- Minimalist
- Expressive
- Authentic

## Common Tasks

### Add a New Component

1. Create component class in `src/chuk_mcp_linkedin/posts/components/`
2. Inherit from `PostComponent`
3. Implement `render()` and `validate()` methods
4. Add to `ComposablePost` as `add_*()` method
5. Create tool in `src/chuk_mcp_linkedin/tools/composition_tools.py`
6. Write tests

### Add a New Theme

1. Create theme configuration in `src/chuk_mcp_linkedin/themes/`
2. Extend `ThemeConfig` dataclass
3. Register in `ThemeManager`
4. Write tests

### Add a New Tool

1. Add function to appropriate tools file
2. Use `@mcp.tool` decorator
3. Add comprehensive docstring
4. Write tests
5. Update tool registry

## Debugging

### Debug Mode

```bash
# Run server with debug logging
make debug

# Or manually
DEBUG=1 python -m chuk_mcp_linkedin.server
```

### Interactive Debugging

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use built-in
breakpoint()
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

## Troubleshooting

### Tests Failing

```bash
# Run with verbose output
uv run pytest -vv

# Run specific failing test
uv run pytest tests/test_file.py::TestClass::test_method -vv

# Show stdout/stderr
uv run pytest -s
```

### Import Errors

```bash
# Reinstall in editable mode
make clean
make install
```

### Type Errors

```bash
# Run with detailed output
uv run mypy src --show-error-codes --show-traceback
```

### Coverage Below Threshold

```bash
# See detailed coverage report
make coverage-html
open htmlcov/index.html
```

## Best Practices

### Commits

- Use conventional commit messages
- Keep commits atomic and focused
- Run `make check` before committing

### Pull Requests

- Create focused PRs (one feature/fix)
- Write clear descriptions
- Link related issues
- Ensure CI passes

### Code Review

- Review for correctness
- Check test coverage
- Verify documentation
- Test manually if needed

## Resources

- [CI/CD Guide](./CI_CD.md)
- [Docker Guide](./DOCKER.md)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Project README](../README.md)

## Getting Help

- Check existing [issues](https://github.com/your-org/chuk-mcp-linkedin/issues)
- Review [documentation](./docs/)
- Ask in discussions
- Contact maintainers
