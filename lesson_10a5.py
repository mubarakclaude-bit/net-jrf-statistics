#!/usr/bin/env python3
# Lesson 10A.5 - Census and vital statistics (Unit X). Closes the module.
#
# Current position checked 12 November 2026 against ORGI's official portal:
#   Census   first census 1872 (not synchronous), first synchronous 1881; Census Act
#            1948; permanent office decided May 1949 under RGI/MHA. Census 2027:
#            Phase-I HLO 1 Apr-30 Sep 2026; Phase-II dates vary by Gazette order.
#            Goa, UP, Punjab and non-snow-bound Uttarakhand: self-enumeration 16-30
#            Nov 2026, PE 1 Dec 2026-4 Jan 2027, revisional round 5-9 Jan 2027.
#            Snow-bound areas and other States/UTs follow separate ORGI notifications.
#   CRS      RBD Act 1969, amended in 2023 and 2026; usual reporting period 21 days.
#            Official CRS 2024 registration levels: 99.1% births and 99.4% deaths
#            (national report released July 2026).
#   SRS      pilot 1964-65, full scale 1969-70; dual record system; 8,839 sampling units
#            and 8.981 million people in 2024; designed so IMR has RSE under 15%.
#   Figures  SRS 2024: CBR 18.3, CDR 6.4, IMR 24, TFR 1.9, SRB 918 (2022-24).
#            MMR 87 per lakh live births for 2022-24, down from 88 for 2021-23; SDG target 70.
import json, io

def P(*x): return list(x)
SC = []

SC.append(dict(
  kind="foundation", id="s0", title="Before the lesson — four things it will assume", mins=5,
  objective="Have the rates, the fertility measures and the life table ready, so the institutional facts attach to "
            "quantities you can compute.",
  body=P(
   "This topic has two halves that are examined differently. The institutional half — who runs the census, under which "
   "Act, on what date — is recall. The measurement half — birth rates, fertility measures, life tables — is arithmetic, "
   "and it is where the marks are easier to secure because they do not depend on remembering a year.",
   "The four checks below are the measurement half. Get them solid and the rest of the lesson is a set of names and "
   "dates hung on quantities you can already produce."),
  items=[
   dict(ask="Define the crude birth rate, crude death rate, infant mortality rate and maternal mortality ratio, and say "
            "what denominator each uses.",
     recall="CBR and CDR are events per 1,000 mid-year population. IMR is deaths under one year per 1,000 LIVE BIRTHS. "
            "MMR is maternal deaths per 1,00,000 live births. The natural growth rate is CBR minus CDR.",
     refresh=P(
      "The trap is the denominator, not the formula. CBR and CDR are per 1,000 of the whole population, which is why "
      "they are called crude: they take no account of the age structure. IMR and MMR are per live births, because "
      "infant and maternal deaths are events of childbearing, not of the population at large.",
      "MMR additionally uses a different multiplier, 1,00,000 rather than 1,000, because maternal deaths are rare. "
      "India's MMR of 87 and IMR of 24 are therefore not on the same scale at all, and a question that asks you to "
      "compare them is testing exactly that.",
      "Keep the word ratio for MMR. It is a ratio because the denominator — live births — does not contain the "
      "population at risk of a maternal death, which is pregnancies, not births.")),
   dict(ask="Define GFR, ASFR, TFR, GRR and NRR, and give the relations between them.",
     recall="GFR = births per 1,000 women aged 15-49. ASFR is the same, computed within an age group. TFR = sum of "
            "ASFRs across the reproductive span, times the width of each age group — the number of children a woman "
            "would bear under current rates. GRR = TFR × proportion of births that are female. NRR = GRR × probability "
            "of a girl surviving to the mean age of childbearing.",
     refresh=P(
      "The sequence refines a single idea. GFR fixes the crude birth rate's worst fault by using only women of "
      "reproductive age. ASFR then splits that by age, so the measure no longer depends on how women are distributed "
      "across the span. TFR sums the ASFRs into one number with a meaning you can state in words.",
      "GRR narrows TFR to daughters, because only daughters reproduce in the next generation. NRR narrows it again by "
      "letting some of those daughters die before they reproduce, so NRR = 1 is exactly replacement: each generation "
      "reproduces itself. NRR < 1 means an eventual decline, however large the current population.",
      "With five-year age groups, TFR = 5 × Σ ASFR, with ASFRs expressed per woman. Forgetting the factor of 5, or "
      "forgetting to divide by 1,000, is the most common arithmetic slip in this topic.")),
   dict(ask="What is a life table, and what do the columns lₓ, dₓ, qₓ and eₓ mean?",
     recall="A table that follows a hypothetical cohort through mortality at current age-specific rates. lₓ is the "
            "number surviving to exact age x; dₓ the deaths between x and x+1; qₓ the probability of dying in that "
            "interval; and eₓ the expectation of life at age x. An abridged life table uses five-year intervals "
            "instead of single years.",
     refresh=P(
      "The life table turns a set of age-specific death rates into a single intelligible statement: given today's "
      "mortality, how long would a newborn live. That is e₀, life expectancy at birth, and it is a property of the "
      "current rates, not a forecast about anyone alive.",
      "The internal relations are worth carrying: dₓ = lₓ − lₓ₊₁, and qₓ = dₓ / lₓ. Everything else in the table is "
      "built from the lₓ column and the person-years lived, Lₓ.",
      "The SRS publishes abridged life tables for India using five-year aggregates of its own data, which is why the "
      "life table belongs in this topic and not only in a methods paper.")),
   dict(ask="What is the difference between de jure and de facto enumeration, and between a crude and a standardised rate?",
     recall="De facto counts a person where they actually are at the reference moment; de jure counts them at their "
            "usual place of residence. A crude rate divides events by the whole population; a standardised rate "
            "reweights age-specific rates to a common age distribution so that two populations can be compared.",
     refresh=P(
      "India's census is essentially de facto, built on a single reference moment, which is why the reference moment "
      "matters so much and why houseless people are enumerated on a separate, specified night.",
      "Standardisation exists because a crude death rate is as much a statement about age structure as about mortality. "
      "A retirement town and a university town can have identical age-specific death rates and very different crude "
      "rates. Direct standardisation applies the two populations' age-specific rates to one standard age "
      "distribution; indirect standardisation applies a standard set of rates to the two age distributions.",
      "This is the reason the exam asks for crude rates and for TFR in the same breath. One is contaminated by "
      "structure and the other is not."))]))

