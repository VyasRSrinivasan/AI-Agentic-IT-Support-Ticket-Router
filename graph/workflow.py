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
)


def build_graph():
    g = StateGraph(GraphState)

    g.add_node("detect", detect_node)
    g.add_node("classify", classify_node)
    g.add_node("retrieve", retrieve_node)
    g.add_node("route", route_node)
    g.add_node("resolve", resolve_node)
    g.add_node("verify", verify_node)

    g.set_entry_point("detect")

    g.add_edge("detect", "classify")
    g.add_edge("classify", "retrieve")
    g.add_edge("retrieve", "route")
    g.add_edge("route", "resolve")
    g.add_edge("resolve", "verify")
    g.add_edge("verify", END)

    return g.compile()