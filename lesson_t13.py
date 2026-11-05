#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 4.13 — Confidence intervals and pivots (topic inference-t13).

Built on PYQ evidence. June 2026 Q10 asked for the (1 − α) UPPER confidence bound for μ in
a normal sample with σ unknown; the official answer is (−∞, x̄ + t(n−1, α) s/√n) and the
response sheet shows a sign error — the minus-sign option was marked. The ten practice
variants on that question ask, between them: the two-sided interval with σ unknown, the
lower bound, the pivot for σ², the one-sided versus two-sided multiplier, the degrees of
freedom of the t pivot, the sample size needed to halve the width, the definition of a
pivotal quantity, the σ known upper bound, what "a 95% confidence interval" actually means,
and what happens as the confidence level rises. All ten are taught here and all ten are in
the pool.

Writes seed/lesson_t13.json and seed/inference_t13_mastery.json.
Run: python3 lesson_t13.py
"""
import json, io, os, re

OUT = "seed/lesson_t13.json"
POOL = "seed/inference_t13_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Recover the two sampling distributions every interval in this topic is built from, and settle what the percentile notation means.",
 "ask": {
  "q": "Three of the four checks below describe the behaviour of a statistic. The fourth is about notation. Why would notation deserve a place among them?",
  "nudge": "Look at the four options of a typical interval question. How many of them differ only in which percentile was used?"},
 "body": [
  "An interval estimate answers a different question from a point estimate. A point estimate says 'the mean is about 52.4'. An interval says 'the mean is somewhere between 49.2 and 55.6, and the method that produced those two numbers gets it right 95% of the time'.",
  "Everything in this topic comes from one trick. Find a quantity built from the data and the unknown parameter whose distribution does not depend on the parameter at all. Then you know its percentiles, you can trap it between two of them, and rearranging the trap isolates the parameter.",
  "Four checks. Two sampling distributions, the notation for percentiles, and one about what a random interval is."],
 "items": [
  {"ask": "For an iid N(μ, σ²) sample with σ unknown, what is the distribution of (x̄ − μ)/(s/√n), where s² = Σ(xᵢ − x̄)²/(n − 1)?",
   "recall": "Student's t with n − 1 degrees of freedom.",
   "refresh": [
    "With σ known the same quantity using σ instead of s is standard normal. Replacing σ by its estimate s costs you the normal distribution and gives you t instead, with heavier tails.",
    "The degrees of freedom are n − 1, not n. One degree of freedom was spent estimating μ with x̄, and that is the one subtracted.",
    "Notice what this quantity does and does not contain. It contains the data and the unknown μ, but its DISTRIBUTION contains neither μ nor σ. That property is the whole engine of this topic."]},
  {"ask": "For the same sample, what is the distribution of (n − 1)s²/σ²?",
   "recall": "Chi-square with n − 1 degrees of freedom.",
   "refresh": [
    "Equivalently Σ(xᵢ − x̄)²/σ² has that distribution, since (n − 1)s² is exactly Σ(xᵢ − x̄)².",
    "Again the degrees of freedom are n − 1 for the same reason: the deviations are taken about x̄ rather than about μ.",
    "This is the quantity that gives an interval for σ². It is the second of the only two sampling distributions this lesson needs."]},
  {"ask": "What do z_α and t(α, ν) mean — the upper α point or the lower?",
   "recall": "By the convention this lesson and the NET paper use, both are UPPER points: P(Z > z_α) = α and P(T > t(α, ν)) = α. So z₀.₀₅ = 1.645 and z₀.₀₂₅ = 1.96.",
   "refresh": [
    "Books differ, and this is a real source of lost marks. Some write t_α for the lower point. Read the stem: if it tells you t(n − 1, α) is the upper α point, use that.",
    "The ARGUMENT ORDER also varies. June 2026 Q10 wrote t(n − 1, α) with the degrees of freedom first; this lesson writes t(α, n − 1) with the tail area first. They mean the same thing, and you have to read which is which rather than pattern-match the option.",
    "For a two-sided interval at level 1 − α you need the α/2 point, because the α is split between the two tails. For a one-sided bound you need the α point itself. Half the wrong options in this topic are the other one of those two."]},
  {"ask": "In the statement P(x̄ − 1.96 σ/√n < μ < x̄ + 1.96 σ/√n) = 0.95, which parts are random?",
   "recall": "x̄ is random, so both endpoints are random. μ is a fixed unknown constant and is not random at all.",
   "refresh": [
    "The interval moves from sample to sample; the parameter stays still. The probability statement is about where the moving interval lands relative to the fixed target.",
    "That is why the statement is made BEFORE the sample is drawn. Once you have numbers — 49.2 and 55.6 — nothing is random any more, and μ is either in that fixed interval or it is not.",
    "Getting this straight is what section 8 is about, and it is the one conceptual question this topic reliably asks."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "A number with its uncertainty attached",
 "objective": "See why a single estimate is almost never a usable answer, and what an interval adds.",
 "body": [
  "A point estimate is a guess with no admission of error. Taken literally it is almost certainly wrong — the chance that a continuous parameter equals your estimate exactly is zero. What makes an estimate useful is knowing how far off it might be.",
  "An interval estimate carries that information in its width. A narrow interval says the data pinned the parameter down; a wide one says it barely constrained it. Two studies reporting the same estimate can be worlds apart in what they established, and only the interval shows it.",
  "The confidence level is the second half of the report, and it is a property of the METHOD rather than of the particular interval you ended up with. That distinction is subtle enough that it gets its own section, and it is the thing most often stated wrongly."],
 "scenario": {
  "teaser": "A water testing lab has to put one number on a report that a municipality will act on.",
  "title": "The number on the report",
  "body": [
   "A district water lab measures fluoride in borewell samples. The permissible limit is 1.5 mg per litre. A village's sample of twelve readings averages 1.42.",
   "If the lab reports 1.42 and stops there, the municipality reads it as 'below the limit' and does nothing. But twelve readings scatter, and the honest question is what the average of twelve readings tells you about the true level in that aquifer.",
   "Suppose the interval works out as 1.28 to 1.56. Now the report says something different and far more useful: the true level might well be above the limit, and the data cannot rule that out. The same 1.42 that looked reassuring becomes a reason to sample again.",
   "Notice which direction the lab actually cares about. Nobody is worried that the fluoride is too low. The useful statement is a one-sided one — an upper bound on the true level — and that is precisely the form June 2026 Q10 asked for. One-sided bounds are not a curiosity; in any setting with a limit in one direction they are the natural thing to report.",
   "And a one-sided bound at the same confidence level is TIGHTER than either end of the two-sided interval, because it spends the whole α in one tail instead of splitting it. That is the trade: you learn more about the direction you care about by giving up any claim about the other."],
  "q": "Why is a one-sided upper bound at 95% lower than the upper end of the two-sided 95% interval?",
  "answer": "Because the two-sided interval has to leave 2.5% in each tail, so its upper end is pushed out to the 2.5% point. The one-sided bound leaves the whole 5% in the one tail it cares about, so it only has to reach the 5% point, which is closer in. For n = 12 the multipliers are 2.201 and 1.796 — the one-sided bound is appreciably tighter, bought by saying nothing at all about how low the true value might be."},
 "ask": {
  "q": "The lab could report a wider interval and be more confident, or a narrower one and be less confident. With twelve readings fixed, is there any way to have both?",
  "nudge": "Look at what the width depends on. Which of those things can the lab change without collecting more samples?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Does a 95% interval actually cover 95% of the time?",
 "objective": "Find out that the stated confidence level is a promise about a procedure, and that some procedures keep it badly.",
 "viz": {"type": "ci-coverage", "n": 30, "conf": 0.95, "p": 0.2},
 "body": [
  "This shows a stated confidence level against what the procedure actually achieves. The method on display is the ordinary interval for a proportion — estimate plus or minus 1.96 standard errors — and the curve is its true coverage, computed exactly from the binomial distribution rather than simulated.",
  "Start at n = 30, stated level 95%, and read the coverage at p = 0.2. It comes to 0.946, which is close enough to the promise to be reassuring.",
  "Now slide p down towards 0.05. The coverage collapses — at p = 0.05 with n = 30 it is 0.782. A procedure advertising 95% is delivering 78%. Nothing is wrong with the arithmetic; the normal approximation behind the 1.96 simply does not hold when the counts are small.",
  "Raise n to 100 and read p = 0.05 again: 0.878. Better, and still not 95%. This is why sample-size rules of thumb for proportions exist.",
  "Now set p back to 0.5 and vary n. Coverage hovers near the promise but wobbles, and the wobble is the discreteness of the binomial — with a finite number of possible outcomes there is no way to hit 95% exactly.",
  "Two conclusions worth carrying. First, 'confidence' is a property of the method averaged over samples, not a guarantee attached to the interval in front of you. Second, the normal-mean intervals in the rest of this lesson do NOT have this defect: they are exact for every n because the t and chi-square distributions used are exact, not approximations. The optional section at the end comes back to the proportion case."],
 "ask": {
  "q": "The t interval for a normal mean is exact for every n, but this proportion interval is not. What is different about the two situations?",
  "nudge": "In one case the sampling distribution of the pivot is known exactly. In the other, what is the 1.96 standing in for?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The pivot method, which is the whole technique",
 "objective": "Learn the one recipe, in the order that works, and know what qualifies as a pivot.",
 "blocks": [
  {"t": "def", "h": "A pivotal quantity",
   "body": "A pivotal quantity is a function of the data AND the unknown parameter whose distribution does not depend on that parameter — nor on any other unknown. The function may mention θ; its distribution may not. That is the whole definition, and it is asked directly."},
  {"t": "formula", "h": "The three pivots this syllabus uses",
   "body": "normal mean, σ known:    (x̄ − μ)/(σ/√n)  ~  N(0, 1)\nnormal mean, σ unknown:  (x̄ − μ)/(s/√n)  ~  t with n − 1 df\nnormal variance:         (n − 1)s²/σ²    ~  chi-square with n − 1 df"},
  {"t": "step", "h": "The recipe, in the order that works",
   "body": "1. Find a pivot containing the parameter you want.\n2. Trap it between two percentiles of its known distribution, so that the trap holds with probability 1 − α.\n3. Rearrange the two inequalities to isolate the parameter in the middle.\nThe third step is where the algebra is, and it is where a sign or a reciprocal gets flipped. Rearranging is the whole examinable skill."},
  {"t": "formula", "h": "The recipe run once, on the normal mean with σ unknown",
   "body": "P( −t(α/2, n−1)  <  (x̄ − μ)/(s/√n)  <  t(α/2, n−1) ) = 1 − α\n⟹  P( x̄ − t(α/2, n−1) s/√n  <  μ  <  x̄ + t(α/2, n−1) s/√n ) = 1 − α"},
  {"t": "step", "h": "Two-sided or one-sided — read the question",
   "body": "A two-sided interval at level 1 − α splits α between the tails and uses the α/2 point. A one-sided bound puts the whole α in one tail and uses the α point. An UPPER confidence bound for μ is an interval of the form (−∞, U): it bounds μ from above, so it runs upward to x̄ + t(α, n−1) s/√n. A LOWER confidence bound is (L, ∞) and runs downward to x̄ − t(α, n−1) s/√n. The names describe which end is the finite one, and getting the sign the other way round is the single most common error on this question."},
  {"t": "def", "h": "Pivots outside the normal family",
   "body": "The method is not limited to the normal. For an exponential with mean θ, 2Σxᵢ/θ is chi-square with 2n degrees of freedom — a pivot, so the interval for θ comes from chi-square percentiles. For a uniform on (0, θ), the ratio X₍ₙ₎/θ has distribution function uⁿ on (0, 1), free of θ, so it is a pivot too. What makes each one work is only ever the same thing: the distribution came out free of the parameter."}],
 "flow": {
  "title": "From a pivot to an interval",
  "alt": "Flow chart for constructing a confidence interval by the pivot method",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "Parameter θ unknown", "kind": "start"},
   {"id": "b", "r": 1, "c": 1, "label": "Find Q(data, θ) whose distribution is free of θ", "kind": "step"},
   {"id": "c", "r": 2, "c": 0, "label": "Two-sided: trap Q between the α/2 points", "kind": "step"},
   {"id": "d", "r": 2, "c": 2, "label": "One-sided: bound Q by the α point", "kind": "step"},
   {"id": "e", "r": 3, "c": 1, "label": "Rearrange to isolate θ", "kind": "step"},
   {"id": "f", "r": 4, "c": 0, "label": "Interval (L, U)", "kind": "end"},
   {"id": "g", "r": 4, "c": 2, "label": "Bound (−∞, U) or (L, ∞)", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"},
   {"from": "b", "to": "c", "label": "interval wanted"},
   {"from": "b", "to": "d", "label": "bound wanted"},
   {"from": "c", "to": "e"}, {"from": "d", "to": "e"},
   {"from": "e", "to": "f"}, {"from": "e", "to": "g"}],
  "note": "Only step three involves any work. Steps one and two are recall, and the whole topic is one recipe applied to three pivots."},
 "ask": {
  "q": "Is x̄ − μ a pivotal quantity for a normal sample with σ unknown?",
  "nudge": "Write down its distribution. Does anything unknown appear in that distribution?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — the two-sided interval for a normal mean",
 "objective": "Run the recipe end to end with numbers, and see where each percentile comes from.",
 "ask": {
  "q": "The interval came out as 49.20 to 55.60. What would change if the sample standard deviation had been 12 instead of 6?",
  "nudge": "Which of the three ingredients of the half-width is s? Is the relationship proportional?"},
 "problem": "A sample of n = 16 observations from N(μ, σ²) with σ unknown gives x̄ = 52.4 and s = 6.0. Construct the 95% confidence interval for μ. Use t(0.025, 15) = 2.131.",
 "steps": [
  {"say": "Name the pivot and its distribution.",
   "math": "Q = (x̄ − μ)/(s/√n)  ~  t with n − 1 = 15 degrees of freedom",
   "why": "σ is unknown, so s replaces it and the reference distribution is t rather than normal. The degrees of freedom are 15, not 16 — one was spent estimating μ."},
  {"say": "Trap the pivot between the two percentiles that leave α/2 in each tail.",
   "math": "P( −2.131  <  (x̄ − μ)/(s/√n)  <  2.131 ) = 0.95",
   "why": "The level 0.95 means α = 0.05, split as 0.025 per tail, so the percentile needed is the upper 0.025 point. Using the upper 0.05 point here — 1.753 — would give an 90% interval, and that wrong interval is normally among the options."},
  {"say": "Rearrange to isolate μ. Multiply through by the standard error, then subtract x̄ and negate.",
   "math": "x̄ − 2.131 (s/√n)  <  μ  <  x̄ + 2.131 (s/√n)",
   "why": "Negating an inequality reverses it, which is why the two percentiles swap ends and the result comes out symmetric about x̄. Doing this slowly once is worth more than memorising the formula."},
  {"say": "Put the numbers in.",
   "math": "s/√n = 6.0/√16 = 6.0/4 = 1.5\nhalf-width = 2.131 × 1.5 = 3.197\ninterval = 52.4 ± 3.197 = (49.203, 55.597)",
   "why": "The standard error is the piece to compute first and check: 1.5, not 6. Dividing by n instead of √n is the other standard slip, and it would give a half-width near 0.8."},
  {"say": "State it the way a report would.",
   "math": "95% CI for μ:  (49.20, 55.60)",
   "why": "Two decimal places, both ends, and the level attached. An interval reported without its confidence level is not an answer."}],
 "after": "Look at what controlled the width: the percentile, the sample standard deviation, and √n. Only two of those three are yours to change — you can lower the confidence level, or collect more data. The scatter in the population is not negotiable, which is the honest reason some questions cannot be settled with the sample you have."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the definition and the recipe before going on.",
 "intro": "Answer each one before revealing it.",
 "items": [
  {"q": "Define a pivotal quantity.",
   "a": "A function of the data and the parameter whose distribution does not depend on the parameter, or on any other unknown."},
  {"q": "Name the pivot for a normal mean with σ unknown, and its distribution.",
   "a": "(x̄ − μ)/(s/√n), which is t with n − 1 degrees of freedom."},
  {"q": "Name the pivot for a normal variance, and its distribution.",
   "a": "(n − 1)s²/σ², which is chi-square with n − 1 degrees of freedom."},
  {"q": "For a two-sided interval at level 1 − α, which percentile do you use?",
   "a": "The upper α/2 point, because α is split between the two tails. A one-sided bound uses the upper α point."},
  {"q": "In a 95% interval, what is random before the sample is drawn?",
   "a": "Both endpoints, because they are built from x̄ and s. The parameter is a fixed constant."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — the one-sided bounds (June 2026, Q10)",
 "objective": "Build the upper and lower confidence bounds yourself, which is where the sign error happens.",
 "problem": "X₁,…,Xₙ is a random sample from N(μ, σ²) with σ unknown. Give the (1 − α) upper confidence bound for μ, then the lower confidence bound. Then evaluate the upper bound for the sample of section 4: n = 16, x̄ = 52.4, s = 6.0, α = 0.05, with t(0.05, 15) = 1.753.",
 "steps": [
  {"say": "Decide which percentile a one-sided bound needs, and why it differs from the two-sided case.",
   "blank": {"prompt": "At level 1 − α, which upper point of the t distribution does a one-sided bound use?",
             "answer": "the upper α point, t(α, n − 1)",
             "accept": ["t(alpha, n-1)", "the alpha point", "upper α point", "t(α, n−1)",
                        "alpha not alpha/2", "the α point, not α/2"],
             "hint": "A two-sided interval splits α between two tails. A one-sided bound has only one tail to pay for."},
   "why": "All of α goes into the single tail, so the point needed is t(α, n − 1) and not t(α/2, n − 1). This is why a one-sided bound is tighter than the corresponding end of the two-sided interval."},
  {"say": "Now the upper bound. An upper confidence bound is an interval of the form (−∞, U) — it bounds μ from above.",
   "blank": {"prompt": "Write the (1 − α) upper confidence bound for μ.",
             "answer": "(−∞, x̄ + t(α, n − 1) s/√n)",
             "accept": ["(-inf, xbar + t(alpha,n-1) s/sqrt(n))",
                        "(−∞, x̄ + t(α,n−1)·s/√n)",
                        "minus infinity to xbar plus t times s over root n",
                        "(-∞, X̄ + t(n−1, α) S/√n)"],
             "hint": "The bound is an upper limit on μ, so the finite end must be ABOVE x̄. Which sign puts it there?"},
   "why": "This is exactly June 2026 Q10, and the official answer. The response sheet shows the minus-sign option was marked — the classic error. 'Upper bound' names which END is finite, not which tail of the distribution you took, so the sign is plus."},
  {"say": "And the lower bound, which is the mirror image.",
   "blank": {"prompt": "Write the (1 − α) lower confidence bound for μ.",
             "answer": "(x̄ − t(α, n − 1) s/√n, ∞)",
             "accept": ["(xbar - t(alpha,n-1) s/sqrt(n), inf)",
                        "(x̄ − t(α,n−1)·s/√n, ∞)",
                        "xbar minus t s over root n to infinity"],
             "hint": "A lower bound on μ has its finite end BELOW x̄, and the interval runs upward from there."},
   "why": "Same percentile, opposite sign, and the infinite end at the other side. Writing both down together once is the cure for the confusion, because the pair makes the naming obvious."},
  {"say": "Finally, evaluate the upper bound for the sample from section 4 and compare it with the two-sided interval.",
   "blank": {"prompt": "Compute the 95% upper confidence bound for μ when n = 16, x̄ = 52.4, s = 6.0.",
             "answer": "(−∞, 55.03)",
             "accept": ["55.03", "(-inf, 55.03)", "55.030", "up to 55.03", "(−∞, 55.030)"],
             "hint": "52.4 + 1.753 × 1.5. The standard error is the same 1.5 as before."},
   "why": "52.4 + 1.753(1.5) = 52.4 + 2.630 = 55.03. Compare with the two-sided interval's upper end of 55.60: the one-sided bound is tighter by over half a unit, bought by giving up any statement about how small μ might be."}],
 "after": "The sign is the whole question here, and the fix is structural rather than mnemonic: write the shape of the interval first — (−∞, U) or (L, ∞) — and then the sign that puts the finite end on the correct side of x̄ is forced. Memorising 'plus for upper' works until a question phrases it differently."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "What '95% confidence' means, and what it does not",
 "objective": "Get the interpretation exactly right, because the conceptual question in this topic is almost always this one.",
 "blocks": [
  {"t": "def", "h": "The correct statement",
   "body": "The confidence level is a property of the PROCEDURE. If you were to repeat the whole business — draw a sample, compute the interval — a great many times, about 95% of the intervals produced would contain the true parameter. The 95% describes how often the method succeeds, over samples."},
  {"t": "step", "h": "Why it cannot be a statement about your interval",
   "body": "Once the sample is in hand, the interval is two fixed numbers and μ is a fixed constant. Either μ lies between them or it does not; there is nothing left to be 95% about. Saying 'there is a 95% probability that μ lies in (49.20, 55.60)' treats μ as random, and in this framework it is not. That option appears in NET questions and it is wrong."},
  {"t": "step", "h": "The three wrong readings that get offered as options",
   "body": "'95% of the data lies in the interval' — false, and not even close: the interval is about the mean, not about individual observations, and it shrinks as n grows while the data's spread does not. '95% of sample means lie in this interval' — false; that would be a statement about x̄, whose own interval is a different thing. 'There is a 95% chance μ is in this particular interval' — false in this framework, for the reason above. The correct one is always the statement about the procedure covering the parameter in 95% of repetitions."},
  {"t": "def", "h": "The interval that CAN be read as a probability about the parameter",
   "body": "A Bayesian credible interval does support the statement 'there is a 95% probability that θ lies here', because it treats θ as a random quantity with a posterior distribution. That is a different construction resting on a prior, and it is topic 4.7's territory. The two are often numerically close and conceptually different, and a question that offers the probability reading as correct is usually testing whether you noticed which framework you are in."},
  {"t": "step", "h": "What the level does not promise",
   "body": "It does not promise that this interval is narrow, that the model is right, or — as the explore section showed — that an approximate procedure achieves its stated level at a given sample size. The normal-mean and normal-variance intervals here are exact; many procedures elsewhere are not."}],
 "ask": {
  "q": "A statistician computes a 95% interval and it comes out as (49.20, 55.60). Is the statement 'μ is in this interval' true or false?",
  "nudge": "It has a definite truth value — you simply do not know which. What does that tell you about attaching a probability to it?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — an interval for the variance",
 "objective": "Use the chi-square pivot, where the rearrangement inverts and the interval comes out asymmetric.",
 "problem": "A sample of n = 10 from N(μ, σ²) with μ unknown gives Σ(xᵢ − x̄)² = 36. Construct the 95% confidence interval for σ². Use the upper 0.025 point of chi-square with 9 df = 19.023 and the upper 0.975 point = 2.700.",
 "hints": [
  "Direction — the pivot is (n − 1)s²/σ², equivalently Σ(xᵢ − x̄)²/σ², which is chi-square with n − 1 = 9 degrees of freedom. Trap it between the two percentiles that leave 0.025 in each tail.",
  "Second step — to isolate σ² you have to take reciprocals of all three parts of the inequality. Taking reciprocals of positive quantities REVERSES the inequalities, so the two percentiles swap ends.",
  "Last step — that reversal is why the LARGER chi-square point ends up in the denominator of the LOWER limit. If your lower limit is bigger than your upper limit, you have not reversed."],
 "answer": "(1.892, 13.331).",
 "check": "Three things an examiner looks for. The degrees of freedom are n − 1 = 9, not 10. The percentiles swap ends when you take reciprocals, so 19.023 — the larger one — divides into the sum of squares to give the LOWER limit, and 2.700 gives the upper. And the interval is not symmetric about s² = 4: it runs from 1.89 to 13.33, with the upper end much further away. That asymmetry is correct and expected, because the chi-square distribution is skewed; an interval for a variance that comes out symmetric has been built wrongly.",
 "scenario": {
  "teaser": "A pharmaceutical filling line is judged on its consistency, not its average.",
  "title": "When the variance is the thing you care about",
  "body": [
   "A filling line doses syrup into bottles. The target is 100 ml and the line is well centred — the average is reliably close. What the regulator asks about is the spread, because a bottle 8 ml short is a complaint whether or not the average is perfect.",
   "So the quantity of interest is σ², and a point estimate of it is no more sufficient here than a point estimate of a mean. With ten bottles sampled you need to know how well ten bottles pin down a variance, and the answer is: not very well.",
   "That is what the interval in this section shows. The sample variance is 4, and the 95% interval runs from 1.89 to 13.33 — the upper end more than three times the estimate. Ten observations constrain a variance far more loosely than they constrain a mean, which is a genuinely useful thing to know before designing a study.",
   "The asymmetry is not a defect either. A variance is bounded below by zero and unbounded above, so the uncertainty cannot be symmetric. The chi-square distribution's skew is the honest shape of that uncertainty."],
  "q": "Why does ten observations pin down a variance so much more loosely than a mean?",
  "answer": "Because the variance is estimated from squared deviations, and squaring amplifies the sampling variation — one unusual observation moves the sum of squares a great deal. The precision of a variance estimate improves with n in the same √n fashion, but it starts from a much weaker position, which is why variance intervals are wide and why a sample of ten says so little about consistency."},
 "solution": [
  {"say": "Write the pivot and its distribution.",
   "math": "Q = Σ(xᵢ − x̄)²/σ² = (n − 1)s²/σ²  ~  chi-square with 9 df",
   "why": "Note the question gave Σ(xᵢ − x̄)² = 36 directly, so s² = 36/9 = 4. Either form of the pivot works; using the sum of squares avoids one division."},
  {"say": "Trap it between the two percentiles.",
   "math": "P( 2.700  <  36/σ²  <  19.023 ) = 0.95",
   "why": "0.025 is left in each tail. The left-hand number is the upper 0.975 point, which is the small one — the naming catches people, so read which point the question is giving you."},
  {"say": "Take reciprocals of all three parts, reversing the inequalities.",
   "math": "1/19.023  <  σ²/36  <  1/2.700",
   "why": "This is the step the whole exercise is about. Reciprocals of positive numbers reverse order, so the 19.023 moves to the left-hand end."},
  {"say": "Multiply through by the sum of squares.",
   "math": "36/19.023  <  σ²  <  36/2.700\n1.892  <  σ²  <  13.331",
   "why": "The larger chi-square point gives the lower limit, as the reversal demands."},
  {"say": "State it, and note the shape.",
   "math": "95% CI for σ²:  (1.892, 13.331),  with s² = 4\nfor σ:  (1.375, 3.651)",
   "why": "Asymmetric about 4, as it must be. For σ itself, take square roots of both ends — legitimate because the square root is increasing, so it preserves the trapping inequality. That is the invariance of an interval under a monotone transformation, and it is worth knowing: you never have to rebuild an interval for a monotone function of a parameter."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims this topic's multi-statement and conceptual questions are built from.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "The (1 − α) upper confidence bound for μ with σ unknown is (−∞, x̄ + t(α, n−1) s/√n).",
   "tf": True,
   "why": "True, and this is June 2026 Q10. 'Upper bound' means the finite end is above x̄, so the sign is plus, and the percentile is the α point because all of α sits in one tail."},
  {"claim": "A two-sided (1 − α) interval and a one-sided (1 − α) bound use the same percentile.",
   "tf": False,
   "why": "False. The two-sided interval splits α between two tails and uses the α/2 point; the one-sided bound uses the α point. At 95% with 15 df those are 2.131 and 1.753."},
  {"claim": "The t pivot for μ has n degrees of freedom.",
   "tf": False,
   "why": "False — it has n − 1. One degree of freedom is spent estimating μ by x̄, and the deviations in s² are taken about x̄ rather than about μ. Both wrong options in Q10's set used n."},
  {"claim": "To halve the width of a confidence interval for μ, the sample size must be multiplied by four.",
   "tf": True,
   "why": "True. The width is proportional to 1/√n, so to halve it you need √n doubled, which means n quadrupled. This is the same √n that governed power in topic 4.12."},
  {"claim": "A 95% confidence interval contains 95% of the sample observations.",
   "tf": False,
   "why": "False, and not nearly true. The interval is about the mean, and its width shrinks like 1/√n while the spread of the observations does not shrink at all. For large n the interval contains almost none of the data."},
  {"claim": "Raising the confidence level from 90% to 99% with the same data widens the interval.",
   "tf": True,
   "why": "True. A higher level demands a percentile further out — at 15 df the multipliers go from 1.753 to 2.947 — so the interval widens. More confidence from the same data is bought only with less precision."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 7,
 "title": "On your own — width, sample size and level",
 "objective": "Answer the three quantitative questions this topic asks about the width rather than the interval.",
 "problem": "For the two-sided interval for a normal mean: (a) how does the width depend on n? (b) By what factor must n be multiplied to halve the width? (c) A study with n = 16 gives a 95% interval of width 6.39. Roughly how wide would the 99% interval be, given t(0.005, 15) = 2.947? (d) At the same level, how does the width of the one-sided bound compare?",
 "hints": [
  "The width is twice the half-width, and the half-width is the percentile times s/√n. Only one of those three ingredients involves n.",
  "For (c) you do not need the data: the width is proportional to the percentile, so scale the known width by the ratio of the two percentiles.",
  "For (d) remember that a one-sided bound has only one finite end, so 'width' is not comparable in the same way — compare the distance from x̄ to the finite end instead."],
 "answer": "(a) proportional to 1/√n  (b) 4  (c) about 8.84  (d) the distance from x̄ is 1.753 s/√n against 2.131 s/√n, so the one-sided bound is about 18% closer in.",
 "check": "The point of (b) is that precision is expensive: four times the data for twice the precision, which is the single most useful planning fact in the topic. In (c) scaling by the percentile ratio works because everything else in the half-width is unchanged by the confidence level — this shortcut saves real time in an exam. And in (d) the comparison must be made on the distance from the centre, not on 'width', because a one-sided bound has infinite width; an option offering a width ratio for a one-sided bound is incoherent.",
 "solution": [
  {"say": "(a) Read the width off the formula.",
   "math": "width = 2 t(α/2, n−1) s/√n\nso  width  ∝  1/√n   (ignoring the slow change in t with df)",
   "why": "The percentile also changes with n through the degrees of freedom, but it settles quickly towards the normal value, so the 1/√n dependence is what matters. For n beyond about 30 the t multiplier is within a few percent of the normal one."},
  {"say": "(b) Solve for the multiplier.",
   "math": "half the width  ⟹  √n doubled  ⟹  n × 4",
   "why": "This is the answer the variant on this question wants, and it generalises: to reduce the width by a factor k you need n multiplied by k²."},
  {"say": "(c) Scale by the ratio of percentiles.",
   "math": "width(99%) = width(95%) × 2.947/2.131\n  = 6.39 × 1.383 = 8.84",
   "why": "s and n are unchanged, so the only thing that moved is the multiplier. Confirming directly: 2 × 2.947 × 1.5 = 8.84."},
  {"say": "(d) Compare the distance from the centre.",
   "math": "one-sided:  1.753 s/√n = 2.630\ntwo-sided:  2.131 s/√n = 3.197\nratio 1.753/2.131 = 0.823",
   "why": "The one-sided bound sits about 18% closer to x̄ at the same stated level. That is the gain from spending the whole α in one tail, and the cost is making no claim at all about the other direction."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "Pivots beyond the normal family",
 "objective": "See the method applied where the distribution is not normal, which is where it stops looking like a formula to memorise.",
 "blocks": [
  {"t": "formula", "h": "The exponential",
   "body": "Let X₁,…,Xₙ be iid exponential with mean θ. Then 2Σxᵢ/θ is chi-square with 2n degrees of freedom. So from\n    P( χ²(1−α/2, 2n)  <  2Σxᵢ/θ  <  χ²(α/2, 2n) ) = 1 − α\nrearranging gives the interval ( 2Σxᵢ/χ²(α/2, 2n),  2Σxᵢ/χ²(1−α/2, 2n) ) for θ."},
  {"t": "step", "h": "Why that one works",
   "body": "Each 2Xᵢ/θ is exponential with mean 2, which is a chi-square with 2 degrees of freedom; independent chi-squares add, giving 2n. Nothing unknown survives in the distribution, so it is a pivot. Note the reciprocal reversal again — the same step as the variance interval, and the same place people slip."},
  {"t": "formula", "h": "The uniform",
   "body": "For X₁,…,Xₙ iid uniform on (0, θ), the ratio U = X₍ₙ₎/θ has P(U ≤ u) = uⁿ on (0, 1), which involves no parameter. A one-sided interval follows from P(U > α^(1/n)) = 1 − α, giving the (1 − α) interval ( X₍ₙ₎,  X₍ₙ₎/α^(1/n) ) for θ."},
  {"t": "step", "h": "The common thread, and what is not required",
   "body": "A pivot is not required to be a nice ratio, to be symmetric, or to be normal. The only requirement is that its distribution is free of every unknown. Note also what the uniform case shows: the interval's lower end is X₍ₙ₎ itself, because θ cannot be smaller than the largest observation. A pivot can encode that kind of hard logical constraint, which a normal-theory formula never would."},
  {"t": "step", "h": "When no exact pivot exists",
   "body": "Often none does, and then the usual route is an approximate pivot based on large-sample normality of an estimator — (θ̂ − θ)/se(θ̂) treated as standard normal. That is what the proportion interval in the explore section was, and the explore section is also what it looks like when the approximation is poor. Exact when you can, approximate when you must, and know which one you are using."}],
 "ask": {
  "q": "In the uniform case the interval's lower end is the largest observation itself. Why can the interval not start any lower?",
  "nudge": "If one observation is 7.3, what does that tell you about θ with certainty, before any probability is involved?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the one-sided forms and the planning facts, which are what gets asked.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Write the (1 − α) upper confidence bound for μ, σ unknown.",
   "a": "(−∞, x̄ + t(α, n−1) s/√n). Upper bound means the finite end is above x̄, so the sign is plus, and the percentile is the α point."},
  {"q": "And with σ known?",
   "a": "(−∞, x̄ + z_α σ/√n). Same shape; the normal percentile replaces the t one and there are no degrees of freedom."},
  {"q": "By what factor must n grow to halve an interval's width?",
   "a": "Four. Width is proportional to 1/√n."},
  {"q": "Which chi-square percentile gives the LOWER limit of a variance interval?",
   "a": "The larger one, the upper α/2 point, because taking reciprocals reverses the inequalities."},
  {"q": "State what a 95% confidence level means.",
   "a": "That the procedure, applied repeatedly, produces intervals containing the true parameter about 95% of the time. It is not a probability about the particular interval in front of you."},
  {"q": "Is 2Σxᵢ/θ a pivot for an exponential with mean θ, and what is its distribution?",
   "a": "Yes — chi-square with 2n degrees of freedom, which involves no unknown."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Define a pivotal quantity, and check whether a proposed quantity qualifies by looking at whether its distribution is free of every unknown.",
  "Name the three standard pivots — normal mean with σ known, normal mean with σ unknown, normal variance — and their distributions with the right degrees of freedom.",
  "Run the recipe: trap the pivot between percentiles, then rearrange to isolate the parameter, reversing inequalities correctly when you negate or take reciprocals.",
  "Write both one-sided bounds for a normal mean from the shape of the interval rather than from memory, and so get the sign right.",
  "Build an interval for a variance, and expect it to be asymmetric; take square roots to get one for σ.",
  "Answer the width questions: proportional to 1/√n, four times the data to halve it, wider at a higher level, and tighter one-sided than two-sided at the same level.",
  "State correctly what a confidence level means, and reject the three wrong readings — about the data, about sample means, and as a probability for the particular interval."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "Where the standard interval for a proportion goes wrong",
 "objective": "Follow up the explore section with the actual numbers, and meet the fix.",
 "blocks": [
  {"t": "step", "h": "The interval in question",
   "body": "For a binomial proportion the textbook interval is p̂ ± z(α/2) √(p̂(1 − p̂)/n), called the Wald interval. It comes from treating (p̂ − p)/√(p̂(1 − p̂)/n) as an approximate pivot with a standard normal distribution. Both steps are approximations: the normal limit, and using p̂ in place of p in the standard error."},
  {"t": "formula", "h": "What it actually delivers",
   "body": "Exact coverage of the nominal 95% Wald interval, computed from the binomial:\n    n = 30,  p = 0.50  →  0.957\n    n = 30,  p = 0.20  →  0.946\n    n = 30,  p = 0.10  →  0.809\n    n = 30,  p = 0.05  →  0.782\n    n = 100, p = 0.05  →  0.878"},
  {"t": "step", "h": "Reading those numbers",
   "body": "At p = 0.05 with thirty observations a procedure advertising 95% delivers 78%. That is not a rounding problem; it is a procedure that does not do what it says. And the failure does not vanish with a respectable sample size — a hundred observations at p = 0.05 still leaves it at 88%. The reason is that the normal approximation to the binomial needs np and n(1 − p) both reasonably large, and np = 5 is not."},
  {"t": "step", "h": "The degenerate case",
   "body": "Worse, when p̂ = 0 the standard error computes as zero and the interval collapses to the single point 0 — a 95% interval claiming certainty. Observing no successes in thirty trials plainly does not establish that p is exactly zero. Any procedure that can return a zero-width interval is broken, and this one can."},
  {"t": "step", "h": "The fixes, and the moral",
   "body": "The Wilson score interval inverts the test using p rather than p̂ in the standard error and behaves far better; the Clopper–Pearson interval is exact by construction, obtained by inverting the binomial test, and is conservative rather than wrong. A quick practical patch is the Agresti–Coull interval, which adds two successes and two failures before applying the Wald formula. The moral is the one the explore section opened with: an interval's stated level is a claim about a procedure, and for an approximate procedure that claim needs checking rather than trusting. The normal-theory intervals in the rest of this lesson need no such check, because their pivots have exact distributions."}],
 "ask": {
  "q": "Why does the Wald interval's coverage fail at p = 0.05 but hold up at p = 0.5, for the same n = 30?",
  "nudge": "Compute np in each case. Which one satisfies the usual condition for a normal approximation to the binomial?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "inference_t13_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "inferencet13",
 "topicId": "inference-t13",
 "moduleId": "inference",
 "title": "Confidence Intervals and Pivotal Quantities",
 "breadcrumb": "Statistical Inference → Interval Estimation → Confidence intervals and pivots",
 "engine": "C",
 "engineName": "Interval estimation — a range, and how often the method gets it right",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Define a pivotal quantity and decide whether a proposed quantity is one.",
  "Construct a confidence interval by the pivot method, rearranging the inequalities correctly.",
  "Write the two-sided interval and both one-sided bounds for a normal mean, with σ known and unknown.",
  "Build an interval for a normal variance using the chi-square pivot, and explain its asymmetry.",
  "Answer the width questions: the dependence on n, the sample size to halve it, and the effect of the confidence level.",
  "State correctly what a confidence level means, and reject the standard misreadings."],
 "prereq": [
  {"id": "p1", "name": "The t and chi-square distributions",
   "why": "Every interval here ends at a percentile of one of these two. You need to know which distribution goes with which pivot, and that both carry n − 1 degrees of freedom in this setting."},
  {"id": "p2", "name": "Sampling distribution of the mean and variance",
   "why": "The pivots are built from x̄ and s². If the distribution of (x̄ − μ)/(s/√n) is not familiar, that comes first."},
  {"id": "p3", "name": "Size and power of a test",
   "why": "A confidence interval is the set of null values a test would not reject, so the α here is the same α as in topic 4.12 and the one-sided and two-sided distinction is the same distinction."},
  {"id": "p4", "name": "Rearranging inequalities",
   "why": "The one examinable skill in this topic is isolating the parameter, which means reversing inequalities when negating or taking reciprocals. Every error in the variance interval is this."}],
 "traps": [
  "An UPPER confidence bound is (−∞, U) and its finite end is ABOVE x̄, so the sign is plus.",
  "A two-sided interval uses the α/2 point; a one-sided bound uses the α point.",
  "The degrees of freedom are n − 1, not n.",
  "Taking reciprocals reverses the inequalities, so the LARGER chi-square point gives the LOWER limit for σ².",
  "The variance interval is asymmetric about s²; a symmetric one has been built wrongly.",
  "Width is proportional to 1/√n, so halving it needs four times the data.",
  "The confidence level is a property of the procedure, not a probability about the interval you have.",
  "A confidence interval for μ says nothing about where 95% of the observations lie."],
 "revision": {
  "sheet": [
   "A pivotal quantity involves the data and the parameter, but its DISTRIBUTION involves no unknown.",
   "Normal mean, σ known: pivot (x̄ − μ)/(σ/√n) ~ N(0,1).",
   "Normal mean, σ unknown: pivot (x̄ − μ)/(s/√n) ~ t with n − 1 df.",
   "Normal variance: pivot (n − 1)s²/σ² = Σ(xᵢ − x̄)²/σ² ~ chi-square with n − 1 df.",
   "Recipe: trap the pivot between percentiles at total probability 1 − α, then rearrange to isolate the parameter.",
   "Two-sided interval for μ, σ unknown: x̄ ± t(α/2, n−1) s/√n.",
   "Upper confidence bound: (−∞, x̄ + t(α, n−1) s/√n). Lower bound: (x̄ − t(α, n−1) s/√n, ∞).",
   "With σ known, replace the t point by z_α (one-sided) or z_(α/2) (two-sided); no degrees of freedom.",
   "Interval for σ²: ( (n−1)s²/χ²(α/2, n−1),  (n−1)s²/χ²(1−α/2, n−1) ) — larger point gives the lower limit.",
   "For σ, take square roots of both ends; a monotone transformation preserves the interval.",
   "Width ∝ 1/√n. To reduce the width by a factor k, multiply n by k². Halving needs n × 4.",
   "Raising the confidence level widens the interval: at 15 df the multipliers are 1.753 (90%), 2.131 (95%), 2.947 (99%).",
   "A one-sided bound at the same level is tighter than the corresponding end of the two-sided interval, because all of α is in one tail.",
   "Interpretation: the procedure covers the parameter in (1 − α) of repetitions. NOT a probability about this interval, not about where the data lie, and not about sample means.",
   "Exponential with mean θ: 2Σxᵢ/θ ~ chi-square with 2n df. Uniform on (0, θ): X₍ₙ₎/θ has cdf uⁿ.",
   "Approximate pivots give approximate levels. The Wald interval for a proportion has coverage 0.78 at n = 30, p = 0.05 against a nominal 0.95."],
  "cards": [
   ["Pivotal quantity", "A function of data and parameter whose distribution is free of every unknown"],
   ["Pivot for μ, σ unknown", "(x̄ − μ)/(s/√n), which is t on n − 1 degrees of freedom"],
   ["Pivot for σ²", "(n − 1)s²/σ², which is chi-square on n − 1 degrees of freedom"],
   ["Two-sided interval for μ", "x̄ ± t(α/2, n−1) s/√n — the α/2 point, because α is split between two tails"],
   ["Upper confidence bound", "(−∞, x̄ + t(α, n−1) s/√n) — finite end above x̄, so the sign is plus"],
   ["Lower confidence bound", "(x̄ − t(α, n−1) s/√n, ∞) — same percentile, opposite sign"],
   ["Variance interval", "Sum of squares over the chi-square points, LARGER point giving the lower limit, because reciprocals reverse"],
   ["Why it is asymmetric", "A variance is bounded below by zero and unbounded above, and the chi-square distribution is skewed"],
   ["Width and n", "Width ∝ 1/√n; multiply n by k² to reduce the width by a factor k, so four times the data halves it"],
   ["Higher confidence level", "A percentile further out, so a wider interval — more confidence costs precision"],
   ["What 95% means", "The procedure covers the true parameter in about 95% of repeated samples"],
   ["What 95% does not mean", "Not a probability about this interval, not 95% of the data, not 95% of sample means"]],
  "tricks": [
   "Write the SHAPE of a one-sided answer first — (−∞, U) or (L, ∞) — and the sign is then forced. Mnemonics fail when the wording changes.",
   "Check the standard error before anything else: s/√n, never s/n. A half-width that looks too small usually means √n was dropped.",
   "In a variance interval, verify that your lower limit is below s² and your upper limit above it. If not, the reciprocals were not reversed.",
   "To change only the confidence level of a known interval, scale its width by the ratio of the two percentiles — everything else is unchanged.",
   "If an option offers a probability statement about the particular interval, it is the wrong option in this framework."],
  "shortcuts": [
   "At 15 df: 1.753 for 90%, 2.131 for 95%, 2.947 for 99%. The one-sided 95% point IS the two-sided 90% point — that coincidence is worth knowing and is often what the question turns on.",
   "Reducing width by a factor k costs n × k². Doubling precision costs four times the data, every time.",
   "For n beyond about 30 the t multiplier is within a few percent of the normal one, so a z-based answer is a good check on arithmetic."],
  "remember": [
   "Upper bound means the finite end is above x̄. Plus sign.",
   "Two-sided takes α/2, one-sided takes α.",
   "Degrees of freedom n − 1. Reciprocals reverse. Width goes as 1/√n."]},
 "howto": "Read this in order. The opening checks matter more here than usual, because the whole topic rests on just two sampling distributions and one piece of notation — and the notation is where marks actually go, since several wrong options in a typical question differ from the right one only in which percentile was used. Sections 4, 7 and 9 are the spine: the recipe worked once with numbers, the one-sided bounds where the sign error happens, and the variance interval where the rearrangement inverts. Section 8 is the conceptual one and is worth reading twice, because the interpretation question is the one this topic asks most reliably. Attempt the question at the end of each section before opening the answer. The optional section at the end follows up the coverage chart with real numbers; it can wait for a second pass.",
 "refs": [
  {"title": "Confidence Intervals for One Mean", "where": "Lesson 14", "site": "Penn State STAT 415",
   "url": "https://online.stat.psu.edu/stat415/lesson/14", "type": "Course notes", "free": True,
   "checked": "2026-10-30",
   "why": "The pivot method applied to the normal mean with both the σ known and σ unknown cases, plus the sample-size calculation. Read it after section 4."},
  {"title": "Mathematical Statistics 18.655 — lecture notes",
   "where": "Sessions on estimation and confidence sets", "site": "MIT OpenCourseWare",
   "url": "https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type": "Lecture notes", "free": True, "checked": "2026-10-30",
   "why": "Confidence sets treated as inverted tests, which is the connection to topic 4.12 and the cleanest way to see why the α matches."},
  {"title": "Statistical Inference", "where": "Weeks on interval estimation",
   "site": "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee",
   "url": "https://archive.nptel.ac.in/noc/courses/noc21/SEM1/noc21-ma23", "type": "Video course",
   "free": True, "checked": "2026-10-30",
   "why": "Indian syllabus notation for the percentiles, including the degrees-of-freedom-first ordering that June 2026 Q10 used."},
  {"title": "Statistical Inference, 2nd edition", "where": "Sections 9.1–9.2",
   "site": "Casella and Berger", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "Pivotal quantities defined properly, and interval estimation presented as the inversion of a test."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 11",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "Worked intervals for the normal, exponential and uniform families, matching the pivots in section 12."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored October 2026 for this platform against the UGC NET Statistics syllabus, and prioritised from the June 2026 paper, where Q10 asked for the (1 − α) upper confidence bound for μ with σ unknown; the official answer is (−∞, x̄ + t(n−1, α) s/√n) and the stored response sheet shows the minus-sign option was marked, so the sign error is treated here as the lesson's central trap and is the subject of its fill-in section. The ten practice variants on that question — the two-sided interval, the lower bound, the σ² pivot, the one-sided versus two-sided multiplier, the degrees of freedom, the sample size to halve the width, the definition of a pivot, the σ known bound, the meaning of 95%, and the effect of raising the level — are each taught in a named section and each appear in the pool. Every numerical value was computed rather than recalled: the t points 2.131, 1.753 and 2.947 at 15 df, the chi-square points 19.023 and 2.700 at 9 df, the resulting intervals (49.20, 55.60), (−∞, 55.03) and (1.892, 13.331), and the exact Wald coverage figures in the optional section (0.957, 0.946, 0.809, 0.782 at n = 30 and 0.878 at n = 100). Previous-year questions themselves are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "inf-t13-m-%02d" % i, "format": fmt, "topic": "inference-t13",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "Let X₁,…,Xₙ be a random sample from an N(μ, σ²) population with σ unknown. The (1 − α) upper confidence bound for μ is:",
 ["(−∞, X̄ + t(n−1, α)·S/√n)", "(−∞, X̄ − t(n−1, α)·S/√n)",
  "(−∞, X̄ + t(n, α)·S/√n)", "(−∞, X̄ − t(n, α)·S/√n)"],
 "A",
 "An upper confidence bound is an interval (−∞, U) that bounds μ from above, so its finite end lies ABOVE x̄ and the sign is plus. The degrees of freedom are n − 1, since one was spent estimating μ by x̄. This is June 2026 Q10, where the minus-sign option was the one marked."))

I.append(q(2, "single", "easy",
 "A pivotal quantity is one whose:",
 ["distribution does not depend on the unknown parameter",
  "value does not depend on the unknown parameter",
  "value does not depend on the data",
  "distribution is always normal"],
 "A",
 "The quantity itself is allowed — indeed required — to involve the parameter; it is the DISTRIBUTION that must be free of it, and of every other unknown. A quantity whose value did not involve the parameter could not be rearranged to isolate it, and nothing requires the distribution to be normal: the chi-square pivot for σ² is not."))

I.append(q(3, "single", "easy",
 "The degrees of freedom of the t pivot (x̄ − μ)/(s/√n) for a normal mean are:",
 ["n", "n − 1", "n − 2", "2n"],
 "B",
 "One degree of freedom is used in estimating μ by x̄, and the deviations in s² are measured about x̄ rather than about μ. Both of the wrong options in June 2026 Q10's set used n, which is why this is worth being certain about."))

I.append(q(4, "order", "easy",
 "Arrange the steps of constructing a confidence interval by the pivot method in the correct order.",
 ["B, D, A, C", "D, B, A, C", "B, A, D, C", "D, A, B, C"],
 "A",
 "Find a pivot first, then decide whether the question wants a two-sided interval or a one-sided bound, because that decides which percentile you need. Only then trap the pivot and rearrange. Choosing the percentile before knowing which form is wanted is how the α/2 and α confusion arises.",
 items=["A. Trap the pivot between the chosen percentiles at total probability 1 − α",
        "B. Find a quantity involving the parameter whose distribution is free of all unknowns",
        "C. Rearrange the inequalities to isolate the parameter",
        "D. Decide whether a two-sided interval or a one-sided bound is required"]))

I.append(q(5, "single", "easy",
 "Compared with a two-sided interval at the same confidence level, a one-sided confidence bound uses:",
 ["the upper α/2 point", "the upper α point", "the upper 2α point", "the same percentile"],
 "B",
 "A two-sided interval must leave α/2 in each tail, so it uses the α/2 point. A one-sided bound has a single tail to pay for and uses the α point, which is closer in — so the bound is tighter than the corresponding end of the two-sided interval. At 15 degrees of freedom these are 2.131 and 1.753."))

I.append(q(6, "single", "easy",
 "As the confidence level is raised from 90% to 99% with the same data, the interval:",
 ["becomes narrower", "becomes wider", "is unchanged", "becomes narrower then wider"],
 "B",
 "A higher confidence level demands a percentile further out in the tail — at 15 degrees of freedom the multiplier goes from 1.753 to 2.947 — so the interval widens. More confidence from a fixed sample is bought only by giving up precision."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "A sample of n = 16 from N(μ, σ²) gives x̄ = 52.4 and s = 6.0. Using t(0.025, 15) = 2.131, the 95% confidence interval for μ is:",
 ["(49.20, 55.60)", "(50.80, 54.00)", "(49.77, 55.03)", "(40.41, 64.39)"],
 "A",
 "s/√n = 6.0/4 = 1.5, and the half-width is 2.131 × 1.5 = 3.197, giving 52.4 ± 3.20. Option B divides by n instead of √n. Option C uses the one-sided 0.05 point 1.753, which gives a 90% interval. Option D uses s itself as the standard error.",
 check="The standard error is s/√n = 1.5, not 6.0 and not 0.375. If the half-width exceeds s, the division by √n was missed."))

I.append(q(8, "numeric", "moderate",
 "For the same sample — n = 16, x̄ = 52.4, s = 6.0 — the 95% UPPER confidence bound for μ, using t(0.05, 15) = 1.753, is:",
 ["(−∞, 55.03)", "(−∞, 49.77)", "(−∞, 55.60)", "(49.77, ∞)"],
 "A",
 "The finite end is 52.4 + 1.753(1.5) = 55.03, and it lies above x̄ because the bound is an upper one. Option B has the sign wrong — the error made on June 2026 Q10. Option C is the upper end of the two-sided interval, using 2.131. Option D is the lower confidence bound, which is a different interval.",
 check="An upper bound runs (−∞, U) with U above x̄. If your finite end is below 52.4, the sign is wrong; if it is 55.60, the α/2 point was used instead of the α point."))

I.append(q(9, "single", "moderate",
 "The pivot used for a confidence interval for σ² in a normal sample with μ unknown is:",
 ["(x̄ − μ)/(s/√n)", "(n − 1)s²/σ²", "(n − 1)s²/σ", "n s²/σ²"],
 "B",
 "This quantity, equal to Σ(xᵢ − x̄)²/σ², has a chi-square distribution with n − 1 degrees of freedom, which involves no unknown parameter — so it is a pivot. The first option is the pivot for μ, not σ². The third is dimensionally wrong, and the fourth uses n rather than n − 1 and is not chi-square."))

I.append(q(10, "numeric", "moderate",
 "A sample of n = 10 from N(μ, σ²) gives Σ(xᵢ − x̄)² = 36. Using the upper 0.025 point of chi-square with 9 df = 19.023 and the upper 0.975 point = 2.700, the 95% confidence interval for σ² is:",
 ["(1.892, 13.331)", "(13.331, 1.892)", "(1.703, 11.998)", "(0.473, 3.333)"],
 "A",
 "The limits are 36/19.023 = 1.892 and 36/2.700 = 13.331. Taking reciprocals reverses the inequalities, so the LARGER chi-square point gives the LOWER limit. Option C divides by 10 rather than using the sum of squares directly, and option D divides the sum of squares by n before applying the percentiles.",
 check="The interval must straddle s² = 36/9 = 4, and must be asymmetric about it. A lower limit above 4, or a symmetric interval, means the construction is wrong."))

I.append(q(11, "numeric", "moderate",
 "To halve the width of a confidence interval for μ at a fixed confidence level, the sample size must be multiplied by approximately:",
 ["2", "4", "8", "16"],
 "B",
 "The width is proportional to 1/√n, so halving it requires √n to double, which means n multiplied by four. More generally, reducing the width by a factor k costs n multiplied by k². This is the same √n dependence that governs power in topic 4.12.",
 check="Width goes as 1/√n, never as 1/n. If your answer is 2, the square root was overlooked."))

I.append(q(12, "multi", "moderate",
 "A 95% confidence interval for μ is computed from a sample and comes out as (49.20, 55.60). Which of the following statements are correct?",
 ["A and C only", "B and D only", "A and D only", "A, B and C only"],
 "A",
 "A is true — this is the correct frequentist reading, a statement about how often the procedure succeeds. B is false: once the interval is numbers and μ is a fixed constant, μ either lies in it or does not, and no probability attaches. C is true. D is false, and badly so — the interval is about the mean, and its width shrinks like 1/√n while the spread of the observations does not shrink at all.",
 statements=["If the sampling and construction were repeated many times, about 95% of the intervals produced would contain μ.",
             "There is a 95% probability that μ lies between 49.20 and 55.60.",
             "The 95% is a property of the procedure rather than of this particular interval.",
             "About 95% of the sample observations lie between 49.20 and 55.60."],
 verdicts=verd(
  (True, "True. This is what a confidence level asserts: coverage of the fixed parameter across repeated samples."),
  (False, "False in this framework. μ is a fixed constant and the interval is now fixed numbers, so the statement is either true or false and carries no probability. A Bayesian credible interval does support this reading, but it is a different construction."),
  (True, "True, and it is the cleanest one-line summary of what a confidence level is."),
  (False, "False. A confidence interval for μ makes no claim about where individual observations lie, and for large n it contains almost none of them."))))

I.append(q(13, "single", "moderate",
 "If σ is known, the (1 − α) upper confidence bound for μ is:",
 ["(−∞, x̄ + z_α σ/√n)", "(−∞, x̄ + z_(α/2) σ/√n)",
  "(−∞, x̄ + z_α σ/n)", "(−∞, x̄ − z_α σ/√n)"],
 "A",
 "With σ known the pivot is standard normal, so the t point is replaced by the normal point and there are no degrees of freedom. It is still a one-sided bound, so the percentile is z_α and not z_(α/2); the standard error is σ/√n; and the sign is plus because an upper bound's finite end lies above x̄."))

I.append(q(14, "single", "moderate",
 "For an iid sample from an exponential distribution with mean θ, which quantity is a pivot, and what is its distribution?",
 ["Σxᵢ/θ, chi-square with n df", "2Σxᵢ/θ, chi-square with 2n df",
  "2Σxᵢ/θ, chi-square with n df", "x̄/θ, normal"],
 "B",
 "Each 2Xᵢ/θ is exponential with mean 2, which is a chi-square with 2 degrees of freedom; independent chi-squares add, so the sum of n of them has 2n degrees of freedom. The factor 2 and the doubling of the degrees of freedom go together, and dropping either one gives a quantity that is not chi-square."))

I.append(q(15, "numeric", "moderate",
 "A study with n = 16 gives a 95% interval for μ of width 6.39. Using t(0.005, 15) = 2.947 and t(0.025, 15) = 2.131, the width of the 99% interval from the same data is approximately:",
 ["8.84", "6.39", "4.62", "12.78"],
 "A",
 "Only the percentile changes, so the width scales by 2.947/2.131 = 1.383, giving 6.39 × 1.383 = 8.84. Checking directly: 2 × 2.947 × 1.5 = 8.84. Option C scales the wrong way, and option D doubles the width rather than scaling it by the percentile ratio.",
 check="Raising the confidence level must widen the interval, so the answer has to exceed 6.39. Scaling by the ratio of percentiles is valid because s and n are unchanged."))

I.append(q(16, "single", "moderate",
 "A 95% confidence interval for σ² is (1.892, 13.331). The corresponding 95% interval for σ is:",
 ["(1.375, 3.651)", "(0.946, 6.666)", "(3.580, 177.72)", "cannot be obtained without recomputing"],
 "A",
 "Take square roots of both endpoints: √1.892 = 1.375 and √13.331 = 3.651. This is legitimate because the square root is an increasing function, so it preserves the inequalities that define the interval — an interval for a monotone function of a parameter is obtained by transforming the endpoints. Option B halves the endpoints and option C squares them."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the construction of a confidence interval for σ² in a normal sample using the chi-square pivot.",
 ["A and C only", "A, C and D only", "B and C only", "C and D only"],
 "A",
 "A is true, and it is the step the whole construction turns on. B is false — the interval is asymmetric about s², and must be, because the chi-square distribution is skewed and a variance is bounded below by zero. C is true: the pivot carries n − 1 degrees of freedom. D is false; the interval for σ is obtained simply by taking square roots of the endpoints, since the square root is increasing.",
 statements=["Taking reciprocals of the inequalities reverses them, so the larger chi-square point gives the lower limit.",
             "The resulting interval is symmetric about the sample variance s².",
             "The pivot has n − 1 degrees of freedom when μ is unknown.",
             "An interval for σ cannot be obtained from the interval for σ² without a fresh construction."],
 verdicts=verd(
  (True, "True. Reciprocals of positive quantities reverse the order, which is why the larger percentile ends up dividing into the sum of squares to give the lower limit."),
  (False, "False. The chi-square distribution is skewed and a variance is bounded below by zero, so the interval is asymmetric — for s² = 4 it runs from 1.89 to 13.33. A symmetric answer indicates an error."),
  (True, "True. The deviations are taken about x̄ because μ is unknown, which costs one degree of freedom."),
  (False, "False. The square root is an increasing function, so it preserves the trapping inequalities and the endpoints can simply be square-rooted."))))

I.append(q(18, "numeric", "hard",
 "For a nominal 95% Wald interval for a binomial proportion, p̂ ± 1.96√(p̂(1 − p̂)/n), the exact coverage at n = 30 and p = 0.05 is closest to:",
 ["0.95", "0.90", "0.78", "0.99"],
 "C",
 "Computed exactly from the binomial, the coverage is 0.782 — a procedure advertising 95% delivering 78%. The normal approximation behind the 1.96 requires np and n(1 − p) both reasonably large, and np = 1.5 here. At p = 0.5 with the same n the coverage is 0.957; the failure is driven by p being near a boundary, not by n alone.",
 check="Coverage of an approximate interval can fall well short of its nominal level. Even at n = 100 with p = 0.05 it is only 0.878, so a large n does not rescue it."))

I.append(q(19, "single", "hard",
 "Which of the following is NOT a pivotal quantity for an iid N(μ, σ²) sample with both parameters unknown?",
 ["(x̄ − μ)/(s/√n)", "(n − 1)s²/σ²", "x̄ − μ", "√n(x̄ − μ)/s"],
 "C",
 "The distribution of x̄ − μ is N(0, σ²/n), which depends on the unknown σ — so it is not a pivot, even though it involves the parameter correctly. The first and fourth options are the same t pivot written two ways, and the second is the chi-square pivot; both have distributions free of every unknown. The test is always the same: look at the distribution, not the formula."))

I.append(q(20, "single", "hard",
 "For X₁,…,Xₙ iid uniform on (0, θ), the quantity X₍ₙ₎/θ has distribution function uⁿ on (0, 1). The resulting (1 − α) confidence interval for θ is:",
 ["(X₍ₙ₎, X₍ₙ₎/α^(1/n))", "(X₍ₙ₎ α^(1/n), X₍ₙ₎)",
  "(X₍ₙ₎/n, n X₍ₙ₎)", "(0, X₍ₙ₎/α^(1/n))"],
 "A",
 "Since P(X₍ₙ₎/θ > α^(1/n)) = 1 − α, rearranging gives θ < X₍ₙ₎/α^(1/n) with that probability, and θ ≥ X₍ₙ₎ holds with certainty — no value of θ below the largest observation is possible at all. So the interval runs from X₍ₙ₎ up to X₍ₙ₎/α^(1/n). The second option is below the sample maximum, which is logically impossible, and the fourth ignores the hard lower constraint."))

# A pool whose keys pile onto one letter rewards a guesser, and the validator caps any
# letter at 40%. Swapping positions i and j is its own inverse, so an "option X" mention
# inside an explanation just swaps the same two letters.
LET = "ABCD"
WANT = {"inf-t13-m-02": "C", "inf-t13-m-05": "D", "inf-t13-m-07": "C",
        "inf-t13-m-09": "D", "inf-t13-m-11": "D", "inf-t13-m-13": "C",
        "inf-t13-m-16": "B", "inf-t13-m-19": "B", "inf-t13-m-20": "D"}

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
 "moduleId": "inference", "topicId": "inference-t13", "source": "mastery",
 "label": "Confidence intervals and pivots — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
