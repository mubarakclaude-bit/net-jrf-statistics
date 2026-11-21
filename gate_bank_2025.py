# -*- coding: utf-8 -*-
"""Build the GATE 2025 Statistics (ST) question banks, one per module.

    python gate_bank_2025.py            write seed/<module>_gate25.json
    python gate_bank_2025.py --check    exit 1 if the files on disk differ from what would be written

Source: the GATE 2025 Statistics (ST) question paper (IIT Roorkee), the owner's copy, taken through `tools/intake.js`
(docs/SOURCE_INTAKE.md): every page read as an image, every question accounted for. The paper prints no answer key, so
every answer here is computed, and verify_gate_2025.py recomputes each one
and then confirms it against the official GATE 2025 ST answer key. Q1-Q10 are General Aptitude (verbal and
numerical reasoning, not on the Paper 2 syllabus) and are left out; Q11-Q65 are all kept: 25 single-answer (MCQ),
8 multiple-correct (MSQ) and 22 numerical-answer (NAT) questions. Stems follow the paper; explanations are written fresh.

After the first merge the JSON files are the source of truth (docs/CONTENT_GUIDE.md, 3c); this script then records how
they were made. Pass --force to overwrite them anyway."""
import io, json, os, sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from pyq_bank_common import S, M, N  # noqa: E402

LABEL = "GATE 2025 Statistics (ST) questions"
YEAR = "GATE-2025"
LEFT_OUT = ["Q%d" % k for k in range(1, 11)]   # General Aptitude
MODULE_ORDER = ["maths", "probability", "inference", "stochastic", "multivariate", "nonparam", "regression"]


def R(q):
    return "GATE 2025 ST Q%d" % q


