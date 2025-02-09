.PHONY: help init check-python check-docker build run stop clean test lint format start monitor health logs dev-setup

# Default target when just running 'make'
help:
	@echo "Available commands:"
	@echo "  make init     - Initialize project (create venv, install dependencies)"
	@echo "  make start    - Initialize, build, and start all services"
	@echo "  make build    - Build Docker images"
	@echo "  make run      - Run the application"
	@echo "  make stop     - Stop all services"
	@echo "  make clean    - Remove all containers, volumes, and artifacts"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Run linting"
	@echo "  make logs     - View application logs"
	@echo "  make health   - Check system health"
	@echo "  make monitor  - Open Kafdrop UI"

# Initialize the project
init: check-python check-docker
	@echo "Initializing project..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install -r requirements-dev.txt
	. venv/bin/activate && pip install -e .

# Check Python installation
check-python:
	@which python3 > /dev/null || (echo "Python 3 is not installed. Please install Python 3.9 or later." && exit 1)
	@python3 -c "import sys; assert sys.version_info >= (3, 9), 'Python 3.9 or later is required'" || (echo "Python 3.9 or later is required." && exit 1)

# Check Docker installation
check-docker:
	@which docker > /dev/null || (echo "Docker is not installed. Please install Docker." && exit 1)
	@which docker-compose > /dev/null || (echo "Docker Compose is not installed. Please install Docker Compose." && exit 1)

# Build Docker images
build:
	docker-compose build

# Run the application
run:
	docker-compose up -d

# Stop all services
stop:
	docker-compose down

# Clean everything
clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +

# Run tests
test:
	python -m pytest tests/ -v --cov=src

# Run linting
lint:
	flake8 src/ tests/
	python -m pylint src/**/*.py tests/**/*.py

# Format code
format:
	black src/ tests/

# Start everything
start: init build run
	@echo "Waiting for services to start..."
	@sleep 10
	@make health
	@make monitor

# Development setup
dev-setup:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Health check
health:
	./scripts/health_check.sh

# Monitor topics
monitor:
	@echo "Opening Kafdrop UI..."
	@open http://localhost:9000

# View logs
logs:
	docker-compose logs -f
