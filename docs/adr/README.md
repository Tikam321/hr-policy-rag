# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the HR Policy RAG project.

## What is an ADR?

An ADR documents a significant architectural decision: the context, the decision, and the consequences. ADRs preserve **why** we chose something — critical for cross-session agent continuity and interview explanations.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [000](./000-template.md) | ADR Template | — |
| [001](./001-tech-stack.md) | Tech Stack Selection | accepted |
| [002](./002-synthetic-data.md) | Synthetic Data Strategy | accepted |
| [003](./003-vector-db.md) | Vector Database Selection | accepted |

## When to Create a New ADR

Create a new ADR when:

- Choosing between technologies (DB, framework, embedding model)
- Changing an accepted decision (supersede with new ADR)
- Making trade-offs that future sessions need to understand
- Adding a significant new component (e.g., switching from Streamlit to Next.js)

Do **not** create ADRs for trivial choices (variable names, file layout details covered in `docs/architecture/design.md`).

## Naming Convention

```
NNN-short-kebab-title.md
```

Example: `004-reranker-model.md`

## Status Values

- **proposed** — under discussion
- **accepted** — current decision
- **deprecated** — no longer applies (link to superseding ADR)
- **superseded** — replaced by newer ADR

## For Coding Agents

Before changing any accepted ADR decision, either:

1. Create a new ADR that supersedes the old one, or
2. Ask the user for confirmation

Never silently revert architectural decisions.
