#!/usr/bin/env python3
# Mastery pool for 4.8 — decision theory: loss, risk, admissibility, minimax.
# Twenty unseen items, 6 easy / 10 moderate / 4 hard.
#
# Every figure computed, not quoted:
#   n=4   a=1,   estimator (x+1)/6,     risk 1/36 = 0.027778; MLE worst 1/16 = 0.0625
#   n=9   a=1.5, estimator (x+1.5)/12,  risk 1/64 = 0.015625; MLE worst 1/36 = 0.027778
#   n=16  a=2,   estimator (x+2)/20,    risk 1/100 = 0.01;    MLE worst 1/64 = 0.015625
#   n=25  a=2.5, estimator (x+2.5)/30,  risk 1/144 = 0.006944; MLE worst 1/100 = 0.01
#   n=16 risk crossings: p(1-p)/16 = 1/100 -> p = 0.2 and 0.8 (discriminant 0.36)
#   n=9  risk crossings: p = (1 +- sqrt 0.4375)/2 = 0.169281 and 0.830719
#   weighted absolute loss, k1 under and k2 over -> the k1/(k1+k2) posterior quantile
import json, io, collections

I = []
def q(n, fmt, diff, stem, opts, ans, expl, **kw):
    it = dict(id="inference-t8-m-%02d" % n, format=fmt, topic="inference-t8", diff=diff,
              stem=stem, options=opts, answer=ans, explanation=expl)
    it.update(kw); I.append(it)

# ------------------------------------------------------------------ easy (6)
q(1, "single", "easy",
  "The risk of a decision rule δ is:",
  ["A single number summarising its quality",
   "The loss incurred at the observed sample",
   "The expected loss averaged over a prior for θ",
   "The expected loss over the sampling distribution, as a function of θ"], "D",
  "R(θ, δ) = E_θ[L(θ, δ(X))] — an expectation over the DATA with θ held fixed, so it is a function of θ. The "
  "averaged-over-a-prior option describes Bayes risk, which is a single number, and the loss at the observed sample "
  "is the loss itself, before any expectation is taken at all.")

q(2, "single", "easy",
  "A decision rule δ₂ is inadmissible if:",
  ["Some rule has risk no larger at every θ and strictly smaller at some θ",
   "Its risk is not constant in θ",
   "It is not a Bayes rule for any prior",
   "Its worst-case risk exceeds that of some other rule"], "A",
  "That is the definition of being dominated. Non-constant risk is irrelevant to admissibility, and having a larger "
  "worst case than another rule only means you are not minimax — a rule can lose on the worst case and still be "
  "admissible, because the other rule may be worse elsewhere.")

q(3, "single", "easy",
  "Under squared-error loss, the risk of an estimator equals:",
  ["Its variance", "Its squared bias",
   "Its variance plus its squared bias", "Its variance minus its squared bias"], "C",
  "Risk under squared error is the mean squared error, which decomposes as variance + bias². It reduces to the "
  "variance alone only when the estimator is unbiased — which is why the risk of the sample proportion is just "
  "p(1−p)/n.")

q(4, "single", "easy",
  "A minimax decision rule is one that minimises:",
  ["The average risk over a prior", "The risk at the true parameter value",
   "The variance of the estimator", "The maximum risk over all θ"], "D",
  "Minimax minimises sup_θ R(θ, δ) — the worst case. Minimising the average risk over a prior gives the Bayes rule, "
  "and 'the risk at the true parameter value' is not a usable criterion, since the true value is unknown — that "
  "impossibility is the reason the two collapses of the risk curve exist at all.")

q(5, "numeric", "easy",
  "For X ~ Bin(n, p), the worst-case risk of the maximum likelihood estimator p̂ = X/n under squared-error loss is:",
  ["1/(2n)", "1/(4n)", "1/n", "1/(4n²)"], "B",
  "p̂ is unbiased, so its risk is Var(p̂) = p(1−p)/n, which is largest at p = 0.5 where p(1−p) = 1/4. The worst case "
  "is therefore 1/(4n) — for n = 9 that is 1/36 = 0.0278.",
  check="Maximise p(1−p) first: it peaks at 1/4 when p = 0.5. Then divide by n.")

