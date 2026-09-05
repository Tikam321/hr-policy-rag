"""Generate golden eval Q&A items from known policy parameters."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from typing import Any

from scripts.data_generation.common import (
    validate_against_schema,
)

EvalItem = dict[str, Any]
QuestionFactory = Callable[[dict[str, Any], dict[str, Any]], EvalItem | None]


def _easy_question(
    item_id: str,
    company: dict[str, Any],
    metadata: dict[str, Any],
    *,
    question: str,
    expected_bits: list[str],
    source_section: str,
    policy_type: str | None = None,
) -> EvalItem:
    item: EvalItem = {
        "id": item_id,
        "question": question,
        "expected_answer_contains": expected_bits,
        "source_doc_id": metadata["doc_id"],
        "source_section": source_section,
        "company_id": company["company_id"],
        "difficulty": "easy",
        "answerable": True,
        "category": "factual",
    }
    if policy_type:
        item["policy_type"] = policy_type
    return item


def _unanswerable_question(
    item_id: str,
    company: dict[str, Any],
    *,
    question: str,
) -> EvalItem:
    item: EvalItem = {
        "id": item_id,
        "question": question,
        "company_id": company["company_id"],
        "difficulty": "hard",
        "answerable": False,
        "category": "unanswerable",
    }
    return item


def _leave_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    days = metadata["parameters"]["annual_leave_days"]
    return _easy_question(
        "",
        company,
        metadata,
        question=(
            f"How many paid annual leave days do full-time employees receive at {company['name']}?"
        ),
        expected_bits=[str(days), "days"],
        source_section="Annual Leave Entitlement",
        policy_type="leave_policy",
    )


def _remote_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    days = metadata["parameters"]["remote_days_per_week"]
    return _easy_question(
        "",
        company,
        metadata,
        question=f"How many remote work days per week are allowed at {company['name']}?",
        expected_bits=[str(days)],
        source_section="Remote Schedule",
        policy_type="remote_work",
    )


def _conduct_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    months = metadata["parameters"]["training_frequency_months"]
    return _easy_question(
        "",
        company,
        metadata,
        question=(
            f"How often must employees complete code of conduct training "
            f"at {company['name']}?"
        ),
        expected_bits=[str(months), "month"],
        source_section="Training and Acknowledgment",
        policy_type="code_of_conduct",
    )


def _benefits_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    pct = metadata["parameters"]["health_insurance_coverage_pct"]
    return _easy_question(
        "",
        company,
        metadata,
        question=(
            f"What percentage of health insurance premiums does {company['name']} "
            "cover for employees?"
        ),
        expected_bits=[str(pct), "%"],
        source_section="Health and Dental Coverage",
        policy_type="benefits",
    )


def _expense_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    days = metadata["parameters"]["expense_reimbursement_days"]
    return _easy_question(
        "",
        company,
        metadata,
        question=(
            f"Within how many business days does {company['name']} "
            "reimburse approved expenses?"
        ),
        expected_bits=[str(days), "days"],
        source_section="Receipts and Submission",
        policy_type="expense",
    )


def _performance_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    months = metadata["parameters"]["review_cycle_months"]
    return _easy_question(
        "",
        company,
        metadata,
        question=f"How frequently are formal performance reviews conducted at {company['name']}?",
        expected_bits=[str(months), "month"],
        source_section="Review Cycle and Ratings",
        policy_type="performance",
    )


def _onboarding_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    days = metadata["parameters"]["onboarding_duration_days"]
    return _easy_question(
        "",
        company,
        metadata,
        question=(
            f"How long is the structured onboarding program at {company['name']} "
            "in business days?"
        ),
        expected_bits=[str(days), "days"],
        source_section="Onboarding Program Timeline",
        policy_type="onboarding",
    )


def _termination_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    days = metadata["parameters"]["notice_period_days"]
    return _easy_question(
        "",
        company,
        metadata,
        question=(
            f"What is the required notice period for voluntary resignation "
            f"at {company['name']}?"
        ),
        expected_bits=[str(days), "days"],
        source_section="Notice Period",
        policy_type="termination",
    )


def _security_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    length = metadata["parameters"]["password_min_length"]
    return _easy_question(
        "",
        company,
        metadata,
        question=(
            f"What is the minimum password length for corporate accounts "
            f"at {company['name']}?"
        ),
        expected_bits=[str(length)],
        source_section="Account and Password Standards",
        policy_type="data_security",
    )


def _travel_question(company: dict[str, Any], metadata: dict[str, Any]) -> EvalItem:
    per_diem = metadata["parameters"]["per_diem_usd"]
    return _easy_question(
        "",
        company,
        metadata,
        question=f"What is the domestic per diem allowance at {company['name']}?",
        expected_bits=[str(per_diem), "$"],
        source_section="Per Diem and Lodging",
        policy_type="travel",
    )


QUESTION_BY_POLICY: dict[str, QuestionFactory] = {
    "leave_policy": _leave_question,
    "remote_work": _remote_question,
    "code_of_conduct": _conduct_question,
    "benefits": _benefits_question,
    "expense": _expense_question,
    "performance": _performance_question,
    "onboarding": _onboarding_question,
    "termination": _termination_question,
    "data_security": _security_question,
    "travel": _travel_question,
}

UNANSWERABLE_TEMPLATES = [
    "What is the employee stock option vesting schedule at {name}?",
    "What is the exact office cafeteria subsidy amount at {name}?",
    "What is the CEO's personal email address at {name}?",
    "How many parking spots are reserved for employees at {name}?",
    "What was the company's total revenue last quarter at {name}?",
    "What is the pet insurance coverage at {name}?",
    "What is the company match for charitable donations at {name}?",
    "What is the on-site childcare tuition subsidy at {name}?",
    "What is the executive jet travel policy for interns at {name}?",
    "What is the company policy on moonlighting at second jobs for {name}?",
]


def _medium_leave_benefits(
    item_id: str,
    company: dict[str, Any],
    leave_meta: dict[str, Any],
    benefits_meta: dict[str, Any],
) -> EvalItem:
    leave_days = leave_meta["parameters"]["annual_leave_days"]
    waiting = benefits_meta["parameters"]["waiting_period_days"]
    item: EvalItem = {
        "id": item_id,
        "question": (
            f"At {company['name']}, how many annual leave days are offered and how long is the "
            f"benefits waiting period for new hires?"
        ),
        "expected_answer_contains": [str(leave_days), str(waiting), "days"],
        "source_doc_ids": [leave_meta["doc_id"], benefits_meta["doc_id"]],
        "company_id": company["company_id"],
        "difficulty": "medium",
        "answerable": True,
        "category": "cross_policy",
    }
    return item


def _medium_expense_travel(
    item_id: str,
    company: dict[str, Any],
    expense_meta: dict[str, Any],
    travel_meta: dict[str, Any],
) -> EvalItem:
    reimbursement = expense_meta["parameters"]["expense_reimbursement_days"]
    per_diem = travel_meta["parameters"]["per_diem_usd"]
    item: EvalItem = {
        "id": item_id,
        "question": (
            f"What are the expense reimbursement timelines and domestic per diem "
            f"rates at {company['name']}?"
        ),
        "expected_answer_contains": [str(reimbursement), str(per_diem)],
        "source_doc_ids": [expense_meta["doc_id"], travel_meta["doc_id"]],
        "company_id": company["company_id"],
        "difficulty": "medium",
        "answerable": True,
        "category": "cross_policy",
    }
    return item


def _medium_performance_onboarding(
    item_id: str,
    company: dict[str, Any],
    performance_meta: dict[str, Any],
    onboarding_meta: dict[str, Any],
) -> EvalItem:
    probation = performance_meta["parameters"]["probation_months"]
    onboarding_days = onboarding_meta["parameters"]["onboarding_duration_days"]
    item: EvalItem = {
        "id": item_id,
        "question": (
            f"How long is probation and the structured onboarding program at {company['name']}?"
        ),
        "expected_answer_contains": [str(probation), str(onboarding_days)],
        "source_doc_ids": [performance_meta["doc_id"], onboarding_meta["doc_id"]],
        "company_id": company["company_id"],
        "difficulty": "medium",
        "answerable": True,
        "category": "multi_section",
    }
    return item


def _medium_security_conduct(
    item_id: str,
    company: dict[str, Any],
    security_meta: dict[str, Any],
    conduct_meta: dict[str, Any],
) -> EvalItem:
    mfa = security_meta["parameters"]["mfa_required"]
    hotline = conduct_meta["parameters"]["whistleblower_hotline"]
    item: EvalItem = {
        "id": item_id,
        "question": (
            f"Is MFA required and is a whistleblower hotline available at {company['name']}?"
        ),
        "expected_answer_contains": [str(mfa).lower(), str(hotline).lower()],
        "source_doc_ids": [security_meta["doc_id"], conduct_meta["doc_id"]],
        "company_id": company["company_id"],
        "difficulty": "medium",
        "answerable": True,
        "category": "cross_policy",
    }
    return item


def _policy_map(company_policies: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {policy["policy_type"]: policy for policy in company_policies}


def generate_golden_qa(
    companies: list[dict[str, Any]],
    policies: list[dict[str, Any]],
    *,
    unanswerable_count: int = 10,
) -> list[EvalItem]:
    items: list[EvalItem] = []
    counter = 1

    policies_by_company: dict[str, list[dict[str, Any]]] = {}
    for policy in policies:
        policies_by_company.setdefault(policy["company_id"], []).append(policy)

    for policy in policies:
        factory = QUESTION_BY_POLICY[policy["policy_type"]]
        item = factory(company=_company_for(companies, policy["company_id"]), metadata=policy)
        item["id"] = f"eval-{counter:03d}"
        items.append(item)
        counter += 1

    for company in companies:
        company_policies = policies_by_company.get(company["company_id"], [])
        policy_map = _policy_map(company_policies)
        medium_builders = [
            (
                ("leave_policy", "benefits"),
                lambda: _medium_leave_benefits(
                    "",
                    company,
                    policy_map["leave_policy"],
                    policy_map["benefits"],
                ),
            ),
            (
                ("expense", "travel"),
                lambda: _medium_expense_travel(
                    "",
                    company,
                    policy_map["expense"],
                    policy_map["travel"],
                ),
            ),
            (
                ("performance", "onboarding"),
                lambda: _medium_performance_onboarding(
                    "",
                    company,
                    policy_map["performance"],
                    policy_map["onboarding"],
                ),
            ),
            (
                ("data_security", "code_of_conduct"),
                lambda: _medium_security_conduct(
                    "",
                    company,
                    policy_map["data_security"],
                    policy_map["code_of_conduct"],
                ),
            ),
        ]
        for required_types, builder in medium_builders:
            if any(ptype not in policy_map for ptype in required_types):
                continue
            item = builder()
            item["id"] = f"eval-{counter:03d}"
            items.append(item)
            counter += 1

    for idx, company in enumerate(companies):
        if idx >= unanswerable_count:
            break
        template = UNANSWERABLE_TEMPLATES[idx % len(UNANSWERABLE_TEMPLATES)]
        item = _unanswerable_question(
            f"eval-{counter:03d}",
            company,
            question=template.format(name=company["name"]),
        )
        items.append(item)
        counter += 1

    while len([i for i in items if not i["answerable"]]) < unanswerable_count:
        company = companies[len(items) % len(companies)]
        template = UNANSWERABLE_TEMPLATES[len(items) % len(UNANSWERABLE_TEMPLATES)]
        item = _unanswerable_question(
            f"eval-{counter:03d}",
            company,
            question=template.format(name=company["name"]),
        )
        items.append(item)
        counter += 1

    for item in items:
        validate_against_schema(item, "eval_qa.schema.json")
    return items


def _company_for(companies: list[dict[str, Any]], company_id: str) -> dict[str, Any]:
    return next(c for c in companies if c["company_id"] == company_id)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate golden eval Q&A from policy metadata.")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    from scripts.data_generation.common import configure_logging, load_companies

    configure_logging(args.log_level)
    print("Use batch_generate.py to produce policies and golden Q&A together.")
    _ = load_companies()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
