# 1000 MCQ Statistics PDF — supplementary batch 2 audit

## Scope
UGC NET/JRF Statistics Paper 2 only. These are source-derived supplementary practice questions, not attributed official PYQs. Source: `1000 MCQ statistics.pdf`.

## Added after page-image verification

| PDF page | New item ID | Topic | Format | Verified answer |
|---|---|---|---|---|
| 1016 | `mcq1000-p1016` | Probability — Bayes theorem and conditional probability (`probability-t12`) | Single choice | C — (1/2^9=1/512) |
| 1020 | `mcq1000-p1020` | Probability — independence and inclusion–exclusion (`probability-t8`) | Multi-select | A — statements A and C only |

### Page 1016
The scan states that a randomly selected child is found to be a girl. Conditional on this observation, the selected child is already known to be a girl; the remaining nine independent children must all be girls. The probability is therefore ((1/2)^9). The scan's marked answer is option 3, matching option C in the repository's letter-labelled format.

### Page 1020
The scan gives independent (X\sim U(0,2)) and (Y\sim U(1,3)), and asks which of four probability statements about (X<Y), (X+Y\ge4), (X-Y\le-1), and (X>Y) are correct. The joint support is a rectangle of area 4. Geometric area calculations give:
- (P(X>Y)=1/8), hence (P(X<Y)=7/8);
- (P(X+Y\ge4)=1/8);
- (P(X-Y\le-1)=1/2).

Thus statements A and C are true. The scan marks statements 1 and 3. The source's four-statement form was converted to the repository's multi-select combination-option contract; the four source statements were retained.

## Held out during this page-range review
- Page 1017: the displayed CLT answer option appears inconsistent with standardization of the stated Rademacher sum; not imported.
- Page 1018: the condition involving (X_K=K) and the geometric parameterization are not sufficiently clear in the scan; not imported.
- Page 1019: the expression involving (55\alpha^2) is visually ambiguous (the answer options suggest a possible superscript on 55); not imported.
- Page 1021: Gamma parameterization is not specified, so options A and D depend on convention; not imported.

## Duplicate/quality cautions
Pages 1022/1029 and 1027/1028 appeared duplicated in the initial contact-sheet review. They were not imported in this batch. OCR was used only to locate candidate material; final transcription and answer checks above were made from enlarged page images.

## Batch count
The Probability supplementary pool on the batch-2 branch increases from 394 to 396 items. The full repository-wide semantic duplicate audit and the remaining unreviewed pages are still outstanding; this batch does not claim the full PDF is complete.


## Further verified additions — pages 1023–1042

The following questions were visually transcribed from enlarged page images, solved independently, and added with worked explanations:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 1023 | `mcq1000-p1023` | Probability T5 — Poisson distribution | A (0.7619) |
| 1024 | `mcq1000-p1024` | Probability T13 — t sampling distribution / paired t statistic | C (5.2856) |
| 1025 | `mcq1000-p1025` | Probability T6 — normal distribution | B (95.45%) |
| 1026 | `mcq1000-p1026` | Probability T5 — continuity correction | C ((P(Y<9.5))) |
| 1030 | `mcq1000-p1030` | Probability T6 — normal quantile | A (124.9) |
| 1031 | `mcq1000-p1031` | Probability T8 — independence and covariance | B (0) |
| 1033 | `mcq1000-p1033` | Statistical Inference T13 — confidence interval | B (̅x=14, margin=2) |
| 1034 | `mcq1000-p1034` | Probability T5 — Binomial variance | A ((p(1-p)/6)) |
| 1036 | `mcq1000-p1036` | Probability T8 — covariance from joint density | A (0.02) |
| 1038 | `mcq1000-p1038` | Probability T5 — continuity correction | A ((119.5<Y<130.5)) |
| 1040 | `mcq1000-p1040` | Probability T5 — discrete mean and standard deviation | D (μ=1.226, σ=1.123) |
| 1041 | `mcq1000-p1041` | Regression T4 — least-squares regression line | A (ŷ=1.125+1.5625x) |
| 1042 | `mcq1000-p1042` | Statistical Inference T5 — estimator MSE | A (θ(1-θ)/4) |

### Items deliberately held out

