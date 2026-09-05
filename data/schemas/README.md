# JSON Schemas

Data contracts for synthetic generation, ingestion, and evaluation.

| Schema | Validates | Used in |
|--------|-----------|---------|
| [company.schema.json](./company.schema.json) | Company seed profiles | Phase 1.2 seed data |
| [policy.schema.json](./policy.schema.json) | Policy document metadata | Phase 1.5 metadata JSON |
| [chunk.schema.json](./chunk.schema.json) | Ingested chunk payloads | Phase 2 ingestion |
| [eval_qa.schema.json](./eval_qa.schema.json) | Golden eval Q&A items | Phase 1.5, Phase 7 eval |

Validate with `jsonschema` (Python) or any Draft 2020-12 compatible validator.

```bash
# Example (after pip install jsonschema)
python -c "
import json, jsonschema
schema = json.load(open('data/schemas/company.schema.json'))
data = json.load(open('data/seed/companies.json'))  # array or single — adjust validator wrapper
"
```

Policy type enum values match ADR-002 and `docs/architecture/design.md`.
