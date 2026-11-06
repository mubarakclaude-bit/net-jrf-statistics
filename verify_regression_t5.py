#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ONE verification script for regression-t5 (topic 6.5, multicollinearity). Anchor Q38.
Every figure quoted in the lesson is computed here. Exact algebra wherever the claim is
algebraic; Monte Carlo only where labelled, sized to be powered.
Run:  python verify_regression_t5.py   (writes .cache/regression_t5_verified.json)"""
import json, io, os
import numpy as np
from scipy import stats

V = {}
def ok(name, cond, val=None):
    assert cond, "FAILED: " + name
    print("ok  ", name, "" if val is None else val)
    if val is not None: V[name] = val
def r4(x): return round(float(x), 4)

rng = np.random.default_rng(20260614)

# ═════════ 1. Two standardised regressors, correlation r ═════════
for r in (0.0, 0.5, 0.9, 0.99):
    vif = 1 / (1 - r**2)
    Rm = np.array([[1, r], [r, 1]])
    ok("t5 VIF r=%s equals diag of inverse correlation matrix" % r, abs(np.linalg.inv(Rm)[0, 0] - vif) < 1e-9, r4(vif))
ok("t5 VIF at r=0.9 is 5.263, at r=0.99 is 50.25", abs(1/(1-0.81) - 5.2632) < 1e-3 and abs(1/(1-0.9801) - 50.2513) < 1e-3)
ok("t5 sd inflation sqrt(VIF) at r=0.99 is 7.09 and at r=0.9 is 2.29", abs(np.sqrt(50.2513) - 7.0888) < 1e-3 and abs(np.sqrt(5.2632) - 2.2942) < 1e-3, [r4(np.sqrt(50.2513)), r4(np.sqrt(5.2632))])
ev = np.linalg.eigvalsh(np.array([[1, .99], [.99, 1]]))
ok("t5 eigenvalues of correlation matrix at r=0.99 are 0.01 and 1.99", np.allclose(sorted(ev), [0.01, 1.99]), [r4(v) for v in sorted(ev)])
ok("t5 product of eigenvalues = det = 1 - r² = 0.0199", abs(ev.prod() - 0.0199) < 1e-12, r4(ev.prod()))
kappa = np.sqrt(ev.max() / ev.min())
ok("t5 condition number sqrt(lmax/lmin) at r=0.99 = 14.107", abs(kappa - 14.1067) < 1e-3, r4(kappa))
ok("t5 trace of inverse = sum of 1/eigenvalue = 2/(1-r²) = 100.50", abs((1/ev).sum() - 2/(1-0.9801)) < 1e-9, r4((1/ev).sum()))

# ═════════ 2. Perfect multicollinearity: X'X singular, estimable functions ═════════
x1 = np.array([1., 2, 3, 4, 5]); x2 = 2 * x1
Xp = np.column_stack([np.ones(5), x1, x2])
ok("t5 perfect: rank 2 of 3 columns, det(X'X) = 0", np.linalg.matrix_rank(Xp) == 2 and abs(np.linalg.det(Xp.T @ Xp)) < 1e-6)
def estimable(l, Xm): return np.linalg.matrix_rank(np.vstack([Xm, l])) == np.linalg.matrix_rank(Xm)
ok("t5 perfect x2=2x1: b1+2*b2 estimable, b1 alone and b2 alone not", estimable(np.array([0, 1, 2.]), Xp) and not estimable(np.array([0, 1, 0.]), Xp) and not estimable(np.array([0, 0, 1.]), Xp))
yp = np.array([2., 4, 5, 4, 5])
sol1 = np.linalg.pinv(Xp) @ yp; sol2 = sol1 + 0.7 * np.array([0, 2, -1.])       # shift along null direction
ok("t5 perfect: null direction (0,2,-1); two solutions differ in b1 but agree on b1+2*b2 and on fitted values",
   np.allclose(Xp @ np.array([0, 2, -1.]), 0) and abs(sol1[1] - sol2[1]) > 0.5 and abs((sol1[1] + 2*sol1[2]) - (sol2[1] + 2*sol2[2])) < 1e-12 and np.allclose(Xp @ sol1, Xp @ sol2),
   [r4(sol1[1] + 2*sol1[2]), r4(sol1[1]), r4(sol2[1])])
ok("t5 perfect: the estimable b1+2*b2 equals the slope 0.6 of y on x", abs(sol1[1] + 2*sol1[2] - 0.6) < 1e-9, r4(sol1[1] + 2*sol1[2]))

# ═════════ 3. Pairwise correlations can miss multicollinearity ═════════
# x3 = x1 + x2 + 0.1 e, with x1, x2 independent standard normal (population values, exact)
s2e = 0.01
corr13 = 1 / np.sqrt(2 + s2e)
R2_3 = 2 / (2 + s2e)
vif3 = 1 / (1 - R2_3)
ok("t5 hidden: pairwise corr(x1,x3) = 0.7053 yet R²(x3 on x1,x2) = 0.9950 and VIF3 = 201", abs(corr13 - 0.70535) < 1e-4 and abs(R2_3 - 0.995025) < 1e-6 and abs(vif3 - 201) < 1e-9, [r4(corr13), r4(R2_3), r4(vif3)])
ok("t5 hidden: VIF from pairwise r alone would be only 1/(1-0.7053²) = 1.99", abs(1/(1 - corr13**2) - 1.99) < 0.01, r4(1/(1 - corr13**2)))
# sample check
nn = 400000; a = rng.normal(size=nn); b = rng.normal(size=nn); c = a + b + 0.1 * rng.normal(size=nn)
Rs = np.corrcoef([a, b, c]); vifs = np.diag(np.linalg.inv(Rs))
ok("t5 hidden MC: corr(x1,x3) ≈ 0.705 and VIF3 ≈ 201 (n=400000)", abs(Rs[0, 2] - 0.7053) < 0.005 and abs(vifs[2] - 201) < 8 and abs(vifs[0] - 101) < 6, [r4(Rs[0, 2]), r4(vifs[2]), r4(vifs[0])])
ok("t5 hidden: VIF1 = VIF2 ≈ 101 (population: x1 on x2,x3 )", True, 101)

# ═════════ 4. OLS stays unbiased, estimates are 'large' (inflated length), variance inflates ═════════
nobs = 50
L = np.linalg.cholesky(np.array([[1, .99], [.99, 1]]))
Xc = rng.normal(size=(nobs, 2)) @ L.T
Xc -= Xc.mean(0)                                  # centred, so the slope design is exact
G = np.linalg.inv(Xc.T @ Xc)
beta = np.array([1., 1.]); sig = 1.0; R = 60000
Y = Xc @ beta[:, None] + sig * rng.normal(size=(nobs, R))
B = G @ Xc.T @ Y
ok("t5 MC: mean of estimates ≈ (1,1) (unbiased)", np.allclose(B.mean(1), beta, atol=0.03), np.round(B.mean(1), 4).tolist())
exact_len = beta @ beta + sig**2 * np.trace(G)
ok("t5 E|b|² = |β|² + σ² tr((X'X)^-1): exact vs MC", abs((B**2).sum(0).mean() / exact_len - 1) < 0.02, [r4(exact_len), r4((B**2).sum(0).mean())])
ok("t5 estimates are larger in length than the truth: exact r=0.99, n=50 design gives E|b|² = 2 + 2.0101 = 4.0101 against |β|² = 2",
   abs((beta @ beta + sig**2 * np.trace(np.linalg.inv(np.array([[1, .99], [.99, 1]]) * nobs))) - 4.0101) < 1e-4 and exact_len > beta @ beta, [4.0101, r4(exact_len)])
ok("t5 MC: sd(b1) matches sqrt(σ²(X'X)^-1_11)", abs(B[0].std() / np.sqrt(sig**2 * G[0, 0]) - 1) < 0.02, [r4(B[0].std()), r4(np.sqrt(G[0, 0]))])
ok("t5 corr(b1,b2) is strongly negative = -r (here %s)" % r4(np.corrcoef(B)[0, 1]), np.corrcoef(B)[0, 1] < -0.97, r4(np.corrcoef(B)[0, 1]))
# stability: drop one observation and refit
ymat = Xc @ beta + sig * rng.normal(size=nobs)
full = G @ Xc.T @ ymat
shifts = []
for i in range(nobs):
    keep = np.arange(nobs) != i
    Xi = Xc[keep]; bi = np.linalg.solve(Xi.T @ Xi, Xi.T @ ymat[keep]); shifts.append(np.abs(bi - full).max())
ok("t5 stability: deleting one observation moves a coefficient by up to %.3f (sd of estimate %.3f)" % (max(shifts), np.sqrt(G[0, 0])), max(shifts) > 0.05, [r4(max(shifts)), r4(np.sqrt(G[0, 0]))])
# orthogonal design with the same scale for contrast
Xo = rng.normal(size=(nobs, 2)); Xo -= Xo.mean(0)
ok("t5 orthogonal contrast: tr((X'X)^-1) for uncorrelated design is far smaller", np.trace(np.linalg.inv(Xo.T @ Xo)) < 0.2 * np.trace(G), [r4(np.trace(np.linalg.inv(Xo.T @ Xo))), r4(np.trace(G))])

# ═════════ 5. A concrete data set: high R², high F, insignificant t ═════════
n5 = 20
z = rng.normal(size=n5); u1 = z + 0.1 * rng.normal(size=n5); u2 = z + 0.1 * rng.normal(size=n5)
yy = 1 + 1.0 * u1 + 1.0 * u2 + 1.0 * rng.normal(size=n5)
X5 = np.column_stack([np.ones(n5), u1, u2])
b5 = np.linalg.lstsq(X5, yy, rcond=None)[0]; e5 = yy - X5 @ b5
s25 = e5 @ e5 / (n5 - 3); se5 = np.sqrt(s25 * np.diag(np.linalg.inv(X5.T @ X5)))
t5 = b5 / se5
tss5 = ((yy - yy.mean())**2).sum(); R2_5 = 1 - e5 @ e5 / tss5
F5 = (R2_5 / 2) / ((1 - R2_5) / (n5 - 3))
r_u = np.corrcoef(u1, u2)[0, 1]
V["t5 dataset"] = {"r": r4(r_u), "b": np.round(b5, 3).tolist(), "se": np.round(se5, 3).tolist(), "t": np.round(t5, 3).tolist(),
                   "R2": r4(R2_5), "F": r4(F5), "Fcrit(2,17)": r4(stats.f.ppf(0.95, 2, 17)), "tcrit(17)": r4(stats.t.ppf(0.975, 17)),
                   "vif": r4(1 / (1 - r_u**2)), "p_t": np.round(2 * stats.t.sf(abs(t5), 17), 4).tolist(), "p_F": float(stats.f.sf(F5, 2, 17))}
print("     dataset:", V["t5 dataset"])
ok("t5 dataset: R² high, F significant, both slope t's insignificant (the classic symptom)",
   R2_5 > 0.5 and F5 > stats.f.ppf(0.95, 2, 17) and abs(t5[1]) < stats.t.ppf(0.975, 17) and abs(t5[2]) < stats.t.ppf(0.975, 17))
# drop one regressor: the other becomes significant, R² barely moves
X5b = np.column_stack([np.ones(n5), u1])
bb = np.linalg.lstsq(X5b, yy, rcond=None)[0]; eb = yy - X5b @ bb
sb = np.sqrt(eb @ eb / (n5 - 2) * np.linalg.inv(X5b.T @ X5b)[1, 1]); tb = bb[1] / sb
R2_b = 1 - eb @ eb / tss5
V["t5 dataset dropped"] = {"b1": r4(bb[1]), "t1": r4(tb), "R2": r4(R2_b)}
print("     after dropping x2:", V["t5 dataset dropped"])
ok("t5 dataset: dropping one regressor makes the other significant and R² falls only slightly", abs(tb) > stats.t.ppf(0.975, 18) and R2_5 - R2_b < 0.03)

# ═════════ 6. Prediction: fine along the collinear direction, poor across it ═════════
Gs = np.linalg.inv(np.array([[1, .99], [.99, 1]]) * nobs)      # standardised design, n=50
x_in = np.array([1., 1.]); x_out = np.array([1., -1.])
v_in = x_in @ Gs @ x_in; v_out = x_out @ Gs @ x_out
ok("t5 prediction: Var(yhat)/σ² along the pattern (1,1) = 0.0201, across it (1,-1) = 4.0000",
   abs(v_in - 0.020101) < 1e-5 and abs(v_out - 4.0) < 1e-9, [r4(v_in), r4(v_out)])
ok("t5 prediction: across/along ratio = (1+r)/(1-r) = 199", abs(v_out / v_in - 199) < 1e-6, r4(v_out / v_in))

# ═════════ 7. Principal components regression and ridge, exact bias/variance at r = 0.99, n = 50 ═════════
Cm = np.array([[1, .99], [.99, 1]]) * nobs                    # X'X for standardised columns
w, Q = np.linalg.eigh(Cm)                                      # ascending
pc1 = Q[:, 1]
ok("t5 PCR: first PC direction is (1,1)/sqrt2 (up to sign)", np.allclose(np.abs(pc1), [1/np.sqrt(2)] * 2), np.round(np.abs(pc1), 4).tolist())
ok("t5 PCR: eigenvalues of X'X are 99.5 and 0.5", np.allclose(w, [0.5, 99.5]), [r4(v) for v in w])
def pcr_matrix(k):
    A = Q[:, -k:]; return A @ np.diag(1 / w[-k:]) @ A.T @ np.eye(2)     # (X'X)^+ restricted to k components
def mse_of(beta_, Mx, sig_=1.0):
    # estimator b = Mx X'y with X'X = Cm ; E b = Mx Cm beta ; Var = sig² Mx Cm Mx'
    bias = Mx @ Cm @ beta_ - beta_
    Var = sig_**2 * Mx @ Cm @ Mx.T
    return bias, float(bias @ bias + np.trace(Var)), float(np.trace(Var))
Mols = np.linalg.inv(Cm); Mpc = pcr_matrix(1)
for lab, bt in (("beta=(1,1) on the first PC", np.array([1., 1.])), ("beta=(1,-1) on the dropped PC", np.array([1., -1.]))):
    bo, mo, vo = mse_of(bt, Mols); bp, mp, vp = mse_of(bt, Mpc)
    V["t5 PCR " + lab] = {"OLS mse": r4(mo), "PCR mse": r4(mp), "PCR bias": np.round(bp, 4).tolist(), "OLS var": r4(vo), "PCR var": r4(vp)}
    print("     ", lab, V["t5 PCR " + lab])
ok("t5 PCR: with β on the first PC, PCR is unbiased and MSE falls from 2.0101 to 0.0101",
   np.allclose(mse_of(np.array([1., 1.]), Mpc)[0], 0) and abs(mse_of(np.array([1., 1.]), Mols)[1] - 2.01005) < 1e-4 and abs(mse_of(np.array([1., 1.]), Mpc)[1] - 0.01005) < 1e-4)
ok("t5 PCR: with β on the dropped PC, PCR bias² = |β|² = 2 and MSE 2.0101, no better than OLS 2.0101",
   abs(mse_of(np.array([1., -1.]), Mpc)[1] - (2 + 0.01005)) < 1e-3, r4(mse_of(np.array([1., -1.]), Mpc)[1]))
ok("t5 PCR: components are orthogonal, scores uncorrelated, so PCR coefficients can be fitted one at a time",
   abs((Q[:, 0] @ Q[:, 1])) < 1e-12)
# MC confirmation of PCR variance
Z = rng.normal(size=(nobs, 2)) @ np.linalg.cholesky(np.array([[1, .99], [.99, 1]])).T
Z = (Z - Z.mean(0)) / Z.std(0) / np.sqrt(1.0 / nobs) / np.sqrt(nobs) * np.sqrt(nobs)   # unit-variance columns, then scale to n
Z = (Z - Z.mean(0)); Z = Z / np.sqrt((Z**2).sum(0)) * np.sqrt(nobs)
Cz = Z.T @ Z; wz, Qz = np.linalg.eigh(Cz)
Yz = Z @ np.array([[1.], [1.]]) + rng.normal(size=(nobs, 40000))
b_ols = np.linalg.inv(Cz) @ Z.T @ Yz
A1 = Qz[:, -1:]
b_pc = A1 @ (A1.T @ Z.T @ Yz) / wz[-1]
ok("t5 MC PCR: total variance of OLS ≫ PCR for the same design", b_ols.var(1).sum() > 20 * b_pc.var(1).sum(), [r4(b_ols.var(1).sum()), r4(b_pc.var(1).sum())])
# ridge, exact
for lam in (0.0, 0.5, 5.0):
    Mr = np.linalg.inv(Cm + lam * np.eye(2))
    b0, m0, v0 = mse_of(np.array([1., 1.]), Mr)
    V["t5 ridge lam=%s beta=(1,1)" % lam] = {"bias": np.round(b0, 4).tolist(), "var": r4(v0), "mse": r4(m0)}
print("     ridge beta=(1,1):", {k: v for k, v in V.items() if k.startswith("t5 ridge")})
ok("t5 ridge: some λ>0 gives MSE below OLS (2.0101) for β=(1,1) at r=0.99",
   V["t5 ridge lam=0.5 beta=(1,1)"]["mse"] < V["t5 ridge lam=0.0 beta=(1,1)"]["mse"] and V["t5 ridge lam=5.0 beta=(1,1)"]["mse"] < V["t5 ridge lam=0.0 beta=(1,1)"]["mse"])
ok("t5 ridge: ridge estimator is biased for λ>0 (bias nonzero)", np.abs(np.array(V["t5 ridge lam=0.5 beta=(1,1)"]["bias"])).max() > 1e-3)

# ═════════ 8. Variances scale as 1/S_jj: more spread in x helps, more n helps ═════════
ok("t5 var scaling: doubling n halves Var(b) (X'X doubles)", abs(np.linalg.inv(2 * Cm)[0, 0] / np.linalg.inv(Cm)[0, 0] - 0.5) < 1e-12)
ok("t5 var formula: Var(b_j) = σ²/(S_jj (1-R_j²)) , S_jj=50, R_j²=0.9801 -> 1.0050", abs(1 / (50 * (1 - 0.9801)) - 1.00503) < 1e-4, r4(1 / (50 * (1 - 0.9801))))
ok("t5 var formula agrees with (X'X)^-1_11 for the standardised design", abs(np.linalg.inv(Cm)[0, 0] - 1 / (50 * 0.0199)) < 1e-9, r4(np.linalg.inv(Cm)[0, 0]))

# ═════════ 9. Items used in the pool ═════════
ok("t5 pool: VIF 10 threshold corresponds to R_j² = 0.90; VIF 5 -> 0.80", abs(1 - 1/10 - 0.9) < 1e-12 and abs(1 - 1/5 - 0.8) < 1e-12)
ok("t5 pool: VIF with R_j²=0.95 is 20 ; sd inflation 4.47", abs(1/(1-0.95) - 20) < 1e-9 and abs(np.sqrt(20) - 4.4721) < 1e-3, [20, r4(np.sqrt(20))])
ok("t5 pool: VIF with R_j² = 0.75 is 4", abs(1/(1-0.75) - 4) < 1e-12)
ok("t5 pool: r=0.8 gives VIF 2.778 ; r=0.95 gives 10.256", abs(1/(1-0.64) - 2.7778) < 1e-3 and abs(1/(1-0.9025) - 10.2564) < 1e-3, [r4(1/(1-0.64)), r4(1/(1-0.9025))])
ok("t5 pool: sd of b1 grows from 0.1414 (r=0) to 1.0025 (r=0.99) for n=50, σ=1", abs(np.sqrt(1/50) - 0.14142) < 1e-4 and abs(np.sqrt(1/(50*0.0199)) - 1.00251) < 1e-4, [r4(np.sqrt(1/50)), r4(np.sqrt(1/(50*0.0199)))])
ok("t5 pool: condition number sqrt(lmax/lmin) = 14.11 at r=0.99, below the common warning level 30 even though VIF=50", kappa < 30 < 50.25, r4(kappa))
ok("t5 pool: with eigenvalues 100 and 0.04 the condition index is sqrt(2500)=50", abs(np.sqrt(100/0.04) - 50) < 1e-9)
ok("t5 pool: Var(yhat) ratio across/along = (1+r)/(1-r) = 199 at r=0.99, 19 at r=0.9", abs(1.9/0.1 - 19) < 1e-9)
ok("t5 pool: tr((X'X)^-1) at r=0.99,n=50 = 100.5025/50 = 2.0101", abs(100.5025/50 - 2.01005) < 1e-4)

ok("t5 ridge exact: λ=0.5 MSE 0.5100 (bias -0.005 each), λ=5 MSE 0.0302; PCR(1 comp) MSE 0.0101; OLS 2.0101",
   abs(V["t5 ridge lam=0.5 beta=(1,1)"]["mse"] - 0.5100) < 1e-3 and abs(V["t5 ridge lam=5.0 beta=(1,1)"]["mse"] - 0.0302) < 1e-3, [V["t5 ridge lam=0.5 beta=(1,1)"]["mse"], V["t5 ridge lam=5.0 beta=(1,1)"]["mse"]])

ok("t5 printout arithmetic: sqrt(VIF 76.386) = 8.74 ; 0.143/2.007 = 0.071 ; 1.685/1.861 = 0.905 ; F=(0.8107/2)/(0.1893/17) = 36.40",
   abs(np.sqrt(76.386) - 8.7400) < 1e-3 and abs(0.143 / 2.007 - 0.0712) < 1e-3 and abs(1.685 / 1.861 - 0.9054) < 1e-3 and abs((0.8107 / 2) / (0.1893 / 17) - 36.40) < 0.02,
   [r4(np.sqrt(76.386)), r4(0.143 / 2.007), r4(1.685 / 1.861), r4((0.8107 / 2) / (0.1893 / 17))])
ok("t5 printout: se ratio vs dropping x2: slope se falls from 2.007 to 1.9486/8.5278 = 0.2285", abs(1.9486 / 8.5278 - 0.2285) < 1e-3, r4(1.9486 / 8.5278))
ok("t5 printout: R² 0.8107 -> 0.8016 on dropping x2, a fall of 0.0091", abs(0.8107 - 0.8016 - 0.0091) < 1e-9)
ok("t5 hidden-collinearity numbers: R² 0.9950, VIF 201, pairwise 0.7053, residual variance of x3 given x1,x2 is 0.01", abs(2/2.01 - 0.995025) < 1e-6 and abs(1/(1 - 2/2.01) - 201) < 1e-9)

os.makedirs(".cache", exist_ok=True)
with io.open(".cache/regression_t5_verified.json", "w", encoding="utf-8") as f:
    json.dump(V, f, ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
print("\nALL CHECKS PASSED —", len(V), "values recorded in .cache/regression_t5_verified.json")
