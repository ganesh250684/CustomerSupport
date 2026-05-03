# Phase 4 Evidence List

## Required Evidence Mapping

1. Document ingestion proof
- Input docs folder: `data/kb/raw`
- Indexing script: `scripts/run_phase4_indexing.py`
- Evidence: terminal output showing document count and index path

2. Embeddings + vector store proof
- Implementation: `src/phase4/indexer.py`
- Vector store output file: `outputs/phase4/vector_index.json`
- Evidence: file exists and query retrieval works
- Technical check: index file contains `embedding_model`, `entry_count`, and chunk entries

3. Semantic retrieval proof
- Retrieval implementation: `src/phase4/retriever.py`
- Evidence: non-zero retrieved_count for matching scenarios in comparison results
- Technical check: cosine similarity with threshold `0.45` and top-k `4`

4. Response comparison proof (with vs without retrieval)
- Runner: `scripts/run_phase4_rag_eval.py`
- JSON output: `outputs/phase4/rag_comparison_results.json`
- Table output: `reports/phase4_rag_comparison.md`

5. Missing information handling proof
- Scenario: `R4-04` in `data/phase4/rag_eval_test_set.json`
- Expected: explicit uncertainty + escalation when retrieval is missing
- Evidence: row entry in JSON/table showing safe fallback behavior

6. Retrieval-quality snapshot proof
- Source: `outputs/phase4/rag_comparison_results.json`
- Capture these metrics in submission text:
	- total cases
	- retrieved cases count
	- missing-retrieval cases count
	- with-citation cases count
	- missing-info escalation correctness

## Manual Commands
1. `python scripts/run_phase4_indexing.py`
2. `python scripts/run_phase4_rag_eval.py`

## Submission Attachments
- `reports/phase4_implementation.md`
- `reports/phase4_evidence_list.md`
- `reports/phase4_rag_comparison.md`
- `outputs/phase4/rag_comparison_results.json`
- `outputs/phase4/vector_index.json`
- Terminal transcript excerpts for indexing and evaluation runs
