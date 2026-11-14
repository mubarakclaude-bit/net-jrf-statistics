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
# Chebyshev: symmetric {-1,+1} variable has variance 1; P(|X| >= 2)=0 <= 1/4.
values=(-1.0,1.0); probs=(.5,.5)
mu=sum(v*p for v,p in zip(values,probs))
variance=sum(p*(v-mu)**2 for v,p in zip(values,probs))
event=sum(p for v,p in zip(values,probs) if abs(v-mu)>=2)
assert math.isclose(variance,1.0,abs_tol=1e-12)
assert event <= variance/4
# Cantelli bound at one standard deviation is 1/2.
k=1.0
assert math.isclose(1/(1+k*k),.5,abs_tol=1e-12)
print("Probability T7 inequality anchors: PASS")
