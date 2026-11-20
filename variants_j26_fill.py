#!/usr/bin/env python3
"""Gap-fill variants for June 2026 Paper 2 booklet questions 1-50, so that every one of them has at least ten variants.

The existing variant banks hold 501 variants for booklet Q1-Q50, unevenly. This adds exactly what is missing (49 variants)
and removes nothing: variant ids carry learner progress. Ids use the prefix j26v-gNN-MM (g = gap fill), because some legacy
ids do not follow their question number and a fresh prefix cannot collide with them.
Output: seed/<module>_j26fill_pyq_variants.json (the _pyq_variants suffix makes them variant banks; srcQ is the booklet number).
Every number is computed here; R output was confirmed with R 4.5.1. Check with verify_j26_fill_variants.py."""
import json
from fractions import Fraction as F
from pathlib import Path

R = Path(__file__).resolve().parent
NEED = {1: 2, 2: 1, 5: 1, 11: 4, 14: 4, 20: 1, 22: 10, 23: 1, 25: 1, 27: 1, 29: 1, 30: 1, 34: 1, 38: 6, 41: 8, 42: 1, 44: 1, 45: 1, 48: 3}
MODULE = {1: "maths", 2: "multivariate", 5: "maths", 11: "regression", 14: "inference", 20: "multivariate", 22: "rprog", 23: "timeseries", 25: "probability",
          27: "maths", 29: "maths", 30: "inference", 34: "probability", 38: "regression", 41: "nonparam", 42: "nonparam", 44: "probability", 45: "probability", 48: "rprog"}

def ff(x):
    x = F(x); return (str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)).replace("-", "−")
def d(x, k): return ("%." + str(k) + "f") % float(x)
def combo(tr): return "A, B, C, D" if len(tr) == 4 else ", ".join(tr) + " only"
ALLC = ["A only", "B only", "C only", "D only", "A, B only", "A, C only", "A, D only", "B, C only", "B, D only", "C, D only", "A, B, C only", "A, B, D only", "A, C, D only", "B, C, D only", "A, B, C, D"]
def near(corr): return sorted((x for x in ALLC if x != corr), key=lambda x: (abs(len(x) - len(corr)), x))[:3]

def q1():   # nullity / rank of a product
    out = []
    for n, a, b, kind in [(6, 4, 5, "rank"), (7, 2, 3, "nullity")]:
        if kind == "rank":
            lo, hi = max(0, a + b - n), min(a, b); val = lo; cands = [lo - 1, hi + 1, a + b]
            stem = "A and B are %d × %d matrices with rank(A) = %d and rank(B) = %d. Which of the following is a possible value of rank(AB)?" % (n, n, a, b)
            why = ("Sylvester's inequality gives rank(A) + rank(B) − n ≤ rank(AB) ≤ min{rank(A), rank(B)}, i.e. %d ≤ rank(AB) ≤ %d. Only %d lies in that range. "
                   "Trap: rank(AB) can never exceed the smaller rank, and adding the ranks overshoots.") % (lo, hi, val)
        else:
            lo, hi = max(a, b), a + b; val = hi; cands = [lo - 1, hi + 1, min(a, b) - 1 if min(a, b) > 1 else hi + 2]
            stem = "A and B are %d × %d matrices with nullity υ(A) = %d and υ(B) = %d. Which of the following is a possible value of υ(AB)?" % (n, n, a, b)
            why = ("For square matrices, max{υ(A), υ(B)} ≤ υ(AB) ≤ υ(A) + υ(B) (equivalent to Sylvester's rank inequality), i.e. %d ≤ υ(AB) ≤ %d. Only %d lies in that range. "
                   "Trap: the nullity of a product is at least the larger nullity, never the smaller.") % (lo, hi, val)
        out.append((stem, str(val), [str(c) for c in cands], why))
    return out

