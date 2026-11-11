#!/usr/bin/env python3
# Mastery pool for 10A.5 — census and vital statistics.
# Twenty unseen items, 6 easy / 10 moderate / 4 hard.
#
# Deliberately NOT tested as a bare number: the single-year IMR, since an earlier
# official release gives 27 for 2021 against 25 for 2023 — every item that uses it
# names the period.
import json, io, collections

I = []
def q(n, fmt, diff, stem, opts, ans, expl, **kw):
    it = dict(id="official-t5-m-%02d" % n, format=fmt, topic="official-t5", diff=diff,
              stem=stem, options=opts, answer=ans, explanation=expl)
    it.update(kw); I.append(it)

# ------------------------------------------------------------------ easy (6)
q(1, "numeric", "easy",
  "The first synchronous census of India was conducted in:",
  ["1872", "1881", "1891", "1948"], "B",
  "1881 was the first synchronous census — the whole country enumerated at one reference moment — and censuses have "
  "been decennial since. 1872 is the first census of India, but it was taken at different times in different parts of "
  "the country, and 1948 is the year of the Census Act.",
  check="1872 first census, 1881 first synchronous, 1948 the Act, 1949 the permanent organisation. The question asks "
        "which was synchronous.")

q(2, "single", "easy",
  "The census of India is conducted by:",
  ["The National Statistical Office, MoSPI",
   "The National Statistical Commission",
   "The Registrar General of India, Ministry of Home Affairs",
   "The Central Statistics Office"], "C",
  "The Registrar General of India, who is ex-officio Census Commissioner, in the Ministry of Home Affairs. This is the "
  "one part of Unit X that does not sit with MoSPI, and the examiner knows that the rest of the module trains you to "
  "answer MoSPI by reflex.")

q(3, "single", "easy",
  "The infant mortality rate is defined as deaths under one year of age per:",
  ["1,000 mid-year population", "1,00,000 live births", "1,000 women aged 15-49", "1,000 live births"], "D",
  "IMR is per 1,000 live births. The crude birth and death rates use mid-year population, the maternal mortality ratio "
  "uses 1,00,000 live births, and 1,000 women aged 15-49 is the denominator of the general fertility rate — every "
  "wrong option is a real denominator borrowed from a neighbouring measure.")

q(4, "single", "easy",
  "Registration of births and deaths in India is compulsory under:",
  ["The Registration of Births and Deaths Act, 1969",
   "The Census Act, 1948",
   "The Collection of Statistics Act, 2008",
   "The Census Rules, 1990"], "A",
  "The Registration of Births and Deaths Act, 1969 made registration compulsory throughout India, and was amended in "
  "2023. The Census Act, 1948 and the Census Rules, 1990 govern the census, and the Collection of Statistics Act, 2008 "
  "governs the statistical surveys of MoSPI — three different instruments for three different operations.")

q(5, "single", "easy",
  "The Sample Registration System is based on:",
  ["A dual record system", "Complete enumeration of all households",
   "Administrative returns from hospitals only", "Decennial retrospective interviews"], "A",
  "Two independent records of the same events — continuous recording by a part-time local enumerator and a half-yearly "
  "retrospective survey by a supervisor — are matched, and the mismatches are verified in the field. That matching is "
  "what lets the SRS catch events a single register would miss.")

q(6, "numeric", "easy",
  "A birth or death must be reported to the registrar within how many days of the event?",
  ["7 days", "14 days", "21 days", "30 days"], "C",
  "21 days, at the place where the event occurred, with penalties rising for delay. The figure of 30 days belongs "
  "elsewhere in the same law — it is the window for filing an appeal with the District Registrar or Chief Registrar.",
  check="21 days to report; 30 days to appeal; 90 days for the appeal to be decided. The question asks about reporting.")

# ------------------------------------------------------------------ moderate (10)
q(7, "single", "moderate",
  "For the four poll-bound States/areas named in ORGI's 5 September 2026 notification, the self-enumeration window is:",
  ["1-15 November 2026", "16-30 November 2026", "1-15 December 2026", "16-31 December 2026"], "B",
  "ORGI's schedule for Goa, Uttar Pradesh, Punjab and non-snow-bound Uttarakhand provides self-enumeration 16-30 "
  "November, Population Enumeration 1 December 2026-4 January 2027 and revisional round 5-9 January 2027.",
  check="Self-enumeration in November; door-to-door enumeration across December and early January; revisional round immediately afterwards.")

q(8, "single", "moderate",
  "Which statement about the Population Enumeration schedule of Census 2027 is correct?",
  ["All States and UTs use one identical fieldwork window in February 2027",
   "Goa, Uttar Pradesh, Punjab and non-snow-bound Uttarakhand have a separate notified schedule",
   "The self-enumeration window for the four poll-bound areas is 1-15 November 2026",
   "The revisional round for the four poll-bound areas ends on 30 November 2026"], "B",
  "ORGI's current portal lists a separate schedule for these four States/areas: self-enumeration 16-30 November "
  "2026, Population Enumeration 1 December 2026-4 January 2027 and revisional round 5-9 January 2027. Fieldwork "
  "dates must not be confused with the national reference moment.")

