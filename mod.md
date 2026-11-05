# Week 1 — Point Estimation

## Self-learning module · UGC NET Statistics (107) · Paper 2

This module covers the whole of week 1: sufficiency, completeness, ancillarity, Rao–Blackwell, Lehmann–Scheffé, maximum likelihood, the method of moments, and the Cramér–Rao inequality. It is written to be worked through with a pen, not read.

**Why this week is built the way it is.** Your June paper breaks down into three tiers: recognition questions 70%, conceptual questions 36%, computational questions 15%. Eighty marks sat in that last tier and you took twelve of them. So this module deliberately carries three separate practice sets — conceptual, numerical, and multi-statement — rather than one mixed bank. The numerical and multi-statement sets are the ones that matter most, and they are the ones you will be tempted to skip.

## How the module feeds the five-step deep session

| Step | Minutes | What you use |
|---|---|---|
| 1 Understand | 15 | The theory section for that day — sections 1 to 9 |
| 2 Reproduce | 15 | The **Reproduce from memory** box at the end of each section |
| 3 Solve | 25 | Section 13, the numerical set — every answer ends with one check |
| 4 Exam format | 15 | Section 14, five multi-statement questions |
| 5 Repair | 10 | Log the error type; redo one wrong problem from blank paper |

If a session runs short, cut problems from step 3. Never cut step 2 or step 5.

## The day grid

| Day | Deep session | Light slots |
|---|---|---|
| Mon | §2 Sufficiency and factorisation | §1; the four definitions |
| Tue | §3 Exponential families, §4 Completeness and ancillarity | Paper 1: UGC, AICTE, NAAC, NCTE |
| Wed | §5 Rao–Blackwell, then Q61 and Q74 in §11 | MLE property list from §7.6 |
| Thu | §6 Lehmann–Scheffé, then Q40 and Q78 | Paper 1: university types, NEP 2020 |
| Fri | §7 Maximum likelihood, §8 method of moments, then Q41 and Q57 | Write the carry sheet, §16 |
| Sat | §9 Cramér–Rao; then the full numerical set §13 | Paper 1: RUSA, NIRF, SWAYAM, Shodhganga |
| Sun | §15 Self-test, 60 minutes closed book | Review the error log; fix the top two types |

**Every day without exception:** five multi-statement questions from section 14 — judge each statement true or false and write the reason *before* looking at the options. And every numerical answer in section 13 ends with one check. Those two habits are the week's real content; the theory is what makes them possible.

## Contents

| | Section | |
|---|---|---|
| 1 | What makes an estimator good | theory |
| 2 | Sufficiency | theory |
| 3 | Exponential families | theory |
| 4 | Completeness and ancillarity | theory |
| 5 | The Rao–Blackwell theorem | theory |
| 6 | Lehmann–Scheffé and the UMVUE | theory |
| 7 | Maximum likelihood estimation | theory |
| 8 | Method of moments | theory |
| 9 | Fisher information and Cramér–Rao | theory |
| 10 | The master table | recall target |
| 11 | The six June 2026 questions, worked | — |
| 12 | Practice set A — 40 conceptual questions | step 4 |
| 13 | Practice set B — 25 numerical problems | **step 3** |
| 14 | Practice set C — 35 multi-statement questions | **step 4, five a day** |
| 15 | Sunday self-test | checkpoint |
| 16 | Carry sheet | light slots |

A working rule for every derivation here: read it once, close the page, reproduce it on blank paper, then compare. Reading a derivation and understanding it is not the same as producing it in ninety seconds under pressure, and only the second earns marks.

---

# 1. What makes an estimator good

## 1.1 The setting

A random sample X₁, …, Xₙ comes from a distribution f(x; θ) where θ is unknown. A **statistic** is any function T(X₁, …, Xₙ) that does not involve θ. An **estimator** is a statistic used to guess θ (or some function τ(θ) of it). An **estimate** is the number it produces for a particular sample.

Keep the three words apart. The estimator is a random variable and has a distribution; the estimate is a number and has none.

## 1.2 Unbiasedness

T is **unbiased** for τ(θ) if

E_θ(T) = τ(θ) for every θ in the parameter space.

"For every θ" is the whole content of the definition. An estimator that happens to be right at one value of θ is not unbiased.

**Bias** is b(θ) = E_θ(T) − τ(θ).

## 1.3 Mean squared error — the decomposition to memorise

MSE(T) = E[(T − τ(θ))²] = **Var(T) + [Bias(T)]²**

*Proof.* Write T − τ = (T − E T) + (E T − τ). Square and expand; the cross term is 2(E T − τ)·E(T − E T) = 0. ∎

Two consequences that get examined:

- For an **unbiased** estimator, MSE = Var. This is why, once we restrict to unbiased estimators, "minimum variance" and "minimum MSE" mean the same thing.
- A **biased** estimator can beat an unbiased one on MSE. The MLE of σ² in a normal sample, Σ(Xᵢ − X̄)²/n, has smaller MSE than the unbiased S², despite being biased. Unbiasedness is a convention, not a law of nature.

## 1.4 Consistency

T_n is **consistent** for θ if T_n →ᵖ θ, that is P(|T_n − θ| > ε) → 0 for every ε > 0.

**The sufficient condition you will actually use:** if Bias(T_n) → 0 and Var(T_n) → 0, then MSE → 0 and T_n is consistent. (Convergence in mean square implies convergence in probability, by Chebyshev.)

So X̄ is consistent for μ whenever the variance is finite: it is unbiased and Var(X̄) = σ²/n → 0.

## 1.5 Why we need more than unbiasedness

There are usually infinitely many unbiased estimators. For a sample of size 3 from any distribution with mean μ, all of these are unbiased:

X̄, X₁, (X₁ + X₂)/2, 0.5X₁ + 0.3X₂ + 0.2X₃

They differ enormously in variance. So the programme of this week is: among all unbiased estimators, find the one with the smallest variance — the **UMVUE** (uniformly minimum variance unbiased estimator), "uniformly" meaning smallest for every θ at once.

Two machines deliver it. **Rao–Blackwell** says conditioning on a sufficient statistic never makes things worse. **Lehmann–Scheffé** says that if the sufficient statistic is also complete, the result is uniquely best. Everything in sections 2 to 6 is built to feed those two theorems.

---

# 2. Sufficiency

## 2.1 The idea

A sufficient statistic is a summary of the data that loses nothing about θ. Once you know T, the remaining detail in the sample is noise as far as θ is concerned.

Concretely: toss a coin 10 times and record HTTHHHTHTH. For estimating p, does the *order* matter? No — only the number of heads does. The order is information about the experiment, but not about p. So ΣXᵢ is sufficient and the sequence is not needed.

## 2.2 Definition

T is **sufficient** for θ if the conditional distribution of the sample given T = t does not depend on θ.

