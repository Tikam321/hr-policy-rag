# ADR-003: Vector Database Selection

## Status

accepted

## Date

2026-08-17

## Context

We need a vector database for the RAG retrieval layer that:

- Supports metadata filtering (company_id, status, version, policy_type)
- Handles 500 docs (~5,000–15,000 chunks) initially; room to grow
- Supports hybrid search (dense vectors + sparse/BM25) for production retrieval
- Runs locally in Docker Compose and has a managed cloud option
- Has a good Python client and is interview-explainable

Expected scale:

| Stage | Documents | Est. chunks |
|-------|-----------|-------------|
| MVP | 50 | ~500–1,500 |
| Scale | 500 | ~5,000–15,000 |
| Future | 5,000+ | ~50,000–150,000 |

## Decision

Use **Qdrant** as the vector database.

Configuration:

- Collection per environment (dev, prod) — not per company (use payload filters for multi-tenancy)
- Embedding dimension: 1536 (OpenAI text-embedding-3-small)
- Payload indexes on: `company_id`, `doc_id`, `status`, `policy_type`, `version`
- Hybrid search: Qdrant dense vectors + sparse vectors (or BM25 fusion via application layer for MVP)
- Distance metric: Cosine

## Consequences

### Positive

- Native metadata filtering — critical for multi-company HR policies
- Hybrid search support (dense + sparse) in recent Qdrant versions
- Excellent Python client (`qdrant-client`)
- Runs in Docker with minimal config
- Qdrant Cloud available for production deployment
- Good performance at our scale; handles millions of vectors if needed later

### Negative

- Another service to operate (vs pgvector in existing Postgres)
- Team must learn Qdrant-specific APIs (mitigated by thin wrapper in `rag/ingestion/indexer.py`)

### Neutral

- BM25 can start as application-layer fusion (rank_bm25) and migrate to Qdrant sparse vectors later
- Collection schema changes require re-indexing (document in RUNBOOK)

## Alternatives Considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|--------------|
| **pgvector** | Single DB with Postgres; simpler ops | Weaker hybrid search; slower at scale for vector-only queries | Qdrant better for retrieval-focused workload |
| **Chroma** | Easy local setup | Less production-proven; weaker filtering | Better for prototypes |
| **Weaviate** | Hybrid search built-in | Heavier deployment; more complex | Qdrant simpler for our scale |
| **Pinecone** | Managed, scalable | Vendor lock-in; cost; less local dev control | Qdrant Cloud gives managed option with local dev parity |
| **FAISS** | Fast, in-memory | No metadata filtering; no persistence story | Not production-ready alone |
| **Elasticsearch** | Strong BM25 | Heavier ops; vector support secondary | Overkill for MVP; Qdrant hybrid sufficient |

## References

- Qdrant documentation: https://qdrant.tech/documentation/
- `rag/ingestion/indexer.py` — Qdrant integration (to be implemented)
- `rag/retrieval/hybrid.py` — retrieval layer (to be implemented)
