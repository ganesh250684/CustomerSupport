from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class AdaptationConfig:
    escalation_sensitivity: str
    response_style: str
    clarification_aggressiveness: str


def derive_adaptation(reason_counts: Dict[str, int], helpful_ratio: float) -> AdaptationConfig:
    """Derive runtime behavior knobs from aggregated feedback signals."""
    escalation_sensitivity = "normal"
    response_style = "balanced"
    clarification_aggressiveness = "normal"

    if reason_counts.get("missed_escalation", 0) >= 1:
        escalation_sensitivity = "high"

    if reason_counts.get("too_generic", 0) >= 2:
        clarification_aggressiveness = "high"

    if reason_counts.get("too_verbose", 0) >= 2:
        response_style = "concise"

    if helpful_ratio < 0.5:
        clarification_aggressiveness = "high"

    return AdaptationConfig(
        escalation_sensitivity=escalation_sensitivity,
        response_style=response_style,
        clarification_aggressiveness=clarification_aggressiveness,
    )
