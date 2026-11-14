# Stochastic Processes and Multivariate Analysis — Mathematical Audit
Date: 14 November 2026

## Base and scope
- Repository: `mubarakclaude-bit/net-jrf-statistics`
- Base: `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`
- Branch: `audit/stochastic-multivariate-math-2026-11-14`
- Paper 2 only. No Paper 1, application code, shared manifests, workflows or deployment files changed.

## Coverage in this pass
- Stochastic Processes T1–T9: inspected selected learner-facing worked/guided numerical scenes and all nine 20-item mastery pools (180 items); independently recomputed transition, stationary-vector, hitting-time, period, Poisson-process, gambler’s-ruin, queue, branching and renewal calculations.
- Multivariate Analysis T1–T9: inspected worked/completion/guided numerical scenes and all nine 20-item mastery pools (180 items); independently recomputed conditional normal moments, Schur complements, partial/multiple correlations, PCA eigenvalues, Hotelling transformations, Wishart degrees of freedom, canonical correlations, covariance MLEs and Mahalanobis distances.
- This remains a scoped audit of selected learner-facing scenes and mastery pools, not a certification of every theory/revision statement or every possible derivation in Paper 2.

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

## Additional confirmed findings

### SM-002 — Hotelling T² mastery item has no correct option
- File: `seed/multivariate_t4_mastery.json`; item `mv-t4-m-07`.
- For n=10, p=2 and T²=8, F=[(10−2)/(2×9)]×8=32/9≈3.556.
- Before: the options were 2.0, 3.2, 4.0 and 8.0; the explanation instructed learners to choose the nearest value 4.0.
- After: option C contains the exact value 32/9≈3.556.

### SM-003 — Second Hotelling T² mastery item has no correct option
- File: `seed/multivariate_t4_mastery.json`; item `mv-t4-m-13`.
- For p=3, n=12 and T²=9, F=[(12−3)/(3×11)]×9=27/11≈2.455.
- Before: options were 2, 1, 3 and 9; the explanation again advised choosing the nearest value.
- After: option A contains 27/11≈2.455.

### SM-004 — Covariance MLE explanation cites the wrong option ordering
- File: `seed/multivariate_t7_mastery.json`; item `mv-t7-m-17`.
- The centred outer-product sum is [[6,3],[3,2]]; dividing by n=3 gives [[2,1],[1,2/3]].
- The mastery item’s correct option is B, as its answer key already stated. The explanation incorrectly said “official option D” without distinguishing the original exam’s option ordering.
- After: the explanation explicitly says B for this mastery item and D for the original June 2026 paper.

### SM-005 — Factor-analysis mastery answer key selects an incorrect option
- File: `seed/multivariate_t9_mastery.json`; item `mv-t9-m-01`.
- The purpose of common factor analysis is to explain shared covariance among observed variables; this is option B.
- Before: answer key was D (“Estimate a regression slope”), contradicting the explanation.
- After: answer key corrected to B.

## Additional verifier changes
- `verify_multivariate_t4.py`: exact-fraction assertions for both Hotelling F values and their corrected options.
- `verify_multivariate_t7.py`: asserts the mastery item’s option B and the distinction from the original paper’s option D.
- `verify_multivariate_t9.py`: asserts the correct answer key B for item `mv-t9-m-01`.

## Stochastic Processes T5–T9 spot-check outcome
No additional confirmed numerical or answer-key defects were identified in the worked calculations and mastery pools inspected in this pass. Stochastic T4’s two already-known learner-facing answer mismatches remain owned by PR #93 and are not duplicated here.
