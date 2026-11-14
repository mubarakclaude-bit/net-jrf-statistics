# Statistical Inference independent mathematical verification — 2026-11-14

## Scope and repository state

- Repository: `mubarakclaude-bit/net-jrf-statistics`
- Base branch: `main`
- Base commit at branch creation: `b78be4bf68a02029d4c906a9afa760eb54aec40f`
- Task branch: `audit/inference-independent-verification-2026-11-14`
- Catalog source: `seed/catalog.json`
- Catalog count: 17 Statistical Inference topics.
- T9 is deliberately excluded from edits and independent verification in this branch because open draft PR #93 already changes `seed/lesson_t9.json` and adds a T9 verifier. No other inference lesson/mastery files were listed in PR #93's changed-file list.
- No application code, shared manifests, workflow configuration, Claude artifacts/services, or deployment settings were changed.

## Topic-by-topic status

Status describes the mathematical audit of current lesson material and available mastery pools. A manual first-pass review has now covered all 20 items in each of the 16 available non-T9 pools (320 items total), alongside independent calculations and automated checks. This is not a formal proof of every possible distractor or theorem nuance; the verifier checks repeatable calculations, structure and multi-statement key consistency.

| Topic | Catalog subject | Status | Notes |
|---|---|---|---|
| T1 | Sufficiency, factorisation, minimal sufficiency | CLARIFIED | Mastery item now states the closed-endpoint Uniform convention consistently with its boundary likelihood |
| T2 | Completeness, exponential families, ancillarity, Basu | PASS — first pass | Poisson/Bernoulli completeness arguments, Uniform range counterexample and Basu conditions checked |
| T3 | Rao–Blackwell and Lehmann–Scheffé | PASS — first pass | Poisson and Bernoulli UMVUE derivations, variance comparisons and transformation traps checked |
| T4 | MLE: computation, invariance, properties | POOL CORRECTED; LESSON BLOCKED | All 20 mastery items reviewed; corrected the rounded UMVUE value in `mle-m-12` (INF-033). Catalog entry and pool exist, but `seed/lesson_t4.json` is absent from current main |
| T5 | Method of moments, minimum chi-square, least squares | CORRECTED | Uniform MOM items now distinguish the parameter space, sample-compatible region and decision-theoretic admissibility |
| T6 | Cramér–Rao bound and Fisher information | PASS — first pass | Bernoulli, Poisson, normal and function-of-parameter bounds checked; equality-to-UMVUE wording now requires attainment throughout the model |
| T7 | Bayesian estimation and conjugate priors | CORRECTED | Normal–normal posterior corrected; HPD equality and Bayesian/frequentist asymptotic claims qualified; squared-error convention made explicit; Gamma posterior median rounding corrected; see INF-001, INF-016, INF-020 and INF-030 |
| T8 | Decision theory: loss, risk, admissibility, minimax | CORRECTED | Normal-mean minimax explanation states the lower bound; Bayes-rule admissibility is qualified by prior support and regularity; constant risk alone is not treated as sufficient |
| T9 | Neyman–Pearson, MLR, UMP | DEFERRED | Conflicts with open draft PR #93; left untouched |
| T10 | Likelihood ratio test and Wilks | CORRECTED | General likelihood-ratio range now includes zero consistently in both pool explanations |
| T11 | SPRT | CORRECTED | Wald boundary/intercept explanations corrected; average-sample-size advantage no longer promises a fixed factor; see INF-005, INF-006 and INF-023 |
| T12 | Size and power computation | CORRECTED | Power key corrected; size is distinguished from the preselected significance level; see INF-002 and INF-024 |
| T13 | Confidence intervals and pivots | CORRECTED | Variance-interval endpoint rounding and Uniform-pivot interval explanation corrected; see INF-003, INF-007 and INF-025 |
| T14 | Chi-square goodness of fit | CORRECTED | Poisson tail pooling explanation corrected; statistic and df independently recomputed; see INF-004 |
| T15 | Choosing the right test | CORRECTED | Corrected p-value/data mismatch and sign/Wilcoxon target; qualified family-wise error, robustness and interval interpretation; corrected post-hoc Bonferroni guidance; see INF-008, INF-009 and INF-026–INF-029 |
| T16 | Contingency tables: independence and homogeneity | CORRECTED | Expected counts, Pearson/Yates statistics and df checked; significance/practical-magnitude wording clarified; see INF-015 |
| T17 | UMP unbiased and UMP invariant tests | CORRECTED | Exponential-rate one-sided direction/cutoffs checked; equal-tail symmetry condition qualified; see INF-014 |