- **Page 1032:** the stated 95% margin of error does not match the listed options under the standard (z=1.96) critical value; the nearest printed option is not exact.
- **Page 1035:** the sample-size question does not state the population standard deviation (or another usable variance bound), so the answer cannot be determined.
- **Page 1037:** duplicate of the continuity-correction question on page 1026; excluded.
- **Page 1039:** multiple listed statistics are sufficient for the Bernoulli parameter: ΣXᵢ, ΣXᵢ² (equal to the sum for Bernoulli data), and a nonzero scalar multiple of the sum. The single-answer format is therefore invalid; excluded.
- **Page 1043:** an F critical value cannot be determined without a stated significance level and tail convention; excluded.
- **Page 1044:** both Σlog(Xᵢ) and its negative are one-to-one transformations and hence sufficient for θ; the single-answer options are ambiguous; excluded.
- Pages **1022/1029** and **1027/1028** were duplicates in the source scan and remain excluded.

### Current counts on this branch

- Probability supplementary pool: **406**
- Statistical Inference supplementary pool: **169**
- Regression supplementary pool: **4**
- Multivariate supplementary pool: **15**
- Stochastic supplementary pool: **7**
- Total supplementary items: **601**

These are branch counts, not production counts. The new pages have not been merged or deployed. Exact-stem and semantic duplicate reconciliation against the full set of lesson/mastery/PYQ banks remains a required review gate.


## Further verified additions — pages 761–769

Eight more questions were visually transcribed and checked:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 761 | `mcq1000-p761` | Probability T3 — conditional expectation | D, ((X_1+\theta)/2) |
| 762 | `mcq1000-p762` | Statistical Inference T12 — size of a test | C, 0 |
| 763 | `mcq1000-p763` | Statistical Inference T5 — method of moments | B, (3\bar X) |
| 765 | `mcq1000-p765` | Statistical Inference T3 — unbiased estimator properties | B, statements 2 and 3 |
| 766 | `mcq1000-p766` | Statistical Inference T3 — MVUE | D, (\sum(X_i-\mu)^2/n) |
| 767 | `mcq1000-p767` | Statistical Inference T3 — UMVU estimator | C, (\bar X^2-1/n) |
| 768 | `mcq1000-p768` | Statistical Inference T4 — Poisson MLE | A, (\bar X) |
| 769 | `mcq1000-p769` | Statistical Inference T13 — asymptotic confidence interval | B, endpoints ((1\pm1.96/\sqrt n)/\bar X) |

### Pages held out
- **Page 764:** the term “efficiency of estimator A relative to estimator B” is convention-dependent unless the variance ratio convention is stated; held out rather than guessing the intended convention.
- **Page 770:** the upper endpoint in the Uniform model is visually ambiguous between a fixed 50 and (5\theta). Since the parameter is otherwise absent if read as fixed 50, (5\theta) is plausible but not sufficiently clear to assert as a faithful transcription. Held out pending a clearer source.

### Count update
- Probability: **407**
- Statistical Inference: **176**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **7**
- Total: **609 supplementary items** on this draft branch.

Page 765 is encoded as a four-statement multi-select item. Page 769 retains the source's intended option B while explaining that the lower and upper endpoints must be read in increasing order. The new additions remain draft-only pending CI and duplicate/content review.


## Further verified additions — pages 771–780

Ten further questions were checked against enlarged source images and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 771 | `mcq1000-p771` | Statistical Inference T1 — sufficiency | B, product of observations |
| 772 | `mcq1000-p772` | Statistical Inference T12 — test size | C, 0 |
| 773 | `mcq1000-p773` | Probability T6 — harmonic mean of a continuous variable | B, 1/3 |
| 774 | `mcq1000-p774` | Probability T4 — moments of functions of normal variables | B, 2 |
| 775 | `mcq1000-p775` | Probability T9 — chi-square distribution and CLT | B, statements A, B and D |
| 776 | `mcq1000-p776` | Probability T6 — normalising a piecewise density | B, 1/25 |
| 777 | `mcq1000-p777` | Probability T12 — Bayes theorem after transfer | A, 15/29 |
| 778 | `mcq1000-p778` | Probability T12 — defective-product Bayes problem | B, 25/69 |
| 779 | `mcq1000-p779` | Probability T8 — symmetry, covariance and independence | B, statements B, C and D |
| 780 | `mcq1000-p780` | Probability T7 — covariance bound, variance and Jensen | C, statements C and D |

