from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


def retrieve_relevant_docs(
    index_payload: Dict[str, Any],
    query: str,
    k: int = 4,
    min_similarity: float = 0.45,
) -> List[Tuple[Document, float]]:
    """Retrieve semantically similar docs using cosine similarity."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    query_vec = embeddings.embed_query(query)

    scored: List[Tuple[Document, float]] = []
    for entry in index_payload.get("entries", []):
        doc_vec = entry.get("vector", [])
        sim = _cosine_similarity(query_vec, doc_vec)
        if sim >= min_similarity:
            doc = Document(page_content=entry.get("text", ""), metadata=entry.get("metadata", {}))
            scored.append((doc, sim))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:k]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return -1.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return -1.0
    return dot / (norm_a * norm_b)
