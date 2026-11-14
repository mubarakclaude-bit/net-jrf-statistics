# Design of Experiments mathematical audit — 2026-11-14

## Scope and baseline

- Paper 2 only — Design of Experiments, topics `design-t1` through `design-t8`.
- Baseline: `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`.
- Reviewed all eight lesson JSON files and all eight mastery pools (160 questions).
- Checked pool structure: each topic has 20 items, the expected easy/moderate/hard split (6/10/4), and A/B/C/D key counts of 5 each. Independently reconciled multi-statement verdicts against the keyed option for all multi-select items.
- Recomputed representative calculations for CRD/RBD/Latin-square ANOVA, factorial effects and sums of squares, BIBD identities, block-confounding counts, missing-value estimators and connectedness rank.
- This is a scoped mathematical audit, not certification of every theoretical statement, reference or possible experimental design.

## Confirmed finding

### DOE-001 — Latin-square single-missing-value estimator has an unstated p=2 boundary

**Files:** `seed/lesson_design_t7.json`, theory scene `s4`; `seed/design_t7_mastery.json`, items `design-t7-m-05` and `design-t7-m-14`.

The classical one-missing-value estimator for a Latin square is

`x̂=[p(R+C+T)−2G]/[(p−1)(p−2)]`

and the ordinary Latin-square error degrees of freedom are also `(p−1)(p−2)`.

The lesson gave the estimator without stating its domain. At `p=2`, both denominator and error df are zero. A 2×2 Latin square is saturated under the additive row/column/treatment model; with one observation missing, the missing value cannot be recovered by this classical estimator. The formula therefore requires `p≥3`.

The lesson now states this boundary explicitly. The related mastery explanations clarify the condition and distinguish the valid p=3 worked example from the degenerate p=2 case. The existing `verify_design_t7.py` now checks the boundary algebraically and asserts that the learner-facing lesson and mastery explanation preserve it.

## Cross-topic checks and non-findings

- **T1 CRD/RBD:** recomputed the worked CRD and RBD sums of squares, degrees of freedom and treatment F statistics; the exact decompositions and keys reconcile.
- **T2 CRD/RBD/Latin square:** recomputed the worked operator-block RBD and 3×3 Latin-square ANOVA; source sums of squares and F statistics reconcile.
- **T3 factorial designs:** recomputed the 2² marginal effects, interaction contrast, replicated ANOVA decomposition and error degrees of freedom.
- **T4 BIBD:** checked `bk=vr`, `λ(v−1)=r(k−1)`, incidence-matrix row/column sums and `NN′=(r−λ)I+λJ` for the worked example. The lesson correctly distinguishes necessary conditions from an existence proof.
- **T5 principles:** checked the distinction between genuine independent replication, chance allocation and local control; no confirmed mathematical defect.
- **T6 confounding/split-plot/PBIBD:** checked block counts, the ABC aliasing example, whole-plot versus subplot error strata and class-specific concurrence; no confirmed mathematical defect.
- **T8 connectedness/orthogonality:** checked rank(C)=v−1 for connectedness, rank(C)=v−c for c components, and the distinction between connectedness and pair balance; no confirmed mathematical defect.
- No answer-key changes were required in the 160 mastery items. All multi-statement keys matched their item verdicts.

## Changes in this PR

- Added the p≥3 condition to the T7 Latin-square missing-value theory.
- Clarified the related mastery explanations.
- Extended the existing T7 verifier with exact denominator/error-df boundary assertions.
- Updated the T7 evidence map.

## Boundaries

Only T7 lesson/pool explanations, the T7 verifier, the T7 evidence map and this audit report are changed. No catalog, shared manifest, application code, workflows, Paper 1, other modules, Claude artifacts, databases or infrastructure changed. Keep this PR in draft; no merge or deployment is authorised.
