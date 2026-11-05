#!/usr/bin/env python3
# Repair the 21 real-paper questions whose options did not survive text extraction.
# Stems and options are transcribed from the rendered pages of the official PDF
# (pdftoppm at 130 dpi, read page by page); every key is re-derived here rather
# than trusted, and the derivation is appended to the explanation.
import json, io

R = {}

def Q(n, stem, opts, key, why=None):
    R[n] = dict(stem=stem, options=opts, key=key, why=why)

Q(3, "For estimating the AR(2) process yt = Φ₁·yt−1 + Φ₂·yt−2 + εt the Yule–Walker equations are used. "
     "If the sample autocorrelations are r₁ = 0.8 and r₂ = 0.5, then the estimate of Φ₂ is:",
  ["−7/18", "16/18", "7/18", "−16/18"], "A",
  "Yule–Walker: r₁ = φ₁ + φ₂r₁ and r₂ = φ₁r₁ + φ₂, so φ₂ = (r₂ − r₁²)/(1 − r₁²) = (0.5 − 0.64)/(1 − 0.64) = −0.14/0.36 = −7/18.")

Q(4, "For testing H₀: μ = (3.5, 2.5)′ based on the three observation vectors X₁ = (1, 2)′, X₂ = (4, 4)′ and "
     "X₃ = (4, 3)′ from N₂(μ, Σ), the value of Hotelling's T² statistic is approximately:",
  ["2.33", "3.5", "7.0", "7.5"], "C",
  "x̄ = (3, 3)′ so d = x̄ − μ₀ = (−0.5, 0.5)′. With divisor n − 1 = 2, S = [[3, 1.5], [1.5, 1]] and |S| = 0.75, "
  "so S⁻¹ = [[4/3, −2], [−2, 4]]. T² = n·d′S⁻¹d = 3 × 2.333 = 7.0.")

Q(10, "Let X₁, X₂, …, Xₙ be a random sample from an N(μ, σ²) population. Then the (1 − α) upper confidence "
      "bound for μ is given by:",
  ["(−∞, X̄ + t(n−1, α)·S/√n)", "(−∞, X̄ − t(n−1, α)·S/√n)",
   "(−∞, X̄ + t(n, α)·S/√n)", "(−∞, X̄ − t(n, α)·S/√n)"], "A",
  "An upper bound keeps the whole lower tail, so the interval runs from −∞ upward and the half-width is added. "
  "S estimates σ, so the multiplier is t with n − 1 degrees of freedom, not n.")

Q(11, "Let y₁ = β₁ + β₂ + u₁; y₂ = 2β₁ + u₂; y₃ = β₁ − β₂ + u₃ with V(uᵢ) = σ², i = 1, 2, 3. "
      "Then the best linear unbiased estimators of β₁ and β₂ are respectively:",
  ["(y₁ + 2y₂ + y₃)/2, (y₁ − y₃)/6",
   "(1/6)(y₁ + 2y₂ + y₃), (1/2)(y₁ − y₃)",
   "(y₁ + 2y₂ + y₃)/2, (y₁ + y₃)/6",
   "6(y₁ + y₂ + y₃), 2(y₁ − y₃)"], "B",
  "With X = [[1, 1], [2, 0], [1, −1]], X′X = [[6, 0], [0, 2]] and X′y = (y₁ + 2y₂ + y₃, y₁ − y₃)′. "
  "So β̂₁ = (y₁ + 2y₂ + y₃)/6 and β̂₂ = (y₁ − y₃)/2 — the divisors are 6 and 2, not 2 and 6.")

Q(13, "In samples of size 5 from a U[0, 1] population, the mean of the distribution of the median is:",
  ["1/2", "1/3", "1/4", "1"], "A",
  "The median is the 3rd order statistic of 5, which is Beta(3, 3); its mean is 3/(3 + 3) = 1/2. "
  "Symmetry alone gives the same answer.")

