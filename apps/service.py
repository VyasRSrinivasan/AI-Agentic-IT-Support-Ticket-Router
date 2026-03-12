from schemas import Ticket
from graph.workflow import build_graph

_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph

def run_pipeline(ticket):
    graph = get_graph()
    state = graph.invoke({"ticket": ticket})

    out = {}
    for k, v in state.items():
        out[k] = v.model_dump() if hasattr(v, "model_dump") else v
    return out