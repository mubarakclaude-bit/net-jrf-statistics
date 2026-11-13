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
| T1 | Sufficiency, factorisation, minimal sufficiency | PASS — first pass | Worked derivations and key examples recalculated; mastery structure and multi-statement keys checked |
| T2 | Completeness, exponential families, ancillarity, Basu | PASS — first pass | Poisson/Bernoulli completeness arguments, Uniform range counterexample and Basu conditions checked |
| T3 | Rao–Blackwell and Lehmann–Scheffé | PASS — first pass | Poisson and Bernoulli UMVUE derivations, variance comparisons and transformation traps checked |
| T4 | MLE: computation, invariance, properties | BLOCKED — lesson absent | Catalog entry and 20-item mastery pool exist, but `seed/lesson_t4.json` is absent from current main; no substitute lesson source found in the seed tree |
| T5 | Method of moments, minimum chi-square, least squares | PASS — first pass | Gamma/Uniform moment estimates, exponential-rate bias and OLS normal equations recalculated |
| T6 | Cramér–Rao bound and Fisher information | PASS — first pass | Bernoulli, Poisson, normal and function-of-parameter bounds checked |
| T7 | Bayesian estimation and conjugate priors | CORRECTED | Normal–normal posterior answer in completion scene s6 was wrong; see INF-001 |
| T8 | Decision theory: loss, risk, admissibility, minimax | PASS — first pass | Binomial minimax rule/risk, crossings and asymmetric absolute-loss quantile checked |
| T9 | Neyman–Pearson, MLR, UMP | DEFERRED | Conflicts with open draft PR #93; left untouched |
| T10 | Likelihood ratio test and Wilks | PASS — first pass | Normal mean/variance LRTs and degrees-of-freedom examples recalculated |
| T11 | SPRT | PASS — first pass | Wald boundaries, Bernoulli log-ratio slope, sample path and ASN approximations recalculated |
| T12 | Size and power computation | CORRECTED | Mastery item `inf-t12-m-10` had an incorrect answer key; see INF-002 |
| T13 | Confidence intervals and pivots | CORRECTED | Variance-interval endpoint rounding corrected in lesson and mastery item; see INF-003 |
| T14 | Chi-square goodness of fit | CORRECTED | Poisson tail pooling explanation corrected; statistic and df independently recomputed; see INF-004 |
| T15 | Choosing the right test | PASS — first pass | Family-wise error, Bonferroni, p-value and test-selection examples checked |
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
- The verifier is at repository root so the existing `tools/run-verifiers.js` CI discovery rule (`verify_*.py` at root) executes it on this PR. The first CI run is pending at report authoring time.
- GitHub Actions/PR checks are therefore still pending at report authoring time.
- No test result is claimed merely because the verifier file exists.

## Files changed

Modified:
- `seed/lesson_t7.json`
- `seed/inference_t12_mastery.json`
- `seed/lesson_t13.json`
- `seed/inference_t13_mastery.json`
- `seed/lesson_t14.json`
- `seed/inference_t14_mastery.json`

Added:
- `verify_inference_math.py`
- `audits/statistical_inference_verification_2026-11-14.md`

No other lesson or module files were changed.

## Outstanding limitations and dependencies

1. **T4 content gap:** The catalog and 20-item mastery pool exist, but the lesson JSON is absent from current main. This task does not author a replacement lesson or change catalog/application architecture.
2. **T9 dependency:** T9 is reserved for PR #93. A follow-up should compare that PR's T9 verifier and lesson changes against this audit's scope before integrating.
3. **Mastery key depth:** All available non-T9 pools were checked for item count, IDs, answer labels and multi-statement verdict/key consistency. Numerical/single-choice examples were independently recalculated on a representative basis; an exhaustive manual proof of every single-choice/numeric key remains outstanding and must not be inferred from these structural checks.
4. **Verifier execution:** Run `python verify_inference_math.py` from a full checkout and resolve any failures before treating the audit as complete.
5. No branch merge, production deployment, Vercel push or workflow/configuration change was made.
