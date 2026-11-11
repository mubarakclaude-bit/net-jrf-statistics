# Mathematics — Unit II production acceptance

Scope: Paper 2 Statistics, Mathematics module, 16 topics.

## Existing production lessons (preserve)
- maths-t1 — Rank, Nullity, Sylvester and Frobenius
- maths-t4 — Sequences, Series and Power Series

## Remaining topics
- maths-t2 — Eigenvalues, eigenvectors, diagonalisation and Cayley–Hamilton
- maths-t3 — Quadratic forms, definiteness, canonical reduction and inertia
- maths-t5 — Continuity, differentiability, Rolle's theorem and mean value theorems
- maths-t6 — Maxima, minima and local extrema
- maths-t7 — Riemann integration, fundamental theorem and improper integrals
- maths-t8 — Generalised inverse (Moore–Penrose and reflexive inverses; estimability link)
- maths-t9 — Taylor's theorem, L'Hôpital's rule and uniform continuity
- maths-t10 — Functions of two variables, partial and total derivatives
- maths-t11 — Saddle points, constrained extrema and Lagrange multipliers
- maths-t12 — Double/triple integrals, change of variables and applications
- maths-t13 — Vector spaces, subspaces, span, basis and dimension
- maths-t14 — Linear systems, consistency, rank criterion and RREF
- maths-t15 — Gram–Schmidt, orthogonality and orthogonal matrices
- maths-t16 — Trace, determinant, inverse and matrix identities

## Package acceptance gate (per topic)
1. Versioned lesson JSON and mastery-pool JSON are the canonical, self-contained source of truth. Any optional generation tooling must be deterministic; no external Claude artifact database or runtime dependency is permitted.
2. 11–16 mandatory core scenes (extensions may be additional, within the repository cap).
3. Four or more measurable objectives; at least three prerequisites; two substantial scenarios; one flow; two guided problems including an unseen transfer; worked derivation; completion exercise; trap check; summary; quiz.
4. Exactly 20 unseen mastery items: 6 easy, 10 moderate, 4 hard; at least 4 numeric with sanity checks and 2 multi-statement items with four verdicts; answer-key spread; worked explanations.
5. Exact arithmetic / symbolic verification for every numerical anchor and identity. Extremal claims must be proved or constructed, never inferred from random sampling.
6. Evidence map with syllabus alignment and references; no invented PYQ attribution.
7. Verification report records script output and manual mathematical review.
8. Run lesson structural validation, formula rendering, pool audit, full repository tests and click-through tests.

## Cross-topic dependencies
- T2 supplies the spectral theorem and eigenvalue tools used in T3 and T8.
- T3 connects quadratic forms to positive definiteness, optimisation and regression.
- T8 connects matrix rank/estimability (T1 and regression Unit VI).
- T13–T15 build the vector-space and orthogonality foundations needed by matrix algebra and multivariate analysis.
- T5–T9 form the single-variable real-analysis sequence.
- T10–T12 form the multivariable calculus sequence.

## Release outcome — 12 November 2026
- Consolidated release PR: [#59](https://github.com/mubarakclaude-bit/net-jrf-statistics/pull/59) — MERGED.
- Merge commit: `f389b07e484b04b17e599155d4e3233db5d3ba97`.
- All 16 Mathematics topics are registered as `approved` in `seed/meta_lessons.json` and present in `seed/catalog.json`.
- The 14 newly completed lesson packages and their 280 mastery questions are in `main`; the original T1 and T4 packages were preserved.
- Pre-merge validation: mathematical anchor checks, lesson schema checks, formula rendering, repository index/harness checks, build, app integration and lesson click-through all passed on the validated code revision.
- Vercel deployment and live-site verification are intentionally excluded from this release task.

## Release rule
A topic is part of the repository production release only after its complete package passes the gates above and is merged into `main`. A green lesson-level check or a feature branch alone is not a production release. Live Vercel deployment is a separate release step.
