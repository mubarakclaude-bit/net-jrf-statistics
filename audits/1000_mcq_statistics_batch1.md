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


## Batch 17 — pages 157–168

Twelve further questions were imported from pages 157–168:
- Joint-density normalisation and conditional density, pp157–158.
- Covariance and reciprocal covariance from a triangular joint density, pp159–160.
- Ordering probability for two Gamma(2,3) variables and one independent Exponential(scale 3) variable, p161.
- Uniform-in-p Chebyshev sample-size guarantee for Bernoulli observations, p162.
- Expected median of an odd-sized standard normal sample, p163.
- Odd-probability for a Poisson mixture from its MGF, p164.
- Double integral over a triangular strip, p165.
- Reciprocal moment of a chi-square variable, p166.
- Negative-binomial cumulative limit using CLT, p167.
- Mean from a product of binomial MGFs, p168.

All 12 entries are in Probability and include worked derivations and PDF page provenance. Page 159, 162 and 164 are numeric-answer items with explicit verification checks.


## Batch 18 — pages 169–180

Eight questions were imported from pages 169, 170, 174, 175, 176, 178, 179 and 180, all in Probability:
- Symmetry argument for an expected ratio of iid Uniform variables, p169.
- Maximum of three iid Uniform variables, p170.
- Perfect-square divisors of an integer, p174.
- Conditional binomial thinning of a Poisson variable and conditional expectation, p175.
- Sum of two Uniform variables and a triangular density, p176.
- Gamma variance from a given mean, p178.
- Maximising a binomial point probability as a function of p, p179.
- Conditional probability given a union of independent events, p180.

### Pages held out after inspection

- **Page 171:** held out because the numerator and denominator sums overlap, so the displayed ratio is not a standard F ratio of independent chi-square variables as claimed.
- **Pages 172–173:** held out because the weighted-average formula is too faint/ambiguous and the visible variance options do not reconcile with the most direct reading of the weights and stated variance.
- **Page 177:** held out because the numerator is included in the denominator, so the displayed ratio cannot have the stated standard F distribution under the usual independent-gamma construction.


## Batch 19 — pages 181–192

Ten further questions were imported from pages 181–183, 185–186 and 188–192, all in Probability:
- Absolute ratio of two independent standard normals, p181.
- Exponential survival probability at mean plus variance, p182.
- Bayes' theorem with conditional probabilities, p183.
- Variance of a lognormal transformation 10^X, p185.
- Identifying an exponential distribution from its MGF, p186.
- Reciprocal-shift expectation for a Poisson variable, p188.
- Second moment of a t distribution with four degrees of freedom, p189.
- Mean and variance from a discrete MGF, p190.
- First decisive outcome in repeated fair-die rolls, p191.
- Expectation identity involving chi-square and standard normal marginals, p192.

### Pages held out after inspection

- **Page 184:** held out because the order-statistic notation and parameter labels (a, d, n) are too ambiguous in the scan to determine which random variable Y is intended.
- **Page 187:** held out because the definition of Y is missing from the displayed question; the success-probability options cannot be evaluated without it.

Page 192 is keyed conservatively: the source does not explicitly state independence, so only E(X+Y²)=n+1 is guaranteed by the given marginal distributions. Page 185 is a numeric-answer item with a direct lognormal-MGF check; page 189's t moment is checked using ν/(ν−2).


## Batch 20 — pages 193–204

Seven further questions were imported from pages 193, 194, 198, 199–200, 201, 202 and 204, all in Probability:
- Independent-event conditional probability from sum/product constraints, p193.
- Normalising constant for the standard Cauchy density, p194.
- A max transformation of a Uniform(0,1) variable, p198.
- Determinant-zero probability for a random symmetric 3×3 matrix, pp199–200.
- Chebyshev upper bound for an exponential variable, p201.
- Hypergeometric probability of a box containing no defectives, p202.
- Conditional selection of the youngest student within a known section, p204.

### Pages held out after inspection

- **Page 195:** the displayed density is Cauchy, whose variance does not exist; none of the four finite numerical options is correct.
- **Page 196:** the displayed power function appears to have support extending to infinity, under which it is not a normalisable density for the indicated positive shape parameter. The intended upper endpoint is not clear enough to repair safely.
- **Page 197:** the function 2x/a² on 0<x<a integrates to one for every a>0, so the instruction to determine a has no unique answer; the printed choices do not resolve this.

Page 202 uses the exact hypergeometric model: C(9750,100)/C(10000,100)≈0.0785077. The simpler binomial approximation is ≈0.07952 and is noted in the explanation.


## Batch 21 — pages 205–216

Eleven additional questions were imported from pages 205–216, all in Probability:
- Two-colour draw without replacement from a bag with ratio information, p205.
- Complement counting for three balls not all of one colour, p206.
- Cube-face corner incidence, p208.
- At least one success among three independent race outcomes, p209.
- Mixture of two toffee boxes with a parameter solved from a different-colour draw probability, p210.
- Arrangements with a fixed cover, ordered theory pages and a contiguous drawing block, p211.
- Repeated-letter arrangements with restrictions on vowel positions, p212.
- At least one named player selected across two independent teams, p213.
- Parity of the product of three fair dice, p214.
- Total probability for choosing one of two bags, p215.
- Three different colours in three draws with replacement, p216.

### Source-key correction

- **Page 208:** the source marks 1/5, but there are 8 corners and C(6,3)=20 equally likely triples of face positions. The correct probability is 8/20=2/5. The option was corrected and the discrepancy recorded.
- **Page 216:** the derived probability is 8/81, which is not among the four numerical options; the source's 'None of these' option is therefore correct.

### Page held out

- **Page 207:** held out because 'right place' is not defined precisely (correct square versus correct row), and none of the printed formula options unambiguously matches either natural interpretation.


## Batch 22 — pages 217–228

Twelve further questions were imported from pages 217–228, all in Probability:
- Honour-card draws from a standard deck, p217.
- Ball-count algebra from a stated colour probability, p218.
- Sum-at-most-four probability for two dice, p219.
- Alternating red/yellow die game with the first red roll losing, p220.
- Ordered sequence probability for a square-biased eight-faced die, p221.
- Contiguous block arrangement of girls in a row, p222.
- Hypergeometric selection of two girls and one boy, p223.
- Count of non-venomous snakes from a single-draw probability, p224.
- Probability neither interview candidate is selected, p225.
- Selection from two classes, p226.
- Three red cards from a standard deck, p227.
- Contiguous-block arrangement with five boys and an unknown number of girls, p228.

### Source-key and wording notes

- **Page 217:** the correct probability is 11/221, but none of the printed numerical options matches. Option C was corrected to 11/221.
- **Page 224:** the wording is unclear around the number of snakes caught; the revised stem makes the single-snake interpretation explicit, which gives 135 non-venomous snakes.
- **Page 225:** the source does not state independence; the revised stem states the independence assumption required for the accepted 60% answer.
- Single-choice items were standardised to four options to match the repository's Paper 2 question schema. For page 216, the correct 8/81 was moved into option D and the source's 'None of these' was removed.


## Batch 23 — pages 229–240

Seventeen further questions were imported from pages 229–230 and 232–240:
- **Probability (14):** two even-numbered balls from 1–21, p229 Q1; colour probability, p229 Q2; independent draw pattern with replacement, p229 Q3; at least three heads from four coins, p229 Q4; committee with at least two women, p229 Q5; no-green draw, p229 Q6; three different ball types, p230 Q7; neighbours around a round table, p230 Q9; ordered white-then-black draw, p230 Q10; expected payout in a conditional second-roll game, p232; expected range of five Uniform(0,1) observations, p233; reciprocal F-quantile relation, p236; difference of independent normal products, p237; expectation of a product involving independent uniforms, p239.
- **Multivariate Analysis (1):** maximum attainable rank of a sum of outer products, p235.
- **Statistical Inference (2):** Bernoulli MLE, p238; consistent estimator for θ in N(2θ,θ²), p240.

