#!/usr/bin/env python3
# Mastery pool for 10A.1 — twenty unseen items, 6 easy / 10 moderate / 4 hard, so a
# retake can draw a fresh ten at the 3/5/2 mix. Keys are spread five to a letter.
# Every fact here is one the lesson teaches and that was checked against a source.
import json, io, collections

I = []
def q(n, fmt, diff, stem, opts, ans, expl, **kw):
    it = dict(id="official-t1-m-%02d" % n, format=fmt, topic="official-t1", diff=diff,
              stem=stem, options=opts, answer=ans, explanation=expl)
    it.update(kw); I.append(it)

# ---------------------------------------------------------------- easy (6)
q(1, "numeric", "easy",
  "In which year did the Ministry of Statistics and Programme Implementation become an independent ministry?",
  ["1991", "1999", "2005", "2019"], "B",
  "MoSPI was formed on 15 October 1999 by merging the Department of Statistics with the Department of Programme "
  "Implementation. 2005 is the NSC resolution and 2019 is the CSO–NSSO merger, which is why both appear as distractors.",
  check="The ministry is younger than the offices inside it. If a year predates 1999, it cannot be the ministry's.")

q(2, "single", "easy",
  "The National Statistics Office (NSO) was created by merging which two bodies?",
  ["The Central Statistical Organisation and the National Sample Survey Office",
   "The National Sample Survey Office and the Labour Bureau",
   "The Central Statistical Organisation and the Registrar General of India",
   "The Indian Statistical Institute and the Central Statistical Organisation"], "A",
  "The CSO, which compiled the national accounts, and the NSSO, which ran the sample surveys, were merged into the NSO in "
  "2019. The Labour Bureau, the Registrar General and the ISI are separate bodies under different authorities and were "
  "never part of the merger.")

q(3, "single", "easy",
  "What is the legal status of the National Statistical Commission?",
  ["A constitutional body named in the Constitution",
   "A statutory body created by an Act of Parliament",
   "A non-statutory body created by a government resolution",
   "A registered society under the Societies Registration Act"], "C",
  "The NSC was created by a government resolution dated 1 June 2005 and became effective in 2006. A bill to give it "
  "statutory standing has been drafted but not enacted, so it remains an executive body that recommends rather than "
  "directs. This single word carries more marks in this module than any other fact.")

q(4, "numeric", "easy",
  "In which year were the CSO and the NSSO merged into the National Statistics Office?",
  ["2014", "2017", "2019", "2021"], "C",
  "The merger took effect on 23 May 2019. The older names survive in speech and in past papers, but as organisations they "
  "were folded into a single office under MoSPI.",
  check="Fix it between the 2017-18 consumption round that was withheld and the pandemic year.")

q(5, "single", "easy",
  "Which body conducts the Population Census of India?",
  ["The National Statistics Office", "The National Statistical Commission",
   "The Central Statistics wing of MoSPI", "The Registrar General and Census Commissioner of India"], "D",
  "The Census is conducted by the Registrar General and Census Commissioner under the Ministry of Home Affairs, governed by "
  "the Census Act, 1948. MoSPI runs sample surveys; it does not run the complete enumeration. Placing the Census inside "
  "MoSPI is one of the three commonest errors in this topic.")

q(6, "single", "easy",
  "MoSPI is organised into which two wings?",
  ["Statistics and Economics", "National Accounts and Sample Surveys",
   "Central Statistics and Data Governance", "Statistics and Programme Implementation"], "D",
  "The two wings are the Statistics wing — which is the National Statistics Office — and the Programme Implementation "
  "wing. Central Statistics and Data Governance are sub-wings inside the NSO, not wings of the ministry, which makes the "
  "third option the attractive wrong answer.")

# ---------------------------------------------------------------- moderate (10)
q(7, "multi", "moderate",
  "Consider the following statements about the National Statistical Commission.",
  ["A and C only", "B and D only", "B and C only", "A, C and D only"], "D",
  "A is correct: the Rangarajan review of the statistical system, which reported in 2001, recommended a permanent "
  "commission. B is wrong: it is non-statutory, created by resolution. C is correct: the Chief Statistician of India, who "
  "is also Secretary to the Government in MoSPI, is Secretary to the Commission. D is correct: the CEO of NITI Aayog sits "
  "ex-officio. So A, C and D hold.",
  statements=["It was recommended by the Rangarajan review of the Indian statistical system.",
              "It is a statutory body established under an Act of Parliament.",
              "The Chief Statistician of India acts as its Secretary.",
              "The Chief Executive Officer of NITI Aayog is an ex-officio member."],
  verdicts={"A": {"tf": True,  "why": "The commission chaired by Dr C. Rangarajan reported in 2001 and recommended it."},
            "B": {"tf": False, "why": "Created by a government resolution of 1 June 2005 — non-statutory."},
            "C": {"tf": True,  "why": "The CSI, also Secretary to the Government in MoSPI, is Secretary to the Commission."},
            "D": {"tf": True,  "why": "The CEO of NITI Aayog is the ex-officio member."}})

