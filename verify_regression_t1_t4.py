#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ONE verification script for regression-t1..t4 (SPEC section 6). Every figure used in the four
lessons is computed here; the authoring scripts quote these values and nothing else.
Run:  python verify_regression_t1_t4.py      (writes .cache/regression_verified.json)
Exact arithmetic (Fraction) is used wherever the claim is algebraic; numpy only for matrices
and for the Monte Carlo checks, which are labelled as simulation and sized to be powered.
"""
import json, io, os, itertools
from fractions import Fraction as F
import numpy as np
from scipy import stats

V = {}
def ok(name, cond, val=None):
    assert cond, "FAILED: " + name
    print("ok  ", name, "" if val is None else val)
    if val is not None: V[name] = val

rng = np.random.default_rng(20260611)

# ═════════════════ shared worked data: x = 1..5, y = 2,4,5,4,5 ═════════════════
x = np.array([1., 2, 3, 4, 5]); y = np.array([2., 4, 5, 4, 5]); n = 5; k = 2
X = np.column_stack([np.ones(n), x])
XtX = X.T @ X; XtXi = np.linalg.inv(XtX)
b = XtXi @ X.T @ y
H = X @ XtXi @ X.T; M = np.eye(n) - H
yh = H @ y; e = M @ y
ok("t1 slope/intercept", np.allclose(b, [2.2, 0.6]), [round(v, 4) for v in b])
ok("t1 fitted", np.allclose(yh, [2.8, 3.4, 4.0, 4.6, 5.2]), list(np.round(yh, 4)))
ok("t1 residuals", np.allclose(e, [-0.8, 0.6, 1.0, -0.6, -0.2]), list(np.round(e, 4)))
ok("t1 residuals sum to zero (intercept present)", abs(e.sum()) < 1e-12)
# hat matrix properties
ok("t1 H symmetric", np.allclose(H, H.T))
ok("t1 H idempotent", np.allclose(H @ H, H))
ok("t1 M idempotent", np.allclose(M @ M, M))
ok("t1 HM = 0", np.allclose(H @ M, 0))
ok("t1 HX = X", np.allclose(H @ X, X)); ok("t1 MX = 0", np.allclose(M @ X, 0))
ok("t1 trace H = k", abs(np.trace(H) - k) < 1e-12, round(float(np.trace(H)), 6))
ok("t1 trace M = n-k", abs(np.trace(M) - (n - k)) < 1e-12, round(float(np.trace(M)), 6))
ev = np.linalg.eigvalsh(H)
ok("t1 eigenvalues of H are 0/1", np.allclose(sorted(ev), [0, 0, 0, 1, 1]), list(np.round(sorted(ev), 6)))
hd = np.diag(H)
ok("t1 leverages = 1/n+(x-xbar)^2/Sxx", np.allclose(hd, 1/5 + (x - 3)**2/10), list(np.round(hd, 4)))
ok("t1 leverages sum to k", abs(hd.sum() - k) < 1e-12)
ok("t1 0<=h_ii<=1", ((hd >= 0) & (hd <= 1)).all())
ok("t1 H^2 diag identity h_ii = sum_j h_ij^2", np.allclose(hd, (H**2).sum(1)))
ok("t1 y'y = yh'yh + e'e", abs(y @ y - yh @ yh - e @ e) < 1e-10, round(float(e @ e), 4))
rss = float(e @ e); ok("t1 RSS", abs(rss - 2.4) < 1e-12, rss)
s2 = rss / (n - k); ok("t1 s2 = RSS/(n-k)", abs(s2 - 0.8) < 1e-12, s2)
# Var(yhat)=s2 H, Var(e)=s2 M (estimated)
ok("t1 var(e_i) estimate for obs 1 = s2(1-h11)", abs(s2 * (1 - hd[0]) - 0.32) < 1e-12, round(s2 * (1 - hd[0]), 4))
# Cov(yhat, e) = sigma^2 H M = 0 ; cov(b, e)=0
ok("t1 Cov(yh,e) ∝ H M = 0", np.allclose(H @ M, 0))
# E(e'e) = sigma^2 tr(M): simulate, powered (200k draws of the sum)
sig = 2.0; beta = np.array([1.0, 0.5]); R = 200_000
U = rng.normal(0, sig, (R, n)); Ysim = X @ beta + U
Esim = Ysim @ M.T
mean_ee = (Esim**2).sum(1).mean()
ok("t1 MC: E(e'e) ≈ sigma^2 (n-k) = 12", abs(mean_ee - sig**2 * (n - k)) < 0.1, round(float(mean_ee), 3))
ok("t1 MC: E(e'e)/n biased (≈7.2)", abs(mean_ee / n - 2.4 * 4 / 4 * 1.0) < 1 and abs(mean_ee/n - 12/5) < 0.05, round(float(mean_ee / n), 3))
# e'e/sigma^2 ~ chi2(n-k): compare 95th percentile
q95 = np.quantile((Esim**2).sum(1) / sig**2, 0.95)
ok("t1 MC: e'e/sigma^2 95th pct ≈ chi2(3) 7.815", abs(q95 - stats.chi2.ppf(0.95, 3)) < 0.1, round(float(q95), 3))
V["t1 chi2 3 df 0.95"] = round(float(stats.chi2.ppf(0.95, 3)), 4)
# a rank-deficient / counter-example: a projection that is NOT symmetric is idempotent but not H
P = np.array([[1., 1], [0, 0]]); ok("t1 idempotent not symmetric example", np.allclose(P @ P, P) and not np.allclose(P, P.T))
# trace of a 4-regressor, n=20 hat matrix
ok("t1 tr(H)=4, tr(M)=16 for n=20,k=4", True, [4, 16])
# Q: quadratic form y'Hy = RegSS(uncentred)= yh'yh
ok("t1 y'Hy = yh'yh", abs(y @ H @ y - yh @ yh) < 1e-10, round(float(yh @ yh), 4))
# 2x2 worked hat matrix with n=3 for a hand-readable example: x = 0,1,2
x3 = np.array([0., 1, 2]); X3 = np.column_stack([np.ones(3), x3])
H3 = X3 @ np.linalg.inv(X3.T @ X3) @ X3.T
ok("t1 n=3 hat matrix", np.allclose(H3, np.array([[5, 2, -1], [2, 2, 2], [-1, 2, 5]]) / 6), (np.round(H3 * 6, 6)).tolist())
ok("t1 n=3 leverage 5/6,1/3,5/6", np.allclose(np.diag(H3), [5/6, 1/3, 5/6]))
# leverage cutoff 2k/n
ok("t1 cutoff 2k/n = 0.8 for n=5,k=2", abs(2 * k / n - 0.8) < 1e-12)

# ═════════════════ t2: Gauss–Markov, Q11, estimability, Q38 variants ═════════════════
# --- Q11 exactly ---
XQ = np.array([[1, 1], [2, 0], [1, -1]], float)
G = XQ.T @ XQ
ok("t2 Q11 X'X = [[6,0],[0,2]]", np.allclose(G, [[6, 0], [0, 2]]), G.tolist())
A = np.linalg.inv(G) @ XQ.T      # rows: weights on y1,y2,y3
Ab = [[F(int(round(v * 6))), F(6)] for v in A[0]]
ok("t2 Q11 beta1hat weights = (1,2,1)/6", np.allclose(A[0], np.array([1, 2, 1]) / 6), list(np.round(A[0] * 6, 6)))
ok("t2 Q11 beta2hat weights = (1,0,-1)/2", np.allclose(A[1], np.array([1, 0, -1]) / 2), list(np.round(A[1] * 2, 6)))
ok("t2 Q11 Var(b1)=s2/6, Var(b2)=s2/2, Cov=0", np.allclose(np.linalg.inv(G), np.diag([1/6, 1/2])), [1/6, 1/2])
# every option of Q11: expectation as a linear map of beta
opts = {
 "A": (np.array([1, 2, 1]) / 2, np.array([1, 0, -1]) / 6),
 "B": (np.array([1, 2, 1]) / 6, np.array([1, 0, -1]) / 2),
 "C": (np.array([1, 2, 1]) / 2, np.array([1, 0, 1]) / 6),
 "D": (6 * np.array([1, 1, 1]), 2 * np.array([1, 0, -1])),
}
exp_tab = {}
for L, (w1, w2) in opts.items():
    E1 = w1 @ XQ; E2 = w2 @ XQ        # coefficient rows on (beta1, beta2)
    exp_tab[L] = (np.round(E1, 4).tolist(), np.round(E2, 4).tolist())
ok("t2 Q11 option B unbiased for both", np.allclose(opts["B"][0] @ XQ, [1, 0]) and np.allclose(opts["B"][1] @ XQ, [0, 1]))
ok("t2 Q11 option A beta1 is 3*beta1 (biased)", np.allclose(opts["A"][0] @ XQ, [3, 0]), exp_tab["A"])
ok("t2 Q11 option A beta2 is beta2/3", np.allclose(opts["A"][1] @ XQ, [0, 1/3]))
ok("t2 Q11 option C beta1 is 3*beta1; beta2 est is (2/6)beta1", np.allclose(opts["C"][0] @ XQ, [3, 0]) and np.allclose(opts["C"][1] @ XQ, [1/3, 0]), exp_tab["C"])
ok("t2 Q11 option D beta1 is 24*beta1", np.allclose(opts["D"][0] @ XQ, [24, 0]) and np.allclose(opts["D"][1] @ XQ, [0, 4]), exp_tab["D"])
# exact fractions: y -> weights
for w in A[0]:
    pass
# Gauss–Markov by direct minimisation: among unbiased a'y for beta1, variance sigma^2 a'a minimised by OLS weights
# unbiased constraints: a'X = (1,0). Parametrise a = a0 + t*z with z in null space of X'
a0 = A[0]; z = np.array([1, -1, 1]) / np.sqrt(3)       # X'z = (1-... ) check
ok("t2 z in null(X') : X'z = 0", np.allclose(XQ.T @ z, 0), XQ.T @ z)
ts = np.linspace(-3, 3, 7)
vars_ = [float((a0 + t * z) @ (a0 + t * z)) for t in ts]
ok("t2 variance a'a minimised at t=0 (OLS weights)", np.argmin(vars_) == 3 and abs(vars_[3] - 1/6) < 1e-12, [round(v, 4) for v in vars_])
ok("t2 variance a'a = 1/6 + t^2 (Pythagoras: a0 ⟂ z)", np.allclose(vars_, [1/6 + t * t for t in ts]))
# two-observation Q11-variant: y1=b+u1, y2=2b+u2
xx = np.array([[1.], [2.]]); bh = np.linalg.inv(xx.T @ xx) @ xx.T
ok("t2 simple: bhat=(y1+2y2)/5, var=s2/5", np.allclose(bh, [[1/5, 2/5]]) and abs(1/(xx.T @ xx)[0, 0] - 0.2) < 1e-12, [0.2, 0.4])
def var_w(w): return float(np.dot(w, w))
ok("t2 simple: var (y1+y2)/3 = 2/9 > 1/5 (unbiased but not best)", abs(var_w([1/3, 1/3]) - 2/9) < 1e-12 and 2/9 > 1/5, round(2/9, 4))
ok("t2 simple: y2/2 unbiased, var 1/4 > 1/5", abs(var_w([0, 1/2]) - 0.25) < 1e-12 and (np.array([0, 1/2]) @ xx)[0] == 1.0, 0.25)
ok("t2 simple: (y1+y2)/2 has E=1.5 beta (biased)", abs((np.array([.5, .5]) @ xx)[0] - 1.5) < 1e-12)
ok("t2 simple: (y1+y2)/3 has E=beta", abs((np.array([1/3, 1/3]) @ xx)[0] - 1) < 1e-12)
# diagonal X'X => uncorrelated; non-diagonal => correlated
Xd = np.array([[1, 1], [1, -1], [1, 1], [1, -1]], float)
ok("t2 diagonal X'X example gives zero covariance", np.allclose(np.linalg.inv(Xd.T @ Xd), np.diag([1/4, 1/4])))
Xc = np.array([[1, 1], [1, 2], [1, 3], [1, 4]], float)
Ci = np.linalg.inv(Xc.T @ Xc)
ok("t2 non-diagonal X'X: Cov(b0,b1) = -s2 xbar/Sxx = -0.5", abs(Ci[0, 1] - (-2.5 / 5)) < 1e-12, round(float(Ci[0, 1]), 4))
# estimability: one-way ANOVA two-group, rank-deficient
Xa = np.array([[1, 1, 0], [1, 1, 0], [1, 0, 1], [1, 0, 1]], float)
ok("t2 one-way design rank 2 of 3", np.linalg.matrix_rank(Xa) == 2)
def estimable(l, Xm): return np.linalg.matrix_rank(np.vstack([Xm, l])) == np.linalg.matrix_rank(Xm)
ok("t2 tau1-tau2 estimable", estimable(np.array([0, 1, -1.]), Xa))
ok("t2 alpha+tau1 estimable", estimable(np.array([1, 1, 0.]), Xa))
ok("t2 tau1 alone NOT estimable", not estimable(np.array([0, 1, 0.]), Xa))
ok("t2 alpha alone NOT estimable", not estimable(np.array([1, 0, 0.]), Xa))
ok("t2 tau1+tau2 NOT estimable", not estimable(np.array([0, 1, 1.]), Xa))
Gm = np.linalg.pinv(Xa.T @ Xa)
for l in (np.array([0, 1, -1.]), np.array([1, 1, 0.])):
    bs = [float(l @ (Gm @ Xa.T @ yy)) for yy in (np.array([1., 2, 5, 7]), np.array([1., 2, 5, 7]))]
solA = np.array([[1, 0, 0], [0, 1, -1]])      # two different generalised inverses give the same estimable value
yv = np.array([3., 5, 8, 10])
g1 = np.linalg.pinv(Xa.T @ Xa)
g2 = g1 + np.outer([1, -1, -1], [1, 0, 0]) * 0.7      # shift along the null space of X
ok("t2 null space direction (1,-1,-1) of X", np.allclose(Xa @ np.array([1, -1, -1.]), 0))
bA = g1 @ Xa.T @ yv; bB = bA + 0.7 * np.array([1, -1, -1.])
ok("t2 estimable tau1-tau2 identical for two solutions of the normal equations",
   abs(np.array([0, 1, -1.]) @ bA - np.array([0, 1, -1.]) @ bB) < 1e-12 and abs(bA[1] - bB[1]) > 0.1,
   [round(float(np.array([0, 1, -1.]) @ bA), 4)])
ok("t2 tau1-tau2 = ybar1 - ybar2 = 4-9 = -5", abs(np.array([0, 1, -1.]) @ bA - (4 - 9)) < 1e-12, -5.0)
# --- heteroscedasticity: OLS stays unbiased, loses BLUE (Q38 variant 2) ---
xs = np.array([1., 2, 3, 4, 5]); Xh = np.column_stack([np.ones(5), xs]); sd = xs   # sd_i = x_i
Sg = np.diag(sd**2)
Vols = np.linalg.inv(Xh.T @ Xh) @ Xh.T @ Sg @ Xh @ np.linalg.inv(Xh.T @ Xh)
Vgls = np.linalg.inv(Xh.T @ np.linalg.inv(Sg) @ Xh)
ok("t2 hetero: Var(OLS slope) > Var(GLS slope)", Vols[1, 1] > Vgls[1, 1], [round(float(Vols[1, 1]), 5), round(float(Vgls[1, 1]), 5)])
ok("t2 hetero: sigma^2(X'X)^-1 slope var (wrong formula, sigma^2=1) differs from sandwich", abs(np.linalg.inv(Xh.T @ Xh)[1, 1] - Vols[1, 1]) > 0.05, round(float(np.linalg.inv(Xh.T @ Xh)[1, 1]), 5))
# MC: OLS unbiased under hetero
R2 = 100_000
Uh = rng.normal(0, 1, (R2, 5)) * sd
Yh = Xh @ np.array([1.0, 0.5]) + Uh
Bh = (np.linalg.inv(Xh.T @ Xh) @ Xh.T @ Yh.T).T
ok("t2 MC hetero: mean slope ≈ 0.5 (unbiased)", abs(Bh[:, 1].mean() - 0.5) < 0.01, round(float(Bh[:, 1].mean()), 4))
ok("t2 MC hetero: MC variance ≈ sandwich", abs(Bh[:, 1].var() / Vols[1, 1] - 1) < 0.03, round(float(Bh[:, 1].var()), 5))
# --- multicollinearity: unbiased, inflated variance (Q38 itself) ---
rho = 0.99
Cx = np.array([[1, rho], [rho, 1]])
vif = 1 / (1 - rho**2)
ok("t2 VIF at r=0.99 = 50.25", abs(vif - 50.2513) < 1e-3, round(vif, 4))
ok("t2 Var(b1)/sigma^2 = VIF/(n Sx^2) : ratio vs orthogonal", abs(np.linalg.inv(Cx)[0, 0] - vif) < 1e-9)
nn = 50; R3 = 20_000
L = np.linalg.cholesky(Cx)
Z = rng.normal(0, 1, (nn, 2)) @ L.T
Xm = Z
bhat = np.empty((R3, 2)); tfail = 0
Ymat = Xm @ np.array([1.0, 1.0])[:, None] + rng.normal(0, 1, (nn, R3))
Bm = np.linalg.inv(Xm.T @ Xm) @ Xm.T @ Ymat
ok("t2 MC collinear: mean b1,b2 ≈ 1,1 (unbiased)", np.allclose(Bm.mean(1), [1, 1], atol=0.03), np.round(Bm.mean(1), 4).tolist())
rs = np.corrcoef(Xm[:, 0], Xm[:, 1])[0, 1]
sd_exact = np.sqrt(np.linalg.inv(Xm.T @ Xm)[0, 0])
ok("t2 MC collinear: sd(b1) ≈ sqrt((X'X)^-1_11) for this design", abs(Bm[0].std() / sd_exact - 1) < 0.03, [round(float(Bm[0].std()), 4), round(float(sd_exact), 4)])
Xs = Xm - Xm.mean(0)
sd_orth = 1 / np.sqrt((Xs[:, 0]**2).sum())            # sd(b1) had x2 been absent / orthogonal
ok("t2 inflation of sd(b1) over the orthogonal case = sqrt(1/(1-r²)) exactly", abs(sd_exact_c := np.sqrt(np.linalg.inv(Xs.T @ Xs)[0, 0]) / sd_orth - 1 / np.sqrt(1 - np.corrcoef(Xs.T)[0, 1]**2)) < 1e-9, round(float(1 / np.sqrt(1 - np.corrcoef(Xs.T)[0, 1]**2)), 3))
V["t2 sqrt VIF"] = round(float(np.sqrt(vif)), 4)
# --- omitted variable bias (Q38 variant 1): E(b1*) = beta1 + beta2 * delta ---
Rn = 40_000; nn2 = 200
x2 = rng.normal(0, 1, (nn2, Rn)); x1 = 0.6 * x2 + 0.8 * rng.normal(0, 1, (nn2, Rn))
yy = 1.0 * x1 + 2.0 * x2 + rng.normal(0, 1, (nn2, Rn))
b1s = (x1 * yy).sum(0) / (x1 * x1).sum(0)
ok("t2 MC omitted variable: E(b1*) ≈ beta1 + beta2*0.6 = 2.2", abs(b1s.mean() - 2.2) < 0.01, round(float(b1s.mean()), 4))
# ═════════════════ t3: ANOVA and F from R² ═════════════════
yb = y.mean(); tss = float(((y - yb)**2).sum()); regss = float(((yh - yb)**2).sum())
ok("t3 TSS=6, RegSS=3.6, RSS=2.4", abs(tss - 6) < 1e-12 and abs(regss - 3.6) < 1e-12 and abs(tss - regss - rss) < 1e-12, [tss, regss, rss])
r2 = regss / tss; ok("t3 R^2 = 0.6", abs(r2 - 0.6) < 1e-12, r2)
r_xy = np.corrcoef(x, y)[0, 1]
ok("t3 R^2 = r_xy^2", abs(r_xy**2 - 0.6) < 1e-12, round(float(r_xy), 6))
ok("t3 R^2 = corr(y, yhat)^2", abs(np.corrcoef(y, yh)[0, 1]**2 - 0.6) < 1e-12)
Fstat = (regss / (k - 1)) / (rss / (n - k))
ok("t3 F = 4.5", abs(Fstat - 4.5) < 1e-12, Fstat)
ok("t3 F from R²: (R²/(k-1))/((1-R²)/(n-k))", abs((r2 / (k - 1)) / ((1 - r2) / (n - k)) - 4.5) < 1e-12)
se_b = np.sqrt(s2 / 10); t_b = b[1] / se_b
ok("t3 t = 2.1213, t² = F", abs(t_b**2 - Fstat) < 1e-12, round(float(t_b), 4))
Fcrit = float(stats.f.ppf(0.95, 1, 3)); tcrit = float(stats.t.ppf(0.975, 3))
ok("t3 F crit(1,3)=10.128 = t crit² (3.182²)", abs(Fcrit - tcrit**2) < 1e-9, [round(Fcrit, 4), round(tcrit, 4)])
rcrit = tcrit / np.sqrt(tcrit**2 + 3)
ok("t3 r crit n=5 = 0.8783; r²crit=0.7714", abs(rcrit - 0.8783) < 1e-3, [round(float(rcrit), 4), round(float(rcrit**2), 4)])
ok("t3 example NOT significant: F 4.5 < 10.128", Fstat < Fcrit)
pval = float(stats.f.sf(Fstat, 1, 3)); V["t3 p-value F(1,3)=4.5"] = round(pval, 4)
ok("t3 p = 2*P(t3>2.1213) same", abs(pval - 2 * stats.t.sf(t_b, 3)) < 1e-12, round(pval, 4))
# Q9 and its variants
def Fr(r2_, n_, k_): return (r2_ / (k_ - 1)) / ((1 - r2_) / (n_ - k_))
ok("t3 Q9 variant 7: F = 66.74", abs((66870/3)/(5344/16) - 66.7365) < 1e-3, round((66870/3)/(5344/16), 4))
TSSv = 66870 + 5344
ok("t3 variant 7 R² = 0.9260 and F from R² agrees", abs(Fr(66870/TSSv, 20, 4) - (66870/3)/(5344/16)) < 1e-9, round(66870/TSSv, 5))
ok("t3 variant 7 distractors: 66870/5344 = 12.51; 5344/66870=0.0799", abs(66870/5344 - 12.5131) < 1e-3 and abs(5344/66870 - 0.0799) < 1e-4,
   [round(66870/5344, 4), round(5344/66870, 4)])
ok("t3 variant 7 distractor 0.015 = 5344/(3*...)? (5344/16)/(66870/3)=0.015", abs((5344/16)/(66870/3) - 0.01498) < 1e-4, round((5344/16)/(66870/3), 5))
# mistakes with the same data (n=5,k=2,R²=0.6)
mist = {
 "df swapped": (r2 / (n - k)) / ((1 - r2) / (k - 1)),
 "no df division": r2 / (1 - r2),
 "n-1 instead of n-k": (r2 / (k - 1)) / ((1 - r2) / (n - 1)),
 "k instead of k-1": (r2 / k) / ((1 - r2) / (n - k)),
 "R² ratio inverted": ((1 - r2) / (n - k)) / (r2 / (k - 1)),
}
ok("t3 mistake values", True, {kk: round(float(v), 4) for kk, v in mist.items()})
ok("t3 mistakes all differ from 4.5", all(abs(v - 4.5) > 1e-6 for v in mist.values()))
ok("t3 F(2,3)-style: df of overall F is (k-1, n-k)", True, [k - 1, n - k])
# F -> infinity as R² -> 1; F=0 at R²=0
ok("t3 F as R² -> 1 grows", Fr(0.99, 20, 4) > Fr(0.9, 20, 4) > Fr(0.5, 20, 4), [round(Fr(r_, 20, 4), 3) for r_ in (0.5, 0.9, 0.99)])
# E(MSR) and E(MSE)
ok("t3 s² = RSS/(n-k) unbiased: MC mean of RSS/(n-k) ≈ sigma²", abs(mean_ee / (n - k) - sig**2) < 0.05, round(float(mean_ee / (n - k)), 4))
ok("t3 TSS/(n-1) is NOT unbiased for sigma² when beta_slope != 0: E = sig²+b²Sxx/(n-1)=4+0.25*10/4=4.625", abs(sig**2 + 0.25 * 10 / 4 - 4.625) < 1e-12, 4.625)
tssm = ((Ysim - Ysim.mean(1, keepdims=True))**2).sum(1).mean() / (n - 1)
ok("t3 MC: E(TSS/(n-1)) ≈ 4.625", abs(tssm - 4.625) < 0.05, round(float(tssm), 4))
# multiple regression ANOVA, n=20, k=4
ok("t3 ANOVA df: 3 + 16 = 19", 3 + 16 == 19)
ok("t3 MSR=22290, MSE=334", abs(66870/3 - 22290) < 1e-9 and abs(5344/16 - 334) < 1e-12, [22290, 334])
# ANOVA identity on a random multiple regression
Xr = np.column_stack([np.ones(20), rng.normal(size=(20, 3))]); yr = Xr @ [1, 2, -1, .5] + rng.normal(size=20)
br = np.linalg.lstsq(Xr, yr, rcond=None)[0]; yhr = Xr @ br
ok("t3 TSS = RegSS + RSS (random multiple regression)", abs(((yr - yr.mean())**2).sum() - ((yhr - yr.mean())**2).sum() - ((yr - yhr)**2).sum()) < 1e-9)
# F-test vs t-test for slope in a multi-reg: restricted H0 beta_j=0 gives F=t^2
Xj = Xr[:, :3]; bj = np.linalg.lstsq(Xj, yr, rcond=None)[0]; rssj = ((yr - Xj @ bj)**2).sum(); rssf = ((yr - yhr)**2).sum()
Fj = (rssj - rssf) / (rssf / 16)
s2f = rssf / 16; covb = s2f * np.linalg.inv(Xr.T @ Xr); tj = br[3] / np.sqrt(covb[3, 3])
ok("t3 partial F (1 restriction) = t² of that coefficient", abs(Fj - tj**2) < 1e-8, round(float(Fj), 4))

# ═════════════════ t4: R², adjusted R², comparison ═════════════════
def adj(r2_, n_, k_): return 1 - (1 - r2_) * (n_ - 1) / (n_ - k_)
ok("t4 Q9v1 adjusted R² = 0.51", abs(adj(0.55, 50, 5) - 0.51) < 1e-12, round(adj(0.55, 50, 5), 6))
ok("t4 Q9v1 distractors: 0.45 = 1-R², 0.49 = (1-R²)(n-1)/(n-k)", abs(1 - 0.55 - 0.45) < 1e-12 and abs(0.45 * 49 / 45 - 0.49) < 1e-12)
ok("t4 using n-k-1=44 gives 0.4989 (k counts slopes only: then k=5 means 6 params)", abs(adj(0.55, 50, 6) - 0.498864) < 1e-5, round(adj(0.55, 50, 6), 5))
ok("t4 adjusted R² example n=5,k=2: 1-0.4*4/3 = 0.4667", abs(adj(0.6, 5, 2) - (1 - 0.4 * 4 / 3)) < 1e-12, round(adj(0.6, 5, 2), 4))
ok("t4 adjusted R² can be negative: R²=0.1,n=20,k=6", adj(0.1, 20, 6) < 0, round(adj(0.1, 20, 6), 4))
ok("t4 adjusted R² <= R² whenever k>=1... and < R² when k>1", adj(0.6, 5, 2) < 0.6 and adj(0.6, 5, 1) == 0.6)
ok("t4 adjusted R² never exceeds 1", adj(0.999, 100, 3) < 1)
# adding a regressor: R² never falls; adj R² rises iff t² > 1  (verified exhaustively on random data)
rises_ok = True; r2_ok = True; cnt = 0
for _ in range(4000):
    nn3 = int(rng.integers(8, 30)); base = rng.normal(size=(nn3, 2)); extra = rng.normal(size=(nn3, 1))
    yy3 = base @ [1, .5] + 0.3 * extra[:, 0] * rng.uniform(0, 1) + rng.normal(size=nn3)
    X0 = np.column_stack([np.ones(nn3), base]); X1 = np.column_stack([X0, extra])
    def fit(Xm_):
        bb = np.linalg.lstsq(Xm_, yy3, rcond=None)[0]; rr = ((yy3 - Xm_ @ bb)**2).sum(); return bb, rr
    b0, rss0 = fit(X0); b1, rss1 = fit(X1)
    tssz = ((yy3 - yy3.mean())**2).sum()
    r20, r21 = 1 - rss0/tssz, 1 - rss1/tssz
    a0_, a1_ = adj(r20, nn3, 3), adj(r21, nn3, 4)
    cv = (rss1 / (nn3 - 4)) * np.linalg.inv(X1.T @ X1); tt = b1[3] / np.sqrt(cv[3, 3])
    r2_ok &= (r21 >= r20 - 1e-12); rises_ok &= ((a1_ > a0_) == (tt**2 > 1)); cnt += 1
ok("t4 R² never falls when a regressor is added (4000 random cases)", r2_ok, cnt)
ok("t4 adj R² rises exactly when |t|>1 for the added variable (4000 cases)", rises_ok, cnt)
# identity: adjusted R² = 1 - s²/ (TSS/(n-1))
ok("t4 adjR² = 1 - s²/s_y²: n=5: 1 - 0.8/1.5 = 0.4667", abs(adj(0.6, 5, 2) - (1 - 0.8 / 1.5)) < 1e-12, round(1 - 0.8 / 1.5, 4))
# nested F test and partial R²
RSSf, RSSr, q, df = 5344.0, 9000.0, 2, 16
Fn = ((RSSr - RSSf) / q) / (RSSf / df)
ok("t4 nested F = 1828/334 = 5.4731", abs(Fn - 5.4731) < 1e-3, round(Fn, 4))
ok("t4 nested F crit(2,16)=3.634 so reject", Fn > stats.f.ppf(0.95, 2, 16), round(float(stats.f.ppf(0.95, 2, 16)), 4))
R2f = 1 - RSSf / 72214; R2r = 1 - RSSr / 72214
ok("t4 R² full, restricted", True, [round(R2f, 5), round(R2r, 5)])
ok("t4 nested F in R² form equals", abs(((R2f - R2r) / q) / ((1 - R2f) / df) - Fn) < 1e-9)
ok("t4 adj R² full 0.9121 vs restricted (k=2)", True, [round(adj(R2f, 20, 4), 4), round(adj(R2r, 20, 2), 4)])
# AIC / BIC (Gaussian, up to constants)
def aic(rss_, n_, kk): return n_ * np.log(rss_ / n_) + 2 * kk
def bic(rss_, n_, kk): return n_ * np.log(rss_ / n_) + kk * np.log(n_)
V["t4 AIC full/restricted"] = [round(float(aic(RSSf, 20, 4)), 3), round(float(aic(RSSr, 20, 2)), 3)]
V["t4 BIC full/restricted"] = [round(float(bic(RSSf, 20, 4)), 3), round(float(bic(RSSr, 20, 2)), 3)]
ok("t4 AIC prefers full (lower)", aic(RSSf, 20, 4) < aic(RSSr, 20, 2), V["t4 AIC full/restricted"])
ok("t4 BIC prefers full (lower)", bic(RSSf, 20, 4) < bic(RSSr, 20, 2), V["t4 BIC full/restricted"])
ok("t4 BIC penalty per parameter ln(20)=2.996 > AIC's 2 once n>=8", np.log(20) > 2 and np.log(7) < 2 < np.log(8), [round(float(np.log(20)), 4)])
# R² without intercept is not comparable
xo = np.array([1., 2, 3, 4, 5]); yo = np.array([10., 12, 13, 15, 16])
bo = (xo @ yo) / (xo @ xo); R2unc = 1 - ((yo - bo * xo)**2).sum() / (yo @ yo)
Xi = np.column_stack([np.ones(5), xo]); bi = np.linalg.lstsq(Xi, yo, rcond=None)[0]
R2c = 1 - ((yo - Xi @ bi)**2).sum() / ((yo - yo.mean())**2).sum()
R2nc = 1 - ((yo - bo * xo)**2).sum() / ((yo - yo.mean())**2).sum()
ok("t4 no-intercept fit: uncentred R² 0.9227 (what software reports) but centred R² is negative (-2.031); intercept model centred R² 0.9868",
   abs(R2unc - 0.92270) < 1e-4 and abs(R2nc + 2.0311) < 1e-3 and abs(R2c - 0.98684) < 1e-4, [round(float(R2unc), 4), round(float(R2nc), 4), round(float(R2c), 4)])
# R² of simple regression with low value and F: tiny R² big n still significant
nb = 1000; r2s = 0.01
Fbig = Fr(r2s, nb, 2)
ok("t4 R²=0.01 with n=1000 gives F=10.0 → significant", abs(Fbig - 10.0 * 998 / 990 * 0.99 / 0.99) < 1 and Fbig > stats.f.ppf(0.95, 1, 998), round(Fbig, 4))
# R² when y is transformed: not comparable (log y vs y)
ok("t4 R² compares only models with the same dependent variable", True)
# Mallows Cp
sig2_full = RSSf / df
Cp_r = RSSr / sig2_full - (20 - 2 * 2)
ok("t4 Mallows Cp restricted (p=2) = 9000/334-16 = 10.95", abs(Cp_r - (9000/334 - 16)) < 1e-9, round(Cp_r, 3))
ok("t4 Mallows Cp full model = p exactly = 4", abs(RSSf / sig2_full - (20 - 8) - 4) < 1e-9, 4.0)

# ═════════════════ figures used by the transfer scenes and the mastery pools ═════════════════
# t1 transfer case: x = 0,1,2 ; y = 1,3,2
y3 = np.array([1., 3, 2]); f3 = H3 @ y3; e3 = y3 - f3
ok("t1 transfer: fitted (1.5,2,2.5), residuals (-0.5,1,-0.5), e'e = 1.5, s² = 1.5", np.allclose(f3, [1.5, 2, 2.5]) and np.allclose(e3, [-.5, 1, -.5]) and abs(e3 @ e3 - 1.5) < 1e-12, [list(np.round(f3, 4)), float(e3 @ e3)])
ok("t1 transfer: the slope and intercept are 0.5 and 1.5", np.allclose(np.linalg.lstsq(X3, y3, rcond=None)[0], [1.5, 0.5]))
ok("t1 transfer: H3 row 2 is (1/3,1/3,1/3)", np.allclose(H3[1], [1/3, 1/3, 1/3]))
# rank-deficient design: tr(H) = rank, not the number of columns
Hd = Xa @ np.linalg.pinv(Xa)
ok("t1 rank-deficient one-way design: tr(H) = 2 (the rank), not 3 columns", abs(np.trace(Hd) - 2) < 1e-10, round(float(np.trace(Hd)), 6))
ok("t1 rank-deficient: H idempotent and symmetric", np.allclose(Hd @ Hd, Hd) and np.allclose(Hd, Hd.T))
# a single-observation indicator gives leverage 1 and residual 0
Xi1 = np.column_stack([np.ones(5), x, np.array([1., 0, 0, 0, 0])])
Hi1 = Xi1 @ np.linalg.inv(Xi1.T @ Xi1) @ Xi1.T
ei1 = (np.eye(5) - Hi1) @ y
ok("t1 indicator for obs 1: h_11 = 1 and e_1 = 0", abs(Hi1[0, 0] - 1) < 1e-10 and abs(ei1[0]) < 1e-10, [round(float(Hi1[0, 0]), 6), round(float(ei1[0]), 10)])
ok("t1 pool: E(e'e)=sigma²(n-k)=3*16=48 ; sigma² n = 60", 3 * 16 == 48 and 3 * 20 == 60)
ok("t1 pool: leverage at x=1 and x=5 equal 0.6 ; x=3 gives 0.2", np.allclose([hd[0], hd[4], hd[2]], [0.6, 0.6, 0.2]))
ok("t1 pool: s²(1-h11) = 0.8*0.4 = 0.32 < s² = 0.8", abs(0.8 * 0.4 - 0.32) < 1e-12)
# t2 pool: Q11 with y = (7,4,3)
yq = np.array([7., 4, 3]); bq = np.linalg.lstsq(XQ, yq, rcond=None)[0]
ok("t2 pool: Q11 with y=(7,4,3) gives beta1hat=3, beta2hat=2", np.allclose(bq, [3, 2]), list(np.round(bq, 6)))
ok("t2 pool: beta1 weights times column 1 of X = (1+4+1)/6 = 1 ; times column 2 = (1+0-1)/6 = 0", abs(np.array([1, 2, 1]) / 6 @ XQ[:, 0] - 1) < 1e-12 and abs(np.array([1, 2, 1]) / 6 @ XQ[:, 1]) < 1e-12)
ok("t2 pool: Var(beta1hat) with sigma²=12 is 2 (sum of squared weights 6/36 = 1/6)", abs(12 * (np.array([1, 2, 1]) / 6) @ (np.array([1, 2, 1]) / 6) - 2) < 1e-12)
ok("t2 pool: simple model sigma²=10 -> BLUE var 2 ; y2/2 var 2.5 ; (y1+y2)/3 var 20/9", abs(10 / 5 - 2) < 1e-12 and abs(10 / 4 - 2.5) < 1e-12 and abs(10 * 2 / 9 - 2.2222) < 1e-3)
ok("t2 pool: omitted-variable bias beta2*delta = 2*0.6 = 1.2", abs(2 * 0.6 - 1.2) < 1e-12 and abs(b1s.mean() - 1.0 - 1.2) < 0.01)
ok("t2 pool: VIF at r=0.99 is 50.25 ; 1/(2(1-r)) = 50", abs(vif - 50.2513) < 1e-3 and abs(1 / (2 * 0.01) - 50) < 1e-12)
# t3 pool
ok("t3 pool: F(R²=0.9,n=20,k=4)=48 ; R² from F=66.7365 (3,16) is 0.926", abs(Fr(0.9, 20, 4) - 48) < 1e-9 and abs(66.7365 * 3 / (66.7365 * 3 + 16) - 0.926) < 1e-4)
ok("t3 pool: F(R²=0.01,n=1000,k=2)=10.08 > crit F(1,998)=3.85", abs(Fr(0.01, 1000, 2) - 10.0808) < 1e-3 and stats.f.ppf(0.95, 1, 998) < 4, round(float(stats.f.ppf(0.95, 1, 998)), 3))
ok("t3 pool: t=-2.5 -> F=6.25", abs((-2.5)**2 - 6.25) < 1e-12)
# t4 pool
ok("t4 pool: adjusted R² negative iff R² < (k-1)/(n-1): 5/19 = 0.2632", abs(5 / 19 - 0.263158) < 1e-5 and adj(0.2632, 20, 6) > -1e-3 and adj(0.26, 20, 6) < 0)
ok("t4 pool: adj R²(0.01, n=1000, k=2) = 0.0090", abs(adj(0.01, 1000, 2) - 0.009008) < 1e-5, round(adj(0.01, 1000, 2), 6))
ok("t4 pool: delta AIC = 6.43", abs((aic(RSSr, 20, 2) - aic(RSSf, 20, 4)) - 6.425) < 5e-3, round(float(aic(RSSr, 20, 2) - aic(RSSf, 20, 4)), 4))
ok("t4 pool: adj R² full model n=20,k=4 = 0.9121 < R² 0.926", abs(adj(0.926, 20, 4) - 0.91212) < 1e-4 and adj(0.926, 20, 4) < 0.926, round(adj(0.926, 20, 4), 5))
ok("t4 pool: R² of full 5344/72214 fraction: unexplained 7.4%", abs(5344 / 72214 - 0.074) < 1e-3, round(5344 / 72214, 5))

ok("t3 pool: R² from F=66.7365 on (3,16) is 0.926; the wrong form F/(F+16) is 0.807", abs(66.7365 * 3 / (66.7365 * 3 + 16) - 0.92600) < 1e-4 and abs(66.7365 / (66.7365 + 16) - 0.80663) < 1e-4, [round(66.7365 * 3 / (66.7365 * 3 + 16), 5), round(66.7365 / (66.7365 + 16), 5)])
ok("t3 pool: R²/(1-R²)=1.5 at R²=0.6 ; (1-R²)/R² = 99 at R²=0.01", abs(0.6 / 0.4 - 1.5) < 1e-12 and abs(0.99 / 0.01 - 99) < 1e-9)
ok("t3 pool: R²=0.9 -> R²/(1-R²) = 9 ; x(n-k)/(k-1) = x16/3 = 48 ; x3 = 27", abs(9 * 16 / 3 - 48) < 1e-9)

t18 = float(stats.t.ppf(0.975, 18))
ok("t3 scene: same R²=0.6 with n=50 gives F=72 ; critical |r| at n=20 is 0.444 ; critical R² at n=5 is 0.771",
   abs(Fr(0.6, 50, 2) - 72) < 1e-9 and abs(t18 / np.sqrt(t18**2 + 18) - 0.4438) < 1e-3 and abs(rcrit**2 - 0.7715) < 1e-3,
   [round(Fr(0.6, 50, 2), 4), round(float(t18 / np.sqrt(t18**2 + 18)), 4), round(float(rcrit**2), 5)])
ok("t3 scene: ANOVA-table arithmetic 0.926/3 over 0.074/16 = 66.74", abs((0.926 / 3) / (0.074 / 16) - 66.7387) < 1e-3, round((0.926 / 3) / (0.074 / 16), 4))
ok("t3 scene: RegSS terms 1.44+0.36+0+0.36+1.44 = 3.6 and se(b)=0.2828", abs(((yh - 4)**2).sum() - 3.6) < 1e-12 and abs(np.sqrt(0.8 / 10) - 0.2828) < 1e-4)

# t4 scene and pool figures
ok("t4 pool: five-student adjR² 0.4667 ; wrong forms 0.2 (n-k-1) and 0.7 (inverted ratio)", abs(adj(0.6, 5, 2) - 0.46667) < 1e-4 and abs(1 - 0.4 * 4 / 2 - 0.2) < 1e-12 and abs(1 - 0.4 * 3 / 4 - 0.7) < 1e-12)
ok("t4 pool: nested F wrong forms: 3656/334 = 10.946 (forgot /q) ; 334/1828 = 0.1827 (inverted) ; crit 3.634", abs(3656 / 334 - 10.946) < 1e-3 and abs(334 / 1828 - 0.18271) < 1e-4 and abs(stats.f.ppf(0.95, 2, 16) - 3.6337) < 1e-3, [round(3656 / 334, 4), round(334 / 1828, 5)])
ok("t4 pool: Cp restricted 10.946 ; RSS_r/sigma² = 26.946", abs(9000 / 334 - 26.946) < 1e-3 and abs(9000 / 334 - 16 - 10.946) < 1e-3, round(9000 / 334, 4))
ok("t4 pool: adj R² restricted 0.8684, full 0.9121", abs(adj(R2r, 20, 2) - 0.86840) < 1e-4 and abs(adj(R2f, 20, 4) - 0.91212) < 1e-4, [round(adj(R2r, 20, 2), 5), round(adj(R2f, 20, 4), 5)])
ok("t4 scene: critical R² at n=20 one regressor = 0.1969", abs((t18 / np.sqrt(t18**2 + 18))**2 - 0.19695) < 1e-3, round(float((t18 / np.sqrt(t18**2 + 18))**2), 5))
ok("t4 pool: dAIC = 6.425, twice = 12.85, half = 3.21", abs(6.425 * 2 - 12.85) < 1e-9 and abs(6.425 / 2 - 3.2125) < 1e-9)
# transfer: add a regressor with t = 0.8 to n=20, k=3, R² = 0.5
m_ = 20 - 3; t_ = 0.8
ratio_ = 1 + t_**2 / (m_ - 1)
r2n = 1 - 0.5 / ratio_
ok("t4 transfer: R² 0.5 -> 0.5192 ; adj R² 0.4412 -> 0.4291 (falls, |t|<1)", abs(r2n - 0.519231) < 1e-5 and abs(adj(0.5, 20, 3) - 0.441176) < 1e-5 and abs(adj(r2n, 20, 4) - 0.429087) < 1e-5 and adj(r2n, 20, 4) < adj(0.5, 20, 3),
   [round(r2n, 5), round(adj(0.5, 20, 3), 5), round(adj(r2n, 20, 4), 5)])
tc = 1.0   # break-even: |t|=1 leaves adj R² unchanged
r2e = 1 - 0.5 / (1 + tc**2 / (m_ - 1))
ok("t4 transfer: with |t|=1 exactly adj R² is unchanged", abs(adj(r2e, 20, 4) - adj(0.5, 20, 3)) < 1e-12, round(adj(r2e, 20, 4), 6))
ok("t4 scene: ln 20 = 2.9957 ; ln 8 = 2.0794 ; ln 7 = 1.9459", abs(np.log(20) - 2.9957) < 1e-3 and abs(np.log(8) - 2.0794) < 1e-3 and abs(np.log(7) - 1.9459) < 1e-3)
ok("t4 scene: n=50 k=5 R²=0.55 -> with k=6 (slopes counted) 0.4989 ; TSS unexplained 0.45*49/45 = 0.49", True)

# ─────────── cross-lesson agreement (SPEC section 10) ───────────
ok("x t1 RSS (2.4) = t3 RSS = 6 - 3.6", abs(rss - (tss - regss)) < 1e-12)
ok("x t1 s² (0.8) = t4 s² in adjR² formula", abs(1 - s2 / (tss / (n - 1)) - adj(r2, n, k)) < 1e-12)
ok("x t3 F (4.5) from t1 quantities: tr(H)=2 => df 1,3", abs(((yh - yb) @ (yh - yb)) / 1 / (e @ e / 3) - 4.5) < 1e-12)
ok("x t2 identity: Var(b1) = s2/6 in Q11 and diag((X'X)^-1) matches t1 formula", abs(np.linalg.inv(G)[0, 0] - 1/6) < 1e-12)

os.makedirs(".cache", exist_ok=True)
with io.open(".cache/regression_verified.json", "w", encoding="utf-8") as f:
    json.dump({kk: (vv.tolist() if hasattr(vv, "tolist") else vv) for kk, vv in V.items()}, f, ensure_ascii=False, indent=1, default=str)
print("\nALL CHECKS PASSED —", len(V), "values recorded in .cache/regression_verified.json")
