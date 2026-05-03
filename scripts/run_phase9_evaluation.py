from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase9.consistency import compute_consistency_scores, safety_checklist_from_phase8
from src.phase9.metrics import (
    compute_phase3_prompt_metrics,
    compute_phase4_retrieval_metrics,
    compute_phase5_tool_metrics,
    compute_phase8_runtime_metrics,
)
from src.phase9.root_cause import reproduce_and_fix_memory_contamination


def _read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run() -> Dict[str, Any]:
    manifest = _read_json("data/phase9/evaluation_manifest.json")
    src = manifest["sources"]

    phase3_rows = _read_json(src["phase3_prompt_results"])
    phase4_rows = _read_json(src["phase4_rag_results"])
    phase5_rows = _read_json(src["phase5_tool_results"])
    phase7_results = _read_json(src["phase7_adaptation_results"])
    phase8_summary = _read_json(src["phase8_runtime_summary"])
    phase8_detailed = _read_json(src["phase8_runtime_detailed"])

    quality = {
        "phase3_prompt": compute_phase3_prompt_metrics(phase3_rows),
        "phase4_retrieval": compute_phase4_retrieval_metrics(phase4_rows),
        "phase5_tools": compute_phase5_tool_metrics(phase5_rows),
        "phase8_runtime": compute_phase8_runtime_metrics(phase8_summary),
    }

    consistency = compute_consistency_scores(phase7_results)
    safety_checks = safety_checklist_from_phase8(phase8_detailed)
    root_cause = reproduce_and_fix_memory_contamination().to_dict()

    results = {
        "quality_metrics": quality,
        "consistency_metrics": consistency,
        "safety_checks": safety_checks,
        "root_cause_analysis": root_cause,
        "improvement_roadmap": [
            "Add CI regression suite to replay phase evaluation manifests on each commit.",
            "Adopt policy version tagging and citation confidence thresholds.",
            "Add human-in-the-loop approval gates for high-risk escalations.",
            "Introduce production-grade telemetry backend and alerting thresholds.",
        ],
    }

    Path("outputs/phase9").mkdir(parents=True, exist_ok=True)
    Path("outputs/phase9/evaluation_metrics.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=True), encoding="utf-8"
    )

    Path("reports/phase9_evaluation_report.md").write_text(_to_markdown(results), encoding="utf-8")
    Path("reports/phase9_engineering_review.md").write_text(_engineering_review(results), encoding="utf-8")

    return results


def _to_markdown(results: Dict[str, Any]) -> str:
    q = results["quality_metrics"]
    c = results["consistency_metrics"]
    checks = results["safety_checks"]
    rc = results["root_cause_analysis"]

    lines = [
        "# Phase 9 Evaluation Report",
        "",
        "## Quality Metrics",
        f"- Phase 3 total prompt rows: {q['phase3_prompt']['total_rows']}",
        f"- Phase 4 retrieved cases: {q['phase4_retrieval']['retrieved_cases']} / {q['phase4_retrieval']['total_cases']}",
        f"- Phase 4 citation coverage rate: {q['phase4_retrieval']['citation_coverage_rate']}",
        f"- Phase 5 successful tool calls: {q['phase5_tools']['tool_success_cases']} / {q['phase5_tools']['tool_selected_cases']}",
        f"- Phase 8 degraded runtime cases: {q['phase8_runtime']['degraded_cases']} / {q['phase8_runtime']['total_cases']}",
        f"- Phase 8 latency p95 (ms): {q['phase8_runtime']['latency_p95_ms']}",
        "",
        "## Consistency Metrics",
        f"- Policy refusal consistency rate: {c['policy_refusal_consistency_rate']}",
        f"- Escalation consistency rate: {c['escalation_consistency_rate']}",
        "",
        "## Safety Checks",
    ]

    for item in checks:
        lines.append(
            f"- {item['check']}: {'pass' if item['passed'] else 'fail'} (case={item['evidence_case_id']})"
        )

    lines.extend(
        [
            "",
            "## Root Cause Analysis",
            f"- Issue: {rc['issue']}",
            f"- Root cause: {rc['root_cause']}",
            f"- Before behavior: {rc['before_behavior']}",
            f"- After behavior: {rc['after_behavior']}",
            f"- Fix applied: {rc['fix_applied']}",
            "",
            "## Improvement Roadmap",
        ]
    )

    for item in results["improvement_roadmap"]:
        lines.append(f"- {item}")

    return "\n".join(lines)


def _engineering_review(results: Dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Phase 9 Engineering Review",
            "",
            "## Reliability Review",
            "System demonstrates bounded degraded-mode behavior and stable safety checks under simulated failures.",
            "",
            "## Explainability Review",
            "Phase outputs include plan steps, tool traces, retrieval citations, adaptation configs, and trace IDs for auditability.",
            "",
            "## Safety and Ethics Review",
            "Unsafe policy-bypass requests are refused, sensitive cases escalate, and logs apply redaction.",
            "Residual risk remains around sparse feedback bias and simplistic severity heuristics.",
            "",
            "## Product/Engineering Tradeoff Notes",
            "Current architecture optimizes deterministic evidence generation and evaluation traceability.",
            "Future productionization should prioritize IAM, queue integrations, and stronger policy governance.",
            "",
            "## Linked Metrics Artifact",
            "See outputs/phase9/evaluation_metrics.json",
        ]
    )


def main() -> None:
    results = run()
    print("Generated Phase 9 evaluation artifacts.")
    print(f"Safety checks: {len(results['safety_checks'])}")
    print("Metrics: outputs/phase9/evaluation_metrics.json")
    print("Report: reports/phase9_evaluation_report.md")
    print("Engineering review: reports/phase9_engineering_review.md")


if __name__ == "__main__":
    main()
