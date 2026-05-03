from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_kb_documents(kb_dir: Path) -> List[Document]:
    """Load raw KB files (procedure + FAQ) into LangChain Document objects."""
    if not kb_dir.exists():
        return []

    docs: List[Document] = []
    for file_path in sorted(kb_dir.rglob("*")):
        if not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        if not content:
            continue

        doc_type = "procedure" if "procedure" in file_path.name.lower() else "faq"
        docs.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(file_path).replace('\\\\', '/'),
                    "doc_type": doc_type,
                    "filename": file_path.name,
                },
            )
        )

    return docs
