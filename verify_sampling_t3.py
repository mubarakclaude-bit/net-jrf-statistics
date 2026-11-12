#!/usr/bin/env python3
"""Independent exact arithmetic checks for ratio and regression estimation."""
from fractions import Fraction as F

# Main worked example: xbar=10, ybar=12, Xbar=15, b=1.2.
xbar, ybar, Xbar, b = F(10), F(12), F(15), F(6, 5)
ratio_factor = Xbar / xbar
ratio_est = ybar * ratio_factor
reg_est = ybar + b * (Xbar - xbar)
assert ratio_factor == F(3, 2)
assert ratio_est == 18
assert reg_est == 18

# Completion example: ybar=20, xbar=5, Xbar=6, b=2.
assert F(20) * F(6, 5) == 24
assert F(20) + F(2) * (F(6) - F(5)) == 22

# Guided ratio example.
assert F(30) * F(8, 6) == 40

# Transfer regression example.
assert F(50) + F(3, 2) * (F(12) - F(10)) == 53

# Additional mastery numeric items.
assert F(18) * F(9, 6) == 27
assert F(10, 8) == F(5, 4)
assert F(12) * F(4, 3) == 16
assert F(20) + F(2) * (F(6) - F(5)) == 22

# Formula identity when Xbar equals xbar.
for mean in (F(12), F(30), F(50)):
    assert mean * (F(7) / F(7)) == mean
    assert mean + F(9, 7) * (F(7) - F(7)) == mean

print("PASS: worked ratio estimate =", ratio_est)
print("PASS: worked regression estimate =", reg_est)
print("PASS: completion, guided, transfer and mastery arithmetic")
print("PASS: both adjustments reduce to ybar when Xbar equals xbar")