**Worked check — Bernoulli.** X₁, …, Xₙ iid Bernoulli(p), T = ΣXᵢ. For any particular sequence x with Σxᵢ = t,

P(X = x | T = t) = P(X = x)/P(T = t) = p^t·(1−p)^(n−t) / [C(n,t) p^t·(1−p)^(n−t)] = 1/C(n,t)

which is free of p. So given the total, every arrangement is equally likely, whatever p is. T is sufficient. ∎

Working from the definition means computing a conditional distribution every time. The factorisation theorem removes that labour.

## 2.3 The factorisation theorem (Fisher–Neyman)

> **T is sufficient for θ if and only if the joint density factorises as**
> **f(x; θ) = g(T(x); θ) · h(x)**
> where g depends on the data only through T, and h does not involve θ at all.

This is the single most used tool in the unit. The recipe is mechanical: write the likelihood, then try to split it into a piece that touches θ and a piece that does not.

## 2.4 Worked examples — do each one yourself before reading on

**(a) Bernoulli(p).**

L = ∏ p^(xᵢ) (1−p)^(1−xᵢ) = p^(Σxᵢ) (1−p)^(n−Σxᵢ) = [p/(1−p)]^(Σxᵢ) (1−p)ⁿ

Everything depends on the data only through Σxᵢ, and h(x) = 1. **T = ΣXᵢ.**

**(b) Poisson(λ).**

L = ∏ exp(−λ) λ^(xᵢ) / xᵢ! = exp(−nλ) λ^(Σxᵢ) · (1/∏xᵢ!)

g(T, λ) = exp(−nλ)λ^T, h(x) = 1/∏xᵢ!. **T = ΣXᵢ.**

**(c) Exponential with rate θ, f = θexp(−θx).**

L = θⁿ exp(−θΣxᵢ)

**T = ΣXᵢ.** Note that the mean is 1/θ, so the same T serves for the mean.

**(d) Normal N(μ, σ²), both unknown.**

L = (2πσ²)^(−n/2) exp[−Σ(xᵢ − μ)²/(2σ²)]

Expand the sum: Σ(xᵢ − μ)² = Σxᵢ² − 2μΣxᵢ + nμ². So the exponent involves the data only through Σxᵢ and Σxᵢ².

**T = (ΣXᵢ, ΣXᵢ²)**, a two-dimensional sufficient statistic. Equivalently (X̄, S²), since each pair is a one-to-one function of the other.

**(e) Normal with σ² known.** Only Σxᵢ survives in the θ-involving part, so **T = ΣXᵢ** and the statistic is one-dimensional. The dimension of the sufficient statistic matches the number of unknown parameters here — which is typical, but not a rule.

**(f) Uniform U(0, θ) — the one that breaks the pattern.**

f(x; θ) = 1/θ on 0 ≤ x ≤ θ. Write it with an indicator:

L = (1/θⁿ) · ∏ I(0 ≤ xᵢ ≤ θ) = (1/θⁿ) · I(x₍ₙ₎ ≤ θ) · I(x₍₁₎ ≥ 0)

The condition "all xᵢ ≤ θ" is exactly "the largest is ≤ θ". So

g(T, θ) = (1/θⁿ) I(x₍ₙ₎ ≤ θ), h(x) = I(x₍₁₎ ≥ 0)

**T = X₍ₙ₎**, the sample maximum.

**This is the key lesson of the uniform family: when the support depends on θ, the sufficient statistic comes from the indicator, not from the algebra.** Nothing about the formula 1/θⁿ involves the data at all.

**(g) Uniform U(θ, θ+1).** The indicators give x₍₁₎ ≥ θ and x₍ₙ₎ ≤ θ+1, so

**T = (X₍₁₎, X₍ₙ₎)**

Two-dimensional, for a single parameter. Remember this one — it is the standard counterexample in section 4.

## 2.5 Minimal sufficiency

The whole sample is always sufficient, trivially. So is any one-to-one function of a sufficient statistic. We want the *coarsest* such summary.

T is **minimal sufficient** if it is a function of every other sufficient statistic.

> **The test (Lehmann–Scheffé criterion):** T is minimal sufficient if, for any two sample points x and y,
> f(x; θ)/f(y; θ) is free of θ **if and only if** T(x) = T(y).

**Worked example — Poisson.**

f(x;λ)/f(y;λ) = λ^(Σxᵢ − Σyᵢ) · (∏yᵢ!/∏xᵢ!)

This is free of λ precisely when Σxᵢ = Σyᵢ. So ΣXᵢ is minimal sufficient.

**Points that get examined**

- A minimal sufficient statistic is not unique: any one-to-one function of one is another. X̄ and ΣXᵢ are both minimal sufficient.
- A complete sufficient statistic is always minimal sufficient. The converse is false — U(θ, θ+1) again.
- The dimension of a minimal sufficient statistic can exceed the number of parameters. In the Cauchy family it equals the whole ordered sample, however large n is: no genuine reduction is possible.

## 2.6 Common traps

1. **Sufficiency is about θ, not about the data.** A statistic sufficient for μ in a normal sample says nothing about σ².
2. **h(x) must be completely free of θ**, including in its support. This is where U(0, θ) catches people: the indicator carries θ.
3. **Sufficiency does not imply unbiasedness or consistency.** X₍ₙ₎ is sufficient for θ in U(0, θ) but biased.
4. The factorisation is not unique; any constant can be shuffled between g and h.

---

> **Reproduce from memory — step 2 of the session.** Write the factorisation theorem, then derive the sufficient statistic for Bernoulli, Poisson, exponential and U(0, θ) with the page closed. All four should take under four minutes.

---

# 3. Exponential families

## 3.1 Why this section exists

Almost every distribution in the syllabus except the uniform belongs to a single family, and membership automatically hands you a complete sufficient statistic. Recognising the form is quicker than any computation.

## 3.2 The one-parameter form

f(x; θ) = **h(x) · c(θ) · exp[w(θ) · t(x)]**

for x in a support that does **not** depend on θ. Then for a random sample,

**T = Σ t(Xᵢ)** is sufficient — and, under a mild condition below, complete.

## 3.3 Putting the standard distributions into the form

| Distribution | h(x) | c(θ) | w(θ) | t(x) | Sufficient statistic |
|---|---|---|---|---|---|
| Bernoulli(p) | 1 | 1 − p | log[p/(1−p)] | x | ΣXᵢ |
| Poisson(λ) | 1/x! | exp(−λ) | log λ | x | ΣXᵢ |
| Exponential(θ) | 1 | θ | −θ | x | ΣXᵢ |
| N(μ, σ² known) | exp(−x²/2σ²) | exp(−μ²/2σ²) | μ/σ² | x | ΣXᵢ |
| N(μ known, σ²) | 1 | 1/σ | −1/2σ² | (x−μ)² | Σ(Xᵢ−μ)² |
| Geometric(p) | 1 | p | log(1−p) | x − 1 | ΣXᵢ |

