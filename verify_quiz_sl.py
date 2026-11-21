# -*- coding: utf-8 -*-
"""Verification for seed/probability_sl_quiz.json (built by quiz_bank_sl.py).

Every answer is recomputed here without reading the item text: by exact fractions, by enumerating the sample space
(dice, coins, subsets, cards, ball transfers), or, for the statement-type and symbolic questions, by testing every
option on random and constructed finite probability spaces and on sample parameter values, so that the keyed option is
the only one that survives. Then the structure is audited the way verify_pyq_distributions.py audits the CSIR banks.

Standard library only.   Run from the repository root:  python verify_quiz_sl.py
"""
import random, re, sys
from fractions import Fraction as Fr
from itertools import product, combinations
from math import comb, factorial

import quiz_bank_sl as B

N, FAILS = [0], []


def ok(cond, what):
    N[0] += 1
    if not cond:
        FAILS.append(what)
        print("FAIL " + what)


items = {x["item"]["id"]: x["item"] for x in B.ITEMS}
L = "ABCD"


def key_value(i):
    it = items[i]
    return it["options"][L.index(it["answer"])]


def only_key(i, truth_by_letter, what):
    """truth_by_letter: {letter: bool}. Exactly the keyed letter is True."""
    want = {Lt: Lt == items[i]["answer"] for Lt in L}
    ok(truth_by_letter == want, "%s: %s (got %s)" % (i, what, truth_by_letter))


def numeric_options(i):
    out = {}
    for Lt, o in zip(L, items[i]["options"]):
        try:
            out[Lt] = Fr(o)
        except ValueError:                               # a text option such as 'None of these'
            pass
    return out


def key_is(i, exact, tol=Fr(0)):
    vals = numeric_options(i)
    hits = [Lt for Lt, v in vals.items() if abs(v - exact) <= tol]
    ok(hits == [items[i]["answer"]], "%s: computed %s matches only the key (matches %s)" % (i, exact, hits))


rng = random.Random(20261121)


def rand_space(n):
    w = [Fr(rng.randint(1, 20)) for _ in range(n)]
    s = sum(w)
    return [x / s for x in w]


def P(space, ev):
    return sum(space[a] for a in ev)


# ------------------------------------------------------------------ Day 1
key_is("slq-d1-01", (Fr(2, 10) * Fr(4, 10)) / Fr(4, 10))                       # 0.2; 'None' is not numeric
ok(key_value("slq-d1-01") == "0.2", "d1-01 key reads 0.2")

# d1-02: test every option's three parts on random spaces
def chain_ok(opt, A, Bv, sp, case):
    pA, pB, pAB, pAuB = P(sp, A), P(sp, Bv), P(sp, A & Bv), P(sp, A | Bv)
    parts = {
        "A": [pAB >= pAuB >= pA, pA + pB >= pA <= pAB, pA <= pAB >= 0],
        "B": [pAB <= pAuB <= pA, pAB <= 0, pAB >= pAuB <= 1],
        "C": [pAuB <= pAB <= pA, pAB >= pAuB >= 0, pA <= pAB <= pAuB],
        "D": [pAuB >= pA >= pAB, pAuB >= pA >= pA * pB, pAuB >= pA >= 0],
    }
    return parts[opt][case]
holds = {Lt: True for Lt in L}
for _ in range(400):
    sp = rand_space(4)                                   # atoms: AB, A only, B only, neither
    A, Bv = {0, 1}, {0, 2}
    pa, pb = rand_space(2)[0], rand_space(2)[0]          # independent: product space
    ind = [pa * pb, pa * (1 - pb), (1 - pa) * pb, (1 - pa) * (1 - pb)]
    dis = rand_space(3)                                  # disjoint: atoms A only, B only, neither
    for Lt in L:
        holds[Lt] &= chain_ok(Lt, A, Bv, sp, 0) and chain_ok(Lt, A, Bv, ind, 1) and chain_ok(Lt, {0}, {1}, dis, 2)
only_key("slq-d1-02", holds, "only the keyed set holds in all three cases")

tails = [s.count("T") for s in product("HT", repeat=2)]
key_is("slq-d1-03", Fr(sum(tails), 4))
key_is("slq-d1-04", Fr(9, 10) ** 10 + 10 * Fr(1, 10) * Fr(9, 10) ** 9, tol=Fr(5, 10000))
red = Fr(2, 6) * Fr(4, 12) + Fr(4, 6) * Fr(3, 8)
key_is("slq-d1-05", (Fr(1, 6) * Fr(4, 12)) / red)

