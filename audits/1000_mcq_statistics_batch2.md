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


## Further verified additions — pages 861–870

Six further questions were transcribed from enlarged page images and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 861 | `mcq1000-p861` | Statistical Inference T4 — exponential-rate MLE | B, statistics A, B and D are not the MLE |
| 862 | `mcq1000-p862` | Statistical Inference T3 — minimum-variance combination of unbiased estimators | C, equal-weight average |
| 863 | `mcq1000-p863` | Statistical Inference T13 — pooled two-sample t confidence interval | B, (−0.20, 1.00) |
| 867 | `mcq1000-p867` | Probability T8 — non-adjacent selection in a row | A, (1-2/n) |
| 868 | `mcq1000-p868` | Probability T6 — symmetry of the logistic distribution | C, odd central moments are zero |
| 870 | `mcq1000-p870` | Probability T2 — conditional bivariate normal distribution | D, (ho=0.8) |

### Pages held out
- **Page 864:** the displayed function (f(x;\theta)=x\exp\{-(x+\theta)\theta^2\}) does not integrate to one as printed; it is not a valid density in the displayed form.
- **Page 865:** the rational/irrational discontinuity question is mathematical analysis rather than a statistics Paper 2 learning objective in the current module scope; not imported into the statistics bank.
- **Page 866:** the two-parameter exponential density and parameter notation are not legible enough to identify the intended parameterisation and moment equations; held.
- **Page 869:** using the supplied chi-square critical values, the 95% interval for the standard deviation is approximately (3.90, 9.33), which does not match any printed option. The marked answer was not copied; held.

### Updated branch counts
- Probability: **457**
- Statistical Inference: **206**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **8**
- Total: **690 supplementary items** on this branch (104 additions in this batch branch).

No question from this range was imported where the source formula was invalid, unreadable or inconsistent with the options.


## Further verified additions — pages 872–880

Nine further questions were checked and solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 872 | `mcq1000-p872` | Probability T8 — volume of a simplex in the unit cube | A, 1/6 |
| 873 | `mcq1000-p873` | Stochastic Processes T6 — gambler's ruin | D, 7/31 |
| 874 | `mcq1000-p874` | Probability T8 — covariance and independence concepts | A, neither statement |
| 875 | `mcq1000-p875` | Probability T8 — variance as covariance | A, Cov(X,X) |
| 876 | `mcq1000-p876` | Probability T10 — fractional part of a Uniform variable | C, Uniform(0,1) |
| 877 | `mcq1000-p877` | Probability T4 — expectation of a Poisson function | D, ((1-e^{-\lambda})/\lambda) |
| 878 | `mcq1000-p878` | Probability T6 — reciprocal moment of a Beta variable | B, none of the listed expressions generally |
| 879 | `mcq1000-p879` | Probability T11 — characteristic function of the Cauchy law | A, Cauchy(0,1) |
| 880 | `mcq1000-p880` | Statistical Inference T5 — consistency via second moments | C, (sqrt{\sum X_i^2/(5n)}) |

### Page held out
- **Page 871:** the displayed function (f(x;\theta)=x\theta^2+x^2) on (0,1) does not integrate to one for general (	heta\in[-1,1]). It is not a valid density as printed; excluded.

### Updated branch counts
- Probability: **464**
- Statistical Inference: **207**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **9**
- Total: **699 supplementary items** on this branch (113 additions in this batch branch).

Page 878's reciprocal Beta moment was not assumed finite for all (p>0): it exists only for (p>1), and then equals ((p+q-1)/(p-1)). This is why the source's listed (q/p) is rejected.


## Further verified additions — pages 882–890

Eight questions were transcribed and independently checked:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 882 | `mcq1000-p882` | Probability T11 — Fourier transform/characteristic function identity | C, (pi e^{-|x|}) |
| 884 | `mcq1000-p884` | Probability T4 — MGF of zero-truncated Poisson | B, ((e^{\lambda e^t}-1)/(e^\lambda-1)) |
| 885 | `mcq1000-p885` | Probability T4 — existence of an MGF | C, does not exist |
| 886 | `mcq1000-p886` | Probability T4 — moment-generating functions | A, both expressions |
| 887 | `mcq1000-p887` | Probability T5 — minimum of independent geometric variables | A, geometric |
| 888 | `mcq1000-p888` | Probability T8 — expectation in sampling without replacement | D, (n(N+1)/2) |
| 889 | `mcq1000-p889` | Probability T8 — variance with finite-population correction | D, (n(N+1)(N-n)/12) |
| 890 | `mcq1000-p890` | Statistical Inference T12 — factors affecting Type II error | C, sample size and test size |

### Pages held out
- **Page 881:** the notation for the requested function (r_2(e^{itx})) is not sufficiently clear to identify whether a characteristic function or another transform is intended. Although the stated factorial moments resemble the standard exponential distribution, the requested quantity is ambiguous.
- **Page 883:** the printed condition (|E(e^{itX})|=5) is impossible for a characteristic function, whose modulus cannot exceed 1. The source expression is likely corrupted; excluded.

### Updated branch counts
- Probability: **471**
- Statistical Inference: **208**
- Regression: **4**
- Multivariate: **15**
- Stochastic: **9**
- Total: **707 supplementary items** on this branch (121 additions in this batch branch).

Pages 888 and 889 are linked: both retain the source's without-replacement sampling setup. The variance solution uses the finite-population correction.


## Further verified additions — pages 891–900

Seven additional questions were visually transcribed and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 891 | `mcq1000-p891` | Probability T1 — ordering of iid continuous variables | B, 1/6 |
| 893 | `mcq1000-p893` | Stochastic Processes T6 — expected waiting time for consecutive heads | A, B and D |
| 896 | `mcq1000-p896` | Probability T10 — products of independent normal variables | B, statements A, B and C |
| 897 | `mcq1000-p897` | Multivariate T2 — validity of a correlation matrix | C, identity matrix |
| 898 | `mcq1000-p898` | Probability T10 — expectation of the standard normal cdf at a normal variable | D, none of A–C |
| 899 | `mcq1000-p899` | Statistical Inference T9 — Neyman–Pearson power | A, 0.0975 |
| 900 | `mcq1000-p900` | Statistical Inference T12 — size and power for a Uniform family | statements A and B, size 0.15 and power 0.68 |

### Source corrections and holds
- **Page 900:** the source's printed answer 0.83 does not follow from the displayed Uniform(θ,θ²) models and rejection region. Direct calculation gives size 0.15 and power 0.68; the item records the correction.
- **Page 892:** the displayed Pareto-like density has support (x>0), on which it is not integrable. A likely (x>1) correction cannot be silently assumed; held.
- **Page 894:** for 10 draws with replacement from 10 values, (P(i\text{ included})=1-0.9^{10}\approx0.6513) and the expected number of distinct values is about 6.513. The printed 0.613 and 6.13 correspond to 9 draws, not 10; held.
- **Page 895:** the random-walk starting position/boundary context needed to define (P_i) is not provided; held.

### Updated branch counts
- Probability: **474**
- Statistical Inference: **210**
- Multivariate: **16**
- Stochastic: **10**
- Regression: **4**
- Total: **714 supplementary items** on this branch (128 additions in this batch branch).

The source's numeric/key discrepancies are documented rather than copied into the learner bank.


## Further verified additions — pages 901–910

Six additional questions were independently solved from enlarged scans:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 901 | `mcq1000-p901` | Probability T4 — second moment of a weighted normal sum | Numeric: 385 |
| 903 | `mcq1000-p903` | Probability T13 — mode of a chi-square distribution | Numeric: 7 |
| 904 | `mcq1000-p904` | Probability T6 — Cauchy moments and covariance existence | Undefined |
| 907 | `mcq1000-p907` | Statistical Inference T13 — shortest confidence interval for shifted exponential location | Numeric: 0.4816 |
| 908 | `mcq1000-p908` | Statistical Inference T9 — Neyman–Pearson power | Numeric: 0.09 (rounded) |
| 910 | `mcq1000-p910` | Statistical Inference T9 — likelihood-ratio critical value for normal means | Numeric: 1.6449 |

### Corrections and exclusions
- **Page 904:** the source answer 0 is not mathematically defined as a covariance. Although sign and magnitude are independent for a symmetric Cauchy variable, (E|Z|=\infty); covariance does not exist. The bank explicitly answers “Undefined”.
- **Page 907:** the shortest 91% interval length is (-\ln(0.09)/5\approx0.4816), not the printed 0.018.
- **Page 908:** size 0.06 gives cutoff (c=0.18); the power is (sqrt{1.18}-1\approx0.0863), which rounds to 0.09, not 0.08.
- **Page 902:** the normal mean notation is not legible enough to determine the intended model and moment equation; held.
- **Pages 905 and 906:** exact duplicates of pages 881 and 899 respectively; excluded.
- **Page 909:** an MSE cannot be computed without specifying the estimator whose MSE is requested; held.

### Updated branch counts
- Probability: **477**
- Statistical Inference: **213**
- Multivariate: **16**
- Stochastic: **10**
- Regression: **4**
- Total: **720 supplementary items** on this branch (134 additions in this batch branch).

Numeric-response items use the repository's numeric format with explicit worked solutions and verification checks.


## Further verified additions — pages 912–919

Six additional questions were checked and solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 912 | `mcq1000-p912` | Statistical Inference T13 — coverage of a shifted-exponential confidence interval | Numeric: 84% |
| 913 | `mcq1000-p913` | Statistical Inference T3 — UMVU estimator for a Poisson functional | Numeric: 8.33 |
| 915 | `mcq1000-p915` | Probability T4 — variance of squared normal observations | Numeric: 6 |
| 916 | `mcq1000-p916` | Probability T6 — normalising a rational density | Numeric: 1.4142 |
| 917 | `mcq1000-p917` | Statistical Inference T4 — consistency of Uniform-family MLE | Numeric: 1 (Yes) |
| 919 | `mcq1000-p919` | Statistical Inference T1 — sufficient statistic for exponential sample | Numeric: 10 |

