#!/usr/bin/env python3
"""Exhaustive checks for the June 2026 Spearman/Kendall anchor and lesson examples."""
from itertools import permutations
from math import factorial, sqrt

crude = [77.91, 82.00, 89.20, 73.37, 66.42, 80.10, 69.78, 72.09, 92.14, 96.31]
gas = [65.46, 64.18, 65.66, 59.23, 65.68, 69.55, 67.81, 67.39, 82.06, 84.40]
rx = [5, 7, 8, 4, 1, 6, 2, 3, 9, 10]
ry = [3, 2, 4, 1, 5, 8, 7, 6, 9, 10]
d = [a - b for a, b in zip(rx, ry)]
assert d == [2, 5, 4, 3, -4, -2, -5, -3, 0, 0]
assert sum(d) == 0 and sum(x*x for x in d) == 108
rho = 1 - 6 * sum(x*x for x in d) / (10 * (10*10 - 1))
assert round(rho, 6) == 0.345455

concordant = discordant = 0
for i in range(10):
    for j in range(i + 1, 10):
        s = (rx[i] - rx[j]) * (ry[i] - ry[j])
        concordant += s > 0
        discordant += s < 0
assert (concordant, discordant) == (29, 16)
assert round((concordant - discordant) / 45, 6) == 0.288889

def corr(a, b):
    ma, mb = sum(a)/len(a), sum(b)/len(b)
    num = sum((x-ma)*(y-mb) for x, y in zip(a, b))
    den = sqrt(sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b))
    return num / den
assert round(corr(crude, gas), 6) == 0.716682

def exact_lower_tail(n, observed):
    total = 0
    for p in permutations(range(1, n+1)):
        s = sum((i+1-p[i])**2 for i in range(n))
        total += s <= observed
    return total, factorial(n)

assert exact_lower_tail(5, 4) == (8, 120)
assert exact_lower_tail(6, 0) == (1, 720)
assert exact_lower_tail(7, 20) == (350, 5040)
assert exact_lower_tail(10, 108) == (599491, 3628800)
assert [n*(n*n-1)//3 for n in (5, 6, 10)] == [40, 70, 330]
print("PASS Spearman rho, Kendall tau, raw Pearson r, exact permutation tails and rank-difference bounds")
