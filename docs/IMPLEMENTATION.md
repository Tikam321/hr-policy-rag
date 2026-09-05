# Implementation Checklist

> **Primary progress tracker.** Check off `[x]` items as completed. Update after every coding agent session.
> Last updated: **2026-09-03** | Current phase: **Phase 2 — Ingestion pipeline**

**Instructions:** Complete phases in order. One agent session = one sub-section when possible.
For system design details, see [`architecture/`](./architecture/). For session handoff, see [`architecture/interview-guide.md`](./architecture/interview-guide.md).

---

## Phase 0 — Project Setup & Documentation

- [x] Create repository structure (folders + placeholder READMEs)
- [x] Write `AGENTS.md` (agent context)
- [x] Write architecture docs (`docs/architecture/`, `docs/IMPLEMENTATION.md`)
- [x] Write initial ADRs (001, 002, 003)
- [x] Create `docs/SESSION_LOG.md`
- [x] Create `.cursor/rules/project-context.mdc`
- [x] Initialize `pyproject.toml` with dependencies
- [x] Create `.env.example` and `.gitignore`
- [x] Create `Makefile` with placeholder commands
- [x] Write `docs/RUNBOOK.md` (ops procedures skeleton)

---

## Phase 1 — Synthetic Data Generation (50 PDFs)

**Target:** 5 companies × 10 policy types = **50 PDFs** + **~80 golden Q&A pairs**

### 1.1 Data Schemas

- [x] Define `data/schemas/company.schema.json`
- [x] Define `data/schemas/policy.schema.json`
- [x] Define `data/schemas/chunk.schema.json`
- [x] Define `data/schemas/eval_qa.schema.json`

### 1.2 Seed Data

- [x] Create `data/seed/companies.json` (5 company profiles)
- [x] Define policy parameter ranges per policy type (leave days, probation, etc.)

### 1.3 Policy Templates

- [x] Create HTML template for each of 10 policy types in `data/templates/policy_html/`
- [x] Create LLM generation prompt templates in `data/templates/prompts/`
- [x] Template includes: header, version, effective date, section numbering, footer

### 1.4 Generation Scripts

- [x] `scripts/data_generation/generate_companies.py` — validate/load seed companies
- [x] `scripts/data_generation/generate_policies.py` — LLM text generation from params
- [x] `scripts/data_generation/render_pdf.py` — HTML → PDF (WeasyPrint or similar)
- [x] `scripts/data_generation/generate_eval_qa.py` — Q&A from known parameters
- [x] `scripts/data_generation/batch_generate.py` — orchestrate: companies × policies → PDFs + metadata + eval

### 1.5 Generate MVP Corpus

- [x] Run batch generator for 5 companies × 10 policies = 50 PDFs
- [x] Output to `data/documents/{company_id}/`
- [x] Output metadata to `data/metadata/{doc_id}.json`
- [x] Output golden Q&A to `data/eval/golden_qa.json` (~80 questions)
- [x] Manual review: spot-check 5 PDFs for quality and structure
- [x] Include unanswerable questions in eval set (~10)

---

## Phase 2 — Ingestion Pipeline

### 2.1 Core Config

- [ ] `rag/config.py` — pydantic-settings (env vars, model names, chunk params)
- [ ] `pyproject.toml` — add core deps (pymupdf, qdrant-client, openai, pydantic)

### 2.2 PDF Parser

- [ ] `rag/ingestion/parser.py` — extract text, headings, page numbers
- [ ] Unit test with sample PDF fixture
- [ ] Handle edge cases: empty pages, tables (basic)

### 2.3 Chunker

- [ ] `rag/ingestion/chunker.py` — structure-aware splitting
- [ ] Configurable: target tokens (512), overlap (15%), min/max bounds
- [ ] Attach section + page metadata to each chunk
- [ ] Unit tests: verify chunk sizes, overlap, metadata

### 2.4 Embedder

- [ ] `rag/ingestion/embedder.py` — batch embedding via OpenAI
- [ ] Store embedding model name + version in chunk metadata
- [ ] Retry logic + rate limit handling
- [ ] Unit test with mocked API

### 2.5 Indexer

- [ ] `rag/ingestion/indexer.py` — Qdrant collection create/upsert
- [ ] PostgreSQL schema: `documents`, `chunks` tables
- [ ] Idempotent upsert (same doc_id + version → replace old chunks)
- [ ] Mark old version chunks as `status=archived`

### 2.6 Ingestion Orchestrator

- [ ] `rag/ingestion/pipeline.py` — parse → chunk → embed → index
- [ ] CLI command: `python -m rag.ingestion.pipeline --doc path/to.pdf`
- [ ] Integration test: ingest 1 PDF → verify chunks in Qdrant + PG

### 2.7 Batch Ingest MVP Corpus

- [ ] Ingest all 50 PDFs
- [ ] Log: total chunks, avg chunk size, ingestion time
- [ ] Verify no duplicate chunk_ids

---

## Phase 3 — Retrieval

### 3.1 Vector Search

- [ ] `rag/retrieval/hybrid.py` — Qdrant vector search (top 30)
- [ ] Metadata filters: `company_id`, `status=active`

### 3.2 BM25 Keyword Search

- [ ] Add BM25 index (Qdrant sparse vectors or rank_bm25 in-memory for MVP)
- [ ] Merge vector + BM25 scores (weighted fusion)

### 3.3 Reranker

- [ ] `rag/retrieval/reranker.py` — cross-encoder (sentence-transformers)
- [ ] Input: top 30 candidates → output: top 5–8
- [ ] Unit test with known query-chunk pairs

