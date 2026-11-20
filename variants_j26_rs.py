#!/usr/bin/env python3
"""Practice variants of the June 2026 Paper 2 questions that are identified by official question ID
(seed/<module>_pyq_j26_rs.json). Batch 1: thirteen computational questions; batch 2: fifteen more. Ten variants each.

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

# ------------------------------------------------------------------------------------------------- batch 2 generators
def powstr(a, e):
    """a^e shown as an integer when e is a whole number, otherwise a^(e)."""
    e = F(e)
    if e.denominator == 1: return fr(F(a) ** e.numerator) if e >= 0 else "1/%s" % fr(F(a) ** (-e.numerator))
    return "%s^(%s)" % (fr(a), fr(e))

def g_maxexp():          # 55125114523
    out = []
    for a, c, kind in [(2,1,"max"),(3,2,"max"),(2,4,"max"),(5,2,"min"),(10,1,"max"),(2,3,"min"),(3,4,"max"),(4,3,"max"),(7,2,"min"),(2,5,"max")]:
        if kind == "max":
            corr = powstr(a, F(c * c, 4)); dis = ["1", powstr(a, F(c * c, 2)), powstr(a, c * c)]
            stem = "The maximum value of f(x) = %d^(x(%d − x)), 0 ≤ x ≤ %d, is" % (a, c, c)
            why = ("Because %d > 1, %d^t increases with t, so f is largest where the exponent t = x(%d − x) is largest. That downward parabola peaks at its midpoint "
                   "x = %s, where t = %s. So the maximum is %d^(%s) = %s. Trap: the endpoints x = 0 and x = %d give t = 0 and f = 1, which is the minimum, not the maximum.") % (
                   a, a, c, fr(F(c, 2)), fr(F(c * c, 4)), a, fr(F(c * c, 4)), corr, c)
        else:
            corr = powstr(a, -F(c * c, 4)); dis = ["1", powstr(a, F(c * c, 4)), powstr(a, -F(c * c, 2))]
            stem = "The minimum value of f(x) = %d^(x(x − %d)), 0 ≤ x ≤ %d, is" % (a, c, c)
            why = ("Because %d > 1, f is smallest where the exponent t = x(x − %d) is smallest. That upward parabola is lowest at x = %s, where t = −%s. "
                   "So the minimum is %d^(−%s) = %s. Trap: forgetting the minus sign gives %s, which is larger than f(0) = 1.") % (
                   a, c, fr(F(c, 2)), fr(F(c * c, 4)), a, fr(F(c * c, 4)), corr, powstr(a, F(c * c, 4)))
        out.append((stem, corr, dis, why))
    return out

def xm(r):
    """(x − r) written properly for negative r and r = 0."""
    r = F(r); return "x" if r == 0 else ("(x + %s)" % fr(-r) if r < 0 else "(x − %s)" % fr(r))
def par(v): v = F(v); return "(%s)" % fr(v) if v < 0 else fr(v)
def poly3(s, r1, r2, k):
    """s·[x³ − (3/2)(r1+r2)x² + 3r1r2·x] + k, written with integer coefficients."""
    b = F(-3 * (r1 + r2), 2) * s; c = 3 * r1 * r2 * s; a = s
    def term(coef, pw_, first=False):
        coef = F(coef)
        if coef == 0: return ""
        sign = "−" if coef < 0 else ("" if first else "+")
        mag = abs(coef); m = "" if (mag == 1 and pw_) else fr(mag)
        body = m + {3: "x³", 2: "x²", 1: "x", 0: ""}[pw_]
        return (sign + body) if first else " %s %s" % (sign, body)
    return term(a, 3, True) + term(b, 2) + term(c, 1) + term(k, 0)

def g_extrema():         # 55125114525
    COMBOS = ["A, D only", "B, C only", "A, C only", "B, D only"]
    out = []
    for s, r1, r2, k in [(1,1,3,-8),(1,2,4,1),(-1,1,3,2),(1,-1,1,5),(1,0,2,-3),(-1,0,4,7),(1,1,5,0),(-1,-1,3,4),(1,-3,1,2),(-1,2,6,-1)]:
        fx = poly3(s, r1, r2, k)
        # f'' at r1 is -3(r2 - r1)s: for s > 0, r1 is a local max and r2 a local min
        corr = "B, C only" if s > 0 else "A, D only"
        dis = [x for x in COMBOS if x != corr]
        stem = ("Consider f(x) = %s and the statements: A. x = %s is a point of local minimum. B. x = %s is a point of local maximum. "
                "C. x = %s is a point of local minimum. D. x = %s is a point of local maximum. Choose the correct answer from the options given below:") % (fx, fr(r1), fr(r1), fr(r2), fr(r2))
        why = ("f′(x) = %s%s%s, so the critical points are x = %s and x = %s. f″(x) = %s, giving f″(%s) = %s and f″(%s) = %s. "
               "A negative second derivative means a local maximum and a positive one a local minimum, so x = %s is a local %s and x = %s a local %s: %s. "
               "Trap: the sign of the leading coefficient decides which critical point is the maximum.") % (
               fr(3 * s), xm(r1), xm(r2), fr(r1), fr(r2), "%s(2x %s %s)" % (fr(3 * s), "−" if r1 + r2 >= 0 else "+", fr(abs(r1 + r2))) if r1 + r2 else "%sx" % fr(6 * s),
               par(r1), fr(3 * s * (r1 - r2)), par(r2), fr(3 * s * (r2 - r1)),
               fr(r1), "maximum" if s > 0 else "minimum", fr(r2), "minimum" if s > 0 else "maximum", corr)
        out.append((stem, corr, dis, why))
    return out

def g_rolle_c():         # 55125114516
    out = []
    for a, b, form in [(0,3,1),(0,6,1),(1,4,1),(0,3,2),(2,8,1),(0,9,2),(-3,3,1),(1,7,2),(0,12,1),(-2,4,2)]:
        if form == 1: fx = "(x − %s)(x − %s)²" % (fr(a), fr(b)); c = F(2 * a + b, 3); other = F(a + 2 * b, 3); dbl = b
        else: fx = "(x − %s)²(x − %s)" % (fr(a), fr(b)); c = F(a + 2 * b, 3); other = F(2 * a + b, 3); dbl = a
        fx = fx.replace("x − −", "x + ").replace("(x − 0)", "x")
        cands = [F(a + b, 2), other, dbl, F(b, 3), F(a + b, 3)]
        dis = [x for x in dict.fromkeys(fr(v) for v in cands) if x != fr(c)][:3]
        stem = "For f(x) = %s on [%s, %s], the value c ∈ (%s, %s) given by Rolle's theorem (f′(c) = 0) is" % (fx, fr(a), fr(b), fr(a), fr(b))
        why = ("f is a polynomial (continuous and differentiable) with f(%s) = f(%s) = 0, so Rolle's theorem applies. The product rule factors f′: "
               "the double root %s is a root of f′ too, and the other root of f′ is c = %s, which lies strictly inside (%s, %s). "
               "Trap: x = %s also makes f′ zero, but it is an endpoint, not a point of the open interval; the midpoint %s is not a root of f′.") % (
               fr(a), fr(b), fr(dbl), fr(c), fr(a), fr(b), fr(dbl), fr(F(a + b, 2)))
        out.append((stem, fr(c), dis, why))
    return out

def g_laplace():         # 55125114507
    out = []
    for i, lam in enumerate([2, 3, F(1,2), 4, F(1,3), 5, F(3,2), F(2,3), F(1,4), 6]):
        lam = F(lam)
        co = lam / 2; cs = "" if co == 1 else ("%s" % ff(co) if co.denominator == 1 else "(%s)" % ff(co))
        ex = ff(lam) if lam.denominator == 1 else "(%s)" % ff(lam)
        dens = "%se^(−%s|x|)" % (cs, ex)
        pair = lambda u, v: "%s, %s" % (fr(u), fr(v))
        if i % 2 == 0:
            ask = "E(|X|) and Var(|X|)"; corr = pair(1 / lam, 1 / lam ** 2)
            dis = [pair(1 / lam, 2 / lam ** 2), pair(lam, lam ** 2), pair(2 / lam, 1 / lam ** 2)]
            why = ("|X| has density λe^(−λy), y > 0: the two halves of the symmetric Laplace density fold onto an exponential with rate λ = %s. So E|X| = 1/λ = %s and Var|X| = 1/λ² = %s. "
                   "Trap: Var(X) = 2/λ² = %s is the variance of X itself, not of |X|.") % (fr(lam), fr(1 / lam), fr(1 / lam ** 2), fr(2 / lam ** 2))
        else:
            ask = "E(X) and Var(X)"; corr = pair(0, 2 / lam ** 2)
            dis = [pair(0, 1 / lam ** 2), pair(1 / lam, 2 / lam ** 2), pair(1 / lam, 1 / lam ** 2)]
            why = ("The density is symmetric about 0, so E(X) = 0. Var(X) = E(X²) = E(|X|²), and |X| is exponential with rate λ = %s, so E(|X|²) = 2/λ² = %s. "
                   "Trap: 1/λ² = %s is Var(|X|); it misses the (E|X|)² = 1/λ² that X² keeps.") % (fr(lam), fr(2 / lam ** 2), fr(1 / lam ** 2))
        stem = "Let X have density f(x) = %s, −∞ < x < ∞. Then %s are, respectively," % (dens, ask)
        out.append((stem, corr, dis, why))
    return out

def g_wlln():            # 55125114510
    out = []
    for i, (mu, s2) in enumerate([(2,4),(2,9),(3,4),(4,25),(4,9),(1,9),(3,16),(5,4),(2,16),(3,25)]):
        s = math.isqrt(s2); assert s * s == s2, "the CLT statement needs an exact σ"
        true = ["(1/n)ΣXᵢ →ᵖ %d" % mu, "(1/n)ΣXᵢ² →ᵖ %d" % (s2 + mu * mu), "(√n/%d)(X̄ₙ − %d) →ᵈ N(0, 1)" % (s, mu), "E[(1/(n−1))Σ(Xᵢ − X̄ₙ)²] = %d" % s2]
        false = ["(1/n)ΣXᵢ →ᵖ %d" % (mu * mu), "(1/n)ΣXᵢ² →ᵖ %d" % s2, "(√n/%d)(X̄ₙ − %d) →ᵈ N(0, 1)" % (s2, mu), "E[(1/n)Σ(Xᵢ − X̄ₙ)²] = %d" % s2][i % 4]
        k = i % 4; corr = false; dis = true[:k] + true[k + 1:]
        reason = ["the WLLN sends X̄ₙ to the mean %d, not to its square %d" % (mu, mu * mu),
                  "(1/n)ΣXᵢ² tends to E(X²) = σ² + μ² = %d + %d = %d, not to %d" % (s2, mu * mu, s2 + mu * mu, s2),
                  "the CLT standardises by σ = %d, not by σ² = %d" % (s, s2),
                  "with divisor n the expectation is (n − 1)σ²/n, not σ² = %d; the divisor n − 1 is what makes it unbiased" % s2][k]
        stem = "Let X₁, X₂, …, Xₙ be iid random variables with mean %d and variance %d. Which of the following statements is incorrect?" % (mu, s2)
        why = ("Check each statement against a standard result: the WLLN (sample averages tend to population means), the CLT (√n(X̄ₙ − μ)/σ → N(0,1)) and the "
               "unbiasedness of S² with divisor n − 1. The incorrect one is '%s': %s. Trap: the other three are exactly the standard results.") % (false, reason)
        out.append((stem, corr, dis, why))
    return out

BIBDS = [(7,7,3,3,1),(7,7,4,4,2),(6,15,5,2,1),(6,10,5,3,2),(9,12,4,3,1),(13,13,4,4,1),(11,11,5,5,2),(5,10,4,2,1),(5,10,6,3,3),(8,14,7,4,3)]
def g_bibd():            # 55125114528
    out = []
    for v, b, r, k, l in BIBDS:
        assert r * (k - 1) == l * (v - 1) and b * k == v * r
        val = r * k * (r - l) ** (v - 1)
        dis = [str(r * k * (r - l) ** v), str((r - l) ** (v - 1)), str(r * k * (r - l) ** (v - 2))]
        stem = "N is the incidence matrix of a BIBD with parameters v = %d, b = %d, r = %d, k = %d, λ = %d. The value of |NN′| is" % (v, b, r, k, l)
        why = ("NN′ has r = %d on the diagonal and λ = %d everywhere else, i.e. NN′ = (r − λ)I + λJ. Its eigenvalues are r + (v − 1)λ = rk = %d (once, eigenvector 1) and "
               "r − λ = %d (v − 1 = %d times). The determinant is their product: |NN′| = rk(r − λ)^(v−1) = %d × %d^%d = %d. "
               "Trap: raising r − λ to the power v counts the eigenvalue rk as if it were r − λ.") % (r, l, r * k, r - l, v - 1, r * k, r - l, v - 1, val)
        out.append((stem, str(val), dis, why))
    return out

def g_factdf():          # 55125114529
    out = []
    for n, r, lay in [(3,2,"crd"),(3,2,"rbd"),(2,3,"crd"),(2,4,"rbd"),(3,3,"crd"),(4,2,"rbd"),(2,5,"crd"),(3,4,"rbd"),(4,2,"crd"),(2,3,"rbd")]:
        t = 2 ** n; N = t * r
        crd, rbd = t * (r - 1), (r - 1) * (t - 1)
        val = crd if lay == "crd" else rbd
        cands = [rbd if lay == "crd" else crd, N - 1, t - 1, N, r * (t - 1)]
        dis = [x for x in dict.fromkeys(str(c) for c in cands) if x != str(val)][:3]
        how = "completely randomized (CRD)" if lay == "crd" else "laid out in %d randomized blocks, one replicate per block" % r
        stem = "A 2%s factorial experiment is replicated %d times, %s. The error degrees of freedom are" % (sup(n), r, how)
        why = ("There are 2%s = %d treatment combinations and N = %d observations, so total df = %d and treatment df (all factorial effects) = %d. "
               "%s Trap: forgetting the block df (or charging block df in a CRD) gives %d.") % (
               sup(n), t, N, N - 1, t - 1,
               ("In a CRD the rest is error: %d − %d = %d." % (N - 1, t - 1, crd)) if lay == "crd" else
               ("Blocks take r − 1 = %d df, so error df = %d − %d − %d = %d = (r − 1)(2%s − 1)." % (r - 1, N - 1, t - 1, r - 1, rbd, sup(n))),
               rbd if lay == "crd" else crd)
        out.append((stem, str(val), dis, why))
    return out

def g_pps():             # 55125114531
    out = []
    for X, i in [((2,5,3,8,2),4),((10,20,30,40),2),((4,6,10),1),((3,3,6,12,6),3),((7,1,2),1),((5,15,10,20),4),((1,2,3,4,5,5),5),((12,8,20),1),((6,2,4,8),2),((9,3,3,9,6),1)]:
        T = sum(X); N = len(X); M = max(X); xi = X[i - 1]
        val = F(xi, T)
        cands = [F(1, N), F(xi, N * M), F(xi, M), F(xi, T - xi)]
        dis = [x for x in dict.fromkeys(fr(c) for c in cands) if x != fr(val)][:3]
        stem = ("Lahiri's method is used to draw a sample with probability proportional to size, with replacement, from N = %d units with sizes X = (%s). "
                "The probability that unit %d is selected at any given draw is") % (N, ", ".join(map(str, X)), i)
        why = ("Lahiri's method picks a unit at random (probability 1/N) and a number between 1 and M = max Xⱼ = %d; it accepts the unit if the number is at most its size, "
               "otherwise it tries again. Each trial accepts unit i with probability Xᵢ/(NM), so after the repeats P(unit i) = Xᵢ/ΣXⱼ = %d/%d = %s, exactly PPS. "
               "Trap: Xᵢ/(NM) = %s is the chance of accepting unit %d on one trial, not on a completed draw.") % (M, xi, T, fr(val), fr(F(xi, N * M)), i)
        out.append((stem, fr(val), dis, why))
    return out

def combo(letters):
    letters = sorted(letters)
    if len(letters) == 4: return "A, B, C, D"
    return ", ".join(letters) + " only"

def g_poisson_unb():     # 55125114545
    out = []
    sets = [[(F(3,10),F(7,10)),(1,1)], [(F(1,2),F(1,2)),(2,-1)], [(1,1),(F(1,4),F(3,4))], [(2,-1),(3,-1)], [(F(2,5),F(3,5)),(F(1,2),F(1,3))],
            [(F(1,3),F(1,3)),(F(3,2),F(-1,2))], [(F(3,4),F(1,4)),(0,2)], [(F(5,4),F(-1,4)),(F(1,5),F(4,5))], [(F(1,2),F(1,4)),(3,-2)], [(2,0),(F(-1,2),F(3,2))]]
    for i, ((a, b), (c, d)) in enumerate(sets):
        def lin(u, v):
            u, v = F(u), F(v); out_ = []
            for coef, sym in ((u, "X̄"), (v, "S²")):
                if coef == 0: continue
                mag = "" if abs(coef) == 1 else ff(abs(coef))
                if not out_: out_.append(("−" if coef < 0 else "") + mag + sym)
                else: out_.append(("− " if coef < 0 else "+ ") + mag + sym)
            return " ".join(out_)
        stA = "X̄ is unbiased for λ"; stB = ("X̄² is unbiased for λ²" if i % 3 == 2 else "S² is unbiased for λ"); tB = (i % 3 != 2)
        stC = "%s is unbiased for λ" % lin(a, b); tC = (a + b == 1)
        stD = "%s is unbiased for λ" % lin(c, d); tD = (c + d == 1)
        truth = ["A"] + (["B"] if tB else []) + (["C"] if tC else []) + (["D"] if tD else [])
        corr = combo(truth)
        allc = ["A only", "A, B only", "A, C only", "A, D only", "A, B, C only", "A, B, D only", "A, C, D only", "A, B, C, D"]
        near = sorted((x for x in allc if x != corr), key=lambda x: (abs(len(x) - len(corr)), x))
        dis = near[:3]
        stem = ("Let X₁, X₂, …, Xₙ be a random sample from Poisson(λ), with X̄ = (1/n)ΣXᵢ and S² = (1/(n−1))Σ(Xᵢ − X̄)². Consider the statements: "
                "A. %s. B. %s. C. %s. D. %s. Choose the correct answer from the options given below:") % (stA, stB, stC, stD)
        why = ("For a Poisson distribution the mean and the variance are both λ, so E(X̄) = λ and E(S²) = λ. A linear combination uX̄ + vS² then has expectation (u + v)λ, "
               "so it is unbiased exactly when u + v = 1 (negative weights are allowed). %sHere C has u + v = %s and D has u + v = %s, so the true statements are %s. "
               "Trap: a sum like X̄ + S² has expectation 2λ, not λ.") % (
               ("E(X̄²) = Var(X̄) + λ² = λ/n + λ², so X̄² is biased for λ². " if not tB else ""), fr(a + b), fr(c + d), corr.replace(" only", ""))
        out.append((stem, corr, dis, why))
    return out

def vec(v): return "(" + ", ".join(fr(x) for x in v) + ")"
def g_stationary():      # 55125114598
    out = []
    for p in [F(1,3), F(2,3), F(1,4), F(3,4), F(2,5), F(3,5), F(1,5), F(4,5), F(3,10), F(7,10)]:
        q = 1 - p; rr = p / q; w = [F(1), rr, rr * rr]; s = sum(w); pi = [x / s for x in w]
        corr = vec(pi); dis = ["(1/3, 1/3, 1/3)", vec(pi[::-1]), "(1/4, 1/2, 1/4)"]
        stem = MC % fr(p) + "The stationary distribution (π₁, π₂, π₃) of the chain is"
        why = ("Solve πP = π. The balance between neighbouring states gives pπ₁ = qπ₂ and pπ₂ = qπ₃, so π ∝ (1, p/q, (p/q)²) with p/q = %s. "
               "Normalising: π = %s. Trap: (1/3, 1/3, 1/3) would need every column of P to sum to 1 (doubly stochastic), which happens only when p = q = 1/2.") % (fr(rr), corr)
        out.append((stem, corr, dis, why))
    return out

def first_return(P, i, n):
    """f_ii^(n) by the taboo recursion: leave i, avoid i until step n."""
    v = [P[i][b] if b != i else F(0) for b in range(3)]
    if n == 1: return P[i][i]
    for step in range(2, n + 1):
        nv = [sum(v[a] * P[a][b] for a in range(3)) for b in range(3)]
        if step == n: return nv[i]
        nv[i] = F(0); v = nv

def g_first_return():    # 55125114600
    out = []
    for p, i, n in [(F(1,3),1,3),(F(1,2),1,2),(F(2,5),2,2),(F(1,4),1,4),(F(3,5),3,3),(F(2,3),2,3),(F(1,2),3,2),(F(1,3),2,4),(F(3,4),1,3),(F(2,5),3,4)]:
        P = chain(p); val = first_return(P, i - 1, n)
        cands = [mpow(P, n)[i-1][i-1], first_return(P, i - 1, n - 1), first_return(P, i - 1, n + 1), P[i-1][i-1] ** n, first_return(P, i - 1, n + 2)]
        dis = [x for x in dict.fromkeys(ff(c) for c in cands) if x != ff(val)][:3]
        stem = MC % fr(p) + "The probability f%s%s⁽%s⁾ that the chain, started in state %d, returns to state %d for the first time at step %d is" % ("₀₁₂₃"[i], "₀₁₂₃"[i], sup(n), i, i, n)
        why = ("A first return at step %d means leaving state %d and avoiding it at steps 1 to %d. Carry the path probabilities forward, setting state %d to zero at each step before step %d. "
               "This gives f%s%s⁽%s⁾ = %s. Trap: p%s%s⁽%s⁾ = %s also counts paths that came back earlier.") % (
               n, i, n - 1, i, n, "₀₁₂₃"[i], "₀₁₂₃"[i], sup(n), ff(val), "₀₁₂₃"[i], "₀₁₂₃"[i], sup(n), ff(mpow(P, n)[i-1][i-1]))
        out.append((stem, ff(val), dis, why))
    return out

TSM = ("Consider yₜ = Φ₁yₜ₋₁ + Φ₂yₜ₋₂ + εₜ − θ₁εₜ₋₁ − θ₂εₜ₋₂, where {εₜ} is white noise with variance 1. ")
def tri(a1, a2): return (a1 + a2 < 1) and (a2 - a1 < 1) and (abs(a2) < 1)
def g_statinv():         # 55125114603
    CAT = ["Both stationary and invertible", "Stationary but not invertible", "Invertible but not stationary", "Neither stationary nor invertible"]
    out = []
    for f1, f2, t1, t2 in [(F(4,10),F(3,10),F(6,10),F(4,10)),(F(5,10),F(2,10),F(3,10),F(2,10)),(F(1,2),F(1,2),F(1,2),F(1,4)),(F(-3,10),F(4,10),F(1,2),F(6,10)),
                           (F(6,10),F(5,10),F(7,10),F(5,10)),(F(2,10),F(1,10),F(-4,10),F(3,10)),(F(1,10),F(-12,10),F(2,10),F(1,10)),(F(3,10),F(3,10),F(-8,10),F(4,10)),
                           (F(9,10),F(2,10),F(-3,10),F(-1,10)),(F(-5,10),F(-2,10),F(2,10),F(11,10))]:
        st, iv = tri(f1, f2), tri(t1, t2)
        corr = CAT[0 if st and iv else 1 if st else 2 if iv else 3]; dis = [c for c in CAT if c != corr]
        stem = TSM + "If Φ₁ = %s, Φ₂ = %s, θ₁ = %s, θ₂ = %s, then the process is" % tuple(fr(x) for x in (f1, f2, t1, t2))
        why = ("Stationarity depends only on the AR part and invertibility only on the MA part. For a second-order polynomial 1 − a₁z − a₂z², both roots lie outside "
               "the unit circle exactly when a₁ + a₂ < 1, a₂ − a₁ < 1 and |a₂| < 1. AR: %s + %s = %s, %s − %s = %s, |Φ₂| = %s → %s. MA: %s + %s = %s, %s − %s = %s, |θ₂| = %s → %s. "
               "So the process is: %s. Trap: an MA part never affects stationarity, and an AR part never affects invertibility.") % (
               fr(f1), par(f2), fr(f1 + f2), fr(f2), par(f1), fr(f2 - f1), fr(abs(f2)), "stationary" if st else "not stationary",
               fr(t1), par(t2), fr(t1 + t2), fr(t2), par(t1), fr(t2 - t1), fr(abs(t2)), "invertible" if iv else "not invertible", corr.lower())
        out.append((stem, corr, dis, why))
    return out

def g_pacf():            # 55125114607
    CAT = ["α(h) = 0 for all h ≥ 1", "α(h) = 0 for all h ≥ 2", "α(h) = 0 for all h ≥ 3", "α(h) ≠ 0 for all h ≥ 1"]
    out = []
    for f1, f2, t1 in [(F(6,10),F(3,10),0),(F(5,10),0,0),(0,0,F(5,10)),(0,0,0),(F(2,10),F(5,10),0),(F(-7,10),0,0),(0,0,F(-4,10)),(F(1,2),F(-3,10),0),(F(8,10),0,0),(0,0,F(7,10))]:
        if t1 != 0: corr = CAT[3]; model = "an MA(1) with θ₁ = %s" % fr(t1); reason = "an invertible MA(1) is an AR(∞), so its partial autocorrelations decay but never become exactly zero"
        elif f2 != 0: corr = CAT[2]; model = "a stationary AR(2)"; reason = "an AR(2) has α(2) = Φ₂ = %s ≠ 0 and α(h) = 0 for every h ≥ 3" % fr(f2)
        elif f1 != 0: corr = CAT[1]; model = "a stationary AR(1)"; reason = "an AR(1) has α(1) = Φ₁ = %s and α(h) = 0 for every h ≥ 2" % fr(f1)
        else: corr = CAT[0]; model = "white noise"; reason = "white noise has no correlation at any lag, so every α(h) is zero"
        assert tri(f1, f2)
        dis = [c for c in CAT if c != corr]
        stem = TSM + "If Φ₁ = %s, Φ₂ = %s, θ₁ = %s, θ₂ = 0, and α(h) is the partial autocorrelation at lag h, then" % (fr(f1), fr(f2), fr(t1))
        why = ("With these values the model is %s. The partial autocorrelation cuts off after lag p for an AR(p): %s. "
               "Trap: it is the ACF, not the PACF, that cuts off for a moving average.") % (model, reason)
        out.append((stem, corr, dis, why))
    return out

def arima_name(f1, f2, t1, t2):
    q = 2 if t2 != 0 else (1 if t1 != 0 else 0)
    if f1 + f2 == 1:                          # unit root: 1 - f1 z - f2 z^2 = (1 - z)(1 + f2 z)
        return "ARIMA(%d, 1, %d) process" % (1 if f2 != 0 else 0, q)
    return "ARMA(%d, %d) process" % (2 if f2 != 0 else (1 if f1 != 0 else 0), q)
def g_arima():           # 55125114606
    out = []
    for f1, f2, t1, t2 in [(F(6,10),F(4,10),F(1,2),0),(F(7,10),F(3,10),0,0),(F(1),0,F(4,10),0),(F(1),0,0,0),(F(5,10),F(3,10),F(4,10),0),(F(1,2),F(1,2),F(3,10),F(2,10)),
                           (F(4,10),0,F(1,2),F(3,10)),(F(12,10),F(-2,10),0,0),(F(8,10),F(2,10),F(6,10),0),(F(3,10),F(2,10),0,0)]:
        corr = arima_name(f1, f2, t1, t2)
        q = 2 if t2 != 0 else (1 if t1 != 0 else 0)
        cands = ["ARMA(2, %d) process" % q, "ARIMA(2, 1, %d) process" % q, "ARIMA(1, 1, %d) process" % q, "ARIMA(0, 1, %d) process" % q, "ARMA(1, %d) process" % q,
                 "ARMA(%d, 2) process" % (2 if f2 else 1), "ARIMA(1, 1, %d) process" % (1 - min(q, 1))]
        dis = [x for x in dict.fromkeys(cands) if x != corr][:3]
        stem = TSM + "If Φ₁ = %s, Φ₂ = %s, θ₁ = %s, θ₂ = %s, then {yₜ} is" % tuple(fr(x) for x in (f1, f2, t1, t2))
        unit = f1 + f2 == 1
        why = ("Look for a unit root in the AR polynomial 1 − Φ₁z − Φ₂z²: at z = 1 it equals 1 − Φ₁ − Φ₂ = %s. %s The MA part has order %d. So {yₜ} is an %s. "
               "Trap: with Φ₁ + Φ₂ = 1 the model is not a stationary ARMA(2, q); one AR factor is the difference operator.") % (
               fr(1 - f1 - f2),
               (("That is zero, so 1 − Φ₁z − Φ₂z² = (1 − z)(1 %s %sz): difference once, and Δyₜ has AR order 1." % ("+" if f2 > 0 else "−", fr(abs(f2)))) if f2 else
                "That is zero, so 1 − Φ₁z = 1 − z: difference once, and Δyₜ has no AR part left.") if unit else
               ("That is not zero, so there is no unit root and the AR order is %d." % (2 if f2 else (1 if f1 else 0))), q, corr.replace(" process", ""))
        out.append((stem, corr, dis, why))
    return out

def g_ma1_spec():        # 55125114604
    out = []
    for b, sgn, s2 in [(F(7,10),"+",1),(F(1,2),"−",1),(F(3,10),"+",2),(F(4,5),"−",1),(F(1,2),"+",4),(F(3,5),"−",2),(F(1,5),"+",1),(F(9,10),"−",1),(F(2,5),"+",3),(F(1,2),"−",2)]:
        c0 = 1 + b * b; c1 = 2 * b if sgn == "+" else -2 * b
        def expr(a0, a1, scale, inv=False):
            sign = "+" if a1 > 0 else "−"
            core = "[%s %s %scos(2πω)]" % (fr(a0), sign, fr(abs(a1)))
            core = (core + "⁻¹") if inv else core
            return core if scale == 1 else "%s%s" % (fr(scale), core)
        corr = expr(c0, c1, s2); dis = [expr(c0, -c1, s2), expr(c0, c1, s2, True), expr(1, c1, s2)]
        stem = ("The MA(1) process yₜ = εₜ %s %sεₜ₋₁ has white-noise variance %s. Its spectral density, taken as f(ω) = σ²|1 %s %se^(−2πiω)|², is") % (
               sgn, fr(b), fr(s2), sgn, fr(b))
        why = ("|1 + ce^(−2πiω)|² = (1 + c e^(−2πiω))(1 + c e^(2πiω)) = 1 + c² + 2c cos(2πω), with c = %s%s here. So f(ω) = %s × [1 + %s %s %scos(2πω)] = %s. "
               "Trap: the sign of the cosine term follows the sign of the MA coefficient; a reciprocal [·]⁻¹ is the shape of an AR(1) spectrum.") % (
               "" if sgn == "+" else "−", fr(b), fr(s2), fr(b * b), "+" if sgn == "+" else "−", fr(2 * b), corr)
        out.append((stem, corr, dis, why))
    return out

BATCH2 = [("55125114523", "maths", g_maxexp), ("55125114525", "maths", g_extrema), ("55125114516", "maths", g_rolle_c),
          ("55125114507", "probability", g_laplace), ("55125114510", "probability", g_wlln),
          ("55125114528", "design", g_bibd), ("55125114529", "design", g_factdf), ("55125114531", "sampling", g_pps),
          ("55125114545", "inference", g_poisson_unb), ("55125114598", "stochastic", g_stationary), ("55125114600", "stochastic", g_first_return),
          ("55125114603", "timeseries", g_statinv), ("55125114607", "timeseries", g_pacf), ("55125114606", "timeseries", g_arima),
          ("55125114604", "timeseries", g_ma1_spec)]

BATCH = [  # (official question ID, module, generator)
    ("55125114584", "stochastic", g_ruin), ("55125114581", "stochastic", g_memoryless), ("55125114585", "stochastic", g_poisson_split),
    ("55125114597", "stochastic", g_nstep), ("55125114599", "stochastic", g_first_passage),
    ("55125114568", "timeseries", g_ar1_var), ("55125114605", "timeseries", g_ar1_acov),
    ("55125114527", "design", g_rbd), ("55125114526", "design", g_anova_f),
    ("55125114530", "sampling", g_neyman), ("55125114558", "regression", g_adjr2), ("55125114563", "regression", g_dw),
    ("55125114508", "probability", g_mgf)] + BATCH2

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
