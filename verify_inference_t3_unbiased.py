#!/usr/bin/env python3
"""Verification for the inference-t3 revision (lesson v1.4): two gaps found by the source-intake trial.

  1. Unbiased estimators are never unique: a*T1 + (1-a)*T2 is unbiased for every real a,
     and the variance is what picks one. Numbers used in scene s3 and recall s5.
  2. An unbiased estimator of sigma for a normal sample: E(s) = c_n * sigma with
     c_n = sqrt(2/(n-1)) * Gamma(n/2) / Gamma((n-1)/2), so s / c_n is unbiased for sigma.
     Numbers used in worked scene s7b, the revision sheet, and pool item inf-t3-m-14.

c_n is checked three ways: the Gamma formula, numerical integration of E(sqrt(W)) for
W ~ chi-square(n-1), and simulation of normal samples.

Run from the repository root:  python verify_inference_t3_unbiased.py
"""
import math

import numpy as np
from scipy import integrate, stats


def close(a, b, tol=1e-12, what=""):
    assert abs(a - b) <= tol * max(1.0, abs(a), abs(b)), (what, a, b)


def c(n):
    """E(s)/sigma for a normal sample of size n."""
    return math.sqrt(2.0 / (n - 1)) * math.exp(math.lgamma(n / 2) - math.lgamma((n - 1) / 2))


# ---------------------------------------------------------------- 1. non-uniqueness (scene s3, recall s5)
# Two observations X1, X2, independent, mean mu, variance sigma^2.
# E[a X1 + (1-a) X2] = a mu + (1-a) mu = mu for every a.
# Var[a X1 + (1-a) X2] = sigma^2 * (a^2 + (1-a)^2).
def var_factor(a):
    return a * a + (1 - a) ** 2

for a in (-2.0, 0.0, 0.25, 0.5, 1.0, 3.0):
    close(a * 1.0 + (1 - a) * 1.0, 1.0, what="weights sum to one")     # mean factor
close(var_factor(1.0), 1.0, what="a=1: X1 alone")
close(var_factor(0.5), 0.5, what="a=1/2: the sample mean")
close(var_factor(3.0), 13.0, what="a=3: 3X1 - 2X2")
# derivative 2a - 2(1-a) = 4a - 2 vanishes at a = 1/2; second derivative 4 > 0
close(4 * 0.5 - 2, 0.0, what="stationary point")
grid = np.linspace(-5, 5, 100001)
a_min = grid[np.argmin(grid ** 2 + (1 - grid) ** 2)]
close(a_min, 0.5, tol=1e-9, what="grid minimiser")

rng = np.random.default_rng(20261121)
mu, sigma = 10.0, 2.0
X = rng.normal(mu, sigma, size=(2_000_000, 2))
T3 = 3 * X[:, 0] - 2 * X[:, 1]
se = sigma * math.sqrt(13) / math.sqrt(len(T3))
assert abs(T3.mean() - mu) < 4 * se, ("3X1-2X2 unbiased by simulation", T3.mean())
assert abs(T3.var() / sigma ** 2 - 13) < 0.05, ("3X1-2X2 variance factor", T3.var() / sigma ** 2)
print("1. non-uniqueness: Var factor a=1 -> 1, a=1/2 -> 0.5, a=3 -> 13; minimum at a = 1/2.  "
      f"sim mean of 3X1-2X2 = {T3.mean():.4f} (mu = {mu})")

# ---------------------------------------------------------------- 2. c_n and the unbiased estimator of sigma
# (a) closed form at n = 5: Gamma(5/2) = (3/4) sqrt(pi), Gamma(2) = 1,
#     c_5 = sqrt(2/4) * (3/4) sqrt(pi) = 3 sqrt(2 pi) / 8
close(math.gamma(2.5), 0.75 * math.sqrt(math.pi), what="Gamma(5/2)")
close(math.gamma(2.0), 1.0, what="Gamma(2)")
c5 = c(5)
close(c5, 3 * math.sqrt(2 * math.pi) / 8, what="c_5 closed form")
close(c5, math.sqrt(0.5) * 0.75 * math.sqrt(math.pi), what="c_5 step by step")
print(f"2a. c_5 = 3*sqrt(2*pi)/8 = {c5:.6f}   1/c_5 = {1 / c5:.6f}   "
      f"(1/c_5 - 1) = {100 * (1 / c5 - 1):.2f}%")

# (b) E(sqrt(W)) for W ~ chi-square(k) by integration, and the Gamma identity
#     E(W^(1/2)) = sqrt(2) Gamma((k+1)/2) / Gamma(k/2).  With k = n-1, E(s) = sigma * E(sqrt W) / sqrt(n-1).
for n in (2, 3, 5, 10, 30):
    k = n - 1
    num, _ = integrate.quad(lambda w: math.sqrt(w) * stats.chi2.pdf(w, k), 0, np.inf)
    formula = math.sqrt(2) * math.exp(math.lgamma((k + 1) / 2) - math.lgamma(k / 2))
    close(num, formula, tol=1e-8, what=f"E sqrt(chi2_{k})")
    close(num / math.sqrt(k), c(n), tol=1e-8, what=f"c_{n} by integration")
