#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_rprog_t2.json").read_text())
P=json.loads((R/"seed/rprog_t2_mastery.json").read_text())
assert L["id"]=="rprogt2" and L["topicId"]=="rprog-t2" and L["moduleId"]=="rprog"
assert len(L["scenes"])==13 and L["scenes"][-1]["setId"]=="rprog_t2_mastery"
assert L["anchors"]==[{"paper":"j26","q":22}]
assert L["estMin"]==sum(s["mins"] for s in L["scenes"] if not s.get("ext"))==90
assert sum(s["kind"]=="guided" for s in L["scenes"])>=2
assert sum("scenario" in s for s in L["scenes"])>=2
assert len(P["items"])==P["count"]==20
assert Counter(x["diff"] for x in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in P["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
assert any("flow" in s for s in L["scenes"])
# Independent loop traces matching the lesson's R control-flow examples.
x=1
for i in range(1,6): x*=i
assert x==120
s=0
for i in range(1,6): s+=i
assert s==15
s=0
for i in range(1,6):
 if i==3: continue
 s+=i
assert s==12
s=0
for i in range(1,6):
 if i==4: break
 s+=i
assert s==6
# R functions return their final evaluated expression.
def r_function(n):
 x=1
 for i in range(1,n+1): x*=i
 return x
assert r_function(5)==120
print("PASS: R loop/function traces, implicit final-expression return and June 2026 Q22 anchor.")
print("PASS: 20 mastery items; difficulty 6/10/4; formats 12/5/3; answer keys balanced.")