### Pages held out
- **Page 911:** the two density formulas are corrupted in the scan; the null and alternative models cannot be identified with confidence.
- **Page 914:** the normal model's mean/variance notation and the displayed sum-of-squares divisor are unclear, and the printed interval length does not reconcile with the visible quantities.
- **Page 918:** the event (3\mid |X^2-Y^2|) is shown for positive-integer variables, but no joint distribution or sampling mechanism for X and Y is given; the probability is not determined.
- **Page 920:** the displayed ratio of two independent chi-square(5) variables is not Student-t distributed in the stated form; the claimed t representation is not accepted.

### Updated branch counts
- Probability: **479**
- Statistical Inference: **217**
- Multivariate: **16**
- Stochastic: **10**
- Regression: **4**
- Total: **726 supplementary items** on this branch (140 additions in this batch branch).

Numeric-response items were added with explicit formulas and check steps. No assumptions about missing probability models were supplied for held-out questions.


## Further verified additions — pages 921–929

Eight additional questions were checked from enlarged page images and independently solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 921 | `mcq1000-p921` | Probability T4 — mean from an MGF | Numeric: 2.2 |
| 922 | `mcq1000-p922` | Probability T5 — Binomial MGF and support | Numeric: 1 |
| 923 | `mcq1000-p923` | Probability T4 — Poisson MGF and variance | Numeric: 3.47 |
| 924 | `mcq1000-p924` | Statistical Inference T1 — complete sufficient statistic for discrete Uniform | Numeric: 10 |
| 925 | `mcq1000-p925` | Statistical Inference T4 — exponential scale MLE | Numeric: 2 |
| 926 | `mcq1000-p926` | Probability T8 — strictly increasing outcomes for three dice | Numeric: 0.09 |
| 927 | `mcq1000-p927` | Stochastic Processes T9 — renewal stopping time for Uniform increments | Numeric: (e\approx2.7183) |
| 929 | `mcq1000-p929` | Probability T8 — von Neumann debiasing using a biased coin | Numeric: 2 tosses per pair |

### Corrections and exclusions
- **Page 927:** the source's answer 2 is not the expected total number of samples. The tail-sum formula gives (E(N)=\sum_{n=0}^{\infty}1/n!=e\approx2.7183). The bank corrects the answer.
- **Page 928:** the Bernoulli-generator notation below the question is too corrupted to determine the intended algorithm; held.
- **Page 930:** duplicate of page 872 (three independent Uniform(0,1) variables with sum at most 1); excluded.

### Updated branch counts
- Probability: **484**
- Statistical Inference: **219**
- Multivariate: **16**
- Stochastic: **11**
- Regression: **4**
- Total: **734 supplementary items** on this branch (148 additions in this batch branch).

Page 929's two-toss method is the von Neumann construction: HT and TH have equal probability for any coin bias; identical pairs are discarded and retried.


## Further verified additions — pages 931–940

Nine additional questions were transcribed and solved:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 931 | `mcq1000-p931` | Probability T5 — negative-binomial mean | Numeric: 4 |
| 932 | `mcq1000-p932` | Statistical Inference T12 — size, power and Type II error | Numeric: (alpha+\beta=1/3\approx0.3333) |
| 933 | `mcq1000-p933` | Probability T13 — chi-square distribution with 2 degrees of freedom | Numeric: 4 |
| 934 | `mcq1000-p934` | Statistical Inference T13 — chi-square pivot for exponential rate | Numeric: (K=1/2) |
| 935 | `mcq1000-p935` | Statistical Inference T13 — coverage of shifted-exponential interval | Numeric: (alpha=0.05) |
| 936 | `mcq1000-p936` | Probability T6 — normal standardisation | Numeric: 0.5987 |
| 938 | `mcq1000-p938` | Probability T4 — expectation of a polynomial function | Numeric: 3 |
| 939 | `mcq1000-p939` | Probability T8 — union/complement with independent solvers | Numeric: 0.75 |
| 940 | `mcq1000-p940` | Statistical Inference T4 — Laplace location and scale MLE | Numeric: 2.8 |

### Corrections and holds
- **Page 932:** the source answer 1.16 is inconsistent with the displayed Uniform(θ,θ²) hypotheses and rejection region. Direct calculation gives (alpha=0.25), power (=11/12), (eta=1/12), and (alpha+\beta=1/3).
- **Page 937:** the three students' solving events are not stated to be independent. The displayed answer 7/8 requires independence; held rather than adding that unstated assumption.
- **Page 930:** duplicate of page 872; excluded.
- **Page 928:** notation for the Bernoulli-generator construction is too corrupted to identify the intended procedure; held.

### Updated branch counts
- Probability: **489**
- Statistical Inference: **223**
- Multivariate: **16**
- Stochastic: **11**
- Regression: **4**
- Total: **743 supplementary items** on this branch (157 additions in this batch branch).


## Further verified additions — pages 941–953

Eleven additional questions were checked from enlarged source images:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 941 | `mcq1000-p941` | Statistical Inference T13 — sample range covering a Laplace location | Numeric: (z=30) |
| 942 | `mcq1000-p942` | Probability T13 — chi-square mode | Numeric: 1 |
| 944 | `mcq1000-p944` | Probability T2 — conditional expectation for geometric variables | Numeric: 1.5 |
| 945 | `mcq1000-p945` | Probability T2 — conditional distribution given geometric sum | Numeric: 3 |
| 946 | `mcq1000-p946` | Probability T1 — expected cdf of the sample minimum | Numeric: 0.0476 |
| 947 | `mcq1000-p947` | Probability T4 — Poisson variance from MGF | Numeric: 0.9 |
| 949 | `mcq1000-p949` | Probability T5 — mean of zero-based geometric variable | Numeric: 0.01 |
| 950 | `mcq1000-p950` | Probability T10 — expectation of Φ(X) for a symmetric normal | Numeric: 0.5 |
| 951 | `mcq1000-p951` | Probability T13 — chi-square transform of a Uniform variable | Numeric: 2 degrees of freedom |
| 952 | `mcq1000-p952` | Probability T8 — variance of a normal linear combination | Numeric: 1 |
| 953 | `mcq1000-p953` | Probability T5 — Binomial support from MGF | Numeric: 0 |

### Pages held out
- **Page 943:** the statistic and conditions defining S are too corrupted to identify the intended covariance/correlation problem.
- **Page 948:** the displayed function ((x^3-1)/[(1+x)^5B(3,2)]) is negative for (0<x<1), so it is not a valid density on the stated support (x>0). Excluded.

### Updated branch counts
- Probability: **499**
- Statistical Inference: **224**
- Multivariate: **16**
- Stochastic: **11**
- Regression: **4**
- Total: **754 supplementary items** on this branch (168 additions in this batch branch).

Page 949 uses the geometric distribution on support ({0,1,2,\ldots}), as indicated by the stated memoryless identity; its mean is ((1-p)/p), not (1/p).


## Final remaining-page additions — pages 1012–1044

Eight additional questions were verified from enlarged page images:

| PDF page | Item ID | Topic mapping | Verified answer |
|---|---|---|---|
| 1012 | `mcq1000-p1012` | Statistical Inference T4 — MLE set for Uniform location | C, (T_3) is an MLE |
| 1013 | `mcq1000-p1013` | Statistical Inference T4 — MLE set for shifted Uniform | A, 1.8 lies in the feasible MLE interval |
| 1014 | `mcq1000-p1014` | Statistical Inference T4 — Gamma-shape-2 scale MLE | B, (sum X_i/(2n)) |
| 1015 | `mcq1000-p1015` | Statistical Inference T1 — sufficiency for Uniform(0,θ) | C, maximum sufficient; minimum not |
| 1032 | `mcq1000-p1032` | Statistical Inference T13 — margin of error with known σ | Numeric: 1.3475 |
| 1037 | `mcq1000-p1037` | Probability T13 — continuity correction | B, (P(Y>19.5)) |
| 1039 | `mcq1000-p1039` | Statistical Inference T1 — Bernoulli sufficient statistic | B, (sum X_i) |
| 1044 | `mcq1000-p1044` | Statistical Inference T1 — one-to-one transformations of sufficient statistic | A, statements A, C and D |

### Pages held out
- **Page 1035:** sample-size calculation does not provide a population standard deviation or another variance estimate; the requested sample size is not determined by the visible information.
- **Page 1043:** an F critical value requires a significance level/tail convention as well as the degrees of freedom. Only (n_1,n_2) are shown; held.

### Updated branch counts
- Probability: **500**
- Statistical Inference: **231**
- Multivariate: **16**
- Stochastic: **11**
- Regression: **4**
- Total: **762 supplementary items** on this branch (176 additions in this batch branch).

This completes the page-by-page eligibility pass for the remaining unreviewed 1012–1044 segment. Pages with unreadable, underspecified, invalid or duplicate content remain excluded and documented rather than being forced into the bank.


## Final duplicate reconciliation — batch 2

A normalized-stem comparison across all five supplementary pools found two exact duplicates against the first imported batch:
- Page 837 duplicated page 641 (integer-constrained normal MLE).
- Page 952 duplicated page 265 (variance of a standard-normal linear combination).

The later copies (pages 837 and 952) were removed from batch 2; the first imported items remain. A repeat exact-normalised-stem scan across all five supplementary pools now finds **zero exact stem duplicates** within the combined pools.

