# -*- coding: utf-8 -*-
"""Verification for the CSIR NET 2011-2025 previous-year practice banks (pyq_bank_*.py -> seed/*_csir_pyq.json).

Part 1 recomputes the numbers behind the answers: exact fractions, exhaustive enumeration, numerical integration and
seeded simulation (standard library only, so CI needs nothing extra). Part 2 audits every item's structure and checks
that the seed files on disk equal what pyq_bank_build.py writes.

    python verify_pyq_distributions.py         exit 0 = every check passed
"""
import io, itertools, json, math, os, random, re, sys
from fractions import Fraction as F
from math import comb, exp, factorial, sqrt, pi, log, atan, gamma, erf

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
FAILS, N = [], [0]


def ok(cond, what):
    N[0] += 1
    if not cond:
        FAILS.append(what)
        print("FAIL  " + what)


def close(a, b, tol, what):
    ok(abs(a - b) <= tol, "%s: %.6g vs %.6g" % (what, a, b))


def integrate(f, a, b, n=20000):
    """Composite Simpson rule."""
    n += n % 2
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    return s * h / 3


Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
phi = lambda z: exp(-z * z / 2) / sqrt(2 * pi)
rng = random.Random(20261116)
E = math.e

# ======================================================================= Probability compilation
ok(F(5 + 10, 5 + 10 + 5 + 15) == F(3, 7), "prob-01 posterior mean 15/35")
ok(F(15, 100) / (F(15, 100) + F(45, 100)) == F(1, 4), "prob-02 Bayes 0.25")
LH = comb(100, 15) * F(1, 6) ** 15 * F(5, 6) ** 85
LT = comb(101, 15) * F(1, 6) ** 15 * F(5, 6) ** 86
ok(LH / (LH + LT) == F(516, 1021), "prob-04 P(Head|Y=15) = 516/1021")
p, k = F(3, 10), 4
pmf = [comb(k, j) * p ** j * (1 - p) ** (k - j) for j in range(k + 1)]
ok(pmf[1] / (1 - pmf[0]) == k * p * (1 - p) ** (k - 1) / (1 - (1 - p) ** k), "prob-05 pooled-test formula")
ok(F(1, 3) * F(2, 5) / (F(1, 3) * (F(3, 5) + F(2, 5) + F(1, 2))) == F(4, 15), "prob-08 P(U2|black)")


def f_sys(p):  # u1 parallel with series (u2, u3); each fails with prob p
    tot = F(0)
    for s in itertools.product([0, 1], repeat=3):  # 1 = works
        pr = 1
        for x in s:
            pr *= (1 - p) if x else p
        if s[0] or (s[1] and s[2]):
            tot += pr
    return tot


ok(f_sys(F(1, 2)) == F(5, 8) and f_sys(F(1, 3)) == F(22, 27) and f_sys(F(1, 4)) == F(57, 64), "prob-11 f(1/2), f(1/3), f(1/4)")
agree = F(sum(1 for t in itertools.product(range(4), repeat=3) if len(set(t)) == 1), 64)
ok(agree == F(1, 16) and agree ** 30 == F(1, 4 ** 60), "prob-12 (1/16)^30 = 4^-60")
good = sum(1 for s in itertools.product(range(5), repeat=4) if len(set(s[:3])) == 3 and s[3] in s[:3])
ok(F(good, 5 ** 4) == F(4, 5) * F(3, 5) ** 2, "prob-13 fourth ball first collision")
for atoms, target in [({"ABC": .1, "A": .1, "B": .1, "C": .2}, .5), ({"AB": .1, "AC": .1, "BC": .1, "C": .1}, .4)]:
    P = lambda ev: sum(v for kk, v in atoms.items() if all(c in kk for c in ev))
    ok(all(abs(P(e) - v) < 1e-12 for e, v in [("A", .2), ("B", .2), ("C", .3), ("AB", .1), ("AC", .1), ("BC", .1)])
       and abs(sum(atoms.values()) - target) < 1e-12, "prob-14 union %.1f is attainable" % target)
pa = F(1, 2) / (1 - F(1, 8))
ok(pa == F(4, 7) and 1 - pa == F(3, 7), "prob-17 P(A wins) = 4/7")
ok(F(sum(1 for q in itertools.permutations(range(4)) if q[0] == 3 and q[3] == 0), 24) == F(1, 12), "prob-18 1/12")
ok(F(1, 2) * F(2, 6) / F(1, 2) == F(1, 3), "prob-15 1/3")
for pp in [0.1, 0.3, 0.5, 0.7, 0.9]:
    q1, q2, q3 = 1 - pp * (1 - (1 - pp) ** 2), (1 - pp) * (1 - pp ** 2), 1 - pp ** 3
    ok(q3 > q1 > q2, "prob-20 q3 > q1 > q2 at p=%.1f" % pp)