Q(14, "Let X₁, X₂, …, Xₙ be a random sample from the exponential distribution with pdf f(x; θ) = θe^(−θx), "
      "x > 0, θ > 0. For testing H₀: θ = θ₀ against H₁: θ ≠ θ₀, the UMP critical region of size α — where "
      "χ²(α, n) denotes the upper α point of the χ² distribution — is given by:",
  ["Σxᵢ ≤ (1/(2θ₀))·χ²(1−α, 2n)",
   "Σxᵢ ≥ (1/(2θ₀))·χ²(α, 2n)",
   "(1/(2θ₀))·χ²(α, 2n) ≤ Σxᵢ ≤ (1/(2θ₀))·χ²(1−α, 2n)",
   "No UMP test exists"], "D",
  "The alternative is two-sided. The most powerful region against θ < θ₀ is an upper tail of Σxᵢ and against "
  "θ > θ₀ a lower tail, so no single region is most powerful against both — MLR gives a UMP test only for a "
  "one-sided alternative.")

Q(19, "Let X ~ N₃(μ, Σ) where μ′ = [1 0 −1] and Σ = [[1, −1, 0], [−1, 2, 0], [0, 0, 3]]. Which of the following "
      "are independent? A. X₁ and X₂; B. (X₁, X₂) and X₃; C. X₂ and (X₂ + 2X₁); D. (X₂ + X₃)/2 and (X₁ + X₂)/2",
  ["A, B only", "A, D only", "B, C only", "B, D only"], "C",
  "Under normality zero covariance is independence. A: Cov = −1 ≠ 0. B: both covariances with X₃ are 0 ✓. "
  "C: Cov(X₂, X₂ + 2X₁) = 2 + 2(−1) = 0 ✓. D: Cov = (−1 + 2 + 0 + 0)/4 = 0.25 ≠ 0.")

Q(21, "Let u and v be two n × 1 vectors with u′v ≠ 0. Let P = Iₙ − (1/u′v)·uv′ and Q = uv′. Then PQ is equal to:",
  ["0", "uv′", "1 − u′v", "The product of P and Q is not possible"], "A",
  "PQ = uv′ − u(v′u)v′/(u′v) = uv′ − uv′ = 0, because v′u is the scalar u′v and cancels.")

Q(22, "Given the R program\n  f = function (n) { x = 1; for (i in 1:n) { x = x * i }; x }\n  f(5)\n"
      "which of the following is the output?",
  ["1", "5", "20", "120"], "D",
  "The loop multiplies x by every i from 1 to 5, so f(5) = 5! = 120.")

Q(24, "Let X ~ N₃(0, Σ) where Σ = [[4, 1, 1], [1, 2, α], [1, α, 2]]. The value of α for which r₂₃.₁ = 5/7 is:",
  ["1", "3/2", "2/3", "1/2"], "B",
  "r₂₃.₁ = (σ₂₃ − σ₁₂σ₁₃/σ₁₁)/√((σ₂₂ − σ₁₂²/σ₁₁)(σ₃₃ − σ₁₃²/σ₁₁)) = (α − 1/4)/1.75. "
  "Setting it to 5/7 = 0.714 gives α = 0.25 + 1.25 = 3/2.")

Q(25, "Let X and Y be independent random variables each following the exponential distribution with parameter λ. "
      "Then the conditional distribution of X given X + Y = 2 should be:",
  ["Exponential(2)", "β₁(λ/2, λ/2)", "Uniform(0, 2)", "Gamma(2, λ)"], "C",
  "The joint density of (X, X+Y) is flat in x on (0, 2) once the sum is fixed — the λ cancels — so X | X+Y = 2 "
  "is uniform on (0, 2). This is the Poisson-process fact that one event in a fixed interval lands uniformly.")