k = 4
EsqrtW = math.sqrt(2) * math.gamma(2.5) / math.gamma(2)
close(EsqrtW, 3 * math.sqrt(2 * math.pi) / 4, what="E sqrt(chi2_4)")
close(EsqrtW / 2, c5, what="c_5 = E sqrt(chi2_4) / sqrt(4)")
print(f"2b. E sqrt(chi2_4) = 3*sqrt(2*pi)/4 = {EsqrtW:.6f};  /sqrt(4) = {EsqrtW / 2:.6f} = c_5")

# small table for the lesson: c_n rises to 1
table = {n: c(n) for n in (2, 5, 10, 30)}
close(table[2], math.sqrt(2 / math.pi), what="c_2 = sqrt(2/pi)")
assert table[2] < table[5] < table[10] < table[30] < 1
print("    c_n: " + ", ".join(f"n={n}: {v:.4f}" for n, v in table.items()))

# (c) simulation: n = 5 normal samples, both parameters unknown
mu, sigma, n, R = 50.0, 3.0, 5, 2_000_000
S = rng.normal(mu, sigma, size=(R, n)).std(axis=1, ddof=1)
mean_s = S.mean()
se_s = S.std() / math.sqrt(R)
assert abs(mean_s - c5 * sigma) < 4 * se_s, ("E(s) by simulation", mean_s, c5 * sigma)
assert abs((S / c5).mean() - sigma) < 4 * se_s / c5, ("s/c_5 unbiased by simulation", (S / c5).mean())
assert mean_s < sigma - 20 * se_s, "s is biased low, and visibly so at this R"
assert abs((S ** 2).mean() - sigma ** 2) < 0.02 * sigma ** 2, "s^2 unbiased for sigma^2"
# the figures quoted in scene s7b, step 8 (rounded far coarser than the standard error 0.0007)
assert (f"{mean_s:.2f}", f"{c5 * sigma:.3f}", f"{(S / c5).mean():.2f}") == ("2.82", "2.820", "3.00")
assert (f"{c(2):.3f}", f"{c(10):.3f}", f"{c(30):.3f}") == ("0.798", "0.973", "0.991")
print(f"2c. simulation, n=5, sigma={sigma}, R={R:,}: mean s = {mean_s:.5f} "
      f"(c_5*sigma = {c5 * sigma:.5f}, se {se_s:.5f});  mean s/c_5 = {(S / c5).mean():.5f}")
# Var(s) = sigma^2 - (E s)^2 = sigma^2 (1 - c_5^2) > 0 is why E(s) < sigma
close(1 - c5 ** 2, 1 - 9 * math.pi / 32, what="1 - c_5^2")
assert abs(S.var() / sigma ** 2 - (1 - c5 ** 2)) < 0.005
print(f"    Var(s)/sigma^2 = 1 - c_5^2 = {1 - c5 ** 2:.5f} (sim {S.var() / sigma ** 2:.5f})")

# ---------------------------------------------------------------- 3. worked example (scene s7b)
data = [23, 19, 18, 21, 19]
n = len(data)
xbar = sum(data) / n
dev = [x - xbar for x in data]
ss = sum(d * d for d in dev)
s2 = ss / (n - 1)
s = math.sqrt(s2)
assert n == 5 and xbar == 20 and dev == [3, -1, -2, 1, -1] and ss == 16 and s2 == 4 and s == 2
sigma_hat = s / c5
close(sigma_hat, 16 / (3 * math.sqrt(2 * math.pi)), what="2/c_5 closed form")
print(f"3. data {data}: mean {xbar:g}, deviations {dev}, SS {ss:g}, s^2 {s2:g}, s {s:g}, "
      f"s/c_5 = {sigma_hat:.4f}")
assert f"{c5:.4f}" == "0.9400" and f"{sigma_hat:.3f}" == "2.128" and f"{1 / c5:.4f}" == "1.0638"

# ---------------------------------------------------------------- 4. pool item inf-t3-m-14
s_obs = 3.0
umvue = s_obs / c5                   # option B
naive = s_obs                        # option A: s itself
times = s_obs * c5                   # option C: multiplied instead of divided
mle = s_obs * math.sqrt((n - 1) / n) # option D: square root of the MLE of sigma^2
opts = {"A": f"{naive:.2f}", "B": f"{umvue:.2f}", "C": f"{times:.2f}", "D": f"{mle:.2f}"}
assert opts == {"A": "3.00", "B": "3.19", "C": "2.82", "D": "2.68"}, opts
assert len(set(opts.values())) == 4
assert umvue > naive > times and naive > mle   # the check line: the answer must exceed s
print(f"4. pool m-14: s = 3, n = 5 -> s/c_5 = {umvue:.4f}; options {opts}, key B")

print("ALL CHECKS PASS")
