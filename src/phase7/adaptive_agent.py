from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict

from src.phase7.adaptive_policy import AdaptationConfig


@dataclass
class AdaptiveResponse:
    user_message: str
    response: str
    escalate: bool
    escalation_reason: str
    adaptation_applied: Dict[str, str]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class Phase7AdaptiveAgent:
    """Behavior can be changed by adaptation config derived from feedback."""

    def __init__(self, config: AdaptationConfig) -> None:
        self.config = config

    def respond(self, user_message: str) -> AdaptiveResponse:
        text = user_message.lower()
        escalate = False
        escalation_reason = ""

        sensitive = any(token in text for token in ["suspicious", "unauthorized", "legal", "abuse", "security"])
        policy_bypass = any(token in text for token in ["bypass", "skip verification", "override policy"])

        if policy_bypass:
            return AdaptiveResponse(
                user_message=user_message,
                response="I cannot assist with bypassing policy controls. I can guide compliant steps.",
                escalate=True,
                escalation_reason="policy_violation_request",
                adaptation_applied={
                    "escalation_sensitivity": self.config.escalation_sensitivity,
                    "response_style": self.config.response_style,
                    "clarification_aggressiveness": self.config.clarification_aggressiveness,
                },
            )

        if sensitive:
            if self.config.escalation_sensitivity in {"high", "normal"}:
                escalate = True
                escalation_reason = "sensitive_or_unresolved_case"

        if self.config.clarification_aggressiveness == "high" and "refund" in text and "invoice" not in text:
            response = (
                "To proceed safely, please share invoice id, cancellation date, and billing account reference. "
                "I will escalate if policy conditions are unclear."
            )
        else:
            response = "I can help with this request and guide next policy-safe steps."

        if self.config.response_style == "concise":
            response = response.split(".")[0] + "."

        return AdaptiveResponse(
            user_message=user_message,
            response=response,
            escalate=escalate,
            escalation_reason=escalation_reason,
            adaptation_applied={
                "escalation_sensitivity": self.config.escalation_sensitivity,
                "response_style": self.config.response_style,
                "clarification_aggressiveness": self.config.clarification_aggressiveness,
            },
        )
