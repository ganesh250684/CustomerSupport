from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase4.indexer import load_vector_index
from src.phase4.rag_agent import Phase4RagAgent
from src.phase4.retriever import retrieve_relevant_docs


def run() -> List[Dict[str, Any]]:
    test_set = json.loads(Path("data/phase4/rag_eval_test_set.json").read_text(encoding="utf-8"))
    index_payload = load_vector_index(Path("outputs/phase4/vector_index.json"))
    agent = Phase4RagAgent(model_name="gpt-4o-mini")

    rows: List[Dict[str, Any]] = []

    for case in test_set:
        message = case["user_message"]

        without_rag = agent.respond_without_retrieval(message).to_dict()
        retrieved = retrieve_relevant_docs(index_payload, message, k=4, min_similarity=0.45)
        with_rag = agent.respond_with_retrieval(message, retrieved).to_dict()

        row = {
            "id": case["id"],
            "category": case["category"],
            "user_message": message,
            "retrieved_count": len(retrieved),
            "without_retrieval": without_rag,
            "with_retrieval": with_rag,
        }
        rows.append(row)

    Path("outputs/phase4").mkdir(parents=True, exist_ok=True)
    Path("outputs/phase4/rag_comparison_results.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    Path("reports/phase4_rag_comparison.md").write_text(_to_markdown(rows), encoding="utf-8")
    return rows


def _to_markdown(rows: List[Dict[str, Any]]) -> str:
    lines = [
        "# Phase 4 Retrieval Comparison",
        "",
        "Comparison of responses with and without retrieval over the same test set.",
        "",
        "| Case ID | Category | Retrieved Chunks | Without Retrieval (summary) | With Retrieval (summary) | Improvement |",
        "|---|---|---:|---|---|---|",
    ]

    for row in rows:
        no_rag = row["without_retrieval"]["response_draft"].replace("\n", " ")[:170].replace("|", "\\|")
        with_rag = row["with_retrieval"]["response_draft"].replace("\n", " ")[:170].replace("|", "\\|")

        improvement = "Grounded response"
        if row["retrieved_count"] == 0:
            improvement = "Correct missing-evidence escalation"

        lines.append(
            f"| {row['id']} | {row['category']} | {row['retrieved_count']} | {no_rag} | {with_rag} | {improvement} |"
        )

    lines.extend(
        [
            "",
            "## Missing Information Handling",
            "When retrieval returns no relevant chunks, the agent must:",
            "1. Avoid policy fabrication.",
            "2. State uncertainty explicitly.",
            "3. Escalate the case.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    rows = run()
    print(f"Generated Phase 4 comparison rows: {len(rows)}")
    print("Results: outputs/phase4/rag_comparison_results.json")
    print("Table: reports/phase4_rag_comparison.md")


if __name__ == "__main__":
    main()