def q2():   # equicorrelation principal components
    p, rho = 4, F(1, 3); big = 1 + (p - 1) * rho; small = 1 - rho; share = big / p
    sts = [("The first principal component is (1/2)(X₁ + X₂ + X₃ + X₄)", True), ("The largest eigenvalue of Σ is %s" % ff(big), True),
           ("The first principal component explains %s%% of the total variability" % ff(share * 100), True), ("The smallest eigenvalue of Σ is %s" % ff(rho), False)]
    corr = combo([L for L, (_, t) in zip("ABCD", sts) if t])
    stem = ("X = (X₁, X₂, X₃, X₄)′ has E(X) = 0 and a covariance matrix Σ with 1 on the diagonal and 1/3 everywhere else. Consider: A. %s. B. %s. C. %s. D. %s. "
            "Choose the correct answer from the options given below:") % tuple(s for s, _ in sts)
    why = ("An equicorrelation matrix with p = 4 and ρ = 1/3 has eigenvalues 1 + 3ρ = %s (once, eigenvector (1, 1, 1, 1)/2) and 1 − ρ = %s (three times). The total variance is 4, "
           "so the first component explains %s/4 = %s%%. The smallest eigenvalue is %s, not ρ. Trap: the eigenvalues are 1 + (p − 1)ρ and 1 − ρ, not ρ itself.") % (
           ff(big), ff(small), ff(big), ff(share * 100), ff(small))
    return [(stem, corr, near(corr), why)]

def q5():
    n, k = 10, 3
    stem = "X is a %d × %d matrix of rank %d and P = Iₙ − X(X′X)⁻¹X′. The trace of P is" % (n, k, k)
    why = ("P is symmetric and idempotent, with n − k = %d eigenvalues equal to 1 and k = %d equal to 0, so tr(P) = n − k = %d. "
           "Trap: X(X′X)⁻¹X′ has trace k; subtracting it from Iₙ leaves n − k.") % (n - k, k, n - k)
    return [(stem, str(n - k), [str(k), str(n), "1"], why)]

def lin(coefs):
    """(a y₁ + b y₂ + c y₃)/d with integers."""
    from math import gcd
    den = 1
    for c in coefs: den = den * c.denominator // gcd(den, c.denominator)
    nums = [int(c * den) for c in coefs]; parts = []
    for num, sym in zip(nums, ("y₁", "y₂", "y₃")):
        if num == 0: continue
        mag = "" if abs(num) == 1 else str(abs(num))
        parts.append((("−" if num < 0 else "") + mag + sym) if not parts else (("− " if num < 0 else "+ ") + mag + sym))
    body = " ".join(parts)
    return body if den == 1 else "(%s)/%d" % (body, den)
def blue(X):
    XtX = [[sum(X[r][a] * X[r][b] for r in range(3)) for b in range(2)] for a in range(2)]
    det = F(XtX[0][0] * XtX[1][1] - XtX[0][1] * XtX[1][0]); inv = [[XtX[1][1] / det, -XtX[0][1] / det], [-XtX[1][0] / det, XtX[0][0] / det]]
    return [[sum(inv[a][c] * X[r][c] for c in range(2)) for r in range(3)] for a in range(2)]
def q11():
    out = []
    for X, which in [([[1, 1], [2, 0], [1, -1]], 1), ([[1, 2], [1, 0], [1, -2]], 2), ([[1, 1], [1, -1], [2, 0]], 1), ([[2, 1], [0, 1], [1, -2]], 2)]:
        B = blue(X); corr = lin(B[which - 1]); other = lin(B[2 - which])
        naive = lin([F(X[r][which - 1]) for r in range(3)]); avg = lin([F(X[r][which - 1], 3) for r in range(3)])
        dis = [x for x in dict.fromkeys([other, naive, avg]) if x != corr][:3]
        eq = "; ".join("y%s = %s + u%s" % ("₁₂₃"[r], " + ".join(("%sβ%s" % ("" if X[r][c] == 1 else ("−" if X[r][c] == -1 else str(X[r][c]).replace("-", "−")), "₁₂"[c])) for c in range(2) if X[r][c] != 0).replace("+ −", "− "), "₁₂₃"[r]) for r in range(3))
        stem = "Let %s with uncorrelated errors of variance σ². The best linear unbiased estimator of β%s is" % (eq, "₁₂"[which - 1])
        why = ("By the Gauss–Markov theorem the BLUE is the OLS estimator b = (X′X)⁻¹X′y with design matrix X = %s. Here X′X = %s, and the row of (X′X)⁻¹X′ for β%s gives %s. "
               "Trap: X′y without (X′X)⁻¹ is not unbiased, and the other row estimates the other coefficient.") % (
               str(X).replace("-", "−"), str([[sum(X[r][a] * X[r][b] for r in range(3)) for b in range(2)] for a in range(2)]).replace("-", "−"), "₁₂"[which - 1], corr)
        out.append((stem, corr, dis, why))
    return out

