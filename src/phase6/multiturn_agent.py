from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List

from src.phase6.memory_store import SessionMemoryStore
from src.phase6.planner import build_plan


@dataclass
class TurnOutput:
    user_message: str
    used_memory: bool
    memory_summary: str
    plan_steps: List[Dict[str, str]]
    response: str
    escalation: bool
    escalation_reason: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class Phase6MultiTurnAgent:
    """Agent variant with planning + optional session memory."""

    def __init__(self, use_memory: bool, max_memory_turns: int = 6) -> None:
        self.use_memory = use_memory
        self.memory = SessionMemoryStore(max_turns=max_memory_turns)

    def run_turn(self, user_message: str) -> TurnOutput:
        text = user_message.lower().strip()
        if text in {"reset", "reset memory", "clear context"}:
            self.memory.reset(reason="user_requested")
            response = "Session context reset completed."
            output = TurnOutput(
                user_message=user_message,
                used_memory=self.use_memory,
                memory_summary="No prior session context.",
                plan_steps=[{"name": "reset_memory", "status": "done", "note": "user_requested"}],
                response=response,
                escalation=False,
                escalation_reason="",
            )
            return output

        plan = build_plan(user_message)
        memory_summary = self.memory.summary() if self.use_memory else "Memory disabled for this run."

        response, escalate, reason = self._compose_response(user_message, memory_summary)

        if self.use_memory:
            self.memory.add_turn(user_message=user_message, agent_response=response, tags=["phase6"])

        return TurnOutput(
            user_message=user_message,
            used_memory=self.use_memory,
            memory_summary=memory_summary,
            plan_steps=[asdict(step) for step in plan],
            response=response,
            escalation=escalate,
            escalation_reason=reason,
        )

    @staticmethod
    def _compose_response(user_message: str, memory_summary: str) -> tuple[str, bool, str]:
        text = user_message.lower()

        if any(token in text for token in ["bypass", "skip verification", "override policy"]):
            return (
                "I cannot assist with bypassing verification or policy controls. "
                "I can guide you through compliant recovery steps instead.",
                True,
                "policy_violation_request",
            )

        if any(token in text for token in ["suspicious", "unauthorized", "legal", "abuse"]):
            return (
                "This appears sensitive. I recommend immediate escalation to specialized support. "
                f"Context considered: {memory_summary}",
                True,
                "sensitive_or_unresolved_case",
            )

        if "refund" in text or "charged" in text:
            return (
                "Please share invoice id and cancellation date. "
                "I will use this session context to avoid repeating questions. "
                f"Context considered: {memory_summary}",
                False,
                "",
            )

        return (
            "Please provide more details so I can assist accurately. "
            f"Context considered: {memory_summary}",
            False,
            "",
        )
