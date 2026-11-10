#!/usr/bin/env python3
"""Independent exact-arithmetic checks for stochastic-t1 Markov-chain examples."""
from fractions import Fraction as F

P = [[F(1,2), F(1,2)], [F(1,4), F(3,4)]]
def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def add(A, B):
    return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def eq(A, B):
    assert A == B, (A, B)
assert all(x >= 0 for row in P for x in row)
assert all(sum(row) == 1 for row in P)
P2, P3 = mm(P,P), mm(mm(P,P),P)
eq(P2, [[F(3,8),F(5,8)],[F(5,16),F(11,16)]])
eq(P3, [[F(11,32),F(21,32)],[F(21,64),F(43,64)]])
# Chapman–Kolmogorov: P^(1+2) = P P^2 = P^3 = P^2 P.
eq(mm(P,P2), P3)
eq(mm(P2,P), P3)
# From state 1, after two steps: 3/8 in state 1, 5/8 in state 2.
assert P2[0] == [F(3,8),F(5,8)]
# Stationary row vector pi solves pi P = pi and sums to one.
pi = [F(1,3),F(2,3)]
assert [sum(pi[i]*P[i][j] for i in range(2)) for j in range(2)] == pi
assert sum(pi) == 1
# A different absorbing example: state 2 cannot be left.
A = [[F(1),F(0)],[F(2,5),F(3,5)]]
assert all(sum(row)==1 for row in A)
assert A[0] == [1,0]
print("PASS: stochastic rows; exact P^2 and P^3; Chapman–Kolmogorov both orders;")
print("PASS: two-step probabilities; stationary distribution; absorbing-state example.")
print("P^2 =", P2)
print("P^3 =", P3)
print("pi =", pi)