### Source-format adaptations
- Page 775 contains two original statements. Two additional statements were added to satisfy the platform's four-statement multi-select contract; the audit and item metadata identify the adaptation.
- Page 779 was encoded as a multi-select item, preserving the four original statements and the mathematically verified true set B, C and D.
- Page 780 was encoded as a multi-select item, preserving the four original statements and the mathematically verified true set C and D.

### Exact-stem duplicate screen
The ten new items were compared against the corresponding Probability and Statistical Inference mastery pools and the existing Probability/Inference PYQ variant banks (13 files in total). No exact normalised-stem duplicate was found in that targeted comparison. This does not establish a complete semantic duplicate audit across every seed file.

### Updated draft counts
- Probability: **415**
- Statistical Inference: **178**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **7**
- Total: **619 supplementary items** on this branch, including the 33 additions made in batch 2.

Page 770 remains held because the upper endpoint in the Uniform model is visually ambiguous. These additions remain draft-only.


## Further verified additions — pages 781–789

Seven additional questions were transcribed from enlarged page images and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 781 | `mcq1000-p781` | Probability T6 — exponential/Gamma lifetime and series reliability | B, (2e^{-2}) |
| 782 | `mcq1000-p782` | Probability T2 — conditional density | B, (1/27) |
| 783 | `mcq1000-p783` | Statistical Inference T10 — likelihood-ratio/variance test direction | A, upper-tail residual sum of squares |
| 786 | `mcq1000-p786` | Statistical Inference T4 — geometric MLE | D, (1/(1+\bar X)) |
| 787 | `mcq1000-p787` | Statistical Inference T5 — method of moments | C, (sum X_i^2/n) |
| 788 | `mcq1000-p788` | Statistical Inference T6 — Fisher information | B, (1/3) |
| 789 | `mcq1000-p789` | Statistical Inference T3 — UMVU estimator | A, (((n+1)/n)X_{(n)}) |

### Source correction
- **Page 783:** the scan marks option B, but the stated alternative is (sigma^2>sigma_0^2). The rejection region must therefore be an upper-tail region with a large residual sum of squares. We corrected the key to A and explicitly recorded the discrepancy rather than repeating the source mark.

### Pages held out in this range
- **Page 784:** the displayed model statement is incomplete/ambiguous, so the likelihood and parameter cannot be transcribed confidently.
- **Page 785:** the displayed target moment appears incompatible with the stated Uniform(-θ,0) model and all listed choices; held pending source clarification.
- **Page 790:** for the printed Beta(1,θ) model, the likelihood ratio depends on (prod(1-X_i)), not simply (prod X_i) as in the listed critical regions. The source's marked option is not justified by the displayed model; excluded.

### Updated branch counts
- Probability: **417**
- Statistical Inference: **183**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **7**
- Total: **626 supplementary items** on this branch (40 additions in this batch branch).

These additions are still draft-only and require latest-head CI and review.


## Further verified additions — pages 791–799

Seven additional questions were visually checked and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 791 | `mcq1000-p791` | Statistical Inference T1 — sufficiency | A, B and C (one-to-one transformations of the full sample) |
| 793 | `mcq1000-p793` | Statistical Inference T3 — UMVU estimation | B, 0.77 |
| 794 | `mcq1000-p794` | Statistical Inference T3 — UMVU for a Poisson functional | B, 0.216 |
| 796 | `mcq1000-p796` | Statistical Inference T4 — MLE for a discrete model | B, 14/25 |
| 797 | `mcq1000-p797` | Statistical Inference T1 — sufficiency with parameter-dependent support | D, sample maximum |
| 798 | `mcq1000-p798` | Statistical Inference T3 — variance of the MVUE | D, (	heta^2/[4n(n+1)]) |
| 799 | `mcq1000-p799` | Statistical Inference T5 — method of moments | B, 29/50 |

### Held out in this range
- **Page 792:** left side of the density is clipped, so its normalising constant and exponent cannot be transcribed with confidence.
- **Page 795:** the symbol in the question (“(X_i)” versus a possible order-statistic (X_{(1)})) is unclear, changing the meaning of the sufficiency question.
- **Page 800:** the convergence-arrow notation in the options is too unclear to distinguish the intended mode of convergence.

### Updated draft counts
- Probability: **417**
- Statistical Inference: **190**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **7**
- Total: **633 supplementary items** on this branch (47 additions in this batch branch).

No additions from this range were accepted solely from the printed answer mark; each answer was independently derived. These items remain draft-only.
