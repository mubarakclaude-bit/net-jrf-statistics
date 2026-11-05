#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 7.6 — Random walk with and without drift (timeseries-t6).

PYQ anchor. June 2026 Q23 (answered CORRECTLY, marked D): for y_t = mu + y_{t-1} + eps_t with
E(eps)=0 and Var(eps)=sigma^2, the mean and variance of y_t are t*mu and t*sigma^2 — option D.
Both moments grow with t, which is the defining feature: a random walk has no fixed level to
return to and no fixed variance.

Nine variants under Q23, all taught in named sections and pooled. They cover more than the
random walk itself — weak vs strict stationarity, trend-stationary vs difference-stationary,
over-differencing, and the ARIMA(0,1,0) label — so the lesson is the random walk treated as the
canonical non-stationary process rather than as an isolated formula.

Boundaries with the two time-series lessons already built:
 - 7.5 covers unit roots, the Dickey-Fuller test and ARIMA orders in general. This lesson does
   not repeat them; it cross-references and instead works the random walk's own moments, its
   slowly decaying ACF, and the trend- versus difference-stationary distinction.
 - 7.3 covers Yule-Walker. Referenced once, not repeated.

Uses the existing `ar-acf` visualisation rather than a new one: a random walk is the AR(1) case
phi = 1, which sits exactly on the stationarity boundary, so the chart reports non-stationarity
and names the failing condition. That is the right picture for this topic.