## Confirmed errors and corrections

### INF-001 — Incorrect normal–normal posterior in T7

File: `seed/lesson_t7.json`, scene `s6`, completion step 4. Severity: **Major**.

Given prior μ ~ N(50, 16), known sampling variance σ² = 8, n = 4 and x-bar = 56:

- Prior precision = 1/16.
- Data precision = n/σ² = 4/8 = 1/2.
- Posterior precision = 1/16 + 1/2 = 9/16.
- Posterior variance = **16/9 = 1.7778**, not 8/3.
- Posterior mean = [(50/16) + (4×56/8)] / (9/16) = **166/3 = 55.3333**, not 55.

The completion answer was corrected.

### INF-002 — Incorrect mastery answer key in T12

File: `seed/inference_t12_mastery.json`, item `inf-t12-m-10`. Severity: **Major**.

For n = 25, σ = 10, H0: μ = 50, H1: μ = 54, upper-tail size 0.05:

- Critical boundary = 50 + 1.645(10/5) = 53.29.
- Power = P(X-bar > 53.29 | μ = 54) = P(Z > -0.355) = **0.6387**.
- 0.6387 is option **A**, but the stored key was D (0.8023).

The answer key was corrected from D to A. The existing explanation's numerical calculation already supported A.

### INF-003 — Variance confidence interval rounding in T13

Files: `seed/lesson_t13.json`, scene `s8`; `seed/inference_t13_mastery.json`, item `inf-t13-m-10`. Severity: **Minor**.

Using sum of squares 36 and supplied chi-square points 19.023 and 2.700:

- Lower endpoint = 36/19.023 = 1.892446, displayed as 1.892.
- Upper endpoint = 36/2.700 = **13.333333**, displayed as 13.333, not 13.331.
- Square-root interval = **(1.376, 3.651)** to three decimals.

The lesson and mastery option/explanation were corrected.

### INF-004 — Contradictory Poisson pooling explanation in T14

Files: `seed/lesson_t14.json`, scene `s6`; `seed/inference_t14_mastery.json`, item `inf-t14-m-18`. Severity: **Minor**.

For the 100-shift Poisson example, λ-hat = 0.93. Expected frequencies are approximately 39.455, 36.693, 17.062, 5.289, 1.230 and 0.270 for 0, 1, 2, 3, 4 and 5+ events.

- The expected frequency for 3 is **5.289**, slightly above 5; it is not below 5.
- Expected frequencies for 4 and 5+ are below 5.
- Pooling the upper tail as 3+ gives expected frequency approximately **6.789** and observed frequency 8.
- The independently recomputed statistic is approximately **0.752**, with df = 4 pooled classes - 1 - 1 estimated parameter = **2**.

The wording now explains the threshold correctly and identifies 3+ as a broader upper-tail pooling choice rather than claiming the class 3 expectation is below 5.

### INF-005 — SPRT boundary-constant explanation contradicted the answer key

File: `seed/inference_t11_mastery.json`, item `inf-t11-m-04`. Severity: **Minor**.

The keyed option C correctly gives A = (1 − β)/α = 18 and B = β/(1 − α) = 0.10526 for α = 0.05 and β = 0.10. The explanation incorrectly claimed that option C used the wrong formula. The explanation was rewritten to identify option C as correct and accurately explain the distractors.

### INF-006 — SPRT boundary intercepts omitted dependence on hypotheses

File: `seed/inference_t11_mastery.json`, item `inf-t11-m-09`. Severity: **Major**.

For Bernoulli SPRT boundaries, a = log(A)/k and b = −log(B)/k, where A and B depend on α and β, while k = log[p₁(1 − p₀)/(p₀(1 − p₁))] depends on the two hypotheses. Therefore both intercepts depend on BOTH the hypotheses and the error rates. The old answer “the two error rates only” was wrong, and the original options did not contain a correct answer. The options and key were corrected to include “both the hypotheses and the two error rates.”

