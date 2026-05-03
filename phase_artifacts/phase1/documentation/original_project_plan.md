# Original Project Plan

## Project
Customer Support AI Support Resolution Agent (SaaS Support), built with LangChain.

## Purpose
Deliver a safety-first, explainable, reliable agent that supports realistic support workflows and produces auditable evidence across all phases.

## Locked Decisions
- Industry scenario: SaaS Product Support
- Framework: LangChain
- LLM provider target: OpenAI via langchain-openai
- Deployment readiness target: Local FastAPI service with curl-based demo evidence
- Safety requirements:
  - Refuse unsafe or policy-violating requests
  - Never fabricate policies
  - Escalate sensitive or unresolved cases
  - Do not store personal data in logs

## End-to-End Phase Plan

### Phase 1: Understand the Problem and Define Success
Objective:
Define the business workflow, user persona, measurable success, and risk boundaries before implementation.

Outputs:
- Persona and workflow map (as-is and to-be)
- Problem statement
- Inputs, outputs, constraints, assumptions
- 3-5 example user questions
- Success criteria with metrics and thresholds
- Failure/edge case list with expected handling
- Evaluation foundation for later phases

### Phase 2: Build a Basic Working Agent
Objective:
Create a minimal Python baseline agent to establish initial behavior and expose limitations.

Outputs:
- Python agent that accepts user input and returns template/rule responses
- Sample interaction logs
- Evidence of at least 2 baseline limitations
- Short analysis of why baseline is insufficient for real users

### Phase 3: Make the Agent Smarter
Objective:
Integrate an LLM and compare prompt strategies on the same test set.

Outputs:
- LLM integration using LangChain
- 2-3 prompt variants tested on same scenarios
- Comparison table: Prompt -> Output -> Improved/Worsened
- Failure analysis of new LLM-specific issues
- Default prompt strategy selection with justification

### Phase 4: Add Knowledge and Retrieval
Objective:
Ground answers in evidence from provided KB documents.

Outputs:
- Ingestion of provided procedure and FAQ documents
- Embeddings and vector retrieval pipeline
- RAG-enhanced response generation with citations
- With-vs-without retrieval comparison
- Missing-info handling (uncertainty + escalation, no fabrication)

### Phase 5: Enable Tool Usage
Objective:
Allow controlled tool calling for operational actions.

Outputs:
- At least two tools (for example: ticket lookup and escalation creation)
- Tool selection and calling logic
- Demonstration of correct and incorrect tool usage
- Safeguards for misuse, retries, and loop prevention

### Phase 6: Planning, Memory, and Context
Objective:
Improve multi-turn reasoning and conversation quality.

Outputs:
- Multi-step planning flow
- Session memory with retention/reset rules
- Multi-turn behavior improvements demonstrated
- Privacy-preserving memory handling

### Phase 7: Adaptive Behavior
Objective:
Use feedback signals to adjust future behavior.

Outputs:
- Feedback capture mechanism
- Adaptation logic tied to feedback
- Before-vs-after behavior evidence
- Explanation of what changed and why

### Phase 8: Deployment Readiness
Objective:
Package for reproducible local deployment and observability.

Outputs:
- FastAPI deployment package
- Environment and run instructions
- Latency and error tracing/logging
- Graceful failure handling for dependency outages
- Assumptions and deployment limitations documented

### Phase 9: Evaluation and Engineering Review
Objective:
Measure quality/safety/reliability and propose next improvements.

Outputs:
- Evaluation harness and test scenarios
- Quality, consistency, and safety metrics report
- Root cause analysis for at least one failure with fix evidence
- Improvement roadmap

## Required Final Submission Package
- Working AI agent
- Problem Framing Document (1-2 pages)
- Demo Script (3-5 forced interactions)
- Evaluation Report
- Engineering and Product Justification

## Required Evidence Rules
- Prompt comparison must use the same test set and 2-3 prompt variants
- Must provide concrete proof for retrieval, tool usage, memory, and adaptation
- Must include at least one failure case with root cause and before/after fix
- Must demonstrate safety enforcement behavior

## Verification Gates
- Each phase must produce its planned artifact(s)
- Safety checks must pass:
  - Refusal correctness
  - Anti-fabrication behavior
  - Escalation correctness
  - PII-safe logging
- Demo script must run reproducibly with saved logs and timestamps
