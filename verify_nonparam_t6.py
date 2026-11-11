#!/usr/bin/env python3
"""Independent numeric checks for KS and runs-test examples."""
from fractions import Fraction
f0=[Fraction(10,100),Fraction(35,100),Fraction(55,100),Fraction(75,100),Fraction(95,100)]
fn=[Fraction(i,5) for i in range(1,6)]
left=[Fraction(i-1,5) for i in range(1,6)]
dplus=max(a-b for a,b in zip(fn,f0)); dminus=max(a-b for a,b in zip(f0,left)); D=max(dplus,dminus)
assert (dplus,dminus,D)==(Fraction(1,10),Fraction(15,100),Fraction(15,100))
n1,n2=6,4; N=n1+n2; ER=1+2*n1*n2/N
VR=Fraction(2*n1*n2*(2*n1*n2-N),N*N*(N-1))
assert ER==5.8 and VR==Fraction(152,75)
assert max([0.10,0.05,0.15,0.02])==0.15
print(f"PASS one-sample KS D={float(D):.2f}; runs E(R)={ER:.1f}, Var(R)={float(VR):.4f}")
