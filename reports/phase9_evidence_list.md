# Phase 9 Evidence List

## Required Evidence Mapping

1. Evaluation harness proof
- Files:
  - `data/phase9/evaluation_manifest.json`
  - `scripts/run_phase9_evaluation.py`
- Check: multi-phase inputs are loaded and processed

2. Quality/consistency metrics proof
- File: `outputs/phase9/evaluation_metrics.json`
- Check:
  - quality metrics sections present
  - consistency metrics sections present

3. Root cause analysis proof
- Files:
  - `src/phase9/root_cause.py`
  - `reports/phase9_evaluation_report.md`
- Check: before/after behavior and fix documented

4. Safety/ethics review proof
- File: `reports/phase9_engineering_review.md`
- Check: safety pass/fail and residual risk statements

5. Improvement roadmap proof
- File: `reports/phase9_evaluation_report.md`
- Check: concrete next steps listed

## Manual Commands
1. `python scripts/run_phase9_evaluation.py`
2. `pwsh -File scripts/sync_phase_artifacts.ps1`

## Submission Attachments
- `reports/phase9_implementation.md`
- `reports/phase9_evidence_list.md`
- `reports/phase9_manual_verification_steps.md`
- `reports/phase9_evaluation_report.md`
- `reports/phase9_engineering_review.md`
- `outputs/phase9/evaluation_metrics.json`
