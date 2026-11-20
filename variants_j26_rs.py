#!/usr/bin/env python3
"""Practice variants of the June 2026 Paper 2 questions that are identified by official question ID
(seed/<module>_pyq_j26_rs.json). Batch 1: thirteen computational questions; batch 2: fifteen more; batch 3: fifteen conceptual questions whose answers a rule here still decides; batch 4: the last seven. Ten variants each.

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
    x = F(x); return (str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)).replace("-", "−")
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

# ------------------------------------------------------------------------------------------------- batch 3 generators
# Conceptual questions whose answer is still decided by a rule this script can execute (graph structure of a chain, a
# linear system, a derivative, an order/rank condition, an exact expectation, a fact table, or R's own output).
def mat(M): return "[" + ", ".join("[" + ", ".join(ff(x) for x in row) + "]" for row in M) + "]"
def reach(P):
    n = len(P); R_ = [[i == j or P[i][j] > 0 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                R_[i][j] = R_[i][j] or (R_[i][k] and R_[k][j])
    return R_
def classes(P):
    R_ = reach(P); n = len(P); seen = set(); out = []
    for i in range(n):
        if i in seen: continue
        c = sorted(j for j in range(n) if R_[i][j] and R_[j][i]); seen |= set(c); out.append(c)
    return out
def period(P, i):
    n = len(P); g = 0; M = [[F(int(a == b)) for b in range(n)] for a in range(n)]
    for step in range(1, 3 * n + 1):
        M = [[sum(M[a][k] * P[k][b] for k in range(n)) for b in range(n)] for a in range(n)]
        if M[i][i] > 0: g = math.gcd(g, step)
    return g
def cls_str(cs): return ", ".join("{" + ", ".join(str(i + 1) for i in c) + "}" for c in cs)

CHAINS = [  # transition matrices; every state lies on a cycle, and within a chain every class has the same period
    [[0,1,0],[F(1,2),0,F(1,2)],[0,1,0]], [[F(1,2),F(1,2),0],[F(1,3),F(1,3),F(1,3)],[0,F(1,2),F(1,2)]],
    [[0,1,0],[0,0,1],[1,0,0]], [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],
    [[F(1,2),F(1,2),0],[F(1,2),F(1,2),0],[0,0,1]], [[0,F(1,2),0,F(1,2)],[F(1,2),0,F(1,2),0],[0,F(1,2),0,F(1,2)],[F(1,2),0,F(1,2),0]],
    [[0,1,0],[0,F(1,2),F(1,2)],[1,0,0]], [[0,0,1],[1,0,0],[F(1,2),F(1,2),0]],
    [[F(1,3),F(2,3),0,0],[F(1,2),F(1,2),0,0],[0,0,F(1,4),F(3,4)],[0,0,F(1,2),F(1,2)]], [[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]]]
def g_irred():           # 55125114582
    CAT = ["Irreducible and aperiodic", "Irreducible and periodic", "Reducible and aperiodic", "Reducible and periodic"]
    out = []
    for P in CHAINS:
        cs = classes(P); irr = len(cs) == 1; pers = {period(P, c[0]) for c in cs}; assert len(pers) == 1; d = pers.pop()
        corr = CAT[(0 if irr else 2) + (1 if d > 1 else 0)]; dis = [c for c in CAT if c != corr]
        stem = "Consider the Markov chain on states {%s} with transition probability matrix P = %s. Then the Markov chain is" % (", ".join(str(i + 1) for i in range(len(P))), mat(P))
        why = ("Irreducible means every state can reach every other; here the communicating classes are %s, so the chain is %s. The period of a state is the gcd of the "
               "step counts at which a return is possible; here every class has period %d, so the chain is %s. Trap: a zero diagonal does not by itself make a chain periodic — "
               "what matters is the gcd of all return times (a cycle of length 2 together with one of length 3 gives period 1).") % (
               cls_str(cs), "irreducible" if irr else "reducible (more than one class)", d, "periodic" if d > 1 else "aperiodic")
        out.append((stem, corr, dis, why))
    return out

CLS_CHAINS = [
    [[F(1,2),F(1,2),0],[F(1,2),F(1,2),0],[F(1,3),F(1,3),F(1,3)]], [[0,1,0],[1,0,0],[0,F(1,2),F(1,2)]], [[1,0,0],[F(1,2),0,F(1,2)],[0,0,1]],
    [[F(1,2),F(1,2),0,0],[F(1,2),F(1,2),0,0],[0,0,F(1,2),F(1,2)],[0,0,F(1,2),F(1,2)]], [[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,F(1,2),F(1,2)]],
    [[F(1,3),F(2,3),0],[0,F(1,2),F(1,2)],[0,F(1,2),F(1,2)]], [[0,1,0],[0,0,1],[1,0,0]], [[F(1,2),0,F(1,2),0],[0,1,0,0],[F(1,2),0,F(1,2),0],[F(1,4),F(1,4),F(1,4),F(1,4)]],
    [[0,F(1,2),F(1,2)],[F(1,2),0,F(1,2)],[0,0,1]], [[F(1,2),F(1,2),0,0],[0,0,1,0],[0,1,0,0],[0,0,F(1,2),F(1,2)]]]
def g_classes():         # 55125114583
    out = []
    for P in CLS_CHAINS:
        n = len(P); cs = classes(P); R_ = reach(P); corr = cls_str(cs)
        oneway = [sorted(j for j in range(n) if R_[i][j]) for i in range(n)]       # trap: "reachable from" instead of "communicates with"
        cands = [cls_str([list(range(n))]), cls_str([[i] for i in range(n)]), cls_str(sorted({tuple(o) for o in oneway}))]
        for k in range(len(cs) - 1):                                                # merge two neighbouring classes
            cands.append(cls_str(cs[:k] + [sorted(cs[k] + cs[k + 1])] + cs[k + 2:]))
        for k, c in enumerate(cs):                                                  # split a class (one state treated as separate)
            if len(c) > 1: cands.append(cls_str(sorted(cs[:k] + [[c[0]], c[1:]] + cs[k + 1:])))
        cands += [cls_str([[0, 2], [1, 3]] if n == 4 else [[0, 2], [1]]), cls_str([[0], list(range(1, n))])]   # tidy-looking wrong partitions
        dis = [x for x in dict.fromkeys(cands) if x != corr][:3]
        closed = [c for c in cs if all(P[i][j] == 0 for i in c for j in range(n) if j not in c)]
        stem = "For the Markov chain with transition probability matrix P = %s on states 1 to %d, the communicating classes are" % (mat(P), n)
        why = ("States i and j communicate when each can reach the other (i → j and j → i). Communication is an equivalence relation, so the states split into disjoint classes: %s. "
               "The closed classes (no way out) are %s; any other class is transient. Trap: 'i can reach j' alone does not put i and j in the same class.") % (
               corr, cls_str(closed))
        out.append((stem, corr, dis, why))
    return out

def mean_passage(P, j):
    """m_i = expected steps to reach j from i (i != j), and the mean return time m_jj; solved exactly."""
    n = len(P); idx = [i for i in range(n) if i != j]
    A = [[(F(1) if a == b else F(0)) - P[a][b] for b in idx] + [F(1)] for a in idx]
    for c in range(len(idx)):
        pv = next(r for r in range(c, len(idx)) if A[r][c] != 0); A[c], A[pv] = A[pv], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(len(idx)):
            if r != c: A[r] = [A[r][k] - A[r][c] * A[c][k] for k in range(len(idx) + 1)]
    m = {idx[r]: A[r][-1] for r in range(len(idx))}
    m[j] = 1 + sum(P[j][k] * m[k] for k in idx)
    return m
def g_meanpass():        # 55125114601
    out = []
    for p, i, j in [(F(1,3),1,2),(F(1,2),1,2),(F(2,5),1,3),(F(1,4),2,1),(F(3,5),3,2),(F(2,3),1,3),(F(1,2),3,1),(F(1,3),2,2),(F(3,4),2,3),(F(2,5),1,1)]:
        P = chain(p); m = mean_passage(P, j - 1); val = m[i - 1]
        w = [F(1), p / (1 - p), (p / (1 - p)) ** 2]; pi = [x / sum(w) for x in w]
        cands = ([1 / P[i-1][j-1]] if P[i-1][j-1] else []) + [mean_passage(P, (j % 3))[i - 1], m[(i % 3) if (i % 3) != j - 1 else (i + 1) % 3],
                 1 / (1 - P[j-1][j-1]), F(3), val + 1]
        dis = [x for x in dict.fromkeys(ff(c) for c in cands) if x != ff(val)][:3]
        what = ("the mean recurrence time of state %d (expected number of steps to return to %d, starting there)" % (j, j)) if i == j else \
               ("the expected number of steps to reach state %d for the first time, starting from state %d" % (j, i))
        stem = MC % fr(p) + "Then %s is" % what
        why = ("Let mₖ be the expected number of steps to reach state %d from state k. One step is always taken, then the chain continues from where it lands: "
               "mₖ = 1 + Σ_{l ≠ %d} pₖₗ mₗ. Solving these equations exactly gives %s = %s.%s Trap: counting only the direct jump (or the time to leave state %d) ignores the detours the chain can take.") % (
               j, j, ("m%s%s" % ("₀₁₂₃"[i], "₀₁₂₃"[j])), ff(val),
               (" Check: the mean recurrence time is 1/π%s = 1/%s, where π is the stationary distribution (Kac's formula)." % ("₀₁₂₃"[j], "(" + ff(pi[j - 1]) + ")")) if i == j else "", j)
        out.append((stem, ff(val), dis, why))
    return out

def pstr(c):
    """Polynomial c[0] + c[1]x + c[2]x² + c[3]x³ as text."""
    parts = []
    for k in range(len(c) - 1, -1, -1):
        a = F(c[k])
        if a == 0: continue
        mag = abs(a); m_ = "" if (mag == 1 and k) else (ff(mag) if (mag.denominator == 1 or k == 0) else "(%s)" % ff(mag))
        body = m_ + ["", "x", "x²", "x³"][k]
        parts.append((("−" if a < 0 else "") + body) if not parts else (("− " if a < 0 else "+ ") + body))
    return " ".join(parts) if parts else "0"
def peval(c, x): return sum(F(a) * F(x) ** k for k, a in enumerate(c))
def pder(c): return [k * F(a) for k, a in enumerate(c)][1:] or [F(0)]
def g_piecewise():       # 55125114524
    CH = ["A, C only", "B, D only", "A, D only", "A, B only", "B, C only", "A, B, C only"]
    out = []
    for g1, g2, a, c, b in [([1,0,1],[3,-1],0,1,2), ([1,0,-1],[1,0,F(-1,4)],-1,0,2), ([1,2],[0,0,1],0,1,3), ([0,2,-1],[1],0,1,2), ([0,0,1],[0,0,0,1],-1,0,1),
                            ([0,1],[2,-1],0,1,2), ([0,0,1],[-1,2],0,1,2), ([4,-4,1],[0,0,1],0,1,2), ([0,2,1],[0,2,-1],-2,0,2), ([0,4,-2],[2,0,0],0,1,2)]:
        cont = peval(g1, c) == peval(g2, c); diff = cont and peval(pder(g1), c) == peval(pder(g2), c)
        ends = peval(g1, a) == peval(g2, b); rolle = cont and diff and ends
        truth = [L for L, t in (("A", cont and diff), ("B", not diff), ("C", rolle), ("D", not rolle)) if t]
        corr = ", ".join(truth) + " only"; assert corr in CH, corr
        dis = [x for x in CH if x != corr][:3]
        stem = ("Given f(x) = %s for %s ≤ x ≤ %s, and f(x) = %s for %s < x ≤ %s, consider the statements: A. f(x) is continuous and differentiable at all points. "
                "B. f(x) is not differentiable at x = %s. C. Rolle's theorem is applicable on [%s, %s]. D. Rolle's theorem is not applicable on [%s, %s]. "
                "Choose the correct answer from the options given below:") % (pstr(g1), fr(a), fr(c), pstr(g2), fr(c), fr(b), fr(c), fr(a), fr(b), fr(a), fr(b))
        why = ("Check the join x = %s: the left piece gives %s and the right piece %s, so f is %s there. Slopes at the join: left %s, right %s, so f is %s at x = %s. "
               "Rolle's theorem needs continuity on [%s, %s], differentiability on (%s, %s) and f(%s) = f(%s); here f(%s) = %s and f(%s) = %s, so it is %s. True statements: %s. "
               "Trap: equal end values alone are not enough; a corner inside the interval breaks Rolle's theorem.") % (
               fr(c), fr(peval(g1, c)), fr(peval(g2, c)), "continuous" if cont else "not continuous",
               fr(peval(pder(g1), c)), fr(peval(pder(g2), c)), "differentiable" if diff else "not differentiable", fr(c),
               fr(a), fr(b), fr(a), fr(b), fr(a), fr(b), fr(a), fr(peval(g1, a)), fr(b), fr(peval(g2, b)), "applicable" if rolle else "not applicable", corr.replace(" only", ""))
        out.append((stem, corr, dis, why))
    return out

def g_eigen():           # 55125114519
    out = []
    for A, fdesc, fn, wrong in [
        ([[2,1],[1,2]], "A⁻¹", lambda l: 1 / l, [lambda l: l, lambda l: -l, lambda l: l * l]),
        ([[4,1],[2,3]], "A²", lambda l: l * l, [lambda l: 2 * l, lambda l: l, lambda l: 1 / l]),
        ([[3,0],[0,5]], "A − 2I", lambda l: l - 2, [lambda l: l + 2, lambda l: l, lambda l: l / 2]),
        ([[2,2],[1,3]], "3A + I", lambda l: 3 * l + 1, [lambda l: 3 * l, lambda l: l + 1, lambda l: 3 * (l + 1)]),
        ([[5,2],[2,2]], "A′ (the transpose of A)", lambda l: l, [lambda l: 1 / l, lambda l: -l, lambda l: l * l]),
        ([[1,2],[2,1]], "A⁻¹", lambda l: 1 / l, [lambda l: l, lambda l: -l, lambda l: l * l]),
        ([[6,2],[2,3]], "A² − A", lambda l: l * l - l, [lambda l: l * l, lambda l: l, lambda l: 2 * l]),
        ([[4,-2],[1,1]], "(A − I)⁻¹", lambda l: 1 / (l - 1), [lambda l: l - 1, lambda l: 1 / l - 1, lambda l: 1 / l]),
        ([[3,1],[0,2]], "A³", lambda l: l ** 3, [lambda l: l * l, lambda l: l, lambda l: 1 / l ** 3]),
        ([[7,-2],[4,1]], "2A⁻¹", lambda l: 2 / l, [lambda l: l / 2, lambda l: 1 / (2 * l), lambda l: 2 * l])]:
        a, b, c, d = map(F, (A[0][0], A[0][1], A[1][0], A[1][1])); tr = a + d; det = a * d - b * c
        disc = tr * tr - 4 * det; sq = math.isqrt(int(disc)); assert sq * sq == disc
        l1, l2 = (tr + sq) / 2, (tr - sq) / 2
        corr = ff(fn(l1)); other = ff(fn(l2))
        dis = [x for x in dict.fromkeys(ff(w(l1)) for w in wrong) if x not in (corr, other)]
        assert len(dis) >= 3, (A, fdesc, dis)
        stem = "The matrix A = %s has λ = %s as an eigenvalue. Which of the following is an eigenvalue of %s?" % (mat(A), ff(l1), fdesc)
        why = ("If Av = λv then any polynomial (or inverse) in A acts on the same eigenvector by the same function of λ: here %s v = f(λ)v with f(λ) = %s at λ = %s. "
               "(A's eigenvalues are %s and %s: the trace is %s and the determinant %s.) Trap: the eigenvector stays the same; only the eigenvalue is transformed, so do not leave λ unchanged.") % (
               fdesc.split(" (")[0], corr, ff(l1), ff(l1), ff(l2), ff(tr), ff(det))
        out.append((stem, corr, dis[:3], why))
    return out

def g_ident():           # 55125114562
    CAT = ["Both (i) and (ii) are identified", "(i) is identified but (ii) is not", "(ii) is identified but (i) is not", "Both (i) and (ii) are unidentified"]
    out = []
    for e1, e2 in [({1,2},{2}), ({1},{2}), ({1,2},{1,2}), ({1},{1,2}), ({1,3},{2}), ({1,2,3},{3}), ({2},{1,3}), ({1,2},{1,3}), ({3},{3}), ({1},{2,3})]:
        allx = sorted(e1 | e2)
        def ident(own, other):              # rank condition with 2 equations: an excluded exogenous variable must appear in the other equation
            return any(x not in own and x in other for x in allx)
        i1, i2 = ident(e1, e2), ident(e2, e1)
        corr = CAT[0 if i1 and i2 else 1 if i1 else 2 if i2 else 3]; dis = [x for x in CAT if x != corr]
        xs = lambda S, k: " + ".join("β%s%s x%s" % ("₀₁₂₃"[k], "₀₁₂₃"[j], "₀₁₂₃"[j]) for j in sorted(S))
        stem = ("Consider the two-equation model (i) y₁ = γ₁y₂ + %s + ε₁ and (ii) y₂ = γ₂y₁ + %s + ε₂, where the y's are endogenous and the x's are exogenous "
                "(all coefficients shown are non-zero). Then") % (xs(e1, 1), xs(e2, 2))
        def say(own, other, nm):
            exc = [x for x in allx if x not in own]
            return "(%s) excludes %s" % (nm, ", ".join("x%s" % "₀₁₂₃"[x] for x in exc) if exc else "no exogenous variable")
        why = ("With G = 2 equations, an equation is identified when it excludes at least G − 1 = 1 exogenous variable that appears elsewhere in the system "
               "(order condition; with two equations and non-zero coefficients this also satisfies the rank condition). %s and %s, so: %s. "
               "Trap: including more exogenous variables in an equation makes it harder, not easier, to identify.") % (
               say(e1, e2, "i"), say(e2, e1, "ii"), corr.lower())
        out.append((stem, corr, dis, why))
    return out

def cpar(x):
    x = F(x); return ff(x) if x.denominator == 1 else "(%s)" % ff(x)
def over_n(c):
    """c/n written cleanly: 1/n, 4/n, 1/(4n)."""
    c = F(c)
    if c == 1: return "1/n"
    if c.denominator == 1: return "%d/n" % c.numerator
    if c.numerator == 1: return "1/(%dn)" % c.denominator
    return "%s/n" % ff(c)
def g_shiftexp():        # 55125114514
    out = []
    for lam, picks in [(2,"ABCD"),(1,"BCDE"),(3,"AFGH"),(F(1,2),"ACEG"),(2,"BDFH"),(4,"AEFC"),(F(1,3),"GBHD"),(1,"AHCE"),(3,"FDGB"),(F(1,2),"EHAC")]:
        lam = F(lam); L = lam
        pool = {
            "A": ("X̄ₙ →ᵖ θ + %s" % ff(1 / L), True),
            "B": ("If Y = min(X₁, …, Xₙ), then f(y) = %sn e^(−%sn(y − θ)), y ≥ θ" % ("" if L == 1 else cpar(L), "" if L == 1 else cpar(L)), True),
            "C": ("V(X̄ₙ) = %s" % over_n(1 / (L * L)), True),
            "D": ("X̄ₙ →ᵖ θ", False),
            "E": ("min(X₁, …, Xₙ) →ᵖ θ", True),
            "F": ("V(X̄ₙ) = %sn" % ("" if L == 1 else cpar(1 / (L * L))), False),
            "G": ("E[min(X₁, …, Xₙ)] = θ + %s" % over_n(1 / L), True),
            "H": ("E[min(X₁, …, Xₙ)] = θ", False)}
        st = [pool[k] for k in picks]
        truth = [L_ for L_, (_, t) in zip("ABCD", st) if t]
        corr = ("A, B, C, D" if len(truth) == 4 else ", ".join(truth) + " only")
        allc = ["A, B only", "B, C, D only", "A, C, D only", "A, B, C only", "A, B, C, D", "A, C only", "B, D only", "A, D only", "C, D only", "B, C only", "A, B, D only",
                "A only", "B only", "C only", "D only"]
        dis = sorted((x for x in allc if x != corr), key=lambda x: (abs(len(x) - len(corr)), x))[:3]
        dens = "e^(−(x − θ))" if L == 1 else "%se^(−%s(x − θ))" % (cpar(L), cpar(L))
        stem = ("Let X₁, …, Xₙ be iid with pdf f(x | θ) = %s for x ≥ θ, and 0 otherwise. Consider: A. %s. B. %s. C. %s. D. %s. Choose the correct answer from the options given below:") % (
               dens, st[0][0], st[1][0], st[2][0], st[3][0])
        why = ("X − θ is exponential with rate λ = %s, so E(X) = θ + 1/λ = θ + %s and Var(X) = 1/λ² = %s. Hence X̄ₙ →ᵖ θ + %s (not θ) and V(X̄ₙ) = %s/n. "
               "The minimum exceeds y only if every observation does: P(Y > y) = e^(−nλ(y − θ)), so Y − θ is exponential with rate nλ, E(Y) = θ + 1/(nλ), and Y →ᵖ θ. "
               "True statements: %s. Trap: the sample mean estimates the mean θ + 1/λ, not the start of the support θ.") % (
               ff(L), ff(1 / L), ff(1 / (L * L)), ff(1 / L), ff(1 / (L * L)), corr.replace(" only", ""))
        out.append((stem, corr, dis, why))
    return out

UMVUE = [  # (family, sufficient statistic, indicator, correct, distractors, explanation of E(T))
    ("exponential with mean θ", "ΣXᵢ", "T = 1 if X₁ > c, and 0 otherwise (c > 0 fixed)", "e^(−c/θ)", ["1 − e^(−c/θ)", "θ", "1/θ"], "E(T) = P(X₁ > c) = e^(−c/θ)"),
    ("exponential with pdf λe^(−λx), x > 0", "ΣXᵢ", "T = 1 if X₁ ≤ c, and 0 otherwise (c > 0 fixed)", "1 − e^(−λc)", ["e^(−λc)", "λc", "1/λ"], "E(T) = P(X₁ ≤ c) = 1 − e^(−λc)"),
    ("Poisson(λ)", "ΣXᵢ", "T = 1 if X₁ = 0, and 0 otherwise", "e^(−λ)", ["1 − e^(−λ)", "λ", "λe^(−λ)"], "E(T) = P(X₁ = 0) = e^(−λ)"),
    ("Poisson(λ)", "ΣXᵢ", "T = 1 if X₁ = 1, and 0 otherwise", "λe^(−λ)", ["e^(−λ)", "λ", "1 − e^(−λ)"], "E(T) = P(X₁ = 1) = λe^(−λ)"),
    ("Bernoulli(p)", "ΣXᵢ", "T = X₁X₂", "p²", ["p", "2p", "p(1 − p)"], "E(T) = E(X₁)E(X₂) = p² by independence"),
    ("Binomial(m, p) with m known", "ΣXᵢ", "T = 1 if X₁ = 0, and 0 otherwise", "(1 − p)^m", ["1 − p", "p^m", "mp"], "E(T) = P(X₁ = 0) = (1 − p)^m"),
    ("N(μ, 1)", "ΣXᵢ", "T = 1 if X₁ ≤ c, and 0 otherwise (c fixed)", "Φ(c − μ)", ["Φ(μ − c)", "φ(c − μ)", "c − μ"], "E(T) = P(X₁ ≤ c) = P(Z ≤ c − μ) = Φ(c − μ)"),
    ("Uniform(0, θ)", "max(X₁, …, Xₙ)", "T = 1 if X₁ ≤ c, and 0 otherwise (0 < c < θ, c fixed)", "c/θ", ["1 − c/θ", "θ/c", "cθ"], "E(T) = P(X₁ ≤ c) = c/θ"),
    ("geometric with P(X = x) = p(1 − p)^x, x = 0, 1, 2, …", "ΣXᵢ", "T = 1 if X₁ = 0, and 0 otherwise", "p", ["1 − p", "p(1 − p)", "1/p"], "E(T) = P(X₁ = 0) = p"),
    ("Poisson(λ)", "ΣXᵢ", "T = 1 if X₁ ≥ 1, and 0 otherwise", "1 − e^(−λ)", ["e^(−λ)", "λ", "λe^(−λ)"], "E(T) = P(X₁ ≥ 1) = 1 − e^(−λ)")]
def g_umvue():           # 55125114538
    out = []
    for fam, S, T, corr, dis, et in UMVUE:
        stem = "Let X₁, X₂, …, Xₙ (n ≥ 2) be iid %s, and let S = %s. Define %s. Then E[T | S] is the UMVUE of" % (fam, S, T)
        why = ("T is unbiased for its own expectation: %s. S is a complete sufficient statistic for this family, so by Rao–Blackwell and Lehmann–Scheffé, E[T | S] is the unique "
               "UMVUE of %s. Trap: the answer is what T estimates (a probability or expectation), not the parameter itself.") % (et, corr)
        out.append((stem, corr, dis, why))
    return out

def g_sprt():            # 55125114552
    out = []
    for a, b in [(F(5,100),F(10,100)),(F(1,100),F(5,100)),(F(10,100),F(20,100)),(F(5,100),F(5,100)),(F(2,100),F(10,100))]:
        A_, B_ = (1 - b) / a, b / (1 - a)
        for ask in ("upper", "lower"):
            corr = fr(A_) if ask == "upper" else fr(B_)
            cands = [B_, (1 - a) / b, 1 / a, b / a, 1 / b] if ask == "upper" else [A_, a / (1 - b), b, a, b / a]
            dis = [x for x in dict.fromkeys(fr(c) for c in cands) if x != corr][:3]
            stem = ("In Wald's SPRT with type I error α = %s and type II error β = %s, sampling continues while B < λₘ < A, where λₘ is the likelihood ratio L₁/L₀. "
                    "Wald's approximation for the %s boundary %s is") % (fr(a), fr(b), ask, "A" if ask == "upper" else "B")
            why = ("Wald's approximations are A ≈ (1 − β)/α and B ≈ β/(1 − α). Here A ≈ (1 − %s)/%s = %s and B ≈ %s/(1 − %s) = %s. "
                   "H₁ is accepted when the ratio first reaches A and H₀ when it falls to B. Trap: swapping α and β in the formulas gives %s.") % (
                   fr(b), fr(a), fr(A_), fr(b), fr(a), fr(B_), fr((1 - a) / b) if ask == "upper" else fr(a / (1 - b)))
            out.append((stem, corr, dis, why))
    return out

DENS = [  # (density text, statements [(text, truth)], explanation)
    ("f(x, y) = (1/4)(1 + xy) for |x| < 1, |y| < 1", [("X and Y are independent", False), ("f(x) = 1/2 for −1 < x < 1", True), ("E(XY) = 1/9", True), ("Cov(X, Y) = 0", False)],
     "Integrating out y gives f(x) = 1/2 and likewise f(y) = 1/2, but f(x)f(y) = 1/4 ≠ (1/4)(1 + xy), so X and Y are dependent. E(XY) = (1/4)∫∫x²y² = (1/4)(2/3)(2/3) = 1/9, and since E(X) = E(Y) = 0, Cov(X, Y) = 1/9 ≠ 0."),
    ("f(x, y) = 4xy for 0 < x < 1, 0 < y < 1", [("X and Y are independent", True), ("f(x) = 2x for 0 < x < 1", True), ("E(X) = 1/2", False), ("E(XY) = 4/9", True)],
     "The density factorises as (2x)(2y) on a rectangle, so X and Y are independent with f(x) = 2x. E(X) = ∫2x² dx = 2/3, not 1/2, and E(XY) = E(X)E(Y) = 4/9."),
    ("f(x, y) = x + y for 0 < x < 1, 0 < y < 1", [("X and Y are independent", False), ("f(x) = x + 1/2 for 0 < x < 1", True), ("E(X) = 7/12", True), ("E(XY) = E(X)E(Y)", False)],
     "f(x) = ∫(x + y)dy = x + 1/2 and similarly for y; (x + 1/2)(y + 1/2) ≠ x + y, so they are dependent. E(X) = ∫x(x + 1/2)dx = 1/3 + 1/4 = 7/12. E(XY) = 1/3 but E(X)E(Y) = 49/144."),
    ("f(x, y) = 2 for 0 < x < y < 1", [("X and Y are independent", False), ("f(x) = 2(1 − x) for 0 < x < 1", True), ("f(y) = 2y for 0 < y < 1", True), ("E(Y) = 1/2", False)],
     "The support 0 < x < y < 1 is a triangle, not a rectangle, so X and Y cannot be independent. f(x) = ∫ₓ¹ 2 dy = 2(1 − x), f(y) = ∫₀ʸ 2 dx = 2y, and E(Y) = ∫2y² dy = 2/3."),
    ("f(x, y) = e^(−(x + y)) for x > 0, y > 0", [("X and Y are independent", True), ("P(X > Y) = 1/2", True), ("X + Y has a gamma distribution with shape 2", True), ("E(XY) = 2", False)],
     "The density is e^(−x)·e^(−y) on a product region: independent standard exponentials. By symmetry P(X > Y) = 1/2; the sum of two independent Exp(1) variables is Gamma(2, 1); and E(XY) = 1 × 1 = 1, not 2."),
    ("f(x, y) = 6x for 0 < x < y < 1", [("X and Y are independent", False), ("f(x) = 6x(1 − x) for 0 < x < 1", True), ("f(y) = 3y² for 0 < y < 1", True), ("E(X) = 1/2", True)],
     "On the triangle 0 < x < y < 1, f(x) = ∫ₓ¹ 6x dy = 6x(1 − x) and f(y) = ∫₀ʸ 6x dx = 3y². Their product is not 6x, so they are dependent. E(X) = ∫6x²(1 − x)dx = 2 − 3/2 = 1/2."),
    ("f(x, y) = (3/2)(x² + y²) for 0 < x < 1, 0 < y < 1", [("X and Y are independent", False), ("f(x) = (3/2)x² + 1/2 for 0 < x < 1", True), ("E(X) = 5/8", True), ("E(X²) = 1/2", False)],
     "f(x) = (3/2)(x² + 1/3) = (3/2)x² + 1/2, and f(x)f(y) ≠ (3/2)(x² + y²), so they are dependent. E(X) = ∫x((3/2)x² + 1/2)dx = 3/8 + 1/4 = 5/8; E(X²) = 3/10 + 1/6 = 7/15, not 1/2."),
    ("f(x, y) = 8xy for 0 < x < y < 1", [("X and Y are independent", False), ("f(y) = 4y³ for 0 < y < 1", True), ("f(x) = 4x(1 − x²) for 0 < x < 1", True), ("f(x, y) factorises, so X and Y are independent", False)],
     "8xy looks like a product, but the support 0 < x < y < 1 is not a rectangle, so X and Y are dependent: knowing y limits x to (0, y). f(y) = ∫₀ʸ 8xy dx = 4y³ and f(x) = ∫ₓ¹ 8xy dy = 4x(1 − x²)."),
    ("f(x, y) = 1/2 for |x| + |y| < 1", [("X and Y are independent", False), ("Cov(X, Y) = 0", True), ("f(x) = 1 − |x| for −1 < x < 1", True), ("E(X) = 0", True)],
     "The square |x| + |y| < 1 has area 2, so the density is 1/2. f(x) = ∫ 1/2 dy over |y| < 1 − |x| = 1 − |x|. By symmetry E(X) = 0 and E(XY) = 0, so Cov(X, Y) = 0; yet the support is not a rectangle, so X and Y are dependent — uncorrelated does not mean independent."),
    ("f(x, y) = 2e^(−x − 2y) for x > 0, y > 0", [("X and Y are independent", True), ("E(Y) = 1/2", True), ("P(X < Y) = 1/3", True), ("E(X) = 1/2", False)],
     "f = e^(−x)·2e^(−2y): independent, X ~ Exp(1) and Y ~ Exp(rate 2), so E(X) = 1 and E(Y) = 1/2. P(X < Y) = 1/(1 + 2) = 1/3 (the rate of X over the sum of the rates).")]
def g_joint():           # 55125114512
    allc = ["A, B only", "B, C only", "A, B, C only", "B, C, D only", "A, D only", "A, B, C, D", "A, B, D only", "A, C, D only", "B, D only", "A, C only", "C, D only"]
    out = []
    for dens, sts, ex in DENS:
        truth = [L for L, (_, t) in zip("ABCD", sts) if t]
        corr = "A, B, C, D" if len(truth) == 4 else ", ".join(truth) + " only"
        dis = sorted((x for x in allc if x != corr), key=lambda x: (abs(len(x) - len(corr)), x))[:3]
        stem = "Let X and Y have joint pdf %s (and 0 otherwise). Consider: A. %s. B. %s. C. %s. D. %s. Choose the correct answer from the options given below:" % (
            dens, sts[0][0], sts[1][0], sts[2][0], sts[3][0])
        why = ex + " So the true statements are %s. Trap: independence needs both a factorised density and a rectangular (product) support." % corr.replace(" only", "")
        out.append((stem, corr, dis, why))
    return out

RSNIP = [  # (code lines, R output confirmed with R 4.5.1, distractors, explanation)
    (["x <- 2", "f <- function(y) {", "  x <- 10", "  x * y", "}", "f(3)"], "30", ["6", "13", "5"], "Inside f, x <- 10 creates a local x that hides the global x = 2, so f(3) = 10 × 3 = 30. Trap: 6 uses the global x."),
    (["x <- 1", "f <- function() {", "  x <<- 5", "  x + 1", "}", "f()", "x"], "5", ["1", "6", "2"], "<<- assigns in the enclosing (here global) environment, so f() changes the global x to 5 (and returns 6). The last line prints x = 5. Trap: with <- instead of <<- the global x would stay 1."),
    (["f <- function(a, b = a * 2) {", "  a + b", "}", "f(3)"], "9", ["3", "6", "5"], "A default argument may refer to another argument: b defaults to a * 2 = 6, so f(3) = 3 + 6 = 9. Trap: 3 ignores the default for b."),
    (["x <- c(1, 2, 3, 4)", "y <- x[x > 2]", "sum(y)"], "7", ["10", "3", "2"], "x > 2 is the logical vector (FALSE, FALSE, TRUE, TRUE), so y = c(3, 4) and sum(y) = 7. Trap: 2 counts the selected elements instead of adding them."),
    (["g <- function(n) {", "  s <- 0", "  for (i in 1:n) s <- s + i", "  s", "}", "g(4)"], "10", ["4", "24", "6"], "The loop adds 1 + 2 + 3 + 4 = 10, and the last expression s is returned. Trap: 24 is 4! (a product, not a sum)."),
    (["x <- 5", "h <- function(x) {", "  x <- x + 1", "  x", "}", "h(x)", "x"], "5", ["6", "1", "11"], "R passes arguments by value: h works on its own copy of x and returns 6, but the global x is untouched. The last line prints 5. Trap: 6 is what h(x) returns, not the new value of x."),
    (["v <- 1:4 * 1:2", "sum(v)"], "16", ["10", "30", "20"], "The shorter vector is recycled: 1:4 * c(1, 2, 1, 2) = c(1, 4, 3, 8), whose sum is 16. Trap: 30 multiplies the two sums, and 20 treats 1:2 as the single number 2; R multiplies element by element after recycling."),
    (["f <- function(n) if (n <= 1) 1 else n * f(n - 1)", "f(4)"], "24", ["4", "10", "1"], "f calls itself on n − 1 until the base case n ≤ 1 returns 1: f(4) = 4 × f(3) = 4 × 3 × f(2) = 4 × 3 × 2 × f(1) = 24, the factorial of 4. Trap: 10 adds the numbers instead of multiplying them."),
    (["x <- c(2, 4, 6)", "x[2] <- 10", "mean(x)"], "6", ["4", "18", "10"], "After x[2] <- 10 the vector is c(2, 10, 6), whose mean is 18/3 = 6. Trap: 4 is the mean before the change; 18 is the sum."),
    (["a <- 3", "f <- function() {", "  a <- a + 2", "  g <- function() a * 2", "  g()", "}", "f()"], "10", ["6", "12", "5"], "Inside f, a <- a + 2 makes a local a = 5. g is defined inside f, so it finds that a (lexical scoping) and returns 5 × 2 = 10. Trap: 6 uses the global a = 3.")]
def g_rprog():           # 55125114589
    out = []
    for code, ans, dis, ex in RSNIP:
        prompt, depth = [], 0
        for l in code:
            prompt.append(("> " if depth == 0 else "+ ") + l)
            depth += l.count("{") - l.count("}")
        stem = "A part of an R program is given below:\n" + "\n".join(prompt) + "\nThe output of the last line is:"
        out.append((stem, ans, dis, ex + " (Output confirmed by running the code in R 4.5.1.)"))
    return out

def matching(pairs_sets, title1, title2, why_head):
    out = []
    for n, pairs in enumerate(pairs_sets):
        k = len(pairs); perm = [(i * 3 + n) % k for i in range(k)]      # where item i's answer sits in List II
        assert sorted(perm) == list(range(k))
        listII = [None] * k
        for i, p in enumerate(perm): listII[p] = pairs[i][1]
        roman = ["I", "II", "III", "IV"]
        corr = ", ".join("%s-%s" % ("ABCD"[i], roman[perm[i]]) for i in range(k))
        def alt(q): return ", ".join("%s-%s" % ("ABCD"[i], roman[q[i]]) for i in range(k))
        swaps = [[perm[1], perm[0], perm[2], perm[3]], [perm[0], perm[2], perm[1], perm[3]], [perm[3], perm[1], perm[2], perm[0]]]
        dis = [alt(q) for q in swaps]
        stem = "Match LIST-I with LIST-II. LIST-I (%s): %s. LIST-II (%s): %s. Choose the correct answer from the options given below:" % (
            title1, "; ".join("%s. %s" % ("ABCD"[i], pairs[i][0]) for i in range(k)), title2, "; ".join("%s. %s" % (roman[j], listII[j]) for j in range(k)))
        why = why_head + " " + "; ".join("%s → %s" % (pairs[i][0], pairs[i][1]) for i in range(k)) + ". So the matching is %s. Trap: each item of LIST-II is used exactly once, so fix the pairs you are sure of first." % corr
        out.append((stem, corr, dis, why))
    return out

STATS = [("R. A. Fisher", "Analysis of variance and maximum likelihood"), ("J. Neyman", "Theory of confidence intervals"), ("Karl Pearson", "Chi-square goodness-of-fit test"),
         ("W. S. Gosset", "Student's t distribution"), ("P. C. Mahalanobis", "D² distance in multivariate analysis"), ("C. R. Rao", "Cramér–Rao inequality and the Rao–Blackwell theorem"),
         ("R. C. Bose", "Partially balanced incomplete block designs"), ("S. N. Roy", "Union–intersection principle in multivariate testing"), ("A. Wald", "Sequential probability ratio test"),
         ("A. N. Kolmogorov", "Axiomatic foundation of probability"), ("H. Hotelling", "T² statistic and principal components"), ("C. Spearman", "Rank correlation coefficient"),
         ("F. Wilcoxon", "Signed-rank and rank-sum tests"), ("G. E. P. Box and G. M. Jenkins", "ARIMA model building"), ("J. Durbin and G. S. Watson", "Test for first-order autocorrelation of regression residuals"),
         ("D. G. Horvitz and D. J. Thompson", "Unbiased estimator for unequal-probability sampling without replacement"), ("M. H. Hansen and W. N. Hurwitz", "Estimator for PPS sampling with replacement"),
         ("Des Raj", "Ordered estimator in PPS sampling without replacement"), ("C. F. Gauss", "Method of least squares"), ("W. H. Kruskal and W. A. Wallis", "Rank-based one-way analysis of variance")]
def g_match_stats():     # 55125114593
    sets = [[STATS[i] for i in idx] for idx in [(4,6,7,15),(0,1,2,3),(5,8,9,10),(11,12,13,14),(16,17,18,19),(4,5,6,7),(0,8,12,16),(1,10,14,17),(2,9,13,18),(3,11,15,19)]]
    return matching(sets, "statisticians", "contributions", "Recall each statistician's best-known contribution:")

SAMP = [("Simple random sampling", "Homogeneous population"), ("Stratified random sampling", "Heterogeneous population that splits into homogeneous groups"),
        ("Cluster sampling", "No list of elementary units is available"), ("Sampling with varying probabilities (PPS)", "Units of very different sizes, giving larger units more weight"),
        ("Systematic sampling", "Every k-th unit from an ordered list after a random start"), ("Multistage sampling", "Large, widely spread population sampled in successive stages"),
        ("Double (two-phase) sampling", "Auxiliary information collected first on a large preliminary sample"), ("Quota sampling", "Non-probability method: interviewers fill fixed numbers per category"),
        ("Ratio estimation", "Auxiliary variable roughly proportional to the study variable (line through the origin)"), ("Regression estimation", "Linear relation with a non-zero intercept between study and auxiliary variables"),
        ("Inverse sampling", "Sampling continues until a fixed number of units with a rare attribute is found"), ("Snowball sampling", "Respondents recruit further respondents from a hidden population")]
def g_match_samp():      # 55125114535
    sets = [[SAMP[i] for i in idx] for idx in [(0,1,2,3),(4,5,6,7),(8,9,10,11),(0,4,8,11),(1,5,9,10),(2,6,7,3),(0,2,5,9),(1,3,6,10),(4,7,8,2),(5,11,0,6)]]
    return matching(sets, "methods", "when used / key feature", "Link each method to the situation it is designed for:")

NPT = [("Chi-square test", "Homogeneity or independence in a contingency table"), ("Wilcoxon signed-rank test", "Two related (paired) samples"), ("Mann–Whitney U test", "Two independent samples"),
       ("Kruskal–Wallis test", "Several independent samples: rank version of one-way ANOVA"), ("Friedman test", "Several related samples in blocks: rank version of two-way ANOVA"),
       ("Kolmogorov–Smirnov one-sample test", "Goodness of fit to a fully specified continuous distribution"), ("Run test", "Randomness of a sequence"), ("Sign test", "Median of a single population using only signs"),
       ("Spearman's rank correlation", "Monotone association between two variables"), ("McNemar test", "Change in paired binary (yes/no) responses"), ("Median test", "Equality of medians of independent samples"),
       ("Kendall's coefficient of concordance W", "Agreement among several judges ranking the same objects")]
def g_match_np():        # 55125114554
    sets = [[NPT[i] for i in idx] for idx in [(0,1,2,3),(4,5,6,7),(8,9,10,11),(0,4,8,11),(1,5,9,10),(2,6,7,3),(0,2,5,9),(1,3,6,10),(4,7,8,2),(5,11,0,6)]]
    return matching(sets, "tests", "purpose", "Match each test to the design or question it answers:")

ORGS = [("Indian Statistical Institute (ISI)", 1931), ("National Sample Survey (NSS)", 1950), ("Central Statistical Organisation (CSO)", 1951), ("Indian Statistical Service (ISS)", 1961),
        ("Ministry of Statistics and Programme Implementation (MoSPI)", 1999), ("National Statistical Commission (NSC)", 2006), ("NITI Aayog", 2015), ("National Statistical Office (NSO)", 2019)]
def g_orgs():            # 55125114590
    out = []
    for n, idx in enumerate([(0,1,2,4,7),(2,3,4,5,6),(0,2,3,5,7),(1,3,4,6,7),(0,1,3,5,6),(1,2,4,5,7),(0,2,4,6,7),(0,1,2,3,5),(3,4,5,6,7),(0,1,4,5,7)]):
        items = [ORGS[i] for i in idx]; k = len(items)
        order = [(n + 2 * j) % k for j in range(k)]                  # how the five are listed as A..E
        listed = [items[o] for o in order]
        chron = sorted(range(k), key=lambda j: listed[j][1])
        corr = ", ".join("ABCDE"[j] for j in chron)
        def sw(a, b): q = chron[:]; q[a], q[b] = q[b], q[a]; return ", ".join("ABCDE"[j] for j in q)
        dis = [sw(0, 1), sw(2, 3), sw(3, 4)]
        stem = "Arrange the following in order of their year of establishment, from oldest to latest: %s. Choose the correct answer from the options given below:" % (
            " ".join("%s. %s" % ("ABCDE"[j], listed[j][0]) for j in range(k)))
        why = ("Founding years: %s. Sorting them gives %s. Trap: the NSO (2019) is the newest — it was formed by merging the CSO and the NSSO.") % (
            "; ".join("%s %d" % (listed[j][0], listed[j][1]) for j in chron), corr)
        out.append((stem, corr, dis, why))
    return out

BATCH3 = [("55125114582", "stochastic", g_irred), ("55125114583", "stochastic", g_classes), ("55125114601", "stochastic", g_meanpass),
          ("55125114524", "maths", g_piecewise), ("55125114519", "maths", g_eigen), ("55125114562", "regression", g_ident),
          ("55125114514", "inference", g_shiftexp), ("55125114538", "inference", g_umvue), ("55125114552", "inference", g_sprt),
          ("55125114512", "probability", g_joint), ("55125114589", "rprog", g_rprog),
          ("55125114593", "official", g_match_stats), ("55125114535", "sampling", g_match_samp), ("55125114554", "nonparam", g_match_np),
          ("55125114590", "official", g_orgs)]

# ------------------------------------------------------------------------------------------------- batch 4 generators
# The last seven ID-keyed questions. Three are made numeric so the verifier can check them against an actual projection
# matrix; four are statement sets whose truth values are recorded here and, separately, in the verifier.
def v2(v): return "(" + ", ".join(ff(x) for x in v) + ")′"
def g_bias():            # 55125114556
    out = []
    for XX, d in [([[2,1],[1,1]], (1,2)), ([[3,1],[1,1]], (2,0)), ([[2,0],[0,4]], (4,2)), ([[5,2],[2,1]], (1,1)), ([[1,1],[1,2]], (3,-1)), ([[4,2],[2,2]], (2,4))]:
        a, b, c, e = map(F, (XX[0][0], XX[0][1], XX[1][0], XX[1][1])); det = a * e - b * c
        inv = [[e / det, -b / det], [-c / det, a / det]]; d = [F(x) for x in d]
        bias = [inv[0][0] * d[0] + inv[0][1] * d[1], inv[1][0] * d[0] + inv[1][1] * d[1]]
        cands = [d, [a * d[0] + b * d[1], c * d[0] + e * d[1]], [-x for x in bias], [d[0] / a, d[1] / e]]
        dis = [x for x in dict.fromkeys(v2(cv) for cv in cands) if x != v2(bias)][:3]
        stem = ("In the regression model y = Xβ + u with two regressors, X′X = %s and E(X′u) = δ = %s (X fixed). If b = (X′X)⁻¹X′y is the OLS estimator, "
                "then E(b − β) is") % (mat(XX), v2(d))
        why = ("b − β = (X′X)⁻¹X′u, so E(b − β) = (X′X)⁻¹E(X′u) = (X′X)⁻¹δ. Here (X′X)⁻¹ = %s (determinant %s), and multiplying by δ gives %s. "
               "OLS is unbiased only when E(X′u) = 0. Trap: (X′X)δ multiplies instead of solving, and δ alone forgets (X′X)⁻¹.") % (mat(inv), ff(det), v2(bias))
        out.append((stem, v2(bias), dis, why))
    for b1, b2, s11, s12, s22 in [(2, 3, 10, 4, 8), (1, -2, 5, 2, 6), (F(1,2), 4, 8, -2, 5), (3, 1, 20, 10, 9)]:
        b1, b2 = F(b1), F(b2); val = b1 + b2 * F(s12, s11)
        dis = [x for x in dict.fromkeys([ff(b1), ff(b1 + b2 * F(s12, s22)), ff(b2)]) if x != ff(val)][:3]
        stem = ("The true model is y = β₁x₁ + β₂x₂ + u with β₁ = %s, β₂ = %s and E(u) = 0 (no intercept; x₁, x₂ fixed with Σx₁² = %d, Σx₁x₂ = %s, Σx₂² = %d). "
                "If y is regressed on x₁ alone, b₁ = Σx₁y/Σx₁² has expectation") % (ff(b1), ff(b2), s11, ff(s12), s22)
        why = ("Substituting the true model: b₁ = Σx₁(β₁x₁ + β₂x₂ + u)/Σx₁² = β₁ + β₂Σx₁x₂/Σx₁² + Σx₁u/Σx₁². Taking expectations, E(b₁) = %s + %s × %s/%d = %s. "
               "This is omitted-variable bias: it vanishes only if β₂ = 0 or x₁ and x₂ are orthogonal. Trap: dividing by Σx₂² regresses x₁ on x₂ instead of x₂ on x₁.") % (
               ff(b1), ("(%s)" % ff(b2)) if b2 < 0 else ff(b2), ff(s12), s11, ff(val))
        out.append((stem, ff(val), dis, why))
    return out

def g_resid():           # 55125114559
    out = []
    specs = [("ee", 30, 4, 2), ("ee", 25, 5, 3), ("ee", 40, 6, F(1,2)), ("een", 20, 4, 5), ("een", 50, 5, 2), ("var", 20, 3, 4, F(1,5)), ("var", 15, 2, 6, F(1,3)),
             ("cov", 12, 3, 2, F(1,4)), ("s2", 30, 5, 3), ("yhat", 10, 2, 5, F(2,5))]
    for sp in specs:
        kind, n, k, s2 = sp[0], sp[1], sp[2], F(sp[3]); h = F(sp[4]) if len(sp) > 4 else None
        if kind == "ee": val = s2 * (n - k); ask = "E(e′e)"; cands = [s2 * n, s2 * k, s2 * (n - k - 1)]
        elif kind == "een": val = s2 * (n - k) / n; ask = "E(e′e/n)"; cands = [s2, s2 * (n - k), s2 * k / n]
        elif kind == "var": val = s2 * (1 - h); ask = "Var(eᵢ) for an observation with leverage hᵢᵢ = %s" % ff(h); cands = [s2, s2 * h, s2 * (1 + h)]
        elif kind == "cov": val = -s2 * h; ask = "Cov(eᵢ, eⱼ) for two observations with hᵢⱼ = %s (i ≠ j)" % ff(h); cands = [F(0), s2 * h, s2 * (1 - h)]
        elif kind == "s2": val = s2; ask = "E(s²), where s² = e′e/(n − k)"; cands = [s2 * (n - k) / n, s2 * (n - k), s2 * n / (n - k)]
        else: val = s2 * h; ask = "Var(ŷᵢ) for an observation with leverage hᵢᵢ = %s" % ff(h); cands = [s2, s2 * (1 - h), s2 * h * h]
        dis = [x for x in dict.fromkeys(ff(c) for c in cands) if x != ff(val)][:3]
        stem = ("In the linear model y = Xβ + u with X of order %d × %d and full column rank, E(u) = 0 and E(uu′) = σ²Iₙ with σ² = %s. With P = X(X′X)⁻¹X′, "
                "the residuals are e = (Iₙ − P)y. Then %s is") % (n, k, ff(s2), ask)
        why = ("Because (Iₙ − P)X = 0, e = (Iₙ − P)u, so E(ee′) = σ²(Iₙ − P), a symmetric idempotent matrix with trace n − k. Hence E(e′e) = σ²(n − k), "
               "Var(eᵢ) = σ²(1 − hᵢᵢ), Cov(eᵢ, eⱼ) = −σ²hᵢⱼ, and the fitted values ŷ = Py have Var(ŷᵢ) = σ²hᵢᵢ. With n = %d, k = %d and σ² = %s the requested quantity is %s. "
               "Trap: the residuals are not independent with variance σ²; they lose k degrees of freedom to the fit.") % (n, k, ff(s2), ff(val))
        out.append((stem, ff(val), dis, why))
    return out

def g_proj():            # 55125114561
    out = []
    specs = [("trP", 20, 3), ("trP", 35, 6), ("trM", 25, 4), ("trM", 18, 2), ("rkM", 30, 5), ("EyMy", 22, 4, 3), ("EyPy", 20, 3, 2, 50), ("EyPy", 40, 5, 4, 30),
             ("cross", 15, 3, 2), ("eig1", 28, 4)]
    for sp in specs:
        kind, n, k = sp[0], sp[1], sp[2]
        if kind == "trP": ask = "tr(P)"; val = F(k); cands = [n, n - k, 1]
        elif kind == "trM": ask = "tr(Iₙ − P)"; val = F(n - k); cands = [n, k, n - k - 1]
        elif kind == "rkM": ask = "the rank of Iₙ − P"; val = F(n - k); cands = [n, k, n - 1]
        elif kind == "eig1": ask = "the number of eigenvalues of P that equal 1"; val = F(k); cands = [n, n - k, 1]
        elif kind == "EyMy": s2 = F(sp[3]); ask = "E[y′(Iₙ − P)y] when σ² = %s" % ff(s2); val = s2 * (n - k); cands = [s2 * n, s2 * k, s2 * (n - k - 1)]
        elif kind == "EyPy": s2, q = F(sp[3]), F(sp[4]); ask = "E(y′Py) when σ² = %s and β′X′Xβ = %s" % (ff(s2), ff(q)); val = k * s2 + q; cands = [k * s2, q, n * s2 + q]
        else: s2 = F(sp[3]); ask = "E[(Py)′(Iₙ − P)y] when σ² = %s" % ff(s2); val = F(0); cands = [s2 * k, s2 * (n - k), s2]
        dis = [x for x in dict.fromkeys(ff(c) for c in cands) if x != ff(val)][:3]
        stem = ("In the linear model y = Xβ + u, X is %d × %d of full column rank, E(u) = 0 and E(uu′) = σ²Iₙ. With P = X(X′X)⁻¹X′, %s is") % (n, k, ask)
        why = ("P is the orthogonal projection onto the column space of X: symmetric and idempotent (P² = P), so its eigenvalues are 0 or 1 and tr(P) = rank(P) = k = %d; "
               "Iₙ − P projects onto the orthogonal complement, with trace and rank n − k = %d. For a quadratic form, E(y′Ay) = σ²tr(A) + β′X′AXβ; with A = Iₙ − P the second "
               "term vanishes, with A = P it equals β′X′Xβ, and P(Iₙ − P) = 0 makes the fitted values and residuals orthogonal. So the requested quantity is %s. "
               "Trap: tr(P) counts the columns of X (k), not the observations (n).") % (k, n - k, ff(val))
        out.append((stem, ff(val), dis, why))
    return out

def statement_sets(sets, intro, explain):
    allc = ["A only", "B only", "C only", "D only", "A, B only", "A, C only", "A, D only", "B, C only", "B, D only", "C, D only",
            "A, B, C only", "A, B, D only", "A, C, D only", "B, C, D only", "A, B, C, D"]
    out = []
    for ctx, sts in sets:
        truth = [L for L, (_, t, _) in zip("ABCD", sts) if t]
        corr = "A, B, C, D" if len(truth) == 4 else (", ".join(truth) + " only") if truth else None
        assert corr, ctx
        dis = sorted((x for x in allc if x != corr), key=lambda x: (abs(len(x) - len(corr)), sum(L in x for L in truth) * -1, x))[:3]
        stem = "%s Consider the following statements: A. %s. B. %s. C. %s. D. %s. Choose the correct answer from the options given below:" % (
            (intro + " " + ctx).strip(), sts[0][0], sts[1][0], sts[2][0], sts[3][0])
        why = " ".join("%s is %s: %s" % (L, "true" if t else "false", r) for L, (_, t, r) in zip("ABCD", sts)) + " So the answer is %s. %s" % (corr.replace(" only", ""), explain)
        out.append((stem, corr, dis, why))
    return out

RB = {
 "unb": ("E(h | T) is unbiased for θ", True, "E[E(h | T)] = E(h) = θ by the law of iterated expectations."),
 "var": ("Var{E(h | T)} ≤ Var(h)", True, "Var(h) = Var{E(h | T)} + E{Var(h | T)}, and the last term is non-negative."),
 "free": ("E(h | T) does not depend on θ", True, "the conditional distribution of the data given a sufficient T is free of θ, so E(h | T) is a genuine statistic."),
 "umvu_nc": ("E(h | T) is the unique UMVUE of θ", False, "uniqueness of the UMVUE needs T to be complete as well as sufficient, which is not given."),
 "umvu_c": ("E(h | T) is the unique UMVUE of θ", True, "with T complete and sufficient, Lehmann–Scheffé makes E(h | T) the unique UMVUE."),
 "strict": ("Var{E(h | T)} < Var(h) always", False, "equality holds when h is already a function of T."),
 "fn": ("If h is already a function of T, then E(h | T) = h", True, "conditioning on T leaves any function of T unchanged."),
 "needc": ("Rao–Blackwellisation reduces variance only when T is complete", False, "the variance reduction needs only sufficiency; completeness is needed for uniqueness."),
 "anyU": ("E(h | U) is an estimator for every statistic U", False, "if U is not sufficient, E(h | U) can depend on θ and then is not a statistic at all."),
 "mse": ("MSE{E(h | T)} ≤ MSE(h)", True, "conditioning keeps the mean and cannot increase the variance, so the mean squared error cannot rise."),
 "bias": ("E(h | T) has a smaller bias than h", False, "conditioning keeps the expectation, so the bias is unchanged (here both are unbiased).")}
def g_rb():              # 55125114543
    combos = [("", ["unb", "var", "umvu_nc", "free"]), ("T is also complete.", ["unb", "var", "umvu_c", "free"]), ("", ["strict", "fn", "needc", "unb"]),
              ("", ["anyU", "mse", "bias", "var"]), ("T is also complete.", ["umvu_c", "strict", "fn", "anyU"]), ("", ["free", "needc", "mse", "umvu_nc"]),
              ("", ["bias", "unb", "fn", "strict"]), ("T is also complete.", ["needc", "umvu_c", "mse", "bias"]), ("", ["var", "anyU", "free", "fn"]), ("", ["umvu_nc", "bias", "needc", "fn"])]
    sets = [(ctx, [RB[k] for k in ks]) for ctx, ks in combos]
    return statement_sets(sets, "Let h be an unbiased estimator of θ with E(h²) < ∞, and let T be a sufficient statistic.",
                          "Trap: Rao–Blackwell needs only sufficiency; Lehmann–Scheffé adds completeness to get uniqueness.")

PIVOTS = [  # (setting, quantity, correct, distractors, explanation)
 ("X₁, …, Xₙ iid N(μ, σ²)", "(X̄ − μ)/(S/√n), where S² = Σ(Xᵢ − X̄)²/(n − 1)", "μ when σ² is unknown", ["μ when σ² is known only", "σ² when μ is known", "both μ and σ² jointly"],
  "It has a t distribution with n − 1 df whatever μ and σ are, and it contains only μ as an unknown, so it gives intervals for μ without knowing σ."),
 ("X₁, …, Xₙ iid N(μ, σ²)", "Σ(Xᵢ − μ)²/σ²", "σ² when μ is known", ["σ² when μ is unknown", "μ when σ² is known", "both μ and σ² jointly"],
  "It is χ² with n df, free of the parameters, but computing it needs μ, so it serves for σ² only when μ is known."),
 ("X₁, …, Xₙ iid N(μ, σ²)", "(n − 1)S²/σ²", "σ² when μ is unknown", ["μ when σ² is unknown", "μ when σ² is known", "neither μ nor σ²: it is not a pivot"],
  "It is χ² with n − 1 df and involves only σ² (μ is estimated by X̄ inside S²), so it gives intervals for σ² with μ unknown."),
 ("X₁, …, Xₙ iid Uniform(0, θ)", "X₍ₙ₎/θ, where X₍ₙ₎ is the sample maximum", "θ", ["θ only when n is large", "no parameter: its distribution depends on θ", "1/θ² only"],
  "P(X₍ₙ₎/θ ≤ t) = tⁿ on (0, 1) whatever θ is, so it is a pivot and can be inverted for θ."),
 ("X₁, …, Xₙ iid with pdf λe^(−λx), x > 0", "2λΣXᵢ", "λ", ["λ only when n is large", "no parameter: its distribution depends on λ", "the mean only when λ is known"],
  "2λΣXᵢ is χ² with 2n df for every λ, so it is an exact pivot for λ."),
 ("X₁, …, Xₙ iid exponential with mean θ", "ΣXᵢ/θ", "θ", ["θ only when n is large", "no parameter: its distribution depends on θ", "θ² only"],
  "ΣXᵢ/θ has a Gamma(n, 1) distribution free of θ, so it is a pivot for θ."),
 ("X₁, …, Xₙ iid N(μ, σ²) with σ unknown", "X̄ − μ", "no parameter: its distribution depends on the unknown σ", ["μ", "σ²", "both μ and σ² jointly"],
  "X̄ − μ ~ N(0, σ²/n), so its distribution involves the unknown σ; it is not a pivot until it is divided by S/√n."),
 ("independent samples from N(μ₁, σ²) and N(μ₂, σ²), sizes m and n, common σ² unknown", "[(X̄ − Ȳ) − (μ₁ − μ₂)]/[Sₚ√(1/m + 1/n)], with Sₚ² the pooled variance",
  "μ₁ − μ₂", ["σ²", "μ₁/μ₂", "no parameter: its distribution depends on σ²"],
  "It has a t distribution with m + n − 2 df whatever the parameters are, so it is a pivot for the difference in means."),
 ("independent samples from N(μ₁, σ₁²) and N(μ₂, σ₂²), sizes m and n", "(S₁²/σ₁²)/(S₂²/σ₂²)", "σ₁²/σ₂²", ["μ₁ − μ₂", "σ₁² − σ₂²", "no parameter: its distribution depends on σ₁ and σ₂"],
  "It has an F distribution with (m − 1, n − 1) df free of all parameters, and it involves only the ratio σ₁²/σ₂²."),
 ("X₁, …, Xₙ iid with pdf e^(−(x − θ)), x > θ", "X₍₁₎ − θ, where X₍₁₎ is the sample minimum", "θ", ["θ only when n is large", "no parameter: its distribution depends on θ", "e^θ only"],
  "X₍₁₎ − θ is exponential with rate n for every θ, so it is a pivot and gives exact intervals for θ.")]
def g_pivot():           # 55125114536
    out = []
    for setting, qty, corr, dis, ex in PIVOTS:
        stem = "Suppose we have %s. The quantity %s can be used as a pivot to obtain a confidence interval for" % (setting, qty)
        why = "A pivot is a function of the data and the parameter whose distribution does not depend on any unknown parameter. " + ex + \
              " Trap: a quantity whose distribution still involves an unknown nuisance parameter is not a pivot."
        out.append((stem, corr, dis, why))
    return out

SAMPST = {
 "wr": ("Simple random sampling with replacement is more efficient than without replacement (same n)", False, "SRSWOR has variance (1 − n/N)S²/n, smaller than SRSWR's σ²/n."),
 "ratio": ("The usual ratio estimator of the population mean is biased", True, "it is a ratio of random variables; its bias is of order 1/n."),
 "clneg": ("Cluster sampling is more efficient than SRSWOR when the intraclass correlation is negative", True, "the design effect 1 + (M − 1)ρ falls below 1 when ρ < 0."),
 "sys": ("Systematic sampling beats SRS when the intraclass correlation within systematic samples exceeds −1/(nk − 1)", False, "it beats SRS when that correlation is LESS than −1/(nk − 1)."),
 "prop": ("Stratified sampling with proportional allocation is at least as efficient as SRS (large N)", True, "V(SRS) − V(prop) ≈ (1 − f)/n · ΣWₕ(Ȳₕ − Ȳ)² ≥ 0."),
 "ney": ("Neyman allocation minimises the variance of the stratified mean for a fixed total sample size", True, "minimising ΣWₕ²Sₕ²/nₕ subject to Σnₕ = n gives nₕ ∝ NₕSₕ."),
 "ht": ("The Horvitz–Thompson estimator is unbiased for the population total", True, "E(Σ yᵢ/πᵢ over the sample) = Σ πᵢ·yᵢ/πᵢ = Y."),
 "reg": ("The regression estimator is unbiased for every sample size", False, "with an estimated slope it is biased; the bias is of order 1/n."),
 "fpc": ("The finite population correction (1 − n/N) increases the variance", False, "it is at most 1, so it reduces the variance."),
 "trend": ("For a population with a linear trend, systematic sampling is more efficient than SRS", True, "the systematic sample spreads over the trend, so V(sys) ≤ V(SRS)."),
 "clpos": ("Cluster sampling with positive intraclass correlation is more efficient than SRS of the same number of elements", False, "a positive ρ makes the design effect exceed 1."),
 "dbl": ("Double sampling is used when the population mean of the auxiliary variable is unknown", True, "the first-phase sample estimates the auxiliary mean."),
 "pps": ("PPS sampling gives every unit the same selection probability", False, "selection probabilities are proportional to size."),
 "rcond": ("The ratio estimator beats the sample mean when ρ > (1/2)(Cₓ/Cᵧ)", True, "this is the first-order efficiency condition for the ratio estimator.")}
def g_sampst():          # 55125114533
    combos = [["wr", "ratio", "clneg", "sys"], ["prop", "ney", "ht", "reg"], ["fpc", "trend", "clpos", "dbl"], ["pps", "rcond", "wr", "ht"], ["ratio", "sys", "prop", "fpc"],
              ["clneg", "reg", "trend", "pps"], ["ney", "clpos", "rcond", "dbl"], ["ht", "wr", "reg", "trend"], ["dbl", "pps", "ratio", "ney"], ["sys", "clpos", "fpc", "rcond"]]
    return statement_sets([("", [SAMPST[k] for k in ks]) for ks in combos], "Statements about sampling methods.",
                          "Trap: check the direction of each inequality — several statements reverse a correct condition.")

DESST = {
 "rand": ("Randomization makes the estimate of experimental error valid", True, "it guards against systematic bias in the allocation of treatments."),
 "rep": ("Replication provides an estimate of experimental error", True, "error is measured by the variation between units given the same treatment."),
 "lc": ("Local control (blocking) reduces experimental error", True, "it removes variation between blocks from the error."),
 "crdlc": ("A completely randomized design uses local control", False, "a CRD has no blocking."),
 "rbd3": ("A randomized block design uses all three principles", True, "it randomizes within blocks, replicates across blocks and blocks for local control."),
 "lsd2": ("A Latin square design controls variation in two directions", True, "rows and columns are both blocking factors."),
 "repup": ("Increasing replication increases the error variance of a treatment mean", False, "the variance of a mean falls as σ²/r."),
 "crddf": ("In a CRD with t treatments and N units the error degrees of freedom are N − t", True, "N − 1 total minus t − 1 for treatments."),
 "randrep": ("Randomization removes the need for replication", False, "without replication there is no estimate of error at all."),
 "bibd": ("A BIBD is used when a block cannot hold all the treatments", True, "blocks are incomplete but balanced."),
 "rbdinc": ("In an RBD a block need not contain every treatment", False, "each block of an RBD is complete."),
 "conf": ("Confounding in factorial experiments gives up information on some interactions to reduce block size", True, "chosen high-order interactions are mixed with blocks."),
 "lsdn": ("A Latin square with t treatments needs t² rows", False, "it needs t rows and t columns, i.e. t² units."),
 "crdhom": ("A CRD is most suitable when the experimental units are homogeneous", True, "with no known source of variation there is nothing to block on.")}
def g_desst():           # 55125114534
    combos = [["rand", "rep", "lc", "crdlc"], ["rbd3", "lsd2", "repup", "crddf"], ["randrep", "bibd", "rbdinc", "conf"], ["lsdn", "crdhom", "rand", "rbdinc"], ["crdlc", "rbd3", "bibd", "lsdn"],
              ["rep", "repup", "conf", "crdhom"], ["lc", "randrep", "lsd2", "crddf"], ["crddf", "rbdinc", "rand", "lsdn"], ["bibd", "crdlc", "repup", "lsd2"], ["conf", "rep", "randrep", "rbd3"]]
    return statement_sets([("", [DESST[k] for k in ks]) for ks in combos], "Statements about the principles and layouts of experimental design.",
                          "Trap: the three principles are randomization, replication and local control; a CRD uses only the first two.")

BATCH4 = [("55125114556", "regression", g_bias), ("55125114559", "regression", g_resid), ("55125114561", "regression", g_proj),
          ("55125114543", "inference", g_rb), ("55125114536", "inference", g_pivot), ("55125114533", "sampling", g_sampst), ("55125114534", "design", g_desst)]

BATCH = [  # (official question ID, module, generator)
    ("55125114584", "stochastic", g_ruin), ("55125114581", "stochastic", g_memoryless), ("55125114585", "stochastic", g_poisson_split),
    ("55125114597", "stochastic", g_nstep), ("55125114599", "stochastic", g_first_passage),
    ("55125114568", "timeseries", g_ar1_var), ("55125114605", "timeseries", g_ar1_acov),
    ("55125114527", "design", g_rbd), ("55125114526", "design", g_anova_f),
    ("55125114530", "sampling", g_neyman), ("55125114558", "regression", g_adjr2), ("55125114563", "regression", g_dw),
    ("55125114508", "probability", g_mgf)] + BATCH2 + BATCH3 + BATCH4

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
