# ================================================================================
# Gravity MicroServices Platform - Makefile
# ================================================================================
# This Makefile provides convenient shortcuts for common development tasks
# Author: Lars Björkman (DevOps & Infrastructure Lead)
# ================================================================================

.PHONY: help install test lint format clean docker-up docker-down

# Default target
help:
	@echo "Gravity MicroServices Platform - Development Commands"
	@echo "======================================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Install all dependencies"
	@echo "  make install-dev      Install with development dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run linters (ruff, mypy)"
	@echo "  make format           Format code (black, ruff)"
	@echo "  make format-check     Check formatting without changes"
	@echo "  make type-check       Run type checking (mypy)"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo "  make test-auth        Run auth-service tests only"
	@echo "  make test-gateway     Run api-gateway tests only"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up        Start all services (detached)"
	@echo "  make docker-down      Stop all services"
	@echo "  make docker-logs      View service logs"
	@echo "  make docker-clean     Remove all containers and volumes"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate       Run database migrations"
	@echo "  make db-reset         Reset all databases"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove cache and build files"
	@echo "  make clean-all        Deep clean (includes docker)"
	@echo ""

# Installation
install:
	cd common-library && pip install -e .
	cd auth-service && pip install -e .
	cd api-gateway && pip install -e .

install-dev:
	cd common-library && pip install -e ".[dev,test]"
	cd auth-service && pip install -e ".[dev,test]"
	cd api-gateway && pip install -e ".[dev,test]"
	pip install ruff black mypy pytest pytest-cov

# Code Quality
lint:
	@echo "Running Ruff linter..."
	ruff check auth-service/app api-gateway/app common-library/gravity_common
	@echo "Running MyPy type checker..."
	mypy auth-service/app api-gateway/app common-library/gravity_common

format:
	@echo "Formatting code with Black..."
	black auth-service/app api-gateway/app common-library/gravity_common
	@echo "Sorting imports with Ruff..."
	ruff check --select I --fix auth-service/app api-gateway/app common-library/gravity_common

format-check:
	@echo "Checking code formatting..."
	black --check auth-service/app api-gateway/app common-library/gravity_common

type-check:
	mypy auth-service/app api-gateway/app common-library/gravity_common

# Testing
test:
	@echo "Running all tests..."
	cd auth-service && pytest tests/ -v
	cd api-gateway && pytest tests/ -v
	cd common-library && pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	cd auth-service && pytest tests/ --cov=app --cov-report=html --cov-report=term
	cd api-gateway && pytest tests/ --cov=app --cov-report=html --cov-report=term
	cd common-library && pytest tests/ --cov=gravity_common --cov-report=html --cov-report=term

test-auth:
	cd auth-service && pytest tests/ -v

test-gateway:
	cd api-gateway && pytest tests/ -v

# Docker
docker-up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	sleep 10
	@echo "Services are up! Check status with: docker-compose ps"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Database
db-migrate:
	cd auth-service && alembic upgrade head

db-reset:
	docker-compose down -v
	docker-compose up -d postgres
	sleep 5
	cd auth-service && alembic upgrade head

# Cleanup
clean:
	@echo "Cleaning cache and build files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

clean-all: clean docker-clean
	@echo "Deep clean completed!"

# Security
security-check:
	@echo "Running security checks..."
	pip install bandit safety
	bandit -r auth-service/app api-gateway/app common-library/gravity_common
	safety check

# Documentation
docs:
	@echo "Opening documentation..."
	@echo "Main README: README.md"
	@echo "Architecture: docs/ARCHITECTURE.md"
	@echo "Contributing: CONTRIBUTING.md"
	@echo "Changelog: CHANGELOG.md"

# Quick start
quick-start: install-dev docker-up
	@echo ""
	@echo "✅ Gravity MicroServices Platform is ready!"
	@echo ""
	@echo "Services running:"
	@echo "  - PostgreSQL: localhost:5432"
	@echo "  - Redis: localhost:6379"
	@echo "  - Consul: http://localhost:8500"
	@echo "  - Prometheus: http://localhost:9090"
	@echo "  - Grafana: http://localhost:3000"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run migrations: make db-migrate"
	@echo "  2. Run tests: make test"
	@echo "  3. Start developing! 🚀"
	@echo ""