### Pages held out after inspection

- **Page 230 Q8:** the wording does not specify equal colour probabilities or the sampling model sufficiently to calculate the probability of at least one marble of each colour.
- **Page 232:** the die game is interpreted as a payout equal to the number on the last roll; under that wording the expectation is $4.25.
- **Page 234:** the sample median for the displayed double-exponential sample is 2, but 2 is absent from the printed answer options; held out due to the source-option mismatch.

The p229 questions are individually identified by question number because six distinct items share one source page. The p235 matrix-rank item is stored in Multivariate Analysis; the two estimator items are stored in Statistical Inference.


## Batch 24 — pages 241–252

Nine further questions were imported from pages 241, 243, 245, 246 and 248–252:
- **Probability (6):** parity of a difference of independent binomials, p241; ordering probability for three iid exponentials, p245; shifted-exponential quantile, p246; integer-valued polynomial for a uniformly selected integer, p248; odd-integrand expectation under a symmetric normal distribution, p250; Gamma mode, p251; non-existence of a positive-argument MGF for the Beta-prime distribution, p252.
- **Statistical Inference (2):** coverage probability of a Student-t confidence interval, p243; Neyman–Pearson critical region for Laplace scale testing, p249.

### Pages held out after inspection

- **Page 242:** the displayed function θ/x^(θ+1) on x>0 is not a normalisable density; the usual Pareto support x>1 is not shown, so no distribution is inferred.
- **Page 244:** X is explicitly labelled DiscreteUniform(0,n), so its fractional part is identically zero; none of the continuous Uniform options is correct.
- **Page 247:** duplicate of the Poisson expectation E[1/(X+1)] already imported from page 188.

### Source-option correction

- **Page 248:** for integer n, 16n²+7n+6 is always an integer. The printed options are all fractions below one; the correct option is corrected to 1.


## Batch 25 — pages 253–264

Nine further questions were imported from pages 254–260, 262 and 264:
- **Probability (8):** completeness and sufficiency of the maximum absolute observation for Uniform(−θ,θ), p254; symmetry and indicator moments for a normal variable, p255; expected areas of a square and rectangle with uniform sides, p256; density from a specified hazard function, p258; support of a binomial variable identified from its MGF, p259; conditional expectation for two exchangeable geometric variables given their sum, p260; variance from a Poisson MGF, p262; expected transformed sample minimum using the probability integral transform, p264.
- **Multivariate Analysis (1):** identifying a valid correlation matrix, p257.

### Pages held out after inspection

- **Page 253:** the scan obscures the estimator expressions and confidence-interval quantiles; the true/false selections cannot be verified reliably.
- **Page 242:** the displayed Pareto-like function is not normalisable on the stated support x>0; the usual x>1 support is not printed clearly.
- **Page 244:** the variable is labelled discrete uniform, so its fractional part is zero; the listed continuous-uniform options do not match.
- **Page 247:** duplicate of the Poisson reciprocal expectation already imported from p188.
- **Page 261:** the notation defining S and T and the condition on their expectations/variances are too corrupted to derive the requested correlation.
- **Page 263:** the geometric support convention is not stated; the two common conventions give different means (1/p versus (1−p)/p).


## Batch 26 — pages 265–276

Nine further questions were imported from pages 265–268, 270–273 and 276:
- **Probability (8):** variance of a linear combination of iid standard normals, p265; Uniform-to-chi-square logarithmic transformation, p266; conditional distribution of two iid geometric variables given their sum, p267; mode of χ²₃, p268; expectation of the standard normal CDF at a symmetric normal variable, p270; χ²₂ survival quantile, p271; coverage of the sample range around a population median, p272; normalisation of a five-point symmetric PMF, p276.
- **Statistical Inference (1):** MLE of the scale parameter for a Laplace sample, p273.

### Pages held out after inspection

- **Page 253:** the estimator expressions and confidence-interval quantiles are obscured.
- **Page 269:** the Beta-prime transformation notation in the requested CDF is ambiguous in the scan; no transformation is guessed.
- **Page 274:** the MGF and event threshold are not sufficiently legible to reconcile with the listed probability options.
- **Page 275:** the piecewise density and support endpoints are too faint to verify normalisation or the requested interval probability.


## Batch 27 — pages 279–288

Eight additional questions were imported from pages 279–282 and 285–288, all in Probability:
- Ratio of independent sums of squared normal differences and sums, p279 (F distribution).
- Sum of three iid geometric variables with a negative-binomial probability, p280.
- Beta(m,2) parameter recovery from a median condition and its variance, p281.
- Conditional inclusion-exclusion for three events, p282.
- Mixture of a geometric number of fair-coin tosses and a conditional binomial variable, p285.
- Expected waiting time for an odd sum of two independent Poisson(1) variables, p286.
- Central limit theorem for iid variables with variance 2, p287.
- Iterated expectation for a conditional second moment, p288.

### Pages held out after inspection

- **Page 277:** the interval endpoints in the uniform-distribution question are unreadable.
- **Page 278:** the density and four weighted estimator formulas are too faint to identify reliably.
- **Page 283:** the density and transformation power in W are not sufficiently legible to identify the target distribution.
- **Page 284:** section cover, no question.


## Batch 28 — pages 289–300

Eight questions were imported from pages 289–292, 294, 297, 298 and 300:
- **Probability (7):** CLT at the mean for iid exponential observations, p289; CLT and variance of the sample second moment for normal data, p290; limiting distribution of χ²ₙ/n, p291; a sequence converging in probability but with constant expectation, p292; correlation from a triangular bivariate density, p294; conditional density for joint density e^(−y) on 0<x<y, p297; conditional Gamma mean in a joint exponential-Gamma model, p298.
- **Statistical Inference (1):** least-squares coefficient, variance and covariance formulas in simple linear regression, p300.

### Pages held out after inspection

- **Page 293:** the statement about almost-sure convergence depends on whether the sequence is independent; the scan does not state that assumption clearly, and the expectation expression is faint.
- **Page 295:** the joint density and requested conditional expectation are not sufficiently legible to transcribe safely.
- **Page 296:** the joint density and conditional-expectation options are blurred; the true/false selection cannot be verified.
- **Page 299:** the normalising constant in the triangular joint density is unclear, so the derived sum density cannot be keyed without correcting an assumption.


## Batch 29 — pages 301–312

Nine questions were imported from pages 301–303, 306–308 and 310–312:
- **Probability (1):** joint-density normalisation and conditional probability checks, p303.
- **Statistical Inference (8):** least-squares slope with known intercept, p301; weighted least-squares slope with known heteroscedastic variances, p302; normal-mean MLE, p306; binomial-probability MLE, p307; numerical binomial MLE, p308; level of a Uniform(0,θ) test with a critical region outside the null support, p310; Neyman–Pearson critical value for a power-family density, p311; most powerful one-sided normal-mean test, p312.

### Pages held out after inspection

- **Page 304:** algebra gives α=3, β=−4, but then f(x)=3−4x becomes negative on part of (0,1), so it is not a valid density.
- **Page 305:** the normal-family mean/variance known-versus-unknown assumption is not legible enough to select the correct MLE for σ².
- **Page 309:** the population distribution label T(λ,·) and the estimator options are too corrupted to identify the method-of-moments target safely.


## Batch 30 — pages 313–324

Eight questions were imported after visual review:
- **Probability (3):** symmetry of an MGF for a symmetric density, p315; CLT limit for sums of iid chi-square(5) variables, p317; floor transformation of a Uniform(0,100) variable, p318.
- **Statistical Inference (5):** power of the most powerful one-sided normal-mean test, p313; completeness and sufficiency in a one-parameter exponential family, p319; UMP upper-tail test for a logistic location family, p320; consistency of a Pareto shape estimator, p323; exact confidence intervals for a triangular-scale density, p324.