**Worked conversion — Bernoulli.**

f(x; p) = p^x(1−p)^(1−x) = (1−p)·[p/(1−p)]^x = (1−p)·exp{x·log[p/(1−p)]}

so c(p) = 1 − p, w(p) = log[p/(1−p)] — the **natural parameter**, also called the logit — and t(x) = x. ∎

## 3.4 The k-parameter form

f(x; θ) = h(x) c(θ) exp[Σⱼ₌₁ᵏ wⱼ(θ) tⱼ(x)]

with sufficient statistic (Σt₁(Xᵢ), …, Σt_k(Xᵢ)). The normal with both parameters unknown is the k = 2 case, giving (ΣXᵢ, ΣXᵢ²).

## 3.5 The completeness condition

> The sufficient statistic of an exponential family is **complete** provided the natural parameter space {w(θ) : θ ∈ Θ} contains an open interval (for k parameters, an open k-dimensional rectangle).

For every standard distribution in the syllabus this holds, so in practice: **exponential family ⟹ complete sufficient statistic**. The condition only bites in artificial cases, such as N(θ, θ²), where the two natural parameters are tied together and the parameter space collapses to a curve.

## 3.6 Who is excluded, and why it matters

| Not an exponential family | Reason |
|---|---|
| U(0, θ), U(θ, θ+1) | support depends on θ |
| Cauchy | cannot be written in the form |
| Shifted exponential exp(−(x−θ)), x ≥ θ | support depends on θ |

The uniform and shifted-exponential cases are precisely where the usual machinery misbehaves: the Cramér–Rao bound does not apply, the MLE sits on a boundary, and the sufficient statistic is an order statistic rather than a sum. Examiners use them for exactly that reason.

---

> **Reproduce from memory.** Write the one-parameter exponential form and put Bernoulli and Poisson into it, naming c(θ), w(θ) and t(x) in each. Then list three distributions that are excluded, with the reason.

---

# 4. Completeness and ancillarity

## 4.1 Completeness — the definition

The family of distributions of T is **complete** if

E_θ[g(T)] = 0 for all θ **implies** g(T) = 0 with probability 1.

Read it as: *T admits no non-trivial unbiased estimator of zero.* That is the property we need, because if two different functions of T were both unbiased for the same thing, their difference would be a non-trivial unbiased estimator of zero — and completeness forbids it. Completeness is therefore exactly the uniqueness condition.

## 4.2 Worked proof — Poisson is complete

T = ΣXᵢ ~ Poisson(nλ). Suppose E[g(T)] = 0 for all λ > 0:

Σ over t = 0, 1, 2, … of  g(t)·exp(−nλ)·(nλ)ᵗ/t!  =  0

Multiply by exp(nλ) (which is never zero):

Σ over t = 0, 1, 2, … of  [g(t)·nᵗ/t!]·λᵗ  =  0 for all λ > 0

This is a power series in λ that vanishes identically. A power series is identically zero only if every coefficient is zero, so g(t)nᵗ/t! = 0 for every t, hence g(t) = 0 for every t. ∎

## 4.3 Worked proof — U(0, θ) is complete

T = X₍ₙ₎ has density n tⁿ⁻¹/θⁿ on 0 < t < θ. Suppose E[g(T)] = 0 for all θ > 0:

∫ (0 to θ) g(t) · n tⁿ⁻¹/θⁿ dt = 0  ⟹  ∫ (0 to θ) g(t) tⁿ⁻¹ dt = 0 for all θ > 0

Differentiate both sides with respect to θ (fundamental theorem of calculus):

g(θ) θⁿ⁻¹ = 0 for all θ > 0  ⟹  g(θ) = 0. ∎

Note the technique: for a discrete family, completeness arguments use power series; for a continuous one, they use differentiation under the integral.

## 4.4 The counterexample — U(θ, θ+1) is sufficient but not complete

T = (X₍₁₎, X₍ₙ₎) is sufficient (section 2.4g). Consider the **range**

R = X₍ₙ₎ − X₍₁₎

Since the interval has fixed length 1 whatever θ is, shifting θ shifts both order statistics equally and leaves R unchanged. R therefore has a distribution free of θ, with

E(R) = (n − 1)/(n + 1)

Now set g(T) = R − (n−1)/(n+1). Then E_θ[g(T)] = 0 for every θ, yet g is not identically zero. **Completeness fails.** ∎

This single example answers a family of questions. Commit it.

## 4.5 Ancillary statistics

U is **ancillary** for θ if its distribution does not involve θ. It carries no information about θ on its own.

Examples:
- The range R above, for U(θ, θ+1)
- S² in a normal sample when σ² is known and μ is the parameter of interest
- Any difference Xᵢ − Xⱼ in a location family
- The sample size, in a fixed-design experiment

Sufficiency and ancillarity are opposite poles: a sufficient statistic carries all the information, an ancillary one carries none.

## 4.6 Basu's theorem

> **If T is complete sufficient for θ and U is ancillary, then T and U are independent.**

The power of this is that it proves independence without any joint density calculation.

**Classic application.** In a sample from N(μ, σ²) with σ² known, X̄ is complete sufficient for μ, and S² is ancillary (its distribution involves only σ²). Basu gives **X̄ ⫫ S²** immediately. The usual proof of that independence runs through Helmert's orthogonal transformation and takes a page; Basu does it in a line.

---

> **Reproduce from memory.** State completeness. Prove the Poisson family is complete. Then produce the U(θ, θ+1) counterexample in full, including E(range) = (n−1)/(n+1).

---

# 5. The Rao–Blackwell theorem

## 5.1 Statement

> Let h(X) be an unbiased estimator of τ(θ) with E(h²) < ∞, and let T be sufficient for θ. Define φ(T) = E(h | T). Then
> **(i) φ(T) is a statistic** — it does not involve θ
> **(ii) E[φ(T)] = τ(θ)** — it is unbiased
> **(iii) Var[φ(T)] ≤ Var(h)** for every θ, with equality only if h was already a function of T

## 5.2 Proof

**(i)** Because T is sufficient, the conditional distribution of X given T is free of θ, so the conditional expectation E(h|T) is a function of T alone and contains no unknown parameter. **This is the only place sufficiency is used, and it is indispensable** — without it, E(h|T) would still involve θ and would not be an estimator at all.

**(ii)** By the tower property, E[φ(T)] = E[E(h|T)] = E(h) = τ(θ).

**(iii)** By the law of total variance,

Var(h) = E[Var(h|T)] + Var[E(h|T)] = E[Var(h|T)] + Var[φ(T)]

The first term is an expectation of a variance, hence ≥ 0, so Var(h) ≥ Var[φ(T)]. Equality holds only when Var(h|T) = 0 almost surely, which means h is already determined by T. ∎

## 5.3 What it gives and what it does not