### Final corrected batch-2 counts
- Probability: **499**
- Statistical Inference: **230**
- Multivariate: **16**
- Stochastic: **11**
- Regression: **4**
- Total: **760 supplementary items**, including **174 new non-duplicate additions** in batch 2 over the 586-item batch-1 baseline.

This exact-stem reconciliation is not a complete semantic-equivalence audit of every question in every seed file. Similar questions with different formulations or numerical conditions still require reviewer judgment.


## Learn-module coverage check

Every topic ID used by the 760 retained supplementary items exists in the Paper 2 catalog and has a corresponding approved lesson in the production lesson inventory. The MLE topic `inference-t4` is covered by `seed/lesson_mle.json` (rather than a `lesson_t4.json` filename); all other used topics map to their corresponding Probability, Statistical Inference, Multivariate, Stochastic or Regression lesson files. No new lesson was required for the retained batch-2 questions.


## Re-review of previously held pages — page 784

A higher-resolution inspection resolved the earlier transcription concern for page 784. The model is the Laplace location family with unit scale, (f(x;\mu)=\frac12e^{-|x-\mu|}\), with \(\mu\) restricted to the positive integers. For observations 2.2, 2.7, 3.1, 3.8 and 5.6, the unrestricted location MLE is the sample median 3.1. Under the integer restriction, comparing the adjacent candidates gives total absolute deviations 4.6 at \(\mu=3\) and 5.8 at \(\mu=4\), so the constrained MLE is 3 (source option b). Added as `mcq1000-p784`, mapped to Statistical Inference T4 (MLE).

This question is distinct in its integer-constrained Laplace likelihood from the other MLE questions in this pool, although the general median principle overlaps with Laplace-location estimation. It should remain included as a worked application rather than treated as an exact duplicate.

### Updated branch pool counts after p784
- Probability: 499
- Statistical Inference: 231
- Multivariate Analysis: 16
- Stochastic Processes: 11
- Regression: 4
- **Total: 761 supplementary items**

Page 770 was rechecked at higher resolution and is legible, but it asks for the ordinary MLE of the endpoint in Uniform(0,50), namely the sample maximum. It is not added because this is already represented by several Uniform-endpoint MLE/sufficiency questions in the existing supplementary pool; it would add little new practice value. Pages 785, 790 and the other held items remain excluded for the mathematical or source-quality reasons recorded above.


## Re-review of previously omitted page 930

The enlarged page image clearly states that (X_1,X_2,X_3) are iid Uniform(0,1) and asks for (P(X_1+X_2+X_3\le1)). The event is the tetrahedron in the unit cube bounded by the coordinate planes and (x_1+x_2+x_3=1). Its volume is (1/3!=1/6), matching the source's numerical answer 0.17 to two decimal places. Added as `mcq1000-p930`, mapped to Probability T8 (joint probability/independence), with the integral and geometric argument in the explanation.

### Updated branch pool counts after p930
- Probability: 500
- Statistical Inference: 231
- Multivariate Analysis: 16
- Stochastic Processes: 11
- Regression: 4
- **Total: 762 supplementary items**

Page 871 was also rechecked at high resolution. The likelihood ratio is decreasing in (x), so the most powerful region is a lower tail; however, the displayed level (alpha=0.009) gives cutoff (c=\sqrt[3]{0.009}\approx0.208) under the null, which is not among the listed choices. The source-marked cutoff 0.3 has size 0.027, not 0.009. It remains excluded rather than importing an inconsistent answer.


## Source-audit reconciliation — pages 1032, 1039 and 1044

A second high-resolution audit found that the earlier held-out notes for these pages were stale and did not match the committed question records. The following is the authoritative disposition:

- **Page 1032 — retained.** With known population standard deviation \(\sigma=5.5\), sample size \(n=64\), and \(z_{0.975}=1.96\), the 95% margin of error is \(1.96(5.5/\sqrt{64})=1.3475\). The numeric question is valid and remains in the Inference pool.
- **Page 1039 — retained, answer format corrected.** For iid Bernoulli observations, \(\sum X_i\), \(\sum X_i^2\) (identical because \(X_i^2=X_i\)), and \((1/n^2)\sum X_i\) are all sufficient. The product \(\prod X_i\) is not sufficient for general \(n\). The item has been changed from single-choice to multi-select, with B, C and D marked true.
- **Page 1044 — retained as multi-select.** For the Beta(1,θ) density \(f(x;\theta)=\theta x^{\theta-1}\), the likelihood depends on the sample through \(\sum\log X_i\). That statistic and its one-to-one transformations \(n/\sum\log X_i\) and \(-\sum\log X_i\) are all sufficient. The committed item correctly records A, C and D as true. The earlier held-out note claiming that this page was excluded is superseded.

The total count is unchanged by the p1039 format correction. Current branch counts remain Probability 500, Statistical Inference 231, Multivariate 16, Stochastic 11 and Regression 4: **762 supplementary items**. This correction is important because it prevents learners being marked wrong for mathematically equivalent sufficient statistics.


## Further high-resolution review — pages 806–1021

- **Page 1018 — retained and added.** The scan states a geometric sample with observed values (X_k=k), (k=1,\ldots,9). Under the stated support (1,2,\ldots) and success-probability parameterisation (P(X=x)=\theta(1-\theta)^{x-1}), the MLE is \(\hat\theta=n/\sum x_i=9/45=0.2\), matching source option 3. Added as `mcq1000-p1018`, mapped to Statistical Inference T4 (MLE), with the likelihood derivation.
- **Page 1017 — excluded.** For 36 iid symmetric ±1 observations, the sum has mean 0 and variance 36. The CLT standardises the interval [-9,9] to [-1.5,1.5], giving \(2\Phi(1.5)-1\). The printed options use \(\Phi(0.25)\)-based expressions and do not match; the source-marked option is therefore not imported.
- **Page 814 — excluded.** The two Gamma distributions are shown only as “Gamma(n)” and “Gamma(n+0.5)” without a scale/rate parameterisation. The requested expectation of \(\sqrt{XY}\) depends on that missing parameterisation, so the scan does not support a unique answer.
- **Page 836 — held out.** The item asks four claims about \(U=X+Z\), \(V=Y+Z\) when \(X,Y,Z\) are independent and \(U,V\) are identically distributed. The marked claim (A) requires a convolution-cancellation argument not justified by the conditions as printed in the scan; the other claims also have edge cases (degenerate variables) that affect strict correlation statements. It is not safe to encode the marked key without clarifying assumptions.
- **Pages 806, 870, 911 and 920 — held out.** Their scans have missing or unclear mathematical notation/conditioning (page 870's conditional event and page 911's density notation are especially difficult to distinguish). No answer was added from an uncertain transcription.
- **Pages 809, 824, 1019 and 1021 — held out pending independent reconstruction.** The visible formulas are incomplete or parameterisation-dependent in the scan; they need a cleaner source or a fully unambiguous transcription before inclusion.

After adding page 1018, current branch counts are Probability 500, Statistical Inference 232, Multivariate Analysis 16, Stochastic Processes 11 and Regression 4: **763 supplementary items**. The p930 numeric item now explicitly carries an empty `options` array to satisfy the common question-item contract (numeric write-in items still retain their separate `check` field).


### Resolution of two additional held pages

- **Page 920 — excluded after full-resolution derivation.** The scan gives independent \(X_1,X_2\sim\chi^2_5\) and asks for the Student-t degrees of freedom of \(T=\sqrt5(X_1-X_2)/\sqrt{X_1X_2}\). Since \(F=X_1/X_2\sim F_{5,5}\), the transformation \(T=\sqrt5(\sqrt F-1/\sqrt F)\) has the distribution of \(2t_5\), not a standard \(t_k\) for any degrees of freedom. The source's numeric key 5 therefore does not match the statistic as printed.
- **Page 1019 — excluded after full-resolution derivation.** The scan specifies \(X_i\sim\mathrm{Beta}(8,12)\), \(Y_i=X_i^2/(1-X_i)^2\), and \(E(Y_i)=36/55\). Direct beta-integral calculations give \(E(Y_i^2)=1\), hence \(\operatorname{Var}(Y_i)=1729/3025\). Therefore the CLT scale is \(\alpha^2=1729/3025\), so the asked quantity \(55\alpha^2=1729/55\). The printed choices are sums of cubes equal to 1729, not 1729/55; the source key is inconsistent.
- **Page 824 — excluded.** The upper portion of the scanned question, containing the distributions and parameter definitions for \(x,y,z\), is clipped. The marked options cannot be independently established from the visible portion.

These exclusions are deliberate quality controls: they avoid encoding a source key that conflicts with the formula as printed.


### Additional source-key checks

- **Page 809 — excluded.** The displayed point probabilities sum to \(\theta+2/45\), not 1 for general \(\theta\). Thus the displayed function is not a pmf as claimed (except at one isolated parameter value); the source's “not a pmf” key is consistent.
- **Page 870 — excluded.** The scan asks \(P(4<Y<16\mid X<5)\) for a bivariate normal with \(\mu_X=5,\mu_Y=10,\sigma_X=1,\sigma_Y=5\). By the symmetry \((X-5,Y-10)\mapsto (-(X-5),-(Y-10))\), the conditional probability is independent of positive \(\rho\) and equals \(P(-1.2<Z<1.2)\approx0.7699\), not the printed 0.954. The source-marked \(\rho=0.8\) is unsupported.


## Additional source pages reviewed — pages 30, 32, 71, 78 and 96

Five further questions were added after inspecting the source scans at high resolution and independently deriving their answers:

- **Page 30 — Statistical Inference T3 (method of moments).** For probabilities \(P(X=1)=\theta\), \(P(X=2)=\theta\), \(P(X=3)=1-2\theta\), the first moment is \(E(X)=3-3\theta\), giving \(\hat\theta=(3-\bar X)/3\). Added as `mcq1000-p030`.
- **Page 32 — Probability T1 (variance lower bound).** At least probability 0.5 lies at distance at least 3 from the mean 10, so \(\operatorname{Var}(X)=E[(X-10)^2]\ge9(0.5)=9/2\). Added as `mcq1000-p032`.
- **Page 71 — Multivariate T1 (inverse covariance matrix).** Applied the 2×2 inverse formula to the covariance matrix \(\begin{pmatrix}\sigma_{11}&\sigma_{12}\\\sigma_{12}&\sigma_{22}\end{pmatrix}\), with determinant \(\sigma_{11}\sigma_{22}-\sigma_{12}^2\). Added as `mcq1000-p071`.
- **Page 78 — Probability T4 (law of total variance).** For the given density, \(E(X)=2/\sqrt\pi\) and \(E(X^2)=3/2\). Therefore \(\operatorname{Var}(Y)=E[4X^2+3]+4\operatorname{Var}(X)=15-16/\pi\). Added as `mcq1000-p078`.
- **Page 96 — Multivariate T1 (bivariate normal sign probability).** Using \(P(XY>0)=1/2+\arcsin(\rho)/\pi\), obtain \(\rho=\cos(\pi(1-p))\). Added as `mcq1000-p096`.

Current branch counts after these additions: Probability 502, Statistical Inference 233, Multivariate Analysis 18, Stochastic Processes 11, Regression 4 — **768 supplementary items**. All five additions include worked derivations and are mapped to existing Paper 2 lesson topics.


## Further verified probability questions — pages 115, 120, 121 and 143

- **Page 115 — convergence concepts.** Almost-sure convergence is equivalent to the event \(\{\omega:X_n(\omega)\to X(\omega)\}\) having probability one. Convergence in probability is a weaker condition; the two probability-limit expressions in the scan do not characterise almost-sure convergence. Added as `mcq1000-p115`.
- **Page 120, question 2 — probability axioms.** Both 0 and 1 are valid event probabilities, whereas −0.5 is not. Added as multi-select `mcq1000-p120-q2`.
- **Page 120, question 3 — Bertrand's paradox.** The result depends on the procedure used to choose a random chord; the source key says at least three different valid results. Added as `mcq1000-p120-q3`.
- **Page 121, question 5 — complement rule.** If \(P(A)=0.6\), then \(P(A^c)=0.4\), so the stated pair 0.6 and 0.5 is impossible. Added as `mcq1000-p121-q5`.
- **Page 143 — normal sampling distribution.** For \(\bar X\) from \(N(28.3,2.3^2)\) with \(n=10\), standardising 27 gives \(z\approx-1.79\). The two equivalent expressions \(\Phi(-1.79)\) and \(1-\Phi(1.79)\) are both retained as correct. Added as `mcq1000-p143`.

Page 121, question 4 was deliberately excluded: the source gives \(P(A)=0.3\), \(P(A\cup B)=0.1\), and \(P(A\cap B)=0.5\), which violates \(P(A\cap B)\le P(A\cup B)\). The supplied answer key cannot repair an internally impossible probability specification.

Updated branch counts: Probability 507, Statistical Inference 233, Multivariate Analysis 18, Stochastic Processes 11, Regression 4 — **773 supplementary items**. The batch-2 branch now contributes 187 items over the 586-item batch-1 baseline.


### Topic-to-lesson mapping verification

The new questions were checked against the actual lesson seed `topicId` values and corrected to their matching existing Paper 2 lessons: page 30 → `inference-t5` (Method of Moments); page 32 → `probability-t7` (inequalities); page 78 → `probability-t3` (conditional expectation/total variance); page 115 → `probability-t9` (convergence and limit laws); pages 120 Q2 and 121 Q5 → `probability-t12` (probability axioms/complement rule); page 120 Q3 → `probability-t8` (random chord selection/independence foundations); page 143 → `probability-t13` (sampling distributions); pages 71 and 96 → `multivariate-t1`. This replaces provisional topic tags where necessary; no new lesson seed was required.


## Further source pages reviewed — pages 134, 137, 277, 278, 293 and 299

- **Page 134 — excluded.** The statement gives the marginal distribution \(P(X_n=\pm n^\lambda)=1/2\) but does not state independence or another dependence condition. The strong law conclusion cannot be inferred from the marginals alone; the source key \(\lambda<1/2\) would require additional assumptions.
- **Page 137 — excluded.** The source key says WLLN holds if \(\lambda>0\), but the displayed covariance structure \(\operatorname{Cov}(X_i,X_j)=\lambda\) for adjacent indices and zero otherwise does not justify that restriction. For any admissible covariance parameter, the variance of the sample mean is of order \(1/n\); negative as well as positive admissible adjacent covariance values can satisfy the WLLN. The keyed condition is therefore not correct as printed.
- **Page 277 — retained.** For \(X\sim U(\pi/6,\pi/2)\), \(\cos X>\sin X\) exactly on \((\pi/6,\pi/4)\), giving probability \((\pi/12)/(\pi/3)=1/4\). Added as `mcq1000-p277`.
- **Page 278 — retained.** For iid exponential observations with mean \(\theta\), each listed weighted estimator is unbiased and has variance \(\theta^2\sum w_i^2\). The equal-weight sample mean has the smallest sum of squared weights, \(1/3\), and hence the smallest variance. Added as `mcq1000-p278`.
- **Page 293 — retained with an explicit dependence caveat.** The marginals give \(E(X_n^2)=1/n\to0\), so convergence in second mean holds; they also give convergence in distribution to 0. Almost-sure convergence cannot be inferred without specifying dependence across n. The item is encoded to ask which claims must hold from the given marginals alone. Added as `mcq1000-p293`.
- **Page 299 — retained.** The sum of two independent Uniform(0,1) variables has triangular density \(g(z)=z\) on \(0<z<1\), \(g(z)=2-z\) on \(1<z<2\), and zero elsewhere. Added as `mcq1000-p299`.

Updated branch counts: Probability 510, Statistical Inference 234, Multivariate Analysis 18, Stochastic Processes 11, Regression 4 — **777 supplementary items**. Batch 2 contributes 191 items over the 586-item batch-1 baseline.


## Additional review — pages 314, 321–345 and 367

- **Page 314 — excluded.** For \(X\sim U(\pi/6,\pi/4)\), \(\cos X>\sin X\) throughout the interval except at the endpoint, so the probability is 1. None of the printed options (2/3, 1/2, 1/3, 1/4) is correct.
- **Page 321 — excluded.** The source defines \(s^2=(1/10)\sum_{i=1}^{10}(y_i-\bar y)^2\) and population variance \(\sigma^2=(1/100)\sum_{i=1}^{100}(Y_i-\bar Y)^2\). Under SRSWOR, \(E(s^2)=(10/11)\sigma^2\), so the unbiased estimator of \(\sigma^2\) is \((11/10)s^2\). That factor is absent from the printed options.
- **Page 333 — excluded.** The question asks for the sampling distribution of \(S^2\) from a population specified only by its mean and variance. The chi-square result requires a normal population, which is not stated.
- **Page 334 — retained.** For 100 independent normal expenses with mean 4,000 and standard deviation 500, the sum has mean 400,000 and standard deviation 5,000. Thus \(P(S<407500)=\Phi(1.5)=0.93319\). Added as `mcq1000-p334`.
- **Page 344 — not added as a separate item.** It is another normal-sample-mean probability question of the same form as page 143; it is treated as a close practice variant rather than counted as a new concept item.
- **Page 345 — excluded.** The displayed piecewise density integrates to less than one as printed, so it is not a valid pdf and the conditional probability options do not follow from a valid model.
- **Page 367 — excluded pending clarification.** The strict event \(50<S_n<80\) for \(S_n\sim\operatorname{Poisson}(64)\) does not agree with the listed approximate values under the usual normal approximation with continuity correction. The answer key/rounding convention is not sufficiently reliable to import.

Current branch counts: Probability 511, Statistical Inference 234, Multivariate Analysis 18, Stochastic Processes 11, Regression 4 — **778 supplementary items**. Batch 2 now contributes 192 items over the 586-item batch-1 baseline.


## Further source pages reviewed — pages 410–500

- **Page 410 — retained.** Under \(H_0:p=0.5\), the number of heads in 100 independent tosses is \(N\sim\operatorname{Bin}(100,0.5)\). Exact upper-tail probabilities give \(P(N\ge58)\approx0.0666\) and \(P(N\ge59)\approx0.0443\); hence the 5% critical region is \(N>58\). Added as `mcq1000-p410`.
- **Page 434 — retained.** The six paired measurements lie almost exactly on a positively sloped straight line, so the sample correlation is almost +1. Added as `mcq1000-p434`.
- **Page 444 — retained.** From \(E(T)=\theta\) and \(\operatorname{Var}(T)=\theta^2+\theta\), obtain \(E[T(T-1)/2]=\theta^2\). Added as `mcq1000-p444`.
- **Page 452 — excluded.** “Sum of squares of all deviations” is ambiguous about whether deviations are from zero or from the sample mean; the available options correspond to different conventions.
- **Page 468 — retained.** For independent standard normal variables, \(\operatorname{Cov}(X_1+X_2+X_3,X_1-X_2)=\operatorname{Var}(X_1)-\operatorname{Var}(X_2)=0\). Added as `mcq1000-p468`.
- **Page 477 — retained.** With iid observations of mean 2 and variance 4, the weak law gives \(\bar X_n\to2\), the weak law applied to \(X_i^2\) gives \(n^{-1}\sum X_i^2\to8\), and the CLT gives \(\sqrt n(\bar X_n-2)/2\Rightarrow N(0,1)\). Added as multi-select `mcq1000-p477`.
- **Page 481 — not added.** The order-statistic notation in the scanned options is partially corrupted, so the exact claims cannot be transcribed reliably.
- **Page 495 — excluded.** More than one listed estimator is not unbiased for \(\theta\) under \(U(0,\theta)\), although the source asks for a single answer.
- **Page 498 — retained.** For the two unbiased linear estimators from iid \(N(\theta,1)\) observations, the variances are \(3/8\) and \(1/3\), so the defined relative efficiency is \(8/9\). Added as `mcq1000-p498`.
- **Page 499 — retained.** For two independent exponential component lifetimes in a series system, reliability at time t is \(e^{-2\lambda t}\); substituting \(\hat\lambda=1/\bar X\) gives \(e^{-2t/\bar X}\). Added as `mcq1000-p499`.
- **Page 500 — retained.** For a normal sample, \(\sqrt n(\bar X-\mu)/S\) follows Student's t with \(n-1\) degrees of freedom. Added as `mcq1000-p500`.

