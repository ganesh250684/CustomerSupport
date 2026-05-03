from __future__ import annotations

import re
from typing import Dict, Optional

from src.phase5.tool_schemas import ToolCall


TICKET_ID_RE = re.compile(r"\bTCK-\d{4,}\b", re.IGNORECASE)


def choose_tool(user_message: str) -> Optional[ToolCall]:
    text = user_message.lower()

    if "delete account" in text or "drop database" in text:
        return ToolCall(name="dangerous_internal_action", args={"raw": user_message})

    if "ticket" in text or "status" in text:
        ticket_match = TICKET_ID_RE.search(user_message)
        ticket_id = ticket_match.group(0).upper() if ticket_match else ""
        return ToolCall(name="lookup_ticket_status", args={"ticket_id": ticket_id})

    if any(token in text for token in ["suspicious", "legal", "abuse", "escalate", "urgent", "security"]):
        return ToolCall(
            name="create_escalation_ticket",
            args={
                "reason": "sensitive_or_unresolved_case",
                "severity": "high",
                "summary": user_message[:160],
            },
        )

    return None