Rao–Blackwell is a **method of improvement**, not of identification. It says conditioning on a sufficient statistic never hurts and usually helps. It does **not** say the result is best — different starting estimators h could in principle give different improved estimators. Completeness is what rules that out, and that is section 6.

## 5.4 Worked example — Poisson, estimating exp(−λ)

τ(λ) = exp(−λ) = P(X = 0). Start from the crude unbiased estimator

h(X₁) = I(X₁ = 0), since E[h] = P(X₁ = 0) = exp(−λ) ✓

Condition on T = ΣXᵢ. The key distributional fact: given ΣXᵢ = t, the vector of individual counts is multinomial, so **X₁ | T = t ~ Binomial(t, 1/n)**. Hence

φ(t) = E[I(X₁ = 0) | T = t] = P(X₁ = 0 | T = t) = (1 − 1/n)ᵗ = ((n−1)/n)ᵗ

So the improved estimator is **((n−1)/n)^(ΣXᵢ)**, and since T is complete, section 6 will tell us this is the UMVUE of exp(−λ).

Compare variances at n = 10, λ = 1: the crude h is a Bernoulli indicator with variance exp(−1)(1 − exp(−1)) ≈ 0.2325; the improved version has variance of order 0.01. The improvement is dramatic, and it came from throwing away nothing but noise.

## 5.5 Worked example — the June 2026 question

Exponential with mean θ. T(X₁) = 1 if X₁ > x₀, else 0. Then

E[T(X₁)] = P(X₁ > x₀) = exp(−x₀/θ)

so T(X₁) is unbiased for exp(−x₀/θ). Rao–Blackwellising on T_S = ΣXᵢ gives the UMVUE **of that same quantity**, exp(−x₀/θ).

> **The rule the question is testing: Rao–Blackwell changes the estimator, never the estimand.** Whatever h was unbiased for, E(h|T) is unbiased for. So read off E(h) first, and the answer follows with no computation at all.

For completeness, the explicit form is φ(t) = (1 − x₀/t)ⁿ⁻¹ for t > x₀ and 0 otherwise — but the exam asked only what it estimates.

---

> **Reproduce from memory.** State and prove Rao–Blackwell in three parts, marking the line where sufficiency is used. Then derive the UMVUE of e^(−λ) from the indicator, including the binomial conditional.

---

# 6. Lehmann–Scheffé and the UMVUE

## 6.1 Statement

> Let T be **complete and sufficient** for θ, and let φ(T) be an unbiased estimator of τ(θ). Then φ(T) is the **unique UMVUE** of τ(θ).

## 6.2 Proof

*Minimum variance.* Let h be any unbiased estimator of τ(θ). By Rao–Blackwell, E(h|T) is unbiased with variance no larger. But E(h|T) is an unbiased function of T, and so is φ(T); their difference d(T) = φ(T) − E(h|T) satisfies E[d(T)] = 0 for all θ. Completeness forces d(T) = 0 almost surely, so E(h|T) = φ(T). Therefore Var[φ(T)] ≤ Var(h) for every unbiased h. ∎

*Uniqueness* is the same completeness argument: two unbiased functions of a complete T must coincide.

**Note what each hypothesis does.** Sufficiency makes E(h|T) a statistic. Completeness makes it unique. Drop completeness and you keep improvement but lose "best" — which is exactly why statement C of Q61 was false.

## 6.3 The two routes to a UMVUE

**Route A — guess and verify.** Find any function of the complete sufficient statistic that is unbiased for τ(θ). Done. This is almost always the faster route in an exam.

**Route B — Rao–Blackwellise.** Start from any crude unbiased estimator, often an indicator based on a single observation, and condition on T. Use this when an unbiased function of T is not obvious — typically when τ(θ) is an awkward function such as exp(−λ) or P(X > x₀).

## 6.4 Worked examples

**(a) Poisson λ.** T = ΣXᵢ is complete sufficient; E(X̄) = λ. **UMVUE = X̄.** (Route A, one line.)

**(b) Bernoulli p.** **UMVUE = X̄.**

**(c) Bernoulli p².** Try T(T−1)/(n(n−1)) where T = ΣXᵢ ~ Bin(n, p). Since E[T(T−1)] = n(n−1)p², this is unbiased, and it is a function of the complete sufficient statistic. **UMVUE = T(T−1)/(n(n−1)).**

**(d) Exponential, rate θ.** T = ΣXᵢ ~ Gamma(n, θ). We need E of some function of T to equal θ. Compute

E(1/T) = ∫ (0 to ∞) (1/t) · θⁿ tⁿ⁻¹ exp(−θt)/Γ(n) dt = θ·Γ(n−1)/Γ(n) = θ/(n − 1)

so E[(n−1)/T] = θ. **UMVUE of θ = (n − 1)/ΣXᵢ**, valid for n ≥ 2.

Contrast the MLE, n/ΣXᵢ, whose expectation is nθ/(n−1). The two differ by the factor n/(n−1) — a clean illustration that the MLE need not be unbiased.

**(e) Exponential, mean θ.** T = ΣXᵢ, E(X̄) = θ. **UMVUE = X̄.** The same distribution gives different answers depending on which parameterisation is asked for; read the question.

**(f) U(0, θ).** T = X₍ₙ₎ is complete sufficient with density n tⁿ⁻¹/θⁿ, so

E(X₍ₙ₎) = ∫ (0 to θ) t · n tⁿ⁻¹/θⁿ dt = nθ/(n+1)

The maximum is biased downward — obviously so, since it can never exceed θ. Correcting:

**UMVUE of θ = ((n+1)/n)·X₍ₙ₎**

**(g) Normal.** (ΣXᵢ, ΣXᵢ²) is complete sufficient. **UMVUE of μ = X̄; UMVUE of σ² = S²** with divisor n − 1.

**(h) Poisson exp(−λ).** From section 5.4, **UMVUE = ((n−1)/n)^(ΣXᵢ)**.

## 6.5 Facts about the UMVUE that appear as true/false statements

- The UMVUE is **unique** when it exists.
- It need **not** attain the Cramér–Rao bound. CRLB attainment is sufficient for being UMVUE, not necessary.
- A UMVUE may not exist at all for some parametric functions.
- The UMVUE is always a function of the complete sufficient statistic.
- If an unbiased estimator attains the CRLB, it is automatically the UMVUE.
- The UMVUE is not necessarily the MLE, and the MLE is not necessarily unbiased.

---

> **Reproduce from memory.** State Lehmann–Scheffé and prove both halves. Then write the UMVUE for λ in Poisson, for θ in exponential under both parameterisations, and for θ in U(0, θ) — the last with the (n+1)/n factor derived, not recalled.

---

# 7. Maximum likelihood estimation

## 7.1 The method

The **likelihood** is the joint density read as a function of the parameter with the data held fixed:

L(θ) = ∏ᵢ f(xᵢ; θ)

The MLE θ̂ is the value of θ maximising L, equivalently maximising ℓ(θ) = log L(θ). The usual route is

