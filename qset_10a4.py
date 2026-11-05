#!/usr/bin/env python3
# Mastery pool for 10A.4 — major surveys and indices.
# Twenty unseen items, 6 easy / 10 moderate / 4 hard.
#
# Deliberately NOT tested: the direction in which the IIP linking factor is applied
# (the MoSPI FAQ gives the definition but not the application), and the CPI food
# weight quoted bare, since the group table (40.10%) and the COICOP division table
# (36.75%) give different figures — any item touching it names the table.
import json, io, collections

I = []
def q(n, fmt, diff, stem, opts, ans, expl, **kw):
    it = dict(id="official-t4-m-%02d" % n, format=fmt, topic="official-t4", diff=diff,
              stem=stem, options=opts, answer=ans, explanation=expl)
    it.update(kw); I.append(it)

# ------------------------------------------------------------------ easy (6)
q(1, "numeric", "easy",
  "The base year of the new Consumer Price Index series released in February 2026 is:",
  ["2024", "2022-23", "2023-24", "2012"], "A",
  "The new CPI series is on base 2024=100, replacing 2012=100. Note the form of the answer as much as the number: CPI's "
  "base is a calendar year, whereas the IIP and the WPI both moved to the financial year 2022-23, and 2023-24 is the "
  "consumption survey that supplied the weights rather than a base year.",
  check="CPI base 2024 (calendar); IIP and WPI base 2022-23 (financial); HCES 2023-24 is the survey. Three different things.")

q(2, "single", "easy",
  "The item basket and weights of the CPI series on base 2024=100 are drawn from:",
  ["The Annual Survey of Industries 2023-24",
   "The Household Consumption Expenditure Survey 2023-24",
   "The Periodic Labour Force Survey 2024",
   "The National Family Health Survey, round 6"], "B",
  "HCES 2023-24 supplied the basket and the weights; base-period prices were then collected through calendar 2024. ASI "
  "is a factory-sector survey and feeds the production index, not the consumer index, and the other two measure labour "
  "and health and have nothing to do with a price basket.")

q(3, "single", "easy",
  "The Wholesale Price Index covers:",
  ["Goods and services", "Goods only", "Services only", "Goods, services and administered prices separately"], "B",
  "WPI is a goods-only index, measured at the wholesale or first point of bulk sale. Services are covered instead by the "
  "new quarterly Services Producer Price Index across seven sectors — which is one of the stated reasons for moving to a "
  "producer price framework at all.")

q(4, "single", "easy",
  "Which body produces the Wholesale Price Index?",
  ["The National Statistical Office, MoSPI",
   "The Reserve Bank of India",
   "The Central Statistics Office",
   "The Office of the Economic Adviser, DPIIT"], "D",
  "WPI comes from the Office of the Economic Adviser in the Department for Promotion of Industry and Internal Trade. "
  "MoSPI through the NSO produces the CPI and the IIP, and the RBI uses CPI-Combined as its inflation target without "
  "producing it — the producer is asked as often as the base year.")

q(5, "numeric", "easy",
  "The Periodic Labour Force Survey was launched in:",
  ["2011", "2015", "2017", "2019"], "C",
  "PLFS was launched in 2017, replacing the quinquennial Employment and Unemployment Survey, which had produced an "
  "estimate only once every five years. 2019 is the year the NSSO was merged into the NSO, which is a different event "
  "often misremembered into this slot.",
  check="PLFS launched 2017; redesigned January 2025; NSSO merged into NSO 2019. The question asks for the launch.")

q(6, "single", "easy",
  "Under Current Weekly Status, a person's activity status is determined with reference to:",
  ["The 7 days preceding the survey", "The 30 days preceding the survey",
   "The 365 days preceding the survey", "The current calendar quarter"], "A",
  "Current Weekly Status uses the preceding 7 days. The 365-day window is Usual Status, principal plus subsidiary. PLFS "
  "reports on both, and the monthly bulletins introduced in 2025 are on CWS only, so confusing the two windows costs "
  "marks on more than one question.")

# ------------------------------------------------------------------ moderate (10)
q(7, "numeric", "moderate",
  "The new series of the Index of Industrial Production carries the base year:",
  ["2011-12", "2022-23", "2024", "2023-24"], "B",
  "IIP moved from 2011-12 to 2022-23, with the base-year report in May 2026 and the first release on the new base in "
  "June 2026. The WPI moved to the same financial year, while the CPI moved to calendar 2024 — the three revisions "
  "happened close together and the base years are the standard confusion.",
  check="IIP and WPI both 2022-23; CPI 2024. The question asks for the production index.")

q(8, "single", "moderate",
  "The headline change made to the PLFS from January 2025 was the introduction of:",
  ["Quarterly estimates for urban areas",
   "Annual estimates on a July-to-June year",
   "Monthly all-India estimates of LFPR, WPR and UR on Current Weekly Status",
   "Usual Status estimates for rural areas"], "C",
  "Monthly all-India estimates on CWS did not exist before 2025; the first monthly bulletin was for April 2025. "
  "Quarterly urban estimates and annual Usual Status estimates were part of the original 2017 design, and the July-June "
  "year is what the redesign moved away from — so every wrong option names something that already existed or was "
  "discontinued.")

