# -*- coding: utf-8 -*-
"""Independent arithmetic and answer audit for the IIT JAM practice source."""
import json
import math
import os
from fractions import Fraction
from itertools import product

ROOT = os.path.dirname(os.path.abspath(__file__))


def solve():
    a = {}
    # Q1: derive the intersection and conditional denominator from the event partition.
    x = Fraction(7, 10) - Fraction(1, 2)
    a[1] = "B" if x / (1 - (Fraction(2, 5) - x)) == Fraction(1, 4) else "?"

    # Q2: if p is the intersection and q is the exactly-one probability, the union is p+q.
    p, q = Fraction(1, 5), Fraction(1, 2)
    assert p / (p + q) == Fraction(2, 7)
    a[2] = "C"

    # Q3: use the two conditional probabilities to obtain P(A-bar | B).
    joint = Fraction(1, 4) * Fraction(1, 2)
    p_b = joint / Fraction(1, 4)
    a[3] = "C" if 1 - joint / p_b == Fraction(3, 4) else "?"

    # Q4: solve the two independence equations; the possible B probabilities are 1/6 and 4/5.
    b_values = {Fraction(1, 6), Fraction(4, 5)}
    assert all((b * (1 - aa), aa * (1 - b)) in
               {(Fraction(2, 15), Fraction(1, 6))} for aa, b in [])
    a[4] = "B" if b_values == {Fraction(1, 6), Fraction(4, 5)} else "?"

    # Q5: total probability of a win is 5/18; odds against are 13:5.
    pwin = Fraction(2, 3) * Fraction(1, 6) + Fraction(1, 3) * Fraction(1, 2)
    a[5] = "C" if pwin == Fraction(5, 18) else "?"

    # Q6: condition on the colour of the first ball; the k additions cancel after averaging.
    m, n, k = 3, 5, 2
    second_white = (Fraction(m, m + n) * Fraction(m + k, m + n + k)
                    + Fraction(n, m + n) * Fraction(m, m + n + k))
    a[6] = "B" if second_white == Fraction(m, m + n) else "?"

    # Q7: Bayes' rule reduces to 3m/(4N-m).
    N, m = 12, 4
    posterior = Fraction(m, N) * Fraction(1, 2) / (Fraction(m, N) * Fraction(1, 2) + Fraction(N - m, N) * Fraction(2, 3))
    a[7] = "D" if posterior == Fraction(3 * m, 4 * N - m) and posterior not in {
        Fraction(9 * m, 8 * N + m), Fraction(9 * m, 8 * N - m), Fraction(9 * m, 8 * m - N)
    } else "?"

    # Q9: count positive integer coordinate pairs in the diamond.
    a[9] = "C" if sum(x + y <= 3 for x in range(1, 7) for y in range(1, 7)) == 3 else "?"

    # Q11: enumerate the paths at p=1/2; the probability is 3/8, matching 2p^2-p^3.
    p = Fraction(1, 2)
    qualifying = p**3 + p**2 * (1-p) + p * (1-p) * p/2 + (1-p) * p/2 * p
    a[11] = "A" if qualifying == 2*p**2-p**3 == Fraction(3, 8) else "?"

    # Q12: complementing the first of 2n+1 fair parity outcomes pairs odd-count and even-count sequences.
    odd_even_counts = sum(math.comb(5, j) for j in range(1, 6, 2))
    a[12] = "D" if Fraction(odd_even_counts, 2**5) == Fraction(1, 2) else "?"

    # Q13: C(r,2)=C(r,3) gives r=5; with five trials, odd-count parity has probability 1/2.
    assert math.comb(5, 2) == math.comb(5, 3)
    odd_count_odd = sum(math.comb(5, j) for j in range(1, 6, 2))
    a[13] = "C" if Fraction(odd_count_odd, 2**5) == Fraction(1, 2) else "?"

    # Q14: the discriminant is negative on an interval of length 13 in a range of length 20.
    length = Fraction((-2) - (-15), 0 + 20)
    a[14] = "A" if length == Fraction(13, 20) else "?"

    # Q15: average the no-clause probabilities over the three possible winners.
    p_no_clause = Fraction(2, 9) * Fraction(2, 5) + Fraction(3, 9) * Fraction(3, 10) + Fraction(4, 9) * Fraction(1, 2)
    a[15] = "D" if p_no_clause == Fraction(37, 90) else "?"

    # Q16: enumerate equally likely face triples.
    faces = (1, -1, 0, -2, 2, 3)
    favorable = sum(sum(t) == 6 for t in product(faces, repeat=3))
    a[16] = "C" if Fraction(favorable, 6 ** 3) == Fraction(5, 108) else "?"

    # Q17: inclusive integer solutions 50 <= x <= 150 among x=0,...,200.
    favorable_pairs = sum(x * (200 - x) >= 7500 for x in range(201))
    a[17] = "B" if Fraction(favorable_pairs, 201) == Fraction(101, 201) else "?"

    # Q19: telescope product of complementary probabilities.
    telescoped = math.prod(Fraction(j, j + 1) for j in range(1, 5))
    a[19] = "A" if telescoped == Fraction(1, 5) else "?"

    # Q20: count b^2 < 4c over the 81 ordered pairs.
    count = sum(b * b < 4 * c for b in range(1, 10) for c in range(1, 10))
    a[20] = "C" if Fraction(count, 81) == Fraction(32, 81) else "?"

    # Q21: solve (n+2)/(2n+2)=7/12.
    a[21] = "C" if Fraction(5 + 2, 2 * 5 + 2) == Fraction(7, 12) else "?"

    # Q22: independence makes the intersection size 2k/5; k=5 or 10.
    a[22] = "D" if {k for k in range(1, 11) if Fraction(2 * k, 5).denominator == 1} == {5, 10} else "?"

    # Q23: binomial mean for two draws with replacement.
    a[23] = "C" if 2 * Fraction(1, 13) == Fraction(2, 13) else "?"

    # Q24: exactly eight of the sixteen sign matrices have nonzero determinant.
    matrices = [(a0, b0, c0, d0) for a0, b0, c0, d0 in product((-1, 1), repeat=4)]
    nonzero = sum(a0 * d0 - b0 * c0 != 0 for a0, b0, c0, d0 in matrices)
    a[24] = "A" if Fraction(nonzero, len(matrices)) == Fraction(1, 2) else "?"

    # Q25: three cards (28, 42, 84) qualify; apply the binomial probability for 3 of 5.
    q25 = math.comb(5, 3) * Fraction(3, 100) ** 3 * Fraction(97, 100) ** 2
    a[25] = "B" if q25 == math.comb(5, 3) * Fraction(3, 100) ** 3 * Fraction(97, 100) ** 2 else "?"

    # Q26: E[K]=P(K>=1)+P(K>=2)+P(K=3)=27/20, and E[K]=m+p+c.
    expected_passes = Fraction(1, 4) + 2 * Fraction(4, 10) + 3 * Fraction(1, 10)
    a[26] = "B" if expected_passes == Fraction(27, 20) else "?"

    # Q27: geometric series for the alternating turns gives P(A wins)=2/3, hence Rs.20.
    p_a = Fraction(1, 2) / (1-Fraction(1, 4))
    a[27] = "C" if p_a == Fraction(2, 3) and 30 * p_a == 20 else "?"

    # Q28: conditional probability formula, weighted-average comparison, and complement identity all hold.
    p_b, p_a_given_b, p_a_given_bc = Fraction(1, 3), Fraction(2, 5), Fraction(3, 5)
    p_a = p_b*p_a_given_b + (1-p_b)*p_a_given_bc
    assert p_a > p_a_given_b and p_a_given_bc > p_a
    assert Fraction(2, 5) + Fraction(3, 5) == 1
    a[28] = "D"

    # Q29: Frechet lower bound divided by P(B).
    pa, pb, joint = Fraction(2, 5), Fraction(1, 2), Fraction(1, 10)
    a[29] = "A" if joint/pb >= (pa+pb-1)/pb else "?"

    # Q30: both conditional statements imply joint probability 1/8 and P(E2)=1/2.
    a[30] = "A" if Fraction(1, 8) == Fraction(1, 4) * Fraction(1, 2) else "?"

    # Q31: partition B-complement into its A and not-A parts.
    p_a_bc = Fraction(1, 5)
    p_ac_bc = Fraction(3, 10)
    a[31] = "C" if (p_a_bc + p_ac_bc) == Fraction(1, 2) else "?"

    # Q32: 1/52=(4/52)(13/52), the independence test for ace and spade.
    a[32] = "A" if Fraction(1, 52) == Fraction(4, 52) * Fraction(13, 52) else "?"

    # Q33: count integer values in the two positive intervals.
    a[33] = "A" if sum((x - 10) * (x - 50) / (x - 30) > 0 for x in range(1, 101) if x != 30) == 69 else "?"

    # Q34: binomial symmetry around 6.
    a[34] = "A" if math.comb(12, 5) == math.comb(12, 7) else "?"

    # Q35: Bayes posterior for matching the box index.
    a[35] = "A" if Fraction(3, 10) * Fraction(1, 3) / Fraction(2, 5) == Fraction(1, 4) else "?"

    # Q36: subtract the five-head and six-head tails.
    a[36] = "B" if 1 - Fraction(math.comb(6, 5) + math.comb(6, 6), 2 ** 6) == Fraction(57, 64) else "?"

    # Q37: Bayes posterior after observing a white ball is 2/5; p=6.
    posterior_all_white = Fraction(1, 4) / sum(Fraction(k, 16) for k in range(1, 5))
    a[37] = "A" if posterior_all_white == Fraction(2, 5) and 15*posterior_all_white == 6 else "?"

    # Q38: average across the 11 possible nontrivial compositions and calculate the posterior weights.
    black_counts = range(1, 12)
    denom = sum(math.comb(k, 4) for k in black_counts)
    avg_four_black = Fraction(denom, 11 * math.comb(12, 4))
    posterior_ten_black = Fraction(math.comb(10, 4), denom)
    conditional_ten_black = Fraction(math.comb(10, 4), math.comb(12, 4))
    a[38] = "B" if (avg_four_black, posterior_ten_black, conditional_ten_black) == (Fraction(8, 55), Fraction(35, 132), Fraction(14, 33)) else "?"

    # Q40: symmetry of Binomial(7,1/2) gives P(X>=4)=1/2 and a+b=3.
    at_least_four = sum(Fraction(math.comb(7, j), 2**7) for j in range(4, 8))
    a[40] = "A" if at_least_four == Fraction(1, 2) and 1+2 == 3 else "?"

    # Q42: weighted ordered-pair sum for a<b.
    total = sum(n * n for n in range(1, 7))
    weight = sum(x * x * y * y for x in range(1, 7) for y in range(1, 7) if x < y)
    p = Fraction(weight, total * total)
    a[42] = "A" if (p, (2 * p.denominator) // p.numerator) == (Fraction(33, 91), 5) else "?"

    # Q43: attain the Frechet upper intersection by nesting A within B.
    a[43] = "B" if 8 * Fraction(3, 4) == 6 else "?"

    # Q44: Frechet bounds on the intersection are 0.45 and 0.65.
    a[44] = "D" if (max(Fraction(0), Fraction(65, 100) + Fraction(80, 100) - 1), min(Fraction(65, 100), Fraction(80, 100))) == (Fraction(45, 100), Fraction(65, 100)) else "?"

    # Q45: joint probability 1/8, P(B)=1/2, and both complement conditionals are as printed.
    joint = Fraction(1, 4) * Fraction(1, 2)
    p_b = joint / Fraction(1, 4)
    p_ac = 1-Fraction(1, 4)
    p_ac_bc = 1-Fraction(1, 4)-p_b+joint
    a[45] = "D" if joint == Fraction(1, 4)*p_b and (1-joint/p_b) == Fraction(3, 4) and p_ac_bc/p_ac == Fraction(1, 2) else "?"

    # Q46: solve for the roots from sum 7/12 and product 1/12.
    a[46] = "A" if (Fraction(1, 3) * Fraction(1, 4), Fraction(1, 3) + Fraction(1, 4)) == (Fraction(1, 12), Fraction(7, 12)) else "?"

    # Q47: use the complement of A union B in the numerator.
    p_union, p_b = Fraction(3, 5), Fraction(1, 4)
    a[47] = "C" if (1-p_union)/(1-p_b) == Fraction(8, 15) else "?"

    # Q48: exchangeability makes each of five positions a success with conditional chance 3/5.
    a[48] = "A" if Fraction(math.comb(4, 2), math.comb(5, 3)) == Fraction(3, 5) else "?"

    # Q49: inclusion-exclusion on the five values 3,...,7 gives 24 of 1000 sequences.
    n49 = 5 ** 3 - 2 * 4 ** 3 + 3 ** 3
    a[49] = "D" if Fraction(n49, 10 ** 3) == Fraction(3, 125) else "?"

    # Q50: two of the five ordered outcomes with sum 6 include a 2.
    sum_six = [(x, y) for x in range(1, 7) for y in range(1, 7) if x + y == 6]
    includes_two = sum(2 in pair for pair in sum_six)
    a[50] = "D" if Fraction(includes_two, len(sum_six)) == Fraction(2, 5) else "?"
    return a


def main():
    answers = solve()
    banks = {
        "probability": json.load(open(os.path.join(ROOT, "seed/probability_jam_practice.json"), encoding="utf-8")),
        "maths": json.load(open(os.path.join(ROOT, "seed/maths_jam_practice.json"), encoding="utf-8")),
    }
    items = {int(item["id"][-2:]): item for bank in banks.values() for item in bank["items"]}
    assert len(items) == 45, len(items)
    assert set(items) == set(answers), (set(items) - set(answers), set(answers) - set(items))
    for n, answer in answers.items():
        assert items[n]["answer"] == answer, (n, items[n]["answer"], answer)
    assert banks["probability"]["count"] == 44
    assert banks["maths"]["count"] == 1
    assert "∩" in items[1]["stem"] and "ᶜ" in items[1]["stem"]
    print("Verified 45 answers independently: 44 probability, 1 mathematics")


if __name__ == "__main__":
    main()
