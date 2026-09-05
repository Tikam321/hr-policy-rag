"""Load and validate seed company profiles."""

from __future__ import annotations

import argparse
import json
import sys

from scripts.data_generation.common import configure_logging, load_companies, logger


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and load seed company profiles.")
    parser.add_argument(
        "--output",
        choices=["summary", "json"],
        default="summary",
        help="Print a summary or full JSON to stdout.",
    )
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()
    configure_logging(args.log_level)

    companies = load_companies()
    logger.info("Loaded %s companies", len(companies))

    if args.output == "json":
        json.dump(companies, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for company in companies:
            print(
                f"{company['company_id']}: {company['name']} "
                f"({company['industry']}, {company['region']}, {company['size']})"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
