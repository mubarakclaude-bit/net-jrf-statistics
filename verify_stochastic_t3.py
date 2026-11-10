#!/usr/bin/env python3
"""Independent exact-arithmetic and structural checks for Stochastic T3."""
import json, math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/"seed/lesson_stochastic_t3.json").read_text())
P=json.loads((ROOT/"seed/stochastic_t3_mastery.json").read_text())
assert L["id"]=="stochastict3" and len(L["scenes"])>=11
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
# Exact worked example 1: h1=1+h2/2; h2=1+h1/2 -> both 2.
h1=h2=F(2)
assert h1==1+h2/F(2) and h2==1+h1/F(2)
# Self-loop example: h2=1+h2/2 -> 2; h1=1+3h2/4 -> 5/2.
h2=F(2); h1=1+F(3,4)*h2
assert h1==F(5,2) and h2==1+h2/F(2)
# Guaranteed-arrival example: h2=1; h1=1+h2/3 = 4/3.
h2=F(1); h1=1+F(1,3)*h2
assert h1==F(4,3)
# Two hard numeric pools: verify exact linear systems.
h1=F(12,7); h2=1+h1/F(4)
assert h1==1+h2/F(2)
h1=F(5,2); h2=1+h1/F(2)
assert h1==1+F(2,3)*h2
print("T3 exact arithmetic and structural checks: PASS")
