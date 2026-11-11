#!/usr/bin/env python3
"""Independent exact arithmetic checks for the stratified sampling lesson."""
from fractions import Fraction as F

# Worked example: proportional allocation, N1=100, N2=200, n=30.
N1, N2, n = 100, 200, 30
N = N1 + N2
W1, W2 = F(N1, N), F(N2, N)
n1, n2 = n * W1, n * W2
assert (W1, W2) == (F(1, 3), F(2, 3))
assert (n1, n2) == (10, 20)
f1, f2 = n1 / N1, n2 / N2
assert (f1, f2) == (F(1, 10), F(1, 10))

S1_sq, S2_sq = F(16), F(36)
v1 = W1**2 * (1 - f1) * S1_sq / n1
v2 = W2**2 * (1 - f2) * S2_sq / n2
v = v1 + v2
assert (v1, v2, v) == (F(4, 25), F(18, 25), F(22, 25))
assert float(v) == 0.88

# Neyman allocation with equal unit costs.
a1, a2 = N1 * 4, N2 * 6
ney1 = F(n) * a1 / (a1 + a2)
ney2 = F(n) * a2 / (a1 + a2)
assert (ney1, ney2) == (F(15, 2), F(45, 2))

# Cost-adjusted allocation transfer: N_h*S_h/sqrt(c_h).
# Here weights are 600/sqrt(1) and 1200/sqrt(4).
cost_weight_1 = F(600, 1)
cost_weight_2 = F(1200, 2)
assert cost_weight_1 == cost_weight_2 == 600

# A separate numeric mastery item: proportional n1 for N1=80,N2=120,n=40.
assert F(40 * 80, 200) == 16
# Another mastery item: Neyman n1 for weights 300 and 900, n=24.
assert F(24 * 300, 1200) == 6

print("PASS: proportional allocation =", n1, n2)
print("PASS: variance components =", v1, v2, "total =", v)
print("PASS: Neyman allocation =", ney1, ney2)
print("PASS: cost-adjusted transfer weights =", cost_weight_1, cost_weight_2)
print("PASS: independent mastery arithmetic checks")
