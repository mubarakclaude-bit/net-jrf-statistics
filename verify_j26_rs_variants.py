#!/usr/bin/env python3
"""Independent check of seed/*_j26rs_pyq_variants.json (written by variants_j26_rs.py), batches 1 and 2.

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