SC.append(dict(
  kind="intuition", id="s1", title="Three systems counting the same events", mins=4,
  objective="See why India runs a census, a registration system and a sample survey at once, and what each is for.",
  body=P(
   "Births and deaths are counted three times over in India, by three different systems, and the exam's questions "
   "almost always turn on which of the three a figure came from.",
   "The census is a stock. Once a decade it counts every person where they are at a single reference moment, and that "
   "is the only operation that produces a true denominator — the population itself, by age, sex, district and village. "
   "It is enormously expensive and therefore rare.",
   "The Civil Registration System is a flow, and in principle a complete one. Every birth and death is supposed to be "
   "registered with a local registrar within 21 days, by law. Complete registration would make a sample survey "
   "unnecessary, and the national CRS report for 2024 records 99.1% birth registration and 99.4% death registration. "
   "These are completeness levels of event registration; SRS demographic rates remain a distinct statistical product.",
   "The Sample Registration System is the third: a flow measured on a sample, by a method designed to catch the events "
   "that registration misses. It exists because India needed reliable birth and death rates long before registration "
   "was anywhere near complete, and it is still the source of every rate you are asked to quote — CBR, CDR, IMR, TFR, "
   "MMR.",
   "So the division of labour is: the census gives the denominator, the SRS gives the rates, the CRS gives the legal "
   "record of each individual event. A question asking where a figure came from is asking which of those three jobs it "
   "belongs to."),
  aside=dict(h="The sentence to carry into the exam",
    body="Census = stock, decennial, complete. CRS = flow, continuous, legal, complete in principle. SRS = flow, "
         "continuous, on a sample, and the actual source of India's vital rates."),
  ask=dict(q="If civil registration reached 100% completeness tomorrow, would the Sample Registration System become "
             "redundant?",
    nudge="Ask what the SRS measures that a register of events cannot, and how you would know that registration had in "
          "fact reached 100%.")))

SC.append(dict(
  kind="theory", id="s2", title="The census — history, law and the 2027 round", mins=9,
  objective="Give the census's history, its legal and constitutional basis, its organisation, and distinguish the 2027 reference moments from region-specific fieldwork dates.",
  blocks=[
   dict(t="def", h="Origins",
     body="The first census of India was taken in 1872, but not synchronously: different parts of the country were "
          "enumerated at different times. The first synchronous census — the whole country at one reference moment — "
          "was 1881, and censuses have been decennial since. The organisation was set up afresh for each census, on an "
          "ad-hoc basis, until 1951."),
   dict(t="formula", h="Law and organisation",
     body="The Census Act, 1948 provides the legal framework and defines the duties and powers of census officers; "
          "section 15 makes the information given by an individual confidential and inadmissible as evidence. The "
          "Census Rules, 1990 sit under it. In May 1949 the Government decided to create a permanent organisation under "
          "the Registrar General of India, who is ex-officio Census Commissioner, in the Ministry of Home Affairs. "
          "Census is a Union subject, entry 69 of the Union List in the Seventh Schedule."),
   dict(t="def", h="Census 2027 — the schedule as notified by 12 November 2026",
     body="The census due in 2021 was postponed during the pandemic. Census 2027 is India's 16th census and the 8th "
          "since Independence. Phase I, Houselisting and Housing Census, was notified for 1 April to 30 September "
          "2026. Population Enumeration (Phase II) is governed by later area-specific Gazette notifications: do not "
          "memorise 'February 2027' as one uniform window for every State and Union Territory."),
   dict(t="formula", h="The later schedule for four election-bound States / areas",
     body="ORGI's 5 September 2026 notification schedules Goa, Uttar Pradesh, Punjab and non-snow-bound Uttarakhand "
          "for self-enumeration 16-30 November 2026, Population Enumeration 1 December 2026 to 4 January 2027, and "
          "revisional round 5-9 January 2027. The ORGI Census 2027 website confirms these dates. Other regions follow "
          "the separate Phase-II Gazette notification published in the ORGI catalogue on 2 November 2026; snow-bound "
          "areas have a separate order. Always identify the region before quoting fieldwork dates."),
   dict(t="step", h="Reference moments are not fieldwork windows",
     body="The national reference moment is 00:00 hours on 1 March 2027. ORGI has separate provisions for Ladakh "
          "and snow-bound areas of Jammu and Kashmir, Himachal Pradesh and Uttarakhand, with a 1 October 2026 "
          "reference moment. These reference moments define the date to which population particulars refer; they "
          "are not interchangeable with the dates on which enumerators visit households. A question may ask the "
          "reference date, self-enumeration window, field-enumeration period or revisional round — identify which."),
   dict(t="step", h="What is new in 2027",
     body="It is India's first digital census. Houselisting uses a mobile application that works offline and uploads "
          "later; an optional self-enumeration portal is available in sixteen languages and issues an SE ID that the "
          "enumerator uses to confirm the household's entry. Caste is enumerated, following the Cabinet Committee on "
          "Political Affairs decision of 30 April 2025, during Phase II. The operation engages about 31 lakh "
          "enumerators and supervisors, over one lakh census functionaries and around 18,600 technical staff."),
   dict(t="trap", h="Three things people get wrong",
     body="First, 1872 is the first census and 1881 the first SYNCHRONOUS one; a question naming one wants the other as "
          "the distractor. Second, the permanent census organisation dates from 1949, not from the Act of 1948 and not "
          "from 1951, though the office functioned from 1951. Third, the census sits with the Ministry of Home Affairs "
          "under the RGI, not with MoSPI — the whole of the rest of Unit X is MoSPI, and this topic is the exception.")],
  flow=dict(caption="Three systems, three jobs, one set of events",
    nodes=[
      dict(id="e", r=0, c=0, w=4, label="Births and deaths in India", kind="start"),
      dict(id="c", r=1, c=0, label="Census — decennial, complete", kind="step"),
      dict(id="r", r=1, c=1, label="CRS — continuous, legal", kind="step"),
      dict(id="s", r=1, c=2, w=2, label="SRS — continuous, on a sample", kind="step"),
      dict(id="m", r=2, c=0, w=4, label="Registrar General of India · Ministry of Home Affairs", kind="note"),
      dict(id="d", r=3, c=0, label="Population denominators", kind="end"),
      dict(id="l", r=3, c=1, label="Birth and death certificates", kind="end"),
      dict(id="v", r=3, c=2, w=2, label="CBR · CDR · IMR · TFR · MMR", kind="end")],
    edges=[dict({"from":"e","to":"c"}), dict({"from":"e","to":"r"}), dict({"from":"e","to":"s"}),
           dict({"from":"c","to":"m"}), dict({"from":"r","to":"m"}), dict({"from":"s","to":"m"}),
           dict({"from":"m","to":"d"}), dict({"from":"m","to":"l"}), dict({"from":"m","to":"v"})]),
  scenario=dict(
    teaser="A census due in 2021 held in 2027 — and everything downstream that had to run on 2011 numbers meanwhile.",
    title="Sixteen years between counts",
    body=P(
      "India's censuses have been decennial since 1881, through two world wars, partition and every emergency since. "
      "The 2021 round was the first to be missed. Houselisting had been scheduled for April 2020; the pandemic "
      "intervened, and the operation was postponed repeatedly until the schedule for 2027 was announced.",
      "The gap is not merely a missing data point, because a census is the only operation that produces a complete "
      "population denominator. Every rate in this lesson is events divided by population, and for the whole of that "
      "period the population came from projections rolled forward from 2011. Sampling frames for household surveys are "
      "built from census villages and urban blocks, so the NSS and the PLFS were drawing from a frame that aged by "
      "sixteen years. Delimitation of constituencies, the allocation of seats, and a long list of schemes with "
      "population-based entitlements all wait on census figures.",
      "That is the honest case for why the census is the foundation of the rest of Unit X rather than one more survey "
      "in it. The consumption survey can be run again; the price index can be rebased; but the denominator underneath "
      "all of them is produced once a decade and nothing substitutes for it.",
      "For the exam, carry the stable facts — Census 2027, 16th overall and 8th since Independence — but use the "
      "Gazette notification for the relevant State/UT when a question asks for Phase-II fieldwork dates."),
    close="A census is the denominator the whole statistical system divides by, which is why a missed one propagates "
          "into every rate.")))

