# BACKLOG — what to build next, and why

This file is the queue. **Take the top unchecked item**, build it, tick it off, commit.

Ordering is by **marks still exposed** = module marks × (1 − topic coverage), then by whether a
previous-year anchor exists. An anchor that was *answered wrongly* is worth more than one answered
correctly, because the variant bank then doubles as a diagnosis.

> **The figures in this file are a snapshot from an earlier date and are not kept current.** For the live picture, run
> `npm run content -- gaps` (or read `CONTENT_MAP.md` on the `content-map` branch): it recomputes lessons, coverage and the
> topics with the most marks still unbuilt from the files themselves. Use this file for the reasoning, not the numbers.

Current state: the live lesson count is `counts.lessons` in `site/manifest.json` (`npm run build`, or `/manifest.json` on the deployed site).
The older 43-lesson snapshot and the artifact page and store figures are retired.
Figures below come from `seed/catalog.json` (marks, baseline), the lesson index generated from `seed/lesson_*.json`
(`node tools/gen-index.js`; it is never committed) and `seed/pyq_j26_full.json` (what was answered correctly).

---

## Exposure table

| Module | Marks | June 2026 | Lessons | Bank | **Exposed** |
|---|---|---|---|---|---|
| **Regression** | 22 | 3/11 | 0/15 | ✓ 3 wrong anchors | **22.0** |
| Stochastic processes | 20 | 2/10 | 0/9 | ✗ none | 20.0 |
| Paper 1 — higher education | 20 | 6/10 | 0/6 | ✗ none | 20.0 |
| Multivariate | 18 | 4/9 | 0/9 | ✓ 2 right anchors | 18.0 |
| Mathematics | 18 | 2/9 | 2/16 | ✓ anchors mostly consumed | 15.8 |
| Paper 1 — ICT | 12 | 4/6 | 0/4 | ✗ none | 12.0 |
| Paper 1 — logical reasoning | 12 | 4/6 | 0/5 | ✗ none | 12.0 |
| Paper 1 — maths reasoning | 12 | 3/6 | 0/4 | ✗ none | 12.0 |
| R programming | 12 | **4/6** | 0/9 | ✓ 4 right anchors | 12.0 |
| Probability | 22 | 3/11 | 7/13 | ✓ anchors consumed | 10.2 |
| Sampling theory | 10 | 2/5 | 0/9 | ✗ none | 10.0 |
| Design of experiments | 10 | 2/5 | 0/8 | ✗ none | 10.0 |
| Non-parametric | 6 | 0/3 | 1/8 | ✓ anchor consumed | 5.2 |
| Estimation theory | 34 | 2/17 | **17/17** | — | 0 |
| Time series | 20 | 6/10 | **11/11** | — | 0 |
| Official statistics | 8 | 1/4 | **5/5** | — | 0 |

R programming is deliberately low priority despite 12 marks exposed: **4 of 6 were already
correct with no lessons at all.** Coverage is not the same as need.

---

## 1 — Regression (22 marks, scored 3/11, nothing built)

The strongest target available. Three anchors, **all answered wrongly**, each with a variant bank.

- [ ] **regression-t2** — Gauss–Markov, BLUE, estimability · anchor **Q11**, 6 variants, key B marked D
      The three-equation setup (y₁ = β₁+β₂+u₁, y₂ = 2β₁+u₂, y₃ = β₁−β₂+u₃) is a classic
      estimability question. Verify which linear combinations are estimable by construction.
- [ ] **regression-t5** — Multicollinearity · anchor **Q38**, 4 variants, key C marked B
      "Which is *not* a consequence" — a negation question, so the lesson must drill what
      multicollinearity does and does not do to the OLS estimator.
- [ ] **regression-t1** — Hat matrix, residual maker, quadratic forms · anchor **Q9**, 10 variants,
      key B marked A. Read the full stem before assigning: Q9 may belong to t1 or t2.
- [ ] regression-t3 — ANOVA decomposition and the F test from R²
- [ ] regression-t4 — R², adjusted R², model comparison
- [ ] regression-t7 — Heteroscedasticity and GLS
- [ ] regression-t6 — Autocorrelation and Durbin–Watson *(cross-reference time series 7.2)*
- [ ] regression-t11 — Indicator and dummy variables
- [ ] regression-t8 — Endogeneity and instrumental variables
- [ ] regression-t10 — Two-stage least squares
- [ ] regression-t9 — Identification in simultaneous equations
- [ ] regression-t12 — Logistic regression models
- [ ] regression-t13 — Restricted regression: exact, stochastic and mixed restrictions
- [ ] regression-t14 — Errors in variables and stochastic regressors
- [ ] regression-t15 — k-class estimators

## 2 — Multivariate (18 marks, scored 4/9, nothing built)

Two anchors, both answered *correctly*, so they specify content without diagnosing a weakness.

- [ ] **multivariate-t3** — Principal component analysis · anchor **Q2** (9 variants) sits in the
      *time-series* variant file and is a PCA question. Move those variants before authoring.
- [ ] multivariate-t1 — Multivariate normal: marginals and conditionals
- [ ] multivariate-t4 — Hotelling's T²
- [ ] multivariate-t2 — Partial and multiple correlation
- [ ] multivariate-t7 — MLE of mean vector and covariance
- [ ] multivariate-t8 — Mahalanobis distance, discriminant analysis, MANOVA
- [ ] multivariate-t5 — Wishart distribution
- [ ] multivariate-t6 — Canonical correlation
- [ ] multivariate-t9 — Factor and cluster analysis

