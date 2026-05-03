# Phase 9 Manual Verification Steps

Run from project root in PowerShell.

## 1. Execute Phase 9 evaluation
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe scripts/run_phase9_evaluation.py

Expected outputs:
- outputs/phase9/evaluation_metrics.json
- reports/phase9_evaluation_report.md
- reports/phase9_engineering_review.md

## 2. Verify metric sections
1. Open outputs/phase9/evaluation_metrics.json
2. Confirm keys:
- quality_metrics
- consistency_metrics
- safety_checks
- root_cause_analysis
- improvement_roadmap

## 3. Verify root-cause before/after evidence
1. Open reports/phase9_evaluation_report.md
2. Confirm issue, root cause, before behavior, after behavior, and fix applied are present

## 4. Verify safety/ethics review
1. Open reports/phase9_engineering_review.md
2. Confirm safety posture and residual risks are documented

## 5. Sync centralized artifacts
1. pwsh -File scripts/sync_phase_artifacts.ps1
2. Confirm files under phase_artifacts/phase9/documentation and phase_artifacts/phase9/outputs
