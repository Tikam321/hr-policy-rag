# Core RAG Library

Framework-agnostic RAG pipeline modules. Imported by `apps/api` and `apps/worker`.

| Module | Responsibility | Phase |
|--------|----------------|-------|
| `config.py` | pydantic-settings, env vars | Phase 2 |
| `ingestion/` | Parse → chunk → embed → index | Phase 2 |
| `retrieval/` | Hybrid search → rerank → context | Phase 3 |
| `generation/` | Prompts → LLM → citations | Phase 4 |
| `evaluation/` | Golden set runner, RAGAS metrics | Phase 7 |

Do not put FastAPI routes or Celery tasks here — those belong in `apps/`.
