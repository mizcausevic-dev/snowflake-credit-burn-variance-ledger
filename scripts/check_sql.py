from pathlib import Path

sql = Path("sql/credit_burn_variance_contract.sql").read_text(encoding="utf-8")
required = [
    "warehouse_metering_history",
    "query_history",
    "warehouse_name",
    "monthly_credits",
    "failed_query_percent",
    "unlabeled_query_percent",
]
missing = [token for token in required if token not in sql]
if missing:
    raise SystemExit(f"SQL contract missing: {', '.join(missing)}")
print("sql contract ok")
