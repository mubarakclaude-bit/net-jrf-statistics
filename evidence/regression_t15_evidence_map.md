# Regression T15 evidence map — k-class estimators, LIML and Fuller

- Scope: Unit VI, topic 6.15.
- General estimator: β̂(κ)=[X′(I−κM_Z)X]⁻¹X′(I−κM_Z)Y, with M_Z=I−P_Z.
- Endpoints: κ=0 gives OLS; κ=1 gives 2SLS.
- LIML selects κ using a likelihood/generalized eigenvalue criterion; Fuller applies a finite-sample adjustment to LIML.
- Exact scalar example: X′X=10, X′M_ZX=4, X′Y=20, X′M_ZY=5 gives estimates 2 at κ=0, 2.1875 at κ=0.5 and 2.5 at κ=1.
- Additional exact anchor: (18−4)/(8−2)=7/3.
- Exact arithmetic and pool contracts are checked in verify_regression_t15.py.
- No June 2026 question is claimed as a direct k-class/LIML PYQ.
- References: Greene, Johnston & DiNardo, Wooldridge.
