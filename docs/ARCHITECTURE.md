# Architecture Index

> Slim index to system design docs. **For implementation progress, see [`IMPLEMENTATION.md`](./IMPLEMENTATION.md).**

Last updated: **2026-09-03**

---

## Documentation Structure

We split docs into focused files so agents and developers can read only what they need:

| Document | Purpose | When to read |
|----------|---------|--------------|
| [`IMPLEMENTATION.md`](./IMPLEMENTATION.md) | **Step-by-step checklist** with checkboxes | Every coding session — find next task |
| [`architecture/overview.md`](./architecture/overview.md) | Problem, principles, high-level diagram | Understanding the system |
| [`architecture/design.md`](./architecture/design.md) | Folder structure, data model, pipelines | Building or modifying components |
| [`architecture/operations.md`](./architecture/operations.md) | Production reqs, eval, deployment, observability | Ops, eval, and deployment work |
| [`architecture/interview-guide.md`](./architecture/interview-guide.md) | Session handoff + interview script | New agent sessions, interview prep |
| [`SESSION_LOG.md`](./SESSION_LOG.md) | Per-session progress log | Start of every session |
| [`RUNBOOK.md`](./RUNBOOK.md) | On-call procedures | Troubleshooting |
| [`adr/`](./adr/) | Architecture Decision Records | Understanding trade-offs |

---

## System at a Glance

**What:** Production HR Policy RAG with cited answers, synthetic data, and eval harness.

**Corpus:** 50 PDFs (MVP) → 300–500 PDFs (scale test)

**Stack:** Python, FastAPI, Celery, Qdrant, PostgreSQL, OpenAI — see [ADR-001](./adr/001-tech-stack.md)

**Current phase:** Phase 1 — Synthetic data generation

---

## Quick Navigation

```
Need to build something?     → IMPLEMENTATION.md
Need to understand design?     → architecture/design.md
Need eval targets?             → architecture/operations.md
Need session handoff rules?    → architecture/interview-guide.md
Need to know what changed?     → SESSION_LOG.md
Need to explain in interview?  → architecture/interview-guide.md
```

See also [`docs/README.md`](./README.md) for the full documentation map.
