"""Verify the DKW confidence-band example added to the EDF lesson."""

import math


def margin(n, alpha):
    return math.sqrt(math.log(2 / alpha) / (2 * n))


value = margin(50, 0.05)
assert round(value, 3) == 0.192
assert 0 < value < 1
print(f"PASS: n=50, alpha=0.05 gives epsilon={value:.12f} (rounded 0.192)")
