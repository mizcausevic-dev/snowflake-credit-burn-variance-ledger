from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .ledger import BurnInput, build_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Score Snowflake credit-burn variance lanes.")
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    data = json.loads(args.fixture.read_text(encoding="utf-8"))
    summary = build_summary(data)  # type: ignore[arg-type]

    if args.format == "json":
        print(json.dumps(asdict(summary), indent=2))
        return

    print(f"estate={summary.estate}")
    print(f"variance={summary.aggregate_burn_variance}")
    print(f"escalation={summary.escalation_lanes}")
    print(f"excess_credits={summary.excess_credit_estimate}")
    print(f"recommendation={summary.primary_recommendation}")


if __name__ == "__main__":
    main()
