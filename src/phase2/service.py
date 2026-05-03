from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from src.observability.logger import SafeJsonLogger
from src.phase2.baseline_agent import BaselineSupportAgent


app = FastAPI(title="Phase 2 Baseline Support Agent", version="0.1.0")
agent = BaselineSupportAgent()
logger = SafeJsonLogger("logs/phase2_api_interactions.jsonl")


class QueryRequest(BaseModel):
    user_message: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "phase": "phase2"}


@app.post("/respond")
def respond(request: QueryRequest) -> dict:
    response = agent.respond(request.user_message)
    payload = response.to_dict()
    logger.write_event(
        {
            "event": "api_interaction",
            "phase": "phase2_baseline",
            "user_input": request.user_message,
            "agent_output": payload,
        }
    )
    return payload