SC.append(dict(
  kind="theory", id="s3", title="The Civil Registration System and the law behind it", mins=7,
  objective="State the legal basis of registration, distinguish the 2023 and 2026 amendments, and interpret the latest official completeness figures.",
  blocks=[
   dict(t="def", h="What the CRS is",
     body="The continuous, permanent and compulsory recording of births and deaths as individual legal events. The "
          "Office of the Registrar General, India, set up in 1951, oversees it and coordinates with a Chief Registrar "
          "of Births and Deaths in each state and union territory; the first annual report using civil registration "
          "data appeared in 1958. Registration is done by local registrars, and the informant must report the event "
          "within 21 days, at the place where it occurred, with penalties rising for delay."),
   dict(t="formula", h="The Registration of Births and Deaths Act, 1969",
     body="The parent Act, which made registration of births and deaths compulsory throughout India. Before it, "
          "registration existed in parts of the country under provincial law and was weakly enforced. The Act is the "
          "answer whenever a question asks for the legal basis of birth and death registration in India."),
   dict(t="def", h="The 2023 amendment — national database and certificate",
     body="The Registration of Births and Deaths (Amendment) Act, 2023 came into force on 1 October 2023. It provides "
          "for a national database maintained by the Registrar General and state databases under Chief Registrars; "
          "makes the birth certificate a single document admissible as proof of date and place of birth for specified "
          "purposes including school admission, driving licences, electoral rolls, Aadhaar, marriage registration "
          "and government employment; and provides for use of the database to update the National Population "
          "Register, electoral rolls and ration-card records, subject to data-sharing controls."),
   dict(t="step", h="The 2026 amendment — delayed registration",
     body="ORGI's current Vital Statistics Division page describes the parent Act as amended in both 2023 and 2026. "
          "The 2026 amendment changes the authority for very late registrations: where information is furnished more "
          "than two years after the event, registration requires an order of a Judicial Magistrate of the First Class. "
          "This is a change to the delayed-registration authority, not a new definition of the usual 21-day reporting "
          "period."),
   dict(t="formula", h="Current registration completeness — reference year 2024",
     body="ORGI reports that the national Vital Statistics based on Civil Registration System report for 2024 was "
          "released in July 2026. Registration levels are 99.1% for births and 99.4% for deaths in 2024, compared "
          "with 82.4% and 66.4% respectively in 2011. These are completeness levels of event registration; they are "
          "not the SRS birth rate, death rate or infant mortality rate. Keep the reference year beside every percentage."),
   dict(t="trap", h="Two bodies, two jobs, one office",
     body="The census and the CRS and the SRS all sit under the Registrar General of India in the Ministry of Home "
          "Affairs. What differs is the instrument: the Census Act, 1948 for the census, the RBD Act, 1969 for "
          "registration, and no statute at all for the SRS, which is an administrative survey.")]))

SC.append(dict(
  kind="recall", id="s4", title="Pause and recall", mins=3,
  objective="Retrieve the institutional half before the measurement half is added.",
  intro="Answer aloud, then look. Everything here was in the last two scenes.",
  items=[
   dict(q="Which year saw India's first census, and which the first synchronous one?",
     a="1872 for the first census, not held synchronously; 1881 for the first synchronous census. Decennial since."),
   dict(q="Give the Act governing the census and the Act governing registration of births and deaths.",
     a="The Census Act, 1948 for the census; the Registration of Births and Deaths Act, 1969 for registration."),
   dict(q="Who conducts the census, and under which ministry?",
     a="The Registrar General of India, ex-officio Census Commissioner, in the Ministry of Home Affairs. The permanent "
       "organisation was decided on in May 1949."),
   dict(q="For the four poll-bound States/areas in ORGI's 5 September 2026 notification, give the self-enumeration and Population Enumeration dates.",
     a="Self-enumeration 16-30 November 2026; Population Enumeration 1 December 2026 to 4 January 2027; revisional round 5-9 January 2027."),
   dict(q="What are the key current changes in the RBD Act from the 2023 and 2026 amendments?",
     a="The 2023 amendment provides for the national database and birth-certificate provisions. The 2026 amendment changes delayed-registration authority for information furnished more than two years after the event."),
   dict(q="Within how many days must a birth or death be reported to the registrar?",
     a="21 days, at the place where the event occurred.")]))

