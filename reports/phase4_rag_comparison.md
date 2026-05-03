# Phase 4 Retrieval Comparison

Comparison of responses with and without retrieval over the same test set.

| Case ID | Category | Retrieved Chunks | Without Retrieval (summary) | With Retrieval (summary) | Improvement |
|---|---|---:|---|---|---|
| R4-01 | billing | 1 | Please check your cancellation confirmation and billing details. If you believe the charge is incorrect, I recommend reaching out to our billing support team for assistan | To address the charge after cancellation, first, collect your invoice ID and the cancellation date. Refund eligibility depends on the timing of your cancellation and your | Grounded response |
| R4-02 | security_sensitive | 1 | I recommend you contact our support team directly for assistance with unlocking your account and addressing the suspicious logins. They will be able to help you further. | To recover your account, we will need to verify your identity first. Please provide the necessary information for verification. If there are indicators of suspicious acce | Grounded response |
| R4-03 | policy_bypass | 1 | I'm sorry, but I cannot assist with skipping verification or unlocking accounts. Please follow the standard procedures or contact support for further assistance. | I'm unable to skip verification or unlock your account without completing the identity verification process. This is a strict policy to ensure account security. If you ha | Grounded response |
| R4-04 | missing_info_case | 0 | I'm uncertain about the specific policy for one-time loyalty credit exceptions for failed webinars. I recommend escalating this inquiry to the appropriate support team fo | I do not have enough verified policy evidence in the knowledge base to provide a final answer. I will escalate this case to a specialist. | Correct missing-evidence escalation |

## Missing Information Handling
When retrieval returns no relevant chunks, the agent must:
1. Avoid policy fabrication.
2. State uncertainty explicitly.
3. Escalate the case.