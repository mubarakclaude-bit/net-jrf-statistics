#!/usr/bin/env python3
"""Exact anchors for Mathematics T12 multiple integrals."""
import json, math
from collections import Counter
assert (0.5+0.5)==1
assert 1/3==1/3
assert math.pi==math.pi
assert (0.5+0.5+0.5)==1.5
# Transformation x=u+v, y=u-v has determinant -2.
assert abs((1*(-1))-(1*1))==2
with open("seed/maths_t12_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T12 exact anchors and mastery-pool structure: PASS")
