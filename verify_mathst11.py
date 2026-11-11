#!/usr/bin/env python3
"""Exact anchors for Mathematics T11 multivariable optimisation."""
import json
from collections import Counter
# Hessian tests.
assert 2*(-2)-0**2 == -4
assert 2*4-0**2 == 8
# Line-constrained minimum.
assert (0.5)**2+(0.5)**2 == 0.5 and 0.5+0.5==1
# Circle-constrained extrema: x=y=+/-1/sqrt(2), objective +/-sqrt(2).
assert (1/(2**0.5))**2*2 == 1
with open("seed/maths_t11_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T11 exact anchors and mastery-pool structure: PASS")
