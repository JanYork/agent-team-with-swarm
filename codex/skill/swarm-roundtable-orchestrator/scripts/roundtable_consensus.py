#!/usr/bin/env python3
"""
Aggregate roundtable scoring into a deterministic decision report.
"""

import argparse
import json
import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple


DEFAULT_WEIGHTS = {
    "impact": 0.25,
    "feasibility": 0.25,
    "risk_control": 0.20,
    "time_to_value": 0.15,
    "maintainability": 0.15,
}

DEFAULT_HARD_VETO_ROLES = {"qa_engineer", "devops_engineer", "software_architect", "cto"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute weighted consensus for multi-expert roundtable scoring."
    )
    parser.add_argument("--input", required=True, help="Path to input scores JSON.")
    parser.add_argument(
        "--output",
        default="",
        help="Optional output path for rendered report.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--min-consensus",
        type=float,
        default=0.67,
        help="Minimum approval ratio for decision acceptance.",
    )
    parser.add_argument(
        "--approval-bar",
        type=float,
        default=3.5,
        help="Per-expert score threshold (1-5 scale) counted as approval.",
    )
    parser.add_argument(
        "--max-score",
        type=float,
        default=5.0,
        help="Maximum score value in the scoring scale.",
    )
    parser.add_argument(
        "--tie-margin",
        type=float,
        default=0.20,
        help="If top-2 aggregate score delta is below this value, request round 2.",
    )
    parser.add_argument(
        "--hard-veto-roles",
        default="qa_engineer,devops_engineer,software_architect,cto",
        help="Comma-separated role list whose veto blocks acceptance.",
    )
    return parser.parse_args()


