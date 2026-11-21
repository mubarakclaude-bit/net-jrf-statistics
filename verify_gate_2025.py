# -*- coding: utf-8 -*-
"""Verification for the GATE 2025 Statistics (ST) banks built by gate_bank_2025.py.

The paper prints no answer key, so every keyed answer is derived here by a route of its own: exact fractions, exhaustive
enumeration, numerical integration (Simpson), root finding, seeded simulation, or an explicit counterexample for the
'necessarily / not necessarily' options. Each check compares what is computed with what the bank keys. A few purely
conceptual statements (countability, uniqueness of most powerful tests, eigenvalues of rotations) carry a written reason
in the item; where a concrete example can witness the claim, it is built and checked here.

Standard library only.   Run from the repository root:  python verify_gate_2025.py
"""
import cmath, math, random, re, sys
from fractions import Fraction as Fr
from itertools import product

import gate_bank_2025 as B

N_, FAILS = [0], []


def ok(cond, what):
    N_[0] += 1
    if not cond:
        FAILS.append(what)
        print("FAIL " + what)


I = {x["item"]["id"]: x["item"] for x in B.ITEMS}
L = "ABCD"
rng = random.Random(20251121)


def q(n):
    return I["gate25-q%d" % n]


def key_single(n, letter, why):
    ok(q(n)["format"] == "single" and q(n)["answer"] == letter, "Q%d keyed %s, computed %s: %s" % (n, q(n)["answer"], letter, why))


def key_num(n, value, decimals=None):
    a = q(n)["answer"]
    want = str(int(round(value))) if decimals is None else ("%." + str(decimals) + "f") % value
    if decimals is None:
        ok(abs(value - round(value)) < 1e-9, "Q%d computed value %r is an integer" % (n, value))
    ok(q(n)["format"] == "numeric" and a == want, "Q%d keyed %s, computed %s" % (n, a, want))


def key_multi(n, truth):
    it = q(n)
    got = "".join(Lt for Lt in L if it["verdicts"][Lt]["tf"])
    ok(it["format"] == "multi" and got == truth, "Q%d verdicts %s, computed %s" % (n, got, truth))


def simpson(f, a, b, n=2000):
    n += n % 2
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, n))
    return s * h / 3


Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
phi = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def det(M):
    M = [[Fr(x) for x in r] for r in M]
    n, d = len(M), Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            M[r] = [M[r][k] - f * M[c][k] for k in range(n)]
    return d


def rank(M):
    M = [[Fr(x) for x in r] for r in M]
    rk, rows, cols = 0, len(M), len(M[0])
    for c in range(cols):
        p = next((r for r in range(rk, rows) if M[r][c] != 0), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        for r in range(rows):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]
                M[r] = [M[r][k] - f * M[rk][k] for k in range(cols)]
        rk += 1
    return rk


def mm(A, Bm):
    return [[sum(A[i][k] * Bm[k][j] for k in range(len(Bm))) for j in range(len(Bm[0]))] for i in range(len(A))]


def mpow(A, k):
    R = [[Fr(int(i == j)) for j in range(len(A))] for i in range(len(A))]
    for _ in range(k):
        R = mm(R, A)
    return R


# ------------------------------------------------------------------ Q11-Q24
f11 = lambda x: math.exp(x / 2) - 1
for x in (0.5, 1.0, 2.0):
    lhs, rhs = f11(x) ** 2, simpson(lambda t: f11(t) ** 2 + f11(t), 0, x)
    ok(abs(lhs - rhs) < 1e-9, "Q11 f(x) = e^(x/2) - 1 solves the integral equation at x = %g" % x)
key_single(11, "B" if 1 < f11(2) <= 2 else "?", "f(2) = e - 1 = %.4f" % f11(2))

ok(all(len(list(product((1, 2), repeat=n + 1))) == 2 ** (n + 1) for n in range(8)), "Q12 each finite stage of set A is finite")
key_single(12, "B", "digit sequences from {1, 2} are as many as binary sequences (written reason)")

basis_S = [(1, 0, -1), (0, 1, -1)]                       # spans the plane z = -(x + y)
ok(rank(basis_S) == 2, "Q13 S spans a 2-dimensional plane")
dim_perp = 3 - rank(basis_S)
ok(all(sum(a * b for a, b in zip(v, (1, 1, 1))) == 0 for v in basis_S), "Q13 (1, 1, 1) is orthogonal to S")
key_single(13, {0: "B", 1: "C", 2: "D"}[dim_perp], "dim S-perp = %d" % dim_perp)

