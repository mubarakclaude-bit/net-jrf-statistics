# Sampling Theory mathematical audit — 2026-11-14

## Scope and base

- Paper 2 only; Sampling Theory (Unit III-A), catalog topics `sampling-t1` through `sampling-t9`.
- Base: `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`.
- Reviewed all nine lesson JSON files and all nine 20-item mastery pools (180 questions), focusing on numerical scenes, formula statements, single-answer keys, numeric answers and multi-statement verdicts.
- Inspected existing topic verifiers: `verify_sampling.py` (T1), `verify_sampling_t4.py`, `verify_sampling_t7.py` and `verify_sampling_t9.py`. The content map did not list T9's verifier because its filename does not identify the topic in the map's matching logic.
- This is a scoped mathematical audit, not certification of every prose statement, every reference or every possible sampling design.

## Confirmed finding

### ST-001 — Murthy n=2 variance-estimator factor is wrong

**Files:** `seed/lesson_sampling_t9.json` scene `s10`; `seed/sampling_t9_mastery.json` item `sampling-t9-m20`.

The lesson and mastery item used

`(1-p_1)(1-p_2)(p_1+p_2)/(2-p_1-p_2)^2`

as the coefficient in Murthy's unbiased variance estimator for a two-unit PPSWOR sample. The correct factor is

`(1-p_1)(1-p_2)(1-p_1-p_2)/(2-p_1-p_2)^2`.

The standard expression is given in Singh and Mangat, *Elements of Survey Sampling*, Chapter 4, §4.8, equation (4.26). The source gives the variance estimator as the product of `(1-p_1)(1-p_2)(1-p_1-p_2)`, divided by `(2-p_1-p_2)^2`, times the squared difference of inverse-probability values.

The old example used `p_1=0.2` and `p_2=0.3`, for which `p_1+p_2=1-p_1-p_2=0.5`; the incorrect expression therefore produced the same numeric result. The lesson transfer and mastery item now use `p_1=0.2`, `p_2=0.4`, where the factors differ.

Exact recomputation:
- For the mastery item, inverse-weighted values 50 and 40: correct variance estimate `480/49 ≈ 9.7959`; the old factor would give `720/49 ≈ 14.6939`.
- For the lesson transfer, inverse-weighted values 50 and 30: Murthy estimate `270/7 ≈ 38.5714`; variance estimate `1920/49 ≈ 39.1837`.

The existing `verify_sampling_t9.py` has been strengthened with exact `Fraction` arithmetic, an asymmetric regression case, and assertions that the corrected learner-facing text and pool item match the formula.

## Other coverage notes

- T1–T9 pools contain 20 items each (180 total); all nine meet the repository's minimum answer-letter spread.
- Recomputed representative numerical scenes and numeric pool items across HT, stratified allocation, ratio/regression, cluster, systematic, PPSWR/HH, multistage/two-phase, survey errors, and variance estimators.
- The official June 2026 anchors are Q8 (HT estimator) and Q36 (NSSO sampling design). The official paper key in `seed/pyq_j26_full.json` records Q8=C and Q36=D; topic mapping and variant banks were checked for scope and consistency.
- No other confirmed mathematical defect is included in this PR.

## Changes

- Corrected the Murthy variance-estimator factor in T9's worked transfer and mastery item.
- Changed T9 lesson version from 1.1 to 1.2 and recorded the correction in provenance.
- Strengthened `verify_sampling_t9.py` with exact arithmetic and content assertions.
- Added this audit report.

## Boundaries

No catalog, shared manifest, application code, workflows, Paper 1, other modules, Claude artifacts, databases or infrastructure changed. No merge or deployment is authorised by this audit; keep the PR draft pending independent review and owner approval.
