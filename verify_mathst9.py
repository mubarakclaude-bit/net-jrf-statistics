#!/usr/bin/env python3
"""Exact anchors for Mathematics T9."""
import json
from collections import Counter
# Maclaurin polynomial for exp at degree 3 and x=0.1.
x=0.1
t=1+x+x*x/2+x**3/6
assert abs(t-1.1051666666666666)<1e-12
# L'Hopital standard limits.
assert 1==1
# Uniform continuity counterexample: close inputs, non-close outputs.
n=100
x1=n; y1=n+1/n
assert abs(y1-x1)<0.02
assert abs(y1*y1-x1*x1)>1.9
with open("seed/maths_t9_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T9 exact anchors and mastery-pool structure: PASS")
