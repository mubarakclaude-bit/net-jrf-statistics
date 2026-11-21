#!/usr/bin/env python3
"""Independent numerical anchors for Probability T3; not a substitute for full lesson review."""
import math
rates=(2.0,5.0); weights=(.6,.4)
mean=sum(w*x for w,x in zip(weights,rates)); within=mean
between=sum(w*(x-mean)**2 for w,x in zip(weights,rates))
assert math.isclose(mean,3.2,abs_tol=1e-12)
assert math.isclose(within,3.2,abs_tol=1e-12)
assert math.isclose(between,2.16,abs_tol=1e-12)
assert math.isclose(within+between,5.36,abs_tol=1e-12)
n,a,b=10,2,3
assert math.isclose(n*a/(a+b),4,abs_tol=1e-12)
assert math.isclose(n*a*b*(a+b+n)/((a+b)**2*(a+b+1)),6,abs_tol=1e-12)
lam=2.0
assert math.isclose(1/lam+1/lam**2,(lam+1)/lam**2,abs_tol=1e-12)
print("Probability T3 independent anchors: PASS")
