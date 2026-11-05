#!/usr/bin/env python3
# Mastery pool for 4.7 — Bayesian estimation and conjugate priors.
# Twenty unseen items, 6 easy / 10 moderate / 4 hard.
#
# Every numerical answer here was computed and cross-checked before being written:
#   Beta(2,3)+5/8 -> Beta(7,6);  Gamma(2,1)+Poisson(Sx=10,n=5) -> Gamma(12,6), mean 2;
#   Beta(1,1)+9/10 -> mean 10/12 = 0.8333, mode 0.9;  Normal tau2=4, s2=9, n=3 ->
#   precision 0.58333, variance 12/7 = 1.7143;  Beta(3,7) with n=40 -> w = 0.2;
#   Gamma(2,3)+exp(n=10,Sx=5) -> Gamma(12,8), mean 1.5, mode 1.375, median approx
#   1.4583 against an exact 1.4585;  Laplace with 10 of 10 -> 11/12 = 0.9167;
#   Beta(8,3) -> mean 0.7273, mode 0.7778.
# The Gamma is in the RATE parameterisation throughout, and every item says so where
# it could matter.
import json, io, collections

I = []
def q(n, fmt, diff, stem, opts, ans, expl, **kw):
    it = dict(id="inference-t7-m-%02d" % n, format=fmt, topic="inference-t7", diff=diff,
              stem=stem, options=opts, answer=ans, explanation=expl)
    it.update(kw); I.append(it)

# ------------------------------------------------------------------ easy (6)
q(1, "numeric", "easy",
  "A Beta(2, 3) prior is used for a success probability θ. In 8 independent trials, 5 successes are observed. The "
  "posterior distribution is:",
  ["Beta(7, 6)", "Beta(7, 11)", "Beta(5, 3)", "Beta(10, 6)"], "A",
  "Beta(α + x, β + n − x) = Beta(2 + 5, 3 + 8 − 5) = Beta(7, 6). The option Beta(7, 11) is what you get by adding n "
  "rather than n − x to the second parameter, which is the standard slip; Beta(10, 6) adds n to the first parameter "
  "instead of x.",
  check="First parameter takes the successes, second takes the failures. 2+5 = 7 and 3+3 = 6, and the two parameters "
        "must sum to α+β+n = 13.")

q(2, "single", "easy",
  "Under squared-error loss, the Bayes estimator of a parameter is:",
  ["The posterior mode", "The posterior median", "The maximum likelihood estimate", "The posterior mean"], "D",
  "Squared-error loss gives the posterior mean, absolute-error loss the posterior median, and 0–1 loss the posterior "
  "mode. The MLE is not a Bayes estimator at all, though it coincides with the posterior mode when the prior is flat.")

q(3, "single", "easy",
  "In the expression posterior ∝ likelihood × prior, the omitted denominator ∫ f(x | θ) π(θ) dθ is omitted because it:",
  ["Is always equal to one",
   "Cannot be computed for conjugate families",
   "Depends only on the prior and not on the data",
   "Does not depend on θ and so only normalises"], "D",
  "The marginal, or prior predictive, is a constant in θ, so it cannot change the shape of the posterior — only its "
  "scale. It is generally not equal to one, it is precisely in the conjugate case that it CAN be computed, and it "
  "depends on both the prior and the data.")

q(4, "numeric", "easy",
  "A Gamma(2, 1) prior in the rate parameterisation is used for a Poisson mean λ. A sample of n = 5 gives Σxᵢ = 10. "
  "The posterior mean is:",
  ["1.67", "2.40", "2.00", "1.20"], "C",
  "The Poisson update gives Gamma(α + Σxᵢ, β + n) = Gamma(12, 6), with mean 12/6 = 2.00. Here it happens to equal the "
  "MLE of Σx/n = 2 exactly, because the prior mean α/β = 2 is also 2 — a useful reminder that the posterior mean is a "
  "weighted average of two numbers and coincides with both when they agree.",
  check="Gamma(A, B) in rate form has mean A/B. The posterior mean must lie between the prior mean 2 and the MLE 2, so "
        "it can only be 2.")

