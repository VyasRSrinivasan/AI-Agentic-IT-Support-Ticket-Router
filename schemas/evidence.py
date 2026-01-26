from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, confloat


class EvidenceChunk(BaseModel):
    """
    One retrieved chunk used for grounding and citations.
    """

    doc_id: str = Field(..., description="Stable chunk identifier (hash/path+chunk index)")
    title: str = ""
    source: str = Field(default="", description="File path / URL / dataset reference")
    snippet: str = Field(..., description="Text snippet shown in UI and used for grounding")
    score: Optional[confloat(ge=0.0, le=1.0)] = None
    source_type: Optional[str] = Field(default=None, description="kb | past_ticket | faq | runbook | policy (optional)")
    metadata: dict = Field(default_factory=dict, description="Any extra safe metadata (no PII)")


class EvidenceBundle(BaseModel):
    """
    A structured container for evidence from multiple retrievers.
    """

    kb: List[EvidenceChunk] = Field(default_factory=list)
    past_tickets: List[EvidenceChunk] = Field(default_factory=list)

    def all(self) -> List[EvidenceChunk]:
        return [*self.kb, *self.past_tickets]