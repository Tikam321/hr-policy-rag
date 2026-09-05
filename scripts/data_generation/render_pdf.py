"""Render policy HTML templates to PDF via WeasyPrint."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from scripts.data_generation.common import (
    POLICY_HTML_DIR,
    PROJECT_ROOT,
    configure_logging,
    logger,
    policy_title,
)


def html_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(POLICY_HTML_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def render_policy_html(
    metadata: dict[str, Any],
    sections: dict[str, str],
    company_name: str,
) -> str:
    template_name = f"{metadata['policy_type']}.html"
    template = html_env().get_template(template_name)
    return template.render(
        company_name=company_name,
        title=metadata["title"],
        doc_id=metadata["doc_id"],
        version=metadata["version"],
        effective_date=metadata["effective_date"],
        status=metadata["status"],
        policy_type_label=policy_title(metadata["policy_type"]),
        sections=sections,
    )


def render_html_to_pdf(html: str, output_path: Path) -> Path:
    try:
        from weasyprint import HTML
    except OSError as exc:
        raise RuntimeError(
            "WeasyPrint system libraries are missing. Install Pango/Cairo "
            "(see https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) "
            "or run batch generation with --skip-pdf."
        ) from exc
    output_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(PROJECT_ROOT)).write_pdf(str(output_path))
    logger.info("Wrote PDF", extra={"path": str(output_path)})
    return output_path


def render_policy_pdf(
    metadata: dict[str, Any],
    sections: dict[str, str],
    company_name: str,
    output_path: Path | None = None,
) -> Path:
    html = render_policy_html(metadata, sections, company_name)
    target = output_path or (PROJECT_ROOT / metadata["file_path"])
    return render_html_to_pdf(html, target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a saved HTML string or sample policy to PDF."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()
    configure_logging(args.log_level)

    sample_html = "<html><body><h1>Test</h1><p>PDF render smoke test.</p></body></html>"
    render_html_to_pdf(sample_html, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
