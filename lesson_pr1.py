#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 1.1 — Order statistics (probability-t1).

PYQ anchor. June 2026 Q13 (WRONG, marked D against answer A): in samples of size 5 from U[0,1],
the mean of the distribution of the median. The median of five is X_(3), and E(X_(r)) = r/(n+1),
so the answer is 3/6 = 1/2. The marked option was 1, the mean of nothing in the problem.
Two independent one-line routes reach it: the formula, and the observation that U[0,1] is
symmetric about 1/2 so its median's expectation is 1/2 whatever n is.

Ten variants are filed under Q13 and every one is taught in a named section and present in the
pool: E(X_(2)) for n = 4; X_(r) ~ Beta(r, n-r+1); E(X_(5)) for n = 5; the cdf of the largest;
the cdf of X_(7) for a unit exponential; E(X_(1)) = theta/n; the median of any symmetric
population; the expected range from U(0,1); the joint density of all n order statistics; and
Var of the median for n = 3.

Introduces the `ord-beta` visualisation, written for this lesson.

Writes seed/lesson_pr1.json and seed/probability_t1_mastery.json.
"""
import json, io, os, re

OUT = "seed/lesson_pr1.json"
POOL = "seed/probability_t1_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Fix what an order statistic is and the two cdfs that everything else is built from.",
 "ask": {
  "q": "You have five observations. How many order statistics are there, and are they independent?",
  "nudge": "Sorting does not throw anything away. But can the second-smallest ever exceed the largest?"},
 "body": [
  "Sort a sample into increasing order and write the result X₍₁₎ ≤ X₍₂₎ ≤ … ≤ X₍ₙ₎. These are the order statistics: the same n numbers, rearranged.",
  "Rearranging looks like it should change nothing, and for the sample mean it changes nothing at all. But the DISTRIBUTION of the third-smallest of five is not the distribution of a single observation, and that is the whole subject. The sample median, the sample range, the largest flood on record, the first component to fail — each is a function of the order statistics and each has its own distribution.",
  "Two of those distributions are immediate and everything else follows from them: the largest is below x exactly when ALL observations are, and the smallest exceeds x exactly when all observations do. Both are products, because the original observations are independent.",
  "Note what sorting destroys: independence. The original Xᵢ are independent; the order statistics never are, since they are forced into a fixed order. Four checks before starting."],
 "items": [
  {"ask": "What is the cdf of the largest order statistic X₍ₙ₎?",
   "recall": "P(X₍ₙ₎ ≤ x) = [F(x)]ⁿ.",
   "refresh": [
    "The maximum is at most x precisely when every one of the n observations is at most x, and independence turns that into a product of n identical factors.",
    "Differentiating gives the density n[F(x)]ⁿ⁻¹f(x). For a unit exponential and n = 7, the cdf of the largest is (1 − e^(−x))⁷ — one of the practice variants, answered in one line.",
    "This is the single most useful formula in the topic, because so many applied questions are about a maximum: peak load, worst case, record flood."]},
  {"ask": "And the cdf of the smallest, X₍₁₎?",
   "recall": "P(X₍₁₎ ≤ x) = 1 − [1 − F(x)]ⁿ.",
   "refresh": [
    "Work with the complement: the minimum EXCEEDS x only if all n observations exceed x, which has probability [1 − F(x)]ⁿ. Subtract from 1.",
    "Do not write [F(x)]ⁿ for the minimum, or 1 − [F(x)]ⁿ. The first is the maximum; the second is P(not all below x), which is not the same event.",
    "For an exponential population this gives something remarkable: the minimum of n exponentials with mean θ is itself exponential with mean θ/n. Section 6 derives it."]},
  {"ask": "For a Beta(a, b) distribution, what are the mean and the variance?",
   "recall": "Mean a/(a + b); variance ab/((a + b)²(a + b + 1)).",
   "refresh": [
    "The Beta lives on (0, 1), which is exactly where a uniform order statistic lives — and that is not a coincidence. Section 4 shows X₍ᵣ₎ from U(0,1) IS a Beta.",
    "With a = r and b = n − r + 1 the sum a + b is n + 1, so the mean becomes r/(n+1): the single most asked fact in this topic.",
    "Beta(1, 1) is the uniform itself, which is the n = 1 case — one observation, and the order statistic is the observation."]},
  {"ask": "If a population is symmetric about μ, what is the expectation of the sample median?",
   "recall": "μ, for every sample size.",
   "refresh": [
    "Symmetry pairs X₍ᵣ₎ with X₍ₙ₋ᵣ₊₁₎ as mirror images about μ, so their expectations average to μ. The median is its own mirror image when n is odd, so its expectation must be μ itself.",
    "This answers June 2026 Q13 without any formula: U[0,1] is symmetric about 1/2, so the median of any sample from it has expectation 1/2.",
    "The sample median is therefore unbiased for the centre of any symmetric population — which is why it is the natural robust alternative to the mean."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Why the extremes are a different problem from the average",
 "objective": "See that order statistics answer questions averages cannot.",
 "body": [
  "Most of a statistics course is about the middle: means, variances, and how they behave. A great many real questions are not about the middle at all.",
  "A chain breaks at its weakest link, not at its average link. A dam must hold the worst flood in a century, not the average flood. A warranty is set by when the first failure arrives. A batch is rejected on its worst item. Every one of those is an order statistic, and none of them can be read off a mean.",
  "The second thing to notice is that the extremes are far more sensitive to n than the middle is. Take the largest of n observations from U(0,1): its expectation is n/(n+1), which creeps towards 1 as n grows — 0.833 at n = 5, 0.909 at n = 10, 0.980 at n = 50. Collect more data and the largest value you see grows, necessarily and without bound in the unbounded case. The sample mean, by contrast, settles down.",
  "That is why extremes need their own theory. An estimate of the centre gets more reliable with more data; an estimate of the maximum keeps moving."],
 "scenario": {
  "teaser": "A dam is specified against the worst flood on record and overtops nine years later.",
  "title": "Designing for a maximum using the mean",
  "body": [
   "A reservoir is to be designed for a river with eighty years of annual peak-flow records. The engineers take the largest observed peak as the design flood and add a margin. The dam overtops within a decade.",
   "The error is a confusion between two distributions. The largest value in eighty years is an observation on X₍₈₀₎, whose distribution is [F(x)]⁸⁰ — and the expected maximum over the NEXT period is not the maximum already seen. More sharply: the probability that a fresh year exceeds the largest of the previous eighty is, by symmetry alone, exactly 1/81. Over a thirty-year horizon that is not a remote event.",
   "The symmetry argument is worth seeing because it needs no distribution at all. Among eighty-one exchangeable years, each is equally likely to be the largest, so the chance that the new one takes the record is 1/81. The record is not a ceiling; it is simply the largest draw so far.",
   "The order-statistic view also supplies the right question. A design standard such as a 1-in-200-year flood is a statement about a QUANTILE of the annual distribution, not about any observed maximum, and estimating a quantile far beyond the data requires a model for the tail — which is the business of extreme value theory, the natural continuation of this topic.",
   "There is a second, quieter error in the same decision. The largest of n observations has a large variance and a skewed distribution, so it is a noisy thing to build on. The sample median, by contrast, is stable. Using the single most variable feature of the data as a design input, with a margin chosen by judgement, is as fragile as it sounds.",
   "The honest version: estimate the quantile the standard actually names, state the uncertainty in that estimate, and treat the observed maximum as one draw from a distribution rather than as a bound."],
  "q": "Why is the probability that a new year sets a record exactly 1/81, with no distributional assumption?",
  "answer": "Because the eighty-one annual peaks are exchangeable — independent and identically distributed — so every ordering of them is equally likely. Each of the eighty-one years is therefore equally likely to be the largest, and the chance that it is the new one is 1/81. The argument uses only symmetry among the years, not the shape of the distribution, which is what makes it so robust and what makes treating a record as a ceiling so clearly wrong."},
 "ask": {
  "q": "E(X₍ₙ₎) from U(0,1) is n/(n+1), which rises with n. What does that say about the common claim that more data gives a more stable estimate?",
  "nudge": "Stable around WHAT? Is there a fixed population quantity that the sample maximum is estimating?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Watch the order statistics spread out",
 "objective": "See that the means are equally spaced while the spreads are not.",
 "viz": {"type": "ord-beta", "n": 5, "r": 3,
         "caption": "The density of X₍ᵣ₎ from a sample of n uniform observations, with the smallest and largest shown faintly for contrast. Move r from 1 to n and watch the peak sweep across; change n and watch the spacing tighten."},
 "body": [
  "Start at n = 5 with r = 3 — June 2026's question. The density is Beta(3, 3), symmetric about 0.5, and the marked mean is 0.500. That is the answer, visible rather than computed.",
  "Now step r from 1 to 5 and watch the mean move: 0.167, 0.333, 0.500, 0.667, 0.833. Those are 1/6, 2/6, 3/6, 4/6, 5/6 — equally spaced, 1/(n+1) apart. The n order statistics divide the interval into n + 1 equal expected gaps, and that is true for every n.",
  "Now watch the SPREAD as r moves, because it does something most people guess backwards. The variance is largest in the middle — 0.0357 at r = 3 — and smallest at the ends, 0.0198 at r = 1 and r = 5. The extremes of a uniform sample are the most stable order statistics, not the least, because the boundaries at 0 and 1 pin them down while the middle is free to move.",
  "That is a property of the uniform, not a general law. A normal population has unbounded tails, and there the ordering reverses: its extremes are the most variable. The lesson is to read the spread off the population's shape rather than from intuition about 'extremes are wild'.",
  "Finally push n to 30. The curves narrow and crowd together, every mean at r/31, and the shape of each approaches a normal — which is why large-sample results about sample quantiles exist at all."],
 "ask": {
  "q": "The variance r(n−r+1)/((n+1)²(n+2)) is unchanged if r is replaced by n − r + 1. What does that symmetry say about X₍₁₎ and X₍ₙ₎?",
  "nudge": "Which two values of r swap into each other? And what does the uniform look like reflected about 1/2?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The density of the rᵗʰ order statistic, and the uniform case",
 "objective": "Derive the general density and specialise it to the Beta result that answers most questions.",
 "blocks": [
  {"t": "formula", "h": "The two extremes first",
   "body": "P(X₍ₙ₎ ≤ x) = [F(x)]ⁿ,            density  n[F(x)]ⁿ⁻¹ f(x)\nP(X₍₁₎ ≤ x) = 1 − [1 − F(x)]ⁿ,     density  n[1 − F(x)]ⁿ⁻¹ f(x)\nThe maximum is below x when all are; the minimum is above x when all are. Everything else in this lesson is a generalisation of these two lines."},
  {"t": "formula", "h": "The general density",
   "body": "f₍ᵣ₎(x) = [ n! / ((r−1)! (n−r)!) ] · [F(x)]^(r−1) · [1 − F(x)]^(n−r) · f(x)\nRead it as a multinomial count: r − 1 observations fall below x, one sits at x, and n − r fall above. The factorials count the ways of choosing which. Putting r = n or r = 1 recovers the two formulas above."},
  {"t": "step", "h": "The uniform case, which is most of the exam",
   "body": "For U(0,1), F(x) = x and f(x) = 1 on (0,1), so the density collapses to\n    f₍ᵣ₎(x) = [n!/((r−1)!(n−r)!)] x^(r−1) (1 − x)^(n−r),\nwhich is exactly the Beta(r, n − r + 1) density — the constant n!/((r−1)!(n−r)!) is precisely 1/B(r, n−r+1). So\n    X₍ᵣ₎ ~ Beta(r, n − r + 1).\nAt n = 5, r = 3 the constant is 30, and Beta(3,3) is the density of June 2026's median."},
  {"t": "formula", "h": "Mean and variance for the uniform",
   "body": "E(X₍ᵣ₎) = r/(n + 1)\nVar(X₍ᵣ₎) = r(n − r + 1) / ((n + 1)² (n + 2))\nThe mean follows from the Beta mean a/(a+b) with a + b = n + 1. The variance is symmetric in r ↔ n − r + 1, so X₍₁₎ and X₍ₙ₎ have equal variance, as do X₍₂₎ and X₍ₙ₋₁₎, and so on."},
  {"t": "def", "h": "The joint density of all n together",
   "body": "f(x₁, …, xₙ) = n! · f(x₁) f(x₂) ⋯ f(xₙ),   for x₁ < x₂ < ⋯ < xₙ,\nand zero otherwise. The n! counts the orderings of the original sample that produce the same sorted vector, and the restriction to an increasing region is what the sorting imposes. This is the answer to the variant asking for the joint density, and it is also the cleanest starting point for deriving anything else in the topic."},
  {"t": "step", "h": "What sorting costs: independence",
   "body": "The original observations are independent; the order statistics are not, and cannot be — X₍₂₎ ≤ X₍₃₎ always holds, which no pair of independent continuous variables satisfies. Any calculation that multiplies marginal densities of order statistics is wrong. Use the joint density above instead."}],
 "table": {
  "caption": "All five order statistics of a sample of 5 from U(0,1). Means equally spaced; variances largest in the middle.",
  "head": ["r", "distribution", "E(X₍ᵣ₎)", "Var(X₍ᵣ₎)", "sd"],
  "rows": [
   ["1 (minimum)", "Beta(1, 5)", "1/6 = 0.1667", "0.01984", "0.1409"],
   ["2", "Beta(2, 4)", "2/6 = 0.3333", "0.03175", "0.1782"],
   ["3 (median)", "Beta(3, 3)", "3/6 = 0.5000", "0.03571", "0.1890"],
   ["4", "Beta(4, 2)", "4/6 = 0.6667", "0.03175", "0.1782"],
   ["5 (maximum)", "Beta(5, 1)", "5/6 = 0.8333", "0.01984", "0.1409"]]},
 "flow": {
  "title": "Finding the distribution of an order statistic",
  "alt": "Flow chart for choosing the route to an order statistic's distribution",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "Which order statistic?", "kind": "start"},
   {"id": "b", "r": 1, "c": 0, "label": "Largest or smallest", "kind": "dec"},
   {"id": "c", "r": 1, "c": 2, "label": "A middle one", "kind": "dec"},
   {"id": "d", "r": 2, "c": 0, "label": "Fⁿ  or  1 − (1−F)ⁿ", "kind": "end"},
   {"id": "e", "r": 2, "c": 2, "label": "Population uniform?", "kind": "dec"},
   {"id": "f", "r": 3, "c": 1, "label": "Beta(r, n−r+1): E = r/(n+1)", "kind": "end"},
   {"id": "g", "r": 3, "c": 3, "label": "General density with F and f", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "a", "to": "c"},
   {"from": "b", "to": "d"}, {"from": "c", "to": "e"},
   {"from": "e", "to": "f"}, {"from": "e", "to": "g"}],
  "note": "Three routes. Extremes need one line, the uniform needs the Beta, and anything else needs the general density — which the optional section shows can always be turned into the uniform case."},
 "ask": {
  "q": "The general density has a factorial constant n!/((r−1)!(n−r)!). Why is there no factor for the single observation sitting at x?",
  "nudge": "Count the ways to split n labelled observations into a group below, one at x, and a group above. How many ways are there to arrange a group of one?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — June 2026, Q13, and the whole family around it",
 "objective": "Answer the exam question two ways and read off its neighbours.",
 "ask": {
  "q": "Both routes gave 1/2. Which one would still work if the population were normal with mean 7 instead of uniform?",
  "nudge": "One route used the specific form F(x) = x. The other used only a property of the shape."},
 "problem": "In samples of size 5 from a U[0, 1] population, find the mean of the distribution of the median. Then give the mean and variance of every order statistic of the sample.",
 "steps": [
  {"say": "Identify which order statistic the median is.",
   "math": "n = 5 is odd, so the median is the 3rd smallest: X₍₃₎\n(for even n the sample median is the average of X₍ₙ/₂₎ and X₍ₙ/₂₊₁₎)",
   "why": "Getting this wrong is the commonest way to lose the mark. With five observations, two lie below the median and two above, so r = 3."},
  {"say": "Route one — the formula.",
   "math": "X₍ᵣ₎ ~ Beta(r, n − r + 1) = Beta(3, 3)\nE(X₍₃₎) = r/(n + 1) = 3/6 = 1/2",
   "why": "The Beta mean is a/(a+b) = 3/(3+3) = 1/2. Option A. The marked option was 1, which is the upper limit of the population, not the mean of anything in the question."},
  {"say": "Route two — symmetry, with no formula at all.",
   "math": "U[0,1] is symmetric about 1/2\n⟹ E(sample median) = 1/2, for every n",
   "why": "Symmetry pairs X₍ᵣ₎ with X₍ₙ₋ᵣ₊₁₎ about the centre, and the median of an odd sample is its own mirror image, so its expectation must be the centre. Worth having, because it is instant and it generalises to any symmetric population — which answers the question above."},
  {"say": "Now the means of all five, from r/(n+1).",
   "math": "E(X₍₁₎) = 1/6 ≈ 0.1667      E(X₍₄₎) = 4/6 ≈ 0.6667\nE(X₍₂₎) = 2/6 ≈ 0.3333      E(X₍₅₎) = 5/6 ≈ 0.8333\nE(X₍₃₎) = 3/6 = 0.5000",
   "why": "Equally spaced at 1/(n+1) = 1/6. The five order statistics cut the unit interval into six equal expected pieces, which is the picture to carry away. Note E(X₍₅₎) = 5/6, one of the practice variants."},
  {"say": "And the variances, from r(n−r+1)/((n+1)²(n+2)).",
   "math": "denominator (n+1)²(n+2) = 36 × 7 = 252\nVar(X₍₁₎) = 1×5/252 = 0.01984    Var(X₍₄₎) = 4×2/252 = 0.03175\nVar(X₍₂₎) = 2×4/252 = 0.03175    Var(X₍₅₎) = 5×1/252 = 0.01984\nVar(X₍₃₎) = 3×3/252 = 0.03571",
   "why": "Largest in the middle, smallest at the ends — the opposite of the usual intuition, because the boundaries at 0 and 1 hold the extremes in place. The numerator r(n−r+1) is symmetric in r, so the variances mirror about the median."}],
 "after": "Three things to keep. The median of five from U[0,1] has mean 1/2 and you can see it from symmetry alone. The means are at r/(n+1), equally spaced. And for a uniform population the middle order statistics are the MOST variable — a fact worth remembering precisely because it contradicts the natural guess, and which reverses for a population with unbounded tails."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the core formulas before the exponential case.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "What is the cdf of X₍ₙ₎?",
   "a": "[F(x)]ⁿ — the maximum is below x exactly when all n observations are."},
  {"q": "What is the cdf of X₍₁₎?",
   "a": "1 − [1 − F(x)]ⁿ."},
  {"q": "For U(0,1), what is the distribution of X₍ᵣ₎?",
   "a": "Beta(r, n − r + 1)."},
  {"q": "Give E(X₍ᵣ₎) and Var(X₍ᵣ₎) for U(0,1).",
   "a": "r/(n+1) and r(n − r + 1)/((n+1)²(n+2))."},
  {"q": "Are order statistics independent?",
   "a": "No — they are forced into increasing order, so they cannot be."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — the exponential case",
 "objective": "Apply the extreme formulas where F is not the identity.",
 "problem": "Let X₁, …, X₇ be independent with pdf f(x) = e^(−x) for x ≥ 0 (a unit exponential). Then let X₁, …, Xₙ be exponential with mean θ. Work through the four blanks.",
 "steps": [
  {"say": "First the population cdf, since every formula needs it.",
   "blank": {"prompt": "For f(x) = e^(−x), give F(x) for x ≥ 0.",
             "answer": "F(x) = 1 − e^(−x)",
             "accept": ["1-e^-x", "1 − e^(−x)", "1-exp(-x)"],
             "hint": "Integrate e^(−t) from 0 to x."},
   "why": "The exponential cdf. Mind the parameterisation: with pdf e^(−x) the mean is 1; with (1/θ)e^(−x/θ) the mean is θ and the cdf is 1 − e^(−x/θ)."},
  {"say": "Now the cdf of the largest of the seven.",
   "blank": {"prompt": "Give P(X₍₇₎ ≤ x).",
             "answer": "(1 − e^(−x))⁷",
             "accept": ["(1-e^-x)^7", "(1 − e^(−x))^7", "(1-exp(-x))^7"],
             "hint": "The maximum is at most x exactly when all seven are. Raise F(x) to the 7th power."},
   "why": "Just [F(x)]ⁿ with n = 7. Numerically it is 0.0403 at x = 1 and 0.3614 at x = 2 — so with seven observations the largest is still below 2 only about a third of the time."},
  {"say": "Now the smallest, for the general exponential with mean θ.",
   "blank": {"prompt": "Give P(X₍₁₎ > x), and name the distribution of X₍₁₎.",
             "answer": "e^(−nx/θ); X₍₁₎ is exponential with mean θ/n",
             "accept": ["e^(-nx/theta), exponential mean theta/n",
                        "exponential with mean θ/n", "exp(-nx/θ), Exp(θ/n)"],
             "hint": "All n must exceed x, so multiply n copies of e^(−x/θ). What cdf does that give?"},
   "why": "[1 − F(x)]ⁿ = (e^(−x/θ))ⁿ = e^(−nx/θ), which is the survival function of an exponential with mean θ/n. The minimum of n exponentials is exponential again, with the rate multiplied by n — the memoryless property showing through, and the reason competing-risks and reliability calculations are so tractable."},
  {"say": "Finally its mean.",
   "blank": {"prompt": "Give E(X₍₁₎).",
             "answer": "θ/n",
             "accept": ["theta/n", "θ/n", "mean theta over n"],
             "hint": "An exponential's mean is its parameter, and you just identified the parameter."},
   "why": "θ/n, one of the practice variants. The first of n failures arrives n times sooner than a single component would fail, on average — which is exactly why a system of many parts in series fails early."}],
 "after": "Contrast the two ends. The minimum of n exponentials is exponential with mean θ/n, which shrinks to zero as n grows. The maximum has mean θ(1 + 1/2 + ⋯ + 1/n) = θHₙ, which grows like θ ln n — slowly but without limit. For n = 7 and θ = 1 that is 2.5929. Same population, same sample, and the two extremes behave in completely different ways."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "The median, the range, and what symmetry gives free",
 "objective": "Handle the two derived statistics most often asked, and the symmetry shortcut.",
 "blocks": [
  {"t": "def", "h": "The sample median",
   "body": "For odd n = 2m + 1 the median is X₍ₘ₊₁₎; for even n it is the average of X₍ₙ/₂₎ and X₍ₙ/₂₊₁₎. For U(0,1) with odd n it is Beta(m+1, m+1), symmetric about 1/2, with mean 1/2 and variance (m+1)²/((n+1)²(n+2)). At n = 3 that is Beta(2,2) with variance 4/(16×5) = 1/20 = 0.05 — one of the practice variants."},
  {"t": "formula", "h": "Symmetry: the shortcut worth having",
   "body": "If the population is symmetric about μ, then for every r\n    E(X₍ᵣ₎) + E(X₍ₙ₋ᵣ₊₁₎) = 2μ,\nand in particular the sample median of an odd sample has expectation μ. So the sample median is unbiased for the centre of ANY symmetric population — normal, uniform, Cauchy, t — which is why it is the standard robust estimator of location. For a skewed population it is not unbiased for the mean, and does not claim to be."},
  {"t": "formula", "h": "The sample range",
   "body": "R = X₍ₙ₎ − X₍₁₎. Expectation is just the difference of two expectations, since expectation is linear whether or not the two are independent:\n    E(R) = E(X₍ₙ₎) − E(X₍₁₎).\nFor U(0,1) that is n/(n+1) − 1/(n+1) = (n − 1)/(n + 1) — one of the practice variants. It gives 1/3 at n = 2, 2/3 at n = 5, 0.818 at n = 10 and 0.905 at n = 20: the range creeps towards the full interval, never reaching it."},
  {"t": "step", "h": "Why the range needs the joint density and the mean does not",
   "body": "E(R) needs only linearity, so the dependence between X₍₁₎ and X₍ₙ₎ is irrelevant. Var(R) is a different matter: Var(R) = Var(X₍ₙ₎) + Var(X₍₁₎) − 2Cov(X₍₁₎, X₍ₙ₎), and that covariance is NOT zero, so the joint density is needed. Treating order statistics as independent is the standard error in this topic, and it bites on variances, never on means."},
  {"t": "def", "h": "Quantiles, for large n",
   "body": "Fix a proportion p and track X₍ᵣ₎ with r ≈ np. For large n this sample quantile is approximately normal about the population quantile ξₚ with variance p(1 − p)/(n f(ξₚ)²). Two readings: precision improves at the usual rate 1/n, and it is worst where the density is low — which is why extreme quantiles are hard to estimate however much data there is."}],
 "ask": {
  "q": "E(R) = E(X₍ₙ₎) − E(X₍₁₎) needs no independence, but Var(R) does need the covariance. Why the difference?",
  "nudge": "Which of the two operations, expectation or variance, is linear?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — the range, and a median under symmetry",
 "objective": "Apply both derived statistics, and see what symmetry buys.",
 "problem": "(a) For a sample of n from U(0,1), find E(X₍₁₎), E(X₍ₙ₎) and E(R). (b) Evaluate at n = 5 and n = 20. (c) A sample of 9 is drawn from a normal population with mean 7 and sd 2. What is E(sample median)? (d) Is the sample median of 9 observations from an exponential population with mean 7 equal to 7 in expectation?",
 "hints": [
  "For (a), put r = 1 and r = n into r/(n+1), then subtract — linearity needs no independence.",
  "For (c), is the normal symmetric, and about what?",
  "For (d), is the exponential symmetric? And where does its median sit relative to its mean?"],
 "answer": "(a) 1/(n+1), n/(n+1), and (n−1)/(n+1). (b) 2/3 at n = 5 and 19/21 ≈ 0.905 at n = 20. (c) 7, exactly. (d) No — the exponential is skewed, and its population median is 7 ln 2 ≈ 4.85.",
 "check": "Part (d) is the one that catches people. Symmetry is what makes the median unbiased for the centre, and the exponential has none: its population median is θ ln 2 ≈ 0.693θ, well below its mean θ. The sample median of 9 observations estimates about 4.85, not 7. So 'the median is unbiased' is a statement about symmetric populations, and quoting it for a skewed one is the error the variant on symmetric populations is testing.",
 "scenario": {
  "teaser": "Two analysts summarise the same incomes and disagree by a factor of two, and both are right.",
  "title": "The median is not a robust version of the mean",
  "body": [
   "A team reports household incomes for a district. One analyst gives the mean, another the median, and the median comes out far lower. A manager asks which is correct, assuming one must be wrong.",
   "Both are correct, and they are estimating different things. Income distributions are strongly right-skewed, and for a skewed population the mean and the median are genuinely different population quantities. The sample median is a good estimate of the population median; it is not a robust estimate of the population mean.",
   "The confusion comes from how the median is usually introduced — as the resistant alternative to the mean, the summary that outliers cannot drag around. That is true, and it is why the median is preferred when a few extreme values are recording errors rather than real observations. But resistance to outliers is not the same as estimating the same target.",
   "The precise statement is the one from section 7: if the population is symmetric about μ, the sample median has expectation μ, and the mean does too, so the two estimate the same thing and the median is the robust choice. If the population is not symmetric, they estimate different numbers and the choice is a choice of question, not of method.",
   "For an exponential population with mean θ the gap is exact and large: the median is θ ln 2, about 69% of the mean. Reporting a median where a total matters — a budget, an aggregate liability — understates it badly, because a total depends on the mean and on nothing else.",
   "So the question to settle first is which population quantity the decision needs. If it is a typical household, the median. If it is the district's total income, the mean, outliers and all — and then the right response to suspect outliers is to investigate them, not to switch summaries."],
  "q": "If the median is resistant to outliers and the mean is not, why is the median the wrong summary when a total is wanted?",
  "answer": "Because a total is n times the mean by definition, and nothing else determines it. The median answers a different question — what a typical value is — and for a skewed population that is a genuinely different number, around 69% of the mean for an exponential. Resistance to outliers makes the median a better estimate of the population MEDIAN when the data are contaminated; it never makes it an estimate of the mean. If extreme values are suspected of being errors, the fix is to examine them, since for a total they are precisely the observations that matter most."},
 "solution": [
  {"say": "(a) The two extremes and their difference.",
   "math": "E(X₍₁₎) = 1/(n+1)\nE(X₍ₙ₎) = n/(n+1)\nE(R) = n/(n+1) − 1/(n+1) = (n − 1)/(n + 1)",
   "why": "Both from r/(n+1), and the subtraction is legitimate because expectation is linear — the dependence between the minimum and the maximum does not enter."},
  {"say": "(b) Evaluate.",
   "math": "n = 5:  E(R) = 4/6 = 2/3 ≈ 0.6667\nn = 20: E(R) = 19/21 ≈ 0.9048",
   "why": "The expected range approaches 1 but never attains it; there is always expected gap 1/(n+1) at each end."},
  {"say": "(c) The normal case, by symmetry.",
   "math": "the normal is symmetric about its mean, here 7\n⟹ E(sample median) = 7, exactly, for every n",
   "why": "No Beta, no integration, and the sd of 2 is irrelevant to the expectation. Symmetry alone fixes it."},
  {"say": "(d) The exponential case.",
   "math": "the exponential is right-skewed, not symmetric\npopulation median solves 1 − e^(−m/θ) = 1/2 ⟹ m = θ ln 2\nwith θ = 7:  m = 7 × 0.6931 = 4.852",
   "why": "So the sample median estimates about 4.85, not 7. The symmetry result simply does not apply, and the gap of 31% is not a small correction."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims the variants on this topic are built from.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "The cdf of the largest order statistic is [F(x)]ⁿ.",
   "tf": True,
   "why": "True. The maximum is at most x exactly when all n observations are, and independence makes that a product of n identical factors."},
  {"claim": "For a sample of n from U(0,1), X₍ᵣ₎ follows Beta(r, n − r + 1).",
   "tf": True,
   "why": "True. Substituting F(x) = x and f(x) = 1 into the general density gives exactly the Beta(r, n−r+1) density, with the factorial constant equal to 1/B(r, n−r+1)."},
  {"claim": "Order statistics from an independent sample are themselves independent.",
   "tf": False,
   "why": "False, and it is the main trap. Sorting forces X₍₁₎ ≤ X₍₂₎ ≤ ⋯, which no independent continuous variables satisfy. Multiplying marginal densities of order statistics is always wrong; use the joint density n!∏f(xᵢ) on the increasing region."},
  {"claim": "The joint density of all n order statistics is n! f(x₁)⋯f(xₙ) on x₁ < ⋯ < xₙ.",
   "tf": True,
   "why": "True. The n! counts the orderings of the original labelled sample that sort to the same vector, and the density is zero outside the increasing region."},
  {"claim": "For a uniform population the extreme order statistics have larger variance than the middle ones.",
   "tf": False,
   "why": "False for the uniform — the reverse holds. At n = 5 the median's variance is 0.0357 against 0.0198 at either end, because the boundaries at 0 and 1 pin the extremes down. The claim IS true for a population with unbounded tails, such as the normal, so it is the population's shape that decides."},
  {"claim": "The sample median is unbiased for the population mean.",
   "tf": False,
   "why": "False in general; true only when the population is symmetric. For an exponential with mean θ the population median is θ ln 2 ≈ 0.693θ, so the sample median estimates something about 31% below the mean."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 7,
 "title": "On your own — four quick ones",
 "objective": "Apply the formulas at the speed the exam needs.",
 "problem": "(a) For n = 4 from U(0,1), find E(X₍₂₎). (b) For n = 5 from U(0,1), find E(X₍₅₎). (c) For n = 3 from U(0,1), find Var of the median. (d) Ten independent components each have exponential lifetime with mean 500 hours. What is the expected time to the first failure, and to the last?",
 "hints": [
  "For (a), (b) and (c), use r/(n+1) and r(n−r+1)/((n+1)²(n+2)); identify r first.",
  "For (c), the median of 3 is X₍₂₎.",
  "For (d), the minimum of n exponentials is exponential with mean θ/n; the maximum has mean θHₙ."],
 "answer": "(a) 2/5 = 0.4. (b) 5/6 ≈ 0.8333. (c) 1/20 = 0.05. (d) 50 hours to the first failure, and 500 × H₁₀ ≈ 1464 hours to the last.",
 "check": "Two checks worth doing. In (c), Beta(2,2) has variance ab/((a+b)²(a+b+1)) = 4/(16 × 5) = 0.05, which agrees with r(n−r+1)/((n+1)²(n+2)) = 4/(16 × 5) — the two routes must agree and it is a quick way to catch a slip. In (d), note the asymmetry: the first failure is expected at a thirtieth of the time of the last. Ten components in series fail at 50 hours on average; ten in parallel last nearly 1500.",
 "solution": [
  {"say": "(a) n = 4, second smallest.",
   "math": "E(X₍₂₎) = r/(n+1) = 2/5 = 0.4",
   "why": "Equivalently Beta(2, 3) with mean 2/(2+3) = 0.4. The four order statistics sit at 0.2, 0.4, 0.6, 0.8."},
  {"say": "(b) n = 5, the maximum.",
   "math": "E(X₍₅₎) = 5/6 ≈ 0.8333",
   "why": "Also from the maximum's own density 5x⁴ on (0,1), whose mean is 5/6. Both routes agree, as they must."},
  {"say": "(c) n = 3, the median is X₍₂₎.",
   "math": "X₍₂₎ ~ Beta(2, 2)\nVar = r(n−r+1)/((n+1)²(n+2)) = 2×2/(16 × 5) = 4/80 = 1/20 = 0.05",
   "why": "Note (n+1)² = 16 and (n+2) = 5. With only three observations the median has sd √0.05 ≈ 0.224, which is a quarter of the whole interval — a reminder of how little three observations pin down."},
  {"say": "(d) Ten exponential components, θ = 500.",
   "math": "first failure: X₍₁₎ ~ exponential with mean θ/n = 500/10 = 50 hours\nlast failure:  E(X₍₁₀₎) = θ H₁₀ = 500 × (1 + 1/2 + ⋯ + 1/10)\n             = 500 × 2.928968 = 1464.48 hours",
   "why": "The minimum's mean falls as 1/n while the maximum's grows like ln n. A series system of ten such components has a mean life of 50 hours; a parallel system lasts about 1464."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "Where order statistics reappear",
 "objective": "Recognise the topic across the rest of the syllabus.",
 "blocks": [
  {"t": "step", "h": "In non-parametric testing (module 5)",
   "body": "The sign test, the median test, the Wilcoxon and Mann–Whitney statistics and every rank procedure are functions of order statistics. Distribution-free confidence intervals for a median are built directly from a pair of order statistics, with coverage computed from the binomial — no population shape needed, which is the whole appeal."},
  {"t": "step", "h": "In estimation (module 4)",
   "body": "For U(0, θ) the MLE is X₍ₙ₎, and it is biased: E(X₍ₙ₎) = nθ/(n+1), so the unbiased version is (n+1)X₍ₙ₎/n. X₍ₙ₎ is also the complete sufficient statistic for θ, which makes it the starting point for Lehmann–Scheffé on that family (topic 4.3). Order statistics are jointly sufficient for ANY continuous population, since the sorted sample carries everything the sample does bar the labels."},
  {"t": "step", "h": "In reliability and survival work",
   "body": "A series system fails at X₍₁₎ and a parallel system at X₍ₙ₎, so system lifetime distributions are order-statistic distributions. Censoring at the rᵗʰ failure stops the experiment at X₍ᵣ₎, and the theory of that design is this topic."},
  {"t": "step", "h": "In extreme value theory",
   "body": "The limiting behaviour of X₍ₙ₎, suitably normalised, is one of only three distributions — Gumbel, Fréchet or Weibull. That is the proper tool for the dam problem in section 2, and it is the extreme-value analogue of the central limit theorem."},
  {"t": "def", "h": "The common thread",
   "body": "Every one of these begins by replacing the sample with its sorted version and then asking for the distribution of one position in that order. Whenever a question concerns a maximum, a minimum, a median, a rank or a quantile, the first move is to write down [F(x)]ⁿ, 1 − [1 − F(x)]ⁿ, or the general density — and the rest is algebra."}],
 "ask": {
  "q": "For U(0, θ) the MLE X₍ₙ₎ has expectation nθ/(n+1). How does that follow from what this lesson established for U(0,1)?",
  "nudge": "If U is uniform on (0,1), what is the distribution of θU? And what does scaling do to an expectation?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the derived statistics and the warnings.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "For U(0,1), what is E(sample range)?",
   "a": "(n − 1)/(n + 1), being n/(n+1) − 1/(n+1)."},
  {"q": "The minimum of n exponentials with mean θ is what?",
   "a": "Exponential with mean θ/n."},
  {"q": "And the expected maximum of n exponentials with mean θ?",
   "a": "θHₙ = θ(1 + 1/2 + ⋯ + 1/n), which grows like θ ln n."},
  {"q": "Write the joint density of all n order statistics.",
   "a": "n! f(x₁)⋯f(xₙ) on x₁ < ⋯ < xₙ, and zero elsewhere."},
  {"q": "For U(0,1) with n = 5, which order statistic has the largest variance?",
   "a": "The median X₍₃₎, at 0.0357 against 0.0198 at the ends — the boundaries pin the extremes down."},
  {"q": "When is the sample median unbiased for the population mean?",
   "a": "Only when the population is symmetric. For an exponential the population median is θ ln 2."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Write the cdf and density of the largest and smallest order statistics for any population.",
  "Write the general density of X₍ᵣ₎ and explain its factorial constant as a multinomial count.",
  "Show that X₍ᵣ₎ from U(0,1) is Beta(r, n − r + 1), and use E = r/(n+1) and Var = r(n−r+1)/((n+1)²(n+2)).",
  "Answer June 2026 Q13 two ways: by the formula, and by symmetry in one line.",
  "Handle the exponential case: minimum exponential with mean θ/n, maximum with mean θHₙ.",
  "Give E(range) = (n−1)/(n+1) for U(0,1), and say why the mean needs no independence while the variance does.",
  "State the joint density n!∏f(xᵢ), and never multiply marginal densities of order statistics.",
  "Say when the sample median is unbiased for the mean, and what it estimates when it is not."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "Why it is always the uniform case underneath",
 "objective": "See the transform that reduces every continuous population to U(0,1).",
 "blocks": [
  {"t": "step", "h": "The probability integral transform",
   "body": "If X is continuous with cdf F, then U = F(X) is exactly Uniform(0, 1). The proof is one line: P(F(X) ≤ u) = P(X ≤ F⁻¹(u)) = F(F⁻¹(u)) = u. So every continuous population is a relabelled uniform."},
  {"t": "step", "h": "And it preserves order",
   "body": "F is non-decreasing, so sorting the Xᵢ sorts the Uᵢ in the same order:\n    U₍ᵣ₎ = F(X₍ᵣ₎).\nTherefore F(X₍ᵣ₎) ~ Beta(r, n − r + 1) for EVERY continuous population. The Beta result is not a special fact about the uniform; it is the general fact, seen on the one scale where it is visible."},
  {"t": "formula", "h": "What that buys",
   "body": "Any quantile of X₍ᵣ₎ follows from the corresponding Beta quantile:\n    the p-quantile of X₍ᵣ₎ is F⁻¹( Beta(r, n−r+1) p-quantile ).\nSo an exact confidence interval for a population quantile can be written down from the Beta — or equivalently from the binomial — with no assumption about shape. That is the machinery behind distribution-free intervals in non-parametric statistics."},
  {"t": "step", "h": "Why the variances flip between populations",
   "body": "On the uniform scale, Var(U₍ᵣ₎) is always largest in the middle. Moving back to X stretches that scale by the factor 1/f, since dx/du = 1/f(x). For the uniform f = 1 everywhere, so the pattern survives: middle most variable. For the normal, f is tiny in the tails, so the stretching there is enormous and it overwhelms the pattern, making the extremes the most variable. One picture explains both, and the stretching factor 1/f is the same quantity that appears in the large-sample variance of a sample quantile, p(1−p)/(n f(ξₚ)²)."},
  {"t": "def", "h": "The one-sentence version",
   "body": "Order statistics are the uniform order statistics read through F⁻¹. Everything else — the Beta, the equal spacing at r/(n+1), the flip in the variance pattern, the distribution-free intervals — is a consequence of that single statement."}],
 "ask": {
  "q": "F(X₍ᵣ₎) ~ Beta(r, n−r+1) for every continuous population. Why does that NOT make E(X₍ᵣ₎) = F⁻¹(r/(n+1))?",
  "nudge": "Is the expectation of a non-linear function of a variable the same function of its expectation?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "probability_t1_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "probabilityt1",
 "topicId": "probability-t1",
 "moduleId": "probability",
 "title": "Order Statistics",
 "breadcrumb": "Probability → Order statistics → Distributions of the sorted sample",
 "engine": "B",
 "engineName": "Probability — the distribution of a position in the sorted sample",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Write the cdf and density of the largest and smallest order statistics for any population.",
  "State the general density of X₍ᵣ₎ and read its constant as a multinomial count.",
  "Show that X₍ᵣ₎ from U(0,1) is Beta(r, n−r+1) and use its mean and variance.",
  "Handle the exponential case, including the minimum's mean θ/n and the maximum's θHₙ.",
  "Compute the expected range and the median's distribution, and use the symmetry shortcut.",
  "State the joint density of all n order statistics and why they are never independent."],
 "prereq": [
  {"id": "p1", "name": "Cumulative distribution functions",
   "why": "Every formula in this topic is built from F and f; the extremes are powers of F."},
  {"id": "p2", "name": "The Beta distribution",
   "why": "The uniform order statistics ARE Beta variables, and most questions are answered from the Beta mean and variance."},
  {"id": "p3", "name": "Independence and joint densities",
   "why": "The derivation uses independence of the original sample, and the key warning is that the order statistics lose it."},
  {"id": "p4", "name": "The exponential distribution",
   "why": "The second worked case is exponential, and its memoryless property is what makes the minimum exponential again."}],
 "traps": [
  "The median of n = 5 is X₍₃₎, not X₍₂₎ or the average of two values.",
  "Order statistics are NOT independent — never multiply their marginal densities.",
  "The cdf of the minimum is 1 − [1 − F]ⁿ, not 1 − Fⁿ and not [F]ⁿ.",
  "For U(0,1) the MIDDLE order statistics are the most variable; the pattern reverses for the normal.",
  "The sample median is unbiased for the mean only if the population is symmetric.",
  "E(range) needs only linearity; Var(range) needs the covariance, which is not zero.",
  "E(X₍ₙ₎) for U(0,θ) is nθ/(n+1), so the MLE is biased.",
  "Mind the exponential's parameterisation: pdf e^(−x) has mean 1; (1/θ)e^(−x/θ) has mean θ."],
 "revision": {
  "sheet": [
   "P(X₍ₙ₎ ≤ x) = [F(x)]ⁿ, density n[F(x)]ⁿ⁻¹f(x).",
   "P(X₍₁₎ ≤ x) = 1 − [1 − F(x)]ⁿ, density n[1 − F(x)]ⁿ⁻¹f(x).",
   "General density: f₍ᵣ₎(x) = [n!/((r−1)!(n−r)!)] F^(r−1) (1−F)^(n−r) f — a multinomial count.",
   "For U(0,1): X₍ᵣ₎ ~ Beta(r, n − r + 1); the factorial constant equals 1/B(r, n−r+1).",
   "E(X₍ᵣ₎) = r/(n+1); the n means are equally spaced 1/(n+1) apart.",
   "Var(X₍ᵣ₎) = r(n−r+1)/((n+1)²(n+2)), symmetric in r ↔ n−r+1.",
   "June 2026 Q13: median of n = 5 from U[0,1] is X₍₃₎ ~ Beta(3,3), mean 3/6 = 1/2.",
   "n = 5 table: means 1/6, 2/6, 3/6, 4/6, 5/6; variances 0.01984, 0.03175, 0.03571, 0.03175, 0.01984.",
   "For U(0,1) the median is the MOST variable order statistic; for the normal the extremes are.",
   "Symmetry about μ: E(X₍ᵣ₎) + E(X₍ₙ₋ᵣ₊₁₎) = 2μ, so the sample median has expectation μ.",
   "Exponential mean θ: X₍₁₎ ~ exponential with mean θ/n; E(X₍ₙ₎) = θHₙ ~ θ ln n.",
   "Unit exponential, n = 7: P(X₍₇₎ ≤ x) = (1 − e^(−x))⁷, which is 0.0403 at x = 1 and 0.3614 at x = 2.",
   "E(range) for U(0,1) = (n−1)/(n+1): 1/3 at n = 2, 2/3 at n = 5, 0.905 at n = 20.",
   "Joint density of all n: n! f(x₁)⋯f(xₙ) on x₁ < ⋯ < xₙ, zero elsewhere.",
   "n = 3 from U(0,1): median is Beta(2,2) with variance 4/(16×5) = 1/20 = 0.05.",
   "Reliability: series system fails at X₍₁₎, parallel at X₍ₙ₎. Ten components of mean 500 h give 50 h and 1464 h.",
   "For U(0,θ): MLE is X₍ₙ₎ with E = nθ/(n+1), so (n+1)X₍ₙ₎/n is unbiased.",
   "Probability integral transform: F(X₍ᵣ₎) ~ Beta(r, n−r+1) for EVERY continuous population."],
  "cards": [
   ["cdf of the maximum", "[F(x)]ⁿ"],
   ["cdf of the minimum", "1 − [1 − F(x)]ⁿ"],
   ["X₍ᵣ₎ from U(0,1)", "Beta(r, n − r + 1)"],
   ["E(X₍ᵣ₎) for U(0,1)", "r/(n+1) — equally spaced"],
   ["Var(X₍ᵣ₎) for U(0,1)", "r(n−r+1)/((n+1)²(n+2))"],
   ["Median of 5 from U[0,1]", "X₍₃₎ ~ Beta(3,3), mean 1/2"],
   ["Minimum of n exponentials", "Exponential with mean θ/n"],
   ["Expected maximum of n exponentials", "θHₙ, growing like θ ln n"],
   ["E(range) for U(0,1)", "(n − 1)/(n + 1)"],
   ["Joint density of all n", "n! ∏f(xᵢ) on x₁ < ⋯ < xₙ"],
   ["Are they independent?", "Never — sorting forces the order"],
   ["Sample median unbiased for the mean?", "Only if the population is symmetric"]],
  "tricks": [
   "Identify r first. For odd n the median is X₍(n+1)/2₎ — with n = 5 that is X₍₃₎.",
   "For a symmetric population, the median's expectation is the centre; no formula needed.",
   "For an extreme, write the event in words first — 'all below x' or 'all above x' — then take the product.",
   "Check a Beta answer two ways: r/(n+1) against a/(a+b), and the variance formula against ab/((a+b)²(a+b+1)).",
   "For U(0,θ), scale: everything is θ times the U(0,1) answer, so E(X₍ᵣ₎) = rθ/(n+1).",
   "If a question needs a variance of a difference of order statistics, you need the covariance — it is not zero."],
  "shortcuts": [
   "(n+1)²(n+2) at n = 5 is 36 × 7 = 252, so the variances are r(6−r)/252.",
   "Hₙ for n = 7 is 2.5929 and for n = 10 is 2.9290 — worth knowing for reliability questions.",
   "The exponential's population median is θ ln 2 ≈ 0.693θ, always below its mean."],
  "remember": [
   "Maximum is Fⁿ; minimum is 1 − (1−F)ⁿ.",
   "E(X₍ᵣ₎) = r/(n+1), equally spaced.",
   "Sorting destroys independence."]},
 "howto": "Start with the four checks, then go to the interactive chart in section 2 — sweeping r from 1 to n and watching the mean step along by 1/(n+1) while the spread changes is the fastest way to own this topic. Section 4 is June 2026's own question, answered twice: by the formula and by a one-line symmetry argument worth preferring in the exam. Section 6 drills the exponential case, which is where the extreme formulas have to be used rather than quoted. Sections 7 and 8 cover the median and the range, and section 8's part (d) is the one most people get wrong — the median is unbiased for the mean only under symmetry. If short of time, sections 2, 3, 4 and 6 are the lesson. The optional section shows that F(X₍ᵣ₎) is Beta for EVERY continuous population, so the uniform case is not a special case at all; it also explains why the variance pattern flips between the uniform and the normal.",
 "refs": [
  {"title": "Order Statistics", "where": "Lessons 25 and 26",
   "site": "Penn State STAT 414", "url": "https://online.stat.psu.edu/stat414/",
   "type": "Course notes", "free": True, "checked": "2026-11-03",
   "why": "Derives the general density and the uniform Beta result with worked numerical examples."},
  {"title": "Statistical Inference, 2nd edition", "where": "Section 5.4",
   "site": "Casella and Berger", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The standard treatment: joint and marginal densities of order statistics, and the uniform and exponential cases."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 4",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "Order statistics at exactly the level the NET syllabus sets, with the range and median results stated explicitly."},
  {"title": "Probability and Statistics", "where": "Weeks on order statistics",
   "site": "NPTEL / SWAYAM", "url": "https://archive.nptel.ac.in/courses/111105090",
   "type": "Video course", "free": True, "checked": "2026-11-03",
   "why": "Indian-syllabus notation and the numerical style these questions are posed in."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026, the third lesson of the probability module. PYQ anchor: June 2026 Q13 (answered wrongly, marked D against answer A) — the mean of the median of 5 observations from U[0,1], which is E(X₍₃₎) = r/(n+1) = 1/2; the marked option was 1, the population's upper limit. Taught with two independent routes, the formula and a one-line symmetry argument, since the symmetry route generalises to any symmetric population and is itself one of the ten variants. All ten variants filed under Q13 are taught in named sections and present in the pool. Every figure was computed and cross-checked against a 300,000-to-400,000-sample simulation: the means r/(n+1) and variances r(n−r+1)/((n+1)²(n+2)) at (n,r) = (5,3), (4,2), (5,5), (3,2), (5,1), (10,1) and (10,10); the expected range (n−1)/(n+1) at n = 2, 5, 10, 20; the exponential minimum's mean θ/n and maximum's mean θHₙ at (n,θ) = (7,1), (5,2) and (10,3); the cdf (1−e^(−x))⁷ at x = 0.5, 1 and 2; and the median of a symmetric normal population. The counter-intuitive result that for the uniform the MIDDLE order statistics are the most variable (0.0357 against 0.0198 at n = 5) was confirmed both ways and is taught explicitly, with the contrast to the normal case explained in the optional section via the 1/f stretching factor. Introduces the `ord-beta` visualisation, written for this lesson; its means and variances were checked against the independently computed values at seven (n, r) pairs and its r control clamps to n. Previous-year questions are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "pr-t1-m-%02d" % i, "format": fmt, "topic": "probability-t1",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "numeric", "easy",
 "In samples of size 5 from a U[0, 1] population, the mean of the distribution of the median is:",
 ["1/2", "1/3", "1/4", "1"],
 "A",
 "The median of five observations is X₍₃₎, and E(X₍ᵣ₎) = r/(n+1) = 3/6 = 1/2. Equivalently X₍₃₎ ~ Beta(3,3), whose mean is 3/(3+3). Quicker still: U[0,1] is symmetric about 1/2, so its sample median has expectation 1/2 for every n. This is June 2026 Q13.",
 check="Option D, 1, is the population's upper limit, not a mean. Any answer outside (0,1) or at an endpoint should be rejected immediately."))

I.append(q(2, "single", "easy",
 "For a sample of size n from U(0, 1), the rᵗʰ order statistic follows:",
 ["Beta(r, n − r + 1)", "Beta(r, n − r)", "Beta(n − r + 1, r)", "Gamma(r, n)"],
 "A",
 "Substituting F(x) = x and f(x) = 1 into the general density gives [n!/((r−1)!(n−r)!)] x^(r−1)(1−x)^(n−r), which is exactly the Beta(r, n−r+1) density. Note the parameters sum to n + 1, which is what makes the mean r/(n+1). Option C reverses them, giving the distribution of X₍ₙ₋ᵣ₊₁₎."))

I.append(q(3, "single", "easy",
 "The cdf of the largest order statistic X₍ₙ₎ is:",
 ["[F(x)]ⁿ", "1 − [1 − F(x)]ⁿ", "1 − [F(x)]ⁿ", "n[F(x)]ⁿ⁻¹"],
 "A",
 "The maximum is at most x exactly when all n observations are, and independence makes that a product of n identical factors. Option B is the cdf of the MINIMUM, and option D is the density of the maximum rather than its cdf."))

I.append(q(4, "numeric", "easy",
 "For a sample of size 4 from U(0, 1), E(X₍₂₎) is:",
 ["2/5", "1/3", "2/4", "1/5"],
 "A",
 "E(X₍ᵣ₎) = r/(n+1) = 2/5 = 0.4. Equivalently Beta(2, 3) has mean 2/(2+3). The four order statistics have means 0.2, 0.4, 0.6 and 0.8 — equally spaced at 1/(n+1) = 0.2.",
 check="The denominator is n + 1 = 5, not n = 4. Option C uses n and is the standard slip."))

I.append(q(5, "numeric", "easy",
 "For a sample of size 5 from U(0, 1), E(X₍₅₎) is:",
 ["5/6", "1/6", "4/6", "1"],
 "A",
 "The maximum is r = n = 5, so E = 5/(5+1) = 5/6 ≈ 0.8333. Checking independently, the maximum's density is 5x⁴ on (0,1), whose mean is ∫5x⁵dx = 5/6. The maximum's mean approaches 1 as n grows but never reaches it.",
 check="The expected maximum must be below 1 and above 1/2, which rules out options B and D at once."))

I.append(q(6, "single", "easy",
 "For a population with pdf f(x) = e^(−x), x ≥ 0, the cdf of X₍₇₎ in a sample of size 7 is:",
 ["(1 − e^(−x))⁷", "1 − e^(−7x)", "1 − (e^(−x))⁷", "7(1 − e^(−x))⁶"],
 "A",
 "The population cdf is F(x) = 1 − e^(−x), and the largest order statistic has cdf [F(x)]ⁿ, so (1 − e^(−x))⁷. Option B is the cdf of the MINIMUM of the seven, which is exponential with mean 1/7, and option D is a density, not a cdf."))

# --- moderate (10)
I.append(q(7, "single", "moderate",
 "For a sample of size n from an exponential population with mean θ, X₍₁₎ has mean:",
 ["θ/n", "θ", "nθ", "θ/n²"],
 "A",
 "P(X₍₁₎ > x) = [1 − F(x)]ⁿ = (e^(−x/θ))ⁿ = e^(−nx/θ), which is the survival function of an exponential with mean θ/n. So the minimum of n exponentials is exponential again with the rate multiplied by n — a consequence of the memoryless property, and why a series system of many components fails early."))

I.append(q(8, "single", "moderate",
 "For a sample from any distribution symmetric about μ, the sample median has expectation:",
 ["μ, for every sample size", "μ only as n → ∞",
  "the population mean only if the population is normal", "μ only for odd n"],
 "A",
 "Symmetry pairs X₍ᵣ₎ with X₍ₙ₋ᵣ₊₁₎ as mirror images about μ, so E(X₍ᵣ₎) + E(X₍ₙ₋ᵣ₊₁₎) = 2μ. For odd n the median is its own mirror image, and for even n it is the average of a mirror pair — so the result holds either way, exactly, at every n. This is why the sample median is the standard robust estimator of location."))

I.append(q(9, "numeric", "moderate",
 "The expected value of the sample range from U(0, 1) with n observations is:",
 ["(n − 1)/(n + 1)", "n/(n + 1)", "(n − 1)/n", "1 − 2/n"],
 "A",
 "E(R) = E(X₍ₙ₎) − E(X₍₁₎) = n/(n+1) − 1/(n+1) = (n−1)/(n+1). The subtraction needs only linearity of expectation, so the dependence between the minimum and the maximum is irrelevant here — though it would matter for Var(R).",
 check="At n = 2 this gives 1/3, which is the known mean absolute difference of two uniforms; at n = 20 it gives 0.905."))

I.append(q(10, "single", "moderate",
 "The joint density of all n order statistics from a continuous population with density f is:",
 ["n! f(x₁)⋯f(xₙ) for x₁ < ⋯ < xₙ, zero otherwise",
  "f(x₁)⋯f(xₙ) for all x₁, …, xₙ",
  "n f(x₁)⋯f(xₙ) for x₁ < ⋯ < xₙ",
  "[F(xₙ)]ⁿ f(x₁)⋯f(xₙ)"],
 "A",
 "The n! counts the orderings of the original labelled sample that sort to the same vector, and the density is zero outside the increasing region. Option B would make the order statistics independent, which they never are — sorting forces X₍₁₎ ≤ X₍₂₎ ≤ ⋯, so their marginal densities must never be multiplied."))

I.append(q(11, "numeric", "moderate",
 "For a sample of size 3 from U(0, 1), the variance of the median is:",
 ["1/20", "1/12", "1/16", "1/5"],
 "A",
 "The median of three is X₍₂₎ ~ Beta(2, 2). Var = r(n−r+1)/((n+1)²(n+2)) = 2×2/(16 × 5) = 4/80 = 1/20 = 0.05. The Beta formula ab/((a+b)²(a+b+1)) = 4/(16 × 5) agrees, which is a useful cross-check.",
 check="sd = √0.05 ≈ 0.224, about a quarter of the whole interval — a reminder of how little three observations pin down."))

I.append(q(12, "multi", "moderate",
 "Consider order statistics X₍₁₎ ≤ ⋯ ≤ X₍ₙ₎ from an independent continuous sample.",
 ["A and C only", "A, B and C only", "B and D only", "A, C and D only"],
 "A",
 "A is true, the defining product for the maximum. B is false — the order statistics are never independent, since sorting forces the ordering. C is true: expectation is linear, so no independence is needed for the mean of a difference. D is false: the cdf of the minimum is 1 − [1 − F]ⁿ, not 1 − Fⁿ.",
 statements=["P(X₍ₙ₎ ≤ x) = [F(x)]ⁿ.",
             "X₍₁₎ and X₍ₙ₎ are independent.",
             "E(X₍ₙ₎ − X₍₁₎) = E(X₍ₙ₎) − E(X₍₁₎) regardless of their dependence.",
             "P(X₍₁₎ ≤ x) = 1 − [F(x)]ⁿ."],
 verdicts=verd(
  (True, "True. The maximum is at most x exactly when all n observations are, and independence of the sample makes that a product."),
  (False, "False. Order statistics are never independent: X₍₁₎ ≤ X₍ₙ₎ always holds, which no pair of independent continuous variables satisfies."),
  (True, "True. Expectation is linear, so the mean of a difference is the difference of the means whatever the dependence. Only the VARIANCE of the range needs the covariance."),
  (False, "False. That expression is P(not all observations exceed x), a different event. The minimum's cdf is 1 − [1 − F(x)]ⁿ."))))

I.append(q(13, "numeric", "moderate",
 "Ten independent components each have exponential lifetime with mean 500 hours. The expected time to the FIRST failure is:",
 ["50 hours", "500 hours", "5000 hours", "1464 hours"],
 "A",
 "The minimum of n exponentials with mean θ is exponential with mean θ/n = 500/10 = 50 hours. Option D is the expected time to the LAST failure, θH₁₀ = 500 × 2.9290 = 1464 hours — so a series system of these components averages 50 hours while a parallel one lasts nearly thirty times as long.",
 check="The first of ten failures must come well before the mean life of one component, so any answer at or above 500 is wrong by inspection."))

I.append(q(14, "single", "moderate",
 "For a sample of size 5 from U(0, 1), which order statistic has the LARGEST variance?",
 ["the median X₍₃₎", "the minimum X₍₁₎", "the maximum X₍₅₎",
  "all five have the same variance"],
 "A",
 "Var(X₍ᵣ₎) = r(6−r)/252, which is maximised at r = 3: 0.0357 for the median against 0.0198 at either end. The boundaries at 0 and 1 pin the extremes down while the middle is free to move. For a population with unbounded tails, such as the normal, the ordering reverses — so it is the population's shape that decides, not a general rule about extremes."))

I.append(q(15, "single", "moderate",
 "The general density of X₍ᵣ₎ is f₍ᵣ₎(x) = C · [F(x)]^(r−1) [1 − F(x)]^(n−r) f(x). The constant C is:",
 ["n!/((r − 1)!(n − r)!)", "n!/(r!(n − r)!)",
  "n!/((r − 1)!(n − r + 1)!)", "1/((r − 1)!(n − r)!)"],
 "A",
 "Read it as a multinomial count: r − 1 observations fall below x, one sits at x, and n − r fall above, so C = n!/((r−1)! · 1! · (n−r)!). There is no factor for the single observation at x because 1! = 1. For U(0,1) this constant is exactly 1/B(r, n−r+1); at n = 5, r = 3 it is 30."))

I.append(q(16, "numeric", "moderate",
 "For U(0, θ), the maximum X₍ₙ₎ is the maximum likelihood estimator of θ. Its expectation is:",
 ["nθ/(n + 1)", "θ", "(n + 1)θ/n", "θ/n"],
 "A",
 "Scaling: if U ~ U(0,1) then θU ~ U(0,θ), so E(X₍ₙ₎) = θ · n/(n+1). The MLE is therefore biased downwards — necessarily so, since the maximum of a sample can never exceed θ — and (n+1)X₍ₙ₎/n is the unbiased version, which is option C.",
 check="The estimate can never exceed θ, so its expectation must be strictly below θ — which rules out θ itself and (n+1)θ/n at once, leaving only a value below θ."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the probability integral transform and its consequences for order statistics.",
 ["A, B and C only", "A and C only", "B and D only", "A, B, C and D"],
 "A",
 "A is true and is the transform itself. B is true because F is non-decreasing, so sorting is preserved. C is true, and it is why distribution-free quantile intervals exist. D is false — expectation does not pass through a non-linear function, so E(X₍ᵣ₎) is not F⁻¹ of the Beta mean in general.",
 statements=["If X is continuous with cdf F, then F(X) ~ Uniform(0, 1).",
             "F(X₍ᵣ₎) = U₍ᵣ₎, so F(X₍ᵣ₎) ~ Beta(r, n − r + 1) for every continuous population.",
             "The p-quantile of X₍ᵣ₎ equals F⁻¹ applied to the p-quantile of Beta(r, n − r + 1).",
             "E(X₍ᵣ₎) = F⁻¹(r/(n + 1)) for every continuous population."],
 verdicts=verd(
  (True, "True. P(F(X) ≤ u) = P(X ≤ F⁻¹(u)) = F(F⁻¹(u)) = u, so F(X) is exactly standard uniform."),
  (True, "True. F is non-decreasing, so it preserves order and F(X₍ᵣ₎) is the rᵗʰ order statistic of the transformed uniform sample — which makes the Beta result general, not special to the uniform."),
  (True, "True. Quantiles DO pass through a monotone transformation, which is exactly why exact distribution-free confidence intervals for a population quantile can be built from the Beta or the binomial."),
  (False, "False. Quantiles survive a monotone transformation but expectations do not: E(g(X)) ≠ g(E(X)) for non-linear g. The formula would hold only if F⁻¹ were linear."))))

I.append(q(18, "numeric", "hard",
 "For a unit exponential population, P(X₍₇₎ ≤ 2) in a sample of size 7 is approximately:",
 ["0.361", "0.865", "0.040", "0.639"],
 "A",
 "(1 − e^(−2))⁷ = (0.86466)⁷ = 0.3614. Option B is F(2) for a single observation, and option C is the same expression at x = 1. So even with seven observations, the largest exceeds 2 about 64% of the time — raising a value to the 7th power punishes it hard.",
 check="0.86466⁷ must be well below 0.86466; a rough check is 0.865⁷ ≈ e^(7 ln 0.865) = e^(−1.017) ≈ 0.36."))

I.append(q(19, "single", "hard",
 "Why are the middle order statistics of a uniform sample more variable than the extremes, while for a normal sample the reverse holds?",
 ["on the uniform scale the middle is always most variable, and moving to X stretches by 1/f, which is huge in the normal's tails",
  "because the normal has a larger variance than the uniform",
  "because the uniform is discrete at its endpoints",
  "because the normal's order statistics are independent while the uniform's are not"],
 "A",
 "The probability integral transform puts every continuous population on the uniform scale, where Var(U₍ᵣ₎) = r(n−r+1)/((n+1)²(n+2)) is largest in the middle. Moving back to X stretches by dx/du = 1/f(x). For the uniform f = 1 everywhere so the pattern survives; for the normal f is tiny in the tails, so the stretching there overwhelms it. The same factor 1/f appears in the large-sample variance of a sample quantile."))

I.append(q(20, "single", "hard",
 "A dam is designed using the largest annual flood in 80 years of record. The probability that a single new year exceeds that record is:",
 ["1/81, by exchangeability alone", "1/80", "1/2, since the record is the median",
  "it cannot be found without knowing the flood distribution"],
 "A",
 "Among 81 independent and identically distributed years, every ordering is equally likely, so each year is equally likely to be the largest; the chance the new one takes the record is 1/81. The argument uses only symmetry among exchangeable years, which is why option D is wrong — no distributional knowledge is needed. Over thirty years such exceedances are not remote, which is why a record is not a design ceiling."))

# Spread the answer keys; the validator caps any letter at 40% of the pool.
LET = "ABCD"
WANT = {"pr-t1-m-01": "A", "pr-t1-m-02": "C", "pr-t1-m-03": "D",
        "pr-t1-m-04": "B", "pr-t1-m-05": "C", "pr-t1-m-06": "D",
        "pr-t1-m-08": "B", "pr-t1-m-09": "C", "pr-t1-m-10": "D",
        "pr-t1-m-11": "B", "pr-t1-m-13": "C", "pr-t1-m-14": "D",
        "pr-t1-m-15": "B", "pr-t1-m-16": "C", "pr-t1-m-19": "D",
        "pr-t1-m-20": "B"}

def swapletters(t, a, b):
    """Swap option letters a and b wherever the text cites options — including plural lists
    like "options B and C" and "options A, B and D", which a singular "option X" regex missed
    and which once left a check line ruling out its own answer."""
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
 "moduleId": "probability", "topicId": "probability-t1", "source": "mastery",
 "label": "Order statistics — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
