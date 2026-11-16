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
