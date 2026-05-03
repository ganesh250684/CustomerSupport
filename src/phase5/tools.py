from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from src.phase5.tool_schemas import ToolResult


MOCK_TICKETS: Dict[str, Dict[str, Any]] = {
    "TCK-1001": {
        "status": "open",
        "queue": "billing",
        "priority": "medium",
        "summary": "charged after cancellation",
    },
    "TCK-2002": {
        "status": "pending_security_review",
        "queue": "security",
        "priority": "high",
        "summary": "suspicious login lockout",
    },
}


def lookup_ticket_status(ticket_id: str) -> ToolResult:
    if not ticket_id or not ticket_id.startswith("TCK-"):
        return ToolResult(
            tool_name="lookup_ticket_status",
            success=False,
            output={},
            error="invalid_ticket_id_format",
        )

    ticket = MOCK_TICKETS.get(ticket_id)
    if not ticket:
        return ToolResult(
            tool_name="lookup_ticket_status",
            success=False,
            output={},
            error="ticket_not_found",
        )

    return ToolResult(
        tool_name="lookup_ticket_status",
        success=True,
        output={"ticket_id": ticket_id, **ticket},
    )


def create_escalation_ticket(reason: str, severity: str, summary: str) -> ToolResult:
    if severity not in {"low", "medium", "high", "critical"}:
        return ToolResult(
            tool_name="create_escalation_ticket",
            success=False,
            output={},
            error="invalid_severity",
        )

    if not reason or not summary:
        return ToolResult(
            tool_name="create_escalation_ticket",
            success=False,
            output={},
            error="missing_required_fields",
        )

    escalation_id = f"ESC-{int(datetime.now(timezone.utc).timestamp())}"
    return ToolResult(
        tool_name="create_escalation_ticket",
        success=True,
        output={
            "escalation_id": escalation_id,
            "severity": severity,
            "reason": reason,
            "summary": summary,
            "status": "created",
        },
    )
