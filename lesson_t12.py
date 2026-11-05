#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 4.12 — Size and power computation (topic inference-t12).

Built on PYQ evidence: the June 2026 paper put two of its eleven inference items
directly on this topic (Q49, the five-toss coin; Q39, the uniform density with the
critical region x >= 0.5), and both are worked here in full as the lesson's own
examples. Q43, the ordering of the steps of a test, is the pool's `order` item.

Writes seed/lesson_t12.json and seed/inference_t12_mastery.json.
Run: python3 lesson_t12.py
"""
import json, io, os

OUT = "seed/lesson_t12.json"
POOL = "seed/inference_t12_mastery.json"

# ---------------------------------------------------------------- scenes

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Get back the four small calculations every size-and-power question ends with, so the lesson can spend its time on the ideas instead.",
 "ask": {
  "q": "Of the four checks above, which one is about the rule the test uses rather than about a probability calculation?",
  "nudge": "Three of them ask you to work out a number. One asks you to say what the two mistakes are and which one you get to choose."},
 "body": [
  "This whole topic is two numbers. One says how often the test raises a false alarm. The other says how often it catches a real effect. Everything else is bookkeeping.",
  "But the bookkeeping is where marks go. Every answer ends in a probability — a binomial tail, a normal tail, or the area under a flat density — and the four options in a NET question usually differ only in which hypothesis that probability was computed under.",
  "So four checks first. Answer each one before you open it. If three of the four come back quickly you are ready; if none do, do the probability refresher first, because the ideas here are easy and the arithmetic is not."],
 "items": [
  {"ask": "A fair coin is tossed 5 times. What is the probability of getting 4 or more heads?",
   "recall": "P(X ≥ 4) = [C(5,4) + C(5,5)] / 2^5 = (5 + 1)/32 = 6/32 = 0.1875.",
   "refresh": [
    "There are 2^5 = 32 equally likely sequences of five tosses. Exactly C(5,4) = 5 of them have four heads, and C(5,5) = 1 has five. So 6 of the 32.",
    "Write it as a fraction and keep it as one — 6/32 = 3/16. Decimals invite rounding errors, and NET options are often two fractions that look alike.",
    "The phrase to watch is 'more than 3 heads'. That means 4 or 5, not 3 or more. One word moves the answer from 0.1875 to 0.5."]},
  {"ask": "For a standard normal Z, what value z has P(Z > z) = 0.05? And what is P(Z > 1.96)?",
   "recall": "z = 1.645, and P(Z > 1.96) = 0.025.",
   "refresh": [
    "These two numbers do most of the work in this topic. 1.645 cuts off 5% in one tail; 1.96 cuts off 2.5% in one tail, so it cuts 5% across both tails together.",
    "That is the whole difference between a one-sided and a two-sided test at the same 5% level: the one-sided test spends all 5% on one side, the two-sided test splits it.",
    "Learn the pair 1.645 and 1.96, and also 1.282, which cuts off 10% in one tail and turns up whenever a question asks for 90% power."]},
  {"ask": "X is spread evenly over the interval from 0 to 2, so its density is 1/2 there. What is P(X ≥ 0.5)?",
   "recall": "The density is flat, so probability is just length: P(X ≥ 0.5) = (2 − 0.5)/2 = 1.5/2 = 0.75.",
   "refresh": [
    "An evenly spread — uniform — density is a rectangle of height 1/θ over the interval 0 to θ. Its total area is 1, as every density's must be.",
    "So any probability is the width of the piece you want divided by the full width. No integration needed once you see it as a rectangle.",
    "This single idea answers a whole family of NET questions, including one in the June 2026 paper, which you will work in scene 7."]},
  {"ask": "Name the two ways a test can be wrong, and say which one the significance level controls.",
   "recall": "Type I error: rejecting H₀ when it is true. Type II error: failing to reject H₀ when it is false. The significance level α controls the Type I error only.",
   "refresh": [
    "The two errors are not symmetric in the way the test is built. You choose α first, fixing how often you will raise a false alarm, and then the Type II error is whatever it turns out to be.",
    "That asymmetry is a decision someone made, not a law of nature. It says a false alarm is the error you are willing to pin down and the missed effect is the one you will live with.",
    "The whole of this lesson is working out what that second error actually comes to, in numbers, for a test someone hands you."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Two mistakes, two different prices",
 "objective": "Feel the trade-off in a setting where both errors cost something real, before any symbols appear.",
 "body": [
  "A test is a rule for making up your mind with incomplete information. Any such rule gets things wrong sometimes, and it can get them wrong in two directions. Size and power are just the names for how often each direction happens.",
  "What makes the subject worth learning is that you cannot shrink both at once with the same data. Tighten the rule so false alarms are rare, and you will start missing real effects. Loosen it to catch everything real, and you will cry wolf. The only escape is more data.",
  "Hold that in mind through the scenario: the person setting the rule is choosing where to sit on that trade-off, and the two numbers in this lesson are the coordinates of the seat."],
 "scenario": {
  "teaser": "A dairy has four minutes to decide whether a milk tanker has been watered down.",
  "title": "The tanker at the gate",
  "body": [
   "A collection dairy receives tankers all morning. Watered milk has a lower freezing point than pure milk, so the lab takes a sample and reads the freezing point. Pure milk sits near −0.545 °C; adding water pulls the reading up toward zero.",
   "The rule in use is simple: if the reading is above a threshold, reject the tanker. H₀ is 'this tanker is pure'. Rejecting means sending it back.",
   "Now the two mistakes. Sending back a pure tanker costs the dairy a supplier relationship and a day's milk — a false alarm. Accepting a watered tanker costs them a diluted batch and, if a regulator samples it, a penalty — a missed detection.",
   "Notice that the dairy can set the threshold wherever it likes, and that is the only dial it has. Push the threshold up and almost no pure tanker is ever rejected, but watered tankers slip through. Pull it down and nothing slips through, but honest suppliers get turned away.",
   "The one thing that improves both at once is a better reading — two samples instead of one, a more precise instrument. In statistics that is exactly the role of sample size. It is the only way to buy your way out of the trade-off rather than just moving along it."],
  "q": "If the dairy lowers its threshold, which of the two mistakes becomes more common, and which becomes rarer?",
  "answer": "Lowering the threshold means rejecting more often. So false alarms — rejecting pure tankers — become more common, and missed detections become rarer. In the language of this lesson, the size goes up and so does the power. They move together, which is why you cannot improve one without paying in the other."},
 "ask": {
  "q": "Before reading on: why would anyone fix the false-alarm rate first, instead of just adding the two mistake rates together and making that total as small as possible?",
  "nudge": "Think about who bears each cost, and whether the two mistakes are the kind of thing you can add up in the same units at all."}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Watch the two error rates move",
 "objective": "See size and power as two areas under two curves, and find out by moving the controls what actually raises power.",
 "viz": {"type": "np-power", "n": 9, "d": 1.5, "alpha": 0.05, "sd": 4},
 "scenario": {
  "teaser": "A seed company has to decide how many plots to plant before it can claim its new variety yields more.",
  "title": "How many plots?",
  "body": [
   "A seed company has a new paddy variety it believes yields more than the standard one. It will plant both on matched plots and compare mean yields. H₀ is 'no improvement'.",
   "The agronomist asks a question the statistician cannot dodge: how many plots? Too few, and a real improvement of two quintals a hectare will fail to show up — the trial will end inconclusive and the season is gone. Too many, and the trial costs more than the information is worth.",
   "This is the power calculation and nothing else. Fix α at 0.05 because a false claim of improvement is the error the regulator cares about. Decide the smallest improvement worth detecting — that is an agronomic judgement, not a statistical one. Decide what chance of detecting it you will accept, usually 0.80 or 0.90. Those three numbers and the plot-to-plot variation determine n, and there is only one answer.",
   "What makes this worth seeing before the algebra is the direction of the reasoning. In the exam you are given n and asked for the power. In practice you are given the power you need and asked for n. Scene 9 does it that way round, and it is the harder of the two."],
  "q": "Which of the three numbers the agronomist has to supply is not a statistical question at all?",
  "answer": "The smallest improvement worth detecting. No amount of statistics can tell you whether two quintals a hectare matters to a farmer — that is agronomy and economics. The statistician's job starts once that number is fixed, and a power calculation presented without it is hiding the one judgement that mattered."},
 "body": [
  "Two bell curves. The left one is how the sample mean behaves if H₀ is true. The right one is how it behaves if the true value is higher by the gap shown. The vertical line is the cut-off: readings to its right mean reject.",
  "The red area is the size. It is the part of the left-hand curve that falls past the cut-off — exactly how often you reject when H₀ was true all along.",
  "The shaded part of the right-hand curve to the LEFT of the line is the Type II error. What is left of that curve — everything past the line — is the power.",
  "Three things to try, in this order, because each one teaches a different lesson.",
  "First slide the cut-off by changing α. Both areas change, and they change the same way: more α, more power. That is the trade-off, and it buys you nothing you did not pay for.",
  "Now widen the gap between the two curves. Power climbs and the size does not budge. A real effect that is large is easy to detect; the false-alarm rate has nothing to do with how big the truth is.",
  "Finally raise n. Both curves narrow, they pull apart relative to their own width, and power climbs with the size still pinned at 0.05. That is the only control that gives you something for nothing — and it is why 'how large a sample do I need' is a question with an actual answer."],
 "ask": {
  "q": "With α fixed, is there any gap size at which the power drops below α? What is the smallest power this test can have?",
  "nudge": "Set the gap to zero and read the power off the chart. What is the right-hand curve then?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The two definitions, and the notation trap inside them",
 "objective": "Write down size, power and the power function precisely, and settle the symbol clash that costs people marks.",
 "blocks": [
  {"t": "def", "h": "Size",
   "body": "The size of a test is the probability that it rejects H₀ when H₀ is in fact true. Write it α = P(reject H₀ | H₀ true). You choose it in advance — 0.05, 0.01 — and everything else about the test is then built to respect that choice."},
  {"t": "def", "h": "Power",
   "body": "The power of a test at a particular parameter value θ is the probability that it rejects H₀ when that θ is the truth. Read as a function of θ it is called the power function, and this lesson writes it π(θ). The Type II error probability at θ is β(θ) = 1 − π(θ), the chance of failing to reject when you should have."},
  {"t": "step", "h": "The notation clash, and how to survive it",
   "body": "Books disagree about β, and the disagreement is a genuine mark-loser. Many Indian textbooks use β for the Type II error probability, so that power = 1 − β. Others, Casella and Berger among them, use β(θ) for the power function itself, so that power = β(θ). Both are standard and both appear in question papers. The safe habit: never write β alone in an answer. Write 'power' or 'Type II error' in words, or define your symbol in the first line. In a multiple-choice paper, read the stem for which convention it is using before you match an option — if an option says power = 1 − β and another says power = β(θ), the stem's own wording decides which is being tested."},
  {"t": "formula", "h": "The two numbers side by side",
   "body": "For a test with rejection region W, the size is α = P(X ∈ W | θ₀) and the power at θ is π(θ) = P(X ∈ W | θ). They are the same probability of the same event, computed under two different parameter values. That is the only difference between them, and it is the single most common place to go wrong: computing the size under the alternative, or the power under the null."},
  {"t": "def", "h": "Level versus size",
   "body": "A test has level α₀ if its size is at most α₀. So the size is the exact rejection probability under the null, while the level is any upper bound you are willing to quote. Every size-0.03 test is also a level-0.05 test. The distinction matters for discrete data, where an exact size of 0.05 may be unreachable and the honest statement is 'level 0.05, size 0.0480'."},
  {"t": "step", "h": "The order of work, which never changes",
   "body": "1. Read off the rejection region. It is given to you in this kind of question; you are not being asked to find it.\n2. For the size, compute the probability of that region using the null value of the parameter.\n3. For the power, compute the probability of the same region using the alternative value.\n4. Check the direction: a sensible test has power above its size. If your power comes out below α, you have almost certainly swapped the two hypotheses."}],
 "flow": {
  "title": "From a stated test to its two numbers",
  "alt": "Flow chart: from a rejection region to the size and the power",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "A test is handed to you: a rejection region W", "kind": "start"},
   {"id": "b", "r": 1, "c": 0, "label": "Put the NULL value in the distribution", "kind": "step"},
   {"id": "c", "r": 1, "c": 2, "label": "Put the ALTERNATIVE value in the distribution", "kind": "step"},
   {"id": "d", "r": 2, "c": 0, "label": "P(W) = size α", "kind": "end"},
   {"id": "e", "r": 2, "c": 2, "label": "P(W) = power π(θ₁)", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b", "label": "for the size"},
   {"from": "a", "to": "c", "label": "for the power"},
   {"from": "b", "to": "d"}, {"from": "c", "to": "e"}],
  "note": "One region, two parameter values. Every size-and-power question in a NET paper is this diagram with numbers in it."},
 "ask": {
  "q": "Why must a reasonable test have power at least as large as its size? Can you describe a test where the power is lower?",
  "nudge": "Consider a test that ignores the data completely and rejects with probability 0.05 no matter what. What are its size and its power?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — the five-toss coin (June 2026, Q49)",
 "objective": "Run the whole calculation on a discrete example, and get two numbers you can check against the official key.",
 "ask": {
  "q": "The size here came out as 0.1875, nothing like a conventional 0.05. Does that make the test wrong?",
  "nudge": "Ask who chose the rejection region in this question. Was the size chosen, or is it a consequence of a rule you were handed?"},
 "problem": "Let p be the probability that a coin falls heads in a single toss. To test H₀: p = 1/2 against H₁: p = 3/4 the coin is tossed 5 times, and H₀ is rejected if more than 3 heads are obtained. Find the size and the power of the test.",
 "steps": [
  {"say": "Name the statistic and write the rejection region as an inequality.",
   "math": "X = number of heads in 5 tosses,  X ~ Binomial(5, p)\nreject H₀ when X > 3,  that is  W = {X = 4} ∪ {X = 5}",
   "why": "'More than 3' is 4 or 5. This is the step that decides the whole answer, and it is where the examiner expects a share of candidates to read 'at least 3' and compute 0.5 instead. Write the region out as a set of values before computing anything."},
  {"say": "Size: take that same region under the NULL value p = 1/2.",
   "math": "α = P(X ≥ 4 | p = 1/2)\n  = C(5,4)(1/2)^4(1/2) + C(5,5)(1/2)^5\n  = 5/32 + 1/32 = 6/32 = 3/16 = 0.1875",
   "why": "Under p = 1/2 all 32 sequences are equally likely, so this is just a count: 5 sequences with four heads, 1 with five. Note that 0.1875 is nothing like a conventional 0.05 — the question handed you a rule, and the rule's size is whatever it is. You are not allowed to adjust it to look respectable."},
  {"say": "Power: the same region, now under the ALTERNATIVE value p = 3/4.",
   "math": "π(3/4) = P(X ≥ 4 | p = 3/4)\n  = C(5,4)(3/4)^4(1/4) + (3/4)^5\n  = 5(81/256)(1/4) + 243/1024\n  = 405/1024 + 243/1024 = 648/1024",
   "why": "Identical event, different p. Keeping everything over 1024 makes the addition exact and avoids the rounding that separates two of the four options."},
  {"say": "Reduce and sanity-check.",
   "math": "π(3/4) = 648/1024 = 81/128 = 0.6328\nsize = 0.1875,  power = 0.6328",
   "why": "Power well above size, which is the direction a sensible test must go. So: size 0.1875, power 0.6328. That matches the official key for Q49 — option B."}],
 "after": "Look at what the alternative did. It never touched the rejection region, which was fixed by the question, and it never touched the size. It entered only in the last calculation. Hold on to that: in this kind of question the region comes first, the null gives the size, the alternative gives the power, and the three never mix."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the definitions before going on — this is where the retention actually comes from.",
 "intro": "Answer each one in your head, out loud if you can, before you reveal it. Getting it wrong and then being corrected is worth more than reading the right answer twice.",
 "items": [
  {"q": "Define the size of a test.",
   "a": "The probability that the test rejects H₀, computed under the assumption that H₀ is true. α = P(reject | H₀)."},
  {"q": "Which hypothesis is the power computed under?",
   "a": "The alternative, or more precisely whichever parameter value you are asked about. The power is a function of θ, and its value at θ₀ is the size."},
  {"q": "A test rejects when more than 3 of 5 tosses are heads. Which values of X reject?",
   "a": "X = 4 and X = 5 only. 'More than 3' excludes 3."},
  {"q": "What is the difference between the level and the size of a test?",
   "a": "The size is the exact rejection probability under the null. The level is an upper bound on it. A size-0.0480 test can honestly be called a level-0.05 test."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — the flat density (June 2026, Q39)",
 "objective": "Do the same calculation where the distribution is continuous and the probability is an area, with the scaffolding thinned out.",
 "problem": "Given the density f(x; θ) = 1/θ for 0 ≤ x ≤ θ and 0 otherwise. For testing H₀: θ = 1 against H₁: θ = 2 based on a single observed value of x, the critical region is w = {x : x ≥ 0.5}. Find the power of the test, and its size.",
 "steps": [
  {"say": "Start by picturing the density under each hypothesis. Both are rectangles of total area 1 — a tall narrow one under H₀, a short wide one under H₁.",
   "blank": {"prompt": "Under H₁ (θ = 2), what are the height and the width of the rectangle?",
             "answer": "height 1/2, width 2",
             "accept": ["1/2 and 2", "height 0.5 width 2", "0.5, 2", "h = 1/2, w = 2",
                        "height = 1/2 over 0 to 2"],
             "hint": "The density is 1/θ over the interval 0 to θ. Put θ = 2 in both places."},
   "why": "Total area must be 1, and height times width = (1/2)(2) = 1 confirms it. Once you see the density as a rectangle, every probability in this question is a width times a height and there is nothing to integrate."},
  {"say": "Now the power. It is the probability of the stated region, computed under the alternative.",
   "blank": {"prompt": "Compute P(X ≥ 0.5 | θ = 2).",
             "answer": "0.75",
             "accept": ["3/4", "0.75", ".75", "1.5/2", "75%"],
             "hint": "The slice runs from 0.5 to 2, so its width is 1.5. Multiply by the height 1/2."},
   "why": "Width 1.5 times height 1/2 is 0.75. That is the official answer to June 2026 Q39, and the whole question was this one line."},
  {"say": "The question asked only for the power, but compute the size as well — it is the habit that stops the two getting swapped.",
   "blank": {"prompt": "Compute the size, P(X ≥ 0.5 | θ = 1).",
             "answer": "0.5",
             "accept": ["1/2", "0.5", ".5", "0.50", "50%"],
             "hint": "Under θ = 1 the rectangle only reaches to 1, so the slice is narrower — and the height is now 1."},
   "why": "Width 0.5 times height 1 is 0.5. A size of 0.5 is enormous, and once again that is simply what the rule in the question delivers; you were not asked to improve it."},
  {"say": "Finally, check the pair for sense before you commit to an option.",
   "blank": {"prompt": "Which of the two numbers is larger, and which is it that Q39 asked for?",
             "answer": "the power, 0.75, is larger, and it is what was asked for",
             "accept": ["power is larger, answer 0.75", "0.75, the power",
                        "power 0.75 is bigger and is the answer", "the power"],
             "hint": "A sensible test rejects a false null more often than a true one."},
   "why": "Power above size is the direction every valid test must go. If you had got 0.5 for the power you would have computed it under the null — the commonest error on this question, and exactly why 0.5 sits among the four options."}],
 "after": "Both of the last two scenes were real NET questions, and in both the whole task was: read the region, compute one probability twice. Nothing about best tests, nothing about likelihood ratios. Recognising that this is all that is wanted is worth two marks in about ninety seconds, and candidates lose them by reaching for theory the question never asked for."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "When the null is a range, not a point",
 "objective": "Handle a null hypothesis that covers many parameter values, and see why its size is read off the boundary.",
 "blocks": [
  {"t": "def", "h": "A composite null",
   "body": "H₀: θ = θ₀ names one value and is called simple. H₀: θ ≤ θ₀ names a whole range and is called composite. With a range there is no single 'probability of rejecting when H₀ is true', because H₀ being true could mean any of those values, each giving a different rejection probability."},
  {"t": "formula", "h": "Size of a test with a composite null",
   "body": "The size is defined as the worst case over the null range: α = sup over θ in Θ₀ of π(θ). You promise that the false-alarm rate never exceeds α, whichever null value happens to hold."},
  {"t": "step", "h": "Why the worst case sits at the boundary",
   "body": "For the usual one-sided problems the power function increases in θ. Over the range θ ≤ θ₀ an increasing function is largest at the right-hand end, so the supremum is attained at θ = θ₀ itself. That is why, in practice, you compute the size of a composite-null test exactly as if the null were the single value at the boundary. It is a conclusion, not a definition — it depends on the power function being monotone, which it is for one-sided tests in the families NET uses."},
  {"t": "def", "h": "An unbiased test",
   "body": "A test is called unbiased if its power at every alternative is at least its size: π(θ) ≥ α for all θ in Θ₁. In words, it is never worse than guessing. Any test that fails this is detecting the effect backwards, and the word 'unbiased' here has nothing to do with unbiased estimation — it is an unrelated use of the same word."},
  {"t": "step", "h": "What this changes in practice, and what it does not",
   "body": "Almost nothing changes in the arithmetic: you still compute one probability under one parameter value. What changes is which value, and the answer is the boundary. The marks are lost by candidates who see H₀: μ ≤ 100 and then compute the size at some interior value like 95, where the rejection probability is smaller, and conclude the test is more conservative than it is."}],
 "ask": {
  "q": "For a one-sided test of H₀: μ ≤ 100 that rejects for large x̄, is the size computed at μ = 100 or at μ = 95? Why does it matter which?",
  "nudge": "Which value of μ makes rejection most likely, among all the values the null allows?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "Without the steps — how big a sample do you need?",
 "objective": "Run the calculation backwards: fix the power you want and solve for n. This is the form NET asks when it wants to separate candidates.",
 "problem": "X₁,…,Xₙ are iid N(μ, σ²) with σ² = 25 known. Test H₀: μ = 100 against H₁: μ > 100 at level α = 0.05. How large must n be for the power at μ = 102 to be at least 0.90? You may use that the upper 5% point of the standard normal is 1.645 and the upper 10% point is 1.282.",
 "hints": [
  "Direction — write the rejection region first, in terms of x̄, with n left as a symbol. It is x̄ > 100 + 1.645 σ/√n, because the size condition is fixed under the null and the alternative is on the high side.",
  "Second step — compute the power at μ = 102 by standardising the SAME region under μ = 102, not under 100. You should reach a probability of the form P(Z > something involving √n).",
  "Last step — the power is at least 0.90 when that standardised cut-off is at most −1.282, since P(Z > −1.282) = 0.90. Set up the inequality and solve for √n, then round n UP, because a fractional sample size buys you less power than you asked for."],
 "answer": "n ≥ 54.",
 "check": "Three things an examiner looks for here. The critical value contains μ₀ = 100 and never 102 — the alternative fixes the direction and the power, never the cut-off. The rounding goes UP: 53.54 rounds to 54, because 53 would leave the power just under 0.90, and rounding to the nearest integer is the error the options are built to catch. And the two normal points enter with opposite signs, 1.645 from the size condition and −1.282 from the power condition, so the gap that n has to cover is their sum 2.927 and not their difference.",
 "solution": [
  {"say": "Write the rejection region from the size condition, keeping n symbolic.",
   "math": "reject when  x̄ > 100 + 1.645 σ/√n\nwith σ = 5:  x̄ > 100 + 8.225/√n",
   "why": "The size is fixed under the null, so this step uses μ = 100 and nothing else. Leaving n as a symbol is the point of the exercise."},
  {"say": "Compute the power of that region at μ = 102.",
   "math": "π(102) = P(x̄ > 100 + 8.225/√n | μ = 102)\n  = P(Z > (100 + 8.225/√n − 102)/(5/√n))\n  = P(Z > 1.645 − 2√n/5)",
   "why": "Standardise using the alternative mean 102 and the same standard error 5/√n. The two terms in the numerator rearrange so that n appears once, which is what makes the inequality solvable."},
  {"say": "Impose the power requirement and solve.",
   "math": "P(Z > 1.645 − 2√n/5) ≥ 0.90\n⟺ 1.645 − 2√n/5 ≤ −1.282\n⟺ 2√n/5 ≥ 2.927\n⟺ √n ≥ 7.3175",
   "why": "P(Z > z) ≥ 0.90 exactly when z ≤ −1.282. The step that trips people is the inequality flipping direction when you move the −2√n/5 across, so check the sign by substituting one number at the end."},
  {"say": "Round up and verify.",
   "math": "n ≥ 53.54,  so  n = 54\ncheck: 2√54/5 = 2.939,  1.645 − 2.939 = −1.294\nP(Z > −1.294) = 0.902 ≥ 0.90 ✓",
   "why": "n must be a whole number and the requirement is a floor, so round up. The verification line is worth doing in the exam too: with n = 53 you would get 0.897, just short, which is exactly the trap."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — your verdict on each before you look",
 "objective": "Practise the statement-by-statement discipline the real multi-statement questions demand.",
 "intro": "Decide true or false on every statement before revealing any of them. In a NET paper these six would be one question marked all or nothing, so a statement you skipped is a mark you gambled.",
 "items": [
  {"claim": "The power of a test is computed under the null hypothesis.",
   "tf": False,
   "why": "False, and this is the single most common error in the topic. The power is computed under the alternative — or more generally at whatever parameter value is named. Only the size uses the null."},
  {"claim": "The power function evaluated at the null value equals the size of the test.",
   "tf": True,
   "why": "True, straight from the definitions: π(θ₀) = P(reject | θ₀) = α. It is a useful check on any power function you derive — plug in θ₀ and you must get α back."},
  {"claim": "Increasing the sample size raises the power while leaving the size unchanged.",
   "tf": True,
   "why": "True, and it is the only control with that property. Raising α also raises power, but it raises the false-alarm rate by exactly as much, so nothing is gained."},
  {"claim": "For a fixed sample size and fixed α, a two-sided test has higher power against a one-sided alternative than the corresponding one-sided test.",
   "tf": False,
   "why": "False. The two-sided test splits its α between two tails, so its cut-off on the relevant side is further out — 1.96 instead of 1.645 — and its power against an alternative on that side is lower. You pay for the ability to detect departures in either direction."},
  {"claim": "A test whose size is 0.0480 can correctly be described as a level-0.05 test.",
   "tf": True,
   "why": "True. The level is an upper bound on the size, so any test with size below 0.05 is a level-0.05 test. This is the honest way to describe discrete tests, where an exact 0.05 is often unattainable."},
  {"claim": "If the power of a test at some alternative is below its size, the test is simply weak but still valid.",
   "tf": False,
   "why": "False — such a test is called biased, and it is worse than useless at that alternative: it rejects a false null less often than it rejects a true one. In practice finding this means the rejection region points the wrong way."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 7,
 "title": "On your own — power of a two-sided test, where there are two tails to count",
 "objective": "Handle a rejection region with two pieces, and work out which piece you may ignore and which you may not.",
 "problem": "X₁,…,X₁₆ are iid N(μ, 16), so σ = 4. Test H₀: μ = 10 against H₁: μ ≠ 10 at α = 0.05. Find the power of the test at μ = 12. Then compare it with the power of the one-sided test of H₀: μ = 10 against μ > 10 at the same α.",
 "hints": [
  "Direction — a two-sided alternative splits α across both tails, so the multiplier is 1.96 and not 1.645. Write the region as two separate inequalities on x̄ before computing anything.",
  "Second step — the standard error is σ/√n = 4/4 = 1, which keeps the arithmetic out of the way. Standardise each piece of the region under μ = 12, not under 10.",
  "Last step — add the two probabilities, because the two pieces cannot both occur. Do not discard the far tail before you have looked at how big it is."],
 "answer": "Power ≈ 0.5160 for the two-sided test; 0.6387 for the one-sided test.",
 "check": "Three things an examiner is looking for. The multiplier is 1.96, because a two-sided test at 0.05 spends 0.025 in each tail — using 1.645 gives a test of size 0.10 and is the commonest error here. Both pieces of the region are evaluated under μ = 12, and the answer is their sum. And the far tail, P(Z < −3.96) = 0.00004, is negligible but not zero: if a question asks whether the two-sided power equals the single-tail probability, the answer is no.",
 "solution": [
  {"say": "Write the two-piece rejection region.",
   "math": "σ/√n = 4/√16 = 4/4 = 1\nreject when |x̄ − 10| > 1.96 × 1\nthat is  x̄ > 11.96  or  x̄ < 8.04",
   "why": "A two-sided alternative splits α across both tails, 0.025 each, so the multiplier is 1.96 and not 1.645. The standard error being exactly 1 here is deliberate, to keep the arithmetic out of the way of the idea."},
  {"say": "Compute the probability of each piece under μ = 12.",
   "math": "P(x̄ > 11.96 | μ = 12) = P(Z > (11.96 − 12)/1) = P(Z > −0.04) = 0.5160\nP(x̄ < 8.04 | μ = 12) = P(Z < (8.04 − 12)/1) = P(Z < −3.96) = 0.00004",
   "why": "Both pieces are evaluated under the alternative, because the whole region is what the power measures. Standardise each piece separately using μ = 12."},
  {"say": "Add them, because the two pieces cannot both happen.",
   "math": "π(12) = 0.5160 + 0.00004 = 0.5160  (to four places)",
   "why": "The far tail is negligible but it is not zero, and the examiner may well ask you to say so. In a question that wants three decimal places you may drop it; in a question that asks whether the power is exactly the one-tail probability, the answer is no."},
  {"say": "Compare with the one-sided test on the same data.",
   "math": "one-sided at α = 0.05:  reject when x̄ > 10 + 1.645 = 11.645\nπ(12) = P(Z > −0.355) = 0.6387",
   "why": "0.639 against 0.516, from the same sample and the same α. That is the price of the two-sided alternative, and it makes concrete the statement you ruled on in the previous section. The general lesson: a two-sided test always has less power against a given one-sided departure, so when theory tells you the direction, using it buys real power — and when it does not, the two-sided test is what honesty costs."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 7,
 "title": "What actually moves power — the four levers, and the shape of the curve",
 "objective": "Collect the levers in one place and read a power function off its graph, which is how NET asks the conceptual version.",
 "blocks": [
  {"t": "step", "h": "The four levers",
   "body": "1. Sample size n. Up goes power, size untouched. The only free lunch.\n2. The significance level α. Up goes power, but the false-alarm rate goes up by the same choice. Not a gain, a trade.\n3. The size of the real effect, |θ₁ − θ₀|. Bigger effects are easier to detect. Not under your control.\n4. The spread σ. Smaller spread, more power — which is why careful measurement and good design buy power the same way extra data does."},
  {"t": "formula", "h": "Power of the one-sided normal test, in one line",
   "body": "For H₀: μ = μ₀ against μ > μ₀ with σ known, rejecting when x̄ > μ₀ + z_α σ/√n, the power at μ is\n    π(μ) = P(Z > z_α − (μ − μ₀)√n/σ).\nEverything in the four levers above is visible in that one expression: n and σ and the gap sit together in the term (μ − μ₀)√n/σ, and α sits in z_α."},
  {"t": "def", "h": "What the power curve looks like",
   "body": "For the one-sided normal test, π(μ) rises smoothly from near 0 for μ well below μ₀, passes through exactly α at μ = μ₀, and climbs toward 1 as μ grows. For the two-sided test it is a U turned upside down — a valley with its lowest point α at μ₀, rising to 1 in both directions. Recognising which of these two shapes a graph shows is enough to answer a whole class of question."},
  {"t": "step", "h": "Consistency, in the only sense NET asks about",
   "body": "A test is consistent if its power at every fixed alternative goes to 1 as n grows without limit. The normal one-sided test is consistent, and you can see it in the formula: the term (μ − μ₀)√n/σ grows without limit for any fixed μ > μ₀, so the argument of P(Z > ·) goes to −∞ and the probability goes to 1. Any test that fails this is throwing data away."},
  {"t": "step", "h": "The 'more data' answer, stated carefully",
   "body": "Power rises with √n, not n. Quadrupling the sample halves the gap you can detect at the same power. That square root is why sample-size answers come out larger than people expect, and why a question asking for a doubling of precision expects a factor of four in n."}],
 "ask": {
  "q": "A power curve passes through 0.05 at μ = 10 and rises to the right. What are the test's size, its null value, and the direction of its alternative?",
  "nudge": "The power function's value at the null parameter is always the size. The direction in which it rises tells you which alternative is being tested."}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the bits that are easy to lose",
 "objective": "Retrieve the four or five facts most likely to have faded by the time you sit the paper.",
 "intro": "Same discipline: answer first, reveal second.",
 "items": [
  {"q": "Which single control raises power without raising the false-alarm rate?",
   "a": "Sample size. Raising α also raises power, but at the cost of exactly the error rate you were trying to control."},
  {"q": "Power rises with n or with √n?",
   "a": "With √n. The detectable gap shrinks like 1/√n, so quadrupling n halves it."},
  {"q": "For a composite null H₀: θ ≤ θ₀, where is the size computed?",
   "a": "At the boundary θ = θ₀, because the power function increases in θ and the size is its supremum over the null range."},
  {"q": "What is the power of a two-sided normal test at the null value itself?",
   "a": "Exactly α, split between the two tails. It is the lowest point of the power curve."},
  {"q": "A test rejects with probability 0.05 regardless of the data. What are its size and power?",
   "a": "Both 0.05 everywhere. It is a valid size-0.05 test with no power at all, which shows that controlling the size alone guarantees nothing worth having."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Take a rejection region someone hands you and compute its size by evaluating the probability of that region under the null value.",
  "Compute the power of the same region at any stated alternative, and know that the only change is the parameter value you substitute.",
  "Handle both the discrete case, where you sum a few binomial terms exactly, and the flat-density case, where probability is just a ratio of widths.",
  "Compute the power of a two-sided test as a sum over both tails, and say why it is below the one-sided test's power at the same alternative.",
  "Turn the power requirement round and solve for the sample size, with the size point and the power point entering with opposite signs and the answer rounded up.",
  "Read a power function: its value at the null is the size, its shape tells you one-sided from two-sided, and its limit tells you whether the test is consistent.",
  "Say which of the four levers — n, α, the effect size, the spread — gives you power for nothing, and which only moves you along a trade-off."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "Hitting an exact size when the data are discrete",
 "objective": "See why a discrete test usually cannot have size exactly 0.05, and what a randomised test does about it.",
 "blocks": [
  {"t": "step", "h": "The problem, in the coin example you already did",
   "body": "Go back to five tosses of a fair coin. The possible sizes of a test that rejects for large X are the tail probabilities themselves: P(X ≥ 5) = 1/32 = 0.03125, P(X ≥ 4) = 6/32 = 0.1875, P(X ≥ 3) = 16/32 = 0.5. There is nothing at 0.05, and nothing close to it. A discrete statistic takes finitely many values, so only finitely many sizes are available, and the one you want is almost never among them."},
  {"t": "def", "h": "A randomised test",
   "body": "Allow the test to use a coin of its own on the boundary. Reject outright when X ≥ 5; when X = 4 exactly, reject with probability γ and otherwise do not. Choose γ so that the total rejection probability under the null is exactly α."},
  {"t": "formula", "h": "Solving for the randomisation probability",
   "body": "α = P(X = 5 | p = 1/2) + γ P(X = 4 | p = 1/2)\n0.05 = 1/32 + γ (5/32)\n0.05 = 0.03125 + 0.15625 γ\nγ = 0.01875/0.15625 = 0.12"},
  {"t": "step", "h": "The power that buys",
   "body": "π(3/4) = P(X = 5 | 3/4) + 0.12 P(X = 4 | 3/4) = 243/1024 + 0.12 (405/1024) = 0.2373 + 0.0475 = 0.2848. Compare that with the 0.6328 you computed in scene 5 — far lower, because this test has size 0.05 and that one had size 0.1875. Lower false-alarm rate, lower power. The trade-off is doing exactly what it always does; nothing has been cheated."},
  {"t": "step", "h": "Why this is optional, and where it matters",
   "body": "No practising statistician randomises on the boundary; the honest report is the conservative non-randomised test, 'level 0.05, actual size 0.031'. Randomisation exists because the theory of most powerful tests needs it: without it, the statement 'a most powerful size-α test exists' would be false for discrete families. For NET, recognise the device and be able to find γ from one equation — that is the whole of what gets asked."}],
 "ask": {
  "q": "Why would a statistician report 'level 0.05, size 0.031' rather than randomise to reach 0.05 exactly?",
  "nudge": "Two different people with the same data would reach different conclusions. Ask whether that is acceptable in a result someone has to defend."}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "inference_t12_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "inferencet12",
 "topicId": "inference-t12",
 "moduleId": "inference",
 "title": "Size and Power of a Test",
 "breadcrumb": "Statistical Inference → Testing of Hypotheses → Size and power",
 "engine": "C",
 "engineName": "Testing — fixing one error rate and measuring the other",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Compute the size of a given test by evaluating its rejection region under the null value.",
  "Compute the power of a given test at a stated alternative, for discrete, flat-density and normal models.",
  "Read and sketch a power function, and use the fact that its value at the null equals the size.",
  "Find the size of a test with a composite null, and say why the worst case sits at the boundary.",
  "Solve the sample-size problem: given α and a required power at a stated alternative, find the smallest n.",
  "Say which changes raise power at no cost and which only trade one error against the other."],
 "prereq": [
  {"id": "p1", "name": "Binomial and normal tail probabilities",
   "why": "Every answer in this topic ends as a tail probability. If summing a few binomial terms or reading a normal tail is still slow, do that first — the ideas here will not be the thing holding you up."},
  {"id": "p2", "name": "Type I and Type II errors",
   "why": "Size and power are just these two error rates given numbers. You need both definitions cold, including which hypothesis each is computed under."},
  {"id": "p3", "name": "Distribution of the sample mean",
   "why": "The normal examples all turn on x̄ having standard deviation σ/√n. The sample-size calculation is that fact rearranged."}],
 "traps": [
  "The power is computed under the alternative; only the size uses the null.",
  "'More than 3' means 4 or more — one word moves the answer.",
  "A composite null takes its size at the boundary, not at an interior value.",
  "A two-sided test's power is a sum over both tails, and is lower than the one-sided test's at the same alternative.",
  "Sample size rounds UP; power rises with √n, not n.",
  "β means the Type II error rate in some books and the power function in others — never write it bare."],
 "revision": {
  "sheet": [
   "Size: α = P(reject H₀ | H₀ true). You choose it. Power at θ: π(θ) = P(reject H₀ | θ). Same event, different parameter value.",
   "Type II error at θ: β(θ) = 1 − π(θ). Power = 1 − β. Some books write β(θ) for the power itself — read the stem before matching an option.",
   "π(θ₀) = α always. Use it to check any power function you derive.",
   "Level is an upper bound on the size. A size-0.031 test is a level-0.05 test, and for discrete data that is the honest statement.",
   "Composite null H₀: θ ≤ θ₀ — size is the supremum of π over the null range, attained at the boundary θ₀ when π is increasing.",
   "One-sided normal test, σ known: reject when x̄ > μ₀ + z_α σ/√n, and π(μ) = P(Z > z_α − (μ − μ₀)√n/σ).",
   "Two-sided: multiplier 1.96 not 1.645 at α = 0.05, power is the sum over both tails, lowest point of the curve is α at μ₀.",
   "Sample size for power 1 − β at a gap d: √n ≥ (z_α + z_β)σ/d, then round up. At α = 0.05 and power 0.90 the constant is 1.645 + 1.282 = 2.927.",
   "Four levers: n up (free), α up (a trade), effect size up (not yours to set), σ down (design and measurement).",
   "Unbiased test: π(θ) ≥ α for every alternative. Nothing to do with unbiased estimation.",
   "Discrete data: exact size α is usually unreachable. A randomised test rejects with probability γ on the boundary, with γ fixed by one linear equation."],
  "cards": [
   ["Size of a test", "P(reject H₀ | H₀ true), evaluated at the null value — chosen in advance"],
   ["Power at θ", "P(reject H₀ | θ) — the same rejection region, with θ in place of the null value"],
   ["π(θ₀) equals what?", "α, the size. The power function always passes through the size at the null value"],
   ["Size with a composite null", "The supremum of the power function over the null range — the boundary value, when that function is increasing"],
   ["Sample size for a given power", "√n ≥ (z_α + z_β)σ/d, rounded up. The two normal points add, they do not subtract"],
   ["Two-sided power at α = 0.05", "Sum over both tails using the 1.96 cut-offs; always below the one-sided power at the same alternative"]],
  "tricks": [
   "Power must exceed size. If it does not, you have swapped the hypotheses — check before anything else.",
   "Keep discrete answers over a common denominator (/32, /1024). Two of the four options usually differ only after rounding.",
   "For flat densities, probability is width times height. Never integrate a rectangle.",
   "In a sample-size question, write 1.645 + 1.282 = 2.927 before anything else; seeing a 2.927 in your working confirms the signs are right."],
  "shortcuts": [
   "At α = 0.05 and power 0.90 the constant is 2.927; at power 0.80 it is 1.645 + 0.842 = 2.487.",
   "Two-sided at 0.05 uses 1.96; one-sided uses 1.645. The ratio of their cut-offs is why the two-sided test loses power.",
   "If a question gives you a region and two parameter values, it wants one probability computed twice. There is no theory to apply."],
  "remember": [
   "Null for size, alternative for power. Write which one you are using at the top of your working.",
   "Read the inequality in the stem out loud. 'More than 3' is not 'at least 3'.",
   "Round sample size up, always."]},
 "howto": "This lesson is arithmetic resting on two definitions, so the useful order is strict. Do the four opening checks before anything else — if the binomial tail and the normal tail are slow, nothing later will feel easy. Then read each section once without stopping at the algebra, and come back to the formula only after the worked example below it. Two of the worked examples are real NET questions from June 2026, and they are there to show you how little is actually being asked: read the region, compute one probability twice. The optional section at the end is marked as such; skip it on a first pass. Every section ends with a question — attempt it before opening the answer, because the attempt is what makes it stay.",
 "refs": [
  {"title": "Power of a Statistical Test", "where": "Lesson 25", "site": "Penn State STAT 415",
   "url": "https://online.stat.psu.edu/stat415/lesson/25", "type": "Course notes", "free": True,
   "checked": "2026-10-30",
   "why": "The cleanest treatment of the trade-off, worked on the normal mean with the sample-size calculation done explicitly. Read it after scene 4 if the arithmetic of the size condition still feels unfamiliar."},
  {"title": "Power Functions", "where": "Section 25.2", "site": "Penn State STAT 415",
   "url": "https://online.stat.psu.edu/stat415/lesson/25/25.2", "type": "Course notes", "free": True,
   "checked": "2026-10-30",
   "why": "Power functions drawn and compared, including the two-sided valley shape. The right companion to scene 12."},
  {"title": "Statistical Inference", "where": "Weeks on testing of hypotheses",
   "site": "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee",
   "url": "https://archive.nptel.ac.in/noc/courses/noc21/SEM1/noc21-ma23", "type": "Video course",
   "free": True, "checked": "2026-10-30",
   "why": "Indian syllabus wording and notation, which is what the NET paper uses. Useful if the β convention in a question confuses you."},
  {"title": "Statistical Inference, 2nd edition", "where": "Sections 8.3.1–8.3.4",
   "site": "Casella and Berger", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "The precise definitions, including the one where β(θ) denotes the power function itself. Worth seeing both conventions in print once."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 9",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "Randomised tests and exact sizes for discrete families, treated at the level the optional scene uses."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored October 2026 for this platform against the UGC NET Statistics syllabus, and prioritised from the June 2026 paper, where two of the eleven inference items (Q49, the five-toss coin; Q39, the flat density with critical region x ≥ 0.5) sat directly on this topic and a third (Q43) asked for the order of the steps of a test. Those three are worked here as the lesson's own examples and appear in the pool. Previous-year questions themselves are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "inf-t12-m-%02d" % i, "format": fmt, "topic": "inference-t12",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "The size of a test is the probability that it:",
 ["rejects H₀ when H₀ is true",
  "rejects H₀ when H₁ is true",
  "fails to reject H₀ when H₁ is true",
  "fails to reject H₀ when H₀ is true"],
 "A",
 "The size is the Type I error rate, α = P(reject H₀ | H₀ true). Option B is the power, option C is the Type II error, and option D is the correct non-rejection, 1 − α."))

I.append(q(2, "single", "easy",
 "If β denotes the probability of a Type II error, the power of the test is:",
 ["β", "1 − β", "α", "1 − α"],
 "B",
 "Power is the probability of rejecting a false null, which is one minus the probability of failing to do so: 1 − β. Note that some textbooks write β(θ) for the power function itself, in which case power = β(θ) — always read the stem for the convention in use."))

I.append(q(3, "single", "easy",
 "The power function π(θ) of a test, evaluated at the null value θ₀, equals:",
 ["1", "the size of the test", "the Type II error probability", "zero"],
 "B",
 "π(θ₀) = P(reject H₀ | θ₀) is exactly the definition of the size. This identity is the quickest check on any power function you derive: substitute θ₀ and α must come back."))

I.append(q(4, "order", "easy",
 "A rejection region and two parameter values are given. Arrange the steps of computing the size and the power in the correct order.",
 ["A, B, C, D", "C, A, B, D", "A, C, B, D", "C, B, A, D"],
 "B",
 "Write the region out as a set of values first — this is where 'more than 3' is distinguished from 'at least 3'. Then the null value gives the size, then the alternative gives the power, and the sanity check that power exceeds size comes last. This is the pattern of June 2026 Q43.",
 items=["A. Evaluate the probability of the region under the null value",
        "B. Evaluate the probability of the same region under the alternative value",
        "C. Write the rejection region explicitly as a set of values of the statistic",
        "D. Check that the power exceeds the size"]))

I.append(q(5, "single", "easy",
 "Which change raises the power of a test without raising its size?",
 ["increasing the significance level α",
  "increasing the sample size n",
  "widening the rejection region at fixed n",
  "using a two-sided alternative instead of a one-sided one"],
 "B",
 "Only more data improves the detection rate at no cost in false alarms. Raising α, or equivalently widening the region, raises power and the false-alarm rate together. Going two-sided lowers power against a one-sided departure, because the cut-off moves out from 1.645 to 1.96."))

I.append(q(6, "single", "easy",
 "A test of H₀ based on discrete data has rejection probability 0.031 under the null. Which description is correct?",
 ["its size is 0.05", "it is a level-0.05 test of size 0.031",
  "it is invalid, since the size must equal the stated level",
  "its power is 0.969"],
 "B",
 "The size is the exact null rejection probability, 0.031; the level is any upper bound on it, so 0.05 is a valid level. For discrete statistics only finitely many sizes are attainable and an exact 0.05 usually is not one of them, so this is the ordinary honest description, not a defect."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "A coin is tossed 5 times to test H₀: p = 1/2 against H₁: p = 3/4, and H₀ is rejected if more than 3 heads are obtained. The size of the test is:",
 ["0.1875", "0.5000", "0.0313", "0.3125"],
 "A",
 "More than 3 heads means X = 4 or 5. Under p = 1/2, P(X ≥ 4) = [C(5,4) + C(5,5)]/32 = 6/32 = 0.1875. Option B is P(X ≥ 3), the answer to 'at least 3'; option C is P(X = 5) alone; option D is P(X = 4) alone.",
 check="The size uses p = 1/2 and the values 4 and 5 only. If the number 3 entered the count, the inequality in the stem was read as 'at least'."))

I.append(q(8, "numeric", "moderate",
 "For the same test — 5 tosses, reject H₀: p = 1/2 if more than 3 heads appear — the power against H₁: p = 3/4 is:",
 ["0.3955", "0.2373", "0.6328", "0.1875"],
 "C",
 "P(X ≥ 4 | p = 3/4) = C(5,4)(3/4)⁴(1/4) + (3/4)⁵ = 405/1024 + 243/1024 = 648/1024 = 0.6328. Option A is P(X = 4) alone, option B is P(X = 5) alone, and option D is the size — computed under the null instead of the alternative. This is June 2026 Q49.",
 check="The power must use p = 3/4 and must exceed the size 0.1875. An answer equal to 0.1875 means the null value was substituted."))

I.append(q(9, "numeric", "moderate",
 "The density is f(x; θ) = 1/θ for 0 ≤ x ≤ θ. To test H₀: θ = 1 against H₁: θ = 2 from a single observation, the critical region is x ≥ 0.5. The power of the test is:",
 ["0.50", "0.75", "0.25", "1.00"],
 "B",
 "Under θ = 2 the density is 1/2 on the interval 0 to 2, so P(X ≥ 0.5) = 1.5 × (1/2) = 0.75. Option A is the size, computed under θ = 1, which is the error the options are built around. This is June 2026 Q39.",
 check="The power uses θ = 2, so the rectangle has width 2 and height 1/2. If the width used was 1, the null value was substituted."))

I.append(q(10, "numeric", "moderate",
 "X₁,…,X₂₅ are iid N(μ, 100) with σ = 10 known. H₀: μ = 50 is tested against H₁: μ > 50 at α = 0.05, rejecting when x̄ > 50 + 1.645(σ/√n). The power at μ = 54 is approximately:",
 ["0.6387", "0.3612", "0.8023", "0.0500"],
 "C",
 "σ/√n = 10/5 = 2, so the region is x̄ > 50 + 1.645(2) = 53.29. Under μ = 54 this gives P(Z > (53.29 − 54)/2) = P(Z > −0.355) = 0.6387. Equivalently π(54) = P(Z > 1.645 − (54 − 50)√25/10) = P(Z > 1.645 − 2). Option B is the Type II error 1 − 0.6387, and option D is the size — the power read under the null instead of the alternative.",
 check="Use π(μ) = P(Z > z_α − (μ − μ₀)√n/σ). Here (54 − 50)(5)/10 = 2, so the argument is 1.645 − 2 = −0.355."))

I.append(q(11, "single", "moderate",
 "For a one-sided test of the composite null H₀: μ ≤ 100 that rejects for large x̄, the size of the test is computed at:",
 ["μ = 100, the boundary of the null",
  "the value of μ under the alternative",
  "any convenient value inside the null, since all give the same answer",
  "the observed sample mean"],
 "A",
 "The size of a test with a composite null is the supremum of the power function over the null range. Here the power function increases in μ, so over μ ≤ 100 its largest value sits at the boundary μ = 100. Interior values give smaller rejection probabilities and so understate the size."))

I.append(q(12, "multi", "moderate",
 "Consider the size and power of a test. Read the four statements and decide which are correct.",
 ["A and C only", "A, C and D only", "B and D only", "A and D only"],
 "A",
 "A is true, straight from the definitions. B is false — the power is computed under the alternative, which is the commonest error in the topic. C is true: the power function passes through the size at the null value. D is false — a test can have correct size and no power at all, as the test that ignores the data and rejects with probability α shows.",
 statements=["The size of a test is chosen by the experimenter before the data are seen.",
             "The power of a test is computed under the null hypothesis.",
             "The power function evaluated at the null value equals the size.",
             "A test with the correct size necessarily has acceptable power."],
 verdicts=verd(
  (True, "True. α is a design choice, fixed in advance, and the rejection region is then built to respect it."),
  (False, "False. The power is the rejection probability under the alternative — or at whatever parameter value is named. Only the size uses the null."),
  (True, "True. π(θ₀) = P(reject | θ₀) = α by definition, which makes it a useful check on a derived power function."),
  (False, "False. Controlling the size alone guarantees nothing: a test that rejects with probability α regardless of the data has exact size α and power α everywhere."))))

I.append(q(13, "numeric", "moderate",
 "X₁,…,Xₙ are iid N(μ, 25). Test H₀: μ = 100 against H₁: μ > 100 at α = 0.05. The smallest n for which the power at μ = 102 is at least 0.90 is (use z₀.₀₅ = 1.645, z₀.₁₀ = 1.282):",
 ["54", "53", "17", "28"],
 "A",
 "√n ≥ (1.645 + 1.282)(5)/2 = 2.927(2.5) = 7.3175, so n ≥ 53.54 and the smallest integer is 54. Option B rounds to the nearest integer instead of up, leaving the power just under at 0.897. Option D uses the difference 1.645 − 1.282 rather than the sum.",
 check="The two normal points ADD. If 2.927 does not appear in your working, the signs are wrong; and the final answer is rounded up, never to nearest."))

I.append(q(14, "single", "moderate",
 "At α = 0.05, the two-sided test of H₀: μ = μ₀ based on x̄ with σ known rejects when:",
 ["x̄ > μ₀ + 1.645 σ/√n",
  "|x̄ − μ₀| > 1.96 σ/√n",
  "|x̄ − μ₀| > 1.645 σ/√n",
  "x̄ > μ₀ + 1.96 σ/√n"],
 "B",
 "A two-sided alternative splits α across both tails, 0.025 in each, so the multiplier is 1.96. Option C puts the whole 5% in each tail, giving a size of 0.10. Options A and D are one-sided regions, and D also uses the two-sided multiplier on a one-sided region, giving size 0.025."))

I.append(q(15, "single", "moderate",
 "Two tests of the same H₀: μ = μ₀ use the same data and the same α = 0.05: one is one-sided against μ > μ₀, the other two-sided. At a particular alternative μ₁ > μ₀:",
 ["the one-sided test has the greater power",
  "the two-sided test has the greater power",
  "both have the same power, since α is the same",
  "the comparison depends on σ"],
 "A",
 "The one-sided test spends its whole 5% on the relevant side, so its cut-off is at 1.645 standard errors instead of 1.96 and it rejects more readily against a departure in that direction. The two-sided test pays for its ability to detect departures either way. The ordering holds for every σ and every n."))

I.append(q(16, "single", "moderate",
 "In the one-sided normal test with σ known, the power at a fixed alternative increases with:",
 ["n", "√n", "n²", "1/√n"],
 "B",
 "The power is P(Z > z_α − (μ − μ₀)√n/σ), and n enters only as √n. This is why quadrupling the sample size halves the gap detectable at a given power, and why sample-size answers are larger than intuition suggests."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "A test of H₀: p = 1/2 based on 5 tosses rejects for large X. Consider the following statements about attaining an exact size of 0.05.",
 ["B and C only", "A and C only", "A, B and C only", "C and D only"],
 "A",
 "A is false: the attainable sizes are the tail probabilities 1/32 = 0.031, 6/32 = 0.1875 and so on, and 0.05 is not among them. B is true — the randomised test rejects at X = 5 and with probability γ at X = 4, with γ = (0.05 − 0.03125)/(5/32) = 0.12. C is true. D is false: with size reduced from 0.1875 to 0.05, the power falls to 0.2848, well below 0.6328.",
 statements=["A non-randomised test based on X can attain size exactly 0.05.",
             "A randomised test attains size exactly 0.05 by rejecting with probability 0.12 when X = 4.",
             "Reporting the test as 'level 0.05, size 0.031' is a valid description of the non-randomised test.",
             "The randomised size-0.05 test has higher power at p = 3/4 than the non-randomised test that rejects when X ≥ 4."],
 verdicts=verd(
  (False, "False. X takes six values, so only six tail probabilities are available: 0.031, 0.1875, 0.5 and so on. None equals 0.05."),
  (True, "True. Solve 0.05 = 1/32 + γ(5/32) to get γ = 0.01875/0.15625 = 0.12."),
  (True, "True, and it is the description a practising statistician would use, since the level is an upper bound on the size."),
  (False, "False. The non-randomised X ≥ 4 test has size 0.1875 and power 0.6328; cutting the size to 0.05 cuts the power to 0.2848. Lower false-alarm rate always costs power at fixed n."))))

I.append(q(18, "numeric", "hard",
 "X₁,…,X₁₆ are iid N(μ, 16). The two-sided test of H₀: μ = 10 at α = 0.05 rejects when |x̄ − 10| > 1.96. The power at μ = 12, to four decimal places, is:",
 ["0.5160", "0.5000", "0.4840", "0.6387"],
 "A",
 "σ/√n = 4/4 = 1, so the region is x̄ > 11.96 or x̄ < 8.04. Under μ = 12: P(Z > −0.04) = 0.5160 and P(Z < −3.96) = 0.00004, summing to 0.5160. Option D is the one-sided test's power at the same alternative, which is higher because its cut-off is 1.645 rather than 1.96.",
 check="A two-sided power is a sum over both tails. The far tail is tiny but not zero, and the total must come out below the one-sided power 0.6387."))

I.append(q(19, "single", "hard",
 "A test is described as unbiased. This means:",
 ["its power at every alternative is at least its size",
  "the statistic it uses is an unbiased estimator of θ",
  "its size equals its stated level exactly",
  "its power function is symmetric about θ₀"],
 "A",
 "An unbiased test satisfies π(θ) ≥ α for every θ in the alternative — it never rejects a false null less often than it rejects a true one. The word is unrelated to unbiased estimation, which is option B's confusion, and it says nothing about attaining the level exactly or about symmetry."))

I.append(q(20, "single", "hard",
 "The power function of a test of H₀: μ = 10 is drawn and has a minimum value of 0.05 at μ = 10, rising towards 1 in both directions. The test is:",
 ["a one-sided test of size 0.05",
  "a two-sided test of size 0.05",
  "a biased test, since the power dips",
  "a test of size 0.95"],
 "B",
 "Rising in both directions is the signature of a two-sided rejection region, and the minimum value of a power function at the null value is the size, so α = 0.05. It is not biased: the power is at least 0.05 at every alternative, with equality only at the null value itself, which is not in the alternative."))

# A pool whose keys pile onto one letter rewards a guesser, and the validator caps any
# letter at 40%. Authoring produced ten A's, so swap the correct option into a chosen
# position for nine items. Swapping positions i and j is its own inverse, so any
# "option X" reference inside the explanation just swaps the same two letters.
import re
LET = "ABCD"
WANT = {"inf-t12-m-03": "C", "inf-t12-m-05": "D", "inf-t12-m-10": "D",
        "inf-t12-m-11": "C", "inf-t12-m-13": "D", "inf-t12-m-15": "C",
        "inf-t12-m-16": "D", "inf-t12-m-17": "C", "inf-t12-m-19": "D"}

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
        # statements as bare letters and must be left alone
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
 "moduleId": "inference", "topicId": "inference-t12", "source": "mastery",
 "label": "Size and power of a test — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
