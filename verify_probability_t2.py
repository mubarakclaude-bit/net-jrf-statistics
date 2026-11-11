#!/usr/bin/env python3
"""Exact anchors and mastery-pool structure for Probability T2."""
import json
from collections import Counter
# For f(x,y)=2 on 0<y<x<1: f_X=2x, f_Y=2(1-y).
for x in (0.2,0.5,0.9): assert abs((1/x)*x-1)<1e-12
for y in (0.1,0.4,0.8): assert abs((1/(1-y))*(1-y)-1)<1e-12
assert abs(10+0.6*(4/5)*(15-20)-7.6)<1e-12
assert abs(10+0.6*(4/5)*(25-20)-12.4)<1e-12
assert abs(4**2*(1-0.6**2)-10.24)<1e-12
with open("seed/probability_t2_mastery.json",encoding="utf-8") as f: items=json.load(f)["items"]
assert len(items)==20 and Counter(q["diff"] for q in items)=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["answer"] for q in items)=={"A":5,"B":5,"C":5,"D":5}
assert sum(q["format"]=="numeric" for q in items)>=4 and sum(q["format"]=="multi" for q in items)>=2
for q in items:
 assert len(q["options"])==4 and q["answer"] in "ABCD"
 if q["format"]=="numeric": assert q.get("check")
 if q["format"]=="multi": assert len(q["statements"])==4 and len(q["verdicts"])==4
print("Probability T2 exact anchors and mastery-pool structure: PASS")
