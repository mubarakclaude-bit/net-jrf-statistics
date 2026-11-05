
# 13. Practice set B — 25 numerical problems

**This is step 3 of the deep session, and it is the most important set in the module.** Numerical questions were 4/21 in June — below what guessing returns. Work each problem on paper, write the number, then run the named check *before* moving on. A problem solved without the check does not count as solved.

**1.** n = 10 from Bernoulli(p), with Σxᵢ = 3. Find the MLE of p.
→ **0.3**. p̂ = x̄ = 3/10. *Check: a probability must lie in [0, 1].*

**2.** Same data. Find the UMVUE of p.
→ **0.3**. X̄ is unbiased and a function of the complete sufficient statistic, so MLE and UMVUE coincide here. *Check: ask whether the parameter sits in a denominator — if not, the two usually agree.*

**3.** Same data. Find the UMVUE of p².
→ **0.0667**. T(T−1)/[n(n−1)] = (3)(2)/[(10)(9)] = 6/90. *Check: compare with p̂² = 0.09. They differ, and must — the UMVUE of p² is not the square of the UMVUE of p.*

**4.** n = 5 from Poisson(λ) with Σxᵢ = 12. Find the MLE of λ, the total Fisher information, and the CRLB for unbiased estimators of λ.
→ **λ̂ = 2.4; nI(λ) = 5/2.4 = 2.083; CRLB = λ/n = 0.48**. *Check: Var(X̄) = λ/n equals the bound exactly, so X̄ is efficient.*

**5.** Same Poisson data. Find the UMVUE of e^(−λ) and compare it with the MLE.
→ **UMVUE = (4/5)¹² = 0.0687; MLE = exp(−2.4) = 0.0907**. *Check: both must lie in (0, 1), and they must differ — the MLE of e^(−λ) is biased.*

**6.** n = 8 from exponential with rate θ, Σxᵢ = 20. Find the MLE and the UMVUE of θ, and the bias of the MLE.
→ **MLE = 8/20 = 0.4; UMVUE = 7/20 = 0.35; bias = θ/(n−1) = θ/7**. *Check: the MLE must exceed the UMVUE, since E(MLE) = nθ/(n−1) > θ.*

**7.** Same data, but now θ denotes the **mean**. Find the MLE and the UMVUE.
→ **Both X̄ = 20/8 = 2.5**. *Check: reread which parameterisation the question used. Rate and mean give different answers from identical data.*

**8.** n = 6 from U(0, θ) with x₍₆₎ = 9.2. Find the MLE and the UMVUE of θ.
→ **MLE = 9.2; UMVUE = (7/6)(9.2) = 10.733**. *Check: the UMVUE must exceed the observed maximum — θ cannot be smaller than a value you have already seen.*

**9.** In problem 8, write the variance of the UMVUE.
→ **θ²/[n(n+2)] = θ²/48**. *Check: this falls like 1/n², faster than any CRLB rate — correct, because the support depends on θ and the bound does not apply.*

**10.** n = 10 from N(μ, σ²), both unknown, with Σ(xᵢ − x̄)² = 36. Find the MLE and the UMVUE of σ².
→ **MLE = 36/10 = 3.6; UMVUE = 36/9 = 4**. *Check: divisor n versus n − 1. The MLE is always the smaller.*

**11.** Compute Fisher information for a single Bernoulli observation at p = 0.25.
→ **I(p) = 1/[p(1−p)] = 1/0.1875 = 5.333**. *Check: information is largest near p = 0 or 1 and smallest at p = 0.5 — substitute p = 0.5 and confirm you get 4.*

**12.** With n = 20 and p = 0.25, find the CRLB for unbiased estimators of p.
→ **p(1−p)/n = 0.1875/20 = 0.009375**. *Check: Var(X̄) = p(1−p)/n is identical, so X̄ attains the bound.*

**13.** n = 25 from N(μ, 16). Find the CRLB for μ and state whether X̄ attains it.
→ **σ²/n = 16/25 = 0.64; yes, Var(X̄) = 0.64**. *Check: efficiency = CRLB/Var = 1.*

**14.** n = 10 from exponential with rate θ. Compare the variance of the UMVUE of θ with the CRLB.
→ **Var[(n−1)/ΣXᵢ] = θ²/(n−2) = θ²/8; CRLB = θ²/n = θ²/10**. *Check: the UMVUE's variance is larger. This is legitimate — being UMVUE does not require attaining the bound.*

