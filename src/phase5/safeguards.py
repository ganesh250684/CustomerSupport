from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List, Set

from src.phase5.tool_schemas import ToolCall


@dataclass
class ToolGuardState:
    max_calls_per_turn: int = 2
    call_history: List[str] = field(default_factory=list)
    seen_calls: Set[str] = field(default_factory=set)


ALLOWED_TOOLS = {"lookup_ticket_status", "create_escalation_ticket"}


def validate_tool_allowed(tool_call: ToolCall) -> tuple[bool, str]:
    if tool_call.name not in ALLOWED_TOOLS:
        return False, "tool_not_allowed"
    return True, ""


def validate_max_calls(state: ToolGuardState) -> tuple[bool, str]:
    if len(state.call_history) >= state.max_calls_per_turn:
        return False, "max_tool_calls_exceeded"
    return True, ""


def validate_duplicate_call(state: ToolGuardState, tool_call: ToolCall) -> tuple[bool, str]:
    fingerprint = json.dumps({"name": tool_call.name, "args": tool_call.args}, sort_keys=True)
    if fingerprint in state.seen_calls:
        return False, "duplicate_tool_call_blocked"
    return True, ""


def record_call(state: ToolGuardState, tool_call: ToolCall) -> None:
    fingerprint = json.dumps({"name": tool_call.name, "args": tool_call.args}, sort_keys=True)
    state.call_history.append(tool_call.name)
    state.seen_calls.add(fingerprint)
