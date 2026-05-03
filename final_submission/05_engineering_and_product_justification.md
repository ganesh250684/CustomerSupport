# 5) Engineering and Product Justification

This file is self-contained for reviewers.

Referenced markdown sources included below:
- `final_submission/engineering_product_justification.md`
- `reports/phase8_implementation.md`
- `reports/phase9_implementation.md`

Non-markdown supporting artifact path:
- `phase_artifacts/phase9/outputs/evaluation_metrics.json`

---

## Embedded Content: `final_submission/engineering_product_justification.md`

# Engineering and Product Justification

## Product Justification
Chosen workflow: SaaS customer support resolution with human-in-the-loop approval.

Why this workflow is practical:
- high-frequency operational use case
- clear business value from faster and safer resolution
- explicit compliance and policy constraints
- direct measurable outcomes (latency, escalation correctness, refusal correctness)

## Architecture Justification
System evolved in controlled phases:
- Phase 2 baseline for deterministic control and limitation discovery
- Phase 3 LLM prompt strategy comparison for behavior tuning
- Phase 4 retrieval grounding to reduce unsupported claims
- Phase 5 tool orchestration for operational actions
- Phase 6 planning + memory for multi-turn coherence
- Phase 7 adaptation from user feedback
- Phase 8 deployment readiness with observability and graceful failures
- Phase 9 integrated evaluation and review

Why this design is justified:
- prioritizes reliability and auditable behavior over unnecessary complexity
- each capability added with explicit evidence and regression visibility
- safety behaviors are integrated into every stage rather than bolted on

## Safety-First Engineering Decisions
- refusal path for policy-violating prompts
- anti-fabrication fallback when evidence is missing
- mandatory escalation paths for sensitive/unresolved requests
- redaction pipeline before writing logs
- failure taxonomy and degraded-mode response strategy

## Reliability and Explainability Decisions
- structured outputs and per-stage logs
- trace IDs for request-level observability
- comparison harnesses (prompt variants, with-vs-without retrieval, before-vs-after adaptation)
- root-cause reproduction and explicit fix evidence

## Tradeoffs and Limitations
- lightweight local simulation for tools and deployment, not full enterprise integration
- current adaptation logic is rule-driven and sensitive to feedback sample quality
- consistency scores indicate room for calibration improvements

## Why This Is Deployment-Ready for a Capstone Scope
- reproducible local service
- explicit observability artifacts
- validated graceful failure behavior
- centralized evidence package for engineering review

## Linked Artifacts
- `reports/phase8_implementation.md`
- `reports/phase9_implementation.md`
- `phase_artifacts/phase9/outputs/evaluation_metrics.json`

---

## Embedded Content: `reports/phase8_implementation.md`

# Phase 8 Implementation Report

## Goal
Prepare deployment-ready runtime packaging with observability, latency/error capture, and graceful failure handling.

## Scope Clarification
Phase 8 focuses on:
1. Local deployment packaging.
2. Request tracing and runtime logging.
3. Latency and error metric capture.
4. Graceful handling of dependency failures.
5. Operational assumptions and limitations.

## Technical Implementation Details

### Deployment Packaging
- FastAPI service entrypoint: `src/phase8/service.py`
- Local run script: `deploy/phase8/run_local.ps1`
- Runtime test harness: `scripts/run_phase8_runtime_eval.py`

### Request Tracing and Logging
- Module: `src/phase8/observability.py`
- Per-request trace id generated using UUID.
- Structured JSONL runtime logs written to:
  - `outputs/phase8/runtime_logs.jsonl`
- Logged fields include:
  - `trace_id`
  - stage (`retrieval`, `llm`, `tool`, `final`)
  - status
  - error category/detail
  - latency
  - escalation decision
- PII-safe handling:
  - user and response text are redacted before writing logs.

### Runtime Failure Taxonomy
- `retrieval_failure`
- `llm_failure`
- `tool_failure`

### Graceful Failure Behavior
- Retrieval failure:
  - continue in degraded mode with fallback context
- LLM failure:
  - return safe fallback response
  - force escalation (`model_unavailable`)