### Pages held out after inspection

- **Page 314:** for X~Uniform(π/6,π/4), cos X>sin X almost surely, so the probability is 1; none of the printed options matches.
- **Page 316:** section cover, no question.
- **Page 321:** with the stated finite-population variance denominator N=100 and sample variance denominator n=10, the unbiased multiplier is 11/10, which is absent from the printed options; the highlighted source key 100/99 is not correct for the stated target.
- **Page 322:** held out because the phrasing does not clearly distinguish the negative-binomial family from its geometric special case under convolution.


## Batch 31 — pages 325–336

Ten questions were imported after visual review:
- **Statistical Inference (3):** formulating a one-sided hypothesis for a population mean, p325; definitions of critical region and significance level plus the p-value, p326; interpretation of a p-value, p327.
- **Probability (7):** probability for a weighted die, p328; interval probability from a piecewise density, p329; covariance of two coin-toss indicators, p330; Poisson approximation for misprints per page, p331; exact binomial probability, p332; sample-mean tail probability for a normal population, p335; CLT approximation for a non-normal population with finite variance, p336.

### Pages held out after inspection

- **Page 333:** the chi-square sampling distribution of S² requires a normal population, but normality is not stated in the source stem; the assumption is not silently added.
- **Page 334:** the variance of the sum of 100 expense amounts cannot be determined without an independence/dependence assumption; no assumption is supplied, so the item is held out.

### Source and wording notes

- **Page 330:** the marked answer 1/16 is confirmed: E(X)=E(Y)=1/4, E(XY)=1/8, and Cov(X,Y)=1/16.
- **Page 336:** the stem makes the usual iid and finite-variance CLT conditions explicit so the answer is mathematically valid.


## Batch 32 — pages 337–348

Ten questions were imported after visual review:
- **Statistical Inference (1):** identifying a false statement about sampling distributions and inferential statistics, p337.
- **Probability (9):** standard errors of sample means for four population standard deviations, p338–341; normal-approximation tail probabilities for sample means, p342–343; Bayes' theorem for three urns, p346; union probability for independent events, p347; and the position of the last defective item in sampling without replacement, p348.

### Pages held out after inspection

- **Page 344:** the variance of a sum of 100 expense amounts cannot be determined without an independence/dependence assumption; none is stated.
- **Page 345:** the printed piecewise function integrates to 11/12, not 1, so it is not a valid density as written.

### Source notes

- **Page 342:** the normal-table approximation rounds z≈1.035 to 1.03, giving the source option 0.1515; direct evaluation is approximately 0.1504.
- **Pages 338–341:** these are separate numeric variants of the same standard-error calculation, retained because the population standard deviations differ.


## Batch 33 — pages 349–360

Twelve questions were imported after visual review, all in Probability:
- Joint-density expectation, p349; scaling a normal numerator to obtain a t distribution, p350; variance under Celsius-to-Fahrenheit conversion, p351; absolute-value transformation of an exponential variable, p352; expectation of the positive part of a standard normal, p353; a normal absolute-moment limit, p354; normal-density value at its inflection points, p355; conditional density from a triangular joint support, p356; conditional Poisson distribution given the sum, p357; variance of a sum with common pairwise correlation, p358; an F-distribution ratio, p359; and the mean of a chi random variable, p360.

### Source corrections and exclusions

- **Page 357:** the correct conditional law is Binomial(y, λ₁/(λ₁+λ₂)); none of the printed options gives that law, so the item is keyed as “None of the above”.
- The remaining items in this batch were checked by direct integration, transformation, standard distribution identities or moment formulas; no source-key correction was needed.


## Batch 34 — pages 361–372

Ten questions were imported after visual review:
- **Probability (5):** chi-square distribution of a quadratic form in independent standard normals, p361; Bayes' theorem for a male/female completion problem, p365; a Uniform-plus-Bernoulli mixture distribution, p366; the conditional distribution of independent Bernoulli variables given their sum, p364; and the conditional distribution of independent Poisson variables given their sum, p371.
- **Statistical Inference (5):** exact binomial upper-tail test for a coin, p363; Cramér–Rao lower bound for a power-family density, p368; definition of consistency, p369; Gamma shape estimation by method of moments, p370; and power of a test under a shifted Uniform alternative, p372.

### Pages held out after inspection

- **Page 362:** section cover, no question.
- **Page 367:** the requested strict event is 50<Sₙ<80. Since Sₙ is integer-valued, the continuity-corrected normal interval is 50.5 to 79.5, giving approximately 0.9279; the printed choices do not contain this value. The source choices appear to use a different endpoint convention, so it is held out rather than keyed to a mismatched option.

### Source notes and checks

- **Page 363:** the exact Binomial(100, 0.5) upper tail gives P(N≥59)≈0.0443 and P(N≥58)≈0.0666, confirming N>58 as the non-randomised 5% critical region.
- **Page 364:** only the conditional statement given X+Y=2 is universally true; the Bernoulli sum is not generally Binomial(2,pₓ+pᵧ), and the conditional probability given a sum of one depends on both parameters.
- **Page 368:** the per-observation Fisher information is 1/θ², giving the bound θ²/n.
- **Page 370:** the Gamma method-of-moments formula uses the second raw moment m′₂, not the variance alone.


## Batch 35 — pages 373–384

Twelve questions were imported after visual review:
- **Probability (4):** identify a Poisson distribution from its MGF and calculate P(X≤1), p373; exponential survival probability from a CDF, p375; recover a scale parameter from a tail probability, p379; and a conditional probability from a density proportional to x², p382.
- **Statistical Inference (7):** size and power of a discrete test, p374; exponential method-of-moments estimation, p377; a weighted unbiased and consistent estimator, p378; UMVUE for θ(1−θ) in the Bernoulli family, p380; MLE for Uniform(0,θ), p381; relative efficiency of two normal-mean estimators, p383; and the integer-parameter MLE for Uniform(0,θ), p384.
- **Multivariate Analysis (1):** a linear combination of a bivariate normal vector, p376.

### Pages held out after inspection

- **Page 362:** section cover.
- **Page 367:** the Poisson probability in the printed question does not match any option closely enough; it remains excluded.


## Batch 36 — pages 385–396

Eleven questions were imported after checking the rendered scans:
- **Probability (6):** variance of a lognormal transformation, p385; classification of a mixed distribution from its CDF, p386; conditional probability from three event probabilities, p389; density after the transformation Y=exp(−X²), p390; an F(1,1) ratio formed from independent normal linear combinations, p391; and identification of the weak law from convergence in probability, p394.
- **Statistical Inference (5):** most powerful test for two normal variance values, p387; sufficiency for a normal model with mean and variance both θ, p388; Cramér–Rao bound for exp(−λ) under three Poisson observations, p392; confidence interval for a normal population variance, p395; and a most powerful Gamma shape test, p396.

### Source pages held out

- **Page 393:** the stated CDF F(x)=1−exp(−x/2), x≥0, gives MGF M(t)=1/(1−2t), t<1/2. None of the four printed options matches this expression, so the question is not imported.
- **Page 395 convention:** the confidence-interval item explicitly states the upper-tail chi-square critical-value convention to remove ambiguity in the source's χ² subscript notation.


## Batch 37 — pages 397–408

Ten questions were imported after inspecting the scanned pages:
- **Probability (4):** conditional probability for a Bernoulli transformation, p398; rectangle probability from four bivariate CDF values, p400; point mass recovered from a CDF jump, p407; and a support-bound event for a joint PMF, p408.
- **Multivariate Analysis (1):** identical marginals but dependent variables from a bivariate density, p399.
- **Statistical Inference (5):** Type-I and Type-II errors for an exponential test, p401; UMVUE of θ² for a Poisson sample, p402; expectation and bias of a Gamma rate estimator, p403; two unbiased estimators of μ², p404; and a sufficient statistic from a one-parameter density, p406.
- **Regression (1):** least-squares regression line from summary statistics, p405.

