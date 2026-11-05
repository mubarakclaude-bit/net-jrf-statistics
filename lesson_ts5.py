#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 5.5 — Unit roots, differencing and ARIMA (topic timeseries-t5).

Second lesson of the time-series module, and the natural home of June 2026 Q18 — the question
whose process y_t = 0.6 y_{t-1} + 0.4 y_{t-2} + e_t has coefficients summing to 1. Topic 7.3
worked that question as a warning; this lesson is the full treatment of what it was warning
about.

Seven of the ten practice variants tagged to Q18 are squarely this topic, and all of them were
read with their options before authoring (the sign convention for MA invertibility is not
guessable, and one variant settles it):

  - y_t = y_{t-1} + e_t is a random walk, non-stationary
  - random walk with drift: mean t*mu, variance t*sigma^2
  - phi1 + phi2 = 1 in an AR(2) means a unit root
  - y_t = 1.2y_{t-1} - 0.2y_{t-2} + e_t differences to AR(1) with phi = +0.2
  - ARIMA(2,1,0) is stationary after one differencing
  - MA(1) y_t = e_t - theta e_{t-1} is invertible iff |theta| < 1
  - Dickey-Fuller tests for a unit root
  - a slowly, near-linearly decaying sample ACF means a unit root
  - phi = (0.4, 0.3), theta = (0.6, 0.4) is stationary but NOT invertible

That last one fixes the convention: MA written with MINUS signs, so the invertibility region
mirrors the AR stationarity triangle and theta1 + theta2 = 1.0 fails it.