q(9, "single", "moderate",
  "The Annual Survey of Industries covers:",
  ["All non-agricultural enterprises, incorporated and unincorporated",
   "Unincorporated enterprises outside agriculture",
   "Enterprises with turnover above a prescribed threshold",
   "Factories registered under the Factories Act, 1948"], "D",
  "ASI covers factories registered under sections 2m(i) and 2m(ii) of the Factories Act, 1948, together with bidi and "
  "cigar establishments and certain electricity undertakings, and is collected under the Collection of Statistics Act, "
  "2008. The unincorporated sector is the subject of a separate survey, ASUSE; the two are the formal and informal "
  "halves of one picture.")

q(10, "multi", "moderate",
  "Consider the following statements about the CPI series on base 2024=100.",
  ["A and B only", "A, B and C only", "B and D only", "A, B, C and D"], "D",
  "All four hold. The series adopted COICOP 2018 with twelve divisions in place of six groups, resolving to 358 weighted "
  "items; rural house rent entered the index for the first time; prices are collected electronically on handheld "
  "devices, with e-commerce prices used in twelve large towns; and it remains a modified Laspeyres index, with Jevons "
  "at the elementary level. Candidates reject D because the methodology change feels too large to be entirely true.",
  statements=["It adopts the COICOP 2018 classification, with twelve divisions in place of six groups.",
              "Rural house rent is included for the first time.",
              "Prices are collected electronically, and e-commerce prices are used in some large towns.",
              "It is a modified Laspeyres index."],
  verdicts={"A": dict(tf=True,  why="43 groups, 92 classes, 162 subclasses and 358 items under the new classification."),
            "B": dict(tf=True,  why="And the housing weight rose from 10.07% to 11.88% partly as a result."),
            "C": dict(tf=True,  why="CAPI on handheld devices, with e-commerce prices in twelve towns above 25 lakh population."),
            "D": dict(tf=True,  why="Jevons at the elementary level, Young or modified Laspeyres above it — a fixed basket, repriced.")})

q(11, "single", "moderate",
  "The published Household Consumption Expenditure Survey round immediately preceding 2022-23 was that of:",
  ["2011-12", "2017-18", "2019-20", "2015-16"], "A",
  "A round was fielded in 2017-18 but its results were withheld in November 2019 on stated grounds of data quality, so "
  "the last published round before 2022-23 is 2011-12. That eleven-year gap is why the CPI ran on a 2011-12 basket for "
  "so long, and why two consumption rounds were then run back to back.")

q(12, "match", "moderate",
  "Match the index in List I with its base year and producing body in List II.",
  ["A-I, B-IV, C-II, D-III", "A-II, B-IV, C-I, D-III",
   "A-II, B-III, C-I, D-IV", "A-IV, B-II, C-III, D-I"], "B",
  "CPI: base 2024, NSO. WPI: base 2022-23, Office of the Economic Adviser in DPIIT. IIP: base 2022-23, NSO. PPI: "
  "launched June 2026 by the same office as the WPI. The two traps are giving the CPI a financial-year base and giving "
  "a DPIIT index to MoSPI, and both appear among the wrong options.",
  check="Fix the producing body first — two of the four sit outside MoSPI — then the base years follow.",
  pairs=[["A. Consumer Price Index", "I. Base 2022-23, National Statistical Office"],
         ["B. Wholesale Price Index", "II. Base 2024, National Statistical Office"],
         ["C. Index of Industrial Production", "III. Launched June 2026, Office of the Economic Adviser, DPIIT"],
         ["D. Producer Price Index", "IV. Base 2022-23, Office of the Economic Adviser, DPIIT"]])

q(13, "numeric", "moderate",
  "After the January 2025 redesign, the number of first stage units covered by the PLFS each year is approximately:",
  ["8,000", "12,800", "22,692", "2,72,304"], "C",
  "The design moved from about 12,800 first stage units to 22,692, and from 8 households per unit to 12. The figure "
  "2,72,304 is the resulting number of households, not of first stage units, and 12,800 is the old FSU count — the "
  "question is really testing whether you keep the two quantities apart.",
  check="22,692 FSUs × 12 households ≈ 2,72,304 households, against 12,800 × 8 ≈ 1,02,400 before.")

q(14, "single", "moderate",
  "The National Family Health Survey is conducted under the Ministry of Health and Family Welfare through which nodal agency?",
  ["The National Statistical Office, MoSPI",
   "The Indian Council of Medical Research",
   "The Registrar General of India",
   "The International Institute for Population Sciences, Mumbai"], "D",
  "IIPS Mumbai is the nodal agency. NFHS-6, fielded in 2023-24 and released in May 2026, covered about 6.79 lakh "
  "households across 715 districts and reported a total fertility rate of 2.0. The Registrar General handles the census "
  "and the Sample Registration System, which is a neighbouring topic and the reason that option is attractive.")

