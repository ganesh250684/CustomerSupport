from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.observability.logger import SafeJsonLogger
from src.phase6.multiturn_agent import Phase6MultiTurnAgent


def _new_agent(use_memory: bool) -> Phase6MultiTurnAgent:
    return Phase6MultiTurnAgent(use_memory=use_memory, max_memory_turns=6)


def main() -> None:
    use_memory = True
    agent = _new_agent(use_memory)
    logger = SafeJsonLogger("logs/phase6_interactions.jsonl")

    print("Phase 6 Multi-turn CLI")
    print("Commands: /memory on|off, /reset, /show, exit")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        if user_input.lower().startswith("/memory "):
            requested = user_input.split(maxsplit=1)[1].strip().lower()
            if requested in {"on", "off"}:
                use_memory = requested == "on"
                agent = _new_agent(use_memory)
                print(f"Memory mode set to: {'on' if use_memory else 'off'}")
            else:
                print("Unknown value. Use '/memory on' or '/memory off'.")
            continue

        if user_input.lower() == "/reset":
            output = agent.run_turn("reset memory").to_dict()
            print("Agent >")
            print(json.dumps(output, indent=2))
            continue

        if user_input.lower() == "/show":
            print(f"Memory mode: {'on' if use_memory else 'off'}")
            continue

        output = agent.run_turn(user_input).to_dict()
        print("Agent >")
        print(json.dumps(output, indent=2))

        logger.write_event(
            {
                "event": "interaction",
                "phase": "phase6_multiturn",
                "memory_enabled": use_memory,
                "user_input": user_input,
                "agent_output": output,
            }
        )


if __name__ == "__main__":
    main()