q(5, "single", "easy",
  "Which prior family is conjugate to the binomial likelihood?",
  ["Gamma", "Normal", "Inverse-Gamma", "Beta"], "D",
  "Beta is conjugate to the binomial, because the Beta kernel θ^(α−1)(1−θ)^(β−1) has the same algebraic shape as the "
  "binomial likelihood in θ. Gamma is conjugate to the Poisson and the exponential, Normal to a normal mean with known "
  "variance, and Inverse-Gamma to a normal variance with the mean known.")

q(6, "single", "easy",
  "A 95% credible interval (a, b) licenses the statement:",
  ["95% of intervals constructed this way would contain θ",
   "The sample mean lies in (a, b) with probability 0.95",
   "θ lies in (a, b) in 95% of future samples",
   "θ lies in (a, b) with probability 0.95, given the data and the prior"], "D",
  "A credible interval is a probability statement about θ conditional on the data. The repeated-sampling option — 95% "
  "of intervals constructed this way would contain θ — is the correct reading of a CONFIDENCE interval, which is a "
  "statement about the procedure rather than about the parameter, and attaching it to a credible interval, or the "
  "reverse, is the error this topic is built to catch.")

# ------------------------------------------------------------------ moderate (10)
q(7, "numeric", "moderate",
  "With a uniform prior on θ and 9 successes in 10 trials, the Bayes estimate under squared-error loss is:",
  ["0.9000", "0.8333", "0.9167", "0.8182"], "B",
  "A uniform prior is Beta(1, 1), so the posterior is Beta(10, 2) with mean 10/12 = 0.8333 — Laplace's rule of "
  "succession, (x + 1)/(n + 2). The value 0.9000 is the MLE, which equals the posterior MODE under a flat prior but "
  "not the posterior mean, and that distinction is the whole point of the question.",
  check="Flat prior: posterior mode = MLE, posterior mean = (x+1)/(n+2). The question names squared-error loss, so it "
        "wants the mean.")

q(8, "single", "moderate",
  "A Gamma(α, β) prior in rate form is used for the rate λ of an exponential sample x₁,…,xₙ. The posterior is:",
  ["Gamma(α + Σxᵢ, β + n)", "Gamma(α + n, β + n)",
   "Gamma(α + Σxᵢ, β + Σxᵢ)", "Gamma(α + n, β + Σxᵢ)"], "D",
  "For the exponential, the sample SIZE adds to the shape and the TOTAL TIME adds to the rate: Gamma(α + n, β + Σxᵢ). "
  "The first option is the Poisson update, where the roles are reversed — the sum goes to the shape and n to the rate. "
  "These two cases are mirror images and this is the most productive confusion in the topic.")

q(9, "multi", "moderate",
  "Consider the following statements about conjugate updating.",
  ["A and B only", "A, B and C only", "A, C and D only", "A, B, C and D"], "C",
  "A, C and D hold. B is false: in the Normal–Normal case it is the PRECISIONS that add, not the variances — indeed "
  "the posterior variance must be smaller than both inputs, since adding information cannot increase uncertainty.",
  statements=["Conjugacy is a property of the prior-likelihood pair, not of the prior alone.",
              "In the Normal–Normal case with known variance, the posterior variance is the sum of the prior variance "
              "and σ²/n.",
              "The posterior mean in the Beta–Binomial case lies between the prior mean and the MLE.",
              "Deriving a conjugate posterior requires no integration."],
  verdicts={"A": dict(tf=True,  why="Beta is conjugate to the binomial and to nothing else in this syllabus."),
            "B": dict(tf=False, why="Precisions add: 1/σₙ² = 1/τ² + n/σ². The posterior variance is below both τ² and σ²/n."),
            "C": dict(tf=True,  why="It is a weighted average of the two, with weight (α+β)/(α+β+n) on the prior mean."),
            "D": dict(tf=True,  why="Multiply the two kernels, add the exponents, recognise the family. That is the whole point of conjugacy.")})

q(10, "numeric", "moderate",
  "A prior μ ~ N(μ₀, 4) is used for a normal mean with known variance σ² = 9. A sample of n = 3 is taken. The posterior "
  "variance is:",
  ["7.0000", "1.7143", "3.0000", "0.5833"], "B",
  "Precisions add: 1/4 + 3/9 = 0.25 + 0.3333 = 0.5833, so the posterior variance is 1/0.5833 = 1.7143, or exactly 12/7. "
  "The value 0.5833 is the posterior PRECISION, offered because candidates stop one step early, and 7.0000 adds the "
  "two variances, which is the error the arithmetic is designed to expose.",
  check="The posterior variance must be below both the prior variance 4 and σ²/n = 3. Only 1.7143 passes that test.")

