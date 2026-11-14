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


## Batch 5 — pages 13–24

Six additional questions were imported from visually checked pages 13, 16, 17, 19, 21 and 22: three Probability questions (conditional expectation, exponential scale distribution, zero covariance versus independence, and a mixture-exponential hazard function) and two Statistical Inference questions (method-of-moments endpoints for a uniform distribution, and power of a Neyman–Pearson test). The explanations show the intermediate steps and state the assumptions used.

### Pages held out after inspection

- **Page 14:** held out because the support of the joint density is incomplete in the scan and the conditional notation in the options is ambiguous.
- **Page 15:** held out because the two MLE/sufficiency statements are contradictory without a uniqueness condition; the item cannot be keyed unambiguously as printed.
- **Page 18:** held out because the Markov graph labels/transitions are not sufficiently legible and the final two options are duplicated.
- **Page 20:** held out because the degrees-of-freedom symbols in the chi-square statements are unreadable in the scan.
- **Page 23:** held out because more than one listed statement is false as written, despite the single-answer wording.
- **Page 24:** held out because the limit expression and normalising terms are not legible enough to transcribe without guessing.


## Batch 6 — pages 25–36

Two further items were added from visually checked pages 27 and 35: a one-sample large-sample test for a population proportion (Statistical Inference) and the exponential transformation of a Uniform(−1,1) variable (Probability). The z statistic is computed from the null standard error, and the transformed support is explicitly checked.

### Pages held out after inspection

- **Page 25:** held out because the four conditions are not fully legible, particularly the fourth characteristic-function expression.
- **Page 26:** held out because the covariance matrix and the random-vector transformation are too faint to transcribe reliably.
- **Page 28:** held out because the exact statement quantifiers and correlation condition are ambiguous in the scan.
- **Page 29:** held out because the joint PMF's support and several conditional-probability expressions are unreadable.
- **Page 30:** held out because the discrete PMF's parameterised cases and option expressions are not legible enough for a reliable method-of-moments derivation.
- **Page 31:** held out because the density's piecewise formula and interval endpoint are not sufficiently clear.
- **Page 32:** held out because the moment and event notation is ambiguous in the scan.
- **Page 33:** held out because the definitions of the transformed variables are not legible enough to identify the requested distributions.
- **Page 34:** held out because the joint-density support and event inequalities are partly obscured.
- **Page 36:** held out because the density formula and the four estimator expressions cannot be transcribed with confidence.


## Batch 7 — pages 37–48

Four further questions were imported from visually checked pages 38, 46, 47 and 48: four Probability questions (normalisation and marginal PMFs of a discrete joint distribution; the Beta-prime representation of an F statistic; the large-denominator-df limit of F; and the product of independent beta variables) and one Statistical Inference question (unbiasedness, consistency, sufficiency and UMVU). The explanations derive the normalising constant and marginal sums, and identify the relevant distributional identities.

### Duplicate and exclusion handling

- **Pages 37, 40, 41, 42, 43 and 44:** duplicates of earlier source questions already imported or held out: p35, p26, p23, p21, p16 and p17 respectively. No duplicate entries were created.
- **Page 39:** held out because the two iid sequences and the almost-sure limiting expression are too faint to transcribe reliably.
- **Page 45:** held out because the displayed MLE threshold depends on sample size, but the scan does not make that sample size clear enough to reproduce the printed 1/4 threshold.


## Batch 8 — pages 49–60

Four additional questions were imported from visually checked pages 54, 56, 58 and 60: two Probability questions (a randomised linear combination of independent standard normals and mean/median/variance comparisons), one Stochastic Processes question (irreducibility, period, two-step return probability and stationary distribution of a three-state chain), and one Statistical Inference question (consistency of three estimators for Uniform(0,θ)).

### Duplicate and exclusion handling

- **Pages 51, 52 and 53:** duplicates of pages 14, 35 and 25 respectively; no duplicate entries were created.
- **Page 49:** held out because all displayed endpoint-probability equalities follow from continuity, while the single-choice layout does not distinguish one answer.
- **Page 50:** held out because the event-independence options appear to have multiple true statements and the original single-choice layout is not adequate.
- **Page 55:** held out because the joint-Poisson probability expressions are too faint to transcribe accurately.
- **Page 57:** held out because the completeness claim for the two-statistic normal-family statistic needs a more careful derivation than the scan's terse statements permit.
- **Page 59:** held out because the logical wording of the UMVU/unbiasedness statements and one option is not sufficiently legible.
