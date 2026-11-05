#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 4.15 — Choosing the right test (topic inference-t15).

Built on PYQ evidence. June 2026 Q43 gave the five steps of a hypothesis test out of order
and asked for the sequence; the official answer is C, A, B, D, E — form the hypothesis, then
check the assumptions, then compute, then compare, then infer. The stored response sheet
shows option A was marked, which puts assumption-checking BEFORE the hypothesis is stated;
the reason that is wrong (you cannot know which assumptions matter until you know which test,
which depends on the hypothesis) is this lesson's opening argument.

The ten practice variants on that question are all about the practice of testing rather than
its derivations: the first step, what the null always contains, the p-value, when H₀ is
rejected, when α is fixed, what "failing to reject" means, significance against practical
importance, the cost of many tests at α = 0.05, what determines the critical region, and how
to choose between one and two tails. All ten are taught here and all ten are in the pool.

This is a synthesis lesson: 4.12, 4.10, 4.13 and 4.17 are its prerequisites.

Writes seed/lesson_t15.json and seed/inference_t15_mastery.json.
Run: python3 lesson_t15.py
"""
import json, io, os, re

OUT = "seed/lesson_t15.json"
POOL = "seed/inference_t15_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Settle the four pieces of vocabulary that this topic's questions are built from, because here the words ARE the content.",
 "ask": {
  "q": "This topic has almost no algebra in it. What, then, is it testing?",
  "nudge": "Look at the four checks below. Would a candidate who can derive every critical region in the syllabus necessarily get them right?"},
 "body": [
  "Every other topic in this module derives something. This one does not. It is about the procedure — what order the steps go in, what the words mean, and which test belongs to which situation.",
  "That makes it easy to dismiss and easy to lose marks on. The questions are short, they look like common sense, and they turn on distinctions that are genuinely subtle: the difference between failing to reject a hypothesis and accepting it, or between a result being significant and being important.",
  "Four checks, all vocabulary. If any of them is hazy, the questions in this topic will feel like coin flips even though they are not."],
 "items": [
  {"ask": "What is a p-value, stated precisely?",
   "recall": "The probability, computed under H₀, of getting a result at least as extreme as the one observed.",
   "refresh": [
    "Note what it is conditional on: H₀ being true. It is a statement about the data given the hypothesis, never about the hypothesis given the data.",
    "So it is NOT the probability that H₀ is true, and it is not the probability that the result was due to chance. Both of those readings are offered as options and both are wrong.",
    "A small p-value means the data would be surprising if H₀ held. That is all it means, and it is enough to act on."]},
  {"ask": "When should the significance level α be chosen?",
   "recall": "Before looking at the data.",
   "refresh": [
    "α is a decision about how often you are willing to raise a false alarm. It is a judgement about consequences, not about this particular sample.",
    "Choosing it afterwards — seeing p = 0.04 and declaring α = 0.05, or seeing p = 0.06 and declaring α = 0.10 — means the stated size of the test is fiction. The real size is whatever your decision rule actually was.",
    "The same applies to choosing one-tailed versus two-tailed, and to choosing which test. Every such choice has to be made on grounds that do not involve the observed data."]},
  {"ask": "What does 'we fail to reject H₀' mean, and what does it not mean?",
   "recall": "That this sample gave insufficient evidence against H₀. It does NOT mean H₀ is true, or that it has been shown to be true.",
   "refresh": [
    "A test is built to control the false-alarm rate, not to establish the null. Absence of evidence against something is weak evidence for it at best, and with a small sample it is almost no evidence at all.",
    "This is why the careful phrase is 'fail to reject' rather than 'accept'. Writing 'accept H₀' is treated as an error in most question papers.",
    "The honest companion to a non-rejection is the power: if the test had little power against the effects that matter, the non-result says nothing. Topic 4.12 is what makes that statement quantitative."]},
  {"ask": "A single sample from a normal population, variance unknown, and you want to test a value of the mean. Which test?",
   "recall": "The one-sample t test, with n − 1 degrees of freedom.",
   "refresh": [
    "σ unknown is the usual case, and it means t rather than z. The z test is for σ known, which almost never happens outside a textbook.",
    "The t test needs the observations to be independent and roughly normal — or a sample large enough for the central limit theorem to carry the mean.",
    "Section 11 collects the whole mapping from situation to test. This one is the most common and worth having instantly."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "Why the order of the steps is not a formality",
 "objective": "See that each step constrains the next, so a rearranged procedure is not merely untidy but invalid.",
 "body": [
  "The five steps of a test look like a checklist, and a checklist's order usually does not matter much. Here it does, for a specific reason: each step determines what the next one can be.",
  "The hypothesis has to come first because it decides which test is relevant, and the test decides which assumptions need checking. Checking assumptions before you know the test means checking you do not know what for.",
  "And the significance level has to be fixed before the statistic is computed, because a level chosen after seeing the number is not a level at all.",
  "The deeper point is that the order protects the honesty of the final probability statement. Every step taken out of order lets information from the data leak into a decision that was supposed to be made without it, and the stated error rate quietly stops being true."],
 "scenario": {
  "teaser": "A researcher runs five tests, reports the one that worked, and cannot see what is wrong.",
  "title": "The fifth test",
  "body": [
   "A graduate student is studying a teaching intervention. She measures five outcomes — comprehension, recall, speed, confidence, and attendance — tests each at α = 0.05, and finds one significant result: speed, p = 0.03. The write-up reports that the intervention improves reading speed.",
   "Nothing in the arithmetic is wrong. Each test was computed correctly, and each had size 0.05.",
   "But the chance that AT LEAST ONE of five true nulls gets rejected at α = 0.05 is 1 − 0.95⁵ = 0.226. So a study with no real effect at all produces at least one 'significant' outcome about one time in four. Reporting the winner as though it were the only test performed is reporting a 22.6% procedure as a 5% one.",
   "With twenty outcomes it is worse: 1 − 0.95²⁰ = 0.642. A researcher measuring twenty things and reporting the best is almost guaranteed a finding, and the finding is almost worthless.",
   "The repair is not complicated. Decide in advance which outcome is the primary one, or adjust the level for the number of tests — at five tests, 0.05/5 = 0.01 each, which brings the family-wise rate back to 0.049. What cannot be repaired afterwards is the selection: once the data chose which result to report, the stated p-value describes a procedure nobody ran.",
   "This is the same principle as fixing α in advance, applied to a different choice. The procedure must be decided without the data's help, or its error rate is fiction."],
  "q": "Why does reporting only the significant result make the stated p-value wrong?",
  "answer": "Because the real procedure was 'run five tests and report the smallest p-value', and that procedure rejects a true null 22.6% of the time, not 5%. The p-value of 0.03 correctly describes the speed test considered alone, but the speed test was not considered alone — it was selected because it won. The number is right for a question that was not asked."},
 "ask": {
  "q": "The student could say she had always intended to focus on reading speed. What would make that claim credible?",
  "nudge": "Something written down before the data existed. What is such a document called?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "Significant does not mean important",
 "objective": "Watch a trivial effect become reliably detectable as the sample grows, which is the trap behind one of this topic's questions.",
 "viz": {"type": "np-power", "n": 4, "d": 0.2, "alpha": 0.05, "sd": 1},
 "body": [
  "The two curves are the sampling distribution of the mean under H₀ and under a true effect. The gap between them is set to 0.2 while the population standard deviation is 1 — so the real effect is a fifth of a standard deviation, which in most settings is too small to matter to anybody.",
  "Start at n = 4 and read the power: about 0.11. A study this size would almost never detect the effect, and would be right not to bother.",
  "Now slide n upward and watch the power climb for the SAME trivial effect: about 0.20 at n = 16, 0.35 at n = 40, and 0.71 at n = 120. Nothing about the effect changed. Only the sample size did.",
  "Push n to its maximum. The power approaches 1, which means that with enough data this fifth-of-a-standard-deviation difference becomes a near-certain rejection. And that is not a flaw — the effect is real, and the test is correctly detecting a real effect.",
  "The flaw is in the reporting. 'Statistically significant' means the data are inconsistent with the null; it says nothing about whether the departure is large enough to act on. With a big enough sample every real effect, however tiny, is significant.",
  "The remedy is the one from topic 4.13: report the confidence interval alongside the test. An interval of (0.0004, 0.0396) tells you both that the effect is non-zero and that it is negligible. The p-value alone cannot distinguish those two facts, and a question offering 'a significant result is an important result' is offering a wrong answer."],
 "ask": {
  "q": "If a large study reports p = 0.001 for a difference of 0.02 units, what single further number would settle whether it matters?",
  "nudge": "You need something in the units of the thing being measured, with its uncertainty attached."}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The five steps, and why each one must come where it does",
 "objective": "Fix the sequence and the reason for it, which is exactly what June 2026 Q43 asked.",
 "blocks": [
  {"t": "step", "h": "The sequence",
   "body": "1. Formulate the hypotheses — H₀ and H₁, including whether the alternative is one-sided or two-sided.\n2. Check the assumptions the chosen test requires.\n3. Compute the test statistic.\n4. Compare it with the critical value, or compute the p-value.\n5. Draw the inference, in the language of the original problem.\nThe significance level α is fixed as part of step 1, before anything is computed."},
  {"t": "def", "h": "Why the hypothesis comes before the assumptions",
   "body": "This is the ordering June 2026 Q43 turned on, and the reason is simple once stated: different tests require different assumptions. A t test needs approximate normality of the observations; a chi-square goodness-of-fit test needs adequate expected cell counts; a test on a variance needs normality far more critically than a test on a mean does. Until the hypothesis has told you which test is relevant, there is no determinate list of assumptions to check. Assumption-checking first is checking you do not yet know what for."},
  {"t": "step", "h": "Why α belongs to step 1",
   "body": "α is a judgement about the relative cost of the two errors, which is a feature of the problem and not of the sample. Fixed afterwards, it is chosen to make the result come out, and the stated size of the test becomes untrue. The same goes for the choice of a one-tailed or two-tailed alternative: subject-matter reasoning decides it, never the direction the data happened to go."},
  {"t": "step", "h": "Why the inference comes last and in words",
   "body": "Step 4 produces 'the statistic is 2.43, the critical value is 1.96'. That is not an answer to anybody's question. Step 5 says 'at the 5% level there is evidence that the mean tread depth differs from the specification' — and, if the test did not reject, says so without claiming the null has been established. The marks in a descriptive question are often in this step, because it is where candidates write 'accept H₀'."},
  {"t": "def", "h": "The one step people invent",
   "body": "Looking at the data to decide the hypothesis is not a step. It is the error that the whole ordering exists to prevent, and it has a name — testing a hypothesis suggested by the data. If the data suggested the hypothesis, the honest response is to state it as a hypothesis for a FUTURE sample, not to test it on the sample that suggested it."}],
 "flow": {
  "title": "The order, and what each step fixes",
  "alt": "Flow chart of the five steps of a hypothesis test",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "1. State H₀, H₁ and α — before seeing the data", "kind": "start"},
   {"id": "b", "r": 1, "c": 1, "label": "This fixes WHICH TEST is relevant", "kind": "step"},
   {"id": "c", "r": 2, "c": 1, "label": "2. Check the assumptions THAT test requires", "kind": "step"},
   {"id": "d", "r": 3, "c": 1, "label": "3. Compute the test statistic", "kind": "step"},
   {"id": "e", "r": 4, "c": 1, "label": "4. Compare with the critical value, or find the p-value", "kind": "step"},
   {"id": "f", "r": 5, "c": 1, "label": "5. State the inference in the problem's own words", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "b", "to": "c"}, {"from": "c", "to": "d"},
   {"from": "d", "to": "e"}, {"from": "e", "to": "f"}],
  "note": "Each step is determined by the one above it, which is why the order is not interchangeable. The hypothesis selects the test; the test selects the assumptions."},
 "ask": {
  "q": "Suppose you check assumptions first and find the data badly non-normal. Why does that not justify putting step 2 before step 1?",
  "nudge": "Non-normal matters a great deal for one of the tests in section 11 and hardly at all for another. Which one were you planning to use?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — June 2026, Q43",
 "objective": "Reason out the sequence rather than recalling it, and see why the marked option fails.",
 "ask": {
  "q": "Option A differs from the answer only by swapping the first two steps. Why is that enough to make it wrong?",
  "nudge": "Ask what you would be checking, and against which test's requirements, if you started with step A."},
 "problem": "The steps of testing a hypothesis are given as: A. Checking the assumptions of the test. B. Calculation of the test statistic. C. Formation of hypothesis. D. Comparing with the tabulated values. E. Drawing the inference. Arrange them in proper sequence. The options offered were (A) A, C, B, D, E; (B) C, A, D, B, E; (C) A, C, D, B, E; (D) C, A, B, D, E.",
 "steps": [
  {"say": "Fix the two ends first, because they are the least contestable.",
   "math": "first:  C — formation of hypothesis\nlast:   E — drawing the inference",
   "why": "Every option ends with E, so the last step is free. The first step is where two of the four options disagree, which tells you immediately that this is the distinction being tested."},
  {"say": "Settle whether C or A comes first by asking what A would mean on its own.",
   "math": "A before C:  check the assumptions of... which test?\nC before A:  the hypothesis names the test, and the test names its assumptions",
   "why": "This is the whole question. Assumption-checking is not a generic activity — a t test, a chi-square test and a variance test have different requirements. Without the hypothesis there is no determinate list to check. So C precedes A, which eliminates options A and C."},
  {"say": "Now order the middle two, B and D, among the remaining options.",
   "math": "option B: C, A, D, B, E  — compare with tables, THEN compute the statistic\noption D: C, A, B, D, E  — compute the statistic, THEN compare",
   "why": "You cannot compare a statistic you have not computed. Option B has the comparison before the calculation, which is impossible, so it goes."},
  {"say": "State the answer.",
   "math": "C, A, B, D, E  →  option (D)",
   "why": "Hypothesis, assumptions, calculation, comparison, inference. The official answer is D; the response sheet shows A was marked, which is the A-before-C error specifically."}],
 "after": "Worth noticing how this question was built. One option has an impossible order (comparing before computing) and is there to be discarded quickly. Two options share the A-before-C error, which is the real discriminator. Reasoning from 'what would I be checking, and against what?' settles it in one line, whereas trying to recall a memorised sequence under time pressure is exactly how the wrong option gets picked."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the sequence and the two vocabulary distinctions that carry marks.",
 "intro": "Answer each before revealing it.",
 "items": [
  {"q": "Give the five steps of a hypothesis test in order.",
   "a": "Formulate the hypotheses (and fix α); check the assumptions of the chosen test; compute the statistic; compare with the critical value or find the p-value; draw the inference in words."},
  {"q": "Why must the hypothesis precede the assumption check?",
   "a": "Because the hypothesis determines which test is relevant, and different tests require different assumptions. There is no list to check until the test is known."},
  {"q": "Define the p-value.",
   "a": "The probability, under H₀, of a result at least as extreme as the one observed. Not the probability that H₀ is true."},
  {"q": "What does failing to reject H₀ establish?",
   "a": "That this sample gave insufficient evidence against it. Not that it is true."},
  {"q": "When are α and the choice of one or two tails decided?",
   "a": "Before seeing the data, on grounds of consequences and subject matter respectively."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — pick the test",
 "objective": "Work the mapping from situation to test in the direction the exam asks it.",
 "problem": "For each situation, name the appropriate test. All samples are independent unless stated, and 'normal' means the population may be taken as normal.",
 "steps": [
  {"say": "A single sample of 12 observations from a normal population with unknown variance. You want to test whether the mean equals a stated value.",
   "blank": {"prompt": "Which test?",
             "answer": "the one-sample t test, with 11 degrees of freedom",
             "accept": ["one-sample t test", "t test", "student's t test with n-1 df",
                        "one sample t, 11 df", "t-test with 11 df"],
             "hint": "σ is unknown, which rules out the z test. How many degrees of freedom does s² carry?"},
   "why": "Unknown variance means t, not z, and the degrees of freedom are n − 1 = 11. This is the most frequently needed answer in the whole mapping."},
  {"say": "The same single normal sample, but now you want to test whether the VARIANCE equals a stated value.",
   "blank": {"prompt": "Which test, and what is its statistic?",
             "answer": "the chi-square test, with statistic (n − 1)s²/σ₀² on n − 1 degrees of freedom",
             "accept": ["chi-square test, (n-1)s^2/sigma0^2", "chi square test on n-1 df",
                        "chi-squared test for variance", "χ² test with (n−1)s²/σ₀²"],
             "hint": "This is the pivot from topic 4.13, used as a test statistic rather than inverted into an interval."},
   "why": "The same quantity that gave the confidence interval for σ² gives the test. Note that this test is much more sensitive to non-normality than the t test is — the optional section returns to that."},
  {"say": "Two independent normal samples with equal unknown variances, and you want to compare their means.",
   "blank": {"prompt": "Which test, and on how many degrees of freedom?",
             "answer": "the two-sample t test with a pooled variance, on n₁ + n₂ − 2 degrees of freedom",
             "accept": ["two-sample t test, n1+n2-2 df", "pooled t test", "independent samples t test",
                        "two sample t with pooled variance"],
             "hint": "Two means are estimated, so two degrees of freedom are spent."},
   "why": "The pooled version assumes the two variances are equal; without that assumption the Welch version is used instead, with adjusted degrees of freedom. Which one a question wants is usually stated in the phrase 'equal variances'."},
  {"say": "The same subjects measured before and after an intervention.",
   "blank": {"prompt": "Which test, and why not the two-sample one?",
             "answer": "the paired t test on the differences, with n − 1 degrees of freedom, because the two measurements on a subject are not independent",
             "accept": ["paired t test", "paired t-test on differences, n-1 df",
                        "one-sample t test on the differences", "matched pairs t test"],
             "hint": "Independence is the assumption at stake. Is a subject's 'after' reading independent of their 'before'?"},
   "why": "The two-sample test assumes independent samples, and repeated measurements on one person are not independent. Reducing each pair to its difference restores independence and turns the problem into a one-sample t test on the differences. Choosing the two-sample test here is a genuine error, not a stylistic preference."},
  {"say": "Observed counts in six categories, and a claimed set of probabilities for them.",
   "blank": {"prompt": "Which test, how many degrees of freedom, and what condition must the counts satisfy?",
             "answer": "the chi-square goodness-of-fit test on 5 degrees of freedom, with expected counts large enough (commonly at least 5 per cell)",
             "accept": ["chi-square goodness of fit, 5 df", "goodness of fit test with k-1=5 df",
                        "χ² goodness of fit, expected counts >= 5", "chi squared gof 5 df"],
             "hint": "Six categories, but the probabilities sum to 1 — so how many are free?"},
   "why": "k − 1 = 5 degrees of freedom, because of the sum-to-one constraint; this is exactly the counting rule from topic 4.10. The expected-count condition is what makes the chi-square approximation usable, and it is the assumption step for this test."}],
 "after": "Five situations, five different tests, and in each case the test was determined by two things only: what is being tested (mean, variance, counts) and the structure of the data (one sample, two independent samples, paired). Section 11 puts that in a table. The whole skill is reading those two things off the question."})

S.append({
 "kind": "theory", "id": "s7", "mins": 7,
 "title": "The rules that keep a stated error rate true",
 "objective": "Collect the integrity requirements, which is what most of this topic's variants ask about.",
 "blocks": [
  {"t": "def", "h": "The null hypothesis carries the equality",
   "body": "H₀ always contains the equality: θ = θ₀, or θ ≤ θ₀, or θ ≥ θ₀. The alternative never does. The reason is operational — the critical value has to be computed under a specific distribution, and only a hypothesis that pins the parameter down (at least at a boundary) provides one. A question asking what the null 'always contains' wants the equality sign."},
  {"t": "step", "h": "The critical region is determined before the data",
   "body": "It depends on the null distribution of the statistic, the chosen α, and the direction of the alternative. It does not depend on the observed value. Phrases like 'the critical region is determined by the observed statistic' are wrong, and the error is the same one as choosing α afterwards."},
  {"t": "formula", "h": "When H₀ is rejected",
   "body": "reject H₀  ⟺  the statistic falls in the critical region  ⟺  p-value ≤ α\nThe two formulations are equivalent, not alternatives, and the p-value route is just the critical-value route read backwards."},
  {"t": "step", "h": "One tail or two is a subject-matter decision",
   "body": "Use a one-tailed test when the subject matter rules out one direction, or when only one direction would prompt action. Never choose the tail after seeing which way the data went — that doubles the real size of the test, since you were effectively prepared to reject in either tail at α each. The honest default, absent directional knowledge, is two-tailed."},
  {"t": "def", "h": "Many tests inflate the error rate",
   "body": "With m independent tests each of size α, the probability of at least one false rejection is 1 − (1 − α)^m. At α = 0.05 that is 0.226 for 5 tests, 0.401 for 10 and 0.642 for 20. Controlling it requires either naming one primary outcome in advance or lowering each test's level — the Bonferroni choice α/m brings the family-wise rate back to about α."},
  {"t": "step", "h": "Significance and importance are different questions",
   "body": "A significant result says the data are inconsistent with H₀. Whether the departure matters is a question about its SIZE, which the p-value does not report. With a large enough sample an arbitrarily small real effect becomes significant — the explore section showed a fifth of a standard deviation reaching power 0.71 at n = 120. The remedy is to report a confidence interval, which carries both the direction and the magnitude."}],
 "ask": {
  "q": "Choosing the tail after seeing the data is described as doubling the real size. Why double rather than some other factor?",
  "nudge": "You were willing to reject in the upper tail if the data went up, and in the lower tail if it went down. What is the total probability of rejecting a true null under that rule?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — the cost of many tests",
 "objective": "Put numbers on the multiplicity problem and on its standard correction.",
 "problem": "A study tests m independent null hypotheses, each at α = 0.05, and all of them are in fact true. (a) Give the probability that at least one is rejected, for m = 1, 5, 10 and 20. (b) What is that probability called? (c) Using the Bonferroni correction, what level should each test use when m = 20, and what family-wise rate does it achieve? (d) Why is it not a valid repair to apply the correction after seeing which result was significant?",
 "hints": [
  "For (a), work with the complement: the probability that no true null is rejected is (1 − α) raised to the power m, since the tests are independent.",
  "For (c), Bonferroni divides the overall level by the number of tests. Compute the resulting family-wise rate the same way as in (a), with the new level.",
  "For (d), think about what the procedure actually was. Does it matter whether the correction is applied before or after, if the choice of which result to report came from the data?"],
 "answer": "(a) 0.050, 0.226, 0.401, 0.642. (b) The family-wise error rate. (c) 0.05/20 = 0.0025 each, giving a family-wise rate of 0.0488. (d) Because the selection of which hypothesis to report was itself made using the data, so the procedure actually run was not 'test these m hypotheses' but 'report the smallest p-value', and no after-the-fact adjustment describes it.",
 "check": "Two things to be precise about. The family-wise rate is computed from the complement, and at 20 tests it is 0.642 — a study measuring twenty things and reporting the best is more likely than not to find something in pure noise. And Bonferroni is slightly conservative rather than exact: dividing by m gives 0.0488 rather than exactly 0.05, which is why it is described as controlling the rate AT or below α. For (d) the key idea is that an error rate is a property of a procedure, so the procedure has to be fixed in advance for the rate to mean anything.",
 "scenario": {
  "teaser": "A trial protocol has to name its primary outcome before the first patient is enrolled.",
  "title": "Why protocols are registered in advance",
  "body": [
   "Clinical trials are registered before they begin, and the registration names the primary outcome measure. It is not paperwork; it is the mechanism that makes the trial's eventual p-value mean what it says.",
   "A trial measuring thirty things and reporting the most favourable is running the procedure 'find something', whose false-positive rate is near certainty rather than 5%. Registering the primary outcome fixes the procedure in advance, so the stated error rate describes what was actually done.",
   "Secondary outcomes are still measured and still reported — they are simply labelled as secondary and treated as hypotheses for future work rather than as findings. That is the honest version of looking at everything.",
   "The same discipline applies well outside medicine. A quality engineer monitoring twenty characteristics on a production line will see a characteristic go out of control roughly two-thirds of the time by chance alone at α = 0.05, which is why control charts use much tighter limits than 5% — three standard deviations, about 0.0027 per chart, chosen with exactly this arithmetic in mind."],
  "q": "Why do control charts use three-standard-deviation limits rather than the two that 5% would suggest?",
  "answer": "Because a chart is examined repeatedly — every sample, every shift, across many characteristics — so the relevant error rate is not the rate per test but the rate over all those looks. Three-sigma limits give about 0.0027 per point, which keeps false alarms rare enough to be credible across thousands of points. It is the multiplicity calculation applied to a procedure that never stops running."},
 "solution": [
  {"say": "(a) Compute from the complement.",
   "math": "P(at least one rejection) = 1 − (1 − 0.05)^m\nm = 1:   1 − 0.95    = 0.050\nm = 5:   1 − 0.95⁵   = 0.226\nm = 10:  1 − 0.95¹⁰  = 0.401\nm = 20:  1 − 0.95²⁰  = 0.642",
   "why": "Independence lets the probabilities of not rejecting multiply. Note how fast it grows: by ten tests it is already more likely than not that nothing has gone wrong except chance."},
  {"say": "(b) Name it.",
   "math": "the family-wise error rate (FWER)",
   "why": "'Family' means the whole collection of tests being considered together. The per-test rate stays at 0.05 throughout; it is the rate for the family that has moved."},
  {"say": "(c) Apply Bonferroni.",
   "math": "α* = α/m = 0.05/20 = 0.0025 per test\nFWER = 1 − (1 − 0.0025)²⁰ = 0.0488",
   "why": "0.0488 is at or below the target 0.05, so the correction works. It is conservative, and with many tests it costs real power — which is the price of the protection, and the reason naming one primary outcome is usually better than correcting for thirty."},
  {"say": "(d) Identify what the real procedure was.",
   "math": "intended:  test 20 hypotheses, each at a level fixed in advance\nactual:    report whichever gave the smallest p-value\nno adjustment applied afterwards describes the second procedure",
   "why": "An error rate is a property of a decision rule, and the rule has to exist before the data for the rate to be computable. Once the data selected the hypothesis, the honest statement is that this is a hypothesis for a future sample — which is exactly what registering a primary outcome in advance avoids."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the vocabulary claims this topic's questions are built from.",
 "intro": "Decide true or false on all six before revealing any. These are the distinctions that look like common sense and are not.",
 "items": [
  {"claim": "The p-value is the probability that the null hypothesis is true.",
   "tf": False,
   "why": "False. It is the probability of a result at least as extreme as the observed one, computed ASSUMING the null is true. It is conditional on H₀, not a statement about H₀, and in this framework no probability attaches to a hypothesis at all."},
  {"claim": "Failing to reject H₀ means H₀ has been shown to be true.",
   "tf": False,
   "why": "False. It means this sample gave insufficient evidence against it. A test with low power against the effects that matter can fail to reject almost regardless of the truth, which is why a non-result should be reported with its power."},
  {"claim": "The null hypothesis always contains the equality.",
   "tf": True,
   "why": "True. H₀ is θ = θ₀, θ ≤ θ₀ or θ ≥ θ₀ — always including the boundary — because the critical value must be computed under a specified distribution. The alternative is strict."},
  {"claim": "The significance level may be chosen after the p-value is known, as long as it is stated.",
   "tf": False,
   "why": "False. α is a judgement about the cost of a false alarm and belongs to the design. Chosen afterwards it is selected to produce a conclusion, and the test's stated size becomes untrue — the real size is whatever the actual decision rule was."},
  {"claim": "A statistically significant result is necessarily of practical importance.",
   "tf": False,
   "why": "False. Significance concerns consistency with the null; importance concerns the size of the departure. With a large sample an arbitrarily small real effect becomes significant — the explore section reached power 0.71 on a fifth of a standard deviation. A confidence interval is what distinguishes the two."},
  {"claim": "Performing twenty independent tests at α = 0.05 on true nulls gives about a 64% chance of at least one rejection.",
   "tf": True,
   "why": "True: 1 − 0.95²⁰ = 0.642. The per-test rate is still 0.05; it is the family-wise rate that has grown, and it is why a primary outcome has to be named in advance or the level lowered."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 7,
 "title": "On your own — significant but unimportant",
 "objective": "Produce the situation in numbers, and show what reporting repairs it.",
 "problem": "A sample of n = 10000 from a population with σ = 1 gives a sample mean exceeding the hypothesised μ₀ by 0.02. (a) Compute the two-sided p-value for H₀: μ = μ₀. (b) Is the result significant at 5%? (c) Express the effect in standard deviation units. (d) Compute the 95% confidence interval for the difference and say what it settles.",
 "hints": [
  "For (a), the standard error is σ/√n, and with n = 10000 that is a very small number — which is the whole point.",
  "For (c), the effect in standard deviation units is just the difference divided by σ. Compare it with the usual rough description of 0.2 as a small effect.",
  "For (d), use the method from topic 4.13 with z = 1.96, and then read the interval as a statement about magnitude rather than about significance."],
 "answer": "(a) p = 0.0455. (b) Yes. (c) 0.02 standard deviations. (d) (0.0004, 0.0396) — the effect is non-zero but negligible.",
 "check": "The point of the exercise is the gap between (b) and (c): the result is significant and the effect is a fiftieth of a standard deviation, which is around a tenth of what would usually be called a small effect. Nothing is wrong with the test — the difference is real, and a correct test detected it. What is wrong is reporting only the p-value, because it cannot distinguish 'real and large' from 'real and trivial'. The interval in (d) does both jobs at once: it excludes zero, which is the significance, and it bounds the effect below 0.04, which is the importance. This is why journals increasingly require intervals rather than p-values alone.",
 "solution": [
  {"say": "(a) Compute the standard error and the statistic.",
   "math": "σ/√n = 1/√10000 = 1/100 = 0.01\nz = 0.02/0.01 = 2.00\ntwo-sided p = 2 P(Z > 2.00) = 0.0455",
   "why": "The standard error is what the large sample bought: 0.01, so a difference of 0.02 is two standard errors even though it is trivially small in the units that matter."},
  {"say": "(b) Compare with the level.",
   "math": "0.0455 < 0.05  ⟹  reject H₀ at the 5% level",
   "why": "Significant, and correctly so. The null is false and the test has found it out."},
  {"say": "(c) Express the effect on a scale that means something.",
   "math": "0.02/σ = 0.02 standard deviations",
   "why": "By any conventional reading this is negligible — a tenth of the 0.2 usually described as a small effect. The test has detected a real difference of no consequence."},
  {"say": "(d) Report the interval.",
   "math": "0.02 ± 1.96(0.01) = (0.0004, 0.0396)",
   "why": "The interval excludes zero, which is the same information as the significant test, and it also says the difference is below 0.04 — so whatever the effect is, it is small. One line carrying both facts, where the p-value carried only one."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "The mapping from situation to test",
 "objective": "Have the reference table available, read off two features of the question.",
 "blocks": [
  {"t": "step", "h": "The two features that decide everything",
   "body": "First, WHAT is being tested: a mean, a variance, a proportion, a distribution, an association. Second, the STRUCTURE of the data: one sample, two independent samples, paired observations, or a table of counts. Those two answers pick the row of the table below, and the row names the test and the assumption to check."},
  {"t": "def", "h": "Reading the table in an exam",
   "body": "Most questions in this topic give the situation in one sentence and ask for the test, or give the test and ask which assumption it needs. Both directions are covered by the same table, so it is worth being able to reproduce it rather than recognise it."},
  {"t": "step", "h": "The distinctions that are actually tested",
   "body": "Paired against two-sample is the commonest, and it is a question about independence rather than preference: two measurements on the same subject are dependent, so the paired test is required and not merely tidier. z against t is about whether σ is known, and in practice it never is. And a test on a variance is far more sensitive to non-normality than a test on a mean, which is why the same word 'normality' is a mild assumption in one row and a critical one in another."},
  {"t": "step", "h": "What falls outside this table",
   "body": "When the normality assumption fails badly and the sample is small, the distribution-free tests of topic 6 — the sign test, Wilcoxon, Mann–Whitney, Kruskal–Wallis — are the alternatives, and a question offering one of those as the answer is usually signalling 'small sample, clearly non-normal'. The chi-square tests of topics 4.14 and 4.16 handle counts and tables, and the degrees-of-freedom counting for both comes from topic 4.10."}],
 "table": {
  "caption": "Situation to test. The last column is what step 2 of the procedure has to check for that row.",
  "head": ["What is tested", "Data structure", "Test", "Assumption to check"],
  "rows": [
   ["A mean, σ known", "one sample", "z test", "normality, or n large enough for the CLT"],
   ["A mean, σ unknown", "one sample", "t test, n − 1 df", "normality, or n large; independence"],
   ["Two means, equal variances", "two independent samples", "pooled t test, n₁ + n₂ − 2 df", "normality; equal variances; independence"],
   ["Two means, before and after", "paired observations", "paired t test on differences, n − 1 df", "differences roughly normal; pairs independent"],
   ["A variance", "one sample", "chi-square, (n − 1)s²/σ₀²", "normality — critically, not approximately"],
   ["Ratio of two variances", "two independent samples", "F test", "normality in both; independence"],
   ["A proportion", "one sample of counts", "z test on p̂, or exact binomial", "np and n(1 − p) both reasonably large"],
   ["A whole distribution", "counts in k categories", "chi-square goodness of fit, k − 1 df", "expected counts adequate, commonly ≥ 5"],
   ["Association", "two-way table of counts", "chi-square for independence, (r−1)(c−1) df", "expected counts adequate; independent observations"]]},
 "ask": {
  "q": "Two rows of the table list normality as the assumption, but the lesson calls it mild in one and critical in the other. Which rows, and what makes the difference?",
  "nudge": "One statistic is a sample mean, which the central limit theorem protects. What does the other one depend on?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the numbers and the two mappings that get asked.",
 "intro": "Answer, then reveal.",
 "items": [
  {"q": "Twenty independent tests, all nulls true, α = 0.05. Chance of at least one rejection?",
   "a": "1 − 0.95²⁰ = 0.642. The family-wise error rate, against a per-test rate still at 0.05."},
  {"q": "What level does Bonferroni give each of 20 tests, and what family-wise rate results?",
   "a": "0.05/20 = 0.0025, giving a family-wise rate of 0.0488 — at or below the target, so slightly conservative."},
  {"q": "Before-and-after measurements on the same subjects. Which test, and why not the two-sample one?",
   "a": "The paired t test on the differences. The two measurements on a subject are not independent, so the two-sample test's assumption fails."},
  {"q": "Which of the standard tests is most sensitive to non-normality?",
   "a": "The chi-square test on a variance, and the F test on a ratio of variances. Tests on means are protected by the central limit theorem; tests on variances are not."},
  {"q": "Counts in k categories against claimed probabilities. Degrees of freedom?",
   "a": "k − 1, because the probabilities sum to one. Expected counts should be adequate, commonly taken as at least 5."},
  {"q": "How should the choice between one and two tails be made?",
   "a": "On subject-matter grounds, before seeing the data. Choosing after seeing the direction doubles the real size of the test."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Give the five steps in order and justify the ordering — the hypothesis selects the test, and the test selects the assumptions.",
  "State the p-value correctly, and reject the readings that make it a probability about the hypothesis.",
  "Say what failing to reject does and does not establish, and why 'accept H₀' is the wrong phrase.",
  "Name the rules that keep a stated error rate true: α fixed in advance, the tail chosen on subject-matter grounds, the critical region independent of the observed value.",
  "Compute a family-wise error rate for m tests, apply the Bonferroni correction, and explain why no after-the-fact adjustment repairs a result selected by the data.",
  "Distinguish significance from importance, produce a case where they come apart, and give the confidence interval as the remedy.",
  "Read a situation and name the test, from what is being tested and the structure of the data, together with the assumption that test requires."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "Which assumptions actually matter",
 "objective": "See that 'check the assumptions' is not one instruction but several, with very different stakes.",
 "blocks": [
  {"t": "step", "h": "Robustness is not uniform",
   "body": "Step 2 of the procedure says 'check the assumptions', which sounds like a single chore. It is not. Some assumptions can be violated substantially with almost no effect on the test's real size; others cannot be violated at all without the stated size becoming meaningless. Knowing which is which is what separates following a procedure from understanding it."},
  {"t": "def", "h": "Normality, for a test on a mean",
   "body": "Mild. The t statistic depends on the data through x̄ and s, and the central limit theorem makes x̄ close to normal for moderate n almost regardless of the population shape. For n of thirty or more and a population without extreme skew, the t test's real size stays close to its nominal level. Serious skew or heavy tails with a small sample is where it starts to matter."},
  {"t": "def", "h": "Normality, for a test on a variance",
   "body": "Critical. The statistic (n − 1)s²/σ₀² depends on the fourth moment of the population, and no central limit theorem rescues it. For a heavy-tailed population the real size of a nominal 5% test can be several times 5%. The same applies to the F test on a ratio of variances. This is the sharpest instance of the same word meaning two very different things in two rows of the table."},
  {"t": "def", "h": "Independence, everywhere",
   "body": "Never negotiable. Every variance formula in the syllabus assumes it, and dependence does not merely perturb the size — it can make the standard error wrong by a large factor, usually too small, so the test rejects far too often. This is why the paired design has its own test rather than being handled by the two-sample one, and why time-ordered data needs the methods of module 5 rather than these."},
  {"t": "step", "h": "Equal variances, and the practical order of checks",
   "body": "For the pooled two-sample t test, unequal variances matter little when the two sample sizes are similar and a great deal when they are not; the Welch version avoids the assumption and costs almost nothing, which is why much software uses it by default. So a sensible priority for step 2: independence first, because nothing survives its failure; then the assumption specific to the statistic — normality if it is a variance or ratio test, expected counts if it is a chi-square on counts; and normality of a mean last, since it is the one the central limit theorem is most likely to have taken care of."}],
 "ask": {
  "q": "A question gives a sample of 8 clearly skewed observations and asks for a test on the mean. What is the defensible answer?",
  "nudge": "The central limit theorem needs a moderate n to help. With eight observations and visible skew, which family of tests makes no normality assumption at all?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "inference_t15_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "inferencet15",
 "topicId": "inference-t15",
 "moduleId": "inference",
 "title": "Choosing the Right Test",
 "breadcrumb": "Statistical Inference → Testing of Hypotheses → Choosing and running a test",
 "engine": "C",
 "engineName": "Testing — the procedure, its vocabulary, and which test belongs where",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Give the five steps of a hypothesis test in order and justify the ordering.",
  "State the p-value correctly and reject the standard misreadings of it.",
  "Say what failing to reject H₀ does and does not establish.",
  "Name the requirements that keep a stated error rate true, including when α and the choice of tail are fixed.",
  "Compute a family-wise error rate, apply the Bonferroni correction, and say why selection by the data cannot be corrected afterwards.",
  "Distinguish statistical significance from practical importance and give the remedy.",
  "Read a situation and name the appropriate test together with the assumption it requires."],
 "prereq": [
  {"id": "p1", "name": "Size and power of a test",
   "why": "This topic's whole subject is keeping a stated error rate honest, which is topic 4.12's α and β. The significance-versus-importance section is a power calculation in disguise."},
  {"id": "p2", "name": "Confidence intervals and pivots",
   "why": "The remedy for reporting a p-value alone is to report an interval, and two rows of the decision table use the pivots from topic 4.13 as test statistics."},
  {"id": "p3", "name": "Neyman–Pearson, MLR and UMP tests",
   "why": "The choice between one and two tails is the choice between a one-sided and a two-sided alternative, and what each buys is topic 4.9's and 4.17's material."},
  {"id": "p4", "name": "Sampling distributions of the mean and variance",
   "why": "Every row of the decision table rests on knowing the null distribution of its statistic, and the robustness discussion rests on which of them the central limit theorem protects."}],
 "traps": [
  "The hypothesis comes BEFORE the assumption check — the test determines which assumptions matter.",
  "You cannot compare with tabulated values before computing the statistic.",
  "The p-value is computed assuming H₀, and is not the probability that H₀ is true.",
  "Failing to reject is not accepting; 'accept H₀' is the wrong phrase.",
  "α and the choice of tail are fixed before the data, never after.",
  "The critical region depends on the null distribution and α, not on the observed statistic.",
  "Significance is about consistency with H₀; importance is about magnitude. A large n makes any real effect significant.",
  "Paired data requires the paired test — independence fails, so this is an error and not a preference.",
  "Normality is mild for a test on a mean and critical for a test on a variance."],
 "revision": {
  "sheet": [
   "The five steps: form the hypotheses (and fix α) → check the chosen test's assumptions → compute the statistic → compare with the critical value or find the p-value → state the inference in words.",
   "June 2026 Q43 answer: C, A, B, D, E. The discriminator is that the hypothesis precedes the assumption check.",
   "Why: different tests need different assumptions, so there is no list to check until the test is known.",
   "α is a judgement about the cost of a false alarm and belongs to the design, not to the sample.",
   "The null always contains the equality — θ = θ₀, θ ≤ θ₀ or θ ≥ θ₀ — because a critical value needs a specified distribution.",
   "The critical region is fixed by the null distribution, α and the direction of H₁; never by the observed value.",
   "Reject H₀ ⟺ the statistic is in the critical region ⟺ p-value ≤ α.",
   "p-value: the probability, under H₀, of a result at least as extreme as the one observed. Not P(H₀ true).",
   "Failing to reject means insufficient evidence, not proof of H₀. Report the power alongside a non-result.",
   "One tail or two is decided by subject matter, in advance. Choosing after seeing the direction doubles the real size.",
   "Family-wise error rate for m independent tests at α: 1 − (1 − α)^m. At α = 0.05 that is 0.226 for 5, 0.401 for 10, 0.642 for 20.",
   "Bonferroni: use α/m per test. At m = 20 that is 0.0025 each, giving a family-wise rate of 0.0488.",
   "No after-the-fact correction repairs a result the data selected; the procedure must be fixed in advance.",
   "Significance ≠ importance. n = 10000, difference 0.02, σ = 1 gives p = 0.0455 for an effect of 0.02 standard deviations. Report the interval: (0.0004, 0.0396).",
   "Decision table: mean with σ known → z; mean with σ unknown → t on n − 1; two independent means with equal variances → pooled t on n₁ + n₂ − 2; before-and-after → paired t on differences; a variance → chi-square on (n − 1)s²/σ₀²; ratio of variances → F; a proportion → z on p̂ or exact binomial; a distribution over k categories → chi-square goodness of fit on k − 1; a two-way table → chi-square for independence on (r − 1)(c − 1).",
   "Robustness: normality is mild for a mean (CLT), critical for a variance or a variance ratio. Independence is never negotiable. Unequal variances matter most when the sample sizes differ.",
   "Small sample plus clear non-normality points to the distribution-free tests rather than to the t test."],
  "cards": [
   ["The five steps", "Hypothesis and α → assumptions → statistic → comparison → inference in words"],
   ["Why hypothesis before assumptions", "The test determines which assumptions matter, so there is no list until the test is chosen"],
   ["The p-value", "P(result at least as extreme | H₀ true) — conditional on H₀, never a probability about H₀"],
   ["Failing to reject", "Insufficient evidence against H₀, not proof of it; report the power with a non-result"],
   ["What the null always contains", "The equality, because the critical value needs a specified distribution"],
   ["When α is fixed", "In the design, before any data. Fixed afterwards, the stated size is untrue"],
   ["One tail or two", "Decided by subject matter in advance; choosing after seeing the direction doubles the real size"],
   ["Family-wise error rate", "1 − (1 − α)^m — 0.226 at 5 tests, 0.642 at 20, with α = 0.05"],
   ["Bonferroni", "Use α/m per test; at m = 20 that is 0.0025, giving a family-wise rate of 0.0488"],
   ["Significance vs importance", "Significance is consistency with H₀; importance is magnitude. A large n makes any real effect significant"],
   ["Paired versus two-sample", "Repeated measurements on one subject are dependent, so the paired test is required, not preferred"],
   ["Where normality really matters", "Mild for a mean, thanks to the CLT; critical for a variance or an F ratio, which have no such protection"]],
  "tricks": [
   "On a sequencing question, fix the two ends first — hypothesis first, inference last — then settle the contested pair by asking what each step needs from the one before it.",
   "Discard any option that has the comparison before the calculation; such an option exists to be eliminated quickly.",
   "Read the question for two things only: what is being tested, and the structure of the data. Those two pick the test.",
   "The words 'before and after' or 'the same subjects' mean paired, every time.",
   "If a stem mentions a large sample and a tiny difference, the question is about significance versus importance."],
  "shortcuts": [
   "σ unknown means t, and σ is unknown in every real problem — so t unless the question explicitly says σ is known.",
   "1 − 0.95^m is worth being able to evaluate quickly: roughly 0.05m for small m, and the approximation is good to about 10% up to m = 5.",
   "Counting degrees of freedom for counts: k − 1 for a goodness-of-fit over k categories, (r − 1)(c − 1) for an r by c table."],
  "remember": [
   "Hypothesis first, then assumptions. Compute before comparing.",
   "Fail to reject, never accept.",
   "A significant result still needs an interval before anyone should act on it."]},
 "howto": "This lesson has almost no algebra, which makes it the easiest one to skim and one of the easier ones to lose marks on. Read the opening four checks properly — in this topic the vocabulary IS the content, and the questions turn on distinctions like significance against importance that look like common sense until you are asked. Section 4 is June 2026 Q43 reasoned out rather than recalled, and the reasoning is what transfers. Section 11 holds the decision table; it is the thing to revise from, and it is worth being able to write out rather than recognise. Sections 8 and 10 put numbers on the two failures of practice that this topic asks about most. Attempt the question at the end of each section before opening the answer. The optional section at the end explains which assumptions actually matter, which turns step 2 of the procedure from a chore into a judgement.",
 "refs": [
  {"title": "Applied Statistics — Hypothesis Testing",
   "where": "Lesson 6, sections 6a.1 to 6a.4", "site": "Penn State STAT 500",
   "url": "https://online.stat.psu.edu/stat500/", "type": "Course notes", "free": True,
   "checked": "2026-10-31",
   "why": "The procedure set out step by step with the vocabulary used carefully, including the distinction between failing to reject and accepting. The right companion to sections 3 and 7."},
  {"title": "Statistical Inference", "where": "Weeks on testing of hypotheses",
   "site": "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee",
   "url": "https://archive.nptel.ac.in/noc/courses/noc21/SEM1/noc21-ma23", "type": "Video course",
   "free": True, "checked": "2026-10-30",
   "why": "Indian syllabus phrasing for the steps of a test and for the standard tests, which is the wording NET questions use."},
  {"title": "Mathematical Statistics 18.655 — lecture notes",
   "where": "Sessions on testing", "site": "MIT OpenCourseWare",
   "url": "https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type": "Lecture notes", "free": True, "checked": "2026-10-30",
   "why": "The formal statements behind the practical rules in section 7, for anyone who wants to see why the procedure has to be fixed in advance."},
  {"title": "Statistical Inference, 2nd edition", "where": "Sections 8.1 and 8.3.4",
   "site": "Casella and Berger", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "p-values defined properly, and the relationship between the critical-region and p-value formulations of a test."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapters 9–11",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "The standard tests of the decision table, each with its assumptions stated — useful for checking a row you are unsure of."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored October 2026 for this platform against the UGC NET Statistics syllabus, and prioritised from the June 2026 paper, where Q43 gave the five steps of a hypothesis test out of order; the official answer is C, A, B, D, E and the stored response sheet shows option A was marked, which places assumption-checking before the hypothesis is stated. That ordering error is the subject of sections 3 and 4. The ten practice variants on that question — the first step, what the null always contains, the p-value, when H₀ is rejected, when α is fixed, what failing to reject means, significance against practical importance, the effect of many tests at α = 0.05, what determines the critical region, and how to choose between one and two tails — are each taught in a named section and each appear in the pool. This is a synthesis lesson whose prerequisites are topics 4.12, 4.10, 4.13 and 4.17. Every numerical value was computed rather than recalled: the family-wise error rates 0.050, 0.226, 0.401 and 0.642, the Bonferroni levels 0.01 and 0.0025 with their achieved rates 0.0490 and 0.0488, the power figures 0.107, 0.199, 0.352 and 0.707 for a 0.2 standard deviation effect at n = 4, 16, 40 and 120, and the significance-without-importance case giving p = 0.0455 with interval (0.0004, 0.0396). Previous-year questions themselves are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "inf-t15-m-%02d" % i, "format": fmt, "topic": "inference-t15",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "order", "easy",
 "For testing a hypothesis the different steps are given below. Arrange them in proper sequence.",
 ["A, C, B, D", "C, A, B, D", "A, C, D, B", "C, A, D, B"],
 "B",
 "The hypothesis must be formed first, because it determines which test is relevant and therefore which assumptions need checking. The statistic must be computed before it can be compared with a tabulated value. This is June 2026 Q43, whose answer placed the hypothesis ahead of the assumption check.",
 items=["A. Checking the assumptions of the test",
        "B. Calculation of the test statistic",
        "C. Formation of hypothesis",
        "D. Comparing with the tabulated values"]))

I.append(q(2, "single", "easy",
 "The first step in testing a hypothesis is:",
 ["checking the assumptions of the test", "formulating the null and alternative hypotheses",
  "computing the test statistic", "choosing the tabulated value"],
 "B",
 "The hypothesis comes first because everything downstream depends on it: it selects the test, and the test selects the assumptions to be checked. Beginning with the assumptions means checking requirements without yet knowing whose requirements they are."))

I.append(q(3, "single", "easy",
 "The null hypothesis always contains:",
 ["a strict inequality", "the equality", "the sample mean", "the significance level"],
 "B",
 "H₀ takes the form θ = θ₀, θ ≤ θ₀ or θ ≥ θ₀ — always including the boundary value. The reason is operational: a critical value has to be computed under a specified distribution, and only a hypothesis that pins the parameter down at least at a boundary provides one. The alternative carries the strict inequality."))

I.append(q(4, "single", "easy",
 "The p-value is:",
 ["the probability that H₀ is true",
  "the probability, computed under H₀, of a result at least as extreme as that observed",
  "the probability that the result arose by chance",
  "the significance level of the test"],
 "B",
 "The p-value is conditional on H₀ being true; it is a statement about the data given the hypothesis, never about the hypothesis given the data. In this framework no probability attaches to a hypothesis at all, which rules out the first option, and the third is a loose restatement of the same error."))

I.append(q(5, "single", "easy",
 "The significance level α should be fixed:",
 ["after computing the p-value", "before examining the data",
  "after checking the assumptions", "so that H₀ is rejected"],
 "B",
 "α is a judgement about how often a false alarm is acceptable, which depends on the consequences and not on the particular sample. Chosen after the p-value is known it is selected to produce a conclusion, and the test's stated size becomes untrue — the real size is whatever the actual decision rule was."))

I.append(q(6, "single", "easy",
 "'Failing to reject H₀' means:",
 ["H₀ has been proved true", "this sample gave insufficient evidence against H₀",
  "the test was invalid", "the p-value was exactly α"],
 "B",
 "A test controls the false-alarm rate; it is not built to establish the null. A test with little power against the effects that matter can fail to reject almost regardless of the truth, which is why the careful phrase is 'fail to reject' and why 'accept H₀' is treated as an error."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "Five independent tests are each carried out at α = 0.05, and all five null hypotheses are in fact true. The probability that at least one is rejected is:",
 ["0.050", "0.226", "0.250", "0.400"],
 "B",
 "The tests are independent, so the probability that none is rejected is 0.95⁵ = 0.774, and the complement is 0.226. Option C is the rough approximation 5 × 0.05 without the complement, and option D is the value for ten tests.",
 check="Compute from the complement: 1 − (1 − α)^m. The answer must exceed 0.05 and fall short of 5 × 0.05 = 0.25."))

I.append(q(8, "numeric", "moderate",
 "Twenty independent tests are each carried out at α = 0.05 on true null hypotheses. The probability that at least one is rejected is closest to:",
 ["0.05", "0.26", "0.64", "1.00"],
 "C",
 "1 − 0.95²⁰ = 0.642. A study measuring twenty things and reporting the best is more likely than not to find a 'significant' result in pure noise, which is why a primary outcome must be named in advance or the level lowered.",
 check="The per-test rate stays at 0.05; it is the family-wise rate that grows. The answer must be below 1 but well above 0.5 at twenty tests."))

I.append(q(9, "single", "moderate",
 "Performing many tests each at α = 0.05 causes:",
 ["the power of each test to fall", "the family-wise error rate to exceed 0.05",
  "the p-values to become invalid individually", "the null hypotheses to become dependent"],
 "B",
 "Each individual test still has size 0.05 and each p-value is still correct for its own test, so the third option is wrong. What grows is the probability of at least one false rejection across the family — 0.226 at five tests and 0.642 at twenty. The power of each test is unaffected unless the level is lowered to compensate."))

I.append(q(10, "numeric", "moderate",
 "Twenty tests are to be performed with a family-wise error rate of at most 0.05. The Bonferroni correction sets each test's level at:",
 ["0.05", "0.025", "0.0025", "0.001"],
 "C",
 "Bonferroni divides the overall level by the number of tests: 0.05/20 = 0.0025. The resulting family-wise rate is 1 − (1 − 0.0025)²⁰ = 0.0488, at or just below the target, so the correction is slightly conservative.",
 check="Divide the overall level by the number of tests, not by two. Check the result by computing 1 − (1 − α*)^m and confirming it does not exceed 0.05."))

I.append(q(11, "single", "moderate",
 "The critical region of a test is determined by:",
 ["the observed value of the test statistic",
  "the null distribution of the statistic, the level α and the direction of H₁",
  "the p-value", "the sample mean and variance"],
 "B",
 "All three ingredients are settled before the data are seen, which is precisely what makes the stated error rate meaningful. A critical region that depended on the observed value would be a decision rule chosen after the fact, with an unknown real size."))

I.append(q(12, "multi", "moderate",
 "A study reports p = 0.001 for a difference of 0.02 units, from a sample of n = 10000 with σ = 1. Which statements are correct?",
 ["A and C only", "A, B and C only", "B and D only", "C and D only"],
 "A",
 "A is true — the difference is real and a correct test detected it. B is false: significance concerns consistency with the null, not magnitude, and 0.02 of a standard deviation is negligible by any convention. C is true, and it is the standard remedy. D is false — the test is working exactly as designed; what is inadequate is reporting the p-value alone.",
 statements=["The result is statistically significant at any conventional level.",
             "The result shows the difference is large enough to act on.",
             "Reporting a confidence interval would settle whether the difference matters.",
             "The test is invalid because the sample is too large."],
 verdicts=verd(
  (True, "True. With a standard error of 0.01 the difference is two standard errors or more, so the data are inconsistent with the null."),
  (False, "False. Significance says the departure is real, not that it is big. An effect of 0.02 standard deviations is about a tenth of what is conventionally called small."),
  (True, "True. The interval (0.0004, 0.0396) excludes zero, which is the significance, and bounds the effect below 0.04, which is the importance — both facts in one line."),
  (False, "False. A large sample makes a test more sensitive, not invalid. The problem is in the reporting, not in the test."))))

I.append(q(13, "single", "moderate",
 "A result can be statistically significant but practically unimportant when:",
 ["the significance level is too high", "the sample size is very large and the true effect very small",
  "the test is one-tailed", "the assumptions are violated"],
 "B",
 "The standard error shrinks like 1/√n, so with enough data an arbitrarily small real effect produces a large test statistic. The effect is genuine and the test is correct; what is missing from a p-value alone is the magnitude, which is why a confidence interval should accompany it."))

I.append(q(14, "single", "moderate",
 "Choosing between a one-tailed and a two-tailed test should be based on:",
 ["the direction in which the sample mean fell", "subject-matter reasoning settled before the data are seen",
  "whichever gives the smaller p-value", "the sample size"],
 "B",
 "A one-tailed test is justified when the subject matter rules out one direction or when only one direction would prompt action. Choosing the tail after seeing which way the data went means you were prepared to reject in either tail at α, so the real size is about 2α and the stated level is untrue."))

I.append(q(15, "single", "moderate",
 "The same subjects are measured before and after an intervention. The appropriate test is:",
 ["the two-sample t test with pooled variance", "the paired t test on the differences",
  "the F test for equality of variances", "the chi-square goodness-of-fit test"],
 "B",
 "Two measurements on the same subject are not independent, and the two-sample test assumes independent samples. Reducing each pair to its difference restores independence and turns the problem into a one-sample t test on the differences, with n − 1 degrees of freedom. This is a requirement rather than a preference."))

I.append(q(16, "single", "moderate",
 "H₀ is rejected when:",
 ["the p-value exceeds α", "the p-value is less than or equal to α",
  "the test statistic equals its expected value", "the confidence interval contains the null value"],
 "B",
 "A small p-value means the observed result would be surprising if H₀ held, so rejection happens when the p-value is at or below the level. This is equivalent to the statistic falling in the critical region, and also equivalent to the corresponding confidence interval EXCLUDING the null value — which makes the fourth option the condition for not rejecting."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the assumptions required by the standard tests of the normal family.",
 ["A, B and D only", "A and C only", "B and D only", "A, B and C only"],
 "A",
 "A is true — the central limit theorem makes x̄ close to normal for moderate n, so the t test's real size stays near its nominal level under mild departures. B is true, and it is the sharpest contrast in the topic: the variance statistic depends on the fourth moment and has no such protection. C is false — dependence can make the standard error badly wrong, usually too small, so the test rejects far too often. D is true, which is why the Welch version is often preferred.",
 statements=["A test on a mean is fairly robust to non-normality when n is moderate.",
             "A test on a variance is highly sensitive to non-normality.",
             "A modest failure of independence has little effect on a test's real size.",
             "Unequal variances matter more for a pooled two-sample t test when the sample sizes differ."],
 verdicts=verd(
  (True, "True. The statistic depends on the data through x̄, which the central limit theorem pushes towards normality regardless of population shape."),
  (True, "True. The statistic (n − 1)s²/σ₀² depends on the fourth moment and no central limit theorem rescues it; for heavy-tailed populations the real size of a nominal 5% test can be several times 5%."),
  (False, "False. Independence underlies every variance formula in the syllabus. Dependence typically makes the standard error too small, so the test rejects far more often than its stated level."),
  (True, "True. With similar sample sizes the pooled test is fairly robust to unequal variances; with very different sizes it is not, which is why the Welch version is often used by default."))))

I.append(q(18, "numeric", "hard",
 "A sample of n = 10000 from a population with σ = 1 gives a sample mean exceeding μ₀ by 0.02. The two-sided p-value for H₀: μ = μ₀ is approximately:",
 ["0.0455", "0.3173", "0.0228", "0.5000"],
 "A",
 "The standard error is 1/√10000 = 0.01, so z = 0.02/0.01 = 2.00 and the two-sided p-value is 2 P(Z > 2.00) = 0.0455. Option C is the one-sided value, and option B uses z = 1 by dividing by σ rather than by the standard error. The effect is 0.02 standard deviations — significant and negligible at the same time.",
 check="The standard error is σ/√n = 0.01, not σ = 1. A two-sided p-value is twice the one-sided tail."))

I.append(q(19, "single", "hard",
 "A researcher tests five outcomes at α = 0.05, finds one significant at p = 0.03, and reports only that outcome. Applying the Bonferroni correction afterwards would:",
 ["make the reported result valid, since 0.03 > 0.01 means it is no longer claimed",
  "not repair the problem, because the choice of which outcome to report was itself made using the data",
  "be unnecessary, since each test had the correct size",
  "require the level to be raised rather than lowered"],
 "B",
 "An error rate is a property of a decision rule, and the rule has to be fixed before the data for the rate to be computable. The procedure actually run was 'report the smallest p-value among five', and no adjustment applied after the fact describes that procedure. The correction is useful only when planned in advance; the honest alternative here is to treat the finding as a hypothesis for a future sample."))

I.append(q(20, "single", "hard",
 "A question gives eight observations that are clearly skewed and asks for a test on the population mean. The most defensible choice is:",
 ["the one-sample t test, since it is robust to non-normality",
  "a distribution-free test such as the sign or Wilcoxon signed-rank test",
  "the chi-square test on the variance", "the z test, since σ can be estimated by s"],
 "B",
 "The t test's robustness comes from the central limit theorem acting on x̄, and with eight observations and visible skew there is not enough sample for that protection. A distribution-free test makes no normality assumption and is the standard answer to 'small sample, clearly non-normal'. The variance test would be testing the wrong parameter and is the most normality-sensitive test available, and substituting s into a z test is simply the t test with the wrong reference distribution."))

# A pool whose keys pile onto one letter rewards a guesser, and the validator caps any
# letter at 40%. Swapping positions i and j is its own inverse, so an "option X" mention
# inside an explanation just swaps the same two letters.
LET = "ABCD"
WANT = {"inf-t15-m-02": "C", "inf-t15-m-03": "D", "inf-t15-m-04": "A",
        "inf-t15-m-05": "D", "inf-t15-m-06": "C", "inf-t15-m-09": "D",
        "inf-t15-m-11": "A", "inf-t15-m-13": "C", "inf-t15-m-15": "D",
        "inf-t15-m-16": "A", "inf-t15-m-20": "C"}

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
 "moduleId": "inference", "topicId": "inference-t15", "source": "mastery",
 "label": "Choosing the right test — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