∂ℓ/∂θ = 0 (the **likelihood equation**), then check ∂²ℓ/∂θ² < 0

**But the derivative route only works when the maximum is interior and the function is differentiable.** When the support depends on θ, the maximum sits on a boundary and must be found by inspection. Section 7.3 is that case.

## 7.2 Worked examples — the interior cases

**(a) Bernoulli(p).**

ℓ = (Σxᵢ) log p + (n − Σxᵢ) log(1−p)
∂ℓ/∂p = Σxᵢ/p − (n − Σxᵢ)/(1−p) = 0  ⟹  **p̂ = x̄**

**(b) Poisson(λ).**

ℓ = −nλ + (Σxᵢ) log λ − Σ log xᵢ!
∂ℓ/∂λ = −n + Σxᵢ/λ = 0  ⟹  **λ̂ = x̄**

**(c) Exponential, rate θ.**

ℓ = n log θ − θΣxᵢ
∂ℓ/∂θ = n/θ − Σxᵢ = 0  ⟹  **θ̂ = n/Σxᵢ = 1/x̄**

**(d) Normal, both unknown.**

ℓ = −(n/2)log(2πσ²) − Σ(xᵢ−μ)²/(2σ²)

∂ℓ/∂μ = 0 gives **μ̂ = x̄**. Substituting and solving ∂ℓ/∂σ² = 0 gives

**σ̂² = Σ(xᵢ − x̄)²/n** — divisor n, so biased, with E(σ̂²) = ((n−1)/n)σ²

Hold this beside the UMVUE S², divisor n − 1. The June paper asked both, in Q4 and Q37, from the same three data vectors.

## 7.3 The boundary case — U(0, θ)

L(θ) = (1/θⁿ) · I(θ ≥ x₍ₙ₎)

Differentiating is useless: −n/θⁿ⁺¹ is never zero. Instead reason directly. The likelihood is zero for θ < x₍ₙ₎, because such a θ could not have produced the observed maximum. For θ ≥ x₍ₙ₎ it is 1/θⁿ, which **decreases** in θ. So L is maximised at the smallest permissible value:

**θ̂ = X₍ₙ₎**

and E(X₍ₙ₎) = nθ/(n+1) < θ, so the MLE is biased downward. The UMVUE multiplies it by (n+1)/n.

**Draw this likelihood function once.** It climbs vertically at x₍ₙ₎ and then decays — a picture that makes the whole family of uniform questions obvious.

## 7.4 Non-uniqueness

**U(θ, θ+1).** The likelihood is 1 for every θ in [x₍ₙ₎ − 1, x₍₁₎] and 0 outside. Every point of that interval is an MLE, so the MLE is **not unique**.

**Laplace (double exponential).** Maximising −Σ|xᵢ − θ| gives the sample median, which for even n is any point between the two middle observations — again not unique.

## 7.5 The invariance property

> If θ̂ is the MLE of θ, then **g(θ̂) is the MLE of g(θ)** for any function g.

So the MLE of σ is √σ̂², the MLE of exp(−λ) is exp(−x̄), and the MLE of the exponential mean is 1/θ̂ = x̄.

**Invariance does not carry unbiasedness with it.** exp(−x̄) is the MLE of exp(−λ) but is biased; the UMVUE is the quite different ((n−1)/n)^(Σxᵢ).

## 7.6 Properties — the list to memorise

**Holds, under regularity conditions**

| Property | Statement |
|---|---|
| Function of sufficient statistic | always, since L factorises through T |
| Invariance | MLE of g(θ) is g(θ̂) |
| Consistency | θ̂ →ᵖ θ |
| Asymptotic normality | √n(θ̂ − θ) → N(0, 1/I(θ)) |
| Asymptotic efficiency | attains the Cramér–Rao bound in the limit |

**Does not hold**

| Property | Counterexample |
|---|---|
| Unbiasedness | σ̂² in the normal; X₍ₙ₎ in U(0,θ); n/ΣXᵢ for the exponential rate |
| Uniqueness | U(θ, θ+1); Laplace with even n |
| Existence | likelihood may be unbounded, e.g. a two-component normal mixture |
| Attaining CRLB in finite samples | only asymptotically, in general |

## 7.7 Regularity conditions — why they appear in questions

The asymptotic results and the Cramér–Rao bound require:

1. The support of f does not depend on θ
2. θ is interior to the parameter space, not on its boundary
3. f is twice differentiable in θ and differentiation under the integral sign is valid
4. The Fisher information is finite and non-zero

**U(0, θ) violates condition 1**, which is why its MLE converges at rate n rather than √n, is not asymptotically normal, and has variance below what the CRLB would have predicted. When a question offers a uniform distribution and asks about CRLB or asymptotic normality, the answer is usually "the conditions fail".

---

# 8. Method of moments

The oldest method, and the easiest marks when it appears.

**Procedure.** Equate the first k sample moments to the corresponding population moments and solve for the k parameters.

m₁′ = x̄ = E(X),  m₂′ = (1/n)Σxᵢ² = E(X²), …

**Worked examples**

| Distribution | Equation | MoM estimator |
|---|---|---|
| Poisson(λ) | x̄ = λ | λ̂ = x̄ |
| Exponential, mean θ | x̄ = θ | θ̂ = x̄ |
| Exponential, rate θ | x̄ = 1/θ | θ̂ = 1/x̄ |
| U(0, θ) | x̄ = θ/2 | θ̂ = 2x̄ |
| N(μ, σ²) | x̄ = μ; (1/n)Σxᵢ² = σ² + μ² | μ̂ = x̄, σ̂² = Σ(xᵢ−x̄)²/n |
| Gamma(α, β) | x̄ = α/β; s² = α/β² | β̂ = x̄/s², α̂ = x̄²/s² |

**Properties worth knowing**

- Always consistent, by the weak law of large numbers
- Generally **less efficient** than the MLE
- Not necessarily a function of a sufficient statistic — for U(0, θ) it gives 2X̄, which ignores X₍ₙ₎ entirely and can even produce an estimate smaller than an observed value
- Can give estimates outside the parameter space
- Computationally trivial, which is its only real advantage

The U(0, θ) comparison is the standard exam illustration: MoM gives 2X̄, MLE gives X₍ₙ₎, UMVUE gives ((n+1)/n)X₍ₙ₎, and the three have very different variances.

---

> **Reproduce from memory.** Derive the MLE for Bernoulli, Poisson, exponential and N(μ, σ²). Do U(0, θ) by inspection and sketch its likelihood. Finish with the five properties that hold and the three that do not.

---

# 9. Fisher information and the Cramér–Rao inequality

## 9.1 Fisher information

The **score** is U(θ) = ∂/∂θ log f(X; θ). Under regularity, E[U(θ)] = 0.

**Fisher information** is the variance of the score:

