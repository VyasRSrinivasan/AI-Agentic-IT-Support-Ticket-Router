# rag/indexTickets.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

from data.load_raw_csv import load_tickets  # uses your existing loader
from rag.chunking import chunk_text
from rag.utils import clean_text, stable_hash, safe_metadata
from rag.vectorDB import get_collection


def build_ticket_resolution_index(
    csv_path: Path = Path("data") / "tickets" / "customer_support_tickets.csv",
    collection_name: str = "tickets_store",
    limit: Optional[int] = None,
) -> int:
    col = get_collection(collection_name)

    ids, texts, metas = [], [], []
    count = 0

    for t in load_tickets(csv_path=csv_path, limit=limit):
        # Only index if we have a resolution text in extras
        resolution = None
        if isinstance(t.extras, dict):
            resolution = t.extras.get("Resolution")

        if not resolution:
            continue

        # Create a compact “problem -> resolution” record
        record = f"Subject: {t.subject}\nIssue: {t.body}\nResolution: {resolution}"
        record = clean_text(record)

        chunks = chunk_text(record, chunk_size=900, overlap=100)
        for i, ch in enumerate(chunks):
            chunk_id = f"ticket::{t.ticket_id}::{i}::{stable_hash(ch)}"
            ids.append(chunk_id)
            texts.append(ch)
            metas.append(
                safe_metadata(
                    source_type="past_ticket",
                    source=f"{csv_path}",
                    ticket_id=t.ticket_id,
                    ticket_type=t.ticket_type,
                    ticket_priority=t.ticket_priority,
                    chunk_index=i,
                    title=f"ticket-{t.ticket_id}",
                )
            )

        count += 1

    if texts:
        col.upsert(ids=ids, documents=texts, metadatas=metas)
        print(f"[indexTickets] Indexed {len(texts)} chunks from {count} resolved tickets into '{collection_name}'.")
    else:
        print("[indexTickets] No resolved tickets found to index (Resolution column may be empty).")

    return len(texts)