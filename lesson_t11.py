#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 4.11 — The sequential probability ratio test (topic inference-t11).

PYQ evidence, stated plainly: there is NONE. The June 2026 paper contains no question on
sequential testing, and no practice variant in the bank mentions the SPRT, Wald's boundaries,
the OC function or the average sample number. This is the only one of the seven lessons built
in this run with no previous-year anchor at all.

It is built because the syllabus lists it and the catalog gives it 0.46 expected questions per
paper (0.9 marks) — the lowest weight in the module, which is why it was scheduled last. The
`sprt` visualisation had been built and tested but never used by any lesson; this lesson uses
it. With this, inference is complete at 17 of 17 topics.

Writes seed/lesson_t11.json and seed/inference_t11_mastery.json.
Run: python3 lesson_t11.py
"""
import json, io, os, re

OUT = "seed/lesson_t11.json"
POOL = "seed/inference_t11_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Recover the likelihood ratio and the two error rates, because this test is built from nothing else.",
 "ask": {
  "q": "Every test so far fixed the sample size first and then controlled one error rate. What would you have to give up to control BOTH error rates instead?",
  "nudge": "You have three quantities — α, β and n — and so far two were chosen and one followed. Which one is left to let go of?"},
 "body": [
  "Every test in this module so far has had a fixed sample size. You collected n observations, computed a statistic, and decided. The size α was chosen and the power followed from n.",
  "This test does something different. It fixes BOTH error rates in advance — α and β — and lets the sample size be whatever it turns out to be. After every single observation it asks: is the evidence yet strong enough to decide? If yes, stop. If no, take another.",
  "The pay-off is that it usually needs far fewer observations than a fixed-sample test with the same two error rates — about half, in the example this lesson works through. The price is that you cannot say in advance how many you will need.",
  "Four checks. Two on the likelihood ratio, one on the error rates, and one on logarithms, because the boundaries are much easier to use in log form."],
 "items": [
  {"ask": "For a sample of Bernoulli trials with success probability p, write the likelihood ratio of H₁: p = p₁ against H₀: p = p₀ after n trials with Sₙ successes.",
   "recall": "Λₙ = [p₁^Sₙ (1 − p₁)^(n − Sₙ)] / [p₀^Sₙ (1 − p₀)^(n − Sₙ)].",
   "refresh": [
    "Each trial contributes p₁/p₀ if it is a success and (1 − p₁)/(1 − p₀) if it is a failure, and the trials are independent so the contributions multiply.",
    "So the ratio depends on the data only through Sₙ and n — the number of successes and the number of trials. That is why the whole test can be drawn as a picture with n across and Sₙ up.",
    "Note the direction: the ALTERNATIVE is on top here. A large ratio favours H₁. Some books write it the other way up, so read which convention a question uses."]},
  {"ask": "What do α and β denote, and which hypothesis is each computed under?",
   "recall": "α = P(reject H₀ | H₀ true), the Type I error. β = P(accept H₀ | H₁ true), the Type II error. The first is computed under H₀ and the second under H₁.",
   "refresh": [
    "Exactly as in topic 4.12. What is new here is that both are CHOSEN in advance rather than one being chosen and the other falling out.",
    "That is only possible because the sample size is free. With n fixed you cannot pin down both; with n free you can.",
    "Both appear directly in the boundaries, which is unusual and worth noticing when you meet the formulas in the next-but-one section."]},
  {"ask": "If a product of many terms has to be compared with a constant, why is it easier to work with logarithms?",
   "recall": "Because the logarithm turns the product into a sum, so each observation adds a fixed amount instead of multiplying.",
   "refresh": [
    "The ratio Λₙ is a product over observations. Taking logs makes log Λₙ a running total that each new observation adds to — a random walk.",
    "That is the picture the explore section shows: a walk that drifts upward if H₁ is true and downward if H₀ is true, with a boundary on each side.",
    "It also makes the boundaries into two straight lines, which is the form every examination question uses. Products would give curves and no usable arithmetic."]},
  {"ask": "In a fixed-sample Bernoulli test of p₀ = 0.3 against p₁ = 0.6 with α = 0.05 and β = 0.10, roughly how many observations are needed?",
   "recall": "About 22.",
   "refresh": [
    "From n ≈ [z_α √(p₀(1 − p₀)) + z_β √(p₁(1 − p₁))]²/(p₁ − p₀)², which comes to 21.2 and rounds up to 22.",
    "Keep that number. The sequential test for exactly the same two error rates averages about 11 observations under H₀ and about 12 under H₁.",
    "Halving the data for the same error rates is the entire reason this test exists, and section 9 computes those two averages."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Why stop early",
 "objective": "See that a fixed sample size wastes observations when the answer is already obvious.",
 "body": [
  "A fixed-sample test is designed for the worst case. The sample size is chosen so that even when the truth sits awkwardly between the two hypotheses, the error rates are met. When the truth is nowhere near the boundary, that sample size is far more than needed.",
  "Think about what happens in practice. You test twenty-two items because the formula said twenty-two, and the first six are all defective. You already know. The remaining sixteen tests tell you nothing you did not know after six, and if each test destroys the item or costs money, those sixteen are pure waste.",
  "The sequential test formalises stopping when you know. After each observation it compares the accumulated evidence with two thresholds: one high enough to conclude H₁, one low enough to conclude H₀. Between them, it takes another observation.",
  "What you give up is predictability. You cannot tell the supplier how many items you will test, only what it will average. For destructive or expensive testing that trade is usually worth making, which is why this test was invented for wartime munitions inspection and still lives in quality control."],
 "scenario": {
  "teaser": "A pharmaceutical plant tests ampoule seals by destroying the ampoule.",
  "title": "Every test costs a unit",
  "body": [
   "A plant checks seal integrity on glass ampoules. The test destroys the ampoule, so every observation costs a saleable unit. The acceptable defect rate is 3 in 10; a batch running at 6 in 10 must be caught.",
   "The quality engineer's fixed-sample plan says 22 ampoules. Twenty-two destroyed units per batch, every batch, whatever the batch turns out to be like.",
   "The sequential plan tests one at a time and stops as soon as the evidence is conclusive. A clean batch declares itself quickly; so does a badly bad one. Only a batch sitting near the boundary between acceptable and unacceptable needs many observations — and that is the batch where many observations are genuinely warranted.",
   "Across many batches the saving is real: this plan averages about 11 ampoules when the batch is acceptable and about 12 when it is not, against 22 either way. Half the destroyed stock for the same two error rates.",
   "There is a catch the engineer has to accept. On an awkward batch the plan might ask for 30 ampoules, or 40. The average is halved but the maximum is not bounded, which is why real plans add a truncation rule — stop at some n whatever the evidence says, and decide by the nearer boundary. Truncation breaks the exact theory slightly and is used anyway, because an unbounded test is not something a production line can schedule."],
  "q": "Why does a batch near the boundary between 0.3 and 0.6 need more observations than either a clean or a badly bad one?",
  "answer": "Because the evidence per observation is weakest there. Each result shifts the accumulated log-ratio by a fixed amount up or down, and when the true rate sits between the two hypotheses neither direction dominates — the running total drifts slowly and wanders, so it takes many observations to reach either boundary. A clean batch pushes it steadily downward and a bad one steadily upward, so either reaches a boundary fast. The test spends its observations where the question is genuinely hard, which is exactly where they are worth spending."},
 "ask": {
  "q": "The plan's average is about half the fixed-sample size, but its maximum is unbounded. For which kind of testing is that trade clearly worth making, and for which is it not?",
  "nudge": "Think about what each observation costs, and about whether the testing has to fit a schedule."}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Two boundaries and a walk between them",
 "objective": "Watch the boundaries move as the two error rates and the two hypotheses change.",
 "viz": {"type": "sprt", "p0": 0.3, "p1": 0.6, "alpha": 0.05, "beta": 0.10, "phat": 0.45},
 "body": [
  "The two straight lines are the decision boundaries, drawn with the number of observations across and the number of successes up. The path between them is the accumulated count. Cross the upper line and you conclude H₁; cross the lower line and you conclude H₀; stay between them and you take another observation.",
  "Start with p₀ = 0.3, p₁ = 0.6, α = 0.05 and β = 0.10. The two lines are parallel — both have slope 0.447 — and they are separated by a vertical gap. That parallelism is not an accident, and section 11 shows where the common slope comes from.",
  "Now lower α towards 0.01. The upper line lifts away, because you are demanding more evidence before you will reject a true H₀. Lower β instead and the lower line drops. Both changes widen the corridor, and a wider corridor means more observations before a decision.",
  "That is the trade in its clearest form: smaller error rates, more data. The same trade as in topic 4.12, except that here it shows up in the sample size rather than in the power.",
  "Now move the two hypotheses closer together — p₁ down towards 0.4. The slope changes and the corridor's gap widens in effect, because distinguishing 0.3 from 0.4 takes far more evidence than distinguishing 0.3 from 0.6. Push them apart again and the test becomes very quick.",
  "Last thing to try: set the true rate to sit between the hypotheses, around 0.45. The path wanders rather than drifting, and takes much longer to reach either line. That is the case the previous section's scenario was about, and it is where this test spends its observations."],
 "ask": {
  "q": "The two boundary lines are parallel. What would it mean if they crossed at some sample size?",
  "nudge": "If the corridor closed up, what would happen to a path that had not yet reached either boundary?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The test, and Wald's two boundaries",
 "objective": "State the procedure precisely and get the two constants, which is what every question here needs.",
 "blocks": [
  {"t": "def", "h": "The setting",
   "body": "Two SIMPLE hypotheses, H₀: θ = θ₀ against H₁: θ = θ₁. Both error rates α and β are chosen in advance. Observations arrive one at a time and the sample size is not fixed. The test is due to Abraham Wald, who developed it for munitions inspection during the Second World War."},
  {"t": "formula", "h": "The procedure",
   "body": "After each observation form the likelihood ratio\n    Λₙ = L(θ₁ | x₁,…,xₙ) / L(θ₀ | x₁,…,xₙ),\nand compare it with two constants B < 1 < A:\n    Λₙ ≥ A    → stop, reject H₀ (accept H₁)\n    Λₙ ≤ B    → stop, accept H₀\n    B < Λₙ < A → take another observation."},
  {"t": "formula", "h": "Wald's approximations for the boundaries",
   "body": "A ≈ (1 − β)/α      and      B ≈ β/(1 − α)\nThese are the two formulas to know. Note that both error rates appear in both constants, and that A > 1 > B whenever α and β are less than a half."},
  {"t": "step", "h": "Why the boundaries take those values, in one line each",
   "body": "Consider the sample paths that end by rejecting H₀. On every such path Λₙ ≥ A, so the probability of that set under H₁ is at least A times its probability under H₀ — that is, 1 − β ≥ A α, giving A ≤ (1 − β)/α. The mirror argument on the paths that accept H₀ gives B ≥ β/(1 − α). Wald's approximation is to take these bounds as equalities, which is exact only if the ratio lands exactly on a boundary rather than overshooting it. The optional section at the end quantifies what that costs."},
  {"t": "formula", "h": "The log form, which is what you actually compute with",
   "body": "Taking logarithms turns the product into a sum:\n    log B < log Λₙ < log A   continue\nwhere log Λₙ = Σ zᵢ and zᵢ is the log-ratio contributed by observation i. For Bernoulli trials with Sₙ successes in n trials,\n    log Λₙ = Sₙ log(p₁/p₀) + (n − Sₙ) log((1 − p₁)/(1 − p₀))."},
  {"t": "step", "h": "The two boundaries as straight lines",
   "body": "Rearranging the log inequalities for Sₙ gives two parallel lines in the (n, Sₙ) plane:\n    accept H₀ when  Sₙ ≤ −b + s n\n    reject H₀ when  Sₙ ≥  a + s n\nwith common slope s = log((1 − p₀)/(1 − p₁)) / log(p₁(1 − p₀)/(p₀(1 − p₁))), and intercepts a = log A / k and b = −log B / k where k is that same denominator. The slope depends only on the two hypotheses; the intercepts carry the two error rates. That is why changing α moves one line without tilting it."}],
 "flow": {
  "title": "One cycle of the test",
  "alt": "Flow chart of the sequential probability ratio test",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "Choose θ₀, θ₁, α and β; compute A and B", "kind": "start"},
   {"id": "b", "r": 1, "c": 1, "label": "Take the next observation", "kind": "step"},
   {"id": "c", "r": 2, "c": 1, "label": "Update log Λₙ by adding this observation's log-ratio", "kind": "step"},
   {"id": "d", "r": 3, "c": 0, "label": "log Λₙ ≥ log A → reject H₀", "kind": "end"},
   {"id": "e", "r": 3, "c": 2, "label": "log Λₙ ≤ log B → accept H₀", "kind": "end"},
   {"id": "f", "r": 4, "c": 1, "label": "otherwise: between the boundaries", "kind": "step"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "b", "to": "c"},
   {"from": "c", "to": "d", "label": "upper crossed"},
   {"from": "c", "to": "e", "label": "lower crossed"},
   {"from": "c", "to": "f", "label": "neither"},
   {"from": "f", "to": "b", "label": "continue"}],
  "note": "The only loop in any test in this module. Everything else here decides once; this decides after every observation."},
 "ask": {
  "q": "Both α and β appear in both A and B. Why can a fixed-sample test not fix both error rates the way this one does?",
  "nudge": "With n fixed, how many of the three quantities α, β and n are you free to choose?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — the boundaries for a Bernoulli test",
 "objective": "Turn the formulas into two numbers and two lines you could hand to an inspector.",
 "ask": {
  "q": "The two lines have the same slope, 0.4467. What does a slope of about 0.45 mean in plain terms?",
  "nudge": "The line is a number of successes against a number of trials. What is a slope on those axes measuring?"},
 "problem": "Construct the SPRT for H₀: p = 0.3 against H₁: p = 0.6 with α = 0.05 and β = 0.10, giving the boundaries both as constants on the likelihood ratio and as two lines in the (n, Sₙ) plane.",
 "steps": [
  {"say": "Compute the two boundary constants.",
   "math": "A = (1 − β)/α = 0.90/0.05 = 18\nB = β/(1 − α) = 0.10/0.95 = 0.10526",
   "why": "Stop and reject H₀ once the alternative is 18 times better supported than the null; stop and accept H₀ once it is about 9.5 times worse. Both numbers follow from the two error rates alone."},
  {"say": "Take logarithms, since the computation is additive.",
   "math": "log A = log 18    = 2.890372\nlog B = log 0.10526 = −2.251292",
   "why": "These are the two levels the running total has to reach. Natural logarithms throughout; using base 10 is fine provided it is used everywhere."},
  {"say": "Write the per-observation contributions.",
   "math": "a success adds log(p₁/p₀)          = log(0.6/0.3) = log 2   =  0.693147\na failure adds log((1−p₁)/(1−p₀))  = log(0.4/0.7)          = −0.559616",
   "why": "Every observation moves the total by one of exactly two amounts. The success step is larger in magnitude than the failure step, which is why a run of successes reaches its boundary sooner than a run of failures reaches the other."},
  {"say": "Rearrange for Sₙ to get the two lines. The denominator k is the difference of the two step sizes.",
   "math": "k = 0.693147 − (−0.559616) = 1.252763\n  = log(p₁(1−p₀)/(p₀(1−p₁))) = log 3.5 ✓\ns = 0.559616/1.252763 = 0.44671\na = 2.890372/1.252763 = 2.3072\nb = 2.251292/1.252763 = 1.7971",
   "why": "The check in the second line is worth doing: k should come out as log of p₁(1−p₀)/(p₀(1−p₁)) = (0.6 × 0.7)/(0.3 × 0.4) = 3.5, and log 3.5 = 1.2528. If your k does not match, one of the two step sizes has a sign error."},
  {"say": "State the decision rule an inspector could use.",
   "math": "after n items with Sₙ defectives:\n  reject H₀ (lot bad)  if  Sₙ ≥ 2.3072 + 0.44671 n\n  accept H₀ (lot good) if  Sₙ ≤ −1.7971 + 0.44671 n\n  otherwise test one more",
   "why": "Two lines, computed once, usable by anyone with a tally sheet. That practicality is why the method survived into industrial sampling standards."}],
 "after": "Notice what each ingredient controlled. The two hypotheses fixed the slope 0.4467 — and 0.4467 sits between 0.3 and 0.6, which is the sense in which the boundary tracks a rate partway between the two. The two error rates fixed the intercepts and so the width of the corridor, without tilting either line. Those two facts answer most conceptual questions on this topic."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the procedure and the two boundary formulas.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "What is fixed in advance in an SPRT, and what is not?",
   "a": "Both error rates α and β are fixed; the sample size is not. It is a random variable."},
  {"q": "Give Wald's two boundary constants.",
   "a": "A ≈ (1 − β)/α for rejecting H₀, and B ≈ β/(1 − α) for accepting H₀."},
  {"q": "What happens when the ratio lies strictly between B and A?",
   "a": "Take another observation. No decision is made."},
  {"q": "For α = 0.05 and β = 0.10, what are A and B?",
   "a": "A = 0.90/0.05 = 18 and B = 0.10/0.95 = 0.1053."},
  {"q": "What kind of hypotheses does the SPRT test?",
   "a": "Two simple hypotheses — one specified value against another specified value."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — run the test on a sequence",
 "objective": "Apply the boundaries observation by observation and find where the test stops.",
 "problem": "Using the boundaries from section 4 — reject H₀ if Sₙ ≥ 2.3072 + 0.44671n, accept H₀ if Sₙ ≤ −1.7971 + 0.44671n — run the test on the sequence of results 1, 1, 0, 1, 1, 1 where 1 is a defective.",
 "steps": [
  {"say": "Start with the first two observations, both defective.",
   "blank": {"prompt": "At n = 2 with S₂ = 2, what are the two boundary values and what is the decision?",
             "answer": "reject if S ≥ 3.201, accept if S ≤ −0.904; so continue",
             "accept": ["3.201 and -0.904, continue", "continue",
                        "reject needs 3.20, accept needs -0.90, so continue",
                        "neither boundary reached, take another"],
             "hint": "Substitute n = 2 into both lines. Can a count of successes ever be negative?"},
   "why": "2.3072 + 2(0.44671) = 3.201 and −1.7971 + 2(0.44671) = −0.904. The lower boundary is negative, so accepting H₀ is impossible this early whatever happens — a count cannot be below zero."},
  {"say": "Work out the earliest observation at which the test could possibly stop at all.",
   "blank": {"prompt": "What is the smallest n at which a decision is even possible?",
             "answer": "n = 5, for either decision",
             "accept": ["5", "n=5", "five", "n = 5 either way"],
             "hint": "For rejection you need Sₙ ≥ a + sn with Sₙ at most n, so n(1 − s) ≥ a. For acceptance you need the lower boundary to reach zero."},
   "why": "Rejection needs n(1 − 0.44671) ≥ 2.3072, so n ≥ 4.17 and therefore n = 5 with all five defective. Acceptance needs −1.7971 + 0.44671n ≥ 0, so n ≥ 4.02 and therefore n = 5 with none defective. No SPRT can decide before its boundaries come within reach of the attainable counts."},
  {"say": "Now continue through the sequence to n = 5.",
   "blank": {"prompt": "The results are 1, 1, 0, 1, 1. At n = 5, what is S₅ and what is the decision?",
             "answer": "S₅ = 4, and since the rejection boundary is 4.541 the test continues",
             "accept": ["S=4, continue", "4, continue", "S5 = 4 so continue, 4 < 4.541",
                        "four defectives, not yet"],
             "hint": "2.3072 + 5(0.44671) = 4.541. Is 4 at or above that?"},
   "why": "Four defectives against a boundary of 4.541 — just short. One more observation is needed, and this is the kind of near-miss that makes the test feel finely balanced at small n."},
  {"say": "Take the sixth observation, also defective.",
   "blank": {"prompt": "At n = 6 with S₆ = 5, what is the decision?",
             "answer": "reject H₀ — the boundary is 4.987 and 5 exceeds it",
             "accept": ["reject H0", "reject, 5 >= 4.987", "stop and reject the null",
                        "accept H1, p = 0.6"],
             "hint": "2.3072 + 6(0.44671) = 4.987."},
   "why": "The test stops at n = 6 and concludes p = 0.6. Six observations, against the 22 a fixed-sample test with the same error rates would have required — and this was a fairly clear-cut sequence, which is exactly when the sequential test earns its keep."}],
 "after": "Two things worth taking from this. The lower boundary is negative for small n, so acceptance is impossible early no matter how clean the data — the test cannot clear a lot on two good items. And the stopping point is random: the same test on a different sequence from the same source might have taken 6 observations or 30. The next section is about what it takes on average."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "The OC function, the ASN, and what the approximations cost",
 "objective": "Learn the two functions that describe how the test behaves, and the inequality that bounds its real error rates.",
 "blocks": [
  {"t": "def", "h": "The operating characteristic function",
   "body": "L(θ) is the probability that the test eventually accepts H₀ when the true parameter is θ. It is the sequential analogue of the power function, read the other way up. Two of its values are known by construction: L(θ₀) = 1 − α and L(θ₁) = β. Between them it decreases smoothly, and it tends to 1 for θ far on the null side and 0 for θ far on the alternative side."},
  {"t": "def", "h": "The average sample number",
   "body": "E(N | θ) is the expected number of observations before stopping, as a function of the true parameter. It is largest for θ between the two hypotheses — where the evidence per observation is weakest — and falls away on either side. Quoting a single 'sample size' for an SPRT is meaningless; the ASN at the two hypotheses is the usual summary."},
  {"t": "formula", "h": "Wald's approximation for the ASN",
   "body": "E(N | θ) ≈ [ (1 − L(θ)) log A + L(θ) log B ] / E_θ[Z]\nwhere Z is the log-likelihood-ratio contributed by one observation. At the two hypotheses this gives\n    E(N | H₀) ≈ [α log A + (1 − α) log B] / E₀[Z]\n    E(N | H₁) ≈ [(1 − β) log A + β log B] / E₁[Z]\nwith E₀[Z] negative and E₁[Z] positive, so both come out positive as they must."},
  {"t": "step", "h": "The error probabilities are not exactly α and β",
   "body": "Because the running total overshoots a boundary rather than landing exactly on it, the true error rates α' and β' differ slightly from the nominal α and β. Wald's bounds give α' ≤ α/(1 − β) and β' ≤ β/(1 − α), and the practical statement worth remembering is α' + β' ≤ α + β. So the test is at least as good as advertised in total, though the split between the two may shift. For small α and β the discrepancy is negligible."},
  {"t": "step", "h": "The test terminates",
   "body": "It is not obvious that the procedure stops at all — in principle the ratio could stay between the boundaries forever. Wald proved that it terminates with probability 1 whenever the per-observation log-ratio is not degenerate, and that E(N) is finite. So the sample size is a genuine random variable with a finite mean, not a possibility of running forever. In practice plans are still truncated at some maximum, because an unbounded test cannot be scheduled."}],
 "ask": {
  "q": "L(θ₀) = 1 − α and L(θ₁) = β. Why are those two values true by construction rather than something to be derived?",
  "nudge": "What does 'accepting H₀ when H₀ is true' mean in terms of α? And 'accepting H₀ when H₁ is true' in terms of β?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — the average sample number",
 "objective": "Compute the two headline numbers and compare them with the fixed-sample alternative.",
 "problem": "For the test of section 4 — p₀ = 0.3, p₁ = 0.6, α = 0.05, β = 0.10 — compute (a) E₀[Z] and E₁[Z], (b) the ASN under H₀, (c) the ASN under H₁, and (d) the comparison with the fixed-sample size of 22.",
 "hints": [
  "For (a), Z takes the value log(p₁/p₀) = 0.693147 with probability p and log((1−p₁)/(1−p₀)) = −0.559616 with probability 1 − p. Take the expectation under each hypothesis in turn.",
  "For (b) and (c), use E(N|H₀) ≈ [α log A + (1 − α) log B]/E₀[Z] and E(N|H₁) ≈ [(1 − β) log A + β log B]/E₁[Z], with log A = 2.890372 and log B = −2.251292.",
  "Both answers must come out positive. Under H₀ a negative numerator divides a negative E₀[Z]; under H₁ both are positive."],
 "answer": "(a) E₀[Z] = −0.18379, E₁[Z] = 0.19204. (b) 10.85. (c) 12.37. (d) About half of 22, for the same two error rates.",
 "check": "Three things worth checking. Both ASN values must be positive — if one comes out negative, the sign of E₀[Z] or of log B has been mishandled, and that is the commonest slip here. E₀[Z] must be negative and E₁[Z] positive: under the null the evidence drifts downward on average, which is what makes the test eventually accept H₀. And the comparison in (d) is the point of the whole topic: 10.85 and 12.37 against 22, so roughly half the observations for identical α and β. Note also that the ASN is largest somewhere between the two hypotheses, not at either of them, so neither of these two numbers is the worst case.",
 "scenario": {
  "teaser": "The engineer has to justify the sequential plan to a production manager who schedules shifts.",
  "title": "Half the units, but you cannot say how many",
  "body": [
   "The quality engineer takes the numbers to the production manager. The sequential plan uses about 11 ampoules on a good batch against 22 for the fixed plan, with the same risk of passing a bad batch and the same risk of rejecting a good one. On the stock saved alone it is an easy case.",
   "The manager's objection is not about statistics. The fixed plan needs a known number of ampoules and a known slot of inspector time; the sequential plan needs an unknown number. A line that schedules inspection in fixed blocks cannot absorb 'somewhere between 5 and 40, averaging 11'.",
   "Both are right, and the usual resolution is a truncated plan: run the sequential test but stop at, say, 30 observations whatever the evidence, deciding by whichever boundary is nearer. That bounds the schedule, keeps most of the saving, and costs a small, computable change to the two error rates.",
   "Worth being clear that truncation is a departure from the theory. Wald's boundaries assume the test can run as long as it needs; cutting it short alters the real α and β, and a careful plan recomputes them by simulation. It is done anyway, universally, because the alternative is a plan nobody can staff.",
   "This is a general pattern in applied statistics rather than a quirk of the SPRT: the optimal procedure is modified to fit the constraints of the place it will actually run, and the modification is reported rather than hidden."],
  "q": "The manager wants a bounded plan. What is actually given up by truncating at 30?",
  "answer": "The exactness of the two error rates. Wald's A and B assume the test may continue indefinitely; forcing a decision at n = 30 means some paths are decided on weaker evidence than the boundaries required, so the true α and β shift — usually slightly upward for one of them. The average sample number barely changes, since paths reaching 30 are rare, so almost all of the saving survives. The honest practice is to recompute the real error rates for the truncated plan rather than quoting the nominal ones."},
 "solution": [
  {"say": "(a) Compute the expected log-ratio per observation under each hypothesis.",
   "math": "E₀[Z] = 0.3(0.693147) + 0.7(−0.559616) = 0.207944 − 0.391731 = −0.183787\nE₁[Z] = 0.6(0.693147) + 0.4(−0.559616) = 0.415888 − 0.223846 =  0.192042",
   "why": "Negative under H₀ and positive under H₁ — the walk drifts towards the correct boundary in each case, which is why the test works at all."},
  {"say": "(b) The ASN under H₀.",
   "math": "numerator = 0.05(2.890372) + 0.95(−2.251292)\n          = 0.144519 − 2.138727 = −1.994208\nE(N | H₀) = −1.994208 / −0.183787 = 10.85",
   "why": "Two negatives give a positive. About 11 observations on a good lot."},
  {"say": "(c) The ASN under H₁.",
   "math": "numerator = 0.90(2.890372) + 0.10(−2.251292)\n          = 2.601335 − 0.225129 = 2.376206\nE(N | H₁) = 2.376206 / 0.192042 = 12.37",
   "why": "About 12 observations on a bad lot. Slightly more than under H₀ here, because the failure step is smaller in magnitude than the success step."},
  {"say": "(d) Compare with the fixed-sample test.",
   "math": "fixed-sample n = 22   (from the opening checks)\nsequential: 10.85 under H₀, 12.37 under H₁\nsaving ≈ 51% under H₀, ≈ 44% under H₁",
   "why": "Half the data for the same two error rates. This is the result that justifies the whole method, and it is the number to quote if a question asks why one would use an SPRT at all."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the claims a question on this topic would use.",
 "intro": "Decide true or false on all six before revealing any.",
 "items": [
  {"claim": "In an SPRT both the Type I and Type II error probabilities are fixed in advance.",
   "tf": True,
   "why": "True, and it is what distinguishes the method. A fixed-sample test can fix one and let the other follow from n; here the sample size is free, which leaves room to fix both."},
  {"claim": "The sample size of an SPRT is fixed before sampling begins.",
   "tf": False,
   "why": "False — it is a random variable. Wald proved the test terminates with probability 1 and that E(N) is finite, but no bound is fixed in advance, which is why practical plans add a truncation rule."},
  {"claim": "The boundary constants are A = (1 − β)/α and B = β/(1 − α).",
   "tf": True,
   "why": "True, as Wald's approximations. Both error rates appear in both constants. For α = 0.05 and β = 0.10 they give A = 18 and B = 0.1053."},
  {"claim": "The SPRT can test a composite null against a composite alternative directly.",
   "tf": False,
   "why": "False. The likelihood ratio needs both hypotheses completely specified, so the SPRT in this form is for simple against simple — the same restriction as the Neyman–Pearson lemma. Extensions exist but are outside this syllabus."},
  {"claim": "The average sample number is largest when the true parameter lies between θ₀ and θ₁.",
   "tf": True,
   "why": "True. There the evidence per observation is weakest and the accumulated ratio wanders rather than drifting, so it takes longest to reach either boundary. Neither E(N|H₀) nor E(N|H₁) is the worst case."},
  {"claim": "The true error probabilities of an SPRT are exactly the nominal α and β.",
   "tf": False,
   "why": "False, because the ratio overshoots a boundary rather than landing on it. The true rates satisfy α' ≤ α/(1 − β) and β' ≤ β/(1 − α), and in particular α' + β' ≤ α + β — so the test is no worse in total, though the split can shift. For small α and β the difference is negligible."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 7,
 "title": "On your own — from the log boundaries to the two lines",
 "objective": "Derive the line form, since that is what an examination question hands you or asks for.",
 "problem": "Starting from log B < Sₙ log(p₁/p₀) + (n − Sₙ) log((1 − p₁)/(1 − p₀)) < log A, derive the two boundary lines in the form Sₙ = (intercept) + s n, and identify the slope and both intercepts for p₀ = 0.3, p₁ = 0.6, α = 0.05, β = 0.10.",
 "hints": [
  "Group the terms in Sₙ and the terms in n separately. Write u = log(p₁/p₀) and v = log((1 − p₁)/(1 − p₀)), so the middle expression is Sₙ u + (n − Sₙ)v.",
  "That rearranges to Sₙ(u − v) + n v. Call k = u − v, and note that k is positive while v is negative.",
  "Divide through by k and isolate Sₙ. The slope will come out as −v/k, which is positive because v is negative."],
 "answer": "Slope s = −v/k = 0.44671; upper intercept log A/k = 2.3072; lower intercept log B/k = −1.7971.",
 "check": "Two things to be careful about. k = u − v is a DIFFERENCE of the two step sizes, and since v is negative the difference is larger than u alone — here 1.2528 rather than 0.6931. And the slope is −v/k, with the minus sign making it positive; writing v/k gives a negative slope and two lines sloping the wrong way, which is the standard error in this derivation. A useful check: the slope must lie between p₀ and p₁, since it is the defect rate at which the test is indifferent — here 0.4467 sits between 0.3 and 0.6.",
 "solution": [
  {"say": "Name the two step sizes and group the terms.",
   "math": "u = log(p₁/p₀) = 0.693147,  v = log((1−p₁)/(1−p₀)) = −0.559616\nSₙ u + (n − Sₙ) v = Sₙ(u − v) + n v\nk = u − v = 1.252763",
   "why": "Everything now depends on Sₙ through a single coefficient k, which is what makes the boundaries straight lines."},
  {"say": "Substitute into the continuation inequality.",
   "math": "log B < Sₙ k + n v < log A",
   "why": "The n v term is what gives the lines their slope; without it both boundaries would be horizontal."},
  {"say": "Isolate Sₙ by subtracting n v and dividing by k, which is positive so the inequalities keep their direction.",
   "math": "(log B − n v)/k  <  Sₙ  <  (log A − n v)/k\nSₙ ∈ ( log B/k + n(−v/k),  log A/k + n(−v/k) )",
   "why": "Dividing by a positive k preserves the direction. The term −v/k is the common slope, and it is positive because v is negative."},
  {"say": "Put the numbers in.",
   "math": "s = −v/k = 0.559616/1.252763 = 0.44671\nupper: log A/k = 2.890372/1.252763 =  2.3072\nlower: log B/k = −2.251292/1.252763 = −1.7971\nreject H₀ if Sₙ ≥ 2.3072 + 0.44671 n;  accept H₀ if Sₙ ≤ −1.7971 + 0.44671 n",
   "why": "The same two lines as section 4, now derived rather than quoted. The slope came only from the hypotheses and the intercepts only from the error rates, which is the structural fact worth retaining."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "What the SPRT is optimal for, and what it cannot do",
 "objective": "Place the test against the rest of the module, which is how a conceptual question would frame it.",
 "blocks": [
  {"t": "step", "h": "The optimality result",
   "body": "Wald and Wolfowitz proved that among ALL tests, sequential or fixed, with error probabilities no larger than α and β, the SPRT minimises the expected sample size under BOTH H₀ and H₁ simultaneously. That is an unusually strong statement — most optimality results in this module hold at one parameter value or within a restricted class. Here one procedure is best at both hypotheses at once."},
  {"t": "def", "h": "Where it sits among the tests of this module",
   "body": "Neyman–Pearson (topic 4.9) gives the most powerful test of simple against simple at a fixed sample size. The SPRT takes the same two simple hypotheses and the same likelihood ratio, and optimises a different thing — the expected sample size for given error rates. They are two answers to two questions about the same ratio, which is why both are called likelihood ratio tests and neither supersedes the other."},
  {"t": "step", "h": "The limitations, as a question would list them",
   "body": "It needs two SIMPLE hypotheses, so a composite problem has to be reduced to two representative values. The sample size is unbounded in principle, so practical plans truncate and thereby disturb the error rates. The optimality is about the expected sample size at the two hypotheses only — in the middle, where the ASN is largest, the SPRT is not especially efficient. And observations must arrive one at a time and be assessable immediately, which rules out any setting where the response takes longer to measure than the next item takes to arrive."},
  {"t": "step", "h": "Where it is actually used",
   "body": "Acceptance sampling and destructive testing, where each observation costs a unit; clinical trial monitoring, where continuing to randomise patients to a treatment already shown to be worse is unethical, so stopping early is a duty rather than an economy; and automated monitoring, where a decision rule has to run continuously on arriving data. The common feature is that observations are costly and arrive one at a time — exactly the conditions the method was designed for."}],
 "ask": {
  "q": "The SPRT minimises the expected sample size at θ₀ and θ₁ but not in between, where the ASN is largest. Why is that an acceptable trade in acceptance sampling?",
  "nudge": "In a lot-inspection setting, how often is the true defect rate exactly at the awkward value between the two hypotheses, compared with being clearly good or clearly bad?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the formulas and the two named results.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Give A and B for α = 0.02 and β = 0.05.",
   "a": "A = (1 − 0.05)/0.02 = 47.5 and B = 0.05/0.98 = 0.05102."},
  {"q": "What does the operating characteristic function L(θ) give, and what are L(θ₀) and L(θ₁)?",
   "a": "The probability of eventually accepting H₀ when θ is true. L(θ₀) = 1 − α and L(θ₁) = β."},
  {"q": "State the Wald–Wolfowitz optimality property.",
   "a": "Among all tests with error probabilities at most α and β, the SPRT minimises the expected sample size under both H₀ and H₁."},
  {"q": "What inequality bounds the true error rates of an SPRT?",
   "a": "α' + β' ≤ α + β, with α' ≤ α/(1 − β) and β' ≤ β/(1 − α). The overshoot past a boundary is why they are not exact."},
  {"q": "Where is the average sample number largest?",
   "a": "At a parameter value between θ₀ and θ₁, where the evidence per observation is weakest — not at either hypothesis."},
  {"q": "What does the slope of the two boundary lines depend on?",
   "a": "Only the two hypotheses. The error rates fix the intercepts, so changing α shifts a line without tilting it."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test, and with it Module 4.",
 "body": [
  "State the SPRT: fix both error rates, compute the likelihood ratio after each observation, and stop when it leaves the corridor between B and A.",
  "Compute Wald's boundaries A = (1 − β)/α and B = β/(1 − α), and take their logarithms for use.",
  "Derive the two parallel boundary lines in the (n, Sₙ) plane for Bernoulli data, knowing that the slope comes from the hypotheses and the intercepts from the error rates.",
  "Run the test on a given sequence and find where it stops, including knowing why no decision is possible very early.",
  "Define the operating characteristic function and the average sample number, and quote L(θ₀) = 1 − α and L(θ₁) = β.",
  "Compute the ASN at both hypotheses by Wald's formula and compare it with the fixed-sample size — about half, in the standard example.",
  "State the Wald–Wolfowitz optimality property, and the limitations: simple hypotheses only, unbounded sample size, and the α' + β' ≤ α + β inequality."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "Why A and B are approximations",
 "objective": "See exactly where the overshoot enters and what it costs, which explains the error-rate inequality.",
 "blocks": [
  {"t": "step", "h": "The exact argument, as far as it goes",
   "body": "Let R be the set of sample paths on which the test stops by rejecting H₀. On every path in R the ratio satisfies Λ ≥ A at the stopping point, which means the probability of that path under H₁ is at least A times its probability under H₀. Summing over R gives P₁(R) ≥ A P₀(R), that is 1 − β ≥ A α. So A ≤ (1 − β)/α exactly, as an inequality."},
  {"t": "step", "h": "Where the approximation enters",
   "body": "The step from inequality to equality assumes Λ equals A exactly at the stopping point. It does not: the walk takes a discrete step and lands somewhere at or beyond the boundary. That excess is the overshoot, and it is why A = (1 − β)/α is an approximation rather than an identity. The approximation is good when the individual steps are small relative to the gap between the boundaries, which is the case when α and β are small."},
  {"t": "formula", "h": "What the inequalities give",
   "body": "Running the same argument in both directions with A and B set to their nominal values gives, for the true error rates,\n    α' ≤ α/(1 − β)   and   β' ≤ β/(1 − α),\nand adding them yields the practical statement\n    α' + β' ≤ α + β."},
  {"t": "step", "h": "Reading that inequality",
   "body": "The test is never worse than advertised in TOTAL error, but the split can move: the realised α' might exceed α slightly while β' falls below β by at least as much. For α = 0.05 and β = 0.10 the bounds are α' ≤ 0.0556 and β' ≤ 0.1053 — close enough that the nominal values are reported in practice. For large error rates, or for a discrete observation whose step size is comparable with the corridor width, the discrepancy is worth computing."},
  {"t": "step", "h": "The practical consequence, and the honest report",
   "body": "Two departures from the theory accumulate in a real plan: the overshoot above, and truncation at a maximum sample size. Both are small, both are in the same direction of making the nominal rates approximate, and both are handled the same way — by simulating the plan to obtain its actual α' and β' rather than quoting the design values. That is the difference between a textbook SPRT and one a regulator would accept."}],
 "ask": {
  "q": "The bounds give α' ≤ 0.0556 against a nominal 0.05. Would you expect the overshoot to matter more for a Bernoulli observation or for a normal one?",
  "nudge": "A Bernoulli observation moves the walk by one of two fixed amounts. A normal observation moves it by a continuous amount. Which can land closer to a boundary?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "inference_t11_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "inferencet11",
 "topicId": "inference-t11",
 "moduleId": "inference",
 "title": "The Sequential Probability Ratio Test",
 "breadcrumb": "Statistical Inference → Testing of Hypotheses → Sequential testing",
 "engine": "C",
 "engineName": "Testing — deciding after every observation instead of at a fixed sample size",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "State the SPRT procedure and say what it fixes in advance and what it leaves free.",
  "Compute Wald's boundary constants A = (1 − β)/α and B = β/(1 − α) and their logarithms.",
  "Derive the two parallel boundary lines for Bernoulli data and identify the slope and intercepts.",
  "Run the test on a given sequence and find the stopping point.",
  "Define the OC function and the ASN, and compute the ASN at both hypotheses by Wald's formula.",
  "State the Wald–Wolfowitz optimality property and the method's limitations, including α' + β' ≤ α + β."],
 "prereq": [
  {"id": "p1", "name": "Neyman–Pearson, MLR and UMP tests",
   "why": "The SPRT is built from the same likelihood ratio as the Neyman–Pearson lemma and tests the same kind of hypotheses — two simple ones. It optimises a different quantity."},
  {"id": "p2", "name": "Size and power of a test",
   "why": "Both α and β are fixed in advance here, so the two definitions and which hypothesis each is computed under must be secure."},
  {"id": "p3", "name": "The likelihood function",
   "why": "Every step is a likelihood ratio evaluated at two specified parameter values, accumulated over observations."},
  {"id": "p4", "name": "Logarithms and expectations",
   "why": "The boundaries are used in log form, and the ASN formula is an expectation of a log-ratio. Both are routine but both appear in every calculation."}],
 "traps": [
  "Both α and β are fixed; the SAMPLE SIZE is the random quantity.",
  "A = (1 − β)/α and B = β/(1 − α) — both error rates appear in both constants.",
  "The slope of the boundary lines comes from the hypotheses; the intercepts carry the error rates.",
  "The slope is −v/k, and the minus sign matters — v is negative.",
  "Both ASN values must come out positive; E₀[Z] is negative and E₁[Z] positive.",
  "The ASN is largest BETWEEN the hypotheses, so neither E(N|H₀) nor E(N|H₁) is the worst case.",
  "Simple against simple only.",
  "The true error rates are not exactly α and β; α' + β' ≤ α + β."],
 "revision": {
  "sheet": [
   "The SPRT fixes both α and β in advance and leaves the sample size random.",
   "After each observation compute Λₙ = L(θ₁)/L(θ₀). Reject H₀ if Λₙ ≥ A, accept H₀ if Λₙ ≤ B, otherwise continue.",
   "Wald's boundaries: A ≈ (1 − β)/α and B ≈ β/(1 − α). For α = 0.05, β = 0.10: A = 18, B = 0.1053.",
   "Log form: log Λₙ = Σ zᵢ, a random walk. For Bernoulli, log Λₙ = Sₙ log(p₁/p₀) + (n − Sₙ) log((1 − p₁)/(1 − p₀)).",
   "Boundary lines: accept H₀ if Sₙ ≤ −b + sn; reject H₀ if Sₙ ≥ a + sn. Parallel, common slope.",
   "s = log((1 − p₀)/(1 − p₁)) / log(p₁(1 − p₀)/(p₀(1 − p₁))), a = log A/k, b = −log B/k, with k the same denominator.",
   "Worked example p₀ = 0.3, p₁ = 0.6, α = 0.05, β = 0.10: k = log 3.5 = 1.2528, s = 0.44671, a = 2.3072, b = 1.7971.",
   "So reject H₀ if Sₙ ≥ 2.3072 + 0.44671n; accept H₀ if Sₙ ≤ −1.7971 + 0.44671n.",
   "The slope must lie between p₀ and p₁ — a useful check; 0.4467 lies between 0.3 and 0.6.",
   "No decision is possible before n = 5 in that example: rejection needs n(1 − s) ≥ a, acceptance needs −b + sn ≥ 0.",
   "OC function L(θ) = P(accept H₀ | θ), with L(θ₀) = 1 − α and L(θ₁) = β by construction.",
   "ASN: E(N | θ) ≈ [(1 − L(θ)) log A + L(θ) log B]/E_θ[Z].",
   "At the hypotheses: E(N|H₀) ≈ [α log A + (1 − α) log B]/E₀[Z] and E(N|H₁) ≈ [(1 − β) log A + β log B]/E₁[Z].",
   "Worked ASN: E₀[Z] = −0.18379, E₁[Z] = 0.19204, giving 10.85 under H₀ and 12.37 under H₁ against a fixed-sample 22 — about half.",
   "The ASN is largest for θ between θ₀ and θ₁, where the walk wanders rather than drifting.",
   "True error rates: α' ≤ α/(1 − β), β' ≤ β/(1 − α), and α' + β' ≤ α + β. The cause is overshoot past a boundary.",
   "Wald proved termination with probability 1 and finite E(N). Practical plans still truncate, which disturbs the error rates.",
   "Wald–Wolfowitz: among all tests with error probabilities at most α and β, the SPRT minimises the expected sample size under both H₀ and H₁.",
   "Limitations: simple against simple only; unbounded sample size; optimality at the two hypotheses only; observations must be assessable one at a time."],
  "cards": [
   ["What an SPRT fixes", "Both error rates α and β; the sample size is left random"],
   ["The procedure", "After each observation: Λₙ ≥ A reject H₀, Λₙ ≤ B accept H₀, in between take another"],
   ["Wald's boundaries", "A = (1 − β)/α and B = β/(1 − α) — both rates in both constants"],
   ["A and B for 0.05 and 0.10", "A = 18 and B = 0.1053"],
   ["The two boundary lines", "Parallel: Sₙ = a + sn to reject, Sₙ = −b + sn to accept"],
   ["Where the slope comes from", "The two hypotheses alone; the error rates fix only the intercepts"],
   ["A check on the slope", "It must lie between p₀ and p₁ — 0.4467 between 0.3 and 0.6"],
   ["OC function", "L(θ) = P(accept H₀ | θ), with L(θ₀) = 1 − α and L(θ₁) = β"],
   ["ASN at the hypotheses", "10.85 and 12.37 in the standard example, against a fixed-sample 22"],
   ["Where the ASN peaks", "Between the two hypotheses, where the evidence per observation is weakest"],
   ["The error-rate inequality", "α' + β' ≤ α + β, because the walk overshoots its boundary"],
   ["Wald–Wolfowitz", "Minimises the expected sample size under BOTH hypotheses among all tests with those error rates"]],
  "tricks": [
   "Compute A and B first; they need only α and β and they anchor everything else.",
   "Check that your slope lies between p₀ and p₁. If it does not, a sign has gone wrong in k or in −v/k.",
   "Check that k equals log of p₁(1 − p₀)/(p₀(1 − p₁)); for 0.3 and 0.6 that is log 3.5 = 1.2528.",
   "Both ASN answers must be positive. Under H₀ the numerator and E₀[Z] are both negative.",
   "If a question asks why one would use an SPRT, the answer is a number: about half the observations for the same two error rates."],
  "shortcuts": [
   "The lower boundary is negative for small n, so acceptance is impossible until −b + sn reaches 0. That gives the earliest possible decision in one line.",
   "Rejection first becomes possible when n(1 − s) ≥ a, since Sₙ cannot exceed n.",
   "For a quick ASN sanity check, E(N) is roughly (log A)/E₁[Z] under H₁ when β is small, since the log B term is then negligible."],
  "remember": [
   "Both error rates fixed, sample size random.",
   "A = (1 − β)/α, B = β/(1 − α).",
   "Slope from the hypotheses, intercepts from the error rates."]},
 "howto": "This is the last topic in Module 4 and the lightest in the syllabus, so read it for the shape rather than for depth. Sections 3 and 4 are the whole examinable core: the procedure, the two boundary constants, and the two lines they produce. Section 6 runs the test on an actual sequence, which is the quickest way to see that the method is simpler than its notation. Section 8 computes the average sample number and produces the one number that justifies the method — about half the observations of a fixed-sample test for the same error rates. If you are short of time, sections 3, 4 and 8 are sufficient. Attempt the question at the end of each section before opening the answer. The optional section explains why Wald's boundaries are approximations, which is where the α' + β' ≤ α + β inequality comes from.",
 "refs": [
  {"title": "Sequential Analysis", "where": "Chapters 3 and 7", "site": "Abraham Wald",
   "url": "", "type": "Textbook", "free": False, "checked": "2026-11-03",
   "why": "The original monograph, which defines the test, derives the boundaries and proves termination. Still the clearest source on where A and B come from."},
  {"title": "Testing Statistical Hypotheses, 3rd edition", "where": "Chapter 3 and its sequential sections",
   "site": "Lehmann and Romano", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "Places the SPRT beside the Neyman–Pearson lemma and states the Wald–Wolfowitz optimality result precisely."},
  {"title": "Statistical Inference", "where": "Weeks on testing of hypotheses",
   "site": "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee",
   "url": "https://archive.nptel.ac.in/noc/courses/noc21/SEM1/noc21-ma23", "type": "Video course",
   "free": True, "checked": "2026-11-03",
   "why": "Indian syllabus treatment of the SPRT, OC function and ASN, in the notation NET questions use."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 9",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-11-03",
   "why": "The Bernoulli SPRT worked with the boundary lines and the ASN, at exactly the level this lesson uses."},
  {"title": "Mathematical Statistics 18.655 — lecture notes",
   "where": "Sessions on testing", "site": "MIT OpenCourseWare",
   "url": "https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type": "Lecture notes", "free": True, "checked": "2026-11-03",
   "why": "Background on the likelihood ratio as the common object behind the fixed-sample and sequential tests."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored November 2026 for this platform against the UGC NET Statistics syllabus. The PYQ evidence for this topic is nil and that is stated plainly: the June 2026 paper contains no question on sequential testing, and no practice variant in the bank mentions the SPRT, Wald's boundaries, the OC function or the average sample number. It is the only one of the seven lessons built in this run with no previous-year anchor. It was built because the syllabus lists it and the catalog assigns it 0.46 expected questions per paper, 0.9 marks — the lowest weight in the module, which is why it was scheduled last — and because it completes Module 4 at 17 of 17 topics. It is also the first lesson to use the `sprt` visualisation, which had been built and tested but never used. Every numerical value was computed rather than recalled: A = 18 and B = 0.10526 with logarithms 2.890372 and −2.251292; the per-observation steps 0.693147 and −0.559616 and their difference k = 1.252763 = log 3.5; the slope 0.44671 and intercepts 2.3072 and −1.7971; the stopping point n = 6 for the sequence 1, 1, 0, 1, 1, 1 with the near-miss at n = 5 where S₅ = 4 against a boundary of 4.541; the earliest possible decision at n = 5 for either verdict; E₀[Z] = −0.183787 and E₁[Z] = 0.192042 giving average sample numbers 10.85 and 12.37; and the fixed-sample comparison of 21.22 rounding to 22, a saving of about 51% under H₀. Previous-year questions themselves are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "inf-t11-m-%02d" % i, "format": fmt, "topic": "inference-t11",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "In a sequential probability ratio test, what is fixed in advance?",
 ["the sample size only", "both the Type I and Type II error probabilities",
  "the Type I error probability only", "the power at a single alternative"],
 "B",
 "The SPRT fixes both α and β and leaves the sample size random. A fixed-sample test can fix one error rate and let the other follow from n; because the sample size here is free, there is room to pin down both."))

I.append(q(2, "single", "easy",
 "In an SPRT the sample size is:",
 ["fixed before sampling begins", "a random variable",
  "always equal to the fixed-sample size for the same α", "chosen after the data are seen"],
 "B",
 "Sampling continues until the likelihood ratio leaves the corridor between B and A, so the number of observations is random. Wald proved the test terminates with probability 1 and that the expected sample size is finite, but no bound is fixed in advance — which is why real plans add a truncation rule."))

I.append(q(3, "single", "easy",
 "The SPRT continues sampling as long as:",
 ["Λₙ ≥ A", "B < Λₙ < A", "Λₙ ≤ B", "Λₙ = 1"],
 "B",
 "Strictly between the two boundaries no decision is made and another observation is taken. Reaching or passing the upper boundary stops the test with H₀ rejected; reaching or passing the lower one stops it with H₀ accepted."))

I.append(q(4, "numeric", "easy",
 "For an SPRT with α = 0.05 and β = 0.10, Wald's boundary constants are:",
 ["A = 18, B = 0.1053", "A = 0.1053, B = 18", "A = 19, B = 0.1000", "A = 18, B = 0.0500"],
 "A",
 "A = (1 − β)/α = 0.90/0.05 = 18 and B = β/(1 − α) = 0.10/0.95 = 0.10526. Note that A exceeds 1 and B is below 1; the second option has them the wrong way round, and the third divides by α rather than using 1 − β on top.",
 check="A must be greater than 1 and B less than 1 whenever α and β are below a half. Both error rates appear in both constants."))

I.append(q(5, "single", "easy",
 "The SPRT is designed for testing:",
 ["a simple null against a simple alternative",
  "a composite null against a composite alternative",
  "a simple null against a one-sided composite alternative",
  "goodness of fit of a whole distribution"],
 "A",
 "The likelihood ratio requires both hypotheses to be completely specified, so the SPRT in this form tests one specified value against another — the same restriction as the Neyman–Pearson lemma. A composite problem must be reduced to two representative values first."))

I.append(q(6, "single", "easy",
 "The operating characteristic function L(θ) of an SPRT gives:",
 ["the probability of eventually accepting H₀ when θ is true",
  "the expected number of observations when θ is true",
  "the probability of rejecting H₀ when θ is true",
  "the probability that the test never terminates"],
 "A",
 "L(θ) is the sequential analogue of the power function read the other way up, and two of its values are fixed by construction: L(θ₀) = 1 − α and L(θ₁) = β. The expected number of observations is the average sample number, a different function."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "An SPRT has α = 0.02 and β = 0.05. The value of A is:",
 ["47.5", "19.0", "48.5", "20.0"],
 "A",
 "A = (1 − β)/α = 0.95/0.02 = 47.5. The second option computes 1/α approximately, ignoring the numerator 1 − β, and the third adds rather than using the correct numerator.",
 check="A = (1 − β)/α. A smaller α pushes A higher, since more evidence is being demanded before a true H₀ is rejected."))

I.append(q(8, "numeric", "moderate",
 "For a Bernoulli SPRT of H₀: p = 0.3 against H₁: p = 0.6, the common slope of the two boundary lines in the (n, Sₙ) plane is:",
 ["0.447", "0.300", "0.600", "0.450"],
 "A",
 "s = log((1 − p₀)/(1 − p₁))/log(p₁(1 − p₀)/(p₀(1 − p₁))) = log(1.75)/log(3.5) = 0.559616/1.252763 = 0.44671. The slope depends only on the two hypotheses, never on α or β, and it must lie between p₀ and p₁ — which 0.447 does.",
 check="The slope must lie strictly between p₀ and p₁. A value equal to either hypothesis means the formula was not applied."))

I.append(q(9, "single", "moderate",
 "In the boundary lines Sₙ = a + sn and Sₙ = −b + sn, the quantities a and b depend on:",
 ["the two hypotheses only", "the two error rates only",
  "the sample size", "neither the hypotheses nor the error rates"],
 "B",
 "The intercepts are a = log A/k and b = −log B/k, and A and B are built from α and β alone — the k in the denominator is common to the slope too. So changing α shifts one line without tilting it, while changing a hypothesis tilts both. That separation is the structural fact this topic tests."))

I.append(q(10, "numeric", "moderate",
 "For the test with boundaries 'reject H₀ if Sₙ ≥ 2.3072 + 0.44671n' and 'accept H₀ if Sₙ ≤ −1.7971 + 0.44671n', the earliest observation at which any decision is possible is:",
 ["n = 1", "n = 3", "n = 5", "n = 8"],
 "C",
 "Rejection needs Sₙ ≥ 2.3072 + 0.44671n with Sₙ at most n, so n(1 − 0.44671) ≥ 2.3072 and n ≥ 4.17, giving n = 5 with all five successes. Acceptance needs −1.7971 + 0.44671n ≥ 0, so n ≥ 4.02, again n = 5 with no successes. Before that the lower boundary is negative and the upper one above n.",
 check="A count of successes lies between 0 and n. A decision is impossible while the upper boundary exceeds n and the lower one is below 0."))

I.append(q(11, "numeric", "moderate",
 "Using those boundaries, the sequence of results 1, 1, 0, 1, 1, 1 (where 1 is a success) causes the test to:",
 ["reject H₀ at n = 6", "accept H₀ at n = 6", "reject H₀ at n = 5", "still be continuing at n = 6"],
 "A",
 "The running totals are 1, 2, 2, 3, 4, 5. At n = 5 the rejection boundary is 4.541 and S₅ = 4, just short, so the test continues. At n = 6 the boundary is 4.987 and S₆ = 5, so the test stops and rejects H₀. Six observations against the 22 a fixed-sample test would need.",
 check="Evaluate both boundaries at each n and compare with the running total. The near-miss at n = 5 is the step the question is built on."))

I.append(q(12, "multi", "moderate",
 "Consider the properties of the sequential probability ratio test.",
 ["A and C only", "A, B and C only", "B and D only", "A and D only"],
 "A",
 "A is true and is the method's defining feature. B is false — the ASN is largest for a parameter between the hypotheses, where the evidence per observation is weakest. C is true, from Wald's termination theorem. D is false: the likelihood ratio needs both hypotheses specified.",
 statements=["Both error probabilities are fixed in advance and the sample size is random.",
             "The average sample number is largest under H₀.",
             "The test terminates with probability 1 and has finite expected sample size.",
             "The test applies directly to composite hypotheses on both sides."],
 verdicts=verd(
  (True, "True. This is what distinguishes the SPRT from every fixed-sample test in the module."),
  (False, "False. The ASN peaks at a parameter value between θ₀ and θ₁, where the walk wanders instead of drifting. Neither E(N|H₀) nor E(N|H₁) is the worst case."),
  (True, "True — Wald proved both, so the sample size is a genuine random variable with a finite mean rather than a risk of never stopping."),
  (False, "False. Both hypotheses must be simple, since the likelihood ratio has to be evaluated at two specified parameter values."))))

I.append(q(13, "numeric", "moderate",
 "For the Bernoulli SPRT with p₀ = 0.3 and p₁ = 0.6, the expected log-likelihood-ratio per observation under H₀ is:",
 ["−0.1838", "0.1920", "0.6931", "−0.5596"],
 "A",
 "E₀[Z] = p₀ log(p₁/p₀) + (1 − p₀) log((1 − p₁)/(1 − p₀)) = 0.3(0.693147) + 0.7(−0.559616) = −0.183787. The second option is the same expectation under H₁, and the last two are the individual step sizes rather than their expectation.",
 check="E₀[Z] must be NEGATIVE: under the null the accumulated ratio drifts downward, which is what makes the test eventually accept H₀."))

I.append(q(14, "numeric", "moderate",
 "For that test with α = 0.05 and β = 0.10, log A = 2.8904, log B = −2.2513 and E₀[Z] = −0.18379. The average sample number under H₀ is approximately:",
 ["10.85", "12.37", "22.00", "18.00"],
 "A",
 "E(N|H₀) ≈ [α log A + (1 − α) log B]/E₀[Z] = [0.05(2.8904) + 0.95(−2.2513)]/(−0.18379) = −1.9942/−0.18379 = 10.85. Option B is the ASN under H₁, option C is the fixed-sample size and option D is the constant A.",
 check="Two negatives divide to give a positive. An ASN that comes out negative means the sign of log B or of E₀[Z] was mishandled."))

I.append(q(15, "single", "moderate",
 "The principal practical advantage of an SPRT over a fixed-sample test with the same α and β is:",
 ["it is easier to compute", "it needs about half as many observations on average",
  "it gives exact error probabilities", "it requires no assumptions about the distribution"],
 "B",
 "For the standard example the ASN is 10.85 under H₀ and 12.37 under H₁ against a fixed-sample 22 — roughly half the data for identical error rates. It is not easier to compute, its error rates are approximate rather than exact, and it needs the distribution fully specified under both hypotheses."))

I.append(q(16, "single", "moderate",
 "In practice a sequential sampling plan is usually truncated at some maximum sample size. The consequence is that:",
 ["the plan becomes invalid", "the true error probabilities differ from the nominal α and β",
  "the average sample number rises substantially", "the boundaries become non-linear"],
 "B",
 "Wald's boundaries assume the test may continue as long as needed, so forcing a decision at a maximum n means some paths are decided on weaker evidence than the boundaries demanded, and the realised α and β shift. The ASN barely changes, since paths reaching the truncation point are rare. The honest practice is to recompute the real error rates by simulation."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the exactness of Wald's boundary constants and the error probabilities they deliver.",
 ["A, B and D only", "A and C only", "B and C only", "A, B and C only"],
 "A",
 "A is true — the argument over the rejecting paths gives 1 − β ≥ Aα, an inequality. B is true, and it names the reason the inequality is not an equality. C is false: the correct bounds are α' ≤ α/(1 − β) and β' ≤ β/(1 − α), and the total inequality runs α' + β' ≤ α + β, so the total error cannot exceed the nominal total. D is true and follows from those bounds.",
 statements=["The exact relation between A, α and β is an inequality, A ≤ (1 − β)/α.",
             "Taking that inequality as an equality ignores the overshoot past the boundary.",
             "The realised error rates can jointly exceed the nominal ones, so α' + β' > α + β is possible.",
             "For α = 0.05 and β = 0.10 the bound on the realised Type I error is about 0.056."],
 verdicts=verd(
  (True, "True. On every rejecting path Λ ≥ A, so P₁ ≥ A P₀ over that set, giving 1 − β ≥ Aα."),
  (True, "True. The walk takes a discrete step and lands at or beyond the boundary rather than exactly on it; that excess is the overshoot, and it is the whole source of the approximation."),
  (False, "False. The bounds give α' + β' ≤ α + β — the total is never worse than advertised, though the split between the two may shift."),
  (True, "True: α/(1 − β) = 0.05/0.90 = 0.0556, close enough to 0.05 that the nominal value is what gets reported."))))

I.append(q(18, "numeric", "hard",
 "For the Bernoulli SPRT with p₀ = 0.3, p₁ = 0.6, α = 0.05, β = 0.10, where E₁[Z] = 0.19204, the average sample number under H₁ is approximately:",
 ["10.85", "12.37", "15.05", "11.61"],
 "B",
 "E(N|H₁) ≈ [(1 − β) log A + β log B]/E₁[Z] = [0.90(2.8904) + 0.10(−2.2513)]/0.19204 = 2.3762/0.19204 = 12.37. Option A is the ASN under H₀; note that the ASN is slightly larger under H₁ here, because the failure step is smaller in magnitude than the success step.",
 check="Under H₁ both the numerator and E₁[Z] are positive. The weights on log A and log B are 1 − β and β, not α and 1 − α."))

I.append(q(19, "single", "hard",
 "The Wald–Wolfowitz theorem states that among all tests with error probabilities at most α and β, the SPRT:",
 ["is the most powerful at every alternative",
  "minimises the expected sample size under both H₀ and H₁",
  "minimises the maximum possible sample size",
  "minimises the expected sample size at every parameter value"],
 "B",
 "The result is about expected sample size at the two hypotheses, and it is unusually strong in holding at both simultaneously. It says nothing about the maximum sample size, which is unbounded, and nothing about parameter values between the hypotheses — where the ASN is largest and the SPRT is not especially efficient."))

I.append(q(20, "single", "hard",
 "Which feature of a testing problem would make an SPRT inappropriate?",
 ["observations are expensive and arrive one at a time",
  "the response takes longer to measure than the interval between arriving items",
  "both hypotheses are completely specified",
  "the two error rates are both required to be small"],
 "B",
 "The method depends on assessing each observation before deciding whether to take the next, so a response measured more slowly than items arrive defeats it. The other three features are precisely the conditions the SPRT is designed for: costly observations arriving singly, two simple hypotheses, and both error rates specified in advance."))

# A pool whose keys pile onto one letter rewards a guesser, and the validator caps any
# letter at 40%. Swapping positions i and j is its own inverse, so an "option X" mention
# inside an explanation just swaps the same two letters.
LET = "ABCD"
WANT = {"inf-t11-m-01": "D", "inf-t11-m-03": "C", "inf-t11-m-04": "C",
        "inf-t11-m-05": "D", "inf-t11-m-06": "C", "inf-t11-m-07": "D",
        "inf-t11-m-08": "C", "inf-t11-m-10": "A", "inf-t11-m-13": "D",
        "inf-t11-m-14": "C", "inf-t11-m-17": "D", "inf-t11-m-19": "A"}

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
 "moduleId": "inference", "topicId": "inference-t11", "source": "mastery",
 "label": "The sequential probability ratio test — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