Writes seed/lesson_ts6.json and seed/timeseries_t6_mastery.json.
"""
import json, io, os, re

OUT = "seed/lesson_ts6.json"
POOL = "seed/timeseries_t6_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 7,
 "title": "Before the lesson — four things it will assume",
 "objective": "Fix what stationarity demands, and what accumulating independent shocks does.",
 "ask": {
  "q": "A series is the running total of independent shocks. Can its variance be constant?",
  "nudge": "Each new shock adds its own variance to the total, and nothing ever subtracts any."},
 "body": [
  "A random walk is the simplest non-stationary process, and it is the one against which stationarity is defined. Everything about it follows from one line: it is the running total of independent shocks, so each shock stays in the series forever.",
  "That has two immediate consequences. The variance grows without bound, because variances of independent terms add and nothing removes them. And the effect of any single shock is permanent, because the series never returns to a previous level — there is no level to return to.",
  "Both are exactly what stationarity forbids. So the random walk is the canonical counterexample, and it is also the canonical case where differencing fixes things: the first difference of a random walk is the shock itself, which is white noise.",
  "Four checks before starting."],
 "items": [
  {"ask": "What does weak (second-order) stationarity require?",
   "recall": "A constant mean, a constant variance, and an autocovariance depending only on the LAG, not on where in the series you are.",
   "refresh": [
    "All three conditions are about things not changing with t. A practice variant asks what the autocovariance may depend on, and the answer is the lag only.",
    "Strict stationarity is stronger: the whole joint distribution must be invariant under a time shift. For a GAUSSIAN process the two coincide, since a Gaussian process is determined by its mean and autocovariance — another practice variant.",
    "A random walk fails the second and third conditions while, without drift, satisfying the first. One failure is enough."]},
  {"ask": "If Z₁, …, Zₜ are independent each with variance σ², what is the variance of their sum?",
   "recall": "tσ² — variances of independent terms add.",
   "refresh": [
    "There is no covariance term to worry about, so the total variance is simply t times σ². It therefore grows linearly in t and without limit.",
    "This single fact is why Var(yₜ) = tσ² for a random walk, which is June 2026's answer and the lesson's central result.",
    "The standard deviation grows like √t, which is why a random walk's path wanders ever further from its start but does so at a decelerating rate."]},
  {"ask": "What is the first difference of a random walk yₜ = yₜ₋₁ + εₜ?",
   "recall": "Δyₜ = yₜ − yₜ₋₁ = εₜ, which is white noise — stationary.",
   "refresh": [
    "So one differencing turns the random walk into something stationary, which is what 'integrated of order 1' means and why a random walk is ARIMA(0, 1, 0). Both are practice variants.",
    "With drift, Δyₜ = μ + εₜ, still stationary — just with a non-zero mean. Differencing removes the accumulating part and leaves the drift as a constant.",
    "Topic 7.5 covers unit roots and the Dickey–Fuller test that detects them; this lesson is about the process itself."]},
  {"ask": "What is a purely random process, and what are its mean and autocovariance?",
   "recall": "White noise: mean 0, variance σ², and zero autocovariance at every non-zero lag.",
   "refresh": [
    "'Purely random' is the phrase June 2026's question uses for the shocks. It is stationary by construction, with a flat autocorrelation function that is 1 at lag 0 and 0 everywhere else.",
    "The random walk is built from white noise, which is the point: a stationary input accumulated into a non-stationary output.",
    "Topic 7.7 shows white noise also has a flat spectral density, which is the frequency-domain version of the same statement."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "A process with no level to return to",
 "objective": "See what 'non-stationary' means concretely before the algebra.",
 "body": [
  "Take a stationary AR(1), yₜ = φyₜ₋₁ + εₜ with |φ| < 1. A shock arrives, moves the series, and then fades: its effect at k steps later is φᵏ, which decays geometrically. The series has a mean it returns to and a variance it keeps.",
  "Now set φ = 1. The shock's effect at k steps later is 1ᵏ = 1 — undiminished, forever. Nothing fades, so nothing is returned to. The series is a random walk, and its variance grows as tσ² without limit.",
  "That is the whole distinction, and it is a knife edge. At φ = 0.99 the process is stationary, with a variance of σ²/(1 − 0.99²) ≈ 50σ² — large, but finite, and the series does eventually revert. At φ = 1 the variance is infinite and reversion never happens. A difference of 0.01 in a coefficient changes the qualitative behaviour completely.",
  "The practical importance is that the two look alike in a short sample. A stationary series with φ = 0.99 and a random walk are nearly indistinguishable over a hundred observations, which is why formal tests exist and why eyeballing a plot is not enough — topic 7.5's Dickey–Fuller test is the standard one."],
 "scenario": {
  "teaser": "Two unrelated random walks are regressed on each other and the relationship is highly significant.",
  "title": "The spurious regression, and why it happens",
  "body": [
   "An analyst has two economic series, each of which looks like it trends upward over the sample. Regressing one on the other gives a large t-statistic, a high R², and an apparently strong relationship.",
   "The two series were in fact generated as independent random walks, with no connection whatever. The regression is spurious, and the problem is not bad luck — it happens most of the time. With independent random walks, the proportion of samples in which the slope appears significant at the 5% level rises towards 1 as the sample grows, rather than settling at 0.05.",
   "The cause is the accumulation. Each series wanders away from its start and stays wherever it has wandered, so over any finite window each one has an apparent direction. Two series each with an apparent direction will appear related, and the usual standard errors are computed under an assumption — stationary, weakly dependent errors — that a random walk violates completely.",
   "What breaks specifically is the standard error, not the coefficient. The residuals of such a regression are themselves non-stationary, so the usual residual variance understates the true uncertainty by a factor that grows with the sample size. A larger sample makes the t-statistic bigger rather than more honest, which is the opposite of the usual reassurance.",
   "Two repairs are standard. Difference both series and regress the changes, which is valid because the differences are stationary — at the cost of discarding information about levels. Or test formally whether the two series are cointegrated, meaning some linear combination of them IS stationary, in which case a relationship between the levels is real and can be estimated.",
   "The diagnostic habit worth forming is to check each series for a unit root BEFORE regressing levels on levels. A significant relationship between two non-stationary series is uninformative until that check has been done."],
  "q": "Why does a larger sample make the spurious relationship look stronger rather than exposing it?",
  "answer": "Because the standard error is computed under an assumption the data violate. The usual formula treats the regression residuals as stationary with finite variance, but when both series are random walks the residuals are themselves non-stationary and their variance grows with t. So the reported standard error understates the true uncertainty, and the understatement grows with the sample size — making the t-statistic larger as n increases. The coefficient estimate is not the problem; the yardstick used to judge it is. This is why the rejection rate tends towards 1 rather than towards the nominal 5%, and why a unit-root check has to come before the regression."},
 "ask": {
  "q": "At φ = 0.99 the variance is about 50σ² and at φ = 1 it is unbounded. What does that say about distinguishing the two from a short series?",
  "nudge": "How many observations would you need to see the difference between a slow return to the mean and no return at all?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Watch the stationarity boundary from the inside",
 "objective": "See the ACF survive up to φ = 1 and then vanish.",
 "viz": {"type": "ar-acf", "p1": 0.95, "p2": 0,
         "caption": "The ACF and PACF of an AR process. Set φ₂ to 0 for an AR(1) and move φ₁ towards 1: the ACF decays ever more slowly, and at φ₁ = 1 the process is a random walk, for which no ACF exists at all."},
 "body": [
  "Start with φ₂ = 0 and φ₁ = 0.95, which is a stationary AR(1). The ACF decays geometrically as 0.95ᵏ — slowly, but it does decay, and the process has a finite variance.",
  "Push φ₁ to 1.00. The chart stops drawing stems and reports that the process is not stationary, naming the condition that failed: φ₁ + φ₂ < 1 is violated with equality. This is not a gap in the chart — there is genuinely no ACF to draw, because the autocorrelation function of a non-stationary process is undefined. There is no finite variance to divide by.",
  "That is worth dwelling on. The random walk is the AR(1) with φ = 1, sitting exactly on the boundary. It is not 'an AR(1) with a very persistent memory'; it is outside the stationary family altogether, and the quantities the family is described by do not exist for it.",
  "Now step back to 0.95, 0.90, 0.80 and watch the decay speed up. The contrast between 0.95 and 1.00 is the whole content of unit-root testing: the behaviour changes qualitatively at a single point, while the ACF changes continuously as the boundary is approached.",
  "Section 4 derives what the random walk has INSTEAD of an ACF: a correlation between yₜ and yₜ₊ₖ that depends on t as well as k, and decays like √(t/(t+k)) — very slowly indeed."],
 "ask": {
  "q": "The chart refuses to draw an ACF at φ₁ = 1. What quantity is missing that an ACF requires?",
  "nudge": "An autocorrelation is a covariance divided by something. What is that something for a random walk?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The random walk's moments, and the two kinds of non-stationarity",
 "objective": "Derive every moment and separate trend-stationary from difference-stationary.",
 "blocks": [
  {"t": "formula", "h": "The process and its solution",
   "body": "With drift:    yₜ = μ + yₜ₋₁ + εₜ,   y₀ = 0\nSolving recursively:\n    yₜ = tμ + (ε₁ + ε₂ + ⋯ + εₜ).\nSo the series is a deterministic line tμ plus the running total of all shocks so far. Without drift (μ = 0) it is the running total alone."},
  {"t": "formula", "h": "Mean and variance",
   "body": "E(yₜ) = tμ          (the shocks have mean 0)\nVar(yₜ) = tσ²       (variances of independent shocks add)\nBoth grow with t. This is June 2026's answer, option D. Without drift the mean is 0 but the variance is still tσ², which is a separate practice variant — note the mean can be constant while the variance is not, and one failure is enough to destroy stationarity."},
  {"t": "formula", "h": "Autocovariance and autocorrelation",
   "body": "Cov(yₜ, yₜ₊ₖ) = tσ²,  for k ≥ 0,\nbecause the two sums share exactly their first t shocks and the rest are independent. Hence\n    Corr(yₜ, yₜ₊ₖ) = tσ² / √(tσ² · (t+k)σ²) = √( t/(t+k) ).\nThis depends on t as well as on k, which is precisely what weak stationarity forbids — and it is a practice variant. At t = 100 the correlations at lags 1, 5, 10, 20 and 50 are 0.995, 0.976, 0.953, 0.913 and 0.816: a very slow decay, which is what non-stationarity looks like in a sample ACF."},
  {"t": "step", "h": "Differencing, and the ARIMA label",
   "body": "Δyₜ = yₜ − yₜ₋₁ = μ + εₜ.\nWith no drift this is white noise; with drift it is white noise plus a constant. Either way it is stationary, so the random walk is integrated of order 1 and is exactly ARIMA(0, 1, 0) — no AR terms, one difference, no MA terms. Both the 'differencing once' and the 'ARIMA(0,1,0)' variants are this line."},
  {"t": "def", "h": "Trend-stationary versus difference-stationary",
   "body": "Two quite different processes both look like they trend:\n    yₜ = 5 + 0.2t + εₜ          TREND-stationary: a deterministic line plus stationary noise.\n    yₜ = 0.2 + yₜ₋₁ + εₜ        DIFFERENCE-stationary: a random walk with drift.\nBoth have a mean rising at 0.2 per period. But the first has constant variance σ² and returns to its trend line after a shock, while the second has variance tσ² and never returns. A practice variant asks which category yₜ = 5 + 0.2t + εₜ falls into, and the answer is trend-stationary."},
  {"t": "step", "h": "Why the distinction matters, and over-differencing",
   "body": "The repairs differ. A trend-stationary series should have its trend SUBTRACTED (de-trended); a difference-stationary one should be DIFFERENCED. Applying the wrong repair damages the series.\nDifferencing something already stationary is over-differencing, and it introduces a non-invertible moving-average component: if yₜ = εₜ then Δyₜ = εₜ − εₜ₋₁, an MA(1) with θ = 1, exactly on the invertibility boundary. Simulated: Var(Δy) = 2.01 against the exact 2, and lag-1 autocorrelation −0.4998 against the exact −0.5. A practice variant asks what over-differencing produces, and the answer is that non-invertible MA component."}],
 "table": {
  "caption": "The random walk against its stationary neighbour and its trend-stationary look-alike. Every figure computed and simulated.",
  "head": ["process", "E(yₜ)", "Var(yₜ)", "shock effect", "stationary?"],
  "rows": [
   ["white noise εₜ", "0", "σ²", "one period", "yes"],
   ["AR(1), |φ| < 1", "0", "σ²/(1−φ²)", "φᵏ, decaying", "yes"],
   ["yₜ = 5 + 0.2t + εₜ", "5 + 0.2t", "σ²", "one period", "trend-stationary"],
   ["random walk, no drift", "0", "tσ²", "permanent", "no"],
   ["random walk with drift μ", "tμ", "tσ²", "permanent", "no"]]},
 "flow": {
  "title": "Diagnosing an apparent trend",
  "alt": "Flow chart for deciding whether a trending series should be de-trended or differenced",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "A series that appears to trend", "kind": "start"},
   {"id": "b", "r": 1, "c": 1, "label": "Unit root present?", "kind": "dec"},
   {"id": "c", "r": 2, "c": 0, "label": "No → trend-stationary: de-trend", "kind": "end"},
   {"id": "d", "r": 2, "c": 2, "label": "Yes → difference-stationary: difference once", "kind": "end"},
   {"id": "e", "r": 3, "c": 0, "label": "Differencing here over-differences: MA with θ = 1", "kind": "note"},
   {"id": "f", "r": 3, "c": 2, "label": "De-trending here leaves the unit root", "kind": "note"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "b", "to": "c"}, {"from": "b", "to": "d"},
   {"from": "c", "to": "e"}, {"from": "d", "to": "f"}],
  "note": "One decision, and each wrong branch has its own characteristic damage. The Dickey–Fuller test of topic 7.5 is what settles the decision."},
 "ask": {
  "q": "Corr(yₜ, yₜ₊ₖ) = √(t/(t+k)) depends on t. Which of the three conditions for weak stationarity does that violate, and does the random walk satisfy the others?",
  "nudge": "Without drift the mean is 0 for every t. What about the variance?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — June 2026, Q23",
 "objective": "Derive both moments from the recursion.",
 "ask": {
  "q": "Both the mean and the variance grew with t. Which of the two would still grow if the drift μ were zero?",
  "nudge": "Where did μ enter, and where did σ² enter?"},
 "problem": "For the random walk yₜ = μ + yₜ₋₁ + εₜ, t = 1, 2, …, where {εₜ} is a purely random process with E(εₜ) = 0 and E(εₜ²) = σ²ₑ, find the mean and variance of yₜ.",
 "steps": [
  {"say": "Unroll the recursion.",
   "math": "y₁ = μ + y₀ + ε₁\ny₂ = μ + y₁ + ε₂ = 2μ + y₀ + ε₁ + ε₂\n⋮\nyₜ = tμ + y₀ + (ε₁ + ⋯ + εₜ)\ntaking y₀ = 0:  yₜ = tμ + Σ(i=1 to t) εᵢ",
   "why": "Each step adds one more μ and one more shock, and nothing is ever removed. That accumulation is the whole character of the process — the recursion has coefficient 1 on yₜ₋₁, so the past is carried forward undiminished."},
  {"say": "Take the expectation.",
   "math": "E(yₜ) = tμ + E(Σεᵢ) = tμ + 0 = tμ",
   "why": "The shocks have mean zero, so only the drift terms survive. The mean is therefore a straight line through the origin with slope μ — not a constant, so stationarity already fails when μ ≠ 0."},
  {"say": "Take the variance.",
   "math": "Var(yₜ) = Var(tμ + Σεᵢ) = Var(Σεᵢ)\n        = Σ Var(εᵢ)        [the shocks are independent]\n        = tσ²ₑ",
   "why": "The drift tμ is a constant at each t and contributes nothing to the variance. The shocks are uncorrelated, so there are no cross terms and the variances simply add — t of them, each σ²ₑ."},
  {"say": "Pick the option.",
   "math": "E(yₜ) = tμ,  Var(yₜ) = tσ²ₑ\n⟹ option D",
   "why": "Option A has both constant, which would be a stationary process; option B keeps the variance constant while the mean grows; option C does the reverse. Only D has both growing, and that pairing is the signature of a random walk."},
  {"say": "Check numerically.",
   "math": "200,000 paths with μ = 0.5 and σ = 2\nt = 5:  sim mean 2.4964 (exact 2.5),  sim var 19.99 (exact 20)\nt = 20: sim mean 9.9898 (exact 10),   sim var 79.89 (exact 80)\nt = 40: sim mean 19.956 (exact 20),   sim var 159.4 (exact 160)",
   "why": "Both moments track t exactly. Answering the question above: with μ = 0 the mean becomes 0 for every t, but the variance is still tσ² — so the process is non-stationary either way, and the no-drift case is a separate practice variant with answer (0, tσ²)."}],
 "after": "The transferable move is to unroll the recursion rather than to look for a formula. Once yₜ is written as a sum, the mean and the variance are each one line, and the reason both grow is visible: the coefficient on yₜ₋₁ is exactly 1, so nothing decays. Change that 1 to any φ with |φ| < 1 and the sum becomes geometric, the variance converges to σ²/(1 − φ²), and the process is stationary."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the moments before the variations.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "For a random walk with drift μ, give E(yₜ) and Var(yₜ).",
   "a": "tμ and tσ² — both grow with t."},
  {"q": "And without drift?",
   "a": "0 and tσ². The mean is constant but the variance still grows."},
  {"q": "What is Δyₜ for a random walk with drift?",
   "a": "μ + εₜ — white noise plus a constant, so stationary."},
  {"q": "Which ARIMA model is a random walk?",
   "a": "ARIMA(0, 1, 0)."},
  {"q": "What are the three requirements of weak stationarity?",
   "a": "Constant mean, constant variance, and autocovariance depending only on the lag."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — the correlation structure",
 "objective": "Derive the autocovariance and see why it fails stationarity.",
 "problem": "Work out the covariance structure of a driftless random walk yₜ = yₜ₋₁ + εₜ with y₀ = 0.",
 "steps": [
  {"say": "First the two moments.",
   "blank": {"prompt": "Give E(yₜ) and Var(yₜ) for the driftless case.",
             "answer": "0 and tσ²",
             "accept": ["0, t sigma^2", "0 and t*sigma^2", "zero and t sigma squared"],
             "hint": "Set μ = 0 in the general result."},
   "why": "The mean is 0 for every t, so the FIRST condition for stationarity holds. The variance tσ² still grows, so the second fails — and one failure is enough. Simulated at t = 20 with σ = 2: mean −0.0102 and variance 79.89 against 0 and 80."},
  {"say": "Now the covariance between two time points.",
   "blank": {"prompt": "Give Cov(yₜ, yₜ₊ₖ) for k ≥ 0, and say why.",
             "answer": "tσ² — the two sums share their first t shocks and the rest are independent",
             "accept": ["t sigma^2", "t*sigma^2", "tσ²"],
             "hint": "Write both as sums of shocks. Which shocks appear in both?"},
   "why": "yₜ is the sum of ε₁ … εₜ and yₜ₊ₖ is the sum of ε₁ … εₜ₊ₖ. The shared terms are the first t, contributing tσ², and every other pair is independent and contributes nothing. Note the covariance depends on t, the earlier time point, not on the lag k at all."},
  {"say": "Form the correlation.",
   "blank": {"prompt": "Give Corr(yₜ, yₜ₊ₖ).",
             "answer": "√(t/(t+k))",
             "accept": ["sqrt(t/(t+k))", "√(t/(t+k))", "root t over t+k"],
             "hint": "Divide the covariance by the product of the two standard deviations."},
   "why": "tσ²/√(tσ² · (t+k)σ²) = t/√(t(t+k)) = √(t/(t+k)). Simulated: at t = 10, k = 5 the sample correlation was 0.8164 against the exact 0.8165; at t = 20, k = 20 it was 0.7070 against 0.7071."},
  {"say": "Read off what this means for stationarity.",
   "blank": {"prompt": "Which stationarity condition does this correlation violate?",
             "answer": "the autocovariance must depend only on the lag, not on t",
             "accept": ["depends on t", "autocovariance depends on t not just the lag",
                        "the third condition"],
             "hint": "Compare Corr(y₁₀, y₁₅) with Corr(y₁₀₀, y₁₀₅): same lag, different values."},
   "why": "√(t/(t+k)) depends on both t and k, so the same lag gives different correlations at different points in the series — 0.8165 at t = 10 with k = 5, but 0.9759 at t = 100 with k = 5. Weak stationarity requires the autocovariance to be a function of the lag alone, which this is not."},
  {"say": "Finally, evaluate the decay at a fixed t.",
   "blank": {"prompt": "At t = 100, give the correlations at lags 1, 10 and 50.",
             "answer": "0.995, 0.953 and 0.816",
             "accept": ["0.995, 0.953, 0.816", "0.995 0.953 0.816"],
             "hint": "√(100/101), √(100/110), √(100/150)."},
   "why": "0.9950, 0.9535, 0.8165 — a very slow decay. Compare a stationary AR(1) with φ = 0.9, whose correlation at lag 50 is 0.9⁵⁰ ≈ 0.005. A sample ACF that stays high for many lags is the practical signature of non-stationarity, and it is the first thing to look at before any formal test."}],
 "after": "Two things to carry. The covariance of a random walk depends on WHERE you are, not just on how far apart the two points are — which is the clean statement of why it is non-stationary. And the resulting slow ACF decay is the diagnostic you will actually use on real data, because it is visible in a plot while the formal test needs computing."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "Stationarity: weak, strict, and the Gaussian case",
 "objective": "Separate the two definitions and know when they coincide.",
 "blocks": [
  {"t": "def", "h": "The two definitions",
   "body": "WEAK (second-order, covariance) stationarity: E(yₜ) is constant, Var(yₜ) is finite and constant, and Cov(yₜ, yₜ₊ₖ) depends only on k.\nSTRICT (strong) stationarity: the joint distribution of (yₜ₁, …, yₜₙ) is unchanged by shifting every time index by the same amount, for every n.\nStrict implies weak whenever the second moments exist. The converse fails in general, because matching means and covariances does not match whole distributions."},
  {"t": "step", "h": "Where they coincide",
   "body": "For a GAUSSIAN process the two are equivalent. A Gaussian process is completely determined by its mean function and its autocovariance function, so if those are shift-invariant then every joint distribution is too. That is the practice variant: for a Gaussian process, weak stationarity implies STRICT stationarity. For non-Gaussian processes it implies nothing further — a series could have constant mean and covariance while its skewness changed with t."},
  {"t": "step", "h": "A process can fail on just one condition",
   "body": "The driftless random walk has E(yₜ) = 0 for every t, so it passes the first condition and fails the other two. That is worth knowing because questions sometimes offer 'the mean is constant' as evidence of stationarity — it is necessary, not sufficient. Conversely yₜ = 5 + 0.2t + εₜ has constant variance σ² and a lag-only autocovariance, failing only on the mean, which is why de-trending repairs it completely."},
  {"t": "def", "h": "Ergodicity is a separate matter",
   "body": "Stationarity says the distribution does not shift with time; ergodicity says a single long realisation reveals that distribution, so time averages converge to the corresponding expectations. A process can be stationary without being ergodic — for instance one whose level is a single random draw fixed for all time, which is stationary but tells you only about that one draw however long you watch. Topic 7.9 covers this; it is why the practice variant's option 'ergodicity only' is wrong."},
  {"t": "step", "h": "The practical checklist",
   "body": "Given a series: does the level drift? does the spread change? does the sample ACF decay quickly or stay high for many lags? A slowly decaying ACF, a variance that grows with the window, and a path with no evident level are the three signs of a unit root, and the Dickey–Fuller test of topic 7.5 turns them into a decision."}],
 "ask": {
  "q": "A driftless random walk has a constant mean of 0. Why is that not enough for stationarity?",
  "nudge": "How many conditions are there, and how many must hold?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — classify four series",
 "objective": "Apply the trend-stationary versus difference-stationary distinction.",
 "problem": "Classify each series and give the correct repair. (a) yₜ = 5 + 0.2t + εₜ. (b) yₜ = 0.2 + yₜ₋₁ + εₜ. (c) yₜ = 0.5yₜ₋₁ + εₜ. (d) yₜ = εₜ. Then say what happens if (d) is differenced.",
 "hints": [
  "For each, ask whether the non-stationarity (if any) is in a deterministic trend or in an accumulation of shocks.",
  "For (c), check |φ| against 1.",
  "For the last part, write out εₜ − εₜ₋₁ and identify the model."],
 "answer": "(a) Trend-stationary; de-trend. (b) Difference-stationary random walk with drift; difference once. (c) Stationary AR(1); no repair. (d) Stationary white noise; no repair. Differencing (d) gives an MA(1) with θ = 1, which is non-invertible.",
 "check": "The pairs (a) and (b) are the ones to separate carefully: both have a mean rising at 0.2 per period, and over a short sample their plots can look alike. But (a) has constant variance σ² and returns to its line after a shock, while (b) has variance tσ² and never returns. The repairs are opposite, and each wrong choice has a signature: differencing (a) leaves an MA(1) with θ = 1, while de-trending (b) leaves the unit root untouched.",
 "scenario": {
  "teaser": "A forecaster differences every series as a matter of routine, and one model develops an odd residual pattern.",
  "title": "Over-differencing leaves a fingerprint",
  "body": [
   "A forecasting team adopts a rule: difference every series once before modelling, since so many economic series have unit roots. One series then produces a fitted model with a strong negative autocorrelation at lag 1 in what should be white-noise residuals, and an estimated MA coefficient very close to 1.",
   "That pattern is the fingerprint of over-differencing. The series was stationary to begin with, and differencing a stationary series manufactures structure that was not there. In the extreme case, if yₜ was white noise εₜ, then Δyₜ = εₜ − εₜ₋₁, which is an MA(1) with θ = 1 — variance 2σ² instead of σ², and a lag-1 autocorrelation of exactly −0.5.",
   "The simulation confirms both figures: Var(Δy) came to 2.0102 against the exact 2, and the lag-1 autocorrelation to −0.4998 against the exact −0.5. So differencing has doubled the variance and introduced a correlation, which is the opposite of what the operation was meant to achieve.",
   "The θ = 1 part matters beyond being untidy. The invertibility condition for an MA(1) is |θ| < 1, so θ = 1 sits exactly on the boundary and the model is non-invertible: it cannot be rewritten as a convergent autoregression, the likelihood surface is badly behaved at the boundary, and estimation routines often return a value pinned at or just below 1 with an unreliable standard error.",
   "So the diagnostic sequence runs the other way round from the team's rule. Test for a unit root first; difference only if one is found; and if a fitted MA coefficient comes out near 1 after differencing, suspect that the differencing was unnecessary rather than that the model needs another term.",
   "The general lesson is that both errors are detectable but their signatures differ. Under-differencing leaves a slowly decaying ACF and a near-unit AR root; over-differencing leaves a near-unit MA root. Neither is silent, which is what makes the diagnostic worth running."],
  "q": "What is the specific signature of over-differencing, and why is that particular value awkward?",
  "answer": "A moving-average coefficient estimated close to 1, together with a strong negative autocorrelation at lag 1 in the residuals — exactly −0.5 in the extreme case where the original series was white noise, with the variance doubled from σ² to 2σ². The value is awkward because the invertibility condition for an MA(1) is |θ| < 1, so θ = 1 lies precisely on the boundary: the process cannot be written as a convergent autoregression, the likelihood is ill-behaved there, and estimates pile up at the boundary with unreliable standard errors. It is also diagnostically useful, because under-differencing leaves the opposite fingerprint — a near-unit AR root and a slowly decaying ACF — so the two errors can be told apart."},
 "solution": [
  {"say": "(a) A deterministic trend.",
   "math": "yₜ = 5 + 0.2t + εₜ\nE(yₜ) = 5 + 0.2t  (not constant)\nVar(yₜ) = σ²      (constant)\nCov(yₜ, yₜ₊ₖ) = 0 for k ≥ 1  (lag-only)",
   "why": "Only the mean condition fails, and it fails because of a deterministic line. Subtracting the fitted line leaves stationary noise — this is trend-stationary, and the practice variant's answer."},
  {"say": "(b) A random walk with drift.",
   "math": "yₜ = 0.2 + yₜ₋₁ + εₜ\nE(yₜ) = 0.2t, Var(yₜ) = tσ²\nΔyₜ = 0.2 + εₜ  (stationary)",
   "why": "Difference-stationary: the non-stationarity is an accumulation, not a line, so it is removed by differencing and not by de-trending. Same apparent slope as (a), completely different process."},
  {"say": "(c) A stationary AR(1).",
   "math": "|φ| = 0.5 < 1\nE(yₜ) = 0, Var(yₜ) = σ²/(1 − 0.25) = 1.333σ²\nρₖ = 0.5ᵏ, decaying",
   "why": "Already stationary; no repair needed. Differencing it would over-difference."},
  {"say": "(d) White noise, and what differencing does to it.",
   "math": "yₜ = εₜ is stationary with ρₖ = 0 for k ≥ 1\nΔyₜ = εₜ − εₜ₋₁ : an MA(1) with θ = 1\nVar = 2σ² (sim 2.0102), ρ₁ = −0.5 (sim −0.4998)\n|θ| = 1 is NOT < 1 ⟹ non-invertible",
   "why": "Differencing a stationary series doubles the variance and manufactures a lag-1 correlation of −0.5, with an MA coefficient exactly on the invertibility boundary. That is the answer to the over-differencing variant."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims the variants on this topic are built from.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "For a driftless random walk, E(yₜ) = 0 and Var(yₜ) = tσ².",
   "tf": True,
   "why": "True. The shocks have mean zero so the mean stays at 0, but their variances accumulate, giving tσ². A constant mean with a growing variance is still non-stationary — one failure is enough. Simulated at t = 20 with σ = 2: mean −0.0102 and variance 79.89 against 0 and 80."},
  {"claim": "Weak stationarity requires the autocovariance to depend on both t and the lag.",
   "tf": False,
   "why": "False — it requires dependence on the LAG ONLY. The random walk's Corr(yₜ, yₜ₊ₖ) = √(t/(t+k)) depends on t as well, which is exactly why it is not weakly stationary."},
  {"claim": "For a Gaussian process, weak stationarity implies strict stationarity.",
   "tf": True,
   "why": "True. A Gaussian process is fully determined by its mean and autocovariance functions, so if those are shift-invariant then every joint distribution is too. For a non-Gaussian process weak stationarity implies nothing further."},
  {"claim": "In a random walk, the effect of a single shock dies out geometrically.",
   "tf": False,
   "why": "False — it is PERMANENT. The coefficient on yₜ₋₁ is 1, so a shock is carried forward undiminished at every subsequent step. Geometric decay at rate φᵏ is what happens in a STATIONARY AR(1) with |φ| < 1."},
  {"claim": "The series yₜ = 5 + 0.2t + εₜ should be differenced to make it stationary.",
   "tf": False,
   "why": "False. It is trend-stationary, so the correct repair is to subtract the deterministic trend. Differencing it would over-difference, producing an MA(1) with θ = 1 — non-invertible, with the variance doubled and a lag-1 autocorrelation of −0.5."},
  {"claim": "A random walk is an ARIMA(0, 1, 0) process.",
   "tf": True,
   "why": "True: no AR terms, one difference, no MA terms. Differencing once gives Δyₜ = εₜ, which is white noise, so the series is integrated of order 1 with nothing else in the model."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 8,
 "title": "On your own — six quick ones",
 "objective": "Apply the formulas at exam speed.",
 "problem": "For a random walk with drift μ and shock variance σ², unless stated otherwise: (a) E(y₁₀) and Var(y₁₀) with μ = 0.3, σ² = 4. (b) Corr(y₂₅, y₁₀₀). (c) The distribution of Δyₜ. (d) The ARIMA order. (e) The effect of a shock at time 5 on y₅₀. (f) The sample ACF at lags 1 and 20 for t = 100, and what it signals.",
 "hints": [
  "For (a), both moments are t times something.",
  "For (b), use √(t/(t+k)) with t = 25 and t + k = 100.",
  "For (e), what is the coefficient carrying yₜ₋₁ forward?"],
 "answer": "(a) 3 and 40. (b) 0.5. (c) μ + εₜ, stationary. (d) ARIMA(0, 1, 0). (e) Unchanged — the full shock is still present. (f) 0.995 and 0.913, signalling non-stationarity.",
 "check": "Part (b) is a clean case worth remembering: √(25/100) = 1/2 exactly, so a random walk observed at a quarter of the way along correlates 0.5 with its value at the end. Part (e) is the conceptual core — the shock's coefficient is 1⁴⁵ = 1, so forty-five periods later it is entirely intact. And in (f), note that a stationary AR(1) with φ = 0.9 would have ρ₂₀ = 0.9²⁰ = 0.12 against the random walk's 0.913, which is the practical contrast.",
 "solution": [
  {"say": "(a) The two moments.",
   "math": "E(y₁₀) = tμ = 10 × 0.3 = 3\nVar(y₁₀) = tσ² = 10 × 4 = 40",
   "why": "Both linear in t. Note σ² = 4 means σ = 2, so the standard deviation at t = 10 is √40 ≈ 6.32."},
  {"say": "(b) A correlation.",
   "math": "Corr(y₂₅, y₁₀₀) = √(t/(t+k)) with t = 25, t+k = 100\n= √(25/100) = 0.5",
   "why": "Exactly a half. Simulation of nearby cases matched to four decimals: t = 20, k = 20 gave 0.7070 against √(1/2) = 0.7071."},
  {"say": "(c) and (d) Differencing and the label.",
   "math": "Δyₜ = yₜ − yₜ₋₁ = μ + εₜ,  stationary\nno AR terms, one difference, no MA terms ⟹ ARIMA(0, 1, 0)",
   "why": "The difference is white noise shifted by the drift, so one differencing suffices and nothing else is needed in the model."},
  {"say": "(e) Shock persistence.",
   "math": "coefficient on yₜ₋₁ is 1\nimpact of ε₅ on y₅₀ = 1⁴⁵ = 1\n⟹ unchanged, the full shock is still there",
   "why": "Permanent, which is the defining feature. In a stationary AR(1) with φ = 0.9 the same shock would have impact 0.9⁴⁵ = 0.009, essentially gone."},
  {"say": "(f) The ACF at t = 100.",
   "math": "ρ₁ = √(100/101) = 0.9950\nρ₂₀ = √(100/120) = 0.9129\ncompare AR(1) φ = 0.9: ρ₂₀ = 0.9²⁰ = 0.1216",
   "why": "Still above 0.9 at lag 20. A sample ACF that stays high across many lags is the standard visual signal of a unit root, and it is what sends you to the Dickey–Fuller test."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "Where random walks appear",
 "objective": "Recognise the process across the syllabus and in applications.",
 "blocks": [
  {"t": "step", "h": "In unit-root testing (topic 7.5)",
   "body": "The Dickey–Fuller test has the random walk as its NULL hypothesis: it tests whether the coefficient on yₜ₋₁ equals 1 against the alternative that it is less. Topic 7.5 covers the test and why it needs its own critical values — the usual t-tables do not apply, because under the null the regressor is non-stationary."},
  {"t": "step", "h": "In regression with time-series data (module 6)",
   "body": "Regressing one random walk on another produces a spurious relationship whose apparent significance grows with the sample, as section 2's scenario described. The repairs are to difference both series or to test for cointegration. The Durbin–Watson statistic of topic 6.6 is the standard first warning, since a value near 0 indicates residuals that are themselves close to a random walk."},
  {"t": "step", "h": "In finance and the efficient-markets idea",
   "body": "The claim that asset prices follow a random walk is the statement that price CHANGES are unforecastable from past prices — the difference being white noise. The drift μ corresponds to an expected return. Whether the claim holds is an empirical question, and the tests used are exactly those of topic 7.5."},
  {"t": "step", "h": "As the simplest integrated process",
   "body": "A random walk is ARIMA(0, 1, 0), the base case of the ARIMA family that topic 7.5 develops. Adding AR or MA terms to the differenced series gives ARIMA(p, 1, q); differencing twice gives order 2, which is appropriate for a series whose CHANGES themselves wander — rarely needed, and over-differencing is the usual mistake."},
  {"t": "def", "h": "The common thread",
   "body": "Every one of these turns on a single coefficient being 1 rather than slightly below it. The random walk is not a complicated process; it is the boundary case, and nearly all of applied time-series practice is about deciding which side of that boundary a series is on."}],
 "ask": {
  "q": "The Dickey–Fuller test puts the random walk as the NULL rather than the alternative. What does that choice mean for a series on which the test fails to reject?",
  "nudge": "Failing to reject a null is not evidence for it. What else could explain a non-rejection?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the correlation structure and the classifications.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Give Corr(yₜ, yₜ₊ₖ) for a random walk.",
   "a": "√(t/(t+k)) — depending on t as well as k, which is why it is not stationary."},
  {"q": "At t = 100, what are the correlations at lags 1 and 50?",
   "a": "0.995 and 0.816 — a very slow decay."},
  {"q": "What does over-differencing produce?",
   "a": "A non-invertible MA component: differencing white noise gives an MA(1) with θ = 1."},
  {"q": "Classify yₜ = 5 + 0.2t + εₜ, and give its repair.",
   "a": "Trend-stationary; subtract the trend rather than differencing."},
  {"q": "For which kind of process do weak and strict stationarity coincide?",
   "a": "A Gaussian process, since its mean and autocovariance determine it completely."},
  {"q": "How long does a shock last in a random walk?",
   "a": "Forever — the coefficient carrying it forward is 1, so it never decays."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Unroll the random-walk recursion and derive E(yₜ) = tμ and Var(yₜ) = tσ².",
  "Give the driftless case as 0 and tσ², and say why a constant mean is not enough.",
  "Derive Cov(yₜ, yₜ₊ₖ) = tσ² and Corr = √(t/(t+k)), and name the stationarity condition it violates.",
  "State the three conditions for weak stationarity and when they imply strict stationarity.",
  "Separate trend-stationary from difference-stationary and give the correct repair for each.",
  "Say what over-differencing produces and why θ = 1 is awkward.",
  "Identify a random walk as ARIMA(0, 1, 0) and explain why its shocks are permanent."],
 })

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "Why the spurious regression happens, and what cointegration fixes",
 "objective": "See the mechanism behind section 2's scenario.",
 "blocks": [
  {"t": "step", "h": "The rejection rate goes to 1, not to 0.05",
   "body": "Regress one random walk on an independent other. The t-statistic for the slope does not converge to a fixed distribution as the sample grows; it diverges, growing like √n. So the proportion of samples in which the slope appears significant at any fixed level tends to 1. More data makes the illusion stronger, which is the opposite of the usual reassurance and the reason this is treated as a trap rather than a nuisance."},
  {"t": "step", "h": "What exactly breaks",
   "body": "The usual standard error assumes the regression errors are stationary with finite variance, so that the residual sum of squares divided by n converges. When both series are random walks the residuals are themselves non-stationary and their variance grows with t, so the quantity being divided by n does not settle. The coefficient estimate is not biased in any simple way; it is the YARDSTICK that is wrong, and wrong by a factor that grows."},
  {"t": "def", "h": "Cointegration: when a levels relationship is real",
   "body": "Two series each integrated of order 1 are COINTEGRATED if some linear combination of them is stationary. Then a relationship between the LEVELS genuinely exists — the two wander, but they wander together, and the gap between them reverts. Differencing both would discard exactly that information, which is why cointegration testing exists rather than a blanket rule to difference everything."},
  {"t": "step", "h": "The two repairs, and what each costs",
   "body": "Differencing both series and regressing the changes is always valid for inference, because the differences are stationary — but it answers a question about short-run changes rather than about levels, and it throws away any long-run relationship. Estimating a cointegrating relationship keeps the levels question but requires the cointegration to be present and tested for. Neither is a default; the choice depends on which question is being asked."},
  {"t": "step", "h": "A note on the random walk's variance and forecasting",
   "body": "Because Var(yₜ) = tσ², the variance of a k-step-ahead forecast error from a random walk is kσ² — it grows linearly in the horizon without bound, so forecast intervals widen like √k forever. For a stationary process they widen to a limit, namely the process variance. That contrast is the practical cost of a unit root: long-horizon forecasts from a random walk carry no useful precision, and the point forecast is simply the last observed value plus kμ."}],
 "ask": {
  "q": "A random walk's k-step forecast interval widens like √k without limit, while a stationary process's widens to a ceiling. What is that ceiling?",
  "nudge": "At long horizons a stationary process's best forecast is its mean. What is the uncertainty around that?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "timeseries_t6_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "timeseriest6",
 "topicId": "timeseries-t6",
 "moduleId": "timeseries",
 "title": "Random Walk With and Without Drift",
 "breadcrumb": "Time series → Non-stationarity → The random walk",
 "engine": "B",
 "engineName": "Time series — the process that accumulates every shock it receives",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Derive E(yₜ) = tμ and Var(yₜ) = tσ² by unrolling the recursion.",
  "Derive Cov(yₜ, yₜ₊ₖ) = tσ² and Corr = √(t/(t+k)), and name the condition violated.",
  "State the three conditions for weak stationarity and when they give strict stationarity.",
  "Separate trend-stationary from difference-stationary and choose the right repair.",
  "Say what over-differencing produces and why an MA coefficient of 1 is awkward.",
  "Identify a random walk as ARIMA(0, 1, 0) and explain the permanence of its shocks."],
 "prereq": [
  {"id": "p1", "name": "Expectation and variance of sums",
   "why": "Every moment here comes from the variance of a sum of independent shocks."},
  {"id": "p2", "name": "Stationarity (topic 7.1)",
   "why": "The random walk is defined by which stationarity conditions it fails, so the conditions come first."},
  {"id": "p3", "name": "The AR(1) process",
   "why": "The random walk is the AR(1) with φ = 1, and the contrast with |φ| < 1 is the lesson's spine."},
  {"id": "p4", "name": "Differencing and ARIMA notation (topic 7.5)",
   "why": "The repair is one differencing, and the label ARIMA(0,1,0) is asked directly."}],
 "traps": [
  "Both the mean and the variance grow: tμ and tσ². Options with one constant are the traps.",
  "Without drift the mean is constant at 0 but the variance is still tσ² — still non-stationary.",
  "Corr(yₜ, yₜ₊ₖ) = √(t/(t+k)) depends on t, not on the lag alone.",
  "A shock in a random walk is PERMANENT, not geometrically decaying — that is the stationary AR(1).",
  "yₜ = 5 + 0.2t + εₜ is trend-stationary: de-trend it, do not difference it.",
  "Over-differencing gives a NON-INVERTIBLE MA component with θ = 1, not a better model.",
  "Weak stationarity needs the autocovariance to depend on the lag ONLY.",
  "Weak implies strict only for a Gaussian process."],
 "revision": {
  "sheet": [
   "Random walk with drift: yₜ = μ + yₜ₋₁ + εₜ, y₀ = 0 ⟹ yₜ = tμ + Σεᵢ.",
   "June 2026 Q23: E(yₜ) = tμ and Var(yₜ) = tσ²ₑ — option D, both growing with t.",
   "Simulated with μ = 0.5, σ = 2 over 200,000 paths: at t = 20, mean 9.99 and variance 79.89 against 10 and 80.",
   "Driftless: E(yₜ) = 0 but Var(yₜ) = tσ² — constant mean, growing variance, still non-stationary.",
   "Cov(yₜ, yₜ₊ₖ) = tσ², because the two sums share their first t shocks.",
   "Corr(yₜ, yₜ₊ₖ) = √(t/(t+k)). At t = 100 the lags 1, 5, 10, 20, 50 give 0.995, 0.976, 0.953, 0.913, 0.816.",
   "Simulated: t = 10, k = 5 gave 0.8164 against 0.8165; t = 20, k = 20 gave 0.7070 against 0.7071.",
   "Corr(y₂₅, y₁₀₀) = √(25/100) = 0.5 exactly.",
   "Δyₜ = μ + εₜ, stationary ⟹ the random walk is integrated of order 1, i.e. ARIMA(0, 1, 0).",
   "A shock is PERMANENT: its coefficient k steps later is 1ᵏ = 1. In a stationary AR(1) it is φᵏ.",
   "Weak stationarity: constant mean, constant finite variance, autocovariance depending on the lag only.",
   "Strict stationarity: the whole joint distribution is shift-invariant. For a GAUSSIAN process the two coincide.",
   "Trend-stationary: yₜ = 5 + 0.2t + εₜ — de-trend. Difference-stationary: yₜ = 0.2 + yₜ₋₁ + εₜ — difference.",
   "Both have a mean rising at 0.2 per period; the first has variance σ² and reverts, the second tσ² and never does.",
   "Over-differencing: Δεₜ = εₜ − εₜ₋₁ is an MA(1) with θ = 1 — non-invertible, variance 2σ², ρ₁ = −0.5.",
   "Simulated: Var(Δy) = 2.0102 against 2, and ρ₁ = −0.4998 against −0.5.",
   "A stationary AR(1) has Var = σ²/(1−φ²): about 50σ² at φ = 0.99, infinite at φ = 1 — a knife edge.",
   "Forecast error variance is kσ² at horizon k, so intervals widen like √k without bound.",
   "Spurious regression: two independent random walks appear related, and the rejection rate tends to 1 as n grows."],
  "cards": [
   ["Random walk with drift, moments", "E = tμ, Var = tσ² — both grow"],
   ["Driftless random walk", "E = 0, Var = tσ² — still non-stationary"],
   ["Cov(yₜ, yₜ₊ₖ)", "tσ² — depends on t, not the lag"],
   ["Corr(yₜ, yₜ₊ₖ)", "√(t/(t+k))"],
   ["Effect of a shock", "Permanent — coefficient 1ᵏ = 1"],
   ["Δyₜ", "μ + εₜ, stationary"],
   ["ARIMA order", "(0, 1, 0)"],
   ["Weak stationarity", "Constant mean, constant variance, lag-only autocovariance"],
   ["Weak ⟹ strict", "Only for a Gaussian process"],
   ["yₜ = 5 + 0.2t + εₜ", "Trend-stationary — de-trend, do not difference"],
   ["Over-differencing", "MA(1) with θ = 1: non-invertible, ρ₁ = −0.5"],
   ["Forecast interval at horizon k", "Widens like √k, without limit"]],
  "tricks": [
   "Unroll the recursion rather than recalling a formula; the moments are then one line each.",
   "A coefficient of exactly 1 on yₜ₋₁ means nothing decays — that is the whole diagnosis.",
   "If both the mean and the variance grow linearly in t, it is a random walk with drift.",
   "To tell trend-stationary from difference-stationary, ask whether the variance is constant.",
   "A fitted MA coefficient near 1 after differencing suggests the differencing was unnecessary.",
   "A sample ACF still high at lag 20 signals a unit root; a stationary AR(1) at φ = 0.9 would be at 0.12."],
  "shortcuts": [
   "√(t/(t+k)) at t = 25, k = 75 is exactly 0.5 — a clean case worth remembering.",
   "At t = 100 the random-walk ACF reads 0.995, 0.953, 0.913 at lags 1, 10, 20.",
   "σ²/(1−φ²) is about 50σ² at φ = 0.99 and 5.3σ² at φ = 0.9."],
  "remember": [
   "Both moments grow: tμ and tσ².",
   "Shocks are permanent, not decaying.",
   "Trend-stationary de-trends; difference-stationary differences."]},
 "howto": "Section 5 is June 2026's question and the quickest way in: unroll the recursion, see that yₜ is tμ plus a sum of t shocks, and both moments follow in a line each. Section 3's chart is worth a minute — set φ₂ to 0 and push φ₁ from 0.95 to 1.00, and the chart stops drawing an ACF and tells you why, because a non-stationary process has no finite variance to divide by. Section 7 derives the correlation √(t/(t+k)), which is the cleanest statement of why the process is not stationary: the correlation depends on WHERE you are, not just on how far apart two points are. Section 9's part (a) versus (b) is the distinction most worth getting right, since two series with the same apparent slope need opposite repairs. If short of time, sections 3, 5 and 7 are the lesson. This lesson deliberately does not repeat topic 7.5's material on unit-root testing or ARIMA orders; it cross-references them. The optional section explains the spurious-regression mechanism and what cointegration is for.",
 "refs": [
  {"title": "Time Series Analysis and Its Applications", "where": "Chapters 1 and 3",
   "site": "Shumway and Stoffer", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The random walk with drift worked in full, with its moments, its ACF and the trend-stationary contrast."},
  {"title": "Time Series Analysis: Forecasting and Control", "where": "Chapters 4 and 5",
   "site": "Box, Jenkins and Reinsel", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The ARIMA framework in which a random walk is (0,1,0), and the over-differencing diagnostic."},
  {"title": "Forecasting: Principles and Practice, 3rd edition", "where": "Chapters 8 and 9",
   "site": "Hyndman and Athanasopoulos", "url": "https://otexts.com/fpp3/",
   "type": "Free online textbook", "free": True, "checked": "2026-11-03",
   "why": "Stationarity, differencing and random walks with the diagnostics worked on real series; freely available."},
  {"title": "Time Series Analysis", "where": "Weeks on stationarity and non-stationary processes",
   "site": "NPTEL / SWAYAM", "url": "https://archive.nptel.ac.in/courses/111104049",
   "type": "Video course", "free": True, "checked": "2026-11-03",
   "why": "Indian-syllabus notation, including the 'purely random process' phrasing this question uses."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026, the third lesson of the time-series module. PYQ anchor: June 2026 Q23, which was answered CORRECTLY (marked D) — the mean and variance of a random walk with drift are tμ and tσ²ₑ. The lesson was built anyway because the question's nine variants extend well beyond it, into weak versus strict stationarity, the trend-stationary distinction, over-differencing and the ARIMA(0,1,0) label, and because the random walk is the canonical non-stationary process the rest of the module is defined against. Every figure was computed and cross-checked against a 200,000-path simulation with μ = 0.5 and σ = 2: the means at t = 1, 5, 20, 40 came to 0.495, 2.496, 9.990, 19.956 against the exact 0.5, 2.5, 10, 20, and the variances to 3.99, 19.99, 79.89, 159.36 against 4, 20, 80, 160; the driftless case gave mean −0.0102 and variance 79.89 at t = 20; and the correlation √(t/(t+k)) was confirmed at (t,k) = (10,5), (20,20), (5,45) and (30,30) as 0.8164, 0.7070, 0.3141 and 0.7075 against 0.8165, 0.7071, 0.3162 and 0.7071. The over-differencing result was verified separately: differencing white noise gives variance 2.0102 against the exact 2 and lag-1 autocorrelation −0.4998 against −0.5, with θ = 1 exactly on the invertibility boundary. Scope was set deliberately against the two time-series lessons already built: topic 7.5 owns unit-root testing, the Dickey–Fuller test and general ARIMA orders, and 7.3 owns Yule–Walker, so both are cross-referenced rather than repeated. Uses the existing `ar-acf` visualisation rather than a new one, since a random walk is the AR(1) case φ = 1 and the chart correctly refuses to draw an ACF there while naming the failed stationarity condition — which is the right picture for this topic. Previous-year questions are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "ts-t6-m-%02d" % i, "format": fmt, "topic": "timeseries-t6",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "For the random walk yₜ = μ + yₜ₋₁ + εₜ with E(εₜ) = 0 and E(εₜ²) = σ²ₑ, the mean and variance of yₜ are:",
 ["tμ and tσ²ₑ", "μ and σ²ₑ", "tμ and σ²ₑ", "μ and tσ²ₑ"],
 "A",
 "Unrolling gives yₜ = tμ + Σεᵢ, so the mean is tμ and, since the shocks are independent, the variance is tσ²ₑ. Both grow with t, which is the signature of a random walk. This is June 2026 Q23; the options with one moment held constant are the traps."))

I.append(q(2, "single", "easy",
 "For the random walk yₜ = yₜ₋₁ + εₜ with no drift, E(yₜ) and Var(yₜ) are:",
 ["0 and tσ²", "tμ and tσ²", "μ and σ²", "0 and σ²"],
 "A",
 "The shocks have mean zero so the mean stays at 0, but their variances still accumulate to tσ². A constant mean with a growing variance is still non-stationary — only one of the three conditions has to fail. Simulated at t = 20 with σ = 2: mean −0.0102 and variance 79.89 against 0 and 80."))

I.append(q(3, "single", "easy",
 "Weak stationarity requires the autocovariance to depend on:",
 ["the lag only", "both t and the lag", "t only", "neither"],
 "A",
 "Together with a constant mean and a constant finite variance, that is the definition. The random walk's Corr(yₜ, yₜ₊ₖ) = √(t/(t+k)) depends on t as well as the lag, which is precisely why it fails."))

I.append(q(4, "single", "easy",
 "A random walk becomes stationary after:",
 ["differencing once", "taking logarithms", "squaring", "differencing twice"],
 "A",
 "Δyₜ = yₜ − yₜ₋₁ = μ + εₜ, which is white noise plus a constant and therefore stationary. Differencing twice would over-difference, introducing a non-invertible moving-average component."))

I.append(q(5, "single", "easy",
 "In a random walk, the effect of a single shock on future values is:",
 ["permanent", "alternating", "zero", "it dies out geometrically"],
 "A",
 "The coefficient on yₜ₋₁ is exactly 1, so a shock is carried forward undiminished: its impact k periods later is 1ᵏ = 1. Geometric decay at rate φᵏ is what happens in a STATIONARY AR(1) with |φ| < 1, which is the contrast worth holding."))

I.append(q(6, "single", "easy",
 "ARIMA(0, 1, 0) describes:",
 ["a random walk", "an MA(1)", "white noise", "an AR(1)"],
 "A",
 "No AR terms, one difference, no MA terms. Differencing once leaves Δyₜ = εₜ, which is white noise, so the series is integrated of order 1 with nothing else in the model."))

# --- moderate (10)
I.append(q(7, "single", "moderate",
 "For a random walk, Corr(yₜ, yₜ₊ₖ) equals:",
 ["√(t/(t+k))", "φᵏ", "0", "1"],
 "A",
 "Cov(yₜ, yₜ₊ₖ) = tσ², since the two sums share their first t shocks, and dividing by √(tσ² · (t+k)σ²) gives √(t/(t+k)). Option B is the stationary AR(1)'s autocorrelation. Simulated: t = 10, k = 5 gave 0.8164 against 0.8165; t = 20, k = 20 gave 0.7070 against 0.7071."))

I.append(q(8, "numeric", "moderate",
 "For a driftless random walk, Corr(y₂₅, y₁₀₀) equals:",
 ["0.50", "0.25", "0.75", "0.87"],
 "A",
 "√(t/(t+k)) with t = 25 and t + k = 100 gives √(25/100) = √0.25 = 0.5 exactly. Option B is the ratio t/(t+k) without the square root, which is the standard slip.",
 check="The correlation must exceed the variance ratio 0.25, since taking a square root of a number below 1 increases it."))

I.append(q(9, "single", "moderate",
 "The series yₜ = 5 + 0.2t + εₜ is:",
 ["trend-stationary", "stationary", "difference-stationary", "a random walk"],
 "A",
 "Its mean 5 + 0.2t is not constant, so it is not stationary; but its variance is σ² throughout and its autocovariance depends only on the lag, so subtracting the deterministic line leaves a stationary series. The correct repair is to de-trend, not to difference — differencing would over-difference."))

I.append(q(10, "single", "moderate",
 "Over-differencing a stationary series produces:",
 ["a non-invertible MA component", "a unit root in the AR part",
  "a better model", "white noise"],
 "A",
 "Differencing white noise gives Δyₜ = εₜ − εₜ₋₁, an MA(1) with θ = 1 — exactly on the invertibility boundary |θ| < 1. The variance doubles to 2σ² and a lag-1 autocorrelation of −0.5 appears. Simulated: variance 2.0102 against 2, and ρ₁ = −0.4998 against −0.5."))

I.append(q(11, "single", "moderate",
 "For a Gaussian process, weak stationarity implies:",
 ["strict stationarity", "ergodicity only", "independence", "nothing further"],
 "A",
 "A Gaussian process is completely determined by its mean function and its autocovariance function, so if both are shift-invariant then every joint distribution is too. For a non-Gaussian process weak stationarity implies nothing further — the skewness, for instance, could still change with t."))

I.append(q(12, "multi", "moderate",
 "Consider the driftless random walk yₜ = yₜ₋₁ + εₜ.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true — the mean condition holds. B is true, and it is the reason stationarity fails. C is true: the covariance depends on t. D is false — one differencing suffices, since Δyₜ = εₜ is already white noise.",
 statements=["E(yₜ) = 0 for every t.",
             "Var(yₜ) = tσ², so the variance is not constant.",
             "Cov(yₜ, yₜ₊ₖ) = tσ², which depends on t and not only on the lag.",
             "Two differencings are needed to make it stationary."],
 verdicts=verd(
  (True, "True. The shocks have mean zero, so the first condition for weak stationarity actually holds — which is why a constant mean alone proves nothing."),
  (True, "True. Variances of independent shocks accumulate, giving tσ², and that failure alone destroys stationarity."),
  (True, "True. The two sums share their first t shocks, so the covariance is tσ² — a function of the earlier time point rather than of the separation."),
  (False, "False. One differencing gives Δyₜ = εₜ, which is white noise. A second differencing would over-difference and introduce a non-invertible MA component."))))

I.append(q(13, "numeric", "moderate",
 "For a random walk with μ = 0.3 and σ² = 4, the mean and variance of y₁₀ are:",
 ["3 and 40", "0.3 and 4", "3 and 4", "30 and 40"],
 "A",
 "E(y₁₀) = tμ = 10 × 0.3 = 3 and Var(y₁₀) = tσ² = 10 × 4 = 40. Both are t times the one-step quantity, so the standard deviation at t = 10 is √40 ≈ 6.32.",
 check="Both moments must be exactly ten times their one-step values, which rules out any option holding one of them fixed."))

I.append(q(14, "numeric", "moderate",
 "For a driftless random walk at t = 100, the autocorrelations at lags 1 and 20 are approximately:",
 ["0.995 and 0.913", "0.900 and 0.122", "0.995 and 0.500", "1.000 and 1.000"],
 "A",
 "√(100/101) = 0.9950 and √(100/120) = 0.9129. Option B is a stationary AR(1) with φ = 0.9, whose lag-20 autocorrelation is 0.9²⁰ = 0.122 — the contrast that makes a slowly decaying sample ACF the practical signal of a unit root.",
 check="At lag 50 the value would be √(100/150) = 0.816, still high — the decay is extremely slow by design."))

I.append(q(15, "single", "moderate",
 "Which pair of series has the same mean path but requires opposite repairs?",
 ["yₜ = 5 + 0.2t + εₜ and yₜ = 0.2 + yₜ₋₁ + εₜ",
  "yₜ = εₜ and yₜ = 0.5yₜ₋₁ + εₜ",
  "yₜ = yₜ₋₁ + εₜ and yₜ = 2yₜ₋₁ + εₜ",
  "yₜ = 5 + εₜ and yₜ = 5 + 0.2t + εₜ"],
 "A",
 "Both have a mean rising at 0.2 per period, but the first is trend-stationary with constant variance σ² and reverts to its line, while the second is a random walk with drift, variance tσ², which never reverts. De-trend the first and difference the second; each wrong choice leaves its own characteristic damage."))

I.append(q(16, "numeric", "moderate",
 "A stationary AR(1) with φ = 0.99 has variance σ²/(1 − φ²). How does it compare with a random walk's?",
 ["about 50σ², finite, against the random walk's unbounded tσ²",
  "about 100σ², finite, against the random walk's σ²",
  "identical — both are unbounded",
  "smaller than the random walk's at every t"],
 "A",
 "1/(1 − 0.99²) = 1/0.0199 = 50.25, so the variance is about 50σ² — large but finite, and the process does eventually revert. At φ = 1 the formula breaks down and the variance is tσ², growing without bound. The qualitative change happens at a single point.",
 check="A random walk's variance exceeds 50σ² once t > 50, so option D fails for large t and holds only early on."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider regressing one random walk on an independent other.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true — the rejection rate tends to 1. B is true: the residuals are non-stationary so the standard error is the thing that fails. C is true, and it is what cointegration tests for. D is false — differencing both is valid for inference but answers a question about changes, discarding any long-run relationship.",
 statements=["The proportion of samples in which the slope appears significant tends to 1 as n grows.",
             "What fails is the standard error, because the regression residuals are themselves non-stationary.",
             "If some linear combination of the two series is stationary, a levels relationship is real.",
             "Differencing both series is always the best repair."],
 verdicts=verd(
  (True, "True. The t-statistic diverges like √n rather than converging to a fixed distribution, so more data makes the spurious relationship look stronger, not weaker."),
  (True, "True. The usual formula assumes stationary errors of finite variance; with non-stationary residuals the quantity divided by n never settles, so the yardstick is wrong by a factor that grows."),
  (True, "True — that is the definition of cointegration. The two series wander, but they wander together and the gap between them reverts, so a relationship between levels genuinely exists."),
  (False, "False. Differencing is always valid for inference, but it answers a question about short-run changes and discards any long-run levels relationship. Where cointegration is present, that relationship is exactly what is of interest."))))

I.append(q(18, "numeric", "hard",
 "Differencing a white-noise series yₜ = εₜ gives a series whose variance and lag-1 autocorrelation are:",
 ["2σ² and −0.5", "σ² and 0", "2σ² and +0.5", "σ²/2 and −0.5"],
 "A",
 "Δyₜ = εₜ − εₜ₋₁ has variance σ² + σ² = 2σ², and Cov(Δyₜ, Δyₜ₋₁) = −σ², giving an autocorrelation of −σ²/2σ² = −0.5. So differencing has doubled the variance and manufactured a correlation. Simulated: 2.0102 and −0.4998.",
 check="This is an MA(1) with θ = 1, whose theoretical ρ₁ is −θ/(1+θ²) = −1/2 ✓ — and θ = 1 is exactly on the invertibility boundary."))

I.append(q(19, "single", "hard",
 "The variance of a k-step-ahead forecast error from a random walk is:",
 ["kσ², growing without bound", "σ², constant",
  "σ²/(1 − φ²), the process variance", "zero for k = 1"],
 "A",
 "The k-step error is the sum of the next k shocks, so its variance is kσ² and the interval widens like √k forever. For a stationary process the forecast error variance rises to a ceiling, namely the process variance σ²/(1 − φ²). That contrast is the practical cost of a unit root: long-horizon forecasts from a random walk carry no useful precision."))

I.append(q(20, "single", "hard",
 "A forecaster differences every series by default. One model then shows residual lag-1 autocorrelation near −0.5 and an estimated MA coefficient near 1. The best reading is:",
 ["the series was already stationary and has been over-differenced",
  "a second differencing is needed", "the model needs an extra AR term",
  "the shocks are not white noise"],
 "A",
 "Those two figures are the fingerprint of over-differencing: differencing a stationary series doubles its variance and produces an MA(1) with θ = 1 and ρ₁ = −0.5. The remedy is to undo the differencing, not to add terms. Note the contrast with under-differencing, which leaves a slowly decaying ACF and a near-unit AR root — so the two errors are distinguishable."))

# Spread the answer keys; the validator caps any letter at 40% of the pool.
LET = "ABCD"
WANT = {"ts-t6-m-01": "D", "ts-t6-m-02": "B", "ts-t6-m-03": "C",
        "ts-t6-m-04": "D", "ts-t6-m-05": "B", "ts-t6-m-06": "C",
        "ts-t6-m-07": "D", "ts-t6-m-08": "B", "ts-t6-m-09": "C",
        "ts-t6-m-10": "D", "ts-t6-m-11": "B", "ts-t6-m-13": "C",
        "ts-t6-m-14": "D", "ts-t6-m-15": "B", "ts-t6-m-16": "C",
        "ts-t6-m-18": "D", "ts-t6-m-19": "B", "ts-t6-m-20": "C"}


def swapletters(t, a, b):
    """Swap option letters a and b wherever the text cites options, plural lists included."""
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
 "moduleId": "timeseries", "topicId": "timeseries-t6", "source": "mastery",
 "label": "Random walk with and without drift — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