lam = math.log(2)
mgf = sum(math.exp(-lam) * lam ** k / math.factorial(k) * 3 ** k for k in range(80))
key_single(14, {1: "A", 2: "B", 3: "C", 4: "D"}[round(mgf)], "E(3^X) = %.10f" % mgf)
ok(abs(mgf - 4) < 1e-9, "Q14 series equals 4")

p1, p2, p3 = Fr(3, 10), Fr(1, 10), Fr(6, 10)
num = sum(Fr(x2) * Fr(math.comb(60, x2)) * p1 ** (60 - x2) * p2 ** x2 for x2 in range(61))
den = sum(Fr(math.comb(60, x2)) * p1 ** (60 - x2) * p2 ** x2 for x2 in range(61))
key_single(15, {25: "A", 15: "B", 30: "C", 45: "D"}[num / den], "E(X2 | X3 = 40) = %s" % (num / den))

ys = [0.5 + math.atan(math.tan(math.pi * (rng.random() - 0.5))) / math.pi for _ in range(100000)]
ok(abs(sum(ys) / len(ys) - 0.5) < 0.01, "Q16 Y = F(X) averages to 1/2")
def cauchy_mean(n):
    return sum(math.tan(math.pi * (rng.random() - 0.5)) for _ in range(n)) / n
spread = sorted(abs(cauchy_mean(2000)) for _ in range(200))
ok(spread[100] > 0.3, "Q16 Cauchy averages do not concentrate (median |mean| of 2000 draws = %.2f, about 1 for a standard Cauchy)" % spread[100])
key_single(16, "A", "WLLN for Uniform(0, 1); no mean for Cauchy")

ov = lambda a, b, c, d: max(0, min(b, d) - max(a, c))
rate = 2
cov = lambda i, j: rate * ov(*i, *j)
X, Y, W, Z = (1, 6), (3, 5), (5, 6), (1, 3)
opts17 = {"A": cov(W, Z) == 2, "B": rate * ((Y[1] - Y[0]) + (Z[1] - Z[0])) == 10 and ov(*Y, *Z) == 0,
          "C": False, "D": cov(X, Y) == 4}
ok(opts17 == {"A": False, "B": False, "C": False, "D": True}, "Q17 only Cov(X, Y) = 4 holds (%s)" % opts17)
key_single(17, "D", "Cov(X, Y) = Var(Y) = 4")

key_single(18, "D", "T minimal sufficient, so T is a function of U; U need not be a function of T (written reason)")

c = 1.959963984540054
power19 = lambda th: 1 - Phi(c - math.sqrt(2) * th) + Phi(-c - math.sqrt(2) * th)
grid = [k / 100 for k in range(-400, 401)]
ok(min(power19(t) for t in grid) >= 0.05 - 1e-9 and abs(power19(0) - 0.05) < 1e-6, "Q19 LRT power is at least 0.05 everywhere")
one_sided = lambda th: 1 - Phi(1.6448536269514722 - math.sqrt(2) * th)          # MP for theta > 0
ok(one_sided(1) > power19(1) and one_sided(-1) < power19(-1), "Q19 no single test is most powerful on both sides")
sim = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(200000)]
e_x1phi = sum(a for a, b in sim if abs(a + b) / math.sqrt(2) > c) / len(sim)
ok(abs(e_x1phi) < 0.01, "Q19 E0(X1 phi) is 0 by symmetry (simulated %.4f)" % e_x1phi)
key_single(19, "B", "LRT is unbiased")

tests20 = {"reject X > 1": (lambda x: x > 1), "reject X > 1 or X < 0.05": (lambda x: x > 1 or x < 0.05)}
size = {k: simpson(lambda x: float(t(x)), 0, 1, 20000) for k, t in tests20.items()}
power = {k: simpson(lambda x: float(t(x)), 1, 2, 20000) for k, t in tests20.items()}
ok(all(abs(p - 1) < 1e-3 for p in power.values()), "Q20 both tests have power 1, so both are most powerful at level 0.05")
ok(size["reject X > 1"] < 1e-3 and abs(size["reject X > 1 or X < 0.05"] - 0.05) < 1e-3, "Q20 their sizes differ (0 and 0.05)")
key_single(20, "B", "power 1 is forced; size and rejection region are not")

# Q21: with f0 = f1 every level-0.05 test of size 0.05 has power 0.05, so many tests are most powerful
pw = [simpson(lambda x: float(x < 0.05), 0, 1, 20000), simpson(lambda x: float(x > 0.95), 0, 1, 20000)]
ok(all(abs(p - 0.05) < 1e-3 for p in pw), "Q21 two different tests are both most powerful when f0 = f1 (uniqueness fails)")
key_single(21, "A", "uniqueness is not guaranteed")

