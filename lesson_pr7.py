#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 1.7 — Jensen, Markov, Chebyshev and Cauchy-Schwarz (probability-t7).

PYQ ANCHOR: June 2026 Q31, which was answered CORRECTLY (key C, the user also marked C). The
priority document listed this lesson among anchors "answered wrongly with a sizeable variant
bank"; that is wrong for Q31 and the doc is being corrected alongside this lesson. The topic is
built anyway, because its ten-variant bank (j26v-q30-10 .. -19, retagged to srcQ 31) covers four
distinct inequalities plus the tail-integral identities, and the bank IS the specification.

Q31's four statements, with the key excluding C:
  A. integral 2x[1-F(x)]dx = E(X^2)      TRUE
  B. integral [1-F(x)]dx  = E(X)         TRUE
  C. E(1/X) <= 1/E(X)                    FALSE -- Jensen gives >=, which is why C is excluded
  D. E(log X) <= log E(X)                TRUE
So the key "A, B and D" turns on knowing the DIRECTION of Jensen for a convex versus concave
function. That direction is this lesson's spine.

Verified:
  Unif(1,3): E(1/X) = ln(3)/2 = 0.549306 vs 1/E(X) = 0.5 -- Jensen's >= confirmed.
             E(log X) = (3ln3-2)/2 = 0.647918 vs log(2) = 0.693147 -- concave, so <=.
  Gamma(3,1): E(1/X) = 1/(k-1) = 0.5 vs 1/E(X) = 1/3 = 0.333333.
  Exp(1): E(1/X) DIVERGES. Jensen still holds, but the left side is infinite -- a caveat the
          lesson states, because it is the natural example to reach for and it misbehaves.
  MARKOV on Exp(1): true tail e^-a = 0.13534, 0.04979, 0.00674 at a = 2, 3, 5 against bounds
          1/a = 0.5, 0.3333, 0.2. Very slack. Tight exactly for X = a w.p. p, else 0.
  CHEBYSHEV: bound 1/k^2. Normal truth 0.317311, 0.133614, 0.045500, 0.002700 at k = 1, 1.5, 2, 3
          -- ratios to the bound 0.317, 0.301, 0.182, 0.024. Laplace at k=2 gives 0.059106
          (ratio 0.236), the closest of the smooth cases. Uniform's tail hits exactly 0 at
          k = sqrt(3) = 1.732 while the bound is still 1/3.
          TIGHT: 3 points at -k, 0, +k with p = 1/(2k^2) at each end. Variance checks to 1.000000
          and P(|X| >= k) = 2p = 1/k^2 exactly, at k = 2 and k = 3.
  TAIL IDENTITIES: integral P(X>x)dx = 1.000000, 0.500000, 1.500000 for Exp(1), Exp(2), Unif(0,3)
          against E(X) = 1, 0.5, 1.5; integral 2x P(X>x) dx = 2.000000, 0.500000, 3.000000
          against E(X^2) = 2, 0.5, 3. Exact to six decimals by quadrature.
  DISCRETE: sum_{k>=1} P(X >= k) = 3.333333 and 2.000000 for Geom(0.3) and Geom(0.5), matching 1/p.
  CAUCHY-SCHWARZ: |E(XY)| <= sqrt(E X^2 E Y^2) checked at rho = 0, 0.5, -0.8, 0.95; equality
          attained exactly when Y = 3X (2.9961 both sides).

Uses the new `ineq-bounds` visualisation (Chebyshev's bound against the true tail, across k, for
five distributions including the 3-point one that attains it).

