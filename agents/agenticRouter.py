from __future__ import annotations

from schemas import Ticket, DetectorOutput, TriageOutput, Decision


AUTO_RESOLVE_CONF_THRESHOLD = 0.78
RESOLVER_CONF_THRESHOLD = 0.80  # used later if you pass resolver confidence in

def run_router(ticket: Ticket, detector_out: DetectorOutput, triage_out: TriageOutput) -> Decision:
    # Security always escalates
    if detector_out.security_risk == "High" or triage_out.department == "Security":
        return Decision(
            decision="ESCALATE",
            reason="High security risk; requires human review.",
            confidence=0.9,
            target_queue="Security",
            escalation_level="Security",
        )

    # Missing info -> ask clarifying
    if detector_out.missing_info:
        return Decision(
            decision="ASK_CLARIFYING",
            reason="Ticket is missing key details needed to resolve safely.",
            confidence=0.6,
            clarifying_questions=[
                "Can you share the exact error message (if any)?",
                "When did this start happening and what changed recently?",
                "What steps have you already tried?"
            ]
        )

    # If classifier confidence is high and complexity not high, allow auto-resolve attempt
    if triage_out.confidence >= AUTO_RESOLVE_CONF_THRESHOLD and triage_out.complexity != "Complex":
        return Decision(
            decision="AUTO_RESOLVE",
            reason="High routing confidence and manageable complexity.",
            confidence=triage_out.confidence,
            target_queue=None,
            escalation_level="None",
        )

    # Otherwise escalate to department queue
    return Decision(
        decision="ESCALATE",
        reason="Low confidence or high complexity; route to human specialist.",
        confidence=triage_out.confidence,
        target_queue=triage_out.department,
        escalation_level="L1" if triage_out.complexity != "Complex" else "L2",
    )