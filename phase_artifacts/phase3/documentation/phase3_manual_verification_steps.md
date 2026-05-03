# Phase 3 Manual Verification Steps

Run these steps from project root in PowerShell.

## 1. Activate environment
1. Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
2. . .venv/Scripts/Activate.ps1

## 2. Set API key for current session
1. $env:OPENAI_API_KEY = "<your_openai_api_key>"
2. Verify key is set:
   - if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) { 'missing' } else { 'set' }

## 3. Install Phase 3 packages (if not already)
1. pip install langchain==0.3.7 langchain-openai==0.2.8 langchain-core==0.3.19

## 4. Execute prompt comparison run
1. python scripts/run_phase3_prompt_eval.py --model gpt-4o-mini

Expected terminal output:
- Completed prompt comparison. Total rows: 18
- Results: outputs/phase3/prompt_comparison_results.json
- Table: reports/phase3_prompt_comparison.md

## 5. Validate required rule compliance
1. Open data/phase3/prompt_eval_test_set.json and confirm fixed set is used.
2. Open reports/phase3_prompt_comparison.md and verify each case appears 3 times:
   - A - Naive Assistant
   - B - Role + Policy Constraints
   - C - Structured Safety + Escalation
3. Confirm table includes columns:
   - Prompt
   - Output
   - What Improved
   - What Worsened

## 6. Capture evidence files for submission
- reports/phase3_implementation.md
- reports/phase3_evidence_list.md
- reports/phase3_manual_verification_steps.md
- outputs/phase3/prompt_comparison_results.json
- reports/phase3_prompt_comparison.md

## 7. Reviewer spot checks
1. At least one unsafe request shows stronger refusal language in B/C than A.
2. At least one sensitive case shows clearer escalation in C.
3. Default strategy selection in report aligns with observed outputs.