I(θ) = E[(∂/∂θ log f(X; θ))²] = **−E[∂²/∂θ² log f(X; θ)]**

The second form is almost always easier to compute — differentiate twice and take an expectation, with no squaring.

**Additivity.** For a random sample of size n, I_n(θ) = n·I(θ). Information accumulates linearly with sample size, which is the formal reason estimator variances fall like 1/n.

## 9.2 Worked computations

**(a) Bernoulli(p).**

log f = x log p + (1−x) log(1−p)
∂/∂p = x/p − (1−x)/(1−p)
∂²/∂p² = −x/p² − (1−x)/(1−p)²
−E[∂²/∂p²] = p/p² + (1−p)/(1−p)² = 1/p + 1/(1−p) = **1/[p(1−p)]**

**(b) Poisson(λ).**

log f = −λ + x log λ − log x!;  ∂²/∂λ² = −x/λ²;  −E = λ/λ² = **1/λ**

**(c) Exponential, rate θ.**

log f = log θ − θx;  ∂²/∂θ² = −1/θ²;  **I(θ) = 1/θ²**

**(d) Normal, mean μ with σ² known.**

log f = −(x−μ)²/(2σ²) + const;  ∂²/∂μ² = −1/σ²;  **I(μ) = 1/σ²**

**(e) Normal, variance.** Treating σ² as the parameter, **I(σ²) = 1/(2σ⁴)**.

Notice the pattern: in each case I(θ) is the reciprocal of the asymptotic variance of the MLE. That is the content of asymptotic efficiency.

## 9.3 The Cramér–Rao inequality

> For any unbiased estimator T of τ(θ), under the regularity conditions,
> **Var(T) ≥ [τ′(θ)]² / (n·I(θ))**

For τ(θ) = θ the numerator is 1 and the bound is the familiar 1/(nI(θ)).

**Equality condition.** The bound is attained if and only if the score factorises as

∂/∂θ log L = k(θ)·[T − τ(θ)]

for some function k not involving the data. This happens exactly in exponential families with T linear in the natural sufficient statistic.

**Efficiency** of an unbiased estimator is eff(T) = CRLB/Var(T), lying between 0 and 1. An estimator with eff = 1 is **efficient**.

## 9.4 Worked example — Poisson

I(λ) = 1/λ, so the bound for unbiased estimators of λ is λ/n. And Var(X̄) = λ/n exactly. So X̄ attains the bound, is efficient, and is therefore the UMVUE — confirming by a second route what Lehmann–Scheffé gave in section 6.

## 9.5 Worked example — where the bound fails

For U(0, θ) the support depends on θ, so the CRLB does not apply. The UMVUE ((n+1)/n)X₍ₙ₎ has variance

Var = θ²/[n(n+2)]

which decreases like 1/n², far faster than the 1/n rate the bound would suggest. **An estimator "beating" the Cramér–Rao bound is always a sign that the regularity conditions have failed**, never that the mathematics is wrong.

## 9.6 Relationships to keep straight

- Attaining the CRLB ⟹ UMVUE. The converse is false.
- CRLB is a bound for **unbiased** estimators only. Biased estimators can have smaller variance, and often smaller MSE.
- The bound involves n·I(θ) because information is additive.
- MLEs attain it **asymptotically**, not in finite samples.

---

> **Reproduce from memory.** Write both expressions for Fisher information, compute I(θ) for Bernoulli, Poisson and exponential, state the Cramér–Rao bound with its equality condition, and say in one sentence why U(0, θ) escapes it.

---

# 10. The master table

Reproducing this from memory is Sunday's checkpoint. Build it in pieces across the week.

| Distribution | Complete sufficient statistic | MLE | UMVUE | Notes |
|---|---|---|---|---|
| Bernoulli(p) | ΣXᵢ | X̄ | X̄ | attains CRLB |
| Binomial(n known, p) | ΣXᵢ | X̄/n | X̄/n | |
| Poisson(λ) | ΣXᵢ | X̄ | X̄ | attains CRLB |
| Poisson, estimating exp(−λ) | ΣXᵢ | exp(−X̄) | ((n−1)/n)^(ΣXᵢ) | MLE biased |
| Geometric(p) | ΣXᵢ | 1/X̄ | — | |
| N(μ, σ² known) | ΣXᵢ | X̄ | X̄ | attains CRLB |
| N(μ known, σ²) | Σ(Xᵢ−μ)² | Σ(Xᵢ−μ)²/n | Σ(Xᵢ−μ)²/n | |
| N(μ, σ²) both unknown | (ΣXᵢ, ΣXᵢ²) | X̄, Σ(Xᵢ−X̄)²/n | X̄, S² | divisors n vs n−1 |
| Exponential, rate θ | ΣXᵢ | n/ΣXᵢ | (n−1)/ΣXᵢ | MLE biased by n/(n−1) |
| Exponential, mean θ | ΣXᵢ | X̄ | X̄ | |
| Exponential, est. exp(−x₀/θ) | ΣXᵢ | exp(−x₀/X̄) | (1 − x₀/T)ⁿ⁻¹ | T = ΣXᵢ |
| U(0, θ) | X₍ₙ₎ | X₍ₙ₎ | ((n+1)/n)X₍ₙ₎ | CRLB inapplicable |
| U(θ, θ+1) | (X₍₁₎, X₍ₙ₎) | not unique | — | sufficient, **not complete** |
| Gamma(α known, β) | ΣXᵢ | α/X̄ | (nα−1)/ΣXᵢ | |

**Fisher information**

| Distribution | I(θ) |
|---|---|
| Bernoulli(p) | 1/[p(1−p)] |
| Poisson(λ) | 1/λ |
| Exponential(θ) | 1/θ² |
| N(μ), σ² known | 1/σ² |
| N(σ²), μ known | 1/(2σ⁴) |

---

# 11. The six June 2026 questions, worked

**Q40 — exponential, f(x,θ) = θexp(−θx).** Correct: **(C), A, B and C only.**

B is true: (n−1)/Σxᵢ is the UMVUE of θ (section 6.4d). C is true: Σxᵢ is sufficient. D is false: ΣXᵢ ~ Gamma(**n**, θ), not Gamma(1, θ) — Gamma(1, θ) is a single exponential. A is, strictly, false: the MLE of θ is n/Σxᵢ, not Σxᵢ/n. Since only options (B) and (C) contain both B and C, and D is false, (C) is the only possible answer. **Technique: when a multi-statement question appears to have no perfect option, eliminate on the statement you are surest about.**

**Q41 — Type II censoring, first r order statistics from exponential with mean θ.** Correct: **(D), T₁ + (n−r)T₂.**

The total time on test is Σᵢ₌₁ʳ X₍ᵢ₎ + (n−r)X₍ᵣ₎ — the failures contribute their own times, and each of the n−r survivors contributes X₍ᵣ₎. Its expectation is rθ, so dividing by r gives an unbiased estimator. Check it at r = n: the correction vanishes and the estimator becomes X̄, as it must.

