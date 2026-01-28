# rag/loadKB.py
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from rag.utils import read_text_file


def load_kb_documents(kb_dir: Path = Path("data") / "kb") -> List[Tuple[str, str]]:
    """
    Returns list of (doc_id, text).
    doc_id is based on relative path.
    """
    if not kb_dir.exists():
        return []

    docs = []
    for path in kb_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            text = read_text_file(path)
            doc_id = str(path.relative_to(kb_dir))
            docs.append((doc_id, text))
    return docs