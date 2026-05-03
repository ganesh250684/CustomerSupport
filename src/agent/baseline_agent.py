from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List


UNSAFE_PATTERNS: List[str] = [
    "bypass",
    "skip verification",
    "override policy",
    "hack",
    "exploit",
]

SENSITIVE_PATTERNS: List[str] = [
    "suspicious login",
    "unauthorized access",
    "data breach",
    "legal",
    "abuse",
]


@dataclass
class AgentResponse:
    response_draft: str
    confidence: str
    citations: List[str]
    escalate: bool
    escalation_reason: str
    uncertainty_note: str
    handling_label: str

    def to_dict(self) -> dict:
        return asdict(self)


class BaselineSupportAgent:
    """A deterministic rules/template baseline for Phase 2."""

    def respond(self, user_message: str) -> AgentResponse:
        text = user_message.lower().strip()

        if self._contains_any(text, UNSAFE_PATTERNS):
            return AgentResponse(
                response_draft=(
                    "I cannot help with requests that bypass verification or violate policy. "
                    "I can help with a compliant recovery path instead."
                ),
                confidence="high",
                citations=["POLICY_PLACEHOLDER: security_access_controls"],
                escalate=True,
                escalation_reason="policy_violation_request",
                uncertainty_note="",
                handling_label="refusal",
            )

        if self._contains_any(text, SENSITIVE_PATTERNS) or "lock" in text:
            return AgentResponse(
                response_draft=(
                    "This appears security-sensitive. Please complete identity verification steps. "
                    "I am escalating this ticket to the security support queue now."
                ),
                confidence="medium",
                citations=["PROC_PLACEHOLDER: account_recovery_v1"],
                escalate=True,
                escalation_reason="security_sensitive_case",
                uncertainty_note="",
                handling_label="escalation",
            )

        if any(token in text for token in ["refund", "charged", "billing", "invoice"]):
            return AgentResponse(
                response_draft=(
                    "I can help review your billing issue. Please share the invoice id and cancellation date. "
                    "If criteria match policy, a refund request can be submitted."
                ),
                confidence="medium",
                citations=["FAQ_PLACEHOLDER: billing_refunds"],
                escalate=False,
                escalation_reason="",
                uncertainty_note="",
                handling_label="guided_resolution",
            )

        if any(token in text for token in ["feature", "plan", "upgrade"]):
            return AgentResponse(
                response_draft=(
                    "I can explain plan differences and available upgrade paths. "
                    "Please confirm your current plan so I can provide accurate options."
                ),
                confidence="medium",
                citations=["FAQ_PLACEHOLDER: plan_features"],
                escalate=False,
                escalation_reason="",
                uncertainty_note="",
                handling_label="guided_resolution",
            )

        return AgentResponse(
            response_draft=(
                "I may not have enough information to provide a policy-safe resolution yet. "
                "Please share more details, and I can escalate if the case remains unresolved."
            ),
            confidence="low",
            citations=[],
            escalate=True,
            escalation_reason="insufficient_context",
            uncertainty_note="No strong rule match in baseline agent.",
            handling_label="fallback",
        )

    @staticmethod
    def _contains_any(text: str, patterns: List[str]) -> bool:
        return any(pattern in text for pattern in patterns)