**Q57 — shifted exponential, f = exp(−(x−θ)), x ≥ θ.** Correct: **(A), A and B only.**

E(X) = θ + 1 and V(X) = 1. So X̄ →ᵖ θ+1 (A true; D false, the limit is θ+1 not θ). V(X̄) = 1/n, not n (C false). The minimum of n such variables has density n exp(−n(y−θ)) (B true) — the minimum of n exponentials is exponential at n times the rate.

**Q61 — Rao–Blackwell.** Correct: **(D), A, B and D only.**

A and B are the theorem. D is true: sufficiency is exactly what makes E(h|T) free of θ. C is false — uniqueness as UMVUE needs **completeness**, which the question never assumes.

**Q74 — E[T(X₁)|T_S] where T(x₁) = I(X₁ > x₀).** Correct: **(C), exp(−x₀/θ).**

E[T(X₁)] = P(X₁ > x₀) = exp(−x₀/θ). Rao–Blackwell preserves the estimand.

**Q78 — Poisson, which are unbiased for λ.** Correct: **(D), A, B and D only.**

Mean and variance both equal λ, so X̄ (A) and S² (B) are unbiased. X̄ + S² has expectation 2λ (C false). Weights summing to one preserve unbiasedness, so 0.3X̄ + 0.7S² works (D). **Any aX̄ + (1−a)S² is unbiased for λ** — the question could use any coefficients.

---

# 12. Practice set A — 40 conceptual questions

These test whether you **recognise** the right idea. They are step 4 material, not step 3 — recognition was already your strongest tier in June, so do not let these crowd out sections 13 and 14. Answers covered, 40 questions in 45 minutes.

**Sufficiency**

**1.** A statistic T is sufficient for θ if:
(A) T is unbiased (B) the conditional distribution of the sample given T is free of θ (C) T has minimum variance (D) T is consistent
→ **(B)**.

**2.** For a random sample from N(μ, σ²) with both unknown, a sufficient statistic is:
(A) X̄ (B) S² (C) (ΣXᵢ, ΣXᵢ²) (D) X₍ₙ₎
→ **(C)**. Two unknown parameters, two-dimensional sufficient statistic.

**3.** For U(0, θ) the sufficient statistic is:
(A) X̄ (B) ΣXᵢ (C) X₍ₙ₎ (D) X₍₁₎
→ **(C)**. It comes from the indicator I(x₍ₙ₎ ≤ θ), not from the algebra.

**4.** The factorisation theorem states that T is sufficient if and only if:
(A) f(x;θ) = g(T;θ)h(x) (B) f(x;θ) = g(T)h(θ) (C) E(T) = θ (D) T is complete
→ **(A)**.

**5.** For U(θ, θ+1) the minimal sufficient statistic is:
(A) X̄ (B) X₍₁₎ (C) X₍ₙ₎ (D) (X₍₁₎, X₍ₙ₎)
→ **(D)**. One parameter, two-dimensional statistic — perfectly possible.

**6.** Which is **not** necessarily true of a sufficient statistic?
(A) it is unbiased (B) it exists (C) the whole sample is one (D) any one-to-one function of it is sufficient
→ **(A)**. X₍ₙ₎ is sufficient for θ in U(0,θ) but biased.

**7.** For a sample from the Cauchy distribution, the minimal sufficient statistic is:
(A) X̄ (B) the sample median (C) the full set of order statistics (D) ΣXᵢ²
→ **(C)**. No genuine reduction is possible.

**8.** If T is sufficient for θ, then the MLE:
(A) equals T (B) is a function of T (C) is unrelated to T (D) does not exist
→ **(B)**. The likelihood depends on the data only through T.

**Exponential families and completeness**

**9.** Which distribution is **not** a member of the exponential family?
(A) Poisson (B) Bernoulli (C) U(0, θ) (D) exponential
→ **(C)**. Its support depends on θ.

**10.** The natural parameter of the Bernoulli family is:
(A) p (B) 1 − p (C) log[p/(1−p)] (D) p²
→ **(C)**.

**11.** Completeness of T means:
(A) E[g(T)] = 0 for all θ implies g(T) = 0 a.s. (B) T is unbiased (C) T is minimal (D) Var(T) = 0
→ **(A)**.

**12.** A statistic that is sufficient but not complete arises in:
(A) Poisson (B) U(θ, θ+1) (C) Bernoulli (D) normal with σ² known
→ **(B)**.

**13.** For U(θ, θ+1), the range X₍ₙ₎ − X₍₁₎ is:
(A) sufficient (B) complete (C) ancillary (D) the MLE
→ **(C)**. Its distribution is free of θ.

**14.** Every complete sufficient statistic is:
(A) minimal sufficient (B) unbiased (C) efficient (D) ancillary
→ **(A)**. The converse fails.

**15.** Basu's theorem concerns the independence of:
(A) two sufficient statistics (B) a complete sufficient statistic and an ancillary statistic (C) X̄ and the median (D) MLE and UMVUE
→ **(B)**.

**16.** In N(μ, σ²) with σ² known, Basu's theorem shows immediately that:
(A) X̄ and S² are independent (B) X̄ is unbiased (C) S² is complete (D) X̄ is efficient
→ **(A)**.

**Rao–Blackwell and UMVUE**

**17.** Rao–Blackwell requires T to be:
(A) complete (B) sufficient (C) unbiased (D) minimal
→ **(B)**. Sufficiency alone; completeness is needed only for Lehmann–Scheffé.

**18.** E(h|T) has variance:
(A) larger than Var(h) (B) no larger than Var(h) (C) equal to Var(h) always (D) zero
→ **(B)**.

**19.** Lehmann–Scheffé needs T to be:
(A) sufficient only (B) complete only (C) complete and sufficient (D) ancillary
→ **(C)**.

**20.** The UMVUE, when it exists, is:
(A) unique (B) one of many (C) always the MLE (D) always unbiased for every parameter
→ **(A)**.

**21.** The UMVUE of λ in Poisson(λ) is:
(A) S² (B) X̄ (C) X₍ₙ₎ (D) ΣXᵢ
→ **(B)**.

**22.** The UMVUE of θ in U(0, θ) is:
(A) X₍ₙ₎ (B) ((n+1)/n)X₍ₙ₎ (C) 2X̄ (D) nX₍ₙ₎
→ **(B)**.

**23.** The UMVUE of θ for exponential with pdf θexp(−θx) is:
(A) X̄ (B) 1/X̄ (C) (n−1)/ΣXᵢ (D) n/ΣXᵢ
→ **(C)**.

**24.** The UMVUE of exp(−λ) in a Poisson sample is:
(A) exp(−X̄) (B) ((n−1)/n)^(ΣXᵢ) (C) 1/X̄ (D) I(X₁ = 0)
→ **(B)**. Option (A) is the MLE and is biased; (D) is the crude unbiased estimator you Rao–Blackwellise.

