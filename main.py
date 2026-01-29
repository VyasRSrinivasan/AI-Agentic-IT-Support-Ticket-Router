
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

        dec = state.get("decision")
        print(f"Processed ticket {ticket.ticket_id} -> {dec.decision if dec else None}")


if __name__ == "__main__":
    main()