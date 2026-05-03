from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from src.utils.redaction import redact_pii


class RuntimeTracer:
    """Tracks request latency, trace id, and structured error records."""

    def __init__(self, log_file: str = "outputs/phase8/runtime_logs.jsonl") -> None:
        self.log_path = Path(log_file)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def new_trace_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def start_timer() -> float:
        return time.perf_counter()

    @staticmethod
    def elapsed_ms(start: float) -> float:
        return round((time.perf_counter() - start) * 1000.0, 2)

    def log_event(self, event: Dict[str, Any]) -> None:
        sanitized = {
            **event,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        for key in ["user_message", "response", "error_detail"]:
            if key in sanitized and isinstance(sanitized[key], str):
                sanitized[key] = redact_pii(sanitized[key])

        with self.log_path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(sanitized, ensure_ascii=True) + "\n")
