#!/usr/bin/env python3
# Mastery pool for 10A.3 — Indian statisticians and their contributions.
# Twenty unseen items, 6 easy / 10 moderate / 4 hard.
# Deliberately avoided: the year of the Mahalanobis distance (1930 vs 1936 in the
# sources) and anything resting on it.
import json, io, collections

I = []
def q(n, fmt, diff, stem, opts, ans, expl, **kw):
    it = dict(id="official-t3-m-%02d" % n, format=fmt, topic="official-t3", diff=diff,
              stem=stem, options=opts, answer=ans, explanation=expl)
    it.update(kw); I.append(it)

# ------------------------------------------------------------------ easy (6)
q(1, "numeric", "easy",
  "National Statistics Day is observed in India on:",
  ["29 June", "17 December", "10 September", "28 June"], "A",
  "29 June is Mahalanobis's birthday and has been observed as National Statistics Day since 2007, the decision having "
  "been taken in 2006. 28 June is the date of his death, 17 December the date of the ISI's founding meeting, and "
  "10 September C. R. Rao's birthday — all three are built to catch a half-remembered date.",
  check="Born 29 June 1893, died 28 June 1972; the Day is the birthday, not the death anniversary.")

q(2, "single", "easy",
  "The Indian Statistical Institute was founded by:",
  ["C. R. Rao", "P. C. Mahalanobis", "R. C. Bose", "P. V. Sukhatme"], "B",
  "Mahalanobis founded the ISI in Calcutta in 1931. Bose and Rao both built their careers there and Rao led its "
  "research and training school for decades, but neither founded it; Sukhatme's institutional work was at the ICAR and "
  "the FAO.")

q(3, "single", "easy",
  "The Rao–Blackwell theorem concerns:",
  ["Testing a composite hypothesis by union and intersection",
   "Bounding the variance of an unbiased estimator below",
   "Improving an unbiased estimator by conditioning on a sufficient statistic",
   "Constructing a partially balanced design from an association scheme"], "C",
  "Rao–Blackwell says that conditioning an unbiased estimator on a sufficient statistic cannot increase its variance. "
  "The variance lower bound is Cramér–Rao, the union–intersection principle is S. N. Roy's, and the association-scheme "
  "design is Bose's PBIBD — the three other options are the three other names in this topic.")

q(4, "single", "easy",
  "Which journal was founded by Mahalanobis at the Indian Statistical Institute?",
  ["Biometrika", "Calcutta Statistical Association Bulletin",
   "Journal of the Indian Society of Agricultural Statistics", "Sankhyā"], "D",
  "Sankhyā was founded in 1933, two years after the Institute. Biometrika is British and far older; the other two are "
  "genuine Indian journals but neither is Mahalanobis's ISI journal, which is what makes them usable distractors.")

q(5, "single", "easy",
  "P. V. Sukhatme is associated above all with:",
  ["Information geometry", "Multivariate test statistics",
   "Agricultural and survey sampling", "Error-correcting codes"], "C",
  "Sukhatme's work was in sampling applied to agriculture and food, at the ICAR and then as director of the FAO's "
  "Statistics Division. Information geometry is Rao's, multivariate test statistics Roy's, and error-correcting codes "
  "Bose's with Ray-Chaudhuri.")

q(6, "single", "easy",
  "Rao's score test is the third member of a classical trio of tests. The other two are:",
  ["The sign test and the run test", "The likelihood ratio and Wald tests",
   "The t test and the F test", "The union–intersection and largest root tests"], "B",
  "The likelihood ratio, Wald and Rao score tests are the three asymptotically equivalent classical tests, all built "
  "from the likelihood. The sign and run tests are nonparametric, t and F are small-sample normal-theory tests, and the "
  "union–intersection and largest root tests are Roy's multivariate work.")

# ------------------------------------------------------------------ moderate (10)
q(7, "numeric", "moderate",
  "The Indian Statistical Institute was declared an Institute of National Importance in:",
  ["1931", "1950", "1959", "1972"], "C",
  "An Act of Parliament in 1959 declared the ISI an Institute of National Importance and empowered it to award its own "
  "degrees. 1931 is its founding, 1950 the start of the National Sample Survey, and 1972 the year of Mahalanobis's "
  "death.",
  check="Founded 1931, journal 1933, NSS 1950, Institute of National Importance 1959. The question asks for the last.")