Current branch counts: Probability 514, Statistical Inference 238, Multivariate Analysis 19, Stochastic Processes 11, Regression 4 — **786 supplementary items**. Batch 2 contributes 200 items over the 586-item batch-1 baseline.


## Further source pages reviewed — pages 502–559

- **Page 502 — excluded.** The source repeats the same proposition for options C and D (“Z and W are independent”), leaving duplicated answer choices and no well-formed single-answer item.
- **Page 508 — excluded.** With known standard deviation 2, the requested 95% precision of 0.1 requires a sample size around 1,537, which is not among the options 25, 30, 40 and 50.
- **Page 513 — retained.** For iid Poisson(λ), \(E[(-1)^X]=e^{-2\lambda}\); the sample average is unbiased and consistent. Conditioning \((-1)^{X_1}\) on the complete sufficient statistic \(T=\sum X_i\) gives \((1-2/n)^T\), the UMVU estimator, which is also consistent. Added as multi-select `mcq1000-p513`.
- **Page 517 — retained.** Since \(\bar X\sim N(\theta,\sigma^2/n)\), the normal MGF gives \(E[e^{2\bar X}]=e^{2\theta+2\sigma^2/n}\). Thus \(e^{2\bar X-2\sigma^2/n}\) is unbiased and, by completeness and sufficiency, UMVU. Added as `mcq1000-p517`.
- **Page 518 — retained.** For the normal likelihood and normal prior under squared-error loss, the posterior mean is \(n\sigma^2\bar X/(1+n\sigma^2)\). Added as `mcq1000-p518`.
- **Page 529 — retained.** Integrating the conditional density \(6x(y-x)y^{-3}\) over \(0\le x\le y\) gives \(E(X\mid Y=y)=y/2\). Added as `mcq1000-p529`.
- **Page 536 — retained.** Positive scaling and location shifts leave correlation unchanged, so the transformed variables retain correlation 1/2. Added as `mcq1000-p536`.
- **Page 541 — retained.** For iid Uniform(−1,2), the sample mean tends to 1/2, not 0; the even/odd subsequence average difference tends to zero; the sample supremum and infimum tend to the support endpoints 2 and −1 almost surely. Added as multi-select `mcq1000-p541`.
- **Page 544 — retained.** With independent normal variables of mean 2 and variance 5, the sample mean tends to 2, the average square tends to 9, its squared sample mean tends to 4, and \(\sum(X_i/n)^2\to0\). Added as multi-select `mcq1000-p544`.
- **Page 546 — retained.** The independent, bounded, zero-mean sequence satisfies \(\operatorname{Var}(Y_n)\le1/n\to0\) and Kolmogorov's strong-law condition \(\sum_i\operatorname{Var}(X_i)/i^2<\infty\), so \(Y_n\to0\) almost surely. Added as `mcq1000-p546`.
- **Page 559 — retained.** The numerator is independent of the sample standard deviation from the first 99 observations; the resulting pivot has a Student t distribution with 98 degrees of freedom. Added as `mcq1000-p559`.

Updated branch counts: Probability 519, Statistical Inference 241, Multivariate Analysis 20, Stochastic Processes 11, Regression 4 — **795 supplementary items**. Batch 2 contributes 209 items over the 586-item batch-1 baseline.


## Further source pages reviewed — pages 617–655

- **Page 617 — retained.** For \(X\sim U(0,\theta)\), the rule rejects when \(X>0.5\). Under \(H_0:\theta=1\), size is 0.5; under \(H_1:\theta=2\), power is 0.75. Added as `mcq1000-p617`.
- **Page 621 — excluded.** The joint-density formula and normalising constant are not legible enough to independently verify the requested order probability.
- **Page 624 — retained with option normalisation.** For a normal sample with unknown variance, \(\bar X^2-S^2/n\) is unbiased for \(\mu^2\), but that expression is not among the source choices. The source's “none of the above” is retained. The source contains five choices; the app's four-option format was respected by removing the separate “does not exist” distractor and retaining the none-of-listed-expressions response. Added as `mcq1000-p624`.
- **Page 626 — excluded.** The multinomial likelihood gives \(\hat\theta=1/15\), so the estimated proportion with two cars is \(2/15\), which is not among the visible options.
- **Page 637 — retained.** The joint likelihood for independent \(X\sim N(0,\sigma^2)\) and \(Y\sim\operatorname{Exp}(\text{mean }2\sigma^2)\) depends on \(X^2+Y\) through a monotone likelihood ratio. The UMP test rejects for large \(X^2+Y\). Added as `mcq1000-p637`.
- **Page 655 — retained.** Uniform sampling from the triangle \(x\ge0,y\ge0,x+y\le\theta\) gives likelihood proportional to \(\theta^{-2n}\) on \(\theta\ge\max_i(X_i+Y_i)\). Hence \(\hat\theta=\max_i(X_i+Y_i)\). Added as multi-select `mcq1000-p655`.

Updated branch counts: Probability 519, Statistical Inference 245, Multivariate Analysis 20, Stochastic Processes 11, Regression 4 — **799 supplementary items**. Batch 2 contributes 213 items over the 586-item batch-1 baseline.


## Further source pages reviewed — pages 706–800

- **Page 706 — excluded.** The variance parameter in the displayed binomial question is clipped, so the binomial parameter and requested probability cannot be recovered reliably.
- **Page 707 — excluded.** The two missing cards' suits/ranks are unspecified; the probability of drawing a spade depends on which cards are missing.
- **Page 713 — retained.** For \(X\sim\operatorname{Bin}(5,p)\), \(np+np(1-p)=1.8\) gives \(p=0.2\). Hence \(P(X=2)=\binom52(0.2)^2(0.8)^3=0.2048\). Added as `mcq1000-p713`.
- **Page 714 — excluded.** The wording conflates the chance of making a 7-point shot with expected points per attempt; the source's expected-value target is not sufficiently clear.
- **Page 715 — excluded.** The payout wording does not specify how the overlapping events (a king of hearts or queen of spades) are paid, so a unique fair entry amount cannot be determined.
- **Page 727 — excluded.** The two grade probabilities are unreadable in the scan.
- **Page 733 — held out.** The systematic-sampling design and intra-class correlation description do not provide enough detail to derive the claimed relative efficiency without additional assumptions about the population ordering.
- **Page 737 — not added.** It restates the almost-sure convergence event definition already added from page 115.
- **Page 741 — excluded.** The type-I error is \(e^{-2}\), while the type-II error under \(\theta=2\theta_0\) is \(1-e^{-4}\). None of the printed options gives this pair; the source choices omit the required leading 1−.
- **Page 764 — retained.** For Uniform(0,θ), \(\operatorname{Var}(2\bar X)=\theta^2/(3n)\) and \(\operatorname{Var}(((n+1)/n)X_{(n)})=\theta^2/[n(n+2)]\). The defined relative efficiency is \(3/(n+2)\). Added as `mcq1000-p764`.
- **Page 770 — not added.** The Uniform(0,θ) endpoint MLE is already represented several times in the bank; this adds no distinct practice value.
- **Page 800 — held out.** Several listed convergence statements are true simultaneously for iid normal observations, but the scan presents a single-choice format. It is not safe to preserve the source's single-answer structure.

Updated branch counts: Probability 520, Statistical Inference 246, Multivariate Analysis 20, Stochastic Processes 11, Regression 4 — **801 supplementary items**. Batch 2 contributes 215 items over the 586-item batch-1 baseline.


## Further source pages reviewed — pages 806–895

- **Pages 806, 808 and 809 — excluded.** Page 806 has a clipped/illegible probability expression; page 808 does not clearly specify whether the two lifespan events are independent; page 809's displayed mass function does not normalise to one for general parameter values.
- **Page 814 — excluded.** The Gamma parameterisation is not specified, so the requested expectation depends on an unstated scale/rate convention.
- **Page 819 — excluded.** The distributional symbols in the premise are unreadable.
- **Page 824 — excluded.** The Gamma shape parameters and Beta parameter labels are clipped/illegible, preventing a reliable transcription.
- **Page 834 — retained.** Under H₀ the density is Uniform(0,1); under H₁ the triangular density is \(g(t)=t\) on \([0,1]\) and \(g(t)=2-t\) on \((1,2]\). The most powerful size-0.1 test rejects on the alternative-only support \((1,2]\) and on \((0.9,1]\), giving power \(0.595\). Added as `mcq1000-p834`.
- **Page 836 — held out.** The equality in distribution of \(X+Z\) and \(Y+Z\) does not by itself make the printed claims safe without checking convolution-cancellation and degenerate edge cases. No source key was imported.
- **Page 837 — not added.** It is an exact duplicate of the already retained integer-constrained normal-mean MLE question from page 641.
- **Page 858 — excluded.** The probability for a “random chord” depends on the chord-selection mechanism, which is not specified.
- **Pages 864 and 866 — held out.** Page 864's density is too poorly rendered to recover the exponent and support reliably; page 866's two-parameter exponential parameterisation and moment notation are ambiguous in the scan.
- **Page 865 — excluded from this statistics bank.** It is a real-analysis continuity question rather than a Statistics Paper 2 probability/inference item.
- **Page 869 — excluded.** The stated chi-square quantiles and sample standard deviation produce confidence limits that do not match the printed answer choices.
- **Page 871 — excluded.** The level \(\alpha=0.009\) gives the cutoff \(c=\sqrt[3]{0.009}\approx0.208\), not the source-marked 0.3.
- **Pages 881, 883, 892, 894 and 895 — held out.** The moment notation, transformed-distribution expression, sampling-with-replacement wording and random-walk setup are incomplete or ambiguous in the scanned pages.

