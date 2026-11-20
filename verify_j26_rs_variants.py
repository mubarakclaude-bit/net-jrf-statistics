#!/usr/bin/env python3
"""Independent check of seed/*_j26rs_pyq_variants.json (written by variants_j26_rs.py), batches 1 to 3.

It does not reuse the generator: it reads the numbers back out of each stem and recomputes the keyed option with its own
formulas, then checks the structure (ten variants per source question, globally unique ids, every srcQid is a real
June 2026 question, four options with distinct values, keys spread over A-D, the explanation states the answer, no
candidate data). Standard library only."""
import json, math, re
from fractions import Fraction as F
from math import comb
from pathlib import Path
from collections import Counter, defaultdict

R = Path(__file__).resolve().parent
src = {}
for f in R.glob("seed/*_pyq_j26_rs.json"):
    for it in json.loads(f.read_text(encoding="utf-8"))["items"]: src[it["questionId"]] = it
allids = Counter()
for f in R.glob("seed/*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    if isinstance(d, dict) and isinstance(d.get("items"), list):
        allids.update(i["id"] for i in d["items"] if isinstance(i, dict) and "id" in i)

items = []
for f in sorted(R.glob("seed/*_j26rs_pyq_variants.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    assert d["source"] == "variant" and d["count"] == len(d["items"]) and f.name == d["moduleId"] + "_j26rs_pyq_variants.json", f.name
    items += d["items"]

num = lambda s: F(s.replace("−", "-"))
def val(o):
    t = o.replace("−", "-").replace("^", "**").replace("e**", "math.e**")
    if "," in t: return o
    try: return float("%.12g" % float(eval(t, {"math": math})))
    except Exception: return o              # a text option (statement, model name): compared as text
def key(it): return it["options"]["ABCD".index(it["answer"])]
def fr(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    d = x.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return ("%.10f" % float(x)).rstrip("0").rstrip(".") if d == 1 else "%d/%d" % (x.numerator, x.denominator)
def close(opt, x, tol=1e-9): return abs(float(val(opt)) - float(x)) <= tol * max(1, abs(float(x)))

def chk_ruin(it):
    a, p = re.search(r"starts with Rs\. (\d+).*probability ([\d/]+)", it["stem"]).groups(); a = int(a); p = num(p); q = 1 - p
    return close(key(it), (q / p) ** a if p > q else 1, 1e-12) if p > q else key(it) == "1"
def chk_memoryless(it):
    lam, s, t = re.search(r"rate ([\d/.]+) per minute.*more than ([\d/.]+) minutes, the probability that it is more than ([\d/.]+)", it["stem"]).groups()
    return close(key(it), math.exp(-float(num(lam) * (num(t) - num(s)))))
def chk_split(it):
    a, b, k, n = re.search(r"rates (\d*)λ and (\d*)λ.*P\(N₁\(t\) = (\d+) \| N₁\(t\) \+ N₂\(t\) = (\d+)\)", it["stem"]).groups()
    a = int(a or 1); b = int(b or 1); k = int(k); n = int(n); pr = F(a, a + b)
    return close(key(it), comb(n, k) * pr ** k * (1 - pr) ** (n - k), 1e-12)
SUBI = {"₁": 1, "₂": 2, "₃": 3}
SUPN = lambda c: "¹²³⁴⁵⁶⁷⁸⁹".index(c) + 1
def P_of(it):
    p = num(re.search(r"p = ([\d/.]+) and q", it["stem"]).group(1)); q = 1 - p
    return [[q, p, 0], [q, 0, p], [0, q, p]]
def mat_pow(P, n):
    M = [[F(int(i == j)) for j in range(3)] for i in range(3)]
    for _ in range(n): M = [[sum(M[i][k] * P[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return M
def chk_nstep(it):
    i, j, n = re.search(r"p([₁₂₃])([₁₂₃])⁽([¹²³⁴⁵⁶⁷⁸⁹])⁾ is", it["stem"]).groups()
    return close(key(it), mat_pow(P_of(it), SUPN(n))[SUBI[i] - 1][SUBI[j] - 1], 1e-12)
def chk_fp(it):
    i, j, n = re.search(r"f([₁₂₃])([₁₂₃])⁽([¹²³⁴⁵⁶⁷⁸⁹])⁾", it["stem"]).groups(); i, j, n = SUBI[i] - 1, SUBI[j] - 1, SUPN(n)
    P = P_of(it)
    # enumerate every path of length n: first visit to j exactly at step n
    total = F(0)
    def walk(state, step, prob):
        nonlocal total
        if prob == 0: return
        if step == n: total += prob if state == j else 0; return
        if step > 0 and state == j: return
        for nxt in range(3): walk(nxt, step + 1, prob * P[state][nxt])
    walk(i, 0, F(1))
    return close(key(it), total, 1e-12)
def chk_ar1var(it):
    phi, s2 = re.search(r"yₜ = (−?[\d/.]+) yₜ₋₁ \+ εₜ with E\(εₜ\) = 0 and E\(εₜ²\) = ([\d/.]+)", it["stem"]).groups()
    phi = num(phi); s2 = num(s2); return close(key(it), s2 / (1 - phi * phi), 1e-12)
def chk_ar1acov(it):
    phi, s2, h = re.search(r"yₜ = (−?[\d/.]+) yₜ₋₁ \+ εₜ, where \{εₜ\} is white noise with variance ([\d/.]+), the autocovariance at lag (\d+)", it["stem"]).groups()
    phi = num(phi); s2 = num(s2); return close(key(it), phi ** int(h) * s2 / (1 - phi * phi), 1e-12)
def chk_rbd(it):
    t, b, sst, ssb, tot = map(int, re.search(r"with (\d+) treatments and (\d+) blocks, the treatment sum of squares is (\d+), the block sum of squares is (\d+) and the total sum of squares is (\d+)", it["stem"]).groups())
    return close(key(it), F(tot - sst - ssb, (t - 1) * (b - 1)), 1e-12)
def chk_f(it):
    k, n, a, e = map(int, re.search(r"compares (\d+) treatments using (\d+) observations.*treatment sum of squares is (\d+) and the error sum of squares is (\d+)", it["stem"]).groups())
    return abs(float(key(it)) - (a / (k - 1)) / (e / (n - k))) < 5e-5
def chk_neyman(it):
    n, N1, N2, S1, S2, h = map(int, re.search(r"size (\d+) .*N₁ = (\d+), N₂ = (\d+), S₁ = (\d+) and S₂ = (\d+)\. The number of units to be selected from stratum (\d)", it["stem"]).groups())
    w = [N1 * S1, N2 * S2]; return key(it) == str(F(n * w[h - 1], sum(w)))
def chk_adj(it):
    n, k, r2 = re.search(r"y is (\d+)×1 and X is \d+×(\d+) .*R² = ([\d.]+)", it["stem"]).groups(); n, k = int(n), int(k)
    return key(it) == "%.3f" % (1 - (1 - float(r2)) * (n - 1) / (n - k))
def chk_dw(it):
    s0, s1 = re.search(r"Σeₜ² ≈ ([\d.]+) and Σeₜeₜ₋₁ ≈ (−?[\d.]+)", it["stem"]).groups()
    rho = float(num(s1)) / float(num(s0)); return key(it) == ("%.2f, %.2f" % (rho, 2 * (1 - rho))).replace("-", "−")
def chk_mgf(it):
    m = re.search(r"e\^\(((−?\d*)t \+ )?(\d*/?\d*)t²\)\. Then (.*) is$", it["stem"]); lin, c2, ask = m.group(2), m.group(3), m.group(4)
    mu = 0 if m.group(1) is None else (int(lin.replace("−", "-")) if lin not in ("", "−") else (1 if lin == "" else -1))
    s2 = 2 * (F(c2) if c2 else F(1))
    want = {"the fourth central moment of X": 3 * s2 ** 2, "the variance of X": s2, "E(X²)": s2 + mu * mu, "the third central moment of X": 0}[ask]
    return close(key(it), want, 1e-12)

CHECK = {"55125114584": chk_ruin, "55125114581": chk_memoryless, "55125114585": chk_split, "55125114597": chk_nstep,
         "55125114599": chk_fp, "55125114568": chk_ar1var, "55125114605": chk_ar1acov, "55125114527": chk_rbd,
         "55125114526": chk_f, "55125114530": chk_neyman, "55125114558": chk_adj, "55125114563": chk_dw, "55125114508": chk_mgf}

# ---------------------------------------------------------------------------------------------- batch 2 checks
import cmath
def fv(s): return F(s.replace("−", "-").strip("()"))
def chk_maxexp(it):
    m = re.search(r"The (maximum|minimum) value of f\(x\) = (\d+)\^\(x\((?:(\d+) − x|x − (\d+))\)\), 0 ≤ x ≤ (\d+)", it["stem"])
    kind, a, c = m.group(1), int(m.group(2)), int(m.group(5))
    xs = [c * j / 4000 for j in range(4001)]
    vals = [a ** (x * (c - x)) if kind == "maximum" else a ** (x * (x - c)) for x in xs]
    want = max(vals) if kind == "maximum" else min(vals)
    return abs(float(val(key(it))) - want) < 1e-9 * max(1, want)
def poly_coeffs(expr):
    e = expr.replace(" ", "").replace("−", "-"); co = {3: F(0), 2: F(0), 1: F(0), 0: F(0)}
    for t in re.findall(r"[+-]?[^+-]+", e):
        for pw_, sym in ((3, "x³"), (2, "x²"), (1, "x")):
            if t.endswith(sym):
                c = t[: -len(sym)]; co[pw_] += F(-1 if c == "-" else 1 if c in ("", "+") else c); break
        else: co[0] += F(t)
    return co
def chk_extrema(it):
    m = re.search(r"Consider f\(x\) = (.*?) and the statements: A\. x = (\S+) is .* C\. x = (\S+) is", it["stem"])
    co = poly_coeffs(m.group(1)); r1, r2 = fv(m.group(2)), fv(m.group(3))
    d1 = lambda x: 3 * co[3] * x * x + 2 * co[2] * x + co[1]; d2 = lambda x: 6 * co[3] * x + 2 * co[2]
    assert d1(r1) == 0 and d1(r2) == 0
    truth = [L for L, ok in (("A", d2(r1) > 0), ("B", d2(r1) < 0), ("C", d2(r2) > 0), ("D", d2(r2) < 0)) if ok]
    return key(it) == ", ".join(truth) + " only"
def chk_rolle(it):
    m = re.search(r"For f\(x\) = (.*) on \[(\S+), (\S+)\]", it["stem"]); fx, lo, hi = m.group(1), fv(m.group(2)), fv(m.group(3))
    roots = []
    for fac, sq in re.findall(r"(x|\(x [−+] [\d.]+\))(²?)", fx):
        r = F(0) if fac == "x" else (fv(fac[4:-1]) * (1 if "−" in fac else -1))
        roots += [r] * (2 if sq else 1)
    a, b, c = roots                     # f = (x-a)(x-b)(x-c): f' = 3x² - 2(a+b+c)x + (ab+bc+ca)
    A, B, C = 3, -2 * (a + b + c), a * b + b * c + c * a
    disc = B * B - 4 * A * C; sq = math.isqrt(int(disc * 36)) / 6 if disc >= 0 else None
    zs = [(-B + s * math.sqrt(float(disc))) / (2 * A) for s in (1, -1)]
    inside = [z for z in zs if float(lo) + 1e-9 < z < float(hi) - 1e-9]
    return len(inside) == 1 and abs(float(val(key(it))) - inside[0]) < 1e-9
def chk_laplace(it):
    m = re.search(r"f\(x\) = (?:\(?([\d/]+)\)?)?e\^\(−\(?([\d/]+)\)?\|x\|\),.*Then (E\(\|X\|\) and Var\(\|X\|\)|E\(X\) and Var\(X\))", it["stem"])
    co = F(m.group(1) or 1); lam = F(m.group(2)); assert co == lam / 2
    # numerical moments of the density
    h = 1e-3 / float(lam); ys = [h * (j + 0.5) for j in range(int(40 / (float(lam) * h)))]
    m1 = sum(2 * float(co) * y * math.exp(-float(lam) * y) for y in ys) * h          # E|X|
    m2 = sum(2 * float(co) * y * y * math.exp(-float(lam) * y) for y in ys) * h      # E X²
    want = (m1, m2 - m1 * m1) if "|X|" in m.group(3) else (0.0, m2)
    got = [float(F(x)) for x in key(it).split(", ")]
    return all(abs(g - w) < 1e-4 * max(1, abs(w)) for g, w in zip(got, want))
def chk_wlln(it):
    mu, s2 = map(int, re.search(r"mean (\d+) and variance (\d+)", it["stem"]).groups())
    def truth(o):
        m = re.fullmatch(r"\(1/n\)ΣXᵢ →ᵖ (\d+)", o)
        if m: return int(m.group(1)) == mu
        m = re.fullmatch(r"\(1/n\)ΣXᵢ² →ᵖ (\d+)", o)
        if m: return int(m.group(1)) == s2 + mu * mu
        m = re.fullmatch(r"\(√n/(\d+)\)\(X̄ₙ − (\d+)\) →ᵈ N\(0, 1\)", o)
        if m: return int(m.group(1)) ** 2 == s2 and int(m.group(2)) == mu
        m = re.fullmatch(r"E\[\(1/\(n−1\)\)Σ\(Xᵢ − X̄ₙ\)²\] = (\d+)", o)
        if m: return int(m.group(1)) == s2
        m = re.fullmatch(r"E\[\(1/n\)Σ\(Xᵢ − X̄ₙ\)²\] = (\d+)", o)
        if m: return False
        raise AssertionError(o)
    t = [truth(o) for o in it["options"]]
    return t.count(False) == 1 and not truth(key(it))
def detF(M):
    M = [[F(x) for x in row] for row in M]; n = len(M); d = F(1)
    for c in range(n):
        pv = next(r for r in range(c, n) if M[r][c] != 0)
        if pv != c: M[c], M[pv] = M[pv], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]; M[r] = [M[r][k] - f * M[c][k] for k in range(n)]
    return d
def chk_bibd(it):
    v, b, r, k, l = map(int, re.search(r"v = (\d+), b = (\d+), r = (\d+), k = (\d+), λ = (\d+)", it["stem"]).groups())
    assert b * k == v * r and r * (k - 1) == l * (v - 1)
    return int(key(it)) == detF([[r if i == j else l for j in range(v)] for i in range(v)])
def chk_factdf(it):
    n, r = re.search(r"A 2([¹²³⁴⁵⁶⁷⁸⁹]) factorial experiment is replicated (\d+) times", it["stem"]).groups(); n = SUPN(n); r = int(r)
    blocks = "randomized blocks" in it["stem"]; N = 2 ** n * r
    return int(key(it)) == (N - 1) - (2 ** n - 1) - ((r - 1) if blocks else 0)
def chk_pps(it):
    X, i = re.search(r"sizes X = \(([\d, ]+)\)\. The probability that unit (\d+)", it["stem"]).groups()
    X = [int(x) for x in X.split(", ")]; return F(key(it)) == F(X[int(i) - 1], sum(X))
def chk_poisson_unb(it):
    sts = re.search(r"A\. (.*)\. B\. (.*)\. C\. (.*)\. D\. (.*)\. Choose", it["stem"]).groups()
    def truth(s):
        if s == "X̄ is unbiased for λ" or s == "S² is unbiased for λ": return True
        if s == "X̄² is unbiased for λ²": return False
        body = s[: -len(" is unbiased for λ")].replace(" ", "").replace("−", "-")
        u = v = F(0)
        for t in re.findall(r"[+-]?[^+-]+", body):
            c = t[:-2]; c = F(-1 if c == "-" else 1 if c in ("", "+") else c)
            if t.endswith("X̄"): u += c
            elif t.endswith("S²"): v += c
            else: raise AssertionError(t)
        return u + v == 1
    tr = [L for L, s in zip("ABCD", sts) if truth(s)]
    want = "A, B, C, D" if len(tr) == 4 else ", ".join(tr) + " only"
    return key(it) == want
def P_mc(it):
    p = fv(re.search(r"with p = ([\d/.]+) and q", it["stem"]).group(1)); q = 1 - p
    return [[q, p, 0], [q, 0, p], [0, q, p]]
def chk_stationary(it):
    P = P_mc(it)
    # solve pi (P - I) = 0 with sum(pi) = 1 by elimination (rows: first two balance equations + normalisation)
    A = [[P[0][0] - 1, P[1][0], P[2][0], 0], [P[0][1], P[1][1] - 1, P[2][1], 0], [1, 1, 1, 1]]
    for c in range(3):
        pv = next(r for r in range(c, 3) if A[r][c] != 0); A[c], A[pv] = A[pv], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(3):
            if r != c: A[r] = [A[r][k] - A[r][c] * A[c][k] for k in range(4)]
    pi = [A[i][3] for i in range(3)]
    return [F(x) for x in key(it).strip("()").split(", ")] == pi
def chk_first_return(it):
    i, n = re.search(r"started in state (\d), returns to state \d for the first time at step (\d+)", it["stem"]).groups(); i = int(i) - 1; n = int(n)
    P = P_mc(it); total = F(0)
    def walk(state, step, prob):
        nonlocal total
        if prob == 0: return
        if step == n: total += prob if state == i else 0; return
        if 0 < step and state == i: return
        for nx in range(3): walk(nx, step + 1, prob * P[state][nx])
    walk(i, 0, F(1)); return F(key(it)) == total
def params(it):
    return [fv(x) for x in re.search(r"Φ₁ = (\S+), Φ₂ = (\S+), θ₁ = (\S+), θ₂ = ([^,]+?)(?:,| then)", it["stem"]).groups()]
def roots_outside(a1, a2):
    if a2 == 0: return a1 == 0 or abs(1 / float(a1)) > 1
    d = cmath.sqrt(float(a1) ** 2 + 4 * float(a2))      # roots of 1 - a1 z - a2 z^2
    zs = [(-float(a1) + s * d) / (2 * float(a2)) for s in (1, -1)]
    return all(abs(z) > 1 + 1e-12 for z in zs)
def chk_statinv(it):
    f1, f2, t1, t2 = params(it); st, iv = roots_outside(f1, f2), roots_outside(t1, t2)
    return key(it) == ["Neither stationary nor invertible", "Invertible but not stationary", "Stationary but not invertible", "Both stationary and invertible"][2 * st + iv]
def chk_pacf(it):
    f1, f2, t1, _ = params(it); f1, f2, t1 = float(f1), float(f2), float(t1)
    H = 8
    if t1:                                       # MA(1): y = e - t1 e(-1)
        rho = [1.0, -t1 / (1 + t1 * t1)] + [0.0] * H
    else:                                        # AR(2) Yule-Walker
        r1 = f1 / (1 - f2) if f2 != 1 else 0.0; rho = [1.0, r1]
        for h in range(2, H + 2): rho.append(f1 * rho[-1] + f2 * rho[-2])
    # Durbin-Levinson
    pacf, phi = [], []
    for h in range(1, H + 1):
        if h == 1: ph = [rho[1]]
        else:
            num_ = rho[h] - sum(phi[j] * rho[h - 1 - j] for j in range(h - 1)); den = 1 - sum(phi[j] * rho[j + 1] for j in range(h - 1))
            a = num_ / den; ph = [phi[j] - a * phi[h - 2 - j] for j in range(h - 1)] + [a]
        phi = ph; pacf.append(ph[-1])
    zero = [abs(x) < 1e-12 for x in pacf]
    if all(zero): want = "α(h) = 0 for all h ≥ 1"
    elif not any(zero): want = "α(h) ≠ 0 for all h ≥ 1"
    else: want = "α(h) = 0 for all h ≥ %d" % (zero.index(True) + 1); assert all(zero[zero.index(True):])
    return key(it) == want
def chk_arima(it):
    f1, f2, t1, t2 = params(it); q = 2 if t2 else (1 if t1 else 0)
    poly = [F(1), -f1, -f2]                       # 1 - f1 z - f2 z^2
    d = 0
    while sum(poly) == 0 and len(poly) > 1:       # root at z = 1: divide by (1 - z)
        new, carry = [], F(0)
        for c in poly[:-1]: carry += c; new.append(carry)
        poly = new; d += 1
    while len(poly) > 1 and poly[-1] == 0: poly.pop()
    p = len(poly) - 1
    want = ("ARIMA(%d, %d, %d) process" % (p, d, q)) if d else ("ARMA(%d, %d) process" % (p, q))
    return key(it) == want
def chk_spec(it):
    sgn, b, s2 = re.search(r"yₜ = εₜ ([+−]) ([\d.]+)εₜ₋₁ has white-noise variance ([\d.]+)", it["stem"]).groups()
    c = float(b) * (1 if sgn == "+" else -1); s2 = float(s2)
    m = re.fullmatch(r"([\d.]+)?\[([\d.]+) ([+−]) ([\d.]+)cos\(2πω\)\](⁻¹)?", key(it))
    sc = float(m.group(1) or 1); a0 = float(m.group(2)); a1 = float(m.group(4)) * (1 if m.group(3) == "+" else -1)
    for w in (0.05, 0.17, 0.31, 0.45):
        truef = s2 * abs(1 + c * cmath.exp(-2j * math.pi * w)) ** 2
        g = sc * (a0 + a1 * math.cos(2 * math.pi * w)); g = 1 / g if m.group(5) else g
        if abs(g - truef) > 1e-9: return False
    return True
CHECK.update({"55125114523": chk_maxexp, "55125114525": chk_extrema, "55125114516": chk_rolle, "55125114507": chk_laplace, "55125114510": chk_wlln,
              "55125114528": chk_bibd, "55125114529": chk_factdf, "55125114531": chk_pps, "55125114545": chk_poisson_unb, "55125114598": chk_stationary,
              "55125114600": chk_first_return, "55125114603": chk_statinv, "55125114607": chk_pacf, "55125114606": chk_arima, "55125114604": chk_spec})

# ---------------------------------------------------------------------------------------------- batch 3 checks
# Conceptual items. Where a rule decides the answer it is re-run here by a different method (BFS / Kosaraju for chain
# structure, Cramer's rule for passage times, characteristic polynomial of f(A), numerical integration for densities and
# expectations). Fact-based items (matching, founding years, R output) are checked against this file's own fact tables,
# which were written separately from the generator's; R output is also re-run when Rscript is available.
import os, shutil, subprocess, tempfile
def parse_mat(s):
    rows = re.findall(r"\[([^\[\]]+)\]", s)
    return [[F(x.strip().replace("−", "-")) for x in r.split(",")] for r in rows]
def mat_in(stem): return parse_mat(re.search(r"P = (\[\[.*?\]\])", stem).group(1))
def bfs_reach(P, s):
    seen, st = {s}, [s]
    while st:
        u = st.pop()
        for v in range(len(P)):
            if P[u][v] > 0 and v not in seen: seen.add(v); st.append(v)
    return seen
def sccs(P):
    n = len(P); order, seen = [], set()
    def dfs(u, G, out):
        stack = [(u, iter(range(n)))]; seen.add(u)
        while stack:
            x, it_ = stack[-1]
            for v in it_:
                if G(x, v) and v not in seen: seen.add(v); stack.append((v, iter(range(n)))); break
            else: stack.pop(); out.append(x)
    for u in range(n):
        if u not in seen: dfs(u, lambda a, b: P[a][b] > 0, order)
    seen.clear(); comps = []
    for u in reversed(order):
        if u not in seen: c = []; dfs(u, lambda a, b: P[b][a] > 0, c); comps.append(sorted(c))
    return sorted(comps)
def period_bfs(P, s):
    # period = gcd of (level(u) + 1 - level(v)) over edges u->v inside the class reachable from s
    lvl = {s: 0}; q = [s]; g = 0; comp = [c for c in sccs(P) if s in c][0]
    while q:
        u = q.pop(0)
        for v in comp:
            if P[u][v] > 0:
                if v not in lvl: lvl[v] = lvl[u] + 1; q.append(v)
                else: g = math.gcd(g, lvl[u] + 1 - lvl[v])
    return abs(g)
def chk_irred(it):
    P = mat_in(it["stem"]); cs = sccs(P); irr = len(cs) == 1
    pers = {period_bfs(P, c[0]) for c in cs}; assert len(pers) == 1; d = pers.pop()
    return key(it) == ("Irreducible" if irr else "Reducible") + (" and periodic" if d > 1 else " and aperiodic")
def chk_classes(it):
    P = mat_in(it["stem"])
    return key(it) == ", ".join("{" + ", ".join(str(i + 1) for i in c) + "}" for c in sccs(P))
def chk_meanpass(it):
    p = fv(re.search(r"with p = ([\d/.]+) and q", it["stem"]).group(1)); q = 1 - p; P = [[q, p, 0], [q, 0, p], [0, q, p]]
    m = re.search(r"mean recurrence time of state (\d)", it["stem"])
    if m:
        j = int(m.group(1)) - 1; r = p / q; w = [F(1), r, r * r]; want = sum(w) / w[j]          # Kac: 1/pi_j
    else:
        j, i = [int(x) - 1 for x in re.search(r"reach state (\d) for the first time, starting from state (\d)", it["stem"]).groups()]
        o = [k for k in range(3) if k != j]
        a11, a12, a21, a22 = 1 - P[o[0]][o[0]], -P[o[0]][o[1]], -P[o[1]][o[0]], 1 - P[o[1]][o[1]]
        det = a11 * a22 - a12 * a21                                                              # Cramer's rule, right side (1, 1)
        sol = {o[0]: (a22 - a12) / det, o[1]: (a11 - a21) / det}; want = sol[i]
    return F(key(it).replace("−", "-")) == want
def parse_poly(t):
    t = t.replace(" ", "").replace("−", "-"); c = [F(0)] * 4
    for term in re.findall(r"[+-]?[^+-]+", t):
        mm_ = re.fullmatch(r"([+-]?)(\(?[\d/]*\)?)(x[²³]?)?", term); sgn = -1 if mm_.group(1) == "-" else 1
        co = mm_.group(2).strip("()"); co = F(co) if co else F(1); pw_ = {None: 0, "x": 1, "x²": 2, "x³": 3}[mm_.group(3)]
        c[pw_] += sgn * co
    return c
def pv_(c, x): return sum(a * x ** k for k, a in enumerate(c))
def pd_(c): return [k * c[k] for k in range(1, len(c))] + [F(0)]
def chk_piecewise(it):
    m = re.search(r"Given f\(x\) = (.*?) for (\S+) ≤ x ≤ (\S+), and f\(x\) = (.*?) for \S+ < x ≤ (\S+), consider", it["stem"])
    g1, a, c, g2, b = parse_poly(m.group(1)), fv(m.group(2)), fv(m.group(3)), parse_poly(m.group(4)), fv(m.group(5))
    cont = pv_(g1, c) == pv_(g2, c); diff = cont and pv_(pd_(g1), c) == pv_(pd_(g2), c); rolle = diff and pv_(g1, a) == pv_(g2, b)
    tr = [L for L, t in (("A", diff), ("B", not diff), ("C", rolle), ("D", not rolle)) if t]
    return key(it) == ", ".join(tr) + " only"
def mmul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def minv(A): d = A[0][0] * A[1][1] - A[0][1] * A[1][0]; return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]
def chk_eigen(it):
    A = parse_mat(re.search(r"A = (\[\[.*?\]\])", it["stem"]).group(1)); I = [[F(1), F(0)], [F(0), F(1)]]
    lam = fv(re.search(r"has λ = (\S+) as an eigenvalue", it["stem"]).group(1)); f = re.search(r"eigenvalue of (.*)\?$", it["stem"]).group(1)
    add = lambda X, Y, s=1: [[X[i][j] + s * Y[i][j] for j in range(2)] for i in range(2)]
    sc = lambda c, X: [[c * X[i][j] for j in range(2)] for i in range(2)]
    M = {"A⁻¹": lambda: minv(A), "A²": lambda: mmul(A, A), "A − 2I": lambda: add(A, sc(2, I), -1), "3A + I": lambda: add(sc(3, A), I),
         "A′ (the transpose of A)": lambda: [[A[j][i] for j in range(2)] for i in range(2)], "A² − A": lambda: add(mmul(A, A), A, -1),
         "(A − I)⁻¹": lambda: minv(add(A, I, -1)), "A³": lambda: mmul(mmul(A, A), A), "2A⁻¹": lambda: sc(2, minv(A))}[f]()
    tr = M[0][0] + M[1][1]; det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    is_eig = lambda x: x * x - tr * x + det == 0
    vals = [F(o.replace("−", "-")) for o in it["options"]]
    # lam must be an eigenvalue of A; the key is an eigenvalue of f(A); no other option is
    trA = A[0][0] + A[1][1]; detA = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return lam * lam - trA * lam + detA == 0 and is_eig(F(key(it).replace("−", "-"))) and sum(map(is_eig, vals)) == 1
def chk_ident(it):
    e1 = set(map(int, re.findall(r"β₁(\d)", it["stem"].translate(str.maketrans("₀₁₂₃", "0123")).replace("β1", "β₁"))))
    s = it["stem"].translate(str.maketrans("₀₁₂₃", "0123"))
    e1 = set(int(x) for x in re.findall(r"β1(\d) x", s)); e2 = set(int(x) for x in re.findall(r"β2(\d) x", s))
    allx = e1 | e2
    ok1 = len(allx - e1) >= 1 and any(x in e2 for x in allx - e1); ok2 = len(allx - e2) >= 1 and any(x in e1 for x in allx - e2)
    want = {(True, True): "Both (i) and (ii) are identified", (True, False): "(i) is identified but (ii) is not",
            (False, True): "(ii) is identified but (i) is not", (False, False): "Both (i) and (ii) are unidentified"}[(ok1, ok2)]
    return key(it) == want
def coef(t): t = t.strip("()"); return F(t) if t else F(1)
def chk_shiftexp(it):
    s = it["stem"]; m = re.search(r"f\(x \| θ\) = (\(?[\d/]*\)?)e\^\(−", s); lam = coef(m.group(1))
    sts = re.search(r"Consider: A\. (.*)\. B\. (.*)\. C\. (.*)\. D\. (.*)\. Choose", s).groups()
    def over(t):
        if t == "1/n": return F(1)
        m_ = re.fullmatch(r"(\d+)/n", t)
        if m_: return F(int(m_.group(1)))
        m_ = re.fullmatch(r"1/\((\d+)n\)", t); return F(1, int(m_.group(1)))
    def truth(x):
        m_ = re.fullmatch(r"X̄ₙ →ᵖ θ \+ (\S+)", x)
        if m_: return F(m_.group(1)) == 1 / lam
        if x == "X̄ₙ →ᵖ θ": return False
        m_ = re.fullmatch(r"If Y = min\(X₁, …, Xₙ\), then f\(y\) = (\(?[\d/]*\)?)n e\^\(−(\(?[\d/]*\)?)n\(y − θ\)\), y ≥ θ", x)
        if m_: return coef(m_.group(1)) == lam and coef(m_.group(2)) == lam
        m_ = re.fullmatch(r"V\(X̄ₙ\) = (1/n|\d+/n|1/\(\d+n\))", x)
        if m_: return over(m_.group(1)) == 1 / lam ** 2
        m_ = re.fullmatch(r"V\(X̄ₙ\) = (\(?[\d/]*\)?)n", x)
        if m_: return False                                   # grows with n: never the variance of a mean
        if x == "min(X₁, …, Xₙ) →ᵖ θ": return True
        m_ = re.fullmatch(r"E\[min\(X₁, …, Xₙ\)\] = θ \+ (.+)", x)
        if m_: return over(m_.group(1)) == 1 / lam
        if x == "E[min(X₁, …, Xₙ)] = θ": return False
        raise AssertionError(x)
    tr = [L for L, x in zip("ABCD", sts) if truth(x)]
    return key(it) == ("A, B, C, D" if len(tr) == 4 else ", ".join(tr) + " only")
def expr_val(e, env):
    t = e.replace("−", "-").replace("²", "^2").replace("^", "**").replace("e**(", "EXP(").replace("Φ(", "PHI(").replace("φ(", "PDF(")
    t = re.sub(r"(?<=[\dθλpμcm)])(?=[θλpμcm(]|EXP|PHI|PDF)", "*", t)
    for k, v in env.items(): t = t.replace(k, "(%r)" % v)
    return eval(t, {"EXP": math.exp, "PHI": lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2))), "PDF": lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)})
def chk_umvue(it):
    s = it["stem"]; env = {"θ": 2.3, "λ": 0.7, "p": 0.3, "μ": 0.4, "c": 1.1, "m": 3}
    th, la, p_, mu, c, m_ = env["θ"], env["λ"], env["p"], env["μ"], env["c"], env["m"]
    if "exponential with mean θ" in s: want = math.exp(-c / th)                                      # P(X1 > c), integral of e^(-x/θ)/θ
    elif "exponential with pdf λe^(−λx)" in s: want = 1 - math.exp(-la * c)
    elif "Poisson(λ)" in s and "X₁ = 0," in s: want = math.exp(-la)
    elif "Poisson(λ)" in s and "X₁ = 1," in s: want = la * math.exp(-la)
    elif "Poisson(λ)" in s and "X₁ ≥ 1" in s: want = 1 - math.exp(-la)
    elif "Bernoulli(p)" in s: want = p_ * p_
    elif "Binomial(m, p)" in s: want = comb(m_, 0) * (1 - p_) ** m_
    elif "N(μ, 1)" in s: want = 0.5 * (1 + math.erf((c - mu) / math.sqrt(2)))
    elif "Uniform(0, θ)" in s: want = c / th
    elif "geometric" in s: want = p_
    else: raise AssertionError(s)
    vals = [expr_val(o, env) for o in it["options"]]
    return abs(expr_val(key(it), env) - want) < 1e-12 and sum(abs(v - want) < 1e-9 for v in vals) == 1
def chk_sprt(it):
    a, b, which = re.search(r"α = (\S+) and type II error β = (\S+), .*approximation for the (upper|lower) boundary", it["stem"]).groups()
    a, b = fv(a), fv(b); want = (1 - b) / a if which == "upper" else b / (1 - a)
    return F(key(it)) == want
# joint densities: (support test, density) and numerical evaluation of each statement on a fine grid
JD = {"f(x, y) = (1/4)(1 + xy) for |x| < 1, |y| < 1": ((-1, 1, -1, 1), lambda x, y: (1 + x * y) / 4),
      "f(x, y) = 4xy for 0 < x < 1, 0 < y < 1": ((0, 1, 0, 1), lambda x, y: 4 * x * y),
      "f(x, y) = x + y for 0 < x < 1, 0 < y < 1": ((0, 1, 0, 1), lambda x, y: x + y),
      "f(x, y) = 2 for 0 < x < y < 1": ((0, 1, 0, 1), lambda x, y: 2.0 if x < y else 0.0),
      "f(x, y) = e^(−(x + y)) for x > 0, y > 0": ((0, 14, 0, 14), lambda x, y: math.exp(-x - y)),
      "f(x, y) = 6x for 0 < x < y < 1": ((0, 1, 0, 1), lambda x, y: 6 * x if x < y else 0.0),
      "f(x, y) = (3/2)(x² + y²) for 0 < x < 1, 0 < y < 1": ((0, 1, 0, 1), lambda x, y: 1.5 * (x * x + y * y)),
      "f(x, y) = 8xy for 0 < x < y < 1": ((0, 1, 0, 1), lambda x, y: 8 * x * y if x < y else 0.0),
      "f(x, y) = 1/2 for |x| + |y| < 1": ((-1, 1, -1, 1), lambda x, y: 0.5 if abs(x) + abs(y) < 1 else 0.0),
      "f(x, y) = 2e^(−x − 2y) for x > 0, y > 0": ((0, 14, 0, 14), lambda x, y: 2 * math.exp(-x - 2 * y))}
def chk_joint(it):
    s = it["stem"]; dens = re.search(r"joint pdf (.*?) \(and 0 otherwise\)", s).group(1); (x0, x1, y0, y1), f = JD[dens]
    N = 400 if x1 - x0 < 5 else 700; hx = (x1 - x0) / N; hy = (y1 - y0) / N
    xs = [x0 + hx * (i + 0.5) for i in range(N)]; ys = [y0 + hy * (j + 0.5) for j in range(N)]
    G = [[f(x, y) for y in ys] for x in xs]
    tot = sum(map(sum, G)) * hx * hy; assert abs(tot - 1) < 2e-2, (dens, tot)
    fx = [sum(r) * hy for r in G]; fy = [sum(G[i][j] for i in range(N)) * hx for j in range(N)]
    E = lambda g: sum(g(xs[i], ys[j]) * G[i][j] for i in range(N) for j in range(N)) * hx * hy
    EX, EY, EXY = E(lambda x, y: x), E(lambda x, y: y), E(lambda x, y: x * y)
    indep = max(abs(G[i][j] - fx[i] * fy[j]) for i in range(0, N, 15) for j in range(0, N, 15)) < 5e-2
    def num(t): return float(F(t.replace("−", "-")))
    def truth(st):
        if st in ("X and Y are independent",): return indep
        if st == "f(x, y) factorises, so X and Y are independent": return indep
        if st == "Cov(X, Y) = 0": return abs(EXY - EX * EY) < 5e-3
        if st == "E(XY) = E(X)E(Y)": return abs(EXY - EX * EY) < 5e-3
        if st == "X + Y has a gamma distribution with shape 2":     # compare P(X + Y <= 1) with the Gamma(2, 1) cdf 1 - 2/e
            return abs(E(lambda x, y: 1.0 if x + y < 1 - 1e-12 else (0.5 if abs(x + y - 1) < 1e-12 else 0.0)) - (1 - 2 / math.e)) < 1e-2
        m = re.fullmatch(r"(E\(XY\)|E\(X\)|E\(Y\)|E\(X²\)|P\(X > Y\)|P\(X < Y\)) = (\S+)", st)
        if m:
            g = {"E(XY)": lambda x, y: x * y, "E(X)": lambda x, y: x, "E(Y)": lambda x, y: y, "E(X²)": lambda x, y: x * x,
                 "P(X > Y)": lambda x, y: 1.0 if x > y else (0.5 if x == y else 0.0), "P(X < Y)": lambda x, y: 1.0 if x < y else (0.5 if x == y else 0.0)}[m.group(1)]
            return abs(E(g) - num(m.group(2))) < 1e-2
        m = re.fullmatch(r"f\((x|y)\) = (.*) for .*", st)
        if m:
            var, ex_ = m.group(1), m.group(2).replace("−", "-").replace("²", "**2").replace("³", "**3").replace("|x|", "abs(x)").replace("(3/2)x", "(3/2)*x")
            ex_ = re.sub(r"(\d)([xy(])", r"\1*\2", ex_).replace(")(", ")*(").replace("x(", "x*(")
            grid, marg = (xs, fx) if var == "x" else (ys, fy)
            return max(abs(eval(ex_, {var: g, "abs": abs}) - m_) for g, m_ in list(zip(grid, marg))[5:-5:20]) < 3e-2
        raise AssertionError(st)
    sts = re.search(r"Consider: A\. (.*)\. B\. (.*)\. C\. (.*)\. D\. (.*)\. Choose", s).groups()
    tr = [L for L, st in zip("ABCD", sts) if truth(st)]
    return key(it) == ("A, B, C, D" if len(tr) == 4 else ", ".join(tr) + " only")
R_OUT = {"f(3)|x * y": "30", "x <<- 5": "5", "b = a * 2": "9", "x[x > 2]": "7", "for (i in 1:n)": "10", "h(x)": "5", "1:4 * 1:2": "16", "n * f(n - 1)": "24", "x[2] <- 10": "6", "g <- function() a * 2": "10"}
RS = shutil.which("Rscript") or next((p for p in [r"C:\Program Files\R\R-4.5.1\bin\Rscript.exe"] if os.path.exists(p)), None)
def chk_rprog(it):
    code = "\n".join(l[2:] for l in it["stem"].split("\n")[1:-1])
    want = [v for k, v in R_OUT.items() if all(part in code for part in k.split("|"))]; assert len(want) == 1, code
    if RS:
        with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as fh: fh.write(code + "\n")
        out = subprocess.run([RS, "-e", "cat(source('%s', echo=FALSE)$value)" % fh.name.replace("\\", "/")], capture_output=True, text=True).stdout.strip()
        os.unlink(fh.name); assert out == want[0], (out, want)
    return key(it) == want[0]
FACTS = {  # written independently of the generator's tables
 "P. C. Mahalanobis": "D² distance in multivariate analysis", "R. C. Bose": "Partially balanced incomplete block designs", "S. N. Roy": "Union–intersection principle in multivariate testing",
 "D. G. Horvitz and D. J. Thompson": "Unbiased estimator for unequal-probability sampling without replacement", "R. A. Fisher": "Analysis of variance and maximum likelihood",
 "J. Neyman": "Theory of confidence intervals", "Karl Pearson": "Chi-square goodness-of-fit test", "W. S. Gosset": "Student's t distribution",
 "C. R. Rao": "Cramér–Rao inequality and the Rao–Blackwell theorem", "A. Wald": "Sequential probability ratio test", "A. N. Kolmogorov": "Axiomatic foundation of probability",
 "H. Hotelling": "T² statistic and principal components", "C. Spearman": "Rank correlation coefficient", "F. Wilcoxon": "Signed-rank and rank-sum tests",
 "G. E. P. Box and G. M. Jenkins": "ARIMA model building", "J. Durbin and G. S. Watson": "Test for first-order autocorrelation of regression residuals",
 "M. H. Hansen and W. N. Hurwitz": "Estimator for PPS sampling with replacement", "Des Raj": "Ordered estimator in PPS sampling without replacement",
 "C. F. Gauss": "Method of least squares", "W. H. Kruskal and W. A. Wallis": "Rank-based one-way analysis of variance",
 "Simple random sampling": "Homogeneous population", "Stratified random sampling": "Heterogeneous population that splits into homogeneous groups",
 "Cluster sampling": "No list of elementary units is available", "Sampling with varying probabilities (PPS)": "Units of very different sizes, giving larger units more weight",
 "Systematic sampling": "Every k-th unit from an ordered list after a random start", "Multistage sampling": "Large, widely spread population sampled in successive stages",
 "Double (two-phase) sampling": "Auxiliary information collected first on a large preliminary sample", "Quota sampling": "Non-probability method: interviewers fill fixed numbers per category",
 "Ratio estimation": "Auxiliary variable roughly proportional to the study variable (line through the origin)", "Regression estimation": "Linear relation with a non-zero intercept between study and auxiliary variables",
 "Inverse sampling": "Sampling continues until a fixed number of units with a rare attribute is found", "Snowball sampling": "Respondents recruit further respondents from a hidden population",
 "Chi-square test": "Homogeneity or independence in a contingency table", "Wilcoxon signed-rank test": "Two related (paired) samples", "Mann–Whitney U test": "Two independent samples",
 "Kruskal–Wallis test": "Several independent samples: rank version of one-way ANOVA", "Friedman test": "Several related samples in blocks: rank version of two-way ANOVA",
 "Kolmogorov–Smirnov one-sample test": "Goodness of fit to a fully specified continuous distribution", "Run test": "Randomness of a sequence", "Sign test": "Median of a single population using only signs",
 "Spearman's rank correlation": "Monotone association between two variables", "McNemar test": "Change in paired binary (yes/no) responses", "Median test": "Equality of medians of independent samples",
 "Kendall's coefficient of concordance W": "Agreement among several judges ranking the same objects"}
def chk_match(it):
    m = re.search(r"LIST-I \([^)]*\): (.*)\. LIST-II \([^)]*\): (.*)\. Choose", it["stem"])
    left = [x.split(". ", 1)[1] for x in m.group(1).split("; ")]; right = {x.split(". ", 1)[0]: x.split(". ", 1)[1] for x in m.group(2).split("; ")}
    inv = {v: k for k, v in right.items()}
    return key(it) == ", ".join("%s-%s" % ("ABCD"[i], inv[FACTS[l]]) for i, l in enumerate(left))
YEARS = {"Indian Statistical Institute (ISI)": 1931, "National Sample Survey (NSS)": 1950, "Central Statistical Organisation (CSO)": 1951, "Indian Statistical Service (ISS)": 1961,
         "Ministry of Statistics and Programme Implementation (MoSPI)": 1999, "National Statistical Commission (NSC)": 2006, "NITI Aayog": 2015, "National Statistical Office (NSO)": 2019}
def chk_orgs(it):
    body = re.search(r"latest: (.*)\. Choose", it["stem"]).group(1)
    parts = re.split(r"(?:^| )([A-E])\. ", body)[1:]; lab = dict(zip(parts[0::2], parts[1::2]))
    return key(it) == ", ".join(sorted(lab, key=lambda L: YEARS[lab[L].strip()]))
CHECK.update({"55125114582": chk_irred, "55125114583": chk_classes, "55125114601": chk_meanpass, "55125114524": chk_piecewise, "55125114519": chk_eigen,
              "55125114562": chk_ident, "55125114514": chk_shiftexp, "55125114538": chk_umvue, "55125114552": chk_sprt, "55125114512": chk_joint,
              "55125114589": chk_rprog, "55125114593": chk_match, "55125114535": chk_match, "55125114554": chk_match, "55125114590": chk_orgs})

by = defaultdict(list)
for it in items: by[it["srcQid"]].append(it)
assert set(by) == set(CHECK), set(by) ^ set(CHECK)
for qid, vs in by.items():
    assert qid in src, qid
    assert len(vs) == 10, (qid, len(vs))
    spread = Counter(v["answer"] for v in vs); assert set(spread) == set("ABCD") and max(spread.values()) <= 3, (qid, spread)
    for n, it in enumerate(sorted(vs, key=lambda v: v["id"]), 1):
        assert it["id"] == "j26v-id%s-%02d" % (qid[-6:], n) and allids[it["id"]] == 1, it["id"]
        assert it["format"] == "single" and len(it["options"]) == 4 and len(set(it["options"])) == 4, it["id"]
        nums = [val(o) for o in it["options"]]; assert len(set(map(str, nums))) == 4, (it["id"], it["options"])
        assert not {"youMarked", "responseSheet"} & set(it), it["id"]
        assert len(it["explanation"]) >= 150 and "Trap:" in it["explanation"], it["id"]
        assert not re.search(r"(^|[ (\[,])-[0-9]", it["stem"] + " " + " ".join(it["options"]) + " " + it["explanation"]), ("ASCII minus", it["id"])
        assert CHECK[qid](it), (it["id"], it["stem"], it["options"], it["answer"])
print("PASS: %d variants of %d June 2026 questions; every key recomputed from its stem" % (len(items), len(by)))
