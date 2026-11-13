# Non-parametric methods — evidence map

This map records the repository evidence supporting each of the eight syllabus topics. The lesson JSON files contain the detailed textbook/online references, worked examples, provenance and scope boundaries; the mastery pools provide 20 unseen questions per topic.

| Topic | Lesson seed | Mastery pool | Numerical verifier | June 2026 anchor / evidence |
|---|---|---|---|---|
| 5.1 Mann–Whitney U | `seed/lesson_nonparam_t1.json` | `seed/nonparam_t1_mastery.json` | `verify_nonparam_t1.py` | Q42; two independent executive groups, pooled midranks and U statistics |
| 5.2 Sign and Wilcoxon signed-rank | `seed/lesson_nonparam_t2.json` | `seed/nonparam_t2_mastery.json` | `verify_nonparam_t2.py` | Paired-design contrast and signed-rank calculations; no separate direct anchor |
| 5.3 Kruskal–Wallis and Friedman | `seed/lesson_nonparam_t3.json` | `seed/nonparam_t3_mastery.json` | `verify_nonparam_t3.py` | Syllabus coverage of independent multi-group and blocked/repeated designs |
| 5.4 Spearman and Kendall rank correlation | `seed/lesson_np4.json` | `seed/nonparam_t4_mastery.json` | `verify_nonparam_t4.py` | Q35; crude-oil/gasoline ranks, Σd² = 108 and Spearman ρ |
| 5.5 Matching tests to study design | `seed/lesson_nonparam_t5.json` | `seed/nonparam_t5_mastery.json` | `verify_nonparam_t5.py` | Cross-topic decision matrix covering independent, paired, blocked and association designs |
| 5.6 Kolmogorov–Smirnov and runs tests | `seed/lesson_nonparam_t6.json` | `seed/nonparam_t6_mastery.json` | `verify_nonparam_t6.py` | EDF gaps, continuity cautions and randomness/run-count calculations |
| 5.7 Empirical distribution function | `seed/lesson_nonparam_t7.json` | `seed/nonparam_t7_mastery.json` | `verify_nonparam_t7.py` | Definition, jumps, expectation, variance, covariance and quantile construction |
| 5.8 Linear rank tests for location and scale | `seed/lesson_nonparam_t8.json` | `seed/nonparam_t8_mastery.json` | `verify_nonparam_t8.py` | Wilcoxon scores and Ansari–Bradley/Mood scale-score patterns |

The source paper is `seed/pyq_j26_full.json`. Q35 belongs to Non-parametric methods even though the earlier variant bank placed it in Mathematics. Q42 is the Mann–Whitney U item. The corrected Non-parametric variant bank now contains ten variants for each of those two anchors; unrelated Q33 and Q41 variants are excluded from this module.
