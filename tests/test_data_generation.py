from scripts.data_generation.common import (
    build_policy_metadata,
    load_companies,
    make_doc_id,
    sample_parameters,
    validate_against_schema,
)
from scripts.data_generation.generate_eval_qa import generate_golden_qa
from scripts.data_generation.generate_policies import generate_policy_document
from scripts.data_generation.render_pdf import render_policy_html


def test_load_companies_validates_schema() -> None:
    companies = load_companies()
    assert len(companies) == 5
    assert companies[0]["company_id"] == "novatech-solutions"


def test_sample_parameters_respect_ranges() -> None:
    params = sample_parameters("leave_policy")
    assert 12 <= params["annual_leave_days"] <= 30
    assert 1 <= params["probation_months"] <= 6


def test_build_policy_metadata_matches_schema() -> None:
    company = load_companies()[0]
    params = sample_parameters("leave_policy")
    metadata = build_policy_metadata(company, "leave_policy", params)
    assert metadata["doc_id"] == make_doc_id(company["company_id"], "leave_policy", "2024-01")
    validate_against_schema(metadata, "policy.schema.json")


def test_generate_policy_document_dry_run() -> None:
    company = load_companies()[0]
    metadata, sections = generate_policy_document(company, "leave_policy", dry_run=True)
    assert metadata["policy_type"] == "leave_policy"
    assert len(sections) == 5
    assert "annual_leave_entitlement" in sections


def test_render_policy_html_contains_header_fields() -> None:
    company = load_companies()[0]
    metadata, sections = generate_policy_document(company, "benefits", dry_run=True)
    html = render_policy_html(metadata, sections, company["name"])
    assert company["name"] in html
    assert metadata["doc_id"] in html
    assert "1." in html


def test_generate_golden_qa_count_and_unanswerable() -> None:
    companies = load_companies()
    policies = [
        build_policy_metadata(company, policy_type, sample_parameters(policy_type))
        for company in companies
        for policy_type in [
            "leave_policy",
            "remote_work",
            "code_of_conduct",
            "benefits",
            "expense",
            "performance",
            "onboarding",
            "termination",
            "data_security",
            "travel",
        ]
    ]
    items = generate_golden_qa(companies, policies, unanswerable_count=10)
    assert len(items) == 80
    assert sum(1 for item in items if not item["answerable"]) == 10
    assert all(item["id"].startswith("eval-") for item in items)
