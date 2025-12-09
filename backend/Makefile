.PHONY: install run lint format test clean

# 환경 설정
PYTHON = poetry run python3
UVICORN = poetry run uvicorn

install:
	@echo "🚀 Installing dependencies..."
	@poetry install

run:
	@echo "🚀 Starting server..."
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	@echo "🚀 Running Linter (Ruff) & Type Checker (MyPy)..."
	@poetry run black --preview --check .
	@poetry run ruff check --show-files .
	@poetry run mypy .

format:
	@echo "🚀 Formatting code..."
	@poetry run black --preview .
	@poetry run ruff format .
	@poetry run ruff check . --fix

test:
	@echo "🚀 Running Tests..."
	@poetry run pytest

clean:
	@echo "🚀 Cleaning cache..."
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf __pycache__