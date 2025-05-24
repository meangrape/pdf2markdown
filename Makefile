.PHONY: test format lint typecheck build changelog release clean help

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python
UV := uv
PYTEST := pytest
RUFF := ruff
ISORT := isort
MYPY := mypy
GIT_CHGLOG := git-chglog

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

test: ## Run tests
	@echo "Running tests..."
	@$(UV) run $(PYTEST) -v

format: ## Format code with ruff
	@echo "Formatting code..."
	@$(UV) run $(RUFF) format .

lint: ## Run ruff linter with auto-fix
	@echo "Running linter..."
	@$(UV) run $(RUFF) check --fix .

sort-imports: ## Sort imports with isort
	@echo "Sorting imports..."
	@$(UV) run $(ISORT) .

typecheck: ## Run type checking with mypy
	@echo "Running type checker..."
	@$(UV) run $(MYPY) .

build: ## Build the package
	@echo "Building package..."
	@$(UV) build

changelog: ## Update changelog
	@echo "Updating changelog..."
	@$(GIT_CHGLOG) -o CHANGELOG.md

clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	@rm -rf dist/ build/ *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

# Release process
release: ## Run full release process (test, format, build, etc.)
	@echo "Starting release process..."
	@echo ""
	@CURRENT_VERSION=$$(grep -E "^version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
	echo "Current version: $$CURRENT_VERSION"; \
	echo ""; \
	read -p "Enter new version number: " NEW_VERSION; \
	if [ -z "$$NEW_VERSION" ]; then \
		echo "Error: Version number cannot be empty"; \
		exit 1; \
	fi; \
	echo ""; \
	echo "Updating to version $$NEW_VERSION..."; \
	echo ""; \
	sed -i '' "s/^version = \".*\"/version = \"$$NEW_VERSION\"/" pyproject.toml && \
	$(UV) lock && \
	echo "Running quality checks..." && \
	echo "" && \
	$(MAKE) sort-imports && \
	$(MAKE) format && \
	$(MAKE) lint && \
	$(MAKE) typecheck && \
	$(MAKE) test && \
	echo "" && \
	echo "Building package..." && \
	$(MAKE) clean && \
	$(MAKE) build && \
	echo "" && \
	git add pyproject.toml uv.lock && \
	git commit -m "chore: Bump version to $$NEW_VERSION" && \
	git tag -s "v$$NEW_VERSION" -m "Release v$$NEW_VERSION" && \
	$(MAKE) changelog && \
	git add CHANGELOG.md && \
	git commit -m "docs: Update changelog for v$$NEW_VERSION" && \
	echo "" && \
	echo "✨ Release v$$NEW_VERSION prepared successfully!" && \
	echo "" && \
	echo "Next steps:" && \
	echo "  1. Review the changes: git log --oneline -5" && \
	echo "  2. Push commits: git push origin main" && \
	echo "  3. Push tag: git push origin v$$NEW_VERSION" && \
	echo ""

# Additional convenience targets
check: lint typecheck test ## Run all checks (lint, typecheck, test)

fix: sort-imports format lint ## Fix all auto-fixable issues