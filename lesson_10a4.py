#!/usr/bin/env python3
# Lesson 10A.4 - Major surveys and indices (Unit X).
#
# Everything institutional here is volatile, so it was checked against primary
# sources in October 2026 rather than recalled:
#   CPI   base 2024=100, first release 12 Feb 2026 (PIB), COICOP 2018, 358 items,
#         linking factors 0.5222/0.5320/0.5267 applied by MULTIPLYING the old index.
#   IIP   base 2022-23=100, base report 25 May 2026, first release 1 Jun 2026,
#         general linking factor 1.3834 (defined the other way round).
#   WPI   base revised to 2022-23, launched with the Output PPI on 15 Jun 2026;
#         WPI continues to be published alongside Output PPI, trial Input PPI and phased Services PPIs.
#   PLFS  revamped Jan 2025: monthly all-India CWS bulletins, quarterly rural+urban,
#         annual on a calendar year, 22,692 FSUs and 12 households per FSU.
#   HCES  2022-23 and 2023-24 rounds; MPCE 4,122 rural / 6,996 urban in 2023-24.
#   NFHS institutional responsibility: MoHFW, with IIPS Mumbai as nodal agency; verify round-specific releases before quoting results.
#   ASI   2023-24 results released 27 Aug 2025; 2,60,061 factories.
import json, io

def P(*x): return list(x)
SC = []

SC.append(dict(
  kind="foundation", id="s0", title="Before the lesson — four things it will assume", mins=5,
  objective="Have the index-number machinery and the survey vocabulary ready, so the institutional facts attach to ideas "
            "rather than floating free.",
  body=P(
   "This topic sits at the join of two things you already half-know. One is index numbers, which you met as formulae. "
   "The other is sample surveys, which you met as designs. Unit X asks what India actually builds with them, and the "
   "questions are a mark each.",
   "The four checks below are the machinery. If they are solid, the rest of this lesson is a set of names, years and "
   "weights hung on a frame you already have. If they are not, the names will be a list to forget."),
  items=[
   dict(ask="Write the Laspeyres, Paasche and Fisher price index formulae, and say which weights each uses.",
     recall="Laspeyres uses base-period quantities: P_L = Σp₁q₀ / Σp₀q₀. Paasche uses current-period quantities: "
            "P_P = Σp₁q₁ / Σp₀q₁. Fisher is their geometric mean: P_F = √(P_L × P_P).",
     refresh=P(
      "The whole difference is which basket you price. Laspeyres asks what the base-year basket costs now; Paasche asks "
      "what the current basket would have cost then. Laspeyres needs quantities only once, so it is what statistical "
      "offices actually use.",
      "Laspeyres has an upward bias and Paasche a downward one, because neither lets the basket respond to the price "
      "change it is measuring. Fisher's geometric mean splits the difference and satisfies the time-reversal and "
      "factor-reversal tests, which is why it is called the ideal index.",
      "India's CPI is a modified Laspeyres index — a fixed basket, repriced. That one sentence explains why the basket "
      "has to be replaced every so often, which is what a base-year revision is.")),
   dict(ask="What is a base year, and what does it mean to rebase an index and link the two series?",
     recall="The base year is the period set equal to 100, whose basket and weights the index carries. Rebasing replaces "
            "that period, basket and weight set. Linking is the arithmetic that puts the old series onto the new base, "
            "using a factor estimated from a period in which both series ran.",
     refresh=P(
      "An index with a fixed basket drifts out of date: items disappear, new ones appear, and spending patterns move. "
      "Rebasing resets the basket to a recent consumption or production pattern.",
      "The cost is comparability. The new series is not the old one continued, so a linking factor is computed from an "
      "overlap period and applied to the old numbers. It works at the top level and usually nowhere below it, because "
      "the two baskets are not classified the same way.",
      "Keep a sharp distinction between a base year being revised and a series being discontinued. Both have happened in "
      "India recently, to different indices, and a question will put one where the other belongs.")),
   dict(ask="What is a multistage stratified sample, and what is a first stage unit?",
     recall="A design that selects larger units first and smaller ones within them, with the population divided into "
            "strata and sampling done independently inside each. The first stage unit is the larger unit selected first "
            "— in Indian household surveys, a census village in rural areas and an urban frame survey block in towns.",
     refresh=P(
      "You cannot list every household in India, so you list villages and blocks, select some, then list households only "
      "inside the selected ones. That is the multistage idea, and it exists to make the frame manageable.",
      "Stratification — by state, by district, by distance from a city — reduces variance and guarantees that each "
      "stratum is represented. Sampling independently within strata is what lets the office publish state-level numbers.",
      "The arithmetic to carry: sample size in these surveys is usually quoted as first stage units times households per "
      "unit. When a survey is redesigned, those two numbers are what change, and the exam asks for them.")),
   dict(ask="What is the difference between a nominal and a real series, and what is a deflator?",
     recall="A nominal series is measured in the prices of its own period; a real series is measured in the prices of a "
            "fixed period, so that only quantity changes remain. A deflator is the price index used to divide the "
            "nominal series into the real one.",
     refresh=P(
      "If output in rupees rose 12% and prices rose 5%, real output rose by roughly 7% — more precisely, by the ratio of "
      "the two indices. The price index doing the dividing is the deflator.",
      "This is where the indices in this lesson stop being bookkeeping. The wholesale index is the deflator for much of "
      "the industrial production series; the consumer index is the one that enters wage indexation and the inflation "
      "target.",
      "So a change in one index propagates. That is the reason base-year revisions are news, and the reason the exam "
      "treats the three indices as one connected system rather than three separate facts."))]))