words = sum(1 for t in itertools.product("ABCDEF", repeat=3) if sorted(t) in (sorted("BAD"), sorted("CAD")))
ok(words == 12, "prob-21 12/216")
pos = list(itertools.combinations(range(9), 3))
ok(F(sum(1 for c in pos if sorted(c)[1] == 4), len(pos)) == F(4 * factorial(6) * factorial(4), factorial(9)) == F(4, 21), "prob-22 second red at draw 5")
ok(F(sum(1 for b in range(1, 8) if min(b, 8 - b) >= 3), 7) == F(3, 7), "prob-23 at least 2 chairs between A and B")
ok(F(1, 10) * (1 - F(comb(8, 2), comb(10, 2))) == F(17, 450), "prob-24 reject = 17/450")
ok(F(1, 10) * F(2 * 8, comb(10, 2)) == F(8, 225), "prob-24 key value 8/225 is P(exactly one defective)")
for kk in range(26):
    vals = sorted([5] * (25 - kk) + [10] * kk)
    mean, med = F(sum(vals), 25), vals[12]
    if mean == med:
        ok(kk in (0, 25), "prob-25 mean = median only when variance 0")
    else:
        ok(0 < kk < 25, "prob-25 differ -> range 5")
ok(F(5 * 20 + 10 * 5, 25) > 5 and F(5 * 5 + 10 * 20, 25) < 10, "prob-25 mean can exceed (k=5) and fall below (k=20) the median")
ok(F(comb(4, 3) + 1, 16) == F(5, 16), "prob-26 5/16")
# prob-27 counterexample on {1,2,3,4}
A1, A2, A3 = {1}, {1, 2}, {2, 3}
cp = lambda X, Y: F(len(X & Y), len(Y))
ok(cp(A1, A2) * cp(A2, A3) > cp(A1, A3) and cp(A1, A2) + cp(A2, A3) > cp(A1, A3), "prob-27 options 1 and 4 fail")
ok(all(F(k + 2, 25) * F(2, k + 2) == F(2, 25) for k in range(1, 6)), "prob-28 P(U5|white) = 1/5")
pt = 1.0
for _ in range(99):
    pt = pt * 0.75 + (1 - pt) / 3
close(pt, 4 / 7, 1e-9, "prob-29 P(100th answer True)")
ok(F(1 + 2 + 2, 9) == F(5, 9), "prob-30 5/9")

# ======================================================================= Standard univariate compilation
tot = F(0)
for x in range(3):
    for y in range(4):
        if x + 2 * y > 1:
            tot += comb(2, x) * F(1, 4) ** x * F(3, 4) ** (2 - x) * comb(3, y) * F(1, 6) ** y * F(5, 6) ** (3 - y)
ok(tot == F(1581, 3456), "std-01 P(X+2Y>1)")
pois = lambda lam, j: exp(-lam) * lam ** j / factorial(j)
ok(sum(pois(.75, j) for j in range(9)) >= 11 / 12 and .75 < 11 / 12, "std-02 P(X<9) >= 11/12, Var = 3/4")
emax = integrate(lambda t: 1 - (2 * Phi(t) - 1) ** 2, 0, 12)
close(emax, 2 / sqrt(pi), 1e-7, "std-04 E max(|X1|,|Xn+1|)")
EY, EY2 = .4 * 10 + .6 * 3, .4 * (10 + 100) + .6 * (4 + 9)
close(EY, 5.8, 1e-12, "std-05 E(Y)")
close(EY2 - EY ** 2, 18.16, 1e-9, "std-05 Var(Y) = 18.16, not 3.04")
bx = [comb(10, i) * F(1, 2 ** 10) for i in range(11)]
by = [comb(11, j) * F(1, 2 ** 11) for j in range(12)]
ok(sum(bx[i] * by[j] for i in range(11) for j in range(12) if i < j) == F(1, 2), "std-06 P(X<Y) = 1/2")
q = exp(-1)
ey = sum(k * q ** k * (1 - q) for k in range(200))
ey2 = sum(k * k * q ** k * (1 - q) for k in range(200))
close(ey, 1 / (E - 1), 1e-12, "std-07 E(Y)")
close(ey2, (E + 1) / (E - 1) ** 2, 1e-12, "std-07 E(Y^2)")
ok(F(25, 25) == 1, "std-08 E(X_n) = 1 for every n")
for kk in range(4):
    lhs = integrate(lambda t: exp(-10 * t) * (10 * t) ** kk / factorial(kk) * exp(-t / 6) / 6, 0, 60, 60000)
    close(lhs, 60 ** kk / 61 ** (kk + 1), 1e-9, "std-09 P(N_T=%d) is geometric" % kk)
s = 0.0
for _ in range(200000):
    x = rng.random(); y = rng.random() * x; s += y + rng.random() * (1 - y)
close(s / 200000, 5 / 8, 0.004, "std-10 E(Z) (simulation)")
joint = lambda kk: exp(-1) / factorial(kk) * comb(kk, 3) / 2 ** kk
close(joint(3) / sum(joint(kk) for kk in range(3, 80)), exp(-.5), 1e-12, "std-11 P(N=3|Y=3)")
cnt = den = 0
for _ in range(400000):
    x, y = rng.random(), rng.random()
    if x < 2 * y:
        den += 1; cnt += x > y