q(8, "single", "moderate",
  "Euler's conjecture on orthogonal Latin squares was disproved by:",
  ["Bose, Shrikhande and Parker", "Bose, Nair and Mesner",
   "Bose, Ray-Chaudhuri and Hocquenghem", "Rao, Bose and Shrikhande"], "A",
  "Bose, S. S. Shrikhande and E. T. Parker, working in 1959–60, became known as Euler's spoilers. Nair is Bose's "
  "co-author on partially balanced designs, Mesner on association-scheme algebra, and Ray-Chaudhuri and Hocquenghem on "
  "BCH codes — each wrong option keeps Bose and swaps in a different one of his genuine collaborators.")

q(9, "single", "moderate",
  "The union–intersection principle is due to:",
  ["C. R. Rao", "R. C. Bose", "D. Basu", "S. N. Roy"], "D",
  "S. N. Roy gave the union–intersection principle, which builds a test for a composite hypothesis out of tests for its "
  "components, and from which his largest root test follows. Basu's name attaches to Basu's theorem on complete "
  "sufficient and ancillary statistics, which is a different kind of result altogether.")

q(10, "single", "moderate",
  "Basu's theorem states that:",
  ["An unbiased estimator conditioned on a sufficient statistic has no larger variance",
   "The Fisher information bounds the variance of an unbiased estimator",
   "A minimal sufficient statistic is a function of every sufficient statistic",
   "A complete sufficient statistic is independent of any ancillary statistic"], "D",
  "Basu's theorem gives the independence of a complete sufficient statistic from any ancillary statistic. The "
  "conditioning statement is Rao–Blackwell, the information statement is Cramér–Rao, and the function-of-every-"
  "sufficient-statistic line is the definition of minimal sufficiency — all correct statements, but none of them is "
  "Basu's.")

q(11, "single", "moderate",
  "P. V. Sukhatme directed the Statistics Division of which international body?",
  ["The World Health Organization", "The United Nations Statistical Commission",
   "The International Statistical Institute", "The Food and Agriculture Organization"], "D",
  "He directed the FAO's Statistics Division in Rome from 1951 to 1971, which follows from his agricultural work at the "
  "ICAR. The International Statistical Institute is a learned society with no such division, and the abbreviation ISI "
  "shared with the Indian Statistical Institute is itself a standard trap.")

q(12, "multi", "moderate",
  "Consider the following results, each said to be due to C. R. Rao.",
  ["A and B only", "A, B and D only", "A, C and D only", "A, B, C and D"], "B",
  "The Cramér–Rao bound, orthogonal arrays and the Rao distance are all his. The Bose–Mesner algebra belongs to R. C. "
  "Bose with D. M. Mesner, so every option that keeps C is wrong and the choice turns on that one statement.",
  statements=["The Cramér–Rao lower bound.",
              "Orthogonal arrays.",
              "The Bose–Mesner algebra.",
              "The Rao distance."],
  verdicts={"A": dict(tf=True,  why="His, derived independently of Cramér."),
            "B": dict(tf=True,  why="His, and the basis of Taguchi-style industrial experimentation."),
            "C": dict(tf=False, why="R. C. Bose with D. M. Mesner, 1959 — a different man and a different field."),
            "D": dict(tf=True,  why="His, from the information-geometry work of the 1945 paper.")})

q(13, "numeric", "moderate",
  "P. V. Sukhatme's Sampling Theory of Surveys with Applications was published in:",
  ["1934", "1944", "1954", "1964"], "C",
  "It appeared in 1954, three years after he moved to the FAO and fourteen years after he became Statistical Adviser to "
  "the ICAR. The decade dates are built to be confused with those two appointments, which is the reason to carry the "
  "sequence rather than the single year.",
  check="ICAR 1940, FAO 1951, textbook 1954. The question asks for the book, not an appointment.")

q(14, "match", "moderate",
  "Match the statistician in List I with the contribution in List II.",
  ["A-III, B-I, C-IV, D-II", "A-I, B-III, C-II, D-IV",
   "A-III, B-II, C-I, D-IV", "A-IV, B-I, C-III, D-II"], "A",
  "Bose gave partially balanced designs, Roy the largest root test, Mahalanobis fractile graphical analysis (his method "
  "for comparing two populations from survey data), and Rao the score test. Every wrong option moves at least two of the "
  "four, so the mapping has to be checked pair by pair rather than guessed from one recognised entry.",
  check="Fix the two you are sure of first; here Bose–III and Rao–II are the anchors.",
  pairs=[["A. R. C. Bose", "I. Roy's largest root test"],
         ["B. S. N. Roy", "II. Rao's score test"],
         ["C. P. C. Mahalanobis", "III. Partially balanced incomplete block designs"],
         ["D. C. R. Rao", "IV. Fractile graphical analysis"]])

