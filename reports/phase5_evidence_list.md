# Phase 5 Evidence List

## Required Evidence Mapping

1. Tool definition proof
- Files:
  - `src/phase5/tools.py`
  - `src/phase5/tool_schemas.py`
- Check: at least two tools with validated arguments

2. Tool calling logic proof
- Files:
  - `src/phase5/router.py`
  - `src/phase5/tool_agent.py`
- Check: selected tool and args recorded per case

3. Correct tool selection proof
- Cases:
  - `T5-01` -> `lookup_ticket_status`
  - `T5-02` -> `create_escalation_ticket`
- Evidence: `outputs/phase5/tool_run_results.json`

4. Incorrect/failed tool usage proof
- Cases:
  - `T5-03` invalid/missing ticket id causes tool failure
  - `T5-04` disallowed action is blocked by safeguard
- Evidence: `outputs/phase5/tool_run_results.json` and `outputs/phase5/tool_audit_log.jsonl`

5. Safeguard proof
- Enforced controls:
  - allowlist
  - max calls per turn
  - duplicate call suppression
- Evidence: `src/phase5/safeguards.py` + blocked result rows in outputs

6. Evaluation summary proof
- Table: `reports/phase5_tool_usage_comparison.md`
- Output: `outputs/phase5/tool_run_results.json`

## Manual Commands
1. `python scripts/run_phase5_tool_eval.py`
2. `pwsh -File scripts/sync_phase_artifacts.ps1`

## Submission Attachments
- `reports/phase5_implementation.md`
- `reports/phase5_evidence_list.md`
- `reports/phase5_tool_usage_comparison.md`
- `outputs/phase5/tool_run_results.json`
- `outputs/phase5/tool_audit_log.jsonl`
