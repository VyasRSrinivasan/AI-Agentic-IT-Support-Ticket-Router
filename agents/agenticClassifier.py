from __future__ import annotations

from schemas import Ticket, DetectorOutput, TriageOutput


DEPT_KEYWORDS = {
    "Billing": ["invoice", "charge", "refund", "payment", "billing", "receipt", "subscription", "cancel", "cancellation"],
    "Account": ["login", "sign in", "invalid credentials", "account", "password", "locked out", "2fa", "mfa", "email change"],
    "Technical Support": ["crash", "error", "bug", "install", "setup", "network", "wifi", "update", "firmware", "not turning on"],
    "Product Support": ["feature request", "how do i", "where can i", "option", "configure", "guide", "instructions"],
    "Security": ["phishing", "suspicious", "hacked", "unauthorized", "compromised", "malware", "different domain"],
}


def _pick_department(text: str, detector_out: DetectorOutput) -> tuple[str, float]:
    if detector_out.security_risk == "High":
        return "Security", 0.9

    best_dept = "Technical Support"
    best_score = 0

    for dept, kws in DEPT_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in text)
        if score > best_score:
            best_score = score
            best_dept = dept

    confidence = 0.55
    if best_score >= 3:
        confidence = 0.85
    elif best_score == 2:
        confidence = 0.75
    elif best_score == 1:
        confidence = 0.65

    return best_dept, confidence


def _infer_urgency(ticket: Ticket, text: str, detector_out: DetectorOutput) -> str:
    # Security overrides everything
    if detector_out.security_risk == "High":
        return "Critical"

    # Start from dataset priority as a hint, not a final answer
    urgency = "Medium"
    if ticket.ticket_priority:
        p = ticket.ticket_priority.strip().lower()
        if p == "critical":
            urgency = "High"   # soften by default; reserve Critical for truly severe cases
        elif p == "high":
            urgency = "High"
        elif p == "medium":
            urgency = "Medium"
        elif p == "low":
            urgency = "Low"

    # Text-based urgency overrides
    if any(w in text for w in ["urgent", "asap", "immediately", "right away"]):
        urgency = "High"

    if any(w in text for w in ["can't access", "locked out", "not turning on", "data loss"]):
        urgency = "High"

    if "data loss" in text:
        urgency = "Critical"

    return urgency


def _infer_complexity(text: str) -> str:
    # Truly complex / high-effort cases
    if any(w in text for w in ["data loss", "crash", "intermittent"]):
        return "Complex"

    # Moderate: common support cases with some troubleshooting needed
    if any(w in text for w in ["after update", "network", "won't start", "not turning on", "login", "reset", "refund", "charge", "setup", "install"]):
        return "Moderate"

    return "Simple"


def run_classifier(ticket: Ticket, detector_out: DetectorOutput) -> TriageOutput:
    text = ticket.text_for_llm().lower()

    dept, dept_conf = _pick_department(text, detector_out)
    urgency = _infer_urgency(ticket, text, detector_out)
    complexity = _infer_complexity(text)

    summary = []
    summary.append(f"Primary issue appears related to {dept}.")
    if ticket.product:
        summary.append(f"Product: {ticket.product}.")
    if detector_out.security_risk != "Low":
        summary.append(f"Security risk flagged: {detector_out.security_risk}.")
    if detector_out.missing_info:
        summary.append("Ticket may be missing key details; clarification may be needed.")

    confidence = dept_conf

    # lower confidence if info is missing
    if detector_out.missing_info:
        confidence = max(0.35, confidence - 0.2)

    # slightly lower confidence for complex cases
    if complexity == "Complex":
        confidence = max(0.40, confidence - 0.10)

    return TriageOutput(
        department=dept,
        urgency=urgency,
        complexity=complexity,
        confidence=confidence,
        summary=summary[:5],
        entities=[],
        sentiment=None,
    )