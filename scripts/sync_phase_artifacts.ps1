$ErrorActionPreference = 'Stop'

function Copy-IfExists {
    param(
        [string]$Source,
        [string]$Destination
    )

    if (Test-Path $Source) {
        $destDir = Split-Path -Parent $Destination
        if (-not [string]::IsNullOrWhiteSpace($destDir)) {
            New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        }

        Copy-Item -Path $Source -Destination $Destination -Force
        Write-Host "Copied: $Source -> $Destination"
    }
    else {
        Write-Host "Skipped (missing): $Source"
    }
}

function Ensure-Dir {
    param([string]$Path)
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

# Canonical artifact root
$root = "phase_artifacts"

# Ensure phase folders exist
Ensure-Dir "$root/phase1/documentation"
Ensure-Dir "$root/phase1/outputs"
Ensure-Dir "$root/phase2/documentation"
Ensure-Dir "$root/phase2/outputs"
Ensure-Dir "$root/phase3/documentation"
Ensure-Dir "$root/phase3/outputs"
Ensure-Dir "$root/phase4/documentation"
Ensure-Dir "$root/phase4/outputs"
Ensure-Dir "$root/phase5/documentation"
Ensure-Dir "$root/phase5/outputs"
Ensure-Dir "$root/phase6/documentation"
Ensure-Dir "$root/phase6/outputs"
Ensure-Dir "$root/phase7/documentation"
Ensure-Dir "$root/phase7/outputs"
Ensure-Dir "$root/phase8/documentation"
Ensure-Dir "$root/phase8/outputs"
Ensure-Dir "$root/phase9/documentation"
Ensure-Dir "$root/phase9/outputs"

# Phase 1 docs
Copy-IfExists "docs/phase1_problem_framing.md" "$root/phase1/documentation/phase1_problem_framing.md"
Copy-IfExists "docs/phase1_evidence_checklist.md" "$root/phase1/documentation/phase1_evidence_checklist.md"
Copy-IfExists "docs/original_project_plan.md" "$root/phase1/documentation/original_project_plan.md"

# Phase 2 docs
Copy-IfExists "reports/phase2_implementation.md" "$root/phase2/documentation/phase2_implementation.md"
Copy-IfExists "reports/phase2_evidence_list.md" "$root/phase2/documentation/phase2_evidence_list.md"
Copy-IfExists "reports/phase2_manual_verification_steps.md" "$root/phase2/documentation/phase2_manual_verification_steps.md"

# Phase 2 outputs
Copy-IfExists "logs/phase2_forced_demo_outputs.json" "$root/phase2/outputs/phase2_forced_demo_outputs.json"
Copy-IfExists "logs/phase2_forced_demo.jsonl" "$root/phase2/outputs/phase2_forced_demo.jsonl"
Copy-IfExists "logs/phase2_interactions.jsonl" "$root/phase2/outputs/phase2_interactions.jsonl"
Copy-IfExists "logs/phase2_api_interactions.jsonl" "$root/phase2/outputs/phase2_api_interactions.jsonl"
Copy-IfExists "reports/evidence/phase2_api_health.json" "$root/phase2/outputs/phase2_api_health.json"
Copy-IfExists "reports/evidence/phase2_api_log_excerpt.txt" "$root/phase2/outputs/phase2_api_log_excerpt.txt"
Copy-IfExists "reports/evidence/phase2_api_normal.json" "$root/phase2/outputs/phase2_api_normal.json"
Copy-IfExists "reports/evidence/phase2_api_refusal.json" "$root/phase2/outputs/phase2_api_refusal.json"
Copy-IfExists "reports/evidence/phase2_pii_redaction_proof.txt" "$root/phase2/outputs/phase2_pii_redaction_proof.txt"

# Phase 3 docs
Copy-IfExists "reports/phase3_implementation.md" "$root/phase3/documentation/phase3_implementation.md"
Copy-IfExists "reports/phase3_evidence_list.md" "$root/phase3/documentation/phase3_evidence_list.md"
Copy-IfExists "reports/phase3_manual_verification_steps.md" "$root/phase3/documentation/phase3_manual_verification_steps.md"
Copy-IfExists "reports/phase3_prompt_comparison.md" "$root/phase3/documentation/phase3_prompt_comparison.md"

# Phase 3 outputs
Copy-IfExists "outputs/phase3/prompt_comparison_results.json" "$root/phase3/outputs/prompt_comparison_results.json"

# Phase 4 docs
Copy-IfExists "reports/phase4_implementation.md" "$root/phase4/documentation/phase4_implementation.md"
Copy-IfExists "reports/phase4_evidence_list.md" "$root/phase4/documentation/phase4_evidence_list.md"
Copy-IfExists "reports/phase4_manual_verification_steps.md" "$root/phase4/documentation/phase4_manual_verification_steps.md"
Copy-IfExists "reports/phase4_rag_comparison.md" "$root/phase4/documentation/phase4_rag_comparison.md"

# Phase 4 outputs
Copy-IfExists "outputs/phase4/vector_index.json" "$root/phase4/outputs/vector_index.json"
Copy-IfExists "outputs/phase4/rag_comparison_results.json" "$root/phase4/outputs/rag_comparison_results.json"

# Phase 5 docs
Copy-IfExists "reports/phase5_implementation.md" "$root/phase5/documentation/phase5_implementation.md"
Copy-IfExists "reports/phase5_evidence_list.md" "$root/phase5/documentation/phase5_evidence_list.md"
Copy-IfExists "reports/phase5_manual_verification_steps.md" "$root/phase5/documentation/phase5_manual_verification_steps.md"
Copy-IfExists "reports/phase5_tool_usage_comparison.md" "$root/phase5/documentation/phase5_tool_usage_comparison.md"

# Phase 5 outputs
Copy-IfExists "outputs/phase5/tool_run_results.json" "$root/phase5/outputs/tool_run_results.json"
Copy-IfExists "outputs/phase5/tool_audit_log.jsonl" "$root/phase5/outputs/tool_audit_log.jsonl"

# Phase 6 docs
Copy-IfExists "reports/phase6_implementation.md" "$root/phase6/documentation/phase6_implementation.md"
Copy-IfExists "reports/phase6_evidence_list.md" "$root/phase6/documentation/phase6_evidence_list.md"
Copy-IfExists "reports/phase6_manual_verification_steps.md" "$root/phase6/documentation/phase6_manual_verification_steps.md"
Copy-IfExists "reports/phase6_multiturn_comparison.md" "$root/phase6/documentation/phase6_multiturn_comparison.md"

# Phase 6 outputs
Copy-IfExists "outputs/phase6/multiturn_results.json" "$root/phase6/outputs/multiturn_results.json"
Copy-IfExists "outputs/phase6/memory_state_snapshot.json" "$root/phase6/outputs/memory_state_snapshot.json"

# Phase 7 docs
Copy-IfExists "reports/phase7_implementation.md" "$root/phase7/documentation/phase7_implementation.md"
Copy-IfExists "reports/phase7_evidence_list.md" "$root/phase7/documentation/phase7_evidence_list.md"
Copy-IfExists "reports/phase7_manual_verification_steps.md" "$root/phase7/documentation/phase7_manual_verification_steps.md"
Copy-IfExists "reports/phase7_adaptation_comparison.md" "$root/phase7/documentation/phase7_adaptation_comparison.md"

# Phase 7 outputs
Copy-IfExists "outputs/phase7/adaptation_results.json" "$root/phase7/outputs/adaptation_results.json"
Copy-IfExists "outputs/phase7/feedback_log.jsonl" "$root/phase7/outputs/feedback_log.jsonl"

# Phase 8 docs
Copy-IfExists "reports/phase8_implementation.md" "$root/phase8/documentation/phase8_implementation.md"
Copy-IfExists "reports/phase8_evidence_list.md" "$root/phase8/documentation/phase8_evidence_list.md"
Copy-IfExists "reports/phase8_manual_verification_steps.md" "$root/phase8/documentation/phase8_manual_verification_steps.md"
Copy-IfExists "reports/phase8_runtime_comparison.md" "$root/phase8/documentation/phase8_runtime_comparison.md"

# Phase 8 outputs
Copy-IfExists "outputs/phase8/deployment_readiness_results.json" "$root/phase8/outputs/deployment_readiness_results.json"
Copy-IfExists "outputs/phase8/latency_error_summary.json" "$root/phase8/outputs/latency_error_summary.json"
Copy-IfExists "outputs/phase8/runtime_logs.jsonl" "$root/phase8/outputs/runtime_logs.jsonl"

# Phase 9 docs
Copy-IfExists "reports/phase9_implementation.md" "$root/phase9/documentation/phase9_implementation.md"
Copy-IfExists "reports/phase9_evidence_list.md" "$root/phase9/documentation/phase9_evidence_list.md"
Copy-IfExists "reports/phase9_manual_verification_steps.md" "$root/phase9/documentation/phase9_manual_verification_steps.md"
Copy-IfExists "reports/phase9_evaluation_report.md" "$root/phase9/documentation/phase9_evaluation_report.md"
Copy-IfExists "reports/phase9_engineering_review.md" "$root/phase9/documentation/phase9_engineering_review.md"

# Phase 9 outputs
Copy-IfExists "outputs/phase9/evaluation_metrics.json" "$root/phase9/outputs/evaluation_metrics.json"

Write-Host "Artifact sync complete."
