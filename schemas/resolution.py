from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, confloat

from .evidence import EvidenceChunk


class ResolutionDraft(BaseModel):
    """
    Output of agents/resolver.py.
    Must be grounded: citations should not be empty for auto-resolve paths.
    """

    response_text: str = Field(..., description="Customer-facing draft response")
    citations: List[EvidenceChunk] = Field(default_factory=list, description="Evidence used to ground the response")
    next_steps: List[str] = Field(default_factory=list, description="Actionable next steps")
    confidence: confloat(ge=0.0, le=1.0) = 0.5