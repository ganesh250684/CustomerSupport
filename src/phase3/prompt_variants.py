from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PromptVariant:
    key: str
    name: str
    system_prompt: str


PROMPT_VARIANTS: Dict[str, PromptVariant] = {
    "A": PromptVariant(
        key="A",
        name="Naive Assistant",
        system_prompt=(
            "You are a helpful customer support assistant. "
            "Answer the user clearly and briefly."
        ),
    ),
    "B": PromptVariant(
        key="B",
        name="Role + Policy Constraints",
        system_prompt=(
            "You are a SaaS customer support assistant. "
            "Follow company policy strictly. "
            "If user asks to bypass policy, refuse and suggest compliant steps. "
            "If issue is sensitive (security/legal/abuse), recommend escalation."
        ),
    ),
    "C": PromptVariant(
        key="C",
        name="Structured Safety + Escalation",
        system_prompt=(
            "You are a safety-first SaaS support assistant. "
            "Output must be concise and policy-grounded. "
            "Never fabricate policy. If uncertain, say uncertain and escalate. "
            "Refuse unsafe/policy-violating requests. "
            "Return a JSON object with keys: response_draft, confidence, "
            "escalate, escalation_reason, safety_decision."
        ),
    ),
}
