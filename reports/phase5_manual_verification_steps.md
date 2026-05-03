# Phase 5 Manual Verification Steps

Run these in PowerShell from project root.

## 1. Run tool evaluation
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe scripts/run_phase5_tool_eval.py

Expected terminal output:
- Generated Phase 5 tool evaluation rows: 5
- Results: outputs/phase5/tool_run_results.json
- Audit: outputs/phase5/tool_audit_log.jsonl
- Table: reports/phase5_tool_usage_comparison.md

## 2. Verify required behavior
1. Open outputs/phase5/tool_run_results.json
2. Check:
- T5-01 selected_tool is lookup_ticket_status and success true
- T5-02 selected_tool is create_escalation_ticket and success true
- T5-03 tool call fails safely with escalation
- T5-04 is blocked by safeguard and escalated
- T5-05 has no tool execution

## 3. Verify safeguard implementation in code
1. src/phase5/safeguards.py should include:
- allowlist check
- max calls check
- duplicate-call suppression

## 4. Sync centralized artifacts
1. pwsh -File scripts/sync_phase_artifacts.ps1
2. Confirm:
- phase_artifacts/phase5/documentation
- phase_artifacts/phase5/outputs
