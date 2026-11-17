#!/usr/bin/env python3
"""Independent sampling-distribution and correlation anchors for Probability T13."""
import math
assert math.isclose(1/math.pi,.3183098861837907,rel_tol=1e-12)
assert math.isclose(.5,1/2,abs_tol=1e-12)
assert math.isclose(2/math.pi,.6366197723675814,rel_tol=1e-12)
n,r=12,.6
t=r*math.sqrt(n-2)/math.sqrt(1-r*r)
assert math.isclose(t,2.3717082451262845,rel_tol=1e-12)
tcrit=2.2281388519649385
rcrit=tcrit/math.sqrt(n-2+tcrit*tcrit)
assert math.isclose(rcrit,.576,abs_tol=5e-4)
z=.5*math.log((1+r)/(1-r)); se=1/math.sqrt(n-3)
lo=math.tanh(z-1.96*se); hi=math.tanh(z+1.96*se)
assert math.isclose(z,math.log(4)/2,abs_tol=1e-12)
assert math.isclose(lo,.0398,abs_tol=5e-4)
assert math.isclose(hi,.8732,abs_tol=5e-4)
print("Probability T13 sampling-distribution anchors: PASS")
