# schemas/verifier.py
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class VerificationResult(BaseModel):
    is_safe_to_auto_resolve: bool = False
    reasons: List[str] = Field(default_factory=list)