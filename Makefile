# ==============================================================================
# AI Recruitment Suite - Production Makefile
# Author: Ruslan Magana Vsevolodovna
# Website: ruslanmv.com
# License: Apache 2.0
# ==============================================================================

# Use bash as the default shell for all recipes
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[0;33m
NC := \033[0m # No Color

# Project variables
PROJECT_NAME := ai-recruitment-suite
PYTHON_VERSION := 3.11
VENV_DIR := .venv
UV := uvx --python $(PYTHON_VERSION)
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
PYTEST := $(VENV_DIR)/bin/pytest
BLACK := $(VENV_DIR)/bin/black
RUFF := $(VENV_DIR)/bin/ruff
MYPY := $(VENV_DIR)/bin/mypy

# Script locations
INSTALL_SCRIPT := scripts/install.sh
START_SCRIPT := scripts/start.sh
RUN_SCRIPT := scripts/run.sh
STOP_SCRIPT := scripts/stop.sh
PURGE_SCRIPT := scripts/purge.sh

# MCP Context Forge configuration
MCP_GATEWAY_PORT := 4444
MCP_GATEWAY_HOST := 0.0.0.0

# ==============================================================================
# HELP - Self-documenting Makefile
# ==============================================================================
.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║  AI Recruitment Suite - Production Makefile                     ║$(NC)"
	@echo "$(BLUE)║  Author: Ruslan Magana Vsevolodovna | ruslanmv.com              ║$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Available Commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  1. make install        # Set up environment"
	@echo "  2. make start          # Start watsonx Orchestrate"
	@echo "  3. make run            # Import agents and tools"
	@echo "  4. make test           # Run tests"
	@echo ""

# ==============================================================================
# INSTALLATION & SETUP
# ==============================================================================
.PHONY: install
install: ## Install all dependencies using uv
	@echo "$(GREEN)🚀 Starting environment installation...$(NC)"
	@if ! command -v uv &> /dev/null; then \
		echo "$(YELLOW)⚙️  Installing uv package manager...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@echo "$(GREEN)⚙️  Creating virtual environment with Python $(PYTHON_VERSION)...$(NC)"
	@uv venv $(VENV_DIR) --python $(PYTHON_VERSION)
	@echo "$(GREEN)📦 Installing dependencies with uv sync...$(NC)"
	@uv pip install -e ".[dev,test]"
	@echo "$(GREEN)🔧 Installing MCP Context Forge...$(NC)"
	@uv pip install mcp-contextforge-gateway
	@echo "$(GREEN)⚙️  Running additional setup scripts...$(NC)"
	@$(SHELL) $(INSTALL_SCRIPT)
	@echo "$(GREEN)✅ Installation complete!$(NC)"

.PHONY: install-ci
install-ci: ## Install for CI/CD (no interactive prompts)
	@echo "$(GREEN)🤖 Installing for CI/CD environment...$(NC)"
	@uv venv $(VENV_DIR) --python $(PYTHON_VERSION)
	@uv pip install -e ".[test]"
	@echo "$(GREEN)✅ CI installation complete!$(NC)"

.PHONY: update
update: ## Update all dependencies to latest versions
	@echo "$(YELLOW)📦 Updating dependencies...$(NC)"
	@uv pip install --upgrade -e ".[dev,test]"
	@echo "$(GREEN)✅ Dependencies updated!$(NC)"

# ==============================================================================
# CODE QUALITY & LINTING
# ==============================================================================
.PHONY: lint
lint: ## Run all linters (ruff, black check, mypy)
	@echo "$(BLUE)🔍 Running linters...$(NC)"
	@$(RUFF) check tools/ agents/ tests/ || true
	@$(BLACK) --check tools/ agents/ tests/ || true
	@echo "$(GREEN)✅ Linting complete!$(NC)"

.PHONY: format
format: ## Format code with black and ruff
	@echo "$(BLUE)🎨 Formatting code...$(NC)"
	@$(BLACK) tools/ agents/ tests/
	@$(RUFF) check --fix tools/ agents/ tests/ || true
	@echo "$(GREEN)✅ Code formatted!$(NC)"

.PHONY: type-check
type-check: ## Run mypy type checking
	@echo "$(BLUE)🔬 Running type checks...$(NC)"
	@$(MYPY) tools/ agents/ || true
	@echo "$(GREEN)✅ Type checking complete!$(NC)"

.PHONY: quality
quality: format lint type-check ## Run all quality checks (format, lint, type-check)
	@echo "$(GREEN)✅ All quality checks complete!$(NC)"

# ==============================================================================
# TESTING
# ==============================================================================
.PHONY: test
test: ## Run all tests with pytest
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	@$(PYTEST) tests/ -v
	@echo "$(GREEN)✅ Tests complete!$(NC)"

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	@$(PYTEST) tests/ -v -m "unit"
	@echo "$(GREEN)✅ Unit tests complete!$(NC)"

.PHONY: test-integration
test-integration: ## Run integration tests only
	@echo "$(BLUE)🧪 Running integration tests...$(NC)"
	@$(PYTEST) tests/ -v -m "integration"
	@echo "$(GREEN)✅ Integration tests complete!$(NC)"

.PHONY: test-cov
test-cov: ## Run tests with coverage report
	@echo "$(BLUE)🧪 Running tests with coverage...$(NC)"
	@$(PYTEST) tests/ --cov=tools --cov=agents --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/$(NC)"

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	@echo "$(BLUE)🧪 Running tests in watch mode...$(NC)"
	@$(PYTEST) tests/ -v --lf --tb=short

# ==============================================================================
# WATSONX ORCHESTRATE OPERATIONS
# ==============================================================================
.PHONY: start
start: ## Start watsonx Orchestrate server
	@echo "$(GREEN)🚀 Starting watsonx Orchestrate server...$(NC)"
	@$(SHELL) $(START_SCRIPT)
	@echo "$(GREEN)✅ Server started!$(NC)"

.PHONY: run
run: ## Import agents and tools, start application
	@echo "$(GREEN)🏃 Running application setup...$(NC)"
	@$(SHELL) $(RUN_SCRIPT)
	@echo "$(GREEN)✅ Application setup complete!$(NC)"

.PHONY: stop
stop: ## Stop watsonx Orchestrate server
	@echo "$(YELLOW)🛑 Stopping server...$(NC)"
	@$(SHELL) $(STOP_SCRIPT)
	@echo "$(GREEN)✅ Server stopped!$(NC)"

.PHONY: purge
purge: ## Remove all containers and Docker images
	@echo "$(RED)🔥 Purging environment...$(NC)"
	@$(SHELL) $(PURGE_SCRIPT)
	@echo "$(GREEN)✅ Environment purged!$(NC)"

.PHONY: restart
restart: stop start ## Restart watsonx Orchestrate server
	@echo "$(GREEN)✅ Server restarted!$(NC)"

# ==============================================================================
# MCP CONTEXT FORGE OPERATIONS
# ==============================================================================
.PHONY: mcp-start
mcp-start: ## Start MCP Context Forge gateway
	@echo "$(GREEN)🌐 Starting MCP Context Forge gateway...$(NC)"
	@$(VENV_DIR)/bin/mcpgateway \
		--host $(MCP_GATEWAY_HOST) \
		--port $(MCP_GATEWAY_PORT) \
		--log-level info &
	@echo "$(GREEN)✅ MCP Gateway started on http://$(MCP_GATEWAY_HOST):$(MCP_GATEWAY_PORT)$(NC)"

.PHONY: mcp-stop
mcp-stop: ## Stop MCP Context Forge gateway
	@echo "$(YELLOW)🛑 Stopping MCP Context Forge gateway...$(NC)"
	@pkill -f mcpgateway || true
	@echo "$(GREEN)✅ MCP Gateway stopped!$(NC)"

.PHONY: mcp-status
mcp-status: ## Check MCP Context Forge gateway status
	@echo "$(BLUE)📊 Checking MCP Gateway status...$(NC)"
	@curl -s http://$(MCP_GATEWAY_HOST):$(MCP_GATEWAY_PORT)/health || \
		echo "$(RED)❌ MCP Gateway is not running$(NC)"

# ==============================================================================
# DATABASE OPERATIONS
# ==============================================================================
.PHONY: db-init
db-init: ## Initialize recruitment database
	@echo "$(BLUE)🗄️  Initializing database...$(NC)"
	@$(PYTHON) -c "from tools.db_manager_enhanced import init_db; init_db()"
	@echo "$(GREEN)✅ Database initialized!$(NC)"

.PHONY: db-clean
db-clean: ## Clean recruitment database
	@echo "$(RED)🗑️  Cleaning database...$(NC)"
	@rm -f recruitment.db
	@echo "$(GREEN)✅ Database cleaned!$(NC)"

.PHONY: db-reset
db-reset: db-clean db-init ## Reset database (clean + init)
	@echo "$(GREEN)✅ Database reset complete!$(NC)"

# ==============================================================================
# DEVELOPMENT
# ==============================================================================
.PHONY: dev
dev: install start run ## Full development setup (install + start + run)
	@echo "$(GREEN)✅ Development environment ready!$(NC)"
	@echo "$(BLUE)🌐 Open http://localhost:3000/chat-lite$(NC)"

.PHONY: shell
shell: ## Activate virtual environment shell
	@echo "$(BLUE)🐚 Activating virtual environment...$(NC)"
	@$(VENV_DIR)/bin/activate

.PHONY: clean
clean: ## Clean build artifacts and cache
	@echo "$(YELLOW)🧹 Cleaning build artifacts...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	@echo "$(GREEN)✅ Cleaned!$(NC)"

.PHONY: clean-all
clean-all: clean db-clean ## Clean everything (build + db + venv)
	@echo "$(YELLOW)🧹 Cleaning virtual environment...$(NC)"
	@rm -rf $(VENV_DIR)
	@echo "$(GREEN)✅ Everything cleaned!$(NC)"

# ==============================================================================
# DOCUMENTATION
# ==============================================================================
.PHONY: docs
docs: ## Generate documentation
	@echo "$(BLUE)📚 Generating documentation...$(NC)"
	@$(VENV_DIR)/bin/mkdocs build
	@echo "$(GREEN)✅ Documentation generated in site/$(NC)"

.PHONY: docs-serve
docs-serve: ## Serve documentation locally
	@echo "$(BLUE)📚 Serving documentation...$(NC)"
	@$(VENV_DIR)/bin/mkdocs serve

# ==============================================================================
# BUILD & RELEASE
# ==============================================================================
.PHONY: build
build: quality test ## Build distribution packages
	@echo "$(BLUE)📦 Building distribution packages...$(NC)"
	@uv build
	@echo "$(GREEN)✅ Build complete! Check dist/$(NC)"

.PHONY: release
release: build ## Prepare release (build + tag)
	@echo "$(YELLOW)🚀 Preparing release...$(NC)"
	@echo "$(BLUE)Run: git tag -a vX.Y.Z -m 'Release X.Y.Z'$(NC)"
	@echo "$(BLUE)Then: git push origin vX.Y.Z$(NC)"

# ==============================================================================
# CI/CD
# ==============================================================================
.PHONY: ci
ci: install-ci quality test ## Run CI pipeline (install, quality, test)
	@echo "$(GREEN)✅ CI pipeline complete!$(NC)"

# ==============================================================================
# UTILITIES
# ==============================================================================
.PHONY: version
version: ## Show project version
	@echo "$(BLUE)AI Recruitment Suite v1.0.0$(NC)"
	@echo "$(BLUE)Author: Ruslan Magana Vsevolodovna$(NC)"
	@echo "$(BLUE)Website: ruslanmv.com$(NC)"

.PHONY: deps
deps: ## Show dependency tree
	@echo "$(BLUE)📦 Dependency tree:$(NC)"
	@uv pip tree

.PHONY: check-env
check-env: ## Check environment configuration
	@echo "$(BLUE)🔍 Checking environment...$(NC)"
	@echo "Python version: $$(python --version)"
	@echo "UV version: $$(uv --version)"
	@if [ -f .env ]; then \
		echo "$(GREEN)✅ .env file exists$(NC)"; \
	else \
		echo "$(RED)❌ .env file missing (copy from .env.template)$(NC)"; \
	fi

.PHONY: info
info: ## Show project information
	@echo ""
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║           AI Recruitment Suite - Project Information            ║$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Project:$(NC)       $(PROJECT_NAME)"
	@echo "$(GREEN)Version:$(NC)       1.0.0"
	@echo "$(GREEN)Author:$(NC)        Ruslan Magana Vsevolodovna"
	@echo "$(GREEN)Website:$(NC)       ruslanmv.com"
	@echo "$(GREEN)License:$(NC)       Apache 2.0"
	@echo "$(GREEN)Python:$(NC)        $(PYTHON_VERSION)+"
	@echo ""
	@echo "$(BLUE)Backend:$(NC)       IBM MCP Context Forge"
	@echo "$(BLUE)Framework:$(NC)     watsonx Orchestrate"
	@echo ""

# Declare all phony targets
.PHONY: all
all: help
