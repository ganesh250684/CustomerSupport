from __future__ import annotations

from fastapi import FastAPI

from src.phase8.observability import RuntimeTracer
from src.phase8.runtime_models import ResolveRequest, ResolveResponse


app = FastAPI(title="Phase 8 Deployment Ready Service", version="0.1.0")
tracer = RuntimeTracer()


def _retrieve_context(user_message: str, simulate_failure: bool) -> str:
    if simulate_failure:
        raise RuntimeError("retrieval_backend_unavailable")
    if "refund" in user_message.lower() or "charged" in user_message.lower():
        return "refund_policy_context"
    if "suspicious" in user_message.lower() or "lock" in user_message.lower():
        return "security_procedure_context"
    return "general_support_context"


def _call_model(user_message: str, context: str, simulate_failure: bool) -> str:
    if simulate_failure:
        raise RuntimeError("llm_provider_timeout")
    if context == "refund_policy_context":
        return "Please share invoice id and cancellation date to validate refund eligibility."
    if context == "security_procedure_context":
        return "This appears sensitive; complete verification and escalate to security support."
    return "Please share additional details so I can provide a policy-safe resolution."


def _tool_action(user_message: str, simulate_failure: bool) -> str:
    if simulate_failure:
        raise RuntimeError("tool_timeout")
    if "suspicious" in user_message.lower():
        return "escalation_ticket_created"
    return "no_tool_needed"


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "phase": "phase8", "service": "deployment_readiness"}


@app.post("/resolve", response_model=ResolveResponse)
def resolve(request: ResolveRequest) -> ResolveResponse:
    trace_id = tracer.new_trace_id()
    start = tracer.start_timer()

    degraded_mode = False
    error_category = ""
    escalation = False
    escalation_reason = ""

    try:
        context = _retrieve_context(request.user_message, request.simulate_retrieval_failure)
    except Exception as exc:  # noqa: BLE001
        degraded_mode = True
        error_category = "retrieval_failure"
        context = "fallback_no_retrieval"
        tracer.log_event(
            {
                "trace_id": trace_id,
                "stage": "retrieval",
                "status": "error",
                "error_category": error_category,
                "error_detail": str(exc),
                "user_message": request.user_message,
            }
        )

    try:
        response = _call_model(request.user_message, context, request.simulate_llm_failure)
    except Exception as exc:  # noqa: BLE001
        degraded_mode = True
        error_category = "llm_failure"
        response = (
            "I am currently unable to generate a full response safely. "
            "I will escalate this case to a human specialist."
        )
        escalation = True
        escalation_reason = "model_unavailable"
        tracer.log_event(
            {
                "trace_id": trace_id,
                "stage": "llm",
                "status": "error",
                "error_category": error_category,
                "error_detail": str(exc),
                "user_message": request.user_message,
            }
        )

    try:
        tool_outcome = _tool_action(request.user_message, request.simulate_tool_failure)
        if tool_outcome == "escalation_ticket_created":
            escalation = True
            escalation_reason = escalation_reason or "sensitive_case"
    except Exception as exc:  # noqa: BLE001
        degraded_mode = True
        if not error_category:
            error_category = "tool_failure"
        escalation = True
        escalation_reason = escalation_reason or "tool_execution_failed"
        tracer.log_event(
            {
                "trace_id": trace_id,
                "stage": "tool",
                "status": "error",
                "error_category": "tool_failure",
                "error_detail": str(exc),
                "user_message": request.user_message,
            }
        )

    if "bypass" in request.user_message.lower() or "skip verification" in request.user_message.lower():
        response = "I cannot assist with bypassing policy controls."
        escalation = True
        escalation_reason = "policy_violation_request"

    latency_ms = tracer.elapsed_ms(start)

    tracer.log_event(
        {
            "trace_id": trace_id,
            "stage": "final",
            "status": "ok",
            "user_message": request.user_message,
            "response": response,
            "degraded_mode": degraded_mode,
            "error_category": error_category,
            "latency_ms": latency_ms,
            "escalation": escalation,
            "escalation_reason": escalation_reason,
        }
    )

    return ResolveResponse(
        trace_id=trace_id,
        response=response,
        escalation=escalation,
        escalation_reason=escalation_reason,
        degraded_mode=degraded_mode,
        latency_ms=latency_ms,
        error_category=error_category,
    )
