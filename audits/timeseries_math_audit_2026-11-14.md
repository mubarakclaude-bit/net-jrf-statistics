# Time Series Paper 2 — Independent Mathematical Audit
**Date:** 14 November 2026  
**Repository:** `mubarakclaude-bit/net-jrf-statistics`  
**Branch:** `audit/timeseries-math-2026-11-14`  
**Base:** `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`

## Scope and catalog

The current Time Series catalog contains 11 topics:

1. Stationarity and Invertibility (`timeseries-t1`)
2. ACF and PACF Identification (`timeseries-t2`)
3. The Yule–Walker Equations (`timeseries-t3`)
4. Autocovariance of AR Processes (`timeseries-t4`)
5. Unit Roots, Differencing and ARIMA (`timeseries-t5`)
6. Random Walk With and Without Drift (`timeseries-t6`)
7. Spectral Density and the Periodogram (`timeseries-t7`)
8. Components, Moving Averages and Smoothing (`timeseries-t8`)
9. Ergodicity (`timeseries-t9`)
10. General Linear Process and Wold Decomposition (`timeseries-t10`)
11. Forecasting Stationary and Invertible Processes (`timeseries-t11`)

The current lessons contain 41 worked/guided/completion scenes and 10 trap-check scenes across the ten topics audited on this branch. Each of those ten topics has a 20-question mastery pool: **200 mastery items** reviewed for key-to-option consistency, including all 20 multi-statement verdict sets.

## Topic-wise result

“Manual review” describes independent mathematical derivation/recalculation. “Verifier execution” is deliberately separate: the scripts have been authored but have **not yet been executed in a full local checkout or by PR CI**.

| Topic | Manual review | Verifier | Notes |
|---|---|---|---|
| T1 Stationarity / invertibility | PASS after corrections | Pending | Canonical invertible MA representation and innovation-variance rescaling clarified. |
| T2 ACF / PACF identification | CORRECTED IN PR #93 BRANCH; pending its CI/merge | Dedicated verifier extended in PR #93 | PACF closed-form sign and displayed values corrected; independent Durbin–Levinson comparison added to the owning verifier. No T2 files changed in this PR. |
| T3 Yule–Walker | PASS | Pending | AR(1)/AR(2) equations, coefficient recovery, stationarity checks and ACF recursion recalculated. |
| T4 AR autocovariance | PASS after corrections | Pending | Variance lower bound corrected from strict (>\sigma^2) to inclusive (\geq\sigma^2). |
| T5 Unit roots / ARIMA | PASS | Pending | Unit-root factorisation, differenced AR signs and Dickey–Fuller reparameterisation checked. |
| T6 Random walk | PASS after corrections | Pending | Second-moment derivations now state the sufficient uncorrelated-shock assumption rather than requiring independence. |
| T7 Spectral density | PASS | Pending | AR(1)/MA(1) densities, frequency peaks, area-to-variance identities and smoothing rate checked. |
| T8 Decomposition / smoothing | PASS | Pending | SES weights, average age/half-life, centred filters, seasonal normalisation and moving-average ACF checked. |
| T9 Ergodicity | PASS after corrections | Pending | Finite-sample variance, long-run variance, effective sample size and fixed-effect counterexample checked; mastery wording refined. |
| T10 Linear process / Wold | PASS after corrections | Pending | Overlap autocovariances checked; long-run variance identity now states its summability condition. |
| T11 Forecasting | PASS after corrections | Pending | Best linear predictor distinguished from full conditional expectation; MA invertibility wording made canonical-representation specific; interval statement qualified. |

**Interpretation:** These are manual mathematical-review results, not green CI results. Do not treat the branch as fully release-verified until the scripts and repository checks execute successfully.

## Confirmed corrections

### Lesson JSON

- `seed/lesson_ts1.json`
  - Clarified that invertibility guarantees convergence of the inverse filter for a chosen MA parameterisation.
  - Clarified that a non-invertible MA parameterisation has an observationally equivalent invertible representation when the innovation variance is rescaled.
  - Removed the overstatement that forecasting from observations is impossible for a non-invertible parameterisation.

- `seed/lesson_ts4.json`
  - Corrected the AR variance lower-bound language. Since (\gamma_0=\sigma^2\sum_j\psi_j^2) and (\psi_0=1), (\gamma_0\geq\sigma^2); equality holds for white noise, and strict inequality requires a non-zero past-shock weight.

- `seed/lesson_ts6.json`
  - Made the random-walk second-moment assumption explicit: uncorrelated shocks suffice for the variance/covariance calculations; independence is stronger than required.

- `seed/lesson_ts11.json`
  - Distinguished the conditional expectation (the optimal predictor among all measurable predictors) from the Wold-weight best linear predictor.
  - Clarified that uncorrelated Wold innovations alone do not guarantee that the full conditional expectation is linear.
  - Clarified that invertibility is imposed on the canonical MA representation; it is not a claim that a non-invertible parameterisation makes the observed process unforecastable.

### Mastery pools