Q(26, "The rank of the matrix [[2, 6, 4, 2], [3, 7, 4, 2], [4, 8, 4, 2], [5, 9, 4, 2]] is:",
  ["1", "2", "3", "4"], "B",
  "Column 4 is half of column 3, and column 2 = column 1 + column 3. Only two columns are independent, so the rank is 2.")

Q(28, "The interval of convergence of the power series Σ(n = 0 to ∞) |x − 5|ⁿ / ((n + 1)(n + 2)) is:",
  ["(−5, 5)", "(0, 1)", "(4, 6)", "∞"], "C",
  "The ratio test gives convergence for |x − 5| < 1, i.e. 4 < x < 6; the (n+1)(n+2) denominator makes the "
  "endpoints converge too, but among the options only (4, 6) describes the interval.")

Q(31, "Let X be a non-negative random variable with distribution function F(x). Read the statements: "
      "A. ∫₀^∞ 2x[1 − F(x)]dx = E(X²); B. ∫₀^∞ [1 − F(x)]dx = E(X); C. E(1/X) ≤ 1/E(X); D. E(log X) ≤ log E(X)",
  ["A, B and C", "B, C and D", "A, B and D", "C and D"], "C",
  "A and B are the standard survival-function identities for the first two moments. D is Jensen's inequality for "
  "the concave log. C reverses Jensen for the convex 1/x — the true statement is E(1/X) ≥ 1/E(X).")

Q(34, "Let A₁, A₂, …, Aₙ be n independent events such that P(Aᵢ) = 1 − 1/2^i, i = 1, 2, …, n. Then the "
      "probability that at least one of the events A₁, A₂, …, Aₙ occurs is:",
  ["1/2ⁿ", "1 − 1/2ⁿ", "1/2^(n(n+1)/2)", "1 − 1/2^(n(n+1)/2)"], "D",
  "P(none occurs) = ∏(1/2^i) = 1/2^(1+2+…+n) = 1/2^(n(n+1)/2), so P(at least one) is one minus that.")

Q(37, "The maximum likelihood estimates of μ and Σ based on the observations X₁ = (1, 2)′, X₂ = (4, 4)′ and "
      "X₃ = (4, 3)′ from N₂(μ, Σ) are respectively:",
  ["(3, 3)′ and [[2/3, 1], [1, 2]]",
   "(3, 3)′ and [[2/3, 3], [3, 6]]",
   "(3, 3)′ and [[6, 3], [3, 2]]",
   "(3, 3)′ and [[2, 1], [1, 2/3]]"], "D",
  "μ̂ = x̄ = (3, 3)′. The MLE of Σ divides by n, not n − 1: deviations (−2,−1), (1,1), (1,0) give "
  "Σ̂ = [[6/3, 3/3], [3/3, 2/3]] = [[2, 1], [1, 2/3]].")

Q(41, "Let X₍₁₎ ≤ X₍₂₎ ≤ … ≤ X₍ᵣ₎ be the first r observed order statistics of a random sample of size n from the "
      "exponential distribution with mean θ. Consider T₁ = (1/r)·Σ(i = 1 to r) X₍ᵢ₎ and T₂ = X₍ᵣ₎/r. "
      "Which one of the following is an unbiased estimate of θ?",
  ["T₁", "T₁ + (r − 1)T₂", "T₁ + (n − 1)T₂", "T₁ + (n − r)T₂"], "D",
  "Under Type II censoring the total time on test is ΣX₍ᵢ₎ + (n − r)X₍ᵣ₎, and dividing it by r is unbiased for θ. "
  "That is exactly T₁ + (n − r)T₂. T₁ alone understates θ because the largest lifetimes are still running.")

Q(43, "For testing a hypothesis the different steps are given below (A to E). Arrange them in proper sequence. "
      "A. Checking the assumptions of the test. B. Calculation of the test statistic. C. Formation of hypothesis. "
      "D. Comparing with the tabulated values. E. Drawing the inference.",
  ["A, C, B, D, E", "C, A, D, B, E", "A, C, D, B, E", "C, A, B, D, E"], "D",
  "The hypothesis comes first — it decides which test is even a candidate — then its assumptions are checked, "
  "then the statistic is computed, compared with the tabulated value, and only then is the inference drawn.")

