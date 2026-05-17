from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.observability.logger import SafeJsonLogger
from src.phase7.adaptive_agent import Phase7AdaptiveAgent
from src.phase7.adaptive_policy import AdaptationConfig


def _build_agent(config: AdaptationConfig) -> Phase7AdaptiveAgent:
    return Phase7AdaptiveAgent(config=config)


def main() -> None:
    config = AdaptationConfig(
        escalation_sensitivity="normal",
        response_style="balanced",
        clarification_aggressiveness="normal",
    )
    agent = _build_agent(config)
    logger = SafeJsonLogger("logs/phase7_interactions.jsonl")

    print("Phase 7 Adaptive Agent CLI")
    print("Commands:")
    print("  /set escalation normal|high|low")
    print("  /set style balanced|concise")
    print("  /set clarification normal|high")
    print("  /show")
    print("  exit")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        if user_input.lower() == "/show":
            print(json.dumps(config.__dict__, indent=2))
            continue

        if user_input.lower().startswith("/set "):
            parts = user_input.split()
            if len(parts) != 3:
                print("Usage: /set <escalation|style|clarification> <value>")
                continue

            _, key, value = parts
            key = key.lower()
            value = value.lower()

            if key == "escalation" and value in {"normal", "high", "low"}:
                config.escalation_sensitivity = value
            elif key == "style" and value in {"balanced", "concise"}:
                config.response_style = value
            elif key == "clarification" and value in {"normal", "high"}:
                config.clarification_aggressiveness = value
            else:
                print("Invalid setting or value.")
                continue

            agent = _build_agent(config)
            print("Configuration updated.")
            print(json.dumps(config.__dict__, indent=2))
            continue

        output = agent.respond(user_input).to_dict()
        print("Agent >")
        print(json.dumps(output, indent=2))

        logger.write_event(
            {
                "event": "interaction",
                "phase": "phase7_adaptive",
                "config": config.__dict__,
                "user_input": user_input,
                "agent_output": output,
            }
        )


if __name__ == "__main__":
    main()
