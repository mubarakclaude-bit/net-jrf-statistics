#!/usr/bin/env python3
"""June 2026 Paper 2: the 50 questions not in seed/pyq_j26_full.json (which holds booklet questions 1-50).

Source: the official NTA response sheet and the official answer key (question ID -> correct option ID) for UGC NET June 2026,
107ST Statistics. The booklet numbers of these 50 are not known, so each item is identified by its official question ID.
This script checks every item against the official key below, the structure of the sets, that no candidate data is
present, that the three questions whose key holds only under a corrected reading carry a keyNote, and recomputes every
numerical answer. Standard library only."""
import json, glob, math, re
from fractions import Fraction as F
from pathlib import Path

R = Path(__file__).resolve().parent
OFFICIAL = {  # official question ID -> correct option (1-4), from the NTA answer key
 "55125114590": 4, "55125114538": 3, "55125114512": 2, "55125114584": 4, "55125114582": 2, "55125114583": 2, "55125114510": 2,
 "55125114514": 1, "55125114581": 2, "55125114519": 2, "55125114516": 4, "55125114593": 3, "55125114527": 1, "55125114556": 4,
 "55125114523": 4, "55125114563": 2, "55125114559": 4, "55125114533": 1, "55125114561": 2, "55125114562": 3, "55125114558": 2,
 "55125114531": 3, "55125114568": 3, "55125114552": 2, "55125114525": 2, "55125114530": 3, "55125114507": 1, "55125114529": 1,
 "55125114534": 3, "55125114535": 4, "55125114585": 2, "55125114526": 3, "55125114508": 4, "55125114554": 1, "55125114545": 4,
 "55125114524": 4, "55125114528": 2, "55125114543": 4, "55125114589": 2, "55125114536": 1, "55125114597": 2, "55125114598": 4,
 "55125114601": 4, "55125114599": 1, "55125114600": 3, "55125114603": 2, "55125114607": 3, "55125114604": 2, "55125114605": 3,
 "55125114606": 4}
KEYNOTE = {"55125114512", "55125114598", "55125114604"}

