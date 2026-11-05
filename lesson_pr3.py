#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 3.3 — Conditional expectation, total variance and mixtures (probability-t3).

First lesson of the probability module, which is the largest uncovered block in the syllabus:
10 questions and 20 marks in June 2026 with no lessons at all, 4 answered correctly.

PYQ anchor. Q45 (WRONG, marked A): X ~ Exponential with mean 1/λ and Y | X = x ~ Poisson(x);
Var(Y) = E(X) + Var(X) = 1/λ + 1/λ² = (λ + 1)/λ², option D. The marked option A was
λ(λ + 1)/λ², a factor of λ too large. Worked in full in section 6.

Q45 showed ZERO variants. Nine of the nineteen tagged to Q46 are conditional-expectation and
mixture items that plainly belong to Q45, and were retagged on 2026-11-03 — the sixth such
misfiling found in this project and the second that rescued a question with no practice
material. Those nine are: the law of total variance; E(Y) when Y|X ~ Poisson(X); Poisson mixed
over a Gamma mean; the variance of an exponential; the variance of any Poisson mixture;
what E(Y|X) is; E(Y|X) under independence; Binomial(n, X) with X ~ Beta(a, b); and Var(Y) when
Y|X ~ N(X,1) with X ~ N(0, σ²). All nine are taught here and all nine are in the pool.

No explore scene: src/30-viz.js has no visualisation for mixtures or overdispersion. One
would serve this topic and the two distribution topics; it is not built yet.