ITEMS = [
    # ------------------------------------------------------------------ Q11-Q35, one mark
    S("gate25-q11", "maths", "maths-t5", R(11),
      "Let f: [0, ∞) → [0, ∞) be a differentiable function with f(x) > 0 for all x > 0, and f(0) = 0. Further, f satisfies "
      "(f(x))² = ∫₀ˣ ((f(t))² + f(t)) dt, x > 0. Then which one of the following options is correct?",
      ["0 < f(2) ≤ 1", "1 < f(2) ≤ 2", "2 < f(2) ≤ 3", "3 < f(2) ≤ 4"], "B",
      "Differentiate both sides (fundamental theorem of calculus): 2f(x)f′(x) = f(x)² + f(x). For x > 0, f(x) > 0, so divide "
      "by f: f′ = (f + 1)/2. Then d/dx ln(f + 1) = 1/2, so ln(f + 1) = x/2 + c, and f(0) = 0 gives c = 0. Hence "
      "f(x) = e^(x/2) − 1 and f(2) = e − 1 ≈ 1.718, which lies in (1, 2].", year=YEAR),
    S("gate25-q12", "maths", "maths-t4", R(12),
      "Among the following four statements about countability and uncountability of different sets, which is the correct "
      "statement?",
      ["The set ⋃ₙ₌₀^∞ {x ∈ ℝ : x = Σᵢ₌₀ⁿ 10ⁱ aᵢ, where aᵢ ∈ {1, 2} for i = 0, 1, 2, …, n} is uncountable",
       "The set {x ∈ (0, 1) : x = Σₙ₌₁^∞ aₙ/10ⁿ, where aₙ = 1 or 2 for each n ∈ ℕ} is uncountable",
       "There exists an uncountable set whose elements are pairwise disjoint open intervals in ℝ",
       "The set of all intervals with rational end points is uncountable"], "B",
      "The first set is a countable union of finite sets (each n gives 2ⁿ⁺¹ integers), so it is countable. The second set is "
      "every infinite sequence of digits from {1, 2}; distinct sequences give distinct numbers, and such sequences are as "
      "many as the binary sequences, so it is uncountable. Disjoint open intervals each contain a different rational, so "
      "there are at most countably many. Intervals with rational end points are indexed by pairs of rationals, a countable "
      "set.", year=YEAR, diff="easy"),
    S("gate25-q13", "maths", "maths-t13", R(13),
      "Let S = {(x, y, z) ∈ ℝ³ \\ {(0, 0, 0)} : z = −(x + y)}. Denote S⊥ = {(p, q, r) ∈ ℝ³ : px + qy + rz = 0 for all "
      "(x, y, z) ∈ S}. Then which one of the following options is correct?",
      ["S⊥ is not a subspace of ℝ³", "S⊥ = {(0, 0, 0)}", "dim(S⊥) = 1", "dim(S⊥) = 2"], "C",
      "S is the plane x + y + z = 0 with the origin removed; it still spans that plane, which has dimension 2. The vectors "
      "orthogonal to the plane form its normal line, spanned by (1, 1, 1). So S⊥ is a subspace of dimension 3 − 2 = 1.",
      year=YEAR, diff="easy"),
    S("gate25-q14", "probability", "probability-t4", R(14),
      "Let X be a random variable having the Poisson distribution with mean logₑ 2. Then E(e^((logₑ 3)X)) equals",
      ["1", "2", "3", "4"], "D",
      "This is the moment generating function at t = ln 3. For Poisson(λ), E(e^(tX)) = exp(λ(eᵗ − 1)). With λ = ln 2 and "
      "eᵗ = 3: exp(ln 2 × 2) = 2² = 4.", year=YEAR, diff="easy"),
    S("gate25-q15", "probability", "probability-t2", R(15),
      "Let (X₁, X₂, X₃) follow the multinomial distribution with the number of trials being 100 and the probability vector "
      "(3/10, 1/10, 3/5). Then E(X₂ | X₃ = 40) equals",
      ["25", "15", "30", "45"], "B",
      "Given X₃ = 40, the other 60 trials fall in category 1 or 2 with probabilities in the ratio 3/10 : 1/10, so "
      "X₂ | X₃ = 40 is Binomial(60, (1/10)/(4/10)) = Binomial(60, 1/4). Its mean is 60/4 = 15.", year=YEAR, diff="easy"),
    S("gate25-q16", "probability", "probability-t9", R(16),
      "Let {Xₙ}ₙ≥₁ be a sequence of i.i.d. random variables with the common probability density function "
      "f(x) = 1/(π(1 + x²)), −∞ < x < ∞. Define Yₙ = 1/2 + (1/π) tan⁻¹(Xₙ) for n = 1, 2, …. Then which one of the "
      "following options is correct?",
      ["(1/n) Σᵢ₌₁ⁿ Yᵢ → 1/2 in probability as n → ∞", "(1/n) Σᵢ₌₁ⁿ Yᵢ → 0 in probability as n → ∞",
       "(1/n) Σᵢ₌₁ⁿ Xᵢ → 0 in probability as n → ∞", "(1/n) Σᵢ₌₁ⁿ Xᵢ → 1/2 in probability as n → ∞"], "A",
      "Yₙ is the Cauchy distribution function evaluated at Xₙ, so each Yₙ is Uniform(0, 1), with mean 1/2. The Yᵢ are i.i.d. "
      "with finite mean, so the weak law gives (1/n)ΣYᵢ → 1/2. The Cauchy Xᵢ have no mean: (1/n)ΣXᵢ is again standard "
      "Cauchy for every n, so it converges in probability to no constant.", year=YEAR),
    S("gate25-q17", "stochastic", "stochastic-t5", R(17),
      "Let {N(t) : t ≥ 0} be a homogenous Poisson process with the intensity/rate λ = 2. Let X = N(6) − N(1), "
      "Y = N(5) − N(3), W = N(6) − N(5), Z = N(3) − N(1). Then which one of the following options is correct?",
      ["Cov(W, Z) = 2", "Y + Z ~ Poisson(10)", "Pr(Y = Z) = 1", "Cov(X, Y) = 4"], "D",
      "Counts on disjoint intervals are independent, and a count on an interval of length L is Poisson(2L). W and Z cover "
      "(5, 6] and (1, 3], disjoint, so Cov(W, Z) = 0. Y + Z = N(5) − N(1) is Poisson(2 × 4) = Poisson(8). Y and Z are "
      "independent Poisson(4) variables, not equal. X = Z + Y + W, so Cov(X, Y) = Var(Y) = 4.", year=YEAR),
    S("gate25-q18", "inference", "inference-t2", R(18),
      "Let T be a complete and sufficient statistic for a family 𝒫 of distributions and let U be a sufficient statistic for "
      "𝒫. If P_f(T ≥ 0) = 1 for all f ∈ 𝒫, then which one of the following options is NOT necessarily correct?",
      ["T² is a complete statistic for 𝒫", "T² is a minimal sufficient statistic for 𝒫", "T is a function of U",
       "U is a function of T"], "D",
      "A complete sufficient statistic is minimal sufficient, and a minimal sufficient statistic is a function of every "
      "sufficient statistic, so T is a function of U. Because T ≥ 0, T² is a one-to-one function of T, so T² is also "
      "complete and minimal sufficient. But a sufficient U can carry more than T (the whole sample, for instance), so U "
      "need not be a function of T.", year=YEAR),
    S("gate25-q19", "inference", "inference-t10", R(19),
      "Let X₁, X₂ be a random sample from N(θ, 1) distribution, where θ ∈ ℝ. Consider testing H₀: θ = 0 against H₁: θ ≠ 0. "
      "Let φ(X₁, X₂) be the likelihood ratio test of size 0.05 for testing H₀ against H₁. Then which one of the following "
      "options is correct?",
      ["φ(X₁, X₂) is a uniformly most powerful test of size 0.05", "E_θ(φ(X₁, X₂)) ≥ 0.05 ∀ θ ∈ ℝ",
       "There exists a uniformly most powerful test of size 0.05", "E_θ=0(X₁ φ(X₁, X₂)) = 0.05"], "B",
      "The likelihood ratio test rejects when √2·|X̄| > 1.96. Its power 1 − Φ(1.96 − √2θ) + Φ(−1.96 − √2θ) is smallest at "
      "θ = 0, where it equals 0.05, so the test is unbiased: power ≥ 0.05 everywhere. For a two-sided alternative no UMP test "
      "exists, because the one-sided most powerful tests differ for θ > 0 and θ < 0. Under θ = 0 the test is unchanged by "
      "(X₁, X₂) → (−X₁, −X₂), so E(X₁φ) = 0, not 0.05.", year=YEAR),
    S("gate25-q20", "inference", "inference-t9", R(20),
      "Let a random variable X follow a distribution with density f ∈ {f₀, f₁}, where f₀(x) = 1 if 0 ≤ x ≤ 1 and 0 "
      "otherwise, and f₁(x) = 1 if 1 ≤ x ≤ 2 and 0 otherwise. Let φ be a most powerful test of level 0.05 for testing "
      "H₀: f = f₀ against H₁: f = f₁ based on X. Then which one of the following options is necessarily correct?",
      ["E_f₀(φ(X)) = 0.05", "E_f₁(φ(X)) = 1", "P_f(φ(X) = 1) = P_f(X > 1), ∀ f ∈ {f₀, f₁}", "P_f₁(φ(X) = 1) < 1"], "B",
      "The two supports overlap only at the single point 1. The test that rejects when X > 1 has size 0 and power 1, so "
      "every most powerful test of level 0.05 must have power 1. It need not use its whole level: it may also reject on any "
      "part of [0, 1] of probability up to 0.05, or on none of it, so its size can be anything in [0, 0.05] and "
      "P_f₀(φ = 1) need not equal P_f₀(X > 1) = 0.", year=YEAR),
    S("gate25-q21", "inference", "inference-t9", R(21),
      "Let X be a random variable having probability density function f ∈ {f₀, f₁}. Let φ be a most powerful test of level "
      "0.05 for testing H₀: f = f₀ against H₁: f = f₁ based on X. Then which one of the following options is NOT necessarily "
      "correct?",
      ["φ is the unique most powerful test of level 0.05", "E_f₁(φ(X)) ≥ 0.05", "E_f₀(φ(X)) ≤ 0.05",
       "For some constant c ≥ 0, P_f(f₁(X) > cf₀(X)) ≤ P_f(φ(X) = 1), ∀ f ∈ {f₀, f₁}"], "A",
      "Level 0.05 means E_f₀(φ) ≤ 0.05. A most powerful test is at least as powerful as the trivial test φ ≡ 0.05, so its "
      "power is at least 0.05. By the necessity part of the Neyman–Pearson lemma, a most powerful test rejects (almost surely) "
      "wherever f₁ > cf₀ for some c, which gives the last inequality. Uniqueness can fail: on the set where f₁ = cf₀ the test "
      "may randomise in many ways, or where both densities vanish it may do anything.", year=YEAR),
    S("gate25-q22", "nonparam", "nonparam-t7", R(22),
      "Let {Xₙ}ₙ≥₁ be a sequence of i.i.d. random variables with common distribution function F, and let Fₙ be the "
      "empirical distribution function based on {X₁, X₂, …, Xₙ}. Then, for each fixed x ∈ (−∞, ∞), which one of the "
      "following options is correct?",
      ["√n(Fₙ(x) − F(x)) → 0 in probability as n → ∞",
       "n(Fₙ(x) − F(x)) / √(F(x)(1 − F(x))) → Z in distribution as n → ∞, where Z ~ N(0, 1)",
       "Fₙ(x) → F(x) almost surely as n → ∞", "lim n Var(Fₙ(x)) = 0 as n → ∞"], "C",
      "nFₙ(x) counts the Xᵢ ≤ x, a Binomial(n, F(x)) variable. So Fₙ(x) is an average of i.i.d. indicators with mean F(x), "
      "and the strong law gives Fₙ(x) → F(x) almost surely. The CLT scaling is √n, not n: √n(Fₙ(x) − F(x)) tends to "
      "N(0, F(x)(1 − F(x))), not to 0, and n Var(Fₙ(x)) = F(x)(1 − F(x)) for every n.", year=YEAR, diff="easy"),
    S("gate25-q23", "multivariate", "multivariate-t1", R(23),
      "Let (X, Y)ᵀ follow a bivariate normal distribution with E(X) = 3, E(Y) = 4, Var(X) = 25, Var(Y) = 100, and "
      "Cov(X, Y) = 50ρ, where ρ ∈ (−1, 1). If E(Y | X = 5) = 4.32, then ρ equals",
      ["0.08", "0.8", "0.32", "0.5"], "A",
      "E(Y | X = x) = E(Y) + [Cov(X, Y)/Var(X)](x − E(X)) = 4 + (50ρ/25)(5 − 3) = 4 + 4ρ. Setting 4 + 4ρ = 4.32 gives "
      "ρ = 0.08. (Here ρ is also the correlation, since 50ρ/√(25 × 100) = ρ.)", year=YEAR, diff="easy"),
    S("gate25-q24", "regression", "regression-t2", R(24),
      "For a given data (xᵢ, yᵢ), i = 1, 2, …, n, with Σxᵢ² > 0, let β̂ minimise Σ(yᵢ − βxᵢ)² over β ∈ ℝ. Further, let "
      "vⱼ = yⱼ − xⱼ and uⱼ = 2xⱼ, for j = 1, 2, …, n, and let γ̂ minimise Σ(vᵢ − γuᵢ)² over γ ∈ ℝ. If β̂ = 10, then the "
      "value of γ̂ is",
      ["4.5", "5", "10", "9"], "A",
      "Least squares through the origin gives β̂ = Σxy/Σx² = 10. Likewise γ̂ = Σuv/Σu² = Σ2x(y − x)/Σ4x² = "
      "(2Σxy − 2Σx²)/(4Σx²) = (β̂ − 1)/2 = 9/2 = 4.5.", year=YEAR),
    N("gate25-q25", "maths", "maths-t12", R(25),
      "Let I = π² ∫₀¹ ∫₀¹ y² cos π(1 + xy) dx dy. The value of I is equal to ________ (answer in integer).", "-1",
      "cos(π + πxy) = −cos(πxy). Integrate in x first: ∫₀¹ cos(πxy) dx = sin(πy)/(πy). So I = −π² ∫₀¹ y² sin(πy)/(πy) dy "
      "= −π ∫₀¹ y sin(πy) dy. By parts, ∫₀¹ y sin(πy) dy = [−y cos(πy)/π]₀¹ + ∫₀¹ cos(πy)/π dy = 1/π + 0. Hence "
      "I = −π × (1/π) = −1.",
      "The integrand y² cos π(1 + xy) is negative wherever xy < 1/2, so a negative answer is expected.", year=YEAR),
    N("gate25-q26", "maths", "maths-t2", R(26),
      "Let P = [[1, 2], [−1, 4]] and Q = P³ − 2P² − 4P + 13I₂, where I₂ denotes the identity matrix of order 2. Then the "
      "determinant of Q is equal to ________ (answer in integer).", "50",
      "P has trace 5 and determinant 4 + 2 = 6, so its eigenvalues are the roots of λ² − 5λ + 6: λ = 2 and 3. Q = q(P) with "
      "q(λ) = λ³ − 2λ² − 4λ + 13 has eigenvalues q(2) = 8 − 8 − 8 + 13 = 5 and q(3) = 27 − 18 − 12 + 13 = 10. "
      "det Q = 5 × 10 = 50.",
      "det Q is the product of q at the eigenvalues of P; both are positive, so det Q > 0.", year=YEAR, diff="easy"),
    N("gate25-q27", "maths", "maths-t1", R(27),
      "Let T: ℝ³ → ℝ³ be a linear map defined by T(x₁, x₂, x₃) = (3x₁ + 5x₂ + x₃, x₃, 2x₁ + 2x₃). Then the rank of T is "
      "equal to ________ (answer in integer).", "3",
      "The matrix of T has rows (3, 5, 1), (0, 0, 1), (2, 0, 2). Expanding along the second row: det = −1 × det[[3, 5], "
      "[2, 0]] = −1 × (0 − 10) = 10 ≠ 0. A non-zero determinant means full rank, 3.",
      "The rank of a 3 × 3 matrix is at most 3, and it is 3 exactly when the determinant is non-zero.", year=YEAR, diff="easy"),
    N("gate25-q28", "probability", "probability-t5", R(28),
      "Let X be a random variable with distribution function F, such that lim_{h→0⁻} F(3 + h) = 1/4 and F(3) = 3/4. Then "
      "16 Pr(X = 3) equals ________ (answer in integer).", "8",
      "The jump of a distribution function at a point is the probability of that point: Pr(X = 3) = F(3) − F(3⁻) = "
      "3/4 − 1/4 = 1/2. So 16 × 1/2 = 8.",
      "Pr(X = 3) must lie between 0 and 1, so 16 Pr(X = 3) lies between 0 and 16.", year=YEAR, diff="easy"),
    N("gate25-q29", "probability", "probability-t5", R(29),
      "Let X ~ Bin(2, 1/3). Then 18 E(X²) equals ________ (answer in integer).", "16",
      "E(X²) = Var(X) + [E(X)]² = 2 × (1/3)(2/3) + (2/3)² = 4/9 + 4/9 = 8/9. So 18 × 8/9 = 16.",
      "Directly: P(X = 1) = 4/9 and P(X = 2) = 1/9, so E(X²) = 4/9 + 4/9; the two routes agree.", year=YEAR, diff="easy"),
    N("gate25-q30", "probability", "probability-t13", R(30),
      "Let X follow a 10-dimensional multivariate normal distribution with zero mean vector and identity covariance matrix. "
      "Define Y = logₑ √(XᵀX) and let M_Y(t) denote the moment generating function of Y at t, t > −10. Then M_Y(2) equals "
      "________ (answer in integer).", "10",
      "W = XᵀX is chi-square with 10 degrees of freedom, and Y = (1/2) ln W. So M_Y(2) = E(e^(2Y)) = E(e^(ln W)) = E(W) = 10.",
      "e^(2Y) is exactly XᵀX, so the answer is the mean of a χ²₁₀ variable, its degrees of freedom.", year=YEAR, diff="easy"),
    N("gate25-q31", "stochastic", "stochastic-t5", R(31),
      "Let {W(t) : t ≥ 0} be a standard Brownian motion. Then E((W(2) + W(3))²) equals ________ (answer in integer).", "9",
      "For standard Brownian motion E(W(s)W(t)) = min(s, t). So E((W(2) + W(3))²) = E(W(2)²) + 2E(W(2)W(3)) + E(W(3)²) "
      "= 2 + 2 × 2 + 3 = 9.",
      "Write W(3) = W(2) + (W(3) − W(2)) with an independent increment: 2W(2) + increment has variance 4 × 2 + 1 = 9.",
      year=YEAR),
    N("gate25-q32", "inference", "inference-t4", R(32),
      "Let x₁ = 0, x₂ = 1, x₃ = 1, x₄ = 1 and x₅ = 0 be observed values of a random sample of size 5 from Bin(1, θ) "
      "distribution, where θ ∈ (0, 0.7]. Then the maximum likelihood estimate of θ based on the above sample is ________ "
      "(rounded off to two decimal places).", "0.60",
      "The likelihood θ³(1 − θ)² is maximised over (0, 1) at the sample proportion x̄ = 3/5 = 0.6. That value lies inside "
      "the allowed range (0, 0.7], so the restriction does not bind and the MLE is 0.60.",
      "Had x̄ exceeded 0.7, the MLE would have been the boundary value 0.7; compare x̄ with the bound first.", year=YEAR,
      diff="easy"),
    N("gate25-q33", "inference", "inference-t6", R(33),
      "Let X₁, …, X₅ be a random sample from N(θ, 6), where θ ∈ ℝ, and let c(θ) be the Cramer-Rao lower bound for the "
      "variances of unbiased estimators of θ based on the above sample. Then 15 inf_{θ∈ℝ} c(θ) equals ________ (answer in "
      "integer).", "18",
      "For N(θ, σ²) with σ² known, the Fisher information in one observation is 1/σ², so the bound for n observations is "
      "σ²/n = 6/5, the same for every θ. Hence 15 × 6/5 = 18.",
      "X̄ is unbiased with variance σ²/n = 6/5 and attains the bound, so the bound cannot be larger than Var(X̄).", year=YEAR,
      diff="easy"),
    N("gate25-q34", "nonparam", "nonparam-t4", R(34),
      "Let (1, 3), (2, 4), (7, 8) be three independent observations. Then the sample Spearman rank correlation coefficient "
      "based on the above observations is ________ (rounded off to two decimal places).", "1.00",
      "Rank each coordinate: x gives ranks 1, 2, 3 and y gives ranks 1, 2, 3. Every rank difference is 0, so "
      "ρ = 1 − 6Σd²/(n(n² − 1)) = 1 − 0 = 1.00.",
      "Spearman's ρ only sees ranks; both coordinates increase together, so the answer must be its maximum, 1.", year=YEAR,
      diff="easy"),
    N("gate25-q35", "regression", "regression-t4", R(35),
      "Consider the multi-linear regression model yᵢ = β₀ + β₁x₁ᵢ + β₂x₂ᵢ + β₃x₃ᵢ + β₄x₄ᵢ + εᵢ, i = 1, 2, …, 25, where "
      "βᵢ, i = 0, 1, 2, 3, 4, are unknown parameters, the errors εᵢ are i.i.d. random variables having N(0, σ²) distribution, "
      "where σ > 0 is unknown. Suppose that the value of the coefficient of determination R² is obtained as 5/6. Then the "
      "value of adjusted R² is ________ (rounded off to two decimal places).", "0.80",
      "Adjusted R² = 1 − (1 − R²)(n − 1)/(n − p − 1) with n = 25 observations and p = 4 regressors: "
      "1 − (1/6)(24/20) = 1 − 0.2 = 0.80.",
      "Adjusted R² is never larger than R² = 0.833 when regressors are present; 0.80 is just below it.", year=YEAR, diff="easy"),

    # ------------------------------------------------------------------ Q36-Q65, two marks
    S("gate25-q36", "maths", "maths-t5", R(36),
      "Let ℱ = {f: [a, b] → ℝ | f is continuous on [a, b] and differentiable on (a, b)}. Which one of the following options "
      "is correct?",
      ["There exists a non-constant f ∈ ℱ such that |f(x) − f(y)| ≤ |x − y|² for all x, y ∈ [a, b]",
       "If f ∈ ℱ and x₀ ∈ (a, b), then there exist distinct x₁, x₂ ∈ [a, b] such that (f(x₁) − f(x₂))/(x₁ − x₂) = f′(x₀)",
       "Let f ∈ ℱ and f′(x) ≥ 0 for all x ∈ (a, b). If f′ is zero only at two distinct points, then f is strictly increasing",
       "Let f ∈ ℱ. If f′(x₁) < c < f′(x₂) for some x₁, x₂ ∈ (a, b), then there may NOT exist an x₀ ∈ (x₁, x₂) such that "
       "f′(x₀) = c"], "C",
      "If f′ ≥ 0 and f′ vanishes only at two points, then for x < y the mean value theorem on small pieces avoiding those "
      "points shows f(y) − f(x) > 0, so f is strictly increasing. The other three fail. |f(x) − f(y)| ≤ |x − y|² forces "
      "f′ = 0 everywhere, so f is constant. For f(x) = x³ on [−1, 1] and x₀ = 0, a secant of slope f′(0) = 0 would need "
      "f(x₁) = f(x₂) with x₁ ≠ x₂, impossible for a strictly increasing function. Darboux's theorem says derivatives have the "
      "intermediate value property, so such an x₀ always exists.", year=YEAR),
    S("gate25-q37", "maths", "maths-t11", R(37),
      "Let U = {(x, y) ∈ ℝ² : x + y ≤ 2}. Define f: U → ℝ by f(x, y) = (x − 1)⁴ + (y − 2)⁴. The minimum value of f over U is",
      ["0", "1/16", "17/81", "1/8"], "D",
      "The unconstrained minimum is at (1, 2), but 1 + 2 = 3 > 2, so it is outside U and the minimum lies on the line "
      "x + y = 2. Put u = x − 1 and v = y − 2; then u + v = −1 and we minimise u⁴ + v⁴. By symmetry and convexity the minimum "
      "is at u = v = −1/2 (Lagrange: 4u³ = 4v³ gives u = v), with value 2 × (1/2)⁴ = 1/8.", year=YEAR),
    S("gate25-q38", "maths", "maths-t1", R(38),
      "Let P = (aᵢⱼ) be a 10 × 10 matrix with aᵢⱼ = −1/10 if i ≠ j and aᵢⱼ = 9/10 if i = j. Then rank(P) equals",
      ["10", "9", "1", "8"], "B",
      "P = I − (1/10)J, where J is the all-ones matrix. J has eigenvalue 10 once (eigenvector 1) and 0 nine times, so P has "
      "eigenvalue 1 − 1 = 0 once and 1 nine times. P is symmetric, so its rank is the number of non-zero eigenvalues: 9. "
      "(P is the centring matrix: P1 = 0.)", year=YEAR),
    S("gate25-q39", "probability", "probability-t6", R(39),
      "Let X be a random variable with the distribution function F(x) = 0 if x < 0, α(1 + 2x²) if 0 ≤ x < 1, and 1 if "
      "x ≥ 1, where α is a real constant. If the median of X is 1/√2, then the value of α equals",
      ["1/2", "1/3", "1/4", "1/6"], "C",
      "The median m satisfies F(m) = 1/2. At m = 1/√2: α(1 + 2 × 1/2) = 2α = 1/2, so α = 1/4. Check that F is a valid "
      "distribution function: it jumps by 1/4 at 0, rises to 3/4 just below 1, and jumps to 1 at 1.", year=YEAR, diff="easy"),
    S("gate25-q40", "probability", "probability-t6", R(40),
      "Let X be a continuous random variable with probability density function f(x) = (1/(σx√(2π))) "
      "e^(−(1/2)((logₑ x − μ)/σ)²), x > 0, where μ ∈ ℝ, σ > 0. If logₑ(E(X²)/(E(X))²) = 4, then Var(logₑ X) equals",
      ["2", "4", "16", "64"], "B",
      "X is lognormal: ln X ~ N(μ, σ²). Its moments are E(Xᵏ) = e^(kμ + k²σ²/2), so E(X²)/(E X)² = e^(2μ + 2σ²)/e^(2μ + σ²) "
      "= e^(σ²). Then ln of the ratio is σ² = 4, and Var(ln X) = σ² = 4.", year=YEAR),
    S("gate25-q41", "probability", "probability-t2", R(41),
      "Let X and Y be discrete random variables with joint probability mass function p_{X,Y}(m, n) = λⁿe^(−λ)/(2ⁿ m!(n − m)!), "
      "m = 0, …, n, and n = 0, 1, 2, …, where λ is a fixed positive real number. Then which one of the following options is "
      "correct?",
      ["The marginal distribution of X is Poisson with mean λ", "The marginal distribution of Y is Poisson with mean 2λ",
       "The conditional distribution of X given Y = 3 is Bin(3, 1/2)", "E(Y | X = 2) = λ/2"], "C",
      "Rewrite the pmf as [e^(−λ)λⁿ/n!] × [C(n, m)(1/2)ⁿ]. The first factor is the Poisson(λ) pmf of Y, the second the "
      "Binomial(n, 1/2) pmf of X given Y = n. So X | Y = 3 is Bin(3, 1/2) and Y is Poisson(λ), not Poisson(2λ). Thinning "
      "makes X Poisson(λ/2) and Y − X an independent Poisson(λ/2), so E(Y | X = 2) = 2 + λ/2.", year=YEAR),
    S("gate25-q42", "inference", "inference-t1", R(42),
      "Let X₁, …, Xₙ, n ≥ 2, be a random sample from a N(−θ, θ) distribution, where θ > 0 is an unknown parameter. Then which "
      "one of the following options is correct?",
      ["Σᵢ₌₁ⁿ Xᵢ is a minimal sufficient statistic", "Σᵢ₌₁ⁿ Xᵢ² is a minimal sufficient statistic",
       "((1/n)ΣXᵢ, (1/(n − 1))Σⱼ(Xⱼ − (1/n)ΣXᵢ)²) is a complete statistic",
       "−(1/n)ΣXᵢ is a uniformly minimum variance unbiased estimator of θ"], "B",
      "The log density is −(x + θ)²/(2θ) − (1/2) ln(2πθ) = −x²/(2θ) − x − θ/2 − (1/2) ln(2πθ). The term −x does not involve "
      "θ, so the likelihood depends on the data only through Σxᵢ², which is minimal sufficient (and complete: a one-parameter "
      "exponential family). (X̄, S²) is not complete, since E(X̄ + S²) = −θ + θ = 0 for all θ. −X̄ is unbiased but is not a "
      "function of ΣXᵢ², so it is not the UMVUE.", year=YEAR, diff="hard"),
    S("gate25-q43", "inference", "inference-t3", R(43),
      "Let X₁, X₂ be a random sample from a distribution having probability density function f_θ(x) = (1/θ)e^(−x/θ) if "
      "x > 0 and 0 otherwise, where θ ∈ (0, ∞) is an unknown parameter. For testing H₀: θ ≤ 1 against H₁: θ > 1, consider "
      "the test φ(X₁, X₂) = 1 if X₁ > 1, 0 otherwise. Then which one of the following tests has the same power function as φ?",
      ["φ₁ = (X₁ + X₂ − 1)/(X₁ + X₂) if X₁ + X₂ > 1, 0 otherwise",
       "φ₂ = (2X₁ + 2X₂ − 1)/(2(X₁ + X₂)) if X₁ + X₂ > 1, 0 otherwise",
       "φ₃ = (3X₁ + 3X₂ − 1)/(3(X₁ + X₂)) if X₁ + X₂ > 1, 0 otherwise",
       "φ₄ = (4X₁ + 4X₂ − 1)/(4(X₁ + X₂)) if X₁ + X₂ > 1, 0 otherwise"], "A",
      "Condition φ on the sufficient statistic S = X₁ + X₂ (Rao–Blackwell): given S = s, X₁ is Uniform(0, s), so "
      "E(φ | S = s) = P(X₁ > 1 | S = s) = (s − 1)/s for s > 1 and 0 otherwise. A test and its conditional expectation given S "
      "have the same expectation under every θ, hence the same power function. The other three equal 1 − 1/(ks) with k > 1, "
      "which is larger.", year=YEAR, diff="hard"),
    S("gate25-q44", "nonparam", "nonparam-t1", R(44),
      "Let X, Y₁, Y₂ be independent random variables such that X has the probability density function f(x) = 2e^(−2x) if "
      "x ≥ 0 and 0 otherwise, and Y₁ and Y₂ are identically distributed with probability density function g(x) = e^(−x) if "
      "x ≥ 0 and 0 otherwise. For i = 1, 2, let Rᵢ denote the rank of Yᵢ among X, Y₁, Y₂. Then E(R₁ + R₂) equals",
      ["13/3", "22/5", "21/5", "9/2"], "A",
      "The rank of Y₁ is 1 plus the number of the other two variables below it: R₁ = 1 + 1{X < Y₁} + 1{Y₂ < Y₁}. "
      "P(X < Y₁) for independent exponentials with rates 2 and 1 is 2/(2 + 1) = 2/3, and P(Y₂ < Y₁) = 1/2 by symmetry. So "
      "E(R₁) = 1 + 2/3 + 1/2 = 13/6, and by symmetry E(R₁ + R₂) = 13/3.", year=YEAR),
    S("gate25-q45", "multivariate", "multivariate-t5", R(45),
      "Let X₁, X₂, …, X₅ be i.i.d. random vectors following the bivariate normal distribution with zero mean vector and "
      "identity covariance matrix. Define the 5 × 2 matrix X as X = (X₁, X₂, …, X₅)ᵀ. Further, let W = (Wᵢⱼ) = XᵀX, and "
      "Z = W₁₁ + 4W₁₂ + 4W₂₂. Then Var(Z) equals",
      ["150", "200", "250", "300"], "C",
      "W is Wishart with 5 degrees of freedom and scale I. With a = (1, 2)ᵀ, aᵀWa = W₁₁ + 2·2W₁₂ + 4W₂₂ = Z. For a Wishart "
      "matrix, aᵀWa ~ (aᵀIa)χ²₅ = 5χ²₅, so Var(Z) = 25 × Var(χ²₅) = 25 × 10 = 250.", year=YEAR),
    S("gate25-q46", "regression", "regression-t3", R(46),
      "Consider the simple linear regression model yᵢ = α + βxᵢ + εᵢ, i = 1, 2, …, 24, where α ∈ ℝ and β ∈ ℝ are unknown "
      "parameters, the errors εᵢ are i.i.d. random variables having N(0, σ²) distribution, where σ > 0 is unknown. Suppose the "
      "following summary statistics are obtained from a data set of 24 observations: S_xx = 22.82, S_yy = 43.62, and "
      "S_xy = 15.48. Then, for testing H₀: β = 0 against H₁: β ≠ 0, the value of the F-test statistic based on the least "
      "squares estimator of β, whose distribution is F₁,₂₂, equals (rounded off to two decimal places)",
      ["2.54", "2.98", "3.17", "6.98"], "D",
      "Regression sum of squares SSR = S_xy²/S_xx = 15.48²/22.82 = 10.501. Error sum of squares SSE = S_yy − SSR = 33.119, "
      "on 24 − 2 = 22 degrees of freedom, so MSE = 1.5054. F = SSR/MSE = 10.501/1.5054 = 6.98.", year=YEAR),
    M("gate25-q47", "maths", "maths-t4", R(47),
      "Let {xₙ}ₙ≥₁ be a sequence defined as xₙ = 1 + 1/√2 + 1/√3 + ⋯ + 1/√n − 2(√n − 1). Then which of the following "
      "options is/are correct?",
      ["The sequence {xₙ}ₙ≥₁ is unbounded", "The sequence {xₙ}ₙ≥₁ is monotonically decreasing",
       "The sequence {xₙ}ₙ≥₁ is bounded but does not converge", "The sequence {xₙ}ₙ≥₁ converges"],
      "BD",
      ["False: it is decreasing and bounded below (see the reasons for B and D).",
       "xₙ₊₁ − xₙ = 1/√(n + 1) − 2(√(n + 1) − √n) = 1/√(n + 1) − 2/(√(n + 1) + √n) < 0, since √(n + 1) + √n < 2√(n + 1).",
       "False: a bounded monotone sequence converges.",
       "Comparing with ∫ dx/√x, Σₖ≤ₙ 1/√k − 2√n stays above −2 + 1 > −∞, so xₙ is decreasing and bounded below, hence "
       "convergent."],
      "A",
      "Each step adds 1/√(n + 1) but subtracts 2(√(n + 1) − √n) = 2/(√(n + 1) + √n), which is larger, so xₙ decreases. The "
      "integral comparison Σₖ₌₁ⁿ 1/√k ≥ ∫₁ⁿ⁺¹ dx/√x = 2√(n + 1) − 2 keeps xₙ above 2(√(n + 1) − √n) > 0, so it is bounded "
      "below and converges (to 2 + ζ(1/2) ≈ 0.54).", year=YEAR),
    M("gate25-q48", "maths", "maths-t15", R(48),
      "Let 𝒪 = {P : P is a 3 × 3 real matrix satisfying PᵀP = I₃ and det(P) = 1}, where I₃ denotes the identity matrix of "
      "order 3. Then which of the following options is/are correct?",
      ["There exists a P ∈ 𝒪 with λ = 1/2 as an eigen value", "There exists a P ∈ 𝒪 with λ = 2 as an eigen value",
       "If λ is the only real eigen value of P ∈ 𝒪, then λ = 1", "There exists a P ∈ 𝒪 with λ = −1 as an eigen value"],
      "CD",
      ["False: an orthogonal matrix preserves length, so every eigenvalue has |λ| = 1.",
       "False: for the same reason |λ| = 1, so 2 is impossible.",
       "True: the eigenvalues are 1 and a pair e^(±iθ), or real ±1 values with product 1; a real eigenvalue of a rotation "
       "in 3D is always 1 (the axis), so if only one real value appears it is 1.",
       "True: rotation by π about an axis, diag(1, −1, −1), has determinant 1 and eigenvalue −1."],
      "D",
      "Matrices in 𝒪 are rotations of ℝ³. They preserve length, so real eigenvalues are ±1, and the product of the three "
      "eigenvalues is det P = 1, which forces the eigenvalue 1 (the rotation axis). A half-turn has eigenvalues 1, −1, −1.",
      year=YEAR),
    M("gate25-q49", "probability", "probability-t13", R(49),
      "Let X₁, X₂, and X₃ be independent standard normal random variables, and let Y₁ = X₁ − X₂, Y₂ = X₁ + X₂ − 2X₃ and "
      "Y₃ = X₁ + X₂ + X₃. Then which of the following options is/are correct?",
      ["Y₁, Y₂ and Y₃ are independently distributed", "Y₁² + Y₂² + Y₃² ~ χ²₃", "2Y₃/√(3Y₁² + Y₂²) ~ t₂",
       "(3Y₁² + 2Y₃²)/(2Y₂²) ~ F₁,₁"],
      "AC",
      ["True: the coefficient vectors (1, −1, 0), (1, 1, −2), (1, 1, 1) are mutually orthogonal, so the jointly normal Yᵢ are "
       "uncorrelated and hence independent.",
       "False: Var(Y₁) = 2, Var(Y₂) = 6, Var(Y₃) = 3, so the squares are not standard chi-squares and the sum is not χ²₃.",
       "True: Y₃/√3 ~ N(0, 1) and Y₁²/2 + Y₂²/6 = (3Y₁² + Y₂²)/6 ~ χ²₂, independent, and (Y₃/√3)/√((3Y₁² + Y₂²)/12) = "
       "2Y₃/√(3Y₁² + Y₂²).",
       "False: (3Y₁² + 2Y₃²)/6 ~ χ²₂ and Y₂²/6 ~ χ²₁, so the ratio is [χ²₂/2]/[χ²₁/1], an F₂,₁ variable."],
      "C",
      "Standardise first: Y₁/√2, Y₂/√6 and Y₃/√3 are independent N(0, 1). Then each statement is a question about which sums "
      "of their squares appear: the t-ratio in C uses two squares below one normal, so 2 degrees of freedom; the ratio in D "
      "has two squares on top, so F₂,₁ and not F₁,₁.", year=YEAR, diff="hard"),
    M("gate25-q50", "probability", "probability-t9", R(50),
      "Let {Xₙ}ₙ≥₁ be a sequence of independent random variables and Xₙ → 0 almost surely as n → ∞. Then which of the "
      "following options is/are necessarily correct?",
      ["E(Xₙ³) → 0 as n → ∞", "Xₙ⁷ → 0 in probability as n → ∞", "For any ε > 0, Σₙ₌₁^∞ Pr(|Xₙ| ≥ ε) < ∞",
       "Xₙ² + Xₙ + 5 → 5 almost surely as n → ∞"],
      "BCD",
      ["Not necessarily: take Xₙ = n with probability 1/n² and 0 otherwise; Xₙ → 0 a.s. but E(Xₙ³) = n → ∞.",
       "True: Xₙ⁷ → 0 almost surely by continuity, and almost sure convergence implies convergence in probability.",
       "True: if the sum were infinite for some ε, the second Borel–Cantelli lemma (independence) would give |Xₙ| ≥ ε "
       "infinitely often with probability 1, contradicting Xₙ → 0 a.s.",
       "True: x ↦ x² + x + 5 is continuous, so it carries almost sure convergence to 0 into convergence to 5."],
      "A",
      "Continuous functions preserve almost sure convergence (B, D). Independence turns a.s. convergence into the summability "
      "of Pr(|Xₙ| ≥ ε) through the second Borel–Cantelli lemma (C). Moments need uniform integrability, which is not given, so "
      "A can fail.", year=YEAR, diff="hard"),
    M("gate25-q51", "stochastic", "stochastic-t2", R(51),
      "Consider a Markov chain {Xₙ : n = 1, 2, …} with state space S = {1, 2, 3} and transition probability matrix "
      "P = [[0, 1/2, 1/2], [1/3, 0, 2/3], [2/5, 3/5, 0]]. Define π = (18/67, 24/67, 25/67). Which of the following options "
      "is/are correct?",
      ["π is a stationary distribution of P", "πᵀ is an eigen vector of Pᵀ", "Pr(X₃ = 1 | X₁ = 1) = 11/30",
       "At least one state is transient"],
      "ABC",
      ["True: πP = ((24/67)(1/3) + (25/67)(2/5), (18/67)(1/2) + (25/67)(3/5), (18/67)(1/2) + (24/67)(2/3)) = "
       "(18/67, 24/67, 25/67) = π.",
       "True: πP = π transposes to Pᵀπᵀ = πᵀ, so πᵀ is an eigenvector of Pᵀ with eigenvalue 1.",
       "True: the two-step return probability is P²₁₁ = (1/2)(1/3) + (1/2)(2/5) = 1/6 + 1/5 = 11/30.",
       "False: every state reaches every other, so the finite chain is irreducible and all states are recurrent."],
      "D",
      "Check πP = π column by column; a stationary row vector is a left eigenvector of P, i.e. an eigenvector of Pᵀ. Two-step "
      "probabilities come from P², and a finite irreducible chain has no transient states.", year=YEAR),
    M("gate25-q52", "inference", "inference-t3", R(52),
      "Let X₁, …, Xₙ be a random sample from a uniform distribution over the interval (−θ/2, θ/2), where θ > 0 is an "
      "unknown parameter. Then which of the following options is/are correct?",
      ["2 max{X₁, …, Xₙ} is the maximum likelihood estimator of θ", "(min{X₁, …, Xₙ}, max{X₁, …, Xₙ}) is a sufficient statistic",
       "(min{X₁, …, Xₙ}, max{X₁, …, Xₙ}) is a complete statistic",
       "(2(n + 1)/n) max{|X₁|, …, |Xₙ|} is a uniformly minimum variance unbiased estimator of θ"],
      "BD",
      ["False: the likelihood θ⁻ⁿ needs θ ≥ 2 max|Xᵢ|, so the MLE is 2 max|Xᵢ|; 2 max Xᵢ can even be negative.",
       "True: the likelihood depends on the data through max|Xᵢ| = max(−min Xᵢ, max Xᵢ), a function of (min, max).",
       "False: E(min Xᵢ + max Xᵢ) = 0 for every θ by symmetry, though min + max is not zero, so the pair is not complete.",
       "True: T = max|Xᵢ| is complete sufficient; |Xᵢ| ~ Uniform(0, θ/2) gives E(T) = nθ/(2(n + 1)), so (2(n + 1)/n)T is "
       "unbiased and, by Lehmann–Scheffé, the UMVUE."],
      "D",
      "The whole problem turns on T = max|Xᵢ|: it is the minimal sufficient statistic and it is complete, while the pair "
      "(min, max) is sufficient but carries a symmetric ancillary piece that destroys completeness.", year=YEAR, diff="hard"),
    M("gate25-q53", "multivariate", "multivariate-t1", R(53),
      "Let X = (X₁, X₂, X₃)ᵀ be a 3-dimensional random vector having multivariate normal distribution with mean vector "
      "(0, 0, 0)ᵀ and covariance matrix Σ = diag(4, 9, 4). Let αᵀ = (2, 0, −1) and βᵀ = (1, 1, 1). Then which of the "
      "following statements is/are correct?",
      ["E(trace(XXᵀααᵀ)) = 20", "Var(trace(Xαᵀ)) = 20", "E(trace(XXᵀ)) = 17", "Cov(αᵀX, βᵀX) = 3"],
      "ABC",
      ["True: trace(XXᵀααᵀ) = (αᵀX)², and E(αᵀX)² = αᵀΣα = 4·4 + 0 + 1·4 = 20.",
       "True: trace(Xαᵀ) = αᵀX, whose variance is αᵀΣα = 20.",
       "True: trace(XXᵀ) = XᵀX, with mean trace(Σ) = 4 + 9 + 4 = 17.",
       "False: Cov(αᵀX, βᵀX) = αᵀΣβ = 2·4·1 + 0·9·1 + (−1)·4·1 = 4."],
      "A",
      "Each trace collapses to a scalar: trace(XXᵀααᵀ) = (αᵀX)², trace(Xαᵀ) = αᵀX and trace(XXᵀ) = XᵀX. Then use "
      "Var(aᵀX) = aᵀΣa, E(XᵀX) = trace Σ and Cov(aᵀX, bᵀX) = aᵀΣb.", year=YEAR),
    M("gate25-q54", "regression", "regression-t2", R(54),
      "For Y ∈ ℝⁿ, X ∈ ℝⁿˣᵖ, and β ∈ ℝᵖ, consider a regression model Y = Xβ + ε, where ε has an n-dimensional multivariate "
      "normal distribution with zero mean vector and identity covariance matrix. Let Iₚ denote the identity matrix of order p. "
      "For λ > 0, let β̂ₙ = (XᵀX + λIₚ)⁻¹XᵀY be an estimator of β. Then which of the following options is/are correct?",
      ["β̂ₙ is an unbiased estimator of β", "(XᵀX + λIₚ) is a positive definite matrix", "β̂ₙ has a multivariate normal distribution",
       "Var(β̂ₙ) = (XᵀX + λIₚ)⁻¹"],
      "BC",
      ["False: E(β̂ₙ) = (XᵀX + λI)⁻¹XᵀXβ, which differs from β whenever β ≠ 0 (ridge shrinks towards 0).",
       "True: vᵀ(XᵀX + λI)v = ‖Xv‖² + λ‖v‖² > 0 for every v ≠ 0.",
       "True: β̂ₙ is a fixed linear transformation of the normal vector Y.",
       "False: Var(β̂ₙ) = (XᵀX + λI)⁻¹XᵀX(XᵀX + λI)⁻¹, which is not (XᵀX + λI)⁻¹ in general."],
      "C",
      "This is the ridge estimator. Adding λI makes the matrix positive definite and invertible even when XᵀX is singular, at "
      "the cost of bias; being linear in Y it stays normal, with the sandwich variance A XᵀX A where A = (XᵀX + λI)⁻¹.",
      year=YEAR),
    N("gate25-q55", "maths", "maths-t11", R(55),
      "Let f: ℝ² → ℝ be defined as f(x, y) = x²y² + 8x − 4y. The number of saddle points of f is ________ (answer in "
      "integer).", "1",
      "Critical points solve f_x = 2xy² + 8 = 0 and f_y = 2x²y − 4 = 0. The second gives y = 2/x²; substituting, "
      "8/x³ + 8 = 0, so x = −1 and y = 2: one critical point. There f_xx = 2y² = 8, f_yy = 2x² = 2, f_xy = 4xy = −8, and "
      "f_xx f_yy − f_xy² = 16 − 64 < 0, so it is a saddle point.",
      "A saddle point must first be a critical point; there is only one, so the answer is 0 or 1.", year=YEAR),
    N("gate25-q56", "maths", "maths-t16", R(56),
      "Let P be the 5 × 5 matrix with rows (0, 1, 1, 1, 1), (−1, 0, 1, 1, 1), (−1, −1, 0, 1, 1), (−1, −1, −1, 0, 1), "
      "(−1, −1, −1, −1, 0). If λ₁, λ₂, λ₃, λ₄, and λ₅ are eigen values of P, then ∏ᵢ₌₁⁵ λᵢ equals ________ (answer in "
      "integer).", "0",
      "The product of the eigenvalues is det P. P is skew-symmetric (Pᵀ = −P), so det P = det(Pᵀ) = det(−P) = (−1)⁵ det P "
      "= −det P, which forces det P = 0.",
      "Every odd-order skew-symmetric matrix is singular; check that Pᵀ = −P before computing anything.", year=YEAR,
      diff="easy"),
    N("gate25-q57", "maths", "maths-t2", R(57),
      "Let P = [[2, 1], [1, 2]] and Q = [[1, 1], [−2, 4]]. Then the value of trace(P⁵ + Q⁴) equals ________ (answer in "
      "integer).", "341",
      "Trace of a power is the sum of the eigenvalues' powers. P has eigenvalues 1 and 3 (trace 4, determinant 3), so "
      "trace(P⁵) = 1 + 243 = 244. Q has trace 5 and determinant 4 + 2 = 6, so eigenvalues 2 and 3 and trace(Q⁴) = 16 + 81 "
      "= 97. Total 244 + 97 = 341.",
      "trace(P⁵) alone is dominated by 3⁵ = 243 and trace(Q⁴) by 3⁴ = 81, so the answer must exceed 324.", year=YEAR),
    N("gate25-q58", "probability", "probability-t5", R(58),
      "The moment generating functions of three independent random variables X, Y and Z are respectively given as "
      "M_X(t) = (1/9)(2 + eᵗ)², M_Y(t) = e^(eᵗ − 1) and M_Z(t) = e^(2(eᵗ − 1)), t ∈ ℝ. Then 10 Pr(X > Y + Z) equals "
      "________ (rounded off to two decimal places).", "0.44",
      "Read the distributions from the MGFs: X ~ Bin(2, 1/3), Y ~ Poisson(1), Z ~ Poisson(2), so S = Y + Z ~ Poisson(3). "
      "X > S needs X = 1, S = 0 or X = 2, S ≤ 1: Pr = (4/9)e⁻³ + (1/9)(4e⁻³) = (8/9)e⁻³ = 0.04425. Times 10: 0.44.",
      "X ≤ 2, so S must be 0 or 1, and Pr(S ≤ 1) = 4e⁻³ ≈ 0.2; the probability has to be small.", year=YEAR),
    N("gate25-q59", "probability", "probability-t12", R(59),
      "The service times (in minutes) at two petrol pumps P₁ and P₂ follow distributions with probability density functions "
      "f₁(x) = λe^(−λx), x > 0 and f₂(x) = λ²xe^(−λx), x > 0, respectively, where λ > 0. For service, a customer chooses P₁ or "
      "P₂ randomly with equal probability. Suppose, the probability that the service time for the customer is more than one "
      "minute, is 2e⁻². Then the value of λ equals ________ (answer in integer).", "2",
      "Total probability: Pr(T > 1) = (1/2)e^(−λ) + (1/2)(1 + λ)e^(−λ) = ((2 + λ)/2)e^(−λ). Setting this equal to 2e⁻²: "
      "λ = 2 gives (4/2)e⁻² = 2e⁻². The left side decreases in λ, so this is the only solution.",
      "Substitute the answer back: (2 + 2)/2 × e⁻² = 2e⁻².", year=YEAR, diff="easy"),
    N("gate25-q60", "probability", "probability-t9", R(60),
      "Let {Xₙ}ₙ≥₁ be a sequence of independent random variables with Pr(Xₙ = −1/2ⁿ) = Pr(Xₙ = 1/2ⁿ) = 1/2 ∀ n ∈ ℕ. "
      "Suppose that Σᵢ₌₁ⁿ Xᵢ → U in distribution as n → ∞. Then 6 Pr(U ≤ 2/3) equals ________ (answer in integer).", "5",
      "Write Xₙ = (2Bₙ − 1)/2ⁿ with Bₙ independent fair bits. Then ΣXₙ = 2ΣBₙ/2ⁿ − Σ1/2ⁿ = 2V − 1, where V = ΣBₙ/2ⁿ is a "
      "random binary expansion, Uniform(0, 1). So U ~ Uniform(−1, 1) and Pr(U ≤ 2/3) = (2/3 + 1)/2 = 5/6; times 6 gives 5.",
      "U is symmetric about 0 with |U| ≤ 1, and 2/3 > 0, so Pr(U ≤ 2/3) is between 1/2 and 1.", year=YEAR, diff="hard"),
    N("gate25-q61", "inference", "inference-t4", R(61),
      "Let X₁, X₂, …, X₇ be a random sample from a population having the probability density function "
      "f(x) = (1/2)λ³x²e^(−λx), x > 0, where λ > 0 is an unknown parameter. Let λ̂ be the maximum likelihood estimator of λ, "
      "and E(λ̂ − λ) = αλ be the corresponding bias, where α is a real constant. Then the value of 1/α equals ________ (answer "
      "in integer).", "20",
      "Each Xᵢ is Gamma(3, λ). The log-likelihood 21 ln λ − λΣxᵢ + const is maximised at λ̂ = 21/S with S = ΣXᵢ ~ Gamma(21, λ). "
      "E(1/S) = λ/20, so E(λ̂) = 21λ/20 and the bias is λ/20: α = 1/20 and 1/α = 20.",
      "For S ~ Gamma(k, λ), E(1/S) = λ/(k − 1), so the MLE kλ/(k − 1) overshoots by a factor k/(k − 1) = 21/20.", year=YEAR),
    N("gate25-q62", "inference", "inference-t9", R(62),
      "Let X₁, X₂ be a random sample from a population having probability density function f_θ(x) = e^(x − θ) if "
      "−∞ < x ≤ θ, and 0 otherwise, where θ ∈ ℝ is an unknown parameter. Consider testing H₀: θ ≥ 0 against H₁: θ < 0 at "
      "level α = 0.09. Let β(θ) denote the power function of a uniformly most powerful test. Then β(logₑ 0.36) equals "
      "________ (rounded off to two decimal places).", "0.69",
      "The maximum M = max(X₁, X₂) is sufficient, with Pr_θ(M ≤ c) = e^(2(c − θ)) for c ≤ θ. Small values of M point to "
      "small θ, so the UMP test rejects when M ≤ c, with size e^(2c) = 0.09 at θ = 0, i.e. c = ln 0.3. At θ = ln 0.36 "
      "(> c): β = e^(2c)/e^(2θ) = 0.09/0.36² = 0.09/0.1296 = 0.694, which rounds to 0.69.",
      "e^(2θ) at θ = ln 0.36 is 0.36² = 0.1296, not 0.36; dividing by 0.36 instead gives the wrong 0.25.", year=YEAR,
      diff="hard"),
    N("gate25-q63", "inference", "inference-t12", R(63),
      "Let X ~ Bin(3, θ), where θ ∈ (0, 1) is an unknown parameter. For testing H₀: 1/4 ≤ θ ≤ 3/4 against H₁: θ < 1/4 or "
      "θ > 3/4, consider the test φ(x) = 1 if x ∈ {0, 3} and 0 if x ∈ {1, 2}. The size of the test φ is ________ (rounded "
      "off to two decimal places).", "0.44",
      "The rejection probability is θ³ + (1 − θ)³ = 1 − 3θ + 3θ², a parabola with its minimum at θ = 1/2. Over the null "
      "interval [1/4, 3/4] its largest value is at the endpoints: (1/4)³ + (3/4)³ = 1/64 + 27/64 = 28/64 = 0.4375, so the "
      "size is 0.44.",
      "Size is the supremum over the whole null set, not the value at its centre (which would be 0.25).", year=YEAR),
    N("gate25-q64", "multivariate", "multivariate-t2", R(64),
      "Let (X₁, X₂, X₃)ᵀ follow N₃ with mean (0, 0, 0)ᵀ and covariance matrix with rows (1, 0.4, 0), (0.4, 1, 0.6), "
      "(0, 0.6, 1). Then the value of the partial correlation coefficient between X₁ and X₂ given X₃ is ________ (rounded off "
      "to two decimal places).", "0.50",
      "With unit variances the covariances are the correlations: ρ₁₂ = 0.4, ρ₁₃ = 0, ρ₂₃ = 0.6. "
      "ρ₁₂.₃ = (ρ₁₂ − ρ₁₃ρ₂₃)/√((1 − ρ₁₃²)(1 − ρ₂₃²)) = (0.4 − 0)/√(1 × 0.64) = 0.4/0.8 = 0.50.",
      "Partialling out X₃, which is uncorrelated with X₁, can only enlarge |ρ₁₂| here, since the denominator is below 1.",
      year=YEAR, diff="easy"),
    N("gate25-q65", "multivariate", "multivariate-t1", R(65),
      "Let (X, Y)ᵀ follow a bivariate normal distribution with E(X) = 2, E(Y) = 3, Var(X) = 16, Var(Y) = 25, and "
      "Cov(X, Y) = 14. Then 2π(Pr(X > 2, Y > 3) − 1/4) equals ________ (rounded off to two decimal places).", "0.78",
      "The correlation is ρ = 14/(4 × 5) = 0.7. For a bivariate normal, the probability that both variables exceed their "
      "means is the orthant probability 1/4 + arcsin(ρ)/(2π). So 2π(Pr − 1/4) = arcsin(0.7) = 0.7754, which rounds to 0.78.",
      "arcsin of a positive correlation is positive and below π/2 ≈ 1.57; for ρ = 0.7 it is a little above 0.7.", year=YEAR),
]


