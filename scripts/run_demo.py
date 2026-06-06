import json
from pathlib import Path

from snowflake_credit_burn_variance_ledger.ledger import build_summary

summary = build_summary(json.loads(Path("fixtures/credit_burn_variance.json").read_text(encoding="utf-8")))
print(f"estate={summary.estate}")
print(f"variance={summary.aggregate_burn_variance}")
print(f"escalation={summary.escalation_lanes}")
print(f"excess_credits={summary.excess_credit_estimate}")
print(f"recommendation={summary.primary_recommendation}")
