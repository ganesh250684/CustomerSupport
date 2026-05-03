from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase4.indexer import build_vector_index
from src.phase4.kb_loader import load_kb_documents


def main() -> None:
    kb_dir = Path("data/kb/raw")
    index_file = Path("outputs/phase4/vector_index.json")

    docs = load_kb_documents(kb_dir)
    if not docs:
        raise RuntimeError(
            "No KB docs found in data/kb/raw. Add your procedure/FAQ documents first."
        )

    index_payload = build_vector_index(docs, index_file)
    print(f"Indexed {len(docs)} source documents.")
    print(f"Index file: {index_file}")
    print(f"Indexed chunks: {index_payload.get('entry_count', 0)}")


if __name__ == "__main__":
    main()
