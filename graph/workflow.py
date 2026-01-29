# graph/workflow.py
from __future__ import annotations

from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.nodes import (
    detect_node,
    classify_node,
    retrieve_node,
    route_node,
    resolve_node,
    verify_node,
    human_review_node,
)

def after_route(state):
    d = state["decision"].decision  # Decision is a Pydantic model
    if d == "AUTO_RESOLVE":
        return "resolve"
    if d == "ASK-CLARIFYING":
        return END
    # If we are escalating or asking clarifying, go to human review interrupt
    return "human_review"

def after_verify(state: GraphState) -> str:
    # If verifier says safe, end (auto-resolve complete)
    if state["verification"].is_safe_to_auto_resolve:
        return END
    # Otherwise require human review (interrupt)
    return "human_review"

'''
def _route_after_decision(state: GraphState):
    d = state["decision"]["decision"] if isinstance(state["decision"], dict) else state["decision"].decision
    if d == "AUTO_RESOLVE":
        return "resolve"
    if d == "ASK_CLARIFYING":
        return END
    return END
'''

def build_graph():
    g = StateGraph(GraphState)

    g.add_node("detect", detect_node)
    g.add_node("classify", classify_node)
    g.add_node("retrieve", retrieve_node)
    g.add_node("route", route_node)
    g.add_node("resolve", resolve_node)
    g.add_node("verify", verify_node)

    g.add_node("human_review", human_review_node)

    g.set_entry_point("detect")

    g.add_edge("detect", "classify")
    g.add_edge("classify", "retrieve")
    g.add_edge("retrieve", "route")

    g.add_conditional_edges("route", after_route)


    g.add_edge("resolve", "verify")
    g.add_conditional_edges("verify", after_verify)

    g.add_edge("human_review", END)

    return g.compile()