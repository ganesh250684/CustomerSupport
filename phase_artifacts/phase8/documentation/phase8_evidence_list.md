# Phase 8 Evidence List

## Required Evidence Mapping

1. Deployment packaging proof
- Files:
  - `src/phase8/service.py`
  - `deploy/phase8/run_local.ps1`
- Check: service boots and health endpoint returns ok

2. Runtime tracing/logging proof
- File: `outputs/phase8/runtime_logs.jsonl`
- Check: each request has trace_id and stage logs

3. Latency/error capture proof
- Files:
  - `outputs/phase8/deployment_readiness_results.json`
  - `outputs/phase8/latency_error_summary.json`
- Check: p95 and error category counts are present

4. Graceful failure proof
- Case set: `data/phase8/runtime_eval_cases.json`
- Check degraded responses for retrieval/llm/tool failures

5. Operational documentation proof
- File: `reports/phase8_implementation.md`
- Check assumptions and limitations section exists

## Manual Commands
1. `python scripts/run_phase8_runtime_eval.py`
2. `pwsh -File deploy/phase8/run_local.ps1`
3. `pwsh -File scripts/sync_phase_artifacts.ps1`

## Submission Attachments
- `reports/phase8_implementation.md`
- `reports/phase8_evidence_list.md`
- `reports/phase8_manual_verification_steps.md`
- `reports/phase8_runtime_comparison.md`
- `outputs/phase8/deployment_readiness_results.json`
- `outputs/phase8/latency_error_summary.json`
- `outputs/phase8/runtime_logs.jsonl`
