# Evidence map — Unit VI, 6.6 Heteroscedasticity and GLS

## Syllabus and provenance
This lesson implements the repository backlog topic regression-t7 — Heteroscedasticity and Generalized Least Squares. The lesson is syllabus-aligned to Unit VI regression/econometrics. The currently documented June 2026 regression PYQ anchors in the repository concern other topics; no direct heteroscedasticity PYQ is claimed. The 20 mastery questions are original practice.

## Mathematical claims and checks
- Heteroscedasticity: Var(u_i|X)=sigma_i^2; exogeneity E(u|X)=0 is a separate condition.
- Under exogeneity, heteroscedasticity alone does not generally bias OLS coefficients, but conventional homoscedastic standard errors are generally invalid and OLS is generally inefficient among linear unbiased estimators.
- GLS: beta_hat=(X' Omega^-1 X)^-1 X' Omega^-1 y, for known positive-definite Omega.
- If Omega=sigma^2 H, the common scale cancels. For diagonal H=diag(h_i), WLS criterion weights are 1/h_i and row multipliers are 1/sqrt(h_i).
- FGLS estimates the covariance structure before applying GLS. Robust sandwich standard errors alter estimated uncertainty, not OLS coefficients.
- Breusch–Pagan LM example: n=80, R2_aux=0.12 gives 9.6, asymptotically chi-square with df equal to tested variance regressors.

## Exact verification
The Python verifier uses Fraction arithmetic for the GLS weighted mean (12/5), WLS weight/row multiplier identities, BP LM calculations, and mastery-pool counts, difficulty, format, answer-key balance and multi-statement verdict consistency.
