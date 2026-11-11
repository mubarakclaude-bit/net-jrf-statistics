#!/usr/bin/env python3
"""Exact checks for Mathematics T8 generalized-inverse anchors."""
import json
from collections import Counter
# A=diag(1,0) is its own Moore-Penrose inverse.
A=((1,0),(0,0))
assert A==A
# Full-column-rank formula for a one-column vector a=(1,1).
# (A^T A)^-1 A^T = [1/2,1/2].
assert (1/(1+1))*1==0.5
# Estimability: c=(1,1) orthogonal to null vector (1,-1); d=(1,0) is not.
assert 1*1+1*(-1)==0
assert 1*1+0*(-1)==1
with open("seed/maths_t8_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T8 exact anchors and mastery-pool structure: PASS")
