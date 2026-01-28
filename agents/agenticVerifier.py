# agents/agenticVerifier.py
from __future__ import annotations

from schemas import (
    Ticket,
    DetectorOutput,
    TriageOutput,
    EvidenceBundle,
    ResolutionDraft,
    Decision,
    VerificationResult,
)

AUTO_RESOLVE_MIN_CONF = 0.80
MIN_CITATIONS = 1


def run_verifier(
    ticket: Ticket,
    detector: DetectorOutput,
    triage: TriageOutput,
    evidence: EvidenceBundle,
    resolution: ResolutionDraft,
    decision: Decision,
) -> tuple[VerificationResult, Decision]:
    """
    Minimal safety + grounding verifier.

    - AUTO_RESOLVE is allowed only if:
      * security risk is not High
      * there is at least MIN_CITATIONS citation
      * resolution confidence >= AUTO_RESOLVE_MIN_CONF
      * triage complexity isn't Complex (optional)
    """

    reasons: list[str] = []

    # Security gate
    if detector.security_risk == "High":
        reasons.append("High security risk: must escalate to human.")
        verified = VerificationResult(is_safe_to_auto_resolve=False, reasons=reasons)
        updated = Decision(
            decision="ESCALATE",
            reason="; ".join(reasons),
            confidence=0.95,
            target_queue="Security",
            escalation_level="Security",
        )
        return verified, updated

    # If decision isn't AUTO_RESOLVE, we won't force it to resolve.
    if decision.decision != "AUTO_RESOLVE":
        # Still provide verification notes for logging.
        if len(resolution.citations) < MIN_CITATIONS:
            reasons.append("No citations found (grounding weak).")
        if resolution.confidence < AUTO_RESOLVE_MIN_CONF:
            reasons.append(f"Resolution confidence {resolution.confidence:.2f} below threshold.")
        return VerificationResult(is_safe_to_auto_resolve=False, reasons=reasons), decision

    # AUTO_RESOLVE gates
    if triage.complexity == "Complex":
        reasons.append("Complex ticket: prefer escalation.")
    if len(resolution.citations) < MIN_CITATIONS:
        reasons.append("Missing citations: cannot auto-resolve safely.")
    if resolution.confidence < AUTO_RESOLVE_MIN_CONF:
        reasons.append(f"Resolution confidence {resolution.confidence:.2f} below threshold.")

    is_safe = len(reasons) == 0

    if is_safe:
        return VerificationResult(is_safe_to_auto_resolve=True, reasons=[]), decision

    # If not safe, override AUTO_RESOLVE → ESCALATE (or ASK_CLARIFYING if missing info)
    if detector.missing_info:
        updated = Decision(
            decision="ASK_CLARIFYING",
            reason="; ".join(reasons) + " Missing info: ask clarifying questions.",
            confidence=0.65,
            clarifying_questions=[
                "Can you share the exact error message (if any)?",
                "When did this start happening and what changed recently?",
                "What steps have you already tried?",
            ],
        )
    else:
        updated = Decision(
            decision="ESCALATE",
            reason="; ".join(reasons),
            confidence=decision.confidence,
            target_queue=triage.department,
            escalation_level="L1" if triage.complexity != "Complex" else "L2",
        )

    return VerificationResult(is_safe_to_auto_resolve=False, reasons=reasons), updated