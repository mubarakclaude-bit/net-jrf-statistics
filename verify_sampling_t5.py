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
