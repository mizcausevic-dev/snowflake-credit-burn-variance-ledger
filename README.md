# snowflake-credit-burn-variance-ledger

[![ci](https://github.com/mizcausevic-dev/snowflake-credit-burn-variance-ledger/actions/workflows/ci.yml/badge.svg)](https://github.com/mizcausevic-dev/snowflake-credit-burn-variance-ledger/actions/workflows/ci.yml)
[![pages](https://github.com/mizcausevic-dev/snowflake-credit-burn-variance-ledger/actions/workflows/pages.yml/badge.svg)](https://github.com/mizcausevic-dev/snowflake-credit-burn-variance-ledger/actions/workflows/pages.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)

Snowflake credit-burn variance ledger for warehouse spend drift, query waste, idle warehouses, unlabeled work, auto-suspend gaps, and owner accountability.

- Live: https://mizcausevic-dev.github.io/snowflake-credit-burn-variance-ledger/
- Repo: https://github.com/mizcausevic-dev/snowflake-credit-burn-variance-ledger

![Overview proof](screenshots/01-overview-proof.png)
![Ledger proof](screenshots/02-ledger-proof.png)

## What this product does

This product gives finance, RevOps, data engineering, and platform leaders a shared Snowflake cost-governance ledger. Instead of treating warehouse spend drift, query waste, idle time, unlabeled work, and auto-suspend gaps as disconnected admin findings, it turns them into one board-readable view of avoidable credit burn and ownership.

The SaaS go-to-market analyst view is that Snowflake spend is a growth efficiency signal. Data-platform waste can distort campaign analytics, margin narratives, pricing discipline, and investor confidence if leadership sees only high-level cloud spend. The ledger shows where usage is outpacing accountable value.

The SaaS value architect view is focused on the path to savings. It ranks warehouse lanes by burn variance, excess credits, owner, and next remediation action so teams can decide whether to fix labeling, query hygiene, warehouse sizing, idle policies, or auto-suspend posture first.

Technically, the repo demonstrates Snowflake governance proof without production credentials or warehouse data. It includes a Python scoring engine, CLI, synthetic Snowflake warehouse fixture, SQL extraction contract, unit tests, prerendered static surface, screenshot proof, and smoke checks. The shared Kinetic Gain pattern is to convert platform evidence into decision-ready business proof while keeping the technical contract inspectable.

## Why this exists

Snowflake cost governance is not just cheaper warehouses. It is spend variance, failed queries, unlabeled work, idle time, and missing ownership becoming visible before the finance narrative turns into generic cloud-spend noise.

## What it includes

- Python scoring engine and CLI
- synthetic Snowflake warehouse credit-burn fixture
- Snowflake SQL extraction contract
- static GitHub Pages surface
- README proof renders
- CI tests, SQL contract check, prerender smoke test

## Local run

```bash
python -m pip install -e .
python -m unittest discover -s tests
python scripts/run_demo.py
python -m snowflake_credit_burn_variance_ledger.cli fixtures/credit_burn_variance.json --format json
```

## Board-readable output

- aggregate credit-burn variance score
- escalation-lane count
- excess credit estimate
- posture per warehouse lane: `escalate`, `watch`, or `contained`
- primary recommendation tied to the highest-risk warehouse
