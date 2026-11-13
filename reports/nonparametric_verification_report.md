# Non-parametric module — verification report

## Scope

Eight syllabus topics (5.1–5.8), eight lessons, eight mastery pools, the June 2026 variant bank, and eight topic-level numerical verification scripts, a group runner, and a 20-item PYQ variant bank.

## Structural review

- Topics 5.1, 5.2, 5.3, 5.5, 5.6, 5.7 and 5.8 each contain 15 core scenes, 96 estimated minutes, five learning objectives, three prerequisites, two scenarios, two guided scenes and a flow diagram.
- Each of those seven pools contains 20 questions with a 6 easy / 10 moderate / 4 hard mix, at least five numeric items, two multi-statement items, explanations above the 40-character floor, numeric sanity checks and balanced answer keys (the largest key count is six).
- Existing topic 5.4 contains 15 core scenes (16 total including the optional extension), 100 estimated minutes and a 20-question pool with the required difficulty mix.
- The t7 verifier's float-versus-rational comparison has been corrected to use exact Fraction arithmetic.
- A dedicated t4 verifier now recomputes the Q35 rank differences, Spearman coefficient, Kendall coefficient, raw Pearson correlation and exact permutation probabilities. For n = 10 it exhaustively counts 599,491 outcomes at least as extreme out of 3,628,800 permutations (p = 0.165204); this replaces the earlier Monte Carlo wording.
- The June 2026 module variant bank contains 20 items: ten Q35 rank-correlation variants (preserved from the former Mathematics bank) and ten Q42 Mann–Whitney variants (the original nine plus one new complementary-U item). Q35 is removed from the Mathematics bank; the unrelated parametric Q33 variants are removed from the Non-parametric bank. Explanations across all 20 variants were expanded to show the calculation or decision rule.

The group runner, verify_nonparametric.py, executes all eight topic-level verifiers in one command.

## Validation boundary

This is a source-level structural and arithmetic audit. GitHub Actions Validate, Browser and Acceptance are the independent release gates and must all pass on the consolidated pull request. No production merge or Vercel deployment is performed by this change.
