"""Exact checks for the worked values added from the distribution sheet."""

from fractions import Fraction
from itertools import product
from math import comb, factorial


def multinomial_probability(counts, probabilities):
    n = sum(counts)
    coefficient = Fraction(factorial(n), 1)
    for count in counts:
        coefficient /= factorial(count)
    result = coefficient
    for count, probability in zip(counts, probabilities):
        result *= probability ** count
    return result


def check_discrete_uniform():
    values = range(2, 6)
    probabilities = [Fraction(1, 4)] * 4
    mean = sum(x * p for x, p in zip(values, probabilities))
    variance = sum((x - mean) ** 2 * p for x, p in zip(values, probabilities))
    assert sum(probabilities) == 1
    assert mean == Fraction(7, 2)
    assert variance == Fraction(5, 4)


def check_multinomial():
    probabilities = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    n = 4
    counts = [x for x in product(range(n + 1), repeat=3) if sum(x) == n]
    masses = {x: multinomial_probability(x, probabilities) for x in counts}
    assert sum(masses.values()) == 1
    assert masses[(2, 1, 1)] == Fraction(1, 6)

    means = [sum(x[i] * mass for x, mass in masses.items()) for i in range(3)]
    assert means == [Fraction(2), Fraction(4, 3), Fraction(2, 3)]
    covariance_01 = sum(
        (x[0] - means[0]) * (x[1] - means[1]) * mass
        for x, mass in masses.items()
    )
    assert covariance_01 == -Fraction(2, 3)

    # Combining categories 1 and 2 gives a Binomial(n, p1+p2) count.
    for k in range(n + 1):
        marginal = sum(mass for x, mass in masses.items() if x[0] + x[1] == k)
        binomial = comb(n, k) * (probabilities[0] + probabilities[1]) ** k * probabilities[2] ** (n - k)
        assert marginal == binomial


def check_affine_normal_example():
    mean = (Fraction(1), Fraction(2))
    covariance = ((Fraction(4), Fraction(1)), (Fraction(1), Fraction(9)))
    transform = (Fraction(1), Fraction(-1))
    offset = Fraction(2)

    transformed_mean = offset + sum(c * m for c, m in zip(transform, mean))
    transformed_variance = sum(
        transform[i] * covariance[i][j] * transform[j]
        for i in range(2)
        for j in range(2)
    )
    assert transformed_mean == 1
    assert transformed_variance == 11


if __name__ == "__main__":
    check_discrete_uniform()
    check_multinomial()
    check_affine_normal_example()
    print("Verified discrete uniform, multinomial and affine-normal examples exactly.")
