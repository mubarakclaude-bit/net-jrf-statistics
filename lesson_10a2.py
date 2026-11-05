#!/usr/bin/env python3
# Lesson 10A.2 — Commissions and committees (Unit X, Indian Statistical System).
#
# Checked October 2026 against: the Carnegie history of India's statistical system
# (Bowley-Robertson, the National Income Committee, the Rangarajan Commission's
# recommendations and which were implemented, the first NSC under Tendulkar), the
# text of the Collection of Statistics (Amendment) Act 2017, and the 2023-24 record
# of the SCES/SCoS and its dissolution. Where sources disagree on a year, the lesson
# says so rather than picking one.
import json, io

def P(*x): return list(x)

SC = []

SC.append(dict(
  kind="foundation", id="s0", title="Before the lesson — four things it will assume", mins=5,
  objective="Separate the kinds of body that recur here, and know what a report can and cannot do.",
  body=P(
   "This topic is a list of names, years and chairpersons, and the only way it goes wrong is if the categories blur. A "
   "committee is not a commission, a recommendation is not a law, and a body that was renamed is not a body that was "
   "replaced.",
   "Four checks. Each one is a distinction that a question will be built on, and each takes a minute."),
  items=[
   dict(ask="What is the difference between a committee, a commission and a working group?",
     recall="In Indian official practice these are degrees of standing rather than sharply defined legal forms. A working "
            "group is usually small, internal and tasked with one question; a committee is appointed for a defined subject "
            "and reports; a commission is the weightiest, usually chaired by an eminent outsider and reviewing a whole "
            "system. None of the three is automatically statutory.",
     refresh=P(
      "The labels matter for the exam because questions quote them exactly. The Rangarajan body that reviewed the "
      "statistical system in 2000-01 is called a Commission; the bodies that have fixed poverty lines are called "
      "Committees or Expert Groups; the bodies inside the Planning Commission that did preparatory work were Task Forces "
      "and Working Groups.",
      "What they share is that they advise. Whether their advice becomes binding depends entirely on whether the "
      "government acts on it, which is the theme of this whole topic.",
      "One practical rule: if a body has a chairperson who is a serving official and a one-line remit, it is a working "
      "group; if it is chaired by a former governor or a professor and reviews a system, it is a commission.")),
   dict(ask="What does it mean that a committee 'recommended' something?",
     recall="That it put the proposal in its report. Nothing follows automatically. A recommendation becomes real only "
            "when the government accepts it and issues a resolution, a rule or an Act — and governments accept some "
            "recommendations and quietly drop others.",
     refresh=P(
      "The clearest example in this topic is the Rangarajan Commission of 2001. It recommended a statutory apex body "
      "accountable to Parliament, a professional statistician as the ministry's Secretary, regular statistical audits, "
      "and a reformed Collection of Statistics Act.",
      "What actually happened: the professional statistician post was created, the Act was reformed in 2008, and the "
      "statutory body never arrived — the National Statistical Commission exists, but by resolution and without statutory "
      "backing. Regular audits were not instituted.",
      "So a question asking 'which of the following did the Rangarajan Commission recommend' and one asking 'which was "
      "implemented' have different answers, and the paper knows it.")),
   dict(ask="What is a poverty line, and why does fixing one need a committee?",
     recall="A poverty line is a level of consumption expenditure below which a household is counted as poor. It needs a "
            "committee because every element of it is a judgement: which basket of goods, which calorie norm if any, "
            "which price index to update it with, and whether rural and urban lines should be derived separately.",
     refresh=P(
      "The oldest Indian approach anchored the line to a calorie requirement — famously 2,250 calories a day in the "
      "Dandekar–Rath work — and then asked what expenditure buys that in practice.",
      "Later committees moved away from calories towards a broader basket including health and education, and changed "
      "the price indices used to update the line over time. Each change moves the headcount, sometimes by tens of "
      "millions of people, without anybody's actual consumption changing.",
      "That is why the chairs of these committees are household names in Indian economics and why the sequence of them is "
      "examinable: the poverty number is a methodological artefact as much as a measurement.")),
   dict(ask="What is the National Sample Survey, and why do committees keep being appointed over it?",
     recall="The NSS is the large household and enterprise survey system run by the NSS wing of the NSO, in numbered "
            "rounds since 1950. Committees are appointed over it because its design decisions — sampling, questionnaire, "
            "reference period, tabulation — determine the official figures for consumption, employment and poverty.",
     refresh=P(
      "If you change the recall period over which a household is asked to report its spending, you change measured "
      "consumption and therefore measured poverty. If you change the sampling frame you change who is represented.",
      "So the technical committees that advise on survey design are not administrative detail: they are where the "
      "numbers are really made, which is why their composition, and who chairs them, becomes a public question.",
      "This is the thread that runs from the National Income Committee of 1949 to the committees of the 2020s."))]))

