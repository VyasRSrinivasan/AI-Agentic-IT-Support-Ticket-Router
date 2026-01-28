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
    # hard override for security
    if detector_out.security_risk == "High":
        return "Security", 0.9

    best_dept = "Technical Support"
    best_score = 0

    for dept, kws in DEPT_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in text)
        if score > best_score:
            best_score = score
            best_dept = dept

    # convert keyword hit count into a rough confidence
    confidence = 0.55
    if best_score >= 3:
        confidence = 0.85
    elif best_score == 2:
        confidence = 0.75
    elif best_score == 1:
        confidence = 0.65

    return best_dept, confidence

def _infer_urgency(ticket: Ticket, text: str) -> str:
    # Use raw dataset priority if present
    if ticket.ticket_priority:
        p = ticket.ticket_priority.strip().lower()
        if p in {"critical"}:
            return "Critical"
        if p in {"high"}:
            return "High"
        if p in {"medium"}:
            return "Medium"
        if p in {"low"}:
            return "Low"

    # otherwise infer
    if any(w in text for w in ["urgent", "asap", "immediately", "right away"]):
        return "High"
    if any(w in text for w in ["can't access", "locked out", "not turning on", "data loss"]):
        return "High"
    return "Medium"

def _infer_complexity(text: str) -> str:
    if any(w in text for w in ["data loss", "crash", "intermittent", "after update", "network", "won't start"]):
        return "Complex"
    if any(w in text for w in ["login", "reset", "refund", "charge", "setup", "install"]):
        return "Moderate"
    return "Simple"

def run_classifier(ticket: Ticket, detector_out: DetectorOutput) -> TriageOutput:
    text = ticket.text_for_llm().lower()

    dept, dept_conf = _pick_department(text, detector_out)
    urgency = _infer_urgency(ticket, text)
    complexity = _infer_complexity(text)

    summary = []
    summary.append(f"Primary issue appears related to {dept}.")
    if ticket.product:
        summary.append(f"Product: {ticket.product}.")
    if detector_out.security_risk != "Low":
        summary.append(f"Security risk flagged: {detector_out.security_risk}.")
    if detector_out.missing_info:
        summary.append("Ticket may be missing key details; clarification may be needed.")

    # overall confidence: department confidence adjusted down if missing info
    confidence = dept_conf
    if detector_out.missing_info:
        confidence = max(0.35, confidence - 0.2)

    return TriageOutput(
        department=dept,
        urgency=urgency,            # "Low|Medium|High|Critical"
        complexity=complexity,      # "Simple|Moderate|Complex"
        confidence=confidence,
        summary=summary[:5],
        entities=[],
        sentiment=None
    )