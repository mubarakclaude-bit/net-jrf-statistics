# Regression T14 evidence map — Errors in variables

- Scope: Unit VI, topic 6.14.
- Classical regressor measurement equation: W=X+v, with v mean zero and independent of X and u.
- Reliability ratio: λ=Var(X)/[Var(X)+Var(v)]; naive slope probability limit is λβ.
- Exact anchors: Var(X)=9, Var(v)=3 gives λ=3/4 and β=2 gives 1.5; Var(X)=4, Var(v)=1 gives λ=4/5; Var(X)=5, Var(v)=15 and β=−4 gives −1.
- Independent outcome error Y*=Y+e increases residual variance but leaves the slope unbiased under the stated assumptions.
- Berkson error is distinguished as X=W+v.
- IV correction requires relevance for true X and orthogonality to both structural and measurement errors.
- Exact arithmetic and pool contracts are checked in verify_regression_t14.py.
- No June 2026 question is claimed as a direct errors-in-variables PYQ.
- References: Wooldridge, Greene, Johnston & DiNardo.