def q14():
    out = []
    specs = [
     ("X₁, …, Xₙ is a random sample from f(x; θ) = θe^(−θx), x > 0", "H₁: θ > θ₀", "Σxᵢ ≤ (1/(2θ₀))·χ²(1−α, 2n)",
      ["Σxᵢ ≥ (1/(2θ₀))·χ²(α, 2n)", "(1/(2θ₀))·χ²(α, 2n) ≤ Σxᵢ ≤ (1/(2θ₀))·χ²(1−α, 2n)", "No UMP test exists"],
      "The family has a monotone likelihood ratio in −Σxᵢ, so for the one-sided H₁: θ > θ₀ a UMP test rejects for small Σxᵢ. Under H₀, 2θ₀ΣXᵢ ~ χ²(2n), so the cut-off is χ²(1−α, 2n)/(2θ₀) (the lower α point)."),
     ("X₁, …, Xₙ is a random sample from f(x; θ) = θe^(−θx), x > 0", "H₁: θ < θ₀", "Σxᵢ ≥ (1/(2θ₀))·χ²(α, 2n)",
      ["Σxᵢ ≤ (1/(2θ₀))·χ²(1−α, 2n)", "(1/(2θ₀))·χ²(α, 2n) ≤ Σxᵢ ≤ (1/(2θ₀))·χ²(1−α, 2n)", "No UMP test exists"],
      "Smaller θ means larger observations, so the UMP test for H₁: θ < θ₀ rejects for large Σxᵢ; with 2θ₀ΣXᵢ ~ χ²(2n) under H₀ the cut-off is χ²(α, 2n)/(2θ₀)."),
     ("X₁, …, Xₙ is a random sample from N(μ, 1)", "H₁: μ ≠ μ₀", "No UMP test exists",
      ["X̄ ≥ μ₀ + z_α/√n", "X̄ ≤ μ₀ − z_α/√n", "|X̄ − μ₀| ≥ z_(α/2)/√n is UMP"],
      "The most powerful test against μ > μ₀ rejects for large X̄ and against μ < μ₀ for small X̄; no single test is best on both sides, so no UMP test exists (the two-sided test is UMP unbiased only)."),
     ("X₁, …, Xₙ is a random sample from Poisson(λ)", "H₁: λ > λ₀", "reject H₀ for large Σxᵢ (randomizing at the boundary if needed)",
      ["reject H₀ for small Σxᵢ", "reject H₀ when Σxᵢ is far from nλ₀ on either side", "No UMP test exists"],
      "The Poisson family has a monotone likelihood ratio in Σxᵢ, so by Karlin–Rubin the UMP test for the one-sided H₁: λ > λ₀ rejects for large Σxᵢ; randomization attains size α exactly.")]
    for samp, h1, corr, dis, ex in specs:
        stem = "%s. For testing H₀: %s against %s at level α%s, the uniformly most powerful (UMP) critical region is" % (
            samp, h1.split(":")[1].strip().replace(">", "=").replace("<", "=").replace("≠", "="), h1, " (χ²(α, ν) is the upper α point of χ² with ν df)" if "χ²" in corr + "".join(dis) else "")
        stem = stem.replace("H₀: θ = θ₀ against", "H₀: θ = θ₀ against").replace("H₀: μ = μ₀", "H₀: μ = μ₀")
        out.append((stem, corr, dis, ex + " Trap: a UMP test exists for one-sided alternatives in a family with a monotone likelihood ratio, but not for a two-sided one."))
    return out