items = {}
for f in sorted(R.glob("seed/*_pyq_j26_rs.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    assert d["source"] == "pyq" and d["topicId"] is None and d["count"] == d["clean"] == len(d["items"]), f.name
    assert f.name == d["moduleId"] + "_pyq_j26_rs.json", f.name
    for it in d["items"]:
        assert it["id"] not in items, it["id"]
        items[it["id"]] = it
assert len(items) == 50 == len(OFFICIAL), len(items)
full = json.loads((R / "seed/pyq_j26_full.json").read_text(encoding="utf-8"))
assert not set(items) & {i["id"] for i in full["items"]}
for it in items.values():
    qid = it["questionId"]
    assert it["id"] == "j26-id" + qid[-6:] and qid in OFFICIAL, it["id"]
    assert it["format"] == "single" and len(it["options"]) == 4 and len(set(it["options"])) == 4, it["id"]
    assert it["answer"] == "ABCD"[OFFICIAL[qid] - 1], (it["id"], it["answer"])
    assert ("Official answer: %s (" % it["answer"]) in it["explanation"] and len(it["explanation"]) >= 200 and " Working: " in it["explanation"], it["id"]
    assert not {"youMarked", "responseSheet"} & set(it), it["id"]
    assert not re.search(r"Q\d+\s*$", it["topic"]), it["id"]          # never read as a booklet number by tools/papers.js
    assert ("keyNote" in it) == (qid in KEYNOTE), it["id"]
raw = " ".join(p.read_text(encoding="utf-8") for p in R.glob("seed/*_pyq_j26_rs.json"))
assert not re.search(r"KL\d{6,}|\b2605\d{8}\b|you marked", raw, re.I)
by = {it["questionId"]: it for it in items.values()}
opt = lambda q: by[q]["options"]["ABCD".index(by[q]["answer"])]

# ---- numerical answers, recomputed ----
assert opt("55125114527") == "7" and F(477 - 177 - 195, 3 * 5) == 7                       # RBD MSE
assert opt("55125114523") == "2^(1/4)" and max(x / 1000 * (1 - x / 1000) for x in range(1001)) == 0.25
assert opt("55125114563") == "0.25, 1.50" and F(132, 528) == F(1, 4) and 2 * (1 - F(1, 4)) == F(3, 2)
assert opt("55125114558") == "0.51" and round(1 - 0.45 * 49 / 45, 2) == 0.51
assert opt("55125114568") == "6.25" and 4 / (1 - 0.6 ** 2) == 6.25
assert opt("55125114530") == "35" and 50 * 350 * 2 / (150 * 2 + 350 * 2) == 35             # Neyman, S1 = S2 = 2
assert opt("55125114585") == "2⁵/3⁴" and 4 * F(1, 3) * F(2, 3) ** 3 == F(2 ** 5, 3 ** 4)
assert opt("55125114526") == "66.7365" and round((66870 / 3) / (5344 / 16), 4) == 66.7365
assert opt("55125114508") == "48" and 3 * 4 ** 2 == 48                                    # N(2,4): mu4 = 3 sigma^4
assert opt("55125114589") == "9"
assert opt("55125114605") == "(0.6)^h/0.64" and abs(1 / (1 - 0.36) - 1 / 0.64) < 1e-12
# Laplace: |X| ~ Exp(1); numeric integration of E|X| and E|X|^2
h = 1e-3; xs = [h * (k + 0.5) for k in range(40000)]
m1 = sum(x * math.exp(-x) for x in xs) * h; m2 = sum(x * x * math.exp(-x) for x in xs) * h
assert opt("55125114507") == "1, 1" and abs(m1 - 1) < 1e-4 and abs(m2 - m1 ** 2 - 1) < 1e-3
# gambler's ruin against an infinitely rich adversary
assert opt("55125114584") == "(1/3)^100" and F(1, 4) / F(3, 4) == F(1, 3)
# Poisson process, memoryless: P(T > 6 | T > 4) = e^(-2*2)
assert opt("55125114581") == "e^(−4)" and abs(math.exp(-12) / math.exp(-8) - math.exp(-4)) < 1e-15
# Markov chain P = [[q,p,0],[q,0,p],[0,q,p]] at an arbitrary p
def mat(p):
    q = 1 - p; return [[q, p, 0], [q, 0, p], [0, q, p]]
mul = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
for p in (F(1, 3), F(2, 5), F(1, 2)):
    P = mat(p); q = 1 - p; P3 = mul(mul(P, P), P)
    assert P3[0][1] == p * q * (1 + p)                                                     # 55125114597
    pi = [F(1), p / q, (p / q) ** 2]; s = sum(pi); pi = [x / s for x in pi]
    assert [sum(pi[i] * P[i][j] for i in range(3)) for j in range(3)] == pi
    assert (pi == [F(1, 3)] * 3) == (p == F(1, 2))                                         # 55125114598: key needs p = 1/2
    f115 = q ** 4 * p; assert f115 == P[0][0] ** 4 * P[0][1]                               # 55125114599
    assert P[1][1] == 0 and P[2][0] == 0                                                   # 55125114600: f11(3) = 0
assert opt("55125114601") == "p⁻¹" and opt("55125114600") == "0" and opt("55125114599") == "q⁴p"
assert "keyNote" in by["55125114598"]
# r23.1 is not in this set; BIBD |NN'| = rk(r-lambda)^(v-1), checked on the (7,3,1) Fano plane
blocks = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
N = [[1 if t in b else 0 for b in blocks] for t in range(7)]
NN = [[sum(N[i][k] * N[j][k] for k in range(7)) for j in range(7)] for i in range(7)]
def det(M):
    M = [[F(x) for x in row] for row in M]; n = len(M); d = F(1)
    for c in range(n):
        pv = next(r for r in range(c, n) if M[r][c] != 0)
        if pv != c: M[c], M[pv] = M[pv], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]; M[r] = [M[r][k] - f * M[c][k] for k in range(n)]
    return d
assert det(NN) == 3 * 3 * (3 - 1) ** 6 and opt("55125114528") == "rk(r − λ)^(v−1)"     # r = k = 3, lambda = 1, v = 7
# MA(1) spectrum: the printed minus sign gives 1.49 - 1.4cos; the key is the plus-sign form (keyNote)
w = 0.1; b = 0.7
assert abs(abs(1 - b * complex(math.cos(2 * math.pi * w), -math.sin(2 * math.pi * w))) ** 2 - (1.49 - 1.4 * math.cos(2 * math.pi * w))) < 1e-12
assert opt("55125114604") == "[1.49 + 1.4cos(2πω)]" and "keyNote" in by["55125114604"]
# ARMA roots: 1 - 0.6z - 0.4z^2 = (1 - z)(1 + 0.4z); 1 - 0.6z - 0.4z^2 MA part of Q146 also has a unit root
assert abs(1 - 0.6 - 0.4) < 1e-12 and opt("55125114606") == "ARIMA(1, 1, 1) process" and opt("55125114603") == "Stationary but not invertible"
# density (1/4)(1 + xy): f(x) = 1/2 and E(X^2 Y^2) = 1/9 (keyNote explains the printed 'cy')
g = [(-1 + (i + 0.5) / 200) for i in range(400)]
ex2y2 = sum(x * x * y * y * (1 + x * y) / 4 for x in g for y in g) * (1 / 200) ** 2
assert abs(ex2y2 - 1 / 9) < 1e-3 and opt("55125114512") == "B, C, D only" and "keyNote" in by["55125114512"]
print("PASS: 50 June 2026 Paper 2 questions match the official key; structure, privacy, keyNotes and the numerical answers checked")
