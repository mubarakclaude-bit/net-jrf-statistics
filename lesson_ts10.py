#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 7.10 — General linear process and Wold decomposition (timeseries-t10).

No PYQ anchor of its own. It is the theoretical keystone of the module: the theorem that says
the MA(infinity) form is not one modelling choice among many but the general shape of every
stationary process.

Scope set against the lessons already built:
 - 7.1 owns the admissible regions and the AR(1)->MA(infinity) expansion for that one case.
   This lesson generalises it. Cross-referenced.
 - 7.4 owns the autocovariance computed from the MODEL equation. This lesson computes it from
   the psi weights instead, which is the other route to the same numbers.
 - 7.7 owns the spectrum; 7.11 owns forecasting. Both are cross-referenced as consequences.
 - THIS lesson owns the general linear process, the square-summability condition, the
   autocovariance in terms of psi, the Wold theorem and the impulse-response reading.

Verified: gamma_k = sigma^2 sum_j psi_j psi_{j+k} computed directly over 4000 terms against the
closed form phi^k/(1-phi^2) for an AR(1), agreeing to six decimals at every phi and k tested:
  phi=0.5: 1.333333, 0.666667, 0.333333, 0.166667 at k=0,1,2,3
  phi=0.7: 1.960784, 1.372549, 0.960784, 0.672549
  phi=0.8: 2.777778, 2.222222, 1.777778, 1.422222
MA(1) minus convention, psi = (1, -theta): gamma_0 = 1+theta^2, gamma_1 = -theta, gamma_k = 0.
Square-summability sum psi_j^2 = 1/(1-phi^2): 10.2564 at phi=0.95, 50.2513 at phi=0.99.

