# Phase 5 Implementation Report

## Goal
Enable controlled tool usage with safe routing, failure handling, and loop/misuse safeguards.

## Scope Clarification
Phase 5 focuses on tool usage orchestration:
1. Define at least two tools.
2. Implement tool selection and invocation logic.
3. Demonstrate correct vs incorrect tool usage.
4. Add safeguards against misuse and loops.

## Technical Implementation Details

### Tool Definitions
- Tool 1: `lookup_ticket_status(ticket_id)`
  - Purpose: fetch ticket status and queue metadata.
  - Success requires ticket id format `TCK-<digits>` and existing ticket in mock store.
- Tool 2: `create_escalation_ticket(reason, severity, summary)`
  - Purpose: create escalation record for sensitive/unresolved cases.
  - Success requires valid severity and required fields.
- Implemented in: `src/phase5/tools.py`

### Tool Routing and Selection
- Router: `src/phase5/router.py`
- Routing policy (deterministic baseline):
  - Ticket/status intent -> `lookup_ticket_status`
  - Sensitive/security/legal/abuse intent -> `create_escalation_ticket`
  - Dangerous command intent -> intentionally maps to disallowed action for safeguard verification
  - Informational requests -> no tool

### Safeguards
- Guard module: `src/phase5/safeguards.py`
- Enforced controls:
  - Tool allowlist (`lookup_ticket_status`, `create_escalation_ticket`)
  - Max tool calls per turn (`2`)
  - Duplicate tool-call suppression (name+args fingerprint)
- Block outcome: return safe response and escalate to human support.

### Tool Agent Orchestration
- Agent: `src/phase5/tool_agent.py`
- Turn flow:
  1. Select tool
  2. Run safeguards
  3. Execute tool
  4. Convert result to customer-safe final response
  5. Mark escalation reason when needed

### Evaluation Harness
- Test set: `data/phase5/tool_eval_test_set.json`
- Runner: `scripts/run_phase5_tool_eval.py`
- Generated outputs:
  - `outputs/phase5/tool_run_results.json`
  - `outputs/phase5/tool_audit_log.jsonl`
  - `reports/phase5_tool_usage_comparison.md`

## Requirement-to-Task Verification

1. Define at least two tools
- Status: Complete
- Evidence: `src/phase5/tools.py`

2. Implement tool calling logic
- Status: Complete
- Evidence: `src/phase5/router.py`, `src/phase5/tool_agent.py`

3. Demonstrate correct tool selection
- Status: Complete
- Evidence:
  - `T5-01` ticket lookup call
  - `T5-02` escalation creation call

4. Show at least one failed or incorrect tool call
- Status: Complete
- Evidence:
  - `T5-03` invalid ticket lookup args -> safe failure
  - `T5-04` disallowed tool request -> blocked by allowlist safeguard

5. Add safeguards against misuse or loops
- Status: Complete
- Evidence:
  - allowlist, max-call guard, duplicate-call guard in `src/phase5/safeguards.py`

## Tool-Usage Quality Snapshot (Current Run)
- Total evaluation cases: 5
- Cases with tool selected: 4
- Successful tool calls: 2
- Failed tool call (invalid args): 1
- Blocked disallowed tool calls: 1
- No-tool-needed cases: 1

## Expected New Failure Modes
- Router false positives on ambiguous intent text.
- Under-triggering escalation when severity terms are implicit.
- Safe blocks increasing escalations for malformed requests.

These are measured in evaluation outputs and will be tuned in later phases.