def q20():
    stem = ("X = (x₁, x₂, x₃, x₄)′ has E(X) = 0 and Σ = [[1, 0, 0.6, 0], [0, 1, 0, 0.3], [0.6, 0, 1, 0], [0, 0.3, 0, 1]]. With x⁽¹⁾ = (x₁, x₂)′ and x⁽²⁾ = (x₃, x₄)′, "
            "the largest canonical correlation between x⁽¹⁾ and x⁽²⁾ is")
    why = ("Here Σ₁₁ = Σ₂₂ = I and Σ₁₂ = diag(0.6, 0.3), so the squared canonical correlations are the eigenvalues of Σ₁₂Σ₂₂⁻¹Σ₂₁Σ₁₁⁻¹ = diag(0.36, 0.09). "
           "The largest canonical correlation is √0.36 = 0.60. Trap: 0.36 is its square, and 0.45 averages the two correlations.")
    return [(stem, "0.60", ["0.36", "0.45", "0.30"], why)]

RS22 = [  # (R code, output, distractors, explanation)
 ("f = function (n) { x = 1; for (i in 1:n) { x = x * i }; x }\nf(4)", "24", ["4", "10", "1"], "the loop multiplies x by 1, 2, 3, 4, so f(4) = 4! = 24; 10 would be the sum"),
 ("f = function (n) { s = 0; for (i in 1:n) { s = s + i^2 }; s }\nf(3)", "14", ["6", "9", "36"], "s accumulates 1² + 2² + 3² = 14; 6 is 1 + 2 + 3 and 36 is (1 + 2 + 3)²"),
 ("f = function (n) { x = 0; for (i in 1:n) { x = x + 2 }; x }\nf(5)", "10", ["5", "15", "32"], "2 is added five times, so x = 10; 32 would be 2⁵"),
 ("f = function (n) { x = 1; while (x < n) { x = x * 2 }; x }\nf(20)", "32", ["16", "20", "64"], "x doubles 1, 2, 4, 8, 16, 32 and stops as soon as x < 20 fails, i.e. at 32; 16 is the last value that was still below 20"),
 ("f = function (v) { s = 0; for (e in v) { if (e > 0) s = s + e }; s }\nf(c(3, -1, 4, -5, 2))", "9", ["3", "-6", "15"], "only the positive elements 3, 4 and 2 are added, giving 9; the plain sum would be 3"),
 ("f = function (n) { x = 0; for (i in 1:n) { for (j in 1:i) { x = x + 1 } }; x }\nf(4)", "10", ["16", "4", "24"], "the inner loop runs i times, so x = 1 + 2 + 3 + 4 = 10; 16 would be 4 × 4"),
 ("f = function (n) { x = 1; for (i in seq(1, n, by = 2)) { x = x * i }; x }\nf(7)", "105", ["5040", "16", "48"], "seq(1, 7, by = 2) is 1, 3, 5, 7, whose product is 105; 5040 is 7!"),
 ("f = function (n) { v = numeric(0); for (i in 1:n) { v = c(v, i * i) }; sum(v) }\nf(4)", "30", ["10", "16", "100"], "v grows to (1, 4, 9, 16) and its sum is 30; 16 is only the last element"),
 ("f = function (n) { x = 10; for (i in 1:n) { x = x - i }; x }\nf(4)", "0", ["6", "-10", "10"], "10 − 1 − 2 − 3 − 4 = 0; 6 would subtract only 4"),
 ("f = function (n) { k = 0; repeat { k = k + 1; if (k^2 > n) break }; k }\nf(30)", "6", ["5", "30", "36"], "the loop stops at the first k with k² > 30, which is k = 6 (36 > 30); 5 is the last k with k² ≤ 30")]
def q22():
    out = []
    for code, ans, dis, ex in RS22:
        lines = code.split("\n")
        stem = "Given the R program\n  %s\n  %s\nwhich of the following is the output?" % (lines[0], lines[1])
        disp = lambda s: "[1] " + s.replace("-", "−")
        out.append((stem.replace("-", "−"), disp(ans), [disp(x) for x in dis],
                    "Trace the loop: " + ex.replace("-", "−") + ". Trap: check exactly when the loop stops and what is accumulated. (Output confirmed by running the code in R 4.5.1.)"))
    return out

