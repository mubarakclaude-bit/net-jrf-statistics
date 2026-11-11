#!/usr/bin/env python3
import json
from collections import Counter
# Disease example: prevalence .01, sensitivity .95, specificity .90.
p_pos=.95*.01+.10*.99
ppv=.95*.01/p_pos
assert abs(p_pos-.1085)<1e-12 and abs(ppv-.08755760368663594)<1e-12
# Machine posterior.
p_def=.02*.60+.05*.40
post=.05*.40/p_def
assert abs(p_def-.032)<1e-12 and abs(post-.625)<1e-12
# Prevalence .02, sensitivity .90, specificity .95.
p_pos2=.90*.02+.05*.98
ppv2=.90*.02/p_pos2
p_neg2=.10*.02+.95*.98
npv2=.95*.98/p_neg2
assert abs(p_pos2-.067)<1e-12 and abs(ppv2-.26865671641791045)<1e-12
assert abs(p_neg2-.933)<1e-12 and abs(npv2-.9978563772775991)<1e-12
with open("seed/probability_t12_mastery.json",encoding="utf-8") as f:q=json.load(f)["items"]
assert len(q)==20 and Counter(x["diff"] for x in q)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["answer"] for x in q)=={"A":5,"B":5,"C":5,"D":5}
assert sum(x["format"]=="numeric" for x in q)>=4 and sum(x["format"]=="multi" for x in q)>=2
for x in q:
 assert len(x["options"])==4
 if x["format"]=="numeric":assert x.get("check")
 if x["format"]=="multi":assert len(x["statements"])==4 and len(x["verdicts"])==4
print("Probability T12 exact anchors and mastery pool: PASS")