### Pages held out after inspection

- **Page 397:** the displayed sequence/normalisation expression in the weak-law condition is too blurred to transcribe without guessing.
- **Page 403:** the source omits the condition np>1 needed for E(p/X̄) to be finite. The imported version states this condition explicitly and records the omission.



## Batch 39 — pages 409–420

Nine questions were imported after visual review:
- **Probability (4):** Gamma distribution of a sum of transformed uniforms, p411; characteristic function of a symmetric two-point variable, p414; almost-sure convergence for independent non-identically distributed variables, p415; and recovering a Poisson component from an independent Poisson sum, p416.
- **Statistical Inference (5):** Type-I error and power from two densities, p409; MLE for a power density on (0,1), p412; coverage probability of an upper confidence limit, p413; constrained Bernoulli MLE, p417; and the joint sufficient statistic for a normal model with unknown mean and variance, p419.

### Pages held out or matched to existing material

- **Page 410:** duplicate of the exact Binomial(100, 1/2) one-sided 5% critical-value question already imported from page 363; not added twice.
- **Page 418:** the minimum and maximum are sufficient, and the option containing minimum, mean and maximum is also sufficient. Since the source asks for a sufficient statistic rather than a minimal sufficient statistic, the single-choice item has more than one valid option and is held out.
- **Page 420:** both the Borel–Cantelli conclusion in option A and the zero expectation limit in option C hold under the stated probabilities; the single-choice item is ambiguous and is held out.


## Batch 40 — pages 421–432

Eight questions were imported after checking the scans:
- **Probability (2):** central limit theorem for a weighted sum of iid Bernoulli variables, p421; and ordering binomial variances for three success probabilities, p429.
- **Statistical Inference (8):** efficiency comparison of two correlated unbiased estimators, p422; MLE for the rate of a Gamma(shape 2) density, p423; MLE of a normal variance with known mean, p424; an unbiased estimator of μ³ under normal sampling, p425; and size and power for a shifted-uniform test, p432.
- **MGF note (p426):** the Laplace symmetry question was also added to Probability. The source says the MGF equality holds for all real t; the bank corrects this to the common MGF domain |t|<1.

### Pages held out after inspection

- **Page 427:** the parameter range for α is not specified clearly enough to validate the claim about power; other statements in the list are false as written.
- **Page 428:** the density and parameterisation are too faint to transcribe safely.
- **Page 430:** the printed power options do not match the direct Laplace-tail calculation unless missing 1/2 factors are supplied; held out pending a clearer source.
- **Page 431:** the density formula is too blurred to identify its normalising constant and moments reliably.


## Batch 41 — pages 433–444

Six questions were imported after visual inspection:
- **Probability (5):** uniform-interval absolute-deviation probability, p437; standard-normal interval probability using symmetry, p438; correlation of overlapping sums of iid variables, p441; dependence of overlapping coin-toss events, p442; and expectation involving a binomial variable and its complement, p443.
- **Regression (1):** unbiased residual-variance estimator in simple linear regression, p439.

### Pages held out after inspection

- **Page 433:** the density expression is too faint to identify the support and polynomial safely.
- **Page 434:** the printed paired-data table is not sufficiently clear to transcribe all observations reliably.
- **Page 435:** the estimator notation and summation limits are unclear in the scan.
- **Page 436:** the parameterised probability table and observed values are not legible enough to establish the likelihood.
- **Page 440:** the exponential-density rate/scale parameter is not clear enough to evaluate the requested density at the mean.
- **Page 444:** the variance expression and target parameter power are too faint to determine the intended unbiased-estimation question.


## Batch 42 — pages 445–456

Five questions were imported after visual inspection:
- **Probability (4):** memoryless conditional probability for a geometric variable, p445; law of total probability for finding lost keys, p447; sum of two independent Poisson scratch counts, p449; and recovering the parameters and variance of a uniform distribution from its mean and a CDF probability, p450.
- **Statistical Inference (1):** size and power of a test for two discrete-uniform hypotheses, p446.

### Pages held out after inspection

- **Page 448:** duplicate of the geometric memoryless conditional-probability question on page 445, with shifted index; not imported twice.
- **Page 451:** the displayed Poisson estimator options and target power are not legible enough to identify the intended unbiased estimator safely.
- **Page 452:** the question does not state whether the displayed standard deviation uses the sample or population divisor; the sum of squared deviations therefore depends on the convention.
- **Page 453:** section/advertisement page, no question.
- **Page 454:** the betting rule and probability are garbled, so the remaining money cannot be calculated reliably.
- **Page 455:** the event notation involving the two discrete-uniform variables is unreadable.
- **Page 456:** the dice event and answer choices are too corrupted to establish the intended probability.


## Batch 43 — pages 457–468

Three questions were imported after visual review:
- **Probability (2):** alternating queue arrangements for four boys and three girls, p458; and the logarithmic expectation of a Beta(θ,1) variable, p467.
- **Statistical Inference (1):** non-existence of an MLE when the Bernoulli parameter space is the open interval (0,1) and all observations are successes, p461. The boundary condition is retained explicitly; if p=1 were allowed, the maximiser would be 1.

### Pages held out after inspection

- **Page 457:** the two life probabilities and event relationship are too corrupted to establish the intended joint probability.
- **Page 459:** the random-variable expression and requested expectation are not legible enough to transcribe.
- **Page 460:** the proposed probability mass function and event statements are corrupted; normalization cannot be checked.
- **Page 462:** the expression involving two standard normal variables is unreadable.
- **Page 463:** the Gamma-distribution parameterisations and requested ratio are unclear.
- **Page 464:** the sample distribution and expression are too faint to identify.
- **Page 465:** the shifted-density formula is not legible enough to determine the MLE.
- **Page 466:** the confidence-interval expression and options are incomplete in the scan.
- **Page 468:** the covariance expression is too corrupted to identify the random variables and coefficients.


## Batch 44 — pages 469–480

Six questions were imported after visual review:
- **Probability (5):** Cauchy reciprocal/sum stability and the distribution of a harmonic-type statistic, p469; correlation of two linear combinations of independent standard normals, p471; expectation of a product involving independent uniforms, p473; weak law, second-moment law and CLT statements from given moments, p476; and properties of the difference of two iid exponential variables, p480.
- **Statistical Inference (1):** sufficient statistics for a normal location model with known variance, p470.

### Pages held out after inspection

- **Page 472:** the distribution symbol and the relation between the original variable and sample statistic are missing from the scan.
- **Page 474:** same missing distribution symbols as the nearby question; insufficient information to reconstruct the claim safely.
- **Page 475:** the conditional binomial formulae and sample-size notation are incomplete/blurred.
- **Page 477:** duplicate of the moment/WLLN/CLT question on page 476; not imported twice.
- **Page 478:** the Gamma shape parameters and ratio expressions are too faint to establish the intended Beta-distribution parameters.
- **Page 479:** the expressions involving the two normal variables are partly illegible; the complete statement set cannot be validated.


## Batch 45 — pages 481–492

Four questions were imported after visual inspection:
- **Probability (3):** expected number of Uniform(0,1) samples until their sum exceeds one, p483; the two-toss von Neumann method for unbiased selection with a biased coin, p485; and strictly increasing outcomes from three sequential fair-die throws, p486.
- **Statistical Inference (1):** size and power for testing between two uniform distributions with a specified critical region, p488.

### Pages held out after inspection

