# rag/embeddings.py
from __future__ import annotations

import hashlib
from typing import List


class FakeEmbeddingFunction:
    """
    Compatible with Chroma embedding interface.
    Chroma calls:
      - embedding_function.name()
      - embedding_function.__call__(input=[...])
      - embedding_function.embed_query(input="...")
      - embedding_function.embed_documents(input=[...])  (some versions)
    """

    def __init__(self, dim: int = 384):
        self.dim = dim

    def name(self) -> str:
        return "fake_embedding_function_v3"

    # Chroma expects parameter name EXACTLY "input"
    def __call__(self, input: List[str]) -> List[List[float]]:
        return [self._embed_one(t) for t in input]

    # Chroma is calling embed_query(input="...")
    def embed_query(self, input: Any, **kwargs) -> List[float]:
        if isinstance(input, list):
            # join list of strings into one query
            input = "\n".join(str(x) for x in input)
        return self._embed_one(str(input))

    # Some Chroma paths call embed_documents(input=[...])
    def embed_documents(self, input: List[str], **kwargs) -> List[List[float]]:
        return [self._embed_one(t) for t in input]

    def _embed_one(self, text: str) -> List[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        v = [(b / 255.0) for b in h]
        return (v * ((self.dim // len(v)) + 1))[: self.dim]


def get_embedding_function():
    return FakeEmbeddingFunction(dim=384)