q(11, "single", "moderate",
  "Jeffreys' prior for the success probability p of a Bernoulli trial is proportional to:",
  ["p^(−½)(1 − p)^(−½)", "1 on (0, 1)", "p(1 − p)", "p^(−1)(1 − p)^(−1)"], "A",
  "Jeffreys' prior is ∝ √I(θ), and for a Bernoulli I(p) = 1/(p(1−p)), so the prior is ∝ p^(−½)(1−p)^(−½) — the "
  "Beta(½, ½) kernel. Note that this puts MORE mass near 0 and 1 than the uniform prior does, so a non-informative "
  "prior is not the same thing as one that pulls towards the middle.")

q(12, "match", "moderate",
  "Match the item in List I with its counterpart in List II.",
  ["A-III, B-IV, C-I, D-II", "A-I, B-III, C-IV, D-II",
   "A-III, B-I, C-IV, D-II", "A-IV, B-III, C-I, D-II"], "A",
  "Squared-error loss gives the posterior mean; absolute-error loss the posterior median; 0–1 loss the posterior mode; "
  "and the Gamma family is conjugate to the Poisson likelihood. Each wrong option moves at least two pairs, so the "
  "mapping has to be checked rather than inferred from one recognised entry.",
  check="Fix the three losses first — mean, median, mode in that order — and the fourth pair follows by elimination.",
  pairs=[["A. Squared-error loss", "I. The posterior mode"],
         ["B. Absolute-error loss", "II. Conjugate to the Poisson likelihood"],
         ["C. 0–1 loss", "III. The posterior mean"],
         ["D. The Gamma family", "IV. The posterior median"]])

q(13, "numeric", "moderate",
  "A Beta(3, 7) prior is combined with a sample of n = 40 trials. The weight the posterior mean places on the prior "
  "mean is:",
  ["0.7500", "0.2000", "0.8000", "0.0750"], "B",
  "The weight is (α + β)/(α + β + n) = 10/(10 + 40) = 0.2000. Read it as a share of a pooled sample: the prior carries "
  "ten observations' worth of opinion against forty real observations, so it gets one fifth of the weight. The option "
  "0.8000 is the weight on the MLE, which is the complement.",
  check="The weight on the prior plus the weight on the MLE must be 1, and with n four times α+β the prior share has "
        "to be 1/5.")

q(14, "single", "moderate",
  "With a uniform prior on a probability, the maximum likelihood estimate coincides exactly with:",
  ["The posterior mode", "The posterior mean",
   "The posterior median", "All three posterior summaries"], "A",
  "A flat prior makes the posterior proportional to the likelihood, so the posterior is maximised where the likelihood "
  "is — the posterior MODE equals the MLE. The posterior mean is (x + 1)/(n + 2), a different number, and the three "
  "summaries coincide only when the posterior is symmetric, which Beta(1 + x, 1 + n − x) generally is not.")

q(15, "multi", "moderate",
  "Consider the following statements about interval estimates.",
  ["A and B only", "B and C only", "A, B and D only", "A, C and D only"], "C",
  "A, B and D hold. C is false: the HPD interval is the SHORTEST set of the required posterior probability, so for a "
  "skewed posterior it is strictly shorter than the equal-tailed interval, not longer; the two coincide only when the "
  "posterior is symmetric and unimodal.",
  statements=["A credible interval is a probability statement about the parameter given the data.",
              "A confidence interval is a statement about the procedure under repeated sampling.",
              "For a skewed posterior the HPD interval is longer than the equal-tailed interval.",
              "A credible interval and a confidence interval converge as the sample size grows with the prior fixed."],
  verdicts={"A": dict(tf=True,  why="P(θ ∈ C | x) = 0.95, which is the statement people wrongly make about confidence intervals."),
            "B": dict(tf=True,  why="95% of such intervals would cover the fixed θ; nothing is asserted about the one in hand."),
            "C": dict(tf=False, why="The HPD is the shortest such set by construction, so it is never longer — equal only under symmetry."),
            "D": dict(tf=True,  why="The weight on the prior tends to zero and the posterior variance approaches σ²/n.")})

