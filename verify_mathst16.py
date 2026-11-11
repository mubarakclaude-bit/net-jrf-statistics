#!/usr/bin/env python3
"""Exact anchors and mastery-pool structure for Mathematics T16."""
import json
from collections import Counter
# Trace cyclic identity for A=[[1,2],[3,4]], B=[[0,1],[2,0]].
A=((1,2),(3,4)); B=((0,1),(2,0))
AB=((4,1),(8,3)); BA=((3,4),(2,4))
assert AB[0][0]+AB[1][1] == 7
assert BA[0][0]+BA[1][1] == 7
assert AB != BA
# det(AB)=det(A)det(B): det(A)=-2, det(B)=-2, det(AB)=4.
assert (1*4-2*3)==-2 and (0*0-1*2)==-2
assert (4*3-1*8)==4
# 3x3 scalar rule: det(3A)=27 det(A).
assert 3**3*2 == 54
# Inverse example A=[[2,1],[1,1]], det=1, inverse is [[1,-1],[-1,2]].
M=((2,1),(1,1)); inv=((1,-1),(-1,2))
for i in range(2):
    for j in range(2):
        assert sum(M[i][k]*inv[k][j] for k in range(2)) == (1 if i==j else 0)
# Pool structure.
with open("seed/maths_t16_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T16 exact anchors and mastery-pool structure: PASS")
