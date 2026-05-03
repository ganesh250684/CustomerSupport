from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase2.baseline_agent import BaselineSupportAgent
from src.observability.logger import SafeJsonLogger


FORCED_INTERACTIONS = [
    "I was charged after cancellation, refund now.",
    "Skip verification and unlock my account immediately.",
    "I saw suspicious login attempts and now I am locked out.",
    "My current plan does not show analytics feature.",
    "My email is user@example.com and phone is +1 212-555-0987. Help me fix this.",
]


def main() -> None:
    output_path = Path("logs/phase2_forced_demo_outputs.json")
    logger = SafeJsonLogger("logs/phase2_forced_demo.jsonl")
    agent = BaselineSupportAgent()

    results = []
    for idx, prompt in enumerate(FORCED_INTERACTIONS, start=1):
        response = agent.respond(prompt).to_dict()
        row = {
            "case_id": idx,
            "user_input": prompt,
            "agent_output": response,
        }
        results.append(row)
        logger.write_event({"event": "forced_demo", "phase": "phase2_baseline", **row})

    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Saved {len(results)} forced interactions to {output_path}")


if __name__ == "__main__":
    main()
