"""Orchestrate synthetic corpus generation: companies × policies → PDFs + metadata + eval."""

from __future__ import annotations

import argparse
import os
from datetime import UTC, datetime
from typing import Any

from scripts.data_generation.common import (
    DOCUMENTS_DIR,
    EVAL_DIR,
    METADATA_DIR,
    POLICY_TYPES,
    PROJECT_ROOT,
    configure_logging,
    load_companies,
    load_json,
    logger,
    make_doc_id,
    save_json,
)
from scripts.data_generation.generate_eval_qa import generate_golden_qa
from scripts.data_generation.generate_policies import generate_policy_document
from scripts.data_generation.render_pdf import render_policy_pdf


def _select_policy_types(count: int) -> list[str]:
    if count <= 0:
        raise ValueError("count must be positive")
    per_company = max(1, count // len(load_companies()))
    per_company = min(per_company, len(POLICY_TYPES))
    return POLICY_TYPES[:per_company]


def generate_corpus(
    *,
    count: int = 50,
    dry_run: bool = False,
    skip_pdf: bool = False,
    resume: bool = False,
    company_ids: list[str] | None = None,
    version: str = "2024-01",
    effective_date: str = "2024-04-01",
) -> dict[str, Any]:
    companies = load_companies()
    if company_ids:
        companies = [c for c in companies if c["company_id"] in company_ids]
    if not companies:
        raise ValueError("No companies selected")

    policy_types = _select_policy_types(count)
    generated_at = datetime.now(tz=UTC).isoformat()
    all_metadata: list[dict[str, Any]] = []
    merged = 0

    for company in companies:
        for policy_type in policy_types:
            metadata_path = METADATA_DIR / (
                f"{make_doc_id(company['company_id'], policy_type, version)}.json"
            )

            if resume and metadata_path.exists():
                logger.info(
                    "Skipping existing document",
                    extra={"doc_id": metadata_path.stem},
                )
                all_metadata.append(load_json(metadata_path))
                merged += 1
                continue

            metadata, sections = generate_policy_document(
                company,
                policy_type,
                dry_run=dry_run,
                version=version,
                effective_date=effective_date,
            )
            metadata["generated_at"] = generated_at
            all_metadata.append(metadata)

            save_json(metadata_path, metadata)

            if not skip_pdf:
                pdf_path = PROJECT_ROOT / metadata["file_path"]
                render_policy_pdf(metadata, sections, company["name"], pdf_path)

    golden_qa = generate_golden_qa(companies, all_metadata)
    eval_path = EVAL_DIR / "golden_qa.json"
    save_json(eval_path, golden_qa)

    summary = {
        "companies": len(companies),
        "policy_types_per_company": len(policy_types),
        "documents": len(all_metadata),
        "resumed_from_existing": merged,
        "eval_questions": len(golden_qa),
        "dry_run": dry_run,
        "skip_pdf": skip_pdf,
        "documents_dir": str(DOCUMENTS_DIR.relative_to(PROJECT_ROOT)),
        "metadata_dir": str(METADATA_DIR.relative_to(PROJECT_ROOT)),
        "eval_path": str(eval_path.relative_to(PROJECT_ROOT)),
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic HR policy corpus.")
    per_company = int(os.getenv("DEFAULT_CORPUS_COMPANIES", "5"))
    parser.add_argument("--count", type=int, default=per_company * 10)
    parser.add_argument(
        "--dry-run", action="store_true", help="Skip LLM; use deterministic section stubs."
    )
    parser.add_argument(
        "--skip-pdf", action="store_true", help="Write metadata only; skip PDF rendering."
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip documents whose metadata file already exists on disk.",
    )
    parser.add_argument("--company-id", action="append", dest="company_ids")
    parser.add_argument("--version", default="2024-01")
    parser.add_argument("--effective-date", default="2024-04-01")
    parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"))
    args = parser.parse_args()
    configure_logging(args.log_level)

    summary = generate_corpus(
        count=args.count,
        dry_run=args.dry_run,
        skip_pdf=args.skip_pdf,
        resume=args.resume,
        company_ids=args.company_ids,
        version=args.version,
        effective_date=args.effective_date,
    )
    logger.info("Corpus generation complete", extra=summary)
    for key, value in summary.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
