# Documentation Index

> Navigation hub for the HR Policy RAG project.
> **Coding agents:** read [`AGENTS.md`](../AGENTS.md) first, then [`IMPLEMENTATION.md`](./IMPLEMENTATION.md).

---

## Quick Links

| I want to… | Read this |
|------------|-----------|
| See what to build next | [`IMPLEMENTATION.md`](./IMPLEMENTATION.md) — **checklist with checkboxes** |
| Understand system design | [`architecture/overview.md`](./architecture/overview.md) |
| See repo layout | [`architecture/design.md`](./architecture/design.md) — folder structure + data model + pipeline |
| Plan production ops | [`architecture/operations.md`](./architecture/operations.md) |
| Prepare for interviews | [`architecture/interview-guide.md`](./architecture/interview-guide.md) |
| See what changed last session | [`SESSION_LOG.md`](./SESSION_LOG.md) |
| On-call / troubleshooting | [`RUNBOOK.md`](./RUNBOOK.md) |
| Understand why we chose X | [`adr/`](./adr/) — Architecture Decision Records |
| Look up terms | [`glossary.md`](./glossary.md) |

---

## Document Map

```
docs/
├── README.md                    ← you are here
├── IMPLEMENTATION.md            ← step-by-step checklist (update every session)
├── ARCHITECTURE.md              ← slim index to architecture docs
├── SESSION_LOG.md               ← per-session progress log
├── RUNBOOK.md                   ← ops procedures
├── adr/                         ← architectural decisions
└── architecture/
    ├── overview.md              ← problem, principles, high-level diagram
    ├── design.md                ← folder structure, data model, pipelines
    ├── operations.md            ← production reqs, eval, deployment, observability
    └── interview-guide.md       ← session handoff + interview script
```

---

## Current Status

| Field | Value |
|-------|-------|
| **Phase** | Phase 2 — Ingestion pipeline |
| **Last updated** | 2026-09-03 |
| **Next step** | Phase 2.1 — Core config (`rag/config.py`) |

See [`IMPLEMENTATION.md`](./IMPLEMENTATION.md) for full progress.
