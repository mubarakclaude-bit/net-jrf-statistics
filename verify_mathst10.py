#!/usr/bin/env python3
"""Exact anchors for Mathematics T10 partial and total derivatives."""
import json
from collections import Counter
# f=x^2 y + 3 x y^2
# f_x=2xy+3y^2; f_y=x^2+6xy; mixed=2x+6y.
# z=x^2+y^2 along x=t,y=2t => dz/dt=10t.
for t in (0,1,2):
    assert 2*t*1 + 2*(2*t)*2 == 10*t
# At (1,2), gradient=(2,4), norm=2sqrt(5), direction dot=22/5.
assert 2*3/5 + 4*4/5 == 22/5
with open("seed/maths_t10_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T10 exact anchors and mastery-pool structure: PASS")
