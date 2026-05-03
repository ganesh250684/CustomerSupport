from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def build_vector_index(documents: List[Document], index_file: Path) -> Dict[str, Any]:
    """Create and persist a lightweight JSON vector index from KB documents."""
    if not documents:
        raise ValueError("No KB documents found to index.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])

    entries: List[Dict[str, Any]] = []
    for chunk, vector in zip(chunks, vectors):
        entries.append(
            {
                "text": chunk.page_content,
                "metadata": chunk.metadata,
                "vector": vector,
            }
        )

    index_payload: Dict[str, Any] = {
        "embedding_model": "text-embedding-3-small",
        "entry_count": len(entries),
        "entries": entries,
    }

    index_file.parent.mkdir(parents=True, exist_ok=True)
    index_file.write_text(json.dumps(index_payload, ensure_ascii=True), encoding="utf-8")
    return index_payload


def load_vector_index(index_file: Path) -> Dict[str, Any]:
    """Load existing JSON vector index from disk."""
    if not index_file.exists():
        raise FileNotFoundError(f"Vector index file not found: {index_file}")
    return json.loads(index_file.read_text(encoding="utf-8"))
