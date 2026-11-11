# Sampling Theory — evidence map and release trace (Paper 2, Unit III-A)

Status: **content packages authored and internally audited; GitHub Actions validation is pending on the release branch.** This is not a production claim. Production status begins only after merge to `main`; Vercel deployment is tracked separately.

## Scope and package inventory

All nine official syllabus topics are included. Each topic has a lesson seed, 20-item mastery pool, deterministic authoring/serialization entry point, independent numerical verifier, and topic-specific verification report.

| Topic | Lesson | Mastery pool | Authoring | Verifier | Report |
|---|---|---|---|---|---|
| sampling-t1 — Horvitz–Thompson and varying probability sampling | `seed/lesson_sampling_t1.json` | `seed/sampling_t1_mastery.json` | `lesson_sampling_t1.py` | `verify_sampling.py` | `reports/sampling_t1_verification_report.md` |
| sampling-t2 — Stratified sampling and allocation | `seed/lesson_sampling_t2.json` | `seed/sampling_t2_mastery.json` | `lesson_sampling_t2.py` | `verify_sampling_t2.py` | `reports/sampling_t2_verification_report.md` |
| sampling-t3 — Ratio and regression estimators | `seed/lesson_sampling_t3.json` | `seed/sampling_t3_mastery.json` | `lesson_sampling_t3.py` | `verify_sampling_t3.py` | `reports/sampling_t3_verification_report.md` |
| sampling-t4 — Cluster sampling | `seed/lesson_sampling_t4.json` | `seed/sampling_t4_mastery.json` | `lesson_sampling_t4.py` | `verify_sampling_t4.py` | `reports/sampling_t4_verification_report.md` |
| sampling-t5 — Systematic sampling | `seed/lesson_sampling_t5.json` | `seed/sampling_t5_mastery.json` | `lesson_sampling_t5.py` | `verify_sampling_t5.py` | `reports/sampling_t5_verification_report.md` |
| sampling-t6 — PPS schemes and their estimators | `seed/lesson_sampling_t6.json` | `seed/sampling_t6_mastery.json` | `lesson_sampling_t6.py` | `verify_sampling_t6.py` | `reports/sampling_t6_verification_report.md` |
| sampling-t7 — Two-stage, multi-stage and double sampling | `seed/lesson_sampling_t7.json` | `seed/sampling_t7_mastery.json` | `lesson_sampling_t7.py` | `verify_sampling_t7.py` | `reports/sampling_t7_verification_report.md` |
| sampling-t8 — Non-sampling errors | `seed/lesson_sampling_t8.json` | `seed/sampling_t8_mastery.json` | `lesson_sampling_t8.py` | `verify_sampling_t8.py` | `reports/sampling_t8_verification_report.md` |
| sampling-t9 — Nonnegative variance estimation, ordered and unordered estimators | `seed/lesson_sampling_t9.json` | `seed/sampling_t9_mastery.json` | `lesson_sampling_t9.py` | `verify_sampling_t9.py` | `reports/sampling_t9_verification_report.md` |

## Structural audit

- 9 lesson packages and 9 mastery pools.
- 180 mastery questions total; each pool is intended to follow the 6 easy / 10 moderate / 4 hard contract.
- 117 unique scene IDs; each lesson has 13 scenes, five objectives, three prerequisites, two guided scenes, a quiz scene wired to its corresponding pool, a flow diagram, and two substantial scenarios.
- Topic and module identifiers are paired consistently (`sampling-t1` … `sampling-t9`, module `sampling`).
- No hand-maintained `seed/meta_lessons.json` edit is made; generated seed tooling remains the index owner.
- Authored practice prompts and mastery questions are not labelled as official PYQs.

## Official PYQ trace

The two exact official-paper anchors are retained from `seed/pyq_j26_full.json` and are separately classified in `seed/sampling_question_bank.json`.

| Source ID | Paper | Question | Topic | Official key | Candidate response |
|---|---:|---:|---|---|---|
| j26-q08 | June 2026 Paper 2 | Q8 | sampling-t1 | C (B and C only) | D |
| j26-q36 | June 2026 Paper 2 | Q36 | sampling-t4 / sampling-t7 | D (stratified multi-stage) | B |

## Mathematical review boundaries

1. HT: indicator-variable proof of design unbiasedness; positive first-order inclusion probabilities; second-order probabilities and zero-pair edge case.
2. Stratification: independent stratum samples, finite-population corrections, proportional and Neyman allocation.
3. Ratio/regression: distinguish exact unbiasedness from approximate bias/variance; state known auxiliary-total/mean assumptions.
4. Cluster: derive under the stated one- or two-stage design; do not treat design-effect approximations as universal identities.
5. Systematic: state random-start and frame ordering; do not promise a general variance estimator from one random start.
6. PPS: distinguish draw probabilities from final inclusion probabilities; distinguish Hansen–Hurwitz from HT.
7. Multi-stage/double sampling: multiply conditional stage probabilities only for nested stages; keep two-phase auxiliary-data designs distinct.
8. Non-sampling errors: separate coverage, nonresponse, measurement, response and processing mechanisms; larger n does not remove systematic error.
9. Variance estimators: distinguish nonnegative true variance, possibly negative unbiased estimates, and conditions for nonnegative SYG/ordered/unordered forms.

## References

- Cochran, W. G. *Sampling Techniques*, 3rd ed. (1977).
- Lohr, S. L. *Sampling: Design and Analysis*, 2nd ed. (2010).
- Horvitz, D. G. and Thompson, D. J. (1952), “A Generalization of Sampling Without Replacement from a Finite Universe,” *JASA*, 47(260), 663–685.
- Hansen, M. H. and Hurwitz, W. N. (1943), “On the Theory of Sampling from Finite Populations,” *Annals of Mathematical Statistics*, 14(4), 333–362.

## Validation and release gate

The topic verifier scripts use exact rational arithmetic for their numerical examples. Their execution against the final release branch is **not yet confirmed**. The current-head `Validate` workflow must complete its `validate`, `browser`, and `acceptance` jobs successfully before this PR is marked ready for review. Do not count these topics as production until merged into `main`. Vercel deployment is deliberately out of scope.