n22, F22 = 400, 0.3
probs = [math.comb(n22, k) * F22 ** k * (1 - F22) ** (n22 - k) for k in range(n22 + 1)]
p_far = sum(p for k, p in enumerate(probs) if abs(math.sqrt(n22) * (k / n22 - F22)) > 0.1)
ok(p_far > 0.5, "Q22 sqrt(n)(Fn - F) does not go to 0 (P(|.| > 0.1) = %.2f at n = 400)" % p_far)
nvar = n22 * sum(p * (k / n22 - F22) ** 2 for k, p in enumerate(probs))
ok(abs(nvar - F22 * (1 - F22)) < 1e-9, "Q22 n Var(Fn(x)) = F(1 - F), not 0")
key_single(22, "C", "strong law for indicators")

rho = (Fr(432, 100) - 4) / 4
key_single(23, {Fr(8, 100): "A", Fr(8, 10): "B", Fr(32, 100): "C", Fr(1, 2): "D"}[rho], "rho = %s" % rho)

xs = [rng.uniform(-3, 3) for _ in range(30)]
ys_ = [10 * x + rng.gauss(0, 1) for x in xs]
b = sum(x * y for x, y in zip(xs, ys_)) / sum(x * x for x in xs)
ys_ = [y + (10 - b) * x for x, y in zip(xs, ys_)]        # shift so that beta-hat is exactly 10
b = sum(x * y for x, y in zip(xs, ys_)) / sum(x * x for x in xs)
u, v = [2 * x for x in xs], [y - x for x, y in zip(xs, ys_)]
g = sum(a * c_ for a, c_ in zip(u, v)) / sum(a * a for a in u)
ok(abs(b - 10) < 1e-9, "Q24 constructed data has beta-hat = 10")
key_single(24, {4.5: "A", 5.0: "B", 10.0: "C", 9.0: "D"}[round(g, 9)], "gamma-hat = %.6f" % g)

# ------------------------------------------------------------------ Q25-Q35 (numerical answers)
inner = lambda y: simpson(lambda x: y * y * math.cos(math.pi * (1 + x * y)), 0, 1, 400)
I25 = math.pi ** 2 * simpson(inner, 0, 1, 400)
key_num(25, round(I25, 6))
ok(abs(I25 + 1) < 1e-6, "Q25 double integral = %.8f" % I25)

P26 = [[Fr(1), Fr(2)], [Fr(-1), Fr(4)]]
Id = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]
P2, P3 = mpow(P26, 2), mpow(P26, 3)
Q26 = [[P3[i][j] - 2 * P2[i][j] - 4 * P26[i][j] + 13 * Id[i][j] for j in range(2)] for i in range(2)]
key_num(26, float(det(Q26)))

key_num(27, rank([[3, 5, 1], [0, 0, 1], [2, 0, 2]]))
key_num(28, float(16 * (Fr(3, 4) - Fr(1, 4))))
pmf29 = {k: Fr(math.comb(2, k)) * Fr(1, 3) ** k * Fr(2, 3) ** (2 - k) for k in range(3)}
key_num(29, float(18 * sum(k * k * p for k, p in pmf29.items())))
sim30 = sum(sum(rng.gauss(0, 1) ** 2 for _ in range(10)) for _ in range(40000)) / 40000
ok(abs(sim30 - 10) < 0.1, "Q30 E(e^(2Y)) = E(X'X) simulated %.3f" % sim30)
key_num(30, 10)
sim31 = []
for _ in range(100000):
    w2 = rng.gauss(0, math.sqrt(2)); w3 = w2 + rng.gauss(0, 1)
    sim31.append((w2 + w3) ** 2)
ok(abs(sum(sim31) / len(sim31) - 9) < 0.15, "Q31 simulated %.3f" % (sum(sim31) / len(sim31)))
key_num(31, 2 + 2 * min(2, 3) + 3)
data32 = [0, 1, 1, 1, 0]
ll = lambda t: sum(math.log(t) if x else math.log(1 - t) for x in data32)
best = max((k / 10000 for k in range(1, 7001)), key=ll)
key_num(32, best, 2)
key_num(33, float(15 * Fr(6, 5)))
pts = [(1, 3), (2, 4), (7, 8)]
rk = lambda vals: [sorted(vals).index(v_) + 1 for v_ in vals]
rx, ry = rk([p[0] for p in pts]), rk([p[1] for p in pts])
d2 = sum((a - b_) ** 2 for a, b_ in zip(rx, ry))
key_num(34, 1 - 6 * d2 / (3 * (9 - 1)), 2)
key_num(35, float(1 - (1 - Fr(5, 6)) * Fr(24, 20)), 2)