q(8, "numeric", "moderate",
  "Apart from the chairperson and the ex-officio member, how many part-time members does the National Statistical "
  "Commission have?",
  ["Three", "Four", "Five", "Seven"], "B",
  "The composition is a part-time chairperson and four part-time members, plus one ex-officio member (the CEO of NITI "
  "Aayog), with the Chief Statistician of India as Secretary. Counting the chairperson among the members, or counting the "
  "Secretary as a member, produces the distractors.",
  check="Five appointed seats in all — one chair plus four members — then the ex-officio seat on top.")

q(9, "single", "moderate",
  "The Consumer Price Index for Industrial Workers (CPI-IW) is compiled by:",
  ["The National Statistics Office", "The Labour Bureau",
   "The Office of the Economic Adviser", "The Reserve Bank of India"], "B",
  "CPI-IW is compiled by the Labour Bureau under the Ministry of Labour and Employment. The NSO compiles CPI Rural, Urban "
  "and Combined; the Office of the Economic Adviser in the Ministry of Commerce and Industry compiles the Wholesale Price "
  "Index; the RBI targets inflation but compiles none of these indices.")

q(10, "numeric", "moderate",
  "The Infrastructure and Project Monitoring Division of MoSPI monitors central sector projects costing at least:",
  ["₹50 crore", "₹100 crore", "₹150 crore", "₹500 crore"], "C",
  "The threshold is ₹150 crore, alongside the monitoring of eleven key infrastructure sectors. This sits in the Programme "
  "Implementation wing, the half of the ministry candidates skip, which is exactly why it is asked.",
  check="Two numbers come out of this wing: ₹150 crore for project monitoring and ₹5 crore a year for MPLADS. Keep them "
        "apart — swapping them is the intended error.")

q(11, "numeric", "moderate",
  "Under MPLADS, how much is allocated to each Member of Parliament per year?",
  ["₹1 crore", "₹2 crore", "₹5 crore", "₹10 crore"], "C",
  "Each MP is allocated ₹5 crore a year for works recommended in the constituency. The scheme has been administered end to "
  "end through the eSAKSHI portal since April 2023, and it is run by the MPLADS Division of MoSPI's Programme "
  "Implementation wing.",
  check="The scheme is MP-wise and annual. An answer quoted per constituency per five years is the same money described "
        "differently and is not what the question asks.")

q(12, "single", "moderate",
  "Which of the following is NOT a function of the National Statistical Commission?",
  ["Evolving policies, priorities and standards in statistical matters",
   "Advising on the quality of statistical products and processes",
   "Working with central and state agencies to improve statistical standards",
   "Compiling the national accounts and the index of industrial production"], "D",
  "Compilation is the National Statistics Office's job. The Commission evolves standards, advises on quality and works with "
  "agencies — it recommends, it does not produce statistics. Any option that gives the Commission a production role is the "
  "answer to a 'NOT' question of this shape.")

q(13, "match", "moderate",
  "Match the output in List I with the body that produces it in List II.",
  ["A-III, B-I, C-IV, D-II", "A-III, B-IV, C-I, D-II", "A-I, B-III, C-IV, D-II", "A-III, B-I, C-II, D-IV"], "A",
  "The NSO compiles the CPI (Rural, Urban and Combined); the Labour Bureau compiles CPI-IW; the Office of the Economic "
  "Adviser compiles the Wholesale Price Index; the Registrar General conducts the Population Census. Three price indices "
  "with three different owners, plus the census that belongs to a fourth body, is the standard matching set for this topic.",
  pairs=[["A. Consumer Price Index (Rural/Urban/Combined)", "I. Labour Bureau"],
         ["B. Consumer Price Index for Industrial Workers", "II. Registrar General of India"],
         ["C. Wholesale Price Index", "III. National Statistics Office"],
         ["D. Population Census", "IV. Office of the Economic Adviser"]])

q(14, "single", "moderate",
  "The first National Sample Survey was launched in 1950 and the Central Statistical Organisation was set up in 1951. "
  "Which statement follows?",
  ["The sample survey machinery predates the national accounts machinery",
   "The national accounts machinery predates the sample survey machinery",
   "Both were created by the same resolution",
   "Both were created after the Ministry was formed"], "A",
  "The survey came first, in 1950, on Mahalanobis's design; the CSO followed in 1951 to compile the national accounts. "
  "Candidates reverse the two because the CSO sounds the more senior body. The ministry itself came only in 1999, so the "
  "last option is false by half a century.")

