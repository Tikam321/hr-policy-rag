# Interview Guide & Session Continuity

> How to hand off work between coding agent sessions and explain this project in interviews.

---

## Session Continuity

### Files That Preserve Context

| File | Updated when | Purpose |
|------|--------------|---------|
| `AGENTS.md` | Phase changes | Current status, conventions |
| `docs/IMPLEMENTATION.md` | Step completed | **Checkboxes — primary progress tracker** |
| `docs/SESSION_LOG.md` | Every session | What was done, next steps |
| `docs/adr/*.md` | Design decisions | Trade-offs |
| `.cursor/rules/` | Conventions change | Agent behavior |

### Starting a New Agent Session

```
1. Read AGENTS.md
2. Read docs/SESSION_LOG.md (last entry)
3. Open docs/IMPLEMENTATION.md → find first unchecked [ ] item
4. Implement that item
5. Check off [x], update SESSION_LOG, update AGENTS.md status
```

### Ending an Agent Session

```markdown
## Session YYYY-MM-DD

**Phase:** Phase N — section name
**Completed:**
- [x] item 1
- [x] item 2

**Files changed:** list of files

**Eval results:** (if applicable)

**Next session should:**
- Start with unchecked item X in Phase N
```

---

## Interview Walkthrough Script

Use this 2-minute narrative:

1. **Problem:** HR policy Q&A requires cited, grounded answers
2. **Data:** Synthetic corpus (50→500 PDFs) with ground-truth eval
3. **Ingestion:** Async pipeline, structure-aware chunking, versioned metadata
4. **Retrieval:** Hybrid search + reranking (not pure vector)
5. **Generation:** Citation-required, refusal when insufficient context
6. **Eval:** Golden set, Recall@5, faithfulness, citation accuracy
7. **Ops:** Docker Compose, structured logs, request tracing
8. **Scale:** 500 docs, batch ingest, latency benchmarks

### Strong vs Weak Pitch

**Weak:** "I built a RAG chatbot for HR PDFs."

**Strong:** "I built a versioned HR policy retrieval system with async ingestion, hybrid search plus reranking, citation-required generation, and a golden eval set measuring recall and faithfulness — deployed as containerized services with full request tracing."

---

## Technology Trade-offs

See full rationale in [`../adr/`](../adr/).

| Decision | Chosen | Alternatives considered |
|----------|--------|------------------------|
| Vector DB | Qdrant | pgvector, Weaviate, Chroma |
| BM25 | Qdrant sparse / rank_bm25 | Elasticsearch |
| Worker | Celery + Redis | RQ, Dramatiq |
| UI | Streamlit (MVP) | Next.js |
| Eval | RAGAS + custom | DeepEval, LangSmith |
| Data | Synthetic parameterized | Scraped real PDFs |

### Common Interview Follow-ups

| Question | Strong answer |
|----------|---------------|
| Why hybrid search? | Vector misses exact terms; BM25 catches policy keywords and acronyms |
| How reduce hallucinations? | Context-only prompt, citation requirement, "I don't know" fallback, eval metrics |
| Chunk size? | Structure-based chunks ~300–800 tokens; tested with eval set |
| When to re-embed? | On embedding model change or major parser change; version everything |
| Doc updates? | Soft-delete old chunks, ingest new version, filter by `status=active` |
| Latency budget? | Retrieval <200ms, rerank <100ms, LLM 1–3s |
| Cost control? | Smaller model for rewrite, cache embeddings, batch ingestion, top-k limits |

## Related Docs

- [Overview](./overview.md)
- [Operations](./operations.md)
- [Implementation checklist](../IMPLEMENTATION.md)