## 3 — Stochastic processes (20 marks, scored 2/10, nothing built, NO question bank)

20 marks with zero coverage — the largest single gap — but a **question bank has to be written
first**, which is a different and longer job than authoring a lesson. Treat the bank as task zero.

- [ ] **Write the question bank** — 9 topics, enough items to seed mastery pools
- [ ] stochastic-t1 — Markov chains: n-step, Chapman–Kolmogorov
- [ ] stochastic-t2 — Stationary distribution
- [ ] stochastic-t4 — Classification of states
- [ ] stochastic-t5 — Poisson process *(cross-reference probability 1.5)*
- [ ] stochastic-t3 — First passage and first return, mean passage time
- [ ] stochastic-t6 — Gambler's ruin and random walks *(cross-reference time series 7.6)*
- [ ] stochastic-t7 — Birth–death and M/M/1
- [ ] stochastic-t8 — Branching processes
- [ ] stochastic-t9 — Renewal processes

## 4 — Mathematics (15.8 exposed, scored 2/9, 2 of 16 built)

The worst module score on the paper. Its two remaining wrongly-answered anchors are both
**misfiled to other modules** — Q2 is a PCA question and Q29 a goodness-of-fit question — so the
remaining topics are catalog-weight lessons with no anchor of their own.

- [ ] maths-t2 — Eigenvalues, eigenvectors, Cayley–Hamilton
- [ ] maths-t3 — Quadratic forms and positive definiteness *(feeds regression-t1)*
- [ ] maths-t16 — Trace, determinant and inverse of a matrix
- [ ] maths-t13 — Vector spaces, basis, dimension, row and column space
- [ ] maths-t14 — Systems of linear equations and row reduced echelon form
- [ ] maths-t8 — Generalised inverse *(feeds regression-t2 estimability)*
- [ ] maths-t15 — Gram–Schmidt orthogonalisation and orthogonal matrices
- [ ] maths-t5 — Continuity, differentiability, Rolle, MVT
- [ ] maths-t9 — Taylor's theorem, L'Hôpital's rule, uniform continuity
- [ ] maths-t6 — Maxima, minima, local extrema
- [ ] maths-t11 — Saddle points and Lagrange multipliers
- [ ] maths-t7 — Riemann and improper integrals
- [ ] maths-t10 — Functions of two variables: partial and total derivatives
- [ ] maths-t12 — Double and triple integrals and their applications

## 5 — Probability, finishing the module (10.2 exposed, 7 of 13 built)

No anchors remain; the bank's probability questions are all consumed.

- [ ] probability-t9 — Convergence, WLLN, SLLN, CLT *(builds on 1.7's Chebyshev)*
- [ ] probability-t4 — MGFs, cumulants, central moments
- [ ] probability-t6 — Standard continuous distributions *(completes 1.5)*
- [ ] probability-t12 — Bayes theorem and conditional probability
- [ ] probability-t2 — Conditional distributions *(completes 1.3)*
- [ ] probability-t11 — Characteristic functions

## 6 — Non-parametric, finishing the module (5.2 exposed, 1 of 8 built)

Low marks, but **0 of 3 correct** in June 2026, and 5.4 has already laid the permutation-test
groundwork the rest of the module reuses.

- [ ] nonparam-t1 — Mann–Whitney U
- [ ] nonparam-t2 — Wilcoxon signed-rank and sign test
- [ ] nonparam-t3 — Kruskal–Wallis and Friedman
- [ ] nonparam-t6 — Kolmogorov–Smirnov, run test
- [ ] nonparam-t7 — Empirical distribution function and its properties
- [ ] nonparam-t5 — Matching test to design
- [ ] nonparam-t8 — Linear rank tests for location and scale

---

## Paper 1 — 100 marks, nothing built, no banks

**This is a strategic decision, not a queue item.** The project brief covers both papers; all 43
lessons so far are Paper 2. Paper 1 is nine modules totalling 100 marks with no lessons and no
question banks, and it holds the weakest scores anywhere on either paper.

| Module | Marks | June 2026 |
|---|---|---|
| Higher education system | 20 | 6/10 |
| Mathematical reasoning | 12 | 3/6 |
| Logical reasoning | 12 | 4/6 |
| ICT | 12 | 4/6 |
| Teaching aptitude | 10 | 3/5 |
| **Environment** | 10 | **1/5** |
| Data interpretation | 10 | 2/5 |
| Communication | 8 | 3/4 |
| **Research aptitude** | 6 | **1/3** |

About 46 marks are being lost here on a paper that counts toward the JRF aggregate. Environment
at 1/5 and research aptitude at 1/3 are the two weakest results in the whole attempt.

Opening this up means writing question banks from scratch for nine modules — a large job, and a
real split of effort away from the subject paper. Decide deliberately.

---

## Deliberately not next

- **Deepening estimation theory 4.2–4.6 and 4.9** from 46–56 min to the ~90 min standard. Those
  six topics drew one question between them. Thin-but-correct beats absent.
- **More official statistics.** Five lessons already serve an 8-mark module whose questions were
  pure recall. Overfunded.
- **R programming.** 4 of 6 correct with no lessons at all.
- **Practice sets distinct from mastery pools** for 4.1–4.6 and 4.9.

## Housekeeping, worth doing alongside

- [ ] Move Q2's PCA variants out of the time-series file into multivariate
- [ ] Audit Q22 — still showing zero variants, which usually means it is mistagged
- [ ] Re-check `youMarked` against `answer` for every question before calling it wrongly answered
      (Q31 was listed as wrong in the priority doc for weeks and was in fact correct)