q(15, "single", "moderate",
  "Which sector appears in the new IIP series on base 2022-23 but did not exist as a sector in the 2011-12 series?",
  ["Water supply, sewerage and waste management", "Gas supply",
   "Mining and quarrying", "Electricity"], "A",
  "Water supply, sewerage and waste management is the genuinely new sector, carrying a weight of 2.020. Gas supply was "
  "also added to the index but sits inside Electricity and Gas Supply with a weight of 0.694 — it is a new component, "
  "not a new sector, and that distinction is exactly what the question tests.")

q(16, "multi", "moderate",
  "Consider the following statements about the Wholesale Price Index and the Producer Price Index.",
  ["A and B only", "A, B and C only", "B, C and D only", "A, B, C and D"], "B",
  "A, B and C hold: the base was revised from 2011-12 to 2022-23, the basket expanded from 697 to 957 items, and the "
  "Output PPI was launched alongside it with a quarterly Services PPI covering seven sectors. D is false — the WPI is "
  "to be discontinued after a five-year transition, not immediately, which is the detail the option sets turn on.",
  statements=["The WPI base year was revised from 2011-12 to 2022-23.",
              "The WPI basket expanded from 697 to 957 items.",
              "An Output Producer Price Index was launched alongside the revised WPI.",
              "The WPI was discontinued immediately on the launch of the PPI."],
  verdicts={"A": dict(tf=True,  why="The same financial year the IIP moved to."),
            "B": dict(tf=True,  why="957 items on the revised base, against 697 before."),
            "C": dict(tf=True,  why="Launched 15 June 2026, with a trial Input PPI for manufacturing and a quarterly Services PPI."),
            "D": dict(tf=False, why="A five-year transition window was announced; the WPI continues to be published through it.")})

# ------------------------------------------------------------------ hard (4)
q(17, "numeric", "hard",
  "The CPI combined index on base 2012=100 stood at 180.0 in a certain month. Using the published combined linking "
  "factor of 0.5267, the equivalent figure on base 2024=100 is:",
  ["341.75", "180.00", "94.81", "105.34"], "C",
  "The CPI linking factor is defined as the geometric mean of the new series in 2025 divided by that of the old series "
  "in the same year, so it converts old to new by multiplication: 180.0 × 0.5267 = 94.81. The figure 341.75 is what you "
  "get by dividing instead, and 105.34 is MoSPI's own illustrative answer for an old index of 200, not of 180.",
  check="A month near the 2024 base period must come out near 100. 94.81 passes that check; 341.75 does not.")

q(18, "single", "hard",
  "Rural MPCE as a percentage of urban MPCE was 83.9% in 2011-12 and 69.7% in 2023-24. The official reading of this is that:",
  ["Rural consumption fell in absolute terms",
   "Urban consumption grew faster than rural, widening the gap",
   "Rural consumption grew faster than urban",
   "The two series are not comparable, so no reading is possible"], "C",
  "Both levels rose; the ratio of rural to urban is what fell, and the official reading is that rural consumption has "
  "been growing faster than urban — the two statements are compatible only once you notice that the ratio is being "
  "reported the other way round from how it is usually described. Read the direction of any ratio in this topic before "
  "interpreting it.",
  check="A ratio can fall while both of its parts rise. Decide which quantity is the numerator before reading a trend.")

q(19, "single", "hard",
  "A statement reads: 'All three of India's main indices — CPI, WPI and IIP — were rebased in 2026, and all three "
  "continue to be published on their new bases.' What is wrong with it?",
  ["The WPI is being replaced by the Producer Price Index after a five-year transition",
   "The IIP was not rebased in this period",
   "The CPI was replaced rather than rebased",
   "Nothing is wrong; the statement is accurate"], "A",
  "All three were indeed rebased, so the first half holds. The flaw is in the second half: the WPI alone is also being "
  "replaced, by the Producer Price Index, after a five-year transition window. Rebasing and replacement are different "
  "things, and only one of the three indices is undergoing both.")

q(20, "single", "hard",
  "In the group table of the new CPI series, the weight of food and beverages falls from 45.86% to 40.10%. The correct "
  "interpretation is that:",
  ["Food prices fell between the two base periods",
   "Food consumption fell in absolute terms",
   "Food is being under-weighted relative to its importance",
   "Food accounts for a smaller share of household budgets than it did"], "D",
  "A weight is a measured share of household spending, taken from the consumption survey. A falling weight says the "
  "share has fallen, which is what happens as budgets grow — it says nothing about whether food prices rose or fell, "
  "nor about absolute quantities, nor about any judgement by the statistical office. Note also that the COICOP division "
  "table gives a different food figure, 36.75%, for the same series, so the table always has to be named.")

BODY = dict(moduleId="official", source="mastery", topicId="official-t4",
            label="Major Surveys and Indices — mastery test (unseen)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/official_t4_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I); k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s" % dict(d))
print("  keys       %s" % dict(k))
print("  formats    %s" % dict(f))
