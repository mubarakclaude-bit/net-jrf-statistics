# Sampling Theory — evidence map (Paper 2, Unit 3A)

Status: authoring baseline; not a finished lesson package.

## Scope and official catalog mapping

| Topic ID | Catalog title | Coverage boundary |
|---|---|---|
| sampling-t1 | Horvitz–Thompson and varying probability sampling | First- and second-order inclusion probabilities, HT total/mean, design unbiasedness, variance estimation |
| sampling-t2 | Stratified sampling and allocation | Stratified estimators, within-stratum variance, proportional and Neyman allocation |
| sampling-t3 | Ratio and regression estimators | Auxiliary-variable estimation, ratio/regression forms, bias and approximate variance |
| sampling-t4 | Cluster sampling | One-/two-stage cluster designs, intracluster similarity, design effect |
| sampling-t5 | Systematic sampling | Random start, interval, periodicity, variance estimation limits |
| sampling-t6 | PPS schemes and their estimators | PPS with/without replacement, Hansen–Hurwitz and HT distinction |
| sampling-t7 | Two-stage, multi-stage and double sampling | Nested stages versus two-phase auxiliary-data designs |
| sampling-t8 | Non-sampling errors | Coverage, nonresponse, measurement, response and processing errors |
| sampling-t9 | Nonnegative variance estimation, ordered and unordered estimators | Estimator ordering/invariance and distinction between true variance and unbiased estimator |

## Official PYQ trace

The two questions below are exact official-paper anchors already present in `seed/pyq_j26_full.json`. They are not newly generated practice questions.

| Source ID | Paper | Question | Assigned scope | Official key | Candidate response |
|---|---:|---:|---|---|---|
| j26-q08 | June 2026 Paper 2 | Q8 | sampling-t1 | C (B and C only) | D |
| j26-q36 | June 2026 Paper 2 | Q36 | sampling-t4 / sampling-t7 | D (stratified multi-stage) | B |

The repository's full response-sheet explanation is retained in `seed/pyq_j26_full.json`. The structured transcription is in `seed/sampling_question_bank.json`.

## Core mathematical evidence to verify in lesson packages

1. Horvitz–Thompson: with fixed finite-population values and inclusion indicators, prove (E_p(\hat Y_{HT})=Y) from (E_p(I_i)=\pi_i). Require positive first-order inclusion probabilities.
2. Stratification: derive (hat Y_{st}=\sum_h N_h\bar y_h) and the SRSWOR variance using independent stratum samples. Check finite-population corrections.
3. Ratio/regression: distinguish exact unbiasedness from approximate bias/variance statements. State the auxiliary total/mean known assumption explicitly.
4. Cluster: calculate the variance under a clearly stated cluster design; do not apply a design-effect approximation as an exact identity outside its assumptions.
5. Systematic: state the frame ordering and random-start mechanism. Do not claim a general unbiased variance estimator from a single random start.
6. PPS: distinguish selection probabilities at draw level from unit inclusion probabilities; distinguish Hansen–Hurwitz (with replacement) from Horvitz–Thompson (without replacement / inclusion-probability form).
7. Multi-stage: derive the product of conditional stage probabilities for a unit's overall inclusion probability. Keep two-phase sampling distinct from two-stage sampling.
8. Non-sampling errors: map each error to its mechanism and a design/fieldwork control; do not imply a larger sample removes systematic measurement or coverage error.
9. Variance estimators: distinguish the nonnegative true variance from an unbiased estimator that may be negative for a realised sample under some designs. Verify any ordered/unordered terminology against the cited estimator definition before teaching it.

## Reference spine

- Cochran, W. G. *Sampling Techniques*, 3rd ed. (1977): stratified, ratio, cluster, systematic and unequal-probability sampling.
- Lohr, S. L. *Sampling: Design and Analysis*, 2nd ed. (2010): design-based estimation and complex designs.
- Horvitz, D. G. and Thompson, D. J. (1952), “A Generalization of Sampling Without Replacement from a Finite Universe,” *Journal of the American Statistical Association*, 47(260), 663–685.
- Hansen, M. H. and Hurwitz, W. N. (1943), “On the Theory of Sampling from Finite Populations,” *Annals of Mathematical Statistics*, 14(4), 333–362.

## Quality boundary

The 54 short prompts in `seed/sampling_question_bank.json` are author-created revision prompts. They are not official PYQs and do not yet constitute the 20-item mastery pool required for each lesson. Each finished topic package still needs its own 20-item pool, lesson JSON, authoring script, independent numerical verifier, and verification report.