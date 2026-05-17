from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.observability.logger import SafeJsonLogger
from src.phase8.runtime_models import ResolveRequest
from src.phase8.service import resolve


def main() -> None:
    logger = SafeJsonLogger("logs/phase8_interactions.jsonl")

    simulate_retrieval = False
    simulate_llm = False
    simulate_tool = False

    print("Phase 8 Runtime CLI")
    print("Commands: /simulate none|retrieval|llm|tool, /show, exit")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        if user_input.lower() == "/show":
            print(
                json.dumps(
                    {
                        "simulate_retrieval_failure": simulate_retrieval,
                        "simulate_llm_failure": simulate_llm,
                        "simulate_tool_failure": simulate_tool,
                    },
                    indent=2,
                )
            )
            continue

        if user_input.lower().startswith("/simulate "):
            mode = user_input.split(maxsplit=1)[1].strip().lower()
            simulate_retrieval = mode == "retrieval"
            simulate_llm = mode == "llm"
            simulate_tool = mode == "tool"

            if mode not in {"none", "retrieval", "llm", "tool"}:
                print("Unknown mode. Use none, retrieval, llm, or tool.")
                continue

            print(f"Simulation mode set to: {mode}")
            continue

        request = ResolveRequest(
            user_message=user_input,
            simulate_retrieval_failure=simulate_retrieval,
            simulate_llm_failure=simulate_llm,
            simulate_tool_failure=simulate_tool,
        )
        response = resolve(request)
        payload = response.model_dump() if hasattr(response, "model_dump") else asdict(response)

        print("Agent >")
        print(json.dumps(payload, indent=2))

        logger.write_event(
            {
                "event": "interaction",
                "phase": "phase8_runtime",
                "request": request.model_dump() if hasattr(request, "model_dump") else asdict(request),
                "agent_output": payload,
            }
        )


if __name__ == "__main__":
    main()