SC.append(dict(
  kind="completion", id="s5", title="Your turn — fill in the census and registration facts", mins=6,
  objective="Produce the dates, Acts and figures without prompting.",
  problem="Fill in each blank with the year, Act or figure the lesson has given.",
  steps=[
   dict(say="The census now scheduled was originally due a different year, and was postponed.",
     blank=dict(prompt="Due when, now held when, and why postponed?",
       answer="due 2021, now 2027, postponed by the pandemic",
       accept=["2021, 2027, COVID-19", "due in 2021, held 2027, COVID pandemic",
               "2021 -> 2027, pandemic", "2021 due, 2027 now, because of COVID"],
       hint="The first break in a decennial series running since 1881."),
     why="The gap and its reason are the single most likely current-affairs question in this topic."),
   dict(say="Registration of births and deaths rests on a parent Act, since amended.",
     blank=dict(prompt="Which parent Act, and which amendment year?",
       answer="Registration of Births and Deaths Act 1969, amended 2023",
       accept=["RBD Act 1969, amendment 2023", "Registration of Births and Deaths Act, 1969; 2023",
               "RBD Act, 1969 amended in 2023", "1969 Act, 2023 amendment"],
       hint="The amendment came into force on 1 October of its year."),
     why="The pairing of parent Act and amendment is how this is asked; one year alone is half an answer."),
   dict(say="The Sample Registration System ran a pilot before going to full scale.",
     blank=dict(prompt="Pilot in which year, full scale in which?", answer="pilot 1964-65, full scale 1969-70",
       accept=["1964-65 pilot, 1969-70 full scale", "1964-65 and 1969-70",
               "pilot in 1964-65; full scale from 1969-70", "1964 65 pilot 1969 70 full"],
       hint="Both are financial-year pairs, five years apart."),
     why="Two dates, and the exam picks whichever one you did not memorise."),
   dict(say="The SRS gives India's vital rates. State the 2024 birth and death rates.",
     blank=dict(prompt="CBR and CDR for 2024?", answer="CBR 18.3, CDR 6.4",
       accept=["18.3 and 6.4", "CBR 18.3 CDR 6.4", "birth rate 18.3, death rate 6.4",
               "18.3 per 1000 and 6.4 per 1000"],
       hint="Their difference is the natural growth rate, a round number."),
     why="These two numbers generate the natural growth rate and anchor every other figure in the topic."),
   dict(say="Maternal mortality is reported for a three-year period, on its own scale.",
     blank=dict(prompt="Which MMR, for which period, per what?",
       answer="87 per 1,00,000 live births for 2022-24",
       accept=["87 for 2022-24", "MMR 87, 2022-24, per lakh live births",
               "87 per lakh live births (2022-24)", "87 per 100000 live births for 2022 24"],
       hint="The SDG target for 2030 is 70 on the same scale."),
     why="The multiplier is the examinable part: MMR is per lakh, not per thousand.")],
  after="Two census dates, two Acts, two SRS dates, two rates and one ratio. That is most of the recall this topic "
        "asks for; the rest is arithmetic."))

SC.append(dict(
  kind="theory", id="s6", title="The Sample Registration System and its dual record method", mins=8,
  objective="Explain how the SRS gets a more complete count than a register, and what it publishes.",
  blocks=[
   dict(t="def", h="Why it exists, and when it started",
     body="The SRS was introduced in the 1960s as an interim measure while civil registration was far from complete, "
          "and it has outlasted that description. A pilot ran in selected states in 1964-65 and full-scale operations "
          "began in 1969-70. It is run by the Office of the Registrar General of India — the same body that takes the "
          "census — and it rests on no statute, being an administrative survey rather than a legal register."),
   dict(t="formula", h="The dual record system, which is the examinable core",
     body="Two independent records of the same events are made and then compared. First, continuous enumeration: a "
          "part-time enumerator resident in the sample unit — typically an anganwadi worker or a teacher — records "
          "every birth and death as it occurs, from families, community informants, hospitals and burial or cremation "
          "grounds, visiting urban households monthly and rural households quarterly. Second, a half-yearly "
          "retrospective survey by a full-time supervisor, independently, with a verbal autopsy form completed for each "
          "death."),
   dict(t="step", h="Matching and reconciliation",
     body="The Directorate of Census Operations matches the supervisor's list against the enumerator's. Events on one "
          "list and not the other, and apparent duplicates, are then verified in the field — by a third person, or by "
          "the supervisor and enumerator together. The supervisor also updates the sample unit's population by age, sex "
          "and marital status, which supplies the denominators. The reconciled records go to the RGI for national "
          "tabulation."),
   dict(t="def", h="Why two records beat one",
     body="A single register misses events in a pattern, not at random: deaths of the very old and the very young, "
          "events in households with no reason to approach a registrar, rural events, events to women. Two independent "
          "passes, matched, catch most of what either alone would miss, and the size of the mismatch is itself a "
          "measure of how incomplete a single pass would have been. That is the whole logic of the method, and it is "
          "the standard answer to 'why not simply use the register'."),
   dict(t="formula", h="Size and precision",
     body="In 2024 the SRS covered 8,839 sampling units and 8.981 million people. The sample is designed so that the "
          "infant mortality rate can be estimated with a relative standard error below 15% — a design criterion worth "
          "quoting, because it shows the sample size was chosen for a stated precision on a specific indicator rather "
          "than picked for convenience."),
   dict(t="step", h="What it publishes",
     body="An annual bulletin with CBR, CDR and IMR; a Statistical Report with fertility and mortality indicators "
          "including GFR, ASFR and TFR; special bulletins on maternal mortality and on causes of death, less "
          "frequently; and abridged life tables built on five-year aggregates. The UN Population Division and the RGI "
          "both use SRS estimates for population projections."),
   dict(t="trap", h="SRS against CRS",
     body="The SRS gives RATES from a sample; the CRS gives COUNTS of individually registered events. The CRS cannot "
          "give you a rate without a denominator from the census or a projection, and its completeness is itself "
          "measured against SRS rates. If a question gives you a rate for India, it came from the SRS.")],
  flow=dict(caption="The dual record system, one sample unit",
    nodes=[
      dict(id="u", r=0, c=0, w=4, label="One SRS sample unit — a village or urban block", kind="start"),
      dict(id="e", r=1, c=0, w=2, label="Part-time enumerator: continuous recording", kind="step"),
      dict(id="s", r=1, c=2, w=2, label="Supervisor: half-yearly retrospective survey", kind="step"),
      dict(id="m", r=2, c=0, w=4, label="Matching by the Directorate of Census Operations", kind="note"),
      dict(id="f", r=3, c=0, w=2, label="Unmatched or duplicate events verified in the field", kind="note"),
      dict(id="p", r=3, c=2, w=2, label="Population updated by age, sex, marital status", kind="note"),
      dict(id="o", r=4, c=0, w=4, label="RGI tabulation → CBR · CDR · IMR · TFR · MMR · life tables", kind="end")],
    edges=[dict({"from":"u","to":"e"}), dict({"from":"u","to":"s"}), dict({"from":"e","to":"m"}),
           dict({"from":"s","to":"m"}), dict({"from":"m","to":"f"}), dict({"from":"m","to":"p"}),
           dict({"from":"f","to":"o"}), dict({"from":"p","to":"o"})])))

