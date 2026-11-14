#!/usr/bin/env python3
"""Independent distribution-moment anchors for Probability T5."""
import math
n,p,lam,r=12,.3,4.0,3; q=1-p
assert math.isclose(n*p,3.6,abs_tol=1e-12)
assert math.isclose(n*p*q,2.52,abs_tol=1e-12)
assert math.isclose(q/p**2,.7/.09,abs_tol=1e-12)
assert math.isclose(r*q/p,7.0,abs_tol=1e-12)
assert math.isclose(r*q/p**2,70/3,abs_tol=1e-12)
N,K,draws=20,6,5; ph=K/N
assert math.isclose(draws*ph*(1-ph)*(N-draws)/(N-1),5*.3*.7*15/19,abs_tol=1e-12)
assert math.isclose(1*q/p,q/p,abs_tol=1e-12)
print("Probability T5 distribution-moment anchors: PASS")
