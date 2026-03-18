.PHONY: help install install-dev test lint format clean build run stop logs

help:
	@echo "📚 Vocabulab - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linting (flake8)"
	@echo "  make format       - Format code with black"
	@echo "  make format-check - Check code formatting"
	@echo ""
	@echo "Docker:"
	@echo "  make build        - Build Docker images"
	@echo "  make run          - Start containers"
	@echo "  make stop         - Stop containers"
	@echo "  make logs         - Show container logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo ""

install:
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing -v
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black .

format-check:
	black --check --diff .

build:
	docker-compose build

run:
	docker-compose up -d
	@echo "✅ Application started"
	@echo "Frontend: http://localhost"
	@echo "API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

stop:
	docker-compose down
	@echo "✅ Application stopped"

logs:
	docker-compose logs -f vocabstack_backend

logs-frontend:
	docker-compose logs -f vocabstack_frontend

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".eggs" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup completed"

docker-clean:
	docker-compose down -v
	docker system prune -f
	@echo "✅ Docker cleanup completed"
