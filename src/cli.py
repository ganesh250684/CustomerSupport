from __future__ import annotations

import json

from src.agent.baseline_agent import BaselineSupportAgent
from src.observability.logger import SafeJsonLogger


def main() -> None:
    agent = BaselineSupportAgent()
    logger = SafeJsonLogger("logs/phase2_interactions.jsonl")

    print("Phase 2 Baseline Support Agent")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        response = agent.respond(user_input)
        response_json = response.to_dict()
        print("Agent >")
        print(json.dumps(response_json, indent=2))

        logger.write_event(
            {
                "event": "interaction",
                "phase": "phase2_baseline",
                "user_input": user_input,
                "agent_output": response_json,
            }
        )


if __name__ == "__main__":
    main()
