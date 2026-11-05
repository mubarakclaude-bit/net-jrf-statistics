#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 4.17 — UMP unbiased and UMP invariant tests (topic inference-t17).

Built on PYQ evidence. June 2026 Q14 gave an exponential sample, asked for "the UMP critical
region of size α" for H₀: θ = θ₀ against the TWO-SIDED H₁: θ ≠ θ₀, and the official answer is
option D, "No UMP test exists". The stored response sheet shows option A was marked — and
option A is precisely the UMP region for the ONE-SIDED alternative θ > θ₀, which makes it the
most attractive wrong answer on the paper. That distinction is this lesson's spine.

The six practice variants on that question ask: whether a UMP test exists for a two-sided
alternative in a one-parameter exponential family, what the Neyman-Pearson lemma applies to,
the one-sided exponential UMP region, and whether the two-sided z test for a normal mean is
optimal in any sense (it is UMPU). Two further variants tagged to Q14 are likelihood-ratio
items that duplicate topic 4.10's pool; they are left where they are but noted.

Writes seed/lesson_t17.json and seed/inference_t17_mastery.json.
Run: python3 lesson_t17.py
"""
import json, io, os, re

OUT = "seed/lesson_t17.json"
POOL = "seed/inference_t17_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Recover what 'uniformly most powerful' demands, and the exponential distribution theory this topic is built on.",
 "ask": {
  "q": "The phrase 'uniformly most powerful' contains a demand that the phrase 'most powerful' does not. Which word carries it, and what does it demand?",
  "nudge": "Most powerful against what? One alternative, or all of them at once?"},
 "body": [
  "This lesson is about what to do when the best test does not exist. That sounds like a strange subject, but it is the ordinary situation: for a two-sided alternative there is usually no uniformly most powerful test at all, and almost every real question is two-sided.",
  "The repair is to stop asking for the best test among ALL tests and ask for the best among a sensible smaller class. Two such classes matter for this syllabus: the unbiased tests, and the invariant tests. Inside either one a best test often does exist.",
  "Four checks before that: what the word 'uniformly' is doing, the one theorem that delivers a UMP test when one exists, the distribution theory for the exponential family that every question here uses, and the definition of an unbiased test."],
 "items": [
  {"ask": "What does it mean for a test to be uniformly most powerful of size α?",
   "recall": "Its power is at least that of every other size-α test, at EVERY parameter value in the alternative — simultaneously, with one fixed test.",
   "refresh": [
    "The Neyman–Pearson lemma gives a most powerful test against ONE simple alternative. The region it produces may depend on which alternative you picked.",
    "'Uniformly' demands that one single region be the winner against all of them at once. That is a far stronger requirement, and it is the requirement that usually fails.",
    "So the whole question in this topic is: does the most powerful region change as the alternative moves? If it does not, you have a UMP test. If it does, you do not, and no amount of cleverness will produce one."]},
  {"ask": "State the Karlin–Rubin theorem, and say what it needs.",
   "recall": "If the family has monotone likelihood ratio in a statistic T, then for H₀: θ ≤ θ₀ against H₁: θ > θ₀ the test rejecting for large T is UMP of its size.",
   "refresh": [
    "Monotone likelihood ratio means that for θ₂ > θ₁ the ratio L(θ₂)/L(θ₁) is a monotone function of T. Every one-parameter exponential family has this property in its natural statistic.",
    "Notice the shape of the conclusion: a ONE-SIDED alternative, and a ONE-SIDED region. The theorem says nothing about θ ≠ θ₀, and that silence is not an oversight.",
    "This is the only general tool that delivers a UMP test, which is why 'is the alternative one-sided?' is the first question to ask of any UMP problem."]},
  {"ask": "For an iid sample from the exponential density f(x; θ) = θe^(−θx), what is the distribution of 2θΣxᵢ?",
   "recall": "Chi-square with 2n degrees of freedom.",
   "refresh": [
    "Note the parameterisation: θ here is the RATE, so the mean is 1/θ. A larger θ means smaller observations. Getting this backwards reverses every critical region in the topic.",
    "Each 2θXᵢ is exponential with mean 2, which is chi-square with 2 degrees of freedom, and n independent ones add to 2n.",
    "The degrees of freedom are 2n, not n. June 2026 Q14 wrote its percentiles as χ²(α, n) in the preamble but used 2n inside the options — read the options, not the preamble."]},
  {"ask": "When is a test called unbiased?",
   "recall": "When its power at every alternative is at least its size: π(θ) ≥ α for all θ in the alternative. It is never worse than ignoring the data.",
   "refresh": [
    "This is the same definition met in topic 4.12, and it has nothing to do with unbiased estimation — the word is reused for an unrelated idea.",
    "A biased test rejects a FALSE null less often than it rejects a true one, at some alternative. That is not a weak test; it is a test pointing the wrong way.",
    "The repair in this lesson is to throw such tests out of consideration. Once they are gone, a best test can reappear."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Why the best test can fail to exist",
 "objective": "See the conflict that kills the two-sided UMP test, before any algebra.",
 "body": [
  "Suppose a machine is supposed to run at a set rate and you want to detect any departure, faster or slower. You have one sample and must choose one rejection rule.",
  "If you only cared about 'faster', the best rule is clear: reject when the readings come out small. If you only cared about 'slower', the best rule is equally clear and is the opposite: reject when the readings come out large. Both are genuinely optimal, for their own question.",
  "Now you care about both. You must pick one rule, and whichever you pick is the wrong one half the time. A rule tuned for 'faster' has almost no power against 'slower' — worse than α, in fact, which means it detects a real slowdown LESS often than it falsely alarms on a machine running correctly.",
  "That is the whole content of the non-existence result. It is not a gap in the theory waiting to be filled. The two directions make incompatible demands on one region, and no region can satisfy both."],
 "scenario": {
  "teaser": "A dialysis unit must detect a pump running either fast or slow, and cannot have two rules.",
  "title": "One rule, two directions",
  "body": [
   "A dialysis machine pumps blood at a set rate. Too fast stresses the patient's circulation; too slow leaves the session under-dialysed. Both matter, and a technician checking the machine has one test and must reach one verdict.",
   "Suppose the technician borrows the rule that is best at catching a fast pump: flag the machine when the measured flow times come out unusually short. Against a genuinely fast pump this rule is the best there is. Against a slow pump it is worse than useless — a slow pump produces long flow times, which this rule treats as reassuring. Its power against a slow pump falls below the false-alarm rate.",
   "So the rule is not merely weak in one direction; it is actively misleading there, and a unit using it would be systematically blind to under-dialysis while believing itself protected.",
   "The honest response is to give up the claim of being best overall and ask for something weaker but attainable. Rule out the rules that are misleading in some direction — that is the unbiasedness requirement — and then ask which of the remaining rules is best. That question has an answer, and the answer is a two-tailed rule.",
   "What the unit loses is real. Against a fast pump specifically, the two-tailed rule has less power than the one-tailed rule tuned for it. What it gains is that there is no direction in which it is worse than guessing. For a safety-critical device, that is the trade worth making."],
  "q": "Why is a one-tailed rule's power against the opposite direction below α rather than merely small?",
  "answer": "Because the rejection region sits in the tail where the opposite alternative makes observations LESS likely than the null does. Under a slow pump, short flow times are rarer than they are under a correct pump, so the probability of landing in a short-time rejection region actually falls below α. Power below size is the definition of a biased test, and it is what the unbiasedness restriction exists to exclude."},
 "ask": {
  "q": "Could the technician run both one-tailed tests and reject if either fires?",
  "nudge": "Work out the size of that combined rule if each one-tailed test has size α."}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "The two rival regions, in the distribution they live in",
 "objective": "Find both one-sided critical regions on the one picture, and see that they are disjoint tails of the same distribution.",
 "viz": {"type": "chisq-tail", "k": 10, "alpha": 0.05, "obs": 3.94},
 "body": [
  "This is the distribution of 2θ₀Σxᵢ for an exponential sample of size n = 5 under the null — chi-square with 2n = 10 degrees of freedom. Every critical region in this lesson is a region of this one picture.",
  "Set α = 0.05 and read the upper critical value: 18.307. The region beyond it is the UMP region for the alternative θ < θ₀ — a slower rate, larger observations, a larger sum.",
  "Now the other direction. The UMP region for θ > θ₀ is the LOWER 5% tail, which begins at 3.940. The chart marks the critical value for the upper tail; the lower 5% point is the upper 95% point, so set α to 0.95 to read it off: 3.940.",
  "Those two regions are disjoint. They sit at opposite ends of the same distribution and share no outcome whatsoever. A single test must choose one, and whichever it chooses it has given up the other.",
  "Now the trap that the exam actually sets. Sliding α changes both critical values but it never makes the two regions coincide, at any α and any n. No amount of adjustment produces one region that is simultaneously the best in both directions — which is why the answer to the two-sided question is that no UMP test exists, and not some cleverer region.",
  "Last thing to try: raise the degrees of freedom, which here means a larger sample. The distribution shifts right and both tails move, but they stay at opposite ends. The non-existence is not a small-sample artefact."],
 "ask": {
  "q": "The lower 5% point is read off by setting the control to 0.95. Why?",
  "nudge": "The control shades the UPPER tail. What upper-tail area leaves exactly 5% below the critical value?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "Why no UMP test exists for a two-sided alternative",
 "objective": "Turn the intuition into the argument an examiner wants, and see biasedness in numbers.",
 "blocks": [
  {"t": "step", "h": "The argument, in four lines",
   "body": "1. Fix any alternative θ₁ > θ₀. By Neyman–Pearson the most powerful size-α test against it is a specific region — for the exponential family, a lower tail of Σxᵢ.\n2. Fix any alternative θ₂ < θ₀. The most powerful size-α test against that one is an upper tail of Σxᵢ.\n3. These two regions are disjoint, so no single region can be most powerful against both.\n4. A UMP test would have to be most powerful against every alternative at once. None exists."},
  {"t": "def", "h": "The sharper statement, which is what makes it final",
   "body": "The one-sided test is not merely suboptimal on the far side; it is BIASED there. Its power at alternatives on the wrong side falls below α. So it fails even the weak requirement of beating a coin flip, and the failure gets worse the further out the alternative is."},
  {"t": "formula", "h": "The numbers, for an exponential sample of n = 5 at α = 0.05",
   "body": "θ₀ = 1, so 2Σxᵢ is chi-square with 10 df under H₀.\nUMP test of θ > θ₀:  reject when Σxᵢ ≤ 3.9403/2 = 1.9701.\nUMP test of θ < θ₀:  reject when Σxᵢ ≥ 18.3070/2 = 9.1535.\nThe two regions have no outcome in common."},
  {"t": "step", "h": "Reading the power table below",
   "body": "The table gives the power of the FIRST of those tests — the one built for θ > θ₀ — at values on both sides. At θ₀ it is 0.05, as its size requires. Above θ₀ it climbs, which is what it was built to do. Below θ₀ it collapses to 0.003, far under the size of 0.05. A real halving of the rate is detected by this test about three times in a thousand, while a perfectly correct machine is flagged five times in a hundred. That is the precise sense in which it is not a usable two-sided test."},
  {"t": "step", "h": "What this does and does not rule out",
   "body": "It rules out a UMP test for θ ≠ θ₀. It does NOT rule out a sensible two-sided test — the two-tailed region is a perfectly good size-α test, it simply is not uniformly most powerful among all tests. And it does not rule out optimality in a restricted class, which is the subject of the next two sections. June 2026 Q14 offered the two-tailed region as an option; it is a valid test and the wrong answer, because the question asked for a UMP one."}],
 "table": {
  "caption": "Power of the one-sided UMP test built for θ > θ₀, evaluated on both sides. Exponential rate parameter, n = 5, θ₀ = 1, α = 0.05, rejecting when Σxᵢ ≤ 1.9701.",
  "head": ["true θ", "direction", "power", "verdict"],
  "rows": [
   ["0.5", "below θ₀", "0.003", "far below α — biased"],
   ["0.8", "below θ₀", "0.022", "below α — biased"],
   ["1.0", "the null itself", "0.050", "equals the size, as it must"],
   ["2.0", "above θ₀", "0.360", "above α — working as designed"],
   ["3.0", "above θ₀", "0.703", "above α — working as designed"]]},
 "flow": {
  "title": "What to ask for when no UMP test exists",
  "alt": "Flow chart from a testing problem to the kind of optimality available",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "Testing problem with a composite alternative", "kind": "start"},
   {"id": "b", "r": 1, "c": 1, "label": "Is the alternative one-sided?", "kind": "step"},
   {"id": "c", "r": 2, "c": 0, "label": "MLR holds → Karlin–Rubin gives a UMP test", "kind": "end"},
   {"id": "d", "r": 2, "c": 2, "label": "No UMP test exists among all tests", "kind": "step"},
   {"id": "e", "r": 3, "c": 1, "label": "Restrict to unbiased tests → UMPU test", "kind": "end"},
   {"id": "f", "r": 3, "c": 2, "label": "Restrict to invariant tests → UMP invariant test", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"},
   {"from": "b", "to": "c", "label": "yes"},
   {"from": "b", "to": "d", "label": "no, two-sided"},
   {"from": "d", "to": "e", "label": "rule out the misleading tests"},
   {"from": "d", "to": "f", "label": "or rule out the ones that depend on units"}],
  "note": "The two repairs are different restrictions, not competing theories, and for the standard normal problems they happen to pick out the same familiar test."},
 "ask": {
  "q": "The power at θ = 0.5 is 0.003 against a size of 0.05. Describe in one sentence what a hospital using this test would experience.",
  "nudge": "Compare how often it flags a correct machine with how often it catches one running at half rate."}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — June 2026, Q14",
 "objective": "Derive both one-sided regions for the exponential, then answer the question as asked.",
 "ask": {
  "q": "Option A was the most-marked wrong answer. What makes it so attractive?",
  "nudge": "Compare it with the region you derived in step 3. For which question is option A exactly right?"},
 "problem": "X₁,…,Xₙ are iid with density f(x; θ) = θe^(−θx) for x > 0. For testing H₀: θ = θ₀ against H₁: θ ≠ θ₀, find the UMP critical region of size α, or show that none exists. The options offered were: (A) Σxᵢ ≤ χ²(1−α, 2n)/(2θ₀); (B) Σxᵢ ≥ χ²(α, 2n)/(2θ₀); (C) the two-tailed region between those two bounds' complements; (D) no UMP test exists.",
 "steps": [
  {"say": "Write the likelihood and form the ratio for two parameter values.",
   "math": "L(θ) = θⁿ exp(−θ Σxᵢ)\nL(θ₂)/L(θ₁) = (θ₂/θ₁)ⁿ exp{ −(θ₂ − θ₁) Σxᵢ }",
   "why": "Everything depends on the data through Σxᵢ, which is therefore the sufficient statistic and the only thing a critical region can sensibly be built from."},
  {"say": "Read off the direction of monotonicity. This is the step that decides everything.",
   "math": "for θ₂ > θ₁:  −(θ₂ − θ₁) < 0,  so the ratio is DECREASING in Σxᵢ",
   "why": "θ is the rate, so a larger θ means smaller observations and a smaller sum. The family has monotone likelihood ratio in −Σxᵢ, equivalently decreasing MLR in Σxᵢ. Candidates who read θ as the mean get the direction backwards here and every option then looks wrong."},
  {"say": "Apply Karlin–Rubin to the one-sided alternative θ > θ₀.",
   "math": "reject for large −Σxᵢ, that is for SMALL Σxᵢ\nsize: P(Σxᵢ ≤ c | θ₀) = α  with  2θ₀Σxᵢ ~ chi-square, 2n df\nso  2θ₀c = χ²(1−α, 2n)  and  c = χ²(1−α, 2n)/(2θ₀)",
   "why": "The lower α point of a chi-square is its upper (1 − α) point, which is where the 1 − α in the expression comes from. This region is exactly option A — and it is the correct answer to a question that was not asked."},
  {"say": "Now the other one-sided alternative, θ < θ₀.",
   "math": "reject for SMALL −Σxᵢ, that is for LARGE Σxᵢ\nsize: P(Σxᵢ ≥ c' | θ₀) = α\nso  2θ₀c' = χ²(α, 2n)  and  c' = χ²(α, 2n)/(2θ₀)",
   "why": "This is option B. Two different alternatives, two different most powerful regions, sitting in opposite tails of the same distribution."},
  {"say": "Answer the question that was asked.",
   "math": "the alternative is θ ≠ θ₀, which contains values on BOTH sides\nthe two most powerful regions are disjoint\n⟹ no single region is most powerful against every alternative\nanswer: (D) No UMP test exists",
   "why": "Option C, the two-tailed region, is a legitimate size-α test and is what you would actually use — but it is not UMP, because against any particular θ > θ₀ the one-tailed region beats it. The question asked for a UMP region, and the honest answer is that there is none."}],
 "after": "The lesson in how this question was set: options A and B are each perfectly correct answers to a one-sided version of the question, option C is the test you would really run, and option D is the truth. Three of the four options are defensible statements about something, which is why reading 'θ ≠ θ₀' carefully is worth more here than any amount of algebra. Whenever a question offers 'no such test exists', check the alternative's sidedness before anything else."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the non-existence result and its reason.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "For a one-parameter exponential family and a two-sided alternative θ ≠ θ₀, does a UMP test exist?",
   "a": "No. The most powerful regions against alternatives on the two sides are disjoint, so no single region is most powerful against all of them."},
  {"q": "What does Karlin–Rubin require of the alternative?",
   "a": "That it be one-sided. With monotone likelihood ratio it then gives a UMP test; it says nothing about θ ≠ θ₀."},
  {"q": "For the density θe^(−θx), which tail of Σxᵢ is the UMP region against θ > θ₀?",
   "a": "The lower tail — small Σxᵢ. θ is the rate, so a larger θ means smaller observations."},
  {"q": "Is the one-sided test merely weak against alternatives on the far side, or worse?",
   "a": "Worse — it is biased there, with power below α. At θ = 0.5 in the worked example the power is 0.003 against a size of 0.05."},
  {"q": "Is the two-tailed region a valid size-α test?",
   "a": "Yes, and it is what you would use. It simply is not uniformly most powerful among all tests."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — the one-sided region with numbers",
 "objective": "Build the one-sided UMP region yourself and check its size, which is where the direction and the percentile both get tested.",
 "problem": "X₁,…,X₅ are iid with density f(x; θ) = θe^(−θx). Test H₀: θ = 1 against H₁: θ > 1 at α = 0.05. Use χ²(0.95, 10) = 3.9403 and χ²(0.05, 10) = 18.3070.",
 "steps": [
  {"say": "First settle the direction, because the percentile you need follows from it.",
   "blank": {"prompt": "Against θ > 1, does the UMP test reject for large or small Σxᵢ?",
             "answer": "small Σxᵢ",
             "accept": ["small", "small sum", "lower tail", "for small values of the sum",
                        "small Σx", "reject for small sums"],
             "hint": "θ is the rate, so the mean is 1/θ. A larger θ produces smaller observations."},
   "why": "A larger rate means shorter waiting times and a smaller total. Reading θ as the mean reverses this and is the commonest error in the whole topic."},
  {"say": "Now the distribution theory that converts that into a number.",
   "blank": {"prompt": "Under H₀: θ = 1, what is the distribution of 2Σxᵢ?",
             "answer": "chi-square with 10 degrees of freedom",
             "accept": ["chi-square 10 df", "chi square with 2n=10 df", "χ² with 10 df",
                        "chisq(10)", "chi-squared, 10 degrees of freedom"],
             "hint": "2θΣxᵢ is chi-square with 2n degrees of freedom, and here θ₀ = 1 and n = 5."},
   "why": "2n = 10, not n = 5. The doubling comes with the factor of 2 in front of the sum, and dropping one without the other gives a quantity that is not chi-square at all."},
  {"say": "Put the size condition in and solve for the cut-off.",
   "blank": {"prompt": "Find c such that P(Σxᵢ ≤ c | θ = 1) = 0.05.",
             "answer": "c = 3.9403/2 = 1.9701",
             "accept": ["1.9701", "1.97", "3.9403/2", "about 1.97", "c = 1.97"],
             "hint": "Rejecting for small Σxᵢ means you need the LOWER 5% point of the chi-square, which is its upper 95% point: 3.9403."},
   "why": "The lower α point is the upper (1 − α) point, which is why 0.95 appears where you might expect 0.05. Using 18.3070 here gives the region for the opposite alternative and is the trap."},
  {"say": "Finally, state the test and confirm the direction makes sense.",
   "blank": {"prompt": "Write the critical region, and say what the power does as θ rises above 1.",
             "answer": "reject when Σxᵢ ≤ 1.9701; the power increases with θ",
             "accept": ["Sx <= 1.9701, power increases", "reject if sum <= 1.97 and power rises with theta",
                        "Σxᵢ ≤ 1.97, power increasing in θ", "sum below 1.97; power goes up"],
             "hint": "A bigger rate makes small sums more likely, so landing in the region becomes more likely."},
   "why": "Power rises with θ, reaching 0.360 at θ = 2 and 0.703 at θ = 3. Below θ₀ it falls under α, which is the biasedness the next sections repair."}],
 "after": "Note how little of this was about optimality. Karlin–Rubin was invoked in one line; the work was all direction and percentiles. That is typical, and it is why the direction check — rate or mean? — is the single most valuable habit in this topic."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "UMP unbiased tests — the first repair",
 "objective": "Define the restricted class, state the two conditions, and learn the caveat about equal tails.",
 "blocks": [
  {"t": "def", "h": "The restriction",
   "body": "Consider only UNBIASED tests: those whose power at every alternative is at least α. This throws out exactly the tests that were misleading in some direction, including both of the one-sided tests from the worked example. A test that is most powerful among the survivors is called uniformly most powerful unbiased, or UMPU."},
  {"t": "step", "h": "Why the restriction rescues the problem",
   "body": "The one-sided tests were winning the comparison on their own side precisely by being hopeless on the other. Once hopelessness on either side is disqualifying, they are out of the competition, and a two-tailed test can be the best of what remains. For a one-parameter exponential family and a two-sided alternative, a UMPU test exists and is two-tailed."},
  {"t": "formula", "h": "The two conditions that pin it down",
   "body": "The UMPU test of H₀: θ = θ₀ against θ ≠ θ₀ rejects when T ≤ c₁ or T ≥ c₂, with c₁ and c₂ fixed by TWO equations:\n    size:          P(reject | θ₀) = α\n    unbiasedness:  E[φ(T) T | θ₀] = α E[T | θ₀]\nThe second condition is what makes the power function have its minimum exactly at θ₀, which is the same thing as being unbiased."},
  {"t": "step", "h": "The caveat that gets examined",
   "body": "Two conditions, two unknowns — so the cut-offs are determined, but they are NOT in general the equal-tail points. Putting α/2 in each tail satisfies the size condition and generally fails the unbiasedness condition. Equal tails is UMPU only when the null distribution of T is symmetric. For the normal mean that holds, so the familiar two-sided z test is UMPU. For the exponential, where T has a skewed chi-square law, the equal-tail test is NOT UMPU — the optional section at the end works out by how much."},
  {"t": "def", "h": "Where this leaves the standard tests",
   "body": "The two-sided z test for a normal mean with σ² known is UMPU. So is the two-sided t test for a normal mean with σ² unknown, and the two-sided test on a normal variance once its cut-offs are chosen by the two conditions rather than by equal tails. The everyday tests are therefore optimal — but in the UMPU sense, not the UMP sense, and the distinction is exactly what Q14 was probing."}],
 "ask": {
  "q": "The unbiasedness condition is equivalent to the power function having its minimum at θ₀. Why is that the same as being unbiased?",
  "nudge": "The power function passes through α at θ₀. If that point is the minimum, what can you say about its value everywhere else?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — is the two-sided z test optimal?",
 "objective": "Settle in what sense the most familiar two-sided test is best, which is a variant question on this topic.",
 "problem": "X₁,…,Xₙ are iid N(μ, σ²) with σ² known. For H₀: μ = μ₀ against H₁: μ ≠ μ₀, the usual test rejects when |x̄ − μ₀| > z(α/2) σ/√n. (a) Is it UMP? (b) Is it unbiased? (c) Is it UMPU? (d) Why does equal tails happen to be right here when it was wrong for the exponential?",
 "hints": [
  "For (a), apply the argument from section 4 unchanged: the alternative is two-sided, so compare the most powerful regions against a μ above μ₀ and a μ below it.",
  "For (b), work out the power at a general μ and ask where its minimum is. The power function of this test is symmetric about μ₀.",
  "For (d), look at the unbiasedness condition and ask what symmetry of the null distribution of x̄ does to it."],
 "answer": "(a) No. (b) Yes. (c) Yes. (d) Because the null distribution of x̄ is symmetric about μ₀, so the equal-tail cut-offs satisfy the unbiasedness condition automatically.",
 "check": "Three things worth getting right. The answer to (a) is no, and for exactly the reason Q14 turned on — nothing about the normal distribution rescues a two-sided alternative from the non-existence argument. The answer to (c) is yes, and 'UMPU' is the precise sense in which the test you have used since school is optimal. And (d) is the general principle rather than a normal-distribution curiosity: equal tails is UMPU when the null distribution is symmetric and not otherwise, which is why the same move fails for the exponential and for the variance test.",
 "scenario": {
  "teaser": "A calibration lab is asked to justify using the ordinary two-sided test.",
  "title": "Justifying the obvious",
  "body": [
   "A calibration laboratory reports whether an instrument reads true. Its procedure is the two-sided z test, chosen because everyone uses it. An auditor asks what makes it the right choice, and the honest answer takes some care.",
   "It is not the most powerful test. Against the specific alternative 'the instrument reads 2 units high', a one-tailed test would detect that better. If the lab knew the direction of the drift in advance, it should use that one-tailed test and would be right to.",
   "But it does not know the direction, and a one-tailed test chosen arbitrarily would be worse than useless against drift the other way. Among tests that are not misleading in either direction, the two-sided z test is the best there is. That is the justification, and it is a real one — it is simply a statement about a restricted class rather than about all tests.",
   "There is a second, independent justification that arrives at the same test. Whether the instrument reads true should not depend on whether the lab records in millimetres or inches, and an invariance requirement of that kind also singles out this test. Two different principles, one answer, which is part of why it feels inevitable."],
  "q": "What should the lab do differently if it did know the direction of any likely drift?",
  "answer": "Use the one-tailed test in that direction, which is UMP by Karlin–Rubin and genuinely more powerful against the drift it expects. The cost is being blind — worse than blind, biased — to drift the other way, so this is only defensible when the physics really does rule out one direction. Claiming directional knowledge you do not have is how a one-tailed test becomes misconduct rather than efficiency."},
 "solution": [
  {"say": "(a) Apply the non-existence argument.",
   "math": "against μ₁ > μ₀:  most powerful region is  x̄ > μ₀ + z_α σ/√n\nagainst μ₂ < μ₀:  most powerful region is  x̄ < μ₀ − z_α σ/√n\nthe two are disjoint ⟹ no UMP test",
   "why": "Identical in structure to the exponential case. Normality buys nothing here; the obstruction is the two-sidedness of the alternative."},
  {"say": "(b) Compute the power and locate its minimum.",
   "math": "π(μ) = P(Z > z(α/2) − δ) + P(Z < −z(α/2) − δ),  where δ = (μ − μ₀)√n/σ\nπ(μ₀) = α,  and π is symmetric in δ and increasing in |δ|",
   "why": "The power is a function of |δ| alone, equal to α at δ = 0 and rising in both directions. So the minimum sits at μ₀ and the power is at least α everywhere — the test is unbiased."},
  {"say": "(c) Check the two conditions.",
   "math": "size condition:        α/2 + α/2 = α  ✓\nunbiasedness condition: satisfied, since π has its minimum at μ₀  ✓",
   "why": "Both conditions hold, so the test is the UMPU test. This is the sense in which the two-sided z test is optimal, and it is the answer the variant question on this topic is after."},
  {"say": "(d) Identify what made equal tails work.",
   "math": "x̄ under H₀ is symmetric about μ₀\n⟹ equal tails ⟺ minimum of the power at μ₀ ⟺ unbiasedness condition",
   "why": "Symmetry is doing all the work. For a skewed null distribution — the chi-square of the exponential sum, or the chi-square of a variance test — equal tails no longer puts the power minimum at θ₀, and the UMPU cut-offs are unequal. Section 11's optional follow-up quantifies that for the exponential."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims this topic's questions are built from, including the Q14 pair.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "For a one-parameter exponential family and the two-sided alternative θ ≠ θ₀, a UMP test of size α exists.",
   "tf": False,
   "why": "False, and this is June 2026 Q14. The most powerful regions against alternatives above and below θ₀ are disjoint tails, so no single region is most powerful against all alternatives."},
  {"claim": "For f(x; θ) = θe^(−θx) and H₁: θ > θ₀, the UMP test rejects for small Σxᵢ.",
   "tf": True,
   "why": "True. θ is the rate, so a larger θ gives smaller observations and a smaller sum. The likelihood ratio decreases in Σxᵢ, so Karlin–Rubin puts the region in the lower tail."},
  {"claim": "The Neyman–Pearson lemma, applied directly, gives a UMP test for a composite two-sided alternative.",
   "tf": False,
   "why": "False. The lemma covers one simple hypothesis against one simple hypothesis. Its region generally depends on which alternative was chosen, and for a two-sided alternative that dependence is exactly the obstruction."},
  {"claim": "A one-sided test used against a two-sided alternative is biased.",
   "tf": True,
   "why": "True. Its power at alternatives on the far side falls below α — 0.003 against a size of 0.05 at θ = 0.5 in the worked example. Power below size is the definition of a biased test."},
  {"claim": "The two-sided z test for a normal mean with σ² known is UMP unbiased.",
   "tf": True,
   "why": "True. It is not UMP — no two-sided test is — but among unbiased tests it is most powerful, and the equal-tail cut-offs satisfy the unbiasedness condition because the null distribution of x̄ is symmetric."},
  {"claim": "A two-sided test that puts α/2 in each tail is UMP unbiased whatever the distribution of the statistic.",
   "tf": False,
   "why": "False. Equal tails always has the right size but satisfies the unbiasedness condition only when the null distribution is symmetric. For the skewed chi-square law of an exponential sum it does not, and the UMPU cut-offs are unequal."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 7,
 "title": "On your own — UMP invariant tests",
 "objective": "Meet the second repair, and see which familiar test it picks out.",
 "problem": "X₁,…,Xₙ are iid N(μ, σ²) with BOTH parameters unknown. Test H₀: μ = 0 against H₁: μ ≠ 0. (a) Why does a change of measurement units leave the problem unchanged? (b) Which statistic is unchanged by that change? (c) What is the UMP invariant test? (d) Name one other optimality property the same test has.",
 "hints": [
  "For (a), consider replacing every xᵢ by cxᵢ for a positive constant c. What happens to μ, to σ, and to the hypothesis μ = 0?",
  "For (b), check what the transformation does to x̄, to s, and then to their ratio.",
  "For (c), once attention is restricted to tests built from that invariant statistic, there is one best test and it is one you already know."],
 "answer": "(a) Scaling by c > 0 maps the problem to itself, since μ = 0 if and only if cμ = 0. (b) The t statistic x̄/(s/√n). (c) The two-sided t test. (d) It is also UMPU.",
 "check": "Two things to be precise about. The invariance here is to SCALE, not to location: adding a constant would move μ away from 0 and change the hypothesis, so it is not a symmetry of this problem. And 'UMP invariant' is a statement about a restricted class, exactly like UMPU — the t test is not UMP among all tests, because the alternative is two-sided and section 4's argument applies here too. That the two restrictions pick out the same test is a convenience of the normal family, not a general theorem.",
 "solution": [
  {"say": "(a) Check that scaling is a symmetry of the problem.",
   "math": "xᵢ → c xᵢ  (c > 0)  sends  μ → cμ,  σ → cσ\nμ = 0  ⟺  cμ = 0",
   "why": "The family of distributions is mapped onto itself and the null hypothesis is mapped onto itself. So the problem looks identical in the new units, and a sensible test ought to reach the same verdict — that is the invariance requirement."},
  {"say": "(b) Find what survives the transformation.",
   "math": "x̄ → c x̄,  s → c s\nso  x̄/(s/√n)  →  c x̄/(c s/√n)  =  x̄/(s/√n)",
   "why": "The constant cancels. The t statistic is a maximal invariant: any test that gives the same answer in every system of units must be a function of it."},
  {"say": "(c) Find the best test among those built from it.",
   "math": "reject when |t| > t(α/2, n − 1)",
   "why": "Restricting to invariant tests reduces the problem to one built on t alone, and within that class the two-sided t test is UMP. So the ordinary t test is the UMP invariant test — a second route to the test topic 4.13 and topic 4.10 both arrived at from other directions."},
  {"say": "(d) Note the other property.",
   "math": "the same two-sided t test is also UMPU",
   "why": "Two different restrictions, the same answer. For the normal family the standard tests tend to be optimal in several of these restricted senses at once, which is a large part of why they are standard."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "The hierarchy, and what each restriction costs",
 "objective": "Place the four optimality notions in order, which is how the conceptual question is framed.",
 "blocks": [
  {"t": "step", "h": "The four notions, from strongest claim to weakest",
   "body": "Most powerful (Neyman–Pearson): best against ONE simple alternative. Always available, but the test may depend on which alternative.\nUMP: one test best against EVERY alternative. Available for one-sided alternatives with MLR, by Karlin–Rubin. Not available for two-sided alternatives.\nUMPU: best among unbiased tests. Available for two-sided alternatives in exponential families.\nUMP invariant: best among tests respecting a symmetry of the problem. Available when the problem has such a symmetry."},
  {"t": "def", "h": "What a restriction buys and what it costs",
   "body": "Each restriction makes the competition smaller, so a winner becomes easier to find. The cost is that the winner is only a winner within the class: a UMPU test can be beaten, at a particular alternative, by a biased test. The claim 'this is the best test' is therefore always relative to a class, and naming the class is part of giving the right answer."},
  {"t": "step", "h": "Which restriction to reach for",
   "body": "Unbiasedness is the natural one when the alternative is two-sided and symmetric in spirit — you have no directional knowledge, and you refuse to be misleading in either direction. Invariance is natural when the problem has a symmetry that any sensible answer must respect, such as the choice of units, and it is what justifies the t test and the F test. They are different principles and in general could pick out different tests; for the standard normal problems they agree."},
  {"t": "step", "h": "How the exam frames this",
   "body": "A question asking 'the UMP test' with a two-sided alternative is usually testing whether you know none exists — that was Q14. A question asking in what sense the familiar two-sided test is optimal wants the word UMPU. A question about the t test and units wants UMP invariant. The three are distinguished by a single phrase in the stem, so read for the alternative's sidedness and for the class named."}],
 "ask": {
  "q": "Can a biased test ever have more power than the UMPU test at some alternative?",
  "nudge": "The one-sided test from section 4 is biased. What is its power at an alternative on its own side, compared with a two-tailed test's?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the definitions and the one caveat that carries marks.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "What does UMPU stand for, and what is the restricted class?",
   "a": "Uniformly most powerful unbiased: most powerful among tests whose power is at least α at every alternative."},
  {"q": "What two conditions fix the cut-offs of a UMPU two-sided test?",
   "a": "The size condition, and the unbiasedness condition E[φ(T)T | θ₀] = α E[T | θ₀], which makes the power function's minimum sit at θ₀."},
  {"q": "When is the equal-tail two-sided test UMPU?",
   "a": "Only when the null distribution of the statistic is symmetric — as for the normal mean. For a skewed law such as the chi-square it is not."},
  {"q": "Which test is UMP invariant for a normal mean with σ² unknown, and under what group?",
   "a": "The two-sided t test, under scale changes xᵢ → cxᵢ with c > 0. The t statistic is the maximal invariant."},
  {"q": "For f(x; θ) = θe^(−θx) and H₁: θ ≠ θ₀, what is the answer to 'find the UMP region'?",
   "a": "No UMP test exists. The two-tailed region is a valid test but not a UMP one."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Give the four-line argument that no UMP test exists for a two-sided alternative, and name the disjoint regions it turns on.",
  "Derive both one-sided UMP regions for the exponential rate parameter, getting the direction right from θ being a rate and not a mean.",
  "Recognise that a one-sided test used two-sided is biased, not merely weak, and quote a power below α to show it.",
  "Define an unbiased test and a UMPU test, and state the two conditions that fix a UMPU test's cut-offs.",
  "Say when equal tails is UMPU — symmetric null distribution only — and why that makes the z test optimal but not the equal-tail exponential test.",
  "Define a UMP invariant test, identify the t statistic as the maximal invariant under scale changes, and name the two-sided t test as the result.",
  "Place the four notions in order and name the class whenever you claim a test is best."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "How far equal tails misses for the exponential",
 "objective": "Check the unbiasedness condition numerically, and see that the equal-tail test fails it.",
 "blocks": [
  {"t": "step", "h": "The claim to test",
   "body": "Section 7 asserted that for a skewed null distribution the equal-tail two-sided test has the right size but is not UMPU. That is a checkable statement, and checking it is more convincing than taking it on trust. Take the exponential rate problem with n = 5, θ₀ = 1 and α = 0.05, so that T = Σxᵢ has 2T distributed as chi-square with 10 degrees of freedom."},
  {"t": "formula", "h": "The two conditions, made computable",
   "body": "size:          P(2T ≤ a) + P(2T ≥ b) = α,   with 2T ~ chi-square, 2n df\nunbiasedness:  E[φ(T) T]/E[T] = α\nFor T with a gamma law, E[φ(T)T]/E[T] has a clean form: it is the same tail probability computed with TWO extra degrees of freedom. So the second condition reads\n    P(χ² ≤ a) + P(χ² ≥ b) = α,  evaluated with 2n + 2 df."},
  {"t": "step", "h": "The arithmetic",
   "body": "Equal tails puts 0.025 in each tail of the 10-degree-of-freedom law, giving a = 3.2470 and b = 20.4832. Checking both conditions at those cut-offs: the size condition gives 0.0500, exactly as designed. The unbiasedness condition, evaluated with 12 degrees of freedom, gives 0.0649. It should have been 0.0500."},
  {"t": "def", "h": "What the miss means",
   "body": "The equal-tail test is a perfectly valid size-0.05 test, and it is what almost everyone uses. But its power function does not have its minimum at θ₀ — the minimum sits slightly to one side — so there are alternatives at which it is beaten by another unbiased test. It is not the UMPU test. The true UMPU cut-offs solve the two conditions simultaneously and are unequal, pushing more of the α into one tail than the other to compensate for the skew."},
  {"t": "step", "h": "Why nobody worries much, and why it is still examinable",
   "body": "The loss of power is small, the equal-tail test is far easier to tabulate, and reporting it is standard practice. So in applied work the approximation is accepted deliberately. In an examination the distinction is exactly what separates a candidate who has understood UMPU from one who has memorised 'two-sided means α/2 each side' — which is why a question offering 'the equal-tail test is UMPU' as an option is offering a wrong answer. Contrast the normal mean, where symmetry makes the two conditions coincide and equal tails is genuinely UMPU."}],
 "ask": {
  "q": "The unbiasedness condition came out as 0.0649 rather than 0.0500. To fix it, should more or less of the α go into the lower tail?",
  "nudge": "The condition is the same tail probability computed with a distribution shifted to the right. Which cut-off is it more sensitive to?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "inference_t17_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "inferencet17",
 "topicId": "inference-t17",
 "moduleId": "inference",
 "title": "UMP Unbiased and UMP Invariant Tests",
 "breadcrumb": "Statistical Inference → Testing of Hypotheses → When no best test exists",
 "engine": "C",
 "engineName": "Testing — what to ask for when the best test does not exist",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Give the argument that no UMP test exists against a two-sided alternative, and identify the disjoint regions it rests on.",
  "Derive both one-sided UMP regions for the exponential rate parameter, with the direction settled correctly.",
  "Show that a one-sided test used against a two-sided alternative is biased, not merely weak.",
  "Define an unbiased test and a UMPU test, and state the two conditions fixing a UMPU test's cut-offs.",
  "Say when the equal-tail test is UMPU, and why the two-sided z test qualifies while the exponential equal-tail test does not.",
  "Define a UMP invariant test, identify the maximal invariant under scale changes, and name the resulting test."],
 "prereq": [
  {"id": "p1", "name": "Neyman–Pearson, MLR and UMP tests",
   "why": "This topic begins where 4.9 ends. You need the lemma, monotone likelihood ratio and Karlin–Rubin available, because the non-existence argument is built from them."},
  {"id": "p2", "name": "Size and power of a test",
   "why": "The whole repair turns on the definition of an unbiased test — power at least α at every alternative — which is topic 4.12's vocabulary."},
  {"id": "p3", "name": "The chi-square distribution and its tail values",
   "why": "Every critical region here is a tail of a chi-square, because 2θΣxᵢ has that distribution for an exponential sample."},
  {"id": "p4", "name": "Exponential and gamma distribution theory",
   "why": "The worked example and the optional section both rest on 2θΣxᵢ being chi-square with 2n degrees of freedom, and on θ being a rate rather than a mean."}],
 "traps": [
  "No UMP test exists against a two-sided alternative — that is the answer, not a cleverer region.",
  "In f(x; θ) = θe^(−θx), θ is the RATE, so H₁: θ > θ₀ gives a LOWER tail of Σxᵢ.",
  "The degrees of freedom are 2n, not n.",
  "The lower α point of a chi-square is its upper (1 − α) point.",
  "A one-sided test used two-sided is biased — power below α — not merely low-powered.",
  "The two-tailed region IS a valid size-α test; it just is not UMP.",
  "Equal tails is UMPU only when the null distribution is symmetric.",
  "'Best test' is always relative to a class — name the class."],
 "revision": {
  "sheet": [
   "UMP means one test is most powerful at EVERY alternative simultaneously. 'Uniformly' is the demanding word.",
   "Karlin–Rubin delivers a UMP test only for a ONE-SIDED alternative, given monotone likelihood ratio.",
   "Two-sided alternative in a one-parameter exponential family: no UMP test exists. This is June 2026 Q14, answer D.",
   "The reason: the most powerful region against θ > θ₀ and against θ < θ₀ are disjoint tails of the same distribution.",
   "Exponential f(x; θ) = θe^(−θx): θ is the rate, mean 1/θ, and 2θΣxᵢ ~ chi-square with 2n df.",
   "UMP region against θ > θ₀: Σxᵢ ≤ χ²(1−α, 2n)/(2θ₀) — the LOWER tail, because a larger rate means smaller sums.",
   "UMP region against θ < θ₀: Σxᵢ ≥ χ²(α, 2n)/(2θ₀) — the upper tail.",
   "A one-sided test used against the opposite alternative is biased: for n = 5, θ₀ = 1, α = 0.05, power is 0.003 at θ = 0.5.",
   "Unbiased test: power ≥ α at every alternative. Nothing to do with unbiased estimation.",
   "UMPU: most powerful among unbiased tests. Exists for two-sided alternatives in exponential families, and is two-tailed.",
   "The two conditions: P(reject | θ₀) = α, and E[φ(T)T | θ₀] = α E[T | θ₀] — the second puts the power minimum at θ₀.",
   "Equal tails (α/2 each side) always has the right size, but is UMPU only when the null law is symmetric.",
   "The two-sided z test for a normal mean, σ² known, IS UMPU. So is the two-sided t test with σ² unknown.",
   "The equal-tail exponential test is NOT UMPU: at n = 5 its unbiasedness condition evaluates to 0.0649, not 0.0500.",
   "UMP invariant: most powerful among tests respecting a symmetry. For a normal mean with σ² unknown, the group is scale changes xᵢ → cxᵢ, the maximal invariant is the t statistic, and the two-sided t test is UMP invariant — and also UMPU.",
   "Hierarchy: most powerful (one alternative) → UMP (all, one-sided only) → UMPU or UMP invariant (all, within a restricted class)."],
  "cards": [
   ["Why no two-sided UMP test", "The most powerful regions against the two sides are disjoint tails, so no single region wins against all alternatives"],
   ["Karlin–Rubin's limitation", "It covers one-sided alternatives only; its silence on θ ≠ θ₀ is not an oversight"],
   ["θ in θe^(−θx)", "The RATE, so the mean is 1/θ — a larger θ gives smaller observations and smaller sums"],
   ["UMP region for θ > θ₀", "Σxᵢ ≤ χ²(1−α, 2n)/(2θ₀) — the lower tail, with 2n degrees of freedom"],
   ["Why the one-sided test fails two-sided", "It is biased on the far side: power below α, 0.003 against a size of 0.05 in the worked case"],
   ["Unbiased test", "Power at least α at every alternative — never worse than ignoring the data"],
   ["UMPU", "Most powerful among unbiased tests; exists two-sided for exponential families and is two-tailed"],
   ["The two conditions", "Size, plus E[φ(T)T] = α E[T], which places the power function's minimum at θ₀"],
   ["When equal tails is UMPU", "Only when the null distribution is symmetric — true for the normal mean, false for the chi-square"],
   ["The two-sided z test", "Not UMP, but UMPU — and that is the precise sense in which it is optimal"],
   ["UMP invariant", "Most powerful among tests respecting a symmetry; for a normal mean with σ² unknown the two-sided t test, under scale changes"],
   ["Maximal invariant", "The t statistic x̄/(s/√n), which is unchanged when every observation is multiplied by c > 0"]],
  "tricks": [
   "Read the alternative's sidedness FIRST. If it is two-sided and the question asks for a UMP test, the answer is almost certainly that none exists.",
   "Settle rate-or-mean before writing a single region. In θe^(−θx) it is the rate, and the region for θ > θ₀ is the lower tail.",
   "Degrees of freedom 2n, and the lower α point is the upper (1 − α) point. Two conversions, both routinely got wrong.",
   "When an option says 'no such test exists', treat it as a live candidate rather than a joke — Q14's answer was exactly that.",
   "If asked in what sense a familiar two-sided test is best, the word wanted is UMPU, not UMP."],
  "shortcuts": [
   "Any one-sided region is the correct answer to a one-sided question, so in a two-sided question the one-sided options are there as bait. Recognising them saves the derivation.",
   "For a symmetric null law, equal tails and UMPU coincide, so no extra work is needed for the normal mean. For a skewed one, assume they differ.",
   "The t test is simultaneously UMPU and UMP invariant, so either phrase in a stem points at it."],
  "remember": [
   "Two-sided alternative means no UMP test. Say so.",
   "θ is a rate. Larger θ, smaller sum, lower tail.",
   "Equal tails needs symmetry to be UMPU."]},
 "howto": "Read this in order, and treat section 4 as the heart of it — it is June 2026 Q14 worked in full, and the question is a trap rather than a calculation. The opening checks matter because the one thing that decides every region here is whether θ is a rate or a mean, and the second thing is the 2n degrees of freedom. Sections 7 and 10 introduce the two repairs; section 11 puts the four notions in order and is the one to revise from. Attempt the question at the end of each section before opening the answer. The optional section at the end checks numerically that the equal-tail exponential test is not UMPU; it is marked optional, but it is the only place the UMPU conditions become concrete, so it is worth a second pass.",
 "refs": [
  {"title": "Uniformly Most Powerful Tests", "where": "Lesson 26", "site": "Penn State STAT 415",
   "url": "https://online.stat.psu.edu/stat415/lesson/26", "type": "Course notes", "free": True,
   "checked": "2026-10-30",
   "why": "Karlin–Rubin and the one-sided UMP construction, with the exponential family worked. Read it before section 4 if MLR is not fresh."},
  {"title": "Mathematical Statistics 18.655 — lecture notes",
   "where": "Sessions on testing and optimality", "site": "MIT OpenCourseWare",
   "url": "https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type": "Lecture notes", "free": True, "checked": "2026-10-30",
   "why": "The restricted-class notions, including unbiasedness and invariance, set out together — which is the content of section 11."},
  {"title": "Statistical Inference", "where": "Weeks on testing of hypotheses",
   "site": "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee",
   "url": "https://archive.nptel.ac.in/noc/courses/noc21/SEM1/noc21-ma23", "type": "Video course",
   "free": True, "checked": "2026-10-30",
   "why": "Indian syllabus wording for UMP, UMPU and the exponential-family examples, which is the phrasing the NET paper uses."},
  {"title": "Testing Statistical Hypotheses, 3rd edition", "where": "Chapters 3–6",
   "site": "Lehmann and Romano", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "The definitive treatment: UMP for one-sided alternatives, the two UMPU conditions, and invariance. Chapter 4 is where the two conditions used in the optional section come from."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 9",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "The non-existence of a two-sided UMP test for exponential families, at the level this lesson needs, with the exponential example."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored October 2026 for this platform against the UGC NET Statistics syllabus, and prioritised from the June 2026 paper, where Q14 asked for 'the UMP critical region' for a two-sided alternative in an exponential sample and the official answer is that no UMP test exists. The stored response sheet shows option A was marked, and option A is exactly the UMP region for the one-sided alternative θ > θ₀ — so the lesson treats the sidedness check as its central skill and works the question in full in section 4. The six practice variants on that question — the non-existence result, what Neyman–Pearson applies to, the one-sided exponential region, and the optimality of the two-sided z test — are each taught in a named section and appear in the pool; two further variants tagged to Q14 are likelihood-ratio items duplicating topic 4.10's pool and were left in place. Every numerical value was computed rather than recalled: the chi-square points 3.9403, 18.3070, 3.2470 and 20.4832 at 10 degrees of freedom, the critical values 1.9701 and 9.1535, the power figures 0.003, 0.022, 0.050, 0.360 and 0.703, and the unbiasedness-condition value 0.0649 for the equal-tail test against its required 0.0500. Previous-year questions themselves are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "inf-t17-m-%02d" % i, "format": fmt, "topic": "inference-t17",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "For a one-parameter exponential family and the alternative H₁: θ ≠ θ₀, a UMP test of size α:",
 ["exists and is two-tailed", "exists and is one-tailed",
  "does not exist", "exists only for large samples"],
 "C",
 "The most powerful region against an alternative above θ₀ and the one against an alternative below θ₀ are disjoint tails of the same distribution, so no single region can be most powerful against every alternative. The two-tailed region is a valid size-α test but is not UMP, which is the distinction June 2026 Q14 was built on."))

I.append(q(2, "single", "easy",
 "The Neyman–Pearson lemma applies to:",
 ["a simple null against a simple alternative",
  "a simple null against a composite alternative",
  "any null against any alternative",
  "a composite null against a composite alternative"],
 "A",
 "The lemma requires both hypotheses to be completely specified. Composite alternatives need monotone likelihood ratio and Karlin–Rubin, and even then only when the alternative is one-sided."))

I.append(q(3, "single", "easy",
 "A test is called unbiased if:",
 ["its power equals its size at every alternative",
  "its power is at least its size at every alternative",
  "the statistic it uses is an unbiased estimator",
  "its size equals the stated level exactly"],
 "B",
 "An unbiased test satisfies π(θ) ≥ α for every θ in the alternative — it is never worse than ignoring the data. The term has nothing to do with unbiased estimation, which is a different idea sharing a word."))

I.append(q(4, "single", "easy",
 "For the density f(x; θ) = θe^(−θx) and H₀: θ = θ₀ against H₁: θ > θ₀, the UMP test rejects for:",
 ["large Σxᵢ", "small Σxᵢ", "large Σxᵢ²", "|Σxᵢ − n/θ₀| large"],
 "B",
 "Here θ is the rate, so the mean is 1/θ and a larger θ produces smaller observations. The likelihood ratio L(θ₂)/L(θ₁) for θ₂ > θ₁ decreases in Σxᵢ, so Karlin–Rubin places the critical region in the lower tail. Reading θ as the mean reverses this and is the commonest error in the topic."))

I.append(q(5, "order", "easy",
 "Arrange the steps of deciding what kind of optimal test is available in the correct order.",
 ["C, A, B, D", "A, C, B, D", "C, B, A, D", "A, B, C, D"],
 "A",
 "Check the sidedness of the alternative first, because that alone decides whether a UMP test can exist. If it is one-sided, verify MLR and apply Karlin–Rubin. If it is two-sided, there is no UMP test and the question becomes which restricted class to optimise within.",
 items=["A. If one-sided, check monotone likelihood ratio and apply Karlin–Rubin",
        "B. If two-sided, conclude that no UMP test exists among all tests",
        "C. Determine whether the alternative is one-sided or two-sided",
        "D. Restrict to unbiased or invariant tests and find the best one there"]))

I.append(q(6, "numeric", "easy",
 "For an iid sample of size n = 8 from f(x; θ) = θe^(−θx), the quantity 2θΣxᵢ has a chi-square distribution with how many degrees of freedom?",
 ["8", "16", "7", "14"],
 "B",
 "Each 2θXᵢ is exponential with mean 2, which is a chi-square with 2 degrees of freedom, and n independent ones add to 2n = 16. The factor 2 in front of the sum and the doubling of the degrees of freedom go together. June 2026 Q14 wrote χ²(α, n) in its preamble but used 2n inside its options, so read the options rather than the preamble.",
 check="The degrees of freedom are 2n, so they must be even and twice the sample size. An answer equal to n, or to n − 1, has dropped the doubling."))

# --- moderate (10)
I.append(q(7, "single", "moderate",
 "Let X₁,…,Xₙ be iid with f(x; θ) = θe^(−θx). For testing H₀: θ = θ₀ against H₁: θ ≠ θ₀, the UMP critical region of size α is:",
 ["Σxᵢ ≤ χ²(1−α, 2n)/(2θ₀)", "Σxᵢ ≥ χ²(α, 2n)/(2θ₀)",
  "χ²(1−α, 2n)/(2θ₀) ≤ Σxᵢ ≤ χ²(α, 2n)/(2θ₀)", "no UMP test exists"],
 "D",
 "This is June 2026 Q14. The alternative is two-sided, and the most powerful regions against the two sides are disjoint, so no UMP test exists. The first option is the UMP region for the one-sided H₁: θ > θ₀ and was the most-marked wrong answer; the second is the region for θ < θ₀; the third is the two-tailed test, which is valid and useful but not UMP."))

I.append(q(8, "numeric", "moderate",
 "X₁,…,X₅ are iid with f(x; θ) = θe^(−θx). For H₀: θ = 1 against H₁: θ > 1 at α = 0.05, with χ²(0.95, 10) = 3.9403 and χ²(0.05, 10) = 18.3070, the UMP test rejects when Σxᵢ is:",
 ["≤ 1.9701", "≥ 9.1535", "≤ 3.9403", "≥ 18.3070"],
 "A",
 "Against θ > 1 the region is the lower tail, so the cut-off is the lower 5% point of the chi-square with 10 df — which is its upper 95% point, 3.9403 — divided by 2θ₀ = 2, giving 1.9701. Option B is the region for θ < 1. The remaining options omit the division by 2θ₀.",
 check="Two conversions must both happen: the lower α point is the upper (1 − α) point, and the chi-square value is divided by 2θ₀. Missing the division leaves a number twice too large."))

I.append(q(9, "single", "moderate",
 "A one-sided test built for H₁: θ > θ₀ is applied when the true alternative is two-sided. At alternatives below θ₀ its power is:",
 ["above α but low", "exactly α", "below α", "exactly zero"],
 "C",
 "The rejection region sits in the tail where alternatives below θ₀ make the data LESS likely than the null does, so the chance of landing in it falls below α. For n = 5, θ₀ = 1 and α = 0.05 the power at θ = 0.5 is 0.003. Power below size is the definition of a biased test — the test is misleading, not merely weak."))

I.append(q(10, "single", "moderate",
 "For H₀: μ = μ₀ against H₁: μ ≠ μ₀ in N(μ, σ²) with σ² known, the two-sided z test is:",
 ["UMP among all tests", "UMP unbiased", "biased", "not a size-α test"],
 "B",
 "It is not UMP — no test is, because the alternative is two-sided and the non-existence argument applies to the normal family as much as to any other. But its power function has its minimum at μ₀, so it is unbiased, and among unbiased tests it is most powerful. UMPU is the precise sense in which this familiar test is optimal."))

I.append(q(11, "multi", "moderate",
 "Consider testing H₀: θ = θ₀ against the two-sided alternative H₁: θ ≠ θ₀ in a one-parameter exponential family.",
 ["A and C only", "B and D only", "A, C and D only", "C and D only"],
 "A",
 "A is true, and it is the reason for the non-existence. B is false — the two-tailed region is a perfectly valid size-α test, it merely is not UMP. C is true: the one-sided test's power drops below α on the far side. D is false; a UMPU test does exist for this problem and is two-tailed, which is the whole point of the unbiasedness restriction.",
 statements=["The most powerful regions against alternatives above and below θ₀ are disjoint.",
             "The two-tailed region is not a valid test of size α.",
             "A one-sided test applied here is biased, with power below α on one side.",
             "No optimal test of any kind exists for this problem."],
 verdicts=verd(
  (True, "True. One is a lower tail of the sufficient statistic and the other an upper tail, with no outcome in common — which is exactly why no single region can win against both."),
  (False, "False. The two-tailed region has size α and is the test one would actually use. It simply is not uniformly most powerful among all tests."),
  (True, "True. Its power falls below α at alternatives on the far side — 0.003 against a size of 0.05 in the standard worked case."),
  (False, "False. Restricting to unbiased tests yields a UMPU test, and restricting to invariant tests yields a UMP invariant test. Optimality is available; it is just relative to a class."))))

I.append(q(12, "single", "moderate",
 "The cut-offs of a two-sided UMPU test are determined by:",
 ["the size condition alone, split equally between the tails",
  "the size condition together with E[φ(T)T | θ₀] = α E[T | θ₀]",
  "the size condition together with the requirement that the test be invariant",
  "maximising the power at a single chosen alternative"],
 "B",
 "Two unknown cut-offs need two equations. The second one is the unbiasedness condition, and it is equivalent to requiring the power function to have its minimum exactly at θ₀. Splitting α equally satisfies the size condition only, and in general fails the second."))

I.append(q(13, "single", "moderate",
 "The equal-tail two-sided test, with α/2 in each tail, is UMP unbiased:",
 ["always", "only when the null distribution of the statistic is symmetric",
  "never", "only for discrete statistics"],
 "B",
 "Equal tails always gives the right size, but it satisfies the unbiasedness condition only when symmetry makes the power minimum fall at θ₀. That holds for the normal mean, so the two-sided z test is UMPU. It fails for a skewed law such as the chi-square of an exponential sum, where the UMPU cut-offs are unequal."))

I.append(q(14, "single", "moderate",
 "For H₀: μ = 0 against H₁: μ ≠ 0 in N(μ, σ²) with σ² unknown, the two-sided t test is UMP invariant under the group of:",
 ["scale changes xᵢ → cxᵢ with c > 0", "location shifts xᵢ → xᵢ + a",
  "all one-to-one transformations of the data", "permutations of the observations"],
 "A",
 "Multiplying every observation by a positive constant sends μ to cμ and σ to cσ, so μ = 0 if and only if cμ = 0 and the problem maps onto itself. The t statistic is unchanged by that transformation and is the maximal invariant. A location shift would move μ away from 0 and change the hypothesis, so it is not a symmetry of this problem."))

I.append(q(15, "numeric", "moderate",
 "X₁,…,X₅ are iid with f(x; θ) = θe^(−θx). For H₀: θ = 1 against H₁: θ < 1 at α = 0.05, with χ²(0.05, 10) = 18.3070, the UMP test rejects when Σxᵢ is:",
 ["≥ 9.1535", "≤ 1.9701", "≥ 18.3070", "≤ 9.1535"],
 "A",
 "A smaller rate means larger observations, so the region against θ < 1 is the upper tail: 2Σxᵢ ≥ 18.3070, giving Σxᵢ ≥ 9.1535. Option B is the region for the opposite alternative, option C omits the division by 2θ₀, and option D has the inequality reversed.",
 check="Smaller rate, larger sum, upper tail. The chi-square point is divided by 2θ₀ = 2, and the inequality points the same way as the tail."))

I.append(q(16, "single", "moderate",
 "Which statement about the hierarchy of optimality notions is correct?",
 ["UMP is a weaker requirement than UMP unbiased",
  "A UMPU test is most powerful among all size-α tests",
  "UMP requires one test to be most powerful at every alternative, while UMPU requires this only among unbiased tests",
  "UMP invariant and UMPU are two names for the same property"],
 "C",
 "UMP is the stronger demand, made over all size-α tests; UMPU narrows the competition to unbiased tests, which is why a winner exists two-sided. A UMPU test can be beaten at a particular alternative by a biased test, so the second option is false. UMPU and UMP invariant are different restrictions that happen to pick out the same test for the standard normal problems."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the equal-tail two-sided test for the exponential rate parameter, with n = 5, θ₀ = 1 and α = 0.05, based on 2Σxᵢ being chi-square with 10 degrees of freedom.",
 ["A and C only", "A, B and C only", "B and D only", "A and D only"],
 "A",
 "A is true — the cut-offs 3.2470 and 20.4832 are the 0.975 and 0.025 points of the 10-degree-of-freedom law, and the two tails sum to exactly 0.05. B is false: evaluated with 2n + 2 = 12 degrees of freedom the unbiasedness condition comes out as 0.0649, not 0.0500, so the test is not UMPU. C is true, and it is why the equal-tail test remains standard practice. D is false — a UMPU test does exist here; its cut-offs are simply unequal.",
 statements=["The equal-tail test has size exactly 0.05.",
             "The equal-tail test satisfies the unbiasedness condition and is therefore UMPU.",
             "The equal-tail test is a valid test and is the one used in practice.",
             "Because equal tails fails the unbiasedness condition, no UMPU test exists for this problem."],
 verdicts=verd(
  (True, "True. The cut-offs are the 0.975 and 0.025 points of the chi-square with 10 df, so the two tail probabilities are 0.025 each."),
  (False, "False. The unbiasedness condition evaluates the same tail probabilities with two extra degrees of freedom, giving 0.0649 against the required 0.0500. The power minimum is therefore not at θ₀."),
  (True, "True. The loss of power is small and the equal-tail cut-offs are far easier to tabulate, so this is a deliberate and accepted approximation in applied work."),
  (False, "False. The UMPU test exists and is found by solving the size and unbiasedness conditions together; the solution simply has unequal tail areas."))))

I.append(q(18, "numeric", "hard",
 "For the one-sided UMP test of H₀: θ = 1 against H₁: θ > 1 for an exponential rate with n = 5 and α = 0.05, rejecting when Σxᵢ ≤ 1.9701, the power at θ = 0.5 is approximately:",
 ["0.003", "0.050", "0.360", "0.500"],
 "A",
 "Under θ = 0.5 the quantity 2(0.5)Σxᵢ = Σxᵢ is chi-square with 10 df, so the power is P(χ²₁₀ ≤ 1.9701) = 0.003. That is far below the size of 0.05, which is the precise sense in which the test is biased at alternatives on the far side. Option C is the power at θ = 2, on the side the test was built for.",
 check="Power below the size of 0.05 is the expected answer here — that is what biased means. A value above 0.05 means the power was evaluated on the wrong side of θ₀."))

I.append(q(19, "single", "hard",
 "A test is UMPU of size α. Which of the following is possible?",
 ["Another size-α test has greater power at some alternative",
  "Another size-α test has greater power at every alternative",
  "Its power is below α at some alternative",
  "It is also the most powerful test against every simple alternative"],
 "A",
 "A UMPU test is best only within the unbiased class, so a BIASED size-α test can beat it at a particular alternative — the one-sided test does exactly that on its own side. It cannot be beaten everywhere at once by a size-α test, its power cannot fall below α since it is unbiased, and it cannot be most powerful against every simple alternative, because such a test would be UMP and none exists two-sided."))

I.append(q(20, "single", "hard",
 "The two-sided t test for a normal mean with σ² unknown is both UMP invariant and UMPU. What does this coincidence indicate?",
 ["that UMP invariance and unbiasedness are equivalent requirements",
  "that two different restrictions happen to select the same test for this problem",
  "that the t test is UMP among all size-α tests",
  "that the t test has no optimality property at all"],
 "B",
 "Invariance under scale changes and unbiasedness are different principles, and in general they could select different tests. For the standard normal problems they agree, which is a large part of why those tests feel inevitable — but it is a feature of the normal family, not a theorem about the two notions. The t test is still not UMP, because the alternative is two-sided."))

# A pool whose keys pile onto one letter rewards a guesser, and the validator caps any
# letter at 40%. Swapping positions i and j is its own inverse, so an "option X" mention
# inside an explanation just swaps the same two letters.
LET = "ABCD"
WANT = {"inf-t17-m-02": "D", "inf-t17-m-03": "C", "inf-t17-m-04": "D",
        "inf-t17-m-06": "C", "inf-t17-m-08": "B", "inf-t17-m-10": "D",
        "inf-t17-m-13": "C", "inf-t17-m-15": "B", "inf-t17-m-18": "B",
        "inf-t17-m-19": "D"}

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
 "moduleId": "inference", "topicId": "inference-t17", "source": "mastery",
 "label": "UMP unbiased and UMP invariant tests — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
