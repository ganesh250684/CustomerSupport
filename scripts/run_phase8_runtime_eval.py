from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from src.phase8.service import app


def run() -> Dict[str, Any]:
    cases = json.loads(Path("data/phase8/runtime_eval_cases.json").read_text(encoding="utf-8"))
    client = TestClient(app)

    rows: List[Dict[str, Any]] = []
    latencies: List[float] = []
    error_counts: Dict[str, int] = {}
    degraded_count = 0

    for case in cases:
        resp = client.post("/resolve", json={
            "user_message": case["user_message"],
            "simulate_retrieval_failure": case["simulate_retrieval_failure"],
            "simulate_llm_failure": case["simulate_llm_failure"],
            "simulate_tool_failure": case["simulate_tool_failure"],
        })
        payload = resp.json()
        latencies.append(float(payload["latency_ms"]))

        if payload.get("degraded_mode"):
            degraded_count += 1

        category = payload.get("error_category", "")
        if category:
            error_counts[category] = error_counts.get(category, 0) + 1

        rows.append(
            {
                "id": case["id"],
                "request": case,
                "status_code": resp.status_code,
                "response": payload,
            }
        )

    summary = {
        "total_cases": len(rows),
        "degraded_cases": degraded_count,
        "error_counts": error_counts,
        "latency_ms": {
            "min": min(latencies) if latencies else 0.0,
            "max": max(latencies) if latencies else 0.0,
            "avg": round(statistics.mean(latencies), 2) if latencies else 0.0,
            "p95": _p95(latencies),
        },
    }

    output_payload = {
        "cases": rows,
        "summary": summary,
    }

    Path("outputs/phase8").mkdir(parents=True, exist_ok=True)
    Path("outputs/phase8/deployment_readiness_results.json").write_text(
        json.dumps(output_payload, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    Path("outputs/phase8/latency_error_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    Path("reports/phase8_runtime_comparison.md").write_text(
        _to_markdown(output_payload),
        encoding="utf-8",
    )

    return output_payload


def _p95(values: List[float]) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = max(0, min(len(sorted_vals) - 1, int(0.95 * (len(sorted_vals) - 1))))
    return round(sorted_vals[idx], 2)


def _to_markdown(payload: Dict[str, Any]) -> str:
    lines = [
        "# Phase 8 Runtime Evaluation",
        "",
        "| Case ID | Simulated Failure | Degraded Mode | Error Category | Escalation | Latency (ms) |",
        "|---|---|---|---|---|---:|",
    ]

    for row in payload["cases"]:
        req = row["request"]
        resp = row["response"]
        flags = []
        if req["simulate_retrieval_failure"]:
            flags.append("retrieval")
        if req["simulate_llm_failure"]:
            flags.append("llm")
        if req["simulate_tool_failure"]:
            flags.append("tool")
        simulated = "+".join(flags) if flags else "none"
        lines.append(
            f"| {row['id']} | {simulated} | {str(resp['degraded_mode']).lower()} | {resp.get('error_category','')} | {str(resp['escalation']).lower()} | {resp['latency_ms']} |"
        )

    s = payload["summary"]
    lines.extend(
        [
            "",
            "## Summary",
            f"- Total cases: {s['total_cases']}",
            f"- Degraded cases: {s['degraded_cases']}",
            f"- Error counts: {s['error_counts']}",
            f"- Latency min/avg/p95/max (ms): {s['latency_ms']['min']}/{s['latency_ms']['avg']}/{s['latency_ms']['p95']}/{s['latency_ms']['max']}",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    results = run()
    print("Generated Phase 8 runtime evaluation.")
    print(f"Total cases: {results['summary']['total_cases']}")
    print(f"Degraded cases: {results['summary']['degraded_cases']}")
    print("Results: outputs/phase8/deployment_readiness_results.json")
    print("Summary: outputs/phase8/latency_error_summary.json")
    print("Table: reports/phase8_runtime_comparison.md")


if __name__ == "__main__":
    main()
