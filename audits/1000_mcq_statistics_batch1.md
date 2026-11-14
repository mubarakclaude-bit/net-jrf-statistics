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


## Batch 9 — pages 61–72

Ten additional questions were added from visually inspected pages 61–70:
- **Statistical Inference (1):** MLE and Fisher information for the power density f(x;θ)=θx^(θ−1), p61.
- **Probability (8):** Cramér's theorem for independent summands, p62; normal-sample variance moments, p63; Poisson moment identity/Cantelli bound, p64; WLLN threshold for independent two-point variables, p65; comparison probabilities for discrete uniforms, p66; maximum of four exponential variables, p67; zero correlation and Cauchy–Schwarz, p68; binomial variance maximum, p70.
- **Multivariate/Regression (1):** inequality between regression-line coefficients, p69.

### Pages held out after inspection

- **Page 71:** held out because two printed inverse-matrix options appear visually identical or differ only in a faint exponent in the determinant. The mathematically correct inverse is clear, but the original option lettering cannot be trusted from this scan.
- **Page 72:** held out because the independence assumptions needed for the gamma–beta and exponential-ratio statements are not explicit in the scan. Since the question asks for incorrect statements, those missing assumptions affect the answer key.

Page 62 is keyed conservatively: only the Cramér theorem statement is accepted as written; no joint-normality or independence assumptions are silently added to the other two statements. Page 63 explicitly states the usual unbiased sample-variance convention used for the chi-square result. Page 67 uses the exponential rate parameterisation indicated by the matching printed expression.


## Batch 10 — pages 73–84

Ten more questions were added from visually inspected pages 74–77 and 79–84:
- **Statistical Inference (3):** factorisation/sufficiency for a beta-family sample, p74; Cramér–Rao bound for the zero-truncated Poisson parameter, p77; 99% confidence interval for a population proportion, p79.
- **Probability (5):** joint probability under a factorised exponential density, p75; a logarithmic transformation of a Uniform(0,1) variable, p76; CLT approximation for a sample mean, p81; existence of moments for a Pareto-type density, p83; probability mass at the minimum support point from a negative-binomial MGF, p84.
- **Multivariate Analysis (1):** correlation of linear combinations of independent variables, p80.
- **Stochastic Processes (1):** thinning of a Poisson arrival process and the Erlang waiting-time tail, p82.

### Pages held out after inspection

- **Page 73:** held out because two of the three displayed limits have finite limits (A and C), while the source asks for a single limit without a multiple-answer format.
- **Page 78:** held out because the displayed density and conditional moments imply Var(Y)=15−16/π, which does not match the printed options as legible in the scan.

The page 77 bound is derived from the displayed zero-truncated Poisson PMF. The page 79 interval uses the normal/Wald approximation and z=2.576 for 99% confidence. The page 82 answer uses independent thinning of the stated Poisson car-arrival process.


## Batch 11 — pages 85–96

Six additional questions were imported from visually inspected pages 89, 90, 91, 92, 93 and 95:
- **Statistical Inference (3):** UMVU estimation of a power of the Laplace scale parameter, p89; confidence interval for the endpoint of a Uniform(0,θ) distribution using the sample range, p90; Neyman–Pearson critical region and type II error for a discrete model, p92.
- **Probability (2):** exactly two exceedances for three iid variables with density 3x², p91; product of an independent arcsine variable and Rayleigh variable, p93.
- **Multivariate Analysis (1):** correlation of a standard bivariate normal pair expressed through P(XY>0), p95.

### Pages held out after inspection

- **Page 85:** held out because the displayed function 1/x on (θ−1,θ+1) does not integrate to one as printed, so it is not a valid density without an omitted normalising factor.
- **Page 86:** held out because the printed target state in P(X₃=…|X₀=1) is not consistent with the stated state space {0,1,2}, and the listed numerical options do not match the transition-matrix calculation under the legible diagram.
- **Page 87:** held out because the displayed rejection region uses |X−2Y|≤z_(α/2)√5, whose null probability is 1−α under the usual upper-tail critical-value convention, not any listed answer. The inequality may have been intended as ≥.
- **Page 88:** held out because direct integration of the displayed density gives P(min(X,Y)≤1/2)≈0.5898, which does not match any printed option.
- **Page 94:** held out because the relationship between the displayed chi-square CDF expression and the variable p in the answer choices is not fully stated in the scan.
- **Page 96:** duplicate of page 95; not imported twice.

The page 89 estimator uses completeness and sufficiency of Σ|Xᵢ|. Page 90's interval follows directly from the stated pivotal CDF for the sample range. Page 93's product density is evaluated by a change of variables and equals the N(0,σ²) density.


## Batch 12 — pages 97–108

Nine additional questions were imported from visually checked pages 98–101, 103–107:
- **Probability (6):** expectation of a linear combination without assuming independence, p98; discrete square-root transformation of a PMF, p99; density transformation, p100; conditional covariance from a joint PMF table, p107; conditional expectation of one binomial count given the total, p103; two-standard-deviation location in a sample-mean distribution, p106.
- **Multivariate Analysis (1):** regression coefficient of one independent Poisson variable on their sum, p101.
- **Statistical Inference (2):** UMVU estimator of the upper endpoint N of a discrete uniform distribution, p104; limiting distribution of the maximum-likelihood estimator for Uniform(0,θ), p105.

### Pages held out after inspection

