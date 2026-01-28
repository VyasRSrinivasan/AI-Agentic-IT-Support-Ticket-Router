# rag/indexKB.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

from rag.chunking import chunk_text
from rag.loadKB import load_kb_documents
from rag.utils import clean_text, stable_hash, safe_metadata
from rag.vectorDB import get_collection, KB_COLLECTION


def build_kb_index(kb_dir: Path = Path("data") / "kb", collection_name: str = "kb_store") -> int:
    col = get_collection(collection_name)

    docs = load_kb_documents(kb_dir)
    if not docs:
        print(f"[indexKB] No KB docs found in {kb_dir}. Create data/kb/*.md to use RAG.")
        return 0

    ids = []
    texts = []
    metas = []

    for doc_path_id, raw_text in docs:
        raw_text = clean_text(raw_text)
        chunks = chunk_text(raw_text, chunk_size=800, overlap=120)
        for i, ch in enumerate(chunks):
            chunk_id = f"kb::{doc_path_id}::{i}::{stable_hash(ch)}"
            ids.append(chunk_id)
            texts.append(ch)
            metas.append(safe_metadata(source_type="kb", title=doc_path_id, source=f"{kb_dir}/{doc_path_id}", chunk_index=i))

    # Upsert into Chroma
    col.upsert(ids=ids, documents=texts, metadatas=metas)
    print(f"[indexKB] Indexed {len(texts)} chunks into collection '{collection_name}'.")
    return len(texts)