SC.append(dict(
  kind="intuition", id="s1", title="Why surveys and indices are one topic", mins=4,
  objective="See the chain that runs from a household interview to the inflation number, so the facts have an order.",
  body=P(
   "A syllabus line that reads 'major surveys and indices' looks like two lists to memorise. It is really one chain, and "
   "the chain is what makes the facts stick.",
   "Start at the bottom. A household survey asks what people bought and what it cost. Aggregate that and you have a "
   "consumption pattern — the share of spending that goes on cereals, rent, transport, phone bills. That pattern is the "
   "weight set for a price index. The price index is then produced monthly from a far cheaper operation: field staff who "
   "only collect prices, not quantities, because the quantities are frozen in the weights.",
   "So the expensive survey happens once a decade or so, and the cheap index runs every month off its back. When the "
   "consumption pattern has moved far enough that the frozen basket misleads, you run the survey again and rebase. India "
   "did exactly this: the Household Consumption Expenditure Survey of 2023-24 supplied the basket and weights for the "
   "consumer price index on base 2024=100.",
   "The same logic runs on the production side. An annual census of factories and an industrial survey establish what the "
   "industrial sector makes and in what proportions; the monthly production index then tracks a fixed set of items with "
   "those weights. And the national accounts sit on top of all of it, using the price indices as deflators.",
   "That is the whole architecture: surveys set the weights, indices run on them, accounts consume both."),
  aside=dict(h="The sentence to carry into the exam",
    body="Surveys are infrequent and measure quantities; indices are frequent and measure prices against frozen "
         "quantities. A base-year revision is the moment the newest survey replaces the old weights."),
  ask=dict(q="If the consumer price index freezes quantities from a survey, what happens to measured inflation when "
             "people respond to a price rise by buying less of the item?",
    nudge="Think about which basket is being priced, and whether the index is allowed to notice the substitution.")))

SC.append(dict(
  kind="theory", id="s2", title="The National Sample Survey and what grew out of it", mins=9,
  objective="Place the NSS, its round structure, and the four surveys that now descend from it.",
  blocks=[
   dict(t="def", h="The National Sample Survey",
     body="Set up in 1950 on Mahalanobis's design, the National Sample Survey is the country's large-scale household "
          "survey programme and one of the oldest in the world. Work is organised into rounds, each round covering a set "
          "of subjects over a stated period. Rounds that carry a full-scale subject enquiry are the large or "
          "quinquennial rounds; the lighter ones in between are the thin rounds. The field and processing organisation, "
          "the NSSO, was merged into the National Statistical Office in 2019, so current releases say NSO, MoSPI."),
   dict(t="step", h="What the programme covers",
     body="Household consumption expenditure; employment and unemployment; land and livestock holdings; debt and "
          "investment; housing conditions; health, education and social consumption; unincorporated enterprises; and "
          "the Annual Survey of Industries on the factory side. The subjects rotate across rounds, which is why a "
          "question about 'which round covered X' is a question about the rotation."),
   dict(t="formula", h="The four you must be able to name",
     body="HCES — Household Consumption Expenditure Survey, the consumption survey, which sets the CPI weights and the "
          "poverty estimates. PLFS — Periodic Labour Force Survey, the labour survey, which replaced the quinquennial "
          "Employment and Unemployment Survey in 2017. ASI — Annual Survey of Industries, the registered factory "
          "sector. ASUSE — Annual Survey of Unincorporated Sector Enterprises, the unregistered counterpart."),
   dict(t="def", h="ASI and ASUSE — the two halves of one picture",
     body="ASI covers factories registered under sections 2m(i) and 2m(ii) of the Factories Act, 1948, together with "
          "bidi and cigar establishments under the Act of 1966 and certain electricity undertakings; it is collected "
          "under the Collection of Statistics Act, 2008 as amended in 2017. Its 2023-24 results, released in August "
          "2025, covered 2,60,061 factories. ASUSE covers the unincorporated non-agricultural enterprises that ASI by "
          "definition misses — the far larger employer. Together they are the formal and informal halves of the "
          "non-agricultural economy."),
   dict(t="step", h="Surveys outside MoSPI",
     body="Two major surveys belong to other ministries and are examined all the same. The National Family Health Survey "
          "is conducted by the Ministry of Health and Family Welfare with the International Institute for Population "
          "Sciences, Mumbai, as nodal agency. Quote NFHS indicators only with the published round and reference period; "
          "do not infer NFHS-6 results without the corresponding official report. The Annual Health Survey and the "
          "Sample Registration System belong to the civil registration side and are the next topic's business."),
   dict(t="trap", h="The 2017-18 round that was never published",
     body="A consumption round was fielded in 2017-18 and its results were withheld in November 2019 on stated grounds "
          "of data quality, after figures from it had leaked. That is why the consumption series jumps from 2011-12 to "
          "2022-23, and why the 2022-23 and 2023-24 rounds are not directly comparable with 2011-12 either. A question "
          "asking for 'the previous consumption survey before 2022-23' wants 2011-12, not 2017-18."),
   dict(t="note", h="The NFHS rounds, since they are asked plainly",
     body="The five published rounds are NFHS-1 (1992-93), NFHS-2 (1998-99), NFHS-3 (2005-06), NFHS-4 (2015-16) and "
          "NFHS-5 (2019-21). The long gap is between rounds 3 and 4. Do not treat an announced or ongoing round as a "
          "published source of indicators.")],
  flow=dict(caption="From one survey programme to the surveys and indices in use today",
    nodes=[
      dict(id="n", r=0, c=1, w=2, label="National Sample Survey, 1950", kind="start"),
      dict(id="o", r=1, c=0, w=4, label="NSSO merged into the NSO, 2019 · MoSPI", kind="note"),
      dict(id="h", r=2, c=0, label="HCES (consumption)", kind="step"),
      dict(id="p", r=2, c=1, label="PLFS (labour)", kind="step"),
      dict(id="a", r=2, c=2, label="ASI (factories)", kind="step"),
      dict(id="u", r=2, c=3, label="ASUSE (unincorporated)", kind="step"),
      dict(id="c", r=3, c=0, label="CPI weights · poverty", kind="end"),
      dict(id="l", r=3, c=1, label="LFPR · WPR · UR", kind="end"),
      dict(id="i", r=3, c=2, w=2, label="IIP weights · national accounts", kind="end")],
    edges=[dict({"from":"n","to":"o"}), dict({"from":"o","to":"h"}), dict({"from":"o","to":"p"}),
           dict({"from":"o","to":"a"}), dict({"from":"o","to":"u"}), dict({"from":"h","to":"c"}),
           dict({"from":"p","to":"l"}), dict({"from":"a","to":"i"}), dict({"from":"u","to":"i"})]),
  scenario=dict(
    teaser="A completed national survey whose results were never published — and the eleven-year hole it left.",
    title="The consumption round of 2017-18",
    body=P(
      "A consumption survey was fielded across India in 2017-18. The field work was done, the data were processed, and a "
      "report was prepared. In November 2019 the government announced that the results would not be released, citing "
      "the quality of the data. By then figures from the draft had already appeared in the press.",
      "The decision is the reason the published consumption series runs 2011-12, then nothing, then 2022-23. Eleven "
      "years is a long time for a survey whose output sets the weights of the consumer price index and anchors the "
      "poverty estimates. For that whole period, the CPI ran on a basket drawn from 2011-12 consumption patterns, and "
      "India had no fresh official measure of what households were spending.",
      "The episode belongs in this topic for three reasons. It explains the gap, which is a factual question. It "
      "explains why two consumption rounds were then run back to back, in 2022-23 and 2023-24, instead of the usual "
      "single quinquennial round — the system was rebuilding a series, not just taking its next reading. And it is the "
      "concrete case behind the general concern about the credibility of official statistics that runs through the whole "
      "of Unit X, alongside the 2024 dissolution of the Standing Committee on Statistics.",
      "Treat the facts carefully in an answer. What is established is that the round was conducted, that the results "
      "were withheld in November 2019, and that the stated reason was data quality. Whether the data were in fact poor "
      "is contested, and an exam answer does not need to take a side on it."),
    close="A survey is only as useful as its publication: the 2017-18 round was completed and is still, statistically "
          "speaking, missing.")))

