#!/usr/bin/env python3
"""Practice variants of the June 2026 Paper 2 questions that are identified by official question ID
(seed/<module>_pyq_j26_rs.json). Batch 1: thirteen computational questions, ten variants each.

Every number is computed here, never typed: each generator returns the stem, the correct option, three distractors that
come from named, common mistakes, and an explanation built from the same computed values. The script refuses to write a
variant whose four options are not distinct. Key positions rotate so each question's answers are spread over A-D.
Output: seed/<module>_j26rs_pyq_variants.json (one file per module; the _pyq_variants suffix makes them variant banks).
Run:  python -X utf8 variants_j26_rs.py      Check:  python -X utf8 verify_j26_rs_variants.py"""
import json, math
from fractions import Fraction as F
from pathlib import Path
from math import comb

R = Path(__file__).resolve().parent
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

def fr(x):
    """Exact display: integer, terminating decimal, or a/b, with a typographic minus sign."""
    return _fr(x).replace("-", "−")
def _fr(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    d = x.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    if d == 1:
        s = ("%.10f" % float(x)).rstrip("0").rstrip(".")
        return s
    return "%d/%d" % (x.numerator, x.denominator)

def ff(x):
    """Probability as a fraction (never a decimal), so (1/2)^n and (0.5)^n can never both appear."""
    x = F(x); return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
def d1(x):
    """Allocation display: integer, or one decimal place."""
    x = F(x); return str(x.numerator) if x.denominator == 1 else ("%.1f" % float(x))
def dec(x, k=4): return (("%." + str(k) + "f") % float(x)).replace("-", "−")
def sup(n): return str(n).translate(SUP)
def pw(base, e): return "(%s)^%s" % (base, e)

# --------------------------------------------------------------------------------------------- generators
def g_ruin():            # 55125114584: gambler's ruin against an infinitely rich adversary
    out = []
    for p, a in [(F(2,3),10),(F(3,5),20),(F(4,5),5),(F(3,4),50),(F(5,6),8),(F(2,3),25),(F(1,2),30),(F(2,5),10),(F(7,10),12),(F(3,5),15)]:
        q = 1 - p
        if p > q:
            r = q / p; corr = pw(ff(r), a)
            dis = [pw(ff(q), a), "1 − %s" % pw(ff(p), a), "1"]
            why = ("The game favours the gambler (p = %s > q = %s), so ruin is not certain. Against an opponent with unlimited money, "
                   "P(ruin starting from Rs. a) = (q/p)^a. Here q/p = %s/%s = %s and a = %d, so the ruin probability is %s.") % (ff(p), ff(q), ff(q), ff(p), ff(r), a, corr)
        else:
            corr = "1"
            dis = ([pw(ff(p / q), a), pw(ff(q), a), "1 − %s" % pw(ff(p), a)] if p < q else [pw("1/2", a), "1 − %s" % pw("1/2", a), "0"])
            why = ("The game is %s (p = %s ≤ q = %s). Against an opponent with unlimited money the gambler's fortune drifts "
                   "down or is a fair random walk, which hits 0 with probability 1 from any finite starting capital, so ruin is certain.") % ("fair" if p == q else "unfavourable", ff(p), ff(q))
        stem = ("A gambler starts with Rs. %d against an adversary with unlimited capital. On each play he wins Rs. 1 with probability %s "
                "and loses Rs. 1 otherwise. The probability of the gambler's ultimate ruin is") % (a, ff(p))
        out.append((stem, corr, dis, why + " Trap: (q)^a or 1 − p^a ignores that the walk can move up and come back down many times."))
    return out

def g_memoryless():      # 55125114581
    out = []
    for lam, s, t in [(3,1,3),(1,3,5),(4,2,3),(F(1,2),4,10),(2,1,4),(F(3,2),2,6),(5,2,3),(1,2,6),(F(1,3),3,9),(2,5,8)]:
        d = t - s; e = lambda x: "e^(−%s)" % fr(x)
        corr = e(lam * d)
        dis = [e(lam * t), e(lam * s), "1 − " + e(lam * d)]
        stem = ("Customers arrive at a counter as a Poisson process with rate %s per minute. Given that the time between two successive "
                "arrivals is more than %s minutes, the probability that it is more than %s minutes is") % (fr(lam), fr(s), fr(t))
        why = ("Gaps between Poisson arrivals are exponential with rate λ = %s, and the exponential distribution is memoryless: having waited %s "
               "minutes, the extra wait is again exponential. So P(T > %s | T > %s) = P(T > %s) = e^(−λ·%s) = %s. "
               "Trap: e^(−λ·%s) uses the full %s minutes and ignores the condition.") % (fr(lam), fr(s), fr(t), fr(s), fr(d), fr(d), corr, fr(t), fr(t))
        out.append((stem, corr, dis, why))
    return out

def g_poisson_split():   # 55125114585
    out = []
    for a, b, n, k in [(1,2,4,1),(1,1,5,2),(2,1,3,2),(1,3,4,2),(1,2,5,3),(3,1,4,3),(1,4,3,1),(2,3,4,1),(1,1,6,3),(1,2,3,0)]:
        pr = F(a, a + b); val = comb(n, k) * pr ** k * (1 - pr) ** (n - k)
        swap = comb(n, k) * (1 - pr) ** k * pr ** (n - k)
        nobin = pr ** k * (1 - pr) ** (n - k)
        alt = [fr(F(k, n)), fr(pr), fr(F(1, n + 1))]
        dis = [fr(swap), fr(nobin)] + [x for x in alt if x not in (fr(val), fr(swap), fr(nobin))]
        dis = list(dict.fromkeys(d for d in dis if d != fr(val)))[:3]
        rate = lambda c: ("λ" if c == 1 else "%dλ" % c)
        stem = ("Let N₁(t) and N₂(t) be independent Poisson processes with rates %s and %s respectively. "
                "Then P(N₁(t) = %d | N₁(t) + N₂(t) = %d) is") % (rate(a), rate(b), k, n)
        why = ("Given that %d events occurred in total, each one came from the first process independently with probability %s/(%s + %s) = %s. "
               "So N₁(t) given the total is Binomial(%d, %s): P = C(%d,%d)(%s)^%d(%s)^%d = %s. The time t and λ cancel out. "
               "Trap: swapping the two probabilities gives %s; dropping the binomial coefficient gives %s.") % (
               n, rate(a), rate(a), rate(b), fr(pr), n, fr(pr), n, k, fr(pr), k, fr(1 - pr), n - k, fr(val), fr(swap), fr(nobin))
        out.append((stem, fr(val), dis, why))
    return out

def chain(p):
    p = F(p); q = 1 - p
    return [[q, p, 0], [q, 0, p], [0, q, p]]
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def mpow(A, n):
    M = [[F(int(i == j)) for j in range(3)] for i in range(3)]
    for _ in range(n): M = mm(M, A)
    return M
MC = "A three-state Markov chain has transition matrix P = [[q, p, 0], [q, 0, p], [0, q, p]] with p = %s and q = 1 − p. "

def g_nstep():           # 55125114597
    out = []
    for p, i, j, n in [(F(1,3),1,2,3),(F(1,2),1,2,3),(F(2,5),1,3,2),(F(1,4),2,1,2),(F(3,5),1,2,2),(F(2,3),2,3,3),(F(1,2),3,1,3),(F(1,3),1,1,3),(F(3,4),2,2,2),(F(2,5),3,2,3)]:
        P = chain(p); Pn = mpow(P, n); val = Pn[i-1][j-1]
        cands = [mpow(P, n - 1)[i-1][j-1], mpow(P, n + 1)[i-1][j-1], Pn[j-1][i-1], P[i-1][j-1] ** n] + Pn[i-1] + mpow(P, n + 2)[i-1]
        dis = list(dict.fromkeys(fr(c) for c in cands if fr(c) != fr(val)))[:3]
        stem = MC % fr(p) + "The %d-step transition probability p%s%s⁽%s⁾ is" % (n, "₀₁₂₃"[i], "₀₁₂₃"[j], sup(n))
        row = ", ".join(fr(x) for x in mpow(P, n - 1)[i-1])
        why = ("An n-step transition probability is an entry of Pⁿ: p%s%s⁽%s⁾ is row %d, column %d of P^%d. Row %d of P^%d is (%s); "
               "multiplying it by column %d of P gives %s. Trap: (p%s%s)^%d multiplies one-step probabilities along a single path and misses the other paths.") % (
               "₀₁₂₃"[i], "₀₁₂₃"[j], sup(n), i, j, n, i, n - 1, row, j, fr(val), "₀₁₂₃"[i], "₀₁₂₃"[j], n)
        out.append((stem, fr(val), dis, why))
    return out

def first_passage(P, i, j, n):
    """f_ij^(n): first visit to j at step n, starting from i (taboo probabilities)."""
    v = [F(int(k == i - 1)) for k in range(3)]
    for step in range(1, n + 1):
        nv = [sum(v[a] * P[a][b] for a in range(3)) for b in range(3)]
        if step == n: return nv[j - 1]
        nv[j - 1] = F(0); v = nv

def g_first_passage():   # 55125114599
    out = []
    for p, i, j, n in [(F(1,3),1,2,4),(F(1,2),1,2,5),(F(2,5),3,2,3),(F(1,4),1,2,3),(F(3,5),3,2,4),(F(2,3),1,3,3),(F(1,2),3,1,3),(F(1,3),1,2,2),(F(3,4),3,2,3),(F(2,5),2,1,3)]:
        P = chain(p); val = first_passage(P, i, j, n)
        cands = [mpow(P, n)[i-1][j-1], first_passage(P, i, j, n - 1), first_passage(P, i, j, n + 1), P[i-1][j-1] ** n]
        dis = list(dict.fromkeys(fr(c) for c in cands if c != val))
        k = 2
        while len(dis) < 3: dis = list(dict.fromkeys(dis + [fr(first_passage(P, i, j, n + k))])); dis = [d for d in dis if d != fr(val)]; k += 1
        dis = dis[:3]
        stem = MC % fr(p) + "The first-passage probability f%s%s⁽%s⁾ (first visit to state %d at step %d, starting from state %d) is" % ("₀₁₂₃"[i], "₀₁₂₃"[j], sup(n), j, n, i)
        why = ("A first passage at step %d means the chain is NOT in state %d at steps 1 to %d and IS there at step %d. Track the probability of "
               "every state step by step, setting state %d to zero after each step before step %d (a 'taboo' calculation). This gives f%s%s⁽%s⁾ = %s. "
               "Trap: the ordinary %d-step probability p%s%s⁽%s⁾ = %s also counts paths that reached state %d earlier.") % (
               n, j, n - 1, n, j, n, "₀₁₂₃"[i], "₀₁₂₃"[j], sup(n), fr(val), n, "₀₁₂₃"[i], "₀₁₂₃"[j], sup(n), fr(mpow(P, n)[i-1][j-1]), j)
        out.append((stem, fr(val), dis, why))
    return out

def g_ar1_var():         # 55125114568
    out = []
    for phi, s2 in [(F(1,2),3),(F(4,5),9),(F(-3,5),16),(F(3,10),91),(F(-1,2),6),(F(7,10),51),(F(1,5),24),(F(9,10),19),(F(-4,5),18),(F(2,5),21)]:
        v = s2 / (1 - phi ** 2)
        dis = [fr(s2 / (1 - phi)), fr(s2 / (1 + phi ** 2)), fr(s2 * (1 - phi ** 2))]
        dis = [d for d in dict.fromkeys(dis) if d != fr(v)]
        if len(dis) < 3: dis.append(fr(s2 / (1 - abs(phi))) if fr(s2 / (1 - abs(phi))) not in dis + [fr(v)] else fr(s2))
        stem = "For the AR(1) process yₜ = %s yₜ₋₁ + εₜ with E(εₜ) = 0 and E(εₜ²) = %s, the variance of yₜ is" % (fr(phi), fr(s2))
        why = ("Since |φ| = %s < 1 the process is stationary, so Var(yₜ) = Var(yₜ₋₁) = γ₀. Taking variances of both sides: γ₀ = φ²γ₀ + σ², "
               "so γ₀ = σ²/(1 − φ²) = %s/(1 − %s) = %s. Trap: σ²/(1 − φ) = %s forgets to square φ.") % (fr(abs(phi)), fr(s2), fr(phi ** 2), fr(v), fr(s2 / (1 - phi)))
        out.append((stem, fr(v), dis[:3], why))
    return out

def g_ar1_acov():        # 55125114605
    out = []
    for phi, s2, h in [(F(1,2),3,2),(F(4,5),9,1),(F(-1,2),6,3),(F(3,5),16,2),(F(1,5),24,1),(F(9,10),19,2),(F(-3,5),32,1),(F(2,5),21,2),(F(7,10),51,1),(F(1,2),9,3)]:
        g0 = s2 / (1 - phi ** 2); v = phi ** h * g0
        dis = [fr(phi ** h), fr(phi ** h * s2), fr(phi ** h * s2 / (1 - phi))]
        dis = [d for d in dict.fromkeys(dis) if d != fr(v)]
        if len(dis) < 3: dis.append(fr(g0))
        stem = ("For the AR(1) process yₜ = %s yₜ₋₁ + εₜ, where {εₜ} is white noise with variance %s, the autocovariance at lag %d, γ(%d), is") % (fr(phi), fr(s2), h, h)
        why = ("For a stationary AR(1), γ(0) = σ²/(1 − φ²) = %s/(1 − %s) = %s, and each extra lag multiplies the autocovariance by φ: "
               "γ(h) = φʰγ(0) = (%s)^%d × %s = %s. Trap: φʰ = %s is the autocorrelation ρ(h), not the autocovariance.") % (
               fr(s2), fr(phi ** 2), fr(g0), fr(phi), h, fr(g0), fr(v), fr(phi ** h))
        out.append((stem, fr(v), dis[:3], why))
    return out

def g_rbd():             # 55125114527
    out = []
    for t, b, sst, ssb, tot in [(4,6,177,195,477),(3,5,64,40,152),(5,4,120,57,309),(4,5,90,72,234),(3,6,50,35,125),(5,3,88,40,176),(6,4,150,30,270),(4,4,63,45,153),(3,4,30,18,78),(5,5,200,96,392)]:
        sse = tot - sst - ssb; df = (t - 1) * (b - 1); mse = F(sse, df)
        dis = [fr(F(sse, t * b - t)), fr(F(sse, t * b - 1)), fr(F(sst, t - 1))]
        dis = [d for d in dict.fromkeys(dis) if d != fr(mse)]
        if len(dis) < 3: dis.append(fr(F(ssb, b - 1)))
        stem = ("In a randomized block design with %d treatments and %d blocks, the treatment sum of squares is %d, the block sum of squares is %d "
                "and the total sum of squares is %d. The error mean square is") % (t, b, sst, ssb, tot)
        why = ("In an RBD, Total SS = Treatment SS + Block SS + Error SS, so Error SS = %d − %d − %d = %d. The error degrees of freedom are "
               "(t − 1)(b − 1) = %d × %d = %d, so MSE = %d/%d = %s. Trap: dividing by N − t = %d (the CRD error df) forgets that blocks also use degrees of freedom.") % (
               tot, sst, ssb, sse, t - 1, b - 1, df, sse, df, fr(mse), t * b - t)
        out.append((stem, fr(mse), dis[:3], why))
    return out

def g_anova_f():         # 55125114526
    out = []
    for k, n, sstr, sse in [(4,20,66870,5344),(3,15,240,360),(5,25,880,1000),(4,24,150,400),(3,21,120,288),(6,30,1250,1200),(4,16,90,240),(3,12,54,81),(5,20,320,450),(4,28,207,480)]:
        f = (F(sstr, k - 1)) / (F(sse, n - k))
        dis = [dec(1 / f), dec(F(sstr, sse)), dec(F(sstr, k) / F(sse, n - 1))]
        dis = [d for d in dict.fromkeys(dis) if d != dec(f)]
        stem = ("A one-way ANOVA compares %d treatments using %d observations in all. The treatment sum of squares is %d and the error sum of squares is %d. "
                "The calculated F-ratio is") % (k, n, sstr, sse)
        why = ("F = (treatment mean square)/(error mean square). Treatment MS = %d/(%d − 1) = %s; error MS = %d/(%d − %d) = %s. "
               "F = %s ≈ %s. Trap: SS_Tr/SS_E = %s divides sums of squares without their degrees of freedom.") % (
               sstr, k, fr(F(sstr, k - 1)), sse, n, k, fr(F(sse, n - k)), fr(f), dec(f), dec(F(sstr, sse)))
        out.append((stem, dec(f), dis[:3], why))
    return out

def g_neyman():          # 55125114530
    out = []
    for n, N1, N2, S1, S2, ask in [(50,150,350,2,2,2),(60,200,400,3,6,2),(40,100,300,4,2,1),(30,250,250,5,1,1),(70,300,500,2,3,2),(45,120,180,5,5,1),(64,400,300,1,4,1),(36,90,150,4,3,2),(25,200,100,1,3,2),(90,500,250,3,4,1)]:
        tot = N1 * S1 + N2 * S2; nh = [F(n * N1 * S1, tot), F(n * N2 * S2, tot)]
        prop = [F(n * N1, N1 + N2), F(n * N2, N1 + N2)]
        val = nh[ask - 1]
        assert val.denominator == 1, (n, N1, N2, S1, S2)
        dis = [d1(prop[ask - 1]), d1(nh[2 - ask]), d1(F(n, 2))]
        dis = [d for d in dict.fromkeys(dis) if d != d1(val)]
        for extra in [F(n * [N1, N2][ask - 1] * [S1, S2][ask - 1] ** 2, N1 * S1 ** 2 + N2 * S2 ** 2),   # S² in place of S
                      F([N1, N2][ask - 1] * [S1, S2][ask - 1], tot)]:                                     # forgot to multiply by n
            x = d1(extra) if extra > 1 else ("%.2f" % float(extra))
            if len(dis) < 3 and x not in dis + [d1(val)]: dis.append(x)
        stem = ("A stratified random sample of size %d is to be allocated by Neyman allocation between two strata with N₁ = %d, N₂ = %d, S₁ = %d and S₂ = %d. "
                "The number of units to be selected from stratum %d is") % (n, N1, N2, S1, S2, ask)
        why = ("Neyman (optimum, equal-cost) allocation takes nₕ = n·NₕSₕ/ΣNₕSₕ. Here N₁S₁ = %d and N₂S₂ = %d, total %d, so n%s = %d × %d/%d = %s. "
               "Trap: proportional allocation (nₕ ∝ Nₕ) gives %s; it agrees with Neyman only when S₁ = S₂.") % (
               N1 * S1, N2 * S2, tot, "₁₂"[ask - 1], n, [N1 * S1, N2 * S2][ask - 1], tot, d1(val), d1(prop[ask - 1]))
        out.append((stem, d1(val), dis[:3], why))
    return out

def g_adjr2():           # 55125114558
    out = []
    for n, k, r2 in [(50,5,"0.55"),(30,4,"0.60"),(40,6,"0.70"),(25,3,"0.80"),(61,11,"0.50"),(46,6,"0.64"),(21,5,"0.75"),(100,10,"0.30"),(36,6,"0.85"),(51,11,"0.42")]:
        R2 = F(r2); adj = 1 - (1 - R2) * F(n - 1, n - k)
        dis = [dec(1 - (1 - R2) * F(n - 1, n - k - 1), 3), dec(1 - (1 - R2) * F(n, n - k), 3), dec(R2, 3)]
        corr = dec(adj, 3)
        dis = [d for d in dict.fromkeys(dis) if d != corr]
        stem = ("In the linear model y = Xβ + u, y is %d×1 and X is %d×%d (the first column of X is the intercept). If R² = %s, the adjusted R² is (to three decimals)") % (n, n, k, r2)
        why = ("Adjusted R² = 1 − (1 − R²)(n − 1)/(n − k), where k counts every column of X, the intercept included. "
               "Here 1 − (1 − %s) × %d/%d = %s. Trap: using n − k − 1 counts the intercept twice and gives %s.") % (r2, n - 1, n - k, corr, dec(1 - (1 - R2) * F(n - 1, n - k - 1), 3))
        out.append((stem, corr, dis[:3], why))
    return out

def g_dw():              # 55125114563
    out = []
    for s0, s1 in [("5.28","1.32"),("8.00","5.60"),("6.40","−1.60"),("4.50","2.70"),("10.00","1.00"),("7.20","−3.60"),("3.60","0.90"),("9.00","6.30"),("5.00","−1.00"),("12.00","3.00")]:
        S0 = F(s0); S1 = F(s1.replace("−", "-")); rho = S1 / S0; d = 2 * (1 - rho)
        pair = lambda a, b: "%s, %s" % (dec(a, 2), dec(b, 2))
        corr = pair(rho, d)
        dis = [pair(rho, 2 * (1 + rho)), pair(1 - rho, d), pair(rho, 1 - rho)]
        dis = [x for x in dict.fromkeys(dis) if x != corr]
        stem = ("For the model yₜ = α + βxₜ + uₜ with uₜ = ρuₜ₋₁ + εₜ, the OLS residuals eₜ satisfy Σeₜ² ≈ %s and Σeₜeₜ₋₁ ≈ %s for a large n. "
                "The estimated ρ and the Durbin–Watson statistic are, respectively,") % (s0, s1)
        why = ("Estimate ρ by regressing each residual on the previous one: ρ̂ = Σeₜeₜ₋₁/Σeₜ² = %s/%s = %s. For large n the Durbin–Watson statistic "
               "is d ≈ 2(1 − ρ̂) = %s. Trap: 2(1 + ρ̂) has the sign the wrong way round; positive autocorrelation pushes d below 2.") % (s1, s0, dec(rho, 2), dec(d, 2))
        out.append((stem, corr, dis[:3], why))
    return out

def g_mgf():             # 55125114508
    out = []
    asks = ["the fourth central moment of X", "the variance of X", "E(X²)", "the third central moment of X"]
    for i, (mu, s2) in enumerate([(2,4),(1,2),(3,6),(-1,8),(0,10),(4,2),(2,6),(-2,4),(5,8),(1,12)]):
        a = asks[i % 4]; c2 = F(s2, 2)
        if a.startswith("the fourth"): val = 3 * s2 ** 2; dis = [s2 ** 2, 3 * s2, 3 * c2 ** 2]           # sigma^4; 3sigma^2; halving trap
        elif a.startswith("the variance"): val = s2; dis = [c2, 2 * s2, s2 + mu ** 2]                      # halving trap; doubled; E(X^2)
        elif a == "E(X²)": val = s2 + mu ** 2; dis = [s2, mu ** 2, c2 + mu ** 2]                            # variance only; mean^2 only; halving trap
        else: val = 0; dis = [3 * mu * s2, mu ** 3, s2]                                                     # parts of E(X^3); mean^3; variance
        dis = [fr(x) for x in dict.fromkeys(dis) if fr(x) != fr(val)]
        if len(dis) < 3: dis.append(fr(3 * s2 ** 2 if not a.startswith("the fourth") else s2 + mu ** 2))
        lin = ("%dt" % mu) if mu not in (0, 1, -1) else ("t" if mu == 1 else ("−t" if mu == -1 else ""))
        lin = lin.replace("-", "−")
        expo = (lin + " + " if lin else "") + "%st²" % ("" if c2 == 1 else fr(c2))
        stem = "The moment generating function of a random variable X is Mₓ(t) = e^(%s). Then %s is" % (expo, a)
        why = ("e^(μt + σ²t²/2) is the moment generating function of N(μ, σ²). Matching exponents: μ = %s and σ²/2 = %s, so σ² = %d and X ~ N(%s, %d). "
               "For a normal distribution the third central moment is 0, the fourth is 3σ⁴, and E(X²) = σ² + μ². So %s is %s. "
               "Trap: reading the coefficient of t² as σ² (instead of σ²/2) halves the variance.") % (fr(mu), fr(c2), s2, fr(mu), s2, a, fr(val))
        out.append((stem, fr(val), dis[:3], why))
    return out

BATCH = [  # (official question ID, module, generator)
    ("55125114584", "stochastic", g_ruin), ("55125114581", "stochastic", g_memoryless), ("55125114585", "stochastic", g_poisson_split),
    ("55125114597", "stochastic", g_nstep), ("55125114599", "stochastic", g_first_passage),
    ("55125114568", "timeseries", g_ar1_var), ("55125114605", "timeseries", g_ar1_acov),
    ("55125114527", "design", g_rbd), ("55125114526", "design", g_anova_f),
    ("55125114530", "sampling", g_neyman), ("55125114558", "regression", g_adjr2), ("55125114563", "regression", g_dw),
    ("55125114508", "probability", g_mgf)]

BAD = []
import re
def value(o):
    """Numeric value of an option when it is a plain expression (numbers, fractions, powers, e^(...)); otherwise None."""
    t = o.replace("−", "-").replace("^", "**").replace("e**", "math.e**")
    if "," in t or not re.fullmatch(r"[0-9.+\-*/() ]*(math\.e)?[0-9.+\-*/() ]*", t): return None
    try: return float("%.12g" % float(eval(t, {"math": math})))   # 12 significant digits, so tiny powers stay distinct
    except Exception: return None
def build():
    banks = {}
    for qi, (qid, mod, gen) in enumerate(BATCH):
        vs = gen(); assert len(vs) == 10, (qid, len(vs))
        for n, (stem, corr, dis, why) in enumerate(vs, 1):
            pos = (qi + n - 1) % 4
            opts = dis[:pos] + [corr] + dis[pos:]
            vals = [value(o) for o in opts]; nums = [v for v in vals if v is not None]
            if len(dis) != 3 or len(set(opts)) != 4 or len(set(nums)) != len(nums): BAD.append((qid, n, opts)); continue
            banks.setdefault(mod, []).append({
                "id": "j26v-id%s-%02d" % (qid[-6:], n), "format": "single",
                "topic": "June 2026 Paper 2 variant (official question ID %s)" % qid, "srcQid": qid,
                "stem": stem, "options": opts, "answer": "ABCD"[pos], "explanation": why})
    return banks

if __name__ == "__main__":
    B = build()
    if BAD:
        for b in BAD: print("NOT DISTINCT", b)
        raise SystemExit(1)
    for mod, items in sorted(B.items()):
        doc = {"moduleId": mod, "topicId": None, "source": "variant",
               "label": "June 2026 Paper 2 — practice variants of the questions identified by official question ID",
               "count": len(items), "items": items}
        p = R / "seed" / ("%s_j26rs_pyq_variants.json" % mod)
        p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(len(items), p.name)