q(6, "single", "easy",
  "Which relation is used in practice to establish that a rule is minimax?",
  ["A Bayes rule with constant risk is minimax",
   "Every admissible rule is minimax",
   "Every minimax rule is a Bayes rule for the uniform prior",
   "An unbiased rule with minimum variance is minimax"], "A",
  "This is the relation that does the work: it converts minimising a supremum into choosing a prior that flattens the "
  "risk curve. Admissibility does not imply minimaxity, the least favourable prior is generally not uniform, and "
  "minimum-variance unbiasedness is a separate criterion entirely.")

# ------------------------------------------------------------------ moderate (10)
q(7, "numeric", "moderate",
  "For X ~ Bin(16, p) under squared-error loss, the minimax estimator of p and its risk are:",
  ["(x + 2)/20 and 0.0100", "(x + 4)/24 and 0.0156",
   "(x + 2)/18 and 0.0100", "(x + 2)/20 and 0.0156"], "A",
  "With a = √n/2 = 2, the estimator is (x + a)/(n + 2a) = (x + 2)/20 and the constant risk is 1/(4(1 + √n)²) = "
  "1/(4 × 25) = 0.0100. The value 0.0156 is 1/64, which is the MLE's worst case for n = 16, and (x + 2)/18 has the "
  "wrong denominator — it must be n + 2a, not n + a.",
  check="Denominator n + 2a = 16 + 4 = 20, and 1/(4(1+4)²) = 1/100. Both must be right for the option to be.")

q(8, "single", "moderate",
  "The rule 'ignore the data and always report the constant c' under squared-error loss is:",
  ["Inadmissible, because it uses no data",
   "Minimax, because its risk is constant",
   "Admissible, because its risk is zero at θ = c",
   "Neither admissible nor minimax, because its risk is unbounded"], "C",
  "Its risk is (θ − c)², which is zero at θ = c, so no rule can have risk no larger everywhere and strictly smaller "
  "somewhere — it is admissible. Its risk is not constant and is unbounded, so it is certainly not minimax. This is "
  "the standard demonstration that admissibility is a weak criterion.")

q(9, "multi", "moderate",
  "Consider the following statements about the relations between Bayes, minimax and admissible rules.",
  ["A and B only", "A, B and C only", "A and D only", "A, B, C and D"], "C",
  "A and D hold. B is false without a uniqueness qualifier — a minimax rule need not be admissible, though a UNIQUE "
  "one is. C is false too: a Bayes rule is minimax only if its risk is constant, which most Bayes rules are not.",
  statements=["A unique Bayes rule is admissible.",
              "Every minimax rule is admissible.",
              "Every Bayes rule is minimax.",
              "A Bayes rule whose risk is constant in θ is minimax."],
  verdicts={"A": dict(tf=True,  why="The uniqueness is essential; without it the implication can fail."),
            "B": dict(tf=False, why="Minimaxity concerns the worst case only; a unique minimax rule is admissible, but not every one."),
            "C": dict(tf=False, why="Only if its risk is constant. Most Bayes rules have risk that varies with θ."),
            "D": dict(tf=True,  why="A maximum is at least an average, applied once — and the prior is then the least favourable prior.")})

q(10, "numeric", "moderate",
  "For X ~ Bin(9, p), the risk of the MLE and that of the minimax estimator are equal at:",
  ["p = 0.25 and 0.75", "p = 0.1693 and 0.8307", "p = 0.2 and 0.8", "p = 0.5 only"], "B",
  "Set p(1−p)/9 = 1/64, giving p² − p + 9/64 = 0 and p = (1 ± √0.4375)/2 = 0.1693 and 0.8307. The pair 0.2 and 0.8 is "
  "the answer for n = 16, where the equation is p² − p + 0.16 = 0 — a genuine result for the wrong sample size.",
  check="The two roots must be symmetric about 0.5, since p(1−p) is. And at p = 0.5 the MLE's risk is 0.0278 against "
        "0.0156, so they are certainly not equal there.")

