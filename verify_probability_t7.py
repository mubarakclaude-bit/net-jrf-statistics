#!/usr/bin/env python3
"""Independent inequality anchors for Probability T7."""
import math
x=(1.0,3.0); w=(.5,.5)
lhs=sum(wi/xi for wi,xi in zip(w,x)); rhs=1/sum(wi*xi for wi,xi in zip(w,x))
assert lhs >= rhs and math.isclose(lhs,2/3,abs_tol=1e-12)
a,p=5.0,.2
assert math.isclose(p,(p*a)/a,abs_tol=1e-12)
k=2.0
assert math.isclose(1/(1+k*k),.2,abs_tol=1e-12)
assert abs((1*1+(-1)*(-1))/2) <= 1.0
print("Probability T7 inequality anchors: PASS")
