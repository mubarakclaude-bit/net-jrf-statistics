# Content map

Generated from `seed/` by `node tools/content.js map`; never edit by hand. It is rebuilt from production after every merge and published on the `content-map` branch.
Past-paper links come from a lesson's `anchors` field, its provenance text (read as paper `j26`) and variant-bank `srcQ`/`srcPaper` fields, so treat them as a guide.

## At a glance

- **129 lessons** cover **129 of 167 catalog topics** in 21 modules (12 have at least one lesson).
- **129 mastery pools** (2580 questions), **10 previous-year variant banks** (501 questions), **5 practice sets**, and **1 past paper** (`j26`).
- Past paper `j26` (UGC NET June 2026 — Paper 2, questions 1–50 (actual paper)): 50 questions, 34 answered wrongly; named by a lesson **37/50**; with a variant bank **49/50**; with neither **0**.

## Modules, ranked by marks still without a lesson

| Module | Unit | Marks | Topics | With lesson | Marks without a lesson |
|---|---|---|---|---|---|
| `p1-highered` Higher education and national integration | P1-9 | 20 | 6 | 0 | 19.8 |
| `p1-ict` ICT | P1-7 | 12 | 4 | 0 | 12.0 |
| `p1-logical` Logical reasoning | P1-5 | 12 | 5 | 0 | 12.0 |
| `p1-mathreason` Mathematical reasoning and aptitude | P1-4 | 12 | 4 | 0 | 12.0 |
| `p1-di` Data interpretation | P1-6 | 10 | 4 | 0 | 10.0 |
| `p1-environment` People, development and environment | P1-8 | 10 | 4 | 0 | 10.0 |
| `p1-teaching` Teaching aptitude | P1-1 | 10 | 4 | 0 | 10.0 |
| `p1-communication` Communication | P1-3 | 8 | 3 | 0 | 8.1 |
| `p1-research` Research aptitude | P1-2 | 6 | 4 | 0 | 6.0 |
| `design` Design of experiments | 3B | 10 | 8 | 8 | 0.0 |
| `inference` Statistical inference | 4 | 34 | 17 | 17 | 0.0 |
| `maths` Mathematics | 2 | 18 | 16 | 16 | 0.0 |
| `multivariate` Multivariate analysis | 8 | 18 | 9 | 9 | 0.0 |
| `nonparam` Nonparametric methods | 5 | 6 | 8 | 8 | 0.0 |
| `official` Official statistics | 10A | 8 | 5 | 5 | 0.0 |
| `probability` Probability and distributions | 1 | 22 | 13 | 13 | 0.0 |
| `regression` Regression and linear models | 6 | 22 | 15 | 15 | 0.0 |
| `rprog` R programming | 10B | 12 | 9 | 9 | 0.0 |
| `sampling` Sampling theory | 3A | 10 | 9 | 9 | 0.0 |
| `stochastic` Stochastic processes | 9 | 20 | 9 | 9 | 0.0 |
| `timeseries` Time series | 7 | 20 | 11 | 11 | 0.0 |

## Topics (one row per catalog topic)

`extent` and `imp` come from the catalog; `marks` is the topic's expected marks.

