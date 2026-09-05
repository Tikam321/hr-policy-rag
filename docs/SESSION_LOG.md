# Session Log

> Append a new entry at the **top** after every coding agent session.
> Do not delete prior entries.

---

## Session 2026-09-03 — Phase 1.4 & 1.5: Generation Scripts + MVP Corpus (50 PDFs)

**Phase:** Phase 1.4 (generation scripts) completed + Phase 1.5 (MVP corpus) completed

**Completed:**
- [x] Fixed generation-script bugs surfaced by executing the code:
  - Premature schema validation with empty `id` in `generate_eval_qa.py` helper functions (moved final validation to `generate_golden_qa`, which re-validates every item).
  - `eval_qa.schema.json` required singular `source_doc_id`, conflicting with cross-policy questions using plural `source_doc_ids` — schema now accepts either via `anyOf`.
  - `generate_golden_qa` crashed with `KeyError` on partial corpora (`--count 5`) because medium/cross-policy builders hard-required all 10 policy types — builders now skip gracefully when a needed type is absent.
- [x] Resolved the WeasyPrint PDF-rendering blocker: installed `pango` system libs via Homebrew; `import weasyprint` (v69.0) + PDF smoke render verified.
- [x] Added retry/rate-limit handling to the LLM client (`_build_llm_client`): `max_retries=8`, `timeout=60`, configurable via `DATA_GENERATION_LLM_MAX_RETRIES` / `DATA_GENERATION_LLM_TIMEOUT`. Confirmed backoff handles Mistral HTTP 429 rate limits.
- [x] Switched data-generation LLM provider to **Mistral** (OpenAI-compatible endpoint `https://api.mistral.ai/v1/`, model `mistral-medium`) via `DATA_GENERATION_LLM_PROVIDER=mistral` + `MISTRAL_API_KEY` in `.env` (gitignored).
- [x] Added `load_dotenv` support in `scripts/data_generation/common.py` so scripts read `.env`.
- [x] Added `--resume` flag to `batch_generate.py` — skips documents whose metadata already exists (avoids re-spending LLM calls on partial runs).
- [x] Lint (ruff) and tests (`tests/test_data_generation.py`) all pass — 6/6.
- [x] Generated MVP corpus: **50 PDFs** (5 companies × 10 policy types) + **50 metadata files** + **80 golden Q&A** (50 easy, 20 medium, 10 hard/unanswerable).
- [x] Verified outputs: all 50 metadata valid vs `policy.schema.json`; all 80 QA items valid vs `eval_qa.schema.json`; all 50 PDFs valid (`%PDF` header, real LLM prose); QA source refs all resolve to real doc_ids.

**Phase 1 status:** Phases 1.1–1.5 all complete. `docs/IMPLEMENTATION.md` sections 1.4 and 1.5 checked off.

**Files changed:**
- `scripts/data_generation/generate_eval_qa.py` — removed premature validation, resilient medium-question builders
- `data/schemas/eval_qa.schema.json` — allow `source_doc_id` **or** `source_doc_ids` for answerable items
- `scripts/data_generation/generate_policies.py` — provider-agnostic client build (OpenAI/Mistral) + retry/timeout
- `scripts/data_generation/common.py` — load `.env` at import
- `scripts/data_generation/batch_generate.py` — `--resume` support
- `.env` (created, gitignored) — Mistral provider config
- `docs/IMPLEMENTATION.md`, `docs/SESSION_LOG.md`, `AGENTS.md`, `docs/README.md`, `docs/ARCHITECTURE.md` — status updates

**Next session should:**
- Phase 2 — Ingestion pipeline: 2.1 core config (`rag/config.py`), 2.2 PDF parser, 2.3 chunker, etc.

**Blockers:** None

---

## Session 2026-08-17 (e) — Phase 1.3: Policy Templates

**Phase:** Phase 1.3 — HTML policy templates + LLM prompt templates

**Completed:**
- [x] `data/templates/policy_html/base.html` — shared header (doc_id, version, effective date), footer, print CSS
- [x] 10 policy HTML templates (`leave_policy.html` … `travel.html`) with numbered sections via Jinja2
- [x] `data/templates/prompts/system.txt` — LLM system instructions
- [x] `data/templates/prompts/generate_section.j2` — per-section user prompt template
- [x] `data/templates/prompts/section_outlines.json` — section titles, keys, and parameter bindings per policy type

