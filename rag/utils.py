# rag/utils.py
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, Optional


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def read_text_file(path: Path) -> str:
    # Handles UTF-8 and UTF-8 BOM safely
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def safe_metadata(**kwargs) -> Dict:
    # Keep metadata JSON-serializable and safe (no PII)
    return {k: v for k, v in kwargs.items() if v is not None}


def clean_text(text: str) -> str:
    # Keep this minimal: strip trailing spaces; collapse excessive whitespace.
    return " ".join(text.split())