q(11, "single", "moderate",
  "For a normal mean with known variance σ², the estimator x̄ has risk σ²/n at every θ. It follows that x̄ is:",
  ["Inadmissible, since shrinkage estimators exist",
   "Minimax only if the prior is normal",
   "Not minimax, because its risk does not depend on θ",
   "Minimax, because its risk is constant"], "D",
  "Constant risk means the worst case equals the everywhere-case, and no rule can better it in the worst case — so "
  "x̄ is minimax. Shrinkage estimators beat it near their target and lose elsewhere, so they do not dominate it in "
  "one dimension, and the option denying minimaxity inverts the argument: constant risk is what makes a rule minimax, "
  "not what disqualifies it.")

q(12, "match", "moderate",
  "Match the criterion in List I with its definition in List II.",
  ["A-III, B-IV, C-I, D-II", "A-I, B-III, C-IV, D-II",
   "A-III, B-I, C-II, D-IV", "A-IV, B-III, C-I, D-II"], "A",
  "Risk is the expected loss over the data for fixed θ; Bayes risk averages that over a prior; a minimax rule "
  "minimises the maximum risk; an admissible rule is one that nothing dominates. Each wrong option moves at least two "
  "pairs, so the mapping must be checked rather than inferred from one entry.",
  check="Separate the two that are quantities (risk, Bayes risk) from the two that are properties of a rule (minimax, "
        "admissible), and the mapping halves.",
  pairs=[["A. Risk", "I. Minimises the maximum risk over θ"],
         ["B. Bayes risk", "II. Not dominated by any other rule"],
         ["C. Minimax rule", "III. Expected loss over the data, for a fixed θ"],
         ["D. Admissible rule", "IV. Risk averaged over a prior for θ"]])

q(13, "numeric", "moderate",
  "For X ~ Bin(4, p) under squared-error loss, the minimax value is:",
  ["0.0625", "0.0278", "0.1250", "0.0156"], "B",
  "The minimax value is 1/(4(1 + √n)²) = 1/(4 × 9) = 1/36 = 0.0278. The value 0.0625 is 1/16, which is the MLE's "
  "worst case 1/(4n) for n = 4 — a correct quantity for the wrong question, and the distractor most candidates pick.",
  check="The minimax value must be strictly below the MLE's worst case of 1/(4n) = 0.0625, so 0.0625 cannot be the "
        "answer and 0.1250 is larger still.")

q(14, "single", "moderate",
  "In decision-theoretic language, a test of hypotheses uses the action space {0, 1} and 0–1 loss. Its risk at a "
  "particular θ is:",
  ["The power of the test", "The size of the test",
   "The probability of an error at that θ", "The expected sample size"], "C",
  "With 0–1 loss the expected loss is the probability of taking the wrong action: the probability of a type I error "
  "for θ in H₀, and of a type II error for θ in H₁. Size is the supremum of the first over H₀ and power is one minus "
  "the second, so both are features of that risk function rather than the risk itself.")

q(15, "multi", "moderate",
  "Consider the following statements about admissibility.",
  ["A and B only", "B and C only", "A, C and D only", "A, B and D only"], "C",
  "A, C and D hold. B is false: the maximum likelihood estimator of a normal mean VECTOR is inadmissible once the "
  "dimension is three or more, which is the most famous inadmissibility result in the subject.",
  statements=["A rule that ignores the data entirely can be admissible.",
              "The maximum likelihood estimator is admissible in every problem.",
              "An unbiased estimator need not be admissible.",
              "Admissibility does not imply minimaxity."],
  verdicts={"A": dict(tf=True,  why="Its risk is zero at one parameter value, so nothing can dominate it."),
            "B": dict(tf=False, why="For a normal mean vector in dimension three or more, a shrinkage estimator dominates it everywhere."),
            "C": dict(tf=True,  why="Unbiasedness is a constraint, not a guarantee of undominatedness."),
            "D": dict(tf=True,  why="A constant rule is admissible and its worst-case risk is unbounded.")})

