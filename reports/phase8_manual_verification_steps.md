# Phase 8 Manual Verification Steps

Run from project root in PowerShell.

## 1. Execute runtime evaluation
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe scripts/run_phase8_runtime_eval.py

Expected outputs:
- outputs/phase8/deployment_readiness_results.json
- outputs/phase8/latency_error_summary.json
- reports/phase8_runtime_comparison.md
- outputs/phase8/runtime_logs.jsonl

## 2. Verify graceful failure cases
1. Open outputs/phase8/deployment_readiness_results.json
2. Confirm:
- retrieval failure case sets degraded_mode true
- llm failure case escalates with model_unavailable
- tool failure case escalates with tool_execution_failed

## 3. Verify latency and error summary
1. Open outputs/phase8/latency_error_summary.json
2. Confirm min/avg/p95/max latency and error_counts are populated

## 4. Run local deployment manually
1. pwsh -File deploy/phase8/run_local.ps1
2. In another terminal:
- Invoke-RestMethod -Method GET -Uri http://127.0.0.1:8010/health
- Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8010/resolve -ContentType 'application/json' -Body '{"user_message":"I was charged after cancellation"}'

## 5. Sync centralized artifacts
1. pwsh -File scripts/sync_phase_artifacts.ps1
2. Confirm files under phase_artifacts/phase8/documentation and phase_artifacts/phase8/outputs
