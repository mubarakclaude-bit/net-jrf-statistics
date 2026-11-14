#!/usr/bin/env python3
"""Independent Jacobian/transformation anchors for Probability T10."""
import math
lam,s=1.7,2.0
joint=lam**2*math.exp(-lam*s); sum_density=lam**2*s*math.exp(-lam*s)
assert math.isclose(joint/sum_density,1/s,rel_tol=1e-12)
# For X|X+Y=s with iid exponentials, X is Uniform(0,s).
conditional_mean=s/2
conditional_variance=s**2/12
assert math.isclose(conditional_mean,1.0,abs_tol=1e-12)
assert math.isclose(conditional_variance,1/3,abs_tol=1e-12)
# (u,v) -> (x=u,y=v-u), determinant has absolute value one.
assert abs(1*(-1)-0*1)==1
print("Probability T10 transformation anchors: PASS")