def q23():
    stem = "For the random walk yₜ = μ + yₜ₋₁ + εₜ, where {εₜ} is white noise with variance σ² = 4, the variance of yₜ − yₜ₋₃ is"
    why = ("yₜ − yₜ₋₃ = 3μ + εₜ + εₜ₋₁ + εₜ₋₂, a sum of three uncorrelated shocks, so its variance is 3σ² = 12; the drift μ only shifts the mean. "
           "Trap: the variance of a random walk grows with the number of steps, so it is not just σ² = 4.")
    return [(stem, "12", ["4", "36", "3"], why)]

def q25():
    stem = "Let X and Y be independent, each exponential with parameter λ. Then P(X ≤ 1 | X + Y = 4) is"
    why = ("Given X + Y = s, X is uniform on (0, s) for independent exponentials with the same rate: the joint density λ²e^(−λs) does not depend on how s is split. "
           "So P(X ≤ 1 | X + Y = 4) = 1/4, whatever λ is. Trap: 1 − e^(−λ) is the unconditional P(X ≤ 1).")
    return [(stem, "1/4", ["1/2", "1 − e^(−λ)", "e^(−λ)"], why)]

def q27():
    stem = ("Arrange the following statements of an R programme in the correct order to make a valid program. A. > y <- x * 2  B. > sum(y)  C. > x <- c(2, 3)  D. [1] 10  "
            "Choose the correct answer from the options given below:")
    why = ("x must exist before y is computed from it, y before it is summed, and the printed output comes last: C (x <- c(2, 3)), A (y = (4, 6)), B (sum(y)), D ([1] 10). "
           "Trap: an output line can only follow the command that produces it. (Output confirmed in R 4.5.1.)")
    return [(stem, "C, A, B, D", ["A, C, B, D", "C, B, A, D", "D, C, A, B"], why)]

def q29():
    obs = [12, 25, 33, 10]; n = 80; exp_ = [F(n, 8), F(3 * n, 8), F(3 * n, 8), F(n, 8)]
    chi = sum((F(o) - e) ** 2 / e for o, e in zip(obs, exp_)); wrong = sum((F(o) - e) ** 2 / o for o, e in zip(obs, exp_))
    stem = ("3 coins are tossed 80 times with observed frequencies of 0, 1, 2, 3 heads equal to 12, 25, 33, 10. Assuming the coins are unbiased, the χ² goodness-of-fit "
            "statistic is (to three decimals)")
    why = ("Under fairness the number of heads is Binomial(3, 1/2) with probabilities 1/8, 3/8, 3/8, 1/8, so the expected frequencies are 10, 30, 30, 10. "
           "χ² = Σ(O − E)²/E = 4/10 + 25/30 + 9/30 + 0/10 = %s. Trap: dividing by the observed instead of the expected frequencies gives %s.") % (d(chi, 3), d(wrong, 3))
    return [(stem, d(chi, 3), [d(wrong, 3), d(chi - F(4, 10), 3), d(chi * 2, 3)], why)]

def q30():
    sts = [("0 ≤ λ ≤ 1", True), ("−2 logₑ λ is asymptotically χ² under H₀, with degrees of freedom equal to the number of restrictions", True),
           ("λ can exceed 1 when H₀ is false", False), ("−2 logₑ λ ~ N(0, 1) asymptotically", False)]
    corr = combo([L for L, (_, t) in zip("ABCD", sts) if t])
    stem = ("For testing H₀: θ ∈ Θ₀ against H₁: θ ∈ Θ₁ with Θ = Θ₀ ∪ Θ₁, the likelihood ratio statistic is λ = sup over Θ₀ of the likelihood divided by sup over Θ. "
            "Consider: A. %s. B. %s. C. %s. D. %s. Choose the correct answer from the options given below:") % tuple(s for s, _ in sts)
    why = ("The numerator maximises over a subset of the parameter space, so it cannot exceed the denominator: 0 ≤ λ ≤ 1 always (A true, C false). "
           "By Wilks' theorem −2 log λ is asymptotically χ² with df equal to the number of independent restrictions (B true, D false). Trap: the limit is χ², not normal.")
    return [(stem, corr, near(corr), why)]