**15.** n = 12 from geometric(p), counting trials to the first success, with Σxᵢ = 40. Find the MLE of p.
→ **p̂ = 1/x̄ = 12/40 = 0.3**. *Check: p must lie in (0, 1], and x̄ = 3.33 should be near 1/p = 3.33.*

**16.** n = 10 from U(0, θ) with x̄ = 4.1 and x₍₁₀₎ = 9.2. Find the method-of-moments estimate and comment.
→ **2x̄ = 8.2**, which is **smaller than an observed value**. *Check: any estimate of θ below x₍ₙ₎ is impossible. This is the standard demonstration that the method of moments can ignore a sufficient statistic.*

**17.** n = 5 from Gamma(α = 3 known, β) with Σxᵢ = 30. Find the MLE of β.
→ **β̂ = nα/Σxᵢ = 15/30 = 0.5**. *Check: E(X) = α/β = 6, and x̄ = 6 ✓.*

**18.** n = 8 from N(5, σ²) with μ known to be 5 and Σ(xᵢ − 5)² = 40. Find the MLE and the UMVUE of σ².
→ **Both 40/8 = 5**. *Check: when μ is known, no degree of freedom is spent, so the divisor is n for both.*

**19.** For n = 10, compare the MSE of the MLE of σ² with the MSE of S².
→ **MSE(MLE) = 0.19σ⁴; MSE(S²) = 2σ⁴/9 = 0.222σ⁴**. Working: Var(MLE) = 2(n−1)σ⁴/n² = 0.18σ⁴, bias = −σ²/n so bias² = 0.01σ⁴. *Check: the biased estimator wins on MSE — unbiasedness is a convention, not an optimum.*

**20.** n = 20 from Bernoulli with Σxᵢ = 5. State the efficiency of X̄ as an estimator of p.
→ **1**. Var(X̄) = p(1−p)/n equals the CRLB. *Check: efficiency can never exceed 1 under the regularity conditions.*

**21.** n = 6 from exponential with rate θ and Σxᵢ = 15. Estimate P(X > 2) by maximum likelihood.
→ **θ̂ = 6/15 = 0.4, so exp(−2θ̂) = exp(−0.8) = 0.449**. *Check: a probability, so it must sit in (0, 1); and since the mean is 2.5, P(X > 2) should be a little under 0.5 ✓.*

**22.** n = 4 from Poisson with Σxᵢ = 6. Find the UMVUE of e^(−λ).
→ **(3/4)⁶ = 0.178**. *Check: compare the MLE exp(−1.5) = 0.223. The UMVUE is the smaller here.*

**23.** n = 4 from U(0, θ) with x₍₄₎ = 10 and x̄ = 5.5. Give the MLE, the UMVUE and the MoM estimate.
→ **MLE = 10; UMVUE = (5/4)(10) = 12.5; MoM = 2(5.5) = 11**. *Check: all three must be at least 10. Here they are, but only by luck for MoM.*

**24.** n = 20 from Poisson(λ = 4). Find the total Fisher information and the CRLB for unbiased estimators of λ.
→ **nI(λ) = 20/4 = 5; CRLB = 1/5 = 0.2**. *Check: λ/n = 4/20 = 0.2 ✓, the two routes must agree.*

**25.** A sample of size n from exponential with mean θ. Write the distribution of ΣXᵢ, of 2ΣXᵢ/θ, and E(1/ΣXᵢ).
→ **Gamma(n, 1/θ); χ²₂ₙ; E(1/ΣXᵢ) = 1/[θ(n−1)]**. *Check: the chi-square has 2n degrees of freedom, not n — this is what converts exponential problems onto chi-square tables.*

**Scoring.** Below 15/25, repeat the set on Sunday before attempting the self-test. The target for week 2 is 18/25 on a fresh set of comparable difficulty.

---

# 14. Practice set C — 35 multi-statement questions

**Five a day, every day.** This format was 2/19 in June — worse than guessing — and it is 38 marks of the paper. The method is fixed and not negotiable: **decide true or false for each of A, B, C and D separately, write one word of reason for each, and only then look at the options.** Picking the option that "looks right" is exactly what produced 2/19.

The answers below are written in that form deliberately — a verdict and a reason per statement — so that you can mark your own reasoning, not just your final letter.

## Day 1 — sufficiency

