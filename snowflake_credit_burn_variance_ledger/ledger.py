from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

Posture = Literal["escalate", "watch", "contained"]


class BurnLane(TypedDict):
    lane_id: str
    warehouse: str
    monthly_credits: float
    baseline_credits: float
    idle_percent: float
    failed_query_percent: float
    unlabeled_query_percent: float
    auto_suspend_gap_minutes: float
    owner: str
    next_action: str


class BurnInput(TypedDict):
    as_of: str
    estate: str
    lanes: list[BurnLane]


@dataclass(frozen=True)
class BurnFinding:
    lane_id: str
    warehouse: str
    owner: str
    burn_variance_score: float
    excess_credit_estimate: int
    posture: Posture
    next_action: str


@dataclass(frozen=True)
class BurnSummary:
    as_of: str
    estate: str
    aggregate_burn_variance: float
    escalation_lanes: int
    excess_credit_estimate: int
    primary_recommendation: str
    findings: list[BurnFinding]


def _clamp(value: float, lower: float = 0, upper: float = 100) -> float:
    return min(upper, max(lower, value))


def score_lane(lane: BurnLane) -> BurnFinding:
    baseline = max(lane["baseline_credits"], 1)
    credit_delta_ratio = max(0, (lane["monthly_credits"] - baseline) / baseline)
    score = _clamp(
        credit_delta_ratio * 80
        + lane["idle_percent"] * 1.25
        + lane["failed_query_percent"] * 2.5
        + lane["unlabeled_query_percent"] * 1.1
        + lane["auto_suspend_gap_minutes"] * 1.6
    )
    posture: Posture = "escalate" if score >= 70 else "watch" if score >= 40 else "contained"
    excess_credit_estimate = round(max(0, lane["monthly_credits"] - baseline) + lane["monthly_credits"] * lane["idle_percent"] / 100 * 0.35)
    return BurnFinding(
        lane_id=lane["lane_id"],
        warehouse=lane["warehouse"],
        owner=lane["owner"],
        burn_variance_score=round(score, 2),
        excess_credit_estimate=excess_credit_estimate,
        posture=posture,
        next_action=lane["next_action"],
    )


def build_summary(data: BurnInput) -> BurnSummary:
    if not data["lanes"]:
        raise ValueError("At least one Snowflake credit-burn lane is required.")
    findings = sorted((score_lane(lane) for lane in data["lanes"]), key=lambda item: item.burn_variance_score, reverse=True)
    aggregate = round(sum(item.burn_variance_score for item in findings) / len(findings), 2)
    escalation_lanes = sum(1 for item in findings if item.posture == "escalate")
    excess = sum(item.excess_credit_estimate for item in findings)
    top = findings[0]
    return BurnSummary(
        as_of=data["as_of"],
        estate=data["estate"],
        aggregate_burn_variance=aggregate,
        escalation_lanes=escalation_lanes,
        excess_credit_estimate=excess,
        primary_recommendation=f"{top.lane_id}: {top.next_action}",
        findings=findings,
    )