SC.append(dict(
  kind="theory", id="s3", title="HCES and PLFS — the two surveys that changed recently", mins=8,
  objective="State what each survey measures, the figures it produced, and exactly what the 2025 redesign changed.",
  blocks=[
   dict(t="def", h="HCES — what it measures",
     body="Monthly per capita consumption expenditure, MPCE, item by item, separately for rural and urban areas and by "
          "expenditure class. Two consecutive rounds were run after the long gap: 2022-23 and 2023-24. The 2023-24 round "
          "put average MPCE at about ₹4,122 rural and ₹6,996 urban, or ₹4,247 and ₹7,078 once the imputed value of free "
          "benefits is added."),
   dict(t="formula", h="The two HCES numbers that get asked",
     body="Food share of consumption in 2023-24: about 47% rural and about 40% urban — and it rose in both, reversing a "
          "long decline. Rural MPCE as a percentage of urban: 69.7% in 2023-24, against 83.9% in 2011-12. Read that "
          "second figure carefully: the ratio falling means the gap, measured this way, is not what it was, and the "
          "official reading is that rural consumption has been growing faster than urban."),
   dict(t="def", h="PLFS — what it measures",
     body="Labour Force Participation Rate, Worker Population Ratio and Unemployment Rate, under two reference periods. "
          "Usual Status (principal plus subsidiary) classifies a person by activity over the preceding 365 days; Current "
          "Weekly Status classifies by the preceding 7 days. PLFS was launched in 2017 and replaced the quinquennial "
          "Employment and Unemployment Survey, which had produced an estimate only every five years."),
   dict(t="step", h="What PLFS looked like before 2025",
     body="Quarterly estimates for urban areas only, on Current Weekly Status. Annual estimates for rural and urban, on "
          "both Usual Status and CWS, for a July-to-June year. About 12,800 first stage units a year, 8 households each, "
          "roughly 1,02,400 households."),
   dict(t="formula", h="What the January 2025 redesign changed",
     body="Four things. First, monthly all-India estimates of LFPR, WPR and UR on CWS for rural and urban, which did not "
          "exist before; the first monthly bulletin was for April 2025. Second, quarterly estimates extended from urban "
          "only to rural, urban and combined, including major states. Third, the annual year moved from July-June to the "
          "calendar year, from 2025. Fourth, the sample: 22,692 first stage units a year and 12 households each, about "
          "2,72,304 households — roughly 2.65 times the old size."),
   dict(t="def", h="And the design behind it",
     body="A multistage stratified design in which the basic stratum is now the district for most areas rather than the "
          "NSS region, with rural areas further stratified by distance from the district headquarters or from a city of "
          "over five lakh, and urban areas by million-plus cities. Each selected household is visited four times in "
          "consecutive months — one first visit and three revisits — which is the rotational panel that makes monthly "
          "estimates possible."),
   dict(t="trap", h="The comparability warning",
     body="MoSPI's own note says estimates from January 2025 onwards should not be compared casually with those "
          "published up to December 2024. A question that asks you to read a trend across that boundary is testing "
          "whether you know the break is there.")]))

SC.append(dict(
  kind="recall", id="s4", title="Pause and recall", mins=3,
  objective="Retrieve the survey facts before the three indices are added, so the two halves stay separate.",
  intro="Answer aloud, then look. Everything here was in the last two scenes.",
  items=[
   dict(q="Which survey supplies the weights for the consumer price index, and which round did it for the 2024 base?",
     a="The Household Consumption Expenditure Survey — the 2023-24 round."),
   dict(q="What did PLFS replace, and in what year was PLFS launched?",
     a="The quinquennial Employment and Unemployment Survey; PLFS was launched in 2017."),
   dict(q="Give the two PLFS reference periods and their windows.",
     a="Usual Status (principal plus subsidiary), 365 days; Current Weekly Status, 7 days."),
   dict(q="Which two surveys cover the registered and the unregistered non-agricultural sectors?",
     a="ASI covers registered factories; ASUSE covers unincorporated enterprises."),
   dict(q="Why does the consumption series skip from 2011-12 to 2022-23?",
     a="The 2017-18 round's results were withheld in November 2019 on grounds of data quality."),
   dict(q="Who runs the National Family Health Survey, and through which nodal agency?",
     a="The Ministry of Health and Family Welfare, through the International Institute for Population Sciences, Mumbai.")]))

