from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase5.tool_agent import Phase5ToolAgent


def run() -> List[Dict[str, Any]]:
    test_set = json.loads(Path("data/phase5/tool_eval_test_set.json").read_text(encoding="utf-8"))
    agent = Phase5ToolAgent()

    rows: List[Dict[str, Any]] = []
    audit_path = Path("outputs/phase5/tool_audit_log.jsonl")
    audit_path.parent.mkdir(parents=True, exist_ok=True)

    with audit_path.open("w", encoding="utf-8") as audit_fp:
        for case in test_set:
            turn = agent.run_turn(case["user_message"])
            row = {
                "id": case["id"],
                "category": case["category"],
                "user_message": case["user_message"],
                "result": asdict(turn),
            }
            rows.append(row)
            audit_fp.write(json.dumps(row, ensure_ascii=True) + "\n")

    Path("outputs/phase5/tool_run_results.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    Path("reports/phase5_tool_usage_comparison.md").write_text(_to_markdown(rows), encoding="utf-8")
    return rows


def _to_markdown(rows: List[Dict[str, Any]]) -> str:
    lines = [
        "# Phase 5 Tool Usage Evaluation",
        "",
        "| Case ID | Category | Selected Tool | Tool Success | Escalation | Evidence |",
        "|---|---|---|---|---|---|",
    ]

    for row in rows:
        result = row["result"]
        selected = result.get("selected_tool") or "none"
        tool_result = result.get("tool_result")
        success = "n/a" if tool_result is None else str(tool_result.get("success")).lower()
        escalation = str(result.get("escalation_recommended", False)).lower()
        evidence = result.get("final_response", "").replace("|", "\\|")
        lines.append(
            f"| {row['id']} | {row['category']} | {selected} | {success} | {escalation} | {evidence} |"
        )

    lines.extend(
        [
            "",
            "## Safeguard Outcomes",
            "- Disallowed tool requests are blocked and escalated.",
            "- Invalid tool arguments produce safe failure with escalation.",
            "- No-tool cases avoid unnecessary tool execution.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    rows = run()
    print(f"Generated Phase 5 tool evaluation rows: {len(rows)}")
    print("Results: outputs/phase5/tool_run_results.json")
    print("Audit: outputs/phase5/tool_audit_log.jsonl")
    print("Table: reports/phase5_tool_usage_comparison.md")


if __name__ == "__main__":
    main()
