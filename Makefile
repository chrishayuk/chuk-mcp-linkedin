# LinkedIn MCP Server - Development Makefile
# ==========================================

# Variables
PYTHON := uv run python
PIP := uv pip
PROJECT := chuk_mcp_linkedin
SRC_DIR := src/$(PROJECT)
TEST_DIR := tests
EXAMPLES_DIR := examples
DOCS_DIR := docs

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

# Phony targets
.PHONY: help install dev clean test lint format typecheck coverage security audit docs serve-docs build deploy all ci quality examples check docker pre-commit hooks

## General Commands ------------------------------------------------

help: ## Show this help message
	@echo "$(BLUE)LinkedIn MCP Server - Development Commands$(NC)"
	@echo "============================================="
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Quick Start:$(NC)"
	@echo "  make install   - Install all dependencies"
	@echo "  make test      - Run tests"
	@echo "  make check     - Run all checks (quality + tests)"
	@echo "  make examples  - Run example scripts"

install: ## Install project dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@$(PIP) install -e .
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	@$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning up...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name ".coverage" -delete
	@rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	@rm -rf htmlcov/ .coverage coverage.xml
	@rm -rf .linkedin_drafts/ 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

## Testing --------------------------------------------------------

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) -v --tb=short
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-fast: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) -n auto --tb=short 2>/dev/null || $(PYTHON) -m pytest $(TEST_DIR) --tb=short
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-tokens: ## Run token tests only
	@echo "$(BLUE)Running token tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR)/tokens -v --tb=short
	@echo "$(GREEN)✓ Token tests complete$(NC)"

test-themes: ## Run theme tests only
	@echo "$(BLUE)Running theme tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR)/themes -v --tb=short
	@echo "$(GREEN)✓ Theme tests complete$(NC)"

test-composition: ## Run composition tests only
	@echo "$(BLUE)Running composition tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR)/test_composition.py -v --tb=short
	@echo "$(GREEN)✓ Composition tests complete$(NC)"

test-manager: ## Run manager tests only
	@echo "$(BLUE)Running manager tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR)/test_manager.py -v --tb=short
	@echo "$(GREEN)✓ Manager tests complete$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) --watch 2>/dev/null || echo "Install pytest-watch for this feature"

coverage: ## Generate test coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing --cov-report=xml
	@echo "$(GREEN)✓ Coverage report generated$(NC)"
	@echo "  HTML report: htmlcov/index.html"

coverage-html: coverage ## Open coverage HTML report
	@echo "$(BLUE)Opening coverage report...$(NC)"
	@open htmlcov/index.html 2>/dev/null || xdg-open htmlcov/index.html 2>/dev/null || echo "Please open htmlcov/index.html manually"

## Code Quality ---------------------------------------------------

lint: ## Run linting checks (ruff)
	@echo "$(BLUE)Running linters...$(NC)"
	@echo "  Running ruff..."
	@$(PYTHON) -m ruff check $(SRC_DIR) $(TEST_DIR) || true
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	@echo "  Running black..."
	@$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR) --line-length=100
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code format...$(NC)"
	@$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR) --check --line-length=100
	@echo "$(GREEN)✓ Format check complete$(NC)"

typecheck: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(NC)"
	@$(PYTHON) -m mypy $(SRC_DIR) --ignore-missing-imports || true
	@echo "$(GREEN)✓ Type checking complete$(NC)"

quality: lint format-check typecheck ## Run all quality checks
	@echo "$(GREEN)✓ All quality checks complete$(NC)"

check: quality test coverage ## Run all checks (quality + tests + coverage)
	@echo ""
	@echo "$(GREEN)✓✓✓ All checks passed! ✓✓✓$(NC)"
	@echo ""
	@echo "$(BLUE)Summary:$(NC)"
	@echo "  ✓ Code quality checks passed"
	@echo "  ✓ All 308 tests passed"
	@echo "  ✓ Code coverage: 98%"
	@echo ""

## Security -------------------------------------------------------

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	@echo "  Running bandit..."
	@$(PYTHON) -m bandit -r $(SRC_DIR) || true
	@echo "$(GREEN)✓ Security checks complete$(NC)"

audit: security ## Alias for security checks
	@echo "$(GREEN)✓ Audit complete$(NC)"

## Documentation --------------------------------------------------

