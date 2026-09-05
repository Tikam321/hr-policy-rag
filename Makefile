.PHONY: help install dev down ingest eval generate-data test lint clean

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies in editable mode
	pip install -e ".[dev,web]"

dev: ## Start local Docker Compose stack (Phase 9)
	@echo "Not yet implemented — see docs/IMPLEMENTATION.md Phase 9"
	# docker compose -f infra/docker-compose.yml up --build

down: ## Stop Docker Compose stack
	# docker compose -f infra/docker-compose.yml down

ingest: ## Ingest all PDFs in data/documents/ (Phase 2)
	@echo "Not yet implemented — see docs/IMPLEMENTATION.md Phase 2"
	# python -m rag.ingestion.pipeline --all

eval: ## Run golden set evaluation (Phase 7)
	@echo "Not yet implemented — see docs/IMPLEMENTATION.md Phase 7"
	# python -m rag.evaluation.golden_runner

generate-data: ## Generate synthetic PDF corpus (Phase 1)
	@echo "Usage: make generate-data COUNT=50 DRY_RUN=1"
	python -m scripts.data_generation.batch_generate --count $(or $(COUNT),50) $(if $(DRY_RUN),--dry-run,)

test: ## Run test suite
	pytest tests/ -v

lint: ## Run ruff linter
	ruff check rag/ apps/ scripts/ tests/

clean: ## Remove cache and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