Writes seed/lesson_pr3.json and seed/probability_t3_mastery.json.
"""
import json, io, os, re

OUT = "seed/lesson_pr3.json"
POOL = "seed/probability_t3_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Settle what a conditional expectation actually is, because the whole topic turns on it being a random variable.",
 "ask": {
  "q": "E(Y) is a number. Is E(Y | X) a number?",
  "nudge": "It depends on X. And X is not a number — it is a random variable."},
 "body": [
  "This topic is about quantities that arrive in two stages. A machine is chosen, then it produces defects. A patient's susceptibility is drawn, then they fall ill or not. A claim rate is drawn, then claims arrive.",
  "Two-stage structures are everywhere, and they have a characteristic consequence: the resulting variability is larger than either stage alone would suggest, because it combines the variability WITHIN a stage with the variability BETWEEN stages. The law of total variance is the exact bookkeeping of that split.",
  "The one idea that makes all of it work is that E(Y | X) is itself a random variable — a function of X — and so has its own mean and its own variance. Once that lands, every formula here follows.",
  "Four checks. One on that idea, one on the identity that connects the two stages, and two on the standard distributions the examples use."],
 "items": [
  {"ask": "Is E(Y | X) a number or a random variable?",
   "recall": "A random variable. It is a function of X, so it varies as X varies.",
   "refresh": [
    "E(Y | X = x) is a number: the mean of Y among the cases where X took the value x. But E(Y | X), with X left unspecified, is the rule that maps each x to that number — and since X is random, so is the result.",
    "That is why it makes sense to write E[E(Y | X)] and Var[E(Y | X)]. You are taking the mean and the variance of a random variable, in the ordinary way.",
    "A practice question asks exactly 'E(Y | X) is:' and the answer is 'a random variable, a function of X'. It looks like a triviality and it is the key to the topic."]},
  {"ask": "State the identity connecting E(Y) to E(Y | X).",
   "recall": "E(Y) = E[E(Y | X)] — the tower property, also called the law of total expectation.",
   "refresh": [
    "Average Y within each value of X, then average those averages, weighting by how likely each x is. You recover the overall mean.",
    "So if Y | X ~ Poisson(X), then E(Y | X) = X and therefore E(Y) = E(X). One line, and it answers one of the practice questions outright.",
    "The variance has no such simple identity — averaging the conditional variances is NOT the variance, and the gap between them is what section 3 is about."]},
  {"ask": "For a Poisson random variable with parameter θ, what are the mean and the variance?",
   "recall": "Both equal θ.",
   "refresh": [
    "Mean equal to variance is the Poisson's signature, and it is why the Poisson is the baseline against which 'overdispersion' is defined.",
    "So if Y | X ~ Poisson(X) then E(Y | X) = X and Var(Y | X) = X — the same quantity in both roles, which makes these mixtures unusually clean to compute.",
    "Real count data is usually MORE variable than a Poisson. Section 7 shows that mixing a Poisson is one natural reason why."]},
  {"ask": "For an exponential distribution with mean 1/λ, what is the variance?",
   "recall": "1/λ².",
   "refresh": [
    "The exponential's standard deviation equals its mean, so variance is the square of the mean: (1/λ)² = 1/λ².",
    "A practice question asks this directly, and it is also half of June 2026 Q45 — where the answer is E(X) + Var(X) = 1/λ + 1/λ².",
    "Mind the parameterisation. Written as λe^(−λx) the mean is 1/λ; written as (1/θ)e^(−x/θ) the mean is θ. Read which one a question uses before substituting."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Two sources of variability, not one",
 "objective": "See why the total variance splits into a within part and a between part before any algebra.",
 "body": [
  "Suppose you are told the average number of defects per batch is 3.2. How variable is it? The answer depends on something the average does not reveal: whether all batches are alike.",
  "If every batch comes off the same machine running at rate 3.2, the variability is whatever that one machine produces. But if some batches come off a careful machine at rate 2 and others off a rough one at rate 5, there are two sources of variability stacked on each other — the scatter each machine produces on its own, and the swing between machines.",
  "Both contribute, and they contribute additively. That is the law of total variance: the average of the within-machine variances, plus the variance of the machine averages. Neither term alone is the answer and neither can be ignored.",
  "The practical consequence is that ignoring the second term understates the variability — often badly. A model fitted as though there were one homogeneous population will produce intervals that are too narrow and will be surprised more often than it predicts."],
 "scenario": {
  "teaser": "An insurer prices a policy on the average claim rate and is repeatedly surprised by bad years.",
  "title": "The average was right and the reserves were wrong",
  "body": [
   "A general insurer writes motor policies. Claims from a single policyholder arrive roughly as a Poisson process, and the portfolio's average is one claim per policy per year. The actuary reserves on that basis, treating total claims as Poisson with the portfolio mean.",
   "The average turns out to be right. The variability does not. Bad years are worse and more frequent than the Poisson model allows, and reserves set from it are breached more often than the stated probability.",
   "The missing ingredient is that policyholders are not alike. Each has their own claim rate — some drive carefully, some do not — and that rate is itself a random draw from the population. So claims arise in two stages: draw a rate, then draw claims at that rate.",
   "The law of total variance says the portfolio variance is the average individual variance PLUS the variance of the individual rates. The Poisson model captured the first term and discarded the second, so it understated the variance by exactly the amount of heterogeneity in the population.",
   "This has a name. A Poisson whose rate is itself random always has variance greater than its mean — overdispersion — and the classical result is that mixing a Poisson over a Gamma-distributed rate produces a negative binomial, which is why insurers model claim counts with a negative binomial rather than a Poisson. Section 7 derives it.",
   "Note that no amount of data on the AVERAGE would have revealed the problem. The mean is the same under both models. Only the variance distinguishes them, which is why the decomposition is worth knowing rather than merely being able to quote."],
  "q": "Why did the Poisson model get the mean right and the variance wrong?",
  "answer": "Because the tower property makes the mean insensitive to the heterogeneity: E(Y) = E[E(Y|X)] = E(X), so the portfolio mean is the average rate whether or not rates vary. The variance has no such property — it picks up both E[Var(Y|X)] and Var[E(Y|X)], and the Poisson model silently set the second term to zero. Heterogeneity in the population affects the variance and leaves the mean untouched, so a model can be calibrated correctly on averages and still be badly wrong about risk."},
 "ask": {
  "q": "If every policyholder had exactly the same claim rate, what would Var[E(Y | X)] be, and what would the law of total variance reduce to?",
  "nudge": "A random variable that takes only one value has what variance?"}})

S.append({
 "kind": "theory", "id": "s2", "mins": 9,
 "title": "The two laws, and where the second term comes from",
 "objective": "State both identities precisely and see why the variance needs a second term when the mean does not.",
 "blocks": [
  {"t": "def", "h": "Conditional expectation as a random variable",
   "body": "E(Y | X = x) is a number for each x. The map x ↦ E(Y | X = x), evaluated at the random X, is the random variable E(Y | X). It is a function of X and of nothing else, so it carries only the information X carries. Everything in this topic follows from taking that seriously."},
  {"t": "formula", "h": "The tower property",
   "body": "E(Y) = E[ E(Y | X) ]\nAverage within each value of X, then average over X. Also written as the law of total expectation, and for a discrete X it is just E(Y) = Σ E(Y | X = x) P(X = x) — a weighted average of conditional means."},
  {"t": "formula", "h": "The law of total variance",
   "body": "Var(Y) = E[ Var(Y | X) ]  +  Var[ E(Y | X) ]\nThe first term is the average variability WITHIN a value of X; the second is the variability BETWEEN the conditional means. Both are non-negative, so the total is at least as large as either."},
  {"t": "step", "h": "Where it comes from, in four lines",
   "body": "Write Var(Y) = E(Y²) − [E(Y)]² and apply the tower property to each piece.\n1. E(Y²) = E[E(Y² | X)] = E[Var(Y | X) + (E(Y | X))²], using Var = E(square) − (mean)² conditionally.\n2. [E(Y)]² = (E[E(Y | X)])², again by the tower property.\n3. Subtracting: Var(Y) = E[Var(Y|X)] + E[(E(Y|X))²] − (E[E(Y|X)])².\n4. The last two terms are exactly Var[E(Y | X)]. Done."},
  {"t": "def", "h": "Why the mean needs no second term and the variance does",
   "body": "Expectation is linear, so averaging conditional averages recovers the overall average with nothing left over. Variance is not linear — it involves a square — and squaring does not commute with averaging. The discrepancy is precisely the variance of the conditional means, which is the second term. That is the whole structural reason the two laws look different."},
  {"t": "step", "h": "The independence case, as a check",
   "body": "If X and Y are independent, E(Y | X) = E(Y), a constant. Then Var[E(Y | X)] = 0 and E[Var(Y | X)] = Var(Y), so the law reduces to Var(Y) = Var(Y) — true and empty. The second term is therefore a direct measure of how much X tells you about Y: it is zero exactly when the conditional mean does not move with X. A practice question asks what E(Y | X) equals under independence, and the answer is E(Y)."}],
 "table": {
  "caption": "Standard two-stage models. In each, the mixing makes the marginal more variable than the conditional family alone would allow.",
  "head": ["Y given X", "X distributed as", "Marginal Y is", "Var(Y)"],
  "rows": [
   ["Poisson(X)", "Exponential, mean 1/λ", "geometric-type", "1/λ + 1/λ²"],
   ["Poisson(X)", "Gamma", "negative binomial", "E(X) + Var(X)"],
   ["Binomial(n, X)", "Beta(a, b)", "beta-binomial", "larger than binomial"],
   ["N(X, 1)", "N(0, σ²)", "N(0, 1 + σ²)", "1 + σ²"],
   ["any", "degenerate (constant)", "the conditional family itself", "E[Var(Y|X)] only"]]},
 "flow": {
  "title": "Computing a variance in a two-stage model",
  "alt": "Flow chart for applying the law of total variance",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "Y depends on a random X", "kind": "start"},
   {"id": "b", "r": 1, "c": 0, "label": "Write E(Y | X) as a function of X", "kind": "step"},
   {"id": "c", "r": 1, "c": 2, "label": "Write Var(Y | X) as a function of X", "kind": "step"},
   {"id": "d", "r": 2, "c": 0, "label": "Var of it → the BETWEEN term", "kind": "step"},
   {"id": "e", "r": 2, "c": 2, "label": "E of it → the WITHIN term", "kind": "step"},
   {"id": "f", "r": 3, "c": 1, "label": "Var(Y) = within + between", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "a", "to": "c"},
   {"from": "b", "to": "d"}, {"from": "c", "to": "e"},
   {"from": "d", "to": "f"}, {"from": "e", "to": "f"}],
  "note": "Two functions of X, then one expectation and one variance. Every question on this topic is this diagram with distributions named."},
 "ask": {
  "q": "Both terms of the law are non-negative. What does that tell you about Var(Y) compared with E[Var(Y|X)]?",
  "nudge": "Adding something non-negative to a quantity does what to it? And when is the addition exactly zero?"}})

S.append({
 "kind": "worked", "id": "s3", "mins": 8,
 "title": "Worked in full — two machines, one defect count",
 "objective": "Apply the decomposition to numbers, and check it against the marginal distribution computed directly.",
 "ask": {
  "q": "The within term came to 3.2 and so did E(Y). Is that a coincidence?",
  "nudge": "For a Poisson, how do the mean and the variance compare? Then apply the tower property to each."},
 "problem": "Batches come from machine A with probability 0.6 and machine B with probability 0.4. Machine A produces defects as Poisson with mean 2; machine B as Poisson with mean 5. Find E(Y) and Var(Y) for the defect count Y of a randomly chosen batch.",
 "steps": [
  {"say": "Name the conditioning variable and write both conditional moments.",
   "math": "X = machine, with P(A) = 0.6 and P(B) = 0.4\nE(Y | X = A) = 2,   E(Y | X = B) = 5\nVar(Y | X = A) = 2, Var(Y | X = B) = 5",
   "why": "For a Poisson the mean and variance coincide, so each conditional variance equals its conditional mean. That is what makes this example clean, and it is why the two terms come out as they do."},
  {"say": "The mean, by the tower property.",
   "math": "E(Y) = 0.6(2) + 0.4(5) = 1.2 + 2.0 = 3.2",
   "why": "A weighted average of the conditional means. Note that no information about the spread was needed."},
  {"say": "The within term: average the conditional variances.",
   "math": "E[Var(Y | X)] = 0.6(2) + 0.4(5) = 3.2",
   "why": "Identical to the mean, because each conditional variance equalled its conditional mean and the same weights were applied. This is the Poisson's signature showing through, not a coincidence — and it is the answer to the question above."},
  {"say": "The between term: the variance of the conditional means.",
   "math": "E[(E(Y|X))²] = 0.6(4) + 0.4(25) = 2.4 + 10.0 = 12.4\nVar[E(Y|X)] = 12.4 − (3.2)² = 12.4 − 10.24 = 2.16",
   "why": "The conditional mean takes the value 2 with probability 0.6 and 5 with probability 0.4, so this is just the variance of a two-point random variable. Using E(square) minus square-of-mean is the quickest route."},
  {"say": "Add, and verify against the marginal distribution.",
   "math": "Var(Y) = 3.2 + 2.16 = 5.36\ndirect check: P(Y = k) = 0.6 e^(−2)2ᵏ/k! + 0.4 e^(−5)5ᵏ/k!\nsumming gives mean 3.2000 and variance 5.3600 ✓",
   "why": "The decomposition and the direct calculation agree exactly, as they must. Note that 5.36 exceeds the mean of 3.2 — the mixture is overdispersed relative to a Poisson, and by exactly the between term."}],
 "after": "The structure to carry away: Var(Y) = 5.36 while a single Poisson with mean 3.2 would have variance 3.2. The excess of 2.16 is precisely the variance of the machine rates. So heterogeneity in the population shows up entirely in the variance and not at all in the mean — which is the insurer's problem from the previous section, now with numbers."})

S.append({
 "kind": "recall", "id": "s4", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the two laws before going on.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "What kind of object is E(Y | X)?",
   "a": "A random variable — a function of X — so it has its own mean and variance."},
  {"q": "State the tower property.",
   "a": "E(Y) = E[E(Y | X)]."},
  {"q": "State the law of total variance.",
   "a": "Var(Y) = E[Var(Y | X)] + Var[E(Y | X)] — the within term plus the between term."},
  {"q": "If Y | X ~ Poisson(X), what is E(Y)?",
   "a": "E(X), since E(Y | X) = X and the tower property gives E(Y) = E(X)."},
  {"q": "If X and Y are independent, what is E(Y | X)?",
   "a": "E(Y), a constant — so the between term is zero."}]})

S.append({
 "kind": "completion", "id": "s5", "mins": 8,
 "title": "Your turn — June 2026, Q45",
 "objective": "Apply both terms where the mixing distribution is continuous.",
 "problem": "Let X follow the exponential distribution with mean 1/λ, and let Y given X = x follow the Poisson distribution with parameter x. Find Var(Y).",
 "steps": [
  {"say": "Write both conditional moments as functions of X.",
   "blank": {"prompt": "Give E(Y | X) and Var(Y | X).",
             "answer": "both equal X",
             "accept": ["X and X", "both are X", "E=X, Var=X", "E(Y|X)=X, Var(Y|X)=X"],
             "hint": "Y given X is Poisson with parameter X, and for a Poisson the mean and the variance are both the parameter."},
   "why": "This is what makes Poisson mixtures the standard example: the same function of X serves as both conditional moments, so the two terms of the law become E(X) and Var(X)."},
  {"say": "Now the two moments of the mixing distribution.",
   "blank": {"prompt": "For X exponential with mean 1/λ, give E(X) and Var(X).",
             "answer": "E(X) = 1/λ and Var(X) = 1/λ²",
             "accept": ["1/lambda and 1/lambda^2", "1/λ, 1/λ²", "mean 1/λ variance 1/λ²"],
             "hint": "The exponential's standard deviation equals its mean."},
   "why": "Variance is the square of the mean for an exponential. Mind the parameterisation: with mean 1/λ the variance is 1/λ², whereas if the question had said 'mean θ' it would be θ²."},
  {"say": "Assemble the two terms of the law of total variance.",
   "blank": {"prompt": "Write Var(Y) in terms of λ.",
             "answer": "Var(Y) = E(X) + Var(X) = 1/λ + 1/λ²",
             "accept": ["1/lambda + 1/lambda^2", "1/λ + 1/λ²", "E(X)+Var(X) = 1/λ+1/λ²"],
             "hint": "The within term is E[Var(Y|X)] = E(X); the between term is Var[E(Y|X)] = Var(X)."},
   "why": "Both terms of the law collapse to a moment of X, because E(Y|X) and Var(Y|X) are the same function. This is the whole of the question."},
  {"say": "Put it over a common denominator to match the options.",
   "blank": {"prompt": "Express 1/λ + 1/λ² as a single fraction.",
             "answer": "(λ + 1)/λ²",
             "accept": ["(lambda+1)/lambda^2", "(λ+1)/λ²", "(1+λ)/λ²"],
             "hint": "Multiply the first term by λ/λ."},
   "why": "1/λ = λ/λ², so the sum is (λ + 1)/λ² — the official answer, option D. The marked option was λ(λ + 1)/λ², which simplifies to (λ + 1)/λ: a factor of λ too large, the kind of slip that comes from combining the fractions carelessly rather than from misunderstanding the method."}],
 "after": "Worth a sanity check at the end. With λ = 2 the answer gives E(Y) = 0.5 and Var(Y) = 0.75, so the variance exceeds the mean — as it must for any Poisson mixture. If your expression ever gives a variance below the mean for a mixed Poisson, it is wrong, and that check takes five seconds."})

S.append({
 "kind": "theory", "id": "s6", "mins": 7,
 "title": "The standard mixtures, and overdispersion",
 "objective": "Know the three named results and the general fact that mixing always adds variance.",
 "blocks": [
  {"t": "formula", "h": "Any Poisson mixture is overdispersed",
   "body": "If Y | X ~ Poisson(X) then E(Y) = E(X) and\n    Var(Y) = E(X) + Var(X) = E(Y) + Var(X).\nSo Var(Y) ≥ E(Y), with equality only when Var(X) = 0 — that is, when X is constant and there is no mixing at all. A mixed Poisson can never be underdispersed."},
  {"t": "def", "h": "Poisson over a Gamma gives a negative binomial",
   "body": "Mixing a Poisson over a Gamma-distributed mean produces a negative binomial marginal. This is the classical result behind modelling count data with a negative binomial whenever it is more variable than a Poisson allows — insurance claims, accident counts, species abundance. The Gamma is chosen partly because it makes the integral tractable and partly because it is flexible enough to be plausible."},
  {"t": "def", "h": "Binomial over a Beta gives a beta-binomial",
   "body": "If Y | X ~ Binomial(n, X) with X ~ Beta(a, b), the marginal is beta-binomial, with E(Y) = na/(a + b) and a variance larger than the binomial's at the same mean. It is the natural model when a success probability varies between units — germination rates differing by seed lot, response rates differing by clinic. For n = 10, a = 2, b = 3 it gives mean 4 and variance 6, against 2.4 for a binomial with the same mean."},
  {"t": "formula", "h": "Normal over a normal gives a normal",
   "body": "If Y | X ~ N(X, 1) with X ~ N(0, σ²), then\n    Var(Y) = E[Var(Y|X)] + Var[E(Y|X)] = 1 + σ²,\nand the marginal is exactly N(0, 1 + σ²). The normal family is closed under this kind of mixing, which is unusual and is why it underpins random-effects models — add a random intercept to a normal model and you still have a normal model, with the variances adding."},
  {"t": "step", "h": "The common pattern",
   "body": "In every case the within term is the average of the conditional variances and the between term is the variance of the conditional means, and the marginal is more variable than the conditional family at the same mean. What differs is whether the resulting marginal has a convenient name. Poisson–Gamma, Binomial–Beta and Normal–Normal do; most pairings do not, and then you compute the two moments by the law and stop there — which is exactly what Q45 asks for."}],
 "ask": {
  "q": "A Poisson mixture always has variance at least its mean. Is the same true of a binomial mixture over a random success probability?",
  "nudge": "A binomial already has variance BELOW its mean. Does mixing push the variance up or down, and does it get all the way past the mean?"}})

S.append({
 "kind": "guided", "id": "s7", "mins": 8,
 "title": "On your own — the normal case and a random effect",
 "objective": "Apply the law where both stages are normal, and see why the result matters for real models.",
 "problem": "Let Y | X ~ N(X, 1) with X ~ N(0, σ²). (a) Find E(Y) and Var(Y). (b) Name the marginal distribution of Y. (c) For σ² = 4, how much wider is a 95% interval for Y than one computed ignoring the randomness in X? (d) What does the second term represent in a random-effects model?",
 "hints": [
  "For (a), identify E(Y | X) and Var(Y | X) as functions of X first, then apply both laws.",
  "For (c), compare the standard deviations √(1 + σ²) and √1, since an interval's width is proportional to the standard deviation.",
  "For (d), think about what X is in a model where each group has its own intercept."],
 "answer": "(a) E(Y) = 0 and Var(Y) = 1 + σ². (b) N(0, 1 + σ²). (c) √5 ≈ 2.24 times wider. (d) The between-group variance component.",
 "check": "Two things worth being exact about. In (a) the within term is E[Var(Y|X)] = E(1) = 1, because the conditional variance here is a constant and does not depend on X at all — which is the case that makes the arithmetic easy and also the case people over-think. And in (c) the factor is √5, not 5: variances add, so standard deviations and interval widths grow with the square root. Ignoring a variance component of 4 against a residual variance of 1 makes intervals less than half the width they should be, which is why random-effects models exist.",
 "scenario": {
  "teaser": "A multi-centre trial reports an interval that is far too narrow, and the reason is a term set to zero.",
  "title": "Why a random effect is not optional",
  "body": [
   "A trial runs at twelve centres. Each centre has its own baseline response level — differences in patient mix, staff, measurement habits — and within a centre, responses scatter around that level.",
   "An analyst pools all patients and computes a single mean and standard error as though every observation came from one homogeneous population. That treats the centre effect as zero, which means setting the between term of the law of total variance to zero.",
   "The consequence is in the arithmetic above. If the between-centre variance is four times the within-centre variance, the true standard deviation is √5 times the one assumed, so intervals are less than half as wide as they should be and the stated 95% coverage is nothing like 95%.",
   "The repair is to model the centre effect as random: Y given centre is normal around that centre's level, and the levels themselves are normal around a grand mean. That is exactly the two-stage structure of this section, and the two variances are called the within-group and between-group variance components.",
   "What makes the normal–normal case special is that the marginal is still normal, so the whole analysis stays tractable — the variances simply add. For most other pairings the marginal has no convenient form and one works with the moments alone.",
   "The general lesson is the insurer's again in a different setting: pooling heterogeneous groups gets the mean right and the uncertainty wrong, and the error is always in the direction of overconfidence."],
  "q": "Why does pooling heterogeneous centres leave the estimated mean roughly right while making the interval badly wrong?",
  "answer": "Because the tower property makes the mean insensitive to the grouping — averaging the centre means recovers the grand mean whether or not the centres differ. The variance has no such property: pooling discards Var[E(Y | centre)] entirely, so the reported uncertainty omits the between-centre component. The estimate is near-unbiased and the interval around it is too narrow, which is the worst combination because the result looks both correct and precise."},
 "solution": [
  {"say": "(a) Write both conditional moments and apply the two laws.",
   "math": "E(Y | X) = X,  Var(Y | X) = 1\nE(Y) = E[X] = 0\nVar(Y) = E[1] + Var[X] = 1 + σ²",
   "why": "The conditional variance is the constant 1, so the within term is simply 1. The between term is the variance of the conditional mean, which here is X itself."},
  {"say": "(b) Identify the marginal.",
   "math": "Y = X + (Y − X), a sum of independent N(0, σ²) and N(0, 1)\n⟹ Y ~ N(0, 1 + σ²)",
   "why": "Writing Y as a sum of independent normals makes the marginal immediate. The normal family is closed under this mixing, which is special — the Poisson–Exponential case of section 6 has no such tidy answer."},
  {"say": "(c) Compare the standard deviations.",
   "math": "assumed sd = √1 = 1\ncorrect sd = √(1 + 4) = √5 = 2.236\nratio = 2.236",
   "why": "Interval width is proportional to the standard deviation, so the correct interval is about 2.24 times wider. The ignored variance was four times the residual variance, and yet the width changes by a factor of only √5 — variances add, widths do not."},
  {"say": "(d) Name the term.",
   "math": "Var[E(Y | X)] = σ² = the between-group variance component\nE[Var(Y | X)] = 1  = the within-group variance component",
   "why": "The law of total variance IS the variance-components decomposition of a random-effects model. Setting the between term to zero is precisely the fixed-effects pooling the analyst did, and it is why its intervals were wrong."}]})

S.append({
 "kind": "trapcheck", "id": "s8", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims the practice questions on this topic are built from.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "E(Y | X) is a random variable.",
   "tf": True,
   "why": "True, and it is the foundation of the topic. It is a function of X, so it varies with X and has its own mean and variance — which is what makes E[E(Y|X)] and Var[E(Y|X)] meaningful."},
  {"claim": "Var(Y) = E[Var(Y | X)].",
   "tf": False,
   "why": "False — that is only the within term. The law of total variance adds Var[E(Y | X)], and omitting it understates the variance whenever the conditional mean depends on X. Equality holds only when E(Y|X) is constant."},
  {"claim": "If X and Y are independent then E(Y | X) = E(Y).",
   "tf": True,
   "why": "True. Independence means X carries no information about Y, so conditioning on it changes nothing and the conditional mean is the constant E(Y). The between term is then zero."},
  {"claim": "Any mixture of Poisson distributions has variance equal to its mean.",
   "tf": False,
   "why": "False. Var(Y) = E(X) + Var(X) = E(Y) + Var(X), which exceeds the mean whenever the mixing distribution is non-degenerate. Equality holds only if there is no mixing — a single Poisson."},
  {"claim": "Mixing a Poisson over a Gamma-distributed mean gives a negative binomial.",
   "tf": True,
   "why": "True, and it is the classical justification for modelling overdispersed counts with a negative binomial rather than a Poisson."},
  {"claim": "If Y | X ~ N(X, 1) and X ~ N(0, σ²), then Var(Y) = σ².",
   "tf": False,
   "why": "False — it is 1 + σ². The within term contributes the conditional variance of 1 and the between term contributes σ². Dropping the 1 is the same error as dropping the residual variance from a random-effects model."}]})

S.append({
 "kind": "guided", "id": "s9", "mins": 7,
 "title": "On your own — four quick conditional expectations",
 "objective": "Apply the two laws to cases where one term or the other is the whole answer.",
 "problem": "In each case give what is asked. (a) Y | X ~ Poisson(X), X ~ Gamma with mean 3 and variance 6: find E(Y) and Var(Y). (b) Y | X ~ Binomial(10, X), X ~ Beta(2, 3): find E(Y). (c) X and Y independent with E(Y) = 7: find E(Y | X) and Var[E(Y | X)]. (d) Y | X ~ N(X, X²) with X taking the values 1 and 3 with equal probability: find Var(Y).",
 "hints": [
  "For (a) and (b), identify E(Y|X) and Var(Y|X) as functions of X, then take the required moments of X.",
  "For (c), independence makes the conditional mean a constant. What is the variance of a constant?",
  "For (d) both conditional moments depend on X, so both terms need work. Compute E(X²) and Var(X) for a two-point variable."],
 "answer": "(a) E(Y) = 3, Var(Y) = 9. (b) E(Y) = 4. (c) E(Y | X) = 7 and Var[E(Y | X)] = 0. (d) Var(Y) = 6.",
 "check": "Three points. In (a) the answer Var(Y) = E(X) + Var(X) = 3 + 6 = 9 again exceeds the mean, as every Poisson mixture must. In (c) the whole point is that the between term vanishes under independence, so the law degenerates to an identity — and a question offering a non-zero value there is testing whether you know that. In (d) both terms contribute: the within term is E(X²) = 5 and the between term is Var(X) = 1, giving 6; forgetting that Var(Y|X) = X² depends on X and treating it as a constant is the error.",
 "solution": [
  {"say": "(a) A Poisson mixed over a Gamma.",
   "math": "E(Y|X) = X and Var(Y|X) = X\nE(Y) = E(X) = 3\nVar(Y) = E(X) + Var(X) = 3 + 6 = 9",
   "why": "Both terms reduce to moments of X. The marginal is negative binomial, but the question needs only the two moments — which is the usual situation."},
  {"say": "(b) A binomial mixed over a Beta.",
   "math": "E(Y|X) = 10X\nE(Y) = 10 E(X) = 10 × 2/(2+3) = 10 × 0.4 = 4",
   "why": "A Beta(a, b) has mean a/(a+b). Only the tower property is needed; the variance would be 6 by the beta-binomial formula, against 2.4 for a binomial with the same mean."},
  {"say": "(c) Independence.",
   "math": "E(Y | X) = E(Y) = 7, a constant\nVar[E(Y | X)] = Var(7) = 0",
   "why": "A constant has zero variance, so the between term vanishes and the law of total variance reduces to Var(Y) = E[Var(Y|X)] = Var(Y)."},
  {"say": "(d) Both conditional moments depend on X.",
   "math": "X takes 1 and 3 with probability 1/2 each: E(X) = 2, E(X²) = (1 + 9)/2 = 5, Var(X) = 1\nwithin:  E[Var(Y|X)] = E(X²) = 5\nbetween: Var[E(Y|X)] = Var(X) = 1\nVar(Y) = 5 + 1 = 6",
   "why": "The within term needs E(X²), not [E(X)]² — a distinction worth checking, since E(X²) = 5 while [E(X)]² = 4. Treating the conditional variance as constant would give 4 + 1 = 5 and be wrong."}]})

S.append({
 "kind": "theory", "id": "s10", "mins": 6,
 "title": "Where this idea reappears",
 "objective": "Recognise the same decomposition in the other places the syllabus uses it.",
 "blocks": [
  {"t": "step", "h": "In estimation: Rao–Blackwell",
   "body": "The Rao–Blackwell theorem of topic 4.3 says that conditioning an unbiased estimator on a sufficient statistic never increases its variance. That is the law of total variance read as an inequality: Var(T) = E[Var(T|S)] + Var[E(T|S)] ≥ Var[E(T|S)], so the conditioned estimator E(T|S) has variance at most Var(T). The improvement is exactly the within term that conditioning removes."},
  {"t": "step", "h": "In Bayesian work",
   "body": "A posterior predictive distribution is a mixture: the data's distribution given the parameter, mixed over the posterior for the parameter. Its variance is therefore the average sampling variance plus the posterior variance of the mean — which is why a predictive interval is wider than a confidence interval for the mean, and legitimately so."},
  {"t": "step", "h": "In experimental design and random effects",
   "body": "The within-group and between-group variance components of a random-effects model are precisely the two terms of the law, as section 7 showed. Analysis of variance partitions a sum of squares along the same split, and the intraclass correlation is the between term as a proportion of the total."},
  {"t": "step", "h": "The unifying statement",
   "body": "Conditioning splits variability into the part explained by the conditioning variable and the part left over. Every application above is that one sentence applied to a different conditioning variable — a sufficient statistic, a parameter, a group label. Recognising the decomposition in a new setting is usually faster than re-deriving it."}],
 "ask": {
  "q": "Rao–Blackwell improves an estimator by conditioning. In terms of the two terms, where does the improvement come from?",
  "nudge": "Which of the two terms is the variance of the conditioned estimator, and which is the part that gets discarded?"}})

S.append({
 "kind": "recall", "id": "s11", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the named results and the overdispersion fact.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Y | X ~ Poisson(X). Write Var(Y) in terms of moments of X.",
   "a": "Var(Y) = E(X) + Var(X), which exceeds E(Y) = E(X) whenever X is not constant."},
  {"q": "Poisson mixed over a Gamma gives which marginal?",
   "a": "The negative binomial."},
  {"q": "Binomial(n, X) with X ~ Beta(a, b) gives which marginal, and what mean?",
   "a": "Beta-binomial, with mean na/(a + b)."},
  {"q": "Y | X ~ N(X, 1), X ~ N(0, σ²). What is the marginal?",
   "a": "N(0, 1 + σ²) — the variances add and the family is preserved."},
  {"q": "When does the law of total variance reduce to Var(Y) = E[Var(Y|X)]?",
   "a": "When E(Y | X) is constant — in particular when X and Y are independent."},
  {"q": "X exponential with mean 1/λ. Give E(X) and Var(X).",
   "a": "1/λ and 1/λ²."}]})

S.append({
 "kind": "summary", "id": "s12", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Say what E(Y | X) is — a random variable, a function of X — and why that makes E[E(Y|X)] and Var[E(Y|X)] meaningful.",
  "State and use the tower property E(Y) = E[E(Y | X)].",
  "State the law of total variance, derive it from Var(Y) = E(Y²) − [E(Y)]², and name the within and between terms.",
  "Compute both terms for a two-stage model, including the case where the conditional variance itself depends on X.",
  "Show that any Poisson mixture is overdispersed, and compute Var(Y) = E(X) + Var(X).",
  "Name the three standard mixtures: Poisson–Gamma gives negative binomial, Binomial–Beta gives beta-binomial, Normal–Normal gives normal with variances added.",
  "Recognise the same decomposition in Rao–Blackwell, in posterior predictive variance, and in the variance components of a random-effects model."]})

S.append({
 "kind": "theory", "id": "s13", "mins": 8, "ext": True,
 "title": "Conditional expectation as the best predictor",
 "objective": "See why E(Y | X) is the answer to a minimisation problem, which explains why it appears everywhere.",
 "blocks": [
  {"t": "step", "h": "The question it answers",
   "body": "Suppose you must predict Y using a function of X, and you will be scored by mean squared error. Which function g should you choose? The answer is g(X) = E(Y | X), and it is unique up to events of probability zero. Conditional expectation is not merely a convenient summary; it is the optimal predictor under squared error."},
  {"t": "formula", "h": "Why, in three lines",
   "body": "For any candidate g, write Y − g(X) = [Y − E(Y|X)] + [E(Y|X) − g(X)]. Squaring and taking expectations, the cross term vanishes because\n    E{ [Y − E(Y|X)][E(Y|X) − g(X)] } = E( E{ … | X } ) = 0,\nsince the second bracket is a function of X and the first has conditional mean zero. Hence\n    E[(Y − g(X))²] = E[(Y − E(Y|X))²] + E[(E(Y|X) − g(X))²],\nwhich is minimised by taking g(X) = E(Y | X), leaving the first term alone."},
  {"t": "def", "h": "The geometric reading",
   "body": "That calculation is a Pythagorean identity. In the space of random variables with finite variance, with inner product E(UV), the functions of X form a subspace, and E(Y | X) is the orthogonal PROJECTION of Y onto it. The residual Y − E(Y|X) is orthogonal to every function of X, which is what the vanishing cross term says. Prediction error decomposes like the squared sides of a right triangle."},
  {"t": "step", "h": "And the law of total variance is that identity",
   "body": "Take g(X) = E(Y), a constant, in the decomposition above. The left side becomes Var(Y), the first right-hand term is E[Var(Y|X)], and the second is E[(E(Y|X) − E(Y))²] = Var[E(Y|X)]. So the law of total variance is the Pythagorean identity for this particular choice of predictor — the whole of section 3 in one line, from a different direction."},
  {"t": "step", "h": "What this buys",
   "body": "Three things become unsurprising. The between term is non-negative because it is a squared length. Rao–Blackwell works because projecting onto a smaller subspace cannot increase a norm. And linear regression is the same construction restricted to LINEAR functions of X — projection onto a smaller subspace, which is why least squares and conditional expectation coincide exactly when the true conditional mean happens to be linear."}],
 "ask": {
  "q": "Least squares projects onto linear functions of X; conditional expectation projects onto all functions of X. When do the two coincide?",
  "nudge": "A projection onto a subspace equals the projection onto a larger space exactly when the answer already lies in the smaller one."}})

S.append({
 "kind": "quiz", "id": "s14", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "probability_t3_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "probabilityt3",
 "topicId": "probability-t3",
 "moduleId": "probability",
 "title": "Conditional Expectation, Total Variance and Mixtures",
 "breadcrumb": "Probability → Conditioning → Conditional expectation and total variance",
 "engine": "B",
 "engineName": "Probability — splitting variability into the part a variable explains and the rest",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Say what E(Y | X) is and why it has a mean and a variance of its own.",
  "State and apply the tower property and the law of total variance.",
  "Derive the law of total variance from Var(Y) = E(Y²) − [E(Y)]².",
  "Compute both terms in two-stage models, including when the conditional variance depends on X.",
  "Show that any Poisson mixture is overdispersed and compute its variance.",
  "Name the Poisson–Gamma, Binomial–Beta and Normal–Normal mixtures and their marginals."],
 "prereq": [
  {"id": "p1", "name": "Expectation and variance",
   "why": "Every step is an expectation or a variance, and the derivation uses Var(Y) = E(Y²) − [E(Y)]² directly."},
  {"id": "p2", "name": "Conditional distributions",
   "why": "E(Y | X = x) is the mean of a conditional distribution. If that object is unfamiliar, topic 1.2 comes first."},
  {"id": "p3", "name": "Standard distributions and their moments",
   "why": "The examples need the Poisson's mean and variance, the exponential's variance, and the Beta and Gamma means."},
  {"id": "p4", "name": "Independence",
   "why": "The degenerate case of the law — a zero between term — is exactly the independent case, and it is asked directly."}],
 "traps": [
  "E(Y | X) is a random variable, not a number.",
  "Var(Y) is NOT E[Var(Y|X)] — the between term is missing.",
  "For a mixed Poisson, Var(Y) = E(X) + Var(X) always exceeds the mean.",
  "Y | X ~ N(X, 1) with X ~ N(0, σ²) gives Var(Y) = 1 + σ², not σ².",
  "When Var(Y|X) depends on X, the within term needs E(X²), not [E(X)]².",
  "Mind the exponential's parameterisation: mean 1/λ means variance 1/λ².",
  "1/λ + 1/λ² = (λ + 1)/λ², not λ(λ + 1)/λ².",
  "Independence makes the between term zero, not the within term."],
 "revision": {
  "sheet": [
   "E(Y | X) is a random variable — a function of X — so it has its own mean and variance.",
   "Tower property: E(Y) = E[E(Y | X)].",
   "Law of total variance: Var(Y) = E[Var(Y | X)] + Var[E(Y | X)], the within term plus the between term.",
   "Derivation: expand Var(Y) = E(Y²) − [E(Y)]², apply the tower property to each piece, and the leftover two terms are Var[E(Y|X)].",
   "Both terms are non-negative, so Var(Y) is at least E[Var(Y|X)], with equality iff E(Y|X) is constant.",
   "Independence ⟹ E(Y | X) = E(Y), a constant ⟹ between term zero.",
   "Y | X ~ Poisson(X): E(Y) = E(X) and Var(Y) = E(X) + Var(X) = E(Y) + Var(X) > E(Y) unless X is constant.",
   "June 2026 Q45: X exponential with mean 1/λ, Y|X ~ Poisson(X) ⟹ Var(Y) = 1/λ + 1/λ² = (λ + 1)/λ².",
   "Poisson over Gamma → negative binomial. Binomial(n, X) over Beta(a, b) → beta-binomial, mean na/(a+b). N(X,1) over N(0,σ²) → N(0, 1+σ²).",
   "Worked mixture: machines at Poisson rates 2 and 5 with weights 0.6 and 0.4 give E(Y) = 3.2, within 3.2, between 2.16, Var(Y) = 5.36 — confirmed against the marginal pmf.",
   "When Var(Y|X) is a non-constant function of X, the within term is its expectation: for Var(Y|X) = X², it is E(X²).",
   "The law is the variance-components decomposition of a random-effects model, the inequality behind Rao–Blackwell, and the reason a posterior predictive interval exceeds a confidence interval.",
   "E(Y | X) is the minimum-mean-squared-error predictor of Y from X, and the orthogonal projection of Y onto the functions of X; the law of total variance is the resulting Pythagorean identity."],
  "cards": [
   ["E(Y | X) is", "A random variable — a function of X — with its own mean and variance"],
   ["Tower property", "E(Y) = E[E(Y | X)]"],
   ["Law of total variance", "Var(Y) = E[Var(Y|X)] + Var[E(Y|X)] — within plus between"],
   ["When the between term is zero", "When E(Y|X) is constant, in particular under independence"],
   ["Mixed Poisson variance", "E(X) + Var(X), which always exceeds the mean unless X is constant"],
   ["Q45's answer", "1/λ + 1/λ² = (λ + 1)/λ²"],
   ["Poisson over Gamma", "Negative binomial — the classical model for overdispersed counts"],
   ["Binomial over Beta", "Beta-binomial, mean na/(a + b)"],
   ["N(X,1) over N(0,σ²)", "N(0, 1 + σ²) — variances add and the family is preserved"],
   ["Within term when Var(Y|X) = X²", "E(X²), not [E(X)]²"],
   ["In a random-effects model", "The two terms are the within-group and between-group variance components"],
   ["Why E(Y|X) appears everywhere", "It is the best squared-error predictor of Y from X, the projection onto functions of X"]],
  "tricks": [
   "Write E(Y|X) and Var(Y|X) as functions of X first. Everything after that is one expectation and one variance.",
   "For a mixed Poisson, check that your variance exceeds your mean. If it does not, the between term was dropped.",
   "If the conditional variance is a constant, the within term is that constant — no expectation needed.",
   "If the conditional variance depends on X, you need a second moment of X; E(X²) and [E(X)]² differ.",
   "Under independence the between term is zero, so a question offering a non-zero value there is testing that fact."],
  "shortcuts": [
   "Poisson mixtures: both terms are moments of X, so Var(Y) = E(X) + Var(X) with no integration.",
   "Normal mixtures: variances add, so Var(Y) = conditional variance + mixing variance.",
   "Interval widths grow with the square root of the added variance, so a variance component four times the residual widens intervals by √5, not by 5."],
  "remember": [
   "E(Y|X) is random. That is the whole topic.",
   "Variance needs two terms; the mean needs one.",
   "A mixed Poisson is always overdispersed."]},
 "howto": "This is the first lesson of the probability module. Read the opening checks carefully — the single idea that E(Y | X) is a random variable is what makes everything here work, and it is easy to nod past. Sections 3 and 4 are the core: the two laws with the derivation, then a mixture worked with numbers and checked against the marginal distribution directly. Section 6 is June 2026's own question, where the only real difficulty is combining two fractions. Sections 7 and 9 drill the cases where one term or the other is the whole answer. If short of time, sections 3, 4 and 6 are the lesson. Attempt the question at the end of each section before opening the answer. The optional section shows that E(Y|X) is the best possible predictor of Y from X, which explains why this one object turns up in estimation, in Bayesian prediction and in regression alike. There is no interactive chart yet for this topic.",
 "refs": [
  {"title": "Conditional Distributions and Expectation", "where": "Lessons 19 and 20",
   "site": "Penn State STAT 414", "url": "https://online.stat.psu.edu/stat414/",
   "type": "Course notes", "free": True, "checked": "2026-11-03",
   "why": "Conditional expectation built up from conditional distributions, with the tower property and worked mixture examples."},
  {"title": "Statistical Inference, 2nd edition", "where": "Sections 4.4 and 4.6",
   "site": "Casella and Berger", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The two laws stated and proved, with the hierarchical-model examples this lesson's mixtures come from."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 4",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "Conditional expectation at the level the NET syllabus sets, including the Poisson and binomial mixtures."},
  {"title": "Probability and Statistics", "where": "Weeks on conditional expectation",
   "site": "NPTEL / SWAYAM", "url": "https://archive.nptel.ac.in/courses/111105090",
   "type": "Video course", "free": True, "checked": "2026-11-03",
   "why": "Indian syllabus notation and worked numerical examples in the phrasing NET questions use."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026, the first lesson of the probability module — the largest uncovered block in the syllabus at 10 questions and 20 marks in June 2026. PYQ anchor: Q45 (answered wrongly), where X is exponential with mean 1/λ and Y|X is Poisson(X), giving Var(Y) = E(X) + Var(X) = (λ + 1)/λ²; the marked option was a factor of λ too large. Q45 carried no practice variants; nine of the nineteen tagged to Q46 are conditional-expectation and mixture items plainly belonging to Q45, and were retagged on 2026-11-03 — the sixth misfiling found in this project and the second to rescue a question that had none. All nine are taught in named sections and appear in the pool. Every numerical result was computed and, where possible, checked twice: the two-machine mixture gives Var(Y) = 5.36 both by the decomposition and by summing the marginal pmf directly, and the beta-binomial with n = 10, a = 2, b = 3 gives mean 4 and variance 6 both by formula and by summing its pmf. No explore scene: no visualisation for mixtures or overdispersion exists yet. Previous-year questions are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "pr-t3-m-%02d" % i, "format": fmt, "topic": "probability-t3",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "E(Y | X) is:",
 ["a random variable, being a function of X", "always a constant",
  "equal to E(Y) in general", "undefined unless X and Y are independent"],
 "A",
 "E(Y | X = x) is a number for each x, but E(Y | X) is the function of X that returns it — and since X is random, so is the result. That is why E[E(Y|X)] and Var[E(Y|X)] are meaningful quantities, and it is the idea the whole topic rests on."))

I.append(q(2, "single", "easy",
 "The law of total variance states that Var(Y) equals:",
 ["E[Var(Y | X)] + Var[E(Y | X)]", "E[Var(Y | X)]",
  "Var[E(Y | X)]", "E[Var(Y | X)] × Var[E(Y | X)]"],
 "A",
 "The within term E[Var(Y|X)] averages the conditional variances; the between term Var[E(Y|X)] measures how much the conditional mean itself moves. Both are non-negative, so dropping either understates the variance — and dropping the second is the standard error."))

I.append(q(3, "single", "easy",
 "If Y | X ~ Poisson(X), then E(Y) equals:",
 ["E(X)", "X", "Var(X)", "E(X) + Var(X)"],
 "A",
 "For a Poisson the mean is the parameter, so E(Y | X) = X, and the tower property gives E(Y) = E[E(Y|X)] = E(X). The second option confuses a random variable with its expectation, and the fourth is Var(Y), not E(Y)."))

I.append(q(4, "numeric", "easy",
 "For an exponential distribution with mean 1/λ, the variance is:",
 ["1/λ", "1/λ²", "λ", "λ²"],
 "B",
 "The exponential's standard deviation equals its mean, so the variance is the square of the mean: (1/λ)² = 1/λ². Watch the parameterisation — written as (1/θ)e^(−x/θ) the mean is θ and the variance θ².",
 check="Variance has the squared units of the mean, so if the mean is 1/λ the variance must carry 1/λ²."))

I.append(q(5, "single", "easy",
 "If X and Y are independent, E(Y | X) equals:",
 ["E(Y)", "Y", "0", "E(X)"],
 "A",
 "Independence means X carries no information about Y, so conditioning on it changes nothing and the conditional mean is the constant E(Y). The between term of the law of total variance is then zero, since a constant has no variance."))

I.append(q(6, "single", "easy",
 "A Poisson distribution mixed over a Gamma-distributed mean gives:",
 ["another Poisson", "a negative binomial", "a beta-binomial", "a normal distribution"],
 "B",
 "This is the classical result that justifies modelling overdispersed count data with a negative binomial. The mixing makes the marginal more variable than any single Poisson with the same mean, which is exactly what count data usually shows."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "Let X follow the exponential distribution with mean 1/λ and let Y given X = x follow the Poisson distribution with parameter x. Then Var(Y) equals:",
 ["λ(λ + 1)/λ²", "λ²/(λ + 1)", "λ(λ + 1)", "(λ + 1)/λ²"],
 "D",
 "E(Y|X) = Var(Y|X) = X, so Var(Y) = E(X) + Var(X) = 1/λ + 1/λ². Putting that over a common denominator gives (λ + 1)/λ². This is June 2026 Q45; the marked option simplifies to (λ + 1)/λ, a factor of λ too large.",
 check="Check with λ = 2: E(Y) = 0.5 and Var(Y) = 0.75. A mixed Poisson must have variance above its mean, which rules out any option giving less."))

I.append(q(8, "single", "moderate",
 "For any mixture of Poisson distributions, the variance is:",
 ["equal to the mean", "greater than the mean unless the mixing distribution is degenerate",
  "less than the mean", "unrelated to the mean"],
 "B",
 "Var(Y) = E(X) + Var(X) = E(Y) + Var(X), so the variance exceeds the mean by exactly the variance of the mixing distribution. Equality holds only when X is constant — that is, when there is no mixing and Y is a plain Poisson. A mixed Poisson can never be underdispersed."))

I.append(q(9, "numeric", "moderate",
 "Batches come from machine A with probability 0.6 and machine B with probability 0.4, producing defects as Poisson with means 2 and 5 respectively. Var(Y) for a randomly chosen batch is:",
 ["3.20", "5.36", "2.16", "10.24"],
 "B",
 "The within term is 0.6(2) + 0.4(5) = 3.2, since each conditional variance equals its conditional mean. The between term is 0.6(4) + 0.4(25) − 3.2² = 12.4 − 10.24 = 2.16. The total is 5.36, which agrees with summing the marginal pmf directly. Option A is the within term alone, which is also E(Y).",
 check="The answer must exceed E(Y) = 3.2, because any Poisson mixture is overdispersed. An answer equal to 3.2 has dropped the between term."))

I.append(q(10, "numeric", "moderate",
 "If Y | X ~ N(X, 1) and X ~ N(0, σ²), then Var(Y) equals:",
 ["σ²", "1", "1 + σ²", "1 − σ²"],
 "C",
 "The within term is E[Var(Y|X)] = E(1) = 1, since the conditional variance is constant, and the between term is Var[E(Y|X)] = Var(X) = σ². So Var(Y) = 1 + σ², and the marginal is exactly N(0, 1 + σ²) — the normal family is closed under this mixing. Dropping the 1 is the same error as omitting the residual variance from a random-effects model.",
 check="Variances add here, so the answer must exceed both 1 and σ² separately."))

I.append(q(11, "single", "moderate",
 "If Y | X ~ Binomial(n, X) with X ~ Beta(a, b), then Y follows:",
 ["a binomial distribution", "a beta-binomial distribution",
  "a negative binomial distribution", "a hypergeometric distribution"],
 "B",
 "Mixing a binomial success probability over a Beta gives the beta-binomial, with mean na/(a+b) and a variance larger than a binomial's at the same mean. It is the natural model when a success probability varies between units — germination differing by seed lot, response differing by clinic."))

I.append(q(12, "multi", "moderate",
 "Consider the two laws of conditioning.",
 ["A and C only", "A, B and C only", "B and D only", "C and D only"],
 "A",
 "A is true and is the tower property. B is false — that is the within term only, and the between term is missing. C is true, and it is why the law degenerates under independence. D is false: both terms are non-negative, so Var(Y) is at least as large as either.",
 statements=["E(Y) = E[E(Y | X)].",
             "Var(Y) = E[Var(Y | X)].",
             "If E(Y | X) is constant then Var(Y) = E[Var(Y | X)].",
             "Var(Y) can be smaller than E[Var(Y | X)]."],
 verdicts=verd(
  (True, "True — the tower property. Average within each value of X, then average over X, and you recover the overall mean."),
  (False, "False. That is the within term alone; the law of total variance adds Var[E(Y|X)], which is zero only when the conditional mean does not move with X."),
  (True, "True. A constant conditional mean has zero variance, so the between term vanishes and only the within term remains."),
  (False, "False. Both terms are non-negative and they are added, so Var(Y) is at least E[Var(Y|X)] and at least Var[E(Y|X)]."))))

I.append(q(13, "numeric", "moderate",
 "Y | X ~ Poisson(X) where X has mean 3 and variance 6. Then E(Y) and Var(Y) are:",
 ["3 and 3", "3 and 6", "3 and 9", "9 and 9"],
 "C",
 "E(Y) = E(X) = 3 by the tower property, and Var(Y) = E(X) + Var(X) = 3 + 6 = 9. Option A treats Y as a plain Poisson and option B reports Var(X) rather than Var(Y). The marginal here is negative binomial, but only the two moments are needed.",
 check="The variance must exceed the mean for any Poisson mixture, so 9 > 3 is the expected shape of the answer."))

I.append(q(14, "single", "moderate",
 "In a random-effects model, the term Var[E(Y | X)] of the law of total variance corresponds to:",
 ["the within-group variance component", "the between-group variance component",
  "the residual variance", "the total sum of squares"],
 "B",
 "E(Y | group) is the group's own mean level, so the variance of that quantity across groups is the between-group variance component. The within term E[Var(Y | group)] is the within-group or residual component. The law of total variance IS the variance-components decomposition."))

I.append(q(15, "numeric", "moderate",
 "Y | X ~ N(X, X²) where X takes the values 1 and 3 with equal probability. Then Var(Y) equals:",
 ["5", "6", "4", "10"],
 "B",
 "E(X) = 2, E(X²) = (1 + 9)/2 = 5 and Var(X) = 1. The within term is E[Var(Y|X)] = E(X²) = 5 and the between term is Var[E(Y|X)] = Var(X) = 1, so Var(Y) = 6. Option C uses [E(X)]² = 4 for the within term instead of E(X²) = 5.",
 check="When the conditional variance depends on X, the within term needs the SECOND moment E(X²), which differs from [E(X)]²."))

I.append(q(16, "single", "moderate",
 "Why does the mean require only one term while the variance requires two?",
 ["because variance is always larger than the mean",
  "because expectation is linear and variance, involving a square, is not",
  "because the conditional variance is always constant",
  "because the between term is usually negligible"],
 "B",
 "Averaging conditional averages recovers the overall average exactly, because expectation is linear. Variance involves a square, and squaring does not commute with averaging — the discrepancy is precisely the variance of the conditional means, which is the second term."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider where the law of total variance reappears elsewhere in the syllabus.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true — the law read as an inequality is exactly why conditioning cannot increase variance. B is true: a predictive distribution is a mixture, so its variance carries both terms. C is true, and it is the random-effects reading. D is false — conditional expectation projects onto ALL functions of X, while least squares projects onto the linear ones, so the two coincide only when the true conditional mean happens to be linear.",
 statements=["Rao–Blackwell follows from Var(Y) ≥ Var[E(Y | X)].",
             "A posterior predictive variance exceeds the posterior variance of the mean.",
             "The two terms are the within-group and between-group variance components.",
             "Least squares regression always gives exactly E(Y | X)."],
 verdicts=verd(
  (True, "True. Var(T) = E[Var(T|S)] + Var[E(T|S)] ≥ Var[E(T|S)], so the conditioned estimator E(T|S) has variance no larger than T's."),
  (True, "True. The predictive distribution mixes the sampling distribution over the posterior, so its variance adds the average sampling variance to the posterior variance of the mean."),
  (True, "True. E(Y | group) is the group's level, so its variance across groups is the between-group component, and the average conditional variance is the within-group component."),
  (False, "False. Conditional expectation is the projection onto all functions of X; least squares projects onto the linear ones. They agree exactly when the true conditional mean is linear in X, and not otherwise."))))

I.append(q(18, "numeric", "hard",
 "A variance component of 4 is ignored alongside a residual variance of 1. By what factor are the resulting confidence intervals too narrow?",
 ["5.00", "2.24", "4.00", "1.25"],
 "B",
 "The correct standard deviation is √(1 + 4) = √5 = 2.236, against the assumed √1 = 1. Interval width is proportional to the standard deviation, so the intervals are about 2.24 times too narrow. Option A mistakes the variance ratio for the width ratio — variances add, widths grow with the square root.",
 check="Widths scale with the standard deviation, never with the variance. A factor of 5 in variance is a factor of √5 in width."))

I.append(q(19, "single", "hard",
 "E(Y | X) has a characterisation as the solution to an optimisation problem. It is:",
 ["the function of X maximising the correlation with Y",
  "the function of X minimising E[(Y − g(X))²]",
  "the linear function of X minimising E[(Y − g(X))²]",
  "the function of X minimising E|Y − g(X)|"],
 "B",
 "E(Y | X) is the minimum-mean-squared-error predictor of Y among ALL functions of X — equivalently the orthogonal projection of Y onto the space of functions of X. Restricting to linear functions gives least squares regression instead, and minimising absolute error gives the conditional median, not the conditional mean."))

I.append(q(20, "single", "hard",
 "An insurer models claim counts as Poisson using the portfolio's average rate, and finds the mean accurate but bad years more frequent than predicted. The explanation is:",
 ["the Poisson mean was estimated badly",
  "policyholders have heterogeneous rates, so the between term was set to zero",
  "claims are not independent within a policy",
  "the sample was too small to estimate the variance"],
 "B",
 "The tower property makes the mean insensitive to heterogeneity — E(Y) = E(X) whether or not rates vary — so the average can be right while the variance is badly understated. Treating the portfolio as a single Poisson discards Var[E(Y|X)], the variance of the individual rates, which is exactly the overdispersion that makes bad years more common than the model allows."))

# Spread the answer keys; the validator caps any letter at 40% of the pool.
LET = "ABCD"
WANT = {"pr-t3-m-01": "C", "pr-t3-m-02": "D", "pr-t3-m-03": "C",
        "pr-t3-m-04": "D", "pr-t3-m-05": "C", "pr-t3-m-08": "D",
        "pr-t3-m-11": "A", "pr-t3-m-12": "B", "pr-t3-m-13": "A",
        "pr-t3-m-16": "D", "pr-t3-m-19": "A", "pr-t3-m-20": "D"}

def relabel(items):
    for it in items:
        w = WANT.get(it["id"])
        if not w or not it.get("options"):
            continue
        i, j = LET.index(it["answer"]), LET.index(w)
        if i == j:
            continue
        o = it["options"]
        o[i], o[j] = o[j], o[i]
        it["answer"] = w
        a, b = LET[i], LET[j]
        it["explanation"] = re.sub(
            r"\b([Oo]ption )([ABCD])\b",
            lambda m: m.group(1) + (b if m.group(2) == a else a if m.group(2) == b else m.group(2)),
            it["explanation"])
    return items

relabel(I)
_k = {}
for _it in I:
    _k[_it["answer"]] = _k.get(_it["answer"], 0) + 1
print("key spread:", {L: _k.get(L, 0) for L in LET}, "cap", -(-len(I) * 2 // 5))

POOLD = {
 "moduleId": "probability", "topicId": "probability-t3", "source": "mastery",
 "label": "Conditional expectation, total variance and mixtures — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