# ------------------------------------------------------------------ Q36-Q46
cube = lambda x: x ** 3
secants_zero = [(a, b_) for a in [k / 50 - 1 for k in range(101)] for b_ in [k / 50 - 1 for k in range(101)] if a < b_ and cube(a) == cube(b_)]
ok(not secants_zero, "Q36 x^3 on [-1, 1] has no zero-slope secant, though f'(0) = 0")
inc = lambda x: x - math.sin(x)                          # f' = 1 - cos x >= 0, zero at 0 and 2*pi only on [-1, 7]
xs36 = [k / 100 - 1 for k in range(801)]
ok(all(inc(xs36[k + 1]) > inc(xs36[k]) for k in range(800)), "Q36 a function whose derivative vanishes at two points is strictly increasing")
key_single(36, "C", "strictly increasing; the rest fail")

f37 = lambda x, y: (x - 1) ** 4 + (y - 2) ** 4
boundary = min(f37(t, 2 - t) for t in [k / 10000 for k in range(-20000, 40001)])
inside = min(f37(x, y) for x in [k / 50 for k in range(-100, 151)] for y in [k / 50 for k in range(-100, 151)] if x + y <= 2)
ok(abs(boundary - 0.125) < 1e-8 and inside >= boundary - 1e-12, "Q37 minimum over U is 1/8 (grid %.6f, boundary %.8f)" % (inside, boundary))
key_single(37, "D", "min = 1/8")

P38 = [[Fr(9, 10) if i == j else Fr(-1, 10) for j in range(10)] for i in range(10)]
key_single(38, {10: "A", 9: "B", 1: "C", 8: "D"}[rank(P38)], "rank %d" % rank(P38))

alpha = Fr(1, 2) / (1 + 2 * Fr(1, 2))
ok(0 <= alpha <= 3 * alpha <= 1, "Q39 alpha gives a valid distribution function")
key_single(39, {Fr(1, 2): "A", Fr(1, 3): "B", Fr(1, 4): "C", Fr(1, 6): "D"}[alpha], "alpha = %s" % alpha)

mu, s2 = 0.3, 4.0
m = lambda k: simpson(lambda z: math.exp(k * z) * math.exp(-(z - mu) ** 2 / (2 * s2)) / math.sqrt(2 * math.pi * s2), mu - 60, mu + 60, 20000)
ok(abs(math.log(m(2) / m(1) ** 2) - s2) < 1e-6, "Q40 ln(E X^2 / (E X)^2) = sigma^2 for a lognormal (numerical)")
key_single(40, "B", "Var(ln X) = sigma^2 = 4")

lam41 = 1.3
pmf41 = lambda mm_, nn: lam41 ** nn * math.exp(-lam41) / (2 ** nn * math.factorial(mm_) * math.factorial(nn - mm_))
px = lambda mm_: sum(pmf41(mm_, nn) for nn in range(mm_, 80))
ok(all(abs(px(k) - math.exp(-lam41 / 2) * (lam41 / 2) ** k / math.factorial(k)) < 1e-12 for k in range(6)), "Q41 X is Poisson(lambda/2), not Poisson(lambda)")
py3 = sum(pmf41(k, 3) for k in range(4))
ok(all(abs(pmf41(k, 3) / py3 - math.comb(3, k) / 8) < 1e-12 for k in range(4)), "Q41 X | Y = 3 is Bin(3, 1/2)")
ey_x2 = sum(nn * pmf41(2, nn) for nn in range(2, 80)) / px(2)
ok(abs(ey_x2 - (2 + lam41 / 2)) < 1e-10, "Q41 E(Y | X = 2) = 2 + lambda/2, not lambda/2")
key_single(41, "C", "conditional binomial")

# Q42: two samples with equal sum of squares but different sums have a likelihood ratio free of theta
s1, s2_ = [1.0, -2.0, 2.0], [-1.0, 2.0, 2.0]
loglik = lambda xs_, th: sum(-(x + th) ** 2 / (2 * th) - 0.5 * math.log(2 * math.pi * th) for x in xs_)
ratios = [loglik(s1, th) - loglik(s2_, th) for th in (0.5, 1, 3, 10)]
ok(max(ratios) - min(ratios) < 1e-9, "Q42 likelihood depends on the data only through sum of squares")
zero_mean = sum((lambda xs_: sum(xs_) / 4 + sum((x - sum(xs_) / 4) ** 2 for x in xs_) / 3)([rng.gauss(-2, math.sqrt(2)) for _ in range(4)]) for _ in range(100000)) / 100000
ok(abs(zero_mean) < 0.03, "Q42 E(Xbar + S^2) = 0, so (Xbar, S^2) is not complete (simulated %.4f)" % zero_mean)
key_single(42, "B", "sum of squares is minimal sufficient")