def d1_06_opts(m, p):
    return {"A": p / (1 + (m - 1) * p), "B": (m * p - 1) / (m * p), "C": m * p / (1 + p * (m - 1)), "D": m * p / (1 + (m + 1) * p)}
match = {Lt: True for Lt in L}
for m, p in [(4, Fr(1, 3)), (5, Fr(2, 7)), (2, Fr(3, 5)), (7, Fr(1, 10))]:
    bayes = p / (p + (1 - p) * Fr(1, m))
    for Lt, v in d1_06_opts(m, p).items():
        match[Lt] &= v == bayes
only_key("slq-d1-06", match, "only the keyed expression equals Bayes at sample (m, p)")

subsets = [set(c) for r in range(11) for c in combinations(range(1, 11), r)]
key_is("slq-d1-07", Fr(sum(1 for s in subsets if {3, 7} <= s), len(subsets)))
urn = ["R"] * 3 + ["K"] * 4 + ["G"] * 3
pairs = [(a, b) for a in range(10) for b in range(10) if a != b]
key_is("slq-d1-08", Fr(sum(1 for a, b in pairs if {urn[a], urn[b]} == {"R", "K"}), len(pairs)))
key_is("slq-d1-09", Fr(13, 52) - Fr(1, 52))

# d1-10: P(A) = 3/4, P(B) = 1/2, t = P(A ∩ B) over its whole feasible range
feasible = [t for t in (Fr(k, 400) for k in range(401))
            if min(t, Fr(3, 4) - t, Fr(1, 2) - t, 1 - (Fr(3, 4) + Fr(1, 2) - t)) >= 0]
ok(min(feasible) == Fr(1, 4) and max(feasible) == Fr(1, 2), "d1-10 feasible range is [1/4, 1/2]")
must = {"A": all(t >= Fr(1, 4) for t in feasible), "B": all(t <= Fr(1, 4) for t in feasible),
        "C": all(t >= Fr(3, 4) for t in feasible), "D": all(t <= Fr(3, 4) for t in feasible)}
it = items["slq-d1-10"]
ok({Lt: it["verdicts"][Lt]["tf"] for Lt in L} == must, "d1-10 verdicts equal the statements that must hold")
ok(it.get("keyNote"), "d1-10 records that the source's key was incomplete")

# ------------------------------------------------------------------ Days 2-3
def need_not_hold(i, opts):
    """opts: letter -> function(space with P(A) = 1) -> bool. The keyed letter fails somewhere; the rest always hold."""
    always = {Lt: True for Lt in L}
    for _ in range(300):
        w = rand_space(2)                                # atoms: A∩B, A∩Bᶜ carry all the mass; Aᶜ atoms weigh 0
        sp = {"AB": w[0], "ABc": w[1], "AcB": Fr(0), "AcBc": Fr(0)}
        for Lt, f in opts.items():
            always[Lt] &= f(sp)
    only_key(i, {Lt: not v for Lt, v in always.items()}, "only the keyed statement can fail when P(A) = 1")

need_not_hold("slq-d23-01", {
    "A": lambda s: s["AB"] == s["AB"] + s["AcB"],
    "B": lambda s: s["ABc"] == s["ABc"] + s["AcBc"],
    "C": lambda s: s["AcB"] == 0,
    "D": lambda s: s["AcBc"] == s["ABc"] + s["AcBc"]})
need_not_hold("slq-d23-02", {
    "A": lambda s: s["AB"] + s["ABc"] + s["AcB"] == 1,
    "B": lambda s: s["AcB"] + s["AcBc"] + s["AB"] == s["AB"] + s["AcB"],
    "C": lambda s: 1 - s["AB"] == s["ABc"] + s["AcBc"],
    "D": lambda s: s["AB"] + s["ABc"] + s["AcBc"] == s["ABc"] + s["AcBc"]})

a, b, ab = Fr(3, 4), Fr(1, 5), Fr(1, 8)
vals = {"A": ab / b == Fr(1, 4), "B": (a - ab) / (1 - b) == Fr(25, 32), "C": (b - ab) / b == Fr(3, 4),
        "D": (1 - (a + b - ab)) / (1 - b) == Fr(7, 16)}
only_key("slq-d23-03", vals, "only the keyed conditional probability is right")

match = {Lt: True for Lt in L}
for _ in range(200):
    sp = rand_space(4)                                   # AB, A only, B only, neither
    al, be, ga = sp[0] + sp[1], sp[0] + sp[2], sp[0]
    target = sp[2]                                       # Aᶜ ∩ B
    for Lt, v in {"A": al * (1 - be), "B": be * (1 - al), "C": (1 - al) * (1 - be), "D": be - ga}.items():
        match[Lt] &= v == target
