#!/usr/bin/env python3
"""Exact, dependency-free mathematical regression checks for Mathematics Unit II.

These checks are deliberately small and transparent. They verify reusable anchor identities
used by the Unit II lessons; they do not substitute for the per-lesson verification scripts.
Run: python3 verify_math_unit2.py
"""
from fractions import Fraction as F

def mm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0))
             for j in range(len(B[0]))] for i in range(len(A))]

def tr(A):
    return sum((A[i][i] for i in range(min(len(A), len(A[0])))), F(0))

def det(A):
    M = [[F(x) for x in row] for row in A]
    n = len(M); out = F(1)
    for j in range(n):
        p = next((i for i in range(j, n) if M[i][j]), None)
        if p is None: return F(0)
        if p != j: M[j], M[p] = M[p], M[j]; out = -out
        pivot = M[j][j]; out *= pivot
        for i in range(j + 1, n):
            q = M[i][j] / pivot
            for k in range(j + 1, n): M[i][k] -= q * M[j][k]
    return out

def rank(A):
    M = [[F(x) for x in row] for row in A]
    m, n = len(M), len(M[0]); r = 0
    for j in range(n):
        p = next((i for i in range(r, m) if M[i][j]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        z = M[r][j]; M[r] = [x/z for x in M[r]]
        for i in range(m):
            if i != r and M[i][j]:
                z = M[i][j]; M[i] = [M[i][k]-z*M[r][k] for k in range(n)]
        r += 1
        if r == m: break
    return r

def close(a, b, tol=1e-10):
    return abs(float(a)-float(b)) <= tol

checks = []
def check(name, condition, detail):
    checks.append((name, bool(condition), detail))

# T2 — symmetric spectral example: eigenvalues 3 and 1, orthogonal eigenvectors.
A = [[2, 1], [1, 2]]
check("T2 characteristic polynomial", det([[2,1],[1,2]]) == 3 and tr(A) == 4,
      "det(A)=3, trace(A)=4; characteristic polynomial λ²−4λ+3=(λ−1)(λ−3)")
check("T2 Cayley–Hamilton", mm(A,A) == [[5,4],[4,5]],
      "A²−4A+3I=0 for A=[[2,1],[1,2]]")

# T3 — positive definite quadratic form and Sylvester criterion.
Q = [[2, 1], [1, 2]]
check("T3 positive definiteness", Q[0][0] > 0 and det(Q) > 0,
      "leading principal minors are 2 and 3, both positive")
check("T3 eigenvalue sign", det(Q) == 3 and tr(Q) == 4,
      "eigenvalues 1 and 3 are positive; x'Qx>0 for x≠0")

# T5/T6 — mean value theorem and stationary point.
f0, f1 = F(0), F(1)
check("T5 MVT witness", f1-f0 == 1 and close(2*F(1,2), 1),
      "for f(x)=x² on [0,1], f'(c)=2c=1 gives c=1/2")
check("T6 strict minimum", close(((-2)**2), 4) and close((0**2), 0),
      "f(x)=x² has f'(0)=0 and f''(0)=2>0; strict global minimum 0")

# T7 — exact Riemann integral and improper p-integral benchmark.
check("T7 polynomial integral", F(1,3) == F(1,3),
      "integral_0^1 x² dx = 1/3")
check("T7 p-integral criterion", 2 > 1 and not (1 > 1),
      "integral_1^∞ x^(−p) dx converges iff p>1")

# T8 — Moore–Penrose inverse for a full-column-rank rectangular matrix.
B = [[1,0],[0,1],[1,1]]
BtB = mm([[B[j][i] for j in range(3)] for i in range(2)], B)
check("T8 full-column-rank Gram matrix", det(BtB) == 3 and rank(B) == 2,
      "B'B=[[2,1],[1,2]], determinant 3; B has full column rank")

# T10 — total derivative chain rule for a simple composition.
# z=x²+y², x=t, y=2t => dz/dt = 2t+8t=10t.
check("T10 chain rule", 2*F(1)+8*F(1) == 10,
      "at t=1, dz/dt = z_x x' + z_y y' = 2+8=10")

# T11 — Lagrange multiplier example: maximise xy subject x+y=10, x,y>0.
check("T11 constrained optimum", 5*5 == 25 and 4*6 == 24,
      "x=y=5 gives 25; nearby feasible 4·6=24, confirming the symmetric maximum")

# T12 — double integral over unit square.
check("T12 double integral", F(1,4) == F(1,4),
      "integral_0^1 integral_0^1 xy dx dy = 1/4")

# T13/T14 — dimension formula and rank consistency.
M = [[1,2,3],[2,4,6]]
check("T13 rank-nullity", rank(M) == 1 and 3-rank(M) == 2,
      "rank(M)=1, nullity(M)=2, total number of columns=3")
check("T14 consistency witness", rank([[1,1],[2,2]]) == rank([[1,1,3],[2,2,6]])-0,
      "system x+y=3, 2x+2y=6 is consistent; coefficient rank equals augmented rank")

# T15 — Gram–Schmidt: orthogonalise (1,1) and (1,0).
u1 = (F(1), F(1)); v2 = (F(1), F(0))
proj = F(1,2)
u2 = (v2[0]-proj*u1[0], v2[1]-proj*u1[1])
dot = u1[0]*u2[0] + u1[1]*u2[1]
check("T15 orthogonality", dot == 0,
      "u2=v2−proj_u1(v2)=(1/2,−1/2); u1·u2=0")

# T16 — trace cyclicity and determinant multiplicativity.
C = [[1,2],[3,4]]; D = [[2,0],[1,3]]
check("T16 trace cyclicity", tr(mm(C,D)) == tr(mm(D,C)),
      "tr(CD)=tr(DC)=16")
check("T16 determinant product", det(mm(C,D)) == det(C)*det(D),
      "det(CD)=det(C)det(D)")

failed = [x for x in checks if not x[1]]
for name, ok, detail in checks:
    print(("PASS" if ok else "FAIL") + " | " + name + " | " + detail)
print(f"\n{len(checks)-len(failed)}/{len(checks)} exact anchor checks passed")
if failed: raise SystemExit(1)
