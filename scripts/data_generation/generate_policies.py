"""Generate policy section HTML via LLM or deterministic dry-run stubs."""

from __future__ import annotations

import argparse
import os
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from openai import OpenAI

from scripts.data_generation.common import (
    PROMPTS_DIR,
    build_policy_metadata,
    configure_logging,
    load_companies,
    load_section_outlines,
    logger,
    policy_title,
    rng_for,
    sample_parameters,
)


def _prompt_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(PROMPTS_DIR)),
        autoescape=select_autoescape(enabled_extensions=()),
    )


def _load_system_prompt() -> str:
    return (PROMPTS_DIR / "system.txt").read_text(encoding="utf-8")


def _build_llm_client(model: str | None) -> tuple[OpenAI, str]:
    """Build an OpenAI-compatible client from env config and return (client, model)."""
    max_retries = int(os.getenv("DATA_GENERATION_LLM_MAX_RETRIES", "8"))
    timeout = float(os.getenv("DATA_GENERATION_LLM_TIMEOUT", "60"))
    client_kwargs: dict[str, Any] = {"max_retries": max_retries, "timeout": timeout}
    provider = os.getenv("DATA_GENERATION_LLM_PROVIDER", "openai").strip().lower()
    if provider == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key or api_key.startswith(("sk-your-key", "your-mistral")):
            raise ValueError(
                "MISTRAL_API_KEY is missing or placeholder. Use --dry-run or set a valid key."
            )
        resolved_model = model or os.getenv("DATA_GENERATION_LLM_MODEL", "mistral-medium")
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.mistral.ai/v1/",
            **client_kwargs,
        )
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("sk-your-key"):
            raise ValueError(
                "OPENAI_API_KEY is missing or placeholder. Use --dry-run or set a valid key."
            )
        resolved_model = model or os.getenv("DATA_GENERATION_LLM_MODEL", "gpt-4o-mini")
        client = OpenAI(api_key=api_key, **client_kwargs)
    logger.info("Using LLM provider", extra={"provider": provider, "model": resolved_model})
    return client, resolved_model


def _dry_run_section_html(
    section_title: str,
    parameter_keys: list[str],
    parameters: dict[str, Any],
) -> str:
    parts = [f"<p>This section covers {section_title.lower()}.</p>"]
    if parameter_keys:
        items = "".join(
            f"<li><strong>{key}</strong>: {parameters[key]}</li>"
            for key in parameter_keys
            if key in parameters
        )
        parts.append(f"<ul>{items}</ul>")
    parts.append("<p>Employees should contact HR for exceptions or clarifications.</p>")
    return "\n".join(parts)


def _llm_section_html(
    client: OpenAI,
    model: str,
    company: dict[str, Any],
    policy_type: str,
    parameters: dict[str, Any],
    section: dict[str, Any],
    version: str,
    effective_date: str,
) -> str:
    env = _prompt_env()
    template = env.get_template("generate_section.j2")
    user_prompt = template.render(
        company_name=company["name"],
        company_id=company["company_id"],
        industry=company["industry"],
        region=company["region"],
        size=company["size"],
        employee_count=company["employee_count"],
        policy_type=policy_type,
        policy_title=policy_title(policy_type),
        version=version,
        effective_date=effective_date,
        parameters=parameters,
        required_parameter_keys=section.get("parameter_keys", []),
        section_number=section["number"],
        section_title=section["title"],
        section_instructions=section["instructions"],
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _load_system_prompt()},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )
    content = response.choices[0].message.content or ""
    return content.strip()


def generate_policy_sections(
    company: dict[str, Any],
    policy_type: str,
    parameters: dict[str, Any],
    *,
    dry_run: bool = False,
    model: str | None = None,
    version: str = "2024-01",
    effective_date: str = "2024-04-01",
) -> dict[str, str]:
    outlines = load_section_outlines()[policy_type]["sections"]
    sections: dict[str, str] = {}
    client: OpenAI | None = None

    if not dry_run:
        client, model = _build_llm_client(model)

    for section in outlines:
        key = section["key"]
        parameter_keys = section.get("parameter_keys", [])
        if dry_run:
            sections[key] = _dry_run_section_html(section["title"], parameter_keys, parameters)
        else:
            assert client is not None and model is not None
            logger.info(
                "Generating section",
                extra={
                    "company_id": company["company_id"],
                    "policy_type": policy_type,
                    "section": key,
                },
            )
            sections[key] = _llm_section_html(
                client,
                model,
                company,
                policy_type,
                parameters,
                section,
                version,
                effective_date,
            )
    return sections


def generate_policy_document(
    company: dict[str, Any],
    policy_type: str,
    *,
    dry_run: bool = False,
    model: str | None = None,
    version: str = "2024-01",
    effective_date: str = "2024-04-01",
) -> tuple[dict[str, Any], dict[str, str]]:
    parameters = sample_parameters(policy_type, rng_for(company["company_id"], policy_type))
    metadata = build_policy_metadata(
        company,
        policy_type,
        parameters,
        version=version,
        effective_date=effective_date,
    )
    sections = generate_policy_sections(
        company,
        policy_type,
        parameters,
        dry_run=dry_run,
        model=model,
        version=version,
        effective_date=effective_date,
    )
    return metadata, sections


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate one policy document (metadata + sections)."
    )
    parser.add_argument("--company-id", required=True)
    parser.add_argument("--policy-type", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()
    configure_logging(args.log_level)

    company = next(c for c in load_companies() if c["company_id"] == args.company_id)
    metadata, sections = generate_policy_document(
        company,
        args.policy_type,
        dry_run=args.dry_run,
    )
    print(metadata["doc_id"])
    print(f"sections: {len(sections)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
