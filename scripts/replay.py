from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
print("[debug] sys.path[0] =", sys.path[0])

import argparse
import json
from datetime import datetime
import data


from data.load_raw_csv import load_tickets
from agents.agenticDetector import run_detector
from agents.agenticClassifier import run_classifier
from agents.agenticRouter import run_router
from agents.agenticResolver import run_resolver
from agents.agenticVerifier import run_verifier
from rag.retrieve import retrieve  


from graph.workflow import build_graph


def main(limit: int):
    # Output file
    run_dir = Path("outputs") / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = run_dir / f"replay_{ts}.jsonl"

    print(f"[replay] Writing results to {out_path}")

    count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for ticket in load_tickets(limit=limit):
            try:
                # ---- Agent pipeline ----
                detector_out = run_detector(ticket)
                triage_out = run_classifier(ticket, detector_out)
                decision = run_router(ticket, detector_out, triage_out)

                evidence = retrieve(ticket)  # should return EvidenceBundle or list[EvidenceChunk]
                resolution = run_resolver(ticket, triage_out, evidence)

                verification, decision2 = run_verifier(ticket, detector_out, triage_out, evidence, resolution, decision)
                decision = decision2

                # ---- Serialize one record ----
                record = {
                    "ticket_id": ticket.ticket_id,
                    "decision": decision.model_dump(),
                    "detector": detector_out.model_dump(),
                    "triage": triage_out.model_dump(),
                    "verification": verification.model_dump(),
                    "resolution": resolution.model_dump(),
                }

                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1

                print(f"[replay] processed ticket {ticket.ticket_id}")

            except Exception as e:
                print(f"[replay] ERROR on ticket {ticket.ticket_id}: {e}")

    print(f"[replay] completed {count} tickets")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay tickets through agent pipeline")
    parser.add_argument("--n", type=int, default=5, help="Number of tickets to process")
    args = parser.parse_args()

    main(limit=args.n)