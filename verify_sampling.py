#!/usr/bin/env python3
"""Exact independent checks for Sampling Theory topics; currently covers sampling-t1.
Run: python verify_sampling.py
All worked-example figures are recomputed with Fraction, not copied from lesson output.
"""
from fractions import Fraction as F
from itertools import combinations

# SRSWOR N=3, n=2, y=(10,20,30)
y=(F(10),F(20),F(30)); N=3; n=2
samples=list(combinations(range(N),n))
pi=F(n,N); pij=F(n*(n-1),N*(N-1))
assert len(samples)==3
assert pi==F(2,3) and pij==F(1,3)
ht=[]
vhat=[]
for s in samples:
    weighted=[y[i]/pi for i in s]
    ht.append(sum(weighted,F(0)))
    # Full ordered-pair double sum, including diagonal terms.
    z=F(0)
    for i in s:
        for j in s:
            joint=pi if i==j else pij
            z += ((joint-pi*pi)/joint)*(y[i]/pi)*(y[j]/pi)
    vhat.append(z)
assert ht==[F(45),F(60),F(75)], ht
assert sum(ht,F(0))/len(ht)==sum(y,F(0))==F(60)
variance=sum((x-F(60))**2 for x in ht)/len(ht)
assert variance==F(150), variance
assert vhat==[F(75),F(300),F(75)], vhat
assert sum(vhat,F(0))/len(vhat)==variance
print("PASS: pi =",pi,"pi_ij =",pij)
print("PASS: HT estimates =",[str(x) for x in ht])
print("PASS: design expectation =",sum(ht,F(0))/len(ht))
print("PASS: design variance =",variance)
print("PASS: unbiased variance estimates =",[str(x) for x in vhat])
print("PASS: mean variance estimate =",sum(vhat,F(0))/len(vhat))
# A zero pairwise probability makes the usual variance-estimator term undefined.
pi1=pi2=F(1,2); pi12=F(0)
assert pi1>0 and pi2>0 and pi12==0
try:
    (pi12-pi1*pi2)/pi12
    raise AssertionError("zero-pair term unexpectedly defined")
except ZeroDivisionError:
    pass
print("PASS: first-order positivity does not imply pairwise positivity")
