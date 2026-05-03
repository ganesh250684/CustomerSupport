# Evidence Index (Rubric Mapping)

## Required Final Submission Package
1. Working AI agent
- `final_submission/working_ai_agent.md`
- Runtime service: `src/phase8/service.py`

2. Problem framing document
- `final_submission/problem_framing_document.md`
- Source detail: `docs/phase1_problem_framing.md`

3. Demo script (3-5 forced interactions)
- `final_submission/demo_script.md`

4. Evaluation report
- `final_submission/evaluation_report.md`
- Detailed source: `reports/phase9_evaluation_report.md`

5. Engineering and product justification
- `final_submission/engineering_product_justification.md`

## Required Evidence Rules
1. Prompt comparison same test set with 2-3 variants
- `reports/phase3_prompt_comparison.md`
- `outputs/phase3/prompt_comparison_results.json`

2. Proof for retrieval, tools, memory, adaptation
- Retrieval: `reports/phase4_rag_comparison.md`, `outputs/phase4/rag_comparison_results.json`
- Tools: `reports/phase5_tool_usage_comparison.md`, `outputs/phase5/tool_run_results.json`
- Memory/planning: `reports/phase6_multiturn_comparison.md`, `outputs/phase6/multiturn_results.json`
- Adaptation: `reports/phase7_adaptation_comparison.md`, `outputs/phase7/adaptation_results.json`

3. At least one failure with root cause and before/after fix
- `reports/phase9_evaluation_report.md`
- `outputs/phase9/evaluation_metrics.json` (root_cause_analysis)

4. Safety enforcement demonstration
- Runtime evidence: `outputs/phase8/deployment_readiness_results.json`
- Safety checks summary: `outputs/phase9/evaluation_metrics.json`

## Centralized Evidence Mirror
All phase evidence is synchronized under:
- `phase_artifacts/`
