from __future__ import annotations

from typing import List, Union

from schemas import Ticket, TriageOutput, EvidenceChunk, EvidenceBundle, ResolutionDraft


def _flatten_evidence(evidence: Union[EvidenceBundle, List[EvidenceChunk]]) -> List[EvidenceChunk]:
    if isinstance(evidence, EvidenceBundle):
        return evidence.all()
    return evidence

def run_resolver(
    ticket: Ticket,
    triage_out: TriageOutput,
    evidence: Union[EvidenceBundle, List[EvidenceChunk]],
) -> ResolutionDraft:
    chunks = _flatten_evidence(evidence)

    # If no evidence, do NOT pretend—return a low-confidence draft
    if not chunks:
        return ResolutionDraft(
            response_text=(
                "Thanks for reaching out. I’m not seeing enough knowledge-base context to answer confidently. "
                "I’m escalating this to a specialist so you can get the correct help."
            ),
            citations=[],
            next_steps=["Escalate to human specialist with ticket summary."],
            confidence=0.25,
        )

    # Very simple grounded template (you can later replace with LangChain LLM generation)
    top = chunks[:3]
    evidence_titles = ", ".join([c.title or c.doc_id for c in top])

    response_lines = [
        "Thanks for reaching out — here’s what I found based on our help resources:",
        "",
        f"**Issue category:** {triage_out.department}",
        "",
        "### Suggested steps",
    ]

    # Turn evidence snippets into "steps" (basic heuristic)
    next_steps = []
    for idx, c in enumerate(top, start=1):
        step = c.snippet.strip().split("\n")[0]
        if len(step) > 140:
            step = step[:140].rstrip() + "…"
        response_lines.append(f"{idx}. {step}")
        next_steps.append(step)

    response_lines.append("")
    response_lines.append(f"(Sources consulted: {evidence_titles})")

    # Confidence heuristic: more evidence + higher classifier confidence → higher
    conf = min(0.9, 0.55 + 0.1 * len(top) + 0.25 * triage_out.confidence)

    return ResolutionDraft(
        response_text="\n".join(response_lines),
        citations=top,
        next_steps=next_steps,
        confidence=conf,
    )