### INF-007 — Residual variance-to-standard-deviation interval rounding in T13

File: `seed/inference_t13_mastery.json`, item `inf-t13-m-16`. Severity: **Minor**.

The item still quoted the superseded variance endpoint 13.331 and rounded √1.892 down to 1.375. Using the corrected interval endpoint 13.333, the standard-deviation interval is (1.376, 3.651) to three decimals. The stem, option and explanation were aligned with those values.

### INF-008 — Reported p-value inconsistent with the stated effect and standard error in T15

File: `seed/inference_t15_mastery.json`, item `inf-t15-m-12`. Severity: **Major**.

The stem reported p = 0.001 for a difference of 0.02, n = 10,000 and σ = 1. The standard error is 0.01, so z = 2 and the two-sided p-value is approximately **0.0455**, not 0.001. The confidence interval already shown in the explanation, (0.0004, 0.0396), also corresponds to z = 2. The stem was corrected to p = 0.0455 and the explanation/verdict now describe significance at the 5% level without claiming that significance proves a real effect.

### INF-009 — Sign/Wilcoxon procedures incorrectly presented as distribution-free tests of a skewed mean

File: `seed/inference_t15_mastery.json`, item `inf-t15-m-20`. Severity: **Major**.

The question asked for a test of the population mean with only eight clearly skewed observations, but keyed a sign or Wilcoxon signed-rank procedure. The sign test targets a median; the signed-rank test targets a symmetric location parameter, not the mean under arbitrary skewness. The keyed option was rewritten to state that the supplied information does not justify a standard test of the mean and that additional data or modelling assumptions are needed.

### INF-010 — T8 minimax explanation inferred minimaxity from constant risk alone

File: `seed/inference_t8_mastery.json`, item `inference-t8-m-11`. Severity: **Minor**.

The original explanation said constant risk itself makes a rule minimax, which is false in general and contradicted the same pool's item m-18. The normal-mean sample average is minimax, but the justification also needs the normal location problem's minimax lower bound, which equals σ²/n. The explanation now states that lower bound and explicitly says constant risk alone is not sufficient.

### INF-011 — T5 used “inadmissible” for an estimate outside the sample-compatible parameter region

File: `seed/inference_t5_mastery.json`, item `inf-t5-m-09` and the D-verdict of `inf-t5-m-03`. Severity: **Minor**.

For U(0, θ), the method-of-moments value 2x̄ can fall below the observed maximum. This makes that realised parameter value incompatible with the observed sample under the usual closed-endpoint convention; it does not, by itself, establish decision-theoretic inadmissibility of the estimator. The explanation and verdict were corrected to use sample-feasibility language.

### INF-012 — T1 Uniform boundary convention made explicit

File: `seed/inference_t1_mastery.json`, item `inf-t1-m-06`. Severity: **Clarification**.

The stem used the open-support notation U(0, θ) while the answer treated θ = x₍ₙ₎ as included in the likelihood support. The stem now uses U[0, θ], matching the stated closed-endpoint likelihood convention and the boundary MLE.

### INF-013 — General likelihood-ratio range incorrectly excluded zero in T10

File: `seed/inference_t10_mastery.json`, item `inf-t10-m-02`. Severity: **Minor**.

For a general likelihood-ratio statistic, the null-constrained maximum can be zero when the observed data are impossible under every null parameter value, particularly in models with parameter-dependent support. Since likelihoods are non-negative and the null parameter space is contained in the unrestricted space, the general range is **0 ≤ λ ≤ 1**, not necessarily 0 < λ ≤ 1. The option and explanation were corrected; strict positivity holds when the maximised null likelihood is positive.

### INF-014 — Equal-tail UMPU condition stated as necessary when it is only sufficient

File: `seed/inference_t17_mastery.json`, item `inf-t17-m-13`. Severity: **Minor**.

