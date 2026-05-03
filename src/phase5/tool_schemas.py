from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ToolCall:
    name: str
    args: Dict[str, Any]


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    output: Dict[str, Any]
    error: str = ""


@dataclass
class AgentTurnResult:
    user_message: str
    selected_tool: Optional[str]
    tool_args: Dict[str, Any] = field(default_factory=dict)
    tool_result: Optional[ToolResult] = None
    escalation_recommended: bool = False
    escalation_reason: str = ""
    final_response: str = ""
    safety_flags: Dict[str, bool] = field(default_factory=dict)