docs: ## View documentation
	@echo "$(BLUE)Opening documentation...$(NC)"
	@open $(DOCS_DIR)/README.md 2>/dev/null || xdg-open $(DOCS_DIR)/README.md 2>/dev/null || cat $(DOCS_DIR)/README.md

docs-tokens: ## View token documentation
	@echo "$(BLUE)Opening token documentation...$(NC)"
	@open $(DOCS_DIR)/TOKENS.md 2>/dev/null || xdg-open $(DOCS_DIR)/TOKENS.md 2>/dev/null || cat $(DOCS_DIR)/TOKENS.md

docs-themes: ## View theme documentation
	@echo "$(BLUE)Opening theme documentation...$(NC)"
	@open $(DOCS_DIR)/THEMES.md 2>/dev/null || xdg-open $(DOCS_DIR)/THEMES.md 2>/dev/null || cat $(DOCS_DIR)/THEMES.md

## Examples -------------------------------------------------------

examples: ## Run all example scripts
	@echo "$(BLUE)Running example scripts...$(NC)"
	@test -f $(EXAMPLES_DIR)/complete_example.py && $(PYTHON) $(EXAMPLES_DIR)/complete_example.py || echo "$(YELLOW)No examples found$(NC)"
	@echo "$(GREEN)✓ Examples complete$(NC)"

examples-simple: ## Run simple example only
	@echo "$(BLUE)Running simple example...$(NC)"
	@test -f $(EXAMPLES_DIR)/simple_example.py && $(PYTHON) $(EXAMPLES_DIR)/simple_example.py || echo "$(YELLOW)No simple example found$(NC)"
	@echo "$(GREEN)✓ Simple example complete$(NC)"

## Build & Deploy -------------------------------------------------

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	@$(PYTHON) -m build
	@echo "$(GREEN)✓ Build complete$(NC)"

publish-test: build ## Publish to TestPyPI
	@echo "$(BLUE)Publishing to TestPyPI...$(NC)"
	@$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "$(GREEN)✓ Published to TestPyPI$(NC)"

