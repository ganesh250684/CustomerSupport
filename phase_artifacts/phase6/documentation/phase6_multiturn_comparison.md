# Phase 6 Multi-Turn Comparison

Comparison of behavior without vs with session memory and planning.

| Conversation | Turn | Without Memory (summary) | With Memory (summary) | Improvement |
|---|---:|---|---|---|
| M6-01 | 1 | Please share invoice id and cancellation date. I will use this session context to avoid repeating questions. Context considered: Memory disabled for this run. | Please share invoice id and cancellation date. I will use this session context to avoid repeating questions. Context considered: No prior session context. | No major change |
| M6-01 | 2 | Please provide more details so I can assist accurately. Context considered: Memory disabled for this run. | Please provide more details so I can assist accurately. Context considered: Turn 1: user='I was charged after cancellation and want a refund.' | Better context continuity |
| M6-01 | 3 | Please provide more details so I can assist accurately. Context considered: Memory disabled for this run. | Please provide more details so I can assist accurately. Context considered: Turn 1: user='I was charged after cancellation and want a refund.' \| Turn 2: user='Invoice is | Better context continuity |
| M6-02 | 1 | This appears sensitive. I recommend immediate escalation to specialized support. Context considered: Memory disabled for this run. | This appears sensitive. I recommend immediate escalation to specialized support. Context considered: No prior session context. | No major change |
| M6-02 | 2 | Please provide more details so I can assist accurately. Context considered: Memory disabled for this run. | Please provide more details so I can assist accurately. Context considered: Turn 1: user='There were suspicious logins and I am locked out.' | Better context continuity |
| M6-02 | 3 | I cannot assist with bypassing verification or policy controls. I can guide you through compliant recovery steps instead. | I cannot assist with bypassing verification or policy controls. I can guide you through compliant recovery steps instead. | No major change |
| M6-03 | 1 | Please provide more details so I can assist accurately. Context considered: Memory disabled for this run. | Please provide more details so I can assist accurately. Context considered: No prior session context. | No major change |
| M6-03 | 2 | Session context reset completed. | Session context reset completed. | No major change |
| M6-03 | 3 | Please provide more details so I can assist accurately. Context considered: Memory disabled for this run. | Please provide more details so I can assist accurately. Context considered: No prior session context. | No major change |

## Quality Snapshot
- Total turns (without memory): 9
- Total turns (with memory): 9
- Context mentions (without memory): 7
- Context mentions (with memory): 7
- Context-rich turns (without memory): 0
- Context-rich turns (with memory): 3
- Memory resets detected: 1