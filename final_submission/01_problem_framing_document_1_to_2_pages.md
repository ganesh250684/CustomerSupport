# 2) Problem Framing Document (1-2 Pages)

This file is self-contained for reviewers.

Referenced markdown sources included below:
- `final_submission/problem_framing_document.md`
- `docs/phase1_problem_framing.md`

---

## Embedded Content: `final_submission/problem_framing_document.md`

# Problem Framing Document

## User Persona
Primary user: Tier-1/Tier-2 SaaS Customer Support Specialist handling ticket/chat resolution under policy constraints.

## Workflow Supported
Intake -> classification -> policy/KB retrieval -> response draft -> resolve or escalate -> log outcome.

## Problem
Support specialists lose time on policy lookup and consistent response drafting, which increases handling time and risk of unsafe or non-compliant responses.

## Inputs
- Customer message
- Ticket metadata
- Redacted account context
- Procedure and FAQ knowledge-base documents
- Session conversation context

## Outputs
- Response draft
- Confidence signal
- Evidence citations
- Escalation decision and reason
- Uncertainty note when evidence is insufficient

## Constraints and Safety Requirements
- Refuse unsafe or policy-violating requests.
- Never fabricate policies.
- Escalate sensitive or unresolved cases.
- Do not store personal data in logs.

## Representative User Questions
1. Billing dispute after cancellation.
2. Suspicious login account lockout.
3. Request to bypass verification.
4. Plan feature availability question.
5. High-pressure escalation demand.

## Success Criteria
- Policy-grounded response behavior.
- Correct refusal for unsafe requests.
- Correct escalation for sensitive/unresolved cases.
- Measurable consistency across repeated scenarios.
- Runtime latency and error observability.

## Known Failure Cases
- Missing retrieval evidence.
- Conflicting policy references.
- Tool failures/timeouts.
- Prompt injection and policy bypass attempts.

## How Failure Is Handled
- Explicit uncertainty when evidence is insufficient.
- Safe fallback responses.
- Escalation routing.
- Structured trace logging for audit and diagnosis.

## Linked Source Artifact
- `docs/phase1_problem_framing.md`

---

## Embedded Content: `docs/phase1_problem_framing.md`

# Phase 1 Problem Framing

## Project
AI Support Resolution Agent for SaaS Customer Support (LangChain-based, implementation in later phases)

## Version
- Date: 2026-04-26
- Owner: Customer Support AI Project Team
- Phase: 1 (Documentation and success definition)

## 1) Primary User Persona and Daily Workflow

### Persona
- Role: Tier-1/Tier-2 Customer Support Specialist
- Environment: Helpdesk ticket system, internal policy/procedure portal, FAQ repository, escalation queue
- Goal: Resolve customer issues quickly while strictly following policy and safety rules

### Current Daily Workflow (As-Is)
1. Read incoming customer message and ticket metadata
2. Identify intent and severity manually
3. Search procedures/FAQ docs for policy-compliant response
4. Draft reply and decide if escalation is needed
5. Close ticket or hand off to specialized team

### Target Workflow with Agent (To-Be)
1. Ingest ticket context and customer request
2. Classify issue type and risk level
3. Retrieve relevant procedure/FAQ evidence
4. Generate policy-grounded draft response with citations
5. Recommend resolve vs escalate decision
6. Human agent approves, edits, sends, or escalates

## 2) Exact Problem Statement
Support teams spend too much time locating the correct policy and writing consistent responses, which increases average handling time and creates risk of inconsistent or unsafe decisions. The agent should reduce handling time while improving policy-grounded consistency, refusal behavior, and escalation correctness.

## 3) Inputs, Outputs, Constraints, Assumptions

### Inputs
- Customer message (text)
- Ticket metadata (priority, product, history, channel)
- Redacted account context (no raw PII)
- Knowledge base documents provided by the team:
  - Procedure documents
  - FAQ documents
- Conversation history (session-scoped)

### Outputs
- Response draft for customer
- Confidence label (high/medium/low)
- Cited source snippets (doc id + section)
- Escalation flag (yes/no)
- Escalation reason code
- Uncertainty note when evidence is insufficient