q(15, "numeric", "moderate",
  "C. R. Rao received the International Prize in Statistics in:",
  ["2002", "2016", "2023", "2021"], "C",
  "He received it in 2023, a few months before his death at 102. 2002 is the year of his United States National Medal "
  "of Science, and the other two years are prizes awarded to other statisticians — the dates are close enough together "
  "that only the pairing of honour with year distinguishes them.",
  check="National Medal of Science 2002, International Prize in Statistics 2023. The question asks for the second.")

q(16, "single", "moderate",
  "The Mahalanobis distance differs from the ordinary Euclidean distance chiefly in that it:",
  ["Uses absolute deviations instead of squares",
   "Is defined only for two variables",
   "Requires the variables to be independent",
   "Accounts for the covariance structure of the variables"], "D",
  "The Mahalanobis distance scales by the inverse covariance matrix, so correlated and differently scaled variables are "
  "handled correctly; it reduces to the Euclidean distance exactly when the covariance matrix is the identity. The "
  "independence option inverts the point: independence is the special case in which the distance offers nothing new, "
  "not a requirement.")

# ------------------------------------------------------------------ hard (4)
q(17, "single", "hard",
  "Rao's 1945 paper in the Bulletin of the Calcutta Mathematical Society is remembered for containing:",
  ["The score test and orthogonal arrays",
   "The Cramér–Rao bound, the Rao–Blackwell theorem and the seed of information geometry",
   "The Cramér–Rao bound and Basu's theorem",
   "Orthogonal arrays and the Rao distance alone"], "B",
  "That single early paper carried three now-separate results: the variance lower bound, the conditioning theorem, and "
  "the treatment of a family of distributions as a curved space that became information geometry. The score test and "
  "orthogonal arrays came later in his career, and Basu's theorem is not Rao's at all.")

q(18, "single", "hard",
  "A statement reads: 'The Cramér–Rao bound and the Rao–Blackwell theorem are both results of collaborations between "
  "Rao and the second statistician named.' What is wrong with it?",
  ["Both names record independent co-discovery, not collaboration",
   "Only the Rao–Blackwell theorem was a collaboration",
   "Only the Cramér–Rao bound was a collaboration",
   "Neither result is correctly named after two people"], "A",
  "Cramér reached the inequality independently of Rao, and Blackwell independently found the conditioning result; "
  "neither is a joint paper. The hyphen in a statistical result's name records priority disputes and independent "
  "discovery at least as often as it records co-authorship, and this is the standard example.")

q(19, "multi", "hard",
  "Consider the following statements about P. C. Mahalanobis.",
  ["A, B and C only", "A and B only", "B, C and D only", "A, B, C and D"], "A",
  "He chaired the National Income Committee, founded the NSS in 1950, and his two-sector model underlay the Second Plan. "
  "He did not head the Central Statistical Organisation: it was set up in 1951 on the Committee's recommendation as a "
  "government office, and he remained Honorary Statistical Adviser to the Cabinet rather than its head.",
  statements=["He chaired the National Income Committee of 1949.",
              "He founded the National Sample Survey.",
              "His two-sector model underlay the Second Five Year Plan.",
              "He headed the Central Statistical Organisation."],
  verdicts={"A": dict(tf=True,  why="With D. R. Gadgil and V. K. R. V. Rao as the other members."),
            "B": dict(tf=True,  why="Founded in 1950 and run from the ISI in its early years."),
            "C": dict(tf=True,  why="The capital-goods/consumer-goods model behind the 1956-61 plan."),
            "D": dict(tf=False, why="The CSO was created in 1951 on his committee's recommendation; he advised the "
                                    "Cabinet but never headed it.")})

q(20, "single", "hard",
  "The Sukhatme–Margen hypothesis bears on poverty measurement because it argues that:",
  ["Calorie requirements are higher than the official norms assume",
   "The body adapts its efficiency at low intakes, so a fixed calorie norm misclassifies people",
   "Expenditure is a better proxy for welfare than calorie intake",
   "Protein rather than calorie deficiency is the binding constraint"], "B",
  "Sukhatme and Margen argued for intra-individual adaptation: a person's own intake varies more over time than intakes "
  "vary between people, so classifying individuals as deficient against one fixed threshold is unsound. That cuts "
  "directly against the calorie-anchored poverty lines of Dandekar and Rath and of the Alagh and Lakdawala sequence, "
  "which is the link Unit X expects.")

BODY = dict(moduleId="official", source="mastery", topicId="official-t3",
            label="Indian Statisticians and Their Contributions — mastery test (unseen)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/official_t3_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I); k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s" % dict(d))
print("  keys       %s" % dict(k))
print("  formats    %s" % dict(f))