- **Page 481:** the continuous-distribution notation and all multi-select statements are too faint to reconstruct reliably.
- **Page 482:** the binomial mode expression and options are corrupted.
- **Page 484:** the question about generating a normal variate from a Bernoulli generator is not sufficiently specified about the allowed computational operations and precision.
- **Page 487:** the displayed discrete probability formula is unreadable.
- **Page 489:** the density formula for the sample and unknown parameter is too corrupted to derive the MLE safely.
- **Pages 490–491:** the density and confidence-interval expressions are too faint to identify the model and pivot.
- **Page 492:** the chi-square/sum expression is incomplete in the scan.


## Batch 46 — pages 493–504

Three questions were imported after visual inspection:
- **Probability (2):** large-parameter normal approximation for a Poisson variable, p501; and the CLT for the average of squared iid standard normal variables, p504.
- **Statistical Inference (1):** unbiasedness and consistency of a weighted sample-mean estimator, p496.

### Pages held out after inspection

- **Page 493:** the discrete-uniform parameter notation and requested complete/minimal sufficient statistic are incomplete.
- **Page 494:** the quadratic-form definitions and matrix expressions are too faint to determine the degrees of freedom and independence claims.
- **Page 495:** more than one displayed estimator is not unbiased for θ under Uniform(0,θ), so the single-choice wording has multiple correct answers.
- **Page 497:** the Bernoulli parameter interval and estimator expressions are corrupted.
- **Page 498:** the two estimators used in the efficiency comparison are not legible enough to compute their variances.
- **Page 499:** the exponential density and reliability target are too faint to reconstruct the likelihood safely.
- **Page 500:** the displayed statistic and denominator are incomplete, so its sampling distribution cannot be keyed.
- **Page 502:** two answer options repeat the same statement about Z and W, leaving the intended single-choice key ambiguous.
- **Page 503:** the definition of Yᵢ and the normalising constants in the limiting expressions are illegible.


## Batch 47 — pages 505–516

Six questions were imported after visual review:
- **Probability (5):** distributional and dependence properties of ratios of independent standard normals, p505; expectation identity for a normal and a chi-square variable without an independence assumption, p506; fourth moment of a sum of four iid Rademacher variables, p507; nested conditional-uniform expectation, p510; and universal probability bounds for two events, p516.
- **Statistical Inference (1):** comparing size and power of four tests for Uniform(0,θ) hypotheses, p515.

### Pages held out after inspection

- **Page 508:** the stated standard deviation and confidence requirement imply a sample size far larger than any printed option; the scan may have a missing decimal or transcription error.
- **Page 509:** section/advertisement page, no question.
- **Page 511:** the conditional distribution of X_N and the parameter of the binomial family are not sufficiently legible.
- **Page 512:** the random-sum definition and the exceptional value when N=0 are too corrupted to identify unambiguously.
- **Page 513:** the estimator expressions for the exponential functional are too faint to distinguish.
- **Page 514:** the four sequence expressions and normalising factors are incomplete in the scan.


## Batch 48 — pages 517–528

Six questions were imported after visual inspection:
- **Probability (5):** distribution transformations involving uniform and exponential variables, p519; characterisation of CDFs under reflection, mixtures and products, p520; annual expected accident-cleanup cost under a Poisson model, p524; mixture proportions for elective registration, p526; and variance of a product of independent variables, p528.
- **Statistical Inference (1):** sufficiency for the variance parameter in a zero-mean normal sample, p521.

### Pages held out after inspection

- **Page 517:** the UMVU estimator expressions are too faint to distinguish the intended parameter and constants.
- **Page 518:** the prior variance notation and the proposed Bayes estimator are incomplete/blurred.
- **Page 522:** the sample covariance definitions and candidate MLEs for the bivariate-normal correlation are not sufficiently legible.
- **Page 523:** the estimator sequence and target parameter in the consistency question are corrupted.
- **Page 525:** the power of the standard-normal moment in the expectation is not readable.
- **Page 527:** the displayed standardised expectation/variance expression is incomplete.


## Batch 49 — pages 529–540

Eight questions were imported after visual inspection:
- **Probability (7):** central limit theorem for geometric variables, p532; expected minimum of a normal sample of size two, p533; conditional probability for a uniform variable, p534; covariance from a conditional normal model, p535; variance from a probability generating function, p537; correlation involving a product of independent normal variables, p538; and a Bernoulli-driven sequence limit, p540.
- **Stochastic Processes (1):** the defining martingale conditional-expectation identity, p530.

### Pages held out after inspection

- **Page 529:** the joint-density expression and conditional-expectation options are too faint to transcribe safely.
- **Page 531:** the conditional-expectation identities and the final option are partly corrupted; the exact source statements cannot be recovered confidently.
- **Page 536:** the bivariate-normal parameter values and the two linear combinations in the correlation question are not sufficiently legible.
- **Page 539:** the weighted-sum expressions and their normalising constants are blurred, preventing a reliable convergence comparison.


## Batch 50 — pages 541–552

Six questions were imported after visual inspection:
- **Probability (6):** reciprocal relationship between F distributions, p543; covariance of a symmetric two-point variable and its square, p545; a bivariate-normal difference tail probability, p547; a Chebyshev bound for independent symmetric variables, p548; minimum of two independent Poisson counts, p549; and a high-order moment of a Bernoulli variable, p552.

### Pages held out after inspection

- **Page 541:** the first two almost-sure convergence statements are not fully legible, so the complete multi-select key cannot be established.
- **Page 542:** the convergence-in-distribution notation is corrupted and the intended joint limit is unclear.
- **Page 544:** statements 3 and 4 have missing summation/normalising expressions.
- **Page 546:** the distribution probabilities and definition of the partial-sum statistic are not legible enough to identify the limit.
- **Page 550:** the event threshold and summation expression in the limit are incomplete.
- **Page 551:** the Poisson tail thresholds and comparison integral are too faint to determine the correct limiting probability statements.


## Batch 51 — pages 553–564

Nine questions were imported after visual inspection:
- **Probability (9):** covariance of a sample mean and its first residual, p554; LLN for squared shifted-exponential observations, p555; probability that a continuous sample mean equals its mean exactly, p556; characteristic functions under products and mixtures, p557; conditional-normal construction of a standard normal variable, p560; characteristic function of a symmetric two-point variable, p561; dependence in a joint density proportional to x+y, p562; square transformation of a symmetric uniform variable, p563; and a comparison probability for two independent uniform variables, p564.

### Pages held out after inspection

- **Page 553:** the answer depends on the ordering of θ₁ and θ₂, which is not stated; the listed options do not cover both parameter orderings.
- **Page 558:** the limiting statistic and summation bounds are too faint to identify.
- **Page 559:** the statistic W and its scaling are unreadable, so the sampling distribution cannot be keyed.


## Batch 52 — pages 565–576

Eleven additional questions were imported after visual inspection:
- **Probability (11):** identifying a Poisson summand from an independent Poisson sum, p565; marginals and dependence from a triangular joint density, p566; an expectation involving independent identically distributed MGFs, p567; a Gamma law from the probability integral transform, p568; the density of a squared continuous random variable, p569; the ordering probability for two iid continuous variables, p570; a Poisson CDF evaluated at a non-integer point, p571; a Chebyshev upper bound, p572; the positive-part expectation of a standard normal variable, p573; CDF-preserving transformations, p574; and a trigonometric probability under a uniform distribution, p576.

### Page held out after inspection

- **Page 575:** held out because the conditioning notation around the absolute value and integer-part brackets is not sufficiently unambiguous in the scan to reproduce the exact event safely. The algebraic options alone do not resolve the intended conditioning event.

The page 566 marginal was recomputed by integrating the joint density over its triangular support. On page 568, the probability integral transform gives iid Uniform(0,1) variables; applying −log produces iid Exp(1) variables, whose sum is Gamma(n,1). The page 574 functions are both valid CDFs because each is a continuous non-decreasing transformation of F with endpoint values 0 and 1.


## Batch 53 — pages 577–588

