from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from src.utils.redaction import redact_pii


@dataclass
class MemoryTurn:
    turn_id: int
    user_message: str
    agent_response: str
    tags: List[str] = field(default_factory=list)


class SessionMemoryStore:
    """Session-scoped memory with retention and reset behavior."""

    def __init__(self, max_turns: int = 6) -> None:
        self.max_turns = max_turns
        self._turns: List[MemoryTurn] = []
        self._next_turn_id = 1

    def add_turn(self, user_message: str, agent_response: str, tags: List[str] | None = None) -> None:
        clean_user = redact_pii(user_message)
        clean_response = redact_pii(agent_response)
        self._turns.append(
            MemoryTurn(
                turn_id=self._next_turn_id,
                user_message=clean_user,
                agent_response=clean_response,
                tags=tags or [],
            )
        )
        self._next_turn_id += 1

        # Retention rule: keep only most recent N turns.
        if len(self._turns) > self.max_turns:
            self._turns = self._turns[-self.max_turns :]

    def reset(self, reason: str = "manual_reset") -> None:
        self._turns = []
        self._next_turn_id = 1

    def summary(self) -> str:
        if not self._turns:
            return "No prior session context."

        latest = self._turns[-2:] if len(self._turns) >= 2 else self._turns
        bits: List[str] = []
        for turn in latest:
            bits.append(f"Turn {turn.turn_id}: user='{turn.user_message[:80]}'")
        return " | ".join(bits)

    def to_dict(self) -> Dict[str, object]:
        return {
            "max_turns": self.max_turns,
            "stored_turns": [
                {
                    "turn_id": t.turn_id,
                    "user_message": t.user_message,
                    "agent_response": t.agent_response,
                    "tags": t.tags,
                }
                for t in self._turns
            ],
        }
