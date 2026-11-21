# -*- coding: utf-8 -*-
"""Build the Day 1-4 practice-quiz bank (Statistics Lover daily quizzes) for the Probability question bank.

    python quiz_bank_sl.py            write seed/probability_sl_quiz.json
    python quiz_bank_sl.py --check    exit 1 if the file on disk differs from what would be written

Source: the owner's copies of four "Statistics Lover" daily-quiz solution PDFs (Day 1, Days 2-3, Day 4), taken through
`tools/intake.js` (docs/SOURCE_INTAKE.md): every page read as an image, every question accounted for, every answer
recomputed. 29 questions; Day-4 Q3 repeats Day-1 Q7 and is kept once, so 28 items. Stems are restated in plain words
with the source's numbers; explanations are written fresh. Where the source's key is incomplete the item carries a
keyNote; where a stem had to be completed or read, a `repaired` note.

verify_quiz_sl.py recomputes every answer and audits the structure. After the first merge the JSON is the source of
truth (docs/CONTENT_GUIDE.md, 3c); this script then records how it was made. Pass --force to overwrite it anyway."""
import io, json, os, sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from pyq_bank_common import S, M  # noqa: E402

P = "probability"
LABEL = "Daily practice quizzes, Day 1–4 (Statistics Lover)"
OUT = "seed/probability_sl_quiz.json"

