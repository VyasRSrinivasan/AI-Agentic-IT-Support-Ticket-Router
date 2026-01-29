from __future__ import annotations

from typing import Optional, TypedDict

from schemas import (
    Ticket,
    DetectorOutput,
    TriageOutput,
    EvidenceBundle,
    ResolutionDraft,
    Decision,
    VerificationResult,
)

class GraphState(TypedDict, total=False):
    ticket: Ticket

    detector: DetectorOutput
    triage: TriageOutput
    evidence: EvidenceBundle
    resolution: ResolutionDraft

    decision: Decision
    verification: VerificationResult