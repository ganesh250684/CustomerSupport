# Phase 7 Manual Verification Steps

Run in PowerShell from project root.

## 1. Execute adaptation evaluation
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe scripts/run_phase7_adaptation_eval.py

Expected output:
- Generated Phase 7 adaptation evaluation.
- Results: outputs/phase7/adaptation_results.json
- Feedback log: outputs/phase7/feedback_log.jsonl
- Table: reports/phase7_adaptation_comparison.md

## 2. Verify adaptation configuration changed
1. Open outputs/phase7/adaptation_results.json
2. Compare baseline_config vs adapted_config
3. Confirm at least one knob changed due to feedback trends

## 3. Verify before-vs-after behavior evidence
1. Open reports/phase7_adaptation_comparison.md
2. Confirm each case has before and after rows and change notes

## 4. Verify safety remains intact
1. Check policy-bypass prompt case in adaptation outputs
2. Confirm refusal still occurs after adaptation

## 5. Sync centralized artifacts
1. pwsh -File scripts/sync_phase_artifacts.ps1
2. Confirm files under phase_artifacts/phase7/documentation and phase_artifacts/phase7/outputs