**Next session should:**
- Phase 1.4 — Generation scripts (`generate_policies.py`, `render_pdf.py`, `batch_generate.py`, etc.)

**Blockers:** None

---

## Session 2026-08-17 (d) — Phase 1.2: Seed Data

**Phase:** Phase 1.2 — Seed company profiles + policy parameter ranges

**Completed:**
- [x] `data/seed/companies.json` — 5 company profiles (slug `company_id`, varied industry/region/size)
- [x] `data/seed/policy_parameter_ranges.json` — min/max (or enum) ranges for all 10 policy types
- [x] Validated each company record against `company.schema.json`

**Next session should:**
- Phase 1.3 — HTML policy templates in `data/templates/policy_html/` + LLM prompt templates

**Blockers:** None

---

## Session 2026-08-17 (c) — Phase 1.1: Data Schemas

**Phase:** Phase 1.1 — Data schemas

**Completed:**
- [x] `data/schemas/company.schema.json`
- [x] `data/schemas/policy.schema.json`
- [x] `data/schemas/chunk.schema.json`
- [x] `data/schemas/eval_qa.schema.json`
- [x] `data/schemas/README.md`

**Next session should:**
- Phase 1.2 — `data/seed/companies.json` + policy parameter ranges

**Blockers:** None

---

## Session 2026-08-17 (b) — Docs Refactor: Split ARCHITECTURE.md

**Agent task:** Split monolithic `docs/ARCHITECTURE.md` (~900 lines) into focused files.

**Phase:** Phase 0 — documentation improvement

**Completed:**
- [x] Created `docs/IMPLEMENTATION.md` — checklist only (~280 lines)
- [x] Created `docs/architecture/overview.md` — system overview
- [x] Created `docs/architecture/design.md` — folder structure, data model, pipelines
- [x] Created `docs/architecture/operations.md` — production, eval, deployment, observability
- [x] Created `docs/architecture/interview-guide.md` — session handoff + interview script
- [x] Replaced `docs/ARCHITECTURE.md` with slim index (~60 lines)
- [x] Created `docs/README.md` — documentation navigation hub
- [x] Updated all references in AGENTS.md, README.md, Makefile, cursor rules, ADRs

**Next session should:**
- Start **Phase 1.1** — Data schemas in `data/schemas/`

**Blockers:** None

---

## Session 2026-08-17 — Phase 0: Project Setup

**Agent task:** Create project architecture, folder structure, agent context, and ADRs from scratch.

**Phase:** Phase 0 — Project setup & documentation

**Completed:**
- [x] Created repository folder structure (apps, rag, data, scripts, infra, tests, docs)
- [x] Wrote `AGENTS.md` — coding agent context and session handoff protocol
- [x] Wrote `README.md` — project overview
- [x] Wrote `docs/ARCHITECTURE.md` — full system design with phased implementation checklist
- [x] Wrote ADRs: 001 (tech stack), 002 (synthetic data), 003 (vector DB)
- [x] Created `docs/SESSION_LOG.md` (this file)
- [x] Created `.cursor/rules/project-context.mdc`

**Files created:**
- `AGENTS.md`
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/SESSION_LOG.md`
- `docs/adr/README.md`
- `docs/adr/000-template.md`
- `docs/adr/001-tech-stack.md`
- `docs/adr/002-synthetic-data.md`
- `docs/adr/003-vector-db.md`
- `.cursor/rules/project-context.mdc`
- Folder README placeholders under `apps/`, `rag/`, `data/`, `scripts/`, `infra/`, `tests/`

**Eval results:** N/A (no pipeline yet)

**Also completed (same session, continued):**
- [x] `pyproject.toml` — dependencies and tool config
- [x] `.env.example` — environment variable template
- [x] `.gitignore` — ignores generated PDFs and secrets
- [x] `Makefile` — placeholder dev commands
- [x] `docs/RUNBOOK.md` — ops runbook skeleton

**Next session should:**
1. Start **Phase 1.1** — Data schemas in `data/schemas/`
2. Then Phase 1.2 seed data, 1.3 templates, 1.4 generation scripts, 1.5 generate 50 PDFs

**Blockers:** None

**Notes:**
- Synthetic data plan: 5 companies × 10 policy types = 50 PDFs for MVP
- Scale to 300–500 PDFs in Phase 11 after full pipeline is built
- User confirmed approach: build pipeline first with 50 docs, scale later
