# ============================================================
# Lekhak AI - Makefile
# ============================================================
# Quick commands for development and production
# ============================================================

.PHONY: help build up down logs restart clean dev prod db-only shell test

# Default target
help:
	@echo "============================================================"
	@echo "Lekhak AI - Available Commands"
	@echo "============================================================"
	@echo ""
	@echo "Production:"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View logs (follow mode)"
	@echo "  make build     - Rebuild containers"
	@echo ""
	@echo "Development:"
	@echo "  make dev       - Start development environment"
	@echo "  make dev-down  - Stop development environment"
	@echo "  make dev-logs  - View development logs"
	@echo ""
	@echo "Database:"
	@echo "  make db-only   - Start only PostgreSQL"
	@echo "  make db-shell  - Open PostgreSQL shell"
	@echo ""
	@echo "Utilities:"
	@echo "  make shell     - Open shell in backend container"
	@echo "  make clean     - Remove all containers and volumes"
	@echo "  make prune     - Clean up unused Docker resources"
	@echo ""

# ----------------------------------------------------------
# Production Commands
# ----------------------------------------------------------
build:
	docker-compose build --no-cache

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose down
	docker-compose up -d

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-db:
	docker-compose logs -f postgres

# ----------------------------------------------------------
# Development Commands
# ----------------------------------------------------------
dev:
	docker-compose -f docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-build:
	docker-compose -f docker-compose.dev.yml build --no-cache

# ----------------------------------------------------------
# Database Commands
# ----------------------------------------------------------
db-only:
	docker-compose up -d postgres

db-shell:
	docker-compose exec postgres psql -U $${DB_USER:-postgres} -d $${DB_NAME:-lekhak_ai}

# ----------------------------------------------------------
# Utility Commands
# ----------------------------------------------------------
shell:
	docker-compose exec backend /bin/bash

clean:
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans 2>/dev/null || true

prune:
	docker system prune -f
	docker volume prune -f
