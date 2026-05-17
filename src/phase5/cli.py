from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.observability.logger import SafeJsonLogger
from src.phase5.tool_agent import Phase5ToolAgent


def main() -> None:
    agent = Phase5ToolAgent()
    logger = SafeJsonLogger("logs/phase5_interactions.jsonl")

    print("Phase 5 Tool Agent CLI")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        result = asdict(agent.run_turn(user_input))
        print("Agent >")
        print(json.dumps(result, indent=2))

        logger.write_event(
            {
                "event": "interaction",
                "phase": "phase5_tool_agent",
                "user_input": user_input,
                "agent_output": result,
            }
        )


if __name__ == "__main__":
    main()
