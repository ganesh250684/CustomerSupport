from __future__ import annotations

from pydantic import BaseModel, Field


class ResolveRequest(BaseModel):
    user_message: str
    simulate_retrieval_failure: bool = False
    simulate_llm_failure: bool = False
    simulate_tool_failure: bool = False


class ResolveResponse(BaseModel):
    trace_id: str
    response: str
    escalation: bool
    escalation_reason: str
    degraded_mode: bool
    latency_ms: float = Field(ge=0)
    error_category: str = ""
