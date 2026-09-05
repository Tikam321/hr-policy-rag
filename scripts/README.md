# Scripts

Utility and data generation scripts — not part of the runtime application.

| Script | Purpose | Phase |
|--------|---------|-------|
| `data_generation/generate_companies.py` | Load/validate seed companies | Phase 1 |
| `data_generation/generate_policies.py` | LLM policy text generation | Phase 1 |
| `data_generation/render_pdf.py` | HTML → PDF rendering | Phase 1 |
| `data_generation/generate_eval_qa.py` | Golden Q&A from parameters | Phase 1 |
| `data_generation/batch_generate.py` | Full corpus orchestrator | Phase 1 |

Run via: `make generate-data COUNT=50`