def build():
    banks = OrderedDict()
    for x in ITEMS:
        banks.setdefault(x["module"], []).append(x["item"])
    out = OrderedDict()
    for m in sorted(banks, key=lambda k: MODULE_ORDER.index(k)):
        its = banks[m]
        out["seed/%s_gate25.json" % m] = OrderedDict([("moduleId", m), ("source", "variant"), ("label", LABEL),
                                                       ("count", len(its)), ("items", its)])
    return out


def render(d):
    return json.dumps(d, ensure_ascii=False, indent=1) + "\n"


def main(argv):
    files = OrderedDict((f, render(d)) for f, d in build().items())
    if "--check" in argv:
        bad = [f for f, t in files.items()
               if not os.path.exists(os.path.join(ROOT, f))
               or io.open(os.path.join(ROOT, f), encoding="utf-8", newline="").read().replace("\r\n", "\n") != t]
        for f in bad:
            print("differs from the build: " + f)
        return 1 if bad else 0
    for f, t in files.items():
        p = os.path.join(ROOT, f)
        if os.path.exists(p) and "--force" not in argv and io.open(p, encoding="utf-8").read().replace("\r\n", "\n") != t:
            print("refusing to overwrite %s (edited after its first merge?); pass --force" % f)
            return 1
        with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(t)
        print("wrote %s (%d items)" % (f, len(json.loads(t)["items"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