The original item said an equal-tail two-sided test is UMPU *only* when the null distribution is symmetric. Symmetry about the mean is a sufficient condition for equal tails to satisfy both the size and unbiasedness equations, but it is not necessary in general: an asymmetric distribution may satisfy the moment equation by coincidence. The item was reframed to ask for a sufficient condition, and the explanation now states the distinction explicitly.

### INF-015 — Significant contingency-table result overstated practical magnitude

File: `seed/inference_t16_mastery.json`, item `inf-t16-m-20`. Severity: **Minor**.

The original option said a significant chi-square test establishes that at least one cell departs “appreciably” from independence. Statistical significance alone does not establish practical magnitude, particularly with large samples. The option now says “statistically detectably,” and the explanation distinguishes evidence of association from effect size and notes Cramér's V as a magnitude measure.

### INF-016 — Bayesian interval statements omitted regularity and overstated symmetry requirement

File: `seed/inference_t7_mastery.json`, item `inference-t7-m-15`. Severity: **Minor**.

The original explanation said HPD and equal-tailed intervals coincide only for symmetric unimodal posteriors. Symmetry is sufficient, but not necessary: an equal-tailed interval can also be an HPD interval when its endpoints happen to have equal posterior density. The explanation now states the correct shortest-set property and qualifies the equality case. The asymptotic equivalence claim between Bayesian credible intervals and frequentist confidence intervals is also explicitly tied to standard Bernstein–von Mises conditions, including a fixed prior with positive density near the true parameter.


### INF-017 — T5 confused parameter-space membership with sample compatibility

File: `seed/inference_t5_mastery.json`, item `inf-t5-m-03`. Severity: **Minor**.

For U(0, θ), the method-of-moments estimate 2x̄ is positive and therefore remains in the parameter space θ > 0, even when it is below the observed maximum and hence incompatible with that realised sample. The original statement said it could fall outside the parameter space, while its verdict described sample incompatibility. The statement and verdict now distinguish these concepts.

### INF-018 — T5 answer option called a sample-incompatible MOM estimate “inadmissible”

File: `seed/inference_t5_mastery.json`, item `inf-t5-m-15`. Severity: **Minor**.

The keyed option used “inadmissible” even though the explanation correctly said the issue was sample compatibility, not decision-theoretic domination. The option now says the realised estimate lies outside the sample-compatible parameter region and recommends the boundary MLE with its rationale.

### INF-019 — T6 CRLB equality condition did not state the global requirement for UMVUE status

File: `seed/inference_t6_mastery.json`, item `inf-t6-m-07`. Severity: **Minor**.

Attaining the Cramér–Rao bound at one parameter value does not by itself establish a uniformly minimum-variance unbiased estimator over the model. The statement now requires equality for every θ (under the stated regularity conditions), and its verdict explains the distinction.

### INF-020 — T7 Bayes estimate question omitted its loss convention

File: `seed/inference_t7_mastery.json`, item `inference-t7-m-20`. Severity: **Clarification**.

A Bayes estimator is defined relative to a loss function; without one, the posterior mean is not universally implied. The stem now explicitly invokes the module's squared-error-loss convention, and the explanation says this is a convention rather than a general Bayesian theorem.

### INF-021 — T8 stated Bayes-rule admissibility without prior-support conditions

File: `seed/inference_t8_mastery.json`, item `inference-t8-m-09`. Severity: **Minor**.

A Bayes rule is not automatically admissible under every prior: a prior that omits parts of the parameter space can fail to penalise improvements there. The statement now gives a standard sufficient condition using a proper full-support prior, finite Bayes risk and regularity; the verdict no longer implies uniqueness alone is enough.

### INF-022 — T10 repeated an obsolete strict-positive likelihood-ratio range

File: `seed/inference_t10_mastery.json`, item `inf-t10-m-12`. Severity: **Minor**.

The pool's item m-02 had correctly established 0 ≤ λ ≤ 1, including λ = 0 when the null likelihood vanishes. Item m-12's explanation still said 0 < λ ≤ 1. Its explanation and verdict now use the general non-negative range consistently.

### INF-023 — T11 overstated the SPRT's average sample-size reduction as a fixed factor

File: `seed/inference_t11_mastery.json`, item `inf-t11-m-15`. Severity: **Minor**.

