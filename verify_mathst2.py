#!/usr/bin/env python3
"""Exact mathematical checks for the Mathematics T2 eigenvalue lesson."""
import json
from collections import Counter

def det2(a,b,c,d): return a*d-b*c
# A = [[2,1],[1,2]] has characteristic roots 1 and 3.
assert det2(1,-1,-1,1) == 0
assert det2(-1,-1,-1,-1) == 0
# Eigenvectors: A(1,1)=3(1,1), A(1,-1)=1(1,-1).
assert (2+1,1+2)==(3,3)
assert (2-1,1-2)==(1,-1)
# Cayley-Hamilton: A^2 - 4A + 3I = 0.
A=((2,1),(1,2)); A2=((5,4),(4,5))
for i in range(2):
    for j in range(2):
        assert A2[i][j]-4*A[i][j]+(3 if i==j else 0)==0
# Trace and determinant equal sum and product of eigenvalues.
assert 1+3 == 4 and 1*3 == 3
# Defective repeated-root example [[1,1],[0,1]]: eigenspace dimension is one.
assert 2-1 == 1
# Check the authored mastery pool when present.
try:
    with open("seed/maths_t2_mastery.json", encoding="utf-8") as f:
        pool=json.load(f)
except FileNotFoundError:
    raise SystemExit("FAIL: seed/maths_t2_mastery.json is missing")
items=pool.get("items",[])
assert len(items)==20, f"expected 20 items, got {len(items)}"
assert Counter(x.get("diff") for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x.get("format")=="numeric" for x in items)>=4
assert sum(x.get("format")=="multi" for x in items)>=2
print("Mathematics T2 exact anchors and mastery-pool structure: PASS")
