#!/usr/bin/env python3
from fractions import Fraction as F
N1,N2,n=100,200,30
N=N1+N2
W1,W2=F(N1,N),F(N2,N)
n1,n2=n*W1,n*W2
assert (W1,W2,n1,n2)==(F(1,3),F(2,3),10,20)
f1,f2=n1/N1,n2/N2
v1=W1**2*(1-f1)*F(16)/n1
v2=W2**2*(1-f2)*F(36)/n2
assert (v1,v2,v1+v2)==(F(4,25),F(18,25),F(22,25))
a1,a2=100*4,200*6
assert (F(30*a1,a1+a2),F(30*a2,a1+a2))==(F(15,2),F(45,2))
assert F(600,1)==F(1200,2)
assert F(40*80,200)==16
assert F(24*300,1200)==6
print("PASS proportional allocation, variance, Neyman and cost-adjusted checks")