**1.** X₁, …, Xₙ are iid Bernoulli(p).
A. ΣXᵢ is sufficient for p. B. The conditional distribution of the sample given ΣXᵢ = t depends on p. C. X̄ is sufficient for p. D. (X₁, X₂) is sufficient for p.
(A) A, C only (B) A, B, C only (C) A, C, D only (D) B, D only
→ **(A)**. A ✓ by factorisation. B ✗ that is precisely what sufficiency denies. C ✓ one-to-one function of ΣXᵢ. D ✗ it discards the rest of the sample.

**2.** Concerning the factorisation theorem.
A. f(x;θ) = g(T;θ)h(x) is necessary and sufficient for sufficiency. B. h(x) may involve θ through its support. C. The factorisation is unique. D. The whole sample is always sufficient.
(A) A, B only (B) A, D only (C) A, C, D only (D) B, C only
→ **(B)**. A ✓ the theorem is an "if and only if". B ✗ h must be free of θ entirely, support included — this is the U(0,θ) trap. C ✗ constants can be moved between g and h. D ✓ trivially.

**3.** A random sample from U(0, θ).
A. X₍ₙ₎ is sufficient. B. X̄ is sufficient. C. The support depends on θ. D. The family is an exponential family.
(A) A, C only (B) A, B, C only (C) C, D only (D) A, D only
→ **(A)**. A ✓ from the indicator. B ✗ X̄ throws away the maximum. C ✓. D ✗ exponential families cannot have θ-dependent support.

**4.** Concerning minimal sufficiency.
A. A minimal sufficient statistic is a function of every sufficient statistic. B. It is unique. C. A complete sufficient statistic is minimal sufficient. D. For the Cauchy family the order statistics are minimal sufficient.
(A) A, B, C only (B) A, C, D only (C) B, C only (D) A, D only
→ **(B)**. A ✓ by definition. B ✗ unique only up to one-to-one transformation — X̄ and ΣXᵢ are both minimal sufficient. C ✓. D ✓ no genuine reduction is possible there.

**5.** A random sample from N(μ, σ²) with both parameters unknown.
A. (ΣXᵢ, ΣXᵢ²) is sufficient. B. (X̄, S²) is sufficient. C. X̄ alone is sufficient for μ. D. The sufficient statistic is two-dimensional.
(A) A, B, D only (B) A, C only (C) A, B, C, D (D) B, D only
→ **(A)**. A ✓. B ✓ one-to-one with A. C ✗ with σ² unknown, X̄ alone does not reproduce the likelihood. D ✓.

## Day 2 — exponential families, completeness, ancillarity

**6.** Concerning exponential families.
A. Poisson belongs. B. U(0, θ) belongs. C. The natural parameter for Bernoulli is log[p/(1−p)]. D. Membership gives a complete sufficient statistic when the natural parameter space contains an open interval.
(A) A, C, D only (B) A, B, C only (C) C, D only (D) A, D only
→ **(A)**. A ✓. B ✗ θ-dependent support. C ✓ the logit. D ✓ this is the completeness condition.

**7.** Concerning completeness.
A. E[g(T)] = 0 for all θ implying g ≡ 0 is the definition. B. Completeness implies sufficiency. C. For U(θ, θ+1), (X₍₁₎, X₍ₙ₎) is complete. D. For U(0, θ), X₍ₙ₎ is complete.
(A) A, D only (B) A, B, D only (C) A, C only (D) B, C, D only
→ **(A)**. A ✓. B ✗ they are independent properties; neither implies the other. C ✗ the range provides a non-trivial unbiased estimator of zero. D ✓ proved by differentiating under the integral.

**8.** Concerning ancillary statistics.
A. An ancillary statistic has a distribution free of θ. B. The range in U(θ, θ+1) is ancillary. C. An ancillary statistic is sufficient. D. Basu's theorem gives independence of a complete sufficient statistic and any ancillary statistic.
(A) A, B, D only (B) A, B, C only (C) A, D only (D) B, C, D only
→ **(A)**. A ✓ by definition. B ✓ the interval has fixed length. C ✗ it is the opposite pole from sufficiency. D ✓.

**9.** A random sample from N(μ, σ²) with σ² known.
A. X̄ is complete sufficient for μ. B. S² is ancillary. C. X̄ and S² are independent. D. Proving that independence requires Helmert's transformation.
(A) A, B, C only (B) A, C, D only (C) A, B, C, D (D) B, C only
→ **(A)**. A ✓. B ✓ its distribution involves only σ², which is known. C ✓. D ✗ Basu's theorem gives it in one line.

