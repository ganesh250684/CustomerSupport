# Phase 2 Implementation Report

## Scope Completed
Phase 2 baseline was implemented as a deterministic, rule/template-based support agent without LLM usage.

## What Was Built
- Baseline agent logic for intent handling and safe default behavior
- CLI interface for manual interaction runs
- FastAPI interface for programmatic interaction runs
- PII-safe JSONL logging
- Forced interaction demo script for reproducible sample runs

## Components
- Baseline agent: `src/agent/baseline_agent.py`
- CLI entrypoint: `src/cli.py`
- API entrypoint: `src/app.py`
- Safe logger: `src/observability/logger.py`
- PII redaction: `src/utils/redaction.py`
- Forced demo script: `scripts/run_phase2_demo.py`

## Baseline Behavior Summary
1. Unsafe or policy-bypass requests are refused and escalated.
2. Security-sensitive cases are escalated.
3. Billing and plan/feature questions receive template-guided responses.
4. Unknown intents return low-confidence fallback with escalation recommendation.

## Demonstrated Baseline Limitations (Required)
1. Limited semantic understanding:
- The baseline depends on keyword matching and misses nuanced phrasing.
- Impact: can underperform on paraphrased or complex multi-intent tickets.

2. Placeholder citations and no true grounding:
- Citations are static placeholders in Phase 2.
- Impact: policy references are not evidence-grounded yet; this will be fixed in Phase 4 with retrieval.

3. No adaptive reasoning:
- The baseline cannot refine behavior based on context depth or prior feedback.
- Impact: inconsistent usefulness for complex multi-turn support scenarios.

## Why This Version Is Insufficient for Real Users
- It is brittle to language variation and context shifts.
- It cannot provide trustworthy knowledge-grounded citations yet.
- It cannot perform nuanced decision-making across complex workflows.
- It needs LLM reasoning, retrieval grounding, tool support, and memory/adaptation from later phases.

## How This Supports Later Phases
- Phase 3: Replace rule-only output with LLM and compare prompt variants.
- Phase 4: Replace placeholder citations with KB-grounded retrieval from procedure and FAQ docs.
- Phase 5+: Add tools, memory, adaptation, and stronger reliability checks.
