# ADR-002: Synthetic Data Strategy

## Status

accepted

## Date

2026-08-17

## Context

We do not have access to real proprietary HR policy PDFs. We need a document corpus that:

- Is legally safe (no scraping copyrighted handbooks)
- Has **known ground truth** for evaluation (exact leave days, policy rules)
- Scales from MVP (50 docs) to production testing (300–500 docs)
- Produces realistic PDF structure (headings, sections, page numbers, tables)
- Supports multi-company, multi-version scenarios for retrieval testing

## Decision

Use **parameterized synthetic HR policy generation**:

1. **Seed companies** — JSON profiles (name, industry, region, size)
2. **Policy parameters** — typed values per policy type (e.g., `annual_leave_days: 20`)
3. **HTML templates** — one template per policy type with placeholders
4. **LLM generation** — fill templates with natural language from parameters
5. **PDF rendering** — HTML → PDF via WeasyPrint
6. **Metadata JSON** — store all parameters alongside each PDF
7. **Golden Q&A** — auto-generate eval questions from known parameters at creation time

### Corpus Scale Plan

| Phase | Documents | Formula |
|-------|-----------|---------|
| MVP (Phase 1) | **50** | 5 companies × 10 policy types |
| Scale (Phase 11) | **300–500** | 30–50 companies × 10 types (× versions optional) |

### Policy Types (10)

leave_policy, remote_work, code_of_conduct, benefits, expense, performance, onboarding, termination, data_security, travel

### Realism Additions

- Version numbers and effective dates
- 5–10% archived/outdated policy versions (tests version filtering)
- ~10 unanswerable eval questions (tests "I don't know" behavior)
- Tables in benefits and leave policies

## Consequences

### Positive

- **Ground-truth eval** — we know exact answers because we generated the parameters
- **Legally safe** — no proprietary data
- **Scalable** — batch script generates 500 docs in minutes
- **Interview story** — "synthetic corpus with controlled ground truth for eval"
- **Multi-tenant testing** — each company has isolated policy sets

### Negative

- Synthetic language may differ from real HR docs (mitigate with good templates + LLM polish)
- Must disclose in interviews: "synthetic data; pipeline works for real PDFs"
- LLM generation cost for 500 policies (one-time, acceptable)

### Neutral

- Can supplement with 5–10 public domain government labor guidelines later
- Same ingestion pipeline handles synthetic and real PDFs identically

## Alternatives Considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|--------------|
| Scrape real HR PDFs | Realistic language | Legal/ethical risk; no ground truth | Rejected |
| Manual writing | High quality | Not scalable to 500 | Rejected |
| Pure template fill (no LLM) | Deterministic, free | Unnatural language | Use LLM for prose, templates for structure |
| Single giant handbook | Simple | Poor chunking/retrieval testing | Multi-doc per company preferred |
| Public university handbooks only | Real language | Licensing unclear; no parametric ground truth | Supplement only |

## References

- `data/schemas/` — JSON schemas for companies, policies, eval Q&A
- `scripts/data_generation/` — generation scripts
- `docs/architecture/design.md` — data model
