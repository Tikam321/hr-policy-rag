# HR Policy RAG — Production Knowledge Assistant

A production-grade Retrieval-Augmented Generation (RAG) system for HR policy Q&A with cited answers, offline evaluation, and scalable document ingestion.

## Quick Start for Developers & Coding Agents

1. Read **[AGENTS.md](./AGENTS.md)** — project context, conventions, current status
2. Read **[docs/IMPLEMENTATION.md](./docs/IMPLEMENTATION.md)** — step-by-step checklist (check boxes as you go)
3. Read **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** — index to system design docs
3. Check **[docs/SESSION_LOG.md](./docs/SESSION_LOG.md)** — what was done in prior agent sessions
4. Review **[docs/adr/](./docs/adr/)** — architectural decisions and trade-offs

## Project Goals

- Build a **production-level RAG pipeline** from scratch (ingestion → retrieval → generation → eval → deploy)
- Use a **synthetic HR policy corpus** (50 PDFs initially, scale to 300–500 for load testing)
- Maintain **cross-session context** so any coding agent can continue implementation
- Create an **interview-ready** system with eval metrics, observability, and clear trade-offs

## Tech Stack (see ADR-001)

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| API | FastAPI |
| Worker | Celery + Redis |
| Vector DB | Qdrant |
| Metadata DB | PostgreSQL |
| Embeddings | OpenAI `text-embedding-3-small` (local fallback: `bge-small-en-v1.5`) |
| LLM | OpenAI GPT-4o-mini (configurable) |
| PDF parsing | PyMuPDF + structure-aware chunking |
| Eval | RAGAS + custom golden set |
| Infra | Docker Compose → cloud deploy |

## Repository Layout

```
hr-policy-rag/
├── AGENTS.md                 # Coding agent context (read first)
├── docs/
│   ├── README.md             # Documentation index
│   ├── IMPLEMENTATION.md     # Step-by-step checklist (primary tracker)
│   ├── ARCHITECTURE.md       # Slim index to design docs
│   ├── architecture/         # System design (overview, design, operations)
│   ├── SESSION_LOG.md        # Per-session progress
│   └── adr/                  # Architecture Decision Records
├── apps/                     # Application services (api, worker, web)
├── rag/                      # Core RAG library (ingestion, retrieval, generation, eval)
├── data/                     # Schemas, templates, documents, eval sets
├── scripts/                  # Data generation & utility scripts
├── infra/                    # Docker, deployment configs
└── tests/                    # Unit & integration tests
```

## Implementation Status

See the master checklist in **[docs/IMPLEMENTATION.md](./docs/IMPLEMENTATION.md)**.

**Current phase:** Phase 2 — Ingestion pipeline (Phase 1 complete: 50-doc synthetic corpus generated)

## License

MIT (placeholder — update before public release)
