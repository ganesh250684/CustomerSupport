# 1) Working AI Agent (with Source and Run Instructions)

This file is self-contained for reviewers.

Referenced markdown sources included below:
- `final_submission/working_ai_agent.md`

---

## Embedded Content: `final_submission/working_ai_agent.md`

# Working AI Agent

## System
Customer Support AI Support Resolution Agent for SaaS support workflow, implemented across Phases 2-9 with safety-first controls.

## Core Runtime Components
- Baseline support agent: `src/phase2/baseline_agent.py`
- RAG agent entry file: `src/phase4/rag_agent.py`
- Tool-usage agent entry file: `src/phase5/tool_agent.py`
- Planning and memory entry file: `src/phase6/multiturn_agent.py`
- Adaptive behavior entry file: `src/phase7/adaptive_agent.py`
- Deployment-ready runtime service: `src/phase8/service.py`

## Direct Run Commands (Per Phase)
Run these from project root `d:/IITM/CustomerSupport`.

1. Phase 2 (baseline)
- File: `src/phase2/baseline_agent.py`
- Command: `python scripts/run_phase2_demo.py`

2. Phase 3 (prompt strategy comparison)
- File: `src/phase3/prompt_evaluator.py`
- Command: `python scripts/run_phase3_prompt_eval.py`

3. Phase 4 (RAG)
- File: `src/phase4/rag_agent.py`
- Commands:
   - `python scripts/run_phase4_indexing.py`
   - `python scripts/run_phase4_rag_eval.py`

4. Phase 5 (tools + safeguards)
- File: `src/phase5/tool_agent.py`
- Command: `python scripts/run_phase5_tool_eval.py`

5. Phase 6 (planning + memory)
- File: `src/phase6/multiturn_agent.py`
- Command: `python scripts/run_phase6_multiturn_eval.py`

6. Phase 7 (adaptation)
- File: `src/phase7/adaptive_agent.py`
- Command: `python scripts/run_phase7_adaptation_eval.py`

7. Phase 8 (deployment runtime)
- File: `src/phase8/service.py`
- Commands:
   - `python -m uvicorn src.phase8.service:app --host 127.0.0.1 --port 8010`
   - `python scripts/run_phase8_runtime_eval.py`

8. Phase 9 (evaluation and engineering review)
- File: `src/phase9/metrics.py`
- Command: `python scripts/run_phase9_evaluation.py`

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
   - `phase_artifacts/phase8/outputs/deployment_readiness_results.json`
   - `phase_artifacts/phase8/outputs/latency_error_summary.json`
   - `phase_artifacts/phase8/outputs/runtime_logs.jsonl`
- Runtime comparison report:
   - `reports/phase8_runtime_comparison.md`

