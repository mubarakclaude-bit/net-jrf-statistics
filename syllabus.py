#!/usr/bin/env python3
# Build the official-syllabus order document from the UGC NET Statistics (107)
# syllabus PDF. The official paper has 10 units; the catalog splits some of them
# into two modules (Unit III is sampling + design, Unit X is official statistics +
# R programming) and merges Units IV and V into one inference module, so the map
# records both: the sort key that orders the learning path, and the unit each
# module belongs to, for display.
import json, io, datetime

# sort key -> the position a module takes in the official sequence.
# Fractions keep two modules of one unit adjacent and in the right order.
UNITS = [
  ("I",    "Probability and Distributions",                        [("probability", 1)]),
  ("II",   "Real Analysis and Matrix Algebra",                      [("maths", 2)]),
  ("III",  "Sampling Methods and Design of Experiments",            [("sampling", 3), ("design", 3.5)]),
  ("IV",   "Estimation Theory",                                     [("inference", 4)]),
  ("V",    "Testing of Hypotheses",                                 [("nonparam", 5)]),
  ("VI",   "Linear Estimation, Regression Analysis and Econometrics",[("regression", 6)]),
  ("VII",  "Time Series",                                           [("timeseries", 7)]),
  ("VIII", "Multivariate Analysis",                                 [("multivariate", 8)]),
  ("IX",   "Stochastic Processes",                                  [("stochastic", 9)]),
  ("X",    "Indian Statistical System and Research Methodology",    [("official", 10), ("rprog", 10.5)]),
]
# Paper 1 is a separate, general syllabus; this file does not cover it. The order
# below is the standard Paper 1 unit sequence, kept after the subject modules.
P1 = [("p1-teaching", 11), ("p1-research", 12), ("p1-communication", 13),
      ("p1-mathreason", 14), ("p1-logical", 15), ("p1-di", 16), ("p1-ict", 17),
      ("p1-environment", 18), ("p1-highered", 19)]
P1UNIT = {"p1-teaching":"P1-I","p1-research":"P1-II","p1-communication":"P1-IV",
          "p1-mathreason":"P1-V","p1-logical":"P1-VI","p1-di":"P1-VII","p1-ict":"P1-VIII",
          "p1-environment":"P1-IX","p1-highered":"P1-X"}

order, unit = {}, {}
for roman, title, mods in UNITS:
    for mid, k in mods:
        order[mid] = k
        unit[mid] = {"no": roman, "title": title}
for mid, k in P1:
    order[mid] = k
    unit[mid] = {"no": P1UNIT[mid], "title": "Paper 1 — general paper"}

doc = {
  "cycle": "2026",
  "source": "UGC NET Bureau, NET Syllabus, Subject: Statistics, Code 107 — 10 units (official PDF).",
  "note": "Paper 2 modules are ordered by the official unit sequence. The catalog splits Unit III "
          "into sampling and design, and Unit X into official statistics and R programming, so two "
          "modules can share one unit. Paper 1 follows the standard general-paper unit order, which "
          "this subject syllabus does not cover.",
  "order": order,
  "units": unit,
  "updated": datetime.date.today().isoformat(),
}
json.dump(doc, io.open("seed/meta_syllabus.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

cat = json.load(io.open("seed/catalog.json", encoding="utf-8"))
known = {m["id"] for m in cat["modules"]}
print("modules in the catalog :", len(known))
print("modules given an order :", len(order))
print("ordered but not in the catalog:", sorted(set(order) - known) or "none")
print("in the catalog with no order :", sorted(known - set(order)) or "none")
print()
for mid, k in sorted(order.items(), key=lambda x: x[1]):
    m = [x for x in cat["modules"] if x["id"] == mid]
    if m and m[0]["paper"] == 2:
        print("  %-5s Unit %-5s %-34s %2d topics, %2d marks" %
              (k, unit[mid]["no"], m[0]["name"][:34], len(m[0].get("topics", [])), m[0].get("marks", 0)))
