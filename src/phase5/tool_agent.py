from __future__ import annotations

from typing import Dict

from src.phase5.router import choose_tool
from src.phase5.safeguards import (
    ToolGuardState,
    record_call,
    validate_duplicate_call,
    validate_max_calls,
    validate_tool_allowed,
)
from src.phase5.tool_schemas import AgentTurnResult, ToolCall, ToolResult
from src.phase5.tools import create_escalation_ticket, lookup_ticket_status


class Phase5ToolAgent:
    """Phase 5 agent that selects and executes tools with safety safeguards."""

    def __init__(self) -> None:
        self.guard_state = ToolGuardState(max_calls_per_turn=2)

    def run_turn(self, user_message: str) -> AgentTurnResult:
        self.guard_state = ToolGuardState(max_calls_per_turn=2)

        selected = choose_tool(user_message)
        if selected is None:
            return AgentTurnResult(
                user_message=user_message,
                selected_tool=None,
                final_response=(
                    "No tool required for this request. I can provide a direct policy-safe response."
                ),
                safety_flags={"tool_used": False},
            )

        guard_error = self._guard_check(selected)
        if guard_error:
            return AgentTurnResult(
                user_message=user_message,
                selected_tool=selected.name,
                tool_args=selected.args,
                escalation_recommended=True,
                escalation_reason=guard_error,
                final_response=(
                    f"Tool call was blocked by safeguards ({guard_error}). "
                    "Escalating to human specialist."
                ),
                safety_flags={"tool_blocked": True},
            )

        record_call(self.guard_state, selected)
        result = self._execute_tool(selected)

        escalate = (not result.success) or selected.name == "create_escalation_ticket"
        esc_reason = result.error if not result.success else (
            "sensitive_or_unresolved_case" if selected.name == "create_escalation_ticket" else ""
        )

        final_response = self._compose_response(selected, result)
        return AgentTurnResult(
            user_message=user_message,
            selected_tool=selected.name,
            tool_args=selected.args,
            tool_result=result,
            escalation_recommended=escalate,
            escalation_reason=esc_reason,
            final_response=final_response,
            safety_flags={"tool_used": True, "tool_success": result.success},
        )

    def _guard_check(self, tool_call: ToolCall) -> str:
        ok, error = validate_tool_allowed(tool_call)
        if not ok:
            return error

        ok, error = validate_max_calls(self.guard_state)
        if not ok:
            return error

        ok, error = validate_duplicate_call(self.guard_state, tool_call)
        if not ok:
            return error

        return ""

    @staticmethod
    def _execute_tool(tool_call: ToolCall) -> ToolResult:
        if tool_call.name == "lookup_ticket_status":
            return lookup_ticket_status(ticket_id=tool_call.args.get("ticket_id", ""))

        if tool_call.name == "create_escalation_ticket":
            return create_escalation_ticket(
                reason=tool_call.args.get("reason", ""),
                severity=tool_call.args.get("severity", ""),
                summary=tool_call.args.get("summary", ""),
            )

        return ToolResult(tool_name=tool_call.name, success=False, output={}, error="tool_not_implemented")

    @staticmethod
    def _compose_response(tool_call: ToolCall, result: ToolResult) -> str:
        if result.success and tool_call.name == "lookup_ticket_status":
            return (
                f"Ticket {result.output.get('ticket_id')} is {result.output.get('status')} in "
                f"{result.output.get('queue')} queue with {result.output.get('priority')} priority."
            )

        if result.success and tool_call.name == "create_escalation_ticket":
            return (
                f"Escalation created: {result.output.get('escalation_id')} "
                f"(severity={result.output.get('severity')})."
            )

        return (
            f"Tool call failed ({result.error}). Unable to safely complete this action automatically; "
            "escalating to human support."
        )