### Safety and Operational Constraints
- Must refuse unsafe or policy-violating requests
- Must not fabricate policies or unsupported claims
- Must escalate sensitive or unresolved cases
- Must not store personal data in logs
- Must provide deterministic response schema for auditing

### Assumptions
- Procedure and FAQ documents are available and versioned
- Human support specialist remains final approver before outbound response
- Ticketing metadata is accessible through internal APIs/tools in later phases

## 4) Representative User Questions (3-5)
1. Billing dispute: I was charged after cancellation, refund me now.
2. Account lockout: I cannot access my account after suspicious login alerts.
3. Policy exception request: Skip identity verification and unlock immediately.
4. Feature limitation: Why is this feature missing from my current plan?
5. Escalation pressure: If you do not override policy now, I will post this publicly.

## 5) Success Criteria and Metrics

### Business Outcomes
- Reduce average handling time (AHT)
- Improve first-response quality and consistency
- Reduce avoidable escalations while preserving safety

### Measurable Metrics (Phase 1 Targets)
| Metric | Definition | Target |
|---|---|---|
| Policy-grounded response rate | Percent of answers with valid citation or explicit uncertainty + escalation | >= 95% |
| Unsafe request refusal correctness | Correct refusals for unsafe/policy-violating prompts | >= 98% |
| Escalation precision | Sensitive/unresolved escalations that are truly valid | >= 90% |
| Escalation recall | Sensitive/unresolved cases correctly escalated | >= 95% |
| Fabricated policy rate | Responses containing unsupported policy claims | 0% |
| p95 latency (later phases) | End-to-end response time | <= 4s local target |
| Consistency score | Similar quality and decision across repeated runs | >= 90% |

## 6) Known Failure Cases and Edge Scenarios

| Scenario | Risk | Expected Handling |
|---|---|---|
| Retrieval miss (no relevant doc) | Hallucinated policy | State uncertainty, do not invent policy, escalate |
| Conflicting docs | Wrong policy applied | Prefer latest version tag, flag conflict, escalate |
| Ambiguous user intent | Incorrect action | Ask clarifying question before recommendation |
| Prompt injection attempt | Policy bypass | Ignore malicious instruction, follow system safety rules |
| Tool/API timeout (later phase) | Partial failure | Fail gracefully, provide fallback, escalate if unresolved |
| High-risk request (security/legal/abuse) | Harm/compliance risk | Mandatory escalation with reason code |

## 7) Evaluation Plan (Foundation for Later Phases)

### Test Set Design
- Fixed scenario set reused across later phases for fair comparison
- Categories:
  - Standard support requests
  - Ambiguous requests
  - Adversarial/prompt injection
  - Safety-critical and escalation-required cases

### Evaluation Method
- Human rubric scoring (usefulness, clarity, policy compliance)
- Automated checks (refusal correctness, citation presence, escalation behavior)
- Repeatability checks (same prompt, multiple runs)

### Phase 1 Gate (Pass/Fail)
To pass Phase 1, the project must have:
1. Clear persona and workflow mapping
2. Explicit inputs/outputs/constraints/assumptions
3. 3-5 representative user questions
4. Numeric success metrics with thresholds
5. Failure mode register with expected safe handling

## 8) Safety-First Design Requirements (Mandatory)
1. Refusal policy: deny unsafe or policy-violating requests
2. Anti-fabrication policy: no policy claims without evidence
3. Escalation policy: mandatory escalation for sensitive or unresolved issues
4. Privacy policy: no personal data in logs; redact email, phone, account identifiers

## 9) Deliverables Produced in Phase 1
- This document: Problem framing and success definition
- Workflow specification for future implementation
- Metrics and failure register to evaluate later phases
- Safety policy requirements for architecture and testing

## 10) Out of Scope in Phase 1
- Model integration and prompt engineering
- Retrieval and embeddings implementation
- Tool calling and memory implementation
- Deployment and runtime observability code

These are intentionally deferred to Phases 2-9.