- **Page 97:** held out because the stated 90% confidence interval (X̄−1, X̄+1) with σ=4 implies a minimum sample size of 44 using z₀.₉₅≈1.645, but 44 is absent from the printed choices.
- **Page 102:** held out because the normal means are not specified. The ratio (X+Y)/|X−Y| has a t₁/Cauchy law only under a zero-mean condition; that assumption is absent from the scan.
- **Page 108:** is a cover page, not a question; no entry added.

For page 98, only the mean statement is keyed as universally valid because independence is not stated; the variance formula in the source would require additional assumptions. Page 104's estimator is verified by a telescoping expectation sum and completeness of the sample maximum.


## Batch 13 — pages 110–120

Eight additional questions were imported from pages 110, 112, 113, 116, 117 and selected items on page 119:
- **Probability (8):** a sequence of CDFs that fails to converge in distribution, p110; extreme-value limit for n times the sample minimum when the density is positive at zero, p112; Slutsky/continuous-mapping statements, p113; convergence of a centered Binomial(n,1/2) proportion, p116; equivalence and implication facts among convergence modes, p117; possible values of a probability, p119 Q2; Bertrand's paradox, p119 Q3; complement probability consistency, p119 Q5.

### Exclusions and duplicates

- **Pages 109, 111, 114 and 118:** these questions were already imported in the earlier order-statistics/convergence batch; no duplicates added.
- **Page 115:** repeats the definition of almost-sure convergence already covered by page 117; not imported separately.
- **Page 119 Q4:** the supplied values P(A∪B)=0.1 and P(A∩B)=0.5 are impossible because an intersection is a subset of the union; the scan's accepted answer does not repair the inconsistency.
- **Page 119 Q6:** insufficient information is provided to identify P(A∩B) without P(B∩C) or equivalent additional information.
- **Page 120:** duplicates questions 2 and 3 from page 119; not imported twice.

For p112, the limit uses the local approximation F(x)~x/4 implied by the stated density limit. For p116, both convergence-in-probability and convergence-in-distribution statements are included because both follow from the variance tending to zero.


## Batch 14 — pages 121–132

One additional question was imported from page 132: applying the weak law of large numbers to the sample average of squared iid observations, with limit E(X²)=μ²+σ².

### Duplicate handling

- **Pages 121–122:** repeat the probability consistency and set-probability questions from page 119 (including the inconsistent/underdetermined items already held out); no new entries were created.
- **Pages 123–131:** already reviewed and imported in the earlier order-statistics batch; no duplicates were created.


## Batch 15 — pages 133–144

Nine additional questions were imported from pages 133, 135, 136, 138–142 and 144, all in Probability:
- Binomial-to-Poisson limit with npₙ→1/4, p133.
- Chebyshev lower bound for the mean of 100 Uniform(0,20) observations, p135.
- Variance and weak law for independent three-point variables with growing support, p136.
- Asymptotic expected proportion of birds not seen by adjacent birds, p138.
- CLT approximation for total ticket demand, p139.
- Weak-law evaluation of a multiple integral as a ratio of first and second moments, p140.
- Two sufficient conditions for the strong law, p141.
- CLT probability for total passenger weight, p142.
- Sample-mean probability for normally distributed golf-match durations, p144.

### Pages held out after inspection

- **Page 134:** the strong-law question states only the marginal two-point probabilities and does not state independence; the accepted answer λ<1/2 relies on an independence assumption not present in the wording.
- **Page 137:** the accepted key says WLLN holds if λ>0, but the covariance specification for a jointly normal sequence gives Var(X̄ₙ)=[n+2(n−1)λ]/n², which tends to zero for every admissible fixed λ. The source key is therefore not accepted as stated.
- **Page 143:** two printed options, Φ(−1.79) and 1−Φ(1.79), are mathematically identical. The single-choice item has duplicate correct options and is held out rather than arbitrarily selecting one.

For page 138, the source's c=1/4 is retained under independent left/right choices; this independence interpretation is made explicit. For page 139, independence of ticket demands is made explicit for the CLT calculation. Page 144's exact calculation is approximately 0.9954; the source's accepted 0.99 is retained only as the closest listed choice and flagged for coarse rounding.


## Batch 16 — pages 145–156

Eleven additional questions were imported from pages 145–149 and 151–156:
- **Probability (9):** exact tea-cup demand probability for 64 guests, p145; minimum n for a Gamma sum interval, p146; stability of the sample mean of iid Cauchy variables, p147; CLT for the average of squared standard normals, p149; reciprocal of a standard Cauchy variable, p151; minimum of iid Poisson variables, p153; expected maximum of two standard normals, p154; a Poisson CDF at its mean, p155; beta ratio from independent exponential sums, p156.
- **Multivariate Analysis (2):** a false statement involving ratios of iid standard normals, p148; covariance matrix of cumulative sums of three independent standard normals, p152.

### Pages held out after inspection

- **Page 150:** held out because the scan omits or obscures the covariance matrix of the stated multivariate normal vector. Independence of the listed linear combinations cannot be determined from the mean vector alone.

### Corrections to source answer key

- **Page 146:** the source accepted answer is 385, obtained from a normal approximation. The exact Gamma(n,1) calculation gives P(0.9≤Y/n≤1.1)≈0.94982 for n=383 and 0.95012 for n=384. Therefore the exact smallest n is **384**. The answer option was corrected and the source's approximation noted.
- **Page 145:** the total number of cups has Binomial(128,1/2) distribution. Exact probabilities P(S≤72)≈0.9337 and P(S≤73)≈0.9537 confirm the source's accepted answer 73.
