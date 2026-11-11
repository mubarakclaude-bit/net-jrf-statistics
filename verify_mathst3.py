#!/usr/bin/env python3
"""Exact checks for Mathematics T3 quadratic-form anchors."""
import json
from collections import Counter
# 2x2 positive-definite anchor: A=[[2,1],[1,2]], minors 2 and 3.
assert 2 > 0 and (2*2-1*1) > 0
# 2x2 negative-definite anchor: diag(-1,-2), signs (-,+).
assert -1 < 0 and (-1)*(-2) == 2 > 0
# Indefinite anchor diag(1,-4): both signs occur; determinant negative.
assert 1 > 0 and -4 < 0 and 1*(-4) < 0
# Semidefinite anchor diag(3,0,2): nonnegative spectrum, one zero.
eigs=(3,0,2)
assert all(x>=0 for x in eigs) and any(x==0 for x in eigs)
# Inertia is read from diagonal coefficients.
assert (sum(x>0 for x in (3,-2,5)),sum(x<0 for x in (3,-2,5)),sum(x==0 for x in (3,-2,5)))==(2,1,0)
with open("seed/maths_t3_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T3 exact anchors and mastery-pool structure: PASS")
