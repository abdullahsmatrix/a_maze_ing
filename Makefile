.PHONY: install run debug clean lint lint-strict help test all

# Default target
help:
	@echo "Available commands:"
	@echo "  make install      - Install project dependencies"
	@echo "  make run          - Run interactive maze explorer"
	@echo "  make debug        - Run in debug mode (pdb)"
	@echo "  make clean        - Remove cache and temporary files"
	@echo "  make lint         - Run linting (flake8 + mypy)"
	@echo "  make lint-strict  - Run strict linting"
	@echo "  make test         - Run test script"
	@echo "  make all          - Install, lint, and run"

# Install dependencies
install:
	@echo "Installing dependencies with Poetry"
	@command -v poetry >/dev/null 2>&1 || pip install poetry
	poetry install

# Run interactive maze explorer
run:
	@echo "Launching interactive maze explorer..."
	poetry run python3 a_maze_ing.py config.txt

# Run in debug mode with pdb
debug:
	@echo "Running maze generator in debug mode..."
	python3 -m pdb a_maze_ing.py config.txt

# Clean up cache and temporary files
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "Cleanup complete."

# Linting with flake8 and mypy
lint:
	@echo "Running linting checks..."
	poetry run flake8 .
	poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "Linting complete."

# Full workflow: install, lint, and run
all: clean install lint run
	@echo "All tasks completed successfully!"