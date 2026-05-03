from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from src.utils.redaction import redact_pii


class SafeJsonLogger:
    """Writes JSONL logs with basic PII redaction."""

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def write_event(self, event: Dict[str, Any]) -> None:
        sanitized = self._sanitize(event)
        with self.log_path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(sanitized, ensure_ascii=True) + "\n")

    def _sanitize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        clean: Dict[str, Any] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        for key, value in payload.items():
            if isinstance(value, str):
                clean[key] = redact_pii(value)
            elif isinstance(value, dict):
                clean[key] = {
                    nested_key: redact_pii(nested_val) if isinstance(nested_val, str) else nested_val
                    for nested_key, nested_val in value.items()
                }
            else:
                clean[key] = value
        return clean
