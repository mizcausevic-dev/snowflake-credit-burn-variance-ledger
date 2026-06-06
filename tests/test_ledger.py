import json
import unittest
from pathlib import Path

from snowflake_credit_burn_variance_ledger.ledger import build_summary, score_lane


FIXTURE = json.loads(Path("fixtures/credit_burn_variance.json").read_text(encoding="utf-8"))


class SnowflakeCreditBurnLedgerTests(unittest.TestCase):
    def test_prioritizes_bi_executive_warehouse(self) -> None:
        summary = build_summary(FIXTURE)
        self.assertEqual(summary.escalation_lanes, 1)
        self.assertEqual(summary.findings[0].lane_id, "bi-executive-warehouse")
        self.assertIn("Reduce idle BI warehouse windows", summary.primary_recommendation)

    def test_transform_warehouse_is_watch(self) -> None:
        finding = score_lane(FIXTURE["lanes"][1])
        self.assertEqual(finding.posture, "watch")
        self.assertEqual(finding.burn_variance_score, 57.88)

    def test_sandbox_is_contained(self) -> None:
        finding = score_lane(FIXTURE["lanes"][2])
        self.assertEqual(finding.posture, "contained")

    def test_requires_at_least_one_lane(self) -> None:
        with self.assertRaisesRegex(ValueError, "At least one Snowflake credit-burn lane is required."):
            build_summary({"as_of": "2026-06-06T14:00:00Z", "estate": "empty", "lanes": []})

    def test_clean_warehouse_is_contained(self) -> None:
        finding = score_lane(
            {
                "lane_id": "reporting-small",
                "warehouse": "REPORTING_SMALL_WH",
                "monthly_credits": 100,
                "baseline_credits": 98,
                "idle_percent": 1,
                "failed_query_percent": 0,
                "unlabeled_query_percent": 2,
                "auto_suspend_gap_minutes": 1,
                "owner": "Analytics",
                "next_action": "Keep controls attached.",
            }
        )
        self.assertEqual(finding.posture, "contained")


if __name__ == "__main__":
    unittest.main()
