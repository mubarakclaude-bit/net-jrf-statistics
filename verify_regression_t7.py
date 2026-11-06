#!/usr/bin/env python3
# Verify every numerical claim used by regression-t7 (heteroscedasticity and GLS).
# Run with Python 3 and numpy. Exact algebraic identities are also asserted.
import numpy as np
from fractions import Fraction as F

# Example: y = beta0 + beta1*x + u, x = (0,1,2,3), Var(u_i)=sigma^2*w_i.
x=np.array([0.,1.,2.,3.])
X=np.column_stack([np.ones(4),x])
w=np.array([1.,2.,3.,4.])
Omega=np.diag(w)
beta=np.array([1.,2.])
y=X@beta
ols_cov=np.linalg.inv(X.T@X)@X.T@Omega@X@np.linalg.inv(X.T@X)
gls_cov=np.linalg.inv(X.T@np.linalg.inv(Omega)@X)
gls_beta=np.linalg.solve(X.T@np.linalg.inv(Omega)@X,X.T@np.linalg.inv(Omega)@y)
assert np.allclose(gls_beta,beta)
assert np.all(np.linalg.eigvalsh(ols_cov-gls_cov)>-1e-10)
assert np.allclose(ols_cov,[[1.0,-0.5],[-0.5,0.5]])
assert np.allclose(gls_cov,[[49/58,-23/58],[-23/58,25/58]])
# A heteroskedasticity-robust sandwich covariance is not the homoskedastic formula.
# Verify the HC0 meat and dimensions on a nonzero residual vector.
e=np.array([1.,-1.,2.,-2.])
bread=np.linalg.inv(X.T@X)
hc0=bread@X.T@np.diag(e**2)@X@bread
assert hc0.shape==(2,2) and np.allclose(hc0,hc0.T)
# Weighted least squares minimizes sum_i (y_i-x_i'b)^2 / w_i when Var(u_i)=sigma^2*w_i.
assert np.allclose(np.linalg.inv(Omega),np.diag(1/w))
# White test auxiliary regressors for a single x are 1,x,x^2; LM uses n*R_aux^2.
# Degrees of freedom equal the number of nonconstant auxiliary regressors retained.
print("OLS covariance (per sigma^2):",ols_cov.tolist())
print("GLS covariance (per sigma^2):",gls_cov.tolist())
print("GLS coefficient:",gls_beta.tolist())
print("HC0 covariance for stated residual vector:",hc0.tolist())
print("All regression-t7 numerical checks passed.")
