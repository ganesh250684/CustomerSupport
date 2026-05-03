# Phase 8 Runtime Evaluation

| Case ID | Simulated Failure | Degraded Mode | Error Category | Escalation | Latency (ms) |
|---|---|---|---|---|---:|
| D8-01 | none | false |  | false | 0.01 |
| D8-02 | none | false |  | true | 0.02 |
| D8-03 | retrieval | true | retrieval_failure | false | 0.26 |
| D8-04 | llm | true | llm_failure | true | 0.24 |
| D8-05 | tool | true | tool_failure | true | 0.31 |
| D8-06 | none | false |  | true | 0.01 |

## Summary
- Total cases: 6
- Degraded cases: 3
- Error counts: {'retrieval_failure': 1, 'llm_failure': 1, 'tool_failure': 1}
- Latency min/avg/p95/max (ms): 0.01/0.14/0.26/0.31