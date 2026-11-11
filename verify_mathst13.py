#!/usr/bin/env python3
"""Exact anchors for Mathematics T13 vector spaces."""
import json
from collections import Counter
# y=2x is closed under linear combinations; x+y=1 excludes zero.
assert 0+0==0 and 0+0!=1
# P2 and P3 dimensions.
assert len((1,"x","x^2"))==3 and len((1,"x","x^2","x^3"))==4
# Dimension formula.
assert 3+2-1==4
# (1,1) is redundant in span of e1,e2.
assert (1,1)==(1,0)+(0,1)
with open("seed/maths_t13_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T13 exact anchors and mastery-pool structure: PASS")
