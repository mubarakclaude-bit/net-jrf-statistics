#!/usr/bin/env python3
# Mastery pool for 10A.2 — twenty unseen items, 6 easy / 10 moderate / 4 hard.
# Nothing here rests on the Bowley-Robertson year, which the sources disagree on.
import json, io, collections

I = []
def q(n, fmt, diff, stem, opts, ans, expl, **kw):
    it = dict(id="official-t2-m-%02d" % n, format=fmt, topic="official-t2", diff=diff,
              stem=stem, options=opts, answer=ans, explanation=expl)
    it.update(kw); I.append(it)

# ------------------------------------------------------------------ easy (6)
q(1, "numeric", "easy",
  "In which year was the National Income Committee set up?",
  ["1947", "1949", "1951", "1954"], "B",
  "The National Income Committee was constituted in 1949 under P. C. Mahalanobis. 1951 is the year of its first report "
  "(and of the CSO), and 1954 the year of its final report, which is why both appear as distractors.",
  check="Set up 1949, first report April 1951, final report 1954. The question asks for the constitution year.")

q(2, "single", "easy",
  "Who chaired the National Income Committee?",
  ["V. K. R. V. Rao", "D. R. Gadgil", "C. R. Rao", "P. C. Mahalanobis"], "D",
  "Mahalanobis chaired it, with D. R. Gadgil and V. K. R. V. Rao as the other two members. Rao's pre-independence "
  "national income estimates fed the committee's work, which is why he is the attractive wrong answer. C. R. Rao was a "
  "statistician at the ISI but not a member of this committee.")

q(3, "single", "easy",
  "The Collection of Statistics Act currently in force in India was enacted in:",
  ["1953", "2017", "2008", "2019"], "C",
  "The Collection of Statistics Act, 2008 replaced the Act of 1953. It was amended in 2017, which is a different thing "
  "from being enacted then — the amendment changed jurisdiction, added nodal officers and amended the use-of-information "
  "provision, but the parent Act remains the 2008 one.")

q(4, "single", "easy",
  "Which committee anchored the Indian poverty line to a norm of 2,250 calories a day?",
  ["Dandekar and Rath", "Alagh", "Lakdawala", "Tendulkar"], "A",
  "Dandekar and Rath set the line at the expenditure needed to obtain 2,250 calories a day, separately for rural and "
  "urban areas, using NSS data. Alagh and Lakdawala kept a nutritional basis in different forms; Tendulkar abandoned the "
  "calorie anchor altogether.")

q(5, "single", "easy",
  "Who chaired the first National Statistical Commission, constituted in 2006?",
  ["C. Rangarajan", "Pronab Sen", "D. T. Lakdawala", "Suresh Tendulkar"], "D",
  "Suresh Tendulkar chaired the first NSC — the same economist who chaired the poverty expert group that reported in "
  "2009. Rangarajan chaired the commission that recommended the NSC, not the NSC itself; Pronab Sen chaired the Standing "
  "Committee on Statistics much later.")

q(6, "numeric", "easy",
  "In which year did the Rangarajan Commission on the Indian statistical system submit its report?",
  ["1999", "2000", "2001", "2005"], "C",
  "It was constituted in early 2000 and reported in September 2001. 1999 is the year MoSPI was formed and 2005 the year "
  "of the resolution that created the NSC, so every distractor is a real date from the same story.",
  check="Constituted 2000, reported 2001, acted on in 2005. The question asks for the report.")

# -------------------------------------------------------------- moderate (10)
q(7, "multi", "moderate",
  "Consider the following recommendations attributed to the Rangarajan Commission of 2001.",
  ["A and B only", "A, B and C only", "B and D only", "A, B, C and D"], "D",
  "All four were recommended: a statutory apex body accountable to Parliament, a professional statistician as Secretary "
  "of the ministry, regular statistical audits, and reform of the Collection of Statistics Act. The examinable twist is "
  "that only two were implemented — the National Statistician and the new Act of 2008. A question asking what was "
  "recommended and one asking what was implemented have different answers.",
  statements=["A statutory apex statistical body accountable to Parliament.",
              "A professional statistician as Secretary of the ministry.",
              "Regular statistical audits.",
              "Reform of the Collection of Statistics Act."],
  verdicts={"A": {"tf": True, "why": "Recommended — and never enacted."},
            "B": {"tf": True, "why": "Recommended and implemented as the National Statistician."},
            "C": {"tf": True, "why": "Recommended; regular audits were not instituted."},
            "D": {"tf": True, "why": "Recommended and implemented as the Collection of Statistics Act, 2008."}})

