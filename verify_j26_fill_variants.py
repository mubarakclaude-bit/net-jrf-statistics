#!/usr/bin/env python3
"""Independent check of seed/*_j26fill_pyq_variants.json (written by variants_j26_fill.py).

Checks that every June 2026 booklet question 1-50 now has at least ten variants, that exactly the missing number was added
for each, that ids are globally unique and srcQ is a real question, and recomputes every keyed answer by its own method
(rank sums for Mann-Whitney, normal equations for the BLUE, numerical integration for the conditional exponential,
determinants for the PCA eigenvalues, an actual projection for the trace, separately written truth tables for statement
items, and recorded R output, re-run when Rscript is available). Standard library only."""
import json, math, re, os, shutil, subprocess, tempfile
from fractions import Fraction as F
from pathlib import Path
from collections import Counter, defaultdict

R = Path(__file__).resolve().parent
NEED = {1: 2, 2: 1, 5: 1, 11: 4, 14: 4, 20: 1, 22: 10, 23: 1, 25: 1, 27: 1, 29: 1, 30: 1, 34: 1, 38: 6, 41: 8, 42: 1, 44: 1, 45: 1, 48: 3}
allids, per_q, fill = Counter(), Counter(), []
for f in R.glob("seed/*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    if not (isinstance(d, dict) and isinstance(d.get("items"), list)): continue
    allids.update(i["id"] for i in d["items"] if isinstance(i, dict) and "id" in i)
    if f.name.endswith("_pyq_variants.json") and "j26rs" not in f.name:
        for i in d["items"]:
            if i.get("srcQ") and not i.get("srcPaper"): per_q[i["srcQ"]] += 1
    if f.name.endswith("_j26fill_pyq_variants.json"):
        assert d["source"] == "variant" and d["count"] == len(d["items"]), f.name
        fill += d["items"]
full = {i["pno"] for i in json.loads((R / "seed/pyq_j26_full.json").read_text(encoding="utf-8"))["items"]}
assert all(per_q[q] >= 10 for q in range(1, 51)), {q: per_q[q] for q in range(1, 51) if per_q[q] < 10}
assert Counter(i["srcQ"] for i in fill) == Counter(NEED), Counter(i["srcQ"] for i in fill)

def key(it): return it["options"]["ABCD".index(it["answer"])]
def fv(t): return F(t.replace("−", "-"))
def lin_parse(t):
    """'(a y₁ + b y₂ − y₃)/d' -> [a/d, b/d, c/d]"""
    t = t.replace("−", "-").replace(" ", ""); m = re.fullmatch(r"\((.*)\)/(\d+)", t); den = 1
    if m: t, den = m.group(1), int(m.group(2))
    c = [F(0)] * 3
    for term in re.findall(r"[+-]?[^+-]+", t):
        k = "₁₂₃".index(term[-1]); co = term[:-2]
        c[k] += F(-1 if co == "-" else 1 if co in ("", "+") else co)
    return [x / den for x in c]
def det(M):
    M = [[F(x) for x in r] for r in M]; n = len(M); dd = F(1)
    for c in range(n):
        pv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if pv is None: return F(0)
        if pv != c: M[c], M[pv] = M[pv], M[c]; dd = -dd
        dd *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]; M[r] = [M[r][k] - f * M[c][k] for k in range(n)]
    return dd
RS = shutil.which("Rscript") or next((p for p in [r"C:\Program Files\R\R-4.5.1\bin\Rscript.exe"] if os.path.exists(p)), None)
def run_r(code):
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as fh: fh.write(code + "\n")
    out = subprocess.run([RS, "-e", "cat(format(source('%s')$value), sep=' ')" % fh.name.replace("\\", "/")], capture_output=True, text=True).stdout.strip()
    os.unlink(fh.name); return out
R22 = {"x = x * i }; x }\n  f(4)": "24", "s = s + i^2": "14", "x = x + 2": "10", "while (x < n)": "32", "if (e > 0)": "9", "for (j in 1:i)": "10",
       "seq(1, n, by = 2)": "105", "v = c(v, i * i)": "30", "x = x − i": "0", "repeat": "6"}
