
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from graph.workflow import build_graph
from data.load_raw_csv import load_tickets

from langgraph.types import Interrupt


def main(n: int = 5):
    graph = build_graph()

    for ticket in load_tickets(limit=n):
        state_in = {"ticket": ticket}

        try:
            state = graph.invoke(state_in)
        except Interrupt as e:
            print("\n[HITL] interrupt payload:")
            print(e.value)

            # Simulate a human decision:
            resume = {
                **state_in,
                "human_action": "ESCALATE",
                "human_notes": "Auto-resume for local testing.",
            }
            state = graph.invoke(resume)

        tri = state.get("triage")
        dec = state.get("decision")
        ver = state.get("verification")

        print(
            f"Ticket {ticket.ticket_id} | "
            f"dept={tri.department if tri else None} | "
            f"urgency={tri.urgency if tri else None} | "
            f"complexity={tri.complexity if tri else None} | "
            f"triage_conf={tri.confidence if tri else None}"
        )

        print(
            f"Ticket {ticket.ticket_id} -> {dec.decision} | "
            f"reason={dec.reason} | "
            f"safe={ver.is_safe_to_auto_resolve if ver else None} | "
            f"verifier_reasons={ver.reasons if ver else None}"
        )


if __name__ == "__main__":
    main()