SC.append(dict(
  kind="theory", id="s7", title="The current figures, and what each one says", mins=6,
  objective="Carry India's vital rates with their periods, and read what each implies.",
  blocks=[
   dict(t="formula", h="SRS 2024",
     body="Crude birth rate 18.3 per 1,000, down from 18.4 in 2023. Crude death rate 6.4 per 1,000. Natural growth "
          "rate therefore 11.9 per 1,000, which is CBR minus CDR and nothing more. Infant mortality rate 24 per 1,000 "
          "live births. Total fertility rate 1.9."),
   dict(t="def", h="What a TFR of 1.9 means",
     body="It is below the replacement level of 2.1, which is the TFR at which a population reproduces itself once "
          "mortality before the end of childbearing is allowed for — a little above 2 for that reason, not exactly 2. "
          "A below-replacement TFR does not mean the population is falling now: India's population continues to grow "
          "because of its young age structure, which is called population momentum. The state spread is wide: Bihar "
          "highest at 2.9, Delhi lowest at 1.2."),
   dict(t="formula", h="Sex ratio at birth, and the convention",
     body="918 for 2022-24 — females per 1,000 males, averaged over three years because the annual figure is noisy. "
          "Chhattisgarh and Kerala highest at 978 and 974 respectively; Uttarakhand lowest at 872. Note the convention: India reports the sex ratio as "
          "females per 1,000 males, while much international work reports males per 100 females. A question that gives "
          "a figure near 1,050 is using the other convention."),
   dict(t="def", h="Maternal mortality",
     body="87 per 1,00,000 live births for 2022-24, down from 88 for 2021-23 and 130 for 2014-16. The SDG target is 70 or below by 2030. "
          "MMR is published for three-year periods, not single years, because maternal deaths are too rare for an "
          "annual sample estimate to be stable — the same reason the multiplier is a lakh rather than a thousand."),
   dict(t="step", h="Reading the figures together",
     body="Birth rate falling, death rate low and flat, TFR below replacement, infant and maternal mortality falling "
          "but still above the SDG targets, and a sex ratio at birth well below the biological norm of about 950. The "
          "last is the one figure in the set that is not simply a development story, and an exam question asking which "
          "indicator does not fit the pattern of improvement is usually pointing at it."),
   dict(t="trap", h="Period labels are part of the answer",
     body="CBR, CDR, IMR and TFR are annual, currently 2024. Sex ratio at birth is a three-year average, currently "
          "2022-24. MMR is a three-year figure, currently 2022-24. Giving a correct number against the wrong period is "
          "a wrong answer, and the three different period lengths are deliberate.")],
  scenario=dict(
    teaser="One of India's vital statistics has a known biological value. Measure it, and the gap is the finding.",
    title="The one number with a benchmark",
    body=P(
      "Most vital rates have no natural level to compare against. There is no biologically correct birth rate or death "
      "rate; a figure is high or low only relative to another country or another year. The sex ratio at birth is the "
      "exception, and that is what makes it the most statistically interesting number in this topic.",
      "Across human populations, about 105 boys are born for every 100 girls — a regularity so stable that "
      "demographers treat it as a biological constant, though there is no accepted explanation for why it holds. On "
      "India's convention of females per 1,000 males, that is about 952. The excess of boys is then reversed by higher "
      "male mortality at every later age, which is why women outnumber men in the older age groups.",
      "The SRS reports India's sex ratio at birth as 918 for 2022-24. The gap between 918 and roughly 952 is not "
      "sampling error: the SRS sample covers about 8.981 million people, and the figure is averaged over three years "
      "precisely to damp the year-to-year noise. A systematic shortfall of that size, sustained over years, is "
      "evidence of something acting on the ratio before birth or at registration.",
      "The state spread makes the point sharper. Chhattisgarh reports 978 and Kerala 974; Uttarakhand "
      "reports 872, far below the biological value. A single biological constant cannot vary by state, so the variation is in the "
      "behaviour, not in the biology.",
      "For the exam, three things follow. The convention — females per 1,000 males in India, males per 100 females in "
      "much international work, so a figure near 1,050 is the other convention. The period — a three-year average, not "
      "a single year. And the reading — this is the one indicator in the set that does not fit a story of steady "
      "improvement, which is what a question asking for the odd one out is pointing at."),
    close="A statistic with a known expected value is worth more than one without: here the benchmark turns a number "
          "into a finding.")))

SC.append(dict(
  kind="guided", id="s8", title="Compute TFR, GRR and NRR from age-specific rates", mins=8,
  objective="Do the arithmetic the measurement half of this topic actually asks for.",
  problem="For a population, the age-specific fertility rates per 1,000 women are: 15-19: 30, 20-24: 120, 25-29: 130, "
          "30-34: 60, 35-39: 20, 40-44: 8, 45-49: 2. The sex ratio at birth is 918 females per 1,000 males, and the "
          "probability that a newborn girl survives to the mean age of childbearing is 0.95. Find the TFR, the GRR and "
          "the NRR, and say whether the population is replacing itself.",
  hints=["Sum the ASFRs first, then deal with the width of the age groups and the per-1,000 scale.",
         "GRR narrows TFR to daughters only, so you need the proportion of births that are female — not the ratio as "
         "given.",
         "The sex ratio is females per 1,000 males, so the proportion female is 918 divided by the total of females and "
         "males, not by 1,000."],
  solution=[
   dict(say="Sum the age-specific rates. The groups are five years wide, so TFR is five times the sum, with the "
            "per-1,000 scale divided out.",
     math="Σ ASFR = 30+120+130+60+20+8+2 = 370 per 1,000;  TFR = 5 × 370/1000 = 1.85"),
   dict(say="Convert the sex ratio into a proportion. With 918 females per 1,000 males, every 1,918 births contain 918 "
            "females.",
     math="proportion female = 918 / (918 + 1000) = 918/1918 = 0.4786"),
   dict(say="GRR is the TFR counting daughters only.",
     math="GRR = 1.85 × 0.4786 = 0.8855"),
   dict(say="NRR allows for mortality among those daughters before they reach childbearing.",
     math="NRR = 0.8855 × 0.95 = 0.8412"),
   dict(say="NRR is below 1, so each generation of women is being replaced by about 0.84 of a generation; under these "
            "rates the population would eventually decline, even though a young age structure can keep it growing for "
            "decades. Note also that TFR = 1.85 is below the replacement level of 2.1, which says the same thing in "
            "the cruder measure.",
     math="NRR = 0.84 < 1 → below replacement")],
  answer="TFR = 1.85, GRR = 0.885, NRR = 0.841. The population is below replacement.",
  check="Three checks that catch most errors. TFR must be a plausible number of children, so a few units, not "
        "hundreds — if you got 370 or 1,850 you forgot the per-1,000 scale or the factor of 5. GRR must be a little "
        "under half of TFR. NRR must be below GRR, because survival is a probability below 1."))