def q34():
    stem = "A₁, A₂, …, Aₙ are independent events with P(Aᵢ) = 1 − 1/3^i, i = 1, 2, …, n. The probability that at least one of them occurs is"
    why = ("P(none occurs) = Π P(Aᵢᶜ) = Π 3^(−i) = 3^(−(1 + 2 + … + n)) = 3^(−n(n+1)/2), so P(at least one) = 1 − 1/3^(n(n+1)/2). "
           "Trap: 1 − 1/3ⁿ uses only the last event.")
    return [(stem, "1 − 1/3^(n(n+1)/2)", ["1 − 1/3ⁿ", "1/3^(n(n+1)/2)", "1 − 1/2^(n(n+1)/2)"], why)]

NOTCONS = [  # (problem, three genuine consequences, the non-consequence, explanation)
 ("heteroscedastic errors", ["The usual OLS standard errors are biased", "OLS is no longer BLUE", "Tests based on the usual t and F statistics are unreliable"], "OLS estimates of β are biased",
  "With heteroscedasticity OLS stays unbiased (E(u) = 0 is all unbiasedness needs) but loses efficiency, and the usual variance formula σ²(X′X)⁻¹ is wrong."),
 ("positively autocorrelated errors", ["The usual OLS standard errors are understated", "OLS is no longer efficient", "The Durbin–Watson statistic tends to be below 2"], "OLS estimates of β are biased (with fixed regressors)",
  "Autocorrelation leaves OLS unbiased when the regressors are fixed, but it is inefficient and the conventional standard errors are too small."),
 ("perfect multicollinearity", ["X′X is singular", "The individual coefficients cannot be estimated uniquely", "Some linear combinations of β are still estimable"], "The fitted values ŷ cannot be computed",
  "With an exact linear dependence (X′X)⁻¹ does not exist, so individual β's are not identified, yet the projection of y on the column space — the fitted values — is still unique."),
 ("omitting a relevant regressor correlated with the included ones", ["The included coefficients are biased", "The included coefficients are inconsistent", "The error variance is overestimated"], "The included coefficients remain unbiased",
  "The omitted variable's effect is absorbed by the included regressors it is correlated with: E(b₁) = β₁ + (X₁′X₁)⁻¹X₁′X₂β₂ ≠ β₁."),
 ("including an irrelevant regressor", ["The coefficient estimates remain unbiased", "Their variances generally increase", "Some degrees of freedom are lost"], "The coefficient estimates become biased",
  "An extra regressor with true coefficient 0 keeps OLS unbiased; the cost is precision (larger variances) and degrees of freedom."),
 ("classical measurement error in a regressor", ["The slope estimate is biased towards zero", "The slope estimate is inconsistent", "The bias does not vanish as n grows"], "The slope estimate is unbiased",
  "Noise in x makes the regressor correlated with the composite error, so b is attenuated: plim b = β·Var(x*)/(Var(x*) + Var(noise)).")]
def q38():
    out = []
    for prob, cons, nc, ex in NOTCONS:
        stem = "Which of the following is not a consequence of %s on ordinary least squares estimation?" % prob
        out.append((stem, nc, cons, ex + " So '%s' is the one that does not follow. Trap: unbiasedness needs only E(u | X) = 0; most violations damage efficiency or standard errors instead." % nc))
    return out

def q41():
    out = []
    for n, xs in [(10, [2, 3, 5, 6]), (8, [1, 2, 4]), (12, [3, 4, 4, 7, 9]), (6, [2, 5]), (15, [1, 1, 2, 3]), (9, [4, 6, 7]), (20, [2, 3, 3, 5, 6, 8]), (7, [3, 4, 6, 9])]:
        r = len(xs); s = sum(xs); xr = xs[-1]
        val = F(s + (n - r) * xr, r)
        cands = [F(s, r), F(s + (r - 1) * xr, r), F(s + n * xr, r), F(s + (n - r) * xr, n)]
        dis = [x for x in dict.fromkeys(ff(c) for c in cands) if x != ff(val)][:3]
        stem = ("%d items with exponential lifetimes of mean θ are put on test, and the test stops at the %s failure. The failure times are %s. "
                "The unbiased estimate of θ based on the first r = %d order statistics is") % (n, ["", "first", "second", "third", "fourth", "fifth", "sixth"][r], ", ".join(map(str, xs)), r)
        why = ("For type II censoring the total time on test is Σᵢ₌₁ʳ X₍ᵢ₎ + (n − r)X₍ᵣ₎: the r failures plus the n − r survivors, each observed up to X₍ᵣ₎. It is θ times a "
               "Gamma(r, 1) variable, so dividing by r gives an unbiased estimator: (%d + %d × %d)/%d = %s. Trap: the plain average of the failure times ignores the %d survivors and "
               "underestimates θ.") % (s, n - r, xr, r, ff(val), n - r)
        out.append((stem, ff(val), dis, why))
    return out

