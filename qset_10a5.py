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
q(7, "numeric", "moderate",
  "The reference moment for Census 2027, for the country as a whole, is 00:00 hours on:",
  ["1 October 2026", "1 February 2027", "1 March 2027", "1 April 2026"], "C",
  "00:00 hours on 1 March 2027. The date 1 October 2026 is the separate reference moment for Ladakh and the snow-bound "
  "areas of Jammu and Kashmir, Himachal Pradesh and Uttarakhand; February 2027 is when Phase II enumeration is carried "
  "out; and April 2026 is when Phase I houselisting begins.",
  check="Houselisting Apr-Sep 2026; enumeration Feb 2027; reference moments 1 Mar 2027 and 1 Oct 2026. The question "
        "asks for the national reference moment.")

q(8, "single", "moderate",
  "Which of the following is NOT a feature announced for Census 2027?",
  ["Enumeration of caste",
   "Optional self-enumeration through a portal",
   "Collection of houselisting data on a mobile application",
   "A single reference moment for the whole country"], "D",
  "There are two reference moments, not one: 1 March 2027 for the country and 1 October 2026 for Ladakh and the "
  "snow-bound areas of Jammu and Kashmir, Himachal Pradesh and Uttarakhand, where Phase II is held in September 2026. "
  "Caste enumeration, self-enumeration in sixteen languages and the offline-capable mobile app are all genuine "
  "features of India's first digital census.")

q(9, "multi", "moderate",
  "Consider the following statements about the Registration of Births and Deaths (Amendment) Act, 2023.",
  ["A and B only", "A, B and C only", "B, C and D only", "A, B, C and D"], "D",
  "All four hold. The Act came into force on 1 October 2023; it creates a national database of registered births and "
  "deaths maintained by the Registrar General, with state databases under Chief Registrars; it makes the birth "
  "certificate a single document admissible as proof of date and place of birth for a listed set of purposes; and it "
  "permits the database to be used to update the National Population Register and electoral rolls, with central "
  "approval needed for wider sharing.",
  statements=["It came into force on 1 October 2023.",
              "It creates a national database of registered births and deaths under the Registrar General.",
              "It makes the birth certificate a single document of proof of date and place of birth.",
              "It allows the database to be used to update the National Population Register and electoral rolls."],
  verdicts={"A": dict(tf=True,  why="Act No. 20 of 2023, commencing 1 October 2023."),
            "B": dict(tf=True,  why="With Chief Registrars maintaining the corresponding state-level databases."),
            "C": dict(tf=True,  why="For school admission, driving licences, electoral rolls, Aadhaar, marriage registration and government employment."),
            "D": dict(tf=True,  why="Central government approval is needed to share it beyond those uses.")})

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
  "India reports its sex ratio at birth as 917 for 2021-23. The figure is expressed as:",
  ["Males per 100 females", "Males per 1,000 females",
   "Female births as a percentage of all births", "Females per 1,000 males"], "D",
  "India's convention is females per 1,000 males, so 917 means 917 girls for every 1,000 boys — below the biological "
  "value of roughly 952. Much international work reports the ratio the other way round, as males per 100 females, "
  "where the natural value is about 105; a figure near 1,050 in a question is using that other convention.")

q(14, "numeric", "moderate",
  "If the crude birth rate is 18.4 and the crude death rate is 6.4 per 1,000 population, the natural growth rate is:",
  ["12.0 per 1,000", "24.8 per 1,000", "2.88 per 1,000", "1.2 per 1,000"], "A",
  "The natural growth rate is simply CBR minus CDR: 18.4 − 6.4 = 12.0 per 1,000. It is called natural because it "
  "excludes migration. The option 24.8 adds the two rates and 2.88 divides them, both of which are meaningless here.",
  check="Natural growth is a difference, not a sum or a ratio, and it excludes migration entirely.")

q(15, "single", "moderate",
  "The completeness of India's Civil Registration System — 98.4% of births in 2023 — is computed by dividing registered "
  "events by:",
  ["The number of events reported by medical institutions",
   "Events estimated by applying SRS rates to a projected population",
   "Events counted in the most recent census",
   "The number of certificates issued"], "B",
  "Registered events are divided by estimated events, and the estimate comes from applying SRS rates to a projected "
  "population. That is why a high completeness figure cannot by itself justify retiring the SRS: the measure of the "
  "register's completeness is derived from the survey the register would be replacing.")

q(16, "multi", "moderate",
  "Consider the following statements about the Sample Registration System.",
  ["A and C only", "A, B and C only", "A, C and D only", "B, C and D only"], "C",
  "A, C and D hold: it is run by the Registrar General of India, it covered 8,839 sampling units and over 8.8 million "
  "people by 2023, and it is sized so that the infant mortality rate can be estimated with a relative standard error "
  "below 15%. B is false — the SRS is an administrative survey resting on no statute, unlike the census and civil "
  "registration, each of which has its own Act.",
  statements=["It is conducted by the Office of the Registrar General of India.",
              "It operates under a statute of its own.",
              "By 2023 it covered 8,839 sampling units and over 8.8 million people.",
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
  "India's sex ratio at birth for 2021-23 is 917, against a biological value of roughly 952 on the same convention. The "
  "state figures range from 974 to 868. The statistically correct reading is that:",
  ["The gap is within the sampling error of the SRS",
   "The biological value differs across Indian states",
   "The three-year averaging has biased the national figure downwards",
   "The shortfall is systematic, and the state variation must reflect behaviour rather than biology"], "D",
  "A biological constant cannot vary by state, so a range from 974 to 868 locates the variation in behaviour. Nor is "
  "the gap sampling noise: the SRS covers over 8.8 million people and the figure is averaged over three years "
  "precisely to damp year-to-year variation, which reduces noise rather than introducing bias. This is the one "
  "indicator in the set that does not fit a pattern of steady improvement.")

BODY = dict(moduleId="official", source="mastery", topicId="official-t5",
            label="Census and Vital Statistics — mastery test (unseen)",
            count=len(I), items=I)
json.dump(BODY, io.open("seed/official_t5_mastery.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = collections.Counter(x["diff"] for x in I); k = collections.Counter(x["answer"] for x in I)
f = collections.Counter(x["format"] for x in I)
print("pool: %d items" % len(I))
print("  difficulty %s" % dict(d))
print("  keys       %s" % dict(k))
print("  formats    %s" % dict(f))
