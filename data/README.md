# Data Directory

| Path | Contents | Git tracked? |
|------|----------|--------------|
| `schemas/` | JSON Schema definitions | Yes |
| `templates/` | HTML/policy templates for PDF generation | Yes |
| `seed/` | Seed company profiles | Yes |
| `documents/` | Generated PDF files | No (gitignored at scale) |
| `metadata/` | Per-document metadata JSON | No (gitignored) |
| `eval/golden_qa.json` | Golden eval Q&A set | Yes |
| `eval/eval_results/` | Eval run outputs | No (gitignored) |

See ADR-002 for synthetic data strategy.