SC.append(dict(
  kind="completion", id="s5", title="Your turn — fill in the survey and index facts", mins=6,
  objective="Produce the base years and the survey sources without prompting.",
  problem="Fill in each blank with the figure or name the lesson has given.",
  steps=[
   dict(say="The consumer price index was rebased, from one base year to another.",
     blank=dict(prompt="From which base to which base?", answer="2012=100 to 2024=100",
       accept=["2012 to 2024", "from 2012=100 to 2024=100", "2012=100 -> 2024=100", "base 2012 to base 2024"],
       hint="The new base is a calendar year in which base prices were collected."),
     why="Every other fact about the new series hangs on knowing which two bases are involved."),
   dict(say="The item basket and weights of that new series came from a survey.",
     blank=dict(prompt="Which survey, which round?", answer="HCES 2023-24",
       accept=["Household Consumption Expenditure Survey 2023-24", "HCES, 2023-24",
               "Household Consumption Expenditure Survey, 2023-24 round", "HCES 2023 24"],
       hint="The consumption survey, in its second post-gap round."),
     why="This is the link between the two halves of the topic, and the most asked single fact in it."),
   dict(say="The index of industrial production was also rebased.",
     blank=dict(prompt="To which base year?", answer="2022-23=100",
       accept=["2022-23", "2022-23 = 100", "base 2022-23", "2022 23"],
       hint="A financial year, not a calendar year — and the same one the wholesale index moved to."),
     why="The CPI base is a calendar year and the IIP base a financial year; the pairing is examinable."),
   dict(say="The WPI and PPI are now published in parallel.",
     blank=dict(prompt="Which office publishes both series?", answer="Office of the Economic Adviser, DPIIT",
       accept=["OEA, DPIIT", "Office of the Economic Adviser", "Office of Economic Adviser, DPIIT"],
       hint="The same office that publishes the revised WPI also introduced Output PPI."),
     why="PPI is used for selected GDP deflation purposes, but that does not mean WPI publication has ended."),
   dict(say="PLFS now publishes an estimate at a frequency it did not before 2025.",
     blank=dict(prompt="Which frequency, on which reference period?", answer="monthly, on Current Weekly Status",
       accept=["monthly, CWS", "monthly on CWS", "monthly - current weekly status",
               "monthly estimates using current weekly status"],
       hint="The seven-day reference period, not the 365-day one."),
     why="Monthly on CWS is the headline change of 2025 and the one most likely to appear as a single-mark question.")],
  after="Two base years, one survey, one replacement index and one new frequency. Those five facts carry most of the "
        "marks this topic offers."))

SC.append(dict(
  kind="theory", id="s6", title="The three indices, and where they now stand", mins=9,
  objective="State each index's base year, weights, producer and current status, and keep the three apart.",
  blocks=[
   dict(t="def", h="CPI — Consumer Price Index, base 2024=100",
     body="Produced by the NSO, MoSPI. The first release on the new base was on 12 February 2026, replacing base "
          "2012=100. The basket and weights come from HCES 2023-24; base-period prices were collected through calendar "
          "2024. Rural, urban and combined indices are published, the combined being a weighted average of the other "
          "two. It is a modified Laspeyres index: elementary indices use the Jevons formula, higher-level indices a "
          "Young or modified Laspeyres formula."),
   dict(t="formula", h="What changed in the CPI basket",
     body="Classification moved to COICOP 2018 — twelve divisions in place of six groups, resolving to 43 groups, 92 "
          "classes, 162 subclasses and 358 items, up from 299. Goods rose from 259 to 308 and services from 40 to 50. "
          "Food and beverages carry 40.10% in the group table against 45.86% before, and housing 11.88% against 10.07%. "
          "Rural house rent entered the index for the first time. Prices are collected from 1,465 rural markets and 1,395 urban "
          "markets across 434 towns, collected electronically on handheld devices, with e-commerce prices used in twelve "
          "large towns and administrative data for rail fares, postal charges and fuel."),
   dict(t="def", h="WPI and the emerging PPI framework",
     body="The wholesale price index measures prices of goods only — no services — at the wholesale or first point of "
          "bulk sale, and is produced by the Office of the Economic Adviser in the Department for Promotion of Industry "
          "and Internal Trade, not by MoSPI. Its base was revised from 2011-12 to 2022-23 and the basket expanded from "
          "697 to 957 items. Launched alongside it, on 15 June 2026, was the Output Producer Price Index, with a trial "
          "Input PPI for manufacturing and a quarterly Services PPI covering seven sectors. WPI continues to be published alongside Output PPI, trial Input PPI and phased Services PPIs."),
   dict(t="def", h="IIP — Index of Industrial Production, base 2022-23=100",
     body="Produced by the NSO. The base-year report came on 25 May 2026 and the first release on the new base on 1 June "
          "2026, replacing base 2011-12. The basket holds 1,042 products mapped to 463 item groups, against 839 and 407 "
          "before, and the classification used is NIC 2025."),
   dict(t="formula", h="IIP weights, both ways of cutting them",
     body="By sector: manufacturing 76.062, mining and quarrying 11.053, electricity and gas supply 10.865, and — new to "
          "the index — water supply, sewerage and waste management 2.020. Gas supply is inside the electricity sector "
          "with a weight of 0.694, not a sector of its own. By use: primary goods 31.136, intermediate goods 22.416, "
          "consumer non-durables 16.147, consumer durables 11.311, infrastructure and construction goods 10.908, capital "
          "goods 8.082. The movement worth remembering is intermediate goods up from 17.221 and mining down from 14.372."),
   dict(t="step", h="Who produces what",
     body="MoSPI through the NSO: CPI, IIP, the national accounts, and the NSS surveys. DPIIT through the Office of the "
          "Economic Adviser: WPI and now the PPI. Ministry of Health and Family Welfare through IIPS: NFHS. RBI uses "
          "CPI-Combined as the target for monetary policy, but does not produce it."),
   dict(t="trap", h="Three indices, three different revisions",
     body="CPI moved to a calendar base year, 2024. IIP and WPI both moved to a financial year, 2022-23. WPI and PPI are "
          "published concurrently; distinguish publication from the use of a price index as a GDP deflator. Mixing these three up is the single most productive confusion the "
          "examiner has available in this topic.")],
  flow=dict(caption="Who produces which index, on which base, from which source",
    nodes=[
      dict(id="m", r=0, c=0, w=2, label="MoSPI · NSO", kind="start"),
      dict(id="d", r=0, c=2, w=2, label="DPIIT · Office of the Economic Adviser", kind="start"),
      dict(id="c", r=1, c=0, label="CPI, base 2024", kind="step"),
      dict(id="i", r=1, c=1, label="IIP, base 2022-23", kind="step"),
      dict(id="w", r=1, c=2, label="WPI, base 2022-23", kind="step"),
      dict(id="p", r=1, c=3, label="Output PPI, 2026", kind="step"),
      dict(id="h", r=2, c=0, label="weights from HCES 2023-24", kind="note"),
      dict(id="a", r=2, c=1, label="weights from ASI · NIC 2025", kind="note"),
      dict(id="x", r=2, c=2, w=2, label="WPI and PPI published concurrently", kind="end")],
    edges=[dict({"from":"m","to":"c"}), dict({"from":"m","to":"i"}), dict({"from":"d","to":"w"}),
           dict({"from":"d","to":"p"}), dict({"from":"c","to":"h"}), dict({"from":"i","to":"a"}),
           dict({"from":"w","to":"x"}), dict({"from":"p","to":"x"})]),
  scenario=dict(
    teaser="Rural rent had never been in the Indian consumer price index. In 2026 it was, and the housing weight moved.",
    title="How a survey becomes a basket",
    body=P(
      "Follow one item through the machinery. Under the old CPI, base 2012=100, the housing index covered urban house "
      "rent only. Rural housing was outside the index altogether, on the reasoning that most rural households own their "
      "dwellings and pay no rent, so there was nothing to price.",
      "The 2023-24 consumption survey measured what rural households actually spend on housing — rent where it is paid, "
      "and the maintenance, repair, water supply and related services that every household pays whether it owns or "
      "rents. That spending turned out to be large enough to belong in the index.",
      "So the new series, base 2024=100, does three things at once with housing. It includes rural house rent for the "
      "first time. It redefines the housing index as a weighted average of actual rent, maintenance and repair, and "
      "water supply and miscellaneous services. And the housing weight rises from 10.07% to 11.88%, which is not a "
      "judgement by the statistical office but an arithmetic consequence of what the survey found.",
      "The same survey did the same work for every other item. Streaming services came in, having not existed in a "
      "meaningful way in 2012. Out went VCR and DVD players, radios, tape recorders, second-hand clothing, CDs and "
      "DVDs, and coir rope. Food and beverages fell from 45.86% to 40.10% in the group table — not because food got "
      "cheaper, but because households now spend a smaller share of a larger budget on it.",
      "That last sentence is the one examiners like. A falling weight is a statement about budget shares, not about "
      "prices or about hardship, and reading it as the latter is a standard error."),
    close="A weight is a measured consumption share, not a policy choice: the survey decides it, and the index inherits "
          "it.")))

