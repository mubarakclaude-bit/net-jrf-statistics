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

# Population rank correlations are not the finite-sample expectation of Spearman's r_s.
from math import asin, pi, isclose
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
lesson = json.loads((ROOT / "seed/lesson_np4.json").read_text(encoding="utf-8"))
pool = json.loads((ROOT / "seed/nonparam_t4_mastery.json").read_text(encoding="utf-8"))

# Spearman's no-tie formula: n=6, sum(d^2)=35 gives zero; 70 gives -1.
rho_zero = 1 - 6*35/(6*(6**2-1))
rho_reverse = 1 - 6*70/(6*(6**2-1))
assert rho_zero == 0 and rho_reverse == -1

# Exact null variances: equal at n=2, Kendall strictly smaller only for n>2.
def var_spearman(n):
    return 1/(n-1)

def var_kendall(n):
    return 2*(2*n+5)/(9*n*(n-1))

assert var_spearman(2) == var_kendall(2) == 1
assert var_kendall(3) < var_spearman(3)
assert var_kendall(10) < var_spearman(10)

# Bivariate-normal population coefficients vs the finite-sample E(r_s).
r, n = 0.5, 10
rho_population = 6/pi*asin(r/2)
tau_population = 2/pi*asin(r)
expected_sample_rs = 6/(pi*(n+1))*(asin(r)+(n-2)*asin(r/2))
assert isclose(rho_population, 0.4825837395309974, rel_tol=0, abs_tol=1e-12)
assert isclose(tau_population, 1/3, rel_tol=0, abs_tol=1e-12)
assert isclose(expected_sample_rs, 0.4418790832952709, rel_tol=0, abs_tol=1e-12)
assert not isclose(expected_sample_rs, rho_population, rel_tol=0, abs_tol=1e-6)

s7 = next(s for s in lesson["scenes"] if s["id"] == "s7")
normal = next(b for b in s7["blocks"] if b["h"] == "Under bivariate normality")
variance = next(b for b in s7["blocks"] if b["h"] == "Null variances")
assert "E(r_s)" in normal["body"] and "ρ_S" in normal["body"]
assert "equal (both 1)" in variance["body"] and "n>2" in variance["body"]

pool10 = next(q for q in pool["items"] if q["id"] == "np-t4-m-10")
assert "Σd² = 35" in pool10["stem"] and pool10["answer"] == "C"
pool14 = next(q for q in pool["items"] if q["id"] == "np-t4-m-14")
pool20 = next(q for q in pool["items"] if q["id"] == "np-t4-m-20")
assert "At n=2 both null variances equal 1" in pool14["check"]
assert "equal at n=2" in pool20["explanation"]
print("PASS: variance edge case and population/sample Spearman distinction")