q(16, "single", "moderate",
  "The least favourable prior in a minimax problem is best described as:",
  ["The prior against which the best achievable Bayes risk is largest",
   "The prior that a cautious statistician would actually believe",
   "The uniform prior over the parameter space",
   "The prior that minimises the Bayes risk of the minimax rule"], "A",
  "It names the hardest problem in the family — the prior maximising the minimum achievable Bayes risk — and solving "
  "that one problem solves the minimax problem. It is a device rather than a belief, and it is generally not uniform: "
  "for the binomial problem it is Beta(√n/2, √n/2).")

# ------------------------------------------------------------------ hard (4)
q(17, "numeric", "hard",
  "Under the loss L(θ, a) = 3(θ − a) for a < θ and (a − θ) for a ≥ θ, the Bayes rule is:",
  ["The posterior median", "The posterior mean",
   "The 0.25 quantile of the posterior", "The 0.75 quantile of the posterior"], "D",
  "This is weighted absolute-error loss with k₁ = 3 for under-estimation and k₂ = 1 for over-estimation, and the Bayes "
  "rule is the k₁/(k₁ + k₂) quantile — here 3/4. Under-estimating is the costlier error, so the estimate must move "
  "ABOVE the median; the 0.25 quantile is the answer with the weights transposed, which is the error the options are "
  "built around.",
  check="Equal weights must give the median, and 1/(1+1) = 1/2 ✓. Then check the direction: costlier under-estimation "
        "pushes the estimate up.")

q(18, "single", "hard",
  "A rule has perfectly constant risk σ² for every θ, and is not minimax. Which explanation is correct?",
  ["Constant risk is sufficient for minimaxity, so the premise is impossible",
   "Constant risk is only sufficient alongside the rule being a Bayes rule, and this one is not",
   "The risk must be constant AND small for the rule to be minimax",
   "Minimaxity requires the risk to be constant and the loss to be bounded"], "B",
  "The relation has two conditions: a BAYES rule with constant risk is minimax. 'Always report x₁' has constant risk "
  "σ², is flat as anything, and is dominated by x̄ for every n > 1 — so flatness alone proves nothing. The third "
  "option is not a theorem, because 'small' is not a defined condition, and boundedness of the loss is not required.")

q(19, "numeric", "hard",
  "For X ~ Bin(25, p), by what factor does the MLE's worst-case risk exceed the minimax value?",
  ["1.20", "1.44", "1.78", "2.25"], "B",
  "The MLE's worst case is 1/(4n) = 1/100 = 0.0100 and the minimax value is 1/(4(1 + √n)²) = 1/(4 × 36) = 1/144 = "
  "0.006944. The ratio is 144/100 = 1.44. In general the factor is (1 + √n)²/n, which equals 1.78 for n = 9 and "
  "approaches 1 as n grows — the minimax rule's advantage is a small-sample phenomenon.",
  check="The general factor is (1+√n)²/n = (1 + 1/√n)². For n = 25 that is (1 + 0.2)² = 1.44.")

q(20, "single", "hard",
  "Two rules have identical risk at every value of θ. Which conclusion is correct?",
  ["Each dominates the other, so both are inadmissible",
   "They must be the same rule",
   "Both must be minimax",
   "Neither dominates the other, so the admissibility of one says nothing about the other"], "D",
  "Domination requires risk no larger everywhere AND strictly smaller somewhere; identical risk fails the second "
  "condition in both directions, so neither dominates. They need not be the same rule — two different rules can be "
  "risk-equivalent — and whether either is minimax depends on whether that common risk has the smallest achievable "
  "supremum, which identical risk alone does not establish.")

BODY = dict(moduleId="inference", source="mastery", topicId="inference-t8",
            label="Decision Theory: Loss, Risk, Admissibility and Minimax — mastery test (unseen)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/inference_t8_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I); k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s" % dict(d))
print("  keys       %s" % dict(k))
print("  formats    %s" % dict(f))
