# Regression T9 evidence map — Identification in simultaneous equation models

- Scope: Unit VI, topic 6.9.
- Structural demand: Q = 10 − 2P + 3Y + u_d; supply: Q = 2 + P + 4W + u_s.
- At equilibrium, 3P = 8 + 3Y − 4W + u_d − u_s; reduced-form coefficients are π_Y=1 and π_W=−4/3.
- Order condition: excluded exogenous variables k must satisfy k ≥ m, where m is the number of endogenous RHS variables.
- Rank condition: the relevant cross-equation coefficient matrix must have rank m; proportional columns fail.
- Original numerical matrix [[2,4],[1,2]] has rank one because the second column is twice the first.
- All exact algebraic anchors are checked in verify_regression_t9.py.
- No June 2026 Paper 2 question is claimed as a direct simultaneous-equation identification PYQ.
- References: Greene, Wooldridge, and Johnston & DiNardo.
