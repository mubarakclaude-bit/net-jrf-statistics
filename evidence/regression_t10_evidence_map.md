# Regression T10 evidence map — Two-stage least squares

- Scope: Unit VI, topic 6.10.
- Instrument matrix: all included exogenous controls plus excluded instruments.
- First stage: each endogenous structural regressor projected onto Z; fitted columns are P_ZX.
- Second stage: Y regressed on included exogenous controls and fitted endogenous regressors.
- Matrix estimator: (X′P_ZX)⁻¹X′P_ZY, with P_Z=Z(Z′Z)⁻¹Z′.
- Original exact example: Z=(-1,0,1), X=(1,2,4), Y=(2,5,8); first-stage slope 3/2, reduced-form slope 3, 2SLS ratio 2.
- Standard-error safeguard: naive second-stage OLS standard errors are not the final 2SLS covariance estimator.
- Exact arithmetic and pool contracts are checked in verify_regression_t10.py.
- No June 2026 question is claimed as a direct 2SLS PYQ.
- References: Wooldridge, Greene, Johnston & DiNardo.
