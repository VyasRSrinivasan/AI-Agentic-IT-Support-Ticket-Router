# graph/nodes.py
from __future__ import annotations

from graph.state import GraphState

from agents.agenticDetector import run_detector
from agents.agenticClassifier import run_classifier
from agents.agenticRouter import run_router
from agents.agenticResolver import run_resolver
from agents.agenticVerifier import run_verifier
from rag.retrieve import retrieve

from langgraph.types import interrupt

def human_review_node(state: GraphState) -> GraphState:

    if state.get("human_action"):
        return {
            "human_action": state.get("human_action"),
            "human_notes": state.get("human_notes", "")
        }
    decision = state.get("decision")
    verification = state.get("verification")
    triage = state.get("triage")
    evidence = state.get("evidence")
    resolution = state.get("resolution")

    top_kb = []
    if evidence is not None:
        # EvidenceBundle -> evidence.kb is a list[EvidenceChunk]
        top_kb = [c.model_dump() for c in evidence.kb[:3]]

    payload = {
        "message": "Human review required",
        "decision": decision.model_dump() if decision else None,
        "verification": verification.model_dump() if verification else None,
        "triage": triage.model_dump() if triage else None,
        "top_evidence": top_kb,
        "draft_response": resolution.model_dump() if resolution else None,
    }

    human_input = interrupt(payload)

    return {
        "human_action": human_input.get("human_action"),
        "human_notes": human_input.get("human_notes", ""),
    
    }


def detect_node(state: GraphState) -> GraphState:
    ticket = state["ticket"]
    detector_out = run_detector(ticket)
    return {"detector": detector_out}


def classify_node(state: GraphState) -> GraphState:
    ticket = state["ticket"]
    detector_out = state["detector"]
    triage_out = run_classifier(ticket, detector_out)
    return {"triage": triage_out}


def retrieve_node(state: GraphState) -> GraphState:
    ticket = state["ticket"]
    evidence = retrieve(ticket)
    return {"evidence": evidence}


def route_node(state: GraphState) -> GraphState:
    ticket = state["ticket"]
    detector_out = state["detector"]
    triage_out = state["triage"]
    decision = run_router(ticket, detector_out, triage_out)
    return {"decision": decision}


def resolve_node(state: GraphState) -> GraphState:
    ticket = state["ticket"]
    triage_out = state["triage"]
    evidence = state["evidence"]
    resolution = run_resolver(ticket, triage_out, evidence)
    return {"resolution": resolution}


def verify_node(state: GraphState) -> GraphState:
    ticket = state["ticket"]
    detector_out = state["detector"]
    triage_out = state["triage"]
    evidence = state["evidence"]
    resolution = state["resolution"]
    decision = state["decision"]

    verification, updated_decision = run_verifier(
        ticket, detector_out, triage_out, evidence, resolution, decision
    )
    return {"verification": verification, "decision": updated_decision}