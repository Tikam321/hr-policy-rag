# AGENTS.md — Coding Agent Context

> **Read this file first** at the start of every coding agent session.
> Update `docs/SESSION_LOG.md` at the end of every session.

## Project Summary

We are building a **production-grade HR Policy RAG system** from scratch:

- Synthetic HR policy PDF corpus (50 docs → scale to 300–500)
- Full pipeline: PDF → parse → chunk → embed → index → retrieve → rerank → generate (with citations)
- Offline eval harness (golden Q&A + RAGAS metrics)
- Async ingestion, sync low-latency query API
- Docker Compose for local dev; cloud-ready deployment

**Interview goal:** Demonstrate end-to-end production RAG — not a tutorial chatbot.

## Required Reading (in order)

| Priority | File | Purpose |
|----------|------|---------|
| 1 | `docs/IMPLEMENTATION.md` | **Implementation checklist** — check boxes as you complete steps |
| 2 | `docs/ARCHITECTURE.md` | Index to system design docs in `docs/architecture/` |
| 2 | `docs/SESSION_LOG.md` | Prior session work — **do not redo completed steps** |
| 3 | `docs/adr/` | Accepted architectural decisions — **do not contradict without new ADR** |
| 4 | `data/schemas/` | Data contracts for companies, policies, chunks, eval |

## Current Status

| Field | Value |
|-------|-------|
| **Active phase** | Phase 2 — Ingestion pipeline |
| **Document corpus size** | 50 (target: 300–500 later) |
| **Last updated** | 2026-09-03 |
| **Blockers** | None — Phases 0 & 1 complete |

> Agent: update this table and `docs/SESSION_LOG.md` after each session.

## Implementation Rules

### Scope discipline

- Implement **one checklist section** at a time from `docs/IMPLEMENTATION.md`
- Mark completed items `[x]` in the implementation checklist
- Do not skip ahead to later phases unless prior phase checkboxes are done
- Minimize diff scope — no unrelated refactors

### Code conventions

- Python 3.11+, type hints on public functions
- `pydantic` for config and API schemas
- Structured logging (`structlog` or JSON `logging`) — no bare `print` in production code
- Environment variables via `pydantic-settings`; secrets never committed
- One concern per module under `rag/`

### Architecture constraints (from ADRs)

- **Vector DB:** Qdrant (ADR-003)
- **Synthetic data first** (ADR-002) — no scraping proprietary HR PDFs
- **Citations required** in every generated answer
- **Hybrid retrieval** (vector + BM25) before reranking — not pure vector search
- **Eval golden set** generated alongside synthetic PDFs

### Folder ownership

| Path | Responsibility |
|------|----------------|
| `apps/api/` | FastAPI endpoints, auth middleware, request/response models |
| `apps/worker/` | Celery tasks for async ingestion |
| `apps/web/` | Chat UI (Streamlit or Next.js) |
| `rag/ingestion/` | Parse, chunk, embed, index |
| `rag/retrieval/` | Hybrid search, reranking, context assembly |
| `rag/generation/` | Prompts, LLM calls, citation extraction |
| `rag/evaluation/` | Golden set runner, RAGAS metrics |
| `scripts/data_generation/` | Synthetic PDF + eval Q&A generation |
| `data/schemas/` | JSON schemas for all data contracts |
| `data/templates/` | HTML/Markdown policy templates |
| `infra/` | Docker Compose, service configs |

### Session handoff protocol

At the **start** of each session:

1. Read this file and `docs/SESSION_LOG.md`
2. Find the first unchecked item in `docs/IMPLEMENTATION.md`
3. Confirm with user if ambiguous; otherwise proceed

At the **end** of each session:

1. Check off completed items in `docs/IMPLEMENTATION.md`
2. Append entry to `docs/SESSION_LOG.md` (date, phase, files changed, next steps)
3. Update the **Current Status** table above
4. If you made an architectural choice, add an ADR in `docs/adr/`

### ADR policy

- Any significant technology or design change requires a new ADR
- Format: `docs/adr/NNN-short-title.md`
- Status values: `proposed` → `accepted` → `deprecated`
- Do not revert accepted ADRs silently — supersede with a new ADR

## Key Design Decisions (summary)

See full ADRs for rationale.

| Decision | Choice | ADR |
|----------|--------|-----|
| Primary language | Python 3.11+ | ADR-001 |
| Synthetic data strategy | Parameterized templates + LLM | ADR-002 |
| Vector database | Qdrant | ADR-003 |
| Initial corpus size | 50 PDFs (5 companies × 10 policy types) | ADR-002 |
| Scale target | 300–500 PDFs after pipeline complete | ADR-002 |
| Embedding model | `text-embedding-3-small` | ADR-001 |
| Chunking | Structure-aware, 300–800 tokens, 10–15% overlap | architecture/design.md |

## Environment Variables (planned)

```bash
# LLM & Embeddings
OPENAI_API_KEY=

# Databases
DATABASE_URL=postgresql://user:pass@localhost:5432/hr_rag
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379/0

# App
ENV=development
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

## Commands (will be added as implemented)

```bash
# Local dev (not yet available)
# make dev
# make ingest
# make eval
# make generate-data COUNT=50
```

## Interview Talking Points

When explaining this project:

1. Async ingestion vs sync query path
2. Hybrid retrieval + reranking (why not pure vector)
3. Synthetic corpus with ground-truth eval set
4. Citation-required generation + "I don't know" fallback
5. Document versioning and chunk deactivation
6. Observability: request traces linking retrieval → generation
7. Scale test: 50 → 500 documents with same pipeline