**10.** The shifted exponential f(x) = exp(−(x−θ)), x ≥ θ.
A. It belongs to the exponential family. B. X₍₁₎ is sufficient for θ. C. The Cramér–Rao bound applies. D. X̄ − 1 is unbiased for θ.
(A) B, D only (B) A, B only (C) B, C, D only (D) A, C only
→ **(A)**. A ✗ support depends on θ. B ✓ from the indicator. C ✗ the regularity conditions fail. D ✓ since E(X) = θ + 1.

## Day 3 — Rao–Blackwell

**11.** Concerning the Rao–Blackwell theorem.
A. It requires T to be sufficient. B. It requires T to be complete. C. E(h|T) is unbiased for whatever h was unbiased for. D. Var[E(h|T)] ≤ Var(h).
(A) A, C, D only (B) A, B, C only (C) A, B, C, D (D) C, D only
→ **(A)**. A ✓ this is what makes E(h|T) a statistic. B ✗ completeness belongs to Lehmann–Scheffé. C ✓ the estimand never changes. D ✓ by the law of total variance.

**12.** Further statements on Rao–Blackwell.
A. E(h|T) is a statistic because T is sufficient. B. Equality in the variance inequality holds only if h is already a function of T. C. Applying it to a biased estimator makes the result unbiased. D. Its proof uses the law of total variance.
(A) A, B, D only (B) A, B, C only (C) B, C, D only (D) A, D only
→ **(A)**. A ✓. B ✓ equality needs Var(h|T) = 0. C ✗ it preserves bias exactly as it preserves unbiasedness. D ✓.

**13.** Estimating e^(−λ) in a Poisson sample.
A. I(X₁ = 0) is unbiased for e^(−λ). B. X₁ given ΣXᵢ = t is Binomial(t, 1/n). C. The Rao–Blackwell improvement is ((n−1)/n)^ΣXᵢ. D. exp(−X̄) is unbiased for e^(−λ).
(A) A, B, C only (B) A, C, D only (C) B, C, D only (D) A, B only
→ **(A)**. A ✓ P(X₁ = 0) = e^(−λ). B ✓ the multinomial split. C ✓ computed from B. D ✗ it is the MLE and is biased, by Jensen.

**14.** X₁, …, Xₙ iid exponential with mean θ; T(X₁) = 1 if X₁ > x₀, else 0.
A. E[T(X₁)] = e^(−x₀/θ). B. E[T(X₁) | ΣXᵢ] is the UMVUE of θ. C. It is the UMVUE of e^(−x₀/θ). D. Rao–Blackwell changes the estimand.
(A) A, C only (B) A, B only (C) A, C, D only (D) B, D only
→ **(A)**. A ✓ the survival probability. B ✗ wrong estimand. C ✓. D ✗ it changes the estimator, never the estimand.

**15.** More on improvement by conditioning.
A. Conditioning on an ancillary statistic improves an estimator. B. Conditioning on a sufficient statistic never increases variance. C. If T is not complete the improved estimator may still not be UMVUE. D. Rao–Blackwell assumes E(h²) < ∞.
(A) B, C, D only (B) A, B, C only (C) B, D only (D) A, C, D only
→ **(A)**. A ✗ an ancillary statistic carries no information about θ. B ✓. C ✓ this is exactly why completeness matters. D ✓ needed for the variance to exist.

## Day 4 — Lehmann–Scheffé and the UMVUE

**16.** Concerning Lehmann–Scheffé.
A. It requires completeness and sufficiency. B. The UMVUE is unique. C. Every parametric function has a UMVUE. D. The UMVUE is always a function of the complete sufficient statistic.
(A) A, B, D only (B) A, B, C only (C) B, C, D only (D) A, D only
→ **(A)**. A ✓ both. B ✓ completeness forces it. C ✗ existence is not guaranteed. D ✓.

**17.** A random sample from Poisson(λ).
A. X̄ is the UMVUE of λ. B. S² is the UMVUE of λ. C. X̄ attains the Cramér–Rao bound. D. aX̄ + (1−a)S² is unbiased for λ for every a.
(A) A, C, D only (B) A, B, C only (C) A, C only (D) B, C, D only
→ **(A)**. A ✓. B ✗ S² is unbiased for λ but has larger variance and is not a function of the complete sufficient statistic alone. C ✓ Var(X̄) = λ/n. D ✓ weights summing to one preserve unbiasedness.