def power43(k, th):          # E[phi_k] with S ~ Gamma(2, theta); k = None is the original test
    if k is None:
        return math.exp(-1 / th)
    dens = lambda s: s * math.exp(-s / th) / th ** 2
    return simpson(lambda s: (1 - 1 / (k * s)) * dens(s), 1, 1 + 80 * th, 20000)
match43 = {Lt: all(abs(power43(k, th) - power43(None, th)) < 1e-6 for th in (0.5, 1, 2, 4)) for Lt, k in zip(L, (1, 2, 3, 4))}
ok(match43 == {"A": True, "B": False, "C": False, "D": False}, "Q43 only phi_1 has the power function of phi (%s)" % match43)
key_single(43, "A", "Rao-Blackwellised test")

pxy = simpson(lambda y: math.exp(-y) * (1 - math.exp(-2 * y)), 0, 60, 20000)
ok(abs(pxy - 2 / 3) < 1e-8, "Q44 P(X < Y1) = 2/3")
er = 2 * (1 + pxy + 0.5)
sim44 = 0
for _ in range(100000):
    x = rng.expovariate(2); y1 = rng.expovariate(1); y2 = rng.expovariate(1)
    sim44 += (1 + (x < y1) + (y2 < y1)) + (1 + (x < y2) + (y1 < y2))
ok(abs(sim44 / 100000 - 13 / 3) < 0.02, "Q44 simulated E(R1 + R2) = %.3f" % (sim44 / 100000))
key_single(44, {13 / 3: "A", 22 / 5: "B", 21 / 5: "C", 9 / 2: "D"}[min((13 / 3, 22 / 5, 21 / 5, 9 / 2), key=lambda t: abs(t - er))], "E = %.4f" % er)

zs = []
for _ in range(60000):
    rows = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(5)]
    w11 = sum(a * a for a, b_ in rows); w12 = sum(a * b_ for a, b_ in rows); w22 = sum(b_ * b_ for a, b_ in rows)
    zs.append(w11 + 4 * w12 + 4 * w22)
mz = sum(zs) / len(zs); vz = sum((z - mz) ** 2 for z in zs) / (len(zs) - 1)
ok(abs(mz - 25) < 0.3 and abs(vz - 250) < 10, "Q45 simulated mean %.2f (25) and variance %.1f (250)" % (mz, vz))
key_single(45, "C", "Var = 2 x 5 x (a'a)^2 = 250")

ssr = 15.48 ** 2 / 22.82; F46 = ssr / ((43.62 - ssr) / 22)
key_single(46, {"2.54": "A", "2.98": "B", "3.17": "C", "6.98": "D"}["%.2f" % F46], "F = %.4f" % F46)

# ------------------------------------------------------------------ Q47-Q54 (multiple correct)
xn, prev, dec = 0.0, None, True
s47 = 0.0
seq = []
for n in range(1, 200001):
    s47 += 1 / math.sqrt(n)
    val = s47 - 2 * (math.sqrt(n) - 1)
    if prev is not None and val >= prev:
        dec = False
    prev = val
    if n in (1000, 100000, 200000):
        seq.append(val)
ok(dec and seq[-1] > 0 and abs(seq[-1] - seq[-2]) < 1e-3, "Q47 x_n decreases and settles near %.4f" % seq[-1])
ok(abs(seq[-1] - (2 + -1.4603545088095868)) < 1e-2, "Q47 limit is 2 + zeta(1/2)")
key_multi(47, "BD")

half_turn = [[1, 0, 0], [0, -1, 0], [0, 0, -1]]
ok(det(half_turn) == 1 and mm(half_turn, half_turn) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "Q48 the half-turn is in O and has eigenvalue -1")
th = 0.7
Rz = [[math.cos(th), -math.sin(th), 0], [math.sin(th), math.cos(th), 0], [0, 0, 1]]
eig = [cmath.exp(1j * th), cmath.exp(-1j * th), 1]
ok(all(abs(abs(e) - 1) < 1e-12 for e in eig) and sum(1 for e in eig if abs(e.imag) < 1e-12) == 1, "Q48 a generic rotation has one real eigenvalue, and it is 1")
key_multi(48, "CD")

