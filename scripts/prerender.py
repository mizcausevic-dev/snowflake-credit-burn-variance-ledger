import json
from pathlib import Path

from snowflake_credit_burn_variance_ledger.site import render_site

data = json.loads(Path("fixtures/credit_burn_variance.json").read_text(encoding="utf-8"))
Path("site").mkdir(exist_ok=True)
Path("site/index.html").write_text(render_site(data), encoding="utf-8")