SC.append(dict(
  kind="theory", id="s7", title="Linking two series — the arithmetic", mins=6,
  objective="Convert a figure from an old base to a new one, and know why the direction cannot be memorised.",
  blocks=[
   dict(t="def", h="What a linking factor is for",
     body="When an index is rebased, the old and the new series run together for a while. The ratio of their averages "
          "over that overlap is the linking factor, and it is what lets an old figure be quoted on the new base. It is "
          "published at the general-index level only; below that the two baskets are classified differently and the "
          "linking is not reliable."),
   dict(t="formula", h="The CPI case, which is the one to carry",
     body="MoSPI defines the CPI linking factor as the annual geometric mean of the new series in 2025 divided by that "
          "of the old series in 2025 — the overlap year in which both were published. The factors are 0.5222 rural, "
          "0.5320 urban and 0.5267 combined. Because the factor is new over old, you MULTIPLY an old-base figure by it: "
          "an old combined index of 200 becomes 200 × 0.5267 = 105.34 on base 2024=100."),
   dict(t="trap", h="And why the IIP case runs the other way",
     body="The IIP linking factor is defined as the geometric mean of the OLD series during the new base year divided by "
          "that of the new series in the same year — the reciprocal arrangement. Its general value is 1.3834, which says "
          "the old series averaged about 138.34 during 2022-23. With that definition, an old-base figure is DIVIDED by "
          "the factor to reach the new base. The lesson here is not a direction to memorise but a habit: read the "
          "definition of the factor before you use it, because the two offices define it in opposite ways."),
   dict(t="step", h="What this means for growth rates",
     body="A linked series is a convenience, not a continuation. MoSPI says explicitly that growth rates across the two "
          "IIP series are not strictly comparable, because coverage, basket, sectoral composition and weights all "
          "changed. The same caution applies to CPI sub-indices, which cannot be linked at all. An exam statement "
          "claiming the linked series is fully comparable is false."),
   dict(t="note", h="One number worth a sanity check",
     body="The January 2026 CPI combined provisional index on base 2024=100 was 104.46, with year-on-year inflation of "
          "2.75%. Divide 104.46 by 0.5267 and you get about 198.3, which is where the old series stood. If a question "
          "gives you one of these and asks for the other, that is the whole calculation.")]))

SC.append(dict(
  kind="guided", id="s8", title="Work through a linking and a weight calculation", mins=7,
  objective="Do the two pieces of arithmetic this topic actually asks for.",
  problem="(a) The CPI combined index on base 2012=100 stood at 189.4 in a given month. What is the equivalent figure on "
          "base 2024=100? (b) In the new IIP series, manufacturing carries 76.062 and electricity and gas supply 10.865, "
          "of which gas supply is 0.694. What weight does electricity alone carry, and by how many points did the "
          "combined electricity-and-gas weight rise over the 2011-12 series, where electricity alone carried 7.995?",
  hints=["For (a), decide first whether the CPI factor is new-over-old or old-over-new, then multiply or divide "
         "accordingly.",
         "For (b), the sector weight is the sum of its parts; subtract to isolate electricity.",
         "For the rise in (b), compare like with like: the old series had no gas inside the sector, so compare the old "
         "electricity-only weight with the new sector total, and say so."],
  solution=[
   dict(say="(a) The CPI linking factor is defined as the new series mean over the old series mean in the overlap year "
            "2025, so it converts old to new by multiplication. The combined factor is 0.5267.",
     math="LF(combined) = GM(new, 2025) / GM(old, 2025) = 0.5267"),
   dict(say="Multiply the old-base figure by it.",
     math="189.4 × 0.5267 = 99.76 on base 2024 = 100"),
   dict(say="A sanity check: the answer is just under 100, and 100 is the 2024 average. An old-base figure of 189.4 "
            "therefore sits a shade below the new base period, which is consistent.",
     math="99.76 < 100 → the month is a little below the 2024 average"),
   dict(say="(b) The sector total is electricity plus gas, so electricity alone is the remainder.",
     math="10.865 − 0.694 = 10.171 for electricity alone"),
   dict(say="For the rise, the honest comparison states what moved. Electricity alone went from 7.995 to 10.171, a rise "
            "of 2.176 points; the sector as now defined carries 10.865, which is 2.870 points above the old "
            "electricity-only weight.",
     math="10.171 − 7.995 = 2.176 (like for like);  10.865 − 7.995 = 2.870 (sector as redefined)")],
  answer="(a) 99.76 on base 2024=100. (b) Electricity alone 10.171; a like-for-like rise of 2.176 points, or 2.870 "
         "points if the redefined sector total is compared with the old electricity-only weight.",
  check="If (a) came out near 360, you divided instead of multiplying. Check the direction against the base period: a "
        "figure on base 2024=100 for a month near 2024 has to be near 100, and 360 is not."))

