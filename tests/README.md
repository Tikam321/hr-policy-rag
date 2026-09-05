# Tests

| Directory | Scope |
|-----------|-------|
| `unit/` | Individual module tests (chunker, reranker, citations) |
| `integration/` | End-to-end pipeline tests (ingest → query) |
| `fixtures/` | Sample PDFs and test data |

Run: `make test`

Eval targets (Phase 7):
- Recall@5 ≥ 0.85
- Citation accuracy ≥ 0.90
- Faithfulness ≥ 0.80
