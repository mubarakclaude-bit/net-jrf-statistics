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


## Further verified additions — pages 801–810

Seven additional questions were checked and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 801 | `mcq1000-p801` | Statistical Inference T5 — unbiased estimation from a mixture | D, (S_n/(3n)) |
| 802 | `mcq1000-p802` | Probability T9 — consistency via the law of large numbers | C, (	heta/e) |
| 803 | `mcq1000-p803` | Statistical Inference T4 — MLE from coarsened Bernoulli indicators | B, (1-\bar Y) |
| 804 | `mcq1000-p804` | Probability T8 — counting outcomes for five dice | A, (15/6^5) |
| 805 | `mcq1000-p805` | Probability T8 — symmetry and expectation | A, (1/3) |
| 807 | `mcq1000-p807` | Stochastic Processes T6 — multiplicative betting/random walk | D, none of the listed outcomes |
| 810 | `mcq1000-p810` | Probability T8 — modular arithmetic and discrete probability | C, 0.25 |

### Source correction
- **Page 801:** the printed mark appears beside option C, but the mixture has mean (3\mu). The unbiased estimator is (S_n/(3n)), option D. The item records this correction.

### Pages held out in this range
- **Page 806:** the pivotal expression is clipped/ambiguous at the left margin, so the confidence-bound event cannot be transcribed reliably.
- **Page 808:** the intersection probability cannot be determined from the two marginal survival probabilities alone; independence is not stated. The source's product answer assumes an unstated condition, so the item is excluded.
- **Page 809:** the four displayed probabilities sum to (	heta+2/45), not 1 for general (	heta). The displayed function is not a valid pmf as written; excluded.

### Updated draft counts
- Probability: **421**
- Statistical Inference: **192**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **8**
- Total: **640 supplementary items** on this branch (54 additions in this batch branch).

No item was accepted solely on the basis of a printed answer mark. These questions remain draft-only pending CI and review.


## Further verified additions — pages 811–820

Eight questions were checked against enlarged page images and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 811 | `mcq1000-p811` | Probability T8 — arrangements and counting | A, 1/35 |
| 812 | `mcq1000-p812` | Statistical Inference T4 — MLE with shifted-exponential support | A, sample minimum |
| 813 | `mcq1000-p813` | Statistical Inference T5 — least-squares minimisation | B, c=4 |
| 815 | `mcq1000-p815` | Probability T10 — expectation under independent transformations | B, none of the listed values (expectation 0) |
| 816 | `mcq1000-p816` | Statistical Inference T13 — length of a t confidence interval | C, (2s,t_{1-\alpha/2,n-1}/\sqrt n) |
| 817 | `mcq1000-p817` | Probability T6 — Beta log-moment | C, (-1/\theta) |
| 818 | `mcq1000-p818` | Probability T6 — Cauchy reciprocal and stability | B, statements C and D |
| 820 | `mcq1000-p820` | Probability T10 — symmetry of a bivariate normal expression | A, 0 |

### Pages held out in this range
- **Page 814:** the Gamma distributions' scale/rate parameterisation is not stated; (E(\sqrt{XY})) depends on that parameterisation.
- **Page 819:** the distribution denoted by the asterisk is missing from the question statement; cannot determine the requested family for the sample mean.

### Updated branch counts
- Probability: **426**
- Statistical Inference: **195**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **8**
- Total: **648 supplementary items** on this branch (62 additions in this batch branch).

Page 818 was adapted to the repository's four-statement multi-select format by adding one explicitly identified symmetry statement. No claim is made that every item in the scanned PDF has now been reviewed.


## Further verified additions — pages 821–830

Nine more questions were visually transcribed and checked:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 821 | `mcq1000-p821` | Probability T8 — covariance of linear combinations | A, 0 |
| 822 | `mcq1000-p822` | Probability T8 — correlation of linear combinations | D, 0 (none of listed numerical options) |
| 823 | `mcq1000-p823` | Statistical Inference T1 — sufficient statistics in the normal model | D, all four are sufficient |
| 825 | `mcq1000-p825` | Probability T10 — moments and symmetry of a bivariate transformation | A, statements A and C |
| 826 | `mcq1000-p826` | Probability T6 — difference of iid exponential variables | B, statements B and C |
| 827 | `mcq1000-p827` | Probability T1 — order-statistic properties | B, statements A, C and D |
| 828 | `mcq1000-p828` | Probability T5 — Binomial probability ratio | A, decreasing in x |
| 829 | `mcq1000-p829` | Probability T7 — zero variance implication | C, probability 1 |
| 830 | `mcq1000-p830` | Probability T13 — chi-square sampling distribution | C, chi-square with 2 degrees of freedom |

### Page-format notes
- Pages **823, 825, 826 and 827** are represented as multi-select items. Where a source contained fewer than four statements, the repository format was met by explicitly adding mathematically checked statements and identifying the adaptation in the item record/audit.
- Page 827's Beta law was checked from the probability integral transform: (F(X_{(r)})\sim\operatorname{Beta}(r,n-r+1)). The printed option with (r+1) is not correct.

### Page held out
- **Page 824:** the Gamma scale/rate convention is not explicit. The Beta ratio claims require a common rate/scale, which cannot be assumed from the scan alone.

### Updated branch counts
- Probability: **434**
- Statistical Inference: **196**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **8**
- Total: **657 supplementary items** on this branch (71 additions in this batch branch).

The branch remains unmerged and is not a production question count.


## Further verified additions — pages 831–840