q(9, "multi", "moderate",
  "Consider the following statements about amendments to the Registration of Births and Deaths Act, 1969.",
  ["A and B only", "A, C and D only", "B and C only", "A, B, C and D"], "B",
  "A is correct: the 2023 amendment provides for the national database and birth-certificate provisions. B is incorrect: "
  "the delayed-registration magistrate change belongs to the 2026 amendment, not the 2023 Act. C is correct: ORGI's "
  "current page describes the parent Act as amended in both 2023 and 2026. D is correct: for information furnished "
  "more than two years after the event, the 2026 amendment requires an order of a Judicial Magistrate First Class.",
  statements=["The 2023 amendment provides for a national database of registered births and deaths under the Registrar General.",
              "The 2026 delayed-registration change was already part of the 2023 amendment.",
              "ORGI's current Vital Statistics Division page identifies amendments in both 2023 and 2026.",
              "For information furnished more than two years after the event, the 2026 change requires an order of a Judicial Magistrate First Class."],
  verdicts={"A": dict(tf=True, why="The 2023 amendment provides for the national database under the Registrar General."),
            "B": dict(tf=False, why="The delayed-registration magistrate change is in the 2026 amendment, not the 2023 amendment."),
            "C": dict(tf=True, why="ORGI's current page identifies amendments in 2023 and 2026."),
            "D": dict(tf=True, why="The 2026 amendment provides for a Judicial Magistrate First Class order after two years.")})

q(10, "single", "moderate",
  "The Sample Registration System began full-scale operations in:",
  ["1969-70", "1964-65", "1951", "1961"], "A",
  "A pilot ran in selected states in 1964-65 and full-scale operations began in 1969-70. 1951 is the year the Office of "
  "the Registrar General was set up, and both 1964-65 and 1969-70 are correct answers to different questions — which is "
  "why the question specifies full scale.")

q(11, "numeric", "moderate",
  "The age-specific fertility rates per 1,000 women for a population, in five-year groups from 15-19 to 45-49, sum to "
  "340. The total fertility rate is:",
  ["0.34", "1.70", "3.40", "17.00"], "B",
  "With five-year age groups, TFR = 5 × Σ ASFR with the rates expressed per woman: 5 × 340/1000 = 1.70. The figure 3.40 "
  "comes from forgetting the factor of 5 and dividing by 100 instead, 0.34 from omitting the factor of 5 altogether, "
  "and 17.00 from dividing by 100 — all three are the standard slips.",
  check="A TFR is a number of children, so it must be a few units. Anything above about 8 or below about 0.5 should be "
        "rechecked.")

q(12, "match", "moderate",
  "Match the system or measure in List I with its description in List II.",
  ["A-III, B-I, C-IV, D-II", "A-I, B-III, C-II, D-IV",
   "A-III, B-IV, C-I, D-II", "A-IV, B-I, C-III, D-II"], "A",
  "The census is the decennial complete count that supplies population denominators; the CRS is the continuous legal "
  "registration of individual events; the SRS is the continuous sample survey that produces India's vital rates; and "
  "the NRR is the measure for which a value of 1 is exact replacement. Each wrong option moves at least two pairs, so "
  "the mapping has to be checked rather than inferred from one recognised entry.",
  check="Anchor on the two you are certain of — the census and the NRR — then the two registration systems separate by "
        "sample versus complete.",
  pairs=[["A. Census", "I. Continuous legal registration of individual events"],
         ["B. Civil Registration System", "II. A value of 1 means exact replacement"],
         ["C. Sample Registration System", "III. Decennial complete count supplying population denominators"],
         ["D. Net reproduction rate", "IV. Continuous sample survey producing India's vital rates"]])

q(13, "single", "moderate",
  "India reports its sex ratio at birth as 918 for 2022-24. The figure is expressed as:",
  ["Males per 100 females", "Males per 1,000 females",
   "Female births as a percentage of all births", "Females per 1,000 males"], "D",
  "India's convention is females per 1,000 males, so 918 means 918 girls for every 1,000 boys — below the biological "
  "value of roughly 952. Much international work reports the ratio the other way round, as males per 100 females, "
  "where the natural value is about 105; a figure near 1,050 in a question is using that other convention.")

q(14, "numeric", "moderate",
  "If the crude birth rate is 18.3 and the crude death rate is 6.4 per 1,000 population, the natural growth rate is:",
  ["11.9 per 1,000", "24.7 per 1,000", "2.86 per 1,000", "1.2 per 1,000"], "A",
  "The natural growth rate is simply CBR minus CDR: 18.3 − 6.4 = 11.9 per 1,000. It is called natural because it "
  "excludes migration. The option 24.7 adds the two rates and 2.86 divides them, both of which are meaningless here.",
  check="Natural growth is a difference, not a sum or a ratio, and it excludes migration entirely.")