SC.append(dict(
  kind="trapcheck", id="s9", title="Six statements — verdict on each before you look", mins=6,
  objective="Meet the exact confusions the paper builds between the three indices and the surveys.",
  intro="Each is either the standard fact or one detail moved from a neighbouring index.",
  items=[
   dict(claim="The consumer price index on base 2024=100 takes its weights from the Household Consumption Expenditure "
              "Survey of 2023-24.", tf=True,
     why="And base-period prices were collected through calendar 2024. The first release on the new base was in "
         "February 2026."),
   dict(claim="The wholesale price index covers both goods and services.", tf=False,
     why="WPI is a goods-only index. Services are covered by the new quarterly Services PPI, across seven sectors, "
         "which is one of the reasons for moving to a producer price framework at all."),
   dict(claim="The index of industrial production and the wholesale price index were both rebased to 2022-23.", tf=True,
     why="Both moved to the financial year 2022-23. Only CPI moved to a calendar base year, 2024. This is the pairing "
         "to hold: two financial years and one calendar year."),
   dict(claim="PLFS was launched in 2017 and replaced the quinquennial Employment and Unemployment Survey.", tf=True,
     why="Its original design gave quarterly urban estimates on Current Weekly Status and annual rural-and-urban "
         "estimates on both reference periods. The 2025 redesign added monthly all-India estimates."),
   dict(claim="Gas supply is a separate sector in the new IIP series, alongside mining, manufacturing and electricity.",
     tf=False,
     why="Gas supply sits inside Electricity and Gas Supply, with a weight of 0.694 within the sector's 10.865. What is "
         "genuinely new as a sector is water supply, sewerage and waste management, at 2.020."),
   dict(claim="The consumption survey immediately preceding the 2022-23 round was the round of 2017-18.", tf=False,
     why="A round was fielded in 2017-18 but its results were withheld in November 2019, so the last published round "
         "before 2022-23 is 2011-12. The series has a gap, not a continuous sequence.")]))

SC.append(dict(
  kind="guided", id="s10", title="Transfer — a case the lesson has not shown you", mins=6,
  objective="Reason from the architecture when the question asks about something you were never given directly.",
  problem="A question asks: 'The Reserve Bank's inflation target is specified in terms of which index, and why is that "
          "index rather than the wholesale index used for the purpose?' Neither the target nor the reason appears in "
          "your notes as a fact to memorise. How do you answer, and how confident should you be?",
  hints=["Ask which index measures what households actually pay, and which measures what wholesalers charge.",
         "Ask which of the two covers services, and whether a target that ignores services could work.",
         "Consider which index is published rural, urban and combined, and what a national target needs."],
  solution=[
   dict(say="The target has to be about the cost of living, because that is what monetary policy is accountable for. "
            "Between the two, CPI measures retail prices paid by households; WPI measures bulk prices charged earlier "
            "in the chain.",
     math="Target = household cost of living → CPI, not WPI"),
   dict(say="Second, WPI excludes services entirely, and services are a large and growing share of household spending — "
            "50 of the 358 items in the new CPI basket are services. A goods-only index cannot stand in for the cost of "
            "living.",
     math="WPI = goods only; CPI services = 50 items"),
   dict(say="Third, CPI is published rural, urban and combined, and the combined index is the one a national target "
            "needs. So the answer is CPI-Combined, and the confidence is high, because three independent features of "
            "the two indices all point the same way.",
     math="Answer: CPI (Combined)")],
  answer="CPI-Combined, because the target concerns retail prices faced by households, because WPI covers no services, "
         "and because CPI alone is published as a rural-urban combined national index.",
  check="The method generalises: when a question asks which index is used for a purpose, ask what the purpose measures, "
        "then which index's coverage and publication level match it. You rarely need to have memorised the answer."))