Updated branch counts: Probability 520, Statistical Inference 247, Multivariate Analysis 20, Stochastic Processes 11, Regression 4 — **802 supplementary items**. Batch 2 contributes 216 items over the 586-item batch-1 baseline.


## Final source-page checks — pages 902–928

- **Page 906 — retained.** For \(f_0(x)=1\) and \(f_1(x)=2x\) on (0,1), the likelihood ratio increases in x. A size-0.05 most powerful test rejects for \(x>0.95\); its power is \(\int_{0.95}^1 2x\,dx=0.0975\). Added as numeric item `mcq1000-p906`.
- **Page 902 — held out.** The estimator expression and target parameter are clipped.
- **Page 905 — held out.** The requested transform/moment expression is not legible enough to reconstruct.
- **Page 909 — held out.** The Bernoulli parameter interval and proposed estimator are clipped.
- **Page 911 — excluded.** The displayed density/parameter specification is not clear enough to calculate the MP-test power safely; the nearby page 906 question is separately legible and was added.
- **Page 914 — excluded.** The displayed sample-variance divisor and supplied t-quantile do not yield the source's reported interval length under the standard two-sided t interval.
- **Page 918 — held out.** The distributional assumptions for X and Y are missing from the scan.
- **Page 920 — excluded earlier.** The transformed chi-square ratio does not have the claimed standard Student-t distribution.

Updated branch counts: Probability 520, Statistical Inference 248, Multivariate Analysis 20, Stochastic Processes 11, Regression 4 — **803 supplementary items**. Batch 2 contributes 217 items over the 586-item batch-1 baseline.


## Additional source pages reviewed — pages 459, 462, 481 and 487–489

- **Page 459 — retained.** By exchangeability of three iid Uniform(0,1) variables, the three expected ratios \(E[X_i/(X_1+X_2+X_3)]\) are equal and sum to 1, so each is 1/3. Added as `mcq1000-p459`.
- **Page 462 — retained.** For iid standard normals, the first term has zero expectation by sign symmetry in X and the second by exchange symmetry of X and Y. Added as `mcq1000-p462`.
- **Page 481 — retained with a correction to the source claim.** The transformed order statistic \(F(X_{(r)})\) has Beta(r,n−r+1), not Beta(r+1,n−r+1); distinct order statistics are dependent, and the expected difference is (r−s)/(n+1). Added as multi-select `mcq1000-p481`, marking A and C true.
- **Page 487 — retained.** For the negative-binomial convention counting trials to obtain r successes, \(E(X)=r/p\); at r=2,p=1/2 the answer is 4. Added as numeric item `mcq1000-p487`.
- **Page 489 — retained.** For the exponential scale model, the MLE is the sample mean; the observed sample {1,2,3} gives 2, which satisfies the positive-integer restriction. Added as numeric item `mcq1000-p489`.

Updated branch counts: Probability 523, Statistical Inference 249, Multivariate Analysis 21, Stochastic Processes 11, Regression 4 — **808 supplementary items**. Batch 2 contributes 222 items over the 586-item batch-1 baseline.


## Source pages 928–953: additional audit pass

This pass rechecked the high-resolution scans and reconciled them against existing question IDs before adding anything:

- **Page 932 — retained in the existing pool.** For \(X\sim U(\theta,\theta^2)\), \(\theta\in\{2,3\}\), the critical region \(X\ge3.5\) gives size \(\alpha=1/4\), power \(\beta=11/12\), and \(\alpha+\beta=7/6\). The existing item `mcq1000-p932` had a stale answer value; it was corrected from 0.3333 to \(7/6\).
- **Page 933 — already present.** The sum of squares of two independent standard normals is \(\chi^2_2\); the source equation gives p=4. Existing item `mcq1000-p933` was confirmed.
- **Page 935 — already present.** The shifted-exponential confidence interval has coverage \(1-\alpha\); 95% coverage gives \(\alpha=0.05\). Existing item `mcq1000-p935` was confirmed.
- **Page 936 — already present.** Standardisation gives \(P(X\le3)=\Phi(0.25)=0.5987\). Existing item `mcq1000-p936` was confirmed.
- **Page 937 — excluded.** The source does not state that the three students' attempts are independent. The marked answer requires that assumption, so it was not imported.
- **Page 938 — already present.** Direct integration gives \(E[(2X+1)^2]=3\). Existing item `mcq1000-p938` was confirmed.
- **Page 939 — already present.** The source explicitly states independence; the probability at least one student solves the problem is \(1-(1/2)(2/3)(3/4)=3/4\). Existing item `mcq1000-p939` was confirmed.
- **Page 940 — already present.** The Laplace MLE of scale is the mean absolute deviation about a sample median; the estimate is 2.8. Existing item `mcq1000-p940` was confirmed.
- **Page 941 — already present.** For 31 iid Laplace observations centred at θ, the interval between the minimum and maximum has coverage \(1-2^{-30}\), so z=30. Existing item `mcq1000-p941` was confirmed.
- **Page 942 — already present.** The mode of \(\chi^2_3\) is 1. Existing item `mcq1000-p942` was confirmed.
- **Page 943 — excluded.** The estimator/statistic notation is corrupted and the stated variance bound is not sufficient to identify the requested correlation.
- **Page 944 — already present.** Conditional on the sum of two iid geometric variables being 3, the two possible ordered pairs are equally likely; the conditional mean is 1.5. Existing item `mcq1000-p944` was confirmed.
- **Page 945 — already present.** Conditional on the sum being 4, the three ordered pairs are equiprobable, giving y=3. Existing item `mcq1000-p945` was confirmed.
- **Page 946 — already present.** The probability integral transform gives \(E[F(X_{(1)})]=1/21\) for n=20 (approximately 0.05). Existing item `mcq1000-p946` was confirmed.
- **Page 947 — already present.** The MGF is Poisson(0.9), so the variance is 0.9. Existing item `mcq1000-p947` was confirmed.
- **Page 948 — excluded.** The scanned numerator/exponent in the density is not sufficiently clear to identify the distribution without guessing.
- **Page 949 — excluded.** The displayed memoryless identity has an off-by-one issue for the stated geometric support \(\{1,2,\ldots\}\).
- **Page 950 — already present.** Symmetry gives \(E[\Phi(X)]=1/2\) for a zero-centred normal X. Existing item `mcq1000-p950` was confirmed.
- **Page 951 — already present.** For X uniform on (0,1), \(-2\ln X\sim\chi^2_2\). Existing item `mcq1000-p951` was confirmed.
- **Page 952 — added.** For independent standard normals, \(\operatorname{Var}((X_1+X_2-2X_3)/\sqrt6)=1\). Added as `mcq1000-p952`.
- **Page 953 — already present.** The MGF is Binomial(10,0.57), so \(P(X>10)=0\). Existing item `mcq1000-p953` was confirmed.

The page 932 answer correction and page 952 addition bring the branch to Probability 523, Statistical Inference 249, Multivariate Analysis 22, Stochastic Processes 11 and Regression 4 — **809 supplementary items**.


## Remaining scan checks from pages 928–953 and page 1043

- **Page 928 — excluded.** The prompt about generating a standard normal value using a Bernoulli-trial generator is corrupted in the key mathematical notation; the claimed construction cannot be reconstructed safely.
- **Page 929 — already present.** The two-toss von Neumann procedure gives an unbiased binary choice from a biased coin because \(P(HT)=P(TH)=p(1-p)\). Existing item `mcq1000-p929` was confirmed.
- **Page 933 — already present.** The chi-square calculation was reconciled with item `mcq1000-p933`.
- **Page 952 — retained in the multivariate pool.** Item `mcq1000-p952` records the variance of a linear combination of three independent standard normal variables.
- **Page 1043 — excluded.** The F-critical-value question gives only sample sizes \(n_1=10,n_2=14\) but omits the significance level (and tail convention). An F critical value cannot be determined uniquely from the degrees of freedom alone.

The audit does not force the remaining gap to 1,000 with unclear or under-specified questions. All exclusions above remain out of the learner-facing pools.


## Pool-to-topic consistency correction

A final topic-prefix audit found one cross-module mismatch: `mcq1000-p103` was stored in the Statistical Inference supplementary pool but tagged `probability-t3`. Because it asks for a conditional expectation under independent binomial sampling, it belongs in the Probability pool. The item was moved without changing its ID, wording, answer or explanation.

Updated counts: Statistical Inference 248; Probability 524; Multivariate Analysis 22; Stochastic Processes 11; Regression 4 — **809 total**. All supplementary item topic prefixes now match their owning module pool.


## Duplicate-stem reconciliation across all five supplementary pools

A final exact normalised-stem scan across all five supplementary pools found three duplicate pairs:

- `mcq1000-p277` duplicated `mcq1000-p576` (uniform trigonometric probability).
- `mcq1000-p459` duplicated `mcq1000-p805` (exchangeable Uniform ratio expectation).
- `mcq1000-p477` duplicated `mcq1000-p476` (iid mean/variance, WLLN and CLT statements).

