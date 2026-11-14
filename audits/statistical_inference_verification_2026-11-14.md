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

Status describes the first-pass mathematical audit of the current lesson material and the available mastery pool. It does not certify every individual single-choice/numeric mastery item: those still require a full manual key-by-key pass. The regression suite provides repeatable independent calculations and checks the pool structure and all multi-statement keys.

| Topic | Catalog subject | Status | Notes |
|---|---|---|---|
| T1 | Sufficiency, factorisation, minimal sufficiency | CLARIFIED | Mastery item now states the closed-endpoint Uniform convention consistently with its boundary likelihood |
| T2 | Completeness, exponential families, ancillarity, Basu | PASS — first pass | Poisson/Bernoulli completeness arguments, Uniform range counterexample and Basu conditions checked |
| T3 | Rao–Blackwell and Lehmann–Scheffé | PASS — first pass | Poisson and Bernoulli UMVUE derivations, variance comparisons and transformation traps checked |
| T4 | MLE: computation, invariance, properties | BLOCKED — lesson absent | Catalog entry and 20-item mastery pool exist, but `seed/lesson_t4.json` is absent from current main; no substitute lesson source found in the seed tree |
| T5 | Method of moments, minimum chi-square, least squares | CORRECTED | Uniform MOM estimate wording now distinguishes sample feasibility from decision-theoretic admissibility |
| T6 | Cramér–Rao bound and Fisher information | PASS — first pass | Bernoulli, Poisson, normal and function-of-parameter bounds checked |
| T7 | Bayesian estimation and conjugate priors | CORRECTED | Normal–normal posterior answer in completion scene s6 was wrong; see INF-001 |
| T8 | Decision theory: loss, risk, admissibility, minimax | CORRECTED | Normal-mean minimax explanation now states the minimax lower bound; constant risk alone is not treated as sufficient |
| T9 | Neyman–Pearson, MLR, UMP | DEFERRED | Conflicts with open draft PR #93; left untouched |
| T10 | Likelihood ratio test and Wilks | PASS — first pass | Normal mean/variance LRTs and degrees-of-freedom examples recalculated |
| T11 | SPRT | PASS — first pass | Wald boundaries, Bernoulli log-ratio slope, sample path and ASN approximations recalculated |
| T12 | Size and power computation | CORRECTED | Mastery item `inf-t12-m-10` had an incorrect answer key; see INF-002 |
| T13 | Confidence intervals and pivots | CORRECTED | Variance-interval endpoint rounding corrected in lesson and mastery item; see INF-003 |
| T14 | Chi-square goodness of fit | CORRECTED | Poisson tail pooling explanation corrected; statistic and df independently recomputed; see INF-004 |
| T15 | Choosing the right test | CORRECTED | Corrected a p-value/data mismatch and clarified that sign/Wilcoxon procedures do not generally test a skewed population mean |
| T16 | Contingency tables: independence and homogeneity | PASS — first pass | Expected counts, Pearson/Yates statistics, df and association measures checked |
| T17 | UMP unbiased and UMP invariant tests | PASS — first pass | Exponential-rate one-sided direction/cutoffs and normal two-sided UMPU/invariance arguments checked |

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
- The T4 lesson-file gap is detectable.
- The corrected T7, T12, T13 and T14 source values remain in place.

### Test execution status

- Independent calculations were recomputed during the audit using exact arithmetic where possible and numerical tolerances for rounded quantities.
- The verifier is at repository root so the existing `tools/run-verifiers.js` CI discovery rule (`verify_*.py` at root) executes it on this PR. It now contains 54 regression tests.
- GitHub Actions run #1195 (run ID `43564757724`) completed successfully on commit `3830a2e7cc776f02414d503fbf3e8f964b595aed`: validate, acceptance and browser jobs all passed, including the verifier, build, lesson navigation, hosted storage conformance and feature browser tests.
- The additional T1, T5, T8 and T15 edits and the expanded 54-test verifier were committed after that run. A fresh CI run on the latest branch head is required before those follow-up edits are considered validated.

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

Added:
- `verify_inference_math.py`
- `audits/statistical_inference_verification_2026-11-14.md`

No other lesson or module files were changed.

## Outstanding limitations and dependencies

1. **T4 content gap:** The catalog and 20-item mastery pool exist, but the lesson JSON is absent from current main. This task does not author a replacement lesson or change catalog/application architecture.
2. **T9 dependency:** T9 is reserved for PR #93. A follow-up should compare that PR's T9 verifier and lesson changes against this audit's scope before integrating.
3. **Mastery key depth:** All available non-T9 pools were checked for item count, IDs, answer labels and multi-statement verdict/key consistency. Manual review has expanded beyond representative examples and has identified/corrected additional single-choice/numeric inconsistencies, but an exhaustive proof of every single-choice/numeric key remains outstanding and must not be inferred from these checks.
4. **Verifier execution:** Run `python verify_inference_math.py` from a full checkout and resolve any failures before treating the audit as complete.
5. No branch merge, production deployment, Vercel push or workflow/configuration change was made.
