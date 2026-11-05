#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author lesson 4.10 — Likelihood ratio test and Wilks (topic inference-t10).

Built on PYQ evidence. June 2026 Q30 asked which of four statements about the LR statistic
are true (answer: λ = sup over Θ₀ / sup over Θ, and the test is a function of sufficient
statistics; the false pair being 0 < λ < ∞ and −2 log λ ~ N(0,1)). The nine genuine practice
variants on that question ask, between them: the range of λ, the direction of rejection,
what λ = 1 means, the data entering only through sufficient statistics, invariance under
reparameterisation, df from the number of restrictions, the σ² unknown case reducing to the
t-test, the σ² = σ₀² case reducing to a region on Σ(xᵢ − x̄)², and the simple-versus-simple
case coinciding with Neyman–Pearson. All nine are taught here and all nine are in the pool.

Writes seed/lesson_t10.json and seed/inference_t10_mastery.json.
Run: python3 lesson_t10.py
"""
import json, io, os, re

OUT = "seed/lesson_t10.json"
POOL = "seed/inference_t10_mastery.json"

S = []

S.append({
 "kind": "foundation", "id": "s0", "mins": 6,
 "title": "Before the lesson — four things it will assume",
 "objective": "Get back the likelihood, the MLE and the chi-square tail, because the whole topic is those three things put in a ratio.",
 "ask": {
  "q": "Three of the four checks below are about finding a maximum. Which one is not, and why does this topic need it?",
  "nudge": "The test compares two maxima and then has to turn the comparison into a probability. One of the four checks is about that last step."},
 "body": [
  "This topic has one idea and it is worth saying before any symbols. Ask the question: how well can the data be explained if the null hypothesis is true, compared with how well it can be explained if we allow anything at all? If the restriction costs almost nothing, keep it. If it costs a lot, reject it.",
  "That comparison is a ratio of two maximised likelihoods, and everything in the lesson is either computing that ratio or working out what distribution it has.",
  "Four checks. The first three are about maximising a likelihood, which you have done before. The fourth is the chi-square tail, which is how the answer gets turned into a decision."],
 "items": [
  {"ask": "Write the likelihood for an iid sample x₁,…,xₙ from N(μ, σ²) with σ² known, and say what value of μ maximises it.",
   "recall": "L(μ) = (2πσ²)^(−n/2) exp(−Σ(xᵢ − μ)²/(2σ²)), maximised at μ̂ = x̄.",
   "refresh": [
    "Only the exponent involves μ, and it is largest when Σ(xᵢ − μ)² is smallest. The sample mean is what minimises a sum of squared deviations, so μ̂ = x̄ without any calculus.",
    "Hold on to the identity Σ(xᵢ − μ₀)² = Σ(xᵢ − x̄)² + n(x̄ − μ₀)². It is what makes the whole first worked example collapse to one line, and it turns up again in the σ² unknown case.",
    "The phrase 'maximised likelihood' is what the whole topic rests on: you will be computing it twice, once with the null's restriction imposed and once without."]},
  {"ask": "What does 'sup' mean in sup L(θ) over θ in Θ₀, and how does it differ from max?",
   "recall": "It is the largest value the likelihood reaches as θ ranges over the set Θ₀. In every NET question it is attained at a point, so you may read it as 'maximise over that set'.",
   "refresh": [
    "Supremum is the careful word for a largest value that may be approached rather than attained. In this syllabus the maximum is always reached, so nothing is lost by reading sup as max.",
    "What matters is the SET you maximise over. Over Θ₀ you are forced to respect the null hypothesis. Over Θ you may use any parameter value at all.",
    "Because Θ₀ sits inside Θ, the second maximum can never be smaller than the first. That one observation fixes the range of the statistic, and it is the most commonly asked fact about it."]},
  {"ask": "For an iid N(μ, σ²) sample with BOTH parameters unknown, what are the two maximum likelihood estimates?",
   "recall": "μ̂ = x̄ and σ̂² = Σ(xᵢ − x̄)²/n — note the divisor n, not n − 1.",
   "refresh": [
    "The MLE of the variance divides by n. The unbiased estimator s² divides by n − 1. Both are correct answers to different questions, and this topic needs the MLE.",
    "Mixing them up changes the value of the test statistic, which is exactly why the wrong value tends to be sitting among the four options.",
    "You will need both estimates in the σ² unknown case, where the null restricts μ and leaves σ² free to be re-estimated."]},
  {"ask": "If a statistic has a chi-square distribution with 3 degrees of freedom, what value does it exceed 5% of the time?",
   "recall": "7.815. The upper 5% points worth memorising are 3.841 for 1 df, 5.991 for 2, 7.815 for 3 and 9.488 for 4.",
   "refresh": [
    "The chi-square distribution is the one that appears at the end of this topic, because of the theorem in section 7. Its upper tail is where the decision is made.",
    "Those four numbers cover almost every question that gets asked, since the degrees of freedom in a NET question are rarely more than four.",
    "Notice that the critical value grows with the degrees of freedom. More restrictions being tested means more room for the statistic to be large by chance, so more is demanded before you reject."]}]})

S.append({
 "kind": "intuition", "id": "s1", "mins": 7,
 "title": "What a restriction costs",
 "objective": "See the test as a price comparison — the price the null's restriction charges in explanatory power — before any formula.",
 "body": [
  "Every hypothesis test in this topic is the same question in different clothing: you have a model with some freedom in it, the null hypothesis takes some of that freedom away, and you want to know whether the data minds.",
  "The natural way to measure 'minds' is to fit the model twice. Once with the restriction, once without. The unrestricted fit can never be worse — it has every option the restricted fit had, and more. So the question is only ever how much better it is.",
  "If the unrestricted fit is barely better, the restriction cost nothing and there is no case against it. If it is much better, the restriction was doing real damage, and that is evidence against the null.",
  "The ratio of the two fits is the statistic. The rest of the lesson is arithmetic and one theorem about its distribution."],
 "scenario": {
  "teaser": "A tyre plant has two moulding lines and a claim that they are identical.",
  "title": "Two lines, one claim",
  "body": [
   "A tyre plant runs two moulding lines. The plant manager asserts they produce the same mean tread depth; the quality engineer suspects line B drifts. They sample from both.",
   "The engineer can describe the data in two ways. The free description allows each line its own mean — two numbers to estimate. The manager's description forces one common mean — one number. The manager's claim is exactly the statement that the free description's extra parameter is unnecessary.",
   "Fit both. The free fit will match the data at least as well, always, because setting both its means equal is one of the options available to it. So the comparison can only run one way, and the size of the gap is the whole evidence.",
   "What is worth noticing is how general this is. Nothing in the reasoning mentioned tyres, or means, or the normal distribution. Any null hypothesis that can be written as a restriction on a parameter — one mean equals another, a variance equals a stated number, three proportions are all equal — can be tested this way. That generality is why this test exists: the Neyman–Pearson lemma handles one simple hypothesis against another, and almost nothing real looks like that.",
   "The price of the generality is that the ratio's distribution is usually unknown exactly. That is what the theorem in section 7 is for, and it is why the answer is approximate and improves with sample size."],
  "q": "Why can the unrestricted fit never be worse than the restricted one?",
  "answer": "Because the restricted model's parameter set sits inside the unrestricted model's. Every parameter value the restricted fit could choose is still available to the unrestricted fit, so the best it can do is at least as good. This is why the ratio of restricted to unrestricted maximised likelihood can never exceed 1 — the single most-asked fact about the statistic."},
 "ask": {
  "q": "The scenario says the comparison 'can only run one way'. What would it mean if you computed the ratio and got a value above 1?",
  "nudge": "It would not mean the null fits better than the alternative. It would mean one of the two maximisations was done wrong — which one is easier to get wrong?"}})

S.append({
 "kind": "explore", "id": "s2", "mins": 7,
 "title": "The chi-square tail, where the decision gets made",
 "objective": "See how the degrees of freedom and the critical value move together, so the theorem in section 7 has somewhere to land.",
 "viz": {"type": "chisq-tail", "k": 1, "alpha": 0.05, "obs": 3.0},
 "body": [
  "This is the distribution the statistic ends up being compared against. The curve is the chi-square density, the shaded right tail is α, the line at its edge is the critical value, and the marker is the observed statistic.",
  "Start at 1 degree of freedom, which is the case for a null that fixes a single parameter. The critical value is 3.841. Slide the observed statistic across it and watch the p-value cross 0.05 at exactly that point.",
  "Now raise the degrees of freedom. The whole distribution shifts right and the critical value grows — 5.991 at 2, 7.815 at 3, 9.488 at 4. The reason is worth saying in words: each extra restriction being tested gives the statistic another way to be large purely by chance, so more is required before you call it evidence.",
  "This is the trap the exam uses. A statistic of 7.0 is significant at 5% with 1 or 2 degrees of freedom and not significant with 3. Getting the degrees of freedom wrong changes the answer even when the arithmetic is perfect, which is why section 8 is entirely about counting them.",
  "One more thing to try. Set the degrees of freedom to 1 and compare the critical value 3.841 with 1.96², which is 3.8416. That is not a coincidence, and the next section shows why."],
 "ask": {
  "q": "Why should the chi-square critical value at 1 degree of freedom be the square of the normal critical value 1.96?",
  "nudge": "A chi-square variable with 1 degree of freedom is the square of what?"}})

S.append({
 "kind": "theory", "id": "s3", "mins": 9,
 "title": "The statistic, its range, and which way to reject",
 "objective": "Write the definition down precisely and settle the three facts about it that get asked most.",
 "blocks": [
  {"t": "def", "h": "The likelihood ratio statistic",
   "body": "Let the full parameter space be Θ and let the null hypothesis confine θ to a subset Θ₀. Write Θ = Θ₀ ∪ Θ₁. The likelihood ratio statistic is the maximised likelihood under the null divided by the maximised likelihood over the whole space."},
  {"t": "formula", "h": "The definition in symbols",
   "body": "λ(x) = sup L(θ | x) over θ in Θ₀  /  sup L(θ | x) over θ in Θ\nThe numerator maximises with the null's restriction imposed; the denominator maximises with no restriction at all."},
  {"t": "step", "h": "The denominator is over Θ, not over Θ₁ — and this is asked",
   "body": "A very common error, and one of the two false options in June 2026 Q30's neighbourhood, is to write the denominator as a maximum over the ALTERNATIVE set Θ₁. It is over the whole space Θ, which contains Θ₀. That is what guarantees the ratio cannot exceed 1. Some textbooks do define a variant with Θ₁ underneath, and it is a different statistic with a different range; for NET, the definition above is the one being tested."},
  {"t": "formula", "h": "The range",
   "body": "0 < λ ≤ 1.\nThe upper bound holds because Θ₀ sits inside Θ, so the denominator's maximum is taken over more options and can only be larger or equal. The lower bound is strict because a likelihood that is maximised over a larger set is still a positive number. Any option claiming 0 < λ < ∞ is false, and that is exactly the distractor Q30 used."},
  {"t": "step", "h": "Which way to reject",
   "body": "Reject H₀ for SMALL λ. Small means the restriction cost a lot of explanatory power. The test is: reject when λ ≤ c, with c chosen so the size is α. Because λ is bounded above by 1, 'small' and 'close to zero' mean the same thing here, and a value near 1 is evidence for the null, not against it."},
  {"t": "def", "h": "What λ = 1 means",
   "body": "λ = 1 exactly when the unrestricted maximum is attained somewhere inside Θ₀ — that is, when the unrestricted MLE already satisfies the null hypothesis. The data has given you no reason at all to leave the null. It does not mean the null is true; it means this sample contains no evidence against it."},
  {"t": "step", "h": "The data enters only through a sufficient statistic",
   "body": "The whole of λ is built from likelihoods, and by the factorisation theorem the likelihood depends on the data only through a sufficient statistic T, up to a factor that does not involve θ. That factor is identical in the numerator and the denominator and cancels. So λ is a function of T alone. This was the second TRUE statement in Q30, and it connects this topic back to section 4.1 — it is also why the LR test is never wasteful of information."}],
 "flow": {
  "title": "Building and using the statistic",
  "alt": "Flow chart for carrying out a likelihood ratio test",
  "nodes": [
   {"id": "a", "r": 0, "c": 1, "label": "H₀ confines θ to Θ₀ inside Θ", "kind": "start"},
   {"id": "b", "r": 1, "c": 0, "label": "Maximise L over Θ₀ (restriction imposed)", "kind": "step"},
   {"id": "c", "r": 1, "c": 2, "label": "Maximise L over Θ (no restriction)", "kind": "step"},
   {"id": "d", "r": 2, "c": 1, "label": "λ = numerator / denominator, with 0 < λ ≤ 1", "kind": "step"},
   {"id": "e", "r": 3, "c": 0, "label": "Exact route: simplify λ ≤ c into a region on a known statistic", "kind": "step"},
   {"id": "f", "r": 3, "c": 2, "label": "Large-sample route: −2 log λ ≈ chi-square, df = restrictions", "kind": "step"},
   {"id": "g", "r": 4, "c": 1, "label": "Reject H₀ for small λ, equivalently large −2 log λ", "kind": "end"}],
  "edges": [
   {"from": "a", "to": "b"}, {"from": "a", "to": "c"},
   {"from": "b", "to": "d"}, {"from": "c", "to": "d"},
   {"from": "d", "to": "e", "label": "when the algebra closes"},
   {"from": "d", "to": "f", "label": "when it does not"},
   {"from": "e", "to": "g"}, {"from": "f", "to": "g"}],
  "note": "The two routes out of the middle are the whole practical content: the normal cases simplify exactly into a z, t or chi-square test, and everything else leans on Wilks."},
 "ask": {
  "q": "If the denominator were maximised over Θ₁ instead of Θ, what would happen to the claim that λ ≤ 1?",
  "nudge": "Θ₁ does not contain Θ₀. So is there any reason the denominator must be at least as large as the numerator?"}})

S.append({
 "kind": "worked", "id": "s4", "mins": 8,
 "title": "Worked in full — the normal mean, σ² known",
 "objective": "Run the definition end to end and watch it collapse into the test you already know.",
 "ask": {
  "q": "The statistic came out as the square of the z statistic. What does that tell you about the critical values of the two tests?",
  "nudge": "If one statistic is the square of the other, a region of the form 'statistic large' in one is which region in the other?"},
 "problem": "X₁,…,Xₙ are iid N(μ, σ²) with σ² known. Test H₀: μ = μ₀ against H₁: μ ≠ μ₀. Find λ, simplify −2 log λ, and identify the test.",
 "steps": [
  {"say": "Maximise the likelihood under the null. There is nothing to maximise — the null fixes μ.",
   "math": "sup over Θ₀:  L(μ₀) = (2πσ²)^(−n/2) exp(−Σ(xᵢ − μ₀)²/(2σ²))",
   "why": "Θ₀ is the single point μ₀, so the supremum is just the likelihood evaluated there. Whenever the null fixes every free parameter, the numerator needs no work at all."},
  {"say": "Maximise over the whole space. Here μ is free, and its MLE is x̄.",
   "math": "sup over Θ:  L(x̄) = (2πσ²)^(−n/2) exp(−Σ(xᵢ − x̄)²/(2σ²))",
   "why": "The constant in front is the same in both, which is the general reason these ratios simplify: anything not involving the parameter under test cancels."},
  {"say": "Form the ratio and use the decomposition identity from the opening checks.",
   "math": "λ = exp{ −[Σ(xᵢ − μ₀)² − Σ(xᵢ − x̄)²] / (2σ²) }\nΣ(xᵢ − μ₀)² − Σ(xᵢ − x̄)² = n(x̄ − μ₀)²\nso  λ = exp{ −n(x̄ − μ₀)² / (2σ²) }",
   "why": "That identity is doing all the work. Note the result: λ is a function of x̄ alone, which is the sufficient statistic here, exactly as the previous section promised."},
  {"say": "Take −2 log λ.",
   "math": "−2 log λ = n(x̄ − μ₀)² / σ²\n  = [ (x̄ − μ₀) / (σ/√n) ]²\n  = Z²",
   "why": "The statistic is the square of the ordinary z statistic. Since λ ≤ 1 always, log λ ≤ 0 and −2 log λ ≥ 0, which is what lets it be compared with a chi-square."},
  {"say": "Read off the test.",
   "math": "reject when λ small  ⟺  reject when −2 log λ large  ⟺  reject when |Z| large\ncritical value: χ²(0.05, 1) = 3.841 = (1.96)²",
   "why": "The likelihood ratio test of a normal mean with known variance IS the two-sided z test. It did not need to be invented separately, and the agreement of the critical values — 3.841 against 1.96² — is the arithmetic confirmation."}],
 "after": "Two things to carry forward. The statistic turned out to be a function of the sufficient statistic, with every constant cancelling, and that is typical rather than lucky. And −2 log λ came out exactly chi-square with 1 degree of freedom here, for every n, with no approximation at all. The theorem in the next-but-one section says that something like this happens for large n in general — this example is the case where it is exact."})

S.append({
 "kind": "recall", "id": "s5", "mins": 2,
 "title": "Pause and recall",
 "objective": "Retrieve the definition and its three facts before going on.",
 "intro": "Answer each one before revealing it. Correcting a wrong retrieval is worth more than re-reading a right answer.",
 "items": [
  {"q": "Write the likelihood ratio statistic.",
   "a": "λ = (sup of L over Θ₀) / (sup of L over Θ). Restriction imposed on top, no restriction underneath."},
  {"q": "What is the range of λ, and why is the upper limit what it is?",
   "a": "0 < λ ≤ 1. The upper limit is 1 because Θ₀ is contained in Θ, so the denominator maximises over more options."},
  {"q": "Do you reject for large or small λ?",
   "a": "Small. A small ratio means the null's restriction cost a lot of explanatory power."},
  {"q": "What does the data enter λ through?",
   "a": "A sufficient statistic. The factor of the likelihood that does not involve θ is the same above and below, and cancels."},
  {"q": "What does λ = 1 tell you?",
   "a": "The unrestricted MLE already satisfies the null, so this sample gives no evidence against it. Not that the null is true."}]})

S.append({
 "kind": "completion", "id": "s6", "mins": 8,
 "title": "Your turn — testing a normal variance",
 "objective": "Build the statistic yourself in the case where the null fixes the variance and leaves the mean free.",
 "problem": "X₁,…,Xₙ are iid N(μ, σ²) with BOTH parameters unknown. Test H₀: σ² = σ₀² against H₁: σ² ≠ σ₀². Build λ and say what the critical region is based on. Write t for Σ(xᵢ − x̄)²/σ₀².",
 "steps": [
  {"say": "Start with the unrestricted maximisation, where both parameters are free.",
   "blank": {"prompt": "What are the two unrestricted MLEs?",
             "answer": "μ̂ = x̄ and σ̂² = Σ(xᵢ − x̄)²/n",
             "accept": ["xbar and sum(x-xbar)^2/n", "x̄, Σ(xᵢ−x̄)²/n", "mean and S2 with divisor n",
                        "μ=x̄, σ²=Σ(x−x̄)²/n", "x bar, sum of squares over n"],
             "hint": "The MLE of a normal variance divides by n, not by n − 1."},
   "why": "The divisor n is the point of this step. Using n − 1 here gives a different statistic and a wrong value, and the wrong value is usually among the options."},
  {"say": "Now the restricted maximisation. The null fixes σ² but leaves μ free.",
   "blank": {"prompt": "Under H₀, what is the MLE of μ, and what is σ² set to?",
             "answer": "μ̂ = x̄ still, and σ² = σ₀²",
             "accept": ["x̄ and σ₀²", "mean is xbar, variance fixed at sigma0^2",
                        "μ̂=x̄, σ²=σ₀²", "x bar, sigma zero squared"],
             "hint": "The null says nothing about μ, so μ is still estimated — and the estimate does not change."},
   "why": "A null that restricts one parameter leaves the others to be re-estimated. Forgetting to re-estimate the free parameter is the standard error in every multi-parameter LR problem."},
  {"say": "Form the ratio. Both likelihoods are normal likelihoods evaluated at their own maxima.",
   "blank": {"prompt": "Write λ in terms of t = Σ(xᵢ − x̄)²/σ₀² and n.",
             "answer": "λ = (t/n)^(n/2) e^((n − t)/2)",
             "accept": ["(t/n)^(n/2) exp((n-t)/2)", "(t/n)^{n/2}e^{(n-t)/2}",
                        "lambda = (t/n)^(n/2) * e^((n-t)/2)"],
             "hint": "The ratio of the two (2πσ²)^(−n/2) factors gives (σ̂²/σ₀²)^(n/2) = (t/n)^(n/2), and the two exponentials give e^((n − t)/2)."},
   "why": "Everything is now a function of t alone. That is the sufficient statistic for σ² once μ has been estimated, so this is the expected shape."},
  {"say": "Finally, work out what rejecting small λ means in terms of t.",
   "blank": {"prompt": "λ is largest at one particular value of t. Which one, and what does that make the critical region?",
             "answer": "λ is largest at t = n, so the region rejects both small and large t — a two-tailed region on Σ(xᵢ − x̄)²",
             "accept": ["t = n, two-tailed region on t", "largest at t=n so reject in both tails",
                        "t=n; two-sided critical region based on the sum of squares",
                        "at t = n, so both tails"],
             "hint": "Differentiate log λ with respect to t, or just note that t = n is where the restricted and unrestricted variances agree."},
   "why": "Setting the derivative of log λ = (n/2) log(t/n) + (n − t)/2 to zero gives n/(2t) = 1/2, so t = n. λ falls away on both sides, so 'λ small' means t far from n in either direction. The LR test of a normal variance is the two-tailed chi-square test on Σ(xᵢ − x̄)²/σ₀², which is one of the nine things the practice variants on this question ask."}],
 "after": "Compare this with the previous section. There the null fixed the only parameter and the numerator needed no maximising. Here the null fixed one parameter and left another free, so both maxima took work. That is the only structural difference between easy and hard LR problems, and spotting which one you have is the first thing to do."})

S.append({
 "kind": "theory", "id": "s7", "mins": 8,
 "title": "Wilks' theorem — where the chi-square comes from",
 "objective": "State the large-sample result exactly, including the conditions, and know why it is −2 log λ and not λ.",
 "blocks": [
  {"t": "step", "h": "The problem it solves",
   "body": "The normal cases simplified into tests whose exact distributions were already known. Most problems do not. Without something general, each new null hypothesis would need its own exact distribution theory, and for most of them none exists in closed form. Wilks' theorem supplies one answer that covers all of them approximately."},
  {"t": "formula", "h": "Wilks' theorem",
   "body": "Under H₀ and the regularity conditions, as n grows,\n    −2 log λ  →  chi-square with r degrees of freedom,\nwhere r is the number of independent restrictions the null hypothesis imposes — equivalently r = dim(Θ) − dim(Θ₀)."},
  {"t": "step", "h": "Why −2 log λ rather than λ",
   "body": "λ lives in the interval (0, 1] and its distribution there is awkward and depends on the problem. Taking the logarithm sends it to (−∞, 0]; the minus sign flips it to [0, ∞); the factor 2 is what makes the limit come out as a standard chi-square rather than a scaled one. The transformation is monotone decreasing, so small λ corresponds to large −2 log λ, and the rejection region keeps its meaning: reject for large −2 log λ."},
  {"t": "def", "h": "The false claim that gets tested",
   "body": "−2 log λ is asymptotically CHI-SQUARE, not standard normal. The statement '−2 log λ ~ N(0,1) asymptotically' was one of the two false options in June 2026 Q30, and it is false twice over: a standard normal takes negative values and −2 log λ cannot, since λ ≤ 1 forces it to be non-negative. If an option offers a normal limit, that alone rules it out."},
  {"t": "step", "h": "The conditions, in the form NET asks about them",
   "body": "The theorem needs the model to be regular: the support must not depend on the parameter, the true parameter must lie in the INTERIOR of the parameter space rather than on its boundary, the likelihood must be twice differentiable in θ with a non-singular information matrix, and the number of restrictions r must stay fixed as n grows. The uniform family on (0, θ) fails the first two, and the optional section at the end shows what goes wrong — the limit is a chi-square with the wrong degrees of freedom."},
  {"t": "step", "h": "What 'asymptotic' costs you in practice",
   "body": "It is an approximation that improves with n, and for small samples the true size of the test can differ noticeably from the nominal α. When an exact route exists — the z, t and chi-square tests of the normal family — use it. Wilks is for when it does not."}],
 "ask": {
  "q": "Why is '−2 log λ is asymptotically N(0,1)' refutable without knowing anything about Wilks' theorem?",
  "nudge": "What values can −2 log λ take, given that λ ≤ 1? What values can a standard normal take?"}})

S.append({
 "kind": "guided", "id": "s8", "mins": 8,
 "title": "On your own — the normal mean with σ² unknown",
 "objective": "Handle the case where the null restricts one parameter and another has to be re-estimated under both hypotheses.",
 "problem": "X₁,…,Xₙ are iid N(μ, σ²) with BOTH parameters unknown. Test H₀: μ = μ₀ against H₁: μ ≠ μ₀. Find λ, express it in terms of the usual t statistic t = (x̄ − μ₀)/(s/√n) with s² = Σ(xᵢ − x̄)²/(n − 1), and identify the test.",
 "hints": [
  "Direction — under the null, μ is fixed at μ₀ but σ² is still free, so you must find its MLE subject to that restriction. It is Σ(xᵢ − μ₀)²/n, with μ₀ in place of x̄.",
  "Second step — when a normal likelihood is maximised over its variance, the result always takes the form (2π σ̂²)^(−n/2) e^(−n/2). The exponential part is then the same above and below and cancels, so λ reduces to a ratio of the two variance estimates raised to a power.",
  "Last step — use Σ(xᵢ − μ₀)² = Σ(xᵢ − x̄)² + n(x̄ − μ₀)² to turn that ratio into something containing n(x̄ − μ₀)²/Σ(xᵢ − x̄)², then relate that quantity to t²."],
 "answer": "λ = (1 + t²/(n − 1))^(−n/2), and the test is the two-sided one-sample t test.",
 "check": "Three things an examiner looks for. Under the null σ² is re-estimated, not held at some value — a null that is silent about a parameter leaves it free, and treating σ² as known here is the commonest error. The exponential factors cancel because each maximised normal likelihood carries the same e^(−n/2), which is what makes λ a pure ratio of variance estimates. And the conclusion is the t test, not the z test: σ² was unknown, so the exact distribution has n − 1 degrees of freedom rather than being normal. Note also that −2 log λ = n log(1 + t²/(n − 1)) is approximately t² for large n, which is approximately chi-square with 1 degree of freedom — Wilks and the exact t test agreeing in the limit, as they must.",
 "scenario": {
  "teaser": "A fertiliser trial has eight plots and no idea what the plot-to-plot variation is.",
  "title": "Why σ² is almost never known",
  "body": [
   "The previous worked example assumed σ² known. Consider how odd that is. A trial of eight plots, measuring yield response to a fertiliser dose, is run precisely because nobody knows how the yields behave — and that includes their spread.",
   "σ² known is a teaching device. It isolates one difficulty at a time, and it is the case where the algebra closes into a normal distribution. Real problems hand you both parameters unknown, and the honest test has to pay for estimating the second one.",
   "The price is visible in the answer. With σ² known the statistic was exactly chi-square with 1 degree of freedom for every sample size. With σ² unknown it is a t statistic on n − 1 degrees of freedom, whose tails are heavier — so the critical value is larger and the test is more conservative. With eight plots the two-sided 5% point is 2.365 rather than 1.96.",
   "That gap closes as n grows, which is the same statement as Wilks' theorem applied to this problem. For eight plots it is not small: P(|t₇| > 1.96) = 0.091, so using the normal cut-off would mean running a test whose real size is about 9% while believing it to be 5%."],
  "q": "Why is the critical value larger when σ² has to be estimated?",
  "answer": "Because the statistic has an extra source of variation. The denominator s is itself an estimate that wobbles from sample to sample, and a ratio whose denominator wobbles takes extreme values more often than one with a fixed denominator. The t distribution's heavier tails are exactly that extra wobble, and the larger critical value is the price of not knowing σ²."},
 "solution": [
  {"say": "Maximise over the whole space: both parameters free.",
   "math": "μ̂ = x̄,  σ̂² = Σ(xᵢ − x̄)²/n\nsup over Θ:  L = (2π σ̂²)^(−n/2) e^(−n/2)",
   "why": "Substituting the MLE of the variance back into a normal likelihood always leaves the exponent at exactly −n/2. Worth remembering: it is why these ratios collapse."},
  {"say": "Maximise under the null: μ is fixed at μ₀, σ² still free.",
   "math": "σ̂₀² = Σ(xᵢ − μ₀)²/n\nsup over Θ₀:  L = (2π σ̂₀²)^(−n/2) e^(−n/2)",
   "why": "This is the step the question is really testing. The null fixes μ only, so σ² is re-estimated under the restriction — and with μ held at μ₀ the deviations are measured from μ₀, not from x̄."},
  {"say": "Form the ratio; the constants and the exponentials cancel.",
   "math": "λ = (σ̂² / σ̂₀²)^(n/2)\n  = [ Σ(xᵢ − x̄)² / Σ(xᵢ − μ₀)² ]^(n/2)",
   "why": "Both maximised likelihoods carry the same (2π)^(−n/2) and the same e^(−n/2), so only the variance estimates survive. λ ≤ 1 is now visible directly: the numerator sum of squares is the smaller one."},
  {"say": "Use the decomposition and convert to t.",
   "math": "Σ(xᵢ − μ₀)² = Σ(xᵢ − x̄)² + n(x̄ − μ₀)²\nλ = [ 1 + n(x̄ − μ₀)²/Σ(xᵢ − x̄)² ]^(−n/2)\nn(x̄ − μ₀)²/Σ(xᵢ − x̄)² = t²/(n − 1)\nλ = (1 + t²/(n − 1))^(−n/2)",
   "why": "The middle line is the same identity used in the σ² known case. The last substitution follows from t² = n(x̄ − μ₀)²/s² and s² = Σ(xᵢ − x̄)²/(n − 1)."},
  {"say": "Read off the test.",
   "math": "λ small  ⟺  t² large  ⟺  |t| large\nreject when |t| > t(α/2, n − 1)",
   "why": "λ is a decreasing function of t², so the LR test is exactly the two-sided one-sample t test. Another case where the general method reproduces a test that was already standard — which is the main reason to trust the general method."}]})

S.append({
 "kind": "trapcheck", "id": "s9", "mins": 6,
 "title": "Six statements — verdict on each before you look",
 "objective": "Rule on the exact claims the real multi-statement questions use, including the four from June 2026 Q30.",
 "intro": "Decide true or false on all six before revealing any. Four of these are the statements that made up Q30, which was marked all or nothing.",
 "items": [
  {"claim": "λ is the maximised likelihood under H₀ divided by the maximised likelihood over the whole parameter space.",
   "tf": True,
   "why": "True — this is the definition, and it was a TRUE option in Q30. The denominator is over Θ, which contains Θ₀, and that containment is what bounds the ratio by 1."},
  {"claim": "The likelihood ratio statistic satisfies 0 < λ < ∞.",
   "tf": False,
   "why": "False, and this was a FALSE option in Q30. The correct range is 0 < λ ≤ 1. Anything above 1 would mean the restricted maximum beat the unrestricted one, which is impossible."},
  {"claim": "−2 log λ is asymptotically standard normal.",
   "tf": False,
   "why": "False, the other FALSE option in Q30. It is asymptotically chi-square with degrees of freedom equal to the number of restrictions. It cannot be normal: λ ≤ 1 makes −2 log λ non-negative, and a standard normal is not."},
  {"claim": "The likelihood ratio test is a function of sufficient statistics.",
   "tf": True,
   "why": "True, the other TRUE option in Q30. The part of the likelihood that does not involve θ is identical above and below and cancels, leaving λ a function of the sufficient statistic alone."},
  {"claim": "The likelihood ratio test is invariant under a one-to-one reparameterisation of the model.",
   "tf": True,
   "why": "True. Re-expressing the model in terms of a one-to-one function of θ relabels the points of Θ and Θ₀ without changing which likelihood values are attainable, so both suprema are unchanged and so is λ. Testing σ = σ₀ gives the same test as testing σ² = σ₀²."},
  {"claim": "For a simple null against a simple alternative, the likelihood ratio test is the Neyman–Pearson most powerful test.",
   "tf": True,
   "why": "True, though the reasoning needs care. With Θ = {θ₀, θ₁} the statistic is λ = L(θ₀)/max{L(θ₀), L(θ₁)}, which is not the Neyman–Pearson ratio itself. But it is a decreasing function of L(θ₁)/L(θ₀), so 'λ small' and 'Neyman–Pearson ratio large' describe the same rejection region — and that region is most powerful."}]})

S.append({
 "kind": "guided", "id": "s10", "mins": 7,
 "title": "On your own — counting the degrees of freedom",
 "objective": "Get the one number that decides the answer even when the arithmetic is right.",
 "problem": "Give the asymptotic degrees of freedom of −2 log λ in each case. (a) H₀ imposes 3 independent restrictions on θ. (b) A multinomial with 5 categories, where H₀ specifies all five probabilities numerically. (c) Three independent normal samples with unknown common variance, testing H₀: μ₁ = μ₂ = μ₃. (d) A N(μ, σ²) sample, testing H₀: μ = 0 with σ² unknown.",
 "hints": [
  "The rule is r = dim(Θ) − dim(Θ₀): count the free parameters without the restriction, count them with it, subtract. Counting restrictions directly works too, as long as they are independent.",
  "For the multinomial, remember that the probabilities must sum to 1, so 5 categories have only 4 free parameters, not 5. This is the step the question is built on.",
  "For the three means, 'all equal' is not three restrictions. Write it as μ₁ = μ₂ and μ₂ = μ₃ and count — the third equality follows from those two and is not independent."],
 "answer": "(a) 3  (b) 4  (c) 2  (d) 1",
 "check": "Two places this goes wrong in exam conditions. A multinomial with k categories has k − 1 free parameters because of the sum-to-one constraint, so specifying all of them is k − 1 restrictions, not k. And 'three means are all equal' is two independent restrictions, not three — the pattern for k groups is k − 1. In (d) note that σ² is a nuisance parameter present under both hypotheses: it is free in Θ and free in Θ₀, so it contributes nothing to the difference in dimensions. Nuisance parameters never add to the degrees of freedom.",
 "solution": [
  {"say": "(a) Read the rule straight off.",
   "math": "r = number of independent restrictions = 3",
   "why": "This is the definition, and it is how the question is usually phrased when it wants a one-step answer."},
  {"say": "(b) Count the free parameters of a multinomial carefully.",
   "math": "dim(Θ) = 5 − 1 = 4   (the probabilities sum to 1)\ndim(Θ₀) = 0            (all five specified)\nr = 4 − 0 = 4",
   "why": "The sum-to-one constraint is the trap. Answering 5 here is the single most common mistake in goodness-of-fit degrees of freedom, and it carries straight over to section 4.14."},
  {"say": "(c) Write 'all equal' as a set of independent equations.",
   "math": "dim(Θ) = 3 means + 1 variance = 4\ndim(Θ₀) = 1 common mean + 1 variance = 2\nr = 4 − 2 = 2",
   "why": "Equivalently μ₁ = μ₂ and μ₂ = μ₃ are two independent restrictions and μ₁ = μ₃ follows. For k groups the answer is k − 1."},
  {"say": "(d) Watch what the nuisance parameter does.",
   "math": "dim(Θ) = 2  (μ and σ²)\ndim(Θ₀) = 1  (σ² only; μ is fixed at 0)\nr = 2 − 1 = 1",
   "why": "σ² is unknown under both hypotheses, so it cancels out of the subtraction. This is the case you solved exactly in the previous section, and the agreement is a check: n log(1 + t²/(n − 1)) ≈ t², which is approximately chi-square with 1 degree of freedom for large n."}]})

S.append({
 "kind": "theory", "id": "s11", "mins": 6,
 "title": "Where this test sits among the others",
 "objective": "Place the LR test against Neyman–Pearson and the standard normal tests, which is how the conceptual questions are framed.",
 "blocks": [
  {"t": "step", "h": "Against Neyman–Pearson",
   "body": "Neyman–Pearson gives the most powerful test, but only for one simple hypothesis against one simple hypothesis. The LR test gives up the guarantee of being most powerful and buys the ability to handle composite hypotheses on either side. In the simple-versus-simple case the two coincide, so nothing is lost by using the general method where the special one applies."},
  {"t": "def", "h": "Which standard tests it reproduces",
   "body": "Normal mean, σ² known → the two-sided z test. Normal mean, σ² unknown → the two-sided t test. Normal variance with μ unknown → the two-tailed chi-square test on Σ(xᵢ − x̄)²/σ₀². Multinomial goodness of fit → asymptotically the familiar chi-square statistic. The LR principle is not a competitor to these tests; it is the principle that generates them."},
  {"t": "step", "h": "Two properties worth stating as properties",
   "body": "It is a function of the sufficient statistic, so it uses all the relevant information and no irrelevant information. And it is invariant under one-to-one reparameterisation, so the test of σ = σ₀ is the test of σ² = σ₀² — the conclusion cannot be changed by rewriting the model. Both are asked directly."},
  {"t": "step", "h": "What it does not promise",
   "body": "It is not most powerful in general, its distribution is usually only approximate, and the approximation needs regularity conditions that some textbook families violate. It is the workhorse, chosen for generality rather than optimality, and an option claiming the LR test is 'always most powerful' is false."}],
 "ask": {
  "q": "If the LR test is not most powerful in general, why is it the one used most in practice?",
  "nudge": "Count how many real null hypotheses are simple against simple. What else is available for the rest of them?"}})

S.append({
 "kind": "recall", "id": "s12", "mins": 2,
 "title": "Second recall — the parts most likely to fade",
 "objective": "Retrieve the theorem and the counting rules, which are what the exam actually asks.",
 "intro": "Same discipline: answer, then reveal.",
 "items": [
  {"q": "State Wilks' theorem.",
   "a": "Under H₀ and regularity conditions, −2 log λ converges in distribution to a chi-square with degrees of freedom equal to the number of independent restrictions, r = dim(Θ) − dim(Θ₀)."},
  {"q": "A multinomial with 6 categories, null specifying all probabilities. Degrees of freedom?",
   "a": "5. Six categories have 5 free parameters because they sum to 1, and the null leaves none free."},
  {"q": "Testing that 4 group means are all equal. Degrees of freedom?",
   "a": "3. For k groups it is k − 1, because 'all equal' is k − 1 independent equations."},
  {"q": "Does a nuisance parameter unknown under both hypotheses add to the degrees of freedom?",
   "a": "No. It is free in both Θ and Θ₀, so it cancels in the subtraction."},
  {"q": "Which two of Wilks' conditions does the uniform family on (0, θ) violate?",
   "a": "Its support depends on θ, and the maximum is attained at the boundary rather than an interior point. The optional section shows the consequence."}]})

S.append({
 "kind": "summary", "id": "s13", "mins": 3,
 "title": "What you should now be able to do unaided",
 "objective": "Close the loop before the mastery test.",
 "body": [
  "Write the likelihood ratio statistic as the maximised likelihood under the null over the maximised likelihood over the whole space, and say why its range is 0 < λ ≤ 1.",
  "Reject for small λ, equivalently for large −2 log λ, and explain what λ = 1 means and what it does not mean.",
  "Carry out the maximisation in both the easy case, where the null fixes every parameter, and the harder case, where a nuisance parameter must be re-estimated under the restriction.",
  "Reproduce the three normal results: σ² known gives the z test, σ² unknown gives the t test, and a test of the variance gives a two-tailed region on Σ(xᵢ − x̄)².",
  "State Wilks' theorem with its degrees of freedom, and say why the statistic is −2 log λ rather than λ.",
  "Count degrees of freedom correctly in the two cases that catch people: a multinomial with k categories has k − 1 free parameters, and k means being all equal is k − 1 restrictions.",
  "Say that the test is a function of the sufficient statistic, that it is invariant under one-to-one reparameterisation, that it coincides with Neyman–Pearson when both hypotheses are simple, and that it is not most powerful in general."]})

S.append({
 "kind": "theory", "id": "s14", "mins": 8, "ext": True,
 "title": "When Wilks fails — the uniform family",
 "objective": "See a case where the theorem's conditions break and the naive degrees of freedom are simply wrong.",
 "blocks": [
  {"t": "step", "h": "The setup",
   "body": "Let X₁,…,Xₙ be iid uniform on the interval (0, θ), and test H₀: θ = θ₀ against H₁: θ ≠ θ₀. The null fixes the only parameter, so the naive reading of Wilks' theorem would give one restriction and a chi-square with 1 degree of freedom. It is wrong, and this family is the standard counterexample."},
  {"t": "formula", "h": "The statistic",
   "body": "The unrestricted MLE is the sample maximum, θ̂ = X₍ₙ₎. Writing M = X₍ₙ₎,\n    λ = (M/θ₀)^n   when M ≤ θ₀,   and   λ = 0   when M > θ₀.\nThe second case is worth pausing on: a single observation above θ₀ is impossible under the null, so the null's likelihood is exactly zero and the data refutes H₀ outright."},
  {"t": "step", "h": "The exact distribution, which can be worked out in full",
   "body": "Under H₀ the ratio U = M/θ₀ has distribution function P(U ≤ u) = uⁿ on (0, 1). Put Y = −n log U. Then P(Y > y) = P(U < e^(−y/n)) = e^(−y), so Y is exponential with mean 1. Since −2 log λ = −2n log U = 2Y, and twice an exponential with mean 1 is a chi-square with 2 degrees of freedom, the statistic is EXACTLY chi-square with 2 degrees of freedom — for every n, not just in the limit."},
  {"t": "step", "h": "What that tells you",
   "body": "The naive answer was 1 degree of freedom; the truth is 2. Using the wrong one has a measurable cost: you would reject when the statistic exceeded 3.841, the 5% point of a chi-square with 1 degree of freedom, but a chi-square with 2 degrees of freedom exceeds 3.841 with probability e^(−3.841/2) = 0.147. So a test you believed had size 5% would really have size about 15% — three times what you intended. The theorem did not fail by a small margin; its conditions simply did not hold, and its conclusion was unavailable."},
  {"t": "step", "h": "Which conditions broke",
   "body": "Two of them. The support of the density is (0, θ), so it depends on the parameter — differentiating under the integral sign is not valid and the usual regularity machinery does not apply. And the likelihood is maximised at the sample maximum, which sits at the edge of the allowed region rather than at an interior stationary point. Whenever the support depends on the parameter — the uniform family, shifted exponentials — expect the standard asymptotics to be unavailable and look for the exact distribution instead, which in this family is obtainable."}],
 "ask": {
  "q": "In this family, what is the exact value of λ when one observation exceeds θ₀, and what does that say about the test?",
  "nudge": "What is the likelihood of data that the null hypothesis says is impossible?"}})

S.append({
 "kind": "quiz", "id": "s15", "mins": 12,
 "title": "Mastery test",
 "objective": "Demonstrate it independently, on questions you have not seen.",
 "setId": "inference_t10_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id": "inferencet10",
 "topicId": "inference-t10",
 "moduleId": "inference",
 "title": "The Likelihood Ratio Test and Wilks' Theorem",
 "breadcrumb": "Statistical Inference → Testing of Hypotheses → The likelihood ratio test",
 "engine": "C",
 "engineName": "Testing — comparing the best the null can do with the best anything can do",
 "version": "1.0",
 "status": "approved",
 "estMin": sum(s["mins"] for s in CORE),
 "objectives": [
  "Write the likelihood ratio statistic with the correct sets in the numerator and denominator, and justify its range 0 < λ ≤ 1.",
  "Carry out both maximisations, including the case where a nuisance parameter must be re-estimated under the null.",
  "Derive the three standard normal results: the z test, the t test, and the two-tailed region on Σ(xᵢ − x̄)².",
  "State Wilks' theorem with its degrees of freedom and its regularity conditions, and say why the statistic is −2 log λ.",
  "Count degrees of freedom correctly for multinomial nulls, equality-of-means nulls, and nulls with nuisance parameters.",
  "Place the test against Neyman–Pearson, and state its invariance and sufficiency properties."],
 "prereq": [
  {"id": "p1", "name": "Maximum likelihood estimation",
   "why": "The statistic is a ratio of two maximised likelihoods, so every problem begins with two MLE calculations. If finding an MLE is still slow, topic 4.4 comes first."},
  {"id": "p2", "name": "Sufficiency and the factorisation theorem",
   "why": "The reason λ depends on the data only through a sufficient statistic is that the factorisation theorem's θ-free factor cancels between numerator and denominator. This is asked directly."},
  {"id": "p3", "name": "The chi-square distribution and its tail values",
   "why": "Every large-sample conclusion in this topic ends at a chi-square upper tail. You need 3.841, 5.991, 7.815 and 9.488 available without a table."},
  {"id": "p4", "name": "Size and power of a test",
   "why": "The constant in 'reject when λ ≤ c' is fixed by the size condition, exactly as in topic 4.12. That topic also supplies the vocabulary this one uses throughout."}],
 "traps": [
  "The denominator maximises over the WHOLE space Θ, not over the alternative Θ₁.",
  "The range is 0 < λ ≤ 1; '0 < λ < ∞' is false.",
  "−2 log λ is asymptotically chi-square, never standard normal — it cannot be negative.",
  "A null that is silent about a parameter leaves it free, so re-estimate it under the restriction.",
  "A multinomial with k categories has k − 1 free parameters, not k.",
  "'k means are all equal' is k − 1 independent restrictions, not k.",
  "Nuisance parameters unknown under both hypotheses add nothing to the degrees of freedom.",
  "The MLE of a normal variance divides by n, not n − 1."],
 "revision": {
  "sheet": [
   "λ = (sup L over Θ₀) / (sup L over Θ). Restriction imposed on top; no restriction underneath.",
   "Range 0 < λ ≤ 1, because Θ₀ ⊂ Θ means the denominator maximises over more options.",
   "Reject H₀ for SMALL λ, equivalently for LARGE −2 log λ. The transformation is monotone decreasing.",
   "λ = 1 means the unrestricted MLE already satisfies H₀ — no evidence against it in this sample.",
   "λ is a function of the sufficient statistic; the θ-free factor of the likelihood cancels.",
   "λ is invariant under one-to-one reparameterisation: testing σ = σ₀ is testing σ² = σ₀².",
   "Simple versus simple: λ is a decreasing function of the Neyman–Pearson ratio, so the tests coincide.",
   "Wilks: −2 log λ → chi-square with r df, r = dim(Θ) − dim(Θ₀) = number of independent restrictions.",
   "Normal mean, σ² known: λ = exp(−n(x̄ − μ₀)²/(2σ²)), −2 log λ = Z², exactly chi-square 1 df.",
   "Normal mean, σ² unknown: λ = (1 + t²/(n − 1))^(−n/2) — the two-sided t test on n − 1 df.",
   "Normal variance, μ unknown: λ = (t/n)^(n/2) e^((n − t)/2) with t = Σ(xᵢ − x̄)²/σ₀²; λ peaks at t = n, so the region is two-tailed in t.",
   "Degrees of freedom: multinomial with k categories fully specified → k − 1. k means all equal → k − 1. Nuisance parameters → 0.",
   "Chi-square upper 5% points: 3.841 (1 df), 5.991 (2), 7.815 (3), 9.488 (4). Note 3.841 = 1.96².",
   "Wilks needs: support not depending on θ, true θ interior not on the boundary, twice-differentiable likelihood with non-singular information, and r fixed as n grows.",
   "Uniform on (0, θ), H₀: θ = θ₀: λ = (X₍ₙ₎/θ₀)ⁿ and −2 log λ is EXACTLY chi-square with 2 df — the naive answer of 1 df is wrong."],
  "cards": [
   ["The statistic", "λ = sup L over Θ₀ divided by sup L over Θ — the null's best fit over the unrestricted best fit"],
   ["Its range, and why", "0 < λ ≤ 1, because Θ₀ sits inside Θ so the denominator maximises over more options"],
   ["Direction of rejection", "Reject for small λ, equivalently large −2 log λ"],
   ["λ = 1 means", "The unrestricted MLE already satisfies H₀ — no evidence against it, not proof of it"],
   ["Wilks' theorem", "−2 log λ → chi-square with df = number of independent restrictions = dim(Θ) − dim(Θ₀)"],
   ["Why −2 log λ", "λ lives in (0,1] with an awkward law; the transformation sends it to [0,∞) and makes the limit a standard chi-square"],
   ["Normal mean, σ² known", "−2 log λ = Z², exactly chi-square 1 df — the LR test IS the two-sided z test"],
   ["Normal mean, σ² unknown", "λ = (1 + t²/(n−1))^(−n/2) — the two-sided t test"],
   ["Normal variance test", "A two-tailed region on Σ(xᵢ − x̄)²/σ₀², since λ peaks where that equals n"],
   ["Multinomial df", "k categories fully specified gives k − 1, because the probabilities sum to 1"],
   ["Equality of k means", "k − 1 restrictions, not k — the last equality follows from the others"],
   ["Where Wilks fails", "Uniform on (0, θ): support depends on θ and the MLE is on the boundary; −2 log λ is exactly chi-square with 2 df"]],
  "tricks": [
   "Check λ ≤ 1 on every answer you derive. A value above 1 means you maximised the denominator over the wrong set.",
   "If the null fixes every parameter, the numerator needs no maximising at all — spot that first and the problem halves.",
   "Substituting the MLE of a normal variance back in always leaves e^(−n/2), so those factors cancel. Expect λ to reduce to a ratio of variance estimates.",
   "Σ(xᵢ − μ₀)² = Σ(xᵢ − x̄)² + n(x̄ − μ₀)² is the identity behind both normal-mean cases. Write it down before starting.",
   "Any option offering a normal limit for −2 log λ is wrong on sight, because the statistic cannot be negative."],
  "shortcuts": [
   "Count df as dim(Θ) − dim(Θ₀); it never misleads, whereas counting restrictions can if they are not independent.",
   "3.841 = 1.96². If a 1-df chi-square answer disagrees with the squared z answer, one of them has an arithmetic error.",
   "For large n, n log(1 + t²/(n − 1)) ≈ t², so the exact t test and Wilks agree in the limit — a free check on either."],
  "remember": [
   "Denominator over Θ, not Θ₁. Write the two sets out before maximising anything.",
   "A null silent about a parameter leaves it free. Re-estimate it under the restriction.",
   "k categories mean k − 1 free parameters. k equal means mean k − 1 restrictions."]},
 "howto": "Read this one in order; it builds. The opening checks are not optional — the whole topic is two maximum likelihood calculations in a ratio, so if finding an MLE is slow, nothing after section 4 will feel easy. Sections 4, 7 and 9 are the spine: one worked example where the null fixes everything, the theorem, and one worked example where it does not. Attempt the question at the end of each section before opening the answer. The optional section at the end shows a family where the theorem's conditions fail; it is marked optional and can wait for a second pass, though it is the most instructive thing here once the rest is solid.",
 "refs": [
  {"title": "Likelihood Ratio Tests", "where": "Lesson 27", "site": "Penn State STAT 415",
   "url": "https://online.stat.psu.edu/stat415/lesson/27", "type": "Course notes", "free": True,
   "checked": "2026-10-30",
   "why": "The normal-mean and normal-variance derivations done at exactly this level of detail. Read it after section 4 if the algebra of the ratio still feels unfamiliar."},
  {"title": "Mathematical Statistics 18.655 — lecture notes",
   "where": "Sessions on testing and asymptotics", "site": "MIT OpenCourseWare",
   "url": "https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type": "Lecture notes", "free": True, "checked": "2026-10-30",
   "why": "Wilks' theorem stated with its regularity conditions made explicit, which is what the conceptual questions are really about."},
  {"title": "Statistical Inference", "where": "Weeks on testing of hypotheses",
   "site": "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee",
   "url": "https://archive.nptel.ac.in/noc/courses/noc21/SEM1/noc21-ma23", "type": "Video course",
   "free": True, "checked": "2026-10-30",
   "why": "Indian syllabus notation, which is what the NET paper uses. Useful for the degrees-of-freedom conventions."},
  {"title": "Statistical Inference, 2nd edition", "where": "Sections 8.2.1 and 10.3.1",
   "site": "Casella and Berger", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "The definition, the simple-versus-simple connection to Neyman–Pearson, and the asymptotic result, in the order this lesson follows."},
  {"title": "An Introduction to Probability and Statistics, 3rd edition", "where": "Chapter 10",
   "site": "Rohatgi and Saleh", "url": "", "type": "Textbook", "free": False,
   "checked": "2026-10-30",
   "why": "Worked likelihood ratio tests for the normal family, and the uniform counterexample treated at the level of the optional section."}],
 "mastery": {
  "minQ": 10, "pass": 80, "draw": 10,
  "fmtMin": {"numeric": 70, "multi": 70},
  "diffMix": {"easy": 3, "moderate": 5, "hard": 2},
  "noHints": True, "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "provenance": "Authored October 2026 for this platform against the UGC NET Statistics syllabus, and prioritised from the June 2026 paper, where Q30 asked which statements about the likelihood ratio statistic are true (official answer: the definition with Θ underneath, and the sufficiency property; the false pair being the range 0 < λ < ∞ and a normal asymptotic law). The nine genuine practice variants on that question — the range, the direction of rejection, λ = 1, sufficiency, invariance, degrees of freedom from restrictions, the σ² unknown case, the σ² = σ₀² case, and the simple-versus-simple case — are each taught in a named section and each appear in the pool. While authoring, ten further items tagged to Q30 in the variant bank were found to be Jensen, Markov and Chebyshev inequality questions belonging to Q31, and were retagged. Every numerical value here was recomputed rather than recalled, including the exact chi-square-with-2-degrees-of-freedom result for the uniform family. Previous-year questions themselves are stored separately and carry their exam cycle.",
 "scenes": S}

# ---------------------------------------------------------------- pool

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id": "inf-t10-m-%02d" % i, "format": fmt, "topic": "inference-t10",
         "diff": diff, "stem": stem, "options": opts, "answer": ans, "explanation": exp}
    d.update(kw)
    return d

def verd(a, b, c, dd):
    return {"A": {"tf": a[0], "why": a[1]}, "B": {"tf": b[0], "why": b[1]},
            "C": {"tf": c[0], "why": c[1]}, "D": {"tf": dd[0], "why": dd[1]}}

I = []

# --- easy (6)
I.append(q(1, "single", "easy",
 "The likelihood ratio statistic λ for testing H₀: θ ∈ Θ₀ against H₁: θ ∈ Θ₁, where Θ = Θ₀ ∪ Θ₁, is:",
 ["the supremum of L over Θ₀ divided by the supremum of L over Θ",
  "the supremum of L over Θ₀ divided by the supremum of L over Θ₁",
  "the supremum of L over Θ divided by the supremum of L over Θ₀",
  "the supremum of L over Θ₁ divided by the supremum of L over Θ₀"],
 "A",
 "The null's restriction goes on top and the unrestricted maximum over the whole space Θ goes underneath. Putting Θ₁ underneath gives a different statistic whose range is not bounded by 1, and inverting the ratio reverses the direction of rejection. This was a true option in June 2026 Q30."))

I.append(q(2, "single", "easy",
 "The likelihood ratio statistic λ satisfies:",
 ["0 < λ < ∞", "0 < λ ≤ 1", "−1 ≤ λ ≤ 1", "λ ≥ 1"],
 "B",
 "Θ₀ is contained in Θ, so the denominator is a maximum over a larger set and can only be greater than or equal to the numerator. Hence λ ≤ 1, and it is strictly positive because both maximised likelihoods are positive. The claim 0 < λ < ∞ was a false option in June 2026 Q30."))

I.append(q(3, "single", "easy",
 "The likelihood ratio test rejects H₀ when:",
 ["λ is close to 1", "λ is small", "λ exceeds 1", "−2 log λ is small"],
 "B",
 "A small ratio means the null's restriction cost a great deal of explanatory power, which is evidence against it. Since −2 log λ is a decreasing function of λ, small λ is the same as large −2 log λ. A value close to 1 is evidence for the null, not against it."))

I.append(q(4, "order", "easy",
 "Arrange the steps of carrying out a likelihood ratio test in the correct order.",
 ["C, A, B, D", "A, C, B, D", "C, B, A, D", "A, B, C, D"],
 "A",
 "Write down the two parameter sets first — getting Θ and Θ₀ right is what the whole calculation depends on. Then maximise the likelihood over each, form the ratio, and only then convert 'λ small' into a region on a statistic whose distribution you know.",
 items=["A. Maximise the likelihood separately over Θ₀ and over Θ",
        "B. Form the ratio λ and check that it does not exceed 1",
        "C. Identify the full parameter space Θ and the null subset Θ₀",
        "D. Turn 'reject for small λ' into a critical region on a known statistic"]))

I.append(q(5, "single", "easy",
 "Under H₀ and the usual regularity conditions, the asymptotic distribution of −2 log λ is:",
 ["standard normal", "chi-square with degrees of freedom equal to the number of independent restrictions",
  "chi-square with n − 1 degrees of freedom", "exponential with mean 1"],
 "B",
 "This is Wilks' theorem. It cannot be standard normal: λ ≤ 1 forces −2 log λ to be non-negative, while a standard normal takes negative values — so that option is refutable on sight. The degrees of freedom come from the restrictions, not from the sample size. The normal claim was a false option in June 2026 Q30."))

I.append(q(6, "single", "easy",
 "If H₀ imposes 3 independent restrictions on the parameter, the asymptotic degrees of freedom of −2 log λ is:",
 ["1", "2", "3", "n − 3"],
 "C",
 "The degrees of freedom equal the number of independent restrictions, equivalently dim(Θ) − dim(Θ₀). The sample size plays no part in it, which is why the n − 3 option is wrong however large the sample."))

# --- moderate (10)
I.append(q(7, "numeric", "moderate",
 "X₁,…,X₁₆ are iid N(μ, 16) with σ² = 16 known, and x̄ = 11. For H₀: μ = 10 against H₁: μ ≠ 10, the value of −2 log λ is:",
 ["1.00", "0.25", "4.00", "16.00"],
 "A",
 "For the normal mean with known variance, −2 log λ = n(x̄ − μ₀)²/σ² = 16(11 − 10)²/16 = 1.00. Compared with χ²(0.05, 1) = 3.841 this gives no evidence against H₀. The value 0.25 divides by σ⁴ in effect, and 4.00 uses σ rather than σ².",
 check="−2 log λ here must equal Z², and Z = (11 − 10)/(4/4) = 1, so the statistic is 1. If your answer is not a perfect square of the z value, the standard error was computed wrongly."))

I.append(q(8, "single", "moderate",
 "For testing H₀: μ = μ₀ in N(μ, σ²) with σ² unknown, the likelihood ratio test is equivalent to:",
 ["the two-sided z test", "the two-sided t test with n − 1 degrees of freedom",
  "the chi-square test on Σ(xᵢ − x̄)²", "the F test"],
 "B",
 "Carrying out both maximisations gives λ = (1 + t²/(n − 1))^(−n/2), which is a decreasing function of t², so rejecting small λ is rejecting large |t|. Because σ² had to be estimated, the exact reference distribution is t on n − 1 degrees of freedom and not the normal."))

I.append(q(9, "single", "moderate",
 "For testing H₀: σ² = σ₀² in a normal sample with μ unknown, the likelihood ratio test leads to a critical region based on:",
 ["x̄ alone", "Σ(xᵢ − x̄)², with rejection in both tails",
  "Σ(xᵢ − x̄)², with rejection only in the upper tail", "the sample range"],
 "B",
 "With t = Σ(xᵢ − x̄)²/σ₀² the statistic is λ = (t/n)^(n/2) e^((n − t)/2), which is maximised at t = n and falls away on both sides. So 'λ small' means t far from n in either direction, giving a two-tailed region. A one-tailed region would correspond to a one-sided alternative, which is not what was tested."))

I.append(q(10, "numeric", "moderate",
 "A multinomial has 5 categories and H₀ specifies all five cell probabilities numerically. The asymptotic degrees of freedom of −2 log λ is:",
 ["5", "4", "3", "1"],
 "B",
 "The five probabilities must sum to 1, so the unrestricted model has only 4 free parameters. The null leaves none free, so r = 4 − 0 = 4. Answering 5 ignores the sum-to-one constraint and is the commonest degrees-of-freedom error in the whole syllabus.",
 check="Count free parameters, not categories: k categories give k − 1 free parameters. If your answer equals the number of categories, the constraint was missed."))

I.append(q(11, "single", "moderate",
 "For a simple null against a simple alternative, the likelihood ratio test:",
 ["coincides with the Neyman–Pearson most powerful test",
  "is less powerful than the Neyman–Pearson test",
  "cannot be constructed, since both hypotheses are simple",
  "requires Wilks' theorem to find its critical value"],
 "A",
 "With Θ = {θ₀, θ₁} the statistic is λ = L(θ₀)/max{L(θ₀), L(θ₁)}, which is not the Neyman–Pearson ratio itself but is a decreasing function of it. So the two tests have the same rejection region, and that region is most powerful. No asymptotics are needed — the exact distribution is available from the simple hypotheses."))

I.append(q(12, "multi", "moderate",
 "Let f(x₁,…,xₙ, θ) be the likelihood of a sample of size n, and let λ be the likelihood ratio statistic for H₀: θ ∈ Θ₀ against H₁: θ ∈ Θ₁ with Θ = Θ₀ ∪ Θ₁. Which of the following statements are correct?",
 ["A and B only", "A and D only", "B and C only", "C and D only"],
 "B",
 "A is true — it is the definition, with the whole space underneath. B is false: the range is 0 < λ ≤ 1, not 0 < λ < ∞. C is false: the asymptotic law is chi-square, and a normal limit is impossible for a statistic that cannot be negative. D is true, because the θ-free factor of the likelihood cancels between numerator and denominator. This is June 2026 Q30, whose official answer was A and D only.",
 statements=["λ = sup f over θ in Θ₀ divided by sup f over θ in Θ.",
             "0 < λ < ∞.",
             "−2 logₑ λ is asymptotically N(0, 1).",
             "The likelihood ratio test is a function of sufficient statistics."],
 verdicts=verd(
  (True, "True. This is the definition: the null's maximised likelihood over the maximised likelihood on the whole parameter space."),
  (False, "False. Because Θ₀ lies inside Θ, the denominator can only be the larger maximum, so 0 < λ ≤ 1."),
  (False, "False. The limit is chi-square with degrees of freedom equal to the number of restrictions. A normal limit is impossible anyway, since λ ≤ 1 makes −2 log λ non-negative."),
  (True, "True. By the factorisation theorem the likelihood splits into a θ-free factor and a factor depending on the data only through a sufficient statistic; the first cancels in the ratio."))))

I.append(q(13, "numeric", "moderate",
 "A likelihood ratio test gives −2 log λ = 7.20 with 3 degrees of freedom. At α = 0.05, using χ²(0.05, 3) = 7.815, the conclusion is:",
 ["reject H₀, since 7.20 < 7.815", "do not reject H₀, since 7.20 < 7.815",
  "reject H₀, since 7.20 > 3.841", "the test is inconclusive without the sample size"],
 "B",
 "The statistic falls short of the critical value, so there is no evidence against H₀ at the 5% level. The third option uses the 1-degree-of-freedom critical value, which is the error the question is built on — with 3 restrictions the bar is 7.815, not 3.841. The sample size is not needed once the degrees of freedom are known.",
 check="Compare against the critical value for the RIGHT degrees of freedom. The same statistic of 7.20 would have been significant with 1 or 2 df and is not with 3."))

I.append(q(14, "single", "moderate",
 "The likelihood ratio test is invariant under:",
 ["any transformation of the data", "a one-to-one reparameterisation of the model",
  "any change of the significance level", "a change of sample size"],
 "B",
 "Re-expressing the model through a one-to-one function of θ relabels the points of Θ and Θ₀ without changing which likelihood values are attainable, so both suprema and therefore λ are unchanged. In practice this means the test of σ = σ₀ is the same test as the test of σ² = σ₀²: the conclusion cannot be altered by rewriting the parameter."))

I.append(q(15, "numeric", "moderate",
 "A normal sample of size n = 10 with μ unknown gives Σ(xᵢ − x̄)² = 20. For H₀: σ² = 1, the value of −2 log λ is (use −2 log λ = n log(n/t) + t − n with t = Σ(xᵢ − x̄)²/σ₀²):",
 ["3.07", "10.00", "6.93", "0.22"],
 "A",
 "Here t = 20/1 = 20, so −2 log λ = 10 log(10/20) + 20 − 10 = 10(−0.6931) + 10 = −6.931 + 10 = 3.069, which rounds to 3.07. The value 6.93 is the logarithmic term alone with its sign dropped, and 0.22 is λ itself rather than −2 log λ.",
 check="−2 log λ must be non-negative, since λ ≤ 1. It is zero only when t = n, that is when the estimated variance equals the hypothesised one."))

I.append(q(16, "single", "moderate",
 "λ = 1 for an observed sample indicates that:",
 ["H₀ is true", "the unrestricted MLE of θ already lies in Θ₀",
  "the test cannot be carried out", "the sample size is too small"],
 "B",
 "λ = 1 means the two maxima are equal, which happens exactly when the unrestricted maximum is attained at a point satisfying the null. The data gives no reason to leave H₀, but that is not the same as H₀ being true — a sample can easily be consistent with a false hypothesis."))

# --- hard (4)
I.append(q(17, "multi", "hard",
 "Consider the conditions required for −2 log λ to have an asymptotic chi-square distribution.",
 ["A and C only", "B and D only", "A, B and C only", "A and D only"],
 "A",
 "A is true — a support that moves with θ breaks the regularity machinery, which is why the uniform family is the standard counterexample. B is false: the number of restrictions must stay FIXED as n grows; results for a growing number of restrictions are a different and harder theory. C is true, and it is the other condition the uniform family violates. D is false — the statistic is a ratio of maximised likelihoods and no normality of the data is required; the chi-square limit arises from the asymptotics of the likelihood itself.",
 statements=["The support of the density must not depend on the parameter.",
             "The number of restrictions r may grow with the sample size n.",
             "The true parameter must lie in the interior of the parameter space, not on its boundary.",
             "The observations must be normally distributed."],
 verdicts=verd(
  (True, "True. If the support moves with θ, differentiating under the integral sign is invalid and the usual regularity conditions fail — the uniform family on (0, θ) is the standard example."),
  (False, "False. The theorem requires r to be fixed as n grows. A number of restrictions that increases with n needs different theory."),
  (True, "True. The expansion behind the theorem is around an interior stationary point; a maximum attained at the boundary breaks it, as happens for the uniform family."),
  (False, "False. No normality of the data is needed. The chi-square limit comes from the local behaviour of the log-likelihood, which holds for regular families generally."))))

I.append(q(18, "numeric", "hard",
 "A sample of size n = 9 from N(μ, σ²) with σ² unknown gives t = 2.0 for H₀: μ = μ₀. Using λ = (1 + t²/(n − 1))^(−n/2), the value of λ is approximately:",
 ["0.161", "0.667", "0.191", "6.200"],
 "A",
 "λ = (1 + 4/8)^(−4.5) = 1.5^(−4.5) = exp(−4.5 × 0.4055) = exp(−1.8246) = 0.1613. Option B drops the exponent to −1, giving 1/1.5. Option C uses n rather than n − 1 inside the bracket, giving (1 + 4/9)^(−4.5) = 0.191. Option D has the sign of the exponent wrong, and can be dismissed without any arithmetic at all, since λ can never exceed 1.",
 check="λ must lie in (0, 1], so any value above 1 is wrong on sight. The exponent is −n/2 = −4.5 and the divisor inside the bracket is n − 1 = 8, not n."))

I.append(q(19, "single", "hard",
 "The reason the test statistic is taken as −2 log λ rather than λ itself is that:",
 ["λ has no distribution under H₀",
  "the transformation is monotone decreasing and makes the asymptotic law a standard chi-square",
  "λ can be negative, and the logarithm corrects this",
  "it converts the two-sided test into a one-sided test"],
 "B",
 "λ lives in (0, 1] with a law that varies from problem to problem. The logarithm maps it to (−∞, 0], the minus sign to [0, ∞), and the factor 2 makes the limit an unscaled chi-square. Because the transformation is monotone decreasing, 'λ small' becomes 'statistic large' and the rejection region is unchanged in meaning. λ is never negative, so the third option is simply false."))

I.append(q(20, "single", "hard",
 "X₁,…,Xₙ are iid uniform on (0, θ) and H₀: θ = θ₀ is tested against H₁: θ ≠ θ₀. The exact distribution of −2 log λ under H₀ is:",
 ["chi-square with 1 degree of freedom, exactly",
  "chi-square with 1 degree of freedom, only asymptotically",
  "chi-square with 2 degrees of freedom, exactly",
  "not a chi-square distribution for any degrees of freedom"],
 "C",
 "Here λ = (X₍ₙ₎/θ₀)ⁿ. Writing U = X₍ₙ₎/θ₀, which has distribution function uⁿ on (0,1), the variable −n log U is exponential with mean 1, so −2 log λ = 2(−n log U) is twice an exponential with mean 1 — a chi-square with 2 degrees of freedom, exactly, for every n. The naive application of Wilks' theorem would give 1 degree of freedom and is wrong, because the support depends on θ and the MLE sits on the boundary."))

# A pool whose keys pile onto one letter rewards a guesser, and the validator caps any
# letter at 40%. Swapping positions i and j is its own inverse, so an "option X" mention
# inside an explanation just swaps the same two letters.
LET = "ABCD"
WANT = {"inf-t10-m-01": "C", "inf-t10-m-03": "D", "inf-t10-m-05": "D",
        "inf-t10-m-08": "C", "inf-t10-m-11": "D", "inf-t10-m-14": "A",
        "inf-t10-m-16": "C", "inf-t10-m-18": "D", "inf-t10-m-19": "A"}

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
 "moduleId": "inference", "topicId": "inference-t10", "source": "mastery",
 "label": "Likelihood ratio test and Wilks — mastery test (unseen)",
 "count": len(I), "items": I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(LES, f, ensure_ascii=False, indent=1)
with io.open(POOL, "w", encoding="utf-8") as f:
    json.dump(POOLD, f, ensure_ascii=False, indent=1)

print("wrote %s: %d scenes (%d core), estMin %d" % (OUT, len(S), len(CORE), LES["estMin"]))
print("wrote %s: %d items" % (POOL, len(I)))