SC.append(dict(
  kind="intuition", id="s1", title="Why a statistical system keeps appointing committees", mins=4,
  objective="See the committees as a single argument conducted over seventy years, not a list to memorise.",
  body=P(
   "A statistical office faces a problem no other arm of government has. It must produce numbers that the government of "
   "the day may not like, using methods that only a few hundred people in the country can evaluate, on a budget that the "
   "same government sets.",
   "Every committee in this topic is an attempt to answer one question: who guards the credibility of official numbers? "
   "The answers offered have been an expert review every few decades, a permanent commission, a statute, a professional "
   "statistician at the top of the ministry, and standing technical committees over survey design.",
   "Read the sequence that way and the names stop being arbitrary. Bowley and Robertson in the 1930s asked for a single "
   "agency and provincial statisticians. Mahalanobis's National Income Committee in 1949 built the national accounts. "
   "The Rangarajan Commission in 2001 asked for an independent statutory commission. Each answer was partly implemented "
   "and the question came back.",
   "For the exam you need the names, the years and the chairs. For understanding, you need this: the committees recur "
   "because the problem is structural, and a body that advises without statutory power will be appointed, renamed, "
   "merged and dissolved as circumstances change — which is exactly what happened as recently as 2024."),
  aside=dict(h="The sentence to carry into the exam",
    body="Review bodies recommend; only governments implement. Every question in this topic that feels like a trick is "
         "really testing whether you know the difference."),
  ask=dict(q="Why might a government prefer an advisory committee to a statutory commission, even when it says it wants "
             "credible statistics?",
    nudge="Ask what each costs the government in control, and what each offers in credibility.")))

SC.append(dict(
  kind="theory", id="s2", title="The four landmark reviews", mins=8,
  objective="Place Bowley–Robertson, the National Income Committee, the Rangarajan Commission and the first NSC with their chairs.",
  blocks=[
   dict(t="def", h="Bowley and Robertson — the 1930s review",
     body="The colonial government asked the English economists A. L. Bowley and D. H. Robertson to devise a scheme for an "
          "economic census of India. They argued for a single agency to run both the population and the economic census, "
          "and for a statistician in every province. Most Indian sources date the report to 1934; some place the committee "
          "in 1933. Learn what it recommended — one agency, provincial statisticians — rather than betting on the year."),
   dict(t="formula", h="The National Income Committee, 1949 — Mahalanobis, Gadgil, Rao",
     body="Set up in 1949 and chaired by P. C. Mahalanobis, with D. R. Gadgil and V. K. R. V. Rao as members, to build "
          "India's national accounts. Its first report came in April 1951 and its final report in 1954. It drew on V. K. "
          "R. V. Rao's pre-independence estimates of national income. The Central Statistical Organisation (1951) grew out "
          "of this work — the committee is why the CSO exists."),
   dict(t="formula", h="The Rangarajan Commission, 2000–2001",
     body="Constituted in early 2000 under Dr C. Rangarajan, former Governor of the Reserve Bank, and reporting in "
          "September 2001. It found the statistical system badly weakened and recommended: a statutory apex body "
          "independent of government and accountable to Parliament; a professional statistician as Secretary of the "
          "ministry, the National Statistician; regular statistical audits; and reform of the Collection of Statistics Act."),
   dict(t="step", h="What came of it",
     body="The post of National Statistician was created, and the Collection of Statistics Act was replaced in 2008. The "
          "National Statistical Commission was set up — but by a government resolution of 2005, effective 2006, without "
          "the statutory backing the Commission had asked for, and the promised legislation has never been enacted. "
          "Regular statistical audits were not instituted."),
   dict(t="note", h="The first NSC chairman",
     body="The first National Statistical Commission, constituted in 2006, was chaired by Suresh Tendulkar — the same "
          "economist who chaired the 2009 poverty committee. Candidates who learn the two names separately miss that they "
          "are one person, and a matching question will exploit it."),
   dict(t="trap", h="Two Rangarajan bodies",
     body="C. Rangarajan chaired both the 2000–01 Commission on the statistical system and the 2012–14 expert group on "
          "poverty estimation. A question naming 'the Rangarajan Committee' without context is usually about poverty; one "
          "naming 'the Rangarajan Commission' is usually about the statistical system. Read the subject, not the name.")],
  flow=dict(caption="Seventy years of reviews, and what each produced",
    nodes=[
      dict(id="b", r=0, c=0, label="Bowley–Robertson, 1930s", kind="start"),
      dict(id="n", r=1, c=0, label="National Income Committee 1949 (Mahalanobis)", kind="step"),
      dict(id="c", r=2, c=0, label="CSO 1951 · national accounts", kind="note"),
      dict(id="r", r=3, c=0, label="Rangarajan Commission 2000–01", kind="step"),
      dict(id="s", r=4, c=0, label="NSC by resolution 2005, effective 2006", kind="end"),
      dict(id="a", r=3, c=2, label="Collection of Statistics Act 2008", kind="note"),
      dict(id="x", r=4, c=2, label="Statutory commission — never enacted", kind="decision")],
    edges=[dict({"from":"b","to":"n"}), dict({"from":"n","to":"c"}), dict({"from":"c","to":"r"}),
           dict({"from":"r","to":"s","label":"partly"}), dict({"from":"r","to":"a","label":"implemented"}),
           dict({"from":"r","to":"x","label":"dropped"})])))