SC.append(dict(
  kind="trapcheck", id="s9", title="Six statements — verdict on each before you look", mins=6,
  objective="Meet the confusions this topic is built on: the three systems, the denominators and the periods.",
  intro="Each is either the standard fact or one detail moved from a neighbour.",
  items=[
   dict(claim="The census of India is conducted by the Registrar General of India under the Ministry of Home Affairs.",
     tf=True,
     why="The RGI is ex-officio Census Commissioner, and the permanent organisation was decided on in May 1949. The "
         "census is the one part of Unit X that does not sit with MoSPI."),
   dict(claim="The first census of India was held in 1881.", tf=False,
     why="The first census was 1872, held non-synchronously. 1881 is the first SYNCHRONOUS census, and decennial "
         "censuses run from there. Both years are correct answers to different questions."),
   dict(claim="The infant mortality rate is the number of deaths under one year per 1,000 mid-year population.",
     tf=False,
     why="Per 1,000 LIVE BIRTHS. The crude birth and death rates use mid-year population; IMR does not, and MMR uses "
         "live births with a multiplier of a lakh."),
   dict(claim="The Sample Registration System uses a dual record system and is run by the Registrar General of India.",
     tf=True,
     why="Continuous enumeration by a part-time local enumerator, an independent half-yearly retrospective survey by a "
         "supervisor, then matching and field verification of the mismatches."),
   dict(claim="India's maternal mortality ratio of 93 is reported per 1,000 live births.", tf=False,
     why="Per 1,00,000 live births, for the period 2022-24, down from 130 in 2014-16. The multiplier and the "
         "three-year period are both part of the correct statement."),
   dict(claim="A total fertility rate below 2.1 means India's population is already falling.", tf=False,
     why="It means fertility is below replacement, not that the population is declining. A young age structure keeps "
         "the population growing for decades afterwards — population momentum. India's TFR was 1.9 in 2024 and its "
         "population is still rising.")]))

SC.append(dict(
  kind="guided", id="s10", title="Transfer — a case the lesson has not shown you", mins=6,
  objective="Reason about which system a figure must have come from, and what that implies about its reliability.",
  problem="A question asks: 'A newspaper reports that a particular district recorded 12,400 births last year and puts "
          "the district's birth rate at 21 per 1,000. Which systems must have supplied the two figures, and what is "
          "the weakest link in that birth rate?' Nothing in your notes answers this directly.",
  hints=["Separate the numerator from the denominator and ask which system produces each.",
         "Ask whether the SRS can give you a figure for a single district.",
         "Ask where a district population figure for last year comes from, given when the last census was."],
  solution=[
   dict(say="The count of 12,400 births is a count of individually registered events for a named district, so it comes "
            "from the Civil Registration System. The SRS is a sample and does not publish district estimates; the "
            "census does not count births at all.",
     math="numerator 12,400 → CRS"),
   dict(say="A rate needs a population denominator. The census is the only complete source for a district population, "
            "and the last completed census is 2011, so last year's district population must be a projection rolled "
            "forward from 2011.",
     math="denominator → projected from Census 2011"),
   dict(say="So the weakest link is the denominator, not the numerator. Registration completeness is now high and "
            "measurable; a district population projected sixteen years beyond its census, in a district that may have "
            "gained or lost migrants, is not. Any district-level rate computed this way inherits that error.",
     math="rate = CRS count / projected population → error dominated by the projection"),
   dict(say="A secondary point worth stating: CRS completeness varies sharply by state, so in some states the "
            "numerator is also suspect. But as a general answer, the denominator is where the uncertainty sits.",
     math="Answer: numerator CRS, denominator projected census; denominator is the weak link")],
  answer="The count comes from the CRS and the population from a projection of Census 2011; the projection is the "
         "weaker of the two, which is the concrete cost of a sixteen-year gap between censuses.",
  check="The method generalises across this whole topic: for any rate, name the system behind the numerator and the "
        "system behind the denominator separately. Most questions about reliability are really questions about one or "
        "the other."))

SC.append(dict(
  kind="summary", id="s11", title="What you should now be able to do unaided", mins=3,
  objective="Compress the topic to its facts, its formulae and the one habit that answers the rest.",
  body=P(
   "The three systems. Census: a decennial complete count giving the population denominator, under the Census Act, "
   "1948 and the Census Rules, 1990, conducted by the Registrar General of India, ex-officio Census Commissioner, in "
   "the Ministry of Home Affairs; a Union subject, entry 69. CRS: continuous compulsory registration of individual "
   "events under the Registration of Births and Deaths Act, 1969, reported within 21 days, amended in 2023. SRS: a "
   "continuous sample survey giving India's vital rates, by the dual record system, with no statute behind it.",
   "Census dates. First census 1872, not synchronous; first synchronous census 1881; decennial since; permanent "
   "organisation decided May 1949. The 2021 round was postponed owing to the pandemic. Census 2027 is the 16th and "
   "8th since Independence. Phase I HLO ran 1 April to 30 September 2026. Phase-II dates vary by Gazette notification: "
   "for Goa, Uttar Pradesh, Punjab and non-snow-bound Uttarakhand, self-enumeration is 16-30 November 2026, PE is "
   "1 December 2026-4 January 2027 and the revisional round is 5-9 January 2027. The national reference moment is "
   "00:00 on 1 March 2027; notified snow-bound areas have a separate 1 October 2026 reference moment. India's first "
   "digital census includes optional self-enumeration in sixteen languages and caste enumeration.",
   "The 2023 amendment: national database under the Registrar General and state databases under Chief Registrars; "
   "birth certificate as single proof for specified purposes; controlled database use for other records. The 2026 "
   "amendment changes delayed-registration authority for information furnished more than two years after an event. "
   "CRS 2024 completeness: 99.1% birth registration and 99.4% death registration.",
   "The SRS. Pilot 1964-65, full scale 1969-70. Continuous recording by a part-time local enumerator, an independent "
   "half-yearly retrospective survey by a supervisor, matching by the Directorate of Census Operations, field "
   "verification of mismatches. 8,839 sampling units and 8.981 million people in 2024, sized so that IMR has a "
   "relative standard error below 15%. Publishes the annual bulletin, the Statistical Report, special bulletins on "
   "maternal mortality and causes of death, and abridged life tables.",
   "The figures, with their periods. SRS 2024: CBR 18.3, CDR 6.4, natural growth rate 11.9, IMR 24, TFR 1.9. Sex ratio "
   "at birth 918 for 2022-24, females per 1,000 males. MMR 87 per 1,00,000 live births for 2022-24, from 130 for "
   "2014-16, against an SDG target of 70 by 2030.",
   "The formulae. CBR and CDR per 1,000 mid-year population; IMR per 1,000 live births; MMR per 1,00,000 live births. "
   "TFR = 5 × Σ ASFR with five-year groups and rates per woman. GRR = TFR × proportion of births female. NRR = GRR × "
   "survival of a daughter to the mean age of childbearing, and NRR = 1 is exact replacement. Life table: dₓ = lₓ − "
   "lₓ₊₁, qₓ = dₓ / lₓ, e₀ is life expectancy at birth.",
   "The habit. For any rate in this topic, name the system behind the numerator and the system behind the denominator "
   "separately. Nearly every question about where a figure came from, or how much to trust it, falls out of that one "
   "step.")))