The later duplicate entries p277, p459 and p477 were removed; the earlier entries were retained. This is in addition to the prior exact-duplicate reconciliation recorded for the two batch-1 overlaps. A near-duplicate comparison against the current inference, probability and multivariate PYQ-variant pools and the June 2026 full-paper bank found no high-overlap stem candidates at the tested 0.65 token-Jaccard threshold; this is a screening check, not a full semantic proof.

Reconciled pool counts: Statistical Inference 248, Probability 521, Multivariate Analysis 22, Stochastic Processes 11 and Regression 4 — **806 total supplementary items**. The batch-2 additions now stand at 220 over the 586-item batch-1 baseline; 194 remain to reach the 1,000-item target.


### Correction to the pool-to-topic note above

The page 103 item was restored to its original Statistical Inference pool because its question ID already exists in the batch-1 base branch and the repository's ID-stability contract prohibits moving an existing question between pool files (it would orphan saved learner attempts). Its topic tag is now `inference-t3`, retaining the original pool file and stable ID. The corrected counts are Statistical Inference 249 and Probability 520; total remains **806**. This supersedes the earlier statement that the item was moved into the Probability pool.


## Early-source review — pages 3–37

The original scan was reopened and selected unbanked pages were independently checked. Seven useful items were retained:

- **Page 10 — retained as multi-select.** Function A integrates to 1/2 and is not normalised; function C integrates to 1 but becomes negative at x=2. Function B is a valid density. Added as `mcq1000-p010`.
- **Page 15 — retained as multi-select.** Under the likelihood factorisation for a sufficient statistic, an existing MLE can be selected as a function of T; the standard identity \(\operatorname{MSE}=\operatorname{Bias}^2+\operatorname{Var}\) is also true. Added as `mcq1000-p015`.
- **Page 25 — retained as multi-select.** With standard normal marginals, either joint normality plus zero covariance (established by the stated linear-combination variance condition) or joint-MGF factorisation implies independence. Zero covariance alone and a single quadrant probability do not. Added as `mcq1000-p025`.
- **Page 28 — retained as multi-select.** For a bivariate normal pair, zero correlation is equivalent to independence; normal marginals alone do not force a bivariate-normal joint distribution, and zero correlation outside joint normality need not imply independence. Added as `mcq1000-p028`.
- **Page 33 — retained as multi-select.** For independent standard normals, \(\sqrt{X_1^2+X_2^2}\) is Rayleigh(1), while \(X_1/X_2\) is standard Cauchy. Added as `mcq1000-p033`.
- **Page 36 — retained as multi-select.** For the centred Laplace scale model, the MLE is the mean absolute deviation from zero and the method-of-moments estimator is \(\sqrt{\sum X_i^2/(2n)}\). Added as `mcq1000-p036`.
- **Page 37 — retained as multi-select.** If X~Uniform(−1,1) and Y=e^X, then Y has support (e⁻¹,e), density 1/(2y), and cdf (1+ln y)/2 on that interval. Added as `mcq1000-p037`.

Pages 6, 11, 14, 20, 23, 26 and 31 were not imported: the source wording/notation is incomplete, an option set is inconsistent, or the claimed answer is not uniquely supported. Page 32 duplicates the already included variance lower-bound question.

Updated counts: Probability 522, Statistical Inference 251, Multivariate Analysis 25, Stochastic Processes 11, Regression 4 — **813 total supplementary items**. Batch 2 contributes 227 over the 586-item baseline.


## Additional early-source review — pages 39–59

- **Page 39 — retained as multi-select.** For independent iid exponential sequences with rates 1 and 4, \(Z_i=X_i-3Y_i\) has mean \(1-3/4=1/4\). The strong law gives \(\sum_{i=1}^n Z_i\to+\infty\) almost surely; both positive and negative values of a single \(Z_i\) have positive probability. Added as `mcq1000-p039`.
- **Page 42 — retained as multi-select.** The mixture of rate-1 and rate-2 exponentials has constant hazard at the pure-component endpoints p=0 or 1 and a decreasing hazard for 0<p<1. Added as `mcq1000-p042`.
- **Page 43 — retained.** For the exponential rate parameterisation \(f(x)=\sigma e^{-\sigma x}\), the mean is 1/σ; variance is 1/σ² and the MGF is \(1/(1-t/\sigma)\). Added as `mcq1000-p043`.
- **Page 49 — retained as multi-select.** For a continuous random variable, endpoint probabilities vanish, so including or excluding a or b does not change interval probabilities. The repeated source equality was replaced by a “none of A–C” statement so the four-statement item has no duplicated assertion. Added as `mcq1000-p049`.
- **Page 50 — retained as multi-select.** Mutual independence implies A is independent of B∩C and B∪C, and Aᶜ and Bᶜ are independent. Added as `mcq1000-p050`.
- **Page 57 — retained.** For the normal family \(N(\alpha\sigma,\sigma^2)\) with known α, the likelihood depends on the sample through \((\sum X_i,\sum X_i^2)\), establishing sufficiency; a non-degenerate scale-invariant function of this statistic shows it is not complete. Added as `mcq1000-p057`.
- **Page 59 — retained.** UMVU implies unbiasedness, but unbiasedness alone does not imply UMVU; adding an arbitrary function does not preserve unbiasedness. Added as `mcq1000-p059`.

Pages 41 and 53 repeat previously included monotone-likelihood-ratio and joint-normal independence material; page 51 repeats the earlier incomplete joint-density question; page 52 repeats the Uniform-to-exponential transformation; page 55's Poisson formula options are too poorly rendered to classify safely; page 72's “incorrect statements” prompt appears to have all four statements true under the standard assumptions, so it was not imported.

Updated counts: Probability 527, Statistical Inference 253, Multivariate Analysis 25, Stochastic Processes 11, Regression 4 — **820 total supplementary items**. Batch 2 contributes 234 over the 586-item baseline.


## Early-source review — pages 85–173

- **Page 85 — retained.** For a sample from Uniform(θ−1,θ+1), the likelihood support is determined by both sample extremes, so \((X_{(1)},X_{(n)})\) is sufficient for θ. Added as `mcq1000-p085`.
- **Page 86 — held out.** The transition labels in the Markov-chain diagram are not sufficiently clear to reconstruct a stochastic transition matrix with confidence.
- **Page 87 — excluded.** The stated rejection region is central around the null value, but the question's test-size interpretation and notation are not clear enough to derive a unique answer from the scan.
- **Page 88 — excluded.** Direct normalisation and integration of the displayed joint density do not reproduce any of the listed probability options.
- **Page 94 — held out.** The integral defining the chi-square cdf and the subsequent inequality are not legible enough to identify the exact claim.
- **Page 97 — excluded.** For known variance 16 and a 90% normal confidence interval with half-width 1, the required minimum sample size is \(n\ge(1.645\cdot4)^2\), i.e. 44; that value is absent from the options 40, 50, 42 and 55.
- **Page 102 — held out.** The ratio expression's absolute-value/denominator notation is too blurred to determine the exact distributional transform.
- **Page 150 — excluded.** The covariance matrix following the multivariate-normal mean vector is missing from the scan, so the independence selections cannot be determined.
- **Pages 171–173 — excluded.** Page 171's numerator and denominator sums overlap and the sample's stated index range is inconsistent; pages 172–173 have a clipped weighted-statistic definition, so the requested variance cannot be recovered safely.

Updated counts: Probability 527, Statistical Inference 254, Multivariate Analysis 25, Stochastic Processes 11, Regression 4 — **821 total supplementary items**. Batch 2 contributes 235 over the 586-item baseline.


## Further early-source review — pages 177–199

- **Page 177 — excluded.** The displayed ratio uses overlapping sums of exponential observations; the claimed F distribution cannot follow from a constant multiple of that ratio because the numerator and denominator are not independent chi-square sums.
- **Page 184 — held out.** The role of d and n in the Pareto density/estimator expression is not defined clearly enough to select a unique answer.
- **Page 187 — excluded.** The Bernoulli variable Y is not defined as a function of the sample, so its success probability cannot be determined from the stated iid Bernoulli observations alone.
- **Page 195 — retained.** For \(f(x)=c(1+x^2)^{-2}\), symmetry gives mean zero; normalisation gives c=2/π and the second moment is 1, so the variance is 1. Added as `mcq1000-p195`.
- **Page 196 — retained.** If \(f_X(x)=\alpha x^{\alpha-1}\) on (0,1), then \(X^\alpha\sim U(0,1)\), so \(-2\alpha\ln X\sim\chi^2_2\). Added as `mcq1000-p196`.
- **Page 197 — excluded.** The displayed density \(2x/a\) on (0,a) integrates to a, so normalisation would force a=1, which is absent from the options.
- **Page 199 — excluded from the Statistics Paper 2 question bank.** It is a matrix-determinant algebra question rather than a statistics question.

Updated counts: Probability 529, Statistical Inference 254, Multivariate Analysis 25, Stochastic Processes 11, Regression 4 — **822 total supplementary items**. Batch 2 contributes 236 over the 586-item baseline.


## Further early-source review — pages 247–397

