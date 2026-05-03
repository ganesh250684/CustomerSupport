from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from src.phase6.multiturn_agent import Phase6MultiTurnAgent


@dataclass
class RootCauseResult:
    issue: str
    before_behavior: str
    after_behavior: str
    root_cause: str
    fix_applied: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "issue": self.issue,
            "before_behavior": self.before_behavior,
            "after_behavior": self.after_behavior,
            "root_cause": self.root_cause,
            "fix_applied": self.fix_applied,
        }


def reproduce_and_fix_memory_contamination() -> RootCauseResult:
    """Demonstrate a concrete failure and fix from Phase 6 style memory handling."""

    # Before (failure): one shared memory agent used for independent conversations.
    shared_agent = Phase6MultiTurnAgent(use_memory=True, max_memory_turns=6)
    shared_agent.run_turn("I was charged after cancellation and want a refund.")
    contaminated = shared_agent.run_turn("There were suspicious logins on my account.")

    before_behavior = contaminated.memory_summary

    # After (fix): isolate memory per conversation.
    fresh_agent = Phase6MultiTurnAgent(use_memory=True, max_memory_turns=6)
    isolated = fresh_agent.run_turn("There were suspicious logins on my account.")
    after_behavior = isolated.memory_summary

    return RootCauseResult(
        issue="cross_conversation_memory_contamination",
        before_behavior=before_behavior,
        after_behavior=after_behavior,
        root_cause="shared memory instance reused across independent conversations",
        fix_applied="reset/initialize new memory agent per conversation evaluation run",
    )
