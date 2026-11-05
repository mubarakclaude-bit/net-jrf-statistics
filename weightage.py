"""Per-topic exam weightage.

Module marks are real (the paper structure). The split WITHIN a module is an
editorial weight, 3 = core / 2 = important / 1 = supporting, and the expected
number of questions is derived arithmetically from the two:

    questions(topic) = (module marks / 2) * w(topic) / sum of w in the module

Only `inference` has been reviewed topic by topic so far; every other module is
left at an even split and flagged as such, so the UI never implies a judgement
that has not been made. The admin can revise any of it.
"""
import json, datetime

REVIEWED = {
 "inference": {
  "inference-t1":3,  "inference-t2":3,  "inference-t3":3,  "inference-t4":3,
  "inference-t5":2,  "inference-t6":3,  "inference-t7":2,  "inference-t8":1,
  "inference-t9":3,  "inference-t10":2, "inference-t11":1, "inference-t12":2,
  "inference-t13":2, "inference-t14":2, "inference-t15":1,
 },
}
# What the editorial weight was based on, shown in the app next to the number.
BASIS = {
 "inference":"Reviewed against the June 2026 paper, where the six estimation items sat on "
             "sufficiency, Rao–Blackwell and the MLE, and against the syllabus depth each topic is set at.",
}

C=json.load(open("seed/catalog.json",encoding="utf-8"))
for m in C["modules"]:
    w=REVIEWED.get(m["id"])
    reviewed=w is not None
    ws={t["id"]:(w.get(t["id"],2) if reviewed else 2) for t in m["topics"]}
    tot=sum(ws.values()) or 1
    qs=(m.get("marks",0)/2.0)
    m["wReviewed"]=reviewed
    if reviewed: m["wBasis"]=BASIS[m["id"]]
    for t in m["topics"]:
        t["imp"]=ws[t["id"]]
        t["qs"]=round(qs*ws[t["id"]]/tot,2)
        t["marks"]=round(2*t["qs"],1)
C["updated"]=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
json.dump(C,open("seed/catalog.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)

inf=[m for m in C["modules"] if m["id"]=="inference"][0]
print("inference — %d marks over %d topics"%(inf["marks"],len(inf["topics"])))
for t in inf["topics"]:
    print("  %-14s imp=%d  %4.2f q  %4.1f marks  %s"%(t["id"],t["imp"],t["qs"],t["marks"],t["name"][:46]))
print("  check: %.1f marks, %.2f questions"%(sum(t["marks"] for t in inf["topics"]),sum(t["qs"] for t in inf["topics"])))
print()
print("unreviewed modules left at an even split:",
      ", ".join(m["id"] for m in C["modules"] if not m["wReviewed"]))