SC.append(dict(kind="quiz", id="s12", title="Mastery test", mins=12,
  objective="Ten unseen questions, drawn 3 easy / 5 moderate / 2 hard.", setId="official_t5_mastery"))

LES = dict(
  id="officialt5", moduleId="official", topicId="official-t5",
  title="Census and Vital Statistics",
  breadcrumb="Official Statistics → Indian Statistical System → Census and vital statistics",
  engine="A", engineName="Institutions and official statistics — who counts what, how often, and on what denominator",
  estMin=sum(s["mins"] for s in SC), version="1.2", status="approved",
  provenance="Revised and checked on 12 November 2026. Every institutional and numerical fact was checked against a "
             "primary or official source rather than recalled, because the census schedule and the registration law "
             "both changed after most textbook material was written: the PIB release on Census 2027 for the two "
             "Census 2027 area-specific fieldwork dates and Gazette schedule; the census website's own "
             "history page for 1872, 1881, the Census Act 1948 and the May 1949 decision to create a permanent "
             "organisation; the Registration of Births and Deaths (Amendment) Act, 2023 for the national database and "
             "the 1 October 2023 commencement; a CRS/SRS explainer for the dual record system, the 1964-65 pilot and "
             "1969-70 full scale, the 8,839 sampling units and the 2024 CRS completeness figures; the SRS Statistical Report "
             "2024 for current annual CBR, CDR, IMR and TFR and the 2022-24 sex ratio at birth; and the SRS Special "
             "Bulletin on Maternal Mortality 2022-24 for MMR 87. The lesson distinguishes annual rates from three-year "
             "pooled indicators and attaches the reference period to every current figure.",
  objectives=[
    "Distinguish the census, the Civil Registration System and the Sample Registration System by what each measures "
    "and what each is used for.",
    "Give the census's history, legal basis and organisation, and the full Census 2027 schedule with both reference moments.",
    "State what the Registration of Births and Deaths (Amendment) Act, 2023 changed, and from when.",
    "Explain the SRS dual record system and say why two independent records beat one register.",
    "Quote India's current vital rates with their correct periods and denominators.",
    "Compute TFR, GRR and NRR from age-specific fertility rates and read whether a population is replacing itself."],
  prereq=[
    dict(id="p1", name="Vital rates and their denominators",
         why="CBR and CDR use mid-year population, IMR uses live births, MMR uses live births per lakh; the denominator "
             "is what the exam tests."),
    dict(id="p2", name="Fertility measures: GFR, ASFR, TFR, GRR, NRR",
         why="The computation scene needs the chain from age-specific rates to the net reproduction rate."),
    dict(id="p3", name="Life tables and their columns",
         why="The SRS publishes abridged life tables, and lₓ, dₓ, qₓ and eₓ have to mean something."),
    dict(id="p4", name="De jure versus de facto enumeration, crude versus standardised rates",
         why="India's census rests on a single reference moment, and crude rates are contaminated by age structure.")],
  mastery={"minQ":10, "pass":80, "draw":10, "fmtMin":{"numeric":70,"multi":70},
    "diffMix":{"easy":3,"moderate":5,"hard":2}, "noHints":True, "retestDays":7,
    "note":"Platform settings, not an NTA rule. Ten drawn from a pool of twenty at 3 easy / 5 moderate / 2 hard; a "
           "retake draws again, holding the mix and pulling back items previously got wrong."},
  refs=[
    dict(title="Census 2027 — Phase-II notifications and local schedules",
         where="Population Enumeration dates by notified region; poll-bound States/areas have a separate schedule",
         site="Office of the Registrar General and Census Commissioner, India",
         url="https://censusindia.gov.in/census.website/en",
         type="Official portal with Gazette notification links", free=True, checked="2026-11-12",
         why="The ORGI portal lists the Phase-II Gazette notification published 2 November 2026, the snow-bound areas "
             "order and the separate schedule for Goa, Uttar Pradesh, Punjab and non-snow-bound Uttarakhand."),
    dict(title="Vital Statistics Division — Civil Registration System and current completeness",
         where="The Act as amended in 2023 and 2026; 21-day reporting period; 2024 registration levels; SRS method",
         site="Office of the Registrar General and Census Commissioner, India",
         url="https://www.censusindia.gov.in/census.website/en/node/180",
         type="Official government page", free=True, checked="2026-11-12",
         why="Current official source for the RBD Act amendment history, 2024 CRS completeness and SRS dual-record method."),
    dict(title="Sample Registration System Statistical Report 2024",
         where="CBR, CDR, IMR, TFR, sex ratio at birth and 2024 sample coverage",
         site="Office of the Registrar General and Census Commissioner, India",
         url="https://censusindia.gov.in/nada/index.php/catalog/47152",
         type="Official statistical report", free=True, checked="2026-11-12",
         why="Latest annual SRS report available at the time of this revision; includes 2024 vital rates, the 2022-24 sex ratio at birth and the 8,839-unit sample coverage."),
    dict(title="SRS Special Bulletin on Maternal Mortality in India 2022-24",
         where="Latest maternal mortality ratio and three-year reference period",
         site="Office of the Registrar General and Census Commissioner, India",
         url="https://censusindia.gov.in/nada/index.php/catalog/47151",
         type="Official statistical bulletin", free=True, checked="2026-11-12",
         why="Primary source for the national MMR of 87 per 1,00,000 live births for 2022-24, compared with 88 for 2021-23.")],
  revision=dict(
    sheet=[
      "Census = stock, decennial, complete. CRS = flow, continuous, legal. SRS = flow, continuous, on a sample.",
      "First census 1872 (non-synchronous); first synchronous census 1881; decennial since.",
      "Census Act, 1948 and Census Rules, 1990; section 15 makes individual information confidential.",
      "Permanent census organisation decided May 1949, under the RGI, ex-officio Census Commissioner, MHA.",
      "Census is a Union subject — entry 69 of the Union List, Seventh Schedule.",
      "2021 census postponed owing to the pandemic; Census 2027 is the 16th, and the 8th since Independence.",
      "Census 2027 Phase I HLO: 1 Apr-30 Sep 2026; Phase-II field dates differ by region and Gazette notification.",
      "Reference moments: 00:00 on 1 Mar 2027; 00:00 on 1 Oct 2026 for Ladakh and snow-bound J&K, HP, Uttarakhand.",
      "First digital census; optional self-enumeration in 16 languages; caste enumerated (decision 30 Apr 2025).",
      "About 31 lakh enumerators and supervisors, plus over 1 lakh functionaries.",
      "CRS: RGI set up 1951; Registration of Births and Deaths Act, 1969; report within 21 days.",
      "RBD (Amendment) Act, 2023 in force 1 Oct 2023: national database, birth certificate as single proof.",
      "CRS 2024 registration completeness: 99.1% births and 99.4% deaths (national report released July 2026).",
      "SRS: pilot 1964-65, full scale 1969-70; run by the RGI; no statute behind it.",
      "SRS dual record: continuous enumeration + independent half-yearly survey, then matching and field verification.",
      "SRS 2024: 8,839 sampling units and 8.981 million people; sized for IMR with RSE under 15%.",
      "SRS 2024 rates: CBR 18.3, CDR 6.4, natural growth 11.9, IMR 24, TFR 1.9.",
      "Sex ratio at birth 918 (2022-24), females per 1,000 males; Chhattisgarh 978 and Kerala 974 highest, Uttarakhand 872 lowest.",
      "MMR 87 per 1,00,000 live births (2022-24), down from 88 (2021-23) and 130 (2014-16); SDG target 70 by 2030.",
      "TFR = 5 × Σ ASFR (five-year groups, rates per woman); GRR = TFR × proportion female; NRR = GRR × survival.",
      "Life table: dₓ = lₓ − lₓ₊₁; qₓ = dₓ / lₓ; e₀ = life expectancy at birth; abridged = five-year intervals."],
    cards=[
      ["First census, and first synchronous census", "1872 and 1881"],
      ["Act behind the census, and behind registration", "Census Act 1948; RBD Act 1969"],
      ["Who conducts the census, under which ministry", "Registrar General of India, ex-officio Census Commissioner, MHA"],
      ["Census 2027 reference moments", "National: 00:00 1 Mar 2027; notified snow-bound areas: 1 Oct 2026"],
      ["The 2023 RBD amendment", "National database and birth-certificate provisions; commenced 1 Oct 2023"],
      ["SRS pilot and full scale", "1964-65 and 1969-70"],
      ["The SRS method", "Dual record: continuous enumeration + half-yearly survey, then matching"],
      ["SRS 2024 CBR, CDR, IMR, TFR", "18.3, 6.4, 24, 1.9"],
      ["MMR and its period and scale", "87 per 1,00,000 live births, 2022-24"],
      ["TFR from five-year ASFRs", "TFR = 5 × Σ ASFR, rates per woman"],
      ["NRR = 1 means", "Exact replacement — each generation reproduces itself"]],
    tricks=[
      dict(hook="Census for the denominator, SRS for the rate, CRS for the certificate",
           why="One line separates the three systems, and most questions in this topic are asking which one a figure "
               "came from."),
      dict(hook="1872 first, 1881 first synchronous",
           why="Both years are right answers to different questions, and each is the other's distractor."),
      dict(hook="Home Affairs, not Statistics",
           why="The census and both registration systems sit with the RGI under the MHA. The rest of Unit X is MoSPI; "
               "this topic is the exception."),
      dict(hook="Thousand, thousand, thousand, lakh",
           why="CBR and CDR per 1,000 population, IMR per 1,000 live births, MMR per 1,00,000 live births. The "
               "denominators change and so does the multiplier."),
      dict(hook="Five times the sum, then halve it twice over",
           why="TFR = 5 × Σ ASFR; GRR is a little under half of that; NRR is a little under GRR. The sizes alone catch "
               "most arithmetic slips."),
      dict(hook="Below replacement is not the same as falling",
           why="A TFR of 1.9 with a young age structure still gives a growing population — population momentum.")],
    shortcuts=[
      "Any option giving the census to MoSPI is wrong; it is the RGI under the Ministry of Home Affairs.",
      "Any option putting IMR per 1,000 population, or MMR per 1,000 live births, is wrong.",
      "If a question quotes a vital RATE for India, the source is the SRS, not the CRS.",
      "If it quotes a COUNT of registered events for a named district, the source is the CRS.",
      "Any option saying a below-replacement TFR means a falling population is wrong.",
      "For Census 2027, separate the reference moment from the date enumerators visit; check the Gazette notice for the State/UT."],
    remember=[
      "For any rate, name the system behind the numerator and the system behind the denominator separately.",
      "Attach the period to every figure: annual for CBR, CDR, IMR and TFR; three-year for the sex ratio at birth and "
      "for MMR."],
    traps=[
      "Saying the first census of India was 1881; that is the first synchronous one.",
      "Dating the permanent census organisation to 1948 or 1951 instead of the May 1949 decision.",
      "Putting the census or the SRS under MoSPI rather than the RGI in the Ministry of Home Affairs.",
      "Quoting MMR per 1,000 live births, or against a single year rather than 2022-24.",
      "Quoting the sex ratio at birth as a 2023 figure; it is a 2022-24 average.",
      "Forgetting the factor of 5 or the per-1,000 scale when computing TFR from five-year ASFRs.",
      "Taking the proportion of female births as 918/1000 rather than 918/1918.",
      "Treating a TFR below 2.1 as proof that the population is already declining.",
      "Citing CRS completeness as independent evidence that the SRS is unnecessary; it is computed from SRS rates."]),
  traps=[
    "1872 is the first census; 1881 is the first synchronous one.",
    "The census, the CRS and the SRS all sit under the RGI in the Ministry of Home Affairs, not MoSPI.",
    "IMR is per 1,000 live births, not per 1,000 population; MMR is per 1,00,000 live births.",
    "Census 2027 has area-specific fieldwork windows. Separate reference moments from fieldwork dates and use the Gazette notice for the State/UT.",
    "The SRS rests on no statute; the census has the Census Act 1948 and registration the RBD Act 1969.",
    "The proportion of births that are female is 918/1918, not 918/1000.",
    "A TFR below replacement does not mean the population is falling — population momentum.",
    "CRS completeness is measured against SRS-based estimates, so it cannot justify retiring the SRS."],
  scenes=SC)

json.dump(LES, io.open("seed/lesson_10a5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
k = {}
for s in SC: k[s["kind"]] = k.get(s["kind"], 0) + 1
print("lesson 10A.5 written: %d scenes %s" % (len(SC), k))
print("  flow %d · scenarios %d · est %d min" %
      (len([s for s in SC if s.get("flow")]), len([s for s in SC if s.get("scenario")]), LES["estMin"]))