The SPRT can substantially reduce average sample size, but “about half” is not a universal guarantee. The option now says it *can* require substantially fewer observations, and the explanation confines the roughly-half comparison to the numerical example in this pool.

### INF-024 — T12 conflated the chosen significance level with the realised test size

File: `seed/inference_t12_mastery.json`, item `inf-t12-m-12`. Severity: **Minor**.

For a discrete test the actual size may be below the target level. The statement now says the significance level α is chosen before data collection, while the verdict clarifies that actual size is determined by the rejection rule and can be smaller.

### INF-025 — T13 Uniform confidence-interval explanation pointed to the correct option as wrong

File: `seed/inference_t13_mastery.json`, item `inf-t13-m-20`. Severity: **Minor**.

The keyed interval is (X₍ₙ₎, X₍ₙ₎/α^(1/n)); the lower endpoint must be at least the observed maximum. The original explanation incorrectly said the keyed interval ignored that lower constraint. The explanation now derives the interval directly from the pivot and avoids naming the correct option, as required by the repository's self-cited-answer audit.

### INF-026 — T15 described family-wise error inflation as unconditional

File: `seed/inference_t15_mastery.json`, item `inf-t15-m-09`. Severity: **Minor**.

Testing many hypotheses at 0.05 can raise family-wise error above 0.05, but the exact inflation depends on dependence among tests; perfect dependence is an exception. The option now says “can exceed,” and the explanation gives the independent-test examples without implying unconditional inflation.

### INF-027 — T15 overstated what a confidence interval says about practical importance

File: `seed/inference_t15_mastery.json`, item `inf-t15-m-12`. Severity: **Minor**.

A confidence interval quantifies plausible effect sizes and can be compared with a subject-matter threshold; it cannot decide practical importance without that context. The statement and verdict were rewritten to reflect this.

### INF-028 — T15 robustness statement omitted finite-variance and mild-departure qualifications

File: `seed/inference_t15_mastery.json`, item `inf-t15-m-17`. Severity: **Minor**.

The central limit theorem does not guarantee robust small-sample inference under arbitrary heavy tails or severe skewness. The mean-test statement now specifies finite variance and mild departures, and the verdict states the limitation explicitly.

### INF-029 — T15 incorrectly claimed Bonferroni adjustment cannot be applied after seeing the data

File: `seed/inference_t15_mastery.json`, item `inf-t15-m-19`. Severity: **Major**.

Bonferroni family-wise error control remains valid when applied after testing, provided the full family of outcomes searched is included. For five tests and an unadjusted p-value of 0.03, the adjusted p-value is 0.15 (equivalently, compare 0.03 with 0.01), so the result is not significant. The stem, options, key and explanation were rewritten; any undisclosed additional searches must also be included in the family.


### INF-030 — T7 Gamma posterior median was rounded incorrectly

File: `seed/inference_t7_mastery.json`, item `inference-t7-m-17`. Severity: **Minor**.

For the posterior Gamma(12, rate 8), the median is approximately 1.458545, which rounds to **1.4585** to four decimal places, not 1.4583. The option and explanation were corrected; the posterior mean (1.5000) and mode (1.3750) remain unchanged.

### INF-031 — T10 conflated the Neyman–Pearson ratio with a truncated generalized likelihood ratio

File: `seed/inference_t10_mastery.json`, item `inf-t10-m-11`. Severity: **Major**.

For simple H₀ versus simple H₁, the Neyman–Pearson most powerful test rejects for small values of L(θ₀)/L(θ₁). The generalized likelihood-ratio statistic defined elsewhere in the pool as sup over H₀ divided by sup over the full parameter space becomes min(1, L(θ₀)/L(θ₁)) for two disjoint simple hypotheses; it is not a one-to-one transform of the Neyman–Pearson ratio over the full range. The item was rewritten to ask directly for the Neyman–Pearson rejection rule and to explain the distinction.

## Verification implementation

Added `verify_inference_math.py`, a consolidated standard-library verifier with topic-specific unittest groups. It contains independent regression calculations for T1–T8 and T10–T17, including:

