from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.observability.logger import SafeJsonLogger
from src.phase3.llm_client import Phase3LLMClient
from src.phase3.prompt_variants import PROMPT_VARIANTS


def _pretty_output(raw_text: str) -> str:
    stripped = raw_text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            return json.dumps(json.loads(stripped), indent=2)
        except json.JSONDecodeError:
            return raw_text
    return raw_text


def main() -> None:
    variant_key = "C"
    variant = PROMPT_VARIANTS[variant_key]

    try:
        client = Phase3LLMClient(model_name="gpt-4o-mini")
    except Exception as exc:  # noqa: BLE001
        print(f"Phase 3 CLI setup failed: {exc}")
        print("Hint: set OPENAI_API_KEY before running this CLI.")
        return

    logger = SafeJsonLogger("logs/phase3_interactions.jsonl")

    print("Phase 3 Prompt Variant Chat CLI")
    print("Commands: /variant A|B|C, /show, exit")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        if user_input.lower().startswith("/variant "):
            requested = user_input.split(maxsplit=1)[1].strip().upper()
            if requested in PROMPT_VARIANTS:
                variant_key = requested
                variant = PROMPT_VARIANTS[variant_key]
                print(f"Switched to variant {variant_key}: {variant.name}")
            else:
                print("Unknown variant. Use A, B, or C.")
            continue

        if user_input.lower() == "/show":
            print(f"Current variant: {variant_key} - {variant.name}")
            continue

        output = client.generate(variant.system_prompt, user_input)
        pretty = _pretty_output(output)

        print("Agent >")
        print(pretty)

        logger.write_event(
            {
                "event": "interaction",
                "phase": "phase3_prompt_variant_chat",
                "variant": variant_key,
                "variant_name": variant.name,
                "user_input": user_input,
                "agent_output": output,
            }
        )


if __name__ == "__main__":
    main()
