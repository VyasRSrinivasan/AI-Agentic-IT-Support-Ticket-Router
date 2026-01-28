from __future__ import annotations

import re
from typing import List

from schemas import Ticket, DetectorOutput


_EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
_URL_RE = re.compile(r"https?://\S+|www\.\S+")

SECURITY_KEYWORDS_HIGH = {
    "password", "passwd", "otp", "2fa", "mfa", "verification code",
    "reset link", "suspicious", "phishing", "hacked", "compromised",
    "unauthorized", "account takeover", "login from", "different domain",
    "credit card", "ssn", "social security"
}

MISSING_INFO_PATTERNS = [
    r"\bit doesn't work\b",
    r"\bnot working\b",
    r"\bbroken\b",
    r"\bhelp\b$",
    r"\bplease fix\b",
]

def run_detector(ticket: Ticket) -> DetectorOutput:
    text = ticket.text_for_llm().lower()
    signals: List[str] = []

    # Security signals
    urls = _URL_RE.findall(text)
    if urls:
        signals.append(f"contains_url:{len(urls)}")
    if _EMAIL_RE.search(text):
        signals.append("contains_email_address")

    high_hits = [kw for kw in SECURITY_KEYWORDS_HIGH if kw in text]
    if high_hits:
        signals.append("security_keywords:" + ",".join(sorted(high_hits)[:5]))

    security_risk = "Low"
    if high_hits:
        security_risk = "High"
    elif "login" in text or "credentials" in text or "invalid credentials" in text:
        security_risk = "Medium"

    # Missing info detection
    missing_info = False
    for pat in MISSING_INFO_PATTERNS:
        if re.search(pat, text):
            missing_info = True
            signals.append("missing_info_pattern")
            break

    # Very short descriptions are often underspecified
    if len(ticket.body.strip()) < 40:
        missing_info = True
        signals.append("body_too_short")

    return DetectorOutput(
        security_risk=security_risk,
        missing_info=missing_info,
        signals=signals
    )