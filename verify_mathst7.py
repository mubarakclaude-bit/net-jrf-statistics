#!/usr/bin/env python3
"""Exact anchors for Mathematics T7 integrals."""
import json
from collections import Counter
assert (2**2+2)-(0**2+0)==6
assert 1/(3-1)==0.5
assert 1/(1-0.5)==2
assert 1/0.01-1 > 1/0.1-1
with open("seed/maths_t7_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T7 exact anchors and mastery-pool structure: PASS")