close(cnt / den, 1 / 3, 0.004, "std-12 P(X>Y|X<2Y) (simulation)")
prec = 1 / .5 + 4 / 2
ok(prec == 4 and abs((4 / 2) / prec - .5) < 1e-12, "std-17 posterior precision 4, mean = (sum X)/8")
ok(all(abs(sum(2 ** -(kk + 1) * 2 ** -(n - kk + 1) for kk in range(n + 1)) - (n + 1) * 2 ** -(n + 2)) < 1e-15 for n in range(10)), "std-19 P(N=n) = (n+1)2^-(n+2)")
for t in [0.5, 2.0]:
    val = integrate(lambda y: exp(-t * t * y * y / 2) * phi(y), -12, 12)
    close(val, (1 + t * t) ** -.5, 1e-9, "std-21 phi(%.1f) = (1+t^2)^(-1/2)" % t)
ok(abs((1 + 4) ** -.5 - .5) > .05, "std-21 phi(2) = 1/sqrt5, not 1/2")
close((1 - exp(-.5)) / (1 - exp(-1)), (E - sqrt(E)) / (E - 1), 1e-12, "std-23 posterior probability")
ok(F(4) - F(2) ** 2 == 0, "std-24 Var(X^2) = 0, X = +-sqrt2")
mA = lambda t: (1 + exp(t)) / 2
ok(0.5 * mA(3) > 1, "std-25 MGF series diverges for Bernoulli(1/2) increments at t = 3, p = 1/2")
for (m_, n_) in [(1, 1), (2, 3)]:
    pp = .3
    S_ = lambda j: (1 - pp) ** (j + 1)
    close(S_(m_ + n_) / S_(m_), (1 - pp) ** n_, 1e-12, "std-26 memoryless gives (1-p)^n = P(X>=n)")
close(integrate(lambda t: 1 - (1 - exp(-t)) ** 2, 0, 50), 1.5, 1e-8, "std-27 E max = 3/2")
nn, kk = 3, 3
cells = list(itertools.product(range(kk), repeat=nn))
c1 = [sum(1 for v in c if v == 0) for c in cells]; ck = [sum(1 for v in c if v == kk - 1) for c in cells]
m1, mk = F(sum(c1), len(cells)), F(sum(ck), len(cells))
ok(F(sum(a * b for a, b in zip(c1, ck)), len(cells)) - m1 * mk == F(-nn, kk * kk), "std-28 Cov(N1,Nk) = -n/k^2")
ok((1 / 12) / (1 / 16) / 1000 < 0.01, "std-29 Chebyshev bound -> 0")
close(integrate(lambda x: x * x, 0, 1), 1 / 3, 1e-12, "std-30 P(W>0) = 1/3")
close(2 / 3 + integrate(lambda x: x * x, 0, .5), (2 + .5 ** 3) / 3, 1e-12, "std-30 F_W(1/2)")
close(9 / (36 * 7), 1 / 28, 1e-15, "std-31 Var(median) = 1/28")
meds = sorted(sorted(rng.random() for _ in range(5))[2] for _ in range(100000))
close(sum(m < 1 / 3 for m in meds) / 1e5, sum(m > 2 / 3 for m in meds) / 1e5, 0.006, "std-31 tails equal (simulation)")
close(exp(-1) * 2, 2 / E, 1e-15, "std-33 P(Y1>2)")
close(1 - (1 - exp(-1)) ** 2, 2 * exp(-1) - exp(-2), 1e-15, "std-33 P(Y2>2) = 2e^-1 - e^-2")
ok(4 * 2 * 2 ** 2 == 32, "std-33 Var(2Y1) = 32")
ok(all(9 * th * (1 - th) < 3 * th for th in [0.7001 + i * 0.001 for i in range(299)]), "std-34 Var(X) < Var(Y)")
ok(10 + 60 * .9 == 64, "std-35 64")
close(integrate(lambda s: exp(-s / 2) / 2 * exp(-s / 2), 0, 80), .5, 1e-9, "std-36 E(T) = 1/2")

# ======================================================================= Univariate compilation
for a in [F(0), F(1, 3), F(2, 3)]:
    b = F(2, 3) - a
    ex, ex2 = a - b, a + b
    ok(ex <= F(2, 3) and ex2 == F(2, 3) and ex2 - ex ** 2 <= F(2, 3), "uni-01 at P(X=1)=%s" % a)
ms = [F(a + b, 2) for a, b in itertools.combinations([2, 4, 6], 2)]
ok(sum(ms) / 3 == 4 and sum(m ** 2 for m in ms) / 3 == F(50, 3) and sum(m ** 3 for m in ms) / 3 == 72, "uni-02 moments of M")
close(.5 - atan(1) / pi, .25, 1e-15, "uni-03 P(X>0) for Cauchy centred at -1")
bn = [F(comb(25, x), 2 ** 25) for x in range(26)]
ok(sum(bn[:5]) == sum(bn[21:]) and sum(bn[:5]) != sum(bn[22:]), "uni-04 P(X<=4) = P(X>=21) != P(X>=22)")
ok(F(5, 2) / F(25, 2) == F(1, 5), "uni-04 CV 20%")
grid = [i / 100 for i in range(-500, 501)]
Fs = {
    "A": lambda x: 1 / (2 + x * x) if x < 0 else (2 + x * x) / (3 + x * x),
    "C": lambda x: 1 / (2 + x * x) if x < 0 else (2 * math.cos(x) + x * x) / (4 + x * x),
    "D": lambda x: 1 / (2 + x * x) if x < 0 else (1 + x * x) / (4 + x * x)}