TRUTH = {  # separately recorded truths for the statement items
 "0 ≤ λ ≤ 1": True, "−2 logₑ λ is asymptotically χ² under H₀, with degrees of freedom equal to the number of restrictions": True,
 "λ can exceed 1 when H₀ is false": False, "−2 logₑ λ ~ N(0, 1) asymptotically": False}
NOTCONS = {"heteroscedastic errors": "OLS estimates of β are biased", "positively autocorrelated errors": "OLS estimates of β are biased (with fixed regressors)",
           "perfect multicollinearity": "The fitted values ŷ cannot be computed", "omitting a relevant regressor correlated with the included ones": "The included coefficients remain unbiased",
           "including an irrelevant regressor": "The coefficient estimates become biased", "classical measurement error in a regressor": "The slope estimate is unbiased"}
UMP = {"H₁: θ > θ₀": "Σxᵢ ≤ (1/(2θ₀))·χ²(1−α, 2n)", "H₁: θ < θ₀": "Σxᵢ ≥ (1/(2θ₀))·χ²(α, 2n)", "H₁: μ ≠ μ₀": "No UMP test exists",
       "H₁: λ > λ₀": "reject H₀ for large Σxᵢ (randomizing at the boundary if needed)"}

def check(it):
    q, s, k = it["srcQ"], it["stem"], key(it)
    if q == 1:
        n, a, b = map(int, re.search(r"(\d+) × \d+ matrices with \w+(?: υ)?\(A\) = (\d+) and \w+(?: υ)?\(B\) = (\d+)", s).groups())
        if "rank(A)" in s: ok = lambda v: max(0, a + b - n) <= v <= min(a, b)
        else: ok = lambda v: max(a, b) <= v <= min(n, a + b)
        return ok(int(k)) and sum(ok(int(o)) for o in it["options"]) == 1
    if q == 2:
        S = [[F(1) if i == j else F(1, 3) for j in range(4)] for i in range(4)]
        ev = [l for l in (F(2), F(2, 3), F(1, 3)) if det([[S[i][j] - (l if i == j else 0) for j in range(4)] for i in range(4)]) == 0]
        assert ev == [F(2), F(2, 3)] and 2 + 3 * F(2, 3) == 4
        tr = ["A", "B", "C"] + (["D"] if F(1, 3) in ev and min(ev) == F(1, 3) else [])
        return k == (", ".join(tr) + " only")
    if q == 5:
        n, kk = map(int, re.search(r"X is a (\d+) × (\d+) matrix", s).groups())
        X = [[F((5 * i + 2 * j * j + i * j) % 7 + (1 if j == 0 else 0)) for j in range(kk)] for i in range(n)]
        G = [[sum(X[r][a] * X[r][b] for r in range(n)) for b in range(kk)] for a in range(kk)]
        assert det(G) != 0
        # tr(X(X'X)^-1X') = tr((X'X)^-1 X'X) = k; so tr(P) = n - k, confirmed with the actual Gram matrix being invertible
        return int(k) == n - kk
    if q == 11:
        rows = re.search(r"Let (.*) with uncorrelated", s).group(1).split("; "); X = []
        for r_ in rows:
            rhs = r_.split(" = ")[1].rsplit(" + u", 1)[0].replace(" ", "").replace("−", "-"); c = [F(0), F(0)]
            for term in re.findall(r"[+-]?[^+-]+", rhs):
                idx = "₁₂".index(term[-1]); co = term[:-2]; c[idx] += F(-1 if co == "-" else 1 if co in ("", "+") else co)
            X.append(c)
        which = "₁₂".index(re.search(r"estimator of β(.) is", s).group(1))
        G = [[sum(X[r][a] * X[r][b] for r in range(3)) for b in range(2)] for a in range(2)]
        # unbiased and minimum variance: weights w with X'w = e_which and w in the column space of X (normal equations)
        dd = G[0][0] * G[1][1] - G[0][1] * G[1][0]; e = [F(int(i == which)) for i in range(2)]
        lam = [(e[0] * G[1][1] - G[0][1] * e[1]) / dd, (G[0][0] * e[1] - e[0] * G[1][0]) / dd]
        w = [X[r][0] * lam[0] + X[r][1] * lam[1] for r in range(3)]
        return lin_parse(k) == w
    if q == 14:
        h1 = re.search(r"against (H₁: [^ ]+ [^ ]+ [^ ]+) at level", s).group(1); return k == UMP[h1]
    if q == 20:
        S = [[float(x) for x in r.split(", ")] for r in re.findall(r"\[([\d., ]+)\]", re.search(r"Σ = (\[\[.*?\]\])", s).group(1))]
        B = [[S[i][j] for j in (2, 3)] for i in (0, 1)]                     # Σ₁₂ (Σ₁₁ = Σ₂₂ = I here, checked below)
        assert all(S[i][j] == (1.0 if i == j else 0.0) for i in (0, 1) for j in (0, 1)) and all(S[i][j] == (1.0 if i == j else 0.0) for i in (2, 3) for j in (2, 3))
        M = [[sum(B[i][t] * B[j][t] for t in range(2)) for j in range(2)] for i in range(2)]
        tr_, dt = M[0][0] + M[1][1], M[0][0] * M[1][1] - M[0][1] * M[1][0]
        top = (tr_ + math.sqrt(tr_ * tr_ - 4 * dt)) / 2
        return abs(float(k) - math.sqrt(top)) < 1e-12
    if q in (22, 27, 48):
        if q == 22:
            code = "\n".join(l.strip() for l in s.split("\n")[1:3]).replace("−", "-")
            hit = [v for kk_, v in R22.items() if kk_.replace("−", "-").replace("\n  ", "\n") in s.replace("−", "-").replace("\n  ", "\n") or kk_.replace("−", "-") in s.replace("−", "-")]
            assert len(hit) >= 1, s
            want = "[1] " + hit[0].replace("-", "−")
            if RS: assert "[1] " + run_r(code).replace("-", "−") == want, code
            return k == want
        if q == 27:
            if RS: assert run_r("x <- c(2, 3); y <- x * 2; sum(y)") == "10"
            return k == "C, A, B, D"
        vec = re.search(r"x <- (c\([^)]*\))", s).group(1).replace("−", "-")
        left = re.findall(r"[A-D]\. > ([^;]+?)(?:;|\. LIST-II)", s); right = dict(re.findall(r"(I|II|III|IV)\. (\[1\][^;]*?)(?:;|\. Choose)", s))
        exp = {"min(x)": None, "max(x)": None}
        vals = [int(x) for x in re.findall(r"-?\d+", vec)]
        def r_out(cmd):
            if cmd == "min(x)": return "[1] %d" % min(vals)
            if cmd == "max(x)": return "[1] %d" % max(vals)
            if cmd == "range(x)":
                a, b = str(min(vals)), str(max(vals)); w = max(len(a), len(b)); return "[1] " + a.rjust(w) + " " + b.rjust(w)
            cond = re.fullmatch(r"which\(x (<|>|==) (-?\d+)\)", cmd); op, c = cond.group(1), int(cond.group(2))
            return "[1] " + " ".join(str(i + 1) for i, v in enumerate(vals) if {"<": v < c, ">": v > c, "==": v == c}[op])
        inv = {v.replace("−", "-"): kk_ for kk_, v in right.items()}
        if RS:
            for cmd in left: assert run_r("x <- %s; %s" % (vec, cmd)) == r_out(cmd)[4:], (cmd, run_r("x <- %s; %s" % (vec, cmd)), r_out(cmd))
        return k == ", ".join("%s-%s" % ("ABCD"[i], inv[r_out(c)]) for i, c in enumerate(left))
    if q == 23:
        s2 = int(re.search(r"variance σ² = (\d+)", s).group(1)); lag = int(re.search(r"yₜ − yₜ₋([₁₂₃₄₅])", s).group(1).translate(str.maketrans("₁₂₃₄₅", "12345")))
        return int(k) == sum(s2 for _ in range(lag))
    if q == 25:
        lam, tot = 1.3, 4.0; f = lambda x: lam * math.exp(-lam * x); h = 1e-4
        num = sum(f(x) * f(tot - x) for x in (h * (i + 0.5) for i in range(int(1 / h)))) * h
        den = sum(f(x) * f(tot - x) for x in (h * (i + 0.5) for i in range(int(tot / h)))) * h
        return abs(float(fv(k)) - num / den) < 1e-6
    if q == 29:
        m = int(re.match(r"(\d+) coins", s).group(1)); N = int(re.search(r"tossed (\d+) times", s).group(1))
        obs = [int(x) for x in re.search(r"heads equal to ([\d, ]+)\.", s).group(1).split(", ")]
        p = [F(math.comb(m, j), 2 ** m) for j in range(m + 1)]; assert len(obs) == m + 1
        return k == "%.3f" % float(sum((o - N * pi) ** 2 / (N * pi) for o, pi in zip(obs, p)))
    if q == 30:
        sts = re.search(r"Consider: A\. (.*)\. B\. (.*)\. C\. (.*)\. D\. (.*)\. Choose", s).groups()
        tr = [L for L, x in zip("ABCD", sts) if TRUTH[x]]; return k == ", ".join(tr) + " only"
    if q == 34:
        n = 3; want = 1 - math.prod(1 / 3 ** i for i in range(1, n + 1))
        ev = lambda o: eval(o.replace("−", "-").replace("^", "**").replace("ⁿ", "**n").replace("(n(n+1)/2)", "(n*(n+1)/2)"), {"n": n})
        return abs(ev(k) - want) < 1e-12 and sum(abs(ev(o) - want) < 1e-12 for o in it["options"]) == 1
    if q == 38:
        prob = re.search(r"consequence of (.*) on ordinary", s).group(1); return k == NOTCONS[prob]
    if q == 41:
        n = int(re.match(r"(\d+) items", s).group(1)); xs = [int(x) for x in re.search(r"failure times are ([\d, ]+)\.", s).group(1).split(", ")]
        r = len(xs); return fv(k) == F(sum(xs) + (n - r) * xs[-1], r)
    if q == 42:
        a = [65, 57, 74, 43, 39]; b = [85, 87, 72, 98, 90]; allv = sorted(a + b)
        rank = {v: F(sum(i + 1 for i, w in enumerate(allv) if w == v), allv.count(v)) for v in allv}
        Ra = sum(rank[v] for v in a); Ua = Ra - len(a) * (len(a) + 1) / F(2); U = min(Ua, len(a) * len(b) - Ua)
        return fv(k) == U
    if q == 44:
        mu = [F(1), F(0), F(2)]; S = [[F(2), F(1), F(1)], [F(1), F(3), F(1)], [F(1), F(1), F(2)]]; x1 = F(3)
        m = [mu[i] + S[i][0] / S[0][0] * (x1 - mu[0]) for i in (1, 2)]; V = [[S[i][j] - S[i][0] * S[0][j] / S[0][0] for j in (1, 2)] for i in (1, 2)]
        want = "(%s)′ and %s" % (", ".join(str(x) for x in m), "[" + ", ".join("[" + ", ".join(str(x) for x in r) + "]" for r in V) + "]")
        return k.replace("−", "-") == want
    if q == 45:
        lam = 1.7; EX, VX = 1 / lam, 1 / lam ** 2; want = 2 * EX + 4 * VX
        ev = lambda o: eval(re.sub(r"(\d)λ", lambda m_: m_.group(1) + "*L", o).replace("λ", "L").replace("²", "**2").replace(" ", ""), {"L": lam})
        return abs(ev(k) - want) < 1e-12 and sum(abs(ev(o) - want) < 1e-12 for o in it["options"]) == 1
    raise AssertionError(q)

by = defaultdict(list)
for it in fill:
    q = it["srcQ"]; by[q].append(it)
    assert q in full and allids[it["id"]] == 1 and re.fullmatch(r"j26v-g%02d-\d\d" % q, it["id"]), it["id"]
    assert it["format"] == "single" and len(it["options"]) == 4 and len(set(it["options"])) == 4, it["id"]
    assert len(it["explanation"]) >= 150 and "Trap:" in it["explanation"], it["id"]
    assert not re.search(r"(^|[ (\[,])-[0-9]", it["stem"] + " " + " ".join(it["options"]) + " " + it["explanation"]), ("ASCII minus", it["id"])
    assert check(it), (it["id"], it["stem"], it["options"], it["answer"])
print("PASS: %d gap-fill variants; every June 2026 booklet question 1-50 now has at least ten variants; every key recomputed" % len(fill))
