#!/usr/bin/env python3
"""Independent check of seed/*_j26rs_pyq_variants.json (written by variants_j26_rs.py).

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
    return float("%.12g" % float(eval(t, {"math": math}))) if "," not in t else o
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
