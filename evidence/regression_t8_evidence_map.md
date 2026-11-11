# Regression T8 evidence map — Endogeneity and instrumental variables

- Scope: Unit VI, topic 6.8.
- Structural equation: Y = βX + u; endogeneity is represented by Cov(X,u) ≠ 0 (or failure of E(u|X)=0).
- OLS probability limit: β + Cov(X,u)/Var(X).
- IV requirements are separated: relevance (conditional predictive relationship with X) and exclusion (no direct Z→Y path; orthogonality to u).
- Just-identified IV/Wald ratio: reduced-form effect divided by first-stage effect.
- Worked numeric anchor: reduced form 0.60; first stage 0.30; IV estimate 2.
- Mastery numeric anchors are checked with exact rational arithmetic in verify_regression_t8.py.
- No June 2026 Paper 2 question is claimed as a direct endogeneity/IV PYQ. Q9, Q11 and Q38 belong to the existing regression bank's model-fit, BLUE and multicollinearity clusters.
- Primary conceptual references: Wooldridge, *Introductory Econometrics*; Greene, *Econometric Analysis*; Angrist and Pischke, *Mostly Harmless Econometrics*.
