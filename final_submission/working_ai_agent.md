# Working AI Agent

## System
Customer Support AI Support Resolution Agent for SaaS support workflow, implemented across Phases 2-9 with safety-first controls.

## Core Runtime Components
- Baseline support agent: `src/agent/baseline_agent.py`
- RAG agent components: `src/phase4/`
- Tool-usage agent components: `src/phase5/`
- Planning and memory components: `src/phase6/`
- Adaptive behavior components: `src/phase7/`
- Deployment-ready runtime service: `src/phase8/service.py`

## How to Run (Local)
1. Activate environment
- PowerShell:
  - Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  - . .venv/Scripts/Activate.ps1

2. Start deployment-ready API
- python -m uvicorn src.phase8.service:app --host 127.0.0.1 --port 8010

3. Health check
- GET http://127.0.0.1:8010/health

4. Resolve request example
- POST http://127.0.0.1:8010/resolve
- JSON body example:
  {
    "user_message": "I was charged after cancellation and need help.",
    "simulate_retrieval_failure": false,
    "simulate_llm_failure": false,
    "simulate_tool_failure": false
  }

## Safety Guarantees Demonstrated
- Refuses policy-bypass prompts.
- Escalates sensitive/unresolved cases.
- Avoids policy fabrication with uncertainty fallback when evidence is missing.
- Uses PII-safe logging (redaction before persistence).

## Deployment-Readiness Evidence
- Runtime outputs:
  - `outputs/phase8/deployment_readiness_results.json`
  - `outputs/phase8/latency_error_summary.json`
  - `outputs/phase8/runtime_logs.jsonl`
- Runtime comparison report:
  - `reports/phase8_runtime_comparison.md`