q(15, "numeric", "moderate",
  "According to ORGI's national Vital Statistics based on CRS report for 2024, released in July 2026, birth registration "
  "completeness was:",
  ["82.4% (2011)", "Earlier reported value (2023)", "99.1% (2024)", "99.4% (2024)"], "C",
  "ORGI reports birth-registration completeness of 99.1% in 2024, up from 82.4% in 2011. Death registration was 99.4% "
  "in 2024, up from 66.4% in 2011. These percentages describe completeness of registration, not demographic rates "
  "such as CBR or IMR.",
  check="Attach the year: 2024 birth registration 99.1%; death registration 99.4%.")

q(16, "multi", "moderate",
  "Consider the following statements about the Sample Registration System.",
  ["A and C only", "A, B and C only", "A, C and D only", "B, C and D only"], "C",
  "A, C and D hold: it is run by the Registrar General of India, it covered 8,839 sampling units and 8.981 million "
  "people in 2024, and it is sized so that the infant mortality rate can be estimated with a relative standard error "
  "below 15%. B is false — the SRS is an administrative survey resting on no statute, unlike the census and civil "
  "registration, each of which has its own Act.",
  statements=["It is conducted by the Office of the Registrar General of India.",
              "It operates under a statute of its own.",
              "In 2024 it covered 8,839 sampling units and 8.981 million people.",
              "Its sample is designed so that IMR has a relative standard error below 15%."],
  verdicts={"A": dict(tf=True,  why="The same body that takes the census and oversees civil registration."),
            "B": dict(tf=False, why="No statute. The Census Act 1948 covers the census and the RBD Act 1969 registration; the SRS is administrative."),
            "C": dict(tf=True,  why="And the supervisor updates each unit's population by age, sex and marital status."),
            "D": dict(tf=True,  why="The design criterion was set on a named indicator rather than by convenience.")})

# ------------------------------------------------------------------ hard (4)
q(17, "numeric", "hard",
  "A population has a total fertility rate of 2.00 and a sex ratio at birth of 900 females per 1,000 males. Taking the "
  "probability that a newborn girl survives to the mean age of childbearing as 0.90, the net reproduction rate is "
  "approximately:",
  ["1.80", "0.95", "0.85", "0.90"], "C",
  "The proportion of births that are female is 900/(900+1000) = 0.4737, not 900/1000. So GRR = 2.00 × 0.4737 = 0.947 "
  "and NRR = 0.947 × 0.90 = 0.853. The option 0.95 is the GRR, offered because candidates stop one step early, and "
  "1.80 comes from multiplying TFR by the survival probability and forgetting the daughters step altogether.",
  check="NRR must be below GRR, which must be a little under half of TFR. 0.85 < 0.95 < 1.00 passes all three checks.")

q(18, "single", "hard",
  "A statement reads: 'India's total fertility rate of 1.9 is below the replacement level, so India's population is now "
  "declining.' What is wrong with it?",
  ["The replacement level is 1.9, so the TFR is not below it",
   "A below-replacement TFR is consistent with a growing population because of the age structure",
   "The TFR of 1.9 refers to urban India only",
   "Nothing is wrong; the statement is accurate"], "B",
  "Replacement level is about 2.1, so the first half of the statement is right. The flaw is the inference: a young age "
  "structure means a large number of women are entering their childbearing years, so births continue to exceed deaths "
  "for decades after fertility falls below replacement. This is population momentum, and it is why TFR and the growth "
  "rate can point in apparently opposite directions.")

q(19, "single", "hard",
  "A district's registered births for last year are divided by its estimated population to give a birth rate. Which "
  "systems supplied the two quantities, and where does the greater uncertainty lie?",
  ["Numerator from the SRS, denominator from the CRS; the numerator is weaker",
   "Numerator from the CRS, denominator projected from the census; the denominator is weaker",
   "Both from the CRS; the two are equally reliable",
   "Numerator from the census, denominator from the SRS; the denominator is weaker"], "B",
  "A count of registered events for a named district can only come from the CRS, because the SRS is a sample and "
  "publishes no district estimates and the census does not count births. The population must be projected forward from "
  "Census 2011, since the 2021 round was postponed — so the denominator carries sixteen years of projection error, "
  "including unmeasured migration, and that dominates the uncertainty in the rate.")

q(20, "single", "hard",
  "India's sex ratio at birth for 2022-24 is 918, against a biological value of roughly 952 on the same convention. The "
  "state figures range from 978 to 872. The statistically correct reading is that:",
  ["The gap is within the sampling error of the SRS",
   "The biological value differs across Indian states",
   "The three-year averaging has biased the national figure downwards",
   "The shortfall is systematic, and the state variation must reflect behaviour rather than biology"], "D",
  "A biological constant cannot vary by state, so a range from 978 to 872 locates the variation in behaviour. Nor is "
  "the gap sampling noise: the SRS covers 8.981 million people and the figure is averaged over three years "
  "precisely to damp year-to-year variation, which reduces noise rather than introducing bias. This is the one "
  "indicator in the set that does not fit a pattern of steady improvement.")

BODY = dict(moduleId="official", source="mastery", topicId="official-t5",
            label="Census and Vital Statistics — mastery test (unseen; refreshed 12 November 2026)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/official_t5_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I); k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s" % dict(d))
print("  keys       %s" % dict(k))
print("  formats    %s" % dict(f))
