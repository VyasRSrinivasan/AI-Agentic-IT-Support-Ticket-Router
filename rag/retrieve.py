# rag/retrieve.py
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

from schemas import Ticket, EvidenceChunk, EvidenceBundle


KB_DIR = Path("data") / "KB"


def _tokenize(text: str) -> List[str]:
    # simple tokenizer: lowercase words, length >= 3
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [w for w in words if len(w) >= 3]


def _load_kb_files() -> List[Tuple[str, str]]:
    docs: List[Tuple[str, str]] = []
    if not KB_DIR.exists():
        return docs

    for p in KB_DIR.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt"}:
            try:
                text = p.read_text(encoding="utf-8-sig", errors="ignore")
            except Exception:
                continue
            docs.append((str(p), text))
    return docs


def _score(query_tokens: List[str], doc_text: str) -> int:
    doc_lower = doc_text.lower()
    return sum(1 for t in query_tokens if t in doc_lower)


def retrieve(ticket: Ticket, k: int = 5) -> EvidenceBundle:
    """
    Retrieval baseline (no vector DB):
    - Loads KB docs from data/kb/
    - Scores by keyword overlap
    - Returns top-k EvidenceChunks with citations
    """
    query = ticket.text_for_llm()
    q_tokens = _tokenize(query)

    kb_chunks: List[EvidenceChunk] = []
    docs = _load_kb_files()

    scored = []
    for path, text in docs:
        s = _score(q_tokens, text)
        if s > 0:
            scored.append((s, path, text))

    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:k]

    for idx, (s, path, text) in enumerate(top):
        snippet = text.strip().split("\n")
        snippet_text = "\n".join(snippet[:10])[:800]  # first ~10 lines
        kb_chunks.append(
            EvidenceChunk(
                doc_id=f"kb::{Path(path).name}::{idx}",
                title=Path(path).name,
                source=path,
                snippet=snippet_text,
                score=min(1.0, s / max(1, len(q_tokens))) if q_tokens else None,
                source_type="kb",
                metadata={"retrieval": "keyword_overlap"},
            )
        )

    # no past-ticket retrieval in baseline; keep empty
    return EvidenceBundle(kb=kb_chunks, past_tickets=[])