# Phase 7 Evidence List

## Required Evidence Mapping

1. Feedback storage proof
- Code: `src/phase7/feedback_store.py`
- Output: `outputs/phase7/feedback_log.jsonl`
- Check: feedback events include reason tags and helpful labels

2. Adaptation logic proof
- Code: `src/phase7/adaptive_policy.py`
- Output: `outputs/phase7/adaptation_results.json`
- Check: adapted config differs from baseline when feedback warrants change

3. Before-vs-after proof
- Report: `reports/phase7_adaptation_comparison.md`
- Output: `outputs/phase7/adaptation_results.json`
- Check: per-case before and after response comparison exists

4. Change explanation proof
- Report sections:
  - adaptation configuration
  - feedback summary
  - what changed column in comparison table

5. Safety continuity proof
- Code: `src/phase7/adaptive_agent.py`
- Check: policy-bypass refusal remains enforced after adaptation

## Manual Commands
1. `python scripts/run_phase7_adaptation_eval.py`
2. `pwsh -File scripts/sync_phase_artifacts.ps1`

## Submission Attachments
- `reports/phase7_implementation.md`
- `reports/phase7_evidence_list.md`
- `reports/phase7_manual_verification_steps.md`
- `reports/phase7_adaptation_comparison.md`
- `outputs/phase7/adaptation_results.json`
- `outputs/phase7/feedback_log.jsonl`
