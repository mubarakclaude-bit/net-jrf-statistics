#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 1.10 — Transformations and Jacobians (probability-t10).

PYQ anchor. June 2026 Q25 (WRONG, marked D against answer C): X and Y independent exponential(λ);
the conditional distribution of X given X + Y = 2.
    f(x | X+Y = s) = f(x, s-x)/f_{X+Y}(s) = λ²e^(−λs) / (λ²s e^(−λs)) = 1/s  on 0 < x < s,
so X | X+Y = s ~ Uniform(0, s), and at s = 2 that is Uniform(0, 2) — option C. The marked option
Gamma(2, λ) is the distribution of the SUM, not of X given the sum.

The result is striking and worth the lesson: the λ cancels completely, so the answer does not
depend on the rate at all. Verified by simulation (5,397 draws conditioned near X+Y = 2: mean
1.0051 against 1, sd 0.5772 against 2/sqrt(12) = 0.5774, KS p = 0.230).

Nine variants, all taught in named sections and pooled. One of them is the Poisson interarrival
item retagged into Q25 from the maths file earlier in this project; it belongs here, since
memorylessness is what makes the conditional uniform.

Introduces the `gamma-sum` visualisation, written for this lesson and reusable for 1.6 and 1.9.

Writes seed/lesson_pr10.json and seed/probability_t10_mastery.json.
"""
import json, io, os, re

OUT = "seed/lesson_pr10.json"
POOL = "seed/probability_t10_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 7,
 "title": "Before the lesson — four things it will assume",
 "objective": "Fix the exponential's basic facts and the mechanics of changing variables.",
 "ask": {
  "q": "You know the joint density of (X, Y) and you want the density of X + Y. What is the obstacle?",
  "nudge": "A density is a function of as many variables as you have. One sum is one variable — what happened to the other?"},
 "body": [
  "This topic asks for the distribution of something built out of other random variables: a sum, a ratio, a minimum, a scaling. There are three standard routes and the lesson uses all three.",
  "The cdf route works directly on P(g(X) ≤ t) and is best for minima and maxima. The Jacobian route changes variables in the joint density and is the general method. The third route is the one June 2026 used: write a CONDITIONAL density as a ratio, which is a change of variables in disguise.",
  "The obstacle in the question above is that a single sum is one variable where there were two, so you cannot change variables with it alone. The fix is to introduce a second, convenient variable — here U = X and V = X + Y — transform, and then integrate out or condition on whichever one is not wanted.",
  "Four checks before starting."],
 "items": [
  {"ask": "For an exponential with rate λ, give the density, the cdf and the mean.",
   "recall": "f(x) = λe^(−λx) for x ≥ 0; F(x) = 1 − e^(−λx); mean 1/λ, variance 1/λ².",
   "refresh": [
    "Mind the parameterisation: 'rate λ' gives mean 1/λ, while 'mean θ' gives density (1/θ)e^(−x/θ). Exam options usually make clear which, and the mean distinguishes them.",
    "The survival function e^(−λx) is the useful form, because every minimum and every memorylessness calculation is a product of survival probabilities.",
    "Two independent exponentials have joint density λ²e^(−λ(x+y)), which depends on x and y only through their SUM — the single fact behind this whole lesson."]},
  {"ask": "What is the distribution of the sum of n independent exponential(λ) variables?",
   "recall": "Gamma(n, λ), with mean n/λ and variance n/λ².",
   "refresh": [
    "The Gamma's shape parameter counts how many exponentials went in, which is why waiting for the nᵗʰ event of a Poisson process is Gamma-distributed.",
    "Checked by simulation at λ = 1.5: for n = 1, 2, 5, 10 the sample means were 0.667, 1.336, 3.329, 6.671 against the exact 0.667, 1.333, 3.333, 6.667.",
    "A practice variant asks this directly, with 'exponential(nλ)' as the trap — that is the MINIMUM, not the sum."]},
  {"ask": "State the Jacobian method for a change of variables.",
   "recall": "If (U, V) = g(X, Y) is one-to-one, then f(u,v) = f(x,y) · |∂(x,y)/∂(u,v)|, with x and y written in terms of u and v.",
   "refresh": [
    "The Jacobian determinant is the local area-scaling factor. It appears because a density is a per-unit-area quantity, so stretching the plane dilutes it.",
    "For the transformation used throughout this lesson, U = X and V = X + Y, the inverse is x = u, y = v − u, and the Jacobian determinant is the determinant of [[1, 0], [−1, 1]], which is 1. So the joint density transfers unchanged — the reason the algebra stays clean.",
    "The method needs the map to be one-to-one on the region of interest; otherwise split the region into pieces where it is."]},
  {"ask": "Which continuous distribution is memoryless, and what does that mean?",
   "recall": "The exponential, uniquely: P(T > s + t | T > s) = P(T > t).",
   "refresh": [
    "For a Poisson process with rate 2 per minute, P(T > 6 | T > 4) = P(T > 2) = e^(−4) = 0.018316 — a practice variant. The elapsed four minutes are simply forgotten.",
    "Equivalently the hazard rate is constant. Lesson 1.5 showed the geometric is the discrete counterpart and the only discrete law with the property.",
    "Memorylessness is what makes this lesson's central result work: because the exponential has no memory, knowing the TOTAL X + Y tells you nothing about which part of it X occupies, so X is uniform across it."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Knowing the total says nothing about the split",
 "objective": "See why the conditional distribution comes out flat, before the algebra.",
 "body": [
  "Two independent exponential waiting times add to 2 minutes. Where in that interval did the first one end?",
  "The answer is: anywhere, with equal probability. The conditional distribution of X given X + Y = 2 is Uniform(0, 2), so the first waiting time is as likely to have taken 0.1 minutes as 1.0 or 1.9. The intuition that it 'should' be concentrated near the middle, or near zero, is simply wrong.",
  "The reason is visible in the joint density. Two independent exponentials have joint density λ²e^(−λ(x+y)), which depends on x and y ONLY through their sum. So along the line x + y = 2 the density is constant, and conditioning on that line produces a flat distribution. No calculation is needed to see it — only the observation that the joint density is a function of the sum alone.",
  "Notice what cancels: the rate λ disappears entirely. A fast process and a slow one give the same answer, because conditioning on the total has already absorbed everything the rate controls. That is the kind of result worth remembering as a fact rather than re-deriving under exam pressure."],
 "scenario": {
  "teaser": "A fault is known to have occurred during a two-hour window, and an engineer searches the middle first.",
  "title": "Where in the interval did it happen?",
  "body": [
   "A monitoring system records that exactly one fault occurred during a two-hour window but not when. An engineer, reasoning that faults 'tend to cluster around the middle of a period', begins examining logs from the central portion.",
   "If faults arrive as a Poisson process, that reasoning is wrong in a specific and useful way: given that exactly one event occurred in an interval, its time is UNIFORM over that interval. There is no central tendency to exploit, and the first and last minutes are as likely as any other.",
   "This is the same fact as the lesson's main result, seen from the other side. The waiting time to the fault and the waiting time from the fault to the end of the window are the two exponential pieces, and conditioning on their total being two hours makes the split uniform.",
   "The practical consequence is a change of search strategy rather than a correction to it. With no informative prior over position, the efficient approach is a systematic sweep or a bisection of the log, not a guess at the middle. And if the search is costly, the expected cost is the same wherever one starts — which is itself worth knowing, because it means effort should go into making each check cheaper rather than into choosing where to begin.",
   "The result also generalises in a way worth carrying: given that exactly k events occurred in an interval, their times behave like k independent uniform draws on that interval, sorted. So with three faults in the window, their positions are the order statistics of three uniforms — which is lesson 1.1's material, and gives expected positions at 1/4, 1/2 and 3/4 of the way through.",
   "What makes all of this work is memorylessness. A process with wear-out, where faults become more likely as equipment ages, would NOT give a uniform position, and the engineer's instinct could then be right. The uniformity is a consequence of the exponential assumption, not a general truth about intervals."],
  "q": "Why does the engineer's search strategy gain nothing from guessing the middle?",
  "answer": "Because for a Poisson process, given that exactly one event occurred in an interval, its position is uniform over that interval — every moment is equally likely, so there is no region of higher probability to search first. This follows from the same conditioning that makes X | X + Y = s uniform on (0, s): the joint density of the two exponential pieces depends only on their sum, so it is constant along the line where the sum is fixed. The instinct would only be right for a process whose hazard rises with time, which an exponential's by definition does not."},
 "ask": {
  "q": "The rate λ cancelled out of the answer entirely. What does that tell you about how much the conditional distribution depends on how fast the process runs?",
  "nudge": "If you were told the total was 2 minutes, would knowing whether the process is fast or slow change where the split fell?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Watch exponentials add up to a Gamma",
 "objective": "See the shape parameter count the exponentials, and the normal appear.",
 "viz": {"type": "gamma-sum", "n": 1, "lam": 1.5,
         "caption": "The density of a sum of n independent exponential(λ) variables, which is Gamma(n, λ), with a normal curve of the same mean and variance shown from n = 2 onwards."},
 "body": [
  "Start at n = 1. The sum of one exponential is that exponential: the density is highest at zero and decays, with skewness 2 and no interior peak.",
  "Step to n = 2 — the case June 2026's question uses. A peak appears away from the origin, and the density at zero drops to zero. Gamma(2, λ) is the distribution of X + Y, which is what the marked answer gave; the question asked for X GIVEN that sum, which is a different object entirely.",
  "Keep raising n and watch two things at once. The mean n/λ and the variance n/λ² both grow linearly, so the curve slides right and widens — but the RELATIVE spread sd/mean = 1/√n shrinks, which is why the shape tightens in proportion.",
  "The skewness readout is 2/√n: 2 at n = 1, 1.41 at n = 2, 0.89 at n = 5, 0.63 at n = 10, 0.37 at n = 30. The teal normal curve converges on the Gamma at exactly that rate — the central limit theorem arriving, with its speed shown on a slider.",
  "Change λ at fixed n and note what does NOT change: the skewness. The rate rescales the horizontal axis and nothing else, because λ is a scale parameter. Only the shape parameter n changes the shape."],
 "ask": {
  "q": "The skewness is 2/√n regardless of λ. Why does changing the rate leave the shape untouched?",
  "nudge": "If S ~ Gamma(n, λ), what is the distribution of λS? Which parameter survives that rescaling?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "Three routes, and the transformation that does the work",
 "objective": "Know the general method and the specific one this topic keeps using.",
 "blocks": [
  {"t": "formula", "h": "Route one: the cdf method",
   "body": "For a single function of several variables, work on the cdf directly.\n    P(min > t) = P(all > t) = ∏P(Xᵢ > t) = e^(−nλt)  for iid exponential(λ),\nso the minimum is exponential with rate nλ and mean 1/(nλ) — a practice variant, and the trap is to answer exponential(λ/n). Simulated at λ = 1.5: the minimum of 3 had mean 0.2217 against the exact 0.2222, and of 7 had 0.0952 against 0.0952."},
  {"t": "formula", "h": "Route two: the Jacobian method",
   "body": "For a one-to-one map (U, V) = g(X, Y):\n    f_{U,V}(u,v) = f_{X,Y}(x, y) · |∂(x,y)/∂(u,v)|,\nwith x and y expressed through u and v. Then integrate out whichever variable is not wanted. The Jacobian is the area-scaling factor, and it appears because densities are per-unit-area."},
  {"t": "step", "h": "The transformation this topic uses",
   "body": "Take U = X and V = X + Y. The inverse is x = u, y = v − u, and\n    ∂(x,y)/∂(u,v) = det [[1, 0], [−1, 1]] = 1.\nSo the joint density carries over unchanged:\n    f_{U,V}(u, v) = λ²e^(−λv)  on 0 < u < v.\nNotice that it does not involve u at all. That single observation is the whole of June 2026's question: for fixed v, the density is flat in u."},
  {"t": "formula", "h": "Route three: the conditional density as a ratio",
   "body": "f(x | X + Y = s) = f_{X,Y}(x, s − x) / f_{X+Y}(s).\nWith two independent exponentials the numerator is λ²e^(−λs) and the denominator is the Gamma(2, λ) density s λ²e^(−λs), so the ratio is 1/s on 0 < x < s:\n    X | X + Y = s  ~  Uniform(0, s),  and  E(X | X + Y = s) = s/2.\nBoth the result and that expectation are practice variants."},
  {"t": "def", "h": "The exponential–Gamma facts worth knowing cold",
   "body": "Sum of n iid exponential(λ)  → Gamma(n, λ), mean n/λ, variance n/λ².\nMinimum of n iid exponential(λ) → exponential(nλ), mean 1/(nλ).\nX/(X + Y) for two iid           → Uniform(0, 1), the scale-free version of the main result.\n2λX for one exponential(λ)      → χ² with 2 degrees of freedom.\nThe last is a scaling: λX ~ exponential(1) = Gamma(1, 1), and doubling gives Gamma(1, scale 2) = χ²₂. Confirmed by simulation: mean 1.998 and variance 4.005 against the χ²₂ values 2 and 4, with KS p = 0.101."},
  {"t": "step", "h": "Choosing a route",
   "body": "Minimum or maximum → cdf method, one line. A conditional given a sum → the ratio, also one line. Anything else, or a genuinely two-dimensional answer → the Jacobian. The Jacobian is the general tool and the other two are shortcuts worth having, because an exam question on a minimum should not take a page."}],
 "table": {
  "caption": "The exponential family's standard transformations. Every entry was checked against a 600,000-draw simulation.",
  "head": ["construction", "result", "mean", "note"],
  "rows": [
   ["X₁ + ⋯ + Xₙ", "Gamma(n, λ)", "n/λ", "shape counts the exponentials"],
   ["min(X₁, …, Xₙ)", "exponential(nλ)", "1/(nλ)", "rate multiplies, not divides"],
   ["X | X + Y = s", "Uniform(0, s)", "s/2", "λ cancels entirely"],
   ["X/(X + Y)", "Uniform(0, 1)", "1/2", "the same fact, rescaled"],
   ["2λX", "χ² with 2 df", "2", "a pure scaling"],
   ["T | T > s  (shifted)", "exponential(λ)", "1/λ", "memorylessness"]]},
 "flow": {
  "title": "Which route for which transformation",
  "alt": "Flow chart for choosing a method to find the distribution of a transformed variable",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "A function of several variables", "kind": "start"},
   {"id": "b", "r": 1, "c": 0, "label": "A minimum or maximum?", "kind": "dec"},
   {"id": "c", "r": 1, "c": 2, "label": "A conditional given a sum?", "kind": "dec"},
   {"id": "d", "r": 2, "c": 0, "label": "cdf method: products of survivals", "kind": "end"},
   {"id": "e", "r": 2, "c": 2, "label": "ratio f(x, s−x)/f_sum(s)", "kind": "end"},
   {"id": "f", "r": 3, "c": 1, "label": "Otherwise: Jacobian, then integrate out", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "a", "to": "c"},
   {"from": "b", "to": "d"}, {"from": "c", "to": "e"},
   {"from": "b", "to": "f"}, {"from": "c", "to": "f"}],
  "note": "The Jacobian always works. The other two are one-line shortcuts for the two cases that come up most, and recognising them is most of the speed in this topic."},
 "ask": {
  "q": "The transformed joint density λ²e^(−λv) does not involve u at all. Which of this lesson's results follow from that one observation?",
  "nudge": "A density that is constant in u, on the region 0 < u < v, is what kind of distribution for u given v?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — June 2026, Q25",
 "objective": "Derive the conditional distribution and see why the rate disappears.",
 "ask": {
  "q": "The answer Uniform(0, 2) contains no λ. Where did it cancel?",
  "nudge": "Write out the numerator and the denominator of the ratio and compare their exponential factors."},
 "problem": "Let X and Y be independent, each exponential with parameter λ. Find the conditional distribution of X given X + Y = 2.",
 "steps": [
  {"say": "Write the joint density and notice its structure.",
   "math": "f(x, y) = λe^(−λx) · λe^(−λy) = λ² e^(−λ(x+y)),  x, y > 0",
   "why": "It depends on x and y only through their SUM. So along any line x + y = constant the density is constant — which already tells you the answer before any division."},
  {"say": "Get the density of the sum.",
   "math": "X + Y ~ Gamma(2, λ)\nf_{X+Y}(s) = λ² s e^(−λs),  s > 0",
   "why": "The sum of two independent exponential(λ) variables is Gamma(2, λ). This is the distribution the marked answer gave — correct for X + Y, but the question asked about X."},
  {"say": "Form the conditional density as a ratio.",
   "math": "f(x | X + Y = s) = f(x, s − x) / f_{X+Y}(s)\n                 = λ² e^(−λs) / (λ² s e^(−λs))\n                 = 1/s,     for 0 < x < s",
   "why": "Both λ² factors cancel and both e^(−λs) factors cancel — answering the question above. What is left is 1/s, a constant in x, which is the density of a uniform distribution on (0, s)."},
  {"say": "Name the distribution and substitute s = 2.",
   "math": "X | X + Y = s  ~  Uniform(0, s)\nat s = 2:  Uniform(0, 2)\n⟹ option C",
   "why": "Option D, Gamma(2, λ), is the sum's distribution; option A is an exponential, which has unbounded support and so cannot be right for a variable confined to (0, 2); option B is a Beta with the parameters misused."},
  {"say": "Check it against a simulation.",
   "math": "600,000 pairs at λ = 1.5, keeping those with |X+Y − 2| < 0.02 (5,397 draws)\nsample mean 1.0051   (Uniform(0,2) mean 1)\nsample sd   0.5772   (2/√12 = 0.5774)\ndeciles 0.207, 0.499, 1.009, 1.511, 1.792 against 0.2, 0.5, 1.0, 1.5, 1.8\nKolmogorov–Smirnov p = 0.230",
   "why": "Flat across the whole interval, not merely right on average — the quantiles match throughout. A mean of 1 alone would also be consistent with a symmetric distribution peaked at the centre, so the quantiles are the check that matters."}],
 "after": "Two things to carry. The joint density of independent exponentials depends only on the sum, which makes every conditional-given-the-sum question in this family uniform. And the answer has no λ in it, which is worth noticing as a check: if your answer to a 'given the total' question still contains the rate, something has not cancelled that should have."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the main results before the variations.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "What is the conditional distribution of X given X + Y = s, for iid exponentials?",
   "a": "Uniform(0, s), with mean s/2. The rate λ cancels."},
  {"q": "What is the distribution of the sum of n iid exponential(λ)?",
   "a": "Gamma(n, λ), with mean n/λ and variance n/λ²."},
  {"q": "And the minimum of n iid exponential(λ)?",
   "a": "Exponential with rate nλ, so mean 1/(nλ)."},
  {"q": "What is the Jacobian of the map (x, y) → (u, v) = (x, x + y)?",
   "a": "1 — so the joint density transfers unchanged."},
  {"q": "What is the distribution of X/(X + Y) for two iid exponentials?",
   "a": "Uniform(0, 1)."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — three transformations of the same pair",
 "objective": "Apply the three routes to the same exponential pair.",
 "problem": "X and Y are independent exponential(λ). Work out three more facts about them.",
 "steps": [
  {"say": "First the ratio.",
   "blank": {"prompt": "Give the distribution of X/(X + Y).",
             "answer": "Uniform(0, 1)",
             "accept": ["uniform(0,1)", "U(0,1)", "standard uniform"],
             "hint": "You know X | X+Y = s is Uniform(0, s). What does dividing by s do?"},
   "why": "Given X + Y = s, X is Uniform(0, s), so X/s is Uniform(0, 1) — and that holds for EVERY s, so the unconditional distribution of X/(X+Y) is Uniform(0,1) too. Simulated: mean 0.49992 against 0.5, variance 0.08341 against 1/12 = 0.08333, KS p = 0.890."},
  {"say": "Now the conditional expectation.",
   "blank": {"prompt": "Give E(X | X + Y = s).",
             "answer": "s/2",
             "accept": ["s/2", "half of s", "0.5s"],
             "hint": "The mean of a uniform distribution on (0, s)."},
   "why": "s/2, by symmetry of the uniform. The traps offered in the variant are s, 1/λ and s/λ — note that the correct answer contains no λ, consistent with the cancellation in section 5. This is also what the tower property demands: E(E(X | X+Y)) = E((X+Y)/2) = (2/λ)/2 = 1/λ = E(X) ✓."},
  {"say": "Now a pure scaling.",
   "blank": {"prompt": "If X ~ exponential(λ), what is the distribution of 2λX?",
             "answer": "chi-square with 2 degrees of freedom",
             "accept": ["chi-square with 2 df", "χ²₂", "chi2_2"],
             "hint": "First find the distribution of λX, then of twice that."},
   "why": "λX ~ exponential(1) = Gamma(1, 1), and multiplying by 2 gives Gamma(shape 1, scale 2), which is exactly χ² with 2 degrees of freedom. Simulated: mean 1.9984 and variance 4.0045 against the χ²₂ values 2 and 4, KS p = 0.101."},
  {"say": "Finally the minimum, by the cdf route.",
   "blank": {"prompt": "Give the distribution of min(X₁, …, Xₙ) for iid exponential(λ).",
             "answer": "exponential with rate nλ, mean 1/(nλ)",
             "accept": ["exponential(n lambda)", "exp(nλ)", "rate n lambda"],
             "hint": "P(min > t) = P(all > t), and each survival is e^(−λt)."},
   "why": "P(min > t) = (e^(−λt))ⁿ = e^(−nλt), which is the survival function of an exponential with rate nλ. The trap is exponential(λ/n), which would make the minimum SLOWER than one component — the opposite of the truth. Simulated at λ = 1.5: mean 0.2217 for n = 3 against 0.2222."}],
 "after": "Notice that three of the four were one line each, once the right route was chosen: the ratio followed from the conditional, the expectation from the uniform's symmetry, and the minimum from a product of survival functions. Only the scaling needed any manipulation, and that was a change of units. The Jacobian machinery is the fallback, not the first move."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "Conditioning on a total, in three families",
 "objective": "See the same structure in Poisson counts and binomial counts.",
 "blocks": [
  {"t": "step", "h": "The pattern",
   "body": "Conditioning on a total removes the scale of the process and leaves only the proportions. It happened in the exponential case — the rate λ cancelled — and it happens for counts too, where the rates or probabilities cancel and leave a distribution governed purely by relative sizes."},
  {"t": "formula", "h": "Poisson counts given their total: binomial",
   "body": "If N₁ ~ Poisson(μ₁) and N₂ ~ Poisson(μ₂) are independent, then\n    N₁ | N₁ + N₂ = k  ~  Binomial(k, μ₁/(μ₁ + μ₂)).\nFor Poisson processes with rates λ and 2λ the proportion is λ/(3λ) = 1/3 — the λ cancels. So with k = 4,\n    P(N₁ = 1 | total = 4) = C(4,1)(1/3)(2/3)³ = 32/81 = 0.39506,\na practice variant. Simulated over 101,098 qualifying draws: 0.39459."},
  {"t": "formula", "h": "Binomial counts given their total: hypergeometric",
   "body": "If X ~ Binomial(m, p) and Y ~ Binomial(n, p) are independent with the SAME p, then\n    X | X + Y = k  ~  Hypergeometric(m + n, m, k),\nso P(X = j) = C(m,j)C(n,k−j)/C(m+n,k) — free of p entirely. A practice variant asks exactly this. Checked at m = 6, n = 4, k = 3: the empirical probabilities 0.0327, 0.3003, 0.4991, 0.1680 against the exact 0.0333, 0.3000, 0.5000, 0.1667."},
  {"t": "def", "h": "Why p and λ always cancel",
   "body": "In each case the conditional probability is a ratio in which the parameter appears to the same power in numerator and denominator. That is not a coincidence: conditioning on the total fixes the quantity the parameter controls, so nothing is left for it to influence. It is also why these conditional distributions are the basis of EXACT tests — Fisher's exact test is precisely the hypergeometric conditional above, and it needs no estimate of p."},
  {"t": "step", "h": "And the uniform case again",
   "body": "The continuous analogue of the Poisson result is the one from section 5: given that exactly one event of a Poisson process occurred in an interval, its position is uniform over the interval. Given that k occurred, their positions behave like k independent uniforms, sorted — which is the order statistics of lesson 1.1, with expected positions at j/(k+1)."}],
 "ask": {
  "q": "Fisher's exact test uses the hypergeometric conditional distribution. Why is it an advantage that p cancels?",
  "nudge": "What would you otherwise have to do about an unknown nuisance parameter before computing a p-value?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — splitting a Poisson stream",
 "objective": "Apply the conditioning result to counts, with numbers.",
 "problem": "Two independent Poisson processes have rates λ and 2λ. (a) Given that 4 events occurred in total, name the conditional distribution of the number from the first process. (b) Find P(N₁ = 1 | N₁ + N₂ = 4). (c) Find E(N₁ | N₁ + N₂ = 4). (d) Does any of this depend on λ, or on the length of the observation period?",
 "hints": [
  "For (a), the conditional distribution is binomial with the proportion of the total rate.",
  "For (b), use the binomial pmf with that proportion.",
  "For (d), write the proportion in terms of λ and simplify."],
 "answer": "(a) Binomial(4, 1/3). (b) 32/81 = 0.39506. (c) 4/3. (d) No — λ and the period both cancel out of the proportion.",
 "check": "Part (d) is the point of the exercise. The proportion is λt/(λt + 2λt) = 1/3 whatever λ and whatever t, so the answer depends only on the RATIO of the rates. That is why conditioning on a total is such a useful device: it eliminates the nuisance parameter. Simulated over 101,098 qualifying draws, P(N₁ = 1 | total = 4) came to 0.39459 against the exact 0.39506.",
 "scenario": {
  "teaser": "Two call centres share a queue and a manager wants to know each one's share of a busy hour.",
  "title": "Conditioning away the thing you do not know",
  "body": [
   "Two support teams handle calls from a common stream. Team A handles roughly half as many as Team B, and in a given hour 4 calls arrived in total. The manager wants the probability that exactly one of them went to Team A.",
   "The arrival rate is not known — it varies by day, by season and by how the product is behaving — and estimating it would need historical data the manager does not have to hand. It turns out not to matter.",
   "Modelling the two streams as independent Poisson processes with rates λ and 2λ, the conditional distribution of Team A's count given the total of 4 is Binomial(4, 1/3). The λ cancels, because conditioning on the total has already fixed the only thing λ governs: how many calls there were. What remains is purely the split, and the split depends only on the ratio of the rates.",
   "So P(exactly one to Team A) = C(4,1)(1/3)(2/3)³ = 32/81 ≈ 0.395, and the expected count is 4/3. Neither figure requires knowing the arrival rate or even the length of the observation window.",
   "This is the same device that makes several exact tests work. Fisher's exact test conditions on the margins of a 2×2 table precisely so that the unknown common success probability drops out, leaving a hypergeometric calculation that needs no estimate. Conditioning on a sufficient statistic for the nuisance parameter is the general principle, and lesson 4.1's material is where it comes from.",
   "The caution is that the RATIO still has to be known or assumed. Here 'A handles half as many as B' supplied it. Had the manager known only that the two teams differ, nothing could be computed — conditioning removes one unknown, not all of them."],
  "q": "Why can this be answered without knowing the arrival rate, and what would still have to be known?",
  "answer": "Because conditioning on the total of 4 fixes the quantity the rate controls — how many calls arrived — so the rate has nothing left to influence and cancels from the conditional distribution. What survives is the proportion λ/(λ + 2λ) = 1/3, which depends only on the RATIO of the two rates, not on their size or on the length of the window. So the ratio is exactly what must still be known: the statement that Team A handles half as many as Team B supplies it, and without some such assumption the split would be uncomputable. This is the same reason Fisher's exact test conditions on the margins — to eliminate a nuisance parameter while retaining what the question needs."},
 "solution": [
  {"say": "(a) The conditional distribution.",
   "math": "N₁ ~ Poisson(λt), N₂ ~ Poisson(2λt), independent\nN₁ | N₁ + N₂ = k ~ Binomial(k, λt/(λt + 2λt)) = Binomial(k, 1/3)\nwith k = 4:  Binomial(4, 1/3)",
   "why": "The standard result for splitting a Poisson total. The proportion is the first rate over the total rate."},
  {"say": "(b) The probability.",
   "math": "P(N₁ = 1) = C(4,1)(1/3)¹(2/3)³\n          = 4 × (1/3) × (8/27) = 32/81 = 0.395062",
   "why": "Simulated over 101,098 qualifying draws as 0.39459 — agreement to three decimals."},
  {"say": "(c) The conditional expectation.",
   "math": "E = k p = 4 × (1/3) = 4/3 ≈ 1.333",
   "why": "The binomial mean. Sensible: of four calls, the team taking a third of the traffic should get about 1.3 of them."},
  {"say": "(d) What the answer depends on.",
   "math": "proportion = λt/(λt + 2λt) = 1/3\nλ cancels; t cancels",
   "why": "No dependence on the rate or the period — only on the RATIO 1:2. That is the device: conditioning on the total eliminates the nuisance parameter, which is exactly why exact tests condition on margins."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims the variants on this topic are built from.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "For iid exponentials, X | X + Y = s is Uniform(0, s).",
   "tf": True,
   "why": "True, and the rate cancels completely. The joint density λ²e^(−λ(x+y)) depends on x and y only through the sum, so it is constant along any line of fixed sum. Verified by simulation: KS p = 0.230 against Uniform(0,2)."},
  {"claim": "The sum of n iid exponential(λ) variables is exponential with rate nλ.",
   "tf": False,
   "why": "False — that is the MINIMUM. The sum is Gamma(n, λ) with mean n/λ, which GROWS with n, whereas exponential(nλ) has mean 1/(nλ), which shrinks. The two results are easy to swap and point in opposite directions."},
  {"claim": "The minimum of n iid exponential(λ) is exponential with rate nλ.",
   "tf": True,
   "why": "True. P(min > t) = (e^(−λt))ⁿ = e^(−nλt). The rate multiplies by n, so the minimum arrives n times sooner on average — mean 1/(nλ). Answering exponential(λ/n) makes it slower, which is the wrong direction."},
  {"claim": "X/(X + Y) for two iid exponentials is Uniform(0, 1).",
   "tf": True,
   "why": "True, and it follows from the main result: given X + Y = s, X is Uniform(0, s), so X/s is Uniform(0,1) for every s. Simulated mean 0.49992 and variance 0.08341 against 0.5 and 1/12."},
  {"claim": "If X ~ Binomial(m, p) and Y ~ Binomial(n, p) independently, then X | X + Y = k is binomial.",
   "tf": False,
   "why": "False — it is HYPERGEOMETRIC, with P(X = j) = C(m,j)C(n,k−j)/C(m+n,k), free of p. Conditioning on the total makes the problem one of drawing k items without replacement from m + n. This is the distribution behind Fisher's exact test."},
  {"claim": "E(X | X + Y = s) equals 1/λ for iid exponentials.",
   "tf": False,
   "why": "False: it is s/2. 1/λ is the UNCONDITIONAL mean E(X). The conditional expectation must depend on s — it is half of whatever total was observed — and containing λ would contradict the cancellation that makes the conditional uniform."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 8,
 "title": "On your own — six quick ones",
 "objective": "Apply the standard transformations at speed.",
 "problem": "Let X, Y, X₁, …, Xₙ be independent exponential(λ). Give: (a) the distribution of X + Y; (b) the distribution of min(X₁, …, X₅) and its mean when λ = 2; (c) E(X | X + Y = 6); (d) the distribution of 2λX; (e) P(T > 6 | T > 4) for T exponential with rate 2; (f) the Jacobian of (x, y) → (x, x + y).",
 "hints": [
  "For (b), the rate multiplies by the number of variables.",
  "For (c), the conditional is uniform on the interval.",
  "For (e), use memorylessness rather than integrating."],
 "answer": "(a) Gamma(2, λ). (b) Exponential(5λ) = exponential(10), mean 0.1. (c) 3. (d) χ² with 2 df. (e) e^(−4) = 0.018316. (f) 1.",
 "check": "Part (e) is worth doing carefully. Memorylessness gives P(T > 6 | T > 4) = P(T > 2) = e^(−2×2) = e^(−4) = 0.018316. Note the rate is 2, so the exponent is 2 × 2 = 4, not 2 — and the answer is NOT e^(−6) or e^(−2). A direct simulation of this is a poor check: with 600,000 draws only 205 exceed 4, so the conditional estimate has an enormous standard error. Simulating the SHIFTED variable instead, over four million draws, gave 0.018388 against the exact 0.018316.",
 "solution": [
  {"say": "(a) The sum of two.",
   "math": "X + Y ~ Gamma(2, λ),  mean 2/λ, variance 2/λ²",
   "why": "The shape parameter counts the exponentials. This is the distribution the exam's marked answer gave for a question about X."},
  {"say": "(b) The minimum of five.",
   "math": "P(min > t) = e^(−5λt) ⟹ exponential(5λ)\nat λ = 2: rate 10, mean 1/10 = 0.1",
   "why": "Five independent components in series fail five times sooner on average than one."},
  {"say": "(c) A conditional expectation.",
   "math": "X | X + Y = 6 ~ Uniform(0, 6)\nE = 6/2 = 3",
   "why": "Half the total, with no λ anywhere."},
  {"say": "(d) A scaling.",
   "math": "λX ~ exponential(1) = Gamma(1,1)\n2λX ~ Gamma(shape 1, scale 2) = χ²₂",
   "why": "Simulated mean 1.998 and variance 4.005 against the χ²₂ values 2 and 4."},
  {"say": "(e) Memorylessness.",
   "math": "P(T > 6 | T > 4) = P(T > 2) = e^(−2×2) = e^(−4) = 0.018316",
   "why": "The elapsed four minutes are forgotten entirely. The exponent uses the rate times the REMAINING time."},
  {"say": "(f) The Jacobian.",
   "math": "x = u, y = v − u\ndet [[1, 0], [−1, 1]] = 1",
   "why": "Unit Jacobian, so the joint density carries over with no scaling factor — which is what keeps the main derivation to three lines."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "Where transformations do the work",
 "objective": "Recognise the method across the rest of the syllabus.",
 "blocks": [
  {"t": "step", "h": "In the sampling distributions (topic 1.13)",
   "body": "Every classical sampling distribution is a transformation: chi-square is a sum of squared normals, t is a normal over the root of an independent chi-square, F is a ratio of chi-squares. The Jacobian method is how each density is derived, and 2λX ~ χ²₂ from this lesson is the simplest instance."},
  {"t": "step", "h": "In Bayesian work and the Beta",
   "body": "If U ~ Gamma(a, λ) and V ~ Gamma(b, λ) independently, then U/(U+V) ~ Beta(a, b), and this lesson's X/(X+Y) ~ Uniform(0,1) is the case a = b = 1, since Beta(1,1) IS the uniform. The same construction gives the Dirichlet in several dimensions, which is the conjugate prior for the multinomial."},
  {"t": "step", "h": "In exact tests (topics 4.14 and 4.16)",
   "body": "Fisher's exact test conditions a 2×2 table on its margins, which turns the two binomials into the hypergeometric of section 8 and removes the unknown common probability. Conditioning on a sufficient statistic to eliminate a nuisance parameter is the general device, and it comes from the sufficiency material of topic 4.1."},
  {"t": "step", "h": "In simulation",
   "body": "The inverse-transform method generates a variable from any continuous distribution as F⁻¹(U) with U uniform — a transformation whose correctness is the probability integral transform of lesson 1.13. For the exponential it gives −ln(U)/λ, which is the standard generator."},
  {"t": "def", "h": "The common thread",
   "body": "Nothing in this topic is new probability; it is bookkeeping about densities under a change of variables, plus the two shortcuts for minima and for conditioning on a sum. Recognising which of the three routes a question wants is most of the work, and the choice is usually settled by the form of the thing being asked about."}],
 "ask": {
  "q": "U/(U+V) is Beta(a, b) for independent Gammas with the same rate. Which values of a and b give this lesson's Uniform(0,1) result, and why?",
  "nudge": "An exponential is a Gamma with shape 1. And Beta(1,1) is which distribution?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the conditioning results and the directions.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Sum versus minimum of n iid exponential(λ): which is Gamma and which is exponential?",
   "a": "The sum is Gamma(n, λ) with mean n/λ; the minimum is exponential(nλ) with mean 1/(nλ)."},
  {"q": "Two independent Poissons given their total: what distribution, with what parameter?",
   "a": "Binomial(k, μ₁/(μ₁+μ₂)) — for rates λ and 2λ that is Binomial(k, 1/3)."},
  {"q": "Two independent binomials with the same p, given their total?",
   "a": "Hypergeometric, free of p — the basis of Fisher's exact test."},
  {"q": "P(N₁ = 1 | N₁ + N₂ = 4) for rates λ and 2λ?",
   "a": "C(4,1)(1/3)(2/3)³ = 32/81 = 0.3951."},
  {"q": "What is the Jacobian of (x, y) → (x, x + y), and why does it matter?",
   "a": "1, so the joint density transfers unchanged — which keeps the main derivation short."},
  {"q": "For T exponential with rate 2, what is P(T > 6 | T > 4)?",
   "a": "e^(−4) = 0.018316, by memorylessness."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Choose between the cdf route, the Jacobian route and the conditional-ratio route from the form of the question.",
  "Compute the Jacobian of (x, y) → (x, x + y) and say why it is 1.",
  "Derive that X | X + Y = s is Uniform(0, s) and explain where λ cancels.",
  "Give the sum as Gamma(n, λ) and the minimum as exponential(nλ), without swapping them.",
  "Derive X/(X + Y) ~ Uniform(0,1) and 2λX ~ χ²₂.",
  "Condition Poisson counts on their total to get a binomial, and binomial counts to get a hypergeometric.",
  "Use memorylessness rather than integrating, and get the exponent right."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "The Jacobian theorem, and the Beta from two Gammas",
 "objective": "See the general statement and the derivation the topic is really about.",
 "blocks": [
  {"t": "formula", "h": "The theorem in general",
   "body": "Let (U, V) = g(X, Y) be one-to-one and continuously differentiable with non-vanishing Jacobian on the support. Then\n    f_{U,V}(u, v) = f_{X,Y}(h₁(u,v), h₂(u,v)) · |J|,   J = det ∂(x, y)/∂(u, v),\nwhere h is the inverse map. In n dimensions the statement is identical with an n × n determinant. If g is not one-to-one, split the support into pieces on which it is and add the contributions."},
  {"t": "step", "h": "Why a determinant appears",
   "body": "A density is probability per unit area, so if the map stretches a small region by a factor, the density must shrink by the same factor for the probability to be preserved. The determinant of the derivative matrix is precisely the local area-scaling factor, and the absolute value is taken because orientation is irrelevant to area."},
  {"t": "step", "h": "The Beta from two Gammas, derived",
   "body": "Let U ~ Gamma(a, λ) and V ~ Gamma(b, λ) be independent and set\n    R = U/(U+V),  S = U + V.\nThe inverse is u = rs, v = s(1−r), with Jacobian det [[s, r], [−s, 1−r]] = s. Substituting the Gamma densities, the joint density factorises into a function of r times a function of s:\n    f(r, s) ∝ r^(a−1)(1−r)^(b−1) · s^(a+b−1)e^(−λs).\nSo R ~ Beta(a, b) and S ~ Gamma(a+b, λ), and they are INDEPENDENT — which is the striking part. With a = b = 1 the exponential case gives R ~ Beta(1,1) = Uniform(0,1), this lesson's result."},
  {"t": "def", "h": "What the independence buys",
   "body": "The sum carries all the information about the scale and the ratio carries all the information about the split, and the two are independent. That is why conditioning on the sum leaves a distribution free of λ: the ratio never knew about λ in the first place. It is also the construction behind the Dirichlet distribution and behind the standard algorithm for generating Beta variables from Gammas."},
  {"t": "step", "h": "A caution about the one-to-one requirement",
   "body": "For Y = X² with X symmetric about 0, the map is two-to-one and the naive formula fails. Splitting into x > 0 and x < 0 and adding gives f_Y(y) = [f_X(√y) + f_X(−√y)]/(2√y), which for a standard normal is the chi-square with one degree of freedom. Forgetting the second branch halves the answer, and this is the most common way the method is misapplied."}],
 "ask": {
  "q": "In the Beta–Gamma derivation the joint density factorised into a function of r times a function of s. What does that factorisation prove?",
  "nudge": "A joint density that factors into a function of each variable separately says what about those variables?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "probability_t10_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "probabilityt10",
 "topicId": "probability-t10",
 "moduleId": "probability",
 "title": "Transformations and Jacobians",
 "breadcrumb": "Probability → Transformations → Functions of random variables",
 "engine": "B",
 "engineName": "Probability — the distribution of something built from other variables",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Choose between the cdf route, the Jacobian route and the conditional-ratio route.",
  "Compute a Jacobian determinant and say why the density is multiplied by it.",
  "Derive that X | X + Y = s is Uniform(0, s) and explain where the rate cancels.",
  "Give the sum as Gamma(n, λ) and the minimum as exponential(nλ) without confusing them.",
  "Condition Poisson counts on a total to get a binomial, and binomials to get a hypergeometric.",
  "Apply memorylessness correctly, including the exponent."],
 "prereq": [
  {"id": "p1", "name": "The exponential and Gamma distributions",
   "why": "Nearly every example is built from exponentials, and the Gamma is what their sums become."},
  {"id": "p2", "name": "Joint densities and independence",
   "why": "The method starts from a joint density, and independence is what makes it a product."},
  {"id": "p3", "name": "Conditional densities",
   "why": "June 2026's question is a conditional density written as a ratio, which is the quickest of the three routes."},
  {"id": "p4", "name": "Partial derivatives and determinants",
   "why": "The Jacobian is a determinant of partial derivatives, and the lesson computes several."}],
 "traps": [
  "X | X + Y = s is Uniform(0, s), NOT Gamma(2, λ) — the Gamma is the distribution of the SUM.",
  "The sum of n exponentials is Gamma(n, λ); the MINIMUM is exponential(nλ). Do not swap them.",
  "The minimum has rate nλ, not λ/n — it arrives sooner, not later.",
  "E(X | X + Y = s) = s/2, not 1/λ; the conditional answer must contain s and not λ.",
  "Two binomials given their total give a HYPERGEOMETRIC, not a binomial.",
  "In P(T > 6 | T > 4) with rate 2, the exponent is 2 × 2 = 4, not 2 or 6.",
  "The Jacobian formula needs the map to be one-to-one; Y = X² needs both branches.",
  "A conditional-given-the-total answer containing the rate has failed to cancel something."],
 "revision": {
  "sheet": [
   "Three routes: cdf method for minima and maxima; conditional ratio for a sum; Jacobian in general.",
   "Jacobian: f_{U,V}(u,v) = f_{X,Y}(x,y)·|det ∂(x,y)/∂(u,v)|, the determinant being the area-scaling factor.",
   "For (U,V) = (X, X+Y): x = u, y = v−u, Jacobian = det[[1,0],[−1,1]] = 1, so the density transfers unchanged.",
   "June 2026 Q25: f(x | X+Y = s) = λ²e^(−λs)/(λ²s e^(−λs)) = 1/s on (0,s), so X | X+Y = s ~ Uniform(0,s).",
   "At s = 2 that is Uniform(0,2) — option C. The marked Gamma(2,λ) is the distribution of the SUM.",
   "The rate λ cancels entirely, so the answer does not depend on how fast the process runs.",
   "Verified: 5,397 draws conditioned near X+Y = 2 gave mean 1.0051, sd 0.5772 (against 2/√12 = 0.5774), KS p = 0.230.",
   "E(X | X+Y = s) = s/2. Check by the tower property: E((X+Y)/2) = (2/λ)/2 = 1/λ = E(X) ✓.",
   "Sum of n iid exponential(λ) ~ Gamma(n, λ): mean n/λ, variance n/λ², skewness 2/√n.",
   "Minimum of n iid exponential(λ) ~ exponential(nλ): mean 1/(nλ). Simulated at λ=1.5: 0.2217 for n=3 against 0.2222.",
   "X/(X+Y) ~ Uniform(0,1) for two iid exponentials. Simulated mean 0.49992, variance 0.08341 against 1/12.",
   "2λX ~ χ² with 2 df, since λX ~ exponential(1) = Gamma(1,1) and doubling gives scale 2. Simulated mean 1.998, variance 4.005.",
   "Poisson split: N₁ | N₁+N₂ = k ~ Binomial(k, μ₁/(μ₁+μ₂)). Rates λ and 2λ give p = 1/3, free of λ and of t.",
   "P(N₁ = 1 | total = 4) = C(4,1)(1/3)(2/3)³ = 32/81 = 0.39506; simulated 0.39459 over 101,098 draws.",
   "Binomial split: X | X+Y = k ~ Hypergeometric(m+n, m, k), free of p — the basis of Fisher's exact test.",
   "Memorylessness: P(T > s+t | T > s) = P(T > t). Rate 2 gives P(T>6|T>4) = e^(−4) = 0.018316.",
   "Poisson process: given exactly one event in an interval, its position is uniform; given k, the positions are k sorted uniforms.",
   "Beta from Gammas: U/(U+V) ~ Beta(a,b) independent of U+V ~ Gamma(a+b, λ); a = b = 1 gives the uniform result."],
  "cards": [
   ["X | X + Y = s, iid exponentials", "Uniform(0, s) — the rate cancels"],
   ["E(X | X + Y = s)", "s/2, with no λ in it"],
   ["Sum of n exponentials", "Gamma(n, λ), mean n/λ"],
   ["Minimum of n exponentials", "exponential(nλ), mean 1/(nλ)"],
   ["X/(X + Y)", "Uniform(0, 1)"],
   ["2λX for X exponential(λ)", "χ² with 2 degrees of freedom"],
   ["Jacobian of (x, y) → (x, x+y)", "1 — density transfers unchanged"],
   ["Two Poissons given their total", "Binomial(k, μ₁/(μ₁+μ₂))"],
   ["Two binomials given their total", "Hypergeometric, free of p"],
   ["P(T>6 | T>4), rate 2", "e^(−4) = 0.0183, by memorylessness"],
   ["One Poisson event in an interval", "Its position is uniform on the interval"],
   ["U/(U+V) for Gammas", "Beta(a, b), independent of the sum"]],
  "tricks": [
   "Minimum or maximum? Use survival functions and multiply — one line.",
   "Conditional on a sum? Write f(x, s−x)/f_sum(s) — also one line.",
   "Anything else? Jacobian, then integrate out the variable you did not want.",
   "Check a 'given the total' answer for the rate: if λ or p survives, something did not cancel.",
   "Check a conditional expectation contains the conditioning value: s/2 not 1/λ.",
   "For memorylessness, the exponent is the rate times the REMAINING time, not the total."],
  "shortcuts": [
   "(x, x+y) has unit Jacobian, so the joint density needs no adjustment at all.",
   "Gamma skewness is 2/√n, so the normal approximation improves at a visible rate: 2, 1.41, 0.89, 0.63, 0.37 for n = 1, 2, 5, 10, 30.",
   "32/81 = 0.3951 and e^(−4) = 0.0183 are the two numerical answers in this topic's variants."],
  "remember": [
   "Given the total, the split is uniform.",
   "Sum is Gamma; minimum is exponential with rate nλ.",
   "If the rate survives a conditioning, you made an error."]},
 "howto": "Section 5 is June 2026's question and the whole lesson in miniature: the joint density of two independent exponentials depends on x and y only through their sum, so along a line of fixed sum it is constant, and the conditional distribution is therefore flat. Read the cancellation step carefully — both λ² factors and both exponentials disappear, which is why the answer contains no rate, and that absence is a useful check on any question of this kind. Section 3's chart is worth a minute: raise the number of exponentials being added and watch Gamma(n, λ) form a peak and approach a normal, with the skewness 2/√n reported so the rate of convergence is visible rather than asserted. Section 7 generalises the conditioning device to Poisson and binomial counts, where the rate and the success probability cancel in just the same way — and that is the idea behind Fisher's exact test. If short of time, sections 3, 4, 5 and 8 are the lesson. The optional section states the Jacobian theorem properly, derives the Beta from two Gammas, and warns about the one-to-one requirement that Y = X² violates.",
 "refs": [
  {"title": "Functions of Random Variables and Transformations", "where": "Lessons 22 and 23",
   "site": "Penn State STAT 414", "url": "https://online.stat.psu.edu/stat414/",
   "type": "Course notes", "free": True, "checked": "2026-11-03",
   "why": "The cdf method, the Jacobian method and worked exponential and Gamma transformations."},
  {"title": "Statistical Inference, 2nd edition", "where": "Sections 2.1, 4.3 and 4.6",
   "site": "Casella and Berger", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The transformation theorem in general form, the Beta–Gamma construction, and conditioning on sums."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 4",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "Transformations at NET level, with the exponential conditioning result and the Jacobian examples stated explicitly."},
  {"title": "Probability and Statistics", "where": "Weeks on functions of random variables",
   "site": "NPTEL / SWAYAM", "url": "https://archive.nptel.ac.in/courses/111105090",
   "type": "Video course", "free": True, "checked": "2026-11-03",
   "why": "Indian-syllabus notation and the exam style these transformation questions are posed in."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026 on June 2026 Q25 (answered wrongly, marked D against C): X and Y independent exponential(λ), find the conditional distribution of X given X + Y = 2. The conditional density is f(x, s−x)/f_{X+Y}(s) = λ²e^(−λs)/(λ²s e^(−λs)) = 1/s on (0, s), so X | X+Y = s is Uniform(0, s) and the answer is Uniform(0, 2); the marked Gamma(2, λ) is the distribution of the SUM. The striking feature, taught as the lesson's organising idea, is that λ cancels completely — the joint density of independent exponentials depends on x and y only through their sum, so it is constant along any line of fixed sum. Verified by simulation: 600,000 pairs at λ = 1.5, of which 5,397 were kept near X+Y = 2, gave mean 1.0051 against 1, sd 0.5772 against 2/√12 = 0.5774, deciles matching Uniform(0,2) throughout, and a Kolmogorov–Smirnov p-value of 0.230. All nine variants are taught in named sections and pooled, including the Poisson interarrival item retagged into Q25 from the maths variant file earlier in this project, which belongs here because memorylessness is what makes the conditional uniform. Every other figure was computed and simulated: X/(X+Y) ~ Uniform(0,1) (mean 0.49992, variance 0.08341 against 1/12, KS p = 0.890); sums as Gamma(n, λ) at n = 1, 2, 5, 10; minima as exponential(nλ) at n = 3 and 7; 2λX ~ χ²₂ (mean 1.9984, variance 4.0045, KS p = 0.101); the Poisson split P(N₁ = 1 | total = 4) = 32/81 = 0.39506 against a simulated 0.39459 over 101,098 qualifying draws; and the binomial-given-total hypergeometric at m = 6, n = 4, k = 3 (empirical 0.0327, 0.3003, 0.4991, 0.1680 against the exact 0.0333, 0.3000, 0.5000, 0.1667). The memorylessness figure needed a second attempt: conditioning 600,000 draws on T > 4 retained only 205, so the estimate 0.0253 against the exact e^(−4) = 0.018316 was pure sampling error; simulating the shifted variable over four million draws gave 0.018388, confirming the formula. Introduces the `gamma-sum` visualisation, written for this lesson and reusable for 1.6 and 1.9; its means, variances and the skewness 2/√n were checked against the simulated values and its densities integrate to 1.00000000. Previous-year questions are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "pr-t10-m-%02d" % i, "format": fmt, "topic": "probability-t10",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "Let X and Y be independent, each exponential with parameter λ. The conditional distribution of X given X + Y = 2 is:",
 ["Uniform(0, 2)", "Exponential(2)", "Gamma(2, λ)", "Beta(λ/2, λ/2)"],
 "A",
 "f(x | X+Y = s) = λ²e^(−λs)/(λ²s e^(−λs)) = 1/s on 0 < x < s, which is the Uniform(0, s) density; at s = 2 that is Uniform(0, 2). This is June 2026 Q25. Option C is the distribution of the SUM, which is what was marked; option B has unbounded support and so cannot describe a variable confined to (0, 2)."))

I.append(q(2, "single", "easy",
 "If X and Y are iid exponential(λ), then X/(X + Y) follows:",
 ["Uniform(0, 1)", "Exponential(λ)", "Gamma(2, λ)", "Beta(2, 2)"],
 "A",
 "Given X + Y = s, X is Uniform(0, s), so X/s is Uniform(0, 1) — and this holds for every s, so the unconditional distribution is Uniform(0,1) as well. Simulated mean 0.49992 and variance 0.08341 against 0.5 and 1/12 = 0.08333."))

I.append(q(3, "single", "easy",
 "The sum of n iid exponential(λ) variables follows:",
 ["Gamma(n, λ)", "exponential(nλ)", "Normal", "χ²ₙ"],
 "A",
 "The Gamma's shape parameter counts the exponentials, giving mean n/λ and variance n/λ². Option B is the MINIMUM, whose mean 1/(nλ) shrinks with n while the sum's mean grows — the two results point in opposite directions and are easily swapped."))

I.append(q(4, "single", "easy",
 "The minimum of n iid exponential(λ) variables follows:",
 ["exponential(nλ)", "Gamma(n, λ)", "exponential(λ/n)", "Uniform"],
 "A",
 "P(min > t) = (e^(−λt))ⁿ = e^(−nλt), the survival function of an exponential with rate nλ and mean 1/(nλ). Option C would make the minimum slower than a single component, which is the wrong direction. Simulated at λ = 1.5: mean 0.2217 for n = 3 against the exact 0.2222."))

I.append(q(5, "single", "easy",
 "The only continuous distribution with the memoryless property is:",
 ["exponential", "normal", "uniform", "gamma"],
 "A",
 "P(T > s + t | T > s) = P(T > t) characterises the exponential uniquely, and the Gamma has it only in the special case of shape 1, which IS the exponential. The geometric is the discrete counterpart and is likewise unique."))

I.append(q(6, "single", "easy",
 "If X ~ exponential(λ), then 2λX follows:",
 ["χ² with 2 degrees of freedom", "exponential(2)", "Gamma(2, 1)", "χ² with 1 degree of freedom"],
 "A",
 "λX ~ exponential(1) = Gamma(1, 1), and multiplying by 2 gives Gamma(shape 1, scale 2), which is exactly χ²₂. Simulated mean 1.9984 and variance 4.0045 against the χ²₂ values 2 and 4, with KS p = 0.101."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "For iid exponential(λ) variables, E(X | X + Y = s) equals:",
 ["s/2", "s", "1/λ", "s/λ"],
 "A",
 "The conditional distribution is Uniform(0, s), whose mean is s/2. Option C is the UNCONDITIONAL mean E(X); a conditional expectation must depend on the observed total s, and must not contain λ, since λ cancels from the conditional distribution entirely.",
 check="Verify by the tower property: E(E(X | X+Y)) = E((X+Y)/2) = (2/λ)/2 = 1/λ = E(X) ✓."))

I.append(q(8, "numeric", "moderate",
 "If N₁ and N₂ are independent Poisson processes with rates λ and 2λ, then P(N₁ = 1 | N₁ + N₂ = 4) equals:",
 ["32/81", "4/81", "8/27", "16/81"],
 "A",
 "Given the total, N₁ is Binomial(4, p) with p = λ/(λ + 2λ) = 1/3 — the λ cancels, and so does the observation period. So P(N₁ = 1) = C(4,1)(1/3)(2/3)³ = 4 × (1/3) × (8/27) = 32/81 = 0.39506. Simulated as 0.39459 over 101,098 qualifying draws.",
 check="The four probabilities for N₁ = 0,…,4 must sum to 1: (2/3)⁴ + 32/81 + 24/81 + 8/81 + 1/81 = 16/81 + 32/81 + 24/81 + 8/81 + 1/81 = 81/81 ✓."))

I.append(q(9, "single", "moderate",
 "If X ~ Binomial(m, p) and Y ~ Binomial(n, p) are independent, then X | (X + Y = k) follows:",
 ["Hypergeometric", "Binomial", "Poisson", "Negative binomial"],
 "A",
 "P(X = j | X + Y = k) = C(m,j)C(n,k−j)/C(m+n,k), which is the hypergeometric and is free of p entirely. Conditioning on the total turns the problem into drawing k items without replacement from m + n. Checked at m = 6, n = 4, k = 3: empirical 0.0327, 0.3003, 0.4991, 0.1680 against the exact 0.0333, 0.3000, 0.5000, 0.1667. This is the distribution behind Fisher's exact test."))

I.append(q(10, "numeric", "moderate",
 "For a Poisson process with rate 2 per minute, P(interarrival time > 6 | > 4) equals:",
 ["e^(−4)", "e^(−6)", "e^(−1)", "1 − e^(−1)"],
 "A",
 "By memorylessness the elapsed 4 minutes are forgotten: P(T > 6 | T > 4) = P(T > 2) = e^(−2×2) = e^(−4) = 0.018316. The exponent is the rate times the REMAINING time, which is 2 × 2, not 2 × 6 and not 2 × 1.",
 check="Confirmed by simulating the shifted variable over four million draws: 0.018388 against the exact 0.018316. Conditioning a plain simulation on T > 4 keeps only about 200 of 600,000 draws and gives useless precision."))

I.append(q(11, "numeric", "moderate",
 "The Jacobian determinant of the transformation (x, y) → (u, v) = (x, x + y) is:",
 ["1", "−1", "x", "v − u"],
 "A",
 "The inverse map is x = u, y = v − u, so the matrix of partial derivatives is [[1, 0], [−1, 1]] with determinant 1. The joint density therefore transfers unchanged, which is why the main derivation of this lesson takes only three lines.",
 check="A unit Jacobian means the map preserves area, which is plausible: it is a shear, and a shear does not change areas."))

I.append(q(12, "multi", "moderate",
 "Consider two independent exponential(λ) variables X and Y.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true: the joint density λ²e^(−λ(x+y)) is a function of the sum alone. B is true and is the lesson's main result. C is true, since λ cancels from the ratio. D is false — the sum is Gamma(2, λ), not exponential; exponential(2λ) is the MINIMUM.",
 statements=["The joint density depends on x and y only through x + y.",
             "X | X + Y = s is Uniform(0, s).",
             "The conditional distribution does not depend on λ.",
             "X + Y is exponential with rate 2λ."],
 verdicts=verd(
  (True, "True. f(x,y) = λe^(−λx)·λe^(−λy) = λ²e^(−λ(x+y)), so the density is constant along any line of fixed sum — which is the whole reason the conditional comes out flat."),
  (True, "True, with mean s/2. Verified by simulation: KS p = 0.230 against Uniform(0,2) when conditioning near X+Y = 2."),
  (True, "True. Both λ² factors and both e^(−λs) factors cancel in f(x, s−x)/f_{X+Y}(s), leaving 1/s. A conditional answer that still contains λ has failed to cancel something."),
  (False, "False. The SUM is Gamma(2, λ) with mean 2/λ; exponential(2λ) with mean 1/(2λ) is the MINIMUM of the two. The two results move in opposite directions as more variables are added."))))

I.append(q(13, "numeric", "moderate",
 "Five independent components each have exponential lifetime with rate λ = 2. The expected time to the first failure is:",
 ["0.1", "0.5", "2.5", "10"],
 "A",
 "The minimum of 5 iid exponential(2) variables is exponential with rate 5 × 2 = 10, so its mean is 1/10 = 0.1. Option B is the mean lifetime of a single component, 1/λ = 0.5, and option C is the mean of the SUM, 5/λ = 2.5.",
 check="The first of five failures must come sooner than a single component's mean of 0.5, which rules out every option above it."))

I.append(q(14, "single", "moderate",
 "Given that exactly one event of a Poisson process occurred in an interval, the distribution of its position is:",
 ["uniform over the interval", "concentrated at the midpoint",
  "exponential from the start of the interval", "Beta(2, 2) over the interval"],
 "A",
 "This is the same fact as the lesson's main result: the waiting time to the event and the waiting time from it to the end are the two exponential pieces, and conditioning on their total makes the split uniform. Given k events, the positions behave like k independent uniforms, sorted — the order statistics of lesson 1.1."))

I.append(q(15, "numeric", "moderate",
 "The skewness of the sum of n iid exponential variables is:",
 ["2/√n", "2n", "1/n", "2"],
 "A",
 "The sum is Gamma(n, λ), whose skewness is 2/√n — independent of λ, because λ is a pure scale parameter and rescaling cannot change a shape measure. It gives 2, 1.41, 0.89, 0.63 and 0.37 for n = 1, 2, 5, 10 and 30, which is the central limit theorem arriving at a visible rate.",
 check="At n = 1 it must reduce to the exponential's own skewness, which is 2 ✓."))

I.append(q(16, "single", "moderate",
 "Why does the parameter cancel when two independent Poisson counts are conditioned on their total?",
 ["conditioning on the total fixes the quantity the rate governs, so nothing is left for it to influence",
  "because the Poisson has equal mean and variance",
  "because the counts are independent",
  "it does not cancel — the answer depends on λ"],
 "A",
 "The conditional probability is a ratio in which the parameter appears to the same power above and below. Structurally, the total is a sufficient statistic for the rate, so conditioning on it removes the rate entirely. What survives is the RATIO of the two rates — here 1/3 for rates λ and 2λ. The same device makes Fisher's exact test free of the unknown success probability."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the Beta–Gamma construction: U ~ Gamma(a, λ) and V ~ Gamma(b, λ) independent, R = U/(U+V), S = U+V.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true, with Jacobian s. B is true and is the striking part. C is true: an exponential is a Gamma with shape 1, and Beta(1,1) is the uniform. D is false — the Jacobian is s, not 1; the unit Jacobian belongs to the (x, x+y) map.",
 statements=["The inverse map is u = rs, v = s(1−r), and its Jacobian determinant is s.",
             "R ~ Beta(a, b) and S ~ Gamma(a+b, λ), and R and S are independent.",
             "With a = b = 1 this gives X/(X+Y) ~ Uniform(0, 1).",
             "The Jacobian of this transformation is 1."],
 verdicts=verd(
  (True, "True: det [[s, r], [−s, 1−r]] = s(1−r) + rs = s. The Jacobian is not constant here, which is what produces the extra factor of s in the Gamma part."),
  (True, "True, and the independence is the striking part: the sum carries all the information about scale and the ratio all the information about the split. It is also why conditioning on the sum leaves a distribution free of λ — the ratio never depended on λ."),
  (True, "True. An exponential is Gamma with shape 1, so a = b = 1 gives R ~ Beta(1,1), which is the standard uniform — exactly this lesson's result."),
  (False, "False. Its Jacobian is s. The unit Jacobian is that of (x, y) → (x, x+y), a shear, which is a different transformation."))))

I.append(q(18, "single", "hard",
 "For Y = X² with X standard normal, the naive Jacobian formula fails because:",
 ["the map is two-to-one, so both branches x = ±√y must be added",
  "the Jacobian is zero everywhere",
  "Y has no density", "the normal is not continuous"],
 "A",
 "The transformation theorem requires a one-to-one map. Splitting into x > 0 and x < 0 and adding gives f_Y(y) = [f_X(√y) + f_X(−√y)]/(2√y), which for a standard normal is the chi-square with one degree of freedom. Forgetting the second branch halves the answer, and this is the commonest way the method is misapplied."))

I.append(q(19, "numeric", "hard",
 "X and Y are iid exponential(λ). Which of these does NOT depend on λ?",
 ["the distribution of X given X + Y = s", "the distribution of X + Y",
  "the distribution of min(X, Y)", "E(X)"],
 "A",
 "The conditional distribution is Uniform(0, s), with λ cancelled from both numerator and denominator of the ratio. All three others depend on λ: the sum is Gamma(2, λ), the minimum is exponential(2λ), and E(X) = 1/λ.",
 check="Checking which quantities contain the rate is a quick way to eliminate options on a conditioning question, since a correct conditional-given-the-total answer never does."))

I.append(q(20, "single", "hard",
 "A manager must find P(exactly one of 4 calls went to Team A), where two teams' calls arrive as independent Poisson streams with A at half B's rate, and the arrival rate is unknown. The best description is:",
 ["conditioning on the total of 4 removes the unknown rate, leaving Binomial(4, 1/3) and the answer 32/81",
  "the arrival rate must be estimated from historical data first",
  "the answer cannot be determined without the length of the observation period",
  "the answer is 1/2 since there are two teams"],
 "A",
 "Conditioning on the total fixes the only thing the rate governs, so λ and the period both cancel and the conditional distribution is Binomial(4, λ/(λ+2λ)) = Binomial(4, 1/3), giving 32/81 = 0.3951. What must still be known is the RATIO of the rates, which the statement that A handles half of B's traffic supplies. This is the same device by which Fisher's exact test avoids estimating a nuisance parameter."))

# Spread the answer keys; the validator caps any letter at 40% of the pool.
LET = "ABCD"
WANT = {"pr-t10-m-01": "C", "pr-t10-m-02": "B", "pr-t10-m-03": "D",
        "pr-t10-m-04": "C", "pr-t10-m-05": "B", "pr-t10-m-06": "D",
        "pr-t10-m-07": "C", "pr-t10-m-08": "B", "pr-t10-m-09": "D",
        "pr-t10-m-10": "C", "pr-t10-m-11": "B", "pr-t10-m-13": "D",
        "pr-t10-m-14": "C", "pr-t10-m-15": "B", "pr-t10-m-16": "D",
        "pr-t10-m-18": "C", "pr-t10-m-19": "B", "pr-t10-m-20": "D"}


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
 "moduleId": "probability", "topicId": "probability-t10", "source": "mastery",
 "label": "Transformations and Jacobians — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