ITEMS = [
    # ------------------------------------------------------------------ Day 1
    S("slq-d1-01", P, "probability-t12", "Day-1 quiz Q1",
      "Events A and B are independent, with P(A) = 0.2 and P(B) = 0.4. What is P(A | B)?",
      ["0.2", "0.5", "0.08", "None of these"], "A",
      "Independence means P(A ∩ B) = P(A)P(B) = 0.2 × 0.4 = 0.08. Then P(A | B) = P(A ∩ B)/P(B) = 0.08/0.4 = 0.2, "
      "which is just P(A): learning that B happened tells you nothing about A. The value 0.08 is P(A ∩ B), not the "
      "conditional probability.", diff="easy"),
    S("slq-d1-02", P, "probability-t8", "Day-1 quiz Q2",
      "Which set of statements is true when the events A and B are (i) arbitrary, (ii) independent and (iii) mutually "
      "exclusive?",
      ["(i) P(A ∩ B) ≥ P(A ∪ B) ≥ P(A); (ii) P(A) + P(B) ≥ P(A) ≤ P(A ∩ B); (iii) P(A) ≤ P(A ∩ B) ≥ 0",
       "(i) P(A ∩ B) ≤ P(A ∪ B) ≤ P(A); (ii) P(A ∩ B) ≤ 0; (iii) P(A ∩ B) ≥ P(A ∪ B) ≤ 1",
       "(i) P(A ∪ B) ≤ P(A ∩ B) ≤ P(A); (ii) P(A ∩ B) ≥ P(A ∪ B) ≥ 0; (iii) P(A) ≤ P(A ∩ B) ≤ P(A ∪ B)",
       "(i) P(A ∪ B) ≥ P(A) ≥ P(A ∩ B); (ii) P(A ∪ B) ≥ P(A) ≥ P(A) · P(B); (iii) P(A ∪ B) ≥ P(A) ≥ 0"], "D",
      "Because A ∩ B ⊆ A ⊆ A ∪ B, probabilities grow along the chain: P(A ∪ B) ≥ P(A) ≥ P(A ∩ B) ≥ 0 for any two "
      "events. Part (i) of each of the first three sets reverses a link of this chain, so those sets fail at once. In the "
      "last set, (i) is the chain itself; (ii) under independence P(A ∩ B) = P(A)P(B) ≤ P(A), so P(A ∪ B) ≥ P(A) ≥ "
      "P(A)P(B); (iii) for disjoint events P(A ∩ B) = 0, so the chain reads P(A ∪ B) ≥ P(A) ≥ 0."),
    S("slq-d1-03", P, "probability-t5", "Day-1 quiz Q3",
      "A fair coin is tossed twice. What is the expected number of tails?",
      ["0", "1", "2", "3"], "B",
      "The number of tails X is Binomial(2, 1/2): P(X = 0) = 1/4, P(X = 1) = 1/2, P(X = 2) = 1/4. So E(X) = 0 × 1/4 + "
      "1 × 1/2 + 2 × 1/4 = 1, the same as np = 2 × 1/2.", diff="easy"),
    S("slq-d1-04", P, "probability-t5", "Day-1 quiz Q4",
      "A machine makes a defective item with probability 0.1, independently from item to item. What is the probability "
      "that a sample of 10 items contains at most one defective?",
      ["0.736", "0.692", "0.587", "0.452"], "A",
      "The number of defectives X is Binomial(10, 0.1). At most one means X = 0 or X = 1: P(X ≤ 1) = 0.9¹⁰ + "
      "10 × 0.1 × 0.9⁹ = 0.3487 + 0.3874 = 0.7361.", diff="easy"),
    S("slq-d1-05", P, "probability-t12", "Day-1 quiz Q5",
      "Box A has 4 red, 2 white and 6 black balls; box B has 3 red and 5 white balls. A fair die is rolled: on a 1 or a "
      "6 a ball is drawn from box A, otherwise from box B. The ball drawn is red. What is the probability that the die "
      "showed a 6?",
      ["5/13", "4/13", "3/13", "2/13"], "D",
      "First the total probability of red: P(R) = P(box A) × 4/12 + P(box B) × 3/8 = (2/6)(1/3) + (4/6)(3/8) = "
      "1/9 + 1/4 = 13/36. A six and a red ball together: (1/6)(4/12) = 1/18. Bayes: P(six | red) = (1/18)/(13/36) = "
      "2/13. The numerator uses the single face 6, not both faces that lead to box A; using both gives 4/13, which is "
      "the probability that box A was used."),
    S("slq-d1-06", P, "probability-t12", "Day-1 quiz Q6",
      "On a multiple-choice question with m (> 1) options, an examinee knows the answer with probability p and "
      "otherwise guesses at random. Given that the examinee answered correctly, what is the probability that they knew "
      "the answer?",
      ["p/(1 + (m − 1)p)", "(mp − 1)/(mp)", "mp/(1 + p(m − 1))", "mp/(1 + (m + 1)p)"], "C",
      "Let K be 'knows the answer' and C 'answers correctly'. P(C | K) = 1 and P(C | Kᶜ) = 1/m. Bayes: P(K | C) = "
      "p × 1 / [p + (1 − p)/m]. Multiplying top and bottom by m gives mp/(mp + 1 − p) = mp/(1 + (m − 1)p). Check with "
      "p = 1: the examinee always knows, and the formula gives m/m = 1."),
    S("slq-d1-07", P, "probability-t8", "Day-1 quiz Q7; also Day-4 quiz Q3",
      "A subset of {1, 2, …, 10} is chosen at random, all subsets being equally likely. What is the probability that it "
      "contains both 3 and 7?",
      ["1/2", "1/4", "1/5", "1/6"], "B",
      "There are 2¹⁰ = 1024 subsets. With 3 and 7 fixed inside, each of the other 8 elements is in or out freely, giving "
      "2⁸ = 256 subsets, and 256/1024 = 1/4. Equivalently, a random subset contains each element with probability 1/2, "
      "independently, so (1/2)(1/2) = 1/4.", diff="easy"),
    S("slq-d1-08", P, "probability-t5", "Day-1 quiz Q8",
      "An urn holds 3 red, 4 black and 3 green marbles. Two are drawn one after the other without replacement. What is "
      "the probability of getting one red and one black?",
      ["4/15", "5/15", "3/15", "2/15"], "A",
      "Red then black: (3/10)(4/9) = 2/15. Black then red: (4/10)(3/9) = 2/15. Both orders give one red and one black, "
      "so the probability is 4/15. Counting unordered pairs agrees: 3 × 4 / C(10, 2) = 12/45 = 4/15. The value 2/15 "
      "counts only one order.", diff="easy"),
    S("slq-d1-09", P, "probability-t8", "Day-1 quiz Q9",
      "If P(A) = 4/52, P(B) = 13/52 and P(A ∩ B) = 1/52, what is P(Aᶜ ∩ B)?",
      ["40/52", "12/52", "48/52", "13/52"], "B",
      "B splits into the disjoint pieces A ∩ B and Aᶜ ∩ B, so P(Aᶜ ∩ B) = P(B) − P(A ∩ B) = 13/52 − 1/52 = 12/52. "
      "In card terms, with B a club and A an ace, the clubs that are not the ace number 12.", diff="easy"),
    M("slq-d1-10", P, "probability-t8", "Day-1 quiz Q10",
      "For two events A and B, P(A) = 3/4 and P(B) = 1/2. Which of the following must be true?",
      ["P(A ∩ B) ≥ 1/4", "P(A ∩ B) ≤ 1/4", "P(A ∩ B) ≥ 3/4", "P(A ∩ B) ≤ 3/4"],
      "AD",
      ["Bonferroni's inequality: P(A ∩ B) ≥ P(A) + P(B) − 1 = 3/4 + 1/2 − 1 = 1/4.",
       "Not forced: P(A ∩ B) can be any value from 1/4 to 1/2, for example 1/2 when B lies inside A.",
       "Impossible: A ∩ B lies inside B, so P(A ∩ B) ≤ P(B) = 1/2, which is below 3/4.",
       "Always true: P(A ∩ B) ≤ min(P(A), P(B)) = 1/2, which is below 3/4."],
      "C",
      "The two bounds are max(0, P(A) + P(B) − 1) ≤ P(A ∩ B) ≤ min(P(A), P(B)), here 1/4 ≤ P(A ∩ B) ≤ 1/2, and every "
      "value in between can occur. A statement must be true only if it holds across that whole range: the lower bound "
      "1/4 and the cap 3/4 do; 'at most 1/4' fails at 1/2, and 'at least 3/4' never holds.",
      keyNote="The source's key gives only the first statement. The fourth, P(A ∩ B) ≤ 3/4, also always holds because "
              "P(A ∩ B) ≤ 1/2. As printed it is a single-answer question with two correct options, so it is given here "
              "as multiple-correct."),

    # ------------------------------------------------------------------ Days 2-3
    S("slq-d23-01", P, "probability-t8", "Day-2/3 quiz Q1",
      "If P(A) = 1, which of the following need not hold?",
      ["P(A ∩ B) = P(B)", "P(A ∩ Bᶜ) = P(Bᶜ)", "P(Aᶜ ∩ B) = 0", "P(Aᶜ ∩ Bᶜ) = P(Bᶜ)"], "D",
      "P(A) = 1 means P(Aᶜ) = 0, so every event inside Aᶜ has probability 0. Hence P(Aᶜ ∩ B) = 0, P(A ∩ B) = P(B) − "
      "P(Aᶜ ∩ B) = P(B), and in the same way P(A ∩ Bᶜ) = P(Bᶜ). But Aᶜ ∩ Bᶜ also lies inside Aᶜ, so its probability is 0, "
      "and it equals P(Bᶜ) only when P(B) = 1.", diff="easy"),
    S("slq-d23-02", P, "probability-t8", "Day-2/3 quiz Q2",
      "If P(A) = 1, which of the following need not hold?",
      ["P(A ∪ B) = 1", "P(Aᶜ ∪ B) = P(B)", "P(Aᶜ ∪ Bᶜ) = P(Bᶜ)", "P(A ∪ Bᶜ) = P(Bᶜ)"], "D",
      "With P(Aᶜ) = 0: P(A ∪ B) ≥ P(A) = 1, so it is 1. P(Aᶜ ∪ B) = P(Aᶜ) + P(B) − P(Aᶜ ∩ B) = 0 + P(B) − 0 = P(B). "
      "P(Aᶜ ∪ Bᶜ) = 1 − P(A ∩ B) = 1 − P(B) = P(Bᶜ). But A ∪ Bᶜ contains A, so its probability is 1, which equals "
      "P(Bᶜ) only when P(B) = 0.", diff="easy"),
    S("slq-d23-03", P, "probability-t12", "Day-2/3 quiz Q3",
      "Given P(A ∩ B) = 1/8, P(B) = 1/5 and P(A) = 3/4, which of the following is correct?",
      ["P(A | B) = 1/4", "P(A | Bᶜ) = 25/32", "P(Aᶜ | B) = 3/4", "P(Aᶜ | Bᶜ) = 7/16"], "B",
      "P(A | B) = (1/8)/(1/5) = 5/8. P(A | Bᶜ) = [P(A) − P(A ∩ B)]/[1 − P(B)] = (3/4 − 1/8)/(4/5) = (5/8)(5/4) = 25/32. "
      "P(Aᶜ | B) = 1 − 5/8 = 3/8. P(A ∪ B) = 3/4 + 1/5 − 1/8 = 33/40, so P(Aᶜ | Bᶜ) = (1 − 33/40)/(4/5) = (7/40)(5/4) "
      "= 7/32. Of the four printed values only 25/32 is right."),
    S("slq-d23-04", P, "probability-t8", "Day-2/3 quiz Q4",
      "If P(A) = α, P(B) = β and P(A ∩ B) = γ, then P(Aᶜ ∩ B) equals",
      ["α(1 − β)", "β(1 − α)", "(1 − α)(1 − β)", "β − γ"], "D",
      "B is the disjoint union of A ∩ B and Aᶜ ∩ B, so P(Aᶜ ∩ B) = P(B) − P(A ∩ B) = β − γ. The product β(1 − α) "
      "would be right only if A and B were independent, which is not given.", diff="easy"),
    S("slq-d23-05", P, "probability-t12", "Day-2/3 quiz Q5",
      "For events E and F, P(E | F) = 0.5, P(E | F′) = 0.6 and P(F) = 0.6. What is P(E)?",
      ["0.56", "0.44", "0.54", "0.46"], "C",
      "By the law of total probability, P(E) = P(E | F)P(F) + P(E | F′)P(F′) = 0.5 × 0.6 + 0.6 × 0.4 = 0.30 + 0.24 "
      "= 0.54.", diff="easy"),
    S("slq-d23-06", P, "probability-t12", "Day-2/3 quiz Q6",
      "Three dice show a five with probabilities p, q and r respectively. One die is chosen at random, each equally "
      "likely, and thrown; it shows a five. What is the probability that the first die was chosen?",
      ["r/(p + q + r)", "p/(p + q + r)", "q/(p + q + r)", "(p + q + r)/3"], "B",
      "Bayes with equal priors of 1/3: P(first | five) = (1/3)p / [(1/3)p + (1/3)q + (1/3)r] = p/(p + q + r). The "
      "equal priors cancel, so each die's posterior is proportional to its chance of a five. (p + q + r)/3 is the total "
      "probability of a five, not a posterior.", diff="easy",
      repaired="The printed stem stops at 'the die chosen'; it is completed as 'was the first die', the reading the "
               "source's own solution uses."),
    S("slq-d23-07", P, "probability-t8", "Day-2/3 quiz Q7",
      "If P(E) = 1/3, P(F) = 2/5 and P(E ∪ F) − P(E ∩ F) = 1/5, then P(E ∪ F) equals",
      ["11/15", "4/15", "8/15", "7/15"], "D",
      "The addition rule gives P(E ∪ F) + P(E ∩ F) = P(E) + P(F) = 1/3 + 2/5 = 11/15. Adding this to the given "
      "difference: 2P(E ∪ F) = 11/15 + 1/5 = 14/15, so P(E ∪ F) = 7/15, and then P(E ∩ F) = 7/15 − 1/5 = 4/15."),
    S("slq-d23-08", P, "probability-t8", "Day-2/3 quiz Q8",
      "Three dice are thrown. A is the event that the total is a multiple of 5, and B that it is a multiple of 6. What is "
      "P(Aᶜ ∪ Bᶜ)?",
      ["1", "1/2", "5/216", "3883/3888"], "A",
      "By De Morgan's law, Aᶜ ∪ Bᶜ = (A ∩ B)ᶜ. A total that is a multiple of both 5 and 6 is a multiple of 30, but three "
      "dice total between 3 and 18. So P(A ∩ B) = 0 and P(Aᶜ ∪ Bᶜ) = 1.", diff="easy"),
    S("slq-d23-09", P, "probability-t5", "Day-2/3 quiz Q9",
      "A fair coin is tossed 2n times. What is the probability that the numbers of heads and tails are not equal?",
      ["1 − (2n)!/(n!)² · (1/2)²ⁿ", "1 − (2n)!/(n!)²", "(2n)!/(n!)² · (1/2)²ⁿ", "(2n)!/(n!)²"], "A",
      "Equal numbers means exactly n heads, with probability C(2n, n)(1/2)²ⁿ = (2n)!/(n!)² · (1/2)²ⁿ. The event asked "
      "for is the complement, 1 − (2n)!/(n!)² · (1/2)²ⁿ. Check with n = 1: two tosses differ (HT or TH) with "
      "probability 1/2, and the formula gives 1 − 2 × 1/4 = 1/2. Expressions without (1/2)²ⁿ are counts of outcomes, "
      "not probabilities.",
      repaired="The source prints 2n!; it is read as (2n)!, as the source's solution does."),

    # ------------------------------------------------------------------ Day 4
    S("slq-d4-01", P, "probability-t8", "Day-4 quiz Q1",
      "Events E, F and G satisfy P(E | G) = 0.05 and P(F | G) = 0.05. Which statement must be true?",
      ["P(E ∩ F | G) = (0.05)²", "P(Ē ∩ F̄ | G) ≥ 0.90", "P(E ∪ F | G) ≤ 0.05", "P(E ∪ F | Ḡ) ≥ 1 − (0.05)²"], "B",
      "Probabilities given G obey the usual rules. Boole's inequality: P(E ∪ F | G) ≤ 0.05 + 0.05 = 0.10, so "
      "P(Ē ∩ F̄ | G) = 1 − P(E ∪ F | G) ≥ 0.90. The product (0.05)² would need E and F to be independent given G, which is "
      "not given; P(E ∪ F | G) can be as large as 0.10; and nothing at all is known about the events given Ḡ."),
    S("slq-d4-02", P, "probability-t12", "Day-4 quiz Q2",
      "A and B are events that are not mutually exclusive, and P(A | B) = P(B | A). Then",
      ["A ⊂ B but A ≠ B", "A = B", "A ∩ B = ϕ", "P(A) = P(B)"], "D",
      "Write both sides out: P(A ∩ B)/P(B) = P(A ∩ B)/P(A). Since the events are not mutually exclusive, P(A ∩ B) > 0 "
      "and it cancels, leaving P(A) = P(B). Nothing forces A = B or A ⊂ B: with three equally likely outcomes, A = {1, 2} "
      "and B = {2, 3} satisfy the condition.", diff="easy"),
    S("slq-d4-04", P, "probability-t12", "Day-4 quiz Q4",
      "A number is drawn at random from 1, 2, …, 24. A is the event that it is a multiple of 4, and B that it is a "
      "multiple of 5. What is P(A | B) + P(B | A)?",
      ["1/6", "1/3", "11/12", "5/12"], "D",
      "A = {4, 8, 12, 16, 20, 24} has 6 numbers, B = {5, 10, 15, 20} has 4, and A ∩ B = {20}. So P(A | B) = 1/4 and "
      "P(B | A) = 1/6, and the sum is 1/4 + 1/6 = 5/12.",
      repaired="The source says two numbers are drawn with replacement but solves it as a single draw; it is given here as "
               "a single draw. Read as two independent draws (the first a multiple of 4, the second a multiple of 5) the "
               "answer is the same 5/12, since then P(A | B) + P(B | A) = P(A) + P(B) = 1/4 + 1/6."),
    S("slq-d4-05", P, "probability-t8", "Day-4 quiz Q5",
      "A card is drawn at random from a standard 52-card deck. What is the probability that it is an ace or a club?",
      ["17/52", "16/52", "1/4", "1/12"], "B",
      "P(ace or club) = P(ace) + P(club) − P(ace of clubs) = 4/52 + 13/52 − 1/52 = 16/52 = 4/13. Adding 4/52 and 13/52 "
      "without the subtraction counts the ace of clubs twice and gives 17/52.", diff="easy"),
    S("slq-d4-06", P, "probability-t5", "Day-4 quiz Q6",
      "A, B, C and D take turns in that order (A, B, C, D, A, B, …) rolling a fair die; the first to roll a six wins. What "
      "is the probability that D wins?",
      ["121/471", "125/671", "125/371", "125/571"], "B",
      "D wins in round k when all four miss in each of the first k − 1 rounds, then A, B and C miss and D rolls a six: "
      "probability (5/6)^(4(k−1)) × (5/6)³ × (1/6). Summing this geometric series over k = 1, 2, …: P(D wins) = "
      "(5/6)³(1/6) / [1 − (5/6)⁴] = (125/1296)/(671/1296) = 125/671.", diff="hard"),
    S("slq-d4-07", P, "probability-t12", "Day-4 quiz Q7",
      "P(A) = 0.5, P(B) = 0.3 and P(A ∩ Bᶜ) = 0.3. What is P(B | A ∪ Bᶜ)?",
      ["2/9", "1/10", "1/2", "1/8"], "A",
      "First P(A ∩ B) = P(A) − P(A ∩ Bᶜ) = 0.5 − 0.3 = 0.2. The numerator event is B ∩ (A ∪ Bᶜ) = (B ∩ A) ∪ (B ∩ Bᶜ) "
      "= A ∩ B, with probability 0.2. The denominator is P(A ∪ Bᶜ) = P(A) + P(Bᶜ) − P(A ∩ Bᶜ) = 0.5 + 0.7 − 0.3 = 0.9. "
      "So P(B | A ∪ Bᶜ) = 0.2/0.9 = 2/9."),
    S("slq-d4-08", P, "probability-t12", "Day-4 quiz Q8",
      "Urn A holds 4 white and 6 black balls; urn B holds 6 white and 4 black. An urn is chosen at random and a ball "
      "drawn from it is white. What is the probability that urn A was chosen?",
      ["0.4", "0.6", "0.5", "0.45"], "A",
      "Bayes with equal priors: P(urn A | white) = (1/2)(4/10) / [(1/2)(4/10) + (1/2)(6/10)] = 4/10 = 0.4. With equal "
      "priors and equal urn sizes, the posterior is each urn's share of the white balls: 4 of the 10.", diff="easy"),
    S("slq-d4-09", P, "probability-t12", "Day-4 quiz Q9",
      "Three boxes each hold 4 white and 5 black balls. One ball is moved at random from box 1 to box 2, then one from "
      "box 2 to box 3, then one from box 3 to box 1. What is the probability that every box ends with the same numbers "
      "of white and black balls as it started with?",
      ["14/45", "1/45", "1/5", "1/9"], "A",
      "Every box always holds 9 balls, so the question is whether each box is back to 4 white and 5 black. Box 1 loses "
      "the first ball's colour and gains the third's, so those must match; box 2 gains the first and loses the second, "
      "so those must match too. So all three moves carry the same colour. All white: (4/9)(5/10)(5/10) = 1/9, since "
      "boxes 2 and 3 each hold 5 white out of 10 after receiving a white. All black: (5/9)(6/10)(6/10) = 1/5. "
      "Total: 1/9 + 1/5 = 14/45.", diff="hard"),
    S("slq-d4-10", P, "probability-t8", "Day-4 quiz Q10",
      "Consider the probability space (Ω, 𝒢, P) with Ω = {1, 2, 3, 4}, 𝒢 = {ϕ, Ω, {1}, {4}, {2, 3}, {1, 4}, {1, 2, 3}, "
      "{2, 3, 4}} and P({1}) = 1/4. The random variable X has X(1) = 1, X(2) = X(3) = 2 and X(4) = 3. If P(X ≤ 2) = 3/4, "
      "what is P({1, 4})?",
      ["0.25", "0.33", "0.50", "0.75"], "C",
      "{X ≤ 2} = {1, 2, 3}, so P({1, 2, 3}) = 3/4 and P({4}) = 1 − 3/4 = 1/4. The events {1} and {4} are disjoint "
      "members of 𝒢, so P({1, 4}) = 1/4 + 1/4 = 1/2. The single points 2 and 3 are not in 𝒢; only P({2, 3}) = 1/2 is "
      "defined, and it is not needed."),
]


def build():
    banks = OrderedDict()
    for x in ITEMS:
        banks.setdefault(x["module"], []).append(x["item"])
    assert list(banks) == [P], "every item belongs to the Probability bank"
    its = banks[P]
    return OrderedDict([(OUT, OrderedDict([("moduleId", P), ("source", "variant"), ("label", LABEL),
                                           ("count", len(its)), ("items", its)]))])


def render(d):
    return json.dumps(d, ensure_ascii=False, indent=1) + "\n"


def main(argv):
    files = OrderedDict((f, render(d)) for f, d in build().items())
    if "--check" in argv:
        bad = [f for f, t in files.items()
               if not os.path.exists(os.path.join(ROOT, f))
               or io.open(os.path.join(ROOT, f), encoding="utf-8", newline="").read().replace("\r\n", "\n") != t]
        for f in bad:
            print("differs from the build: " + f)
        return 1 if bad else 0
    for f, t in files.items():
        p = os.path.join(ROOT, f)
        if os.path.exists(p) and "--force" not in argv and io.open(p, encoding="utf-8").read() != t:
            print("refusing to overwrite %s (edited after its first merge?); pass --force" % f)
            return 1
        with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(t)
        print("wrote %s (%d items)" % (f, len(json.loads(t)["items"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