- Tool failure:
  - keep response safe
  - force escalation (`tool_execution_failed`)

### Runtime Evaluation
- Cases file: `data/phase8/runtime_eval_cases.json`
- Generated outputs:
  - `outputs/phase8/deployment_readiness_results.json`
  - `outputs/phase8/latency_error_summary.json`
  - `reports/phase8_runtime_comparison.md`

## Requirement-to-Task Verification

1. Deploy locally or on cloud
- Status: Complete (local deployment)
- Evidence:
  - `src/phase8/service.py`
  - `deploy/phase8/run_local.ps1`

2. Capture latency and error logs
- Status: Complete
- Evidence:
  - `outputs/phase8/runtime_logs.jsonl`
  - `outputs/phase8/latency_error_summary.json`

3. Demonstrate graceful failure handling
- Status: Complete
- Evidence:
  - failure simulation cases in `data/phase8/runtime_eval_cases.json`
  - degraded-mode responses in `outputs/phase8/deployment_readiness_results.json`

4. Document deployment assumptions and limitations
- Status: Complete
- Evidence: assumptions section below

## Deployment Assumptions and Limitations
- Assumptions:
  - local Python virtual environment is available
  - FastAPI/uvicorn dependencies are installed
  - local file-system write permissions for output logs
- Limitations:
  - no external production gateway or auth layer in this phase
  - failure simulation is controlled by request flags
  - single-process local runtime only (no horizontal scaling)

## Expected New Failure Modes
- log volume growth under sustained traffic.
- partial loss of observability if disk write fails.
- simplistic error taxonomy may under-classify composite failures.

These are planned for stronger production hardening in later engineering steps.

---

## Embedded Content: `reports/phase9_implementation.md`

# Phase 9 Implementation Report

## Goal
Evaluate response quality, reliability, safety, and engineering readiness; include root-cause analysis and improvement roadmap.

## Scope Clarification
Phase 9 focuses on:
1. Test harness across prior phase outputs.
2. Quality and consistency metrics.
3. Safety/ethics checks.
4. Root-cause analysis with before/after fix evidence.
5. Engineering review and roadmap.

## Technical Implementation Details

### Evaluation Harness
- Manifest: `data/phase9/evaluation_manifest.json`
- Runner: `scripts/run_phase9_evaluation.py`
- Inputs consumed from prior phases:
  - phase3 prompt results
  - phase4 retrieval results
  - phase5 tool results
  - phase7 adaptation results
  - phase8 runtime summaries

### Metrics Computation
- Module: `src/phase9/metrics.py`
- Computed families:
  - prompt behavior metrics
  - retrieval/citation metrics
  - tool usage metrics
  - runtime latency/error metrics

### Consistency and Safety Checks
- Module: `src/phase9/consistency.py`
- Consistency:
  - refusal consistency across before/after adaptation
  - escalation consistency across sensitive prompts
- Safety checklist from deployment runtime:
  - policy-violation refusal
  - llm failure graceful escalation
  - retrieval degraded-mode behavior

### Root Cause Analysis
- Module: `src/phase9/root_cause.py`
- Demonstrated failure:
  - cross-conversation memory contamination
- Before/after evidence generated by reproducible function
- Fix:
  - initialize/reset memory per conversation context

### Generated Artifacts
- `outputs/phase9/evaluation_metrics.json`
- `reports/phase9_evaluation_report.md`
- `reports/phase9_engineering_review.md`

## Requirement-to-Task Verification

1. Create evaluation prompts and test scenarios
- Status: Complete
- Evidence: `data/phase9/evaluation_manifest.json` + linked prior test sets

2. Measure quality and consistency metrics
- Status: Complete
- Evidence: `outputs/phase9/evaluation_metrics.json`

3. Perform root cause analysis
- Status: Complete
- Evidence: root-cause section in `reports/phase9_evaluation_report.md`

4. Propose next-step improvements
- Status: Complete
- Evidence: roadmap section in `reports/phase9_evaluation_report.md`

5. Review safety and ethics
- Status: Complete
- Evidence: `reports/phase9_engineering_review.md`
