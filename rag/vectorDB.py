# rag/vectorDB.py
from __future__ import annotations

from pathlib import Path

import chromadb

from rag.embeddings import get_embedding_function

DEFAULT_DB_DIR = Path("outputs") / "chroma_db"

KB_COLLECTION = "kb_store"
TICKETS_COLLECTION = "tickets_store"


def get_client(persist_dir: Path = DEFAULT_DB_DIR):
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_dir))


def get_collection(name: str, persist_dir: Path = DEFAULT_DB_DIR):
    client = get_client(persist_dir)
    embed_fn = get_embedding_function()
    return client.get_or_create_collection(name=name, embedding_function=embed_fn)