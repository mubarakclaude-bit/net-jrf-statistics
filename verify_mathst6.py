#!/usr/bin/env python3
"""Exact checks for Mathematics T6 extrema examples."""
import json
from collections import Counter
assert 3*(-2)**2-3>0 and 3*0**2-3<0 and 3*2**2-3>0
assert (-1)**3-3*(-1)==2 and 1**3-3*1==-2
assert 2*2-4==0 and 2>0 and 2**2-4*2+7==3
assert 4*0**3==0 and 12*0**2==0 and 0**4==0
assert 3*0**2==0 and 6*0==0
with open("seed/maths_t6_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T6 exact anchors and mastery-pool structure: PASS")