def load_input(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "experts" not in data or not isinstance(data["experts"], list):
        raise ValueError("Input JSON must include an 'experts' list.")
    return data


def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    if not weights:
        weights = DEFAULT_WEIGHTS
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("criteria_weights total must be positive.")
    return {k: v / total for k, v in weights.items()}


def parse_veto_items(raw_veto: Any) -> List[Dict[str, str]]:
    if raw_veto is None:
        return []
    normalized: List[Dict[str, str]] = []
    if isinstance(raw_veto, list):
        for item in raw_veto:
            if isinstance(item, dict):
                option = str(item.get("option", "")).strip()
                reason = str(item.get("reason", "")).strip()
                if option:
                    normalized.append({"option": option, "reason": reason})
            elif isinstance(item, str):
                option = item.strip()
                if option:
                    normalized.append({"option": option, "reason": ""})
    return normalized


def collect_option_ids(data: Dict[str, Any]) -> List[str]:
    option_ids = set()
    if isinstance(data.get("options"), list):
        for item in data["options"]:
            if isinstance(item, dict) and item.get("id"):
                option_ids.add(str(item["id"]))
            elif isinstance(item, str):
                option_ids.add(item)

    for expert in data["experts"]:
        scores = expert.get("scores", {})
        if isinstance(scores, dict):
            option_ids.update(scores.keys())

    if not option_ids:
        raise ValueError("No options found. Provide options or expert scores.")
    return sorted(option_ids)


def expert_option_score(
    option_scores: Dict[str, Any],
    criteria_weights: Dict[str, float],
    max_score: float,
) -> float:
    weighted_sum = 0.0
    for criterion, weight in criteria_weights.items():
        raw_score = option_scores.get(criterion, 0)
        try:
            score = float(raw_score)
        except (TypeError, ValueError):
            score = 0.0
        score = max(0.0, min(score, max_score))
        weighted_sum += score * weight
    return weighted_sum


def stdev(values: List[float]) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def compute_consensus(
    data: Dict[str, Any],
    min_consensus: float,
    approval_bar: float,
    max_score: float,
    tie_margin: float,
    hard_veto_roles: List[str],
) -> Dict[str, Any]:
    criteria_weights = normalize_weights(data.get("criteria_weights", DEFAULT_WEIGHTS))
    option_ids = collect_option_ids(data)
    hard_veto = set(role.strip() for role in hard_veto_roles if role.strip()) or DEFAULT_HARD_VETO_ROLES

    per_option: Dict[str, Dict[str, Any]] = {
        option_id: {
            "option": option_id,
            "expert_scores": [],
            "weighted_sum": 0.0,
            "weight_total": 0.0,
            "approvals": 0,
            "vetoes": [],
            "blocked_by_hard_veto": False,
        }
        for option_id in option_ids
    }

    expert_count = 0
    for expert in data["experts"]:
        scores = expert.get("scores", {})
        if not isinstance(scores, dict):
            continue
        expert_name = str(expert.get("expert") or expert.get("name") or "expert").strip()
        expert_weight = float(expert.get("weight", 1.0))
        expert_weight = max(0.0, expert_weight)
        expert_count += 1

        role_hint = str(expert.get("role") or expert_name).strip()
        vetoes = parse_veto_items(expert.get("veto"))
        veto_by_option = {}
        for veto in vetoes:
            option = veto["option"]
            veto_by_option.setdefault(option, []).append(veto["reason"])

        for option_id in option_ids:
            option_score_map = scores.get(option_id, {})
            if not isinstance(option_score_map, dict):
                option_score_map = {}
            score = expert_option_score(option_score_map, criteria_weights, max_score)

            option_entry = per_option[option_id]
            option_entry["expert_scores"].append({"expert": expert_name, "score": round(score, 4)})
            option_entry["weighted_sum"] += score * expert_weight
            option_entry["weight_total"] += expert_weight
            if score >= approval_bar:
                option_entry["approvals"] += 1

            if option_id in veto_by_option:
                for reason in veto_by_option[option_id]:
                    option_entry["vetoes"].append(
                        {"expert": expert_name, "role": role_hint, "reason": reason}
                    )
                if role_hint in hard_veto:
                    option_entry["blocked_by_hard_veto"] = True

    if expert_count == 0:
        raise ValueError("No valid expert scoring rows found.")

    rankings: List[Dict[str, Any]] = []
    for option_id, entry in per_option.items():
        score = (
            entry["weighted_sum"] / entry["weight_total"]
            if entry["weight_total"] > 0
            else 0.0
        )
        approval_ratio = entry["approvals"] / expert_count
        dispersion = stdev([item["score"] for item in entry["expert_scores"]])
        rankings.append(
            {
                "option": option_id,
                "aggregate_score": round(score, 4),
                "approval_ratio": round(approval_ratio, 4),
                "disagreement_index": round(dispersion, 4),
                "blocked_by_hard_veto": entry["blocked_by_hard_veto"],
                "veto_count": len(entry["vetoes"]),
                "vetoes": entry["vetoes"],
                "expert_scores": entry["expert_scores"],
            }
        )

    rankings.sort(
        key=lambda x: (
            x["blocked_by_hard_veto"],
            -x["approval_ratio"],
            -x["aggregate_score"],
            x["disagreement_index"],
            x["veto_count"],
        )
    )

    top = rankings[0]
    second = rankings[1] if len(rankings) > 1 else None
    score_gap = (
        abs(top["aggregate_score"] - second["aggregate_score"])
        if second
        else None
    )

    decision = "accept_top_option"
    reason = "Top option passed consensus and veto checks."
    if top["blocked_by_hard_veto"]:
        decision = "blocked_by_hard_veto"
        reason = "Top-ranked option has hard veto. Run targeted redesign."
    elif top["approval_ratio"] < min_consensus:
        decision = "run_round_2"
        reason = "Approval ratio below minimum consensus threshold."
    elif score_gap is not None and score_gap < tie_margin:
        decision = "run_round_2"
        reason = "Top-2 options too close. Run focused roundtable on finalists."

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "reason": reason,
        "recommended_option": top["option"],
        "min_consensus": min_consensus,
        "approval_bar": approval_bar,
        "criteria_weights": criteria_weights,
        "hard_veto_roles": sorted(hard_veto),
        "expert_count": expert_count,
        "score_gap_top2": score_gap,
        "rankings": rankings,
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Roundtable Consensus Report")
    lines.append("")
    lines.append(f"- Decision: `{report['decision']}`")
    lines.append(f"- Recommended Option: `{report['recommended_option']}`")
    lines.append(f"- Reason: {report['reason']}")
    lines.append(f"- Experts: {report['expert_count']}")
    lines.append(
        f"- Min Consensus / Approval Bar: {report['min_consensus']} / {report['approval_bar']}"
    )
    if report["score_gap_top2"] is not None:
        lines.append(f"- Top2 Score Gap: {round(report['score_gap_top2'], 4)}")
    lines.append("")
    lines.append("## Ranking")
    lines.append("| Option | Aggregate | Approval | Disagreement | Hard Veto | Veto Count |")
    lines.append("| --- | ---: | ---: | ---: | --- | ---: |")
    for row in report["rankings"]:
        lines.append(
            "| {option} | {aggregate_score:.4f} | {approval_ratio:.4f} | "
            "{disagreement_index:.4f} | {blocked_by_hard_veto} | {veto_count} |".format(
                **row
            )
        )
    lines.append("")
    lines.append("## Machine Readable JSON")
    lines.append("```json")
    lines.append(json.dumps(report, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    data = load_input(args.input)
    hard_veto_roles = [item.strip() for item in args.hard_veto_roles.split(",")]
    report = compute_consensus(
        data=data,
        min_consensus=args.min_consensus,
        approval_bar=args.approval_bar,
        max_score=args.max_score,
        tie_margin=args.tie_margin,
        hard_veto_roles=hard_veto_roles,
    )

    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_markdown(report)
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered)
            if not rendered.endswith("\n"):
                f.write("\n")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