SC.append(dict(
  kind="summary", id="s11", title="What you should now be able to do unaided", mins=3,
  objective="Compress the topic to the facts and the one habit the exam rewards.",
  body=P(
   "Surveys. NSS from 1950, rounds large and thin, NSSO merged into the NSO in 2019. HCES measures MPCE and sets the CPI "
   "weights; rounds 2022-23 and 2023-24, with 2023-24 giving about ₹4,122 rural and ₹6,996 urban, food shares of about "
   "47% and 40%, and rural MPCE at 69.7% of urban against 83.9% in 2011-12. The 2017-18 round was withheld in November "
   "2019, which is why the series jumps from 2011-12.",
   "PLFS, launched 2017, replaced the quinquennial Employment and Unemployment Survey; Usual Status is 365 days and "
   "Current Weekly Status 7 days. From January 2025: monthly all-India CWS estimates, quarterly extended to rural and "
   "combined, a calendar annual year, and 22,692 first stage units with 12 households each — about 2.72 lakh households "
   "against about 1.02 lakh.",
   "ASI covers registered factories under the Factories Act, 1948, collected under the Collection of Statistics Act, "
   "2008; its 2023-24 results covered 2,60,061 factories. ASUSE covers unincorporated enterprises. NFHS belongs to the "
   "Ministry of Health and Family Welfare through IIPS Mumbai; six rounds, NFHS institutional role; do not quote unverified NFHS-6 result statistics.",
   "Indices. CPI base 2024=100, first release February 2026, weights from HCES 2023-24, COICOP 2018, 358 items, food and "
   "beverages 40.10%, housing 11.88%, produced by the NSO, used for the inflation target. WPI base revised to 2022-23, "
   "957 items, goods only, produced by the Office of the Economic Adviser in DPIIT, with Output PPI, trial Input PPI and phased Services PPIs published alongside it from June 2026. IIP base 2022-23=100, first release June 2026, 1,042 "
   "products in 463 item groups on NIC 2025, manufacturing 76.062, mining 11.053, electricity and gas 10.865, water "
   "supply and sewerage 2.020 as a new sector.",
   "Linking. The CPI factor is new-over-old, so multiply: 0.5267 combined. The IIP factor is old-over-new, so divide: "
   "1.3834 general. Factors are published at the general level only, and linked growth rates are not strictly "
   "comparable.",
   "The habit. Every fact in this topic belongs to a chain — survey sets weights, index runs on them, accounts use the "
   "index as a deflator. When a question gives you something you have not memorised, locate it on that chain and the "
   "answer usually follows.")))

SC.append(dict(kind="quiz", id="s12", title="Mastery test", mins=12,
  objective="Ten unseen questions, drawn 3 easy / 5 moderate / 2 hard.", setId="official_t4_mastery"))