| Topic | Name | Extent | Imp | Marks | Lesson | Pool | Past-paper Qs named | Authoring script | Verification |
|---|---|---|---|---|---|---|---|---|---|
| `inference-t1` | Sufficiency, factorisation, minimal sufficiency | Derive | 3 | 2.8 | v4.3 · 104 min · 17 scenes (`seed/lesson_t1.json`) | 20 items (`seed/inference_t1_mastery.json`) | j26 Q6 | `lesson_t1.py` | none |
| `inference-t2` | Completeness, exponential families, ancillarity, Basu | Derive | 3 | 2.8 | v1.3 · 51 min · 14 scenes (`seed/lesson_t2.json`) | 20 items (`seed/inference_t2_mastery.json`) |  | none | none |
| `inference-t3` | Rao–Blackwell and Lehmann–Scheffé | Derive | 3 | 2.8 | v1.3 · 51 min · 14 scenes (`seed/lesson_t3.json`) | 20 items (`seed/inference_t3_mastery.json`) |  | none | none |
| `inference-t4` | MLE: computation, invariance, properties | Derive | 3 | 2.8 | v1.3 · 46 min · 15 scenes (`seed/lesson_mle.json`) | 20 items (`seed/inference_t4_mastery.json`) |  | none | none |
| `inference-t5` | Method of moments, minimum chi-square, least squares | Apply | 2 | 1.8 | v1.3 · 51 min · 14 scenes (`seed/lesson_t5.json`) | 20 items (`seed/inference_t5_mastery.json`) |  | none | none |
| `inference-t6` | Cramér–Rao bound and Fisher information | Apply | 3 | 2.8 | v1.3 · 51 min · 14 scenes (`seed/lesson_t6.json`) | 20 items (`seed/inference_t6_mastery.json`) |  | none | none |
| `inference-t7` | Bayesian estimation and conjugate priors | Apply | 2 | 1.8 | v1.1 · 93 min · 14 scenes (`seed/lesson_t7.json`) | 20 items (`seed/inference_t7_mastery.json`) |  | `lesson_t7.py` | none |
| `inference-t8` | Decision theory: loss, risk, admissibility, minimax | State | 1 | 0.9 | v1.1 · 93 min · 14 scenes (`seed/lesson_t8.json`) | 20 items (`seed/inference_t8_mastery.json`) |  | `lesson_t8.py` | none |
| `inference-t9` | Neyman–Pearson, MLR, UMP, when UMP fails | State | 3 | 2.8 | v1.3 · 56 min · 14 scenes (`seed/lesson_t9.json`) | 20 items (`seed/inference_t9_mastery.json`) |  | none | none |
| `inference-t10` | Likelihood ratio test and Wilks | State | 2 | 1.8 | v1.0 · 99 min · 16 scenes (`seed/lesson_t10.json`) | 20 items (`seed/inference_t10_mastery.json`) | j26 Q30, j26 Q31 | `lesson_t10.py` | none |
| `inference-t11` | SPRT | State | 1 | 0.9 | v1.0 · 98 min · 16 scenes (`seed/lesson_t11.json`) | 20 items (`seed/inference_t11_mastery.json`) |  | `lesson_t11.py` | none |
| `inference-t12` | Size and power computation | Derive | 2 | 1.8 | v1.0 · 99 min · 16 scenes (`seed/lesson_t12.json`) | 20 items (`seed/inference_t12_mastery.json`) | j26 Q39, j26 Q43, j26 Q49 | `lesson_t12.py` | none |
| `inference-t13` | Confidence intervals and pivots | Derive | 2 | 1.8 | v1.0 · 98 min · 16 scenes (`seed/lesson_t13.json`) | 20 items (`seed/inference_t13_mastery.json`) | j26 Q10 | `lesson_t13.py` | none |
| `inference-t14` | Chi-square goodness of fit | Derive | 2 | 1.8 | v1.0 · 98 min · 16 scenes (`seed/lesson_t14.json`) | 20 items (`seed/inference_t14_mastery.json`) | j26 Q28, j26 Q29 | `lesson_t14.py` | none |
| `inference-t15` | Choosing the right test | Recall | 1 | 0.9 | v1.0 · 98 min · 16 scenes (`seed/lesson_t15.json`) | 20 items (`seed/inference_t15_mastery.json`) | j26 Q43 | `lesson_t15.py` | none |
| `inference-t16` | Contingency tables: independence and homogeneity | Apply | 2 | 1.8 | v1.0 · 98 min · 16 scenes (`seed/lesson_t16.json`) | 20 items (`seed/inference_t16_mastery.json`) | j26 Q29, j26 Q33 | `lesson_t16.py` | none |
| `inference-t17` | UMP unbiased and UMP invariant tests | Derive | 2 | 1.8 | v1.0 · 98 min · 16 scenes (`seed/lesson_t17.json`) | 20 items (`seed/inference_t17_mastery.json`) | j26 Q14 | `lesson_t17.py` | none |
| `probability-t1` | Order statistics | Derive | 2 | 1.7 | v1.0 · 98 min · 16 scenes (`seed/lesson_pr1.json`) | 20 items (`seed/probability_t1_mastery.json`) | j26 Q13 | `lesson_pr1.py` | none |
| `probability-t2` | Conditional distributions | Derive | 2 | 1.7 | v1.0 · 95 min · 13 scenes (`seed/lesson_pr2.json`) | 20 items (`seed/probability_t2_mastery.json`) |  | none | none |
| `probability-t3` | Conditional expectation, total variance, mixtures | Derive | 2 | 1.7 | v1.0 · 91 min · 15 scenes (`seed/lesson_pr3.json`) | 20 items (`seed/probability_t3_mastery.json`) | j26 Q45, j26 Q46 | `lesson_pr3.py` | none |
| `probability-t4` | MGFs, cumulants, central moments | Derive | 2 | 1.7 | v1.0 · 100 min · 13 scenes (`seed/lesson_pr4.json`) | 20 items (`seed/probability_t4_mastery.json`) |  | none | none |
| `probability-t5` | Standard discrete distributions | Recall | 2 | 1.7 | v1.0 · 99 min · 16 scenes (`seed/lesson_pr5.json`) | 20 items (`seed/probability_t5_mastery.json`) | j26 Q6 | `lesson_pr5.py` | none |
| `probability-t6` | Standard continuous distributions | Apply | 2 | 1.7 | v1.0 · 100 min · 13 scenes (`seed/lesson_pr6.json`) | 20 items (`seed/probability_t6_mastery.json`) |  | none | none |
| `probability-t7` | Jensen, Markov, Chebyshev, Cauchy–Schwarz | State | 2 | 1.7 | v1.0 · 100 min · 16 scenes (`seed/lesson_pr7.json`) | 20 items (`seed/probability_t7_mastery.json`) | j26 Q31, j26 Q35 | `lesson_pr7.py` | none |
| `probability-t8` | Independence and inclusion–exclusion | Apply | 2 | 1.7 | v1.0 · 98 min · 15 scenes (`seed/lesson_pr8.json`) | 20 items (`seed/probability_t8_mastery.json`) | j26 Q34 | `lesson_pr8.py` | none |
| `probability-t9` | Convergence, WLLN, SLLN, CLT | State | 2 | 1.7 | v1.0 · 105 min · 13 scenes (`seed/lesson_pr9.json`) | 20 items (`seed/probability_t9_mastery.json`) |  | none | none |
| `probability-t10` | Transformations and Jacobians | Derive | 2 | 1.7 | v1.0 · 100 min · 16 scenes (`seed/lesson_pr10.json`) | 20 items (`seed/probability_t10_mastery.json`) | j26 Q25 | `lesson_pr10.py` | none |
| `probability-t11` | Characteristic functions | State | 2 | 1.7 | v1.0 · 100 min · 13 scenes (`seed/lesson_pr11.json`) | 20 items (`seed/probability_t11_mastery.json`) |  | none | none |
| `probability-t12` | Bayes theorem and conditional probability | Apply | 2 | 1.7 | v1.0 · 95 min · 13 scenes (`seed/lesson_pr12.json`) | 20 items (`seed/probability_t12_mastery.json`) |  | none | none |
| `probability-t13` | Sampling distributions: t, chi-square and F | Derive | 2 | 1.7 | v1.0 · 98 min · 16 scenes (`seed/lesson_pr13.json`) | 20 items (`seed/probability_t13_mastery.json`) | j26 Q46 | `lesson_pr13.py` | none |
| `regression-t1` | Hat matrix, residual maker, quadratic forms | Derive | 2 | 1.5 | v1.0 · 100 min · 16 scenes (`seed/lesson_rg1.json`) | 20 items (`seed/regression_t1_mastery.json`) | j26 Q9 | `lesson_rg1.py` | `verify_regression_t1.py`, `verify_regression_t10.py`, `verify_regression_t11.py`, `verify_regression_t12.py`, `verify_regression_t13.py`, `verify_regression_t14.py`, `verify_regression_t15.py`, `verify_regression_t1_t4.py` |
| `regression-t2` | Gauss–Markov, BLUE, estimability | Derive | 2 | 1.5 | v4.1 · 98 min · 16 scenes (`seed/lesson_rg2.json`) | 20 items (`seed/regression_t2_mastery.json`) |  | `lesson_rg2.py` | `verify_regression_t2.py` |
| `regression-t3` | ANOVA decomposition and the F test from R² | Derive | 2 | 1.5 | v1.0 · 100 min · 16 scenes (`seed/lesson_rg3.json`) | 20 items (`seed/regression_t3_mastery.json`) | j26 Q9 | `lesson_rg3.py` | `verify_regression_t3.py` |
| `regression-t4` | R², adjusted R², model comparison | Apply | 2 | 1.5 | v1.0 · 100 min · 16 scenes (`seed/lesson_rg4.json`) | 20 items (`seed/regression_t4_mastery.json`) | j26 Q9 | `lesson_rg4.py` | `verify_regression_t4.py` |
| `regression-t5` | Multicollinearity | State | 2 | 1.5 | v1.0 · 90 min · 16 scenes (`seed/lesson_rg5.json`) | 20 items (`seed/regression_t5_mastery.json`) | j26 Q74 | `lesson_rg5.py` | `verify_regression_t5.py` |
| `regression-t7` | Heteroscedasticity and GLS | State | 2 | 1.5 | v4.1 · 105 min · 16 scenes (`seed/lesson_rg7.json`) | 20 items (`seed/regression_t7_mastery.json`) |  | none | `verify_regression_t7.py` |
| `regression-t6` | Autocorrelation and Durbin–Watson | Apply | 2 | 1.5 | v4.1 · 100 min · 16 scenes (`seed/lesson_rg6.json`) | 20 items (`seed/regression_t6_mastery.json`) |  | none | `verify_regression_t6.py` |
| `regression-t8` | Endogeneity and instrumental variables | State | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg8.json`) | 20 items (`seed/regression_t8_mastery.json`) | j26 Q9, j26 Q11, j26 Q38 | none | `verify_regression_t8.py` |
| `regression-t9` | Identification in simultaneous equations | Apply | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg9.json`) | 20 items (`seed/regression_t9_mastery.json`) |  | none | `verify_regression_t9.py` |
| `regression-t10` | Two-stage least squares | State | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg10.json`) | 20 items (`seed/regression_t10_mastery.json`) |  | none | `verify_regression_t10.py` |
| `regression-t11` | Indicator and dummy variables | Apply | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg11.json`) | 20 items (`seed/regression_t11_mastery.json`) |  | none | `verify_regression_t11.py` |
| `regression-t12` | Logistic regression models | Apply | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg12.json`) | 20 items (`seed/regression_t12_mastery.json`) |  | none | `verify_regression_t12.py` |
| `regression-t13` | Restricted regression: exact, stochastic and mixed restrictions | Derive | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg13.json`) | 20 items (`seed/regression_t13_mastery.json`) |  | none | `verify_regression_t13.py` |
| `regression-t14` | Errors in variables and stochastic regressors | Derive | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg14.json`) | 20 items (`seed/regression_t14_mastery.json`) |  | none | `verify_regression_t14.py` |
| `regression-t15` | k-class estimators | Recall | 2 | 1.5 | v1.0 · 92 min · 15 scenes (`seed/lesson_rg15.json`) | 20 items (`seed/regression_t15_mastery.json`) |  | none | `verify_regression_t15.py` |
| `stochastic-t1` | Markov chains: n-step, Chapman–Kolmogorov | Derive | 2 | 2.2 | v1.0 · 100 min · 15 scenes (`seed/lesson_stochastic_t1.json`) | 20 items (`seed/stochastic_t1_mastery.json`) |  | `lesson_stochastic_t1.py` | `verify_stochastic_t1.py` |
| `stochastic-t2` | Stationary distribution | Derive | 2 | 2.2 | v4.1 · 98 min · 13 scenes (`seed/lesson_stochastic_t2.json`) | 20 items (`seed/stochastic_t2_mastery.json`) |  | `lesson_stochastic_t2.py` | `verify_stochastic_t2.py` |
| `stochastic-t3` | First passage and first return, mean passage time | Derive | 2 | 2.2 | v4.1 · 82 min · 11 scenes (`seed/lesson_stochastic_t3.json`) | 20 items (`seed/stochastic_t3_mastery.json`) |  | `lesson_stochastic_t3.py` | `verify_stochastic_t3.py` |
| `stochastic-t4` | Classification of states | State | 2 | 2.2 | v4.1 · 82 min · 11 scenes (`seed/lesson_stochastic_t4.json`) | 20 items (`seed/stochastic_t4_mastery.json`) |  | `lesson_stochastic_t4.py` | `verify_stochastic_t4.py` |
| `stochastic-t5` | Poisson process | Derive | 2 | 2.2 | v4.1 · 93 min · 15 scenes (`seed/lesson_stochastic_t5.json`) | 20 items (`seed/stochastic_t5_mastery.json`) |  | `lesson_stochastic_t5.py` | `verify_stochastic_t5.py` |
| `stochastic-t6` | Gambler's ruin and random walks | Apply | 2 | 2.2 | v4.1 · 96 min · 15 scenes (`seed/lesson_stochastic_t6.json`) | 20 items (`seed/stochastic_t6_mastery.json`) |  | `lesson_stochastic_t6.py` | `verify_stochastic_t6.py` |
| `stochastic-t7` | Birth–death and M/M/1 | Apply | 2 | 2.2 | v4.1 · 94 min · 15 scenes (`seed/lesson_stochastic_t7.json`) | 20 items (`seed/stochastic_t7_mastery.json`) |  | `lesson_stochastic_t7.py` | `verify_stochastic_t7.py` |
| `stochastic-t8` | Branching processes | State | 2 | 2.2 | v4.1 · 96 min · 14 scenes (`seed/lesson_stochastic_t8.json`) | 20 items (`seed/stochastic_t8_mastery.json`) |  | `lesson_stochastic_t8.py` | `verify_stochastic_t8.py` |
| `stochastic-t9` | Renewal processes | State | 2 | 2.2 | v4.1 · 95 min · 15 scenes (`seed/lesson_stochastic_t9.json`) | 20 items (`seed/stochastic_t9_mastery.json`) |  | `lesson_stochastic_t9.py` | `verify_stochastic_t9.py` |
| `timeseries-t1` | Stationarity and invertibility | Derive | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts1.json`) | 20 items (`seed/timeseries_t1_mastery.json`) |  | `lesson_ts1.py` | none |
| `timeseries-t2` | ACF and PACF identification | Recall | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts2.json`) | 20 items (`seed/timeseries_t2_mastery.json`) |  | `lesson_ts2.py` | none |
| `timeseries-t3` | Yule–Walker equations | Derive | 2 | 1.8 | v1.0 · 106 min · 17 scenes (`seed/lesson_ts3.json`) | 20 items (`seed/timeseries_t3_mastery.json`) | j26 Q2, j26 Q3, j26 Q18 | `lesson_ts3.py` | none |
| `timeseries-t4` | Autocovariance of AR processes | Derive | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts4.json`) | 20 items (`seed/timeseries_t4_mastery.json`) |  | `lesson_ts4.py` | none |
| `timeseries-t5` | Unit roots, differencing, ARIMA | Derive | 2 | 1.8 | v1.0 · 98 min · 16 scenes (`seed/lesson_ts5.json`) | 20 items (`seed/timeseries_t5_mastery.json`) | j26 Q18 | `lesson_ts5.py` | none |
| `timeseries-t6` | Random walk with and without drift | Apply | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts6.json`) | 20 items (`seed/timeseries_t6_mastery.json`) | j26 Q23 | `lesson_ts6.py` | none |
| `timeseries-t7` | Spectral density and the periodogram | Apply | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts7.json`) | 20 items (`seed/timeseries_t7_mastery.json`) | j26 Q7 | `lesson_ts7.py` | none |
| `timeseries-t8` | Components, moving averages, exponential smoothing | Apply | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts8.json`) | 20 items (`seed/timeseries_t8_mastery.json`) |  | `lesson_ts8.py` | none |
| `timeseries-t9` | Ergodicity | Recall | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts9.json`) | 20 items (`seed/timeseries_t9_mastery.json`) |  | `lesson_ts9.py` | none |
| `timeseries-t10` | General linear process and Wold decomposition | Derive | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts10.json`) | 20 items (`seed/timeseries_t10_mastery.json`) |  | `lesson_ts10.py` | none |
| `timeseries-t11` | Forecasting with stationary and invertible processes | Apply | 2 | 1.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_ts11.json`) | 20 items (`seed/timeseries_t11_mastery.json`) |  | `lesson_ts11.py` | none |
| `maths-t1` | Rank, nullity, Sylvester and Frobenius | Derive | 2 | 1.1 | v1.0 · 98 min · 15 scenes (`seed/lesson_ma1.json`) | 20 items (`seed/maths_t1_mastery.json`) | j26 Q1, j26 Q25, j26 Q26 | `lesson_ma1.py` | none |
| `maths-t2` | Eigenvalues, eigenvectors, Cayley–Hamilton | Derive | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma2.json`) | 20 items (`seed/maths_t2_mastery.json`) |  | none | none |
| `maths-t3` | Quadratic forms and positive definiteness | Apply | 2 | 1.1 | v1.0 · 112 min · 16 scenes (`seed/lesson_ma3.json`) | 20 items (`seed/maths_t3_mastery.json`) |  | none | none |
| `maths-t4` | Sequences, series, power series | Apply | 2 | 1.1 | v1.0 · 99 min · 16 scenes (`seed/lesson_ma4.json`) | 20 items (`seed/maths_t4_mastery.json`) | j26 Q28 | `lesson_ma4.py` | none |
| `maths-t5` | Continuity, differentiability, Rolle, MVT | State | 2 | 1.1 | v1.0 · 113 min · 16 scenes (`seed/lesson_ma5.json`) | 20 items (`seed/maths_t5_mastery.json`) |  | none | none |
| `maths-t6` | Maxima, minima, local extrema | Derive | 2 | 1.1 | v1.0 · 112 min · 16 scenes (`seed/lesson_ma6.json`) | 20 items (`seed/maths_t6_mastery.json`) |  | none | none |
| `maths-t7` | Riemann and improper integrals | Apply | 2 | 1.1 | v1.0 · 113 min · 16 scenes (`seed/lesson_ma7.json`) | 20 items (`seed/maths_t7_mastery.json`) |  | none | none |
| `maths-t8` | Generalised inverse | State | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma8.json`) | 20 items (`seed/maths_t8_mastery.json`) |  | none | none |
| `maths-t9` | Taylor's theorem, L'Hôpital's rule, uniform continuity | Apply | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma9.json`) | 20 items (`seed/maths_t9_mastery.json`) |  | none | none |
| `maths-t10` | Functions of two variables: partial and total derivatives | Apply | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma10.json`) | 20 items (`seed/maths_t10_mastery.json`) |  | none | none |
| `maths-t11` | Saddle points and Lagrange multipliers | Apply | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma11.json`) | 20 items (`seed/maths_t11_mastery.json`) |  | none | none |
| `maths-t12` | Double and triple integrals and their applications | Apply | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma12.json`) | 20 items (`seed/maths_t12_mastery.json`) |  | none | none |
| `maths-t13` | Vector spaces, basis, dimension, row and column space | Recall | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma13.json`) | 20 items (`seed/maths_t13_mastery.json`) |  | none | none |
| `maths-t14` | Systems of linear equations and row reduced echelon form | Apply | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma14.json`) | 20 items (`seed/maths_t14_mastery.json`) |  | none | none |
| `maths-t15` | Gram–Schmidt orthogonalisation and orthogonal matrices | Apply | 2 | 1.1 | v1.0 · 105 min · 15 scenes (`seed/lesson_ma15.json`) | 20 items (`seed/maths_t15_mastery.json`) |  | none | none |
| `maths-t16` | Trace, determinant and inverse of a matrix | Apply | 2 | 1.1 | v1.0 · 120 min · 16 scenes (`seed/lesson_ma16.json`) | 20 items (`seed/maths_t16_mastery.json`) |  | none | none |
| `multivariate-t1` | Multivariate normal: marginals and conditionals | Derive | 2 | 2 | v1.0 · 100 min · 16 scenes (`seed/lesson_multivariate_t1.json`) | 20 items (`seed/multivariate_t1_mastery.json`) | j26 Q24 | `lesson_multivariate_t1.py` | `verify_multivariate_t1.py` |
| `multivariate-t2` | Partial and multiple correlation | Derive | 2 | 2 | v1.0 · 90 min · 17 scenes (`seed/lesson_multivariate_t2.json`) | 20 items (`seed/multivariate_t2_mastery.json`) |  | `lesson_multivariate_t2.py` | `verify_multivariate_t2.py` |
| `multivariate-t3` | Principal component analysis | Derive | 2 | 2 | v1.0 · 96 min · 14 scenes (`seed/lesson_multivariate_t3.json`) | 20 items (`seed/multivariate_t3_mastery.json`) | j26 Q2 | `lesson_multivariate_t3.py` | `verify_multivariate_t3.py` |
| `multivariate-t4` | Hotelling's T² | Derive | 2 | 2 | v1.0 · 94 min · 12 scenes (`seed/lesson_multivariate_t4.json`) | 20 items (`seed/multivariate_t4_mastery.json`) | j26 Q4 | `lesson_multivariate_t4.py` | `verify_multivariate_t4.py` |
| `multivariate-t5` | Wishart distribution | State | 2 | 2 | v1.0 · 88 min · 12 scenes (`seed/lesson_multivariate_t5.json`) | 20 items (`seed/multivariate_t5_mastery.json`) | j26 Q17 | `lesson_multivariate_t5.py` | `verify_multivariate_t5.py` |
| `multivariate-t6` | Canonical correlation | Apply | 2 | 2 | v1.0 · 94 min · 12 scenes (`seed/lesson_multivariate_t6.json`) | 20 items (`seed/multivariate_t6_mastery.json`) | j26 Q20 | `lesson_multivariate_t6.py` | `verify_multivariate_t6.py` |
| `multivariate-t7` | MLE of mean vector and covariance | Apply | 2 | 2 | v1.0 · 90 min · 12 scenes (`seed/lesson_multivariate_t7.json`) | 20 items (`seed/multivariate_t7_mastery.json`) | j26 Q37 | `lesson_multivariate_t7.py` | `verify_multivariate_t7.py` |
| `multivariate-t8` | Mahalanobis distance, discriminant analysis, MANOVA | State | 2 | 2 | v1.0 · 75 min · 12 scenes (`seed/lesson_multivariate_t8.json`) | 20 items (`seed/multivariate_t8_mastery.json`) |  | `lesson_multivariate_t8.py` | `verify_multivariate_t8.py` |
| `multivariate-t9` | Factor and cluster analysis | Recall | 2 | 2 | v1.0 · 65 min · 13 scenes (`seed/lesson_multivariate_t9.json`) | 20 items (`seed/multivariate_t9_mastery.json`) |  | `lesson_multivariate_t9.py` | `verify_multivariate_t9.py` |
| `rprog-t1` | sort, rank, order, which, range | Apply | 2 | 1.3 | v1.0 · 55 min · 13 scenes (`seed/lesson_rprog_t1.json`) | 20 items (`seed/rprog_t1_mastery.json`) | j26 Q16 | `lesson_rprog_t1.py` | `verify_rprog_t1.py` |
| `rprog-t2` | Loops, functions, return values | Apply | 2 | 1.3 | v1.0 · 65 min · 13 scenes (`seed/lesson_rprog_t2.json`) | 20 items (`seed/rprog_t2_mastery.json`) | j26 Q22 | `lesson_rprog_t2.py` | `verify_rprog_t2.py` |
| `rprog-t3` | Scoping rules | State | 2 | 1.3 | v1.0 · 60 min · 13 scenes (`seed/lesson_rprog_t3.json`) | 20 items (`seed/rprog_t3_mastery.json`) |  | `lesson_rprog_t3.py` | `verify_rprog_t3.py` |
| `rprog-t4` | Matrices and matrix operators | Apply | 2 | 1.3 | v1.0 · 70 min · 14 scenes (`seed/lesson_rprog_t4.json`) | 20 items (`seed/rprog_t4_mastery.json`) |  | none | `verify_rprog_t4.py` |
| `rprog-t5` | Statement ordering questions | Apply | 2 | 1.3 | v1.0 · 60 min · 12 scenes (`seed/lesson_rprog_t5.json`) | 20 items (`seed/rprog_t5_mastery.json`) |  | none | `verify_rprog_t5.py` |
| `rprog-t6` | Summary functions and NA handling | Recall | 2 | 1.3 | v1.0 · 60 min · 12 scenes (`seed/lesson_rprog_t6.json`) | 20 items (`seed/rprog_t6_mastery.json`) |  | none | `verify_rprog_t6.py` |
| `rprog-t7` | Lists, factors, display and formatting | Recall | 2 | 1.3 | v1.0 · 65 min · 12 scenes (`seed/lesson_rprog_t7.json`) | 20 items (`seed/rprog_t7_mastery.json`) |  | none | `verify_rprog_t7.py` |
| `rprog-t8` | Data frames, data input and output, graphics and plots | Apply | 2 | 1.3 | v1.0 · 70 min · 12 scenes (`seed/lesson_rprog_t8.json`) | 20 items (`seed/rprog_t8_mastery.json`) |  | none | `verify_rprog_t8.py` |
| `rprog-t9` | LaTeX and word processing software | Recall | 2 | 1.3 | v1.0 · 55 min · 12 scenes (`seed/lesson_rprog_t9.json`) | 20 items (`seed/rprog_t9_mastery.json`) |  | none | `verify_rprog_t9.py` |
| `sampling-t1` | Horvitz–Thompson and varying probability sampling | Derive | 2 | 1.1 | v1.0 · 95 min · 13 scenes (`seed/lesson_sampling_t1.json`) | 20 items (`seed/sampling_t1_mastery.json`) | j26 Q8 | `lesson_sampling_t1.py` | `verify_sampling.py` |
| `sampling-t2` | Stratified sampling and allocation | Derive | 2 | 1.1 | v1.0 · 95 min · 13 scenes (`seed/lesson_sampling_t2.json`) | 20 items (`seed/sampling_t2_mastery.json`) |  | `lesson_sampling_t2.py` | none |
| `sampling-t3` | Ratio and regression estimators | Apply | 2 | 1.1 | v1.1 · 95 min · 13 scenes (`seed/lesson_sampling_t3.json`) | 20 items (`seed/sampling_t3_mastery.json`) |  | `lesson_sampling_t3.py` | none |
| `sampling-t4` | Cluster sampling | State | 2 | 1.1 | v1.1 · 95 min · 13 scenes (`seed/lesson_sampling_t4.json`) | 20 items (`seed/sampling_t4_mastery.json`) | j26 Q36 | `lesson_sampling_t4.py` | `verify_sampling_t4.py` |
| `sampling-t5` | Systematic sampling | State | 2 | 1.1 | v1.1 · 95 min · 13 scenes (`seed/lesson_sampling_t5.json`) | 20 items (`seed/sampling_t5_mastery.json`) |  | `lesson_sampling_t5.py` | none |
| `sampling-t6` | PPS schemes and their estimators | Recall | 2 | 1.1 | v1.1 · 95 min · 13 scenes (`seed/lesson_sampling_t6.json`) | 20 items (`seed/sampling_t6_mastery.json`) |  | `lesson_sampling_t6.py` | none |
| `sampling-t7` | Two-stage, multi-stage and double sampling | State | 2 | 1.1 | v1.1 · 95 min · 13 scenes (`seed/lesson_sampling_t7.json`) | 20 items (`seed/sampling_t7_mastery.json`) | j26 Q36 | `lesson_sampling_t7.py` | `verify_sampling_t7.py` |
| `sampling-t8` | Non-sampling errors | Recall | 2 | 1.1 | v1.1 · 95 min · 13 scenes (`seed/lesson_sampling_t8.json`) | 20 items (`seed/sampling_t8_mastery.json`) |  | `lesson_sampling_t8.py` | none |
| `sampling-t9` | Nonnegative variance estimation, ordered and unordered estimators | Derive | 2 | 1.1 | v1.1 · 95 min · 13 scenes (`seed/lesson_sampling_t9.json`) | 20 items (`seed/sampling_t9_mastery.json`) |  | `lesson_sampling_t9.py` | none |
| `design-t1` | ANOVA tables and degrees of freedom | Derive | 2 | 1.2 | v4.1 · 96 min · 14 scenes (`seed/lesson_design_t1.json`) | 20 items (`seed/design_t1_mastery.json`) |  | `lesson_design_t1.py` | `verify_design_t1.py` |
| `design-t2` | CRD, RBD, Latin square | Derive | 2 | 1.2 | v4.1 · 92 min · 14 scenes (`seed/lesson_design_t2.json`) | 20 items (`seed/design_t2_mastery.json`) |  | `lesson_design_t2.py` | `verify_design_t2.py` |
| `design-t3` | Factorial experiments | Derive | 2 | 1.2 | v4.1 · 96 min · 14 scenes (`seed/lesson_design_t3.json`) | 20 items (`seed/design_t3_mastery.json`) |  | `lesson_design_t3.py` | `verify_design_t3.py` |
| `design-t4` | BIBD and incidence matrices | Apply | 2 | 1.2 | v4.1 · 92 min · 15 scenes (`seed/lesson_design_t4.json`) | 20 items (`seed/design_t4_mastery.json`) |  | `lesson_design_t4.py` | `verify_design_t4.py` |
| `design-t5` | Principles of design | Recall | 2 | 1.2 | v4.1 · 88 min · 15 scenes (`seed/lesson_design_t5.json`) | 20 items (`seed/design_t5_mastery.json`) |  | `lesson_design_t5.py` | `verify_design_t5.py` |
| `design-t6` | Confounding, split-plot, PBIBD | State | 2 | 1.2 | v4.1 · 104 min · 15 scenes (`seed/lesson_design_t6.json`) | 20 items (`seed/design_t6_mastery.json`) |  | `lesson_design_t6.py` | `verify_design_t6.py` |
| `design-t7` | Missing plot technique | Apply | 2 | 1.2 | v4.1 · 96 min · 15 scenes (`seed/lesson_design_t7.json`) | 20 items (`seed/design_t7_mastery.json`) |  | `lesson_design_t7.py` | `verify_design_t7.py` |
| `design-t8` | Connectedness and orthogonality of block designs | Recall | 2 | 1.2 | v4.1 · 100 min · 15 scenes (`seed/lesson_design_t8.json`) | 20 items (`seed/design_t8_mastery.json`) |  | `lesson_design_t8.py` | `verify_design_t8.py` |
| `official-t1` | CSO, NSSO, NSO, MoSPI, NSC | Recall | 2 | 1.6 | v1.0 · 79 min · 13 scenes (`seed/lesson_10a1.json`) | 20 items (`seed/official_t1_mastery.json`) |  | `lesson_10a1.py` | none |
| `official-t2` | Commissions and committees | Recall | 2 | 1.6 | v1.0 · 80 min · 13 scenes (`seed/lesson_10a2.json`) | 20 items (`seed/official_t2_mastery.json`) |  | `lesson_10a2.py` | none |
| `official-t3` | Indian statisticians | Recall | 2 | 1.6 | v1.0 · 80 min · 13 scenes (`seed/lesson_10a3.json`) | 20 items (`seed/official_t3_mastery.json`) |  | `lesson_10a3.py` | none |
| `official-t4` | Major surveys and indices | Recall | 2 | 1.6 | v1.1 · 84 min · 13 scenes (`seed/lesson_10a4.json`) | 20 items (`seed/official_t4_mastery.json`) |  | `lesson_10a4.py` | none |
| `official-t5` | Census and vital statistics | Recall | 2 | 1.6 | v1.2 · 83 min · 13 scenes (`seed/lesson_10a5.json`) | 20 items (`seed/official_t5_mastery.json`) |  | `lesson_10a5.py` | none |
| `nonparam-t1` | Mann–Whitney U | Derive | 2 | 0.8 | v1.0 · 96 min · 15 scenes (`seed/lesson_nonparam_t1.json`) | 20 items (`seed/nonparam_t1_mastery.json`) | j26 Q33, j26 Q42 | `lesson_nonparam_t1.py` | none |
| `nonparam-t2` | Wilcoxon signed-rank and sign test | Apply | 2 | 0.8 | v1.0 · 96 min · 15 scenes (`seed/lesson_nonparam_t2.json`) | 20 items (`seed/nonparam_t2_mastery.json`) | j26 Q42 | `lesson_nonparam_t2.py` | none |
| `nonparam-t3` | Kruskal–Wallis and Friedman | Apply | 2 | 0.8 | v1.0 · 96 min · 15 scenes (`seed/lesson_nonparam_t3.json`) | 20 items (`seed/nonparam_t3_mastery.json`) |  | `lesson_nonparam_t3.py` | none |
| `nonparam-t4` | Spearman and Kendall | Derive | 2 | 0.8 | v1.0 · 100 min · 16 scenes (`seed/lesson_np4.json`) | 20 items (`seed/nonparam_t4_mastery.json`) | j26 Q35 | `lesson_np4.py` | none |
| `nonparam-t5` | Matching test to design | Recall | 2 | 0.8 | v1.0 · 96 min · 15 scenes (`seed/lesson_nonparam_t5.json`) | 20 items (`seed/nonparam_t5_mastery.json`) | j26 Q42 | `lesson_nonparam_t5.py` | none |
| `nonparam-t6` | Kolmogorov–Smirnov, run test | State | 2 | 0.8 | v1.0 · 96 min · 15 scenes (`seed/lesson_nonparam_t6.json`) | 20 items (`seed/nonparam_t6_mastery.json`) | j26 Q33, j26 Q42 | `lesson_nonparam_t6.py` | none |
| `nonparam-t7` | Empirical distribution function and its properties | Derive | 2 | 0.8 | v1.0 · 96 min · 15 scenes (`seed/lesson_nonparam_t7.json`) | 20 items (`seed/nonparam_t7_mastery.json`) | j26 Q33, j26 Q42 | `lesson_nonparam_t7.py` | none |
| `nonparam-t8` | Linear rank tests for location and scale | Apply | 2 | 0.8 | v1.0 · 96 min · 15 scenes (`seed/lesson_nonparam_t8.json`) | 20 items (`seed/nonparam_t8_mastery.json`) | j26 Q33, j26 Q42 | `lesson_nonparam_t8.py` | none |
| `p1-highered-t1` | Governance, UGC, AICTE, NAAC, NCTE | Recall | 2 | 3.3 | — | — |  |  |  |
| `p1-highered-t2` | Types of universities | Recall | 2 | 3.3 | — | — |  |  |  |
| `p1-highered-t3` | NEP 2020 and HECI | Recall | 2 | 3.3 | — | — |  |  |  |
| `p1-highered-t4` | Schemes, platforms, institutions | Recall | 2 | 3.3 | — | — |  |  |  |
| `p1-highered-t5` | Commissions and policies | Recall | 2 | 3.3 | — | — |  |  |  |
| `p1-highered-t6` | National integration | Recall | 2 | 3.3 | — | — |  |  |  |
| `p1-mathreason-t1` | Number series | Derive | 2 | 3 | — | — |  |  |  |
| `p1-mathreason-t2` | Percentages, profit and loss | Derive | 2 | 3 | — | — |  |  |  |
| `p1-mathreason-t3` | Interest and ratios | Derive | 2 | 3 | — | — |  |  |  |
| `p1-mathreason-t4` | Basic statistics in Paper 1 | Apply | 2 | 3 | — | — |  |  |  |
| `p1-logical-t1` | Syllogisms | Apply | 2 | 2.4 | — | — |  |  |  |
| `p1-logical-t2` | Indian logic | Recall | 2 | 2.4 | — | — |  |  |  |
| `p1-logical-t3` | Analogies and classification | Apply | 2 | 2.4 | — | — |  |  |  |
| `p1-logical-t4` | Coding and decoding | Apply | 2 | 2.4 | — | — |  |  |  |
| `p1-logical-t5` | Fallacies | State | 2 | 2.4 | — | — |  |  |  |
| `p1-ict-t1` | Generations and hardware | Recall | 2 | 3 | — | — |  |  |  |
| `p1-ict-t2` | Networking and internet | Recall | 2 | 3 | — | — |  |  |  |
| `p1-ict-t3` | Security terms | Recall | 2 | 3 | — | — |  |  |  |
| `p1-ict-t4` | E-governance and digital initiatives | Recall | 2 | 3 | — | — |  |  |  |
| `p1-di-t1` | Tables | Apply | 2 | 2.5 | — | — |  |  |  |
| `p1-di-t2` | Bar and line charts | Apply | 2 | 2.5 | — | — |  |  |  |
| `p1-di-t3` | Pie charts | Apply | 2 | 2.5 | — | — |  |  |  |
| `p1-di-t4` | Speed drills | Apply | 2 | 2.5 | — | — |  |  |  |
| `p1-teaching-t1` | Learner characteristics | State | 2 | 2.5 | — | — |  |  |  |
| `p1-teaching-t2` | Methods of teaching | State | 2 | 2.5 | — | — |  |  |  |
| `p1-teaching-t3` | Evaluation systems | Recall | 2 | 2.5 | — | — |  |  |  |
| `p1-teaching-t4` | Theories of learning | Recall | 2 | 2.5 | — | — |  |  |  |
| `p1-environment-t1` | Pollution types and effects | Recall | 2 | 2.5 | — | — |  |  |  |
| `p1-environment-t2` | Natural hazards and disasters | Recall | 2 | 2.5 | — | — |  |  |  |
| `p1-environment-t3` | Energy resources | Recall | 2 | 2.5 | — | — |  |  |  |
| `p1-environment-t4` | Environmental protocols | Recall | 2 | 2.5 | — | — |  |  |  |
| `p1-communication-t1` | Types and barriers | Recall | 2 | 2.7 | — | — |  |  |  |
| `p1-communication-t2` | Mass media | Recall | 2 | 2.7 | — | — |  |  |  |
| `p1-communication-t3` | Classroom communication | State | 2 | 2.7 | — | — |  |  |  |
| `p1-research-t1` | Types and methods of research | State | 2 | 1.5 | — | — |  |  |  |
| `p1-research-t2` | Research ethics | Recall | 2 | 1.5 | — | — |  |  |  |
| `p1-research-t3` | Thesis and paper writing | Recall | 2 | 1.5 | — | — |  |  |  |
| `p1-research-t4` | Sampling in research | State | 2 | 1.5 | — | — |  |  |  |

## Past paper `j26`: UGC NET June 2026 — Paper 2, questions 1–50 (actual paper), question by question

`marked` is what the candidate marked; a question is a priority when it was answered wrongly.

| Q | Format | Key | Marked | Named by lesson | Variant bank |
|---|---|---|---|---|---|
| 1 | single | D | C ✗ | maths-t1 | maths_pyq_variants |
| 2 | single | D | A ✗ | multivariate-t3, timeseries-t3 | maths_pyq_variants, multivariate_pyq_variants |
| 3 | single | A | B ✗ | timeseries-t3 | timeseries_pyq_variants |
| 4 | single | C | B ✗ | multivariate-t4 | inference_pyq_variants |
| 5 | single | C | C | — | maths_pyq_variants |
| 6 | single | A | B ✗ | inference-t1, probability-t5 | probability_pyq_variants |
| 7 | single | D | D | timeseries-t7 | timeseries_pyq_variants |
| 8 | single | C | D ✗ | sampling-t1 | inference_pyq_variants, sampling_pyq_variants |
| 9 | single | B | A ✗ | regression-t1, regression-t3, regression-t4, regression-t8 | regression_pyq_variants |
| 10 | single | A | B ✗ | inference-t13 | inference_pyq_variants |
| 11 | single | B | D ✗ | regression-t8 | regression_pyq_variants |
| 12 | single | D | C ✗ | — | inference_pyq_variants |
| 13 | single | A | D ✗ | probability-t1 | probability_pyq_variants |
| 14 | single | D | A ✗ | inference-t17 | inference_pyq_variants |
| 15 | single | A | A | — | probability_pyq_variants |
| 16 | single | C | C | rprog-t1 | rprog_pyq_variants |
| 17 | single | B | B | multivariate-t5 | probability_pyq_variants |
| 18 | single | C | A ✗ | timeseries-t3, timeseries-t5 | timeseries_pyq_variants |
| 19 | single | C | A ✗ | — | probability_pyq_variants |
| 20 | single | B | B | multivariate-t6 | multivariate_pyq_variants |
| 21 | single | A | A | — | rprog_pyq_variants |
| 22 | single | D | B ✗ | rprog-t2 | — |
| 23 | single | D | D | timeseries-t6 | timeseries_pyq_variants |
| 24 | single | B | B | multivariate-t1 | multivariate_pyq_variants |
| 25 | single | C | D ✗ | maths-t1, probability-t10 | probability_pyq_variants |
| 26 | single | B | C ✗ | maths-t1 | maths_pyq_variants |
| 27 | single | D | D | — | maths_pyq_variants |
| 28 | single | C | D ✗ | inference-t14, maths-t4 | maths_pyq_variants |
| 29 | single | C | B ✗ | inference-t14, inference-t16 | maths_pyq_variants |
| 30 | single | C | A ✗ | inference-t10 | inference_pyq_variants |
| 31 | single | C | C | inference-t10, probability-t7 | inference_pyq_variants |
| 32 | single | C | C | — | probability_pyq_variants |
| 33 | single | C | C | inference-t16, nonparam-t1, nonparam-t6, nonparam-t7, nonparam-t8 | nonparam_pyq_variants |
| 34 | single | D | A ✗ | probability-t8 | probability_pyq_variants |
| 35 | single | B | C ✗ | nonparam-t4, probability-t7 | maths_pyq_variants |
| 36 | single | D | B ✗ | sampling-t4, sampling-t7 | official_pyq_variants, sampling_pyq_variants |
| 37 | single | D | B ✗ | multivariate-t7 | inference_pyq_variants |
| 38 | single | C | B ✗ | regression-t8 | regression_pyq_variants |
| 39 | single | B | D ✗ | inference-t12 | inference_pyq_variants |
| 40 | single | C | B ✗ | — | inference_pyq_variants |
| 41 | single | D | A ✗ | — | nonparam_pyq_variants |
| 42 | single | A | C ✗ | nonparam-t1, nonparam-t2, nonparam-t5, nonparam-t6, nonparam-t7, nonparam-t8 | nonparam_pyq_variants |
| 43 | single | D | A ✗ | inference-t12, inference-t15 | inference_pyq_variants |
| 44 | single | B | B | — | probability_pyq_variants |
| 45 | single | D | A ✗ | probability-t3 | probability_pyq_variants |
| 46 | single | C | B ✗ | probability-t13, probability-t3 | probability_pyq_variants |
| 47 | single | C | B ✗ | — | official_pyq_variants |
| 48 | single | B | B | — | rprog_pyq_variants |
| 49 | single | B | A ✗ | inference-t12 | inference_pyq_variants |
| 50 | order | D | D | — | rprog_pyq_variants |

## What to build or fix next

### Topics without a lesson, most marks first (top 25)

| Topic | Module | Marks | Extent |
|---|---|---|---|
| `p1-highered-t1` Governance, UGC, AICTE, NAAC, NCTE | p1-highered | 3.3 | Recall |
| `p1-highered-t2` Types of universities | p1-highered | 3.3 | Recall |
| `p1-highered-t3` NEP 2020 and HECI | p1-highered | 3.3 | Recall |
| `p1-highered-t4` Schemes, platforms, institutions | p1-highered | 3.3 | Recall |
| `p1-highered-t5` Commissions and policies | p1-highered | 3.3 | Recall |
| `p1-highered-t6` National integration | p1-highered | 3.3 | Recall |
| `p1-ict-t1` Generations and hardware | p1-ict | 3 | Recall |
| `p1-ict-t2` Networking and internet | p1-ict | 3 | Recall |
| `p1-ict-t3` Security terms | p1-ict | 3 | Recall |
| `p1-ict-t4` E-governance and digital initiatives | p1-ict | 3 | Recall |
| `p1-mathreason-t1` Number series | p1-mathreason | 3 | Derive |
| `p1-mathreason-t2` Percentages, profit and loss | p1-mathreason | 3 | Derive |
| `p1-mathreason-t3` Interest and ratios | p1-mathreason | 3 | Derive |
| `p1-mathreason-t4` Basic statistics in Paper 1 | p1-mathreason | 3 | Apply |
| `p1-communication-t1` Types and barriers | p1-communication | 2.7 | Recall |
| `p1-communication-t2` Mass media | p1-communication | 2.7 | Recall |
| `p1-communication-t3` Classroom communication | p1-communication | 2.7 | State |
| `p1-di-t1` Tables | p1-di | 2.5 | Apply |
| `p1-di-t2` Bar and line charts | p1-di | 2.5 | Apply |
| `p1-di-t3` Pie charts | p1-di | 2.5 | Apply |
| `p1-di-t4` Speed drills | p1-di | 2.5 | Apply |
| `p1-environment-t1` Pollution types and effects | p1-environment | 2.5 | Recall |
| `p1-environment-t2` Natural hazards and disasters | p1-environment | 2.5 | Recall |
| `p1-environment-t3` Energy resources | p1-environment | 2.5 | Recall |
| `p1-environment-t4` Environmental protocols | p1-environment | 2.5 | Recall |

### Past paper `j26`: questions with no lesson and no variant bank

None.

### Lessons and pools to tighten

- `inference-t1`: no verification script mentions this topic
- `inference-t2`: no verification script mentions this topic
- `inference-t3`: no verification script mentions this topic
- `inference-t4`: no verification script mentions this topic
- `inference-t5`: no verification script mentions this topic
- `inference-t6`: no verification script mentions this topic
- `inference-t7`: no verification script mentions this topic
- `inference-t8`: no verification script mentions this topic
- `inference-t9`: no verification script mentions this topic
- `inference-t10`: no verification script mentions this topic
- `inference-t11`: no verification script mentions this topic
- `inference-t12`: no verification script mentions this topic
- `inference-t13`: no verification script mentions this topic
- `inference-t14`: no verification script mentions this topic
- `inference-t15`: no verification script mentions this topic
- `inference-t16`: no verification script mentions this topic
- `inference-t17`: no verification script mentions this topic
- `probability-t1`: no verification script mentions this topic
- `probability-t2`: no verification script mentions this topic
- `probability-t3`: no verification script mentions this topic
- `probability-t4`: no verification script mentions this topic
- `probability-t5`: no verification script mentions this topic
- `probability-t6`: no verification script mentions this topic
- `probability-t7`: no verification script mentions this topic
- `probability-t8`: no verification script mentions this topic
- `probability-t9`: no verification script mentions this topic
- `probability-t10`: no verification script mentions this topic
- `probability-t11`: no verification script mentions this topic
- `probability-t12`: no verification script mentions this topic
- `probability-t13`: no verification script mentions this topic
- `timeseries-t1`: no verification script mentions this topic
- `timeseries-t2`: no verification script mentions this topic
- `timeseries-t3`: no verification script mentions this topic
- `timeseries-t4`: no verification script mentions this topic
- `timeseries-t5`: no verification script mentions this topic
- `timeseries-t6`: no verification script mentions this topic
- `timeseries-t7`: no verification script mentions this topic
- `timeseries-t8`: no verification script mentions this topic
- `timeseries-t9`: no verification script mentions this topic
- `timeseries-t10`: no verification script mentions this topic
- `timeseries-t11`: no verification script mentions this topic
- `maths-t1`: no verification script mentions this topic
- `maths-t2`: no verification script mentions this topic
- `maths-t3`: no verification script mentions this topic
- `maths-t4`: no verification script mentions this topic
- `maths-t5`: no verification script mentions this topic
- `maths-t6`: no verification script mentions this topic
- `maths-t7`: no verification script mentions this topic
- `maths-t8`: no verification script mentions this topic
- `maths-t9`: no verification script mentions this topic
- `maths-t10`: no verification script mentions this topic
- `maths-t11`: no verification script mentions this topic
- `maths-t12`: no verification script mentions this topic
- `maths-t13`: no verification script mentions this topic
- `maths-t14`: no verification script mentions this topic
- `maths-t15`: no verification script mentions this topic
- `maths-t16`: no verification script mentions this topic
- `sampling-t2`: no verification script mentions this topic
- `sampling-t3`: no verification script mentions this topic
- `sampling-t5`: no verification script mentions this topic
- `sampling-t6`: no verification script mentions this topic
- `sampling-t8`: no verification script mentions this topic
- `sampling-t9`: no verification script mentions this topic
- `official-t1`: no verification script mentions this topic
- `official-t2`: no verification script mentions this topic
- `official-t3`: no verification script mentions this topic
- `official-t4`: no verification script mentions this topic
- `official-t5`: no verification script mentions this topic
- `nonparam-t1`: no verification script mentions this topic
- `nonparam-t2`: no verification script mentions this topic
- `nonparam-t3`: no verification script mentions this topic
- `nonparam-t4`: no verification script mentions this topic
- `nonparam-t5`: no verification script mentions this topic
- `nonparam-t6`: no verification script mentions this topic
- `nonparam-t7`: no verification script mentions this topic
- `nonparam-t8`: no verification script mentions this topic

## Where things live

| What | Where | Edit by |
|---|---|---|
| A lesson, once merged | `seed/lesson_<stem>.json` | edit the JSON directly (docs/CONTENT_GUIDE.md, 3a); a new lesson starts from `lessons/TEMPLATE.py` and `./addlesson.sh` |
| A lesson's mastery pool (20 questions) | `seed/<topic>_mastery.json` | the same: edit the JSON once merged |
| Previous-year variant banks | `seed/<module>_pyq_variants.json` | edit the JSON; `npm run check` validates it |
| A past paper, with keys and what was marked | `seed/pyq_<id>_full.json` (`source: "pyq"`); `pyq_j26_full.json` is June 2026 | rarely; keys are facts. A new paper is a new file; see docs/CONTENT_GUIDE.md, 3d |
| Which past questions a lesson is built on | the lesson's `anchors` field: `[{ "paper": "j26", "q": 38 }]` | edit the lesson JSON; CI checks every anchor exists |
| Modules, topics, marks, extent | `seed/catalog.json`; unit numbers in `seed/meta_syllabus.json` | the owner; changes move marks |
| Numbers a lesson relies on | `verify_<group>.py` | whoever authors the lesson |