**18.** Exponential with rate θ.
A. n/ΣXᵢ is the MLE. B. (n−1)/ΣXᵢ is the UMVUE. C. Both are unbiased. D. The UMVUE attains the Cramér–Rao bound.
(A) A, B only (B) A, B, C only (C) A, B, D only (D) B, C only
→ **(A)**. A ✓. B ✓. C ✗ the MLE has expectation nθ/(n−1). D ✗ its variance is θ²/(n−2), above the bound θ²/n.

**19.** A random sample from U(0, θ).
A. X₍ₙ₎ is the MLE. B. ((n+1)/n)X₍ₙ₎ is the UMVUE. C. 2X̄ is the method-of-moments estimator. D. The UMVUE attains the Cramér–Rao bound.
(A) A, B, C only (B) A, B, D only (C) A, C, D only (D) B, C only
→ **(A)**. A ✓ by inspection. B ✓. C ✓ from x̄ = θ/2. D ✗ the bound does not apply at all here.

**20.** Relationships between the UMVUE and the bound.
A. Attaining the Cramér–Rao bound implies being the UMVUE. B. Being the UMVUE implies attaining the bound. C. A UMVUE may have variance strictly above the bound. D. The UMVUE is by definition unbiased.
(A) A, C, D only (B) A, B, D only (C) C, D only (D) A, B, C, D
→ **(A)**. A ✓ nothing can do better than the bound. B ✗ the converse fails. C ✓ as in question 18. D ✓ it is in the name.

## Day 5 — maximum likelihood

**21.** General properties of maximum likelihood estimators.
A. They are always unbiased. B. They are always functions of a sufficient statistic. C. They are invariant. D. They are always unique.
(A) B, C only (B) A, B, C only (C) B, C, D only (D) A, C only
→ **(A)**. A ✗ σ̂², X₍ₙ₎, n/ΣXᵢ are all biased. B ✓ the likelihood factorises through T. C ✓. D ✗ U(θ, θ+1) and the Laplace median.

**22.** A random sample from N(μ, σ²), both unknown.
A. The MLE of σ² has divisor n. B. The MLE of σ² is unbiased. C. S² is the UMVUE of σ². D. The MLE of μ is X̄.
(A) A, C, D only (B) A, B, D only (C) A, D only (D) B, C, D only
→ **(A)**. A ✓. B ✗ E(σ̂²) = ((n−1)/n)σ². C ✓. D ✓.

**23.** A random sample from U(0, θ).
A. The likelihood equation has no solution. B. The MLE is found by inspection. C. The MLE is biased downward. D. The MLE is asymptotically normal.
(A) A, B, C only (B) A, B, D only (C) B, C, D only (D) A, C only
→ **(A)**. A ✓ the derivative is never zero. B ✓ the likelihood decreases beyond x₍ₙ₎. C ✓ E = nθ/(n+1) < θ. D ✗ it converges at rate n and has a non-normal limit.

**24.** The invariance property.
A. The MLE of g(θ) is g(θ̂). B. Invariance preserves unbiasedness. C. The MLE of σ is the square root of the MLE of σ². D. The MLE of e^(−λ) in a Poisson sample is exp(−X̄).
(A) A, C, D only (B) A, B, C only (C) A, D only (D) C, D only
→ **(A)**. A ✓. B ✗ g(θ̂) is generally biased even when θ̂ is not. C ✓. D ✓.

**25.** Asymptotic behaviour.
A. √n(θ̂ − θ) converges to N(0, 1/I(θ)). B. MLEs are consistent under regularity. C. MLEs attain the Cramér–Rao bound in finite samples. D. MLEs are asymptotically efficient.
(A) A, B, D only (B) A, B, C only (C) B, C, D only (D) A, D only
→ **(A)**. A ✓. B ✓. C ✗ only in the limit, and only in exponential families exactly. D ✓.

## Day 6 — method of moments and Cramér–Rao

**26.** Concerning method-of-moments estimators.
A. They are always consistent. B. They are always functions of a sufficient statistic. C. They are generally less efficient than MLEs. D. They can give estimates outside the parameter space.
(A) A, C, D only (B) A, B, C only (C) C, D only (D) A, B, D only
→ **(A)**. A ✓ by the weak law. B ✗ 2X̄ for U(0,θ) ignores X₍ₙ₎ entirely. C ✓. D ✓.

**27.** The method of moments applied to U(0, θ).
A. 2X̄ is the estimator. B. 2X̄ is unbiased. C. 2X̄ can fall below an observed value. D. 2X̄ is the UMVUE.
(A) A, B, C only (B) A, C, D only (C) A, B only (D) B, C, D only
→ **(A)**. A ✓ from x̄ = θ/2. B ✓ E(2X̄) = θ. C ✓ and then it is logically impossible. D ✗ the UMVUE is ((n+1)/n)X₍ₙ₎.