def q42():
    A = [65, 57, 74, 43, 39]; B = [85, 87, 72, 98, 90]
    U1 = sum((1 if a > b else F(1, 2) if a == b else 0) for a in A for b in B); U2 = len(A) * len(B) - U1
    stem = ("Two independent groups give scores ES: 65, 57, 74, 43, 39 and LC: 85, 87, 72, 98, 90. The Mann–Whitney U statistic (the smaller of U_ES and U_LC) is")
    why = ("U_ES counts the pairs in which an ES score beats an LC score: only 74 beats 72, so U_ES = %s, and U_LC = 5 × 5 − %s = %s. The statistic is the smaller, %s. "
           "Trap: U_ES + U_LC = n₁n₂ = 25, so the larger value %s is just the complement.") % (ff(U1), ff(U1), ff(U2), ff(min(U1, U2)), ff(max(U1, U2)))
    return [(stem, ff(min(U1, U2)), [ff(max(U1, U2)), "12.5", "25"], why)]

def q44():
    # X ~ N3(mu, S), condition (x2, x3) on x1 = a
    mu = [1, 0, 2]; S = [[2, 1, 1], [1, 3, 1], [1, 1, 2]]; a = 3
    cm = [F(mu[1]) + F(S[1][0], S[0][0]) * (a - mu[0]), F(mu[2]) + F(S[2][0], S[0][0]) * (a - mu[0])]
    cv = [[F(S[i][j]) - F(S[i][0] * S[0][j], S[0][0]) for j in (1, 2)] for i in (1, 2)]
    fmt = lambda m, V: "(%s)′ and %s" % (", ".join(ff(x) for x in m), "[" + ", ".join("[" + ", ".join(ff(x) for x in r) + "]" for r in V) + "]")
    corr = fmt(cm, cv)
    dis = [fmt([mu[1], mu[2]], [[S[1][1], S[1][2]], [S[2][1], S[2][2]]]), fmt(cm, [[S[1][1], S[1][2]], [S[2][1], S[2][2]]]), fmt([F(mu[1]) + 2 * cm[0] - 2 * F(mu[1]), F(mu[2]) + 2 * cm[1] - 2 * F(mu[2])], cv)]
    stem = ("X = (x₁, x₂, x₃)′ ~ N₃(μ, Σ) with μ = (1, 0, 2)′ and Σ = [[2, 1, 1], [1, 3, 1], [1, 1, 2]]. The conditional mean and covariance matrix of (x₂, x₃)′ given x₁ = 3 are")
    why = ("For a partitioned normal vector, E(X⁽²⁾ | x₁) = μ⁽²⁾ + Σ₂₁Σ₁₁⁻¹(x₁ − μ₁) and Cov(X⁽²⁾ | x₁) = Σ₂₂ − Σ₂₁Σ₁₁⁻¹Σ₁₂. With Σ₁₁ = 2, Σ₂₁ = (1, 1)′ and x₁ − μ₁ = 2 this gives %s. "
           "Trap: the conditional covariance does not depend on the observed x₁, and it is smaller than Σ₂₂.") % corr
    return [(stem, corr, dis, why)]

def q45():
    stem = "X is exponential with mean 1/λ, and given X = x, Y is Poisson with mean 2x. Then Var(Y) equals"
    why = ("By the law of total variance, Var(Y) = E[Var(Y | X)] + Var[E(Y | X)] = E(2X) + Var(2X) = 2/λ + 4/λ² = (2λ + 4)/λ². "
           "Trap: dropping the Var(2X) term leaves only 2/λ, the mean of Y.")
    return [(stem, "(2λ + 4)/λ²", ["2/λ", "(λ + 2)/λ²", "4/λ²"], why)]

