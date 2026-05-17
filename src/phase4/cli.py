from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.observability.logger import SafeJsonLogger
from src.phase4.indexer import build_vector_index, load_vector_index
from src.phase4.kb_loader import load_kb_documents
from src.phase4.rag_agent import Phase4RagAgent
from src.phase4.retriever import retrieve_relevant_docs


def _ensure_index() -> Dict[str, Any]:
    index_file = Path("outputs/phase4/vector_index.json")
    if index_file.exists():
        return load_vector_index(index_file)

    kb_dir = Path("data/kb/raw")
    docs = load_kb_documents(kb_dir)
    if not docs:
        raise RuntimeError(
            "No KB documents found in data/kb/raw and no existing index at outputs/phase4/vector_index.json"
        )

    print("No vector index found. Building index from data/kb/raw ...")
    return build_vector_index(docs, index_file)


def main() -> None:
    try:
        index_payload = _ensure_index()
        agent = Phase4RagAgent(model_name="gpt-4o-mini")
    except Exception as exc:  # noqa: BLE001
        print(f"Phase 4 CLI setup failed: {exc}")
        print("Hint: ensure OPENAI_API_KEY is set and KB files exist under data/kb/raw.")
        return

    logger = SafeJsonLogger("logs/phase4_interactions.jsonl")
    mode = "with"

    print("Phase 4 RAG Chat CLI")
    print("Commands: /mode with|without, /show, /reindex, exit")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        if user_input.lower().startswith("/mode "):
            requested = user_input.split(maxsplit=1)[1].strip().lower()
            if requested in {"with", "without"}:
                mode = requested
                print(f"Switched mode to: {mode}_retrieval")
            else:
                print("Unknown mode. Use 'with' or 'without'.")
            continue

        if user_input.lower() == "/show":
            print(f"Current mode: {mode}_retrieval")
            continue

        if user_input.lower() == "/reindex":
            try:
                index_payload = _ensure_index()
                print(f"Index ready with {index_payload.get('entry_count', 0)} chunks.")
            except Exception as exc:  # noqa: BLE001
                print(f"Reindex failed: {exc}")
            continue

        if mode == "without":
            response = agent.respond_without_retrieval(user_input).to_dict()
            retrieved_count = 0
        else:
            retrieved = retrieve_relevant_docs(index_payload, user_input, k=4, min_similarity=0.45)
            response = agent.respond_with_retrieval(user_input, retrieved).to_dict()
            retrieved_count = len(retrieved)

        print("Agent >")
        print(json.dumps(response, indent=2))

        logger.write_event(
            {
                "event": "interaction",
                "phase": "phase4_rag_chat",
                "mode": mode,
                "user_input": user_input,
                "retrieved_count": retrieved_count,
                "agent_output": response,
            }
        )


if __name__ == "__main__":
    main()