SC.append(dict(
  kind="theory", id="s3", title="The poverty line committees, in order", mins=8,
  objective="Carry the five poverty committees with their years, chairs and the one thing each changed.",
  blocks=[
   dict(t="formula", h="Dandekar and Rath, 1971",
     body="V. M. Dandekar and N. Rath anchored the poverty line to a calorie norm — 2,250 calories a day — and asked what "
          "expenditure buys that, separately for rural and urban areas, using NSS consumption data. The calorie anchor "
          "begins here."),
   dict(t="formula", h="Alagh, 1979",
     body="The Planning Commission task force under Y. K. Alagh fixed rural and urban poverty lines from nutritional "
          "requirements and the consumption expenditure that met them, updated for inflation."),
   dict(t="formula", h="Lakdawala, 1993",
     body="D. T. Lakdawala's expert group kept the calorie-based basket but introduced state-specific poverty lines, "
          "updated using CPI for Industrial Workers and CPI for Agricultural Labourers, and dropped the practice of "
          "scaling NSS consumption to National Accounts aggregates. Its approach was adopted by the government in 1997."),
   dict(t="formula", h="Tendulkar, 2009",
     body="Suresh Tendulkar's expert group moved away from the calorie anchor altogether, used a single poverty line "
          "basket common to rural and urban areas, included private spending on health and education, changed the price "
          "adjustment, and used a mixed reference period for consumption."),
   dict(t="formula", h="Rangarajan, 2014",
     body="C. Rangarajan's expert group, appointed after the controversy over the Tendulkar line, proposed its own "
          "methodology, examined the gap between NSS consumption and the National Accounts, and raised the estimate: "
          "poverty in 2011-12 at 29.5% against Tendulkar's lower figure."),
   dict(t="trap", h="The order, and the two that are easy to swap",
     body="Dandekar–Rath 1971, Alagh 1979, Lakdawala 1993, Tendulkar 2009, Rangarajan 2014. Lakdawala and Tendulkar are "
          "the pair most often reversed; the way to hold them is that Lakdawala kept calories and Tendulkar abandoned "
          "them, and abandonment came later.")],
  flow=dict(caption="What each poverty committee changed",
    nodes=[
      dict(id="d", r=0, c=0, label="Dandekar–Rath 1971: calorie norm", kind="start"),
      dict(id="a", r=1, c=0, label="Alagh 1979: nutrition-based lines", kind="step"),
      dict(id="l", r=2, c=0, label="Lakdawala 1993: state-specific, CPI-IW / CPI-AL", kind="step"),
      dict(id="t", r=3, c=0, label="Tendulkar 2009: drops calories, adds health and education", kind="step"),
      dict(id="r", r=4, c=0, label="Rangarajan 2014: new method, 29.5% in 2011-12", kind="end")],
    edges=[dict({"from":"d","to":"a"}), dict({"from":"a","to":"l"}),
           dict({"from":"l","to":"t"}), dict({"from":"t","to":"r"})]),
  scenario=dict(
    teaser="A committee changed a definition and tens of millions of people crossed a line without moving.",
    title="What a poverty line actually decides",
    body=P(
      "When an expert group changes the basket, the calorie anchor or the price index used to update a poverty line, the "
      "measured headcount moves. Nobody's consumption has changed. What has changed is the instrument.",
      "This is not a technicality, because the number is used. Poverty estimates have informed the allocation of central "
      "funds to states, the targeting of subsidised food, and the political argument about whether a decade of growth "
      "reached the poor. A line drawn one way and another way produces two different countries on paper.",
      "The Tendulkar line drew intense criticism for being too low, which is why the Rangarajan group was appointed and "
      "why its higher estimate for the same year, 29.5% for 2011-12, mattered so much. Two committees, one dataset, two "
      "answers — both defensible, because the disagreement is about definition rather than arithmetic.",
      "For the paper, carry the sequence and what each changed. For understanding, carry this: when a statistic has "
      "consequences, the committee that defines it is doing something closer to policy than to measurement, which is "
      "exactly why the independence of statistical bodies keeps coming back as a question."),
    close="A poverty line is a decision wearing the clothes of a measurement.")))

SC.append(dict(
  kind="recall", id="s4", title="Pause and recall", mins=3,
  objective="Retrieve chairs and years before the next layer goes on.",
  intro="Say each answer aloud before looking. Names and years survive only through retrieval.",
  items=[
   dict(q="Who chaired the National Income Committee of 1949, and who were its two other members?",
     a="P. C. Mahalanobis, with D. R. Gadgil and V. K. R. V. Rao."),
   dict(q="When was the Rangarajan Commission on the statistical system constituted, and when did it report?",
     a="Constituted in early 2000; reported in September 2001."),
   dict(q="Which of the Rangarajan Commission's main recommendations was not implemented?",
     a="The statutory apex body accountable to Parliament. The NSC exists only by resolution; regular statistical audits "
       "were also not instituted."),
   dict(q="Who chaired the first National Statistical Commission in 2006?",
     a="Suresh Tendulkar — the same economist who chaired the 2009 poverty expert group."),
   dict(q="Put the poverty committees in order with their years.",
     a="Dandekar–Rath 1971, Alagh 1979, Lakdawala 1993, Tendulkar 2009, Rangarajan 2014.")]))

