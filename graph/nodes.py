# graph/nodes.py
from __future__ import annotations

from graph.state import GraphState

from agents.agenticDetector import run_detector
from agents.agenticClassifier import run_classifier
from agents.agenticRouter import run_router
from agents.agenticResolver import run_resolver
from agents.agenticVerifier import run_verifier
from rag.retrieve import retrieve


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