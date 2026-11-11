# Evidence map — Unit VI, 6.7 Autocorrelation and Durbin–Watson

## Syllabus and PYQ provenance
This lesson implements backlog topic regression-t6. The June 2026 actual paper includes Q3 on Yule–Walker estimation for an AR(2) process (j26-q03). This is adjacent time-series/autocorrelation knowledge, not a direct Durbin–Watson question. It is used only as a conceptual bridge. All mastery questions are original practice.

## Mathematical claims and checks
- Autocorrelation is cross-observation covariance, distinct from heteroscedasticity (non-constant conditional variance).
- AR(1) disturbance: u_t=rho u_(t-1)+epsilon_t; under standard assumptions |rho|<1 is covariance-stationary.
- DW = sum_{t=2}^n (e_t-e_(t-1))^2 / sum_{t=1}^n e_t^2; range 0 to 4.
- Approximation DW≈2(1-rhat_1), so values near 0/2/4 suggest positive/none/negative first-order residual correlation.
- DW bounds test has lower and upper bounds and an inconclusive region. The usual test is not valid in its standard form with lagged dependent variable regressors.
- Breusch–Godfrey LM is a common alternative for higher-order serial correlation and dynamic regressions.

## Exact verification
The verifier uses Fraction arithmetic for residual differences, the DW statistic and approximation values. It checks the mastery pool counts, difficulty, format, balanced answer positions and multi-statement verdict consistency.
