#!/usr/bin/env python3
"""Exact anchors for Mathematics T15 orthogonality."""
import json, math
from collections import Counter
# Projection of (3,1) onto (1,1) is (2,2); residual is orthogonal.
assert (3+1)/(1+1)==2
assert (3-2,1-2)==(1,-1)
assert (1-1)==0
# Orthonormal vectors from Gram-Schmidt.
assert math.isclose((1+1)/2,1.0)
assert (1-1)/2==0
# Orthogonal matrix determinant.
assert math.isclose((1/2)*(1*1-(-1*1)),1.0)
with open("seed/maths_t15_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T15 exact anchors and mastery-pool structure: PASS")
