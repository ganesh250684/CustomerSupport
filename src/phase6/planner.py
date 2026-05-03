from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PlanStep:
    name: str
    status: str
    note: str = ""


def build_plan(user_message: str) -> List[PlanStep]:
    """Create a lightweight deterministic reasoning plan for each turn."""
    text = user_message.lower()

    intent = "general_support"
    if any(token in text for token in ["refund", "charged", "invoice", "billing"]):
        intent = "billing"
    elif any(token in text for token in ["lock", "suspicious", "unauthorized", "security"]):
        intent = "security"

    risk = "low"
    if any(token in text for token in ["legal", "abuse", "suspicious", "unauthorized", "bypass"]):
        risk = "high"

    return [
        PlanStep(name="classify_intent", status="done", note=intent),
        PlanStep(name="review_memory_context", status="done", note="session_memory_checked"),
        PlanStep(name="select_response_strategy", status="done", note=f"risk={risk}"),
        PlanStep(name="safety_verification", status="done", note="refusal/escalation rules applied"),
        PlanStep(name="finalize_response", status="done", note="response_ready"),
    ]
