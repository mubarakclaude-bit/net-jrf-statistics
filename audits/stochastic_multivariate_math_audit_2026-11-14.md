# Stochastic Processes and Multivariate Analysis — Mathematical Audit
Date: 14 November 2026

## Base and scope
- Repository: `mubarakclaude-bit/net-jrf-statistics`
- Base: `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`
- Branch: `audit/stochastic-multivariate-math-2026-11-14`
- Paper 2 only. No Paper 1, application code, shared manifests, workflows or deployment files changed.

## Coverage in this pass
- Stochastic Processes T1–T4: inspected learner-facing worked/guided calculations and all four 20-item mastery pools (80 items); independently recomputed key transition, stationary-vector, hitting-time and period calculations.
- Multivariate Analysis T1–T3: inspected worked/completion/guided numerical scenes and all three 20-item mastery pools (60 items); independently recomputed conditional normal moments, Schur complements, partial/multiple correlations, PCA eigenvalues and explained-variance calculations.
- This is a scoped audit of these selected topics/scenes and pools, not a certification of all Paper 2 content. Stochastic T5–T9 and Multivariate T4–T9 remain unaudited in this pass. Other theory/revision statements outside the inspected scenes also remain subject to further review.

## Confirmed finding

### SM-001 — PCA mastery item labels a covariance spectrum as a correlation spectrum
- File: `seed/multivariate_t3_mastery.json`
- Item: `mv-t3-m-11`
- Severity: Major (mathematically impossible premise)
- Before: “A correlation matrix has eigenvalues 2.5, 1.2, 0.8 and 0.5.”
- A 4×4 correlation matrix has trace 4 because every diagonal entry is 1. Its eigenvalues must therefore sum to 4. The listed eigenvalues sum to 5, so they cannot be the eigenvalues of a 4×4 correlation matrix.
- Correction: change “correlation matrix” to “covariance matrix”. A covariance matrix may have total variance/trace 5; the listed nonnegative eigenvalues sum to 5. The first two components explain (2.5+1.2)/5 = 3.7/5 = 74%, preserving the intended answer and arithmetic.

## Independent verification
- Extended `verify_multivariate_t3.py` to assert the corrected matrix type and independently check the eigenvalue sum and 74% proportion using exact fractions.
- Existing topic verifiers were inspected for Multivariate T1–T3 and Stochastic T1–T4. They already cover selected exact calculations and structural contracts, but are not treated as proof of every mastery answer.
- No claim is made that the new verifier has passed CI. CI must run on the draft PR.

## Existing overlapping work
- Stochastic T4 has two learner-facing answer mismatches on current `main`: the alternating two-state example and the two-closed-classes example. These are already owned by the open mathematical-integrity PR #93, which includes their corrections. This branch deliberately does not touch `seed/lesson_stochastic_t4.json` or its verifier.

## Change record
- Modified: `seed/multivariate_t3_mastery.json` (one stem correction)
- Modified: `verify_multivariate_t3.py` (exact regression assertion)
- Added: this audit report
- No merge or deployment.
- No Claude-owned files, databases, artifacts or infrastructure used.