A49 = [(1, -1, 0), (1, 1, -2), (1, 1, 1)]
ok(all(sum(a * b_ for a, b_ in zip(A49[i], A49[j])) == 0 for i in range(3) for j in range(i + 1, 3)), "Q49 coefficient vectors are orthogonal (independence)")
ok([sum(a * a for a in r) for r in A49] == [2, 6, 3], "Q49 variances are 2, 6, 3, so the plain sum of squares is not chi-square(3)")
for _ in range(20):
    y1, y2, y3 = rng.gauss(0, 2), rng.gauss(0, 3), rng.gauss(0, 2)
    t_form = (y3 / math.sqrt(3)) / math.sqrt((y1 ** 2 / 2 + y2 ** 2 / 6) / 2)
    f_form = ((y1 ** 2 / 2 + y3 ** 2 / 3) / 2) / (y2 ** 2 / 6)
    ok(abs(t_form - 2 * y3 / math.sqrt(3 * y1 ** 2 + y2 ** 2)) < 1e-9 and abs(f_form - (3 * y1 ** 2 + 2 * y3 ** 2) / (2 * y2 ** 2)) < 1e-9,
       "Q49 option C is a t2 ratio and option D an F(2,1) ratio")
key_multi(49, "AC")

ok(sum(1 / n ** 2 for n in range(1, 100000)) < 2 and all(n ** 3 / n ** 2 == n for n in range(1, 50)), "Q50 X_n = n w.p. 1/n^2 converges a.s. to 0 but E(X_n^3) = n")
key_multi(50, "BCD")

P51 = [[Fr(0), Fr(1, 2), Fr(1, 2)], [Fr(1, 3), Fr(0), Fr(2, 3)], [Fr(2, 5), Fr(3, 5), Fr(0)]]
pi51 = [Fr(18, 67), Fr(24, 67), Fr(25, 67)]
piP = [sum(pi51[i] * P51[i][j] for i in range(3)) for j in range(3)]
ok(piP == pi51 and sum(pi51) == 1, "Q51 pi P = pi")
ok(mm(P51, P51)[0][0] == Fr(11, 30), "Q51 two-step return probability = 11/30")
reach = all(mpow(P51, 2)[i][j] + P51[i][j] > 0 for i in range(3) for j in range(3))
ok(reach, "Q51 chain is irreducible, so no state is transient")
key_multi(51, "ABC")

th52, n52, reps = 2.0, 5, 40000
sm_minmax, sm_T, neg2max = 0.0, 0.0, 0
for _ in range(reps):
    xs_ = [rng.uniform(-th52 / 2, th52 / 2) for _ in range(n52)]
    sm_minmax += min(xs_) + max(xs_); sm_T += max(abs(x) for x in xs_)
    neg2max += 2 * max(xs_) < 2 * max(abs(x) for x in xs_)
ok(abs(sm_minmax / reps) < 0.01, "Q52 E(min + max) = 0, so (min, max) is not complete")
ok(abs(2 * (n52 + 1) / n52 * sm_T / reps - th52) < 0.01, "Q52 2(n+1)/n max|X| is unbiased (simulated)")
ok(neg2max > 0, "Q52 2 max X differs from the MLE 2 max|X| in some samples")
key_multi(52, "BD")

Sig = [4, 9, 4]; a53 = [2, 0, -1]; b53 = [1, 1, 1]
q_ab = lambda u_, v_: sum(u_[i] * Sig[i] * v_[i] for i in range(3))
opts53 = {"A": q_ab(a53, a53) == 20, "B": q_ab(a53, a53) == 20, "C": sum(Sig) == 17, "D": q_ab(a53, b53) == 3}
key_multi(53, "".join(Lt for Lt in L if opts53[Lt]))

Xd = [[1, 0], [1, 1], [1, 2], [1, 3]]; lam54 = Fr(1); beta = [Fr(1), Fr(2)]
XtX = [[sum(Fr(Xd[k][i]) * Xd[k][j] for k in range(4)) for j in range(2)] for i in range(2)]
Mx = [[XtX[i][j] + (lam54 if i == j else 0) for j in range(2)] for i in range(2)]
dM = det(Mx); Minv = [[Mx[1][1] / dM, -Mx[0][1] / dM], [-Mx[1][0] / dM, Mx[0][0] / dM]]
Ebeta = [sum(sum(Minv[i][k] * XtX[k][j] for k in range(2)) * beta[j] for j in range(2)) for i in range(2)]
sandwich = mm(mm(Minv, XtX), Minv)
ok(Ebeta != beta, "Q54 ridge is biased (E beta-hat = %s)" % Ebeta)
ok(det(Mx) > 0 and Mx[0][0] > 0, "Q54 X'X + lambda I is positive definite")
ok(sandwich != Minv, "Q54 Var(beta-hat) is the sandwich, not (X'X + lambda I)^-1")
key_multi(54, "BC")