**28.** Concerning Fisher information.
A. I(θ) = −E[∂²/∂θ² log f]. B. I_n(θ) = nI(θ). C. I(θ) is the variance of the score. D. The expected score equals 1.
(A) A, B, C only (B) A, B, D only (C) B, C, D only (D) A, C only
→ **(A)**. A ✓ the computational form. B ✓ additivity. C ✓ since the score has mean zero. D ✗ the expected score is 0, which is why C holds.

**29.** Concerning the Cramér–Rao inequality.
A. It applies to unbiased estimators. B. Var(T) ≥ [τ′(θ)]²/(nI(θ)). C. It applies when the support depends on θ. D. Equality holds if and only if the score equals k(θ)[T − τ(θ)].
(A) A, B, D only (B) A, B, C only (C) B, C, D only (D) A, D only
→ **(A)**. A ✓. B ✓ note the squared derivative. C ✗ that violates the first regularity condition. D ✓.

**30.** Values of Fisher information.
A. For Bernoulli, I(p) = 1/[p(1−p)]. B. For Poisson, I(λ) = λ. C. For exponential with rate θ, I(θ) = 1/θ². D. For N(μ, σ²) with σ² known, I(μ) = 1/σ².
(A) A, C, D only (B) A, B, D only (C) A, B, C only (D) C, D only
→ **(A)**. A ✓. B ✗ it is 1/λ — information is the reciprocal of the asymptotic variance. C ✓. D ✓.

## Day 7 — mixed revision

**31.** Criteria for comparing estimators.
A. MSE = variance + bias². B. For unbiased estimators MSE equals the variance. C. A biased estimator can have smaller MSE. D. Consistency requires unbiasedness.
(A) A, B, C only (B) A, B, D only (C) A, C, D only (D) B, C only
→ **(A)**. A ✓. B ✓ bias is zero. C ✓ the MLE of σ² beats S² on MSE. D ✗ asymptotic unbiasedness suffices.

**32.** General statements about sufficiency.
A. Sufficiency is defined relative to a parameter. B. A statistic sufficient for μ in a normal sample is also sufficient for σ². C. Any one-to-one function of a sufficient statistic is sufficient. D. Sufficiency implies consistency.
(A) A, C only (B) A, B, C only (C) C, D only (D) A, B only
→ **(A)**. A ✓. B ✗ sufficiency is always for a stated parameter. C ✓. D ✗ X₍ₙ₎ is sufficient for θ in U(0,θ) and biased.

**33.** Distribution facts for the exponential family with rate θ.
A. ΣXᵢ follows Gamma(n, θ). B. 2θΣXᵢ follows χ² with 2n degrees of freedom. C. E(1/ΣXᵢ) = θ/(n−1). D. ΣXᵢ follows Gamma(1, θ).
(A) A, B, C only (B) A, B, D only (C) B, C, D only (D) A, C only
→ **(A)**. A ✓. B ✓ note 2n, not n. C ✓ which is where the UMVUE comes from. D ✗ Gamma(1, θ) is a single exponential — this was the trap in Q40.

**34.** A random sample from U(0, θ).
A. E(X₍ₙ₎) = nθ/(n+1). B. The variance of the UMVUE is θ²/[n(n+2)]. C. The MLE converges at rate √n. D. The UMVUE is ((n+1)/n)X₍ₙ₎.
(A) A, B, D only (B) A, C, D only (C) B, C, D only (D) A, D only
→ **(A)**. A ✓. B ✓. C ✗ the rate is n, which is why the estimator appears to beat the bound. D ✓.

**35.** The architecture of the week.
A. Completeness gives uniqueness of the UMVUE. B. Sufficiency is what makes E(h|T) a statistic. C. Basu's theorem links a complete sufficient statistic with an ancillary one. D. Rao–Blackwell requires completeness.
(A) A, B, C only (B) A, B, D only (C) B, C, D only (D) A, C only
→ **(A)**. A ✓. B ✓. C ✓. D ✗ sufficiency alone — this single word was the whole of Q61.

**Scoring.** Below 20/35, the format is still the problem rather than the content. Redo the set on Sunday writing the four verdicts out in full before looking at any option. The target by week 4 is 60% on fresh multi-statement questions.

---