- Bernoulli conditional likelihood and normal sufficient-statistic variance reconstruction.
- Poisson/Bernoulli completeness and UMVUE calculations.
- MLE, method-of-moments and OLS examples.
- Fisher information and Cramér–Rao bounds.
- Beta-binomial, Gamma-Poisson and normal-normal posterior calculations.
- Binomial minimax risk.
- Normal likelihood-ratio statistics.
- SPRT boundaries and ASN approximations.
- Exact binomial size/power and sample-size calculation.
- Normal and chi-square confidence intervals.
- Goodness-of-fit, family-wise error and contingency-table statistics.
- Exponential-rate one-sided critical regions.

It also checks:
- The catalog has 17 inference topics.
- Each non-deferred mastery pool has 20 uniquely identified items with valid topic IDs and answer-option labels.
- Multi-statement answer keys agree with their individual true/false verdicts.
- The T4 lesson-file gap is detectable; its 20-item mastery pool has been manually reviewed and the additional `mle-m-12` arithmetic correction is regression-tested.
- The corrected T1, T4, T5, T7, T8, T10, T11, T12, T13, T14, T15, T16 and T17 source values/qualifications remain in place.

### Test execution status

- Independent calculations were recomputed during the audit using exact arithmetic where possible and numerical tolerances for rounded quantities.
- The verifier is at repository root so the existing `tools/run-verifiers.js` CI discovery rule (`verify_*.py` at root) executes it on this PR. It contains 73 regression tests, with the unittest entry point after all test classes so all 70 are discovered when run directly.
- GitHub Actions run #1195 (run ID `43564757724`) completed successfully on commit `3830a2e7cc776f02414d503fbf3e8f964b595aed`: validate, acceptance and browser jobs all passed, including the verifier, build, lesson navigation, hosted storage conformance and feature browser tests.
- Run #1447 (ID `43578350970`) on head `32e03a0` has passed validate and acceptance; the browser job is still running. The latest follow-up corrects a stale Gamma-median check hint and adds T4 pool plus T7 consistency regression guards, so the new head requires its own full green CI run.

## Files changed

Modified:
- `seed/lesson_t7.json`
- `seed/inference_t12_mastery.json`
- `seed/lesson_t13.json`
- `seed/inference_t13_mastery.json`
- `seed/lesson_t14.json`
- `seed/inference_t14_mastery.json`
- `seed/inference_t11_mastery.json`
- `seed/inference_t13_mastery.json`
- `seed/inference_t1_mastery.json`
- `seed/inference_t5_mastery.json`
- `seed/inference_t8_mastery.json`
- `seed/inference_t15_mastery.json`
- `seed/inference_t10_mastery.json`
- `seed/inference_t17_mastery.json`
- `seed/inference_t16_mastery.json`
- `seed/inference_t7_mastery.json`

Added:
- `verify_inference_math.py`
- `audits/statistical_inference_verification_2026-11-14.md`

No other lesson or module files were changed.

## Outstanding limitations and dependencies

1. **T4 content gap:** The catalog and 20-item mastery pool exist, but the lesson JSON is absent from current main. This task does not author a replacement lesson or change catalog/application architecture.
2. **T9 dependency:** T9 is reserved for PR #93. A follow-up should compare that PR's T9 verifier and lesson changes against this audit's scope before integrating.
3. **Mastery key depth:** All available non-T9 pools were checked for item count, IDs, answer labels and multi-statement verdict/key consistency. Manual first-pass review has now covered all 320 items in available non-T9 pools. That review is not a formal proof of every single-choice/numeric key; a second independent reviewer or further item-by-item calculation is still advisable for high-stakes release.
4. **Verifier execution:** Run `python verify_inference_math.py` from a full checkout and resolve any failures before treating the audit as complete.
5. No branch merge, production deployment, Vercel push or workflow/configuration change was made.


### INF-032 — T7's answer hint retained the superseded Gamma posterior median

File: `seed/inference_t7_mastery.json`, item `inference-t7-m-17`. Severity: **Minor**.

After correcting the median option and explanation to approximately 1.4585, the item's separate `check` hint still said 1.4583. The hint now uses 1.4585 and consistently compares the posterior mode, median and mean.


### INF-033 — T4 Poisson UMVUE distractor contained an incorrect numerical value