# ------------------------------------------------------------------ Q55-Q65 (numerical answers)
crit = [(x, 2 / x ** 2) for x in [-1.0] if abs(2 * x * (2 / x ** 2) ** 2 + 8) < 1e-12]
roots = [x for x in [k / 1000 for k in range(-5000, 5001) if k] if abs(8 / x ** 3 + 8) < 1e-9]
ok(roots == [-1.0], "Q55 the only critical point has x = -1")
x, y = -1, 2
fxx, fyy, fxy = 2 * y * y, 2 * x * x, 4 * x * y
key_num(55, sum(1 for _ in crit if fxx * fyy - fxy ** 2 < 0))

P56 = [[0 if i == j else (1 if j > i else -1) for j in range(5)] for i in range(5)]
key_num(56, float(det(P56)))
P57 = [[Fr(2), Fr(1)], [Fr(1), Fr(2)]]; Q57 = [[Fr(1), Fr(1)], [Fr(-2), Fr(4)]]
tr = lambda A: sum(A[i][i] for i in range(len(A)))
key_num(57, float(tr(mpow(P57, 5)) + tr(mpow(Q57, 4))))

px58 = {k: Fr(math.comb(2, k)) * Fr(1, 3) ** k * Fr(2, 3) ** (2 - k) for k in range(3)}
pS = lambda k: math.exp(-3) * 3 ** k / math.factorial(k)
prob58 = sum(float(px58[xv]) * sum(pS(s) for s in range(xv)) for xv in range(3))
key_num(58, 10 * prob58, 2)

g59 = lambda l: (2 + l) / 2 * math.exp(-l) - 2 * math.exp(-2)
lo, hi = 0.01, 20.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if g59(mid) > 0 else (lo, mid)
key_num(59, round(lo, 9))

# Q60: the first 18 terms take 2^18 equally likely values; P(sum <= 2/3) approaches 5/6
tot = 0
for bits in range(1 << 18):
    s60 = sum((1 if bits >> k & 1 else -1) / 2 ** (k + 1) for k in range(18))
    tot += s60 <= 2 / 3
p60 = tot / (1 << 18)
ok(abs(p60 - 5 / 6) < 1e-4, "Q60 P(U <= 2/3) = %.6f" % p60)
key_num(60, round(6 * p60))

e_inv = simpson(lambda s: (1 / s) * s ** 20 * math.exp(-s - math.lgamma(21)), 1e-9, 120, 40000)   # S ~ Gamma(21, 1)
ok(abs(e_inv - 1 / 20) < 1e-8, "Q61 E(1/S) = 1/20 for S ~ Gamma(21, 1)")
key_num(61, round(1 / (21 * e_inv - 1), 6))

c62 = math.log(0.3); th62 = math.log(0.36)
ok(abs(math.exp(2 * c62) - 0.09) < 1e-12, "Q62 size at theta = 0 is 0.09")
sim62 = sum(max(th62 - rng.expovariate(1), th62 - rng.expovariate(1)) <= c62 for _ in range(200000)) / 200000
ok(abs(sim62 - math.exp(2 * (c62 - th62))) < 0.005, "Q62 simulated power %.4f matches e^(2(c - theta)) = %.4f" % (sim62, math.exp(2 * (c62 - th62))))
key_num(62, math.exp(2 * (c62 - th62)), 2)

size63 = max(t ** 3 + (1 - t) ** 3 for t in [0.25 + k / 20000 for k in range(10001)])
key_num(63, size63, 2)

S64 = [[1, 0.4, 0], [0.4, 1, 0.6], [0, 0.6, 1]]
d64 = float(det([[Fr(str(v_)) for v_ in r] for r in S64]))
cof = lambda i, j: (-1) ** (i + j) * float(det([[Fr(str(S64[r][c_])) for c_ in range(3) if c_ != j] for r in range(3) if r != i]))
P64 = [[cof(j, i) / d64 for j in range(3)] for i in range(3)]       # precision matrix
pc = -P64[0][1] / math.sqrt(P64[0][0] * P64[1][1])
key_num(64, pc, 2)