**25.** If an unbiased estimator attains the Cramér–Rao bound then it is:
(A) the UMVUE (B) biased (C) inconsistent (D) the MLE
→ **(A)**.

**26.** Rao–Blackwellising an estimator unbiased for τ(θ) gives an estimator unbiased for:
(A) θ (B) τ(θ) (C) 1/τ(θ) (D) anything
→ **(B)**. The estimand never changes.

**Maximum likelihood**

**27.** The MLE of θ in U(0, θ) is:
(A) 2X̄ (B) X₍ₙ₎ (C) X₍₁₎ (D) X̄
→ **(B)**, found by inspection, not differentiation.

**28.** The MLE of σ² in N(μ, σ²) with both unknown is:
(A) Σ(Xᵢ−X̄)²/(n−1) (B) Σ(Xᵢ−X̄)²/n (C) Σ(Xᵢ−μ)²/n (D) S²
→ **(B)**, divisor n.

**29.** MLEs are always:
(A) unbiased (B) unique (C) functions of a sufficient statistic (D) efficient in finite samples
→ **(C)**.

**30.** The invariance property states that the MLE of g(θ) is:
(A) g(θ̂) (B) E[g(θ̂)] (C) g(E θ̂) (D) undefined
→ **(A)**.

**31.** For U(θ, θ+1) the MLE is:
(A) X₍₁₎ (B) X₍ₙ₎ (C) not unique (D) X̄
→ **(C)**. Any value in [X₍ₙ₎ − 1, X₍₁₎].

**32.** √n(θ̂ − θ) converges in distribution to:
(A) N(0, I(θ)) (B) N(0, 1/I(θ)) (C) χ²₁ (D) N(θ, 1)
→ **(B)**.

**33.** The MLE of θ for exponential with rate θ has expectation:
(A) θ (B) nθ/(n−1) (C) (n−1)θ/n (D) θ/n
→ **(B)**, hence biased upward.

**34.** The MLE of the exponential mean 1/θ is:
(A) 1/X̄ (B) X̄ (C) n/ΣXᵢ (D) ΣXᵢ
→ **(B)**, by invariance applied to θ̂ = 1/X̄.

**Method of moments and Cramér–Rao**

**35.** The method-of-moments estimator of θ in U(0, θ) is:
(A) X₍ₙ₎ (B) 2X̄ (C) X̄ (D) ((n+1)/n)X₍ₙ₎
→ **(B)**, and it ignores the sample maximum entirely.

**36.** Method-of-moments estimators are always:
(A) unbiased (B) consistent (C) efficient (D) functions of sufficient statistics
→ **(B)**, by the weak law of large numbers.

**37.** Fisher information can be written as:
(A) E[∂²/∂θ² log f] (B) −E[∂²/∂θ² log f] (C) E[∂/∂θ log f] (D) Var(θ̂)
→ **(B)**.

**38.** For a sample of size n, the total information is:
(A) I(θ) (B) nI(θ) (C) I(θ)/n (D) n²I(θ)
→ **(B)**.

**39.** Fisher information for Bernoulli(p) is:
(A) p(1−p) (B) 1/[p(1−p)] (C) 1/p (D) n/p
→ **(B)**.

**40.** An unbiased estimator with variance smaller than the Cramér–Rao bound indicates:
(A) an error in arithmetic (B) that the regularity conditions fail (C) the estimator is biased (D) the bound is wrong
→ **(B)**. U(0, θ) is the standard instance.

---

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

# 15. Sunday self-test — 60 minutes, closed book

## Part A — the master table (20 minutes, 40 marks)

Reproduce, for each of these ten distributions, the complete sufficient statistic, the MLE and the UMVUE: Bernoulli(p), Poisson(λ), N(μ, σ² known), N(μ known, σ²), N(μ, σ²) both unknown, exponential with rate θ, exponential with mean θ, U(0, θ), U(θ, θ+1), geometric(p).

One mark per correct cell. **Below 32, repeat Thursday's session before starting week 2.**

## Part B — written answers (25 minutes)

1. State the factorisation theorem and use it to find the sufficient statistic for U(0, θ). Explain why differentiating the likelihood is useless here.
2. Give a statistic that is sufficient but not complete, and prove that completeness fails.
3. Prove that E(h|T) is unbiased whenever h is, and state precisely where sufficiency is used in the Rao–Blackwell theorem.
4. The MLE of θ in exponential(θ) is n/ΣXᵢ. Show it is biased and give the unbiased version.
5. T(X₁) = I(X₁ > x₀) in an exponential sample with mean θ. What is E(h|T_S) the UMVUE of, and under what extra condition is it unique?
6. Compute Fisher information for Poisson(λ) and state the Cramér–Rao bound for unbiased estimators of λ. Is it attained? By what?

## Part C — the two weak formats (15 minutes)

Ten numerical problems from section 13 and five multi-statement questions from section 14, both fresh — not ones you
worked earlier in the week. Mark the numerical answers only if you also wrote the check; an unchecked answer scores zero,
because an unchecked answer is what produced 4/21 in June.

## After the test

Log every error by **type** on the week 1 page: wrong quantity reported, missing term, degrees of freedom, sign, pure recall gap. If one type appears three times or more, that is your first target in week 2, ahead of any new topic.

---

# 16. Carry sheet — week 1

Copy this onto one side of paper in your own hand. Handwriting it is part of the method; a printed copy does not stick the same way.

**Four definitions**
Sufficient — conditional distribution of the sample given T is free of θ · Minimal sufficient — a function of every other sufficient statistic · Complete — E[g(T)] = 0 for all θ forces g ≡ 0 · Ancillary — distribution free of θ

**Factorisation** f(x;θ) = g(T;θ)·h(x), with h completely free of θ including its support

**Rao–Blackwell** needs sufficiency → unbiased, variance no larger
**Lehmann–Scheffé** needs completeness too → unique UMVUE
**Basu** complete sufficient ⫫ ancillary

**MLE** function of sufficient statistic · invariant · consistent · asymptotically normal and efficient — but **not** necessarily unbiased, unique or existent

**MLE vs UMVUE, where they differ**
σ²: divisor n vs n−1 · exponential rate: n/ΣXᵢ vs (n−1)/ΣXᵢ · U(0,θ): X₍ₙ₎ vs ((n+1)/n)X₍ₙ₎

**CRLB** Var(T) ≥ [τ′(θ)]²/(nI(θ)), I(θ) = −E[∂²/∂θ² log f], I_n = nI
Attained ⟹ UMVUE. Not attained does **not** mean not UMVUE. Fails entirely when the support depends on θ.

**The counterexample to quote** U(θ, θ+1): (X₍₁₎, X₍ₙ₎) is sufficient, the range is ancillary with mean (n−1)/(n+1), so completeness fails.