Writes seed/lesson_pr7.json and seed/probability_t7_mastery.json.
"""
import json, io, os, re

OUT = "seed/lesson_pr7.json"
POOL = "seed/probability_t7_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 7,
 "title": "Before the lesson — four things it will assume",
 "objective": "Fix convexity and what an inequality is for.",
 "ask": {
  "q": "Is E(1/X) bigger or smaller than 1/E(X) for a positive random variable? Commit to a direction before reading on.",
  "nudge": "Try X taking the values 1 and 3 with probability ½ each, and compute both sides."},
 "body": [
  "This topic is four inequalities and two identities. They do different jobs: Jensen relates the expectation of a function to the function of the expectation; Markov and Chebyshev bound tail probabilities using only a mean or a variance; Cauchy–Schwarz bounds a covariance; and the tail identities express a moment as an integral of the survival function.",
  "What ties them together is that each buys a conclusion with very few assumptions. Chebyshev needs only a finite variance and holds for EVERY such distribution — which is exactly why it is loose, as it must accommodate the worst case. Knowing how loose is part of using it well.",
  "The June 2026 paper tested the direction of Jensen inside a four-statement question, and the statement that made it hard was E(1/X) ≤ 1/E(X), which is false. If you committed to a direction above, section 1 will say whether you were right.",
  "Four checks before starting."],
 "items": [
  {"ask": "What makes a function convex, and what makes it concave?",
   "recall": "Convex: the chord lies above the curve, g''(x) ≥ 0. Concave: the chord lies below, g''(x) ≤ 0.",
   "refresh": [
    "x², eˣ, 1/x on x > 0 and |x| are convex. log x and √x are concave. A linear function is both, which is the equality case throughout this lesson.",
    "The quickest test is the second derivative. For 1/x on the positive half-line, the second derivative is 2/x³ > 0 — convex, which is the fact the exam question turns on.",
    "A concave function is just the negative of a convex one, so every statement about one gives a statement about the other with the inequality reversed. That is the whole reason Jensen has two directions."]},
  {"ask": "Define the survival function and relate it to F.",
   "recall": "S(x) = P(X > x) = 1 − F(x).",
   "refresh": [
    "It answers 'how much probability is still above x'. The tail identities in section 3 integrate it to recover moments, which is often easier than integrating xf(x) when f is awkward but F is simple.",
    "For a non-negative X, the area under S is E(X) exactly. Verified by quadrature: the integral is 1.000000 for Exp(1), 0.500000 for Exp(2) and 1.500000 for Uniform(0,3), matching the means 1, 0.5 and 1.5.",
    "The discrete analogue replaces the integral by a sum: E(X) = Σ(k≥1) P(X ≥ k) for a non-negative integer variable."]},
  {"ask": "State Markov's and Chebyshev's inequalities.",
   "recall": "For X ≥ 0 and a > 0, P(X ≥ a) ≤ E(X)/a. For any X with finite variance, P(|X − μ| ≥ kσ) ≤ 1/k².",
   "refresh": [
    "Markov needs non-negativity and a mean; Chebyshev needs a variance. Chebyshev is Markov applied to (X − μ)², which is how it is proved and why the bound is 1/k² rather than 1/k.",
    "Both are distribution-free, so both must hold for the worst case. At k = 2 Chebyshev allows a quarter of the probability beyond two standard deviations; a normal puts only 0.0455 there.",
    "Non-negativity is not optional for Markov. Applied to a variable that can go negative the statement is simply false."]},
  {"ask": "Give the Cauchy–Schwarz inequality for random variables.",
   "recall": "|E(XY)| ≤ √(E(X²)E(Y²)), with equality exactly when one is a constant multiple of the other.",
   "refresh": [
    "Applied to the centred variables X − μ_X and Y − μ_Y it gives Cov(X,Y)² ≤ Var(X)Var(Y), which rearranges to |ρ| ≤ 1 — so the familiar bound on a correlation coefficient IS Cauchy–Schwarz.",
    "Checked numerically at correlations 0, 0.5, −0.8 and 0.95, and the equality case confirmed with Y = 3X, where both sides come to 2.9961.",
    "The equality condition is the useful part: |ρ| = 1 exactly when the two variables are linearly related, which is what topic 1.13 means by a perfect correlation."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Which way does Jensen point?",
 "objective": "Settle the direction once, with a case you can check by hand.",
 "body": [
  "Take X equal to 1 or 3 with probability a half each. Then E(X) = 2, so 1/E(X) = 0.5. And E(1/X) = ½(1) + ½(1/3) = 2/3 ≈ 0.667. So E(1/X) is LARGER. If you committed to the other direction, that is the error the exam question was built to catch.",
  "The reason is that 1/x is CONVEX on the positive half-line — its second derivative 2/x³ is positive. Jensen's inequality says that for a convex g, averaging first and then applying g gives a SMALLER answer than applying g first and then averaging: g(E(X)) ≤ E(g(X)). The convex function's curvature means the two outer points get pulled up more than the middle point does.",
  "For a concave function everything reverses. log x is concave, so E(log X) ≤ log E(X) — averaging first gives the larger answer. Verified on Uniform(1,3): E(log X) = (3 ln 3 − 2)/2 = 0.647918 against log E(X) = log 2 = 0.693147. And on the same distribution E(1/X) = ln 3 / 2 = 0.549306 against 1/E(X) = 0.5, confirming the convex direction too.",
  "So the June 2026 question's statement C, E(1/X) ≤ 1/E(X), is false, and that is precisely why the key excludes it. Its other three statements are all true, giving 'A, B and D'.",
  "One caveat worth having, because the obvious example for this fails. For X ~ Exponential(1), E(1/X) does not merely exceed 1/E(X) = 1 — it DIVERGES, because the density stays positive at 0 and ∫(1/x)e^(−x)dx has no finite value. Jensen's inequality is still true, with an infinite left-hand side, but a numerical check on an exponential will produce nonsense that grows with the sample size. Use a distribution bounded away from zero, such as Uniform(1,3), or a Gamma with shape above 1, where Gamma(3,1) gives E(1/X) = 1/(k−1) = 0.5 against 1/E(X) = 1/3."],
 "scenario": {
  "teaser": "A simulation of E(1/X) for an exponential gives a different answer every time it is run.",
  "title": "When the quantity being estimated does not exist",
  "body": [
   "An analyst wants to check Jensen's inequality numerically. They draw a million Exponential(1) values, average their reciprocals, and get about 15. Suspicious of the figure, they rerun with ten million draws and get about 40. A third run gives something else again. The code is correct.",
   "The quantity does not exist. For an Exponential(1) the density at zero is 1, so values arbitrarily close to zero occur with appreciable probability and their reciprocals are arbitrarily large. The integral ∫₀^∞ (1/x)e^(−x)dx diverges at the origin, so E(1/X) is infinite and no sample average converges to anything. The estimate grows with the sample size because larger samples eventually include smaller minima.",
   "Jensen's inequality is not violated. It says E(1/X) ≥ 1/E(X) = 1, and an infinite left-hand side satisfies that comfortably. What has gone wrong is the attempt to VERIFY a statement about an expectation that is not finite, which a simulation cannot do.",
   "The diagnostic is general and worth internalising: a sample mean that drifts upward as n grows, rather than settling, is the signature of an infinite or very heavy-tailed expectation. The Cauchy distribution's sample mean does the same thing for the same reason. The fix is never more data.",
   "For checking Jensen specifically, choose a distribution whose support is bounded away from the point where the function misbehaves. Uniform(1,3) keeps X at least 1, so 1/X is at most 1 and everything is finite: E(1/X) = ln 3 / 2 = 0.549306 against 1/E(X) = 0.5, a clean confirmation. A Gamma with shape parameter above 1 also works, since its density vanishes at the origin.",
   "The broader point is that an inequality can be perfectly true while being untestable by the obvious experiment. Before simulating a relation between moments, check that the moments are finite."],
  "q": "A sample average keeps growing as n increases instead of settling. What does that indicate?",
  "answer": "That the expectation being estimated is infinite or the distribution's tail is heavy enough that the mean does not exist in a usable sense. A sample mean converges only when the population mean is finite; when it is not, the average is driven by progressively more extreme observations that larger samples are progressively more likely to contain, so the estimate drifts rather than stabilising. For E(1/X) under an Exponential(1), the density at zero is positive, so ∫(1/x)e^(−x)dx diverges at the origin and no amount of simulation converges — runs of one million and ten million draws gave roughly 15 and 40. The remedy is never more data: it is to recognise the quantity does not exist, and if the goal was to check an inequality, to choose a distribution where the relevant moments are finite, such as a Uniform bounded away from zero."},
 "ask": {
  "q": "Var(X) ≥ 0 is itself an instance of Jensen. Which function g makes it so?",
  "nudge": "Var(X) = E(X²) − (E(X))². What inequality between E(g(X)) and g(E(X)) is that?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "How much slack does Chebyshev carry?",
 "objective": "See the bound against the truth, and find the case that attains it.",
 "viz": {"type": "ineq-bounds", "dist": 0, "k": 2,
         "caption": "The accent curve is Chebyshev's bound 1/k²; the teal curve is the true tail probability of the selected distribution, every one standardised to mean 0 and variance 1."},
 "body": [
  "Start with the Normal at k = 2. The bound is 0.25 and the truth is 0.045500 — the bound overstates the tail by a factor of 5.5. Move to k = 3 and the gap widens sharply: 0.111111 against 0.002700, a factor of 41. For a normal, Chebyshev is very nearly useless as a numerical statement.",
  "Switch to the Laplace. At k = 2 the truth is 0.059106, a ratio of 0.236 — closer to the bound than the normal, because its tails are heavier. That is the general pattern: the heavier the tail, the less slack.",
  "Switch to the Uniform and set k to 1.7. The truth is 0.018505 while the bound is 0.346. Push k past √3 ≈ 1.732 and the true tail becomes exactly ZERO, because a standardised uniform cannot reach beyond that, while the bound is still a third. A bounded distribution is where the inequality is most wasteful.",
  "Now select the 3-point option. The two curves coincide exactly, at every k. This is the distribution Chebyshev's proof cannot improve on: put probability 1/(2k²) at each of −k and +k and the rest at 0. Its variance is exactly 1, and P(|X| ≥ k) = 2 × 1/(2k²) = 1/k² — the bound attained with equality. At k = 2 that is mass 0.125 at each of ±2 and 0.75 at zero.",
  "That last case is the answer to why the inequality is loose. It is DISTRIBUTION-FREE: it must hold for every distribution with a finite variance, so it must hold for this one, and no smaller bound could. The slack is not a defect but the price of assuming almost nothing."],
 "ask": {
  "q": "The 3-point distribution attains the bound. What does that say about trying to improve Chebyshev's inequality?",
  "nudge": "Could a smaller bound still be true for every distribution with a finite variance?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "All four inequalities and both identities",
 "objective": "State each precisely, with its assumptions.",
 "blocks": [
  {"t": "formula", "h": "Jensen's inequality",
   "body": "For a CONVEX function g and a random variable X with finite mean,\n    E(g(X)) ≥ g(E(X)).\nFor a CONCAVE g the inequality reverses: E(g(X)) ≤ g(E(X)). Equality holds exactly when g is linear on the support of X, or X is degenerate.\nConsequences: E(X²) ≥ (E X)², so Var(X) ≥ 0; E(1/X) ≥ 1/E(X) for X > 0, since 1/x is convex; E(log X) ≤ log E(X), since log is concave."},
  {"t": "step", "h": "Var(X) ≥ 0 as an instance",
   "body": "Apply Jensen with g(x) = x², which is convex. Then E(X²) ≥ (E(X))², and rearranging gives E(X²) − (E X)² = Var(X) ≥ 0. So the non-negativity of a variance is not a separate fact but the simplest case of Jensen — which is one of the variant questions in this topic's bank."},
  {"t": "formula", "h": "Markov's inequality",
   "body": "For X ≥ 0 and any a > 0,\n    P(X ≥ a) ≤ E(X)/a.\nNon-negativity is essential; the statement is false without it. It is TIGHT for the two-point variable taking the value a with probability p and 0 otherwise, where E(X) = pa and P(X ≥ a) = p = E(X)/a exactly. For smooth distributions it is very loose: for Exponential(1) the true tail is e^(−a) = 0.13534 at a = 2 against a bound of 0.5, and 0.00674 at a = 5 against 0.2."},
  {"t": "formula", "h": "Chebyshev's inequality",
   "body": "For any X with mean μ and finite variance σ², and any k > 0,\n    P(|X − μ| ≥ kσ) ≤ 1/k².\nIt follows from Markov applied to the non-negative variable (X − μ)² at the level k²σ², which is where the square comes from. At k = 2 the bound is 1/4; a normal puts 0.045500 there and a Laplace 0.059106. It is attained by the three-point distribution with mass 1/(2k²) at each of μ ± kσ."},
  {"t": "formula", "h": "Cauchy–Schwarz",
   "body": "    |E(XY)| ≤ √(E(X²) E(Y²)),\nwith equality exactly when Y = cX for some constant c. Applied to centred variables it gives\n    Cov(X,Y)² ≤ Var(X) Var(Y)   ⟹   |ρ| ≤ 1.\nSo the bound on a correlation coefficient is this inequality. Checked at correlations 0, 0.5, −0.8 and 0.95, and the equality case confirmed with Y = 3X."},
  {"t": "formula", "h": "The tail identities",
   "body": "For a non-negative X with survival function S(x) = 1 − F(x):\n    E(X)  = ∫₀^∞ [1 − F(x)] dx\n    E(X²) = ∫₀^∞ 2x[1 − F(x)] dx\nand more generally E(Xⁿ) = ∫₀^∞ n x^(n−1)[1 − F(x)]dx. Verified by quadrature: the first integral gives 1.000000, 0.500000 and 1.500000 for Exponential(1), Exponential(2) and Uniform(0,3), and the second 2.000000, 0.500000 and 3.000000 — matching the exact moments in all six cases."},
  {"t": "def", "h": "The discrete analogue",
   "body": "For a non-negative INTEGER-valued X,\n    E(X) = Σ(k≥1) P(X ≥ k).\nThe sum counts each value as many times as it exceeds thresholds. Verified for the geometric counting trials: the sum is 3.333333 at p = 0.3 and 2.000000 at p = 0.5, matching 1/p. This is often the quickest route to the mean of a waiting-time variable."}],
 "table": {
  "caption": "Chebyshev's bound against the truth, every distribution standardised to mean 0 and variance 1.",
  "head": ["distribution", "k = 1", "k = 1.5", "k = 2", "k = 3", "ratio at k = 2"],
  "rows": [
   ["Chebyshev bound 1/k²", "1.0000", "0.4444", "0.2500", "0.1111", "1.000"],
   ["Normal", "0.3173", "0.1336", "0.0455", "0.0027", "0.182"],
   ["Laplace", "0.2431", "0.1205", "0.0591", "0.0143", "0.236"],
   ["Uniform", "0.4226", "0.1340", "0", "0", "0"],
   ["3-point at ±k", "1.0000", "0.4444", "0.2500", "0.1111", "1.000"]]},
 "flow": {
  "title": "Choosing an inequality",
  "alt": "Flow chart for selecting among Jensen, Markov, Chebyshev and Cauchy-Schwarz",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "What do you want to bound?", "kind": "start"},
   {"id": "b", "r": 1, "c": 0, "label": "E of a function vs function of E → Jensen (check convexity)", "kind": "end"},
   {"id": "c", "r": 1, "c": 1, "label": "A tail probability", "kind": "step"},
   {"id": "d", "r": 1, "c": 2, "label": "A covariance or correlation → Cauchy–Schwarz", "kind": "end"},
   {"id": "e", "r": 2, "c": 0, "label": "Only a mean, and X ≥ 0 → Markov: E(X)/a", "kind": "end"},
   {"id": "f", "r": 2, "c": 2, "label": "A variance available → Chebyshev: 1/k²", "kind": "end"},
   {"id": "g", "r": 3, "c": 1, "label": "Both are distribution-free, so both are loose for smooth distributions", "kind": "note"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "a", "to": "c"}, {"from": "a", "to": "d"},
   {"from": "c", "to": "e"}, {"from": "c", "to": "f"},
   {"from": "e", "to": "g"}, {"from": "f", "to": "g"}],
  "note": "Chebyshev is Markov applied to (X − μ)², so having a variance is what upgrades 1/a to 1/k²."},
 "ask": {
  "q": "Chebyshev follows from Markov. What extra information buys the improvement from 1/a to 1/k²?",
  "nudge": "Markov needs a mean. What does Chebyshev need?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked — the exam's four statements, ruled on",
 "objective": "Decide each statement and see which one is designed to fail.",
 "ask": {
  "q": "Which single piece of knowledge decides the whole question?",
  "nudge": "Three statements are true and one false. What does the false one hinge on?"},
 "problem": "Let X be a non-negative random variable with distribution function F. Rule on each: A. ∫₀^∞ 2x[1 − F(x)]dx = E(X²). B. ∫₀^∞ [1 − F(x)]dx = E(X). C. E(1/X) ≤ 1/E(X). D. E(log X) ≤ log E(X).",
 "steps": [
  {"say": "Statement B first — it is the simpler identity.",
   "math": "∫₀^∞ [1 − F(x)]dx = ∫₀^∞ P(X > x) dx = E(X)\ncheck: Exp(1) → 1.000000 = E(X) = 1  ✓\n       Exp(2) → 0.500000 = 0.5          ✓\n       Unif(0,3) → 1.500000 = 1.5       ✓",
   "why": "TRUE. The identity follows from swapping the order of integration in E(X) = ∫₀^∞∫₀^x dy f(x)dx. Confirmed by quadrature on three distributions to six decimal places."},
  {"say": "Statement A, the second-moment version.",
   "math": "∫₀^∞ 2x[1 − F(x)]dx = E(X²)\ncheck: Exp(1) → 2.000000 = E(X²) = 2    ✓\n       Exp(2) → 0.500000 = 0.5          ✓\n       Unif(0,3) → 3.000000 = 3         ✓",
   "why": "TRUE. The general form is E(Xⁿ) = ∫₀^∞ n x^(n−1)[1 − F(x)]dx, and n = 2 gives the 2x factor. All three checks exact."},
  {"say": "Statement C — the one the question is built around.",
   "math": "1/x has second derivative 2/x³ > 0 on x > 0 ⟹ CONVEX\nJensen for convex g: E(g(X)) ≥ g(E(X))\n⟹ E(1/X) ≥ 1/E(X),  the OPPOSITE direction\n⟹ statement C is FALSE",
   "why": "FALSE. Concretely, with X equal to 1 or 3 with probability ½: E(1/X) = 2/3 ≈ 0.667 while 1/E(X) = 0.5. And on Uniform(1,3), E(1/X) = ln 3/2 = 0.549306 against 0.5. The inequality runs the other way."},
  {"say": "Statement D, for contrast.",
   "math": "log x has second derivative −1/x² < 0 ⟹ CONCAVE\nJensen for concave g: E(g(X)) ≤ g(E(X))\n⟹ E(log X) ≤ log E(X)  ✓ TRUE\ncheck on Unif(1,3): 0.647918 ≤ 0.693147  ✓",
   "why": "TRUE. Note that C and D have the SAME written form, 'E(g(X)) ≤ g(E(X))', and differ only in whether g is convex or concave. That is the whole difficulty of the question."},
  {"say": "Assemble the answer.",
   "math": "A TRUE, B TRUE, C FALSE, D TRUE\n⟹ A, B and D",
   "why": "Which is the paper's key. The question is well made: it pairs a convex and a concave function in identically shaped statements, so a candidate who has memorised 'Jensen says E(g(X)) ≤ g(E(X))' without the convexity condition will accept both C and D, or reject both."}],
 "after": "Answering the question above: the direction of Jensen, which depends entirely on whether g is convex or concave. The habit to build is to differentiate twice before writing anything down — 1/x gives 2/x³ > 0 and so is convex, log x gives −1/x² < 0 and so is concave, and the inequality follows mechanically from there."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the four statements before applying them.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "State Jensen's inequality for a convex g, and for a concave g.",
   "a": "Convex: E(g(X)) ≥ g(E(X)). Concave: E(g(X)) ≤ g(E(X))."},
  {"q": "Which way round are E(1/X) and 1/E(X), and why?",
   "a": "E(1/X) ≥ 1/E(X), because 1/x is convex on the positive half-line."},
  {"q": "State Markov's inequality and its assumption.",
   "a": "P(X ≥ a) ≤ E(X)/a, requiring X ≥ 0."},
  {"q": "State Chebyshev's inequality and the bound at k = 2.",
   "a": "P(|X − μ| ≥ kσ) ≤ 1/k², so 1/4 at k = 2."},
  {"q": "Give the two tail identities for a non-negative X.",
   "a": "E(X) = ∫₀^∞[1 − F]dx and E(X²) = ∫₀^∞ 2x[1 − F]dx."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — five applications",
 "objective": "Apply each inequality and identity once.",
 "problem": "State the bound or the value, and name what you used.",
 "steps": [
  {"say": "A non-negative X has mean 4. Bound P(X ≥ 20).",
   "blank": {"prompt": "Give the bound and name the inequality.",
             "answer": "Markov: P ≤ 4/20 = 0.2",
             "accept": ["0.2 markov", "markov 0.2", "0.20, markov"],
             "hint": "P(X ≥ a) ≤ E(X)/a."},
   "why": "Markov gives 0.2 with nothing but the mean and non-negativity. It is usually very loose — for an Exponential with mean 4, the true probability is e^(−5) = 0.0067, thirty times smaller."},
  {"say": "X has mean 50 and standard deviation 5. Bound P(|X − 50| ≥ 15).",
   "blank": {"prompt": "Give the bound and name the inequality.",
             "answer": "Chebyshev with k = 3: P ≤ 1/9 = 0.1111",
             "accept": ["1/9 chebyshev", "0.1111, chebyshev", "chebyshev 0.111"],
             "hint": "15 is how many standard deviations?"},
   "why": "15/5 = 3, so k = 3 and the bound is 1/9 = 0.1111. For a normal the true probability would be 0.002700, forty-one times smaller — but Chebyshev holds without assuming normality."},
  {"say": "X ~ Geometric(0.25) counting trials.",
   "blank": {"prompt": "Use the discrete tail identity to give E(X).",
             "answer": "Σ(k≥1) P(X ≥ k) = Σ(0.75)^(k−1) = 1/0.25 = 4",
             "accept": ["4", "4.0", "1/p = 4"],
             "hint": "P(X ≥ k) = (1 − p)^(k−1)."},
   "why": "A geometric series summing to 1/p = 4. Verified at other values: the sum is 3.333333 at p = 0.3 and 2.000000 at p = 0.5, matching 1/p both times. This is usually faster than summing k p(1−p)^(k−1) directly."},
  {"say": "X is positive with E(X) = 2.",
   "blank": {"prompt": "What can you say about E(1/X), and by what?",
             "answer": "E(1/X) ≥ 1/2, by Jensen since 1/x is convex",
             "accept": ["at least 0.5, jensen", ">= 1/2 by jensen", "greater than or equal 0.5"],
             "hint": "Which direction does Jensen point for a convex function?"},
   "why": "Jensen gives E(1/X) ≥ 1/E(X) = 0.5. Note it gives a LOWER bound only — E(1/X) could be anything above 0.5, including infinite, as it is for an exponential."},
  {"say": "Two variables have Var(X) = 9, Var(Y) = 16.",
   "blank": {"prompt": "Bound |Cov(X,Y)|, and name the inequality.",
             "answer": "Cauchy–Schwarz: |Cov| ≤ √(9 × 16) = 12",
             "accept": ["12 cauchy-schwarz", "12, cauchy schwarz", "at most 12"],
             "hint": "Cov² ≤ Var(X)Var(Y)."},
   "why": "√144 = 12, attained only when Y is a linear function of X. Equivalently |ρ| = |Cov|/12 ≤ 1, which is the familiar statement — so the bound on a correlation coefficient is Cauchy–Schwarz in disguise."}],
 "after": "The structure to carry: Markov needs a mean and non-negativity, Chebyshev a variance, Jensen a convexity verdict, Cauchy–Schwarz two variances. Each is cheap to apply and each is loose, because each assumes almost nothing about the distribution."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "Why these bounds are loose, and when loose is enough",
 "objective": "Judge an inequality by what it is for.",
 "blocks": [
  {"t": "step", "h": "The source of the slack",
   "body": "A distribution-free bound must hold for the worst distribution satisfying its assumptions, so its value is set by that worst case and not by the case in front of you. Chebyshev's worst case is the three-point distribution with mass 1/(2k²) at each of μ ± kσ, which attains 1/k² exactly. Markov's is the two-point variable at 0 and a. No smaller bound is available without further assumptions."},
  {"t": "step", "h": "What they are actually for",
   "body": "Not for computing probabilities — if the distribution is known, compute the probability. They are for proving things. Chebyshev gives the weak law of large numbers in two lines: P(|X̄ₙ − μ| ≥ ε) ≤ σ²/(nε²) → 0. That is an asymptotic statement where a loose constant costs nothing, and it is the main reason the inequality is taught."},
  {"t": "step", "h": "The one-sided improvement",
   "body": "For a one-sided tail, Cantelli's inequality gives P(X − μ ≥ kσ) ≤ 1/(1 + k²), which at k = 2 is 0.2 rather than the 0.25 that halving Chebyshev's two-sided bound would suggest. It is a genuine improvement obtained by using the one-sidedness, and it is worth knowing that the two-sided bound should not simply be halved."},
  {"t": "step", "h": "Jensen is different in kind",
   "body": "Jensen is not a bound on a probability but an exact ordering between two quantities, and it is sharp in the sense that equality is attained whenever g is linear on the support. It is also the workhorse of the four: the arithmetic–geometric mean inequality, the non-negativity of variance, the information inequality in statistics and the fact that a log-likelihood's expectation is maximised at the truth are all instances."},
  {"t": "def", "h": "Cauchy–Schwarz as the odd one out",
   "body": "It bounds a covariance rather than a probability, and its equality condition — linear dependence — is what gives it content. Beyond |ρ| ≤ 1 it underlies the Cramér–Rao bound of topic 4.6, where it is applied to a score function and an estimator, and the fact that the bound is attained exactly when the estimator is a linear function of the score."}],
 "ask": {
  "q": "Chebyshev proves the weak law of large numbers despite being loose. Why does the looseness not matter there?",
  "nudge": "What has to happen to σ²/(nε²) as n grows?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — four parts",
 "objective": "Build the extremal cases and compare the bounds.",
 "problem": "(a) Construct a distribution attaining Chebyshev's bound at k = 2, and verify its variance. (b) For X ~ Exponential(1), compare Markov's bound at a = 3 with the truth. (c) Use the tail identity to get E(X²) for Exponential(1). (d) Give the ratio of truth to bound for a normal at k = 1, 2 and 3, and say what the trend shows.",
 "hints": [
  "For (a), put mass p at each of ±2 and the rest at 0, and choose p to make the variance 1.",
  "For (b), the true tail of Exp(1) is e^(−a).",
  "For (c), ∫₀^∞ 2x e^(−x)dx."],
 "answer": "(a) Mass 1/8 at each of ±2 and 3/4 at 0; variance 1 and P(|X| ≥ 2) = 1/4 exactly. (b) Bound 1/3 = 0.3333 against the truth e^(−3) = 0.049787, a factor of 6.7. (c) 2 × 1! = 2. (d) 0.317, 0.182, 0.024 — the slack grows rapidly with k.",
 "check": "In (a) the general recipe is mass 1/(2k²) at each of ±k, which at k = 2 is 1/8 = 0.125; the variance is 2(1/8)(4) = 1 ✓ and the tail probability is 2(1/8) = 0.25 = 1/k² ✓, both verified at k = 2 and k = 3. In (d) the trend matters more than the numbers: Chebyshev's bound decays as 1/k² while a normal's tail decays like e^(−k²/2), so the ratio collapses and the bound becomes progressively more useless the further out you go.",
 "scenario": {
  "teaser": "An engineer uses Chebyshev to set a tolerance and the result is commercially unusable.",
  "title": "A bound too safe to use",
  "body": [
   "A component's measured dimension has mean 50 mm and standard deviation 0.5 mm. An engineer wants an interval containing at least 95% of production. Using Chebyshev, 1/k² = 0.05 gives k = √20 ≈ 4.47, so the interval is 50 ± 2.24 mm. The specification allows ±1.5 mm, so the process appears to fail.",
   "If the dimension is approximately normal, the 95% interval is 50 ± 1.96(0.5) = 50 ± 0.98 mm, comfortably inside specification. The two answers differ by a factor of 2.3 on the half-width, and the decision flips entirely.",
   "Neither calculation is wrong. Chebyshev's answer is correct and guaranteed with no assumption beyond a finite variance; the normal answer is correct if the normality holds. The engineer has to decide which they are entitled to, and that is a question about the process, settled by looking at the data rather than by choosing the more convenient inequality.",
   "The cost of the distribution-free route is visible here as a concrete business outcome: rejecting a process that is in fact capable. That is the practical shape of the slack the chart in section 2 displays, and it is why Chebyshev is a tool for proofs rather than for tolerances.",
   "The right move is to check the distributional assumption. A few hundred measurements and a normal probability plot would settle whether the normal interval is defensible, and if the data are skewed or heavy-tailed, a nonparametric interval based on the empirical quantiles would be far tighter than Chebyshev while still assuming little.",
   "The general principle is that an assumption-free method is not automatically the safe choice. It is safe against being WRONG and unsafe against being USELESS, and which failure matters depends on the decision being made."],
  "q": "Chebyshev's interval is guaranteed while the normal interval is not. Why is the guaranteed answer not automatically the right one to use?",
  "answer": "Because it protects against the wrong kind of error for this decision. Chebyshev's guarantee comes from holding for the worst distribution with that variance, so its interval of 50 ± 2.24 mm is correct but driven by a pathological case the actual process almost certainly is not — and acting on it means rejecting a process that meets specification, a real and costly error. The normal interval of 50 ± 0.98 mm is tighter by a factor of 2.3 but requires an assumption that may or may not hold. The resolution is not to pick whichever inequality gives the preferred answer but to check the assumption empirically, with a few hundred measurements and a probability plot; if normality fails, an interval built from the empirical quantiles would still be far tighter than Chebyshev while assuming little. Assumption-free methods are safe against being wrong and unsafe against being useless."},
 "solution": [
  {"say": "(a) The extremal distribution at k = 2.",
   "math": "put mass p at −2, mass p at +2, mass 1 − 2p at 0\nvariance = 2p(4) = 8p, set equal to 1 ⟹ p = 1/8 = 0.125\nmean = 0 ✓\nP(|X| ≥ 2) = 2p = 0.25 = 1/k² ✓",
   "why": "The general recipe is p = 1/(2k²) at each end. Verified computationally at k = 2 and k = 3: variance 1.000000 in both cases, with tail probabilities 0.250000 and 0.111111 exactly matching 1/k²."},
  {"say": "(b) Markov's slack on an exponential.",
   "math": "bound: E(X)/a = 1/3 = 0.333333\ntruth: P(X ≥ 3) = e^(−3) = 0.049787\nratio: 0.1494, so the bound is 6.7× too large",
   "why": "And it gets worse further out: at a = 5 the bound is 0.2 against a truth of 0.006738, a factor of 30. Markov's bound decays as 1/a while an exponential tail decays geometrically."},
  {"say": "(c) The second moment by the tail identity.",
   "math": "E(X²) = ∫₀^∞ 2x[1 − F(x)]dx = ∫₀^∞ 2x e^(−x)dx\n      = 2 ∫₀^∞ x e^(−x)dx = 2 Γ(2) = 2(1!) = 2",
   "why": "Matching the known E(X²) = 2 for Exponential(1), and confirmed by quadrature at 2.000000. The identity is often easier than integrating x²f(x), especially when F has a simple closed form and f does not."},
  {"say": "(d) The normal ratios.",
   "math": "k=1: 0.317311/1.0000  = 0.3173\nk=2: 0.045500/0.2500  = 0.1820\nk=3: 0.002700/0.1111  = 0.0243",
   "why": "The trend is the lesson. Chebyshev's bound decays as 1/k², polynomially, while a normal tail decays like e^(−k²/2), which is far faster. So the ratio collapses and the bound becomes progressively more useless the further into the tail you go — exactly the opposite of what one would want from a tail bound."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims this topic turns on.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "For a positive random variable, E(1/X) ≤ 1/E(X).",
   "tf": False,
   "why": "False, and it is the statement the June 2026 question excludes from its key. 1/x is CONVEX on the positive half-line, with second derivative 2/x³ > 0, so Jensen gives E(1/X) ≥ 1/E(X). Concretely, X equal to 1 or 3 with probability ½ gives E(1/X) = 2/3 against 1/E(X) = 0.5."},
  {"claim": "E(log X) ≤ log E(X).",
   "tf": True,
   "why": "True, because log is CONCAVE, with second derivative −1/x² < 0, and Jensen reverses for concave functions. Verified on Uniform(1,3): E(log X) = (3 ln 3 − 2)/2 = 0.647918 against log 2 = 0.693147. Note this and the previous statement have identical written form and differ only in the convexity of g."},
  {"claim": "Markov's inequality holds for any random variable with a finite mean.",
   "tf": False,
   "why": "False — it requires X ≥ 0. Without non-negativity the statement fails: a variable with mean 0 taking large positive and negative values would have P(X ≥ a) bounded by 0, which is absurd. Non-negativity is what makes the proof's discarded region contribute nothing negative."},
  {"claim": "Chebyshev's inequality cannot be improved without further assumptions.",
   "tf": True,
   "why": "True. The three-point distribution with mass 1/(2k²) at each of μ ± kσ and the rest at μ has variance exactly σ² and tail probability exactly 1/k², so it attains the bound. Any smaller bound would be false for that distribution, and it satisfies the inequality's only assumption of a finite variance."},
  {"claim": "For a non-negative integer-valued X, E(X) = Σ(k≥1) P(X ≥ k).",
   "tf": True,
   "why": "True — the discrete analogue of the tail integral. Verified for the geometric counting trials, where the sum of (1−p)^(k−1) gives 1/p: 3.333333 at p = 0.3 and 2.000000 at p = 0.5. It is usually the quickest route to the mean of a waiting-time variable."},
  {"claim": "The bound |ρ| ≤ 1 on a correlation coefficient is a separate result from Cauchy–Schwarz.",
   "tf": False,
   "why": "False — it IS Cauchy–Schwarz. Applying |E(XY)| ≤ √(E(X²)E(Y²)) to the centred variables gives Cov(X,Y)² ≤ Var(X)Var(Y), which rearranges directly to |ρ| ≤ 1. The equality condition, linear dependence, is what makes |ρ| = 1 mean a perfect linear relationship."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 8,
 "title": "On your own — six quick values",
 "objective": "Apply the bounds at exam speed.",
 "problem": "(a) X ≥ 0 with mean 6: bound P(X ≥ 30). (b) μ = 100, σ = 10: bound P(|X − 100| ≥ 25). (c) X ~ Geometric(0.2) counting trials: E(X) by the tail sum. (d) Var(X) = 4, Var(Y) = 25: bound |Cov|. (e) Is E(√X) ≥ or ≤ √(E X)? (f) Chebyshev's bound at k = 1, and what it tells you.",
 "hints": [
  "For (b), 25 is 2.5 standard deviations.",
  "For (e), is √x convex or concave?",
  "For (f), substitute k = 1 and read the result."],
 "answer": "(a) 6/30 = 0.2. (b) 1/2.5² = 0.16. (c) 1/0.2 = 5. (d) √100 = 10. (e) ≤, since √x is concave. (f) 1, which is no information at all.",
 "check": "Part (f) is the one worth dwelling on: at k = 1 the bound is 1, and since every probability is at most 1 the inequality says nothing. Chebyshev only becomes informative beyond one standard deviation, which is a real limitation when σ is large relative to the deviation of interest. Part (e) completes the convexity pattern: x² and 1/x are convex so Jensen points one way, while log x and √x are concave so it points the other.",
 "solution": [
  {"say": "(a), (b) and (f): the tail bounds.",
   "math": "Markov: 6/30 = 0.2\nChebyshev: k = 25/10 = 2.5, bound 1/6.25 = 0.16\nChebyshev at k = 1: 1/1 = 1 — vacuous",
   "why": "Note how modest the Chebyshev bound is even at 2.5 standard deviations: 16% of the probability is still permitted out there, where a normal would put 1.24%."},
  {"say": "(c) and (d): the identity and Cauchy–Schwarz.",
   "math": "Σ(k≥1) (0.8)^(k−1) = 1/(1 − 0.8) = 5 = 1/p\n|Cov| ≤ √(4 × 25) = √100 = 10",
   "why": "In (d) the bound 10 is attained only if Y is a linear function of X; equivalently |ρ| = |Cov|/10 ≤ 1."},
  {"say": "(e) The square root.",
   "math": "√x has second derivative −1/(4x^(3/2)) < 0 ⟹ CONCAVE\n⟹ E(√X) ≤ √(E X)",
   "why": "The same direction as log. A quick numerical check: X equal to 1 or 9 with probability ½ gives E(√X) = (1 + 3)/2 = 2 against √(E X) = √5 = 2.236 ✓."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "Where these four turn up again",
 "objective": "See them as tools the rest of the syllabus uses.",
 "blocks": [
  {"t": "step", "h": "The weak law of large numbers",
   "body": "Chebyshev applied to the sample mean gives P(|X̄ₙ − μ| ≥ ε) ≤ σ²/(nε²), which tends to zero for any fixed ε. That is the weak law, proved in two lines, and it is the clearest case of a loose bound being entirely adequate because only the limit matters."},
  {"t": "step", "h": "The Cramér–Rao bound (topic 4.6)",
   "body": "Cauchy–Schwarz applied to an unbiased estimator and the score function gives Var(T) ≥ 1/I(θ). The equality condition — that the two be linearly related — is exactly the condition for an estimator to attain the bound, which is why attainment happens only in exponential families."},
  {"t": "step", "h": "Information inequalities",
   "body": "Jensen applied to the log function shows that the Kullback–Leibler divergence is non-negative, and hence that the expected log-likelihood is maximised at the true parameter. That is the foundation under maximum likelihood's consistency, so topic 4.4 rests on this lesson's first inequality."},
  {"t": "step", "h": "Concentration and moment generating functions",
   "body": "Markov applied to e^(tX) rather than X gives P(X ≥ a) ≤ E(e^(tX))/e^(ta), which optimised over t is the Chernoff bound — exponentially small rather than polynomially small. So the looseness of Markov is not inherent; it comes from applying it to X instead of to a rapidly growing function of X."},
  {"t": "def", "h": "The pattern",
   "body": "Each of these is the same inequality applied to a cleverly chosen function: Chebyshev is Markov on (X − μ)², Chernoff is Markov on e^(tX), Cramér–Rao is Cauchy–Schwarz on an estimator and a score, and the information inequality is Jensen on a log. Learning to choose the function is most of the skill."}],
 "ask": {
  "q": "Chernoff's bound is Markov applied to e^(tX) and is exponentially small. What does that say about Markov's apparent weakness?",
  "nudge": "Was the weakness in the inequality, or in what it was applied to?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the directions and the extremal cases.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Which of x², 1/x, log x, √x are convex, and which concave?",
   "a": "x² and 1/x (on x > 0) are convex; log x and √x are concave."},
  {"q": "Which distribution attains Chebyshev's bound?",
   "a": "Mass 1/(2k²) at each of μ ± kσ, the rest at μ. Variance σ², tail exactly 1/k²."},
  {"q": "Which distribution makes Markov tight?",
   "a": "X = a with probability p and 0 otherwise, giving P(X ≥ a) = p = E(X)/a."},
  {"q": "Give the true tail of a standard normal at k = 2 and 3, against the bound.",
   "a": "0.045500 and 0.002700, against 0.25 and 0.1111 — ratios 0.182 and 0.024."},
  {"q": "Give the general tail identity for the nth moment.",
   "a": "E(Xⁿ) = ∫₀^∞ n x^(n−1)[1 − F(x)]dx for non-negative X."},
  {"q": "What is Chebyshev's bound at k = 1, and what use is it?",
   "a": "1 — vacuous, since every probability is at most 1."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Decide convexity by the second derivative and get Jensen's direction right every time.",
  "Rule on the June 2026 statements and explain why E(1/X) ≤ 1/E(X) is false.",
  "Apply Markov and Chebyshev, and state the assumption each needs.",
  "Construct the distributions that attain each bound and verify them.",
  "Use the tail identities for E(X) and E(X²), and the discrete sum for a waiting time.",
  "Derive |ρ| ≤ 1 from Cauchy–Schwarz and state its equality condition.",
  "Say how much slack a bound carries for a normal, and why that does not make it useless.",
  "Recognise that E(1/X) can be infinite, so a numerical check needs a suitable distribution."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "The proofs, each in a few lines",
 "objective": "See why each holds, which makes the conditions memorable.",
 "blocks": [
  {"t": "step", "h": "Markov",
   "body": "For X ≥ 0 and a > 0, write X ≥ X·1{X ≥ a} ≥ a·1{X ≥ a}. Taking expectations, E(X) ≥ a P(X ≥ a), which rearranges to the result. The first step is where non-negativity is used: without it, discarding the region X < a could remove negative contributions and reverse the inequality."},
  {"t": "step", "h": "Chebyshev from Markov",
   "body": "Apply Markov to the non-negative variable Y = (X − μ)² at level a = k²σ². Then\n    P(|X − μ| ≥ kσ) = P(Y ≥ k²σ²) ≤ E(Y)/(k²σ²) = σ²/(k²σ²) = 1/k².\nThe squaring is what turns 1/a into 1/k², and it is also why a variance rather than a mean is the requirement."},
  {"t": "step", "h": "Jensen, for a differentiable convex g",
   "body": "Convexity means the curve lies above each of its tangents: g(x) ≥ g(m) + g'(m)(x − m) for every x and m. Put m = E(X) and take expectations. The linear term has expectation zero, since E(X − m) = 0, leaving E(g(X)) ≥ g(E(X)). Equality requires the curve to coincide with its tangent over the support of X, which means g is linear there."},
  {"t": "step", "h": "Cauchy–Schwarz",
   "body": "For any real t, 0 ≤ E((X − tY)²) = E(X²) − 2tE(XY) + t²E(Y²). A quadratic in t that is never negative has non-positive discriminant, so 4(E(XY))² − 4E(X²)E(Y²) ≤ 0, giving (E(XY))² ≤ E(X²)E(Y²). Equality needs the quadratic to have a repeated root, that is E((X − tY)²) = 0 for some t, which means X = tY almost surely."},
  {"t": "step", "h": "The tail identity",
   "body": "For X ≥ 0 with density f, write E(X) = ∫₀^∞ x f(x)dx = ∫₀^∞ (∫₀^x dy) f(x)dx and swap the order of integration: = ∫₀^∞ (∫_y^∞ f(x)dx) dy = ∫₀^∞ P(X > y)dy. For the nth moment, replace ∫₀^x dy by ∫₀^x n y^(n−1)dy, which gives the n x^(n−1) factor. The discrete version swaps a double sum in the same way."}],
 "ask": {
  "q": "Three of these four proofs are two or three lines. Does that make the results weak?",
  "nudge": "Compare how much each assumes with how much it concludes."}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "probability_t7_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "probabilityt7",
 "topicId": "probability-t7",
 "moduleId": "probability",
 "title": "Jensen, Markov, Chebyshev and Cauchy–Schwarz",
 "breadcrumb": "Probability → Inequalities → Four bounds and two identities",
 "engine": "B",
 "engineName": "Probability — conclusions bought with almost no assumptions",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Decide convexity by the second derivative and get Jensen's direction right.",
  "Rule on the June 2026 four-statement question and say why E(1/X) ≤ 1/E(X) is false.",
  "Apply Markov and Chebyshev, naming the assumption each requires.",
  "Construct the distributions that attain each bound and verify them.",
  "Use the tail identities for E(X) and E(X²) and the discrete sum for a waiting time.",
  "Derive |ρ| ≤ 1 from Cauchy–Schwarz and state the equality condition."],
 "prereq": [
  {"id": "p1", "name": "Convex and concave functions",
   "why": "Jensen's direction depends entirely on which it is, and the second derivative is the test."},
  {"id": "p2", "name": "Expectation and variance",
   "why": "Every inequality here relates moments, and Chebyshev needs a finite variance to say anything."},
  {"id": "p3", "name": "Distribution and survival functions",
   "why": "The tail identities express moments as integrals of 1 − F(x)."},
  {"id": "p4", "name": "Covariance and correlation (topic 1.13)",
   "why": "|ρ| ≤ 1 is Cauchy–Schwarz applied to centred variables, and its equality case is linear dependence."}],
 "traps": [
  "E(1/X) ≥ 1/E(X), NOT ≤ — 1/x is convex. This is the exam's trap.",
  "Jensen REVERSES for a concave function; log x and √x go the other way from x² and 1/x.",
  "Markov requires X ≥ 0. Without it the statement is false.",
  "Chebyshev at k = 1 gives the bound 1, which is no information at all.",
  "Do not halve the two-sided Chebyshev bound for a one-sided tail; use Cantelli's 1/(1 + k²).",
  "E(1/X) can be INFINITE — for Exponential(1) it diverges, so simulations misbehave.",
  "The bounds are for proving things, not for computing probabilities you could compute exactly.",
  "A sample mean that drifts upward with n signals a non-existent expectation, not a coding bug."],
 "revision": {
  "sheet": [
   "CONVEXITY: g'' ≥ 0 convex, g'' ≤ 0 concave. x², eˣ, 1/x (x > 0), |x| convex. log x, √x concave.",
   "JENSEN, convex g:  E(g(X)) ≥ g(E(X)).   Concave g:  E(g(X)) ≤ g(E(X)).",
   "  Equality iff g is linear on the support of X, or X is degenerate.",
   "⟹ E(X²) ≥ (E X)², i.e. Var(X) ≥ 0 — Jensen with g(x) = x².",
   "⟹ E(1/X) ≥ 1/E(X) for X > 0, since 1/x has second derivative 2/x³ > 0. NOT ≤.",
   "⟹ E(log X) ≤ log E(X) and E(√X) ≤ √(E X), both concave.",
   "  Check: X ∈ {1,3} each w.p. ½ → E(1/X) = 2/3 = 0.667 vs 1/E(X) = 0.5.",
   "  Unif(1,3): E(1/X) = ln3/2 = 0.549306 vs 0.5; E(logX) = (3ln3−2)/2 = 0.647918 vs log2 = 0.693147.",
   "  Gamma(3,1): E(1/X) = 1/(k−1) = 0.5 vs 1/E(X) = 0.333333.",
   "  CAVEAT: for Exp(1), E(1/X) DIVERGES. Jensen holds with an infinite left side; simulations drift.",
   "MARKOV: X ≥ 0, a > 0 ⟹ P(X ≥ a) ≤ E(X)/a. Non-negativity is ESSENTIAL.",
   "  TIGHT for X = a w.p. p, else 0: then P(X ≥ a) = p = E(X)/a exactly.",
   "  Exp(1): truth e^−a = 0.13534, 0.04979, 0.00674 at a = 2, 3, 5 vs bounds 0.5, 0.3333, 0.2.",
   "CHEBYSHEV: P(|X − μ| ≥ kσ) ≤ 1/k². Needs only a finite variance. At k = 1 the bound is 1 — vacuous.",
   "  It is MARKOV applied to (X − μ)² at level k²σ², which is where the square comes from.",
   "  Normal truth: 0.317311, 0.133614, 0.045500, 0.002700 at k = 1, 1.5, 2, 3.",
   "  Ratios truth/bound: 0.317, 0.301, 0.182, 0.024 — the slack GROWS with k.",
   "  Laplace at k=2: 0.059106 (ratio 0.236), closest of the smooth cases. Uniform: exactly 0 past k = √3.",
   "  TIGHT: mass 1/(2k²) at each of μ ± kσ, rest at μ. At k=2 that is 0.125, 0.75, 0.125.",
   "    Variance verified 1.000000; P(|X| ≥ k) = 1/k² exactly at k = 2 and 3. So it CANNOT be improved.",
   "ONE-SIDED (Cantelli): P(X − μ ≥ kσ) ≤ 1/(1 + k²) — 0.2 at k = 2, better than halving 1/4.",
   "CAUCHY–SCHWARZ: |E(XY)| ≤ √(E(X²)E(Y²)), equality iff Y = cX.",
   "  Centred ⟹ Cov(X,Y)² ≤ Var(X)Var(Y) ⟹ |ρ| ≤ 1. So that bound IS Cauchy–Schwarz.",
   "  Verified at ρ = 0, 0.5, −0.8, 0.95; equality with Y = 3X gave 2.9961 both sides.",
   "TAIL IDENTITIES, X ≥ 0:  E(X) = ∫₀^∞[1 − F(x)]dx ;  E(X²) = ∫₀^∞ 2x[1 − F(x)]dx.",
   "  General: E(Xⁿ) = ∫₀^∞ n x^(n−1)[1 − F(x)]dx.",
   "  Verified by quadrature: ∫[1−F] = 1.0, 0.5, 1.5 for Exp(1), Exp(2), Unif(0,3);",
   "    ∫2x[1−F] = 2.0, 0.5, 3.0 — matching E(X) and E(X²) in all six cases.",
   "DISCRETE: non-negative integer X ⟹ E(X) = Σ(k≥1) P(X ≥ k).",
   "  Geometric counting trials: Σ(1−p)^(k−1) = 1/p. Verified 3.333333 at p=0.3, 2.0 at p=0.5.",
   "JUNE 2026 Q31 (answered correctly): statements A (E X² tail), B (E X tail), D (E log X) TRUE;",
   "  C (E(1/X) ≤ 1/E(X)) FALSE. Key = 'A, B and D'. The question pairs a convex and a concave",
   "  function in identically shaped statements, so the convexity condition is the whole difficulty.",
   "WHERE THEY REAPPEAR: Chebyshev ⟹ weak law, P(|X̄ − μ| ≥ ε) ≤ σ²/(nε²).",
   "  Cauchy–Schwarz ⟹ Cramér–Rao (topic 4.6). Jensen ⟹ KL divergence ≥ 0, hence MLE consistency.",
   "  Markov on e^(tX) ⟹ Chernoff, exponentially small — the weakness was the choice of function."],
  "cards": [
   ["Jensen, convex g", "E(g(X)) ≥ g(E(X))"],
   ["Jensen, concave g", "E(g(X)) ≤ g(E(X))"],
   ["E(1/X) vs 1/E(X)", "≥, since 1/x is convex"],
   ["E(log X) vs log E(X)", "≤, since log is concave"],
   ["Var(X) ≥ 0 is Jensen on", "g(x) = x²"],
   ["Markov", "P(X ≥ a) ≤ E(X)/a, needs X ≥ 0"],
   ["Chebyshev", "P(|X − μ| ≥ kσ) ≤ 1/k²"],
   ["Chebyshev at k = 2 vs a normal", "0.25 against 0.0455"],
   ["Attains Chebyshev", "Mass 1/(2k²) at each of μ ± kσ"],
   ["Cauchy–Schwarz", "|E(XY)| ≤ √(E X² E Y²); gives |ρ| ≤ 1"],
   ["E(X) for X ≥ 0", "∫₀^∞[1 − F(x)]dx"],
   ["E(X) for integer X ≥ 0", "Σ(k≥1) P(X ≥ k)"]],
  "tricks": [
   "Differentiate twice before writing anything — convexity decides the direction mechanically.",
   "Chebyshev's k is the deviation DIVIDED BY σ; compute that first.",
   "At k = 1 Chebyshev says nothing, so a question using k = 1 is testing whether you notice.",
   "For a one-sided tail reach for Cantelli's 1/(1 + k²), not half of 1/k².",
   "The tail identity is often easier than ∫xf(x)dx when F is simple and f is not.",
   "If asked to show a bound cannot be improved, produce the extremal distribution."],
  "shortcuts": [
   "1/k² is 1, 0.4444, 0.25, 0.1111, 0.04 at k = 1, 1.5, 2, 3, 5.",
   "Normal two-sided tails: 0.3173, 0.1336, 0.0455, 0.0027 at k = 1, 1.5, 2, 3.",
   "1/(1 + k²) is 0.5, 0.3077, 0.2, 0.1 at k = 1, 1.5, 2, 3."],
  "remember": [
   "1/x is convex, so E(1/X) ≥ 1/E(X).",
   "Markov needs X ≥ 0.",
   "Chebyshev at k = 1 is vacuous."]},
 "howto": "Section 1 settles the one thing the exam question turns on — the direction of Jensen — with a two-value example you can check in your head, and then gives the caveat that matters for anyone trying to verify it numerically: E(1/X) diverges for an exponential, so the obvious simulation produces a figure that grows with the sample size. Section 2's chart is the quantitative half: it draws Chebyshev's bound against the true tail for five distributions, showing the bound overstating a normal's tail by a factor of 5.5 at k = 2 and 41 at k = 3, and then lets you select the three-point distribution that attains it exactly, which is the answer to why the inequality cannot be improved. Section 3 states all four inequalities with their assumptions and both tail identities, and section 4 works the June 2026 question statement by statement — its design is worth noticing, since statements C and D have identical written form and differ only in whether the function is convex or concave. Section 6 applies each tool once, section 8 builds the extremal distributions, and section 10 drills the arithmetic including the vacuous k = 1 case. If short of time, sections 1, 3 and 4 are the lesson. Section 11 shows the four reappearing as the weak law, the Cramér–Rao bound, the information inequality and the Chernoff bound, which is the argument for learning them properly. The optional section proves all four in a few lines each, which is what makes the assumptions memorable.",
 "refs": [
  {"title": "An Introduction to Probability Theory and Its Applications", "where": "Volume 1, Chapter 9",
   "site": "Feller", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "Markov and Chebyshev with their extremal cases and the route to the weak law."},
  {"title": "Probability and Measure", "where": "Chapters 5 and 21",
   "site": "Billingsley", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "Jensen's inequality in general form, with the equality condition and the conditional version."},
  {"title": "Fundamentals of Mathematical Statistics", "where": "Chapters on expectation and inequalities",
   "site": "Gupta and Kapoor", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "All four inequalities with the worked problems and tail identities in the exact form Indian examinations set them."},
  {"title": "Probability and Statistics", "where": "Weeks on inequalities and limit theorems",
   "site": "NPTEL / SWAYAM", "url": "https://archive.nptel.ac.in/courses/111105090",
   "type": "Video course", "free": True, "checked": "2026-11-03",
   "why": "Indian-syllabus treatment, including the four-statement question format NET favours."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026. PYQ anchor: June 2026 Q31, which was answered CORRECTLY — the key is C and the user also marked C. This is a correction to the project's priority document, which listed this lesson among anchors 'answered wrongly with a sizeable variant bank'; that description fits Q35 but not Q31, and the document is being amended alongside this lesson. The topic was built regardless, because its ten-variant bank — j26v-q30-10 through -19, retagged to srcQ 31 — covers four distinct inequalities plus both tail identities, and the bank served as the specification. Q31's design is worth recording: its four statements are the two tail identities, E(1/X) ≤ 1/E(X), and E(log X) ≤ log E(X), with the key excluding only the third. Statements C and D have identical written form and differ solely in whether the function is convex or concave, so the question tests the convexity condition rather than the inequality's shape — which is why the lesson makes that direction its spine. Every figure was verified. Jensen's convex direction was confirmed on Uniform(1,3), where E(1/X) = ln(3)/2 = 0.549306 against 1/E(X) = 0.5, and on Gamma(3,1), where E(1/X) = 1/(k−1) = 0.5 against 1/3; the concave direction on Uniform(1,3), where E(log X) = (3ln3−2)/2 = 0.647918 against log 2 = 0.693147. One caveat is taught explicitly because the obvious example fails: for Exponential(1), E(1/X) DIVERGES, since the density is positive at the origin, so a simulation returns a figure that grows with the sample size — roughly 15 at one million draws and 40 at ten million. Jensen still holds with an infinite left-hand side, but the inequality cannot be checked that way, and the lesson uses this as a scenario about recognising a non-existent expectation from a drifting sample mean. Markov's slack was quantified on Exponential(1): true tails e^(−a) of 0.13534, 0.04979 and 0.00674 at a = 2, 3 and 5 against bounds of 0.5, 0.3333 and 0.2. Chebyshev's slack was computed for four standardised distributions, with a normal's true two-sided tail of 0.317311, 0.133614, 0.045500 and 0.002700 at k = 1, 1.5, 2 and 3 against the bound 1/k², giving ratios of 0.317, 0.301, 0.182 and 0.024 — so the slack GROWS with k, because the bound decays polynomially while a normal tail decays like e^(−k²/2). The Laplace at k = 2 gives 0.059106, the closest of the smooth cases, and a standardised uniform's tail reaches exactly zero past k = √3 ≈ 1.732 while the bound is still 1/3. The three-point distribution attaining the bound was verified by construction: mass 1/(2k²) at each of ±k and the rest at 0 gives a variance of exactly 1.000000 and tail probability exactly 1/k² at both k = 2 and k = 3, which is the lesson's answer to why the inequality cannot be improved. Both tail identities were confirmed by quadrature to six decimals on three distributions, with ∫[1−F]dx giving 1.000000, 0.500000 and 1.500000 and ∫2x[1−F]dx giving 2.000000, 0.500000 and 3.000000 for Exponential(1), Exponential(2) and Uniform(0,3); the discrete analogue Σ(k≥1)P(X ≥ k) = 1/p was confirmed as 3.333333 at p = 0.3 and 2.000000 at p = 0.5. Cauchy–Schwarz was checked at correlations of 0, 0.5, −0.8 and 0.95, with the equality case confirmed at Y = 3X where both sides come to 2.9961. Uses the new `ineq-bounds` visualisation, which plots the bound against the true tail across k for five distributions and lets the attaining case be selected so the two curves coincide. Previous-year questions are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "pr-t7-m-%02d" % i, "format": fmt, "topic": "probability-t7",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "For a convex function g, Jensen's inequality states:",
 ["E(g(X)) ≥ g(E(X))", "E(g(X)) ≤ g(E(X))",
  "E(g(X)) = g(E(X))", "no general relation holds"],
 "A",
 "Convexity means the curve lies above each of its tangents, and taking expectations about the tangent at E(X) gives the result. For a CONCAVE g it reverses to ≤. Equality holds only when g is linear on the support of X."))

I.append(q(2, "single", "easy",
 "For a positive random variable X, E(1/X) compared with 1/E(X) is:",
 ["larger or equal", "smaller or equal", "always equal", "unrelated"],
 "A",
 "1/x has second derivative 2/x³ > 0 on the positive half-line, so it is CONVEX and Jensen gives E(1/X) ≥ 1/E(X). Concretely, X taking 1 or 3 with probability ½ gives E(1/X) = 2/3 ≈ 0.667 against 1/E(X) = 0.5. Getting this direction wrong is the standard error in the topic."))

I.append(q(3, "numeric", "easy",
 "For a non-negative random variable X with distribution function F, ∫₀^∞ [1 − F(x)]dx equals:",
 ["E(X)", "E(X²)", "Var(X)", "1"],
 "A",
 "The integral of the survival function is the mean. It follows from swapping the order of integration in E(X) = ∫₀^∞(∫₀^x dy)f(x)dx. Verified by quadrature: 1.000000 for Exponential(1), 0.500000 for Exponential(2) and 1.500000 for Uniform(0,3), matching the means exactly.",
 check="For Exponential(1), ∫₀^∞ e^(−x)dx = 1, which is indeed E(X)."))

I.append(q(4, "numeric", "easy",
 "For a non-negative X, ∫₀^∞ 2x[1 − F(x)]dx equals:",
 ["E(X²)", "E(X)", "2E(X)", "Var(X)"],
 "A",
 "The general identity is E(Xⁿ) = ∫₀^∞ n x^(n−1)[1 − F(x)]dx, and n = 2 produces the 2x factor. Verified by quadrature as 2.000000, 0.500000 and 3.000000 for Exponential(1), Exponential(2) and Uniform(0,3), matching E(X²) in each case.",
 check="For Exponential(1), ∫₀^∞ 2x e^(−x)dx = 2Γ(2) = 2, which is E(X²)."))

I.append(q(5, "numeric", "easy",
 "Markov's inequality states that for X ≥ 0 and a > 0:",
 ["P(X ≥ a) ≤ E(X)/a", "P(X ≥ a) ≤ E(X)/a²",
  "P(X ≥ a) ≥ E(X)/a", "P(X ≥ a) ≤ Var(X)/a²"],
 "A",
 "Non-negativity is essential — without it the statement is false. It is proved from X ≥ a·1{X ≥ a} by taking expectations. Option D is closer to Chebyshev, which uses a variance rather than a mean.",
 check="It is tight for X = a with probability p and 0 otherwise, where E(X) = pa and P(X ≥ a) = p exactly."))

I.append(q(6, "numeric", "easy",
 "Chebyshev's inequality bounds P(|X − μ| ≥ 2σ) by:",
 ["1/4", "1/2", "1/8", "1"],
 "A",
 "The bound is 1/k² with k = 2, so 0.25. For a standard normal the true probability is only 0.045500 — the bound overstates it by a factor of 5.5 — but Chebyshev holds for every distribution with a finite variance, which is why it must accommodate the worst case.",
 check="At k = 1 the bound would be 1, which is no information at all, since every probability is at most 1."))

# --- moderate (10)
I.append(q(7, "single", "moderate",
 "E(log X) ≤ log E(X) holds because log is:",
 ["concave", "convex", "increasing", "bounded"],
 "A",
 "log x has second derivative −1/x² < 0, so it is concave and Jensen reverses. Being increasing is true but irrelevant — the direction of Jensen depends only on curvature. Note this statement and E(1/X) ≤ 1/E(X) have identical form, yet one is true and the other false, precisely because 1/x is convex."))

I.append(q(8, "single", "moderate",
 "Var(X) ≥ 0 is a special case of Jensen's inequality applied to:",
 ["x²", "log x", "1/x", "√x"],
 "A",
 "g(x) = x² is convex, so E(X²) ≥ (E(X))², and rearranging gives E(X²) − (E X)² = Var(X) ≥ 0. The other three functions are either concave or give different consequences — 1/x gives E(1/X) ≥ 1/E(X), and log x and √x both point the other way."))

I.append(q(9, "single", "moderate",
 "The Cauchy–Schwarz inequality applied to random variables yields:",
 ["|ρ| ≤ 1", "Markov's inequality", "Var(X) ≥ 0", "E(X) ≥ 0"],
 "A",
 "Applying |E(XY)| ≤ √(E(X²)E(Y²)) to the centred variables gives Cov(X,Y)² ≤ Var(X)Var(Y), which rearranges to |ρ| ≤ 1. So the familiar bound on a correlation coefficient is this inequality, and its equality condition — linear dependence — is what makes |ρ| = 1 mean a perfect linear relationship."))

I.append(q(10, "numeric", "moderate",
 "For a non-negative integer-valued X, E(X) equals:",
 ["Σ(k≥1) P(X ≥ k)", "Σ(k≥0) P(X ≥ k)", "Σ(k≥1) P(X = k)", "Σ(k≥1) k P(X ≥ k)"],
 "A",
 "The discrete analogue of the tail integral. Option B adds P(X ≥ 0) = 1, overstating by exactly 1; option C sums to 1, not to the mean. Verified for the geometric counting trials, where Σ(1−p)^(k−1) = 1/p gives 3.333333 at p = 0.3 and 2.000000 at p = 0.5.",
 check="For Geometric(0.25) the sum is 1/0.25 = 4, which matches the known mean 1/p."))

I.append(q(11, "numeric", "moderate",
 "A non-negative random variable has mean 6. Markov's bound on P(X ≥ 30) is:",
 ["0.2", "0.0333", "5", "0.8"],
 "A",
 "E(X)/a = 6/30 = 0.2. The bound uses nothing but the mean and non-negativity, and is usually very loose: for an exponential with mean 6 the true probability is e^(−5) = 0.006738, thirty times smaller.",
 check="Any probability bound must lie in [0, 1], which rules out option C immediately."))

I.append(q(12, "multi", "moderate",
 "Consider the four inequalities.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true — 1/x is convex. B is true: Chebyshev is Markov applied to (X − μ)². C is true, and it is why the bound cannot be improved. D is false — Markov requires non-negativity.",
 statements=["E(1/X) ≥ 1/E(X) for a positive random variable.",
             "Chebyshev's inequality follows from Markov's.",
             "There is a distribution attaining Chebyshev's bound exactly.",
             "Markov's inequality holds for any variable with a finite mean."],
 verdicts=verd(
  (True, "True. 1/x has second derivative 2/x³ > 0 on x > 0, so it is convex and Jensen points that way. On Uniform(1,3) the two sides are 0.549306 and 0.5."),
  (True, "True — apply Markov to the non-negative variable (X − μ)² at the level k²σ². The squaring is what turns 1/a into 1/k², and it is also why a variance rather than a mean is required."),
  (True, "True: mass 1/(2k²) at each of μ ± kσ with the rest at μ. Verified at k = 2 and 3, where the variance comes to exactly 1.000000 and the tail probability exactly 1/k². So no smaller bound could be true for every distribution with a finite variance."),
  (False, "False — it requires X ≥ 0. The proof uses X ≥ a·1{X ≥ a}, which fails if X can be negative, and the conclusion is then simply untrue."))))

I.append(q(13, "numeric", "moderate",
 "X has mean 100 and standard deviation 10. Chebyshev's bound on P(|X − 100| ≥ 25) is:",
 ["0.16", "0.04", "0.4", "0.25"],
 "A",
 "The deviation is 25/10 = 2.5 standard deviations, so k = 2.5 and the bound is 1/6.25 = 0.16. Option D would be the bound at k = 2, which is the error of not dividing by σ.",
 check="For a normal the true probability at k = 2.5 is 0.012419, so the bound is about thirteen times too large — but it needs no distributional assumption."))

I.append(q(14, "single", "moderate",
 "Which distribution attains Chebyshev's bound at a given k?",
 ["mass 1/(2k²) at each of μ ± kσ, the remainder at μ",
  "the normal", "the exponential", "none — the bound is never attained"],
 "A",
 "Its variance is 2 × (1/(2k²)) × (kσ)² = σ² as required, and P(|X − μ| ≥ kσ) = 2/(2k²) = 1/k² exactly. Verified at k = 2, where the masses are 0.125, 0.75, 0.125, and at k = 3. Because this distribution satisfies the inequality's only assumption, no smaller bound is possible."))

I.append(q(15, "single", "moderate",
 "Why is Chebyshev's inequality so loose for a normal distribution?",
 ["it is distribution-free, so its value is set by the worst case rather than by the normal",
  "the normal has no finite variance",
  "it applies only to discrete distributions",
  "the inequality is incorrectly stated in most textbooks"],
 "A",
 "The bound must hold for every distribution with a finite variance, including the three-point one that attains it, so it cannot be tighter. For a normal the ratio of truth to bound falls from 0.317 at k = 1 to 0.182 at k = 2 and 0.024 at k = 3 — the slack grows, because the bound decays as 1/k² while a normal tail decays like e^(−k²/2)."))

I.append(q(16, "numeric", "moderate",
 "Var(X) = 9 and Var(Y) = 16. Cauchy–Schwarz bounds |Cov(X,Y)| by:",
 ["12", "25", "144", "7"],
 "A",
 "Cov² ≤ Var(X)Var(Y) = 144, so |Cov| ≤ 12. Equality holds only when Y is a linear function of X, and dividing through gives |ρ| = |Cov|/12 ≤ 1 — the familiar statement.",
 check="Option C is the product of the variances, which bounds the SQUARE of the covariance, not the covariance itself."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider finer points about these bounds.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true — the density is positive at 0 and the integral diverges. B is true: Cantelli gives 1/(1+k²) = 0.2 at k = 2. C is true, and it shows Markov's weakness lay in the choice of function. D is false — at k = 1 the bound is 1, which is vacuous.",
 statements=["E(1/X) is infinite for an Exponential(1) variable.",
             "For a one-sided tail, Cantelli's bound 1/(1 + k²) improves on Chebyshev.",
             "Markov applied to e^(tX) gives an exponentially small bound.",
             "Chebyshev's inequality is informative at k = 1."],
 verdicts=verd(
  (True, "True. The density of Exponential(1) is 1 at the origin, so ∫(1/x)e^(−x)dx diverges there. Jensen still holds with an infinite left side, but a simulation drifts upward with n — roughly 15 at a million draws and 40 at ten million."),
  (True, "True: at k = 2 Cantelli gives 0.2 against the 0.25 that halving the two-sided bound would suggest. The improvement comes from using the one-sidedness, so a two-sided bound should never simply be halved."),
  (True, "True — that is the Chernoff bound, P(X ≥ a) ≤ E(e^(tX))/e^(ta) optimised over t. It shows the looseness of Markov came from applying it to X rather than to a rapidly growing function of X."),
  (False, "False. At k = 1 the bound is 1/1 = 1, and since every probability is at most 1 the inequality says nothing whatever. It becomes informative only beyond one standard deviation."))))

I.append(q(18, "single", "hard",
 "Let X be non-negative with distribution function F. Which set of statements is correct? A. ∫₀^∞ 2x[1 − F(x)]dx = E(X²). B. ∫₀^∞ [1 − F(x)]dx = E(X). C. E(1/X) ≤ 1/E(X). D. E(log X) ≤ log E(X).",
 ["A, B and D", "A, B and C", "B, C and D", "C and D"],
 "A",
 "A and B are the tail identities, both verified by quadrature on three distributions. D is true because log is concave. C is FALSE: 1/x is convex, so Jensen gives E(1/X) ≥ 1/E(X) — on Uniform(1,3) the two sides are 0.549306 and 0.5. This is the June 2026 question, and its difficulty is that C and D have identical written form and differ only in the curvature of the function."))

I.append(q(19, "numeric", "hard",
 "For X ~ Exponential(1), compare Markov's bound at a = 3 with the true probability.",
 ["bound 0.3333 against a truth of 0.0498, a factor of 6.7",
  "bound 0.0498 against a truth of 0.3333",
  "bound and truth both 0.3333",
  "bound 0.3333 against a truth of 0.3333"],
 "A",
 "The bound is E(X)/a = 1/3 = 0.333333 and the truth is e^(−3) = 0.049787. The gap widens further out: at a = 5 the bound is 0.2 against 0.006738, a factor of 30, because Markov's bound decays as 1/a while an exponential tail decays geometrically.",
 check="Markov's bound must always be at least the true probability, so the larger of the two numbers has to be the bound."))

I.append(q(20, "single", "hard",
 "Chebyshev's inequality is loose, yet it proves the weak law of large numbers. Why is the looseness not a problem there?",
 ["because the bound σ²/(nε²) tends to zero whatever the constant, so only the limit matters",
  "because the sample mean is normally distributed",
  "because the bound becomes tight as n grows",
  "because the weak law does not require an inequality"],
 "A",
 "Applied to X̄ₙ, Chebyshev gives P(|X̄ₙ − μ| ≥ ε) ≤ σ²/(nε²), and a loose constant multiplying 1/n still goes to zero. That is the clearest case of a slack bound being entirely adequate: the inequality is a tool for proving asymptotic statements, not for computing probabilities that could be computed exactly."))

LET = "ABCD"
WANT = {"pr-t7-m-01": "C", "pr-t7-m-02": "B", "pr-t7-m-03": "D",
        "pr-t7-m-04": "C", "pr-t7-m-05": "B", "pr-t7-m-06": "D",
        "pr-t7-m-07": "C", "pr-t7-m-08": "B", "pr-t7-m-09": "D",
        "pr-t7-m-10": "C", "pr-t7-m-11": "B", "pr-t7-m-13": "D",
        "pr-t7-m-14": "C", "pr-t7-m-15": "B", "pr-t7-m-16": "D",
        "pr-t7-m-18": "C", "pr-t7-m-19": "B", "pr-t7-m-20": "D"}


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
 "moduleId": "probability", "topicId": "probability-t7", "source": "mastery",
 "label": "Jensen, Markov, Chebyshev and Cauchy–Schwarz — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