q(8, "single", "moderate",
  "Which recommendation of the Rangarajan Commission was NOT implemented?",
  ["A statutory apex body accountable to Parliament",
   "The post of National Statistician",
   "A new Collection of Statistics Act",
   "A review of the statistical system's weaknesses"], "A",
  "The National Statistician was created and the Act was replaced in 2008. The statutory apex body was not: the National "
  "Statistical Commission exists by a government resolution of 2005, without statutory backing, and the promised "
  "legislation has never been passed. The last option is the Commission's own work, not a recommendation.")

q(9, "numeric", "moderate",
  "The Lakdawala expert group on poverty reported in 1993. In which year was its approach adopted by the government?",
  ["1993", "1995", "1997", "2001"], "C",
  "The expert group reported in 1993 and its approach was adopted in 1997. The gap between a committee reporting and a "
  "government acting is the theme of this topic, and this is the cleanest numerical example of it.",
  check="Two dates, four years apart. The question asks for adoption, not for the report.")

q(10, "match", "moderate",
  "Match the committee in List I with what it changed in List II.",
  ["A-II, B-IV, C-I, D-III", "A-II, B-I, C-IV, D-III", "A-I, B-IV, C-II, D-III", "A-III, B-IV, C-I, D-II"], "B",
  "Dandekar and Rath introduced the calorie anchor; Lakdawala introduced state-specific lines updated by CPI-IW and "
  "CPI-AL; Tendulkar dropped the calorie anchor and brought private health and education spending in; Rangarajan's 2014 "
  "group produced a fresh methodology and the 29.5% estimate for 2011-12.",
  pairs=[["A. Dandekar and Rath", "I. State-specific lines using CPI-IW and CPI-AL"],
         ["B. Lakdawala", "II. Poverty line anchored to a 2,250-calorie norm"],
         ["C. Tendulkar", "III. New methodology, 29.5% poverty in 2011-12"],
         ["D. Rangarajan (2014)", "IV. Calorie anchor dropped; health and education included"]])

q(11, "single", "moderate",
  "Which statement correctly describes the Tendulkar committee's approach of 2009?",
  ["It retained the calorie norm and added state-specific lines",
   "It scaled NSS consumption to National Accounts aggregates",
   "It moved away from the calorie anchor and included private spending on health and education",
   "It applied a single rural poverty line to urban areas without adjustment"], "C",
  "Tendulkar abandoned the calorie anchor, used a common poverty line basket, included private health and education "
  "spending, reformed the price adjustment and used a mixed reference period. State-specific lines were Lakdawala's "
  "contribution, and it was Lakdawala who stopped the scaling to National Accounts aggregates.")

q(12, "numeric", "moderate",
  "In which year was the Standing Committee on Statistics dissolved?",
  ["2019", "2023", "2026", "2024"], "D",
  "MoSPI dissolved the Standing Committee on Statistics in September 2024, citing an overlap with the Steering Committee "
  "for National Sample Surveys. 2019 is when its predecessor the Standing Committee on Economic Statistics was formed "
  "and 2023 when it was renamed, so each distractor is a real date in the same sequence.",
  check="Formed 2019 as SCES, renamed 2023 as SCoS, dissolved 2024. The question asks for the end of the sequence.")

q(13, "single", "moderate",
  "Which statement about the Standing Committee on Statistics is correct?",
  ["It was created in 2023 as an entirely new body with no predecessor",
   "It was the Standing Committee on Economic Statistics, formed in 2019 and renamed in 2023",
   "It was renamed the Standing Committee on Economic Statistics in 2023",
   "It was given statutory status in 2023"], "B",
  "The Standing Committee on Economic Statistics was constituted in December 2019 and renamed the Standing Committee on "
  "Statistics in July 2023, with its remit widened from economic surveys to all NSO surveys. The third option reverses "
  "the direction of the renaming, which is the intended error.")

q(14, "multi", "moderate",
  "Consider the following statements about the Collection of Statistics (Amendment) Act, 2017.",
  ["A and C only", "B and D only", "A, B and C only", "C and D only"], "C",
  "A is correct: the Act now extends to the whole of India, with a proviso for Jammu and Kashmir limited to Union and "
  "Concurrent List matters. B is correct: a new section 3A requires central, state and union territory governments to "
  "designate nodal officers. C is correct: section 9(1) was amended on the use of information furnished. D is wrong: the "
  "amendment did not make the National Statistical Commission statutory, and nothing in it touches the NSC.",
  statements=["It extended the Act's jurisdiction, with a proviso for Jammu and Kashmir.",
              "It required governments to designate nodal officers for statistical activities.",
              "It amended the provision on the use of information furnished under the Act.",
              "It gave the National Statistical Commission statutory status."],
  verdicts={"A": {"tf": True,  "why": "Section 1(2), with the J&K proviso limited to Union and Concurrent List matters."},
            "B": {"tf": True,  "why": "The new section 3A on nodal officers."},
            "C": {"tf": True,  "why": "Section 9(1), on use of the information for statistical purposes."},
            "D": {"tf": False, "why": "The NSC remains non-statutory; no amendment has changed that."}})