Eleven additional questions were imported after visual inspection:
- **Probability (7):** a standard-normal probability obtained by factoring a cubic inequality, p577; a logarithmic transform of a Uniform(0,1) variable, p578; point masses and expectation recovered from a step CDF, p579; the MGF of a binomial-type PMF, p580; a closed-interval probability from a discontinuous CDF, p581; a weak-law/Chebyshev limit for a sum of uniforms, p585; and independence of events in a finite equally likely sample space, p587.
- **Statistical Inference (4):** Neyman–Pearson testing for two values of a Rayleigh-type parameter, p582; a discrete-uniform UMP test, p583; Type I and Type II errors for an exponential test, p586; and the MLE for a power-family density, p588.

### Page held out after inspection

- **Page 584:** decorative/advertising page, not a question.

The p582 test is keyed using the likelihood ratio: for the larger alternative value of λ, the likelihood ratio decreases with ΣXᵢ², so the rejection region is for small sums of squares. Page 583 uses the exact 0.1 null probability P₀(X≤4)=4/40. Page 585's limit is 1 because the threshold exceeds the mean by n^(3/4), which grows faster than the standard deviation of order n^(1/2).


## Batch 54 — pages 589–600

Twelve questions were imported after visual inspection:
- **Probability (7):** conditional regression from a triangular-support joint density, p590; a shifted-uniform square transformation, p592; the Poisson sample-mean CLT, p594; normalising exp(−x⁴) as a density, p595; correlation of two overlapping normal sums, p597; a Poisson–exponential mixture variance, p598; and implications of positive association between two events, p600.
- **Statistical Inference (4):** method-of-moments estimation for a scaled triangular density, p589; MLE for a shifted exponential distribution, p591; power of a test between two shifted uniform distributions, p593; and an MLE determined by sample support constraints, p596.
- **Multivariate Analysis (1):** identifying a valid variance-covariance matrix using symmetry and positive semidefiniteness, p599.

All twelve source questions on pages 589–600 were legible enough to verify. The likelihood in page 596 is maximised at the smallest parameter value satisfying the support restrictions, θ=27.


## Batch 55 — pages 601–624

Fourteen questions from this range are now represented in the supplementary banks: eight were imported in the preceding commits and six are added in this update.

- **Statistical Inference (6):** unbiased-estimator checks for a normal model with mean and variance linked to θ, p601; consistency of variance estimators, p603; MLE set for a location parameter in a uniform model, p605; exponential-rate MLE by invariance, p607; size of an exponential test, p611; size-plus-power calculation for a uniform-family test, p612; and the non-uniqueness of the Laplace location MLE for an even sample, p615; plus the effect of a smaller known variance on a two-sided z-test p-value, p622.
- **Probability (7):** conditional expectation from a triangular joint density, p606; a probability limit for a normal sample mean, p610; conditional probability from a CDF with an atom at zero, p614; density under a monotone square transformation, p616; normalising a density with two exponential tails, p620; and a CLT for the sample mean of squared standard normals, p623.

### Pages held out after visual inspection

- **Page 602:** duplicates an already represented iid-binomial sum/covariance question.
- **Page 604:** formula/statistic expressions are too faint to transcribe reliably.
- **Page 608:** the density and requested expectation are not sufficiently legible.
- **Page 609:** the joint-density normalising expression is too faint to distinguish reliably.
- **Page 613:** the displayed ratio/statistic is unreadable.
- **Page 617:** the alternative distribution is not specified clearly enough; the visible wording only states Uniform(0,1), so size and power cannot both be inferred without assuming a missing parameterised model.
- **Page 618:** the density parameterisation is corrupted.
- **Page 619:** the binomial asymptotic expression and option exponents are not reliably legible.
- **Page 621:** although the joint density is partly readable, the multi-dimensional integral and source answer cannot be independently confirmed from this scan.
- **Page 624:** the estimator formula/options are corrupted.

For p614, the atom at zero is 1/4 and the conditioning event has probability 3/4, giving 1/3. For p616, the shift X+1 is Uniform(0,2), making the square transformation monotone. For p620, symmetry reduces the normalising integral to two exponential tails. For p623, the variance of X² for standard normal X is 2, giving the stated CLT scaling. The p615 MLE is any sample median; with ten observations it is generally an interval, not a unique point.


## Batch 56 — pages 625–636

Five additional questions were imported after visual inspection:
- **Statistical Inference (2):** distribution of the sample-minimum MLE in a shifted exponential location model, p625; and a delta-method asymptotic test for equality of two Poisson means, p628.
- **Probability (3):** Poisson approximation to the overbooking/refusal probability for a 250-ticket, 248-seat flight, p631; an expectation identity that remains valid without independence, p633; and reciprocal invariance of the standard Cauchy distribution, p636.

### Pages held out after inspection
- **Page 626:** the likelihood gives θ̂=1/15 and hence the estimated two-car household proportion is 2θ̂=2/15, which is absent from all four printed options. The item is held out rather than changing its source answer choices.
- Pages 627, 629, 630, 632, 634 and 635 were already imported in the preceding batch and were not duplicated.

The p625 MLE is the sample minimum, whose shifted-exponential scale is σ/n. For p628, the delta method gives asymptotic variance 1/(4m)+1/(4n) for √X̄−√Ȳ under H₀. For p631, refusal occurs with zero or one no-show; the Poisson(2.5) approximation gives e^(−2.5)(1+2.5). Page 633 is keyed using linearity of expectation, which does not require independence.


## Batch 57 — pages 637–648

Four additional questions were imported after visual inspection:
- **Statistical Inference (3):** consistency and limiting mean of the full-data and sign-only MLEs in a bounded normal-location model, p638; unbiasedness of the sample variance across four candidate families, p639; and power calibration for a one-observation Cauchy location test, p645.
- **Stochastic Processes (1):** conditional arrival-time probability in a Poisson process given the second arrival time, p646.

### Pages held out after inspection
- **Page 637:** the printed single-choice item has two mathematically correct choices: the UMP test rejects for large X²+Y, and under H₀ the statistic X²+Y has a chi-square distribution with three degrees of freedom. It is excluded rather than forcing a single answer.
- Pages 640, 641, 642, 643, 644, 647 and 648 were already imported and were not duplicated.

For p638, the sign-only observations are Bernoulli with success probability Φ(θ); the inverse-CDF MLE is consistent, and boundedness gives convergence of its expectation. For p639, the sample variance is unbiased for the population variance, which equals θ in the Poisson(θ) and Normal(0,θ) models only. For p645, the standard Cauchy alternative is symmetric, so the threshold C=0 gives power one-half. For p646, conditional on the second Poisson arrival at 40 minutes, the first arrival is uniform on (0,40), giving probability 1/4 of occurring after minute 30.



## Batch 58 — pages 649–656

Seven additional questions were imported after visual inspection:
- **Probability (4):** four convergence-in-probability statements for independent Normal(2,5) variables, p649; complement probability for two mutually exclusive race winners, p651; conditional Biology readership given Mathematics readership, p652; and the position of the second red ball in sampling without replacement, p653.
- **Statistical Inference (3):** maximum likelihood estimation for a uniform triangular support, p650; UMP upper-tail regions in the power-density family, p654; and limiting power of a Bernoulli one-sided test, p656.

### Pages held out after inspection
- **Page 655:** duplicate of the triangular-region MLE problem on page 650; excluded to avoid duplicate content.
- Pages 651–653 contain short, compactly printed probability questions. The wording and answer choices were checked at higher resolution before transcription.

The p649 statements follow from the weak law and continuous mapping; in particular E(X²)=Var(X)+[E(X)]²=9. For p650, the likelihood is proportional to θ^(−2n) subject to θ≥maxᵢ(Xᵢ+Yᵢ), so the MLE is the smallest feasible value. Page 651 uses mutual exclusivity of the two winning events, not independence. Page 652 is a direct conditional-probability calculation. For p653, there must be one red position among the first four, a red at position five, and the third red after position five, giving 16/C(9,3)=4/21. For p654, the likelihood has a monotone likelihood ratio in Σlog(Xᵢ), supporting the upper-tail region for both stated increasing alternatives. For p656, the alternative mean 3n/4 separates from the null critical boundary near n/2 by order n, so power tends to one.



