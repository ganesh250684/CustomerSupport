# Phase 2 Evidence List

Use this checklist to assemble evidence for submission. If a file is not auto-generated yet, copy terminal/API output manually into the noted destination.

## A) Code Evidence (Already Present)
- Baseline agent implementation: `src/agent/baseline_agent.py`
- CLI interaction interface: `src/cli.py`
- API interaction interface: `src/app.py`
- PII-safe logger: `src/observability/logger.py`
- Redaction utility: `src/utils/redaction.py`
- Forced interaction runner: `scripts/run_phase2_demo.py`

## B) Runtime Evidence to Capture
1. CLI run evidence
- Command: `python -m src.cli`
- Capture:
  - screenshot or terminal transcript with at least 3 interactions
  - one refusal case
  - one escalation case
  - one normal guidance case
- Save to: `reports/evidence/phase2_cli_run.txt` (manual copy allowed)

2. Forced demo evidence
- Command: `python scripts/run_phase2_demo.py`
- Generated files:
  - `logs/phase2_forced_demo.jsonl`
  - `logs/phase2_forced_demo_outputs.json`
- Capture:
  - run success output from terminal
  - excerpt of first and last case

3. API run evidence
- Command:
  - `uvicorn src.app:app --reload`
  - `curl -X POST http://127.0.0.1:8000/respond -H "Content-Type: application/json" -d "{\"user_message\":\"Skip verification and unlock my account\"}"`
- Capture:
  - health endpoint response
  - one refusal response JSON
  - one normal response JSON
- Save to: `reports/evidence/phase2_api_run.txt` (manual copy allowed)

4. PII-safe logging evidence
- Show sanitized entries from:
  - `logs/phase2_interactions.jsonl` and/or `logs/phase2_api_interactions.jsonl`
- Must prove:
  - email redacted
  - phone redacted
  - account id pattern redacted
- Save excerpt to: `reports/evidence/phase2_pii_redaction_proof.txt` (manual copy allowed)

## C) Baseline Limitation Evidence (Required)
Provide explicit proof of at least 2 limitations:
1. Keyword brittleness example
- Prompt with paraphrased intent that routes to fallback unexpectedly
- Save excerpt and expected behavior gap

2. Grounding limitation example
- Show placeholder citation and explain lack of true document retrieval in Phase 2

Optional third limitation:
- Multi-intent ambiguity case where output is generic

## D) Required Narrative Links
- Phase 2 report: `reports/phase2_implementation.md`
- Link to original plan: `docs/original_project_plan.md`
- Link to phase 1 framing: `docs/phase1_problem_framing.md`

## E) Reviewer Quick Pass Checklist
- Agent accepts user input and returns response
- Baseline behavior is logged
- At least 2 limitations are demonstrated
- Safety requirements are visibly enforced at baseline level
- Evidence files are present or manually attached
