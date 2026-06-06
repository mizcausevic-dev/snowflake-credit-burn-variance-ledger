from pathlib import Path

html = Path("site/index.html").read_text(encoding="utf-8")
markers = [
    "Snowflake Credit Burn Variance Ledger",
    "Credit burn variance becomes visible",
    "bi-executive-warehouse",
    "elt-transform-warehouse",
]
missing = [marker for marker in markers if marker not in html]
if missing:
    raise SystemExit(f"Rendered site missing markers: {', '.join(missing)}")
print("smoke ok")