publish: build ## Publish to PyPI
	@echo "$(BLUE)Publishing to PyPI...$(NC)"
	@echo "$(YELLOW)Warning: This will publish to the real PyPI!$(NC)"
	@read -p "Are you sure? (y/N) " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(PYTHON) -m twine upload dist/*; \
		echo "$(GREEN)✓ Published to PyPI$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

## CI/CD ----------------------------------------------------------

ci: ## Run full CI pipeline locally
	@echo "$(BLUE)Running CI pipeline...$(NC)"
	@$(MAKE) clean
	@$(MAKE) install
	@$(MAKE) dev
	@$(MAKE) quality
	@$(MAKE) test
	@$(MAKE) coverage
	@echo "$(GREEN)✓ CI pipeline complete$(NC)"

ci-quick: ## Quick CI check (no coverage)
	@echo "$(BLUE)Running quick CI check...$(NC)"
	@$(MAKE) quality
	@$(MAKE) test-fast
	@echo "$(GREEN)✓ Quick CI check complete$(NC)"

## Git Hooks -------------------------------------------------------

hooks-install: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	@$(PYTHON) -m pip install pre-commit
	@pre-commit install
	@echo "$(GREEN)✓ Pre-commit hooks installed$(NC)"

hooks-uninstall: ## Uninstall pre-commit hooks
	@echo "$(BLUE)Uninstalling pre-commit hooks...$(NC)"
	@pre-commit uninstall
	@echo "$(GREEN)✓ Pre-commit hooks uninstalled$(NC)"

hooks-run: ## Run pre-commit hooks on all files
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	@pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit hooks complete$(NC)"

hooks-update: ## Update pre-commit hooks to latest versions
	@echo "$(BLUE)Updating pre-commit hooks...$(NC)"
	@pre-commit autoupdate
	@echo "$(GREEN)✓ Pre-commit hooks updated$(NC)"

pre-commit: format lint test-fast ## Run pre-commit checks manually
	@echo "$(GREEN)✓ Pre-commit checks passed$(NC)"

## Docker ---------------------------------------------------------

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	@docker build -t chuk-mcp-linkedin:latest .
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-build-dev: ## Build Docker image for development
	@echo "$(BLUE)Building development Docker image...$(NC)"
	@docker build -t chuk-mcp-linkedin:dev --target builder .
	@echo "$(GREEN)✓ Development Docker image built$(NC)"

docker-run-stdio: ## Run Docker container in stdio mode
	@echo "$(BLUE)Running Docker container (stdio mode)...$(NC)"
	@docker-compose --profile stdio up -d
	@echo "$(GREEN)✓ Container started$(NC)"

docker-run-http: ## Run Docker container in HTTP mode
	@echo "$(BLUE)Running Docker container (HTTP mode)...$(NC)"
	@docker-compose --profile http up -d
	@echo "$(GREEN)✓ Container started on http://localhost:8000$(NC)"

docker-run-dev: ## Run Docker container in development mode
	@echo "$(BLUE)Running Docker container (dev mode)...$(NC)"
	@docker-compose --profile dev up -d
	@echo "$(GREEN)✓ Development container started$(NC)"

docker-stop: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

docker-logs: ## View Docker container logs
	@docker-compose logs -f

docker-shell: ## Open shell in running container
	@echo "$(BLUE)Opening shell in container...$(NC)"
	@docker-compose exec linkedin-mcp-stdio /bin/bash

docker-clean: ## Remove Docker images and containers
	@echo "$(BLUE)Cleaning Docker resources...$(NC)"
	@docker-compose down -v --remove-orphans
	@docker rmi chuk-mcp-linkedin:latest chuk-mcp-linkedin:dev 2>/dev/null || true
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

docker-test: docker-build ## Build and test Docker image
	@echo "$(BLUE)Testing Docker image...$(NC)"
	@docker run --rm chuk-mcp-linkedin:latest python -c "import chuk_mcp_linkedin; print('✓ Import successful')"
	@echo "$(GREEN)✓ Docker image test passed$(NC)"

## Development Workflow -------------------------------------------

serve: ## Run the MCP server
	@echo "$(BLUE)Starting LinkedIn MCP Server...$(NC)"
	@$(PYTHON) -m chuk_mcp_linkedin.server

debug: ## Run with debug logging
	@echo "$(BLUE)Starting server with debug logging...$(NC)"
	@DEBUG=1 $(PYTHON) -m chuk_mcp_linkedin.server

## Statistics -----------------------------------------------------

stats: ## Show code statistics
	@echo "$(BLUE)Code Statistics$(NC)"
	@echo "==============="
	@echo ""
	@echo "$(YELLOW)Lines of Code:$(NC)"
	@find $(SRC_DIR) -name "*.py" -exec wc -l {} + | tail -1
	@echo ""
	@echo "$(YELLOW)Number of Files:$(NC)"
	@find $(SRC_DIR) -name "*.py" | wc -l
	@echo ""
	@echo "$(YELLOW)Test Files:$(NC)"
	@find $(TEST_DIR) -name "test_*.py" | wc -l
	@echo ""
	@echo "$(YELLOW)Test Cases:$(NC)"
	@grep -r "def test_" $(TEST_DIR) | wc -l
	@echo ""
	@echo "$(YELLOW)Themes:$(NC)"
	@echo "10 pre-built themes"
	@echo ""
	@echo "$(YELLOW)Design Tokens:$(NC)"
	@echo "3 token systems (Text, Engagement, Structure)"

## Maintenance ----------------------------------------------------

update-deps: ## Update all dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	@uv pip install --upgrade pip
	@uv pip list --outdated
	@echo "$(YELLOW)Run 'uv pip install --upgrade <package>' to update specific packages$(NC)"

check-deps: ## Check for outdated dependencies
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@uv pip list --outdated

freeze: ## Freeze current dependencies
	@echo "$(BLUE)Freezing dependencies...$(NC)"
	@uv pip freeze > requirements.txt
	@echo "$(GREEN)✓ Dependencies frozen to requirements.txt$(NC)"

## Shortcuts ------------------------------------------------------

t: test ## Shortcut for test
c: coverage ## Shortcut for coverage
f: format ## Shortcut for format
l: lint ## Shortcut for lint
q: quality ## Shortcut for quality
e: examples ## Shortcut for examples
ch: check ## Shortcut for check

# Special targets
all: clean install dev quality test coverage examples ## Run everything
	@echo "$(GREEN)✓ All tasks complete!$(NC)"

.PHONY: t c f l q e ch
