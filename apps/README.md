# Application Services

Deployable services — each is a separate process/container.

| Directory | Service | Port | Phase |
|-----------|---------|------|-------|
| `api/` | FastAPI REST API | 8000 | Phase 5 |
| `worker/` | Celery ingestion worker | — | Phase 6 |
| `web/` | Streamlit chat UI | 8501 | Phase 8 |

Core RAG logic lives in `rag/` — apps import from there.