q(15, "single", "moderate",
  "With the base-year revision announced for 2026, the new base year of the Consumer Price Index is:",
  ["2011-12", "2012", "2022-23", "2024"], "D",
  "The new CPI series is on a 2024 base and was released on 12 February 2026, replacing the 2012 base. The two quantity "
  "series moved to 2022-23: GDP from 27 February 2026 and the IIP from May 2026. The distractors are the old CPI base and "
  "the new base of the other two series.")

q(16, "multi", "moderate",
  "Consider the following statements about the 2019 restructuring of the Indian statistical system.",
  ["A and B only", "A, B and D only", "B and C only", "A and D only"], "B",
  "A is correct: the CSO and NSSO were merged into the NSO. B is correct: the NSO is a wing of MoSPI, not an independent "
  "ministry. C is wrong: the National Statistical Commission was not abolished and continues as an advisory body. D is "
  "correct: a stated purpose of the merger was to place survey design and release under one office, and the criticism was "
  "precisely that this removed a separation. So A, B and D.",
  statements=["The Central Statistical Organisation and the National Sample Survey Office were merged into one office.",
              "The resulting office is a wing of MoSPI rather than an independent ministry.",
              "The National Statistical Commission was abolished by the same order.",
              "The merger placed survey design and publication under a single office."],
  verdicts={"A": {"tf": True,  "why": "The merger of 23 May 2019 created the NSO."},
            "B": {"tf": True,  "why": "The NSO is MoSPI's statistics wing."},
            "C": {"tf": False, "why": "The NSC was untouched by the merger and continues to advise."},
            "D": {"tf": True,  "why": "End-to-end responsibility in one office was the stated purpose, and the ground of "
                                      "the criticism."}})

# ---------------------------------------------------------------- hard (4)
q(17, "numeric", "hard",
  "The Household Consumption Expenditure Survey of 2022-23 was released in February 2024. The previous HCES whose results "
  "were published related to 2011-12. How many years separate the two reference periods?",
  ["Nine", "Ten", "Eleven", "Twelve"], "C",
  "2011-12 to 2022-23 is eleven years. A round was conducted in 2017-18 but its results were not released, which is why "
  "the published series has the gap. Counting from the release dates rather than the reference periods, or counting to the "
  "withheld round, gives the distractors.",
  check="The question asks about reference periods, not release dates. 2022 − 2011 = 11.")

q(18, "order", "hard",
  "Arrange the following in chronological order, earliest first.",
  ["A, B, C, D", "B, A, C, D", "A, B, D, C", "B, A, D, C"], "A",
  "The first National Sample Survey was 1950, the CSO was set up in 1951, MoSPI became a ministry in 1999, and the NSC "
  "resolution is dated 1 June 2005. The usual error is to put the CSO before the survey, which gives option B.",
  items=["A. First National Sample Survey", "B. Central Statistical Organisation set up",
         "C. MoSPI becomes an independent ministry", "D. Resolution constituting the National Statistical Commission"])

q(19, "single", "hard",
  "A state government's employment estimate contradicts the national survey. Which statement best describes what the "
  "National Statistical Commission can do about it?",
  ["It can direct the state to adopt the national methodology, as a statutory regulator",
   "It can examine the methods and recommend a standard, but cannot compel the state to adopt it",
   "It can compile its own estimate for the state and publish it in place of the state's",
   "It has no role, because state statistics fall entirely outside its remit"], "B",
  "Working with central and state agencies on the quality of statistical products is within the Commission's remit, so the "
  "last option is wrong. But the Commission is non-statutory and holds no power of direction, which rules out the first. "
  "Nor does it compile statistics — that is the NSO's work — so the third is wrong too. Recommendation, standard-setting "
  "and publication of the divergence are the instruments it actually has.")

q(20, "single", "hard",
  "Which pairing of a 2026 base-year revision with its release date is correct?",
  ["GDP on base 2022-23, released 27 February 2026", "CPI on base 2022-23, released 12 February 2026",
   "GDP on base 2024, released 27 February 2026", "IIP on base 2024, released May 2026"], "A",
  "The prices series moved to a 2024 base and the two quantity series to 2022-23: CPI on 12 February 2026, GDP on "
  "27 February 2026, IIP in May 2026. Each wrong option swaps the price base with a quantity base, which is the single "
  "distinction the question tests.")

BODY = dict(moduleId="official", source="mastery", topicId="official-t1",
            label="The Indian Statistical System: MoSPI, NSO and the NSC — mastery test (unseen)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/official_t1_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I)
k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s   (want easy>=6, moderate>=10, hard>=4)" % dict(d))
print("  keys       %s   (cap %d per letter)" % (dict(k), int(len(I) * 0.4)))
print("  formats    %s   (want numeric>=4, multi>=2)" % dict(f))
