#!/usr/bin/env python3
"""Exact rational verification for stochastic-t2 lesson examples and counterexamples."""
from fractions import Fraction as F

def mv(v,A):
    return [sum(v[i]*A[i][j] for i in range(len(v))) for j in range(len(A[0]))]
def check(P,pi):
    assert all(x>=0 for row in P for x in row)
    assert all(sum(row)==1 for row in P)
    assert all(x>=0 for x in pi) and sum(pi)==1
    assert mv(pi,P)==pi
P1=[[F(4,5),F(1,5)],[F(2,5),F(3,5)]]
pi1=[F(2,3),F(1,3)]; check(P1,pi1)
P2=[[F(7,10),F(3,10)],[F(1,5),F(4,5)]]
pi2=[F(2,5),F(3,5)]; check(P2,pi2)
P3=[[F(1,2),F(1,2),F(0)],[F(0),F(1,2),F(1,2)],[F(1,2),F(0),F(1,2)]]
pi3=[F(1,3)]*3; check(P3,pi3)
P4=[[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(1,3),F(1,3),F(1,3)]]
for t in (F(0),F(1,7),F(1,2),F(1)): check(P4,[t,1-t,F(0)])
P5=[[F(0),F(1)],[F(1),F(0)]]
check(P5,[F(1,2),F(1,2)])
assert mv([F(1),F(0)],P5)==[F(0),F(1)]
assert mv([F(0),F(1)],P5)==[F(1),F(0)]
P6=[[F(1,2),F(1,2),F(0)],[F(1,4),F(1,2),F(1,4)],[F(0),F(1,3),F(2,3)]]
pi6=[F(2,9),F(4,9),F(1,3)]; check(P6,pi6)
print("PASS: exact stationary vectors and probability constraints.")
print("PASS: reducible family at endpoints and interior rational points.")
print("PASS: periodic example has stationary vector but point-mass distributions oscillate.")
print("PASS: hard three-state example pi =",pi6)