SC.append(dict(
  kind="completion", id="s5", title="Your turn — fill in the chairs and the years", mins=6,
  objective="Reproduce the two sequences without the page in front of you.",
  problem="Complete the record of who reviewed what, and when.",
  steps=[
   dict(say="The committee that built India's national accounts, and its chair.",
     blank=dict(prompt="Which committee, in which year, under whom?", answer="National Income Committee, 1949, Mahalanobis",
       accept=["National Income Committee 1949 Mahalanobis","National Income Committee, 1949, P C Mahalanobis",
               "National Income Committee 1949, Mahalanobis","NIC 1949 Mahalanobis"],
       hint="Two years before the office that still compiles the national accounts was created."),
     why="The CSO of 1951 is the direct output of this committee, which is why the two years sit together."),
   dict(say="The commission that reviewed the whole statistical system at the turn of the century.",
     blank=dict(prompt="Which commission, reporting in which year?", answer="Rangarajan Commission, 2001",
       accept=["Rangarajan Commission 2001","Rangarajan, 2001","Rangarajan Commission, September 2001",
               "Rangarajan commission 2001"],
       hint="Chaired by a former Governor of the Reserve Bank; set up in 2000."),
     why="Its recommendation produced the NSC — but not in the form it asked for."),
   dict(say="The form the NSC actually took, and the year.",
     blank=dict(prompt="Created by what instrument, in which year?", answer="Government resolution, 2005",
       accept=["resolution 2005","government resolution, 2005","by resolution in 2005","Resolution of 2005"],
       hint="Not an Act — that is the whole point."),
     why="Resolution rather than statute is the single most examined consequence in this module."),
   dict(say="The poverty committee that abandoned the calorie anchor, and its year.",
     blank=dict(prompt="Which committee, in which year?", answer="Tendulkar, 2009",
       accept=["Tendulkar 2009","Tendulkar committee 2009","Suresh Tendulkar, 2009","Tendulkar Committee, 2009"],
       hint="The same man chaired the first NSC three years earlier."),
     why="Lakdawala kept calories, Tendulkar dropped them: the change is how you remember which came later."),
   dict(say="The committee appointed after the controversy over that line, and its year.",
     blank=dict(prompt="Which committee, in which year?", answer="Rangarajan, 2014",
       accept=["Rangarajan 2014","Rangarajan committee 2014","Rangarajan expert group, 2014","Rangarajan, 2014"],
       hint="The same chair as the 2001 commission, a different subject entirely."),
     why="Two Rangarajan bodies, thirteen years apart, on two different questions — the commonest confusion in this topic.")],
  after="Two sequences, five names: the system reviews (Bowley–Robertson, Mahalanobis, Rangarajan, Tendulkar's NSC) and "
        "the poverty line (Dandekar–Rath, Alagh, Lakdawala, Tendulkar, Rangarajan)."))

SC.append(dict(
  kind="theory", id="s6", title="The law behind the numbers", mins=6,
  objective="State what the Collection of Statistics Act does and what the 2017 amendment changed.",
  blocks=[
   dict(t="def", h="The Collection of Statistics Act, 2008",
     body="The statute that gives legal backing to the collection of statistics in India. It replaced the Collection of "
          "Statistics Act of 1953, and its enactment was one of the Rangarajan Commission's recommendations that the "
          "government did act on. It empowers the appropriate government to collect statistics on economic, demographic, "
          "social, scientific and environmental matters, and it protects the confidentiality of the information given."),
   dict(t="formula", h="The Collection of Statistics (Amendment) Act, 2017 — three changes",
     body="First, jurisdiction: the Act now extends to the whole of India, with a proviso applying it to Jammu and Kashmir "
          "only for matters in the Union and Concurrent Lists. Second, nodal officers: a new section 3A requires the "
          "Central Government, each State Government and each Union territory administration to designate an officer to "
          "coordinate and supervise statistical activities in that government. Third, use of information: section 9(1) was "
          "amended so that information furnished may be used for statistical purposes in the prescribed manner."),
   dict(t="note", h="What the amendment did not do",
     body="It did not create a statutory National Statistical Commission, and it did not change the penalty structure of "
          "the 2008 Act. A question that attributes either to the 2017 amendment is wrong, and both are tempting."),
   dict(t="trap", h="Act versus resolution, once more",
     body="The Collection of Statistics Act is a statute passed by Parliament. The National Statistical Commission is a "
          "resolution of the executive. Both concern official statistics; only one is law. Keeping these apart answers "
          "a surprising share of this module.")]))

