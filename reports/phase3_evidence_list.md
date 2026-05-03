# Phase 3 Evidence List

This list maps required evidence items to artifacts and manual steps.

## Required Prompt Comparison Rule
Must show same test set across 2-3 prompt variants with comparison table.

Evidence locations:
- Test set: `data/phase3/prompt_eval_test_set.json`
- Prompt variants: `src/phase3/prompt_variants.py`
- Runner: `scripts/run_phase3_prompt_eval.py`
- Results JSON: `outputs/phase3/prompt_comparison_results.json`
- Comparison table: `reports/phase3_prompt_comparison.md`

## Manual Run Steps
1. Ensure `OPENAI_API_KEY` is set in environment.
2. Install packages:
   - `pip install langchain==0.3.7 langchain-openai==0.2.8 langchain-core==0.3.19`
3. Run:
   - `python scripts/run_phase3_prompt_eval.py --model gpt-4o-mini`

## What to Capture for Submission
1. Terminal output showing row count completion.
2. Snippet proving each case was run across A/B/C variants.
3. Excerpt from comparison table highlighting improved/worsened columns.
4. Decision note selecting default prompt and tradeoff rationale.

## Expected Gaps at End of Phase 3
- No retrieval grounding yet (Phase 4).
- No tool calls yet (Phase 5).
- No memory/adaptation yet (Phases 6/7).
