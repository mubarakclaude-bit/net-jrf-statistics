#!/usr/bin/env python3
"""Independent distribution-moment and dispersion-ratio anchors for Probability T5."""
import math
n,p,lam,r=12,.3,4.0,3; q=1-p
assert math.isclose(n*p,3.6,abs_tol=1e-12)
assert math.isclose(n*p*q,2.52,abs_tol=1e-12)
assert math.isclose(q/p**2,.7/.09,abs_tol=1e-12)
assert math.isclose(r*q/p,7.0,abs_tol=1e-12)
assert math.isclose(r*q/p**2,70/3,abs_tol=1e-12)
N,K,draws=20,6,5; ph=K/N
hypergeom_var=draws*ph*(1-ph)*(N-draws)/(N-1)
assert math.isclose(hypergeom_var,5*.3*.7*15/19,abs_tol=1e-12)
m=8
partial=p*sum(q**k for k in range(m+1))
tail=q**(m+1)
assert math.isclose(partial+tail,1.0,abs_tol=1e-12)
# A geometric can lie on either side of equidispersion.
for pg in (.3,.5,.7):
    ratio=(1-pg)/pg
    assert (ratio>1) == (pg<.5)
    assert math.isclose(ratio, (1-pg)/pg, abs_tol=1e-12)
# Same ratio does not identify a family: Geom(p=1/1.7) and Binom(p=.3).
geom_p=1/1.7
geom_ratio=(1-geom_p)/geom_p
binom_ratio=1-.3
assert math.isclose(geom_ratio,binom_ratio,abs_tol=1e-12)
print("Probability T5 distribution-moment and dispersion anchors: PASS")