only_key("slq-d23-04", match, "only the keyed expression equals P(Aᶜ ∩ B) on random spaces")

key_is("slq-d23-05", Fr(5, 10) * Fr(6, 10) + Fr(6, 10) * Fr(4, 10))
match = {Lt: True for Lt in L}
for p, q, r in [(Fr(1, 10), Fr(2, 10), Fr(3, 10)), (Fr(1, 6), Fr(1, 2), Fr(1, 3)), (Fr(4, 5), Fr(1, 9), Fr(2, 7))]:
    post = (p / 3) / ((p + q + r) / 3)
    for Lt, v in {"A": r / (p + q + r), "B": p / (p + q + r), "C": q / (p + q + r), "D": (p + q + r) / 3}.items():
        match[Lt] &= v == post
only_key("slq-d23-06", match, "only the keyed expression is the posterior of the first die")

e, f, d = Fr(1, 3), Fr(2, 5), Fr(1, 5)
union = (e + f + d) / 2
ok(0 <= union - d <= min(e, f), "d23-07 the implied P(E ∩ F) is feasible")
key_is("slq-d23-07", union)
rolls = list(product(range(1, 7), repeat=3))
both = sum(1 for t in rolls if sum(t) % 5 == 0 and sum(t) % 6 == 0)
key_is("slq-d23-08", 1 - Fr(both, len(rolls)))

match = {Lt: True for Lt in L}
for n in range(1, 7):
    unequal = Fr(sum(1 for t in product("HT", repeat=2 * n) if t.count("H") != n), 4 ** n)
    c = Fr(factorial(2 * n), factorial(n) ** 2)
    for Lt, v in {"A": 1 - c * Fr(1, 4 ** n), "B": 1 - c, "C": c * Fr(1, 4 ** n), "D": c}.items():
        match[Lt] &= v == unequal
only_key("slq-d23-09", match, "only the keyed expression equals the enumerated probability for n = 1..6")

# ------------------------------------------------------------------ Day 4
# d4-01: B always holds (Boole, given G); a constructed space breaks the other three
for _ in range(300):
    sp = rand_space(8)                                   # atoms indexed by (e, f, g) bits
    at = list(product((0, 1), repeat=3))
    pG = sum(sp[k] for k, (e_, f_, g_) in enumerate(at) if g_)
    pE_G = sum(sp[k] for k, (e_, f_, g_) in enumerate(at) if g_ and e_) / pG
    pF_G = sum(sp[k] for k, (e_, f_, g_) in enumerate(at) if g_ and f_) / pG
    pNone_G = sum(sp[k] for k, (e_, f_, g_) in enumerate(at) if g_ and not e_ and not f_) / pG
    ok(pNone_G >= 1 - pE_G - pF_G, "d4-01 Boole's bound given G")
# 100 equally likely outcomes inside G (0..99) and 100 inside Ḡ (100..199); E = 0..4, F = 5..9
G, Gc, E, F_ = set(range(100)), set(range(100, 200)), set(range(5)), set(range(5, 10))
cp = lambda X, Y: Fr(len(X & Y), len(Y))
ok(cp(E, G) == Fr(5, 100) and cp(F_, G) == Fr(5, 100), "d4-01 the example meets the givens")
example = {"A": cp(E & F_, G) == Fr(1, 400), "B": cp((G - E) - F_, G) >= Fr(9, 10), "C": cp(E | F_, G) <= Fr(5, 100),
           "D": cp(E | F_, Gc) >= 1 - Fr(1, 400)}
only_key("slq-d4-01", example, "in the constructed space only the keyed statement holds")

A2, B2 = {1, 2}, {2, 3}                                  # three equally likely outcomes
c3 = lambda X, Y: Fr(len(X & Y), len(Y))
ok(c3(A2, B2) == c3(B2, A2) and A2 & B2, "d4-02 the example meets the givens")
example = {"A": A2 < B2, "B": A2 == B2, "C": not (A2 & B2), "D": Fr(len(A2), 3) == Fr(len(B2), 3)}
only_key("slq-d4-02", example, "in the example only the keyed statement holds")
for _ in range(200):                                     # and P(A) = P(B) is forced whenever the condition holds
    sp = rand_space(4); pab, pa_, pb_ = sp[0], sp[0] + sp[1], sp[0] + sp[2]
    if pab / pb_ == pab / pa_:
        ok(pa_ == pb_, "d4-02 condition forces P(A) = P(B)")

