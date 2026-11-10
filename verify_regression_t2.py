#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent exact-arithmetic checks for regression-t2. Run: python verify_regression_t2.py."""
from fractions import Fraction as F

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    BT = transpose(B)
    return [[dot(row, col) for col in BT] for row in A]

def check(name, condition, value=None):
    assert condition, "FAILED: " + name
    print("ok", name, "" if value is None else value)

X = [[F(1),F(1)],[F(2),F(0)],[F(1),F(-1)]]
Xt = transpose(X)
G = matmul(Xt, X)
check("Q11 X'X = diag(6,2)", G == [[F(6),F(0)],[F(0),F(2)]], G)
Ginv = [[F(1,6),F(0)],[F(0),F(1,2)]]
W = matmul(Ginv, Xt)
check("beta1 weights = (1,2,1)/6", W[0] == [F(1,6),F(1,3),F(1,6)], W[0])
check("beta2 weights = (1,0,-1)/2", W[1] == [F(1,2),F(0),F(-1,2)], W[1])
check("W X = I", matmul(W, X) == [[F(1),F(0)],[F(0),F(1)]], matmul(W,X))
check("covariance multiplier = diag(1/6,1/2)", Ginv == [[F(1,6),F(0)],[F(0),F(1,2)]])
y = [F(7),F(4),F(3)]
bhat = [dot(row,y) for row in W]
check("worked beta1 = 3", bhat[0] == 3, bhat[0])
check("worked beta2 = 2", bhat[1] == 2, bhat[1])

options = {
 "A": [[F(1,2),F(1),F(1,2)],[F(1,6),F(0),F(-1,6)]],
 "B": W,
 "C": [[F(1,2),F(1),F(1,2)],[F(1,6),F(0),F(1,6)]],
 "D": [[F(6),F(6),F(6)],[F(2),F(0),F(-2)]]
}
unbiased = {k: matmul(v,X) == [[F(1),F(0)],[F(0),F(1)]] for k,v in options.items()}
check("only Q11 option B is unbiased for both coefficients",
      [k for k,v in unbiased.items() if v] == ["B"], unbiased)

X2 = [[F(1)],[F(2)]]
W2 = matmul([[F(1,5)]], transpose(X2))
check("two-observation BLUE weights = (1/5,2/5)", W2 == [[F(1,5),F(2,5)]], W2)
check("variance y2/2 exceeds BLUE variance", F(1,4) > F(1,5), "1/4 > 1/5")

a = [F(1,6),F(1,3),F(1,6)]
z = [F(1),F(-1),F(1)]
check("null-space direction satisfies X'z=0", [dot(row,z) for row in Xt] == [F(0),F(0)])
check("OLS weights orthogonal to null-space direction", dot(a,z) == 0)
for t in [F(-2),F(-1),F(0),F(1),F(2)]:
    c = [ai+t*zi for ai,zi in zip(a,z)]
    check("variance difference equals t^2 for t=%s" % t, dot(c,c)-dot(a,a) == t*t)

Xa = [[F(1),F(1),F(0)],[F(1),F(0),F(1)]]
r1,r2 = Xa
check("tau1-tau2 is row1 minus row2",
      [r1[i]-r2[i] for i in range(3)] == [F(0),F(1),F(-1)])
check("alpha+tau1 is a design row", [F(1),F(1),F(0)] == r1)
# If a(1,1,0)+b(1,0,1)=(0,1,0), the first two coordinates force
# a=1 and b=-1, making the third coordinate -1 rather than 0.
check("tau1 alone is not in the row space", F(-1) != F(0))

rho = F(99,100)
vif = 1/(1-rho*rho)
check("VIF at r=.99 is 50.251256...", abs(float(vif)-50.2512562814) < 1e-9, float(vif))
print("All regression-t2 verification checks passed.")