- `seed/timeseries_t1_mastery.json`: refined invertibility/forecasting explanations and the AR(1) variance lower-bound check.
- `seed/timeseries_t4_mastery.json`: corrected the AR variance lower bound and its multi-statement verdict.
- `seed/timeseries_t5_mastery.json`: reframed invertibility as selection of a canonical MA representation.
- `seed/timeseries_t6_mastery.json`: aligned random-walk variance explanations with uncorrelated innovations.
- `seed/timeseries_t9_mastery.json`: specified the process-standard-deviation baseline for the AR(1) standard-error multiplier and corrected the non-ergodic variance-bracket calculation.
- `seed/timeseries_t10_mastery.json`: qualified the long-run variance identity by requiring convergence of the long-run weight sum; corrected the inclusive AR variance lower bound.
- `seed/timeseries_t11_mastery.json`: refined MA invertibility wording, prediction-interval statement and the distinction between best linear prediction and conditional expectation.

## Independent verifier suite

Ten topic-level scripts have been added. Each computes identities or numerical cases from model parameters and formulas rather than merely asserting a copied lesson answer.

- `tools/verify_timeseries_t1.py` — AR(2) root/triangle equivalence, AR(1) variance, reciprocal MA(1) ACF and variance rescaling.
- `tools/verify_timeseries_t3.py` — AR(2) Yule–Walker solution, back-substitution and AR(1) ACF values.
- `tools/verify_timeseries_t4.py` — AR(1)/AR(2) moments, autocorrelation recursion and variance boundary.
- `tools/verify_timeseries_t5.py` — unit-root polynomial factorisation, differenced AR coefficients, over-differencing moments and DF coefficient mapping.
- `tools/verify_timeseries_t6.py` — random-walk moments/correlation and over-differenced white-noise moments.
- `tools/verify_timeseries_t7.py` — AR(1)/MA(1) spectra, Simpson integration against variance and periodogram smoothing-rate identity.
- `tools/verify_timeseries_t8.py` — SES geometric weights, half-life/average age, centred moving-average filters, seasonal normalisation and moving-average ACF.
- `tools/verify_timeseries_t9.py` — exact finite-sample AR(1) mean variance, long-run variance, effective sample size and fixed-effect non-ergodicity.
- `tools/verify_timeseries_t10.py` — ARMA impulse-response weights, overlap autocovariances, long-run multipliers and square-summability.
- `tools/verify_timeseries_t11.py` — AR(1)/AR(2)/MA forecasts, forecast-error variances and long-horizon limits.
- `tools/verify_timeseries_common.py` — verifies the lesson-to-pool link, 20-item pool count, unique IDs, answer-key letters, four-option structure, explanation/check presence, key distribution, difficulty mix and consistency of multi-statement truth sets with the keyed option.

The scripts contain approximately **197 independent numerical/formula checks** in total, in addition to the shared mastery-pool contract checks. This is the authored test count, **not a claim that the tests have passed execution**.

## T2 coordination — correction owned by PR #93

PR [#93](https://github.com/mubarakclaude-bit/net-jrf-statistics/pull/93) owns `seed/lesson_ts2.json` and its dedicated verifier. The T2 findings identified during this audit were handed to that branch and corrected there:

- The MA(1) PACF closed form now uses  
  `−θ^k(1−θ²)/(1−θ^(2(k+1)))`, consistent with the stated minus convention `ρ₁=−θ/(1+θ²)`.
- At `θ=0.5`, the first four values are approximately `−0.400000, −0.190476, −0.094118, −0.046921`.
- The roots for `ρ₁=−0.49` are `0.8173495` and `1.2234668`; the invertible root is `0.81735`.
- Independent second-pass review then caught a residual stale final answer (`0.857`) in T2 scene s10(f). PR #93 now corrects that final learner-facing line to `0.81735` and strengthens its verifier to assert the exact value and reject any remaining `0.857` string.

The T2 source and verifier remain unchanged on this PR #95 branch to preserve file ownership. The latest PR #93 head is undergoing a fresh CI run after these follow-up corrections; do not mark the combined 11-topic audit fully release-verified until that run passes.

## Execution and limitations

- PR #95's GitHub Actions run `43564752978` completed successfully: validation, all six acceptance scenarios, browser build, strict app test, clicktest, hosted storage adapter conformance and feature browser tests passed.
- The ten topic-level verifiers and shared mastery-pool contract helper were included in the successful validation job. The manual full-inventory step was skipped by workflow design.
- The successful run applies to PR #95 head `6594333bc307a276cf2eb4fdbfb36a1694355bcd`; any subsequent branch changes require fresh CI.
- The T2 follow-up correction is owned by PR #93 and is still awaiting its latest-head CI result.
- No local checkout or local test run is claimed; CI is the recorded execution evidence.
- No shared manifest, architecture, app code, configuration, Paper 1 content, or unrelated module was modified.
- No merge or deployment was performed.

## Changed-file boundary

Only four Time Series lesson JSON files, seven Time Series mastery pools, ten topic-specific verifier scripts, and one shared verifier helper are changed on this branch, plus this audit report. No other module or shared application infrastructure is touched.
