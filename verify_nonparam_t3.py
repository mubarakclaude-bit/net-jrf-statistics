#!/usr/bin/env python3
"""Independent numeric checks for Kruskal–Wallis and Friedman lessons."""
from fractions import Fraction
n=[4,4,4]; R=[10,26,42]; N=sum(n); k=len(n)
assert sum(R)==N*(N+1)//2==78
H=Fraction(12,N*(N+1))*sum(Fraction(r*r,ni) for r,ni in zip(R,n))-3*(N+1)
assert H==Fraction(128,13) and k-1==2
cols=[[3,3,3,2],[1,1,2,3],[2,2,1,1]]
b=4; k=3; sums=[sum(c) for c in cols]
assert sums==[11,7,6] and sum(sums)==b*k*(k+1)//2==24
Q=Fraction(12,b*k*(k+1))*sum(x*x for x in sums)-3*b*(k+1)
assert Q==Fraction(7,2)
C=1-Fraction(2**3-2,6**3-6)
assert C==Fraction(34,35)
Cf=1-Fraction(2**3-2,b*k*(k*k-1))
assert Cf==Fraction(15,16)
print(f"PASS Kruskal–Wallis H={float(H):.6f}, df=2, rank total={sum(R)}")
print(f"PASS Friedman Q={float(Q):.6f}, df=2, treatment rank sums={sums}")
print(f"PASS K-W tie factor={C}; Friedman tie factor={Cf}")
