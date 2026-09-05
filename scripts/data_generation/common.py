"""Shared utilities for synthetic data generation scripts."""

from __future__ import annotations

import json
import logging
import random
from pathlib import Path
from typing import Any

import jsonschema
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
DATA_DIR = PROJECT_ROOT / "data"
SCHEMAS_DIR = DATA_DIR / "schemas"
SEED_DIR = DATA_DIR / "seed"
TEMPLATES_DIR = DATA_DIR / "templates"
POLICY_HTML_DIR = TEMPLATES_DIR / "policy_html"
PROMPTS_DIR = TEMPLATES_DIR / "prompts"
DOCUMENTS_DIR = DATA_DIR / "documents"
METADATA_DIR = DATA_DIR / "metadata"
EVAL_DIR = DATA_DIR / "eval"

POLICY_TYPES = json.loads((SCHEMAS_DIR / "policy.schema.json").read_text())["properties"][
    "policy_type"
]["enum"]

logger = logging.getLogger(__name__)


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_against_schema(data: Any, schema_name: str) -> None:
    schema = load_json(SCHEMAS_DIR / schema_name)
    jsonschema.validate(data, schema)


def load_companies() -> list[dict[str, Any]]:
    companies = load_json(SEED_DIR / "companies.json")
    if not isinstance(companies, list):
        raise ValueError("companies.json must contain a JSON array")
    for company in companies:
        validate_against_schema(company, "company.schema.json")
    return companies


def load_parameter_ranges() -> dict[str, Any]:
    payload = load_json(SEED_DIR / "policy_parameter_ranges.json")
    return payload["policy_types"]


def load_section_outlines() -> dict[str, Any]:
    return load_json(PROMPTS_DIR / "section_outlines.json")


def policy_title(policy_type: str) -> str:
    ranges = load_parameter_ranges()
    return ranges[policy_type]["title"]


def make_doc_id(company_id: str, policy_type: str, version: str) -> str:
    year = version.split("-", maxsplit=1)[0]
    slug = policy_type.replace("_", "-")
    return f"{company_id}-{slug}-{year}"


def make_file_path(company_id: str, policy_type: str, version: str) -> str:
    year = version.split("-", maxsplit=1)[0]
    filename = f"{policy_type}_{year}.pdf"
    return f"data/documents/{company_id}/{filename}"


def sample_parameters(
    policy_type: str,
    rng: random.Random | None = None,
) -> dict[str, Any]:
    ranges = load_parameter_ranges()[policy_type]["parameters"]
    required = load_parameter_ranges()[policy_type]["required_parameters"]
    random_source = rng or random.Random()

    parameters: dict[str, Any] = {}
    for key in required:
        spec = ranges[key]
        param_type = spec["type"]
        if param_type == "integer":
            parameters[key] = random_source.randint(spec["min"], spec["max"])
        elif param_type == "boolean":
            parameters[key] = random_source.choice([True, False])
        elif param_type == "string":
            if "enum" not in spec:
                raise ValueError(f"String parameter {key} missing enum")
            parameters[key] = random_source.choice(spec["enum"])
        else:
            raise ValueError(f"Unsupported parameter type: {param_type}")
    return parameters


def build_policy_metadata(
    company: dict[str, Any],
    policy_type: str,
    parameters: dict[str, Any],
    version: str = "2024-01",
    effective_date: str = "2024-04-01",
    status: str = "active",
) -> dict[str, Any]:
    company_id = company["company_id"]
    doc_id = make_doc_id(company_id, policy_type, version)
    metadata = {
        "doc_id": doc_id,
        "company_id": company_id,
        "policy_type": policy_type,
        "title": policy_title(policy_type),
        "version": version,
        "effective_date": effective_date,
        "status": status,
        "file_path": make_file_path(company_id, policy_type, version),
        "parameters": parameters,
    }
    validate_against_schema(metadata, "policy.schema.json")
    return metadata


def rng_for(company_id: str, policy_type: str) -> random.Random:
    seed = hash((company_id, policy_type)) & 0xFFFFFFFF
    return random.Random(seed)
