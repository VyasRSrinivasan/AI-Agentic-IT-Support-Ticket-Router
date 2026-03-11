import argparse
import json

from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

def safe_get(obj, path, default=None):
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl_path", help="Path to outputs/runs/*.jsonl")
    args = ap.parse_args()

    n = 0
    decisions = Counter()
    safe_auto = 0
    grounded = 0
    has_evidence = 0

    # Optional: confidence averages (if you log them)
    conf_sum = 0.0
    conf_n = 0

    with open(args.jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            n += 1
            obj = json.loads(line)

            d = safe_get(obj, ["decision", "decision"]) or safe_get(obj, ["decision"])
            decisions[d] += 1

            if safe_get(obj, ["verification", "is_safe_to_auto_resolve"]) is True:
                safe_auto += 1

            citations = safe_get(obj, ["resolution", "citations"], []) or []
            if len(citations) > 0:
                grounded += 1

            kb = safe_get(obj, ["evidence", "kb"], []) or []
            pt = safe_get(obj, ["evidence", "past_tickets"], []) or []
            if len(kb) + len(pt) > 0:
                has_evidence += 1

            conf = safe_get(obj, ["resolution", "confidence"])
            if isinstance(conf, (int, float)):
                conf_sum += float(conf)
                conf_n += 1

    def pct(x): 
        return (x / n * 100.0) if n else 0.0

    print(f"tickets: {n}")
    print("decisions:", dict(decisions))
    print(f"AUTO_RESOLVE rate: {pct(decisions.get('AUTO_RESOLVE', 0)):.1f}%")
    print(f"ESCALATE rate:     {pct(decisions.get('ESCALATE', 0)):.1f}%")
    print(f"ASK_CLARIFY rate:  {pct(decisions.get('ASK_CLARIFYING', 0)):.1f}%")
    print(f"verifier_safe:     {safe_auto} ({pct(safe_auto):.1f}%)")
    print(f"grounded (citations present): {grounded} ({pct(grounded):.1f}%)")
    print(f"has evidence:      {has_evidence} ({pct(has_evidence):.1f}%)")
    if conf_n:
        print(f"avg resolution confidence: {conf_sum / conf_n:.3f} (n={conf_n})")


if __name__ == "__main__":
    main()