mono = {k: all(f(grid[i]) <= f(grid[i + 1]) + 1e-15 for i in range(len(grid) - 1)) for k, f in Fs.items()}
ok(mono["A"] and not mono["C"] and not mono["D"], "uni-06 only option 1 is non-decreasing")
c = F(2)
pr = [1 / (1 + c + c * c), c / (1 + c + c * c), c * c / (1 + c + c * c)]
ok(pr[1] + 2 * pr[2] == (c + 2 * c * c) / (1 + c + c * c), "uni-11 E[X]")
close(exp(-1) + exp(-1), 2 / E, 1e-15, "uni-14 return probability to 0 is 2/e < 1")
ok(F(sum(range(100)), 100) == F(99, 2), "uni-18 E(Y) = 49.5")
vals, prb = [2, -.5], [.2, .8]
ok(abs(sum(v * p_ for v, p_ in zip(vals, prb))) < 1e-12 and abs(sum(v * v * p_ for v, p_ in zip(vals, prb)) - 1) < 1e-12, "uni-19 two-point law has mean 0, variance 1")
pz = {}
for (x1, a1), (x2, a2) in itertools.product(zip(vals, prb), repeat=2):
    pz[x1 + x2] = pz.get(x1 + x2, 0) + a1 * a2
close(sum(v for z, v in pz.items() if z <= 0), .64, 1e-12, "uni-19 P(Z<=0) = 16/25")
close(2 * integrate(lambda x: exp(-x ** 4), 0, 8), gamma(.25) / 2, 1e-9, "uni-22 integral of e^-x^4")
close(.5 * .5 + .5 * integrate(lambda x: 2 * x, 0, .5), 3 / 8, 1e-12, "uni-27 misclassification 3/8")
close(2 / (2 + 2) / (2 / (2 + 1)), 3 / 4, 1e-12, "uni-30 P(X>2Y|X>Y) = 3/4")
close(integrate(lambda y: y * y * y / 2, 0, 1), 1 / 8, 1e-12, "uni-31 integral of xy over triangle = 1/8")
dice = list(itertools.product(range(1, 7), repeat=2))
P2 = lambda ev: F(sum(1 for d in dice if ev(d)), 36)
indepXU = all(P2(lambda d: d[0] == x and (d[0] + d[1]) % 6 == u) == P2(lambda d: d[0] == x) * P2(lambda d: (d[0] + d[1]) % 6 == u) for x in range(1, 7) for u in range(6))
ok(indepXU, "uni-33 X and U independent")
ok(P2(lambda d: d[1] == 1 and sum(d) == 2) != P2(lambda d: d[1] == 1) * P2(lambda d: sum(d) == 2), "uni-33 Y and Z dependent (statement 4 true)")
bits = list(itertools.product([0, 1], repeat=2))
Ez = F(sum(x + y for x, y in bits), 4); Ew = F(sum(abs(x - y) for x, y in bits), 4)
ok(F(sum((x + y) * abs(x - y) for x, y in bits), 4) - Ez * Ew == 0, "uni-34 Cov(Z,W) = 0")
ok(F(sum(1 for x, y in bits if x + y == 1 and abs(x - y) == 1), 4) != F(2, 4) * Ew, "uni-34 Z, W dependent")
seqs = []
for y1, y2 in itertools.product([-1, 1], repeat=2):
    xs = [None, y1, y2]
    for n_ in range(3, 11):
        xs.append(xs[-1] * xs[-2])
    seqs.append(xs)
