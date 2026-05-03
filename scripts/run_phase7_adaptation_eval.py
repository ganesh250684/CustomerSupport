from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase7.adaptive_agent import Phase7AdaptiveAgent
from src.phase7.adaptive_policy import AdaptationConfig, derive_adaptation
from src.phase7.feedback_store import FeedbackStore


def run() -> Dict[str, Any]:
    payload = json.loads(Path("data/phase7/adaptation_eval_set.json").read_text(encoding="utf-8"))

    store = FeedbackStore()
    for item in payload["feedback_events"]:
        store.add(
            case_id=item["case_id"],
            user_message=item["user_message"],
            helpful=item["helpful"],
            reason_tag=item["reason_tag"],
        )

    reason_counts = store.reason_counts()
    helpful_ratio = store.helpful_ratio()

    baseline_config = AdaptationConfig(
        escalation_sensitivity="normal",
        response_style="balanced",
        clarification_aggressiveness="normal",
    )
    adapted_config = derive_adaptation(reason_counts, helpful_ratio)

    baseline_agent = Phase7AdaptiveAgent(config=baseline_config)
    adapted_agent = Phase7AdaptiveAgent(config=adapted_config)

    comparisons: List[Dict[str, Any]] = []
    for test in payload["before_after_test_prompts"]:
        before = baseline_agent.respond(test["user_message"]).to_dict()
        after = adapted_agent.respond(test["user_message"]).to_dict()
        comparisons.append(
            {
                "id": test["id"],
                "user_message": test["user_message"],
                "before": before,
                "after": after,
            }
        )

    results = {
        "feedback_summary": {
            "total_feedback_events": len(payload["feedback_events"]),
            "helpful_ratio": helpful_ratio,
            "reason_counts": reason_counts,
        },
        "baseline_config": baseline_config.__dict__,
        "adapted_config": adapted_config.__dict__,
        "before_after_comparisons": comparisons,
    }

    Path("outputs/phase7").mkdir(parents=True, exist_ok=True)
    Path("outputs/phase7/adaptation_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    Path("outputs/phase7/feedback_log.jsonl").write_text(
        "\n".join(str(event.to_dict()) for event in store.events),
        encoding="utf-8",
    )

    Path("reports/phase7_adaptation_comparison.md").write_text(
        _to_markdown(results),
        encoding="utf-8",
    )

    return results


def _to_markdown(results: Dict[str, Any]) -> str:
    lines = [
        "# Phase 7 Adaptation Comparison",
        "",
        "Before-vs-after behavior after ingesting feedback signals.",
        "",
        "| Case ID | Prompt | Before | After | What Changed |",
        "|---|---|---|---|---|",
    ]

    for row in results["before_after_comparisons"]:
        before = row["before"]["response"].replace("|", "\\|")[:160]
        after = row["after"]["response"].replace("|", "\\|")[:160]
        changed = []

        if row["before"]["escalate"] != row["after"]["escalate"]:
            changed.append("escalation decision changed")
        if before != after:
            changed.append("response style/content adapted")

        notes = "; ".join(changed) if changed else "no major change"
        lines.append(f"| {row['id']} | {row['user_message']} | {before} | {after} | {notes} |")

    lines.extend(
        [
            "",
            "## Adaptation Configuration",
            f"- Baseline: {results['baseline_config']}",
            f"- Adapted: {results['adapted_config']}",
            "",
            "## Feedback Summary",
            f"- Total events: {results['feedback_summary']['total_feedback_events']}",
            f"- Helpful ratio: {results['feedback_summary']['helpful_ratio']:.2f}",
            f"- Reason counts: {results['feedback_summary']['reason_counts']}",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    results = run()
    print("Generated Phase 7 adaptation evaluation.")
    print(f"Feedback events: {results['feedback_summary']['total_feedback_events']}")
    print(f"Adapted config: {results['adapted_config']}")
    print("Results: outputs/phase7/adaptation_results.json")
    print("Feedback log: outputs/phase7/feedback_log.jsonl")
    print("Table: reports/phase7_adaptation_comparison.md")


if __name__ == "__main__":
    main()
