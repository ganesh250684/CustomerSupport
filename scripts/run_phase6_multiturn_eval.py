from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase6.multiturn_agent import Phase6MultiTurnAgent


def run() -> Dict[str, Any]:
    dataset = json.loads(Path("data/phase6/multiturn_eval_test_set.json").read_text(encoding="utf-8"))

    results: Dict[str, Any] = {
        "without_memory": [],
        "with_memory": [],
    }

    for convo in dataset:
        convo_id = convo["conversation_id"]
        turns = convo["turns"]

        # Start fresh agent state per conversation for fair comparison.
        no_memory_agent = Phase6MultiTurnAgent(use_memory=False, max_memory_turns=6)
        with_memory_agent = Phase6MultiTurnAgent(use_memory=True, max_memory_turns=6)

        no_mem_rows: List[Dict[str, Any]] = []
        mem_rows: List[Dict[str, Any]] = []

        for turn in turns:
            no_mem_rows.append(no_memory_agent.run_turn(turn).to_dict())
            mem_rows.append(with_memory_agent.run_turn(turn).to_dict())

        results["without_memory"].append({"conversation_id": convo_id, "turns": no_mem_rows})
        results["with_memory"].append({"conversation_id": convo_id, "turns": mem_rows})

    quality = _compute_quality_snapshot(results)
    payload = {"results": results, "quality_snapshot": quality}

    Path("outputs/phase6").mkdir(parents=True, exist_ok=True)
    Path("outputs/phase6/multiturn_results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    snapshot = {
        "conversation_end_memory_states": [
            {
                "conversation_id": convo["conversation_id"],
                "stored_turns": next(
                    c["turns"] for c in results["with_memory"] if c["conversation_id"] == convo["conversation_id"]
                )[-1]["memory_summary"],
            }
            for convo in dataset
        ]
    }

    Path("outputs/phase6/memory_state_snapshot.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    Path("reports/phase6_multiturn_comparison.md").write_text(
        _to_markdown(payload),
        encoding="utf-8",
    )

    return payload


def _compute_quality_snapshot(results: Dict[str, Any]) -> Dict[str, int]:
    without_turns = sum(len(c["turns"]) for c in results["without_memory"])
    with_turns = sum(len(c["turns"]) for c in results["with_memory"])

    with_context_mentions = 0
    without_context_mentions = 0
    context_rich_without_memory = 0
    context_rich_with_memory = 0
    resets_detected = 0

    for convo in results["without_memory"]:
        for turn in convo["turns"]:
            if "Context considered:" in turn["response"]:
                without_context_mentions += 1
            if "Turn " in turn["response"]:
                context_rich_without_memory += 1

    for convo in results["with_memory"]:
        for turn in convo["turns"]:
            if "Context considered:" in turn["response"]:
                with_context_mentions += 1
            if "Turn " in turn["response"]:
                context_rich_with_memory += 1
            if turn["response"] == "Session context reset completed.":
                resets_detected += 1

    return {
        "total_turns_without_memory": without_turns,
        "total_turns_with_memory": with_turns,
        "context_mentions_without_memory": without_context_mentions,
        "context_mentions_with_memory": with_context_mentions,
        "context_rich_without_memory": context_rich_without_memory,
        "context_rich_with_memory": context_rich_with_memory,
        "memory_resets_detected": resets_detected,
    }


def _to_markdown(payload: Dict[str, Any]) -> str:
    lines = [
        "# Phase 6 Multi-Turn Comparison",
        "",
        "Comparison of behavior without vs with session memory and planning.",
        "",
        "| Conversation | Turn | Without Memory (summary) | With Memory (summary) | Improvement |",
        "|---|---:|---|---|---|",
    ]

    by_id_without = {c["conversation_id"]: c for c in payload["results"]["without_memory"]}
    by_id_with = {c["conversation_id"]: c for c in payload["results"]["with_memory"]}

    for convo_id, convo_no in by_id_without.items():
        convo_mem = by_id_with[convo_id]
        for idx, turn_no in enumerate(convo_no["turns"], start=1):
            turn_mem = convo_mem["turns"][idx - 1]
            no_text = turn_no["response"].replace("|", "\\|")[:170]
            mem_text = turn_mem["response"].replace("|", "\\|")[:170]
            improvement = "Better context continuity" if "Turn " in mem_text and "Turn " not in no_text else "No major change"
            lines.append(f"| {convo_id} | {idx} | {no_text} | {mem_text} | {improvement} |")

    q = payload["quality_snapshot"]
    lines.extend(
        [
            "",
            "## Quality Snapshot",
            f"- Total turns (without memory): {q['total_turns_without_memory']}",
            f"- Total turns (with memory): {q['total_turns_with_memory']}",
            f"- Context mentions (without memory): {q['context_mentions_without_memory']}",
            f"- Context mentions (with memory): {q['context_mentions_with_memory']}",
            f"- Context-rich turns (without memory): {q['context_rich_without_memory']}",
            f"- Context-rich turns (with memory): {q['context_rich_with_memory']}",
            f"- Memory resets detected: {q['memory_resets_detected']}",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    payload = run()
    q = payload["quality_snapshot"]
    print("Generated Phase 6 multi-turn evaluation.")
    print(f"Turns with memory: {q['total_turns_with_memory']}")
    print(f"Context-rich turns with memory: {q['context_rich_with_memory']}")
    print("Results: outputs/phase6/multiturn_results.json")
    print("Memory snapshot: outputs/phase6/memory_state_snapshot.json")
    print("Table: reports/phase6_multiturn_comparison.md")


if __name__ == "__main__":
    main()
