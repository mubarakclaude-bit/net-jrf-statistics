#!/usr/bin/env python3
"""Exact anchors for Mathematics T14 linear systems."""
import json
from collections import Counter
# Unique system x+y=3, x-y=1 gives x=2,y=1.
assert 2+1==3 and 2-1==1
# Contradictory row 0=5 is impossible.
assert 0!=5
# Nullity and solution classification.
assert 5-3==2 and 4-2==2
# [[1,1],[1,-1]] determinant -2, full rank.
assert 1*(-1)-1*1==-2
with open("seed/maths_t14_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T14 exact anchors and mastery-pool structure: PASS")