- **Page 247 — retained.** For X~Poisson(λ), \(E[1/(1+X)]=(1-e^{-\lambda})/\lambda\), obtained by shifting the Poisson series. Added as `mcq1000-p247`.
- **Page 253 — held out.** The confidence-interval expression depends on the source's chi-square quantile convention, which is not specified in the scan. The maximum/minimum unbiasedness statements were not accepted from the marked key without that convention.
- **Page 261 — held out.** The notation in the estimator/correlation question is too corrupted to reconstruct.
- **Page 263 — excluded.** The stated geometric memoryless identity has an off-by-one error for support \(\{1,2,\ldots\}\).
- **Page 274 — retained.** The MGF \((5+e^t)^3/216\) identifies Binomial(3,1/6), so \(P(X>1)=2/27\). Added as `mcq1000-p274`.
- **Page 275 — retained.** Direct integration of the two pieces of the density gives \(P(1/2<X<2)=15/16\). Added as `mcq1000-p275`.
- **Page 283 — retained.** The transformation \(U=X^2\) gives Gamma(4,1), so \(2X^2\sim\chi^2_8\). Added as `mcq1000-p283`.
- **Page 295 — retained.** The marginal density of X is \((1+x)^{-2}\), and the conditional density of Y given X=x is Gamma(shape 2, scale 1+x), giving \(E(Y\mid X=x)=2(1+x)\). Added as `mcq1000-p295`.
- **Page 296 — retained as multi-select.** For joint density x+y on the unit square, \(E(X\mid Y=y)=(1/3+y/2)/(1/2+y)\). The correct values are 7/12 at y=1/2 and 11/18 at y=1/4; the other two source statements are incorrect. Added as `mcq1000-p296`.
- **Page 304 — excluded.** Normalisation and the stated mean give α=3, β=−4, making the alleged density negative on part of (0,1); the source options therefore do not define a valid pdf.
- **Page 309 — held out.** The Gamma parameterisation is not sufficiently clear to identify the method-of-moments estimator without assuming a shape/rate convention.
- **Page 322 — retained.** Independent negative-binomial variables with a common success probability add to another negative-binomial variable; the geometric distribution is the r=1 special case. Added as `mcq1000-p322`.
- **Pages 333, 344, 345, 362, 367, 393 and 397 — excluded or held out.** Page 333 omits normality for the chi-square sampling result; page 344 duplicates an existing normal-sample-mean item; page 345's displayed density is not normalised; page 362 is a cover; page 367's Poisson/normal approximation does not match the listed options; page 393's transform is incomplete; and page 397's LLN condition is not legible enough to identify the exact expression.

Updated counts: Probability 536, Statistical Inference 254, Multivariate Analysis 25, Stochastic Processes 11, Regression 4 — **830 total supplementary items**. Batch 2 contributes 244 over the 586-item baseline.


### Additional page 305 check

- **Page 305 — retained.** For a normal sample with known mean μ and unknown variance σ², maximising the likelihood gives \(\hat\sigma^2=n^{-1}\sum(X_i-\mu)^2\). The divisor n−1 is not the MLE in this known-mean setting. Added as `mcq1000-p305`.

Updated counts: Probability 536, Statistical Inference 255, Multivariate Analysis 25, Stochastic Processes 11, Regression 4 — **831 total supplementary items**. Batch 2 contributes 245 over the 586-item baseline.


### Duplicate reconciliation — page 247

A full normalized-stem scan found that page 247 duplicates the Poisson reciprocal-expectation question already present as `mcq1000-p877`. The later duplicate `mcq1000-p247` was removed; the earlier page-877 item is retained. The corrected pool count is Probability 535 and **830 total supplementary items** (244 batch-2 additions over the 586-item baseline).


## Additional source review — pages 420–482

Seventeen independently checked items were retained:

- **Page 420 — retained as multi-select.** For independent symmetric variables with \(P(X_n=\pm n)=1/(n^2+1)\), the variance is bounded by 2 and \(\sum\operatorname{Var}(X_n)/n^2<\infty\). Kolmogorov's strong law gives \(S_n/n\to0\) almost surely; the mean is also zero. Added as `mcq1000-p420`.
- **Page 427 — retained as multi-select.** For the simple hypotheses Uniform(0,1) versus density 6x(1−x), the level-α most powerful region is the central interval \(((1-\alpha)/2,(1+\alpha)/2)\); its power is \(3\alpha/2-\alpha^3/2>\alpha\). Added as `mcq1000-p427`.
- **Page 428 — retained as multi-select.** For a shifted exponential sample, the likelihood depends on the sample through its minimum and sum; the stated range and scaled mean-minus-minimum properties were derived. Added as `mcq1000-p428`.
- **Page 431 — retained as multi-select.** The symmetric density \((15/4)x^2(1-x^2)\) has mean and median zero and variance 3/7. Added as `mcq1000-p431`.
- **Page 433 — retained.** A density proportional to x⁴ on (−3,3) is symmetric, so its expectation is zero. Added as `mcq1000-p433`.
- **Page 435 — retained.** For an exponential distribution with mean λ, \(E(X^2)=2\lambda^2\); hence the average of squared observations divided by 2 is unbiased for λ². Added as `mcq1000-p435`.
- **Page 436 — retained.** The two-observation likelihoods are 0.09 under θ₀ and 0.15 under θ₁, so the MLE is θ₁. Added as `mcq1000-p436`.
- **Page 440 — retained.** For an exponential(rate θ) density, \(E(X)=1/\theta\), so \(f(E(X))=\theta/e\). Added as `mcq1000-p440`.
- **Page 448 — retained.** For the geometric distribution on {0,1,…}, memorylessness gives \(P(X=11\mid X>10)=1/3\). Added as `mcq1000-p448`.
- **Page 451 — retained.** For Poisson(λ), \(E[X(X-1)]=\lambda^2\); the sample average of \(X_i(X_i-1)\) is unbiased for λ². Added as `mcq1000-p451`.
- **Page 455 — retained.** Powers of 7 modulo 5 have period four; four of the 16 equally likely residue pairs make the sum divisible by 5, giving probability 1/4. Added as `mcq1000-p455`.
- **Page 456 — retained.** Five dice summing to 7 correspond to 15 nonnegative integer compositions of 2, giving probability \(15/6^5\). Added as `mcq1000-p456`.
- **Page 457 — retained.** The two marginal probabilities do not determine the intersection; the Fréchet bounds give \(31/40\le P(A\cap B)\le7/8\). Added as `mcq1000-p457`.
- **Page 475 — retained as multi-select.** Conditional on the total successes, two independent binomial counts with common p yield a hypergeometric conditional distribution with the standard mean and variance. Added as `mcq1000-p475`.
- **Page 478 — retained as multi-select with the common-rate assumption made explicit.** Independent Gamma variables with common rate add to Gamma, and their ratios to sums have Beta distributions. Added as `mcq1000-p478`.
- **Page 479 — retained as multi-select.** For independent standard normals, the transformed variable has finite variance and is negative with probability 1/2; both compared expectations in the source are zero. Added as `mcq1000-p479`.
- **Page 482 — retained.** For Binomial(n,p), the adjacent-pmf ratio \(P(X=x)/P(X=x-1)=((n-x+1)/x)(p/(1-p))\) decreases in x. Added as `mcq1000-p482`.

Pages 418 (near-duplicate of the existing uniform-extremes sufficiency item), 430 (printed power options do not match the derived result), 452 (ambiguous deviation convention), 454 (non-statistics betting puzzle), 460 (pmf parameter normalisation is inconsistent), 463 (Gamma parameterisation omitted), 464 (duplicates the existing exponential one-sided interval), 466 (the “minimal length” convention is not specified), and 472/474 (the distribution labels are corrupted) were not imported.

Updated counts: Probability 547, Statistical Inference 260, Multivariate Analysis 25, Stochastic Processes 11, Regression 4 — **847 total supplementary items**. Batch 2 contributes 261 over the 586-item baseline.


## Final focused review of source pages 928–953

- **Page 928 — not imported.** This asks whether a computer-programmed Bernoulli generator can produce a Normal(0,1) value. It is a software/tooling question rather than a suitable standalone Statistics Paper 2 MCQ in this question bank.
- **Page 929 — retained earlier.** The two-toss procedure for selecting between two items with equal probability, regardless of coin bias, is already represented as `mcq1000-p929`.
- **Page 930 — retained earlier.** The simplex probability for three independent Uniform(0,1) variables is already represented as `mcq1000-p930`.
- **Page 931 — retained earlier.** The negative-binomial mean under the trials-until-r-successes parameterisation is already represented as `mcq1000-p931`.
- **Pages 932–942 — relevant questions already represented.** These include the discrete test size/power calculation, chi-square transformation, exponential confidence-limit/pivot items, normal probability, expectation from a density, independent-student probability, Laplace scale MLE, Laplace extreme-order-statistic coverage and chi-square mode.
- **Page 937 — excluded.** The printed question gives individual success/failure probabilities and the overall probability of solving, but does not state that the students' attempts are independent. The keyed answer 7/8 requires that additional assumption, so it is not imported as written.
- **Page 943 — excluded.** The scan states only that an estimator-like statistic has expectation g(λ), with g odd and finite variance, and that S has mean zero and finite variance. It does not supply the covariance or a definition of S sufficient to determine the requested correlation.
- **Page 948 — excluded.** The displayed expression \((x^3-1)/[(1+x)^5B(3,2)]\) is negative for 0<x<1 and therefore is not a valid probability density as printed. The transformation answer cannot be accepted without correcting the source.
- **Pages 944–947 and 949–951 — retained earlier.** The conditional geometric calculations, probability integral transform for the sample minimum, Poisson MGF, geometric memorylessness, symmetry expectation and chi-square transformation are already represented.
- **Page 952 — retained.** For three independent standard normals, the variance of \((X_1+X_2-2X_3)/\sqrt6\) is 1. The verified item is `mcq1000-p952` in the Multivariate Analysis pool.
- **Page 953 — retained earlier.** The binomial MGF question has support 0,…,10, so \(P(X>10)=0\); already represented as `mcq1000-p953`.

The focused review added no further items because the remaining potentially relevant pages were already present or had missing assumptions/invalid source expressions. Current verified counts remain Probability 547, Statistical Inference 260, Multivariate Analysis 25, Stochastic Processes 11 and Regression 4 — **847 supplementary items** (261 in batch 2 over the 586-item batch-1 baseline).
