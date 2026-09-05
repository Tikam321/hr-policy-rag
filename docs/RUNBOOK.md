# Operations Runbook

> Skeleton — fill in procedures as each phase is implemented.
> See [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md) and [`docs/architecture/`](./architecture/) for system design.

---

## Quick Reference

| Service | Local URL | Default Port |
|---------|-----------|--------------|
| API | http://localhost:8000 | 8000 |
| Web UI | http://localhost:8501 | 8501 |
| Qdrant | http://localhost:6333 | 6333 |
| PostgreSQL | localhost | 5432 |
| Redis | localhost | 6379 |

## Commands (to be implemented)

```bash
make dev          # Start full Docker Compose stack
make ingest       # Ingest all PDFs in data/documents/
make eval         # Run golden set evaluation
make generate-data COUNT=50   # Generate synthetic PDF corpus
make logs         # Tail API + worker logs
```

---

## Scenario 1: Start Local Development Stack

**Status:** Not yet implemented (Phase 9)

**Steps:**
1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`
2. Run `make dev`
3. Verify: `curl http://localhost:8000/health`

---

## Scenario 2: Ingest New Documents

**Status:** Not yet implemented (Phase 2)

**Steps:**
1. Place PDF in `data/documents/{company_id}/`
2. Run `python -m rag.ingestion.pipeline --doc path/to.pdf`
3. Or upload via `POST /documents/upload`
4. Check status: `GET /documents/{doc_id}/status`

---

## Scenario 3: Re-Ingest Updated Policy (Version Change)

**Status:** Not yet implemented (Phase 12)

**Steps:**
1. Upload new version PDF with updated `version` metadata
2. Ingestion pipeline marks old chunks as `status=archived`
3. New chunks indexed with `status=active`
4. Run `make eval` to verify no regression

---

## Scenario 4: Bad Answers After Change

**Steps:**
1. Find `request_id` from API response or logs
2. Check retrieval logs: which chunks were retrieved? Scores?
3. Run eval: `make eval` — did Recall@5 drop?
4. Bisect: retrieval issue (Phase 3) vs generation issue (Phase 4)
5. If retrieval: check chunk content, hybrid weights, reranker
6. If generation: check prompt, context size, citation validation

---

## Scenario 5: High Query Latency

**Targets:** p95 < 3 seconds

**Steps:**
1. Check structured logs for `latency_ms` breakdown
2. Common causes:
   - Reranker slow → reduce candidate pool from 30 to 20
   - LLM timeout → check OpenAI status
   - Qdrant slow → check collection size, index health
3. `curl http://localhost:6333/collections` — verify Qdrant health

---

## Scenario 6: Scale Test (300–500 Documents)

**Status:** Phase 11

**Steps:**
1. `make generate-data COUNT=500`
2. Start Celery workers: `docker compose up worker --scale worker=3`
3. Batch ingest: `make ingest --all`
4. Monitor: ingestion jobs/min, failed jobs
5. Run `make eval` — compare metrics to 50-doc baseline
6. Benchmark latency: p50/p95 query times
7. Document results in `docs/SESSION_LOG.md`

---

## Scenario 7: Eval Score Regression

**Thresholds:**

| Metric | Target |
|--------|--------|
| Recall@5 | ≥ 0.85 |
| Citation accuracy | ≥ 0.90 |
| Faithfulness (RAGAS) | ≥ 0.80 |
| Refusal accuracy | ≥ 0.80 |

**Steps:**
1. Run `make eval` — identify failing questions
2. For each failure: retrieval miss or generation error?
3. Do not merge PRs that drop metrics below threshold without ADR justification

---

## Environment Variables

See `.env.example` for full list.

Critical:
- `OPENAI_API_KEY` — required for embeddings and generation
- `DATABASE_URL` — PostgreSQL connection
- `QDRANT_URL` — vector database
- `REDIS_URL` — Celery broker

---

## On-Call Checklist

- [ ] API health: `GET /health`
- [ ] Qdrant health: `GET http://localhost:6333/`
- [ ] Worker queue depth (Redis)
- [ ] Recent error rate in logs
- [ ] Last eval run date and scores