nums = range(1, 25)
A4, B4 = {x for x in nums if x % 4 == 0}, {x for x in nums if x % 5 == 0}
single = Fr(len(A4 & B4), len(B4)) + Fr(len(A4 & B4), len(A4))
two = [(x, y) for x in nums for y in nums]
pa4 = Fr(sum(1 for x, y in two if x % 4 == 0), 576); pb4 = Fr(sum(1 for x, y in two if y % 5 == 0), 576)
pab4 = Fr(sum(1 for x, y in two if x % 4 == 0 and y % 5 == 0), 576)
ok(single == pab4 / pb4 + pab4 / pa4, "d4-04 single-draw and two-draw readings agree, as the repaired note says")
key_is("slq-d4-04", single)

deck = [(r, s) for r in range(13) for s in range(4)]
key_is("slq-d4-05", Fr(sum(1 for r, s in deck if r == 0 or s == 0), 52))
q = Fr(5, 6)
series = sum(q ** (4 * k) for k in range(400)) * q ** 3 * Fr(1, 6)       # truncated series, checked against the closed form
closed = q ** 3 * Fr(1, 6) / (1 - q ** 4)
ok(abs(series - closed) < Fr(1, 10 ** 12), "d4-06 geometric series agrees with the closed form")
key_is("slq-d4-06", closed)
pa7, pb7, pabc = Fr(5, 10), Fr(3, 10), Fr(3, 10)
key_is("slq-d4-07", (pa7 - pabc) / (pa7 + (1 - pb7) - pabc))
key_is("slq-d4-08", (Fr(1, 2) * Fr(4, 10)) / (Fr(1, 2) * Fr(4, 10) + Fr(1, 2) * Fr(6, 10)))

# d4-09: full enumeration of the three transfers, with the end state of every box compared to the start
def transfers():
    total = Fr(0)
    for c1 in "WB":
        boxes = [{"W": 4, "B": 5} for _ in range(3)]
        p1 = Fr(boxes[0][c1], 9); boxes[0][c1] -= 1; boxes[1][c1] += 1
        for c2 in "WB":
            b2 = [dict(x) for x in boxes]
            p2 = Fr(b2[1][c2], 10); b2[1][c2] -= 1; b2[2][c2] += 1
            for c3 in "WB":
                b3 = [dict(x) for x in b2]
                p3 = Fr(b3[2][c3], 10); b3[2][c3] -= 1; b3[0][c3] += 1
                if all(x == {"W": 4, "B": 5} for x in b3):
                    total += p1 * p2 * p3
    return total
key_is("slq-d4-09", transfers())
p1, p4 = Fr(1, 4), 1 - Fr(3, 4)
key_is("slq-d4-10", p1 + p4)

# ------------------------------------------------------------------ structure
def letters(txt):
    if txt == "A, B, C and D":
        return "ABCD"
    return "".join(sorted(re.findall(r"[A-D]", txt.replace(" only", ""))))

ok(len(items) == 28, "28 items")
refs = " ".join(it["ref"] for it in items.values())
for day, n in (("Day-1", 10), ("Day-2/3", 9), ("Day-4", 10)):
    missing = [k for k in range(1, n + 1) if not re.search(re.escape(day) + r" quiz Q%d\b" % k, refs)]
    ok(not missing, "every question of the %s quiz is an item or a named repeat (missing %s)" % (day, missing))
for i, it in items.items():
    ok(len(it["explanation"]) >= 40, i + " explanation at least 40 characters")
    ok(it["topic"].startswith("probability-t"), i + " filed under a probability topic")
    ok(len(it["options"]) == 4 and len(set(it["options"])) == 4 and it["answer"] in L, i + " four distinct options and a key")
    for m in re.finditer(r"\b[Oo]ption ([A-D])\b[^.]*?\b(fail|wrong|incorrect|not)\b", it["explanation"]):
        ok(m.group(1) != it["answer"], i + " explanation does not rule out its own answer")
    if it["format"] == "multi":
        truth = "".join(Lt for Lt in L if it["verdicts"][Lt]["tf"])
        ok(letters(it["options"][L.index(it["answer"])]) == truth, i + " keyed combination = true statements")
        ok(sum(1 for o in it["options"] if letters(o) == truth) == 1, i + " exactly one option is the true combination")
ok(B.main(["--check"]) == 0, "seed/probability_sl_quiz.json equals the build output")
keys = [it["answer"] for it in items.values()]
print("answer-key spread: " + ", ".join("%s %d" % (Lt, keys.count(Lt)) for Lt in L))
print("%d checks, %d failed" % (N[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