## Batch 59 — pages 657–664

Eight additional questions were imported after visual inspection:
- **Probability (3):** reliability of two independent components connected in series, p657; variance comparison between equal-mean Binomial and Poisson variables, p658; and symmetry implied by alternating-sign convergence in distribution, p662.
- **Statistical Inference (5):** consistency versus unbiasedness of a smoothed Bernoulli estimator, p659; a one-sided one-sample t-test decision from seven observations, p660; a Student t distribution arising from an independent normal numerator and sample variance, p661; an unbiased estimator of θ² for a shifted uniform model, p663; and the Neyman–Pearson most powerful test for two specified densities, p664.

All eight items were visually legible and independently checked. For p657, the series-system reliability is the product of the two survival probabilities. For p658, equal means give λ=np and hence np(1−p)<λ. The p659 estimator has bias (1/2−θ)/(√n+1), which tends to zero, and it is consistent. For p660, the observed t statistic is approximately −0.633, so the upper-tail test does not reject at either level. For p661, independence of X₁₀₀ and the first 99 observations gives t(98). Page 662 implies X and −X have the same distribution. Page 663 uses E[(X−5)²]=θ²/3. For p664, the likelihood ratio decreases in X, so the most powerful test rejects for X<α and has power √α.


## Batch 61 — pages 665–672

Eight additional questions were imported after visual inspection:
- **Probability (5):** expected occupancy of the two extreme slots when ten balls are placed randomly into six slots, p667; reliability of a parallel system with independent components, p668; expectations from a joint density with a uniform mixing variable, p669; expectation under a Poisson–Binomial conditional construction, p670; and a random-radius circle area probability, p672.
- **Statistical Inference (2):** power of a Neyman–Pearson most powerful test for two specified densities, p665; and MLE for a Pareto-type density with parameter-dependent support, p666.
- **Stochastic Processes (1):** variance of the index at which cumulative exponential inter-arrival times first exceed a fixed time, p671.

All eight questions were legible and checked independently. The p665 rejection region is an upper tail because the likelihood ratio 2x² increases in x; the resulting power is 19/100. For p666, the likelihood increases in θ over θ≤min(Xᵢ), so the MLE is the sample minimum. The expected occupancy in p667 follows by linearity of expectation. Page 668 uses the probability that all components fail. For p669, Y is Uniform(0,1) and X|Y=y is exponential with mean y. Page 670 is a Poisson variable mixed with a conditional Binomial distribution. Page 671 identifies N as one plus a Poisson(λ) count over unit time. Page 672 reduces the area condition to R<1/√π.


## Batch 62 — pages 673–680

Seven additional questions were imported after visual inspection:
- **Probability (2):** repeated independent target-destruction attempts conditioned on five initial failures, p673; and the geometric distribution induced by grouping an exponential observation into unit intervals, p678.
- **Statistical Inference (5):** a Neyman–Pearson upper-tail test for a one-parameter density, p675; the UMVU variance lower bound when X|Y is Binomial and Y is Poisson, p676; a most powerful test for a Gamma(shape 2) family, p677; Type I and Type II errors for a four-toss binomial test, p679; and MLE of θ² for a shifted exponential model, p680.

**Held out:** page 674 repeats the randomised normal linear-combination question already represented by page 560; it was not imported again.

The p673 probability is 0.2²×0.8=0.032 because attempts after the first five remain independent. For p675, the likelihood ratio is 2x and the size-.2 upper-tail cutoff under Uniform(0,1) is 4/5. For p676, Y is complete sufficient for λ and has variance λ, so it is UMVU. For p677, under H₀, 4X~χ²₄, giving the upper-tail critical value χ²₄,α/4. For p678, P(Y=k)=(1−e^(−1/θ))e^(−k/θ), a geometric pmf on nonnegative integers. For p679, α=1/8 and β=87/128. For p680, the likelihood increases over θ≤min(Xᵢ), so θ̂=1.7 and the MLE of θ² is 2.89.


## Batch 63 — pages 681–688

Seven additional questions were imported after visual inspection:
- **Statistical Inference (7):** consistency of order-statistic estimators for a shifted uniform distribution, p681; sufficiency of the sample sum across four distribution families, p682; the UMVUE of λ² for a Poisson sample, p683; two-sided and one-sided 90% confidence intervals for an exponential rate, p684; the UMVUE of the reciprocal mean of an exponential distribution, p685; the Cramér–Rao lower bound for estimating θ² under an exponential mean parameterisation, p686; and MLE of a reciprocal parameter under a Weibull-type density, p688.

**Held out:** page 687 asks for a single unbiased estimator of θ² from a Normal(θ,2θ²) sample, but both ΣXᵢ²/(3n) and Σ(Xᵢ−X̄)²/[2(n−1)] are unbiased. The source's single-answer marking is therefore not unique; it was excluded rather than silently converted into an MSQ.

