# ADR-001: Tech Stack Selection

## Status

accepted

## Date

2026-08-17

## Context

We need a production-grade RAG stack that:

- Is interview-explainable with clear trade-offs
- Supports async ingestion and sync low-latency queries
- Has strong Python ecosystem support for RAG (embeddings, eval, PDF parsing)
- Can run locally via Docker Compose and deploy to cloud later
- Allows incremental development from MVP (50 docs) to scale (500 docs)

## Decision

| Layer | Choice |
|-------|--------|
| Language | **Python 3.11+** |
| API framework | **FastAPI** |
| Async worker | **Celery + Redis** |
| Metadata DB | **PostgreSQL** |
| Vector DB | **Qdrant** (see ADR-003) |
| PDF parsing | **PyMuPDF (fitz)** |
| Embeddings | **OpenAI text-embedding-3-small** |
| LLM | **OpenAI GPT-4o-mini** (configurable via env) |
| Reranker | **cross-encoder/ms-marco-MiniLM-L-6-v2** (sentence-transformers) |
| Eval | **RAGAS** + custom golden set runner |
| Config | **pydantic-settings** |
| Logging | Structured JSON via **structlog** |
| Frontend (MVP) | **Streamlit** |
| Containerization | **Docker Compose** |
| Cloud (Phase 12) | Railway or Render (TBD in ADR-004) |

## Consequences

### Positive

- FastAPI gives automatic OpenAPI docs — useful for demo and testing
- Python RAG ecosystem is mature (LangChain optional; we use custom `rag/` library for clarity)
- Celery handles batch ingestion of 500 PDFs without blocking API
- GPT-4o-mini keeps costs low for development; easy to swap models
- Docker Compose enables one-command local dev stack

### Negative

- Python GIL limits CPU-bound reranker throughput (mitigate with worker processes)
- OpenAI dependency for embeddings/LLM — requires API key and incurs cost
- Streamlit is not ideal for production UI (acceptable for MVP/portfolio; upgrade later)

### Neutral

- Not using LangChain as core framework — clearer code ownership for interviews
- Local embedding fallback (bge-small) can be added later without architecture change

## Alternatives Considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|--------------|
| Node.js + TypeScript | Good for full-stack | Weaker RAG/ML ecosystem | Python better for RAG pipeline |
| LangChain as core | Faster initial dev | Hard to explain in interviews; abstraction overhead | Custom `rag/` library is clearer |
| LlamaIndex | Good retrieval abstractions | Same as LangChain — less ownership | Custom pipeline preferred |
| Ollama (local LLM) | No API cost | Slower, harder to deploy consistently | OpenAI for MVP; local optional later |
| Next.js frontend first | Production UI | Slows MVP; Streamlit sufficient for demo | Streamlit first, upgrade in Phase 12 |
| RQ instead of Celery | Simpler setup | Less production-proven at scale | Celery for production story |

## References

- `docs/architecture/` — full system design
- OpenAI embedding models: https://platform.openai.com/docs/guides/embeddings