LES = dict(
  id="officialt4", moduleId="official", topicId="official-t4",
  title="Major Surveys and Indices",
  breadcrumb="Official Statistics → Indian Statistical System → Major surveys and indices",
  engine="A", engineName="Institutions and official statistics — what India measures, how often, and on what base",
  estMin=sum(s["mins"] for s in SC), version="1.1", status="approved",
  provenance="Authored for this platform in October 2026. Every institutional figure was checked against a primary "
             "source rather than recalled, because this topic moved substantially in 2025 and 2026: the CPI series on "
             "base 2024=100 (MoSPI first release 12 February 2026, and the CPI 2024 FAQ for the linking factors and "
             "the worked linking example); the IIP series on base 2022-23 (base report 25 May 2026, first release "
             "1 June 2026); the WPI base revision to 2022-23 and the Output PPI launched 15 June 2026; the PLFS "
             "redesign of January 2025 (MoSPI press note on changes in sample design); HCES 2023-24; NFHS-6 (released "
             "29 May 2026); and ASI 2023-24 (released 27 August 2025). Where a source did not state something "
             "explicitly — the direction in which the IIP linking factor is applied — the lesson derives it from the "
             "published definition and says so, and no question tests it.",
  objectives=[
    "Place the National Sample Survey and name the four surveys that now descend from it, with what each measures.",
    "State what HCES measures, its two recent rounds, and the headline MPCE and food-share figures from 2023-24.",
    "Give the PLFS reference periods and the four changes the January 2025 redesign made.",
    "Give the base year, weights, producer and current status of the CPI, the WPI and the IIP.",
    "Apply a linking factor in the right direction and say why a linked series is not fully comparable.",
    "Locate an unfamiliar survey or index on the chain from survey to index to national accounts."],
  prereq=[
    dict(id="p1", name="Laspeyres, Paasche and Fisher index numbers",
         why="India's CPI is a modified Laspeyres index, and the formula explains why a base year has to be revised."),
    dict(id="p2", name="Base years, rebasing and linking",
         why="Three indices were rebased within eighteen months; the arithmetic of linking is examinable."),
    dict(id="p3", name="Multistage stratified sampling and first stage units",
         why="Survey sample sizes are quoted as first stage units times households, and the 2025 PLFS redesign changed "
             "both numbers."),
    dict(id="p4", name="Nominal versus real series, and deflators",
         why="It is what connects the price indices to the production index and the national accounts.")],
  mastery={"minQ":10, "pass":80, "draw":10, "fmtMin":{"numeric":70,"multi":70},
    "diffMix":{"easy":3,"moderate":5,"hard":2}, "noHints":True, "retestDays":7,
    "note":"Platform settings, not an NTA rule. Ten drawn from a pool of twenty at 3 easy / 5 moderate / 2 hard; a "
           "retake draws again, holding the mix and pulling back items previously got wrong."},
  refs=[
    dict(title="First press release of the Consumer Price Index on base 2024=100",
         where="Weights, item counts, COICOP 2018, market coverage and the linking factors",
         site="Press Information Bureau", url="https://www.pib.gov.in/PressReleasePage.aspx?PRID=2227012&reg=3&lang=1",
         type="Government press release", free=True, checked="2026-10-13",
         why="The authority for every CPI figure in scenes 7 and 8. Note that the food weight differs between the "
             "six-group table and the COICOP division table; the lesson quotes the group table and says so."),
    dict(title="Press note on Periodic Labour Force Survey changes in 2025",
         where="Sample design, first stage units, rotational panel and reporting frequencies",
         site="MoSPI", url="https://www.mospi.gov.in/sites/default/files/press_release/Press_note_changes_sample_design_Final.pdf",
         type="Government press note", free=True, checked="2026-10-13",
         why="For the four changes in scene 4, including the comparability warning across January 2025."),
    dict(title="First press release of the Index of Industrial Production, new series base 2022-23",
         where="Sectoral and use-based weights, item counts and linking factors",
         site="Press Information Bureau", url="https://www.pib.gov.in/PressReleasePage.aspx?PRID=2267531&reg=3&lang=1",
         type="Government press release", free=True, checked="2026-10-13",
         why="For the IIP weights in scene 7 and the arithmetic in scene 9.")],
  revision=dict(
    sheet=[
      "NSS from 1950, Mahalanobis's design; large (quinquennial) and thin rounds; NSSO merged into the NSO, 2019.",
      "HCES sets CPI weights and poverty estimates; rounds 2022-23 and 2023-24; 2017-18 round withheld Nov 2019.",
      "HCES 2023-24: MPCE about ₹4,122 rural and ₹6,996 urban; food share about 47% rural, 40% urban.",
      "Rural MPCE as a share of urban: 69.7% in 2023-24 against 83.9% in 2011-12.",
      "PLFS launched 2017, replacing the quinquennial Employment and Unemployment Survey.",
      "PLFS reference periods: Usual Status (ps+ss) 365 days; Current Weekly Status 7 days.",
      "PLFS from Jan 2025: monthly all-India CWS; quarterly rural + urban + combined; calendar annual year.",
      "PLFS sample: 22,692 FSUs × 12 households ≈ 2.72 lakh, from 12,800 × 8 ≈ 1.02 lakh; four visits per household.",
      "ASI = registered factories (Factories Act 1948); ASUSE = unincorporated enterprises. ASI 2023-24: 2,60,061 factories.",
      "NFHS: MoHFW with IIPS Mumbai. Published rounds listed here through NFHS-5 (2019-21); do not quote NFHS-6 indicators without its official report.",
      "CPI base 2024=100 from 12 Feb 2026; weights from HCES 2023-24; COICOP 2018; 358 items; food 40.10%, housing 11.88%.",
      "CPI is a modified Laspeyres index: Jevons at the elementary level, Young/modified Laspeyres above it.",
      "WPI base revised 2011-12 → 2022-23; 957 items; goods only; Office of the Economic Adviser, DPIIT.",
      "Output PPI launched 15 June 2026; WPI base 2022-23 remains published alongside OPPI, trial IPPI and Services PPI.",
      "IIP base 2022-23=100 from 1 June 2026; 1,042 products in 463 item groups; NIC 2025.",
      "IIP sector weights: manufacturing 76.062, mining 11.053, electricity and gas 10.865, water and sewerage 2.020.",
      "IIP use-based: primary 31.136, intermediate 22.416, consumer non-durables 16.147, durables 11.311, infra 10.908, capital 8.082.",
      "CPI linking factors 0.5222 / 0.5320 / 0.5267 — new over old, so MULTIPLY the old index.",
      "IIP general linking factor 1.3834 — old over new, so DIVIDE the old index. Read each definition before using it."],
    cards=[
      ["Survey that sets the CPI weights", "HCES — the 2023-24 round for base 2024=100"],
      ["CPI base year and first release", "2024=100, first released 12 February 2026"],
      ["IIP and WPI base year", "Both 2022-23 — a financial year, unlike CPI's calendar 2024"],
      ["WPI and PPI: current publication status", "WPI base 2022-23 remains published alongside Output PPI and other PPI series"],
      ["WPI's producer", "Office of the Economic Adviser, DPIIT — not MoSPI"],
      ["PLFS reference periods", "Usual Status 365 days; Current Weekly Status 7 days"],
      ["The headline PLFS change of 2025", "Monthly all-India LFPR, WPR and UR on CWS"],
      ["Registered versus unincorporated enterprises", "ASI versus ASUSE"],
      ["Why the consumption series jumps from 2011-12", "The 2017-18 round was withheld in November 2019"],
      ["CPI combined linking factor and its use", "0.5267 — multiply the old-base index by it"]],
    tricks=[
      dict(hook="Calendar for consumers, financial for the rest",
           why="CPI moved to calendar 2024; IIP and WPI both moved to financial 2022-23. One word separates the three."),
      dict(hook="Only one index is being killed",
           why="CPI and IIP were rebased. WPI and PPI series are published concurrently; distinguish publication from GDP deflator use."),
      dict(hook="MoSPI does CPI and IIP; DPIIT does WPI and PPI",
           why="The producer is asked as often as the base year, and the two price indices sit in different ministries."),
      dict(hook="Surveys measure quantities, indices reprice them",
           why="It is the whole architecture in six words, and it tells you which body produces which number."),
      dict(hook="New over old, multiply; old over new, divide",
           why="CPI's factor is defined one way and IIP's the other. The rule is to read the definition, not to "
               "memorise a direction.")],
    shortcuts=[
      "Any option giving the CPI a financial-year base is wrong; any option giving IIP or WPI a calendar base is wrong.",
      "Any option that has WPI covering services is wrong — that is the Services PPI.",
      "Any option naming MoSPI as the producer of WPI is wrong, and vice versa for CPI.",
      "If a question names the previous consumption round before 2022-23, the answer is 2011-12, never 2017-18.",
      "Gas supply is inside the electricity sector of the IIP; the genuinely new sector is water and sewerage."],
    remember=[
      "Locate any unfamiliar fact on the chain: survey → weights → index → deflator → national accounts.",
      "Before applying a linking factor, read whether it is defined as new over old or old over new."],
    traps=[
      "Assuming WPI publication ended when PPI was introduced; OEA currently publishes both.",
      "Giving the CPI a 2022-23 base because the other two indices have it.",
      "Naming 2017-18 as the consumption round preceding 2022-23.",
      "Calling gas supply a new IIP sector; it is inside electricity, and water supply is the new sector.",
      "Comparing PLFS estimates across January 2025 without noting the design break.",
      "Quoting the COICOP division food weight (36.75%) as the group-table weight (40.10%), or the reverse.",
      "Multiplying by the IIP linking factor and dividing by the CPI one, which is the wrong way round for both."]),
  traps=[
    "CPI's base is calendar 2024; IIP's and WPI's is financial 2022-23.",
    "WPI covers goods only and is produced by DPIIT, not MoSPI.",
    "WPI and PPI series are published concurrently; do not infer WPI discontinuation from PPI availability.",
    "The consumption round before 2022-23 is 2011-12; the 2017-18 round was withheld.",
    "Water supply and sewerage is the new IIP sector; gas supply sits inside electricity.",
    "The CPI linking factor is new over old, so it multiplies; the IIP factor is defined the other way round.",
    "PLFS estimates from January 2025 are not casually comparable with earlier ones.",
    "CPI weights come from HCES 2023-24, not from the 2022-23 round."],
  scenes=SC)

json.dump(LES, io.open("seed/lesson_10a4.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
k = {}
for s in SC: k[s["kind"]] = k.get(s["kind"], 0) + 1
print("lesson 10A.4 written: %d scenes %s" % (len(SC), k))
print("  flow %d · scenarios %d · est %d min" %
      (len([s for s in SC if s.get("flow")]), len([s for s in SC if s.get("scenario")]), LES["estMin"]))
