# Adds to the Sufficiency lesson: a decision flowchart, memory aids, and a real-world
# case the learner can drill into and come back from.
import json
P="/home/claude/w1/seed/lesson_t1.json"
L=json.load(open(P,encoding="utf-8"))
S={x["id"]:x for x in L["scenes"]}

# --- the flowchart: how to actually find a sufficient statistic in an exam ---
FLOW={
 "title":"Finding a sufficient statistic — the route the exam expects",
 "alt":"Flow chart from the density to a minimal sufficient statistic",
 "nodes":[
  {"id":"a","r":0,"c":1,"label":"Write the joint density of the whole sample","kind":"start"},
  {"id":"b","r":1,"c":1,"label":"Does the support depend on θ?","kind":"decision"},
  {"id":"c","r":2,"c":0,"label":"Keep the indicator — it belongs in the θ-part g","kind":"note"},
  {"id":"d","r":2,"c":2,"label":"Is it an exponential family?","kind":"decision"},
  {"id":"e","r":3,"c":2,"label":"Read T straight off: the natural statistic","kind":"step"},
  {"id":"f","r":3,"c":0,"label":"Factorise f = g(T;θ)·h(x) by hand","kind":"step"},
  {"id":"g","r":4,"c":1,"label":"Check h(x) really has no θ in it","kind":"decision"},
  {"id":"h","r":5,"c":1,"label":"T is sufficient","kind":"step"},
  {"id":"i","r":6,"c":1,"label":"Ratio f(x;θ)/f(y;θ) free of θ ⇔ T(x)=T(y)?","kind":"decision"},
  {"id":"j","r":7,"c":1,"label":"T is MINIMAL sufficient","kind":"end"}],
 "edges":[
  {"from":"a","to":"b"},
  {"from":"b","to":"c","label":"yes"},
  {"from":"b","to":"d","label":"no"},
  {"from":"d","to":"e","label":"yes"},
  {"from":"d","to":"f","label":"no"},
  {"from":"c","to":"f"},
  {"from":"f","to":"g"},
  {"from":"e","to":"g"},
  {"from":"g","to":"h","label":"yes"},
  {"from":"h","to":"i"},
  {"from":"i","to":"j","label":"yes"}],
 "note":"The two decision diamonds are where marks are lost. A moving support means the indicator carries θ and must go into g; and sufficiency alone is not minimality — the ratio test is a separate step."
}
S["s3"]["flow"]=FLOW   # the theory scene that states the factorisation theorem

# --- a real-world case, drillable from the intuition scene ---
S["s1"]["scenario"]={
 "teaser":"A turbine maker keeps 40,000 failure times and wants to throw almost all of them away.",
 "title":"Throwing away 40,000 numbers and losing nothing",
 "body":[
  "A manufacturer runs accelerated life tests on a bearing. Forty thousand units are run to failure and each failure time is recorded. The reliability team models the lifetimes as exponential with unknown rate λ, and wants a monthly report that the plants can act on.",
  "Shipping forty thousand numbers to every plant is useless, so the question is what to send. Intuition says send the mean. Sufficiency says something much stronger: send Σxᵢ — one number — and you have sent everything the data contain about λ. Not approximately everything. Everything.",
  "The factorisation makes it plain. The joint density is λⁿ e^(−λΣxᵢ), which already depends on the data only through Σxᵢ, with h(x) = 1. Two plants with completely different individual failure times but the same total have, as far as λ is concerned, run the same experiment.",
  "This is why sufficiency matters outside exams. It tells an engineer exactly which summary may be stored and which must not be discarded. Store the total and the count and every future inference about λ is unaffected. Store only the median and you have thrown information away, because the median is not sufficient here."],
 "q":"The team proposes storing the sample mean and the sample variance instead of the total. For estimating λ, have they lost anything?",
 "answer":"No, provided they also keep n: the mean and n give back Σxᵢ exactly, and a one-to-one function of a sufficient statistic is itself sufficient. The variance is simply redundant here — it adds nothing about λ, though it would matter if the exponential model itself were in doubt. That last point is the practical use of an ancillary statistic: it carries no information about the parameter, which makes it free to use for checking the model.",
 "link":"The same reasoning is why a factory SCADA historian stores aggregates rather than raw traces — and why choosing the wrong aggregate is an irreversible loss."
}

# --- memory aids for the right-hand panel ---
L["revision"]["tricks"]=[
 {"hook":"g T h — 'God Takes Half'","why":"f = g(T;θ)·h(x). The g half has θ and sees the data only through T; the h half is free of θ."},
 {"hook":"Support moves → indicator rides with θ","why":"If the range depends on θ, the indicator goes INSIDE g. Forgetting this is the single commonest lost mark."},
 {"hook":"Same ratio, same T","why":"Minimality: f(x;θ)/f(y;θ) free of θ exactly when T(x) = T(y)."},
 {"hook":"Curved means fat","why":"A curved exponential family has more natural statistics than parameters — sufficient, but not complete."}]
L["revision"]["shortcuts"]=[
 "Exponential family? Then (Σt₁(xᵢ), …, Σtₖ(xᵢ)) is sufficient. No factorisation needed.",
 "One unknown parameter usually means one coordinate in T — but U(θ, θ+1) needs two.",
 "Any one-to-one function of a sufficient statistic is sufficient: x̄ and Σxᵢ are interchangeable.",
 "The whole sample is always sufficient. If your answer is the whole sample, you have not finished."]
L["revision"]["remember"]=[
 "Sufficient ≠ minimal ≠ complete. The exam tests the boundaries between them.",
 "h(x) must contain no θ whatsoever — check it explicitly before claiming sufficiency."]

json.dump(L,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("t1 enriched:")
print("  flow chart on scene 3:", len(FLOW["nodes"]), "nodes,", len(FLOW["edges"]), "edges")
print("  scenario on scene 1  :", S["s1"]["scenario"]["title"])
print("  memory aids          :", len(L["revision"]["tricks"]), "mnemonics,",
      len(L["revision"]["shortcuts"]), "shortcuts,", len(L["revision"]["remember"]), "must-remember")
