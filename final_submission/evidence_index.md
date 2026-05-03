# Evidence Index (Rubric Mapping)

## Required Final Submission Package
1. Problem framing document
- `final_submission/problem_framing_document.md`
- Assignment-aligned alias: `final_submission/01_problem_framing_document_1_to_2_pages.md`

2. Demo script (3-5 forced interactions) + evidence
- `final_submission/demo_script.md`
- Assignment-aligned alias: `final_submission/02_demo_script_3_to_5_forced_interactions_plus_evidence.md`
- Evidence paths: `phase_artifacts/phase8/outputs/deployment_readiness_results.json`, `phase_artifacts/phase8/outputs/runtime_logs.jsonl`

3. Prompt comparison table (same test set, 2-3 variants, insights)
- `final_submission/prompt_comparison_table.md`
- Assignment-aligned alias: `final_submission/03_prompt_comparison_table_same_test_set_2_to_3_variants_insights.md`
- Additional evidence wrapper: `final_submission/06_required_evidence_rules_checklist.md`

4. Evaluation report
- `final_submission/evaluation_report.md`
- Detailed evidence: `reports/phase9_evaluation_report.md`

5. Engineering and product justification
- `final_submission/engineering_product_justification.md`
- Assignment-aligned alias: `final_submission/05_engineering_and_product_justification.md`

Supporting artifact
- `final_submission/working_ai_agent.md`
- Runtime service implementation: `src/phase8/service.py`

## Required Evidence Rules
1. Prompt comparison same test set with 2-3 variants
- `final_submission/prompt_comparison_table.md`
- `reports/phase3_prompt_comparison.md`
- `phase_artifacts/phase3/outputs/prompt_comparison_results.json`
- Test set: `data/phase3/prompt_eval_test_set.json`

2. Proof for retrieval, tools, memory, adaptation
- Retrieval: `reports/phase4_rag_comparison.md`, `phase_artifacts/phase4/outputs/rag_comparison_results.json`
- Tools: `reports/phase5_tool_usage_comparison.md`, `phase_artifacts/phase5/outputs/tool_run_results.json`
- Memory/planning: `reports/phase6_multiturn_comparison.md`, `phase_artifacts/phase6/outputs/multiturn_results.json`
- Adaptation: `reports/phase7_adaptation_comparison.md`, `phase_artifacts/phase7/outputs/adaptation_results.json`

3. At least one failure with root cause and before/after fix
- `reports/phase9_evaluation_report.md`
- `phase_artifacts/phase9/outputs/evaluation_metrics.json` (root_cause_analysis)

4. Safety enforcement demonstration
- Runtime evidence: `phase_artifacts/phase8/outputs/deployment_readiness_results.json`
- Runtime logs: `phase_artifacts/phase8/outputs/runtime_logs.jsonl`
- Safety checks summary: `phase_artifacts/phase9/outputs/evaluation_metrics.json`
- PII redaction proof: `reports/evidence/phase2_pii_redaction_proof.txt`

## Canonical Repository Locations
- Source code: `src/`
- Evaluation scripts: `scripts/`
- Reports and outputs: `reports/`, `logs/`, `phase_artifacts/`
