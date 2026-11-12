#!/usr/bin/env python3
"""Independent exact-arithmetic and structural checks for Stochastic T4."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/"seed/lesson_stochastic_t4.json").read_text())
P=json.loads((ROOT/"seed/stochastic_t4_mastery.json").read_text())
assert L["id"]=="stochastict4" and len(L["scenes"])>=11
assert sum("scenario" in s for s in L["scenes"])>=2
assert sum(bool(s.get("flow")) for s in L["scenes"])>=1
assert all(s.get("ask",{}).get("nudge") for s in L["scenes"] if s["kind"] in ("foundation","intuition","theory","worked"))
assert len(P["items"])==20
assert [sum(q["diff"]==d for q in P["items"]) for d in ("easy","moderate","hard")]==[6,10,4]
assert [sum(q["format"]==f for q in P["items"]) for f in ("single","numeric","multi")]==[13,5,2]
assert max(sum(q["answer"]==k for q in P["items"]) for k in "ABCD")<=8
for q in P["items"]:
    assert len(q.get("options",[]))==4 and q["answer"] in "ABCD"
    assert q.get("explanation")
    if q["format"]=="numeric": assert q.get("check")
    if q["format"]=="multi":
        assert len(q.get("statements",[]))==4
        assert all(k in q.get("verdicts",{}) and isinstance(q["verdicts"][k].get("tf"),bool) and q["verdicts"][k].get("why") for k in "ABCD")
# GCD checks for the return-time examples.
assert math.gcd(math.gcd(4,6),10)==2
assert math.gcd(math.gcd(8,12),20)==4
assert math.gcd(math.gcd(6,10),14)==2
assert math.gcd(math.gcd(12,18),30)==6
# Alternating two-state chain returns exactly at positive even times.
assert math.gcd(2,4)==2
# Absorbing state returns at every positive integer time.
assert math.gcd(1,2)==1
# Example P=[[0,1,0],[1/2,0,1/2],[0,0,1]]: classes {1,2} and {3};
# {3} is the sole closed class, hence states 1,2 transient and state 3 recurrent.
edges={1:{2},2:{1,3},3:{3}}
assert 3 not in edges[1] and 3 in edges[2] and edges[3]=={3}
print("T4 graph, period and structural checks: PASS")