The p681 maximum order statistic converges to θ+1/2, making option B converge to θ+1. In p682, the sum is sufficient for Poisson, exponential-rate and Bernoulli models, but not for Normal(0,σ²) with unknown variance, where the sum of squares is sufficient. For p683, the complete sufficient Poisson sum S gives UMVUE S(S−1)/n²; the observed value is 24. For p684, the pivot 2θΣXᵢ~χ²₂ₙ supports the central 90% interval and the one-sided upper 90% interval (with the source's upper-tail chi-square notation). For p685, E(1/S)=1/[(n−1)θ], giving the UMVUE (n−1)/S. Page 686 applies the CRLB with Iₙ(θ)=n/θ² and g′(θ)=2θ. Page 688 uses the invariance property after maximising n log θ−θΣXᵢ³.


## Batch 64 — pages 689–696

Four additional questions were imported after visual inspection:
- **Statistical Inference (4):** MLE for the scale parameter of a Gamma(shape 3) model, p691; most powerful testing for two Laplace scale parameters, p693; unbiasedness and consistency of the normal sample mean and sample variance, p694; and constrained integer-valued normal mean MLE, p695.

**Held out after inspection:**
- **Page 689:** the source asks for a single non-unbiased estimator, but both options C and D are not unbiased under the stated exponential model. The single-answer key is not unique.
- **Page 690:** both X₍n₎ and ((n+1)/n)X₍n₎ are consistent for θ under Uniform(0,θ), although the source says “Select one”.
- **Page 692:** the wording and right-hand distribution statement for option C are cut off in the scan, so the claimed auxiliary/ancillary property cannot be checked reliably.
- **Page 696:** the order-statistic expression in option C is not legible enough to distinguish the statistic inside the minimum; the source's key cannot be independently validated.

For p691, differentiating the Gamma(shape 3, scale θ) log-likelihood gives θ̂=X̄/3. For p693, the likelihood ratio increases with Σ|Xᵢ| when θ₁>θ₀, so the MP test is upper-tailed. For p694, X̄ and the usual unbiased S² are both unbiased, with variances tending to zero. For p695, the sample mean is 0.82 and the closest allowed integer is 1.


## Batch 64 — pages 689–690

Two additional questions were imported after visual inspection:
- **Statistical Inference (2):** identifying the non-unbiased estimator of the mean parameter in an exponential sample, p689; and consistency of endpoint-based statistics for a Uniform(0,θ) sample, p690.

For p689, the source's Exp(θ) notation is interpreted as an exponential distribution with mean θ, as implied by the estimator options. The sample minimum and sample mean are unbiased for θ, and the listed combination of the minimum and sample mean is also unbiased. The scaled second order statistic has a different expectation and is the answer. For p690, the sample maximum and its factor (n+1)/n multiple converge to θ. The sample mean converges to θ/2, while (n+1) times the minimum has a non-degenerate limiting distribution and is not consistent.

Pages 692 and 696 were held out: page 692 contains a clipped/illegible option, while page 696's displayed estimator options and marked key do not agree with the unbiasedness calculations for Uniform(−θ,θ). They are not imported until the source can be resolved unambiguously.


## Batch 65 — pages 697–704

Five additional questions were imported after visual inspection:
- **Statistical Inference (2):** critical value for a size-0.05 likelihood-ratio test between two Normal distributions, p697; and confidence coefficient of an interval based on the minimum from a shifted exponential sample, p700.
- **Probability (3):** probability of at least one defective bulb in a sample without replacement, p702; a two-card event involving a red card and a queen, p703; and the posterior probability that a lost card was a club after two clubs are drawn, p704.

### Source-key correction and held-out items
- **Page 697:** the source answer field gives 0.05, which is the significance level, not the requested critical value. The likelihood-ratio test rejects for large X; under H₀, the correct cutoff is the standard-normal 95th percentile, approximately 1.645. The imported item records the mathematical correction.
- **Page 698:** held out because the keyed power is 2.5, which is impossible for a probability, and the printed density notation is not sufficiently clear to resolve the source's intended model.
- **Page 699:** held out because the estimator whose MSE is requested is not specified in the scan.
- **Page 701:** held out because the displayed Normal parameterisation is unclear and does not reconcile reliably with the keyed sample size.
- Pages 702–704 were legible. Page 702 uses the complement of drawing two good bulbs. Page 703 counts 101 favourable unordered pairs among 1326. Page 704 applies Bayes' theorem to the two possible suits of the lost card.


## Batch 66 — pages 705–712

Six additional probability questions were imported after visual inspection:
- **Page 705:** binomial probability that at least four of five ships arrive safely (independent arrivals assumed).
- **Page 708:** probability that two tickets drawn without replacement are both even.
- **Page 709:** probability that three balls drawn from a three-colour box are not all the same colour.
- **Page 710:** probability that two witnesses contradict each other (independent truth/falsehood outcomes assumed).
- **Page 711:** solving for P(B) under mutual exclusivity and independence, given P(A) and P(A∪B).
- **Page 712:** normalising a discrete probability mass function and evaluating three requested event probabilities.

### Held-out pages
- **Page 706:** the statement omits the variance value after “mean and variance … are 4 and”, so the binomial parameters cannot be recovered from the printed question.
- **Page 707:** the two missing cards are not specified as randomly missing; without that assumption, the spade probability depends on which cards are absent. The scan's intended 1/4 answer requires a random-missing-card assumption, so the item is held out as written.

All six imported items were checked independently. The p705 answer uses the Binomial(5,0.9) model. Pages 708 and 709 use combinations/without-replacement probabilities. Page 710 explicitly records the independence assumption required to compute the contradiction probability. Page 711 uses the addition rule in the mutually exclusive case and the independence formula in the second case. Page 712 normalises the eight masses to obtain a=1/48 before summing the requested probabilities.


## Batch 67 — pages 716–720

Five additional questions were imported after visual inspection:
- **Statistical Inference (4):** sufficiency, completeness and UMVU estimation for a Normal(0,2θ²) sample, p716; critical value for a most powerful test in a Pareto family, p717; size and power of a specified discrete test, p718; and the most powerful rejection region for two exponential-mixture parameter points, p719.
- **Probability (1):** density of the sum of two independent exponential random variables with distinct rates, p720.

### Corrections and held-out pages
- **Page 719:** the source check mark points to the upper-tail option. The likelihood ratio under H₁ versus H₀ is 4ⁿexp(−3ΣXᵢ), which decreases in the sample sum. The mathematically correct most powerful region is therefore the lower tail, option C; the source mark is corrected in the imported item.
- **Page 713:** held out because the number of binomial trials is missing from the scan. The keyed answer 0.2048 would be consistent with five trials and p=0.2, but that trial count is not visible and is not inferred.
- **Page 714:** held out because the weighted expected value from the stated 75% five-point and 25% seven-point outcomes is 5.5, which does not match the marked option 5.25.
- **Page 715:** held out because the fair-game payment does not reconcile with the stated payouts and overlapping card events; the source's marked value cannot be justified without an additional payout convention.

For p716, the full sample vector is sufficient but not complete; the sum of squares is complete sufficient, and its scaled version gives the UMVU estimator. For p717, the likelihood ratio 6/x is decreasing and the H₀ lower-tail probability 0.1 gives k=10/3. For p718, the rejection region {2,3} has size 0.3 and power 0.7. For p719, the lower-tail form follows directly from the decreasing likelihood ratio. For p720, convolution of the two exponential densities yields the hypoexponential density shown in option C.


## Batch 68 — pages 721–728

Six additional questions were imported after visual inspection:
- **Probability (4):** equality case of Jensen's inequality for the exponential function, p721; Gumbel limit of the centred maximum of iid Exponential(1) observations, p722; a conditional density derived from a joint density on 0<x<y<1, p724; and a Chebyshev lower bound for a two-standard-deviation interval, p726.
- **Statistical Inference (2):** exact confidence interval for the rate of an exponential distribution, p725; and the Neyman–Pearson critical region for two specified densities, p728.

### Held-out pages
- **Page 723:** the printed distributions are X~Uniform(0,2), Y~Uniform(1,3), independent. Direct integration gives P(X<Y)=7/8, option C. The source mark indicates 3/4; the imported item corrects that key using the conditional probability integral.
- **Page 727:** the event "get an A in Chemistry" is not clearly distinguished from choosing Chemistry by a fair coin and then getting an A. The corresponding probabilities differ, and the listed options do not resolve the intended event, so the item is held.

For p721, equality in Jensen for a strictly convex function forces X to be constant almost surely. For p722, the maximum CDF is [1−e^(−x)/n]ⁿ after centring, converging to e^(−e^(−x)). For p724, fY(y)=4y³ and fX|Y(x|y)=2x/y². Page 725 follows from 2θΣXᵢ~χ²₂ₙ. Page 726 applies Chebyshev with k=2. Page 728 uses the likelihood ratio 16(x₁x₂)³, so the critical region is ln x₁+ln x₂>c.


### Page 723 correction
The page-723 question is now imported with answer 7/8. The source key's 3/4 is incorrect: for 0<x<1, P(Y>x)=1, and for 1≤x<2, P(Y>x)=(3−x)/2. Integrating against the Uniform(0,2) density gives 1/2+3/8=7/8.


## Batch 69 — pages 729–736

Seven additional questions were imported after visual inspection:
- **Probability (4):** existence of the first moment but not a finite variance for a Pareto-type density, p729; an absolute-value logarithmic transform of a Uniform(−5,5) variable, p730; the negative-binomial distribution of the sum of four geometric variables, p734; and point mass from a jump in a CDF, p735.
- **Statistical Inference (2):** likelihood function with parameter-dependent support, p731; and expected residual sum of squares for a Normal sample, p736.
- **Regression (1):** regression line derived from a shifted exponential conditional density, p732.

### Held-out page
- **Page 733:** the systematic-sampling relative-efficiency question is held out pending clarification of the intended intraclass-correlation design and variance comparison. The marked answer 1/7 is not imported without a fully justified design-effect calculation.

For p729, E(X)=2 but E(X²) diverges, so variance is not finite. For p730, |X|/5 is Uniform(0,1), and its negative logarithm is Exp(1). For p731, the support restriction is θ≥maxᵢ|Xᵢ|. For p732, E(Y|X=x)=x+β. For p734, the sum of four geometric(p=1/4) variables has a negative-binomial distribution. For p735, the jump at x=1/2 is 5/8−1/2=1/8. For p736, E(S)=(11−1)×4=40.