Writes seed/lesson_ts5.json and seed/timeseries_t5_mastery.json.
Run: python3 lesson_ts5.py
"""
import json, io, os, re

OUT = "seed/lesson_ts5.json"
POOL = "seed/timeseries_t5_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Fix the difference operator and the root condition, which together are the whole of this topic.",
 "ask": {
  "q": "Topic 7.3 ended by saying that a process with φ₁ + φ₂ = 1 has no ACF at all. If it has no ACF, what is there left to model?",
  "nudge": "Something derived from the series rather than the series itself. The fourth check names it."},
 "body": [
  "Most real series are not stationary. Prices drift, populations grow, consumption trends upward. Everything in topic 7.3 assumed stationarity, and most data violates it.",
  "The usual repair is simple and it is the subject of this lesson: do not model the series, model its CHANGES. A price that wanders may have changes that are perfectly well behaved, and the methods of 7.3 then apply to the changes.",
  "Knowing when that repair is needed, how many times to apply it, and what it does to the model's name is what this lesson covers. The condition that triggers it is called a unit root.",
  "Four checks. One on notation, one on the root condition from 7.3, one on what stationarity actually demands, and one on the simplest non-stationary process there is."],
 "items": [
  {"ask": "Define the difference operator Δ in terms of the backshift operator B, and say what Δ²yₜ means.",
   "recall": "Δyₜ = yₜ − yₜ₋₁ = (1 − B)yₜ. So Δ = 1 − B, and Δ²yₜ = Δ(Δyₜ) = yₜ − 2yₜ₋₁ + yₜ₋₂.",
   "refresh": [
    "B shifts back one period: Byₜ = yₜ₋₁. So 1 − B is the operator that subtracts the previous value, which is exactly first differencing.",
    "Δ² is differencing twice, not squaring the differences. Expanding (1 − B)² = 1 − 2B + B² gives the three-term formula above.",
    "Writing Δ as (1 − B) is what lets you treat differencing algebraically, factoring it in and out of polynomials. That is the single most useful move in this lesson."]},
  {"ask": "For an AR process written φ(B)yₜ = εₜ, what condition on the roots of φ(z) = 0 makes it stationary?",
   "recall": "Every root must lie strictly outside the unit circle — that is, have modulus greater than 1.",
   "refresh": [
    "From topic 7.3. For an AR(1) the polynomial is 1 − φz with root 1/φ, and |1/φ| > 1 is the same as |φ| < 1.",
    "A root exactly ON the unit circle — at z = 1, say — is the boundary case, and it is what gives this lesson its name.",
    "A root INSIDE the unit circle makes the process explosive, with values growing without limit. That case is mathematically possible and almost never relevant to data, so questions concentrate on the boundary."]},
  {"ask": "What three things must hold for a process to be weakly stationary?",
   "recall": "A constant mean, a constant variance, and an autocovariance γₖ that depends only on the lag k and not on where in time you look.",
   "refresh": [
    "All three can fail, and for the random walk in the next check two of them do: the variance grows with time and so does the mean once a drift is added.",
    "The autocovariance condition is the one that matters for modelling, because the whole ACF-based toolkit needs γₖ to be a function of k alone.",
    "This is 'weak' or 'second-order' stationarity. Strict stationarity asks for the whole joint distribution to be shift-invariant, and for Gaussian processes the two coincide."]},
  {"ask": "For the random walk yₜ = yₜ₋₁ + εₜ starting from y₀ = 0, what are E(yₜ) and Var(yₜ)?",
   "recall": "yₜ is the sum of the first t shocks, so E(yₜ) = 0 and Var(yₜ) = tσ²ε.",
   "refresh": [
    "Unrolling the recursion gives yₜ = ε₁ + ε₂ + … + εₜ. The shocks are uncorrelated, so the variances add.",
    "The variance therefore GROWS with t, without limit. That alone rules out stationarity, and it is why a random walk wanders ever further from where it started instead of returning.",
    "The random walk is the AR(1) with φ = 1 exactly — the simplest unit-root process, and the one section 4 works in full."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Model the changes, not the levels",
 "objective": "See why differencing is the natural repair, and what it costs.",
 "body": [
  "A series with a unit root has no mean to return to. Its variance grows, its correlations stay high at every lag, and the usual question — how far is it from its average — has no answer, because there is no average.",
  "But look at what such a series does from one period to the next. The changes may be small, centred on zero or on a steady drift, and entirely well behaved. The level wanders; the change does not.",
  "So the repair is to work with the changes. Difference the series once, check whether what remains is stationary, and if it is, fit the AR or MA machinery of topic 7.3 to the differenced series. The model is then described by three numbers: how many AR terms, how many differences, how many MA terms.",
  "What differencing costs is the level itself. A model of changes forecasts changes, and to get back to a forecast of the level you accumulate them — which is fine, but it means the forecast uncertainty grows with the horizon rather than settling down. That is not a flaw in the method; it is an honest consequence of the series having no mean to pull it back."],
 "scenario": {
  "teaser": "A treasury desk is handed a model that says the exchange rate is 'significantly related' to the wholesale price index.",
  "title": "Two wandering series and a spurious relationship",
  "body": [
   "A treasury analyst regresses the monthly rupee–dollar rate on the wholesale price index over twenty years. The fit is excellent — a high R², a t statistic above 8 — and the conclusion drawn is that the price index drives the exchange rate.",
   "The trouble is that both series have unit roots. Both wander without returning to any mean, and over twenty years both happen to have drifted upward. A regression of one wandering series on another finds a strong relationship almost regardless of whether any relationship exists, because both are going up and nothing in the arithmetic knows that each is going up for its own reasons.",
   "This is the spurious regression problem, and it is severe: with two independent random walks, the usual t test rejects 'no relationship' far more often than its stated 5%, and the rate gets worse as the sample grows. More data makes the illusion stronger, not weaker.",
   "The diagnosis is available before any regression. Look at the sample ACF of each series: if it stays near 1 and decays slowly and almost linearly rather than geometrically, there is a unit root. Section 4 computes exactly that pattern for a random walk and shows why it looks the way it does.",
   "The repair is to run the analysis on the differenced series — monthly CHANGES in the rate against monthly CHANGES in the index. The spurious relationship vanishes, and whatever genuine relationship exists survives. Often the honest answer is that there is no relationship, which is a less exciting report and a correct one.",
   "There is a more sophisticated route, where two series share a common wandering component and a particular combination of them is stationary. That is cointegration, and it is beyond this syllabus — but it is why a careful analyst tests for unit roots before differencing away something real."],
  "q": "Why does a larger sample make the spurious relationship worse rather than better?",
  "answer": "Because the two series keep wandering, so their apparent co-movement accumulates rather than averaging out. In an ordinary regression more data shrinks the standard error towards zero around a true coefficient; here the standard error is computed under an assumption — stationarity — that fails, so it shrinks towards zero around a coefficient that means nothing. The test statistic therefore grows with the sample size and rejects ever more confidently. The usual intuition that more data cures a weak conclusion relies on stationarity, and it is exactly that assumption which has failed."},
 "ask": {
  "q": "Differencing removes the unit root but also throws away the level. When might that loss matter to a forecaster?",
  "nudge": "Think about what a bank actually needs to know: next month's change, or next month's rate?"}})

S.append({
 "kind": "theory", "id": "s2", "mins": 9,
 "title": "Unit roots, and what goes wrong",
 "objective": "Define the condition precisely and list its consequences, which is what the conceptual questions ask about.",
 "blocks": [
  {"t": "def", "h": "A unit root",
   "body": "A process φ(B)yₜ = εₜ has a unit root if z = 1 is a root of φ(z) = 0. Equivalently, φ(1) = 0, which for an AR(p) means 1 − φ₁ − φ₂ − … − φₚ = 0, that is φ₁ + φ₂ + … + φₚ = 1. The polynomial then has (1 − z) as a factor, and that factor is the difference operator."},
  {"t": "formula", "h": "The test you can do in your head",
   "body": "AR(p):  add the coefficients.\n    sum < 1  →  possibly stationary, check the other conditions\n    sum = 1  →  unit root, not stationary, difference it\n    sum > 1  →  explosive\nFor an AR(2) this is the first of the three stationarity conditions from topic 7.3, and it is the one that fails in both of the examples this lesson works."},
  {"t": "step", "h": "What having a unit root costs you",
   "body": "The variance grows without limit, so there is no finite Var(yₜ) to divide by and no ACF. There is no mean the series returns to, so forecasts do not converge to a level. Shocks are permanent rather than fading — a disturbance today shifts the whole future path instead of decaying away. And regressions involving such series produce spurious relationships, as the previous section described. None of the topic 7.3 toolkit applies, because all of it presumes an ACF."},
  {"t": "formula", "h": "Extracting the factor",
   "body": "If φ(B) has a unit root, write φ(B) = (1 − B)ψ(B) for some lower-order polynomial ψ. Then\n    φ(B)yₜ = εₜ   becomes   ψ(B)(1 − B)yₜ = εₜ,   that is   ψ(B)Δyₜ = εₜ.\nSo the DIFFERENCED series follows the lower-order model ψ. This single rearrangement is what both worked examples in this lesson do, and it is the whole technique."},
  {"t": "def", "h": "ARIMA(p, d, q)",
   "body": "A process is ARIMA(p, d, q) if differencing it d times yields a stationary ARMA(p, q). The three numbers are the AR order, the number of differences, and the MA order. So an ARIMA(2, 1, 0) needs ONE differencing and is then a pure AR(2); an ARIMA(0, 1, 0) is the random walk; and an ARIMA(1, 1, 0) is what both of this lesson's worked examples turn out to be. The 'I' stands for integrated, meaning the series is a cumulative sum of a stationary process."},
  {"t": "step", "h": "How many differences",
   "body": "Almost always one. Economic levels usually need d = 1; a series whose GROWTH also trends may need d = 2; d beyond 2 is essentially never justified. Over-differencing is a real error with a visible signature — it introduces artificial negative autocorrelation at lag 1 and inflates the variance — so the rule is to difference as few times as makes the series stationary and no more. Section 7's test is how that judgement is made formally rather than by eye."}],
 "table": {
  "caption": "The ARIMA naming, with the examples used in this lesson and in topic 7.3.",
  "head": ["Process", "ARIMA", "After differencing d times", "Where it appears"],
  "rows": [
   ["yₜ = yₜ₋₁ + εₜ", "(0, 1, 0)", "Δyₜ = εₜ, white noise", "random walk, section 4"],
   ["yₜ = μ + yₜ₋₁ + εₜ", "(0, 1, 0) with drift", "Δyₜ = μ + εₜ", "random walk with drift"],
   ["yₜ = 0.6yₜ₋₁ + 0.4yₜ₋₂ + εₜ", "(1, 1, 0)", "Δyₜ = −0.4Δyₜ₋₁ + εₜ", "June 2026 Q18"],
   ["yₜ = 1.2yₜ₋₁ − 0.2yₜ₋₂ + εₜ", "(1, 1, 0)", "Δyₜ = +0.2Δyₜ₋₁ + εₜ", "section 6"],
   ["stationary AR(2)", "(2, 0, 0)", "no differencing needed", "topic 7.3"]]},
 "flow": {
  "title": "Deciding what to fit",
  "alt": "Flow chart from a series to an ARIMA specification",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "A series, or an AR equation with numbers in it", "kind": "start"},
   {"id": "b", "r": 1, "c": 1, "label": "Add the coefficients, or inspect the sample ACF", "kind": "step"},
   {"id": "c", "r": 2, "c": 0, "label": "Sum < 1, ACF decays geometrically → stationary", "kind": "step"},
   {"id": "d", "r": 2, "c": 2, "label": "Sum = 1, or ACF decays slowly → unit root", "kind": "step"},
   {"id": "e", "r": 3, "c": 2, "label": "Factor out (1 − B); difference once", "kind": "step"},
   {"id": "f", "r": 4, "c": 1, "label": "Fit ARMA(p, q) to what remains", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"},
   {"from": "b", "to": "c", "label": "no unit root"},
   {"from": "b", "to": "d", "label": "unit root"},
   {"from": "d", "to": "e"},
   {"from": "e", "to": "b", "label": "re-check the differenced series"},
   {"from": "c", "to": "f"}],
  "note": "The loop back is deliberate: after differencing you ask the same question again, which is how d is determined rather than assumed."},
 "ask": {
  "q": "An AR(2) has φ₁ = 0.7 and φ₂ = 0.5. What does adding them tell you, and is differencing the right repair?",
  "nudge": "The sum is 1.2. Which of the three cases is that, and does differencing fix an explosive process?"}})

S.append({
 "kind": "worked", "id": "s3", "mins": 8,
 "title": "Worked in full — the random walk, with and without drift",
 "objective": "Compute the mean, variance and ACF of the simplest unit-root process, and see where the diagnostic signature comes from.",
 "ask": {
  "q": "The ACF at lag 50 is still 0.816. What would the ACF of a stationary AR(1) with φ = 0.9 be at lag 50?",
  "nudge": "0.9⁵⁰. Work out roughly how small that is, and compare."},
 "problem": "For the random walk yₜ = μ + yₜ₋₁ + εₜ with y₀ = 0 and Var(εₜ) = σ²ε, find E(yₜ), Var(yₜ) and the correlation between yₜ and yₜ₊ₖ. Then evaluate that correlation at t = 100 for several lags.",
 "steps": [
  {"say": "Unroll the recursion to express yₜ in terms of the shocks.",
   "math": "y₁ = μ + ε₁\ny₂ = μ + y₁ + ε₂ = 2μ + ε₁ + ε₂\n…\nyₜ = μt + (ε₁ + ε₂ + … + εₜ)",
   "why": "The whole history accumulates. Nothing decays, because the coefficient on the previous value is exactly 1 — there is no factor less than one to shrink old shocks."},
  {"say": "Read off the mean and the variance.",
   "math": "E(yₜ) = μt\nVar(yₜ) = Var(ε₁ + … + εₜ) = tσ²ε",
   "why": "The shocks are uncorrelated so the variances add. Both the mean and the variance depend on t, so two of the three stationarity requirements fail at once. With μ = 0 the mean is constant but the variance still grows, so a driftless random walk is non-stationary too."},
  {"say": "Compute the covariance between two time points.",
   "math": "Cov(yₜ, yₜ₊ₖ) = Cov(ε₁ + … + εₜ,  ε₁ + … + εₜ₊ₖ)\n              = tσ²ε     (only the first t shocks are shared)",
   "why": "The two sums share exactly the first t shocks, and uncorrelated terms contribute nothing. Note that the covariance depends on t, not on k — the opposite of what stationarity requires."},
  {"say": "Form the correlation.",
   "math": "Corr(yₜ, yₜ₊ₖ) = tσ²ε / √(tσ²ε · (t + k)σ²ε)\n              = t/√(t(t + k))\n              = √(t/(t + k))",
   "why": "σ²ε cancels entirely, so the correlation does not depend on the size of the shocks — only on where you are in the series and how far apart the points are."},
  {"say": "Evaluate at t = 100 to see the diagnostic signature.",
   "math": "k = 1:  √(100/101) = 0.995\nk = 5:  √(100/105) = 0.976\nk = 10: √(100/110) = 0.953\nk = 20: √(100/120) = 0.913\nk = 50: √(100/150) = 0.816",
   "why": "This is the pattern one of the practice questions describes as 'decaying very slowly and almost linearly'. Still 0.82 at lag 50. A stationary AR(1) with φ = 0.9 would be at 0.9⁵⁰ ≈ 0.005 — utterly negligible. That contrast is the whole diagnostic."}],
 "after": "Two things to carry. The random walk is ARIMA(0, 1, 0): differencing once gives Δyₜ = μ + εₜ, which is white noise around a constant and completely stationary — the repair is immediate and total. And the sample ACF of a unit-root series looks nothing like a stationary one; the near-linear decay in the numbers above is what you look for in real data, and it is the visual counterpart of adding the coefficients to 1."})

S.append({
 "kind": "recall", "id": "s4", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the definition, the test and the naming.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "What does it mean for an AR process to have a unit root?",
   "a": "z = 1 is a root of the AR polynomial, equivalently the coefficients sum to 1, equivalently (1 − B) is a factor."},
  {"q": "For the random walk with drift, what are the mean and variance of yₜ?",
   "a": "E(yₜ) = μt and Var(yₜ) = tσ²ε, with y₀ = 0. Both depend on t."},
  {"q": "What does the d in ARIMA(p, d, q) count?",
   "a": "The number of times the series is differenced before a stationary ARMA(p, q) remains."},
  {"q": "An ARIMA(2, 1, 0) process becomes stationary after how many differencings?",
   "a": "One. The d in the middle is the answer, and the series is then a pure AR(2)."},
  {"q": "What does a sample ACF that decays slowly and nearly linearly indicate?",
   "a": "A unit root — the series is not stationary and should be differenced."}]})

S.append({
 "kind": "completion", "id": "s5", "mins": 8,
 "title": "Your turn — difference an AR(2) with a unit root",
 "objective": "Factor out the difference operator yourself, and notice how the sign of what remains depends on the factorisation.",
 "problem": "Consider yₜ = 1.2yₜ₋₁ − 0.2yₜ₋₂ + εₜ. Determine whether it is stationary, and if not, find the model satisfied by the differenced series Δyₜ and its ACF.",
 "steps": [
  {"say": "Do the one-line check before anything else.",
   "blank": {"prompt": "Add the coefficients. What does the result tell you?",
             "answer": "1.2 + (−0.2) = 1, so there is a unit root and the process is not stationary",
             "accept": ["1, unit root", "sum is 1 so unit root", "1.0 — not stationary",
                        "they sum to 1, so there is a unit root"],
             "hint": "Mind the sign of the second coefficient — it is −0.2, not +0.2."},
   "why": "Exactly 1, so z = 1 is a root. The minus sign on the second coefficient is easy to misread, and getting 1.4 instead of 1.0 would send you looking for an ACF that does not exist."},
  {"say": "Write the AR polynomial and factor out the difference operator.",
   "blank": {"prompt": "Factor 1 − 1.2z + 0.2z² into (1 − z) times something.",
             "answer": "(1 − z)(1 − 0.2z)",
             "accept": ["(1-z)(1-0.2z)", "(1 − z)(1 − 0.2z)", "(1-z)*(1-0.2z)"],
             "hint": "The constant term must be 1 and the z² coefficient 0.2, so the second factor is 1 − 0.2z. Expand to check."},
   "why": "Expanding: 1 − 0.2z − z + 0.2z² = 1 − 1.2z + 0.2z² ✓. Always expand back out — a sign error here propagates straight into the final answer."},
  {"say": "Rewrite the process using that factorisation.",
   "blank": {"prompt": "What model does Δyₜ satisfy?",
             "answer": "Δyₜ = 0.2Δyₜ₋₁ + εₜ — an AR(1) with φ = +0.2",
             "accept": ["AR(1) with phi = 0.2", "dy_t = 0.2 dy_{t-1} + e_t",
                        "AR(1), coefficient +0.2", "an AR(1) with 0.2"],
             "hint": "(1 − z)yₜ is Δyₜ, so (1 − 0.2B)Δyₜ = εₜ. Move the term across."},
   "why": "(1 − 0.2B)Δyₜ = εₜ gives Δyₜ − 0.2Δyₜ₋₁ = εₜ, so Δyₜ = +0.2Δyₜ₋₁ + εₜ. Note the sign: the factor was (1 − 0.2z), so moving it across gives a PLUS. Contrast this with Q18, where the factor was (1 + 0.4z) and the result was −0.4."},
  {"say": "Give the ACF of the differenced series and name the full model.",
   "blank": {"prompt": "What is the ACF of Δyₜ, and what is this process called in ARIMA notation?",
             "answer": "ρₖ = (0.2)ᵏ, and the process is ARIMA(1, 1, 0)",
             "accept": ["(0.2)^k, ARIMA(1,1,0)", "0.2^k and ARIMA(1,1,0)",
                        "rho_k = 0.2^k; ARIMA(1,1,0)"],
             "hint": "An AR(1) with coefficient φ has ACF φᵏ. One AR term, one difference, no MA terms."},
   "why": "|0.2| < 1 so the differenced series is stationary, and its ACF decays fast — negligible by lag 4. One AR term, one difference, no MA term: ARIMA(1, 1, 0), the same classification as Q18's process despite the opposite sign."}],
 "after": "Put the two side by side. Q18's polynomial factored as (1 − B)(1 + 0.4B), giving Δyₜ = −0.4Δyₜ₋₁ + εₜ and an alternating ACF. This one factors as (1 − B)(1 − 0.2B), giving Δyₜ = +0.2Δyₜ₋₁ + εₜ and a decaying positive ACF. Both are ARIMA(1, 1, 0); the sign of the surviving coefficient comes entirely from the factorisation, and reading it off the original equation gives the wrong answer in both cases."})

S.append({
 "kind": "theory", "id": "s6", "mins": 7,
 "title": "Invertibility — the moving-average mirror",
 "objective": "Get the MA condition and its region, since questions pair it with stationarity.",
 "blocks": [
  {"t": "def", "h": "Why invertibility is wanted",
   "body": "An MA process is written yₜ = θ(B)εₜ. To use it you need to recover the unobserved shocks from the observed data, which means inverting that relation: εₜ = θ(B)⁻¹yₜ. That inversion produces a convergent expression only under a condition on θ, and a process meeting it is called invertible. Without invertibility the shocks cannot be recovered, forecasts cannot be formed from the data, and two different parameter values can give identical autocorrelations — so the model is not even identified."},
  {"t": "formula", "h": "The condition, and the convention it depends on",
   "body": "Write the MA with MINUS signs, as Box and Jenkins do:\n    yₜ = (1 − θ₁B − … − θ_qB�q)εₜ.\nThe process is invertible if every root of θ(z) = 0 lies strictly outside the unit circle. That is the same condition on θ as stationarity imposes on φ, so the regions are identical in shape:\n    MA(1):  |θ| < 1\n    MA(2):  θ₁ + θ₂ < 1,  θ₂ − θ₁ < 1,  |θ₂| < 1.\nSome books write the MA with plus signs, which flips the signs in these inequalities. Read the stem for which convention is in use."},
  {"t": "step", "h": "The duality worth remembering",
   "body": "Stationarity is a condition on the AR part; invertibility is a condition on the MA part; and the two conditions have exactly the same algebraic form. An ARMA(p, q) must satisfy both, and the two are independent — a process can be stationary and not invertible, invertible and not stationary, both, or neither. Questions exploit exactly that independence by giving one set of coefficients that passes and one that fails."},
  {"t": "step", "h": "Worked classification",
   "body": "Take φ₁ = 0.4, φ₂ = 0.3, θ₁ = 0.6, θ₂ = 0.4, an ARMA(2, 2). Stationarity: 0.4 + 0.3 = 0.7 < 1 ✓, 0.3 − 0.4 = −0.1 < 1 ✓, |0.3| < 1 ✓ — stationary. Invertibility: 0.6 + 0.4 = 1.0, which is NOT less than 1 ✗ — the MA part sits exactly on the boundary, so the process is not invertible. The verdict is stationary but not invertible, and a practice question on this topic asks precisely this."},
  {"t": "def", "h": "The unit root in the MA part",
   "body": "θ₁ + θ₂ = 1 means z = 1 is a root of the MA polynomial — a unit root in the MA part rather than the AR part. It has a characteristic cause: OVER-differencing. Differencing a series that was already stationary introduces an MA unit root, which is why over-differencing is detectable and why the rule is to difference as few times as necessary."}],
 "ask": {
  "q": "Over-differencing introduces an MA unit root. Why does that make it detectable rather than merely wasteful?",
  "nudge": "A unit root in the MA part shows up in the ACF of the over-differenced series. What would you see at lag 1?"}})

S.append({
 "kind": "guided", "id": "s7", "mins": 8,
 "title": "On your own — testing for a unit root",
 "objective": "Understand what the Dickey–Fuller test does, which is the formal version of adding the coefficients.",
 "problem": "The Dickey–Fuller test is applied to a series. (a) What null hypothesis does it test, and what is the alternative? (b) Starting from yₜ = φyₜ₋₁ + εₜ, show how the test is set up as a regression on Δyₜ. (c) Why can the ordinary t table not be used? (d) What does a failure to reject mean in practice?",
 "hints": [
  "For (a), the test is named for what it looks for. State both hypotheses in terms of φ, then in words.",
  "For (b), subtract yₜ₋₁ from both sides of the AR(1) equation and see what the coefficient on yₜ₋₁ becomes.",
  "For (d), remember the non-rejection discipline from the inference module — what does insufficient evidence establish?"],
 "answer": "(a) H₀: the series has a unit root (φ = 1, non-stationary) against H₁: it is stationary (|φ| < 1). (b) Δyₜ = (φ − 1)yₜ₋₁ + εₜ = δyₜ₋₁ + εₜ, and the test is of δ = 0 against δ < 0. (c) Because under the null the series is non-stationary, so the usual asymptotic theory fails and the statistic has a non-standard distribution with its own tabulated critical values. (d) That there is insufficient evidence against a unit root — so difference the series — not that a unit root has been proved.",
 "check": "Three things worth being exact about. The null is the UNIT ROOT, which is the opposite way round from most tests and means that failing to reject leads you to difference — the conservative action is to treat the series as non-stationary. The regression is on the differenced series with the LEVEL as regressor, and the coefficient tested is δ = φ − 1, so δ = 0 is the unit root and δ < 0 is stationarity. And the critical values are more negative than the ordinary t values, so using a t table makes the test reject too readily — it would declare stationarity that is not there.",
 "scenario": {
  "teaser": "An analyst reports 'the Dickey–Fuller test was not significant, so the series is stationary'.",
  "title": "The null that catches people out",
  "body": [
   "An analyst tests a monthly production index with the Dickey–Fuller test, gets a p-value of 0.31, and writes that the series is stationary and can be modelled directly.",
   "That conclusion is exactly backwards. In this test the null hypothesis IS the unit root. A p-value of 0.31 means there is insufficient evidence AGAINST non-stationarity — so the sensible reading is that the series probably needs differencing, which is the opposite of what was written.",
   "The confusion is understandable, because almost every other test in the syllabus has a null of 'nothing interesting is happening'. Here the null is the awkward case, and the test is trying to establish stationarity rather than to establish a departure.",
   "There is a second trap waiting. Even a correct rejection does not establish stationarity in the strong sense, and even a correct non-rejection does not prove a unit root — the test has notoriously low power against a φ close to but below 1, say 0.95. With a few hundred observations it often cannot tell 0.95 from 1.00, which is why the usual practice is to combine the test with a look at the sample ACF and with judgement about whether the series ought to have a mean to return to.",
   "The practical discipline: state which hypothesis was the null, report the test alongside the ACF, and remember that a non-rejection sends you to differencing rather than away from it."],
  "q": "Why is low power against φ = 0.95 a particular problem for this test?",
  "answer": "Because 0.95 and 1.00 imply very different behaviour — one series returns to a mean, the other wanders forever — and yet over a few hundred observations their paths look almost identical. The test fails to reject in both cases, so a non-rejection cannot distinguish 'genuinely a unit root' from 'stationary but highly persistent'. Since the consequence of the choice is large and the evidence is weak, the decision usually rests on the sample ACF and on subject-matter reasoning about whether a mean exists, with the test as one input rather than the verdict."},
 "solution": [
  {"say": "(a) State the hypotheses.",
   "math": "H₀: φ = 1   (unit root, non-stationary)\nH₁: |φ| < 1 (stationary)",
   "why": "The null is the unit root. That orientation is the single most important thing about this test, and it is what the analyst in the scenario got wrong."},
  {"say": "(b) Rearrange into a regression on the differences.",
   "math": "yₜ = φyₜ₋₁ + εₜ\nyₜ − yₜ₋₁ = (φ − 1)yₜ₋₁ + εₜ\nΔyₜ = δyₜ₋₁ + εₜ,  where δ = φ − 1\nH₀: δ = 0  against  H₁: δ < 0",
   "why": "Subtracting the lagged level from both sides converts the awkward test of φ = 1 into a test of a coefficient being zero, which is a familiar shape. Note the alternative is one-sided: δ < 0, since φ < 1 means δ < 0."},
  {"say": "(c) Explain the non-standard distribution.",
   "math": "under H₀ the regressor yₜ₋₁ is itself non-stationary\n⟹ the usual asymptotic theory for a t statistic does not apply\n⟹ critical values are tabulated separately and are MORE NEGATIVE than the t values",
   "why": "The ordinary t distribution is derived assuming stationary regressors, which fails under this null by construction. Using a t table makes the test reject too easily, declaring stationarity that is not supported."},
  {"say": "(d) Interpret a non-rejection correctly.",
   "math": "fail to reject ⟹ insufficient evidence against a unit root\n⟹ treat the series as non-stationary and difference it\nNOT ⟹ a unit root has been proved",
   "why": "The non-rejection discipline from the inference module applies unchanged, and here it is reinforced by the test's low power against values of φ just below 1. The action is to difference; the claim is not that the series certainly has a unit root."}]})

S.append({
 "kind": "trapcheck", "id": "s8", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims the variant questions on this topic are built from.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "The process yₜ = yₜ₋₁ + εₜ is non-stationary.",
   "tf": True,
   "why": "True. It is the random walk, the AR(1) with φ = 1 exactly. Its variance is tσ²ε, which grows without limit, so stationarity fails even though the mean stays at zero."},
  {"claim": "For the random walk with drift yₜ = μ + yₜ₋₁ + εₜ starting at zero, E(yₜ) = μ and Var(yₜ) = σ²ε.",
   "tf": False,
   "why": "False. Unrolling gives yₜ = μt + Σεᵢ, so E(yₜ) = μt and Var(yₜ) = tσ²ε. Both grow with t, which is why neither the mean nor the variance is constant."},
  {"claim": "If φ₁ + φ₂ = 1 in an AR(2), the process has a unit root.",
   "tf": True,
   "why": "True. φ(1) = 1 − φ₁ − φ₂ = 0, so z = 1 is a root and (1 − B) factors out. The process is not stationary and must be differenced."},
  {"claim": "An ARIMA(2, 1, 0) process requires two differencings to become stationary.",
   "tf": False,
   "why": "False — it requires ONE. The middle number is d, the number of differences; the 2 is the AR order of what remains. After one differencing you have a stationary AR(2)."},
  {"claim": "The MA(1) process yₜ = εₜ − θεₜ₋₁ is invertible if |θ| < 1.",
   "tf": True,
   "why": "True. The MA polynomial is 1 − θz with root 1/θ, and that root lies outside the unit circle exactly when |θ| < 1 — the same condition on θ that stationarity imposes on φ for an AR(1)."},
  {"claim": "The Dickey–Fuller test takes stationarity as its null hypothesis.",
   "tf": False,
   "why": "False, and this is the commonest error with the test. The null is the UNIT ROOT, so failing to reject points towards differencing. The alternative is stationarity, which is what a rejection supports."}]})

S.append({
 "kind": "guided", "id": "s9", "mins": 7,
 "title": "On your own — classify four processes",
 "objective": "Apply both conditions together, which is the form the summary questions take.",
 "problem": "Classify each as stationary, invertible, both or neither, using the Box–Jenkins minus convention for the MA part. (a) φ₁ = 0.4, φ₂ = 0.3, θ₁ = 0.6, θ₂ = 0.4. (b) yₜ = εₜ − 1.5εₜ₋₁. (c) yₜ = 0.5yₜ₋₁ + εₜ − 0.3εₜ₋₁. (d) yₜ = yₜ₋₁ + εₜ − 0.4εₜ₋₁.",
 "hints": [
  "Apply the triangle to the φ values for stationarity and the same triangle to the θ values for invertibility. They are independent conditions.",
  "For (b) there is no AR part at all, so stationarity is automatic — every finite MA process is stationary. Only invertibility is in question.",
  "For (d) look at the AR part before anything else. What is the coefficient on yₜ₋₁?"],
 "answer": "(a) Stationary but not invertible. (b) Stationary but not invertible. (c) Both. (d) Invertible but not stationary.",
 "check": "Two structural points. A finite MA process is ALWAYS stationary, whatever its coefficients — it is a finite weighted sum of a finite number of shocks, so its variance is finite and its autocovariances depend only on the lag. So for (b) only invertibility can fail, and with |−1.5| > 1 it does. And in (d) the AR coefficient is exactly 1, a unit root, so the process is non-stationary however well behaved the MA part is — this is an ARIMA(0, 1, 1), which differences to a stationary invertible MA(1).",
 "solution": [
  {"say": "(a) Test both triangles.",
   "math": "stationarity: 0.4 + 0.3 = 0.7 < 1 ✓, 0.3 − 0.4 = −0.1 < 1 ✓, |0.3| < 1 ✓\ninvertibility: 0.6 + 0.4 = 1.0, not < 1 ✗\n⟹ stationary but not invertible",
   "why": "The MA part sits exactly on the boundary of its region, which is an MA unit root. This is the practice question's own case and its answer."},
  {"say": "(b) A pure MA(1) with a large coefficient.",
   "math": "no AR part ⟹ stationary automatically\ninvertibility: |−1.5| = 1.5 > 1 ✗\n⟹ stationary but not invertible",
   "why": "A finite MA is always stationary. Note that this process has the same ACF as the invertible MA(1) with θ = 1/1.5 = 0.667 — which is exactly why invertibility is required for identification: without it, two parameter values are indistinguishable from the data."},
  {"say": "(c) An ARMA(1, 1) with modest coefficients.",
   "math": "stationarity: |0.5| < 1 ✓\ninvertibility: |0.3| < 1 ✓\n⟹ both",
   "why": "The usual well-behaved case, and the one a fitted model should land in. Both conditions are checked separately on their own part of the model."},
  {"say": "(d) Check the AR part first.",
   "math": "AR coefficient is 1 ⟹ unit root ⟹ not stationary\ninvertibility: |−0.4| < 1 ✓\n⟹ invertible but not stationary;  ARIMA(0, 1, 1)\ndifferencing gives Δyₜ = εₜ − 0.4εₜ₋₁, a stationary invertible MA(1)",
   "why": "A unit root in the AR part is decisive regardless of the MA part. And the repair is the same as always: difference once, and what remains is well behaved."}]})

S.append({
 "kind": "theory", "id": "s10", "mins": 6,
 "title": "Where this fits — the Box–Jenkins cycle",
 "objective": "See how identification, estimation and checking fit together, which is how the overview questions are framed.",
 "blocks": [
  {"t": "step", "h": "The three stages",
   "body": "IDENTIFICATION: decide d by testing for unit roots and inspecting the sample ACF, then decide p and q from the ACF and PACF of the differenced series. ESTIMATION: fit the chosen ARIMA(p, d, q), by Yule–Walker as a starting point and then maximum likelihood. DIAGNOSTIC CHECKING: examine the residuals; if they are not white noise, the model is wrong and the cycle repeats."},
  {"t": "def", "h": "What each topic of this module contributes",
   "body": "Stationarity and invertibility set the admissible region. Unit roots and differencing, this topic, fix d. The ACF and PACF patterns fix p and q. Yule–Walker, topic 7.3, converts between coefficients and autocorrelations and provides the first estimates. Forecasting uses the fitted model. The module is one procedure taught in pieces."},
  {"t": "step", "h": "The order of operations matters",
   "body": "Determine d FIRST. The ACF and PACF of a non-stationary series are uninformative about p and q — the slow decay swamps everything — so trying to read an order off an undifferenced unit-root series produces nonsense. This is the practical reason unit roots come before identification, and why a question that describes a slowly decaying ACF is asking about differencing rather than about model order."},
  {"t": "step", "h": "The principle of parsimony",
   "body": "Among models that fit the data comparably, prefer the one with fewest parameters. Box and Jenkins made this explicit, and it has a specific consequence here: do not difference twice when once suffices, and do not add an MA term to patch a model whose d is wrong. Over-differencing and over-parameterising both improve the in-sample fit and both worsen forecasts."}],
 "ask": {
  "q": "Why is it useless to read p and q off the ACF and PACF of a series that has a unit root?",
  "nudge": "Look at the random walk's ACF from section 4 — 0.995, 0.976, 0.953, 0.913. What order would that pattern suggest?"}})

S.append({
 "kind": "recall", "id": "s11", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the conditions, the test's orientation and the two factorisations.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "What is the null hypothesis of the Dickey–Fuller test?",
   "a": "That the series has a unit root — non-stationarity. A failure to reject therefore points towards differencing."},
  {"q": "Give the invertibility condition for an MA(1) written yₜ = εₜ − θεₜ₋₁.",
   "a": "|θ| < 1 — the same form as the AR(1) stationarity condition."},
  {"q": "Is a finite MA process ever non-stationary?",
   "a": "No. It is a finite weighted sum of finitely many shocks, so its variance is finite and its autocovariances depend only on the lag."},
  {"q": "yₜ = 1.2yₜ₋₁ − 0.2yₜ₋₂ + εₜ. What does Δyₜ satisfy?",
   "a": "Δyₜ = 0.2Δyₜ₋₁ + εₜ, since 1 − 1.2B + 0.2B² = (1 − B)(1 − 0.2B). An AR(1) with φ = +0.2, so ARIMA(1, 1, 0)."},
  {"q": "What introduces a unit root into the MA part of a model?",
   "a": "Over-differencing — differencing a series that was already stationary."},
  {"q": "Which must be determined first, d or the pair (p, q)?",
   "a": "d. The ACF and PACF of a non-stationary series carry no usable information about p and q."}]})

S.append({
 "kind": "summary", "id": "s12", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Define a unit root three equivalent ways: z = 1 is a root of the AR polynomial, the coefficients sum to 1, and (1 − B) is a factor.",
  "List what a unit root costs: no finite variance, no ACF, permanent shocks, no mean to forecast towards, and spurious regressions.",
  "Compute the mean, variance and ACF of a random walk with drift, and recognise the slowly decaying ACF as the diagnostic signature.",
  "Factor the difference operator out of an AR polynomial and identify the model satisfied by the differenced series, getting the sign right.",
  "Use ARIMA(p, d, q) notation, and know that the middle number is the number of differencings required.",
  "State the invertibility condition for an MA process and apply the mirrored triangle, classifying a process as stationary, invertible, both or neither.",
  "Say what the Dickey–Fuller test tests, that the unit root is its null, and why the ordinary t table does not apply."]})

S.append({
 "kind": "theory", "id": "s13", "mins": 8, "ext": True,
 "title": "Why the Dickey–Fuller distribution is not a t distribution",
 "objective": "See where the standard theory breaks, which explains the separate tables rather than leaving them a recipe.",
 "blocks": [
  {"t": "step", "h": "What the usual theory assumes",
   "body": "The familiar result that a regression coefficient's t statistic is asymptotically normal rests on the regressors behaving well as the sample grows: specifically, that the average of their squares converges to a finite constant. For a stationary regressor that holds, because the series has a fixed variance to average towards."},
  {"t": "formula", "h": "What a unit-root regressor does instead",
   "body": "In Δyₜ = δyₜ₋₁ + εₜ, the regressor under H₀ is a random walk, with Var(yₜ) = tσ²ε. So\n    Σ yₜ₋₁²  grows like n² rather than like n,\nand the usual normalisation by n gives something that diverges. The standard limit theorems simply do not apply to it."},
  {"t": "step", "h": "What the correct limit looks like",
   "body": "Normalising by n² instead of n produces a limit, but it is not normal: it is expressed in terms of integrals of Brownian motion. The resulting distribution of the test statistic is skewed to the left and has no closed form, which is why Dickey and Fuller obtained its percentiles by simulation and published them as tables. Those tables are the reason the test carries their names rather than being called 'the t test for a unit root'."},
  {"t": "def", "h": "The practical consequence",
   "body": "The critical values are substantially MORE NEGATIVE than the ordinary t values — around −2.9 at the 5% level for a regression with a constant, against about −1.65 from the t distribution. So a statistic of −2.2 would be significant on a t table and is not significant on the correct one. Using the wrong table systematically declares stationarity that the data do not support, which is the more damaging direction of error, since it leads to modelling an undifferenced unit-root series."},
  {"t": "step", "h": "Extensions worth recognising by name",
   "body": "The augmented Dickey–Fuller test adds lagged difference terms to absorb autocorrelation in the residuals, which the original test assumes away; it is what software reports by default. The Phillips–Perron test achieves the same correction non-parametrically. And the KPSS test reverses the hypotheses, taking STATIONARITY as its null — which is why the two are often run together: agreement is reassuring and disagreement is honest evidence that the data cannot settle the question."}],
 "ask": {
  "q": "KPSS takes stationarity as its null while Dickey–Fuller takes the unit root. What does it mean if both fail to reject?",
  "nudge": "Each test fails to find evidence against its own null. What does that say about how much the data can distinguish?"}})

S.append({
 "kind": "quiz", "id": "s14", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "timeseries_t5_mastery"})

# --- explore scene, inserted after the intuition once the ar-acf visualisation existed
S.insert(2, {
 "kind": "explore", "id": "s1b", "mins": 7,
 "title": "Walk up to the boundary and over it",
 "objective": "See an ACF disappear as the coefficients reach a unit root, and see how little warning there is beforehand.",
 "viz": {"type": "ar-acf", "p1": 0.6, "p2": 0.35, "K": 14},
 "body": [
  "The stems are the autocorrelations the coefficients below produce. The chart starts at φ₁ = 0.6 and φ₂ = 0.35, which sums to 0.95 — inside the stationarity region, but only just.",
  "Look at how slowly the ACF decays. The readouts give ρ₁, ρ₂ and ρ₃, and the entry 'first lag with |ρ| < 0.05' tells you how long the correlation persists. At this setting the series is genuinely stationary and yet its correlations survive for a long time.",
  "Now raise φ₂ to 0.40, so φ₁ + φ₂ = 1 exactly. The chart stops drawing an ACF and states why: there is a unit root and no autocorrelation function exists. Nothing gradual happened — the sequence did not fade away, it ceased to be defined.",
  "That abruptness is the point of this lesson. On one side of the boundary there is a stationary process with a finite variance and a legitimate ACF; on the other there is a process whose variance grows without limit. The two look almost identical in a sample, which is section 7's problem with the Dickey–Fuller test's power.",
  "Go back and forth across the boundary a few times — 0.35, 0.39, 0.40, 0.41 — and watch what the readouts do. At 0.39 the ACF is still there and barely decaying; at 0.40 it is gone. A real series near this boundary gives you a sample ACF that looks like the 0.39 case whichever side the truth is on.",
  "Finally, set φ₁ = 1.2 and φ₂ = −0.2, the companion case from section 5. The sum is exactly 1, so again no ACF — and yet this process differences to a perfectly well-behaved AR(1) with φ = +0.2. Set φ₁ = 0.2, φ₂ = 0 to see the ACF of that differenced series, which is what the question actually asks for."],
 "ask": {
  "q": "At φ₂ = 0.39 the ACF exists and barely decays; at 0.40 it does not exist at all. What does that say about judging stationarity from a sample ACF?",
  "nudge": "If both sides of the boundary produce nearly identical-looking data, what can the sample tell you, and what can it not?"}})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "timeseriest5",
 "topicId": "timeseries-t5",
 "moduleId": "timeseries",
 "title": "Unit Roots, Differencing and ARIMA",
 "breadcrumb": "Time Series → Non-stationary models → Unit roots and differencing",
 "engine": "B",
 "engineName": "Time series — what to do when the series has no mean to return to",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Define a unit root three equivalent ways and say what it costs a model.",
  "Compute the mean, variance and ACF of a random walk with drift and recognise the diagnostic signature.",
  "Factor the difference operator out of an AR polynomial and identify the differenced model with the correct sign.",
  "Use ARIMA(p, d, q) notation and determine d.",
  "State and apply the invertibility condition, classifying a process as stationary, invertible, both or neither.",
  "Say what the Dickey–Fuller test tests, which hypothesis is its null, and why its critical values are not the t values."],
 "prereq": [
  {"id": "p1", "name": "The Yule–Walker equations",
   "why": "Topic 7.3 supplies the AR machinery, the stationarity triangle and the root condition. This lesson is what happens when that condition fails on the boundary."},
  {"id": "p2", "name": "Stationarity and white noise",
   "why": "Everything here is a departure from stationarity, so the three requirements must be clear enough to see which of them fails."},
  {"id": "p3", "name": "Polynomial factorisation",
   "why": "The entire technique is factoring (1 − B) out of an AR polynomial, and a sign slip there changes the final answer."},
  {"id": "p4", "name": "Size and power of a test",
   "why": "The Dickey–Fuller section turns on which hypothesis is the null and on the test's low power against a φ near 1 — both from the inference module."}],
 "traps": [
  "A unit root means the coefficients sum to exactly 1 — add them first.",
  "A random walk's variance is tσ²ε and grows; with drift the mean is μt and grows too.",
  "The d in ARIMA(p, d, q) is the MIDDLE number — an ARIMA(2,1,0) needs ONE differencing.",
  "The sign of the differenced model comes from the factorisation, not from the original equation.",
  "The Dickey–Fuller NULL is the unit root, so failing to reject means difference the series.",
  "Dickey–Fuller critical values are more negative than t values; a t table rejects too readily.",
  "A finite MA process is always stationary — only invertibility can fail.",
  "Over-differencing introduces an MA unit root and negative lag-1 autocorrelation."],
 "revision": {
  "sheet": [
   "Δ = 1 − B, so Δyₜ = yₜ − yₜ₋₁ and Δ²yₜ = yₜ − 2yₜ₋₁ + yₜ₋₂.",
   "Unit root: z = 1 solves φ(z) = 0; equivalently φ₁ + … + φₚ = 1; equivalently (1 − B) is a factor.",
   "Add the coefficients: sum < 1 possibly stationary, = 1 unit root, > 1 explosive.",
   "Consequences of a unit root: variance grows without limit, no ACF, shocks permanent, no mean to forecast to, spurious regressions.",
   "Random walk yₜ = yₜ₋₁ + εₜ with y₀ = 0: E(yₜ) = 0, Var(yₜ) = tσ²ε. ARIMA(0,1,0).",
   "With drift yₜ = μ + yₜ₋₁ + εₜ: yₜ = μt + Σεᵢ, so E(yₜ) = μt and Var(yₜ) = tσ²ε.",
   "Random-walk ACF: Corr(yₜ, yₜ₊ₖ) = √(t/(t+k)). At t = 100 this is 0.995, 0.976, 0.953, 0.913, 0.816 for k = 1, 5, 10, 20, 50 — the slow, near-linear decay that signals a unit root.",
   "Compare: a stationary AR(1) with φ = 0.9 has ρ₅₀ = 0.9⁵⁰ ≈ 0.005.",
   "Factor and difference: φ(B) = (1 − B)ψ(B) gives ψ(B)Δyₜ = εₜ, so Δyₜ follows the lower-order model.",
   "June 2026 Q18: 1 − 0.6B − 0.4B² = (1 − B)(1 + 0.4B) ⟹ Δyₜ = −0.4Δyₜ₋₁ + εₜ, ACF (−0.4)ᵏ, ARIMA(1,1,0).",
   "Companion case: 1 − 1.2B + 0.2B² = (1 − B)(1 − 0.2B) ⟹ Δyₜ = +0.2Δyₜ₋₁ + εₜ, ACF (0.2)ᵏ, also ARIMA(1,1,0).",
   "ARIMA(p, d, q): differencing d times leaves a stationary ARMA(p, q). d = 1 usually; d = 2 occasionally; never more.",
   "Invertibility (Box–Jenkins minus convention): MA(1) needs |θ| < 1; MA(2) needs θ₁ + θ₂ < 1, θ₂ − θ₁ < 1, |θ₂| < 1 — the same triangle as stationarity, applied to θ.",
   "Stationarity constrains the AR part, invertibility the MA part, and the two are independent.",
   "φ = (0.4, 0.3), θ = (0.6, 0.4): stationary (sum 0.7) but NOT invertible (sum 1.0).",
   "A finite MA process is always stationary; a non-invertible MA has the same ACF as an invertible one, so invertibility is needed for identification.",
   "Over-differencing introduces an MA unit root — the reason to difference as few times as possible.",
   "Dickey–Fuller: from yₜ = φyₜ₋₁ + εₜ write Δyₜ = δyₜ₋₁ + εₜ with δ = φ − 1; test H₀: δ = 0 (unit root) against H₁: δ < 0 (stationary).",
   "Its critical values are tabulated separately and are more negative than t values — about −2.9 at 5% with a constant, against −1.65 from the t distribution.",
   "The test has low power against φ near 1 (say 0.95), so combine it with the sample ACF and with judgement. The augmented version adds lagged differences; KPSS reverses the hypotheses.",
   "Box–Jenkins cycle: identify (d first, then p and q), estimate, check residuals, repeat. Determine d before reading any ACF for order."],
  "cards": [
   ["A unit root, three ways", "z = 1 is a root of φ(z); the coefficients sum to 1; (1 − B) is a factor"],
   ["The one-line test", "Add the AR coefficients: 1 means a unit root, more than 1 means explosive"],
   ["Random walk mean and variance", "With y₀ = 0 and drift μ: E(yₜ) = μt, Var(yₜ) = tσ²ε — both grow with t"],
   ["Random walk ACF", "√(t/(t+k)) — still 0.816 at lag 50 when t = 100, the slow-decay signature"],
   ["What differencing does", "φ(B) = (1 − B)ψ(B), so ψ(B)Δyₜ = εₜ and the differenced series follows ψ"],
   ["Q18's answer", "(1 − B)(1 + 0.4B), so Δyₜ = −0.4Δyₜ₋₁ + εₜ and the ACF is (−0.4)ᵏ"],
   ["The companion case", "(1 − B)(1 − 0.2B), so Δyₜ = +0.2Δyₜ₋₁ + εₜ — the sign comes from the factorisation"],
   ["ARIMA(p, d, q)", "d is the number of differencings; ARIMA(2,1,0) needs one and is then a pure AR(2)"],
   ["Invertibility", "The same triangle as stationarity, applied to the θ's; MA(1) needs |θ| < 1"],
   ["A finite MA process", "Always stationary — only invertibility can fail"],
   ["Dickey–Fuller's null", "The UNIT ROOT. Failing to reject means difference the series"],
   ["Why not a t table", "Under the null the regressor is non-stationary, so the limit is not normal; critical values are more negative"]],
  "tricks": [
   "Add the coefficients before anything else. It settles stationary, unit root or explosive in one line.",
   "Expand any factorisation back out before using it; a sign slip there changes the final ACF.",
   "The sign of the differenced model's coefficient is the opposite of the sign inside its factor: (1 + 0.4B) gives −0.4, (1 − 0.2B) gives +0.2.",
   "For an ARIMA question, read the middle number — that is the one being asked about nine times out of ten.",
   "Check the AR part first when classifying: a unit root there settles non-stationarity regardless of the MA part."],
  "shortcuts": [
   "A finite MA is stationary automatically, so for a pure MA question only invertibility needs testing.",
   "The invertibility conditions are the stationarity conditions with θ in place of φ — one region to remember, not two.",
   "If a question describes a slowly or linearly decaying sample ACF, the answer involves differencing, whatever else it mentions."],
  "remember": [
   "Sum the coefficients. 1 means difference.",
   "d is the middle number.",
   "Dickey–Fuller's null is the unit root."]},
 "howto": "Read this after topic 7.3, which it depends on throughout. Sections 2 and 3 are the core: what a unit root is and what it costs, then the random walk computed in full — and the ACF values at the end of section 3 are the single most useful thing to remember, because they are what non-stationarity looks like in real data. Section 5 has you difference an AR(2) yourself, and the contrast with June 2026 Q18 at the end of it is the point: both are ARIMA(1,1,0) and the surviving coefficients have opposite signs. Section 7 covers the Dickey–Fuller test, whose null trips people up, and section 9 drills the stationary-versus-invertible classification that the summary questions use. If short of time, sections 2, 3, 5 and 7 are the lesson. Attempt the question at the end of each section before opening the answer. The optional section explains why the test needs its own tables.",
 "refs": [
  {"title": "Time Series Analysis", "where": "Lessons 3 and 8, on differencing and non-stationarity",
   "site": "Penn State STAT 510", "url": "https://online.stat.psu.edu/stat510/",
   "type": "Course notes", "free": True, "checked": "2026-11-03",
   "why": "Differencing, ARIMA notation and the identification sequence worked on real series. The right companion to sections 2 and 10."},
  {"title": "Time Series Analysis: Forecasting and Control",
   "where": "Chapters 4 and 6, integrated models and model identification",
   "site": "Box, Jenkins and Reinsel", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The origin of the ARIMA formulation, the invertibility conditions and the three-stage cycle of section 10."},
  {"title": "Time Series Analysis and Its Applications", "where": "Chapters 3 and 5",
   "site": "Shumway and Stoffer", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "Unit-root testing and the non-standard limiting distribution, which is what the optional section sketches."},
  {"title": "Time Series Analysis", "where": "Weeks on ARIMA modelling and unit roots",
   "site": "NPTEL / SWAYAM", "url": "https://archive.nptel.ac.in/courses/111104049",
   "type": "Video course", "free": True, "checked": "2026-11-03",
   "why": "Indian syllabus notation for ARIMA and the Dickey–Fuller test, matching the phrasing NET questions use."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026 for this platform against the UGC NET Statistics syllabus, and the second lesson of the time-series module. It is the natural home of June 2026 Q18, whose process yₜ = 0.6yₜ₋₁ + 0.4yₜ₋₂ + εₜ has coefficients summing to 1; topic 7.3 worked that question as a warning and this lesson is the full treatment. Seven of the ten practice variants tagged to Q18 are squarely this topic, and all ten were read WITH THEIR OPTIONS AND ANSWERS before authoring, because the sign convention for MA invertibility is not guessable: the variant giving φ = (0.4, 0.3) and θ = (0.6, 0.4) with the answer 'stationary but not invertible' establishes that the minus convention is in use, so the invertibility region mirrors the stationarity triangle and θ₁ + θ₂ = 1.0 fails it. The variants taught and pooled are: the random walk's non-stationarity, its mean μt and variance tσ²ε, φ₁ + φ₂ = 1 implying a unit root, the differencing of yₜ = 1.2yₜ₋₁ − 0.2yₜ₋₂ + εₜ to an AR(1) with φ = +0.2, ARIMA(2,1,0) needing one differencing, MA(1) invertibility requiring |θ| < 1, the Dickey–Fuller test's target, the slowly decaying sample ACF, and the ARMA classification above. Every numerical value was computed rather than recalled: the random-walk ACF √(t/(t+k)) evaluated at t = 100 as 0.995, 0.976, 0.953, 0.913 and 0.816 for lags 1, 5, 10, 20 and 50, against 0.9⁵⁰ ≈ 0.005 for a stationary comparison; both factorisations expanded back out as checks; and both triangles applied to the ARMA(2,2) coefficients. Like topic 7.3 this lesson has no explore scene, because src/30-viz.js contains no time-series visualisation. Previous-year questions themselves are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "ts-t5-m-%02d" % i, "format": fmt, "topic": "timeseries-t5",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "The process yₜ = yₜ₋₁ + εₜ is:",
 ["a random walk, non-stationary", "stationary", "an MA(1) process",
  "invertible but not stationary"],
 "A",
 "It is the AR(1) with φ = 1 exactly. Unrolling gives yₜ as the sum of all shocks to date, so Var(yₜ) = tσ²ε grows without limit and stationarity fails. It is the simplest unit-root process, ARIMA(0, 1, 0)."))

I.append(q(2, "numeric", "easy",
 "For the random walk with drift yₜ = μ + yₜ₋₁ + εₜ starting from y₀ = 0, the mean and variance of yₜ are:",
 ["μ and σ²ε", "μ and tσ²ε", "μt and tσ²ε", "μt and σ²ε"],
 "C",
 "Unrolling gives yₜ = μt + (ε₁ + … + εₜ), so the drift accumulates into a mean of μt and the uncorrelated shocks accumulate into a variance of tσ²ε. Both depend on t, so neither the constant-mean nor the constant-variance requirement of stationarity holds.",
 check="Both quantities must carry a factor of t, because both the drift and the shocks accumulate. An answer where either is free of t has not unrolled the recursion."))

I.append(q(3, "single", "easy",
 "If φ₁ + φ₂ = 1 in an AR(2) process, the process:",
 ["is white noise", "is stationary", "is invertible", "has a unit root"],
 "D",
 "φ(1) = 1 − φ₁ − φ₂ = 0, so z = 1 is a root of the AR polynomial and (1 − B) factors out. The process is not stationary, has no ACF, and must be differenced before any ACF-based method applies."))

I.append(q(4, "numeric", "easy",
 "An ARIMA(2, 1, 0) process becomes stationary after:",
 ["two differencings", "one differencing", "no differencing", "taking logarithms"],
 "B",
 "The middle number of ARIMA(p, d, q) is d, the number of differencings required — here 1. The 2 is the AR order of what remains, so after one differencing the series is a stationary AR(2). Confusing p with d is the standard error.",
 check="Read the middle number. It is d, not the AR order and not the MA order."))

I.append(q(5, "single", "easy",
 "The MA(1) process yₜ = εₜ − θεₜ₋₁ is invertible if:",
 ["|θ| > 1", "|θ| < 1", "θ = 1", "always"],
 "B",
 "The MA polynomial is 1 − θz, whose root 1/θ lies outside the unit circle exactly when |θ| < 1. This is the same condition on θ that stationarity imposes on φ for an AR(1) — the invertibility region mirrors the stationarity region."))

I.append(q(6, "single", "easy",
 "The Dickey–Fuller test is used to test for:",
 ["a unit root", "autocorrelation of residuals", "heteroscedasticity", "normality"],
 "A",
 "It tests whether a series has a unit root, and the unit root is its NULL hypothesis — so failing to reject points towards differencing the series. The alternative is stationarity."))

# --- moderate (10)
I.append(q(7, "single", "moderate",
 "A sample ACF that decays very slowly and almost linearly, and is still large at lag 20, suggests:",
 ["seasonality", "a unit root — difference the series", "an MA process", "white noise"],
 "B",
 "A stationary AR or MA ACF decays geometrically and would be negligible by lag 20. A random walk's ACF is √(t/(t+k)), which at t = 100 is still 0.913 at lag 20 and 0.816 at lag 50 — exactly this slow, near-linear pattern. The remedy is differencing, confirmed formally by a Dickey–Fuller test."))

I.append(q(8, "single", "moderate",
 "For yₜ = 1.2yₜ₋₁ − 0.2yₜ₋₂ + εₜ, the differenced series Δyₜ is:",
 ["AR(1) with φ = 0.2", "AR(1) with φ = −0.2", "white noise", "MA(1)"],
 "A",
 "The coefficients sum to 1.2 − 0.2 = 1, so there is a unit root. Factoring: 1 − 1.2B + 0.2B² = (1 − B)(1 − 0.2B), so (1 − 0.2B)Δyₜ = εₜ and therefore Δyₜ = +0.2Δyₜ₋₁ + εₜ. The sign comes from the factor (1 − 0.2B); reading −0.2 off the original equation gives the wrong answer."))

I.append(q(9, "numeric", "moderate",
 "For a random walk with y₀ = 0 observed at t = 100, the correlation between y₁₀₀ and y₁₁₀ is:",
 ["0.995", "0.953", "0.913", "0.500"],
 "B",
 "Corr(yₜ, yₜ₊ₖ) = √(t/(t + k)) = √(100/110) = 0.953. The first option is the lag-1 value √(100/101) and the third is the lag-20 value √(100/120). The point is how slowly this falls: a stationary AR(1) with φ = 0.9 would already be at 0.9¹⁰ = 0.35 by lag 10.",
 check="The correlation depends on both t and k — which is itself proof of non-stationarity, since a stationary ACF depends on k alone."))

I.append(q(10, "single", "moderate",
 "For a process with φ₁ = 0.4, φ₂ = 0.3, θ₁ = 0.6, θ₂ = 0.4 (MA written with minus signs), the process is:",
 ["stationary and invertible", "stationary but not invertible",
  "invertible but not stationary", "neither"],
 "B",
 "Stationarity uses the φ triangle: 0.4 + 0.3 = 0.7 < 1 ✓, 0.3 − 0.4 = −0.1 < 1 ✓, |0.3| < 1 ✓ — stationary. Invertibility uses the same triangle on the θ values: 0.6 + 0.4 = 1.0, which is not less than 1 ✗. The MA part sits exactly on the boundary, an MA unit root, so the process is not invertible."))

I.append(q(11, "single", "moderate",
 "Which statement about a finite moving-average process is correct?",
 ["it is always stationary, whatever its coefficients",
  "it is stationary only if |θ| < 1",
  "it is never stationary", "its stationarity depends on the sample size"],
 "A",
 "A finite MA is a weighted sum of finitely many shocks, so its variance is finite and its autocovariances depend only on the lag — stationarity is automatic. The |θ| < 1 condition is for INVERTIBILITY, not stationarity, and conflating the two is the trap this question sets."))

I.append(q(12, "multi", "moderate",
 "Consider a series with a unit root.",
 ["A, B and D only", "A and C only", "B and C only", "A, B and C only"],
 "A",
 "A is true — the variance of a random walk is tσ²ε. B is true: with no finite variance there is nothing to divide the autocovariances by. C is false — a unit root is the boundary case, and it is roots INSIDE the unit circle that give explosive behaviour. D is true, and it is the practical hazard the regression literature is built around.",
 statements=["The variance grows without limit as t increases.",
             "There is no autocorrelation function.",
             "The process is explosive, with values growing geometrically.",
             "Regressing one such series on another can produce a spurious relationship."],
 verdicts=verd(
  (True, "True. For a random walk Var(yₜ) = tσ²ε, which grows linearly in t and has no limit."),
  (True, "True. The ACF divides autocovariances by the variance, and there is no finite variance to divide by."),
  (False, "False. A unit root sits exactly ON the unit circle and gives a wandering, not an exploding, series. Explosive behaviour needs a root strictly inside the circle, equivalently coefficients summing to more than 1."),
  (True, "True. Two independent random walks that both happen to drift produce a strong apparent relationship, and the problem worsens as the sample grows."))))

I.append(q(13, "single", "moderate",
 "In the Dickey–Fuller regression Δyₜ = δyₜ₋₁ + εₜ, the hypotheses are:",
 ["H₀: δ = 0 against H₁: δ < 0", "H₀: δ = 0 against H₁: δ > 0",
  "H₀: δ = 1 against H₁: δ < 1", "H₀: δ < 0 against H₁: δ = 0"],
 "A",
 "Starting from yₜ = φyₜ₋₁ + εₜ and subtracting yₜ₋₁ gives δ = φ − 1. A unit root means φ = 1, so δ = 0 — the null. Stationarity means φ < 1, so δ < 0, and the alternative is one-sided in the negative direction."))

I.append(q(14, "single", "moderate",
 "A Dickey–Fuller test returns a p-value of 0.31. The correct action is:",
 ["conclude the series is stationary and model it directly",
  "treat the series as non-stationary and difference it",
  "conclude a unit root has been proved",
  "conclude the test is invalid"],
 "B",
 "The null is the unit root, so a large p-value means insufficient evidence against non-stationarity, and the appropriate action is to difference. It does not PROVE a unit root — the test has low power against a φ near 1 — but differencing is the conservative and conventional response."))

I.append(q(15, "single", "moderate",
 "Over-differencing a series that was already stationary:",
 ["has no effect", "introduces a unit root into the MA part",
  "removes all autocorrelation", "always improves forecasts"],
 "B",
 "Differencing a stationary series multiplies its model by (1 − B), which puts a unit root in the MA part — detectable as artificially strong negative autocorrelation at lag 1 and an inflated variance. It is why the rule is to difference as few times as makes the series stationary and no more."))

I.append(q(16, "numeric", "moderate",
 "For the process yₜ = yₜ₋₁ + εₜ − 0.4εₜ₋₁, the classification and ARIMA order are:",
 ["stationary and invertible, ARIMA(1, 0, 1)", "invertible but not stationary, ARIMA(0, 1, 1)",
  "stationary but not invertible, ARIMA(0, 1, 1)", "neither, ARIMA(1, 1, 1)"],
 "B",
 "The AR coefficient is exactly 1, a unit root, so the process is not stationary whatever the MA part does. The MA part has |−0.4| < 1 so it is invertible. No AR terms remain after differencing, one difference, one MA term: ARIMA(0, 1, 1), and Δyₜ = εₜ − 0.4εₜ₋₁ is a stationary invertible MA(1).",
 check="Check the AR part first; a unit root there settles non-stationarity. Then count: p = 0, d = 1, q = 1."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the Dickey–Fuller test and its critical values.",
 ["A, B and D only", "A and C only", "B and C only", "A, B and C only"],
 "A",
 "A is true and is the reason the standard theory fails. B is true — the critical values are around −2.9 at 5% with a constant, against about −1.65 from the t distribution. C is false: using the t table makes the test reject too EASILY, declaring stationarity that is not supported. D is true, and it is why the two tests are often run together.",
 statements=["Under the null the regressor yₜ₋₁ is non-stationary, so the usual asymptotic theory does not apply.",
             "The correct critical values are more negative than the ordinary t values.",
             "Using an ordinary t table makes the test too conservative.",
             "The KPSS test reverses the hypotheses, taking stationarity as its null."],
 verdicts=verd(
  (True, "True. Σyₜ₋₁² grows like n² rather than n under the null, so the limit is not normal — it involves integrals of Brownian motion and was tabulated by simulation."),
  (True, "True — about −2.9 at the 5% level with a constant, against roughly −1.65 from the t distribution."),
  (False, "False, and the direction matters. More negative correct values mean the t table rejects too readily, so the error is declaring stationarity that the data do not support — the more damaging direction."),
  (True, "True. KPSS takes stationarity as its null, so the two are often run together; agreement is reassuring and disagreement shows the data cannot settle the question."))))

I.append(q(18, "single", "hard",
 "Two AR(2) processes both have a unit root: yₜ = 0.6yₜ₋₁ + 0.4yₜ₋₂ + εₜ and yₜ = 1.2yₜ₋₁ − 0.2yₜ₋₂ + εₜ. Their differenced series are:",
 ["both AR(1) with φ = 0.2", "AR(1) with φ = −0.4 and AR(1) with φ = 0.2",
  "AR(1) with φ = 0.6 and AR(1) with φ = 1.2", "both white noise"],
 "B",
 "The polynomials factor as (1 − B)(1 + 0.4B) and (1 − B)(1 − 0.2B) respectively, so the differenced series satisfy Δyₜ = −0.4Δyₜ₋₁ + εₜ and Δyₜ = +0.2Δyₜ₋₁ + εₜ. Both are ARIMA(1, 1, 0) and the surviving coefficients have opposite signs — the sign comes from the factorisation, never from the original equation, which is what the third option wrongly assumes."))

I.append(q(19, "single", "hard",
 "Why is invertibility required of a moving-average model, given that a finite MA is always stationary?",
 ["because without it the variance is infinite",
  "because the shocks cannot otherwise be recovered from the data, and two parameter values give the same ACF",
  "because the mean would depend on time",
  "because the ACF would not decay"],
 "B",
 "Using an MA model means recovering the unobserved shocks from the observed series, which requires inverting the MA operator — and that inversion converges only under the invertibility condition. The identification point is just as important: the MA(1) with θ = 1.5 has exactly the same ACF as the one with θ = 1/1.5, so without invertibility the parameter is not determined by the data."))

I.append(q(20, "single", "hard",
 "An analyst reads p and q from the sample ACF and PACF of an undifferenced series that has a unit root. The result is:",
 ["valid, since the ACF and PACF are computed the same way regardless",
  "uninformative, because the slow decay of a non-stationary ACF swamps any AR or MA pattern",
  "valid only if the series has drift", "an over-differenced model"],
 "B",
 "A unit-root series has an ACF near 1 at every short lag and decaying almost linearly, so it carries no usable information about order — it would suggest a very high AR order at every attempt. This is why d must be determined FIRST, and why a question describing a slowly decaying ACF is asking about differencing rather than about model order."))

# A pool whose keys pile onto one letter rewards a guesser, and the validator caps any
# letter at 40%. Swapping positions i and j is its own inverse, so an "option X" mention
# inside an explanation just swaps the same two letters.
LET = "ABCD"
WANT = {"ts-t5-m-01": "C", "ts-t5-m-03": "B", "ts-t5-m-05": "D",
        "ts-t5-m-06": "D", "ts-t5-m-07": "C", "ts-t5-m-08": "D",
        "ts-t5-m-11": "C", "ts-t5-m-13": "C", "ts-t5-m-15": "A",
        "ts-t5-m-18": "A", "ts-t5-m-19": "D", "ts-t5-m-20": "A"}

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
        # only "option X" wording is swapped; multi-statement explanations refer to
        # statements as bare letters and are left alone
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
 "moduleId": "timeseries", "topicId": "timeseries-t5", "source": "mastery",
 "label": "Unit roots, differencing and ARIMA — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