Writes seed/lesson_ts10.json and seed/timeseries_t10_mastery.json.
"""
import json, io, os, re

OUT = "seed/lesson_ts10.json"
POOL = "seed/timeseries_t10_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 7,
 "title": "Before the lesson — four things it will assume",
 "objective": "Fix the representation and the condition it needs.",
 "ask": {
  "q": "Topic 7.1 wrote a stationary AR(1) as an infinite moving average. Is that a special trick, or does something like it always work?",
  "nudge": "What would it mean if it always worked?"},
 "body": [
  "Topic 7.1 showed that a stationary AR(1) can be written as yₜ = Σφʲεₜ₋ⱼ — an infinite moving average of past shocks. That looked like a convenient manipulation for one particular model.",
  "It is not. Wold's theorem says that EVERY stationary process, with one carefully stated exception, has a representation of that form: a weighted sum of uncorrelated shocks, with weights that are square-summable. The AR(1) expansion was an instance of a general fact.",
  "That changes the status of the moving-average form. It is not one model class competing with AR and ARMA; it is the universal shape, and the finite AR and MA models are parameterisations of particular weight sequences. This lesson states the general process, computes its autocovariance from the weights, and gives the theorem.",
  "Four checks before starting."],
 "items": [
  {"ask": "Write the general linear process and name its parts.",
   "recall": "yₜ = μ + Σ(j≥0) ψⱼεₜ₋ⱼ, with ψ₀ = 1 and {εₜ} white noise.",
   "refresh": [
    "The ψⱼ are the WEIGHTS, and the normalisation ψ₀ = 1 is a convention that fixes the scale — otherwise ψ and σ² could be traded against each other, exactly the non-identifiability of topic 7.1.",
    "The sum is ONE-SIDED: it runs over past and present shocks only, never future ones. That is what makes the representation causal and usable for forecasting.",
    "The εₜ are uncorrelated with mean zero and constant variance σ². Note UNCORRELATED, not necessarily independent — a distinction that matters in the theorem and is discussed in section 7."]},
  {"ask": "What condition must the weights satisfy, and why?",
   "recall": "Square-summability: Σψⱼ² < ∞.",
   "refresh": [
    "The variance of the process is σ²Σψⱼ², so the sum must converge for the variance to be finite — which stationarity requires.",
    "For an AR(1) the weights are φʲ and the sum is 1/(1 − φ²), finite exactly when |φ| < 1. So the square-summability condition IS the stationarity condition for that case. Verified: 10.2564 at φ = 0.95 and 50.2513 at φ = 0.99 — large but finite.",
    "Square-summability is weaker than absolute summability Σ|ψⱼ| < ∞. The stronger condition is sometimes imposed because it gives the ergodicity results of topic 7.9, and every ARMA process satisfies it."]},
  {"ask": "What are the autocovariances of a finite MA(1) under the minus convention?",
   "recall": "γ₀ = σ²(1 + θ²), γ₁ = −θσ², and γₖ = 0 for k ≥ 2.",
   "refresh": [
    "In the ψ language this is the weight sequence ψ₀ = 1, ψ₁ = −θ, and zero thereafter — a finite sequence.",
    "So a finite MA is the general linear process with finitely many non-zero weights, and the cut-off in its ACF is the cut-off in its weights.",
    "This gives the pattern: γₖ depends on the OVERLAP between the weight sequence and its own shift by k, which is the formula in section 3."]},
  {"ask": "What does 'deterministic' mean for a time series component?",
   "recall": "Perfectly predictable from its own infinite past, with zero forecast error.",
   "refresh": [
    "A constant is deterministic. So is a pure sinusoid with fixed amplitude and phase — given enough of its past, the next value is known exactly.",
    "The Wold theorem needs this notion because such components cannot be written as a sum of shocks: they carry no innovation at all. The theorem therefore splits a process into a deterministic part plus a shock-driven part.",
    "A process with no deterministic part is called PURELY NON-DETERMINISTIC, and that is the class for which the MA(∞) form is the whole story."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "The weights are the process's response to a shock",
 "objective": "Read the ψ sequence as something physical.",
 "body": [
  "Suppose a single shock of size 1 arrives at time t and nothing else ever happens. In the representation yₜ = Σψⱼεₜ₋ⱼ, that shock contributes ψ₀ to yₜ, ψ₁ to yₜ₊₁, ψ₂ to yₜ₊₂, and so on. So the weight sequence is literally the path the process traces out in response to one unit shock — the IMPULSE RESPONSE FUNCTION.",
  "That reading makes the weights interpretable rather than algebraic. For an AR(1) with φ = 0.7 the impulse response is 1, 0.7, 0.49, 0.343 — a shock decays geometrically, with about 34% of it still present three periods later. For an MA(1) with θ = 0.5 the response is 1, −0.5, 0, 0, … — a shock is felt once, partially reversed, and then gone entirely.",
  "The square-summability condition now has a meaning too: the response to a shock must die away fast enough that its total squared effect is finite. If it does not — if ψⱼ stays at 1 forever, as it does for a random walk — the process has infinite variance and is not stationary. Topic 7.6's random walk is exactly the case ψⱼ = 1 for all j.",
  "The sum Σψⱼ, when it converges, is the TOTAL long-run effect of a unit shock on the level. For an AR(1) it is 1/(1 − φ): 3.33 at φ = 0.7 and 20 at φ = 0.95. For an MA(1) with θ = 0.5 it is 0.5. That number is what applied work calls the long-run multiplier, and it is read straight off the weights.",
  "So the general linear process is not an abstraction imposed on the data. It is the statement that a stationary series is the accumulated echo of past shocks, and the weights say how loudly each echo still sounds."],
 "scenario": {
  "teaser": "Two models fit a series equally well but disagree about the long-run effect of a shock.",
  "title": "What the weights decide",
  "body": [
   "An analyst fits an AR(1) with φ̂ = 0.7 and reports that a unit shock raises the series by 1 immediately and has a cumulative long-run effect of 1/(1 − 0.7) = 3.33. A colleague fits an ARMA(1,1) with φ̂ = 0.8 and θ̂ = 0.15, whose fit is marginally better, and reports a long-run effect of (1 − 0.15)/(1 − 0.8) = 4.25.",
   "Both are computing the same quantity, Σψⱼ, from their own weight sequences. For an ARMA(1,1) under the minus convention the weights are ψ₀ = 1 and ψⱼ = φ^(j−1)(φ − θ) for j ≥ 1, so the cumulative sum is (1 − θ)/(1 − φ). The two answers differ by 28% because the two models imply different impulse responses even though they fit the observed series similarly.",
   "This is a case where the choice of model matters for the conclusion and the data barely distinguish the candidates. The in-sample fit statistics differ marginally, but the quantity of interest differs substantially, because the cumulative effect depends on the behaviour of the weights far out in the tail — precisely where a short sample carries the least information.",
   "The honest response is to report the sensitivity rather than to pick a number. If the long-run multiplier is the output that matters, its uncertainty should include uncertainty about the model, not just about the parameters of one model. Reporting 3.33 with a tight confidence interval from the AR(1) alone overstates what has been established.",
   "There is a sharper version of the same point. As φ approaches 1 the multiplier 1/(1 − φ) diverges, so in a near-unit-root situation the cumulative effect is essentially unidentified: φ̂ = 0.95 gives 20 and φ̂ = 0.98 gives 50, and the data may not separate those values at all. That is a genuine limitation rather than a failure of technique.",
   "The general lesson is that the ψ weights carry the economically or physically interesting content, and quantities computed from their tail — cumulative effects, long-run multipliers — are the least well determined parts of a fitted model."],
  "q": "Why is a long-run multiplier less reliably estimated than a one-step forecast from the same model?",
  "answer": "Because it depends on the whole tail of the impulse-response sequence while a one-step forecast depends only on its beginning. The one-step forecast error is σ² for any of these models — it uses ψ₀ alone — whereas the cumulative multiplier Σψⱼ sums every weight, including those at lags where a finite sample contains very little information. Small differences in the estimated coefficients compound in the tail: an AR(1) with φ = 0.7 gives 3.33 and one with φ = 0.8 gives 5.0, a 50% difference from a coefficient change the data may barely resolve. The effect is extreme near a unit root, where 1/(1 − φ) diverges and φ̂ = 0.95 against 0.98 gives 20 against 50. So the quantity should be reported with model uncertainty included, not with a confidence interval from one fitted model."},
 "ask": {
  "q": "For a random walk the weights are ψⱼ = 1 for every j. What does that say about the response to a shock, and about stationarity?",
  "nudge": "Does the echo ever fade? And is Σψⱼ² finite?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Weights and the ACF they produce",
 "objective": "See the autocovariance as an overlap of the weight sequence with itself.",
 "viz": {"type": "ar-acf", "p1": 0.7, "p2": 0.0,
         "caption": "An AR(1) with φ = 0.7. Its ψ weights are 0.7ʲ, and every autocorrelation shown can be obtained by overlapping that sequence with a shifted copy of itself."},
 "body": [
  "At φ = 0.7 the ACF reads 0.700, 0.490, 0.343, 0.240. Those come from the weights in a specific way: γₖ = σ²Σⱼ ψⱼψⱼ₊ₖ, the inner product of the weight sequence with itself shifted by k.",
  "Check it at k = 0. With ψⱼ = 0.7ʲ the sum Σ(0.7ʲ)² = Σ0.49ʲ = 1/(1 − 0.49) = 1.9608. Computed directly over four thousand terms: 1.960784, matching to six decimals. That is γ₀.",
  "At k = 1 the sum is Σ0.7ʲ × 0.7^(j+1) = 0.7Σ0.49ʲ = 0.7 × 1.9608 = 1.3725. Computed: 1.372549. So ρ₁ = 1.3725/1.9608 = 0.7 = φ, as topic 7.4 derived by the other route.",
  "The general pattern for this case is γₖ = φᵏ/(1 − φ²), verified at φ = 0.5, 0.7 and 0.8 and at lags 0 through 3 — every value agreeing to six decimals with the direct sum over the weights. Two independent derivations of the same autocovariance function.",
  "Now set φ₁ = 0, φ₂ = 0 for white noise. The weight sequence is ψ₀ = 1 and nothing else, so the overlap at any k ≥ 1 is zero — a flat ACF, as the chart shows. The overlap formula makes the cut-off in a finite MA's ACF obvious too: once the shift exceeds the length of the weight sequence there is nothing left to overlap."],
 "ask": {
  "q": "The overlap formula makes an MA(q)'s ACF cut off after lag q. Say why in one sentence.",
  "nudge": "What happens when you shift a sequence of length q+1 by more than q?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The general process, its moments, and Wold's theorem",
 "objective": "State all three precisely.",
 "blocks": [
  {"t": "formula", "h": "The general linear process",
   "body": "    yₜ = μ + Σ(j≥0) ψⱼ εₜ₋ⱼ,   ψ₀ = 1,   Σψⱼ² < ∞,\nwith {εₜ} white noise: mean 0, variance σ², uncorrelated across time. The sum is ONE-SIDED — past and present shocks only. The normalisation ψ₀ = 1 fixes the scale, since otherwise ψ and σ could be traded against each other."},
  {"t": "formula", "h": "Its mean and autocovariances",
   "body": "    E(yₜ) = μ\n    γₖ = σ² Σ(j≥0) ψⱼ ψⱼ₊ₖ,   and in particular  γ₀ = σ² Σψⱼ².\nThe autocovariance at lag k is the inner product of the weight sequence with itself shifted by k. Square-summability is exactly the condition for γ₀ to be finite, which stationarity requires."},
  {"t": "step", "h": "The special cases",
   "body": "AR(1): ψⱼ = φʲ, giving γₖ = σ²φᵏ/(1 − φ²) — verified to six decimals against the direct sum at φ = 0.5, 0.7 and 0.8 for k = 0 to 3.\nMA(1), minus convention: ψ₀ = 1, ψ₁ = −θ, rest zero, giving γ₀ = σ²(1 + θ²), γ₁ = −θσ², γₖ = 0 beyond.\nARMA(1,1): ψ₀ = 1 and ψⱼ = φ^(j−1)(φ − θ) for j ≥ 1.\nRandom walk: ψⱼ = 1 for all j, so Σψⱼ² diverges — not stationary, as topic 7.6 shows."},
  {"t": "def", "h": "Deterministic and purely non-deterministic",
   "body": "A component is DETERMINISTIC if it is perfectly predictable from its own infinite past, with zero forecast error — a constant, or a sinusoid with fixed amplitude and phase. A process with no such component is PURELY NON-DETERMINISTIC, meaning the one-step forecast error variance from the infinite past is strictly positive."},
  {"t": "formula", "h": "The Wold decomposition",
   "body": "Every weakly stationary process yₜ can be written uniquely as\n    yₜ = dₜ + Σ(j≥0) ψⱼ εₜ₋ⱼ,\nwhere dₜ is deterministic, the second term is a general linear process with ψ₀ = 1 and Σψⱼ² < ∞, and the εₜ are uncorrelated with mean 0 and variance σ² and are uncorrelated with dₜ. If the process is purely non-deterministic, dₜ is just the mean and the MA(∞) term is the whole process."},
  {"t": "def", "h": "What the theorem does and does not say",
   "body": "It says the LINEAR structure of any stationary process is an MA(∞) — so modelling with AR, MA and ARMA forms is modelling particular weight sequences, not choosing among rival shapes. It does NOT say the εₜ are independent or Gaussian, only uncorrelated, so a Wold representation captures second-moment structure and may leave non-linear dependence untouched. Nor is it constructive: the theorem guarantees the weights exist without providing them."}],
 "table": {
  "caption": "ψ weights and autocovariances for the standard models, σ² = 1. AR(1) figures computed directly from the weight sums over 4,000 terms.",
  "head": ["process", "ψⱼ", "γ₀", "γ₁", "Σψⱼ (long-run effect)"],
  "rows": [
   ["white noise", "1, 0, 0, …", "1", "0", "1"],
   ["AR(1), φ=0.5", "0.5ʲ", "1.333333", "0.666667", "2.00"],
   ["AR(1), φ=0.7", "0.7ʲ", "1.960784", "1.372549", "3.33"],
   ["AR(1), φ=0.8", "0.8ʲ", "2.777778", "2.222222", "5.00"],
   ["MA(1), θ=0.5", "1, −0.5, 0, …", "1.25", "−0.5", "0.50"],
   ["MA(1), θ=0.7", "1, −0.7, 0, …", "1.49", "−0.7", "0.30"],
   ["random walk", "1, 1, 1, …", "divergent", "divergent", "divergent"]]},
 "flow": {
  "title": "Where the Wold decomposition sits",
  "alt": "Flow chart showing the Wold decomposition of a stationary process",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "A weakly stationary process", "kind": "start"},
   {"id": "b", "r": 1, "c": 1, "label": "Wold: split into deterministic + shock-driven parts", "kind": "step"},
   {"id": "c", "r": 2, "c": 0, "label": "dₜ: perfectly predictable (constant, fixed sinusoid)", "kind": "end"},
   {"id": "d", "r": 2, "c": 2, "label": "Σψⱼεₜ₋ⱼ with ψ₀ = 1, Σψⱼ² < ∞", "kind": "step"},
   {"id": "e", "r": 3, "c": 2, "label": "AR, MA and ARMA are parameterisations of this", "kind": "end"},
   {"id": "f", "r": 4, "c": 1, "label": "ε uncorrelated, NOT necessarily independent", "kind": "note"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "b", "to": "c"}, {"from": "b", "to": "d"},
   {"from": "d", "to": "e"}, {"from": "e", "to": "f"}, {"from": "c", "to": "f"}],
  "note": "The theorem is an existence result about second-moment structure. It neither constructs the weights nor rules out non-linear dependence in the shocks."},
 "ask": {
  "q": "Wold guarantees the weights exist but does not produce them. What practical activity does that leave to be done?",
  "nudge": "What is model fitting, in this language?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked — autocovariances from the weights",
 "objective": "Compute γₖ by overlap and check against the model-equation route.",
 "ask": {
  "q": "Which route would you choose for an ARMA(1,1), and why?",
  "nudge": "Which one needs the whole weight sequence?"},
 "problem": "For an AR(1) with φ = 0.7 and σ² = 1: (a) give the ψ weights, (b) compute γ₀ and γ₁ by the overlap formula, (c) confirm against topic 7.4's results, (d) give the long-run effect of a unit shock.",
 "steps": [
  {"say": "(a) The weights.",
   "math": "yₜ = 0.7yₜ₋₁ + εₜ\nsubstituting repeatedly: yₜ = εₜ + 0.7εₜ₋₁ + 0.49εₜ₋₂ + 0.343εₜ₋₃ + ⋯\n⟹ ψⱼ = 0.7ʲ",
   "why": "Topic 7.1's expansion. Read as an impulse response: a unit shock contributes 1 now, 0.7 next period, 0.49 after that — about 34% still present three periods on."},
  {"say": "(b) γ₀ by overlap.",
   "math": "γ₀ = σ²Σψⱼ² = Σ(0.7ʲ)² = Σ(0.49)ʲ\n    = 1/(1 − 0.49) = 1/0.51 = 1.960784",
   "why": "A geometric series in 0.49. Computed directly over four thousand terms: 1.960784 — agreement to six decimals. Note the condition: the series converges exactly when φ² < 1, which is the stationarity condition."},
  {"say": "γ₁ by overlap.",
   "math": "γ₁ = σ²Σψⱼψⱼ₊₁ = Σ(0.7ʲ)(0.7^(j+1))\n    = 0.7 Σ(0.49)ʲ = 0.7 × 1.960784 = 1.372549",
   "why": "The shifted sequence is 0.7 times the original, so the whole sum picks up one factor of φ. Computed: 1.372549 ✓. The general result γₖ = φᵏ/(1 − φ²) follows the same way, since shifting by k multiplies by φᵏ."},
  {"say": "(c) Checking against topic 7.4.",
   "math": "topic 7.4: γ₀ = σ²/(1 − φ²) = 1/0.51 = 1.960784 ✓\n           ρ₁ = φ = 0.7\noverlap:   ρ₁ = γ₁/γ₀ = 1.372549/1.960784 = 0.700000 ✓",
   "why": "Two entirely independent derivations — one multiplying the model equation by yₜ₋ₖ and taking expectations, the other summing products of weights — give the same numbers. That agreement is the content of the claim that the two representations describe one process."},
  {"say": "(d) The long-run effect.",
   "math": "Σψⱼ = Σ0.7ʲ = 1/(1 − 0.7) = 1/0.3 = 3.3333",
   "why": "So a unit shock raises the level by 3.33 in cumulative terms. Note this is Σψⱼ, not Σψⱼ², and it is a different quantity from the variance: 3.33 against 1.96. Confusing the two is a natural error, since both are sums over the weights."},
  {"say": "A note on which route is easier.",
   "math": "AR(1):  model-equation route is quicker (two lines)\nMA(q):  overlap route is quicker (finite sum)\nARMA:   model-equation route, since ψⱼ must be derived first",
   "why": "For an MA the weights ARE the coefficients, so the overlap is a short finite sum. For an AR or ARMA the weights have to be derived before the overlap can be computed, so multiplying through and taking expectations is faster. The overlap formula's value is conceptual as much as computational."}],
 "after": "Answering the question above: for an ARMA(1,1) the model-equation route of topic 7.4, because the ψ weights φ^(j−1)(φ − θ) must be derived before any overlap can be summed. The overlap formula's importance is that it holds for EVERY stationary process, which is what Wold's theorem delivers."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the statements before the theorem's fine print.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "Write the general linear process with its two conditions.",
   "a": "yₜ = μ + Σψⱼεₜ₋ⱼ with ψ₀ = 1 and Σψⱼ² < ∞, the sum one-sided over past and present shocks."},
  {"q": "Give γₖ in terms of the weights.",
   "a": "γₖ = σ²Σⱼψⱼψⱼ₊ₖ — the overlap of the weight sequence with its shift by k."},
  {"q": "State the Wold decomposition.",
   "a": "Every weakly stationary process is uniquely a deterministic component plus a one-sided MA(∞) in uncorrelated shocks."},
  {"q": "What are the ψ weights of an AR(1), and what is γ₀?",
   "a": "ψⱼ = φʲ, giving γ₀ = σ²/(1 − φ²) — 1.9608 at φ = 0.7."},
  {"q": "What does the weight sequence mean physically?",
   "a": "The impulse response: the path the process traces after a single unit shock."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — five parts",
 "objective": "Work the weights and the two sums.",
 "problem": "Take σ² = 1 throughout.",
 "steps": [
  {"say": "An AR(1) with φ = 0.8.",
   "blank": {"prompt": "Give ψ₂ and γ₀.",
             "answer": "ψ₂ = 0.64; γ₀ = 1/0.36 = 2.7778",
             "accept": ["0.64 and 2.7778", "0.64, 2.778", "0.64 / 2.78"],
             "hint": "ψⱼ = φʲ and γ₀ = σ²Σψⱼ²."},
   "why": "ψ₂ = 0.8² = 0.64, and Σ(0.64)ʲ = 1/0.36 = 2.777778 — matching the direct computation to six decimals. A shock still has 64% of its force two periods later."},
  {"say": "The same AR(1), the long-run effect.",
   "blank": {"prompt": "Give Σψⱼ.",
             "answer": "1/(1 − 0.8) = 5",
             "accept": ["5", "5.0", "five"],
             "hint": "A geometric series in φ, not φ²."},
   "why": "Note the contrast with γ₀ = 2.78: Σψⱼ = 5 while Σψⱼ² = 2.78. The first is the cumulative effect on the level, the second the variance. They are different sums over the same weights."},
  {"say": "An MA(2) with yₜ = εₜ − 0.6εₜ₋₁ + 0.2εₜ₋₂.",
   "blank": {"prompt": "Give the ψ weights and γ₀.",
             "answer": "ψ = (1, −0.6, 0.2); γ₀ = 1 + 0.36 + 0.04 = 1.40",
             "accept": ["1, -0.6, 0.2 and 1.40", "(1,-0.6,0.2), 1.4"],
             "hint": "For an MA the weights ARE the coefficients, read off the equation."},
   "why": "Reading the signs off the equation as written: ψ₁ = −0.6 and ψ₂ = +0.2. Then γ₀ = Σψⱼ² = 1 + 0.36 + 0.04 = 1.40. Four non-zero overlaps only, so the arithmetic is finite."},
  {"say": "The same MA(2), its lag-1 autocovariance.",
   "blank": {"prompt": "Give γ₁ by the overlap formula.",
             "answer": "ψ₀ψ₁ + ψ₁ψ₂ = (1)(−0.6) + (−0.6)(0.2) = −0.72",
             "accept": ["-0.72", "−0.72", "-0.72 sigma^2"],
             "hint": "Overlap the sequence with its shift by one: only two products survive."},
   "why": "Two products, since ψ₃ onwards are zero. And γ₂ = ψ₀ψ₂ = 0.2, with γ₃ = 0 — the cut-off after lag 2, which the overlap formula makes immediate."},
  {"say": "A process with ψⱼ = 1 for all j.",
   "blank": {"prompt": "Is it a valid general linear process? Why?",
             "answer": "No — Σψⱼ² diverges, so the variance is infinite and it is not stationary",
             "accept": ["no, not square summable", "no — divergent", "no, infinite variance"],
             "hint": "Check the square-summability condition."},
   "why": "This is the random walk, where a shock never decays. Σψⱼ² = Σ1 diverges, so γ₀ is infinite and the process fails stationarity — topic 7.6's result, recovered here from the weights. The Wold theorem applies to stationary processes only, so it says nothing about this case."}],
 "after": "The structure to carry: for an MA the weights are the coefficients and the overlap sums are finite; for an AR they are φʲ and the sums are geometric; Σψⱼ² is the variance while Σψⱼ is the long-run effect; and a weight sequence that does not decay fast enough describes no stationary process at all."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "The theorem's fine print",
 "objective": "Know what Wold does not give you.",
 "blocks": [
  {"t": "step", "h": "Uncorrelated, not independent",
   "body": "The Wold shocks are uncorrelated with mean zero and constant variance — nothing more. They need not be independent, and need not be identically distributed. So a Wold representation captures all the LINEAR dependence in a process and may leave non-linear dependence entirely unaccounted for. A series whose level is unpredictable but whose volatility clusters has a perfectly good Wold representation with white-noise shocks that are plainly not independent."},
  {"t": "step", "h": "Why that matters",
   "body": "It explains how a model can pass every linear diagnostic and still miss something important. Financial returns are the standard case: close to uncorrelated, so the Wold weights are nearly trivial, yet their squares are strongly autocorrelated. Modelling that requires leaving the linear framework, which is what the ARCH and GARCH families do. Nothing in Wold is violated; the theorem simply was never about that structure."},
  {"t": "step", "h": "Existence, not construction",
   "body": "The theorem guarantees the weights exist. It does not say what they are, and for an arbitrary stationary process there is no formula. Fitting an ARMA model is choosing a parsimonious parametric family for the weight sequence and estimating within it — which is why finite ARMA models matter even though the general form is MA(∞): they make an infinite object estimable from finite data."},
  {"t": "step", "h": "The deterministic part is usually dropped",
   "body": "In applied work dₜ is taken to be a constant, so the process is assumed purely non-deterministic apart from its mean. A genuine deterministic sinusoid — a tide, a precisely periodic physical cycle — would belong in dₜ, and treating it as part of the stochastic term would be a specification error. Topic 7.7's spectral view distinguishes them: a deterministic sinusoid gives a spectral line at a single frequency, not a continuous density."},
  {"t": "def", "h": "Invertibility revisited",
   "body": "Topic 7.1's invertibility condition is what lets the Wold representation be inverted into an AR(∞), εₜ = Σπⱼyₜ₋ⱼ, which is the form forecasting needs because it expresses the shock through observables. So the two one-sided infinite representations — MA(∞) from Wold, AR(∞) from invertibility — are the two faces of the same process, and topic 7.11 builds forecasts on the second."}],
 "ask": {
  "q": "A series of financial returns is nearly uncorrelated but its squared values are strongly autocorrelated. Does that contradict Wold?",
  "nudge": "What kind of dependence does the theorem speak about?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — four parts",
 "objective": "Derive weights and compute both sums.",
 "problem": "(a) For an ARMA(1,1) with φ = 0.6 and θ = 0.2 under the minus convention, give ψ₀, ψ₁, ψ₂ and Σψⱼ. (b) For an AR(1) with φ = 0.95, give Σψⱼ² and Σψⱼ. (c) Verify that γₖ = σ²Σψⱼψⱼ₊ₖ reproduces γ₁ = −θσ² for an MA(1). (d) Explain why ψ₀ = 1 is imposed.",
 "hints": [
  "For (a), ψⱼ = φ^(j−1)(φ − θ) for j ≥ 1.",
  "For (b), the two sums are geometric in φ² and in φ.",
  "For (c), the weight sequence has only two non-zero terms."],
 "answer": "(a) 1, 0.4, 0.24; Σψⱼ = (1 − θ)/(1 − φ) = 0.8/0.4 = 2. (b) Σψⱼ² = 10.2564 and Σψⱼ = 20. (c) ψ₀ψ₁ = (1)(−θ) = −θ, with no further overlaps. (d) It fixes the scale, since ψ and σ could otherwise be traded against each other.",
 "check": "In (b) note how different the two sums are at φ = 0.95: the variance factor is 10.26 but the long-run multiplier is 20 — and at φ = 0.99 they are 50.25 and 100. Both diverge as φ approaches 1, but at different rates, since one is geometric in φ² and the other in φ. In (a) the check is that setting θ = 0 must recover the AR(1) weights φʲ, which it does: ψⱼ = φ^(j−1)(φ) = φʲ.",
 "scenario": {
  "teaser": "A model passes every autocorrelation test and still fails in use.",
  "title": "What a Wold representation cannot see",
  "body": [
   "A series of daily returns is modelled. The sample ACF is flat, the PACF is flat, a portmanteau test on the residuals passes comfortably, and the fitted model is essentially white noise with a small mean. By every linear diagnostic the model is correct, and in a sense it is: the Wold representation of this process really does have ψⱼ ≈ 0 for j ≥ 1.",
   "The model is then used to set a risk limit, and performs badly. Quiet periods see the limit set far too wide and turbulent periods see it breached repeatedly. Nothing in the fitting was wrong.",
   "What was missed is that the squared returns are strongly autocorrelated — a large move today makes a large move tomorrow likely, in magnitude though not in direction. That is dependence in the second moment of the shocks, and the Wold theorem says nothing about it. Wold's εₜ are required to be uncorrelated, not independent, and a sequence can be uncorrelated while its squares are highly correlated.",
   "So the model's linear structure was right and its implicit assumption of constant variance was wrong. The diagnostic that would have found it is to compute the ACF of the SQUARED residuals, which is the standard check for this and takes one line.",
   "The repair is outside the linear framework: a model for the conditional variance, which is what the ARCH family provides. The level equation can stay as it is, because Wold already told us the linear part was adequate.",
   "The general point is worth keeping. Wold is an extremely strong theorem about linear structure, and its strength can be mistaken for completeness. A model that satisfies every implication of Wold has got the second-moment structure of the process right and may still be missing the thing the data are being used for."],
  "q": "Why does a flat residual ACF not establish that a model has captured the dependence in a series?",
  "answer": "Because the ACF measures only linear dependence, and that is also all the Wold theorem concerns. Wold's shocks are required to be uncorrelated, not independent, so a process can have a perfectly adequate Wold representation — flat ACF, flat PACF, residuals passing a portmanteau test — while its shocks remain strongly dependent in ways no autocorrelation detects. The standard case is volatility clustering, where the returns themselves are nearly uncorrelated but their squares are not, so large moves cluster in time. The check is to compute the ACF of the squared residuals; structure there indicates conditional heteroskedasticity, which requires a model for the variance such as ARCH or GARCH rather than any change to the linear part. A flat residual ACF establishes that the linear structure is adequate, and nothing beyond that."},
 "solution": [
  {"say": "(a) The ARMA(1,1) weights.",
   "math": "ψ₀ = 1\nψ₁ = φ − θ = 0.6 − 0.2 = 0.4\nψ₂ = φ(φ − θ) = 0.6(0.4) = 0.24\nΣψⱼ = 1 + 0.4/(1 − 0.6) = 1 + 1 = 2\nalso (1 − θ)/(1 − φ) = 0.8/0.4 = 2 ✓",
   "why": "Two routes to the cumulative sum agree. Setting θ = 0 recovers ψⱼ = φʲ, the AR(1) case, which is the check that the general formula is right."},
  {"say": "(b) The persistent AR(1).",
   "math": "Σψⱼ² = 1/(1 − 0.9025) = 1/0.0975 = 10.2564\nΣψⱼ  = 1/(1 − 0.95) = 1/0.05 = 20",
   "why": "Both computed directly and confirmed. The variance is 10.26σ² while the long-run multiplier is 20 — a reminder that Σψⱼ² and Σψⱼ are different quantities. At φ = 0.99 they become 50.25 and 100."},
  {"say": "(c) The MA(1) overlap.",
   "math": "ψ = (1, −θ, 0, 0, …)\nγ₁ = σ²(ψ₀ψ₁ + ψ₁ψ₂ + ⋯) = σ²[(1)(−θ) + (−θ)(0) + ⋯]\n   = −θσ² ✓\nγ₂ = σ²ψ₀ψ₂ = 0 ✓",
   "why": "Only one product survives at lag 1 and none at lag 2, which recovers the standard MA(1) autocovariances. The cut-off is immediate from the overlap: shifting a two-term sequence by two leaves no overlap at all."},
  {"say": "(d) Why ψ₀ = 1.",
   "math": "replacing (ψⱼ, σ) by (cψⱼ, σ/c) leaves every γₖ = σ²Σψⱼψⱼ₊ₖ unchanged\n⟹ the pair is not identified without a normalisation",
   "why": "Exactly the non-identifiability of topic 7.1, in general form. Fixing ψ₀ = 1 picks one representative, making the weights and the shock variance separately meaningful. It also makes ψⱼ an impulse response to a UNIT shock, which is the interpretation of section 1."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims this topic turns on.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "The Wold decomposition requires the shocks to be independent.",
   "tf": False,
   "why": "False — only UNCORRELATED, with mean zero and constant variance. That is why a Wold representation captures linear dependence and can leave non-linear dependence untouched: financial returns are nearly uncorrelated with strongly autocorrelated squares, and nothing in the theorem is violated."},
  {"claim": "The weights of a general linear process must satisfy Σψⱼ² < ∞.",
   "tf": True,
   "why": "True, and the reason is immediate: γ₀ = σ²Σψⱼ², so the sum must converge for the variance to be finite. For an AR(1) it is 1/(1 − φ²), finite exactly when |φ| < 1 — so square-summability IS the stationarity condition in that case."},
  {"claim": "A random walk is a general linear process.",
   "tf": False,
   "why": "False. Its weights are ψⱼ = 1 for every j, so Σψⱼ² diverges and the variance is infinite — it is not stationary, which is topic 7.6's result recovered from the weights. The Wold theorem applies to stationary processes, so it says nothing about this case."},
  {"claim": "The autocovariance of a general linear process is γₖ = σ²Σⱼψⱼψⱼ₊ₖ.",
   "tf": True,
   "why": "True — the inner product of the weight sequence with its shift by k. Verified against the closed form φᵏ/(1 − φ²) for an AR(1) at φ = 0.5, 0.7 and 0.8, agreeing to six decimals at every lag from 0 to 3. It also makes a finite MA's cut-off immediate, since a shift beyond the sequence's length leaves no overlap."},
  {"claim": "Σψⱼ and Σψⱼ² are the same quantity.",
   "tf": False,
   "why": "False and worth keeping distinct. Σψⱼ² scaled by σ² is the VARIANCE, while Σψⱼ is the cumulative long-run effect of a unit shock. At φ = 0.8 they are 2.78 and 5; at φ = 0.95, 10.26 and 20; at φ = 0.99, 50.25 and 100. Both diverge near a unit root, at different rates."},
  {"claim": "Wold's theorem makes finite ARMA models unnecessary.",
   "tf": False,
   "why": "False — it makes them necessary. The theorem is an existence result: it guarantees the weights exist without providing them, and an infinite sequence cannot be estimated from finite data. A finite ARMA model is a parsimonious parametric family for the weight sequence, which is what makes the general form usable."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 8,
 "title": "On your own — six quick values",
 "objective": "Compute at exam speed.",
 "problem": "σ² = 1 throughout. (a) AR(1), φ = 0.6: ψ₃. (b) Same: γ₀ and Σψⱼ. (c) MA(1), θ = 0.7: γ₀ and γ₁. (d) MA(3) with ψ = (1, −0.5, 0.3, −0.1): γ₀. (e) The same MA(3): γ₃. (f) ARMA(1,1), φ = 0.5, θ = 0.5: ψ₁ and Σψⱼ.",
 "hints": [
  "For (d), sum the squares of all four weights.",
  "For (e), only one product survives at lag 3.",
  "For (f), what is φ − θ here?"],
 "answer": "(a) 0.216. (b) γ₀ = 1/0.64 = 1.5625 and Σψⱼ = 2.5. (c) γ₀ = 1.49, γ₁ = −0.7. (d) 1 + 0.25 + 0.09 + 0.01 = 1.35. (e) ψ₀ψ₃ = −0.1. (f) ψ₁ = 0, and Σψⱼ = 1.",
 "check": "Part (f) is the instructive case: φ = θ makes every weight beyond ψ₀ vanish, since ψⱼ = φ^(j−1)(φ − θ) = 0. So the process is white noise — the AR and MA parts cancel exactly, which is the common-factor case. Its ACF is flat and Σψⱼ = 1, consistent with (1 − θ)/(1 − φ) = 0.5/0.5 = 1. An ARMA(1,1) with equal coefficients is over-parameterised white noise, and a fitting routine given such data will struggle to identify either coefficient.",
 "solution": [
  {"say": "(a) and (b): the AR(1).",
   "math": "ψ₃ = 0.6³ = 0.216\nγ₀ = 1/(1 − 0.36) = 1.5625\nΣψⱼ = 1/(1 − 0.6) = 2.5",
   "why": "The two sums again: 1.5625 for the variance (geometric in φ²) and 2.5 for the long-run effect (geometric in φ)."},
  {"say": "(c), (d) and (e): the MA cases.",
   "math": "MA(1) θ=0.7: γ₀ = 1 + 0.49 = 1.49, γ₁ = −0.7\nMA(3): γ₀ = 1 + 0.25 + 0.09 + 0.01 = 1.35\n       γ₃ = ψ₀ψ₃ = (1)(−0.1) = −0.1",
   "why": "For an MA the weights are the coefficients, so every overlap is a short finite sum. At lag 3 only ψ₀ψ₃ survives, and γ₄ = 0 — the cut-off."},
  {"say": "(f) The cancelling ARMA.",
   "math": "ψ₁ = φ − θ = 0.5 − 0.5 = 0\n⟹ ψⱼ = 0 for all j ≥ 1\n⟹ white noise, Σψⱼ = 1",
   "why": "A common factor between the AR and MA polynomials: (1 − 0.5B)yₜ = (1 − 0.5B)εₜ, so the factor cancels and yₜ = εₜ. Such a model is over-parameterised, and a fitting routine will find the two coefficients nearly unidentified."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "What the theorem underwrites elsewhere",
 "objective": "See the module's results as consequences.",
 "blocks": [
  {"t": "step", "h": "The duality of topic 7.1",
   "body": "That topic showed a stationary AR(1) is an MA(∞) and an invertible MA(1) is an AR(∞), case by case. Wold is the general statement of the first half: every stationary process is an MA(∞). Invertibility supplies the second half, giving the AR(∞) form εₜ = Σπⱼyₜ₋ⱼ that expresses the shock through observables."},
  {"t": "step", "h": "Forecasting (topic 7.11)",
   "body": "The minimum mean-squared-error forecast of yₜ₊ₖ from the infinite past is Σ(j≥k)ψⱼεₜ₊ₖ₋ⱼ, the part of the representation already determined at time t, and the forecast error variance is σ²Σ(j<k)ψⱼ². So the ψ weights give both the forecast and its uncertainty at every horizon — the Wold form is the natural language for forecasting."},
  {"t": "step", "h": "The spectrum (topic 7.7)",
   "body": "The spectral density of a general linear process is f(ω) = (σ²/2π)|ψ(e^(−iω))|², where ψ(B) = Σψⱼ Bʲ. So the weights determine the spectrum directly, and the deterministic component of the Wold decomposition shows up as a spectral LINE at a single frequency rather than as part of the continuous density — which is how the two parts are told apart in the frequency domain."},
  {"t": "step", "h": "Ergodicity (topic 7.9)",
   "body": "The long-run variance Σγₖ equals σ²(Σψⱼ)², so the long-run multiplier and the precision of the sample mean are the same quantity seen twice. At φ = 0.8 that gives 5² = 25, matching topic 7.9's figure exactly. Absolute summability of the weights, Σ|ψⱼ| < ∞, is what guarantees it is finite."},
  {"t": "def", "h": "Why it is the keystone",
   "body": "Because it says the module is not a collection of model families to choose between but a set of parameterisations of one general form. Identification picks the shape of the weight sequence, estimation pins down its parameters, forecasting reads off its tail, and the spectrum is its Fourier transform. One object, four views."}],
 "ask": {
  "q": "The long-run variance is σ²(Σψⱼ)². At φ = 0.8 that is 25, which topic 7.9 also gave. What does the coincidence tell you?",
  "nudge": "Were the two computed from the same information?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the conditions and the fine print.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Give the ψ weights of an ARMA(1,1) under the minus convention.",
   "a": "ψ₀ = 1 and ψⱼ = φ^(j−1)(φ − θ) for j ≥ 1, so Σψⱼ = (1 − θ)/(1 − φ)."},
  {"q": "What does the Wold theorem assume about the shocks?",
   "a": "Uncorrelated, mean zero, constant variance — not independent and not Gaussian."},
  {"q": "What is the difference between Σψⱼ and Σψⱼ²?",
   "a": "σ²Σψⱼ² is the variance; Σψⱼ is the cumulative long-run effect of a unit shock."},
  {"q": "Why is ψ₀ = 1 imposed?",
   "a": "To fix the scale: replacing (ψⱼ, σ) by (cψⱼ, σ/c) leaves every autocovariance unchanged."},
  {"q": "Is the Wold theorem constructive?",
   "a": "No — it guarantees the weights exist without producing them, which is why finite ARMA families are needed."},
  {"q": "Give the spectral density of a general linear process.",
   "a": "f(ω) = (σ²/2π)|ψ(e^(−iω))|², with ψ(B) = Σψⱼ Bʲ."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Write the general linear process with ψ₀ = 1 and Σψⱼ² < ∞, and say why each is imposed.",
  "Compute γₖ as the overlap σ²Σψⱼψⱼ₊ₖ and use it on AR, MA and ARMA cases.",
  "Give the ψ weights of an AR(1), an MA(q) and an ARMA(1,1).",
  "Distinguish Σψⱼ² from Σψⱼ and say what each measures.",
  "State the Wold decomposition, including the deterministic component.",
  "Say that the shocks are uncorrelated but need not be independent, and why that matters.",
  "Read the weights as an impulse response and the long-run multiplier from their sum.",
  "Explain why finite ARMA models remain necessary despite the general result."]},)

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "Deriving the ARMA weights, and the common-factor trap",
 "objective": "See where φ^(j−1)(φ − θ) comes from.",
 "blocks": [
  {"t": "step", "h": "Setting up",
   "body": "An ARMA(1,1) under the minus convention is (1 − φB)yₜ = (1 − θB)εₜ. The Wold weights are the coefficients of the power series ψ(B) = (1 − θB)/(1 − φB), so the task is to expand that ratio."},
  {"t": "formula", "h": "The expansion",
   "body": "    (1 − θB)/(1 − φB) = (1 − θB)(1 + φB + φ²B² + ⋯)\n                      = 1 + (φ − θ)B + (φ² − φθ)B² + (φ³ − φ²θ)B³ + ⋯\nso ψ₀ = 1 and ψⱼ = φ^(j−1)(φ − θ) for j ≥ 1. The geometric expansion of 1/(1 − φB) needs |φ| < 1, which is the stationarity condition."},
  {"t": "step", "h": "The cumulative sum",
   "body": "Σψⱼ = ψ(1) = (1 − θ)/(1 − φ), obtained by setting B = 1 — valid when the series converges. At φ = 0.6, θ = 0.2 that is 0.8/0.4 = 2, matching the term-by-term sum 1 + 0.4 + 0.24 + 0.144 + ⋯ = 1 + 0.4/0.4 = 2. Setting θ = 0 recovers 1/(1 − φ), the AR(1) multiplier."},
  {"t": "step", "h": "The common-factor trap",
   "body": "If φ = θ the numerator and denominator share the factor (1 − φB), which cancels: ψⱼ = φ^(j−1)(φ − φ) = 0 for every j ≥ 1, so yₜ = εₜ is white noise. An ARMA(1,1) with equal coefficients is over-parameterised white noise, and a fitting routine given such data cannot identify either coefficient — the likelihood is flat along the line φ = θ. Any shared root between the AR and MA polynomials causes the same thing, and checking for one is part of specifying an ARMA model."},
  {"t": "step", "h": "Why the weights decay geometrically",
   "body": "Beyond ψ₁ every weight is the previous one times φ, so the impulse response is a single exponential scaled by (φ − θ). That means an ARMA(1,1) and an AR(1) have the same SHAPE of response and differ only in its initial size — which is why they can be hard to distinguish in a short sample and why the long-run multipliers can nonetheless differ substantially, as section 1's scenario showed."}],
 "ask": {
  "q": "Any shared root between the AR and MA polynomials cancels. What should that make you check before reporting an ARMA fit?",
  "nudge": "Compare the estimated roots of the two polynomials."}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "timeseries_t10_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "timeseriest10",
 "topicId": "timeseries-t10",
 "moduleId": "timeseries",
 "title": "General Linear Process and Wold Decomposition",
 "breadcrumb": "Time series → Theory → The universal shape of a stationary process",
 "engine": "B",
 "engineName": "Time series — every stationary process is an infinite moving average",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Write the general linear process with ψ₀ = 1 and Σψⱼ² < ∞ and justify both conditions.",
  "Compute γₖ as the overlap σ²Σψⱼψⱼ₊ₖ for AR, MA and ARMA processes.",
  "Give the ψ weights of an AR(1), an MA(q) and an ARMA(1,1).",
  "Distinguish Σψⱼ² from Σψⱼ and say what each measures.",
  "State the Wold decomposition including its deterministic component.",
  "Explain why the shocks are only uncorrelated, and why finite ARMA models remain needed."],
 "prereq": [
  {"id": "p1", "name": "Stationarity and invertibility (topic 7.1)",
   "why": "The AR(1)→MA(∞) expansion is the special case this lesson generalises, and invertibility gives the dual AR(∞) form."},
  {"id": "p2", "name": "Autocovariance of AR processes (topic 7.4)",
   "why": "The overlap formula is a second route to the same autocovariances, and the agreement is the lesson's main check."},
  {"id": "p3", "name": "Geometric series",
   "why": "Every weight sum in the lesson — Σψⱼ, Σψⱼ² and the ARMA expansion — is geometric."},
  {"id": "p4", "name": "White noise",
   "why": "The theorem's shocks are white noise in the weak sense: uncorrelated, not independent, which is the fine print that matters."}],
 "traps": [
  "The Wold shocks are UNCORRELATED, not independent — the theorem is about linear structure only.",
  "Σψⱼ² scaled by σ² is the variance; Σψⱼ is the long-run multiplier. They are different numbers.",
  "A random walk is NOT a general linear process: ψⱼ = 1 gives a divergent Σψⱼ².",
  "The theorem is an existence result and does not construct the weights.",
  "It does not make finite ARMA models unnecessary — it makes them necessary.",
  "ψ₀ = 1 is a normalisation, without which ψ and σ are not separately identified.",
  "An ARMA(1,1) with φ = θ is white noise — a shared root cancels.",
  "The sum is ONE-SIDED: past and present shocks only, never future ones."],
 "revision": {
  "sheet": [
   "GENERAL LINEAR PROCESS: yₜ = μ + Σ(j≥0) ψⱼεₜ₋ⱼ, with ψ₀ = 1 and Σψⱼ² < ∞.",
   "The sum is ONE-SIDED. The εₜ are white noise: mean 0, variance σ², uncorrelated.",
   "ψ₀ = 1 is a NORMALISATION: replacing (ψⱼ, σ) by (cψⱼ, σ/c) leaves every γₖ unchanged.",
   "γ₀ = σ²Σψⱼ², so square-summability is exactly what makes the variance finite.",
   "AUTOCOVARIANCE: γₖ = σ²Σ(j≥0) ψⱼψⱼ₊ₖ — the overlap of the weights with their shift by k.",
   "This makes an MA(q)'s cut-off obvious: shifting past the sequence's length leaves no overlap.",
   "AR(1): ψⱼ = φʲ, γₖ = σ²φᵏ/(1−φ²). Verified to 6 dp against the direct sum at φ = 0.5, 0.7, 0.8.",
   "  φ=0.7: γ₀ = 1.960784, γ₁ = 1.372549, γ₂ = 0.960784, γ₃ = 0.672549.",
   "MA(q): the weights ARE the coefficients. MA(1) minus convention: ψ = (1, −θ).",
   "  γ₀ = σ²(1+θ²), γ₁ = −θσ², γₖ = 0 beyond. At θ=0.7: 1.49 and −0.70.",
   "ARMA(1,1): ψ₀ = 1, ψⱼ = φ^(j−1)(φ − θ) for j ≥ 1. From expanding (1−θB)/(1−φB).",
   "RANDOM WALK: ψⱼ = 1 for all j, so Σψⱼ² diverges — not stationary, not a GLP.",
   "IMPULSE RESPONSE: ψⱼ is the effect on yₜ₊ⱼ of a unit shock at time t. The weights ARE that path.",
   "LONG-RUN MULTIPLIER Σψⱼ: 1/(1−φ) for an AR(1) — 3.33 at φ=0.7, 5 at 0.8, 20 at 0.95, 100 at 0.99.",
   "Σψⱼ² = 1/(1−φ²): 1.96 at 0.7, 2.78 at 0.8, 10.26 at 0.95, 50.25 at 0.99. DIFFERENT from Σψⱼ.",
   "ARMA(1,1) multiplier: Σψⱼ = (1−θ)/(1−φ).",
   "WOLD: every weakly stationary process = dₜ (deterministic) + Σψⱼεₜ₋ⱼ, uniquely.",
   "  dₜ is perfectly predictable from its own infinite past (a constant, a fixed sinusoid).",
   "  Purely non-deterministic ⟹ dₜ is just the mean and the MA(∞) is everything.",
   "FINE PRINT: shocks uncorrelated, NOT independent. Linear structure only.",
   "  So volatility clustering is consistent with Wold — check the ACF of SQUARED residuals.",
   "FINE PRINT: existence, not construction. ARMA families make the infinite object estimable.",
   "COMMON FACTOR: φ = θ in an ARMA(1,1) gives white noise — the polynomials share a root.",
   "Long-run variance (topic 7.9) = σ²(Σψⱼ)²: at φ=0.8 that is 25, matching 7.9 exactly.",
   "Spectral density (topic 7.7): f(ω) = (σ²/2π)|ψ(e^(−iω))|².",
   "Forecasting (topic 7.11): forecast error variance at horizon k is σ²Σ(j<k)ψⱼ²."],
  "cards": [
   ["General linear process", "yₜ = μ + Σψⱼεₜ₋ⱼ, ψ₀ = 1, Σψⱼ² < ∞"],
   ["γₖ from the weights", "σ²Σⱼψⱼψⱼ₊ₖ"],
   ["AR(1) weights", "ψⱼ = φʲ"],
   ["MA(1) weights, minus convention", "(1, −θ, 0, …)"],
   ["ARMA(1,1) weights", "ψⱼ = φ^(j−1)(φ − θ), j ≥ 1"],
   ["Variance", "σ²Σψⱼ²"],
   ["Long-run multiplier", "Σψⱼ = 1/(1−φ) for an AR(1)"],
   ["Wold decomposition", "Deterministic part + one-sided MA(∞)"],
   ["Wold's shocks are", "Uncorrelated, NOT independent"],
   ["Is Wold constructive?", "No — existence only"],
   ["Why ψ₀ = 1?", "Fixes the scale; ψ and σ else unidentified"],
   ["ARMA(1,1) with φ = θ", "White noise — shared root cancels"]],
  "tricks": [
   "For an MA, read the weights straight off the equation — they ARE the coefficients.",
   "For an AR or ARMA, derive the weights first; the model-equation route of 7.4 is usually quicker.",
   "Σψⱼ² is geometric in φ², Σψⱼ in φ. Keep the two sums apart.",
   "Setting θ = 0 in any ARMA formula must recover the AR result — a free check.",
   "Check for a shared root before reporting an ARMA fit; φ ≈ θ means over-parameterisation.",
   "A flat residual ACF establishes only that the LINEAR part is adequate."],
  "shortcuts": [
   "1/(1−φ) is 2, 2.5, 3.33, 5, 20 at φ = 0.5, 0.6, 0.7, 0.8, 0.95.",
   "1/(1−φ²) is 1.333, 1.563, 1.961, 2.778, 10.256 at the same values.",
   "σ²(Σψⱼ)² is the long-run variance: 25 at φ = 0.8."],
  "remember": [
   "Uncorrelated, not independent.",
   "Σψⱼ² is variance; Σψⱼ is the multiplier.",
   "Existence, not construction."]},
 "howto": "Section 1 gives the reading that makes the rest concrete: the ψ weights are the impulse response, the path the process traces after a single unit shock, so the whole apparatus is about how loudly past shocks still sound. Section 3 states the process, the overlap formula for the autocovariances, and the Wold theorem, and section 4 then computes γ₀ and γ₁ for an AR(1) by the overlap route and checks them against topic 7.4's model-equation route — two independent derivations agreeing to six decimals, which is the lesson's main verification. Section 7 is the fine print and is the part most likely to be examined conceptually: the shocks are uncorrelated and not independent, so the theorem is about linear structure alone, and it is an existence result that does not construct the weights. Those two qualifications explain both why volatility clustering is consistent with Wold and why finite ARMA models remain necessary. Section 6 and section 10 drill the weight computations, including the two different sums Σψⱼ² and Σψⱼ, which are easily conflated. If short of time, sections 1, 3 and 7 are the lesson. This topic deliberately does not repeat topic 7.4's derivations or topic 7.1's case-by-case duality, though it generalises the latter. The optional section expands (1 − θB)/(1 − φB) to get the ARMA weights and shows the common-factor trap, where φ = θ makes the process white noise.",
 "refs": [
  {"title": "Time Series Analysis", "where": "Chapter 4.8",
   "site": "Hamilton", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The Wold decomposition stated and proved, with the deterministic component and the uncorrelated-not-independent caveat made explicit."},
  {"title": "Time Series: Theory and Methods", "where": "Chapter 5.7",
   "site": "Brockwell and Davis", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The rigorous treatment, including the Hilbert-space argument and the role of square-summability."},
  {"title": "Time Series Analysis: Forecasting and Control", "where": "Chapter 3.1",
   "site": "Box, Jenkins and Reinsel", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The general linear process and the ψ weights as the basis of the ARIMA framework, with the ARMA expansion."},
  {"title": "Time Series Analysis", "where": "Weeks on linear processes",
   "site": "NPTEL / SWAYAM", "url": "https://archive.nptel.ac.in/courses/111104049",
   "type": "Video course", "free": True, "checked": "2026-11-03",
   "why": "Indian-syllabus treatment of the general linear process and the Wold representation."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026, the tenth lesson of the time-series module. No PYQ anchor of its own; it is the theoretical keystone, the theorem that says the MA(∞) form is not one modelling choice among several but the general shape of every stationary process. Scope was set against the lessons already built: topic 7.1 owns the admissible regions and the AR(1) expansion for that one case, which this lesson generalises; 7.4 owns the autocovariance computed from the model equation, where this lesson computes it from the weights instead; 7.7 owns the spectrum and 7.11 forecasting, both cross-referenced as consequences. The overlap formula γₖ = σ²Σψⱼψⱼ₊ₖ was verified by computing the sums directly over four thousand terms and comparing with the closed form σ²φᵏ/(1−φ²): at φ = 0.5 the values 1.333333, 0.666667, 0.333333 and 0.166667 at lags 0 to 3; at φ = 0.7, 1.960784, 1.372549, 0.960784 and 0.672549; at φ = 0.8, 2.777778, 2.222222, 1.777778 and 1.422222 — every figure agreeing to six decimal places. That agreement is the lesson's central check, since it confirms that the weight-overlap route and topic 7.4's model-equation route describe one process. Square-summability was confirmed as Σψⱼ² = 1/(1−φ²), giving 10.2564 at φ = 0.95 and 50.2513 at φ = 0.99 — large but finite, against the random walk's ψⱼ = 1 where the sum diverges. The lesson keeps Σψⱼ² and Σψⱼ carefully apart throughout, since both are sums over the weights and conflating them is the natural error: at φ = 0.8 they are 2.78 and 5, at φ = 0.95 they are 10.26 and 20. Two qualifications to the theorem are given their own section rather than being mentioned in passing, because both are conceptually examinable and both are commonly misremembered: the shocks are uncorrelated and need NOT be independent, so a Wold representation captures linear dependence and can leave volatility clustering entirely unmodelled; and the theorem is an existence result that does not construct the weights, which is precisely why finite ARMA families remain necessary rather than being superseded. The optional section derives the ARMA(1,1) weights by expanding (1 − θB)/(1 − φB) and ends with the common-factor trap, where φ = θ cancels and the process is white noise with both coefficients unidentified. Previous-year questions are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "ts-t10-m-%02d" % i, "format": fmt, "topic": "timeseries-t10",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "The general linear process is written:",
 ["yₜ = μ + Σ(j≥0) ψⱼεₜ₋ⱼ with ψ₀ = 1",
  "yₜ = μ + Σ(j≥0) ψⱼεₜ₊ⱼ",
  "yₜ = μ + Σ ψⱼyₜ₋ⱼ",
  "yₜ = μ + ψεₜ"],
 "A",
 "The sum is ONE-SIDED over past and present shocks — option B would use future shocks, which makes the process non-causal and useless for forecasting. Option C is an autoregression in y, not a linear process in the shocks."))

I.append(q(2, "numeric", "easy",
 "The condition the weights of a general linear process must satisfy is:",
 ["Σψⱼ² < ∞", "Σψⱼ = 1", "ψⱼ > 0 for all j", "Σψⱼ < ∞ only"],
 "A",
 "Square-summability, because γ₀ = σ²Σψⱼ² and the variance must be finite for stationarity. For an AR(1) the sum is 1/(1 − φ²), finite exactly when |φ| < 1, so the condition IS the stationarity condition in that case.",
 check="A random walk has ψⱼ = 1 for all j, so Σψⱼ² diverges — correctly ruling it out as non-stationary."))

I.append(q(3, "numeric", "easy",
 "The ψ weights of an AR(1) process with coefficient φ are:",
 ["ψⱼ = φʲ", "ψⱼ = φ", "ψⱼ = jφ", "ψⱼ = φ/j"],
 "A",
 "Substituting repeatedly into yₜ = φyₜ₋₁ + εₜ gives yₜ = Σφʲεₜ₋ⱼ. Read as an impulse response, a unit shock has effect 1 now, φ next period, φ² after that — geometric decay.",
 check="At φ = 0.7 the weights are 1, 0.7, 0.49, 0.343, so Σψⱼ² = 1/(1 − 0.49) = 1.9608, which is the AR(1) variance."))

I.append(q(4, "numeric", "easy",
 "The autocovariance at lag k of a general linear process is:",
 ["σ²Σⱼ ψⱼψⱼ₊ₖ", "σ²Σⱼ ψⱼ²", "σ²ψₖ", "σ²Σⱼ ψⱼ"],
 "A",
 "The inner product of the weight sequence with its shift by k. Option B is the special case k = 0, the variance. Verified to six decimals against σ²φᵏ/(1 − φ²) for an AR(1) at several φ and k.",
 check="At k = 0 the formula must reduce to σ²Σψⱼ², the variance, which it does."))

I.append(q(5, "single", "easy",
 "The Wold decomposition states that every weakly stationary process can be written as:",
 ["a deterministic component plus a one-sided infinite moving average of uncorrelated shocks",
  "a finite autoregression", "a finite moving average",
  "a sum of independent identically distributed terms"],
 "A",
 "The decomposition is unique, with the deterministic part perfectly predictable from its own infinite past and the second part a general linear process with ψ₀ = 1 and Σψⱼ² < ∞. Option D overstates it: the shocks are uncorrelated, not independent."))

I.append(q(6, "single", "easy",
 "The ψ weight sequence of a process can be interpreted as:",
 ["the impulse response — the path traced after a single unit shock",
  "the autocorrelation function", "the spectral density",
  "the sequence of forecast errors"],
 "A",
 "A unit shock at time t contributes ψ₀ to yₜ, ψ₁ to yₜ₊₁ and so on, so the weights literally are the response path. For an AR(1) with φ = 0.7 that response is 1, 0.7, 0.49, 0.343 — about 34% of the shock still present three periods later."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "For an AR(1) with φ = 0.7 and σ² = 1, the variance computed from the weights is:",
 ["1.9608", "3.3333", "0.7000", "1.4900"],
 "A",
 "γ₀ = Σψⱼ² = Σ(0.7ʲ)² = Σ0.49ʲ = 1/0.51 = 1.960784, confirmed by direct summation over 4,000 terms and matching topic 7.4's σ²/(1 − φ²). Option B is Σψⱼ = 1/(1 − 0.7) = 3.33, the long-run multiplier — a different sum over the same weights.",
 check="The variance must exceed σ² = 1 for any stationary AR process, and 1.96 does."))

I.append(q(8, "numeric", "moderate",
 "For an AR(1) with φ = 0.8, the cumulative long-run effect of a unit shock is:",
 ["5.0", "2.7778", "0.8", "25"],
 "A",
 "Σψⱼ = Σ0.8ʲ = 1/(1 − 0.8) = 5. Option B is Σψⱼ² = 1/(1 − 0.64) = 2.7778, the variance; option D is the long-run VARIANCE σ²(Σψⱼ)² = 25. All three are sums over the same weights and must be kept apart.",
 check="Σψⱼ must exceed Σψⱼ² here, since each weight 0.8ʲ is below 1 and squaring shrinks it: 5 against 2.7778 ✓."))

I.append(q(9, "numeric", "moderate",
 "The ψ weights of an ARMA(1,1) with yₜ − φyₜ₋₁ = εₜ − θεₜ₋₁ are:",
 ["ψ₀ = 1 and ψⱼ = φ^(j−1)(φ − θ) for j ≥ 1",
  "ψⱼ = φʲ − θʲ", "ψⱼ = φʲθʲ", "ψ₀ = 1 and ψⱼ = φʲ − θ"],
 "A",
 "From expanding (1 − θB)/(1 − φB) = (1 − θB)(1 + φB + φ²B² + ⋯). The cumulative sum is (1 − θ)/(1 − φ).",
 check="Setting θ = 0 must recover the AR(1) weights φʲ, and ψⱼ = φ^(j−1)(φ) = φʲ ✓."))

I.append(q(10, "numeric", "moderate",
 "An MA(3) has weights ψ = (1, −0.5, 0.3, −0.1). Its lag-3 autocovariance, with σ² = 1, is:",
 ["−0.1", "0", "−0.15", "1.35"],
 "A",
 "At lag 3 the only surviving product in Σψⱼψⱼ₊₃ is ψ₀ψ₃ = (1)(−0.1) = −0.1, since ψ₄ onwards are zero. Option D is γ₀ = 1 + 0.25 + 0.09 + 0.01 = 1.35.",
 check="γ₄ must be exactly 0, since shifting a four-term sequence by four leaves no overlap — which is the MA cut-off."))

I.append(q(11, "single", "moderate",
 "The Wold decomposition requires the shocks εₜ to be:",
 ["uncorrelated with mean 0 and constant variance, but not necessarily independent",
  "independent and identically distributed",
  "independent and normally distributed",
  "uncorrelated and normally distributed"],
 "A",
 "Only uncorrelatedness is required, which is why a Wold representation captures all the LINEAR dependence and may leave non-linear dependence untouched. Financial returns are the standard case: nearly uncorrelated, so the weights are nearly trivial, yet their squares are strongly autocorrelated."))

I.append(q(12, "multi", "moderate",
 "Consider the general linear process and Wold's theorem.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true — γ₀ = σ²Σψⱼ² requires convergence. B is true: the shift leaves no overlap beyond lag q. C is true, and it is why ARMA families remain needed. D is false — Σψⱼ² is the variance factor and Σψⱼ the multiplier, 2.78 against 5 at φ = 0.8.",
 statements=["Square-summability of the weights is what makes the variance finite.",
             "The overlap formula makes an MA(q)'s autocovariance cut off after lag q.",
             "Wold's theorem guarantees the weights exist without constructing them.",
             "Σψⱼ and Σψⱼ² are the same quantity."],
 verdicts=verd(
  (True, "True: γ₀ = σ²Σψⱼ², so the sum must converge. For an AR(1) it is 1/(1 − φ²), finite exactly when |φ| < 1 — square-summability IS stationarity there."),
  (True, "True. Shifting a weight sequence of length q+1 by more than q leaves no overlapping terms, so every product in Σψⱼψⱼ₊ₖ is zero and γₖ = 0 exactly."),
  (True, "True, and it is why finite ARMA models are necessary rather than superseded: an infinite weight sequence cannot be estimated from finite data, so a parsimonious parametric family is needed."),
  (False, "False. σ²Σψⱼ² is the variance while Σψⱼ is the cumulative long-run effect of a unit shock. At φ = 0.8 they are 2.78 and 5; at φ = 0.95, 10.26 and 20."))))

I.append(q(13, "single", "moderate",
 "Is a random walk a general linear process?",
 ["No — its weights are all 1, so Σψⱼ² diverges",
  "Yes, with ψⱼ = 1 for all j",
  "Yes, with ψⱼ = 0 for j ≥ 1",
  "Only after differencing twice"],
 "A",
 "The weights ψⱼ = 1 mean a shock never decays, so the variance σ²Σψⱼ² is infinite and the process is not stationary — topic 7.6's result recovered from the weights. Wold's theorem applies to stationary processes, so it says nothing about this case. Differencing ONCE gives white noise, which is a general linear process."))

I.append(q(14, "numeric", "moderate",
 "An ARMA(1,1) has φ = 0.5 and θ = 0.5. The process is:",
 ["white noise, since ψⱼ = 0 for all j ≥ 1", "an AR(1) with φ = 0.5",
  "an MA(1) with θ = 0.5", "non-stationary"],
 "A",
 "ψⱼ = φ^(j−1)(φ − θ) = φ^(j−1)(0) = 0 for every j ≥ 1, so only ψ₀ = 1 survives. The AR and MA polynomials share the factor (1 − 0.5B), which cancels: (1 − 0.5B)yₜ = (1 − 0.5B)εₜ gives yₜ = εₜ.",
 check="Σψⱼ = 1, consistent with (1 − θ)/(1 − φ) = 0.5/0.5 = 1, and the ACF is flat."))

I.append(q(15, "single", "moderate",
 "Why is the normalisation ψ₀ = 1 imposed?",
 ["because replacing (ψⱼ, σ) by (cψⱼ, σ/c) leaves every autocovariance unchanged",
  "because it makes the weights sum to 1",
  "because it guarantees stationarity",
  "because it makes the process Gaussian"],
 "A",
 "Since γₖ = σ²Σψⱼψⱼ₊ₖ, scaling the weights by c and the shock standard deviation by 1/c gives exactly the same autocovariances, so the pair is not identified without a normalisation. This is topic 7.1's non-identifiability in general form, and fixing ψ₀ = 1 also makes ψⱼ the response to a UNIT shock."))

I.append(q(16, "single", "moderate",
 "A fitted model leaves a flat residual ACF and passes a portmanteau test, yet performs poorly in use. The most likely omission is:",
 ["dependence in the second moment, such as volatility clustering",
  "a trend in the mean", "a seasonal component",
  "too few autoregressive terms"],
 "A",
 "A flat residual ACF establishes that the LINEAR structure is adequate, which is all Wold's theorem concerns — its shocks are uncorrelated, not independent. Volatility clustering leaves returns nearly uncorrelated while their squares are strongly autocorrelated, so the check is the ACF of the SQUARED residuals, and the repair is a conditional variance model such as GARCH."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider what the ψ weights determine elsewhere in the theory.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true — at φ = 0.8 that gives 5² = 25, matching topic 7.9. B is true: the forecast error variance at horizon k is σ²Σ(j<k)ψⱼ². C is true, and it is how the deterministic component is told apart in the frequency domain. D is false — the ARMA(1,1) response is a single exponential scaled by (φ − θ), the same shape as an AR(1)'s.",
 statements=["The long-run variance of the sample mean is σ²(Σψⱼ)².",
             "The k-step forecast error variance is σ² times the sum of the first k squared weights.",
             "A deterministic sinusoid appears as a spectral line rather than part of the continuous density.",
             "An ARMA(1,1) impulse response has a different shape from an AR(1)'s."],
 verdicts=verd(
  (True, "True, and it ties this lesson to topic 7.9: at φ = 0.8, Σψⱼ = 5, so the long-run variance is 25 — exactly the figure that topic computed by a different route."),
  (True, "True: σ²Σ(j<k)ψⱼ². At k = 1 that is σ²ψ₀² = σ², the one-step error, and as k grows it rises to σ²Σψⱼ² = γ₀, the process variance."),
  (True, "True. The continuous spectral density belongs to the MA(∞) part, while a perfectly predictable periodic component concentrates all its power at one frequency — which is how the two halves of the Wold decomposition are distinguished spectrally."),
  (False, "False — the shapes are the same. Beyond ψ₁ each ARMA(1,1) weight is the previous one times φ, so the response is a single exponential scaled by (φ − θ), differing from an AR(1)'s only in its initial size. That similarity is why the two can be hard to distinguish in a short sample."))))

I.append(q(18, "numeric", "hard",
 "For an AR(1) with φ = 0.95 and σ² = 1, Σψⱼ² and Σψⱼ are respectively:",
 ["10.2564 and 20", "20 and 10.2564", "10.2564 and 10.2564", "400 and 20"],
 "A",
 "Σψⱼ² = 1/(1 − 0.9025) = 10.2564 is the variance; Σψⱼ = 1/(1 − 0.95) = 20 is the long-run multiplier. Both diverge as φ approaches 1 but at different rates, being geometric in φ² and in φ respectively. Option D's 400 is the long-run VARIANCE σ²(Σψⱼ)².",
 check="At φ = 0.99 the pair becomes 50.2513 and 100, confirming the different rates."))

I.append(q(19, "single", "hard",
 "A long-run multiplier is estimated less reliably than a one-step forecast from the same model because:",
 ["it depends on the whole tail of the weight sequence, where a finite sample is least informative",
  "it requires more data to compute",
  "it is not identified at all",
  "forecasts are always more accurate than structural quantities"],
 "A",
 "The one-step forecast error variance is σ²ψ₀² = σ², using the first weight alone, whereas Σψⱼ sums every weight including those at long lags. Small coefficient differences compound in the tail: φ = 0.7 gives 3.33 and φ = 0.8 gives 5, and near a unit root φ̂ = 0.95 against 0.98 gives 20 against 50. So the quantity should be reported with model uncertainty included."))

I.append(q(20, "single", "hard",
 "Wold's theorem shows every stationary process is an MA(∞). The correct conclusion for modelling practice is:",
 ["finite ARMA models are needed as parsimonious families for the weight sequence",
  "only moving-average models should be fitted",
  "autoregressive models are theoretically invalid",
  "no model is needed, since the form is already known"],
 "A",
 "The theorem is an existence result: it guarantees the weights exist without producing them, and an infinite sequence cannot be estimated from finite data. A finite ARMA model parameterises the weight sequence compactly — ψⱼ = φʲ for an AR(1), φ^(j−1)(φ−θ) for an ARMA(1,1) — which is what makes an infinite object estimable. So the theorem makes such models necessary rather than redundant."))

LET = "ABCD"
WANT = {"ts-t10-m-01": "C", "ts-t10-m-02": "B", "ts-t10-m-03": "D",
        "ts-t10-m-04": "C", "ts-t10-m-05": "B", "ts-t10-m-06": "D",
        "ts-t10-m-07": "C", "ts-t10-m-08": "B", "ts-t10-m-09": "D",
        "ts-t10-m-10": "C", "ts-t10-m-11": "B", "ts-t10-m-13": "D",
        "ts-t10-m-14": "C", "ts-t10-m-15": "B", "ts-t10-m-16": "D",
        "ts-t10-m-18": "C", "ts-t10-m-19": "B", "ts-t10-m-20": "D"}


def swapletters(t, a, b):
    sw = lambda L: b if L == a else a if L == b else L
    def fix(m):
        head, body = m.group(1), m.group(2)
        return head + re.sub(r"[ABCD]", lambda n: sw(n.group(0)), body)
    return re.sub(r"([Oo]ptions?\s+)([ABCD](?:\s*(?:,|and|or)\s*[ABCD])*)", fix, t)


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
        for fld in ("explanation", "check"):
            if it.get(fld):
                it[fld] = swapletters(it[fld], a, b)
    return items

relabel(I)
_k = {}
for _it in I:
    _k[_it["answer"]] = _k.get(_it["answer"], 0) + 1
print("key spread:", {L: _k.get(L, 0) for L in LET}, "cap", -(-len(I) * 2 // 5))

POOLD = {
 "moduleId": "timeseries", "topicId": "timeseries-t10", "source": "mastery",
 "label": "General linear process and Wold decomposition — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