SC.append(dict(
  kind="theory", id="s7", title="The standing committees, and what happened to them", mins=7,
  objective="Follow the most recent chapter: SCES to SCoS to dissolution, and what replaced it.",
  blocks=[
   dict(t="step", h="SCES, December 2019",
     body="The Standing Committee on Economic Statistics was constituted in December 2019 to review the framework and "
          "results of economic surveys — the industrial, services and unincorporated enterprise surveys."),
   dict(t="step", h="Renamed SCoS, July 2023",
     body="In July 2023 its remit was widened to all surveys conducted by the National Statistics Office and it was "
          "renamed the Standing Committee on Statistics, a fourteen-member panel chaired by the economist Pronab Sen, a "
          "former Chief Statistician of India. Its work covered survey methodology, sampling design, questionnaires and "
          "tabulation plans, pilot surveys, administrative statistics and data gaps."),
   dict(t="formula", h="Dissolved, September 2024",
     body="MoSPI dissolved the SCoS in September 2024, citing an overlap with the Steering Committee for National Sample "
          "Surveys chaired by Rajeeva Laxman Karandikar. The replacement body has seventeen members and a non-member "
          "secretary, a two-year tenure, and terms of reference close to those of the SCoS, but a higher proportion of "
          "official members and fewer independent ones."),
   dict(t="note", h="Why this is examinable now",
     body="It is the most recent change in the institutional landscape, it was publicly contested, and it demonstrates the "
          "theme of the whole topic: an advisory body without statutory standing can be renamed, merged or dissolved by "
          "the executive that created it."),
   dict(t="trap", h="SCES was renamed, not abolished",
     body="SCoS is the renamed SCES, not a separate body created alongside it. And the SCoS was dissolved, not renamed "
          "again — its functions moved to a differently constituted steering committee.")],
  scenario=dict(
    teaser="In September 2024 a fourteen-member statistics panel was dissolved, and the reason given was overlap.",
    title="The dissolution of the Standing Committee on Statistics",
    body=P(
      "The Standing Committee on Statistics had been widened only fourteen months earlier, in July 2023, to cover every "
      "survey the National Statistics Office runs. It was chaired by Pronab Sen, himself a former Chief Statistician of "
      "India, and it carried a majority of non-official members — academics and independent economists advising on "
      "methodology.",
      "In September 2024 the ministry dissolved it, citing an overlap with the Steering Committee for National Sample "
      "Surveys, chaired by Rajeeva Laxman Karandikar. The new arrangement has more members, seventeen, but a higher share "
      "of them are officials and fewer are independent.",
      "Both readings of the event are defensible and a paper may expect either. The administrative reading: two bodies "
      "with overlapping terms of reference are a waste of expert time, and consolidation is ordinary housekeeping. The "
      "critical reading, pressed in Parliament and the press at the time: the panel with the largest independent "
      "membership was the one dissolved, and the balance of official to non-official voices shifted.",
      "What is not in dispute is the mechanism. The committee existed by executive order, and could therefore be ended by "
      "executive order. That is the same structural fact that the Rangarajan Commission tried to fix in 2001 by asking for "
      "a statutory commission accountable to Parliament, and that has still not been enacted."),
    close="A body created by order can be ended by order — which is why the argument for statutory standing keeps "
          "returning, twenty-five years after it was first made.")))

SC.append(dict(
  kind="guided", id="s8", title="Attribute each change to the right body", mins=6,
  objective="Apply the two sequences rather than recite them.",
  problem="Name the committee or commission responsible for each: (a) introducing state-specific poverty lines updated by "
          "CPI-IW and CPI-AL; (b) recommending a statutory apex statistical body accountable to Parliament; (c) building "
          "India's first official national accounts; (d) dropping the calorie anchor and adding private health and "
          "education spending to the poverty basket; (e) recommending a single agency for the population and economic "
          "censuses, with provincial statisticians.",
  hints=["Sort them first into two families: the poverty line, and the design of the statistical system itself.",
         "Three of the five are poverty committees; one is a system review from the 2000s; one is from the colonial period.",
         "For (a) and (d), the question is which came first — the one that kept calories or the one that dropped them."],
  solution=[
   dict(say="(a) The Lakdawala expert group of 1993, whose approach the government adopted in 1997.",
     math="State-specific lines, CPI-IW and CPI-AL → Lakdawala 1993"),
   dict(say="(b) The Rangarajan Commission of 2000–01, which reported in September 2001.",
     math="Statutory apex body → Rangarajan Commission 2001 (not implemented)"),
   dict(say="(c) The National Income Committee of 1949, chaired by Mahalanobis with Gadgil and Rao.",
     math="National accounts → National Income Committee 1949"),
   dict(say="(d) The Tendulkar expert group of 2009.",
     math="No calorie anchor, health and education included → Tendulkar 2009"),
   dict(say="(e) Bowley and Robertson, in the 1930s.",
     math="One agency, provincial statisticians → Bowley–Robertson")],
  answer="Lakdawala 1993; Rangarajan Commission 2001; National Income Committee 1949; Tendulkar 2009; Bowley–Robertson 1930s.",
  check="If you attributed (b) to the National Statistical Commission itself, you have confused the body that recommended "
        "with the body that resulted — and the resulting body is precisely the one that did not get the statutory status."))