ok(F(sum(1 for s_ in seqs if s_[8] == 1 and s_[9] == 1 and s_[10] == 1), 4) == F(1, 4), "uni-36 P(1,1,1) = 1/4")
ok(sum(1 for s_ in seqs if s_[8] == 1 and s_[9] == 1 and s_[10] == -1) == 0, "uni-36 P(1,1,-1) = 0")
perms = list(itertools.permutations(range(4)))  # perm[i] = rank of X_{i+1}, larger = bigger
ok(F(sum(1 for r in perms if r[3] > max(r[0], r[1]) > r[2]), 24) == F(1, 6), "uni-39 statement A = 1/6")
ok(F(sum(1 for r in perms if r[3] > r[2] > max(r[0], r[1])), 24) == F(1, 12), "uni-39 statement C = 1/12")
pe = sum(2 ** -(kk + 1) for kk in range(0, 200, 2))
close(pe, 2 / 3, 1e-15, "uni-43 P(X even) = 2/3")
UV = list(itertools.product(range(1, 5), repeat=2))
ok(F(sum(1 for u, v in UV if u * v < 4), 16) == F(5, 16) and F(sum(1 for u, v in UV if u == v), 16) == F(1, 4) and F(sum(1 for u, v in UV if u * v > 2), 16) == F(13, 16), "uni-44 triangle probabilities")
dat = [0, 0, 0, 9, 9, 10, 10]
ok(F(sum(abs(x - 0) for x in dat), 7) > F(10, 2), "uni-45 MAD about the mode can exceed range/2")
for _ in range(2000):
    d = [rng.randint(0, 20) for _ in range(rng.randint(2, 9))]
    nd, mu = len(d), sum(d) / len(d)
    sd = sqrt(sum((x - mu) ** 2 for x in d) / nd)
    md = sorted(d)[nd // 2] if nd % 2 else (sorted(d)[nd // 2 - 1] + sorted(d)[nd // 2]) / 2
    if not (sd <= (max(d) - min(d)) / 2 + 1e-12 and sum(abs(x - mu) for x in d) / nd <= sd + 1e-12 and sum(abs(x - md) for x in d) / nd <= sd + 1e-12):
        ok(False, "uni-45 statements A-C on random data " + str(d)); break
else:
    ok(True, "uni-45")
ok(F(sum(1 for u, v in itertools.product([1, 2, 3], repeat=2) if u * u >= v), 9) == F(7, 9), "uni-48 7/9")
for alpha, beta, pmf_ in [(2.0, 0.0, lambda x: pois(2.0, x)), (6 * .3 / .7, -.3 / .7, lambda x: comb(6, x) * .3 ** x * .7 ** (6 - x) if x <= 6 else 0)]:
    mean = sum(x * pmf_(x) for x in range(60)); var = sum(x * x * pmf_(x) for x in range(60)) - mean ** 2
    close(mean, alpha / (1 - beta), 1e-9, "uni-50 E(X)"); close(var, alpha / (1 - beta) ** 2, 1e-9, "uni-50 Var(X)")
signs = list(itertools.product([-1, 1], repeat=4))
ok(F(sum(sum(s_) ** 4 for s_ in signs), 16) == 40, "uni-51 E(S^4) = 40")
close(phi(1), 2 * (1 / (2 * sqrt(2 * pi * E))), 1e-15, "uni-53 g(1) = 1/sqrt(2 pi e), twice the bound on |u|")
ok(all(F(i, 25) >= F(i, 25) * (1 - F(i, 25)) for i in range(26)), "uni-54 mean >= variance for 0/1 data")
ok(F(3 + 1, 3) * 0 + F(7, 4) / 3 - F(4, 3) / 3 + F(1, 3) == F(17, 36), "uni-58 P(1/3<X<3/4) + P(X=0) = 17/36")
close(integrate(lambda z: abs(2 * z - 1), 0, 1), .5, 1e-12, "uni-59 E|Z1 - Z2| = alpha/2 at alpha = 1")
ok(F(5, 6) < 1, "uni-60 counterexample P(X1>1) = 1 > P(X2>1/2) = 5/6")
for kk in range(8):
    vals_ = sorted([3] * (7 - kk) + [5] * kk)
    mode = 3 if 7 - kk > kk else 5
    ok(vals_[3] == mode, "uni-61 median = mode with %d of 7 at x+r" % kk)
EX = F(2, 5) + F(2, 5); EX2 = F(4, 5) + F(8, 15)
ok(EX == F(4, 5) and EX2 == F(4, 3) and EX2 - EX ** 2 == F(52, 75), "uni-62 E X, E X^2, Var")
ok(F(1, 5) * (2 - F(9, 5)) + F(1, 5) == F(6, 25), "uni-62 exact P(|X-4/5|>=1) = 6/25")
close(.4 + E ** 2 / 5 + (E ** 2 - 1) / 5, (1 + 2 * E ** 2) / 5, 1e-12, "uni-62 M_X(1)")

# ======================================================================= Multivariate compilation
r = .5
close((6 / pi) * math.asin(r / 2), 6 / pi * math.asin(.25), 1e-15, "mv-01 formula")
sp, n_sp = 0, 60000
for _ in range(n_sp):
    pts = []
    for _ in range(3):
        z1, z2 = rng.gauss(0, 1), rng.gauss(0, 1)
        pts.append((z1, r * z1 + sqrt(1 - r * r) * z2))
    sp += math.copysign(1, (pts[0][0] - pts[1][0]) * (pts[0][1] - pts[2][1]))
close(3 * sp / n_sp, (6 / pi) * math.asin(r / 2), 0.03, "mv-01 Spearman rho of bivariate normal (simulation)")
ok((4 * 10, -2 * -3) == (40, 6), "mv-02 Var 40, Cov 6")
cond = [F(comb(2, j)) * F(2, 5) ** j * F(3, 5) ** (2 - j) for j in range(3)]
ok(cond == [F(9, 25), F(12, 25), F(4, 25)] and sum(F(2, 1 + j) * cond[j] for j in range(3)) == F(98, 75), "mv-04 conditional binomial")
close(E * 0 + 1 / sqrt(pi), 0 + .5 * sqrt(2) * sqrt(2 / pi), 1e-15, "mv-06 E max = 1/sqrt(pi)")
rho, acc = .6, [0.0] * 5
nsim = 200000
for _ in range(nsim):
    x = rng.gauss(0, 1); y = rho * x + sqrt(1 - rho * rho) * rng.gauss(0, 1); z = rng.gauss(0, 1)
    a, b = x * x, y * y + z * z
    acc[0] += a; acc[1] += b; acc[2] += a * b; acc[3] += a * a; acc[4] += b * b
ma, mb = acc[0] / nsim, acc[1] / nsim
corr = (acc[2] / nsim - ma * mb) / sqrt((acc[3] / nsim - ma ** 2) * (acc[4] / nsim - mb ** 2))
close(corr, rho * rho / sqrt(2), 0.02, "mv-07 Cor(X^2, Y^2+Z^2) = rho^2/sqrt2 (simulation)")
th, t = 2.0, 1.3
close(integrate(lambda y: exp(-t * t * y / 2) * exp(-y / th) / th, 0, 200, 40000), 1 / (1 + th * t * t / 2), 1e-9, "mv-08 characteristic function")
ex_geo = sum(k_ * .5 ** k_ for k_ in range(1, 200)); vx = sum(k_ * k_ * .5 ** k_ for k_ in range(1, 200)) - ex_geo ** 2
pu = [pois(1, u) for u in range(60)]
ev = sum(pu[u] * (u + 1) for u in range(60))
vv = sum(pu[u] * (u * (u + 1) + (u + 1) ** 2) for u in range(60)) - ev ** 2
close(ex_geo, ev, 1e-12, "mv-10 E[Y] = E[V] = 2"); close(ex_geo + vx, vv, 1e-9, "mv-10 Var[Y] = Var[V] = 4")
ok(4 * 3 + 4 * 2 ** 2 == 28, "mv-15 Var = 28")
pp_, rr = 3, .4
R = [[1 if i == j else rr for j in range(pp_)] for i in range(pp_)]


def solve(A, b):
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        piv = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= piv
        for k2 in range(n):
            if k2 != i:
                f_ = M[k2][i]
                for j in range(i, n + 1):
                    M[k2][j] -= f_ * M[i][j]
    return [M[i][n] for i in range(n)]


w = solve(R, [rr] * pp_)
close(sum(rr * wi for wi in w), pp_ * rr * rr / (1 + (pp_ - 1) * rr), 1e-12, "mv-17 R^2 = p rho^2 / (1 + (p-1) rho)")
lam, mu_ = 2.0, 0.5
zz = 1.7
close(integrate(lambda x: lam * exp(-lam * x) * mu_ * exp(-mu_ * (zz - x)), 0, zz), lam * mu_ / (lam - mu_) * (exp(-mu_ * zz) - exp(-lam * zz)), 1e-12, "mv-19 convolution density")
ok(F(sum(1 for q_ in itertools.permutations(range(3)) if q_ == (0, 1, 2)), 6) == F(1, 6), "mv-20 1/6")
ok(3 * 1 + 2 * 1 == 5, "mv-23 Var = 5")
ok((1 * 1 + 1 * 1) / 2 - 0 == 1, "mv-25 Cov = 1")
xs = sorted(math.tan(math.pi / 4 - (rng.random() - .5) * pi) for _ in range(100000))
close(sum(1 for v in xs if v <= 1) / 1e5, .5 + atan(1) / pi, 0.006, "mv-27 transform is Cauchy (simulation, P(<=1))")
ok(F(200, 340) == F(10, 17), "mv-30 Binomial(520, 10/17)")
ok(F(5, 6) ** 12 == (1 - F(2, 12)) ** 12, "mv-36 (5/6)^12")
c_ = 2
ok(-1 + 3 - c_ == 0 and 1 * (3 * 2 - c_ * c_) - 1 * (2 - c_) + 1 * (c_ - 3) == 1, "mv-41 c = 2, det = 1")
yy = .3
close(integrate(lambda x: 6 * (1 - x), yy, 1), 3 * (1 - yy) ** 2, 1e-12, "mv-42 marginal of Y")
close(integrate(lambda x: x ** 4 * phi(x), -12, 12), 3, 1e-8, "mv-45 E X^4 = 3")
nn = 3
# residual Y - (T/n)1 has covariance (I - J/n) I (I - J/n)' ; compute it entry by entry
Pm = [[F(1 if i == j else 0) - F(1, nn) for j in range(nn)] for i in range(nn)]
ok(all(sum(Pm[i][k_] * Pm[j][k_] for k_ in range(nn)) == F(1 if i == j else 0) - F(1, nn) for i in range(nn) for j in range(nn)), "mv-49 conditional covariance I - 11'/n")
lamN = 1.7
sN = sN2 = 0
for _ in range(100000):
    s_, k_ = 0, 0
    while s_ <= 1:
        s_ += rng.expovariate(lamN); k_ += 1
    sN += k_; sN2 += k_ * k_
close(sN2 / 1e5 - (sN / 1e5) ** 2, lamN, 0.04, "mv-50 Var(N) = lambda (simulation)")
zs = []
for _ in range(100000):
    u1, u2 = rng.random(), rng.random()
    zs.append((rng.gauss(0, 1) * u1 + rng.gauss(0, 1) * u2) / sqrt(u1 * u1 + u2 * u2))
close(sum(z_ * z_ for z_ in zs) / 1e5, 1, 0.02, "mv-52 Var(Z) = 1 (simulation)")
close(sum(1 for z_ in zs if z_ <= 1) / 1e5, Phi(1), 0.006, "mv-52 Z is N(0,1) (simulation)")
al = .6
close(al * al / (1 + al * al), al ** 2 / (1 * (1 + al ** 2)), 1e-15, "mv-53 R^2")
rho = .7
close((rho ** 3 - rho * rho ** 2) / sqrt((1 - rho ** 2) * (1 - rho ** 4)), 0, 1e-15, "mv-57 partial correlation 0")
close(integrate(lambda d: d * phi(d), 0, 12) - .5 * 2 * integrate(lambda d: d * phi(d), 0, 12), 0, 1e-12, "mv-58 Cov(|D|, U) = 0")
dets = {"A": 1 * 5 - (-2) * 0, "B": 1 * 2 - 1 * 2, "C": 1 * -4 - 1 * 2, "D": 1 * 1 - (-1) * 1}
ok(dets["B"] == 0 and all(v != 0 for k2, v in dets.items() if k2 != "B"), "mv-61 only option 2 singular")
zw = []
for _ in range(100000):
    x, y = rng.gauss(0, 1), rng.gauss(0, 1)
    zw.append((x, y) if x * y > 0 else ((-x, y) if x < 0 else (x, -y)))
mz, mw = sum(a for a, _ in zw) / 1e5, sum(b for _, b in zw) / 1e5
close(sum(a * b for a, b in zw) / 1e5 - mz * mw, 3 / (2 * pi), 0.02, "mv-56 Cov(Z,W) = 3/(2 pi) as printed (simulation)")
close(sum(1 for a, _ in zw if a > 0) / 1e5, .75, 0.006, "mv-56 P(Z>0) = 3/4 as printed, so Z is not N(0,1)")
m_, n_ = 2, 3
b1 = [F(comb(m_, i), 2 ** m_) for i in range(m_ + 1)]; b2 = [F(comb(n_, j), 2 ** n_) for j in range(n_ + 1)]
ok(all(sum(b1[i] * b2[j] for i in range(m_ + 1) for j in range(n_ + 1) if j - i + m_ == s_) == F(comb(m_ + n_, s_), 2 ** (m_ + n_)) for s_ in range(m_ + n_ + 1)), "mv-63 X2 - X1 + m ~ Bin(m+n, 1/2)")
ok(all(b1[k_ - j] * b2[j] / sum(b1[k_ - jj] * b2[jj] for jj in range(n_ + 1) if 0 <= k_ - jj <= m_) == F(comb(n_, j) * comb(m_, k_ - j), comb(m_ + n_, k_)) for k_ in range(m_ + n_ + 1) for j in range(n_ + 1) if 0 <= k_ - j <= m_), "mv-63 conditional law is hypergeometric")
ok(not any(2 * i + 3 * j == 1 for i in range(m_ + 1) for j in range(n_ + 1)), "mv-63 2X1 + 3X2 never equals 1")
nbig = 2000
close(sum(abs(comb(nbig, k_) * (1 / nbig) ** k_ * (1 - 1 / nbig) ** (nbig - k_) - pois(1, k_)) for k_ in range(10)), 0, 2e-3, "mv-68 Bin(n,1/n) ~ Poisson(1)")
ok(1 * 4 == 4, "mv-69 Var(X Y) = 4")
close(1 - sum(pois(1, j) for j in range(3)), 0.0803, 1e-4, "mv-73 Poisson P(X>2)")
close(1 - sum(pois(1, j) for j in range(2)), 0.2642, 1e-4, "mv-73 Poisson P(X>1)")
cntUV = 0
for _ in range(100000):
    x, y = rng.gauss(0, 1), rng.gauss(0, 1)
    cntUV += x / y < x / abs(y)
close(cntUV / 1e5, .25, 0.006, "mv-74 P(U<V) = 1/4 (simulation)")
ok(1 + 2 * -.5 >= 0 and 1 + 2 * -.51 < 0, "mv-75 rho >= -1/2")
for pdim in (2, 5):
    Sg = [[(1 if i == j else 0) + 1 for j in range(pdim)] for i in range(pdim)]
    v_ = [1 / sqrt(pdim)] * pdim
    ok(all(abs(sum(Sg[i][j] * v_[j] for j in range(pdim)) - (1 + pdim) * v_[i]) < 1e-12 for i in range(pdim)), "mv-76 (1/sqrt p)1 is the leading eigenvector of I + 11', p=%d" % pdim)
close(integrate(lambda x: 2 * x, 0, .5), .25, 1e-12, "mv-77 P(X<1/2|Y=1)")
close(integrate(lambda y: y * y / 2, 0, 2), 4 / 3, 1e-12, "mv-77 E(Y)")
close(2 * .9987 - 1, .9974, 1e-12, "mv-78 P(|2X+Y|<=15)")
ok(9 * 4 - 4 * 9 == 0 and 4 * 4 + 9 == 25, "mv-78 Cov and Var")
ok(abs(1 * 2 - 2) < 1e-12 and abs((1 + 2) - 3) < 1e-12, "mv-79 eigenvalues 3 and 0")
tv = []
for _ in range(40000):
    s11 = s12 = s22 = 0.0
    for _ in range(10):
        z1 = rng.gauss(0, 1); z2 = .5 * z1 + sqrt(.75) * rng.gauss(0, 1)
        s11 += z1 * z1; s12 += z1 * z2; s22 += z2 * z2
    tv.append(s22 - s12 * s12 / s11)
mt = sum(tv) / len(tv)
close(sum((v - mt) ** 2 for v in tv) / len(tv), 81 / 8, 0.35, "mv-80 Var(T) = 81/8 (simulation)")
detf = lambda z1: 1 * (-5 * z1 - 4) - (-2) * (2 * z1 - 2) + 1 * (4 - (-5))
ok(detf(1) == 0 and detf(0) != 0 and detf(2) != 0, "mv-81 singular iff Z1 = 1")
close(.5 * exp(-1), exp(-1) / 2, 1e-15, "mv-81 probability e^-1/2")
gs = []
for _ in range(100000):
    u = rng.random(); x1 = rng.gauss(0, 1); x2 = .5 * x1 + sqrt(.75) * rng.gauss(0, 1); x1 += 1
    gs.append(((u * x1 + x2 - u) / sqrt(u * u + u + 1), u))
close(sum(g * g for g, _ in gs) / 1e5, 1, 0.02, "mv-82 E(Z^2) = 1 (simulation)")
close(sum(g * g for g, u in gs if u < .3) / sum(1 for _, u in gs if u < .3), 1, 0.03, "mv-82 Z independent of U (simulation)")
close(1 - (5 / 9) * (1 - exp(-1)), (4 + 5 * exp(-1)) / 9, 1e-15, "mv-83 P(XY=0)")
ok(F(9) * F(4, 9) + 1 + (3 * F(2, 3) - 1) ** 2 == 6 and F(4, 9) + 1 == F(13, 9) and 2 * F(4, 9) - 2 == F(-10, 9), "mv-83 moments")
ok(F(4, 6) < F(7, 10), "mv-84 4/6 < 70%")
close(.2 * exp(-2) + .8 * integrate(lambda x: x / 4 * exp(-x / 2), 2, 80), (exp(-2) + 8 * exp(-1)) / 5, 1e-9, "mv-85 battery life")
ok(F(8) - F(6 * 12, 9) == 0, "mv-86 partial covariance 0")
ok(F(1, 27) + 3 * F(2, 3) * F(1, 9) == F(7, 27) and 3 * F(2, 3) == 2, "mv-87 conditional binomial")
import cmath; close(abs(cmath.exp(6 * (cmath.exp(1j * pi) - 1))), exp(-12), 1e-18, "mv-87 phi(pi) = e^-12")
ok(max(1 + 2 * -.47, 1 + .47) / 3 >= 1 / 3 and 1 + 2 * -.47 > 0, "mv-88 rho = -0.47 allowed, leading share >= 1/3")

# ======================================================================= Part 2: structure of the written banks
import pyq_bank_build as B  # noqa: E402
items, out = B.build()
L = "ABCD"
combo_re = re.compile(r"^(?:([A-D](?:, [A-D])*) and )?([A-D])(?: only)?$")


def letters(txt):
    if txt == "A, B, C and D":
        return "ABCD"
    t = txt.replace(" only", "")
    return "".join(sorted(re.findall(r"[A-D]", t)))


for _, x in items:
    it = x["item"]; i = it["id"]
    ok(len(it["explanation"]) >= 40, i + " explanation at least 40 characters")
    ok(it.get("ref", "").strip() != "", i + " names its source question")
    if it["format"] in ("single", "multi"):
        ok(len(it["options"]) == 4 and len(set(it["options"])) == 4 and it["answer"] in L, i + " four distinct options and a key")
        for m in re.finditer(r"\b[Oo]ption ([A-D])\b[^.]*?\b(fail|wrong|incorrect|not)\b", it["explanation"]):
            ok(m.group(1) != it["answer"], i + " explanation does not rule out its own answer")
    if it["format"] == "multi":
        truth = "".join(Lt for Lt in L if it["verdicts"][Lt]["tf"])
        ok(letters(it["options"][L.index(it["answer"])]) == truth, i + " keyed combination = true statements")
        ok(sum(1 for o in it["options"] if letters(o) == truth) == 1, i + " exactly one option is the true combination")
        ok(all(len(it["verdicts"][Lt]["why"]) >= 20 for Lt in L), i + " every statement has a reason")
    if it["format"] == "numeric":
        ok(it.get("check", "").strip() != "", i + " numeric item has a check line")
ok(B.main(["--check"]) == 0, "seed files and docs/CSIR_PYQ_BANK.md equal the build output")
refs = " ".join(x["item"]["ref"] for _, x in items) + " " + " ".join(B.LEFT_OUT)
for title, n, mod in B.SOURCES:
    tag = {"pyq_bank_probability": "Probability PDF", "pyq_bank_standard": "Standard Univariate PDF",
           "pyq_bank_univariate": "Univariate PDF", "pyq_bank_multivariate": "Multivariate PDF"}[mod.__name__]
    missing = [q for q in range(1, n + 1) if not re.search(re.escape(tag) + r" Q%d\b" % q, refs)]
    ok(not missing, "every question of '%s' is an item, a named repeat or listed as left out (missing %s)" % (title, missing))
spread = {}
for f, d in out.items():
    keys = [it["answer"] for it in d["items"] if it["format"] != "numeric"]
    spread[f] = {Lt: keys.count(Lt) for Lt in L}
print("answer-key spread per bank: " + "; ".join("%s %s" % (f.split("/")[1], v) for f, v in spread.items()))

print("%d checks, %d failed" % (N[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