Eight further questions were visually transcribed and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 831 | `mcq1000-p831` | Probability T11 — Cauchy stability under addition and scaling | D, (6/[\pi(4+9t^2)]) |
| 832 | `mcq1000-p832` | Probability T1 — minimum order statistic | D, (3ny^2(1-y^3)^{n-1}) |
| 833 | `mcq1000-p833` | Probability T12 — Bayes theorem with two boxes | B, 1/3 |
| 835 | `mcq1000-p835` | Probability T10 — probability integral transform | C, Uniform(0,1) |
| 837 | `mcq1000-p837` | Statistical Inference T4 — MLE with integer parameter space | B, nearest integer to sample mean |
| 838 | `mcq1000-p838` | Statistical Inference T4 — MLE with non-identical normal variances | C, ((1/n)\sum X_k^2/k) |
| 839 | `mcq1000-p839` | Probability T7 — Chebyshev inequality | D, limit 0 |
| 840 | `mcq1000-p840` | Statistical Inference T10 — likelihood-ratio test for coefficient of variation | A, upper-tail residual sum about known mean |

### Pages held out
- **Page 834:** the support boundary in the second branch of the triangular density is visually unclear (it appears as 0 rather than 1). The displayed piecewise function would not integrate to one if read literally; excluded.
- **Page 836:** the claim that equality in distribution of (X+Z) and (Y+Z) forces equality in distribution of (X) and (Y) needs an additional cancellation condition on the distribution of (Z). Finite variance alone does not guarantee a nonvanishing characteristic function. The source's marked answer is therefore not accepted without a stronger assumption.

### Updated branch counts
- Probability: **439**
- Statistical Inference: **199**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **8**
- Total: **665 supplementary items** on this branch (79 additions in this batch branch).

The held-out items are recorded to prevent uncertain source wording or unverified assumptions from entering the learner question bank.


## Further verified additions — pages 841–850

Ten more questions were checked against enlarged page images and solved independently:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 841 | `mcq1000-p841` | Probability T9 — Poisson CLT | C, limit 1/2 |
| 842 | `mcq1000-p842` | Probability T6 — minimum of independent exponentials | D, minimum is exponential |
| 843 | `mcq1000-p843` | Probability T10 — Gamma–Beta transformation and independence | A, statements A, B and C |
| 844 | `mcq1000-p844` | Probability T10 — hazard under transformations | B, statements A and D |
| 845 | `mcq1000-p845` | Statistical Inference T4 — MLE under Uniform location parameter | C, listed values 0.02 and −0.54 |
| 846 | `mcq1000-p846` | Probability T9 — weak law and continuous mapping | C, all four statements |
| 847 | `mcq1000-p847` | Statistical Inference T1 — sufficiency for Bernoulli sample | C, statements C and D |
| 848 | `mcq1000-p848` | Probability T8 — intersection of independently chosen random subsets | C, (inom{n}{m}3^{n-m}/4^n) |
| 849 | `mcq1000-p849` | Probability T10 — geometric probability in a disk | C, 1/4 |
| 850 | `mcq1000-p850` | Probability T10 — product of independent Uniform variables | C, density (-\ln z) on (0,1) |

### Interpretation and format notes
- Page 845 has a non-unique MLE interval ([-0.70,0.04]). Both listed values 0.02 and −0.54 are valid MLEs; the source marks both, and the platform item is multi-select.
- Pages 843, 844, 846 and 847 use the repository's four-statement multi-select contract. Their combination options were standardised to identify the correct sets without changing the underlying claims.
- Page 848 is represented as two independently and uniformly selected subsets, matching the intended random-subset experiment and the provided answer form.

### Updated branch counts
- Probability: **447**
- Statistical Inference: **201**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **8**
- Total: **675 supplementary items** on this branch (89 additions in this batch branch).

All additions remain draft-only pending the latest complete CI run, duplicate reconciliation and content review.


## Further verified additions — pages 851–860

Nine further questions were visually transcribed and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 851 | `mcq1000-p851` | Probability T6 — normal probability over polynomial regions | A, (Phi(1)) |
| 852 | `mcq1000-p852` | Statistical Inference T4 — MLE for a power-density parameter | B, (-n/\sum\ln X_i-1) |
| 853 | `mcq1000-p853` | Probability T12 — Bayes theorem and vaccination | D, 1/9 |
| 854 | `mcq1000-p854` | Probability T4 — Poisson second moment | B, (lambda) |
| 855 | `mcq1000-p855` | Probability T4 — MGF factorisation, mean and variance | D only, variance (233/450) |
| 856 | `mcq1000-p856` | Probability T8 — mutually exclusive event constraints | A, ([-1/3,1/2]) |
| 857 | `mcq1000-p857` | Probability T8 — geometric probability on a line segment | B, 1/2 |
| 859 | `mcq1000-p859` | Probability T10 — area-ratio geometric probability | B, 1/10 |
| 860 | `mcq1000-p860` | Statistical Inference T3 — UMVU via Poisson factorial moments | C, (X(X-1)(X-2)(X-3)(X-4)) |

### Page held out
- **Page 858:** the phrase “a randomly selected chord” does not specify a chord-selection mechanism. This is the Bertrand paradox: different natural random-chord constructions give different probabilities. The marked 1/2 cannot be treated as uniquely determined from the wording, so the item is excluded.

### Updated branch counts
- Probability: **454**
- Statistical Inference: **203**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **8**
- Total: **684 supplementary items** on this branch (98 additions in this batch branch).

Page 855 is represented as multi-select because only its variance statement is true; the MGF was factored into Bernoulli components to verify each claim. These items remain draft-only.
