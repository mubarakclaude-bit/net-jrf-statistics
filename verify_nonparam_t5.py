#!/usr/bin/env python3
"""Independent arithmetic checks for test-selection numeric examples."""
from fractions import Fraction
from math import comb
# Sign-test effective sample size.
assert 12-3==9
# Runs-test null expectation.
ER=1+2*6*4/(6+4)
assert ER==5.8
# Mann-Whitney U sum.
assert 5*7==35
# KS maximum empirical/reference CDF gap.
gaps=[0.03,0.12,0.08,0.05]
assert max(gaps)==0.12
# Friedman total rank points for four blocks and three treatments.
assert 4*(3*4//2)==24
print("PASS sign-test m=9; runs E(R)=5.8; U sum=35; KS D=0.12; Friedman rank total=24")