RS48 = [  # (vector, the four commands, their outputs as printed by R 4.5.1)
 ("c(5, −2, 8, −7, 0)", ["min(x)", "max(x)", "range(x)", "which(x < 0)"], ["[1] −7", "[1] 8", "[1] −7  8", "[1] 2 4"]),
 ("c(3, 10, −1, 6)", ["min(x)", "max(x)", "range(x)", "which(x > 5)"], ["[1] −1", "[1] 10", "[1] −1 10", "[1] 2 4"]),
 ("c(−4, 7, 0, 2)", ["min(x)", "max(x)", "range(x)", "which(x == 0)"], ["[1] −4", "[1] 7", "[1] −4  7", "[1] 3"])]
def q48():
    out = []
    for n, (vec, cmds, outs) in enumerate(RS48):
        perm = [(i * 3 + n + 1) % 4 for i in range(4)]; listII = [None] * 4
        for i, p in enumerate(perm): listII[p] = outs[i]
        rom = ["I", "II", "III", "IV"]; corr = ", ".join("%s-%s" % ("ABCD"[i], rom[perm[i]]) for i in range(4))
        alt = lambda q: ", ".join("%s-%s" % ("ABCD"[i], rom[q[i]]) for i in range(4))
        dis = [alt([perm[1], perm[0], perm[2], perm[3]]), alt([perm[0], perm[1], perm[3], perm[2]]), alt([perm[2], perm[1], perm[0], perm[3]])]
        stem = ("With x <- %s, match LIST-I with LIST-II. LIST-I: %s. LIST-II: %s. Choose the correct answer from the options given below:") % (
            vec, "; ".join("%s. > %s" % ("ABCD"[i], c) for i, c in enumerate(cmds)), "; ".join("%s. %s" % (rom[j], listII[j]) for j in range(4)))
        why = ("min and max return single values, range returns both extremes as a pair, and which returns the positions (indices) where its logical condition is TRUE, not the values: "
               "%s. So the matching is %s. Trap: which() gives indices; and it needs a logical argument such as x < 0. (Outputs confirmed in R 4.5.1.)") % (
               "; ".join("%s gives %s" % (c, o) for c, o in zip(cmds, outs)), corr)
        out.append((stem, corr, dis, why))
    return out

GEN = {1: q1, 2: q2, 5: q5, 11: q11, 14: q14, 20: q20, 22: q22, 23: q23, 25: q25, 27: q27, 29: q29, 30: q30, 34: q34, 38: q38, 41: q41, 42: q42, 44: q44, 45: q45, 48: q48}

def build():
    banks, bad = {}, []
    for qi, q in enumerate(sorted(NEED)):
        vs = GEN[q](); assert len(vs) == NEED[q], (q, len(vs), NEED[q])
        for n, (stem, corr, dis, why) in enumerate(vs, 1):
            pos = (qi + n - 1) % 4; opts = dis[:pos] + [corr] + dis[pos:]
            if len(dis) != 3 or len(set(opts)) != 4: bad.append((q, n, opts)); continue
            banks.setdefault(MODULE[q], []).append({"id": "j26v-g%02d-%02d" % (q, n), "format": "single", "topic": "June 2026 paper · Q%d (gap-fill variant)" % q,
                                                    "srcQ": q, "stem": stem, "options": opts, "answer": "ABCD"[pos], "explanation": why})
    return banks, bad

if __name__ == "__main__":
    banks, bad = build()
    if bad:
        for b in bad: print("NOT DISTINCT", b)
        raise SystemExit(1)
    for mod, items in sorted(banks.items()):
        doc = {"moduleId": mod, "topicId": None, "source": "variant", "label": "June 2026 paper — gap-fill practice variants (booklet Q1–Q50)", "count": len(items), "items": items}
        p = R / "seed" / ("%s_j26fill_pyq_variants.json" % mod)
        p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(len(items), p.name)