SC.append(dict(
  kind="trapcheck", id="s9", title="Six statements — verdict on each before you look", mins=6,
  objective="Meet the wordings that turn a true fact false.",
  intro="Each is the standard fact or a single-word corruption of it.",
  items=[
   dict(claim="The Rangarajan Commission of 2001 recommended a statutory apex statistical body, and the government "
              "implemented that recommendation in full.", tf=False,
     why="It recommended a statutory body accountable to Parliament. What was created, by resolution in 2005, was a "
         "non-statutory National Statistical Commission. The statutory form was never enacted."),
   dict(claim="The National Income Committee of 1949 was chaired by P. C. Mahalanobis.", tf=True,
     why="With D. R. Gadgil and V. K. R. V. Rao as members. Its first report came in April 1951 and its final report in 1954."),
   dict(claim="The Tendulkar committee of 2009 retained the calorie norm as the basis of the poverty line.", tf=False,
     why="Tendulkar moved away from the calorie anchor, used a common poverty line basket and included private spending on "
         "health and education. It was Lakdawala, in 1993, who kept the calorie-based basket."),
   dict(claim="Suresh Tendulkar chaired both the first National Statistical Commission and a poverty estimation committee.",
     tf=True,
     why="He chaired the first NSC constituted in 2006 and the poverty expert group that reported in 2009. One person, two "
         "well-known bodies."),
   dict(claim="The Standing Committee on Statistics was renamed the Standing Committee on Economic Statistics in 2023.",
     tf=False,
     why="The direction is the other way round. The Standing Committee on Economic Statistics (2019) was renamed the "
         "Standing Committee on Statistics in July 2023, and the SCoS was dissolved in September 2024."),
   dict(claim="The Collection of Statistics (Amendment) Act, 2017 requires central, state and union territory governments "
              "to designate nodal officers for statistical activities.", tf=True,
     why="That is the new section 3A inserted by the amendment, alongside the change to the Act's jurisdiction.")]))

SC.append(dict(
  kind="guided", id="s10", title="Transfer — a case the lesson has not shown you", mins=6,
  objective="Reason from the pattern to a situation the lesson did not cover.",
  problem="Suppose the government today appointed a new expert committee to revise the poverty line using the HCES 2022-23 "
          "data. Predict three things: what the committee would have to decide, whether its conclusions would bind "
          "anyone, and what would determine whether its line is accepted.",
  hints=["Look back at what each previous committee actually had to settle. The list is short and it repeats.",
         "Ask what kind of body it would be, and recall what every such body in this topic can and cannot do.",
         "The last part is not statistical. Think about what happened to the Tendulkar line."],
  solution=[
   dict(say="What it must decide: whether to anchor on calories or on a broader basket; whether rural and urban lines come "
            "from one basket or two; which price index updates the line over time; whether private health and education "
            "spending are counted; and which reference period for consumption to use.",
     math="Basket · anchor · price index · inclusions · reference period"),
   dict(say="Whether it binds: no. It would be an expert group or committee, advising. The line becomes official only if "
            "the government accepts it, exactly as Lakdawala's approach was adopted in 1997 and Rangarajan's 2014 "
            "recommendations were not acted on in the same way.",
     math="Committee → recommends; government → adopts or shelves"),
   dict(say="What determines acceptance: partly technical scrutiny, and partly the consequences of the number. A line that "
            "raises the headcount sharply has fiscal and political costs; one that lowers it invites the charge of "
            "defining poverty away. The Tendulkar episode is the precedent.",
     math="Credibility = method + consequences")],
  answer="It would settle basket, anchor, price index, inclusions and reference period; it would only recommend; and "
         "acceptance would turn on technical scrutiny together with what the resulting number costs politically.",
  check="If your second answer was that the committee's line automatically becomes the official poverty line, re-read what "
        "happened to the Rangarajan 2014 report."))

SC.append(dict(
  kind="summary", id="s11", title="What you should now be able to do unaided", mins=3,
  objective="Compress both sequences to what survives to the exam hall.",
  body=P(
   "The system reviews: Bowley and Robertson in the 1930s (one agency, provincial statisticians); the National Income "
   "Committee of 1949 under Mahalanobis with Gadgil and Rao (national accounts, first report 1951, final 1954); the "
   "Rangarajan Commission constituted in 2000 and reporting in September 2001.",
   "What Rangarajan asked for and what arrived: a statutory body accountable to Parliament, a National Statistician, "
   "regular audits, a reformed Act. Delivered: the National Statistician, and the Collection of Statistics Act 2008. Not "
   "delivered: the statutory commission — the NSC exists by resolution of 2005, effective 2006 — and the audits.",
   "The first NSC, 2006, was chaired by Suresh Tendulkar, who also chaired the 2009 poverty expert group.",
   "The poverty line: Dandekar–Rath 1971 (2,250 calories), Alagh 1979 (nutrition-based lines), Lakdawala 1993 "
   "(state-specific lines, CPI-IW and CPI-AL, adopted 1997), Tendulkar 2009 (no calorie anchor, health and education in, "
   "mixed reference period), Rangarajan 2014 (new method, 29.5% for 2011-12).",
   "The law: Collection of Statistics Act 2008, replacing the 1953 Act; the 2017 amendment extends jurisdiction, inserts "
   "section 3A on nodal officers, and amends section 9(1) on the use of information.",
   "The recent machinery: SCES December 2019, renamed Standing Committee on Statistics in July 2023 under Pronab Sen, "
   "dissolved September 2024, functions moving to the Steering Committee for National Sample Surveys under Rajeeva "
   "Laxman Karandikar.")))

