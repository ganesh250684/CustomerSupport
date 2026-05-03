# Phase 4 Manual Verification Steps

Run from project root in PowerShell.

## 1. Ensure API key is available in this terminal
1. $env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
2. if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) { 'missing' } else { 'set' }

## 2. Ensure dependencies are installed
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe -m pip install -r requirements-phase4.txt

## 3. Add your real KB files
Put your procedure and FAQ files in:
- data/kb/raw

Supported formats:
- .md
- .txt

## 4. Build embeddings + vector index
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe scripts/run_phase4_indexing.py

Expected output:
- Indexed <N> source documents.
- Index file: outputs/phase4/vector_index.json
- Indexed chunks: <M>

## 5. Run with-vs-without retrieval evaluation
1. d:/IITM/CustomerSupport/.venv/Scripts/python.exe scripts/run_phase4_rag_eval.py

Expected output:
- Generated Phase 4 comparison rows: 4
- Results: outputs/phase4/rag_comparison_results.json
- Table: reports/phase4_rag_comparison.md

## 6. Verify missing-information behavior
Check case R4-04 in:
- outputs/phase4/rag_comparison_results.json

Expected:
- with_retrieval.escalate = true when no relevant evidence is retrieved
- uncertainty note present
- no fabricated policy claim

## 7. Evidence files for submission
- reports/phase4_implementation.md
- reports/phase4_evidence_list.md
- reports/phase4_manual_verification_steps.md
- outputs/phase4/vector_index.json
- outputs/phase4/rag_comparison_results.json
- reports/phase4_rag_comparison.md
