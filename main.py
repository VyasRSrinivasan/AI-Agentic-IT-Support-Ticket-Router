
import sys
from pathlib import Path

# Ensure project root is on sys.path (same pattern as replay.py)
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from graph.workflow import build_graph
from data.load_raw_csv import load_tickets


def main(n: int = 5):
    graph = build_graph()

    for ticket in load_tickets(limit=n):
        state = graph.invoke({"ticket": ticket})
        print(f"Processed ticket {ticket.ticket_id}")


if __name__ == "__main__":
    main()