SC.append(dict(kind="quiz", id="s12", title="Mastery test", mins=12,
  objective="Ten unseen questions, drawn 3 easy / 5 moderate / 2 hard.", setId="official_t2_mastery"))

LES = dict(
  id="officialt2", moduleId="official", topicId="official-t2",
  title="Commissions and Committees of the Indian Statistical System",
  breadcrumb="Official Statistics → Indian Statistical System → Commissions and committees",
  engine="A", engineName="Institutions and official statistics — who reviewed what, and what came of it",
  estMin=sum(s["mins"] for s in SC), version="1.0", status="approved",
  provenance="Authored for this platform in October 2026. Checked against the Carnegie Endowment history of India's "
             "statistical system (Bowley–Robertson, the National Income Committee, the Rangarajan Commission's "
             "recommendations and their fate, the first NSC under Tendulkar), the text of the Collection of Statistics "
             "(Amendment) Act 2017, and the public record of the SCES/SCoS and its dissolution in September 2024. Where "
             "sources disagree on a date — the Bowley–Robertson year — the lesson says so instead of choosing.",
  objectives=[
    "Name the four landmark reviews of the Indian statistical system with their chairs and years.",
    "State what the Rangarajan Commission recommended and which recommendations were and were not implemented.",
    "Put the five poverty estimation committees in order and say what each changed.",
    "Distinguish the two Rangarajan bodies, and recognise Tendulkar in both of his roles.",
    "State what the Collection of Statistics Act 2008 does and the three changes made by the 2017 amendment.",
    "Trace the SCES to SCoS to dissolution sequence and say what it illustrates about non-statutory bodies."],
  prereq=[
    dict(id="p1", name="Committee, commission and working group",
         why="Questions quote these labels exactly, and the bodies in this topic carry all three."),
    dict(id="p2", name="Recommendation versus implementation",
         why="The Rangarajan Commission is examined on both, and the answers differ."),
    dict(id="p3", name="What a poverty line is",
         why="Five committees in this topic exist only to fix one, and each changed a specific element of it."),
    dict(id="p4", name="The National Sample Survey",
         why="Most of the standing committees here exist to advise on its design.")],
  mastery={"minQ":10, "pass":80, "draw":10, "fmtMin":{"numeric":70,"multi":70},
    "diffMix":{"easy":3,"moderate":5,"hard":2}, "noHints":True, "retestDays":7,
    "note":"Platform settings, not an NTA rule. Ten drawn from a pool of twenty at 3 easy / 5 moderate / 2 hard; a retake "
           "draws again, holding the mix and pulling back items previously got wrong."},
  refs=[
    dict(title="India's Statistical System: Past, Present, Future",
         where="Sections on the Bowley–Robertson committee, the National Income Committee and the Rangarajan Commission",
         site="Carnegie Endowment for International Peace",
         url="https://carnegieendowment.org/russia-eurasia/research/2023/06/indias-statistical-system-past-present-future",
         type="Research paper", free=True, checked="2026-10-13",
         why="The source for which Rangarajan recommendations were implemented and which were not — the distinction "
             "scene 3 is built on."),
    dict(title="The Collection of Statistics (Amendment) Act, 2017", where="Sections 1(2), 3A and 9(1)",
         site="PRS India", url="https://prsindia.org/files/bills_acts/acts_parliament/2017/the-collection-of-statistics-(amendment)-act,-2017.pdf",
         type="Act of Parliament", free=True, checked="2026-10-13",
         why="The primary text for scene 7. Read it rather than a summary: the three changes are short and precise."),
    dict(title="Dissolution of the Standing Committee on Statistics",
         where="Formation, renaming, dissolution and the replacement committee",
         site="Vajiram and Ravi",
         url="https://vajiramandravi.com/current-affairs/dissolution-of-the-standing-committee-on-statistics-scos-impact-and-future-of-indias-statistical-system/",
         type="Current affairs reference", free=True, checked="2026-10-13",
         why="The most recent chapter, for scene 8. Newer than most printed material on this topic.")],
  revision=dict(
    sheet=[
      "Bowley and Robertson, 1930s: one agency for both censuses, a statistician in every province.",
      "National Income Committee 1949: Mahalanobis (chair), Gadgil, V. K. R. V. Rao. First report April 1951, final 1954.",
      "The CSO (1951) grew out of the National Income Committee's work.",
      "Rangarajan Commission: constituted early 2000, reported September 2001.",
      "It recommended a statutory apex body accountable to Parliament, a National Statistician, regular audits, a new Act.",
      "Implemented: the National Statistician and the Collection of Statistics Act 2008. Not implemented: statutory "
      "commission and regular audits.",
      "NSC created by resolution 1 June 2005, effective 2006; first chairman Suresh Tendulkar.",
      "Poverty: Dandekar–Rath 1971 (2,250 calories), Alagh 1979, Lakdawala 1993 (state-specific, CPI-IW and CPI-AL, "
      "adopted 1997), Tendulkar 2009 (no calorie anchor), Rangarajan 2014 (29.5% in 2011-12).",
      "Collection of Statistics Act 2008 replaced the 1953 Act.",
      "The 2017 amendment: jurisdiction extended with a J&K proviso; section 3A on nodal officers; section 9(1) on use of "
      "information. It did not change penalties and did not make the NSC statutory.",
      "SCES constituted December 2019; renamed Standing Committee on Statistics July 2023 under Pronab Sen, 14 members.",
      "SCoS dissolved September 2024, citing overlap with the Steering Committee for National Sample Surveys under "
      "Rajeeva Laxman Karandikar (17 members, two-year tenure).",
      "C. Rangarajan chaired two different bodies: the 2000–01 statistical system commission and the 2012–14 poverty group.",
      "Suresh Tendulkar chaired two: the first NSC (2006) and the poverty expert group (2009)."],
    cards=[
      ["National Income Committee 1949", "Mahalanobis (chair), Gadgil, V. K. R. V. Rao"],
      ["Rangarajan Commission", "Constituted 2000, reported September 2001 — statistical system"],
      ["Rangarajan's unimplemented recommendation", "A statutory apex body accountable to Parliament"],
      ["First NSC chairman, 2006", "Suresh Tendulkar"],
      ["Dandekar–Rath 1971", "Poverty line anchored to 2,250 calories a day"],
      ["Lakdawala 1993", "State-specific lines, CPI-IW and CPI-AL, adopted 1997"],
      ["Tendulkar 2009", "Calorie anchor dropped; health and education included"],
      ["Rangarajan 2014", "New methodology; 29.5% poverty in 2011-12"],
      ["Collection of Statistics Act", "2008, replacing the 1953 Act; amended 2017"],
      ["SCoS", "SCES 2019 renamed July 2023 under Pronab Sen; dissolved September 2024"]],
    tricks=[
      dict(hook="Two Rangarajans, thirteen years apart",
           why="Commission 2001 = the statistical system. Committee 2014 = poverty. Read the subject, not the name."),
      dict(hook="Tendulkar twice: the Commission then the line",
           why="First NSC chairman in 2006, poverty expert group in 2009. One person, two famous bodies."),
      dict(hook="Lakdawala kept calories, Tendulkar dropped them",
           why="Dropping came later, so Tendulkar (2009) follows Lakdawala (1993). This settles the pair most often reversed."),
      dict(hook="Recommended is not implemented",
           why="The statutory commission was recommended in 2001 and has never been enacted. Half the traps in this topic "
               "live in that gap.")],
    shortcuts=[
      "Poverty years to carry: 1971, 1979, 1993, 2009, 2014.",
      "System review years: 1930s, 1949, 2000-01, 2005-06.",
      "If a statement says the Rangarajan Commission's statutory body was created, it is false.",
      "If a statement says SCoS was renamed SCES, the direction is reversed and it is false."],
    remember=[
      "The Rangarajan Commission asked for a statutory commission in 2001 and it has still not been enacted. That one "
      "sentence explains the NSC, the SCoS dissolution and most of this module.",
      "Tendulkar and Rangarajan each chaired two different famous bodies. Match the subject before the name."],
    traps=[
      "Treating the Rangarajan Commission (2001, statistical system) and the Rangarajan committee (2014, poverty) as one body.",
      "Saying the statutory apex body was implemented.",
      "Reversing Lakdawala and Tendulkar, or attributing the calorie anchor to Tendulkar.",
      "Saying SCoS was renamed SCES rather than the other way round.",
      "Crediting the 2017 amendment with making the NSC statutory or with changing penalties.",
      "Forgetting that the National Income Committee produced the CSO."]),
  traps=[
    "Two different Rangarajan bodies: the 2000–01 Commission on the statistical system and the 2012–14 poverty expert group.",
    "The statutory apex body the Rangarajan Commission recommended was never enacted; the NSC exists by resolution.",
    "Lakdawala (1993) kept the calorie basis; Tendulkar (2009) abandoned it.",
    "SCES (2019) was renamed SCoS (2023), not the reverse; SCoS was dissolved in September 2024.",
    "The 2017 amendment added nodal officers and changed jurisdiction; it did not change penalties or make the NSC statutory.",
    "Suresh Tendulkar chaired the first NSC in 2006 as well as the 2009 poverty group.",
    "The Bowley–Robertson year is given as 1933 in some sources and 1934 in others; learn the recommendation, not the year."],
  scenes=SC)

json.dump(LES, io.open("seed/lesson_10a2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
k = {}
for s in SC: k[s["kind"]] = k.get(s["kind"], 0) + 1
print("lesson 10A.2 written: %d scenes %s" % (len(SC), k))
print("  flow %d · scenarios %d · est %d min · refs %d" %
      (len([s for s in SC if s.get("flow")]), len([s for s in SC if s.get("scenario")]),
       LES["estMin"], len(LES["refs"])))