Q(44, "Let X = (x₁, x₂, x₃)′ ~ N₃(μ, Σ) where μ = (2, −2, 1)′ and Σ = [[1, 1, 1], [1, 3, 2], [1, 2, 2]]. "
      "Write X = (x₁, X⁽²⁾)′ where X⁽²⁾ = (x₂, x₃)′. Then the conditional mean and conditional variance of "
      "X⁽²⁾ given x₁ = 1 are respectively:",
  ["(−2, 1)′ and [[3, 2], [2, 2]]",
   "(−3, 0)′ and [[2, 1], [1, 1]]",
   "(1, −2)′ and [[2, 2], [2, 3]]",
   "(0, −3)′ and [[1, 1], [1, 2]]"], "B",
  "Mean = μ₂ + Σ₂₁Σ₁₁⁻¹(x₁ − μ₁) = (−2, 1)′ + (1, 1)′(1)(1 − 2) = (−3, 0)′. "
  "Variance = Σ₂₂ − Σ₂₁Σ₁₁⁻¹Σ₁₂ = [[3, 2], [2, 2]] − [[1, 1], [1, 1]] = [[2, 1], [1, 1]].")

Q(45, "Let X follow the exponential distribution with mean 1/λ and let Y given X = x follow the Poisson "
      "distribution with parameter x. Then Var(Y) equals:",
  ["λ(λ + 1)/λ²", "λ²/(λ + 1)", "λ(λ + 1)", "(λ + 1)/λ²"], "D",
  "Var(Y) = E[Var(Y|X)] + Var(E[Y|X]) = E[X] + Var(X) = 1/λ + 1/λ² = (λ + 1)/λ². "
  "Both terms are needed — using only E[X] gives 1/λ, which is not an option.")

Q(49, "Let p be the probability that a coin falls heads in a single toss. To test H₀: p = 1/2 against "
      "H₁: p = 3/4 the coin is tossed 5 times and H₀ is rejected if more than 3 heads are obtained. "
      "The size and power of the test are respectively:",
  ["(3/16, 47/128)", "(3/16, 81/128)", "(9/16, 18/128)", "(9/16, 47/128)"], "B",
  "Size = P(X ≥ 4 | p = 1/2) = (5 + 1)/32 = 6/32 = 3/16. "
  "Power = P(X ≥ 4 | p = 3/4) = 5(3/4)⁴(1/4) + (3/4)⁵ = (405 + 243)/1024 = 648/1024 = 81/128.")

P = "seed/pyq_j26_full.json"
d = json.load(io.open(P, encoding="utf-8"))
fixed, keychanged, left = 0, [], []
for q in d["items"]:
    n = q["pno"]
    if n in R:
        r = R[n]
        q["stem"] = r["stem"]
        q["options"] = r["options"]
        if q["answer"] != r["key"]:
            keychanged.append((n, q["answer"], r["key"]))
        q["answer"] = r["key"]
        base = q.get("explanation", "")
        # keep the response-sheet note, add the derivation that was verified here
        if r["why"] and r["why"] not in base:
            q["explanation"] = (r["why"] + " " + base).strip()
        q.pop("needsReview", None)
        q.pop("reviewNote", None)
        q["repaired"] = "options transcribed from the rendered official PDF; key re-derived"
        fixed += 1
    elif q.get("needsReview"):
        left.append(n)
d["count"] = len(d["items"])
d["clean"] = len([x for x in d["items"] if not x.get("needsReview")])
json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("repaired %d items; still flagged: %s" % (fixed, left or "none"))
print("keys that disagreed with the position-mapped answer:", keychanged or "none")
print("items now clean: %d of %d" % (d["clean"], d["count"]))
