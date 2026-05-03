from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from src.utils.redaction import redact_pii


@dataclass
class FeedbackEvent:
    timestamp_utc: str
    case_id: str
    user_message: str
    helpful: bool
    reason_tag: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class FeedbackStore:
    """Stores feedback signals with PII-safe content."""

    def __init__(self) -> None:
        self.events: List[FeedbackEvent] = []

    def add(self, case_id: str, user_message: str, helpful: bool, reason_tag: str) -> None:
        self.events.append(
            FeedbackEvent(
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
                case_id=case_id,
                user_message=redact_pii(user_message),
                helpful=helpful,
                reason_tag=reason_tag,
            )
        )

    def reason_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for event in self.events:
            counts[event.reason_tag] = counts.get(event.reason_tag, 0) + 1
        return counts

    def helpful_ratio(self) -> float:
        if not self.events:
            return 0.0
        positives = sum(1 for event in self.events if event.helpful)
        return positives / len(self.events)

    def dump_jsonl(self, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fp:
            for event in self.events:
                fp.write(f"{event.to_dict()}\n")
