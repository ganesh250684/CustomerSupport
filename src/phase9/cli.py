from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.observability.logger import SafeJsonLogger
from src.phase8.runtime_models import ResolveRequest
from src.phase8.service import resolve
from src.phase9.root_cause import reproduce_and_fix_memory_contamination


def main() -> None:
    logger = SafeJsonLogger("logs/phase9_interactions.jsonl")

    print("Phase 9 Review CLI")
    print("Commands: /root-cause, /help, exit")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        if user_input.lower() == "/help":
            print("Use /root-cause to view the debugged failure case with before/after proof.")
            print("Any other input runs a live phase8-style response for manual review.")
            continue

        if user_input.lower() == "/root-cause":
            root_cause = reproduce_and_fix_memory_contamination().to_dict()
            print("Root Cause Report >")
            print(json.dumps(root_cause, indent=2))

            logger.write_event(
                {
                    "event": "root_cause_report",
                    "phase": "phase9_review",
                    "report": root_cause,
                }
            )
            continue

        request = ResolveRequest(user_message=user_input)
        response = resolve(request)
        payload = response.model_dump() if hasattr(response, "model_dump") else response.dict()

        review = {
            "looks_safe": bool(payload.get("response")) and not payload.get("response", "").lower().startswith("i can bypass"),
            "escalation": payload.get("escalation", False),
            "degraded_mode": payload.get("degraded_mode", False),
            "error_category": payload.get("error_category", ""),
        }

        print("Review Output >")
        print(json.dumps({"response": payload, "review": review}, indent=2))

        logger.write_event(
            {
                "event": "interaction_review",
                "phase": "phase9_review",
                "request": request.model_dump() if hasattr(request, "model_dump") else request.dict(),
                "response": payload,
                "review": review,
            }
        )


if __name__ == "__main__":
    main()