File: `seed/inference_t4_mastery.json`, item `mle-m-12`. Severity: **Minor**.

For (n=8) and (T=24), the UMVUE of (e^{-\lambda}) is (((n-1)/n)^T=(7/8)^{24}=0.0405689\ldots), which rounds to **0.0406**, not 0.0424. The distractor and its explanation's reference value were corrected. The keyed MLE answer D, (e^{-3}\approx0.0498), was already correct and remains unchanged.

### INF-034 — Python unittest entry point preceded the final test class

File: `verify_inference_math.py`. Severity: **Verification coverage**.

The `unittest.main()` entry point appeared before `Topic04AndConsistencyRegressionTests`, so direct execution invoked test discovery before that final class had been defined. The entry point was moved to the end of the file. A further T4 numerical regression test was added, bringing the suite to **70 test methods**, all now defined before test discovery begins.


### INF-035 — T6 introductory explanation overstated pointwise Cramér–Rao attainment

File: `seed/lesson_t6.json`, scene `s1`. Severity: **Minor — conceptual precision**.

The original wording said that finding an unbiased estimator whose variance equals the Cramér–Rao bound makes it “the best unbiased estimator” without distinguishing attainment at one parameter value from a uniform minimum-variance result. Equality at a particular θ establishes minimum variance among unbiased estimators at that θ, under the theorem's regularity conditions; a UMVUE claim for the model requires the minimum-variance property for every θ. The introductory explanation now makes that distinction explicitly. A source-content regression test guards both qualifications and rejects the old overstatement.


### INF-036 — T6 mastery difficulty labels did not match the required paper mix

File: `seed/inference_t6_mastery.json`. Severity: **Assessment metadata / CI contract**.

The 20-item pool was labelled 5 easy, 10 moderate and 5 hard, while the repository's published mastery-paper contract requires 6/10/4. On re-review, the Fisher-information identity multi-statement item (`inf-t6-m-13`) is a moderate application of standard identities, while the combined efficiency, finite-sample MLE, score-attainment and UMVUE synthesis item (`inf-t6-m-17`) is appropriately hard. Their labels were exchanged, yielding the required 6/10/4 mix without changing either question, answer key or explanation. A verifier regression now asserts both the aggregate mix and these two reviewed classifications.


### INF-037 — T2 mastery difficulty labels did not match the required paper mix

File: `seed/inference_t2_mastery.json`. Severity: **Assessment metadata / CI contract**.

The pool was labelled 4 easy, 11 moderate and 5 hard rather than 6/10/4. Two direct formula-substitution items were under-labelled as moderate: the Uniform maximum UMVUE calculation (`inf-t2-m-02`) and the Poisson UMVUE of λ (`inf-t2-m-18`). Both were reclassified easy. The known-variance normal Basu independence application (`inf-t2-m-16`) was reclassified from hard to moderate. Question text, keys and explanations are unchanged.

### INF-038 — T3 mastery difficulty labels did not match the required paper mix

File: `seed/inference_t3_mastery.json`. Severity: **Assessment metadata / CI contract**.

The pool was labelled 4 easy, 10 moderate and 6 hard. Two direct UMVUE formula-substitution items (`inf-t3-m-02`, `inf-t3-m-04`) were reclassified easy. The normal UMVUE of μ² calculation (`inf-t3-m-09`) and the Bernoulli conditional-expectation/Rao–Blackwell calculation (`inf-t3-m-16`) were reclassified moderate rather than hard. No question text, key or explanation changed.

### INF-039 — T5 mastery difficulty labels did not match the required paper mix

File: `seed/inference_t5_mastery.json`. Severity: **Assessment metadata / CI contract**.

The pool was labelled 6 easy, 9 moderate and 5 hard. The Uniform(0,θ) method-of-moments feasibility check (`inf-t5-m-09`) was reclassified from hard to moderate: it requires a moment estimate followed by a sample-compatibility check, but does not require the multi-step synthesis expected of a hard item. Question text, answer key and explanation are unchanged.

A new regression test now verifies the 6/10/4 mix across all 16 available non-T9 inference pools and guards the reviewed classifications. T9 remains excluded while PR #93 owns it.
