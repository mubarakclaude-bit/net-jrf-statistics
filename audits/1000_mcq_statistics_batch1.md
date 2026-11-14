# 1000 MCQ Statistics — source audit, batch 1

**Source:** `1000 MCQ statistics.pdf` (PDF metadata title: *Statistics Test Series*).  
**Actual extent:** 1,044 scanned pages, not 200. OCR of all pages produced approximately 52,846 words. OCR was used for discovery only; imported questions were checked against rendered pages.

## Batch 1 — pages 954–964

Thirty-seven source-derived questions were added as supplementary practice, not attributed official PYQs.

| PDF page | Module/topic | Result |
|---:|---|---|
| 954 | Probability / probability-t4 | Added |
| 955 | Probability / probability-t6 | Added |
| 956 | Probability / probability-t2 | Added |
| 957 | Probability / probability-t4 | Added |
| 958 | Multivariate / multivariate-t1 | Added with corrected key |
| 959 | Inference / inference-t9 | Added with corrected key |
| 960 | Stochastic / stochastic-t1 | Added |
| 961 | Probability / probability-t13 | Added |
| 962 | Multivariate / PCA | Held out: source omits sign restriction on rho |
| 963 | Multivariate / multivariate-t1 | Added |
| 964 | Probability / probability-t9 | Added |

## Source-key and wording findings

- **Page 958:** The scan marks A, C and D. For symmetric idempotent A of rank r and Y~Nₚ(0,Iₚ), the complementary quadratic form has χ²(p−r), their sum has χ²(p), and the two independent forms have degrees of freedom r and p−r. Only A is true as written. The bank records this correction.
- **Page 959:** The scan marks the rejection region 0<x≤α as complete. Under H₁=N(0,1), values outside the null support (0,1) have positive probability while H₀ assigns them zero. An MP test must reject there as well. Within (0,1), the likelihood ratio decreases for x>0, so the remaining size α is assigned to 0<x≤α. The complete region is (−∞,0]∪(0,α]∪[1,∞), up to boundary conventions. Only the existence statement is true as written.
- **Page 962:** The equicorrelation matrix has eigenvalues 1+3ρ and 1−ρ (multiplicity three). The printed answer (1+ρ)/2 assumes ρ≥0. If ρ<0, the two largest eigenvalues are 1−ρ and the proportion is (1−ρ)/2. No sign restriction is supplied, so the item is held out rather than silently repaired.

## Batch 2 — additional answer-marked pages

Thirteen more questions were imported from visually checked pages 967, 971, 973, 975, 984, 988, 991, 998, 999, 1002, 1005, 1008 and 1011. The new additions cover hypergeometric variance, multiple correlation, Neyman–Pearson testing, Markov-chain periods, order statistics, conditional expectation/variance identities, order-statistic covariance, binomial sums, sufficiency/MLE/MOM, MGF probability extraction, Chebyshev's inequality, multivariate-normal linear combinations and compound-Poisson random sums.

### Additional source-key corrections

- **Page 967:** the scan marks the variance option with denominator (m+n+1). The hypergeometric variance has denominator (m+n−1), so option C is correct; the scan's green key is wrong.
- **Page 999:** the scan marks the sufficiency statements and MLE but does not mark the method-of-moments statement. Since E(X)=θ/(θ+1), solving X̄=θ/(θ+1) gives θ̃=X̄/(1−X̄); statement D is also true. The bank records all four as true.

### Additional exclusions and duplicate handling

- **Page 968:** held out because the chi-square quantile subscript convention is not stated, and the interval endpoint order depends on that convention.
- **Page 974:** held out because statement A is ambiguous in the scan's wording, so a defensible four-statement verdict cannot be preserved without guessing.
- **Page 1009:** held out because θ>1 is an open parameter restriction; √X_(n) is not always an attained MLE when X_(n)≤1.
- **Pages 977 and 996:** duplicates of the Uniform(−1,2) law-of-large-numbers question already imported from page 964; not imported again.

## Batch 3 — convergence and order-statistic pages

Fourteen additional questions were imported from pages 109, 111, 114, 118 and 123–131. They cover convergence in distribution, the continuous mapping theorem, dependence and convergence in probability, extreme-value centring for exponential maxima, moments of uniform and exponential order statistics, exponential spacings, Beta order-statistic distributions, and joint/conditional densities for the third and fourth order statistics from f(x)=2x.

No new answer-key correction was required in this batch. Page 111's accepted answer is mathematically correct: positivity alone is insufficient for the continuous mapping theorem; continuity of g at the limiting value is required.

## Verification and boundaries

- `verify_1000_mcq_batch1.py` checks key numerical identities, pool structure, unique IDs, answer formats and explanations.
- Imported count: Probability 28, Multivariate 4, Inference 3, Stochastic 2 (37 total).
- No examination/year/session attribution is inferred.
- The full page-by-page topic classification, duplicate reconciliation against all bank content, and remaining-page question import are still pending. This is only the first batch.


## Batch 4 — opening pages 1–12

Rendered and checked the opening pages against the scan. Added eight more items from pages 1, 2, 4, 5, 7, 8, 9 and 12: seven Probability questions and one Statistical Inference question. They cover competing exponential variables, convolution of exponential variables, a Binomial(3, 1/2) PMF/MGF, a negative-binomial event, a linear combination of standard normals, a chi-square survival quantile, and unbiased estimation of a reciprocal Poisson parameter. The original options and algebra were checked against the page images.

### Opening-page exclusions

- **Page 3:** held out because the exponential parameterisation and sample context are not stated consistently enough to decide which MLE statements are intended.
- **Page 6:** held out pending a careful interpretation of the repair interval and event-gap condition.
- **Page 10:** held out because both options A and C fail the density conditions (A integrates to 1/2; C takes negative values on part of its support), although the source is framed as a single-answer item.
- **Page 11:** held out because the stated chi-square CDF value at 34.382 for 25 degrees of freedom is approximately 0.9000, which does not match any printed option.

The page 4 item was standardised to the app's multi-select format because the source lists three true statements but does not provide a combination-choice list. Page 5's exact probability is 126/2^10=63/2^9 (option C).
