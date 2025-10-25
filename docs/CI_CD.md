# CI/CD Guide

This guide explains the continuous integration and deployment setup for the LinkedIn MCP Server.

## Overview

The project uses:
- **GitHub Actions** for CI/CD
- **Pre-commit hooks** for local development
- **Make targets** for automation

## GitHub Actions Workflows

### CI Workflow (`.github/workflows/ci.yml`)

Triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main`

#### Jobs

**1. Lint**
- Runs `ruff` linter
- Checks code formatting with `ruff format`

**2. Type Check**
- Runs `mypy` static type checker
- Validates type annotations

**3. Security Check**
- Runs `bandit` security scanner
- Checks for common security issues

**4. Test**
- Tests on Python 3.11 and 3.12
- Tests on Ubuntu and macOS
- Generates coverage reports
- Uploads coverage to Codecov

**5. Build**
- Builds distribution packages
- Validates package with `twine`
- Uploads build artifacts

**6. Docker**
- Builds Docker image
- Caches layers for faster builds

## Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality.

### Installation

```bash
# Install pre-commit
make hooks-install

# Or manually
uv pip install pre-commit
pre-commit install
```

### Hooks Configured

1. **Trailing whitespace** - Removes trailing whitespace
2. **End of file fixer** - Ensures files end with newline
3. **Check YAML** - Validates YAML syntax
4. **Check large files** - Prevents committing files >1MB
5. **Check JSON** - Validates JSON syntax
6. **Check TOML** - Validates TOML syntax
7. **Check merge conflicts** - Detects merge conflict markers
8. **Debug statements** - Detects debug imports
9. **Mixed line endings** - Fixes line endings to LF

10. **Ruff linter** - Fast Python linter with auto-fix
11. **Ruff format** - Fast Python formatter
12. **Black** - Python code formatter
13. **MyPy** - Static type checker
14. **Bandit** - Security vulnerability scanner

### Running Hooks Manually

```bash
# Run on all files
make hooks-run

# Or
pre-commit run --all-files

# Run on specific files
pre-commit run --files src/chuk_mcp_linkedin/server.py
```

### Updating Hooks

```bash
make hooks-update

# Or
pre-commit autoupdate
```

### Skipping Hooks

```bash
# Skip all hooks for a commit
git commit -m "message" --no-verify

# Skip specific hook
SKIP=mypy git commit -m "message"
```

## Local CI Commands

### Full CI Pipeline

```bash
# Run complete CI pipeline locally
make ci
```

This runs:
1. Clean build artifacts
2. Install dependencies
3. Run quality checks (lint, format, typecheck)
4. Run tests
5. Generate coverage report

### Quick CI Check

```bash
# Quick check without coverage
make ci-quick
```

This runs:
1. Quality checks
2. Fast tests (parallel)

### Individual Checks

```bash
# Linting
make lint

# Code formatting
make format

# Type checking
make typecheck

# Security check
make security

# All quality checks
make quality

# Tests with coverage
make coverage
```

## Makefile Targets

### CI/CD Targets

```bash
make ci           # Full CI pipeline
make ci-quick     # Quick CI check
make pre-commit   # Pre-commit checks
```

### Hook Targets

```bash
make hooks-install    # Install pre-commit hooks
make hooks-uninstall  # Uninstall hooks
make hooks-run        # Run hooks on all files
make hooks-update     # Update hook versions
```

### Docker Targets

```bash
make docker-build      # Build Docker image
make docker-test       # Build and test image
make docker-run-stdio  # Run in STDIO mode
make docker-run-http   # Run in HTTP mode
make docker-stop       # Stop containers
make docker-clean      # Clean up Docker resources
```

### Quality Targets

```bash
make lint          # Run linter
make format        # Format code
make typecheck     # Run type checker
make security      # Security checks
make quality       # All quality checks
```

### Test Targets

```bash
make test          # Run all tests
make test-fast     # Run tests in parallel
make coverage      # Generate coverage report
make coverage-html # Open HTML coverage report
```

## Code Quality Standards

### Coverage Requirements

- **Minimum coverage**: 90%
- **Current coverage**: 98%

### Linting

- Uses `ruff` for fast, comprehensive linting
- Configuration in `pyproject.toml`

### Formatting

- Uses `black` with 100-character line length
- Consistent style across all Python files

### Type Checking

- Uses `mypy` with relaxed settings
- Ignores missing imports for third-party libraries

### Security

- Uses `bandit` to detect security issues
- Skips assert checks (B101) for tests

## Troubleshooting

### Pre-commit hooks failing

```bash
# Update hooks
make hooks-update

# Clear cache and reinstall
rm -rf ~/.cache/pre-commit
make hooks-install
```

### CI failing on GitHub

1. Check the workflow run logs
2. Run the same checks locally:
   ```bash
   make ci
   ```
3. Fix issues and push again

### Type checking errors

```bash
# Run mypy locally
make typecheck

# Or with more details
uv run mypy src --show-error-codes --show-traceback
```

### Coverage below threshold

```bash
# Generate detailed coverage report
make coverage-html

# Open in browser to see uncovered lines
open htmlcov/index.html
```

## Best Practices

### Before Committing

1. Run quality checks:
   ```bash
   make quality
   ```

2. Run tests:
   ```bash
   make test
   ```

3. Or run full pre-commit:
   ```bash
   make pre-commit
   ```

### Before Push

```bash
# Run full CI pipeline
make ci
```

### Before Release

```bash
# Run everything
make all
```

## GitHub Actions Secrets

Optional secrets for CI/CD:

- `CODECOV_TOKEN` - For coverage upload (optional)

Configure in: Repository Settings → Secrets and variables → Actions

Note: OAuth integration tests do not require LinkedIn credentials as they use mocked tokens.

## Branch Protection

Recommended branch protection rules for `main`:

- ✅ Require pull request reviews
- ✅ Require status checks to pass
  - lint
  - typecheck
  - security
  - test (Python 3.11, Ubuntu)
- ✅ Require branches to be up to date
- ✅ Require conversation resolution

## Continuous Deployment

### PyPI Publishing

```bash
# Build and publish to TestPyPI
make publish-test

# Build and publish to PyPI
make publish
```

### Docker Registry

```bash
# Tag and push to registry
docker tag chuk-mcp-linkedin:latest your-registry/chuk-mcp-linkedin:latest
docker push your-registry/chuk-mcp-linkedin:latest
```

## Monitoring

### GitHub Actions

- View workflow runs: https://github.com/your-org/chuk-mcp-linkedin/actions
- Download artifacts from build jobs
- Review failed checks

### Codecov

- View coverage reports: https://codecov.io/gh/your-org/chuk-mcp-linkedin
- Track coverage trends over time
- Compare coverage between branches

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Codecov Documentation](https://docs.codecov.com/)
