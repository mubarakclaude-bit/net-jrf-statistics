#!/usr/bin/env python3
"""Independent arithmetic checks for linear rank and scale-score examples."""
from fractions import Fraction
assert 28-Fraction(5*6,2)==13
assert 22-Fraction(4*5,2)==12
ab=[1,2,3,4,4,3,2,1]
assert sum(ab[i-1] for i in [1,2,7,8])==6
assert sum(ab[i-1] for i in [3,4,5,6])==14
mood=[(Fraction(i)-Fraction(9,2))**2 for i in range(1,9)]
assert sum(mood[i-1] for i in [1,2,7,8])==37
assert sum(mood[i-1] for i in [3,4,5,6])==5
assert (Fraction(4)-Fraction(9,2))**2==Fraction(1,4)
print("PASS Wilcoxon U conversions; Ansari–Bradley centre scores; Mood tail scores")