r65 = 14 / 20
orth = simpson(lambda x: phi(x) * (1 - Phi(-r65 * x / math.sqrt(1 - r65 ** 2))), 0, 12, 20000)
ok(abs(orth - (0.25 + math.asin(r65) / (2 * math.pi))) < 1e-8, "Q65 orthant probability = 1/4 + arcsin(rho)/(2 pi) (numerical)")
key_num(65, 2 * math.pi * (orth - 0.25), 2)

# ------------------------------------------------------------------ the official key (a second, independent check)
# "Answer Key for Statistics (ST)", GATE 2025 (IIT Roorkee), as republished by the GATE 2026 site
# (gate2026.iitg.ac.in/doc/download/2025_Key/ST_Keys.pdf). Ranges are inclusive. The answers above were computed first;
# this table only confirms them.
OFFICIAL = {11: "B", 12: "B", 13: "C", 14: "D", 15: "B", 16: "A", 17: "D", 18: "D", 19: "B", 20: "B", 21: "A", 22: "C",
            23: "A", 24: "A", 25: (-1, -1), 26: (50, 50), 27: (3, 3), 28: (8, 8), 29: (16, 16), 30: (10, 10), 31: (9, 9),
            32: (0.59, 0.61), 33: (18, 18), 34: (0.98, 1.00), 35: (0.79, 0.81), 36: "C", 37: "D", 38: "B", 39: "C", 40: "B",
            41: "C", 42: "B", 43: "A", 44: "A", 45: "C", 46: "D", 47: "BD", 48: "CD", 49: "AC", 50: "BCD", 51: "ABC",
            52: "BD", 53: "ABC", 54: "BC", 55: (1, 1), 56: (0, 0), 57: (341, 341), 58: (0.42, 0.46), 59: (2, 2), 60: (5, 5),
            61: (20, 20), 62: (0.67, 0.72), 63: (0.42, 0.46), 64: (0.49, 0.51), 65: (0.75, 0.80)}
for n, k in OFFICIAL.items():
    it = q(n)
    if isinstance(k, tuple):
        ok(k[0] <= float(it["answer"]) <= k[1], "Q%d bank answer %s lies in the official range %s" % (n, it["answer"], k))
    elif it["format"] == "multi":
        ok("".join(Lt for Lt in L if it["verdicts"][Lt]["tf"]) == k, "Q%d true statements equal the official key %s" % (n, k))
    else:
        ok(it["answer"] == k, "Q%d bank answer %s equals the official key %s" % (n, it["answer"], k))
ok(sorted(OFFICIAL) == list(range(11, 66)), "official key covers Q11-Q65")

# ------------------------------------------------------------------ structure
def letters(txt):
    if txt == "A, B, C and D":
        return "ABCD"
    return "".join(sorted(re.findall(r"[A-D]", txt.replace(" only", ""))))

ok(len(I) == 55, "55 items (Q11-Q65)")
refs = " ".join(it["ref"] for it in I.values())
missing = [k for k in range(11, 66) if not re.search(r"GATE 2025 ST Q%d\b" % k, refs)]
ok(not missing and B.LEFT_OUT == ["Q%d" % k for k in range(1, 11)], "every question is an item or listed as left out (missing %s)" % missing)
counts = {f: sum(1 for it in I.values() if it["format"] == f) for f in ("single", "multi", "numeric")}
ok(counts == {"single": 25, "multi": 8, "numeric": 22}, "format counts %s" % counts)
for i, it in I.items():
    ok(len(it["explanation"]) >= 40, i + " explanation at least 40 characters")
    if it["format"] in ("single", "multi"):
        ok(len(it["options"]) == 4 and len(set(it["options"])) == 4 and it["answer"] in L, i + " four distinct options and a key")
        for m_ in re.finditer(r"\b[Oo]ption ([A-D])\b[^.]*?\b(fail|wrong|incorrect|not)\b", it["explanation"]):
            ok(m_.group(1) != it["answer"], i + " explanation does not rule out its own answer")
    if it["format"] == "multi":
        truth = "".join(Lt for Lt in L if it["verdicts"][Lt]["tf"])
        ok(letters(it["options"][L.index(it["answer"])]) == truth, i + " keyed combination = true statements")
        ok(sum(1 for o in it["options"] if letters(o) == truth) == 1, i + " exactly one option is the true combination")
    if it["format"] == "numeric":
        ok(it.get("check", "").strip() != "" and it["options"] == [], i + " numeric item has a check line and no options")
ok(B.main(["--check"]) == 0, "seed files equal the build output")
keys = [it["answer"] for it in I.values() if it["format"] != "numeric"]
print("answer-key spread (single + multi): " + ", ".join("%s %d" % (Lt, keys.count(Lt)) for Lt in L))
print("%d checks, %d failed" % (N_[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
