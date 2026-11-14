#!/usr/bin/env python3
"""Independent inequality anchors for Probability T7."""
import math
x=(1.0,3.0); w=(.5,.5)
lhs=sum(wi/xi for wi,xi in zip(w,x)); rhs=1/sum(wi*xi for wi,xi in zip(w,x))
assert lhs >= rhs and math.isclose(lhs,2/3,abs_tol=1e-12)
# Markov equality: X is 25 with probability .2 and 0 otherwise.
a,prob=25.0,.2
expectation=prob*a
assert math.isclose(expectation,5.0,abs_tol=1e-12)
assert math.isclose(prob,expectation/a,abs_tol=1e-12)
# Chebyshev's extremal three-point law is a probability distribution for k >= 1.
for k in (1.0,2.0,3.0):
    edge=1/(2*k*k)
    centre=1-2*edge
    mean=(-k)*edge+k*edge
    variance=edge*k*k+edge*k*k
    tail=2*edge
    assert centre>=0
    assert math.isclose(mean,0.0,abs_tol=1e-12)
    assert math.isclose(variance,1.0,abs_tol=1e-12)
    assert math.isclose(tail,1/(k*k),abs_tol=1e-12)
# For k < 1 the formal central mass is negative: the bound is vacuous, not sharp.
k=.5
assert 1/(k*k)>1 and 1-1/(k*k)<0
# Cantelli bound at one standard deviation is 1/2.
assert math.isclose(1/(1+1**2),.5,abs_tol=1e-12)
print("Probability T7 inequality anchors: PASS")
