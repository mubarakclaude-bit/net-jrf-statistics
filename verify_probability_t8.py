#!/usr/bin/env python3
"""Independent probability identities for Probability T8."""
import math
pA,pB,pAB=.4,.5,.2
assert math.isclose(pA+pB-pAB,.7,abs_tol=1e-12)
assert math.isclose(.3*.6,.18,abs_tol=1e-12)
p1,p2,p3=.2,.3,.4; p12,p13,p23=.06,.08,.12; p123=.024
assert math.isclose(p1+p2+p3-p12-p13-p23+p123,.664,abs_tol=1e-12)
assert math.isclose(1-(.2+.3),.5,abs_tol=1e-12)
print("Probability T8 identity anchors: PASS")
