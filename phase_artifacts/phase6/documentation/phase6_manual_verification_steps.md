# Phase 6 Manual Verification Steps

Run these in PowerShell from project root.

## 1. Execute multi-turn evaluation
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe scripts/run_phase6_multiturn_eval.py

Expected output:
- Generated Phase 6 multi-turn evaluation.
- Results: outputs/phase6/multiturn_results.json
- Memory snapshot: outputs/phase6/memory_state_snapshot.json
- Table: reports/phase6_multiturn_comparison.md

## 2. Verify planning steps
1. Open outputs/phase6/multiturn_results.json
2. Check each turn has plan steps:
- classify_intent
- review_memory_context
- select_response_strategy
- safety_verification
- finalize_response

## 3. Verify memory retention and reset
1. In conversation M6-03, ensure "reset memory" turn returns reset confirmation.
2. Check outputs/phase6/memory_state_snapshot.json contains bounded recent turns only.

## 4. Verify redaction in memory
1. In memory_state_snapshot, confirm email/phone values are redacted tokens, not raw PII.

## 5. Sync centralized artifacts
1. pwsh -File scripts/sync_phase_artifacts.ps1
2. Confirm files under phase_artifacts/phase6/documentation and phase_artifacts/phase6/outputs