q(16, "single", "moderate",
  "For the conjugate families in the syllabus, the posterior mean is always:",
  ["Between the prior mean and the MLE", "Equal to the MLE",
   "Equal to the prior mean", "Outside the range of the prior mean and the MLE"], "A",
  "It is a weighted average of the prior mean and the MLE with weights summing to one, so it must lie between them, "
  "coinciding with one only if the two already agree or a weight is zero. Note the qualifier: this is a property of "
  "these conjugate families, not a general theorem about Bayesian estimation.")

# ------------------------------------------------------------------ hard (4)
q(17, "numeric", "hard",
  "A Gamma(2, 3) prior in rate form is used for the rate λ of an exponential sample with n = 10 and Σxᵢ = 5. Under "
  "0–1 loss, the Bayes estimate of λ is:",
  ["1.5000", "1.3750", "1.4583", "2.0000"], "B",
  "The exponential update gives Gamma(α + n, β + Σxᵢ) = Gamma(12, 8). Under 0–1 loss the estimate is the posterior "
  "MODE, (A − 1)/B = 11/8 = 1.3750. The value 1.5000 is the posterior mean, which squared-error loss would give, and "
  "1.4583 is the posterior median for absolute-error loss — all three are in the options because the question turns on "
  "which loss was named.",
  check="For a right-skewed Gamma the order is mode < median < mean: 1.3750 < 1.4583 < 1.5000. 0–1 loss wants the "
        "smallest of the three.")

q(18, "numeric", "hard",
  "Ten items are tested and all ten pass. Using a uniform prior and squared-error loss, the Bayes estimate of the pass "
  "probability is:",
  ["1.0000", "0.9545", "0.9167", "0.9091"], "C",
  "The posterior is Beta(1 + 10, 1 + 0) = Beta(11, 1), with mean 11/12 = 0.9167 — Laplace's rule of succession. The "
  "MLE of 1.0000 asserts that failure is impossible on the strength of ten trials, which is the practical argument for "
  "not reporting it; 0.9545 is the Jeffreys-prior answer, 21/22, and 0.9091 is 10/11, which is neither.",
  check="(x+1)/(n+2) = 11/12. Any estimate of exactly 1 should be suspected: no finite sample can rule out failure.")

q(19, "single", "hard",
  "A statement reads: 'Because the Bayes estimator under squared-error loss is biased in the frequentist sense, it is "
  "inferior to the unbiased estimator.' What is wrong with it?",
  ["The Bayes estimator under squared-error loss is in fact unbiased",
   "Bias is irrelevant because Bayesian estimators are not random variables",
   "The two optimise different criteria, so bias does not establish inferiority",
   "Nothing is wrong; unbiasedness is the stronger requirement"], "C",
  "The premise is correct — a Bayes estimator generally is biased — but the inference is not. The Bayes estimator "
  "minimises expected posterior loss, and shrinking towards the prior mean buys a variance reduction at the cost of "
  "bias, which can lower mean squared error overall. Unbiasedness is a constraint, not a measure of quality, and "
  "declaring one estimator inferior requires first naming the criterion.")

q(20, "single", "hard",
  "A posterior is Beta(8, 3). A question asks for the Bayes estimate without naming a loss function. The best answer, "
  "and the reason, is:",
  ["0.7778, because the mode is the most probable value",
   "0.7273, because the posterior mean is the convention when no loss is stated",
   "Either, because for a Beta posterior the mean and mode coincide",
   "Neither, because the question cannot be answered without the loss"], "B",
  "Beta(8, 3) has mean 8/11 = 0.7273 and mode 7/9 = 0.7778, so the option claiming the two coincide is wrong on the "
  "arithmetic. The honest position is that 'the Bayes estimator' is undefined until a loss is "
  "named — but the convention in every syllabus and examination is squared-error loss, so the posterior mean is the "
  "expected answer, and refusing to answer would lose the mark.")

BODY = dict(moduleId="inference", source="mastery", topicId="inference-t7",
            label="Bayesian Estimation and Conjugate Priors — mastery test (unseen)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/inference_t7_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I); k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s" % dict(d))
print("  keys       %s" % dict(k))
print("  formats    %s" % dict(f))
