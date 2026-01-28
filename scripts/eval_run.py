import json, sys

path = sys.argv[1]
n = 0
auto_resolve = escalate = clarify = 0
safe = 0
has_citations = 0

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        n += 1
        obj = json.loads(line)
        d = obj["decision"]["decision"]
        if d == "AUTO_RESOLVE": auto_resolve += 1
        elif d == "ESCALATE": escalate += 1
        elif d == "ASK_CLARIFYING": clarify += 1

        if obj["verification"]["is_safe_to_auto_resolve"]:
            safe += 1
        if obj["resolution"].get("citations"):
            has_citations += 1

print("tickets:", n)
print("auto_resolve:", auto_resolve, f"({auto_resolve/n:.1%})")
print("escalate:", escalate, f"({escalate/n:.1%})")
print("ask_clarifying:", clarify, f"({clarify/n:.1%})")
print("verifier_safe:", safe, f"({safe/n:.1%})")
print("grounded (has citations):", has_citations, f"({has_citations/n:.1%})")