q(15, "order", "moderate",
  "Arrange the following poverty estimation committees in chronological order, earliest first.",
  ["B, A, C, D", "A, B, C, D", "A, C, B, D", "B, A, D, C"], "B",
  "Dandekar and Rath 1971, Alagh 1979, Lakdawala 1993, Tendulkar 2009. The usual error is to place Tendulkar before "
  "Lakdawala, because Tendulkar is the better known name; the way to hold the order is that Lakdawala kept the calorie "
  "basis and Tendulkar dropped it, and dropping came later.",
  items=["A. Dandekar and Rath", "B. Alagh", "C. Lakdawala", "D. Tendulkar"])

q(16, "single", "moderate",
  "The members of the National Income Committee, besides its chairman, were:",
  ["D. R. Gadgil and V. K. R. V. Rao", "V. K. R. V. Rao and C. R. Rao",
   "D. R. Gadgil and D. T. Lakdawala", "C. R. Rao and R. C. Bose"], "A",
  "Mahalanobis chaired, with D. R. Gadgil and V. K. R. V. Rao as members. C. R. Rao and R. C. Bose were eminent "
  "statisticians of the same era at the Indian Statistical Institute but were not on this committee, and Lakdawala "
  "belongs to the poverty sequence four decades later.")

# ------------------------------------------------------------------ hard (4)
q(17, "single", "hard",
  "C. Rangarajan chaired two well-known bodies. Which pairing is correct?",
  ["The 2001 commission on poverty estimation and the 2014 commission on the statistical system",
   "The 2001 commission on the statistical system and the 2014 expert group on poverty estimation",
   "The 2001 commission on the statistical system and the first National Statistical Commission",
   "The 2009 expert group on poverty and the 2014 commission on the statistical system"], "B",
  "The Commission that reviewed the statistical system was constituted in 2000 and reported in 2001; the expert group on "
  "poverty estimation reported in 2014. The first NSC was chaired by Tendulkar, not Rangarajan, and the 2009 poverty "
  "group was Tendulkar's — so every other option swaps one of the two men into the other's seat.")

q(18, "numeric", "hard",
  "The Rangarajan expert group of 2014 put the poverty ratio for 2011-12 at approximately:",
  ["29.5%", "21.9%", "25.7%", "37.2%"], "A",
  "The Rangarajan group's estimate for 2011-12 was 29.5%, above the Tendulkar-based figure for the same year — which is "
  "the whole reason the group's report was contested. The other options are figures from the Tendulkar series and from "
  "earlier years, which is why they look plausible.",
  check="Two committees, one dataset, two headcounts. The question asks for the higher, later estimate.")

q(19, "single", "hard",
  "On dissolving the Standing Committee on Statistics, the ministry cited an overlap with which body?",
  ["The National Statistical Commission",
   "The Standing Committee on Economic Statistics",
   "The Steering Committee for National Sample Surveys",
   "The Technical Advisory Committee on Price Indices"], "C",
  "The stated reason was overlap with the Steering Committee for National Sample Surveys, chaired by Rajeeva Laxman "
  "Karandikar, which has seventeen members and a two-year tenure. The SCES is not the answer because it is the same body "
  "as the SCoS under its earlier name, and the NSC is an advisory commission rather than a survey committee.")

q(20, "single", "hard",
  "A statement reads: 'The National Statistical Commission was given statutory backing within a year of the 2005 "
  "resolution, as that resolution promised.' What is wrong with it?",
  ["The resolution was issued in 2006, not 2005",
   "The promise was made but the legislation was never enacted",
   "The NSC was created by an Act, so no further backing was needed",
   "Statutory backing was granted in 2008 through the Collection of Statistics Act"], "B",
  "The 2005 resolution did announce the Commission and indicate statutory backing would follow, and the first NSC was "
  "constituted in 2006 — but Parliament has never enacted the law, so the Commission remains non-statutory. The "
  "Collection of Statistics Act 2008 governs data collection and says nothing about the Commission's status.")

BODY = dict(moduleId="official", source="mastery", topicId="official-t2",
            label="Commissions and Committees of the Indian Statistical System — mastery test (unseen)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/official_t2_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I); k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s" % dict(d))
print("  keys       %s" % dict(k))
print("  formats    %s" % dict(f))
