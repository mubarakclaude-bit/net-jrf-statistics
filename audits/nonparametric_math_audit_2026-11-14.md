# Nonparametric Methods mathematical audit — 2026-11-14

## Scope and base

- Paper 2 only — Nonparametric Methods, catalog topics `nonparam-t1` through `nonparam-t8`.
- Base: `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`.
- Reviewed all eight lesson JSON files and all eight 20-item mastery pools (160 questions), with targeted recomputation of numerical examples and answer-key checks.
- Inspected the existing T4 verifier `verify_nonparam_t4.py`; the content map did not list it as a topic verifier. The script is extended with the newly identified edge-case and finite-sample expectation checks.
- This is a scoped mathematical audit; it does not certify every prose statement, reference or possible implementation of each test.

## Confirmed findings

### NP-001 — Population Spearman relation was labelled as a sample expectation

**File:** `seed/lesson_np4.json`, scene `s7`, the revision sheet and guided transfer `s10`; related explanations in `seed/nonparam_t4_mastery.json`.

The lesson labelled the bivariate-normal population relation
`(6/π)arcsin(r/2)`
as `E(ρ)`, without distinguishing the population Spearman coefficient from the expectation of the finite-sample Spearman statistic. They are not generally equal. For a sample of size n from a bivariate normal population with Pearson correlation r,

`E(r_s)=6/[π(n+1)]{arcsin(r)+(n−2)arcsin(r/2)}`.

The population coefficients are `ρ_S=(6/π)arcsin(r/2)` and `τ=(2/π)arcsin(r)`. At r=0.5, the population values are ρ_S≈0.482584 and τ=0.333333, whereas E(r_s)≈0.441879 at n=10. The lesson now labels population quantities correctly and teaches the finite-sample expectation separately.

References:
- *A robust Spearman correlation coefficient permutation test*, DOI: https://doi.org/10.1080/03610926.2022.2121144 — states the finite-sample expectation formula.
- Mathematical Statistics I notes, https://kpms.karlin.mff.cuni.cz/stud-mater/2017/NMSA331_Mathematical_Statistics_1.pdf — gives the finite-sample expectation formula and distinguishes the population relation.
- Balakrishnan and Lai, *Continuous Bivariate Distributions*, §4.7 — gives the population rank-correlation relation and notes that sample Spearman is not unbiased for population Spearman.

### NP-002 — Kendall null variance is not strictly smaller at every n

**File:** `seed/lesson_np4.json`, scene `s7` and guided transfer `s10`; `seed/nonparam_t4_mastery.json` items `np-t4-m-14` and `np-t4-m-20`.

Under the no-tie independence null,
`Var(r_s)=1/(n−1)` and `Var(τ_n)=2(2n+5)/[9n(n−1)]`.
The inequality `Var(τ_n)<Var(r_s)` holds for n>2. At n=2 both variances equal 1. The lesson and two mastery explanations now state the exact boundary rather than claiming strict inequality for every n.

### Explicit non-finding — T4 mastery item m-10

A truncated earlier result appeared to show `Σd²=70`, which would have made the keyed zero answer wrong. A fresh read of the actual main-branch file confirms the item states `n=6, Σd²=35`; this correctly gives `ρ_s=0`. No change was made to that item.

## Coverage notes

- All eight topic pools contain 20 items (160 total); each meets the repository's minimum answer-letter spread.
- Recomputed representative numerical scenes and pool items for Mann–Whitney, sign/signed-rank, Kruskal–Wallis, Friedman, Spearman, Kendall, runs, KS, EDF and linear-rank scale procedures.
- Recomputed the June 2026 Q42 Mann–Whitney example: pooled ES rank sum 152.5 gives U=32.5, consistent with the lesson.
- No other confirmed mathematical defect is included in this PR.

## Changes

- Clarified population versus finite-sample Spearman/Kendall quantities in T4.
- Corrected the n=2 edge case in the null-variance comparison.
- Updated T4 mastery explanations without changing answer keys.
- Extended existing `verify_nonparam_t4.py` with exact arithmetic and numerical assertions.
- Added this audit report.

## Boundaries

Only T4 lesson/pool content, its existing verifier and this report are changed. No catalog, shared manifest, application code, workflows, Paper 1, other modules, Claude artifacts, databases or infrastructure changed. Keep this PR in draft; no merge or deployment is authorised.
