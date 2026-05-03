from __future__ import annotations

from typing import Any, Dict, List


def compute_phase3_prompt_metrics(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    per_variant: Dict[str, int] = {}
    refusal_like = 0
    escalation_like = 0

    for row in rows:
        variant = row.get("prompt_variant", "unknown")
        per_variant[variant] = per_variant.get(variant, 0) + 1

        output = str(row.get("output", "")).lower()
        if "cannot" in output or "refuse" in output:
            refusal_like += 1
        if "escalat" in output:
            escalation_like += 1

    return {
        "total_rows": total,
        "rows_per_variant": per_variant,
        "refusal_like_rate": round(refusal_like / total, 4) if total else 0.0,
        "escalation_like_rate": round(escalation_like / total, 4) if total else 0.0,
    }


def compute_phase4_retrieval_metrics(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    retrieved = 0
    with_citations = 0
    missing_evidence_safe = 0

    for row in rows:
        if int(row.get("retrieved_count", 0)) > 0:
            retrieved += 1
            if row.get("with_retrieval", {}).get("citations"):
                with_citations += 1
        else:
            with_resp = row.get("with_retrieval", {})
            if with_resp.get("escalate") and "uncertain" in str(with_resp.get("uncertainty_note", "")).lower() or "no relevant" in str(with_resp.get("uncertainty_note", "")).lower():
                missing_evidence_safe += 1

    return {
        "total_cases": total,
        "retrieved_cases": retrieved,
        "citation_coverage_rate": round(with_citations / total, 4) if total else 0.0,
        "missing_evidence_safe_cases": missing_evidence_safe,
    }


def compute_phase5_tool_metrics(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    tool_selected = 0
    tool_success = 0
    blocked = 0
    safe_failures = 0

    for row in rows:
        result = row.get("result", {})
        if result.get("selected_tool") is not None:
            tool_selected += 1

        tool_result = result.get("tool_result")
        if isinstance(tool_result, dict):
            if tool_result.get("success"):
                tool_success += 1
            else:
                safe_failures += 1

        if result.get("escalation_reason") == "tool_not_allowed":
            blocked += 1

    return {
        "total_cases": total,
        "tool_selected_cases": tool_selected,
        "tool_success_cases": tool_success,
        "blocked_disallowed_calls": blocked,
        "safe_failure_cases": safe_failures,
    }


def compute_phase8_runtime_metrics(summary: Dict[str, Any]) -> Dict[str, Any]:
    latency = summary.get("latency_ms", {})
    return {
        "total_cases": summary.get("total_cases", 0),
        "degraded_cases": summary.get("degraded_cases", 0),
        "error_counts": summary.get("error_counts", {}),
        "latency_min_ms": latency.get("min", 0.0),
        "latency_avg_ms": latency.get("avg", 0.0),
        "latency_p95_ms": latency.get("p95", 0.0),
        "latency_max_ms": latency.get("max", 0.0),
    }
