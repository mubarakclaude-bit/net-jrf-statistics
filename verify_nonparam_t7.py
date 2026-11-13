#!/usr/bin/env python3
"""Independent exact checks for empirical distribution function examples."""
from fractions import Fraction
from math import ceil

sample = [2, 3, 3, 4, 6]
assert Fraction(sum(x <= 3 for x in sample), len(sample)) == Fraction(3, 5)
assert Fraction(2, 10) == Fraction(1, 5)
assert Fraction(2, 8) == Fraction(1, 4)
F, n = Fraction(2, 5), 10
assert F * (1 - F) / n == Fraction(6, 250)
assert Fraction(3, 10) * (1 - Fraction(3, 10)) / 20 == Fraction(21, 2000)
assert Fraction(3, 10) * (1 - Fraction(6, 10)) / 10 == Fraction(12, 1000)
assert ceil(Fraction(3, 4) * 12) == 9
print("PASS EDF values, tie jumps, pointwise variance, covariance and inverse-CDF index")
