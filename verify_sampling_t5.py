#!/usr/bin/env python3
from fractions import Fraction as F
N,n=20,4
k=N//n
assert k==5
sample=[3+j*k for j in range(n)]
assert sample==[3,8,13,18]
assert F(1,k)==F(n,N)==F(1,5)
samples=[[r+j*k for j in range(n)] for r in range(1,k+1)]
assert samples==[[1,6,11,16],[2,7,12,17],[3,8,13,18],[4,9,14,19],[5,10,15,20]]
for unit in range(1,N+1):
    assert sum(unit in s for s in samples)==1
assert sum(8 in s and 13 in s for s in samples)==1
assert sum(8 in s and 12 in s for s in samples)==0
k2=36//6
assert k2==6 and [4+j*k2 for j in range(6)]==[4,10,16,22,28,34]
means=[F(3),F(5),F(7),F(9)]
grand=sum(means)/len(means)
variance=sum((x-grand)**2 for x in means)/len(means)
assert grand==6 and variance==5
print("PASS interval, random start, inclusion and pair probabilities")
print("PASS exact design mean =",grand,"variance =",variance)
# sampling-t5-m06 (circular systematic sample, N=12, n=3, R=11): exactly one option is the selected set.
import json
from pathlib import Path
_pool=json.loads((Path(__file__).resolve().parent/"seed"/"sampling_t5_mastery.json").read_text(encoding="utf-8"))
_m06=next(i for i in _pool["items"] if i["id"]=="sampling-t5-m06")
_sel={((11-1+j*4)%12)+1 for j in range(3)}
assert _sel=={11,3,7}
_hits=[k for k,o in enumerate(_m06["options"]) if {int(x) for x in o.replace(" ","").split(",")}==_sel]
assert _hits==["ABCD".index(_m06["answer"])], _hits
print("PASS sampling-t5-m06 has exactly one option equal to the selected set {11,3,7}")