### 3.4 Context Builder

- [ ] `rag/retrieval/context_builder.py` — format chunks for LLM prompt
- [ ] Include doc title, section, page in chunk headers
- [ ] Token budget: max context window minus prompt overhead

### 3.5 Retrieval Integration Test

- [ ] Test: known question → correct doc in top 5
- [ ] Measure Recall@5 on golden set (manual script first)

---

## Phase 4 — Generation

### 4.1 Prompts

- [ ] `rag/generation/prompts.py` — system prompt (context-only, cite sources, say "I don't know")
- [ ] User prompt template with `{context}` and `{question}` placeholders

### 4.2 LLM Client

- [ ] `rag/generation/llm.py` — OpenAI wrapper with timeout, retry, structured output
- [ ] Configurable model via env var

### 4.3 Citations

- [ ] `rag/generation/citations.py` — parse LLM citations, validate against retrieved chunks
- [ ] Reject/fabricate citations not in context

### 4.4 End-to-End Query

- [ ] Wire: retrieval → context → generation → citation validation
- [ ] CLI: `python -m rag.generation.cli --question "..." --company novatech-solutions`
- [ ] Integration test: 5 golden Q&A pairs end-to-end

---

## Phase 5 — API Layer

### 5.1 FastAPI App

- [ ] `apps/api/main.py` — app factory, CORS, lifespan (DB connections)
- [ ] Health endpoints: `GET /health`, `GET /ready`

### 5.2 Chat Endpoint

- [ ] `POST /chat/query` — accept `{question, company_id}`, return structured response
- [ ] Request ID middleware (UUID per request)
- [ ] Structured JSON logging per request

### 5.3 Document Endpoints

- [ ] `POST /documents/upload` — upload PDF, enqueue ingestion job
- [ ] `GET /documents/{doc_id}/status` — ingestion job status

### 5.4 Feedback Endpoint

- [ ] `POST /feedback` — `{request_id, rating, comment}`
- [ ] Store in PostgreSQL `feedback` table

### 5.5 Auth & Rate Limiting (MVP)

- [ ] API key middleware (env-based key for MVP)
- [ ] Rate limit: 60 req/min per key (Redis or in-memory)

---

## Phase 6 — Async Worker

- [ ] `apps/worker/celery_app.py` — Celery config with Redis broker
- [ ] `apps/worker/tasks/ingestion.py` — async ingest task
- [ ] Upload endpoint enqueues task; returns job_id immediately
- [ ] Job status polling via Redis or PostgreSQL job table

---

## Phase 7 — Evaluation Harness

### 7.1 Metrics

- [ ] `rag/evaluation/metrics.py` — Recall@k, citation accuracy, answer contains check
- [ ] `rag/evaluation/golden_runner.py` — run all golden Q&A, output report

### 7.2 RAGAS Integration

- [ ] `rag/evaluation/ragas_runner.py` — faithfulness, context precision, answer relevancy
- [ ] Output results to `data/eval/eval_results/`

### 7.3 Eval CLI

- [ ] `make eval` — run full golden set, print summary table
- [ ] Baseline targets (document in RUNBOOK):
  - Recall@5 ≥ 0.85
  - Citation accuracy ≥ 0.90
  - Faithfulness ≥ 0.80

### 7.4 Eval Before/After

- [ ] Run eval after Phase 3 (retrieval only)
- [ ] Run eval after Phase 4 (full pipeline)
- [ ] Document results in SESSION_LOG

---

## Phase 8 — Frontend (Chat UI)

- [ ] `apps/web/app.py` — Streamlit chat interface (or Next.js)
- [ ] Company selector dropdown
- [ ] Chat history display
- [ ] Citations rendered as expandable source cards
- [ ] Thumbs up/down feedback buttons
- [ ] Connect to `POST /chat/query`

---

## Phase 9 — Infrastructure & Docker

- [ ] `infra/docker-compose.yml` — api, worker, postgres, qdrant, redis
- [ ] `infra/docker/Dockerfile.api`
- [ ] `infra/docker/Dockerfile.worker`
- [ ] `.env.example` with all required vars
- [ ] `make dev` — start full stack locally
- [ ] Verify: upload PDF → ingest → query → answer with citations

---

## Phase 10 — Observability

- [ ] Structured JSON logging (request_id, latency_ms, retrieval_count, model)
- [ ] Log retrieval chunks + scores (debug level)
- [ ] `GET /metrics` endpoint or Prometheus exporter (optional)
- [ ] Langfuse or Phoenix integration for LLM traces (optional)

---

## Phase 11 — Scale Test (300–500 PDFs)

- [ ] Extend `data/seed/companies.json` to 30–50 companies
- [ ] Run `batch_generate.py --count 300` (or 500)
- [ ] Batch ingest with Celery (parallel workers)
- [ ] Measure: total ingestion time, chunks indexed, Qdrant collection size
- [ ] Measure: query p50/p95 latency at scale
- [ ] Re-run eval harness — verify metrics don't degrade
- [ ] Document scale test results in SESSION_LOG + RUNBOOK

---

## Phase 12 — Production Hardening

- [ ] Document versioning: deactivate old chunks on re-ingest
- [ ] Graceful degradation: reranker failure → fall back to hybrid top-k
- [ ] LLM timeout + circuit breaker
- [ ] Input validation + max question length
- [ ] `docs/RUNBOOK.md` — complete ops procedures
- [ ] CI pipeline (GitHub Actions): lint, test, eval on PR
- [ ] Cloud deployment config (Railway / Render / AWS — pick one)
- [ ] Demo video or README walkthrough for portfolio
